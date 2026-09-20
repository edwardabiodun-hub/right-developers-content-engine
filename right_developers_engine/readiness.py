from dataclasses import dataclass, field


READINESS_FIELDS = (
    "mineral", "specification", "quantity", "destination", "inspection",
    "documentation", "payment_pathway", "buyer_authority", "intended_price",
    "technical_requirements",
)


@dataclass(frozen=True)
class InquiryProfile:
    mineral: str | None = None
    specification: str | None = None
    quantity: str | None = None
    destination: str | None = None
    inspection: str | None = None
    documentation: str | None = None
    payment_pathway: str | None = None
    buyer_authority: str | None = None
    intended_price: str | None = None
    technical_requirements: str | None = None


@dataclass(frozen=True)
class ReadinessScore:
    score: int
    complete_fields: list[str]
    missing_fields: list[str]
    stage: str
    flags: list[str] = field(default_factory=list)


def score_inquiry(profile: InquiryProfile) -> ReadinessScore:
    complete = [name for name in READINESS_FIELDS if getattr(profile, name)]
    missing = [name for name in READINESS_FIELDS if name not in complete]
    score = len(complete)
    if score >= 8:
        stage = "QUALIFIED_CONVERSION"
    elif score >= 5:
        stage = "READINESS_EVALUATION"
    elif score >= 3:
        stage = "PARTIAL_INQUIRY"
    else:
        stage = "INTEREST_ONLY"
    return ReadinessScore(score, complete, missing, stage)
