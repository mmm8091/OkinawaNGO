import hashlib
import importlib.util
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "render_r10_official_universe_current",
    ROOT / "scripts" / "render_r10_official_universe_current.py",
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class CurrentR10OfficialUniverseRendererTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tables = MODULE.load_current()
        MODULE.validate_current(cls.tables)

    def test_current_source_universe_and_aggregate_counts_are_locked(self):
        self.assertEqual(616, len(self.tables["universe"]))
        self.assertEqual(190, len(self.tables["issues"]))
        self.assertEqual(150, len(self.tables["departments"]))
        self.assertEqual(365, len(self.tables["partners"]))
        self.assertEqual(
            616,
            sum(int(row["source_row_count"]) for row in self.tables["partners"]),
        )
        self.assertEqual(
            17,
            sum(
                int(row["source_row_count"]) >= 5
                for row in self.tables["partners"]
            ),
        )

    def test_renderer_states_source_row_and_non_inference_boundaries(self):
        f035 = MODULE.render_f035(self.tables)
        f036 = MODULE.render_f036(self.tables)
        combined = f035 + f036
        for expected in (
            "616 条来源行",
            "469/616（76.1%）",
            "来源行数 ≠ 组织数、合同数、拨款数",
            "C4 不等于现金 grant",
            "365 个机器排版标签不是 actor",
            "共同企业体未拆分",
            "项目事业费不等于向标签对应主体付款",
        ):
            self.assertIn(expected, combined)

    def test_renderer_writes_only_four_current_assets_and_preserves_inputs_and_legacy_pngs(
        self,
    ):
        protected = [*MODULE.INPUT_PATHS, *MODULE.LEGACY_PNG_PATHS]
        before = {path: sha256(path) for path in protected}
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            written = MODULE.render_current(output)
            self.assertEqual(MODULE.OUTPUT_FILENAMES, {path.name for path in written})
            self.assertEqual(
                MODULE.OUTPUT_FILENAMES,
                {path.name for path in output.rglob("*") if path.is_file()},
            )
            for path in written:
                if path.suffix == ".svg":
                    ET.fromstring(path.read_text(encoding="utf-8"))
        self.assertEqual(before, {path: sha256(path) for path in protected})

    def test_report_traceability_uses_safe_renderer_and_current_assets(self):
        trace_path = (
            ROOT
            / "outputs"
            / "report_assembly_v1"
            / "figure_traceability_crosswalk_v1.csv"
        )
        manifest_path = (
            ROOT / "outputs" / "report_assembly_v1" / "figure_manifest_v1.csv"
        )
        import csv

        with trace_path.open(encoding="utf-8-sig", newline="") as handle:
            trace = {
                row["asset_id"]: row
                for row in csv.DictReader(handle)
                if row["asset_id"] in {"F035", "F036"}
            }
        with manifest_path.open(encoding="utf-8-sig", newline="") as handle:
            manifest = {
                row["asset_id"]: row
                for row in csv.DictReader(handle)
                if row["asset_id"] in {"F035", "F036"}
            }

        for asset_id in ("F035", "F036"):
            self.assertEqual(
                "scripts/render_r10_official_universe_current.py",
                trace[asset_id]["generation_script"],
            )
            self.assertTrue(manifest[asset_id]["primary_path"].endswith("_current.svg"))
            self.assertEqual(
                manifest[asset_id]["primary_path"],
                trace[asset_id]["figure_path"],
            )
            self.assertNotIn(
                "make_r10_official_collaboration_universe_v1.py",
                trace[asset_id]["generation_script"],
            )

        readme = (
            ROOT
            / "outputs"
            / "R10_official_collaboration_universe_v1"
            / "README.md"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "python scripts/render_r10_official_universe_current.py",
            readme,
        )
        self.assertNotIn(
            "Run with `python scripts/make_r10_official_collaboration_universe_v1.py`",
            readme,
        )


if __name__ == "__main__":
    unittest.main()
