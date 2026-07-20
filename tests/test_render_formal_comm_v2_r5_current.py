import csv
import hashlib
import importlib.util
import tempfile
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "render_formal_comm_v2_r5_current",
    ROOT / "scripts" / "render_formal_comm_v2_r5_current.py",
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class CurrentFormalCommR5RendererTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tables = MODULE.load_current()
        MODULE.validate_current(cls.tables)
        cls.summary = MODULE.summarize(cls.tables)

    def test_current_r5_input_and_identity_layers_are_locked(self):
        participation = self.tables["participation"]
        self.assertEqual(169, len(participation))
        self.assertEqual(
            Counter(
                {
                    "registry_actor": 64,
                    "event_only_identity_human_checked": 22,
                    "event_only_name": 83,
                }
            ),
            Counter(row["identity_status"] for row in participation),
        )
        self.assertEqual(
            MODULE.EXPECTED_EVENT_OBSERVATION_COUNTS,
            Counter(row["event_observation_status"] for row in participation),
        )
        self.assertEqual(
            {
                "EV2010_WWF_67": Counter(
                    {
                        "registry_actor": 16,
                        "event_only_identity_human_checked": 11,
                        "event_only_name": 40,
                    }
                ),
                "EV2015_NACSJ_31": Counter({"registry_actor": 31}),
                "EV2020_OEJP_MMC_71": Counter(
                    {
                        "registry_actor": 17,
                        "event_only_identity_human_checked": 11,
                        "event_only_name": 43,
                    }
                ),
            },
            self.summary["event_identity_counts"],
        )

    def test_repeat_skeleton_is_registry_only_and_current(self):
        self.assertEqual(15, self.summary["registry_repeat_count"])
        self.assertEqual(3, self.summary["registry_all_three_count"])
        self.assertEqual(6, self.summary["human_event_only_repeat_count"])
        self.assertEqual(
            {
                ("EV2010_WWF_67", "EV2015_NACSJ_31"): 10,
                ("EV2010_WWF_67", "EV2020_OEJP_MMC_71"): 8,
                ("EV2015_NACSJ_31", "EV2020_OEJP_MMC_71"): 3,
            },
            self.summary["registry_pairwise_overlap"],
        )

    def test_export_summary_uses_current_2020_registry_count(self):
        rows = MODULE.build_export_rows(self.summary)
        by_label = {row["event"]: row for row in rows}
        self.assertEqual(17, by_label["2020 OEJP／MMC 请求"]["confirmed_registry_rows"])
        self.assertEqual(15, by_label["至少出现两次"]["confirmed_registry_rows"])
        self.assertEqual(3, by_label["贯穿三次"]["confirmed_registry_rows"])
        self.assertEqual(
            "registry 重复骨架",
            by_label["至少出现两次"]["target_or_venue"],
        )

    def test_figure_keeps_sample_and_non_alliance_boundaries(self):
        figure = MODULE.render_figure(self.summary)
        with tempfile.TemporaryDirectory() as temporary:
            svg_path = Path(temporary) / "figure.svg"
            figure.savefig(svg_path, format="svg")
            svg = svg_path.read_text(encoding="utf-8")
        import matplotlib.pyplot as plt

        plt.close(figure)
        self.assertIn("registry 层 15 个组织", svg)
        self.assertIn("3 个贯穿三次", svg)
        self.assertIn("另有 6 个经人审 event-only identity", svg)
        self.assertIn("三个名单均为目的性样本", svg)
        self.assertIn("不等于成员关系、稳定联盟或持续协调", svg)

    def test_renderer_writes_only_fig6_csv_and_png_without_mutating_inputs(self):
        input_paths = [
            MODULE.DEFAULT_PARTICIPATION_PATH,
            MODULE.DEFAULT_R5_DIR / MODULE.EVENT_CATALOG_FILENAME,
            MODULE.DEFAULT_R5_DIR / MODULE.BRIDGE_FILENAME,
            MODULE.DEFAULT_R5_DIR / MODULE.OVERLAP_FILENAME,
        ]
        before = {path: sha256(path) for path in input_paths}
        with tempfile.TemporaryDirectory() as temporary:
            output_dir = Path(temporary)
            written = MODULE.render_current(
                MODULE.DEFAULT_PARTICIPATION_PATH,
                MODULE.DEFAULT_R5_DIR,
                output_dir,
            )
            self.assertEqual(
                MODULE.OUTPUT_RELATIVE_PATHS,
                {path.relative_to(output_dir).as_posix() for path in written},
            )
            self.assertEqual(
                MODULE.OUTPUT_RELATIVE_PATHS,
                {
                    path.relative_to(output_dir).as_posix()
                    for path in output_dir.rglob("*")
                    if path.is_file()
                },
            )
            png_path = output_dir / "fig" / MODULE.FIGURE_FILENAME
            self.assertGreater(png_path.stat().st_size, 10_000)
            with (
                output_dir / "data" / MODULE.DATA_FILENAME
            ).open(encoding="utf-8-sig", newline="") as handle:
                rendered_rows = list(csv.DictReader(handle))
            by_label = {row["event"]: row for row in rendered_rows}
            self.assertEqual(
                "17",
                by_label["2020 OEJP／MMC 请求"]["confirmed_registry_rows"],
            )
        self.assertEqual(before, {path: sha256(path) for path in input_paths})


if __name__ == "__main__":
    unittest.main()
