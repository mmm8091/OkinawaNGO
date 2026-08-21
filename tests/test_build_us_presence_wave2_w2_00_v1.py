import importlib.util
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_us_presence_wave2_w2_00_v1.py"
SPEC = importlib.util.spec_from_file_location("w2_00_builder", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


class W200BuilderTest(unittest.TestCase):
    def test_selection_frames_are_versioned_and_research_only(self):
        frames = MODULE.selection_frames()
        ids = [row["selection_frame_id"] for row in frames]
        self.assertEqual(9, len(frames))
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(all(row["package_scope"] == "research_only" for row in frames))
        self.assertTrue(all(row["central_writeback"] == "no" for row in frames))
        self.assertTrue(all(row["frontend_eligibility"] == "not_frontend_ready" for row in frames))
        by_id = {row["selection_frame_id"]: row for row in frames}
        self.assertEqual(
            "2024-12-31",
            by_id["USF-W2C-ENTRY13-2026-08-22"]["period_end"],
        )
        self.assertEqual(
            "2025-12-31",
            by_id["USF-W2C-NONENTRY-MATCHED-2026-08-22"]["period_end"],
        )
        self.assertEqual(
            "2025-12-31",
            by_id["USF-W2C-PROJECTCHANGE-COUNTEREX-2026-08-22"]["period_end"],
        )

    def test_selection_member_denominators(self):
        actor_members, episode_members = MODULE.selection_members()
        counts = Counter(row["selection_frame_id"] for row in actor_members)
        self.assertEqual(5, counts["USF-W2A-SPOUSE5-2026-08-22"])
        self.assertEqual(1, counts["USF-W2B-USO-LAYERS-2026-08-22"])
        self.assertEqual(15, counts["USF-W2D-BRIDGE-TRACER15-2026-08-22"])
        self.assertEqual(50, counts["USF-W2D-ECOLOGY-S0-A1R-2026-08-22"])
        self.assertEqual(45, counts["USF-W2D-SENSITIVITY-S0-A1C-2026-08-22"])
        self.assertEqual(13, len(episode_members))
        self.assertNotIn("A072", {row["actor_id"] for row in actor_members})
        self.assertEqual(
            9,
            sum(row["fact_layer"] == "reviewed_process_layer" for row in episode_members),
        )
        self.assertEqual(
            4,
            sum(row["fact_layer"] == "candidate_event_layer" for row in episode_members),
        )
        self.assertEqual(1, sum(row["local_gap"] == "yes" for row in episode_members))
        tracer = {
            row["actor_id"]
            for row in actor_members
            if row["selection_frame_id"] == "USF-W2D-BRIDGE-TRACER15-2026-08-22"
        }
        self.assertEqual(15, len(tracer))
        self.assertNotIn("X013", tracer)
        self.assertNotIn("X014", tracer)

    def test_case_scales_remain_initial_and_adaptive(self):
        scales = MODULE.case_scales()
        self.assertEqual(4, len(scales))
        self.assertTrue(all(row["status"] == "initial_scale_registered" for row in scales))
        self.assertTrue(all(row["adaptation_rule"] for row in scales))

    def test_principal_review_queue_is_bounded_and_research_only(self):
        rows = MODULE.principal_review_queue()
        self.assertEqual(7, len(rows))
        self.assertEqual(7, len({row["decision_id"] for row in rows}))
        self.assertTrue(all(row["status"] == "pending_principal_review" for row in rows))
        self.assertTrue(all(row["package_scope"] == "research_only" for row in rows))
        self.assertTrue(all(row["principal_decision"] == "" for row in rows))


if __name__ == "__main__":
    unittest.main()
