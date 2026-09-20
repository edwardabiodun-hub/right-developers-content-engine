import argparse
import json
from datetime import date
from pathlib import Path

from .adapters import render_platform_posts
from .campaigns import CampaignManifest
from .history import History
from .orchestrator import generate_content_package
from .registries import load_domain_registries


SUPPORTED_PLATFORMS = ("linkedin", "instagram", "facebook")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate reviewable Right Developers social content.")
    parser.add_argument("--campaign-id", required=True)
    parser.add_argument("--campaign-name", required=True)
    parser.add_argument("--mineral", required=True)
    parser.add_argument("--audience", required=True)
    parser.add_argument("--stage", default="EDUCATION")
    parser.add_argument("--franchise", default="ASSAY_BEFORE_TERMS")
    parser.add_argument("--platforms", nargs="+", choices=SUPPORTED_PLATFORMS, default=list(SUPPORTED_PLATFORMS))
    parser.add_argument("--output-dir", default="outputs")
    parser.add_argument("--date", default=date.today().isoformat())
    return parser


def _metadata(package, manifest: CampaignManifest) -> dict[str, object]:
    report = package.validation_report
    return {
        "content_id": package.content_id,
        "campaign_id": manifest.campaign_id,
        "platforms": manifest.platforms,
        "validation_result": report.result,
        "human_review_required": package.human_review_required,
        "status": "human_review_required",
        "cta_route": package.cta_route,
        "hard_failures": report.hard_failures,
        "warnings": report.warnings,
    }


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    manifest = CampaignManifest(
        campaign_id=args.campaign_id,
        campaign_name=args.campaign_name,
        status="active",
        objective="build_authority",
        target_audience=args.audience,
        mineral_id=args.mineral,
        stage=args.stage,
        franchise_id=args.franchise,
        platforms=args.platforms,
    )
    root = Path(__file__).resolve().parents[1]
    registries = load_domain_registries(root / "config")
    package = generate_content_package(manifest, History([]), registries)
    if package.validation_report.result == "REJECT":
        print(json.dumps(_metadata(package, manifest), indent=2))
        return 2
    output_dir = Path(args.output_dir) / f"{args.date}-{args.campaign_id.lower()}"
    output_dir.mkdir(parents=True, exist_ok=True)
    for platform, text in render_platform_posts(package, manifest).items():
        (output_dir / f"{platform}.md").write_text(text + "\n", encoding="utf-8")
    (output_dir / "package.json").write_text(json.dumps(_metadata(package, manifest), indent=2) + "\n", encoding="utf-8")
    print(f"Review package written to {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
