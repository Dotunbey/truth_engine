from typing import Dict
from app.models.edge import Edge
from app.models.evaluation import EvaluationResult
from app.core.scoring import calculate_alignment
from app.core.explainability import explain


class TruthEngine:
    def evaluate(self, edge: Edge, inputs: Dict[str, bool]) -> EvaluationResult:
        explanations = []

        for rule in edge.invalidation_rules:
            passed = rule.evaluate(inputs.get(rule.rule_id, False))
            explanations.append(explain(rule.rule_id, passed, True, 0))
            if not passed:
                return EvaluationResult("INVALID", 0.0, explanations)

        for rule in edge.compulsory_rules:
            passed = rule.evaluate(inputs.get(rule.rule_id, False))
            explanations.append(explain(rule.rule_id, passed, False, 0))
            if not passed:
                return EvaluationResult("INVALID", 0.0, explanations)

        passed_weighted = []
        for rule in edge.weighted_rules:
            passed = rule.evaluate(inputs.get(rule.rule_id, False))
            explanations.append(explain(rule.rule_id, passed, False, rule.weight))
            if passed:
                passed_weighted.append(rule)

        score = calculate_alignment(passed_weighted, edge.weighted_rules)
        verdict = "VALID" if score >= 40 else "INVALID"

        return EvaluationResult(verdict, score, explanations)
