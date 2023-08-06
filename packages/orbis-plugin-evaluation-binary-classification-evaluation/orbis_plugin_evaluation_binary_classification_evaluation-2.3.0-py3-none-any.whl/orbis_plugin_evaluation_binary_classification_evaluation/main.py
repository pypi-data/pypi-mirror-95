# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger(__name__)


class Main(object):

    def __init__(self, rucksack):
        super(Main, self).__init__()
        self.rucksack = rucksack
        self.file_name = rucksack.open['config']['file_name']
        self.scorer_condition = rucksack.open['config']['scoring']['condition']
        self.computed = rucksack.open['data']['computed']
        self.gold = rucksack.open['data']['gold']
        self.ignore_empty = rucksack.open['config']['scoring']['ignore_empty']
        self.entities = rucksack.open['config']['scoring'].get('entities', [])

        if len(self.entities) <= 0:
            self.entities = self.get_all_entity_types()

        self.scorer = rucksack.plugins["scoring"]
        self.nel_scorer = self.scorer()
        self.metrics = rucksack.plugins["metrics"]
        self.bc_metrics = self.metrics()

    def get_all_entity_types(self):
        entity_types = set()
        for item_key, item in self.gold.items():

            for entity in item:
                entity_type = entity.get('entity_type', False)
                if entity_type:
                    entity_types.add(entity_type)

        for item_key, item in self.computed.items():
            for entity in item:
                entity_type = entity.get('entity_type', False)
                if entity_type:
                    entity_types.add(entity_type)

        return list(entity_types)

    def run(self):
        self.rucksack.open["results"].update(self.binary_classification())
        return self.rucksack

    def _calculate_metrics(self, confusion_matrix, item_sum, item, current_gold):
        if len(item) == 0 and len(current_gold) == 0:
            # Handling corner case when no element in gold document and no element returned.
            # Handled the same way in gerbil:
            # https://github.com/dice-group/gerbil/wiki/Precision,-Recall-and-F1-measure#dividing-by-0
            precision = 1
            recall = 1
            f1_score = 1
        else:
            precision = self.bc_metrics.get_precision(confusion_matrix["tp_sum"], confusion_matrix["fp_sum"])
            recall = self.bc_metrics.get_recall(confusion_matrix["tp_sum"], item_sum)
            f1_score = self.bc_metrics.get_f1_score(precision, recall)
        return precision, recall, f1_score

    def binary_classification(self):
        results = {
            "items": {},
            "summary": {}
        }
        micro = {
            "tp_sum": 0,
            "fp_sum": 0,
            "fn_sum": 0,
            "item_sum": 0
        }
        macro = {
            "precision": 0,
            "recall": 0,
            "f1_score": 0,
            "item_sum": 0
        }
        stats = {
            "has_score": 0,
            "no_score": 0,
            "empty_responses": 0
        }
        logger.info("Starting Evaluation Calculation for {}".format(self.file_name))
        for item_key, item in self.computed.items():
            # logger.debug(f"Evaluating item: {item}")
            if len(item) <= 0:
                stats["empty_responses"] += 1
                if self.ignore_empty:
                    continue

            # logger.error(f"\n\n77: {self.gold}\n\n")
            current_gold = [entity for entity in self.gold.get(item_key, []) if entity["entity_type"] in self.entities]
            current_computed = [entity for entity in item if entity["entity_type"] in self.entities]

            # Scorer
            confusion_matrix = self.nel_scorer.run(current_computed, current_gold, self.scorer_condition)
            # logger.debug("Gold Entities: {}".format(current_gold))
            # multiline_logging(app, "Gold Entities: {}".format(current_gold))
            # logger.debug("Computed Entities: {}".format(current_computed))
            # multiline_logging(app, "Computed Entities: {}".format(current_computed))
            item_sum = len(current_gold)
            micro["tp_sum"] += confusion_matrix["tp_sum"]
            micro["fp_sum"] += confusion_matrix["fp_sum"]
            micro["fn_sum"] += confusion_matrix["fn_sum"]
            micro["item_sum"] += item_sum
            # Metrics
            precision, recall, f1_score = self._calculate_metrics(confusion_matrix, item_sum, item, current_gold)
            macro["precision"] += precision
            macro["recall"] += recall
            macro["f1_score"] += f1_score
            macro["item_sum"] += 1

            entities_string = ", ".join(self.entities)

            results["items"][item_key] = {
                "binary_classification": {
                    "confusion_matrix": confusion_matrix,
                    "item_sum": item_sum,
                    "precision": precision,
                    "recall": recall,
                    "f1_score": f1_score,
                    "entities": entities_string
                }
            }

            if f1_score > 0 or precision > 0 or recall > 0:
                stats["has_score"] += 1
            else:
                stats["no_score"] += 1
        # Metrics
        micro["precision"] = self.bc_metrics.get_precision(micro["tp_sum"], micro["fp_sum"])
        micro["recall"] = self.bc_metrics.get_recall(micro["tp_sum"], micro["item_sum"])
        micro["f1_score"] = self.bc_metrics.get_f1_score(micro["precision"], micro["recall"])
        if macro["item_sum"] > 0:
            macro["precision"] = macro["precision"] / macro["item_sum"]
            macro["recall"] = macro["recall"] / macro["item_sum"]
            macro["f1_score"] = macro["f1_score"] / macro["item_sum"]
        else:
            macro["precision"] = 0
            macro["recall"] = 0
            macro["f1_score"] = 0
        results["summary"]['binary_classification'] = {
            "has_score": stats["has_score"],
            "no_score": stats["no_score"],
            "empty_responses": stats["empty_responses"],
            "entities": self.entities,

            "total_tp": micro["tp_sum"],
            "total_fp": micro["fp_sum"],
            "total_fn": micro["fn_sum"],
            "total_item_sum": micro["item_sum"],
            "micro": {
                "precision": micro["precision"],
                "recall": micro["recall"],
                "f1_score": micro["f1_score"]
            },
            "macro": {
                "precision": macro["precision"],
                "recall": macro["recall"],
                "f1_score": macro["f1_score"]
            }
        }
        logger.debug(f'Running nel_evaluator for {self.file_name}')
        logger.debug(f'Micro precision = {micro["precision"]}')
        logger.debug(f'Micro recall = {micro["recall"]}')
        logger.debug(f'Micro f1_score = {micro["f1_score"]}')
        logger.debug(f'Macro precision = {macro["precision"]}')
        logger.debug(f'Macro recall = {macro["recall"]}')
        logger.debug(f'Macro f1_score = {macro["f1_score"]}')
        return results
