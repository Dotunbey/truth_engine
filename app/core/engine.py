# app/core/engine.py

from typing import Dict, List
from app.models.edge import Edge
from app.models.evaluation import EvaluationResult, RuleResult
from app.core.explainability import explain

class TruthEngine:
    def evaluate(self, edge: Edge, inputs: Dict[str, bool]) -> EvaluationResult:
        explanations: List[RuleResult] = []
        
        total_possible_points = 0
        earned_points = 0
        
        critical_danger = False 
        compulsory_failed = False 

        # 1. CHECK INVALIDATION (Warning Lights)
        for rule in edge.invalidation_rules:
            passed = rule.evaluate(inputs.get(rule.rule_id, False))
            explanations.append(explain(rule.rule_id, passed, True, 0))
            if not passed:
                critical_danger = True

        # 2. CHECK COMPULSORY (The Anchor)
        for rule in edge.compulsory_rules:
            passed = rule.evaluate(inputs.get(rule.rule_id, False))
            
            total_possible_points += rule.weight
            if passed:
                earned_points += rule.weight
            else:
                compulsory_failed = True # FLAG THE FAILURE
            
            explanations.append(explain(rule.rule_id, passed, False, rule.weight))

        # 3. CHECK WEIGHTED (The Boosters)
        for rule in edge.weighted_rules:
            passed = rule.evaluate(inputs.get(rule.rule_id, False))
            
            total_possible_points += rule.weight
            if passed:
                earned_points += rule.weight
            
            explanations.append(explain(rule.rule_id, passed, False, rule.weight))

        # 4. CALCULATE RAW SCORE
        if total_possible_points == 0:
            raw_score = 0.0
        else:
            raw_score = (earned_points / total_possible_points) * 100

        # --- THE FIX: INTEGRITY PENALTY ---
        final_score = raw_score
        
        if compulsory_failed:
            # DEDUCT 25% from the score directly.
            # 90% becomes 65%. 60% becomes 35%.
            final_score = max(0.0, raw_score - 25.0)
            
            # Add a note to explanations so the user knows why score dropped
            explanations.append(RuleResult(
                rule_id="INTEGRITY_PENALTY",
                passed=False,
                critical=True,
                weight=-25,
                reason="PENALTY: Compulsory Rule Violated (-25%)"
            ))

        # 5. DETERMINE VERDICT
        final_score = round(final_score, 2)

        if critical_danger:
            verdict = "CRITICAL_WARNING"
        elif final_score >= 75.0:
            verdict = "HIGH_CONVICTION"
        elif final_score >= 40.0:
            verdict = "WEAK_ALIGNMENT"
        else:
            verdict = "LOW_PROBABILITY"

        return EvaluationResult(
            verdict=verdict,
            alignment_score=final_score,
            explanations=explanations
        )
