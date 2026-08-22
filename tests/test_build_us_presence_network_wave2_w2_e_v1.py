import csv
import json
import tempfile
import unittest
from pathlib import Path

from scripts.build_us_presence_network_wave2_w2_e_v1 import build
from scripts.validate_research_work_package_v1 import REQUIRED_COLUMNS, validate_package


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
            register = output / "unexpected_findings_register_v1.csv"
            with register.open(encoding="utf-8-sig", newline="") as handle:
                reader = csv.DictReader(handle)
                self.assertEqual(reader.fieldnames, REQUIRED_COLUMNS)
                self.assertEqual(list(reader), [])
            readme = (output / "README.md").read_text(encoding="utf-8")
            self.assertIn("## 意外发现登记", readme)
            self.assertIn("本轮 0 条", readme)
            self.assertIn("lead_only", readme)
            self.assertIn("最多向外追查 3 步", readme)
            self.assertIn("每包最多 10 条新观察", readme)
            self.assertEqual(validate_package(output), [])
            self.assertEqual(report["counts"]["unexpected_findings_rows"], 0)
            self.assertTrue(report["checks"]["unexpected_findings_register_contract"])
            manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["status"], "research_only_principal_checkpoint_pending")
            self.assertIn(
                "unexpected_findings_register_v1.csv",
                {entry["path"] for entry in manifest["files"]},
            )
            self.assertNotIn("publication", {entry["path"].split("/")[0] for entry in manifest["files"]})
            first_manifest_bytes = (output / "manifest.json").read_bytes()
            first_spine_bytes = (output / "historical_spine_v1.csv").read_bytes()
            build(output)
            self.assertEqual((output / "manifest.json").read_bytes(), first_manifest_bytes)
            self.assertEqual((output / "historical_spine_v1.csv").read_bytes(), first_spine_bytes)


if __name__ == "__main__":
    unittest.main()
