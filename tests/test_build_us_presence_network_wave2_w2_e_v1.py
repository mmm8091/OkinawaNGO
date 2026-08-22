import json
import tempfile
import unittest
from pathlib import Path

from scripts.build_us_presence_network_wave2_w2_e_v1 import build


class TestW2EBuilder(unittest.TestCase):
    def test_research_only_package_builds_and_validates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "w2e"
            report = build(output)
            self.assertEqual(report["status"], "PASS")
            self.assertEqual(report["counts"]["historical_spine_rows"], 30)
            self.assertEqual(report["counts"]["accountability_rows"], 18)
            self.assertEqual(report["counts"]["service_care_rows"], 12)
            self.assertEqual(report["counts"]["locally_frozen_new_sources"], 5)
            self.assertTrue((output / "fig_w2e_two_spines_v1.svg").exists())
            manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["status"], "research_only_principal_checkpoint_pending")
            self.assertNotIn("publication", {entry["path"].split("/")[0] for entry in manifest["files"]})


if __name__ == "__main__":
    unittest.main()
