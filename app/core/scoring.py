from typing import List
from app.models.rule import Rule


def calculate_alignment(passed: List[Rule], total: List[Rule]) -> float:
    total_weight = sum(rule.weight for rule in total)
    earned_weight = sum(rule.weight for rule in passed)
    if total_weight == 0:
        return 0.0
    return round((earned_weight / total_weight) * 100, 2)
