import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class RepositoryContractsTests(unittest.TestCase):
    def test_canonical_entry_points_exist_and_are_provider_free(self):
        from right_developers_engine.config_loader import load_json_subset_yaml

        registry = load_json_subset_yaml(ROOT / "config" / "production-entry-points.yaml")
        self.assertEqual(
            set(registry["entry_points"]),
            {"daily_content_package", "content_validation", "performance_observation"},
        )
        self.assertTrue(
            all(item["provider_default"] == "none" for item in registry["entry_points"].values())
        )


if __name__ == "__main__":
    unittest.main()
