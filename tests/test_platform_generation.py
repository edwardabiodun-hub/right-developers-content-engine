import json
import tempfile
import unittest
from pathlib import Path

from right_developers_engine.adapters import render_platform_posts
from right_developers_engine.campaigns import CampaignManifest
from right_developers_engine.history import History
from right_developers_engine.orchestrator import generate_content_package
from right_developers_engine.registries import load_domain_registries


ROOT = Path(__file__).resolve().parents[1]
REGISTRIES = load_domain_registries(ROOT / "config")


def package():
    manifest = CampaignManifest(
        "TR-CLI-001", "Trade Readiness Foundations", "active", "build_authority",
        "PROCUREMENT_TEAM", "ZIRCON_SAND", "EDUCATION", "ASSAY_BEFORE_TERMS",
        ["linkedin", "instagram", "facebook"],
    )
    return generate_content_package(manifest, History([]), REGISTRIES), manifest


class PlatformGenerationTests(unittest.TestCase):
    def test_render_platform_posts_returns_three_native_packages(self):
        content_package, manifest = package()
        posts = render_platform_posts(content_package, manifest)
        self.assertEqual(set(posts), {"linkedin", "instagram", "facebook"})
        self.assertIn("Trade Readiness", posts["linkedin"])
        self.assertIn("Slide 1", posts["instagram"])
        self.assertIn("A mineral inquiry", posts["facebook"])

    def test_platform_posts_do_not_claim_approval_or_publish(self):
        content_package, manifest = package()
        posts = render_platform_posts(content_package, manifest)
        self.assertTrue(all("human_review_required" not in text for text in posts.values()))
        self.assertTrue(all("Published" not in text for text in posts.values()))


if __name__ == "__main__":
    unittest.main()
