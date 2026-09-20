from dataclasses import dataclass, field

from .claims import Claim, validate_claims
from .cta import validate_cta
from .registries import DomainRegistries
from .scoring import ContentScore, score_content


@dataclass(frozen=True)
class ContentUnit:
    content_id: str
    mineral_id: str
    audience_id: str
    pillar_id: str
    concept_ids: list[str]
    franchise_id: str
    stage: str
    claims: list[Claim]
    cta_tier: int
    cta_route: str | None
    body: str
    platform: str


@dataclass
class ValidationReport:
    result: str
    score: ContentScore
    hard_failures: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    generic_language_flags: list[str] = field(default_factory=list)
    human_review_required: bool = True


GENERIC_PHRASES = ("optimize", "unlock", "drive transformation", "improve efficiency", "scale your business")


def validate_content(unit: ContentUnit, registries: DomainRegistries) -> ValidationReport:
    failures: list[str] = []
    warnings: list[str] = []
    if unit.mineral_id not in {item["id"] for item in registries.minerals["minerals"]}:
        failures.append("UNKNOWN_MINERAL")
    if unit.audience_id not in {item["id"] for item in registries.audiences["audiences"]}:
        failures.append("UNKNOWN_AUDIENCE")
    if unit.pillar_id not in {item["id"] for item in registries.pillars["pillars"]}:
        failures.append("UNKNOWN_CONTENT_PILLAR")
    for concept_id in unit.concept_ids:
        if concept_id not in registries.concept_ids():
            failures.append("UNKNOWN_CANONICAL_CONCEPT")
    claim_report = validate_claims(unit.claims, registries)
    failures.extend(claim_report.hard_failures)
    warnings.extend(claim_report.warnings)
    cta_report = validate_cta(unit.stage, unit.cta_tier, unit.cta_route)
    failures.extend(cta_report.hard_failures)
    warnings.extend(cta_report.warnings)
    lowered = unit.body.lower()
    generic_flags = [phrase for phrase in GENERIC_PHRASES if phrase in lowered]
    score = score_content(unit)
    if generic_flags:
        warnings.append("GENERIC_LANGUAGE")
    if failures:
        result = "REJECT"
    elif score.aggregate < 3.5 or generic_flags:
        result = "WARN"
    else:
        result = "PASS"
    return ValidationReport(result, score, failures, warnings, generic_flags)
