from dataclasses import dataclass

from .campaigns import CampaignManifest
from .claims import Claim, ClaimStatus
from .history import History
from .validation import ContentUnit, ValidationReport, validate_content
from .registries import DomainRegistries


@dataclass(frozen=True)
class ContentPackage:
    content_id: str
    thesis: str
    cta_route: str
    human_review_required: bool
    validation_report: ValidationReport


def generate_content_package(manifest: CampaignManifest, history: History, registries: DomainRegistries) -> ContentPackage:
    thesis = "A mineral inquiry becomes commercially useful when specification, quantity, and destination are clear before terms are discussed."
    unit = ContentUnit(
        content_id=f"{manifest.campaign_id}-day-01",
        mineral_id=manifest.mineral_id,
        audience_id=manifest.target_audience,
        pillar_id="BUYER_READINESS",
        concept_ids=["TRADE_READINESS", "INQUIRY_COMPLETENESS"],
        franchise_id=manifest.franchise_id,
        stage=manifest.stage,
        claims=[Claim("Illustrative example: a buyer may need specification, quantity, and destination before terms", ClaimStatus.ILLUSTRATIVE, None, manifest.mineral_id)],
        cta_tier=1,
        cta_route="/request-info",
        body=thesis,
        platform=manifest.platforms[0],
    )
    report = validate_content(unit, registries)
    return ContentPackage(unit.content_id, thesis, "/request-info", True, report)
