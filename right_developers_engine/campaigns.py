from dataclasses import dataclass


@dataclass(frozen=True)
class CampaignManifest:
    campaign_id: str
    campaign_name: str
    status: str
    objective: str
    target_audience: str
    mineral_id: str
    stage: str
    franchise_id: str
    platforms: list[str]
