import json
import tempfile
import unittest
from pathlib import Path

from right_developers_engine.cli import main


class CliTests(unittest.TestCase):
    def test_cli_writes_review_package_for_three_platforms(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "outputs"
            exit_code = main([
                "--campaign-id", "TR-CLI-001",
                "--campaign-name", "Trade Readiness Foundations",
                "--mineral", "ZIRCON_SAND",
                "--audience", "PROCUREMENT_TEAM",
                "--stage", "EDUCATION",
                "--franchise", "ASSAY_BEFORE_TERMS",
                "--platforms", "linkedin", "instagram", "facebook",
                "--output-dir", str(output),
                "--date", "2026-09-20",
            ])
            self.assertEqual(exit_code, 0)
            package_dir = output / "2026-09-20-tr-cli-001"
            self.assertTrue((package_dir / "linkedin.md").exists())
            self.assertTrue((package_dir / "instagram.md").exists())
            self.assertTrue((package_dir / "facebook.md").exists())
            self.assertTrue((package_dir / "assets" / "linkedin.png").exists())
            self.assertTrue((package_dir / "assets" / "instagram.png").exists())
            self.assertTrue((package_dir / "assets" / "facebook.png").exists())
            self.assertTrue((package_dir / "assets" / "asset-manifest.json").exists())
            metadata = json.loads((package_dir / "package.json").read_text(encoding="utf-8"))
            self.assertTrue(metadata["human_review_required"])
            self.assertEqual(metadata["status"], "human_review_required")


if __name__ == "__main__":
    unittest.main()
