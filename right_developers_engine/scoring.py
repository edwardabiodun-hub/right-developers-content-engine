from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .validation import ContentUnit


@dataclass(frozen=True)
class ContentScore:
    aggregate: float
    dimensions: dict[str, float]


def score_content(unit: ContentUnit) -> ContentScore:
    body = unit.body.lower()
    dimensions = {
        "trade_readiness": 5.0 if any(term in body for term in ("inquiry", "specification", "terms", "readiness")) else 1.0,
        "buyer_specificity": 4.0 if unit.audience_id else 0.0,
        "mechanism": 4.0 if any(term in body for term in ("because", "before", "quantity", "destination")) else 1.0,
        "evidence": 4.0 if unit.claims else 0.0,
        "mineral_accuracy": 4.0 if unit.mineral_id else 0.0,
        "inquiry_quality": 4.0 if any(term in body for term in ("quantity", "destination", "specification")) else 1.0,
        "differentiation": 4.0 if unit.concept_ids else 1.0,
        "cta_fit": 4.0,
        "canonical_consistency": 4.0 if unit.concept_ids else 0.0,
        "generic_language": 1.0 if not any(phrase in body for phrase in ("optimize", "unlock", "drive transformation")) else 4.0,
        "repetition": 3.0,
    }
    aggregate = sum(dimensions.values()) / len(dimensions)
    return ContentScore(round(aggregate, 2), dimensions)
