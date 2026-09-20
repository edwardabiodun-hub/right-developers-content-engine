import unittest
from pathlib import Path

from right_developers_engine.claims import Claim, ClaimStatus, validate_claims
from right_developers_engine.registries import load_domain_registries


ROOT = Path(__file__).resolve().parents[1]
REGISTRIES = load_domain_registries(ROOT / "config")


class ClaimValidationTests(unittest.TestCase):
    def test_unverified_price_claim_is_hard_failure(self):
        report = validate_claims(
            [
                Claim(
                    "Zircon is available at $100 per tonne",
                    ClaimStatus.UNKNOWN,
                    None,
                    "ZIRCON_SAND",
                )
            ],
            REGISTRIES,
        )
        self.assertIn("UNSUPPORTED_COMMERCIAL_CLAIM", report.hard_failures)

    def test_labeled_illustration_is_allowed(self):
        report = validate_claims(
            [
                Claim(
                    "Illustrative example: a buyer may need a moisture basis",
                    ClaimStatus.ILLUSTRATIVE,
                    None,
                    "ZIRCON_SAND",
                )
            ],
            REGISTRIES,
        )
        self.assertEqual(report.hard_failures, [])

    def test_monazite_sensitive_claim_requires_source(self):
        report = validate_claims(
            [
                Claim(
                    "Monazite transport requirements depend on applicable rules",
                    ClaimStatus.SOURCE_REQUIRED,
                    None,
                    "MONAZITE",
                )
            ],
            REGISTRIES,
        )
        self.assertIn("SOURCE_REQUIRED", report.warnings)


if __name__ == "__main__":
    unittest.main()
