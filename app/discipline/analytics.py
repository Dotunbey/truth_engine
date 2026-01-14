from typing import List
from app.models.evaluation import EvaluationResult


def edge_adherence(results: List[EvaluationResult]) -> float:
    if not results:
        return 0.0
    valid = sum(1 for r in results if r.verdict == "VALID")
    return round((valid / len(results)) * 100, 2)
