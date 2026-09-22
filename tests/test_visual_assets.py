import tempfile
import unittest
from pathlib import Path

from PIL import Image

from right_developers_engine.campaigns import CampaignManifest
from right_developers_engine.history import History
from right_developers_engine.orchestrator import generate_content_package
from right_developers_engine.registries import load_domain_registries
from right_developers_engine.visuals import render_platform_assets


ROOT = Path(__file__).resolve().parents[1]
REGISTRIES = load_domain_registries(ROOT / "config")


class VisualAssetTests(unittest.TestCase):
    def test_renderer_creates_platform_pngs_and_asset_manifest(self):
        manifest = CampaignManifest(
            "TR-VISUAL-001", "Trade Readiness Foundations", "active", "build_authority",
            "PROCUREMENT_TEAM", "ZIRCON_SAND", "EDUCATION", "ASSAY_BEFORE_TERMS",
            ["linkedin", "instagram", "facebook"],
        )
        package = generate_content_package(manifest, History([]), REGISTRIES)
        with tempfile.TemporaryDirectory() as tmp:
            result = render_platform_assets(package, manifest, Path(tmp))
            self.assertEqual(set(result["assets"]), {"linkedin", "instagram", "facebook"})
            self.assertTrue((Path(tmp) / "asset-manifest.json").exists())
            for platform, details in result["assets"].items():
                image_path = Path(details["path"])
                self.assertTrue(image_path.exists())
                with Image.open(image_path) as image:
                    self.assertGreater(image.width, 0)
                    self.assertGreater(image.height, 0)

    def test_renderer_uses_platform_safe_dimensions(self):
        manifest = CampaignManifest(
            "TR-VISUAL-002", "Trade Readiness Foundations", "active", "build_authority",
            "PROCUREMENT_TEAM", "ZIRCON_SAND", "EDUCATION", "ASSAY_BEFORE_TERMS",
            ["linkedin", "instagram", "facebook"],
        )
        package = generate_content_package(manifest, History([]), REGISTRIES)
        with tempfile.TemporaryDirectory() as tmp:
            result = render_platform_assets(package, manifest, Path(tmp))
            self.assertEqual(result["assets"]["linkedin"]["dimensions"], [1200, 627])
            self.assertEqual(result["assets"]["instagram"]["dimensions"], [1080, 1350])
            self.assertEqual(result["assets"]["facebook"]["dimensions"], [1200, 630])

    def test_renderer_records_provided_source_image(self):
        manifest = CampaignManifest(
            "TR-VISUAL-003", "Trade Readiness Foundations", "active", "build_authority",
            "PROCUREMENT_TEAM", "ZIRCON_SAND", "EDUCATION", "ASSAY_BEFORE_TERMS",
            ["linkedin"],
        )
        package = generate_content_package(manifest, History([]), REGISTRIES)
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "source.png"
            Image.new("RGB", (400, 400), (120, 80, 40)).save(source)
            result = render_platform_assets(package, manifest, Path(tmp) / "assets", source)
            self.assertEqual(result["assets"]["linkedin"]["source"], "provided_image")


if __name__ == "__main__":
    unittest.main()
