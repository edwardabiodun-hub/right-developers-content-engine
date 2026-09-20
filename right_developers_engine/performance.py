import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class PerformanceObservation:
    content_id: str
    platform: str
    qualified_inquiries: int
    saves: int


@dataclass(frozen=True)
class LearningRecommendation:
    kind: str
    rationale: str
    mutates_canonical_strategy: bool = False


def append_performance_observation(path: Path, observation: PerformanceObservation) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(asdict(observation), sort_keys=True) + "\n")


def derive_learning_recommendation(observations: list[PerformanceObservation]) -> LearningRecommendation:
    if not observations:
        return LearningRecommendation("format", "No performance evidence available; preserve current strategy.")
    best = max(observations, key=lambda item: (item.qualified_inquiries, item.saves))
    return LearningRecommendation("platform", f"Review {best.platform} packaging for qualified inquiry signals.")
