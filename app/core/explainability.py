from app.models.evaluation import RuleResult


def explain(rule_id: str, passed: bool, critical: bool, weight: int) -> RuleResult:
    reason = (
        f"Rule {rule_id} satisfied"
        if passed
        else f"Rule {rule_id} violated"
    )
    return RuleResult(
        rule_id=rule_id,
        passed=passed,
        critical=critical,
        weight=weight,
        reason=reason,
    )
