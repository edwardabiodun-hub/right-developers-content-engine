from dataclasses import dataclass, field


REQUEST_INFO_ROUTE = "/request-info"
STAGE_CEILINGS = {"ATTENTION": 0, "EDUCATION": 1, "PROOF": 2, "EVALUATION": 3, "CONVERSION": 4}


@dataclass
class ValidationResult:
    hard_failures: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def validate_cta(stage: str, tier: int, route: str | None) -> ValidationResult:
    result = ValidationResult()
    ceiling = STAGE_CEILINGS.get(stage)
    if ceiling is None:
        result.hard_failures.append("UNKNOWN_FUNNEL_STAGE")
        return result
    if tier > ceiling:
        result.hard_failures.append("CTA_CEILING_EXCEEDED")
    if tier >= 4 and route != REQUEST_INFO_ROUTE:
        result.hard_failures.append("UNAPPROVED_COMMERCIAL_ROUTE")
    if tier < 4 and route is not None and route != REQUEST_INFO_ROUTE:
        result.hard_failures.append("UNAPPROVED_COMMERCIAL_ROUTE")
    return result
