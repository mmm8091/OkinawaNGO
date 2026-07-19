from __future__ import annotations

import csv
import shutil
import tempfile
import unittest
from collections import Counter
from pathlib import Path

from scripts.merge_hr019_scope_reviews_v1 import apply_hr019_scope_reviews


ROOT = Path(__file__).resolve().parents[1]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


class MergeHr019ScopeReviewsV1Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        for relative in (
            "data/interim/07_actor_issue_edges_initial_v0.csv",
            "outputs/R01_R02_actor_issue_v1/HR019/"
            "HR019_edge_scope_review_queue_v0.csv",
            "outputs/R01_R02_actor_issue_v1/HR019/"
            "HR019_bridge_actor_review_queue_v0.csv",
        ):
            destination = self.root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / relative, destination)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_merges_scope_without_overclaiming_edge_review(self) -> None:
        summary = apply_hr019_scope_reviews(self.root)
        rows = read_rows(
            self.root / "data/interim/07_actor_issue_edges_initial_v0.csv"
        )
        by_id = {row["edge_id"]: row for row in rows}
        reviewed = [row for row in rows if row["scope_review_task_id"]]

        self.assertEqual(248, len(rows))
        self.assertEqual(83, len(reviewed))
        self.assertEqual(
            Counter(
                {
                    "organizational_positioning": 47,
                    "institutional_or_case_role": 14,
                    "event_specific": 8,
                    "remain_unclear": 7,
                    "case": 7,
                }
            ),
            Counter(row["scope_kind"] for row in reviewed),
        )
        self.assertEqual("human_checked", by_id["AI016"]["scope_review_status"])
        self.assertEqual("ai_seeded", by_id["AI016"]["review_status"])

        self.assertEqual("rejected", by_id["AI067"]["review_status"])
        self.assertEqual("excluded", by_id["AI067"]["graph_eligibility"])
        self.assertEqual("", by_id["AI067"]["source_ref"])
        self.assertEqual("X014", by_id["AI067"]["invalidated_source_ref"])
        self.assertEqual(
            "retired_external_watchlist_only", by_id["AI067"]["scope_status"]
        )
        self.assertEqual("needs_second_source", by_id["AI038"]["review_status"])
        self.assertEqual("excluded", by_id["AI038"]["graph_eligibility"])
        self.assertEqual(
            "deactivated_pending_actor_unit_repair",
            by_id["AI116"]["scope_status"],
        )
        self.assertEqual("research_lead", by_id["AI116"]["graph_eligibility"])
        self.assertEqual(7, summary["remain_unclear_edges"])

        bridges = read_rows(
            self.root
            / "outputs/R01_R02_actor_issue_v1/HR019/"
            "bridge_actor_human_v1.csv"
        )
        self.assertEqual(30, len(bridges))
        self.assertEqual(
            Counter(
                {
                    "narrative_with_scope": 26,
                    "research_candidate_only": 3,
                    "excluded_from_narrative": 1,
                }
            ),
            Counter(row["narrative_eligibility"] for row in bridges),
        )

    def test_is_idempotent(self) -> None:
        apply_hr019_scope_reviews(self.root)
        central = self.root / "data/interim/07_actor_issue_edges_initial_v0.csv"
        bridge = (
            self.root
            / "outputs/R01_R02_actor_issue_v1/HR019/"
            "bridge_actor_human_v1.csv"
        )
        first_central = central.read_bytes()
        first_bridge = bridge.read_bytes()
        apply_hr019_scope_reviews(self.root)
        self.assertEqual(first_central, central.read_bytes())
        self.assertEqual(first_bridge, bridge.read_bytes())


if __name__ == "__main__":
    unittest.main()
