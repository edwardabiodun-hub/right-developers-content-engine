import unittest
from pathlib import Path

from right_developers_engine.benchmarks import load_fixture, run_benchmark_fixture
from right_developers_engine.registries import load_domain_registries


ROOT = Path(__file__).resolve().parents[1]
REGISTRIES = load_domain_registries(ROOT / "config")


class BenchmarkTests(unittest.TestCase):
    def test_zircon_pricing_prompt_becomes_specification_terms_content(self):
        result = run_benchmark_fixture(load_fixture("zircon-pricing", ROOT / "benchmarks"), REGISTRIES)
        self.assertIn("SPECIFICATION_TERMS", result.selected_concepts)
        self.assertNotIn("invented_price", result.failure_codes)

    def test_monazite_prompt_requires_elevated_review(self):
        result = run_benchmark_fixture(load_fixture("monazite", ROOT / "benchmarks"), REGISTRIES)
        self.assertTrue(result.elevated_review_required)


if __name__ == "__main__":
    unittest.main()
