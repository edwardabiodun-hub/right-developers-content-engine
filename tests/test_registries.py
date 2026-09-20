import unittest
from pathlib import Path

from right_developers_engine.errors import ConfigurationError
from right_developers_engine.registries import load_domain_registries


ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "config"


class RegistryTests(unittest.TestCase):
    def test_registry_contains_trade_readiness_ip(self):
        registries = load_domain_registries(CONFIG_DIR)
        self.assertEqual(
            registries.worldview["north_star"],
            "More transaction-ready conversations; fewer vague inquiries.",
        )
        self.assertIn("TRADE_READINESS", registries.concept_ids())

    def test_unknown_mineral_is_rejected(self):
        registries = load_domain_registries(CONFIG_DIR)
        with self.assertRaises(ConfigurationError):
            registries.mineral("LITHIUM")


if __name__ == "__main__":
    unittest.main()
