from .campaigns import CampaignManifest
from .orchestrator import ContentPackage


def _linkedin(package: ContentPackage, manifest: CampaignManifest) -> str:
    return (
        f"Trade Readiness | {manifest.mineral_id.replace('_', ' ').title()}\n\n"
        f"{package.thesis}\n\n"
        "A serious inquiry should make four things visible early:\n"
        "- the product specification or assay basis\n"
        "- the intended quantity\n"
        "- the destination and delivery context\n"
        "- the inspection and documentation pathway\n\n"
        "Interest starts the conversation. Readiness determines whether the conversation can progress."
    )


def _instagram(package: ContentPackage, manifest: CampaignManifest) -> str:
    mineral = manifest.mineral_id.replace("_", " ").title()
    return (
        f"Slide 1\n{mineral} inquiries need more than a price request.\n\n"
        "Slide 2\nStart with the specification or assay basis.\n\n"
        "Slide 3\nState the intended quantity and cadence.\n\n"
        "Slide 4\nClarify destination, inspection, and documentation.\n\n"
        "Slide 5\nThat is how product interest becomes a transaction-ready conversation.\n\n"
        f"Caption\n{package.thesis} Save this buyer-readiness check before requesting terms."
    )


def _facebook(package: ContentPackage, manifest: CampaignManifest) -> str:
    mineral = manifest.mineral_id.replace("_", " ").title()
    return (
        f"A mineral inquiry about {mineral} is easier to evaluate when the commercial context is visible.\n\n"
        f"{package.thesis}\n\n"
        "Before asking for terms, identify the specification, quantity, destination, inspection expectations, and documentation requirements. "
        "Which of those fields is most often missing from the inquiries your team receives?"
    )


def render_platform_posts(package: ContentPackage, manifest: CampaignManifest) -> dict[str, str]:
    renderers = {"linkedin": _linkedin, "instagram": _instagram, "facebook": _facebook}
    return {platform: renderers[platform](package, manifest) for platform in manifest.platforms if platform in renderers}
