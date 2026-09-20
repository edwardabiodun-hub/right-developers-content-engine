import unittest
from pathlib import Path

from right_developers_engine.claims import Claim, ClaimStatus
from right_developers_engine.registries import load_domain_registries
from right_developers_engine.validation import ContentUnit, validate_content


ROOT = Path(__file__).resolve().parents[1]
REGISTRIES = load_domain_registries(ROOT / "config")


def generic_zircon_price_post():
    return ContentUnit(
        content_id="generic-1", mineral_id="ZIRCON_SAND", audience_id="MINERAL_TRADER",
        pillar_id="TERMS_PRICING_DRIVERS", concept_ids=[], franchise_id="SPECIFICATION_TO_TERMS",
        stage="ATTENTION", claims=[Claim("Zircon prices depend on many factors", ClaimStatus.UNKNOWN, None, "ZIRCON_SAND")],
        cta_tier=0, cta_route=None, body="Optimize your procurement and unlock better pricing.", platform="linkedin",
    )


def qualified_trade_readiness_post(concept_ids=None):
    return ContentUnit(
        content_id="qualified-1", mineral_id="ZIRCON_SAND", audience_id="PROCUREMENT_TEAM",
        pillar_id="BUYER_READINESS", concept_ids=concept_ids or ["TRADE_READINESS", "INQUIRY_COMPLETENESS"],
        franchise_id="INQUIRY_NOT_READY", stage="PROOF",
        claims=[Claim("Illustrative example: a buyer may need a moisture basis before comparing terms", ClaimStatus.ILLUSTRATIVE, None, "ZIRCON_SAND")],
        cta_tier=2, cta_route=None, body="A price request without specification, quantity, and destination is an incomplete commercial question. Use this buyer-readiness check before requesting terms.", platform="linkedin",
    )


class ContentValidationTests(unittest.TestCase):
    def test_generic_commodity_post_is_rejected_or_requires_revision(self):
        report = validate_content(generic_zircon_price_post(), REGISTRIES)
        self.assertIn(report.result, {"WARN", "REJECT"})
        self.assertTrue(report.generic_language_flags)

    def test_trade_readiness_post_with_illustrative_evidence_can_pass_review(self):
        report = validate_content(qualified_trade_readiness_post(), REGISTRIES)
        self.assertEqual(report.result, "PASS")
        self.assertTrue(report.human_review_required)

    def test_unknown_canonical_concept_is_rejected(self):
        report = validate_content(qualified_trade_readiness_post(["INVENTED_CONCEPT"]), REGISTRIES)
        self.assertIn("UNKNOWN_CANONICAL_CONCEPT", report.hard_failures)


if __name__ == "__main__":
    unittest.main()
