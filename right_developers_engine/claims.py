from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .errors import ConfigurationError
from .registries import DomainRegistries


class ClaimStatus(StrEnum):
    VERIFIED = "VERIFIED"
    SOURCE_REQUIRED = "SOURCE_REQUIRED"
    ILLUSTRATIVE = "ILLUSTRATIVE"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class Claim:
    text: str
    status: ClaimStatus
    source: str | None
    mineral_id: str | None


@dataclass
class ValidationReport:
    hard_failures: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def _commercial_language(text: str) -> bool:
    lowered = text.lower()
    return "$" in lowered or "price" in lowered or "available" in lowered or "per tonne" in lowered


def validate_claim(claim: Claim, registries: DomainRegistries) -> ValidationReport:
    report = ValidationReport()
    if claim.mineral_id is not None:
        mineral = registries.mineral(claim.mineral_id)
        if mineral["review_profile"] == "elevated" and claim.status == ClaimStatus.SOURCE_REQUIRED and not claim.source:
            report.warnings.append("SOURCE_REQUIRED")
    if claim.status == ClaimStatus.UNKNOWN and _commercial_language(claim.text):
        report.hard_failures.append("UNSUPPORTED_COMMERCIAL_CLAIM")
    elif claim.status == ClaimStatus.SOURCE_REQUIRED and not claim.source:
        report.warnings.append("SOURCE_REQUIRED")
    elif claim.status == ClaimStatus.ILLUSTRATIVE and not claim.text.lower().startswith(("illustrative", "example", "hypothetical")):
        report.hard_failures.append("UNLABELED_ILLUSTRATION")
    return report


def validate_claims(claims: list[Claim], registries: DomainRegistries) -> ValidationReport:
    result = ValidationReport()
    for claim in claims:
        current = validate_claim(claim, registries)
        result.hard_failures.extend(current.hard_failures)
        result.warnings.extend(current.warnings)
    return result
