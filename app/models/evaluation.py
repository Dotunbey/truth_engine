from dataclasses import dataclass
from typing import Dict, List


@dataclass
class RuleResult:
    rule_id: str
    passed: bool
    critical: bool
    weight: int
    reason: str


@dataclass
class EvaluationResult:
    verdict: str
    alignment_score: float
    explanations: List[RuleResult]
