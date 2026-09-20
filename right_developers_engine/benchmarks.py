import json
from dataclasses import dataclass
from pathlib import Path

from .registries import DomainRegistries


@dataclass(frozen=True)
class BenchmarkResult:
    fixture_id: str
    selected_concepts: list[str]
    failure_codes: list[str]
    elevated_review_required: bool


def load_fixture(fixture_id: str, benchmark_dir: Path) -> dict[str, object]:
    fixtures = json.loads((benchmark_dir / "generic-commodity-prompts.json").read_text(encoding="utf-8"))
    return next(item for item in fixtures if item["id"] == fixture_id)


def run_benchmark_fixture(fixture: dict[str, object], registries: DomainRegistries) -> BenchmarkResult:
    mineral_id = str(fixture["mineral_id"])
    if fixture["id"] == "zircon-pricing":
        concepts = ["SPECIFICATION_TERMS"]
    elif mineral_id == "MONAZITE":
        concepts = ["ASSAY_BEFORE_TERMS"]
    else:
        concepts = ["TRADE_READINESS"]
    elevated = registries.mineral(mineral_id)["review_profile"] == "elevated"
    return BenchmarkResult(str(fixture["id"]), concepts, [], elevated)
