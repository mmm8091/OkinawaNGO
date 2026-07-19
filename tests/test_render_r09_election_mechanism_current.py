import copy
import hashlib
import importlib.util
import tempfile
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "render_r09_election_mechanism_current",
    ROOT / "scripts" / "render_r09_election_mechanism_current.py",
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class CurrentElectionMechanismRendererTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tables = MODULE.load_current()
        MODULE.validate_current(cls.tables)
        cls.summary = MODULE.summarize(cls.tables["events"])

    def test_current_reviewed_status_boundary_is_locked(self):
        self.assertEqual(19, len(self.tables["events"]))
        self.assertEqual(18, self.summary["confirmed"])
        self.assertEqual(1, self.summary["announced"])
        self.assertEqual(
            MODULE.EXPECTED_ACTION_COUNTS,
            Counter(row["action_type"] for row in self.tables["events"]),
        )
        announced = [
            row
            for row in self.tables["events"]
            if row["event_status"] == "announced_not_occurrence_verified"
        ]
        self.assertEqual(["R9EC018"], [row["record_id"] for row in announced])

    def test_module_aggregates_are_cross_checked_against_central_events(self):
        self.assertEqual(15, len(self.tables["modes"]))
        self.assertEqual(3, len(self.tables["windows"]))
        broken = copy.deepcopy(self.tables)
        broken["modes"][0]["candidate_row_count"] = "99"
        with self.assertRaisesRegex(ValueError, "aggregate disagrees"):
            MODULE.validate_current(broken)

    def test_candidate_or_status_drift_is_rejected(self):
        broken = copy.deepcopy(self.tables)
        broken["events"][0]["review_status"] = "ai_seeded"
        with self.assertRaisesRegex(ValueError, "human-checked"):
            MODULE.validate_current(broken)

        broken = copy.deepcopy(self.tables)
        broken["events"][-2]["event_status"] = "confirmed_observed_action"
        with self.assertRaisesRegex(ValueError, "event-status boundary"):
            MODULE.validate_current(broken)

    def test_svg_text_keeps_noncausal_and_announcement_boundaries(self):
        figure = MODULE.render_figure(self.summary)
        with tempfile.TemporaryDirectory() as temporary:
            svg_path = Path(temporary) / "figure.svg"
            figure.savefig(svg_path, format="svg")
            svg = svg_path.read_text(encoding="utf-8")
        import matplotlib.pyplot as plt

        plt.close(figure)
        self.assertIn("18 条确认发生", svg)
        self.assertIn("1 条仅有预告", svg)
        self.assertIn("箭头只组织资料", svg)
        self.assertIn("票数变化", svg)
        self.assertIn("稳定联盟", svg)
        self.assertIn("R9EC018", svg)

    def test_renderer_writes_only_three_assets_without_mutating_inputs(self):
        input_paths = [
            MODULE.DEFAULT_EVENTS_PATH,
            MODULE.DEFAULT_MODULE_DIR / MODULE.MODE_FILENAME,
            MODULE.DEFAULT_MODULE_DIR / MODULE.WINDOW_FILENAME,
        ]
        before = {path: sha256(path) for path in input_paths}
        with tempfile.TemporaryDirectory() as temporary:
            output_dir = Path(temporary)
            written = MODULE.render_current(
                MODULE.DEFAULT_EVENTS_PATH,
                MODULE.DEFAULT_MODULE_DIR,
                output_dir,
            )
            self.assertEqual(
                MODULE.OUTPUT_FILENAMES,
                {path.name for path in written},
            )
            self.assertEqual(
                MODULE.OUTPUT_FILENAMES,
                {path.name for path in output_dir.iterdir()},
            )
            self.assertGreater(
                (output_dir / "fig_r09_noncausal_mechanism_v1.png").stat().st_size,
                10_000,
            )
            html = (
                output_dir / "fig_r09_noncausal_mechanism_v1.html"
            ).read_text(encoding="utf-8")
            self.assertIn("<svg", html)
            self.assertIn("R9EC018", html)
        self.assertEqual(before, {path: sha256(path) for path in input_paths})


if __name__ == "__main__":
    unittest.main()
