import json
import tempfile
import unittest
from pathlib import Path

from right_developers_engine.campaigns import CampaignManifest
from right_developers_engine.history import History, HistoryEntry, append_history_entry, read_history
from right_developers_engine.orchestrator import generate_content_package
from right_developers_engine.performance import (
    PerformanceObservation,
    append_performance_observation,
    derive_learning_recommendation,
)
from right_developers_engine.registries import load_domain_registries


ROOT = Path(__file__).resolve().parents[1]
REGISTRIES = load_domain_registries(ROOT / "config")


def sample_manifest():
    return CampaignManifest(
        campaign_id="TR-001", campaign_name="Trade Readiness Foundations", status="active",
        objective="build_authority", target_audience="PROCUREMENT_TEAM", mineral_id="ZIRCON_SAND",
        stage="EDUCATION", franchise_id="ASSAY_BEFORE_TERMS", platforms=["linkedin"],
    )


class OrchestrationAndMemoryTests(unittest.TestCase):
    def test_orchestrator_creates_reviewable_package_without_network(self):
        package = generate_content_package(sample_manifest(), History([]), REGISTRIES)
        self.assertTrue(package.human_review_required)
        self.assertEqual(package.cta_route, "/request-info")
        self.assertIsNotNone(package.validation_report)

    def test_history_append_does_not_rewrite_existing_entries(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "history.jsonl"
            append_history_entry(path, HistoryEntry("one", "drafted", "Trade Readiness"))
            append_history_entry(path, HistoryEntry("two", "validated", "Buyer Readiness"))
            history = read_history(path)
            self.assertEqual([item.entry_id for item in history], ["one", "two"])

    def test_performance_learning_returns_recommendation_without_mutating_strategy(self):
        recommendation = derive_learning_recommendation(
            [PerformanceObservation("one", "linkedin", qualified_inquiries=3, saves=2)]
        )
        self.assertIn(recommendation.kind, {"evidence_lens", "format", "hook", "platform"})
        self.assertFalse(recommendation.mutates_canonical_strategy)

    def test_performance_observations_are_append_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "performance.jsonl"
            append_performance_observation(path, PerformanceObservation("one", "linkedin", 1, 2))
            append_performance_observation(path, PerformanceObservation("two", "facebook", 2, 4))
            self.assertEqual(len(path.read_text(encoding="utf-8").splitlines()), 2)


if __name__ == "__main__":
    unittest.main()
