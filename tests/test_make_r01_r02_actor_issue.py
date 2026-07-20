import importlib.util
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "make_r01_r02_actor_issue",
    ROOT / "scripts" / "make_r01_r02_actor_issue.py",
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


class ScopeClassificationTests(unittest.TestCase):
    def test_human_reviewed_case_scope_overrides_text_heuristic(self):
        scope, rule = MODULE.classify_scope(
            {
                "scope_kind": "case",
                "scope_review_status": "human_checked",
                "relation_basis": "mission and long-running activity",
            }
        )
        self.assertEqual(scope, "institutional_or_case_role")
        self.assertIn("human-reviewed", rule)

    def test_human_reviewed_remain_unclear_stays_unclear(self):
        scope, _ = MODULE.classify_scope(
            {
                "scope_kind": "remain_unclear",
                "scope_review_status": "human_checked",
                "relation_basis": "mission",
            }
        )
        self.assertEqual(scope, "mixed_or_unclear")


class ActiveHistoryGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.actor_history = MODULE.read_csv(MODULE.REGISTRY)
        cls.edge_history = MODULE.read_csv(MODULE.EDGES)
        cls.issues = MODULE.read_csv(MODULE.ISSUES)
        cls.actors_by_id = {row["actor_id"]: row for row in cls.actor_history}
        cls.issues_by_id = {row["issue_id"]: row for row in cls.issues}
        cls.active_actor_ids = {
            row["actor_id"]
            for row in cls.actor_history
            if MODULE.actor_analysis_gate(row)[0]
        }
        cls.layered_history = MODULE.build_layered_edges(
            cls.edge_history,
            cls.actors_by_id,
            cls.issues_by_id,
            cls.active_actor_ids,
        )
        cls.layered = [
            row for row in cls.layered_history
            if row["analysis_inclusion"] == "active"
        ]

    def test_merged_duplicate_actor_is_history_only(self):
        actor = self.actors_by_id["A072"]
        active, reason = MODULE.actor_analysis_gate(actor)
        self.assertFalse(active)
        self.assertEqual("actor_scope_status_merged_duplicate", reason)
        self.assertNotIn("A072", self.active_actor_ids)

    def test_all_explicit_edge_exclusion_modes_are_history_only(self):
        for row in (
            {"actor_id": "A001", "review_status": "rejected"},
            {"actor_id": "A001", "claim_status": "unsupported"},
            {"actor_id": "A001", "graph_eligibility": "excluded"},
            {"actor_id": "A001", "scope_status": "retired_duplicate"},
            {"actor_id": "A001", "scope_status": "deactivated_until_direct_evidence"},
            {
                "actor_id": "A001",
                "scope_status": "event_specific_excluded_from_default_okinawa_narrative",
            },
            {"actor_id": "A072"},
        ):
            self.assertFalse(MODULE.edge_analysis_gate(row, self.active_actor_ids)[0])

    def test_current_counts_exclude_history_rows(self):
        review = Counter(row["review_layer"] for row in self.layered)
        connected = {row["actor_id"] for row in self.layered}
        self.assertEqual(122, len(self.actor_history))
        self.assertEqual(121, len(self.active_actor_ids))
        self.assertEqual(294, len(self.layered_history))
        self.assertEqual(283, len(self.layered))
        self.assertEqual(116, len(connected))
        self.assertEqual(5, len(self.active_actor_ids - connected))
        self.assertEqual({"human_reviewed": 141, "candidate": 142}, dict(review))
        self.assertEqual(
            11,
            sum(row["analysis_inclusion"] == "excluded_history" for row in self.layered_history),
        )
        self.assertFalse(
            any(
                row["analysis_inclusion"] != "active"
                and row["review_layer"] == "candidate"
                for row in self.layered_history
            )
        )

    def test_ai068_is_not_a_candidate_network_edge(self):
        row = next(row for row in self.layered_history if row["edge_id"] == "AI068")
        central = next(row for row in self.edge_history if row["edge_id"] == "AI068")
        self.assertEqual("excluded_history", row["analysis_inclusion"])
        self.assertEqual("excluded_history", row["review_layer"])
        self.assertEqual("edge_graph_eligibility_excluded", row["analysis_exclusion_reason"])
        self.assertIn(
            "excluded_from_default_okinawa_narrative",
            central["scope_status"],
        )


class CompletedHumanReviewLedgerTests(unittest.TestCase):
    def test_hr019_decisions_remain_closed(self):
        for filename in (
            "HR019_review_v0.csv",
            "HR019_bridge_actor_review_queue_v0.csv",
            "HR019_edge_scope_review_queue_v0.csv",
        ):
            rows = MODULE.read_csv(MODULE.HR / filename)
            self.assertTrue(rows, filename)
            self.assertTrue(
                all(row.get("review_decision", "").strip() for row in rows),
                filename,
            )


if __name__ == "__main__":
    unittest.main()
