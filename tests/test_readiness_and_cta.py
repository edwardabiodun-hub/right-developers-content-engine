import unittest
from right_developers_engine.cta import REQUEST_INFO_ROUTE, validate_cta
from right_developers_engine.readiness import InquiryProfile, score_inquiry


def complete_profile():
    return InquiryProfile(
        mineral="ZIRCON_SAND",
        specification="Grade and moisture basis supplied",
        quantity="26 metric tons/month",
        destination="Destination port supplied",
        inspection="Independent inspection requested",
        documentation="Required documents listed",
        payment_pathway="Payment instrument described",
        buyer_authority="Procurement lead",
        intended_price="Buyer target price supplied",
        technical_requirements="Packaging and handling requirements supplied",
    )


class ReadinessAndCtaTests(unittest.TestCase):
    def test_complete_inquiry_reaches_qualified_conversion(self):
        result = score_inquiry(complete_profile())
        self.assertEqual(result.stage, "QUALIFIED_CONVERSION")
        self.assertGreaterEqual(result.score, 8)

    def test_missing_fields_are_not_treated_as_bad_faith(self):
        result = score_inquiry(InquiryProfile(mineral="ZIRCON_SAND"))
        self.assertIn("quantity", result.missing_fields)
        self.assertNotIn("BAD_FAITH", result.flags)

    def test_attention_cta_cannot_route_to_request_info(self):
        result = validate_cta("ATTENTION", 4, REQUEST_INFO_ROUTE)
        self.assertIn("CTA_CEILING_EXCEEDED", result.hard_failures)


if __name__ == "__main__":
    unittest.main()
