from __future__ import annotations

import csv
import shutil
import tempfile
import unittest
from collections import Counter
from pathlib import Path

from scripts.merge_hr024_hr025_edges_v1 import apply_hr024_hr025_edges


ROOT = Path(__file__).resolve().parents[1]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


class MergeHr024Hr025EdgesV1Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        for relative in (
            "data/interim/03_issue_taxonomy_v0.csv",
            "data/interim/04_place_registry_v0.csv",
            "data/interim/07_actor_issue_edges_initial_v0.csv",
            "data/interim/08_actor_place_edges_initial_v0.csv",
            "outputs/edge_activation_v1/HR024_edge_activation_review_v0.csv",
            "outputs/R03_spatial_dossier_v1/"
            "HR025_actor_place_semantics_review_v0.csv",
        ):
            destination = self.root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / relative, destination)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_merges_case_edges_and_place_semantics(self) -> None:
        summary = apply_hr024_hr025_edges(self.root)

        issue_rows = read_rows(
            self.root / "data/interim/07_actor_issue_edges_initial_v0.csv"
        )
        place_rows = read_rows(
            self.root / "data/interim/08_actor_place_edges_initial_v0.csv"
        )
        issue_by_task = {
            row["review_task_id"]: row
            for row in issue_rows
            if row.get("review_task_id", "").startswith("HR024-")
        }
        place_by_id = {row["edge_id"]: row for row in place_rows}

        self.assertEqual(248, len(issue_rows))
        self.assertEqual(7, summary["hr024_case_issue_edges"])
        self.assertEqual(
            {f"HR024-{number:03d}" for number in range(2, 9)},
            set(issue_by_task),
        )
        self.assertNotIn("HR024-001", issue_by_task)
        self.assertTrue(
            all(row["case_id"] == "R8C01" for row in issue_by_task.values())
        )
        self.assertTrue(
            all(
                row["review_status"] == "human_checked"
                for row in issue_by_task.values()
            )
        )
        self.assertEqual(
            "S093;S060", issue_by_task["HR024-002"]["source_ref"]
        )
        self.assertEqual(
            "case_role", issue_by_task["HR024-008"]["graph_eligibility"]
        )

        self.assertEqual(135, len(place_rows))
        self.assertEqual(47, summary["hr025_reviewed_place_edges"])
        self.assertEqual("P018", place_by_id["AP036"]["place_id"])
        self.assertEqual("Ginowan", place_by_id["AP036"]["place_name"])
        self.assertEqual("headquarters", place_by_id["AP036"]["place_semantic"])
        self.assertEqual("P018", place_by_id["AP044"]["place_id"])
        self.assertEqual("P021", place_by_id["AP049"]["place_id"])
        self.assertEqual(
            "needs_second_source", place_by_id["AP049"]["review_status"]
        )
        self.assertEqual("P007", place_by_id["AP123"]["place_id"])

        self.assertEqual(
            "advocacy_target", place_by_id["AP095"]["place_semantic"]
        )
        self.assertEqual("event_site", place_by_id["AP107"]["place_semantic"])
        self.assertEqual(
            "advocacy_target", place_by_id["AP114"]["place_semantic"]
        )
        self.assertEqual(
            "advocacy_target", place_by_id["AP115"]["place_semantic"]
        )

        reviewed_places = [
            row for row in place_rows if row["place_review_task_id"]
        ]
        active_semantics = Counter(
            row["place_semantic"]
            for row in reviewed_places
            if row["review_status"] != "rejected"
        )
        self.assertEqual(
            Counter(
                {
                    "site_presence": 27,
                    "advocacy_target": 7,
                    "event_site": 4,
                    "headquarters": 4,
                }
            ),
            active_semantics,
        )
        retired = [
            row for row in reviewed_places if row["review_status"] == "rejected"
        ]
        self.assertEqual(5, len(retired))
        self.assertTrue(
            all(row["graph_eligibility"] == "excluded" for row in retired)
        )

    def test_is_idempotent(self) -> None:
        apply_hr024_hr025_edges(self.root)
        issue = self.root / "data/interim/07_actor_issue_edges_initial_v0.csv"
        place = self.root / "data/interim/08_actor_place_edges_initial_v0.csv"
        first_issue = issue.read_bytes()
        first_place = place.read_bytes()
        apply_hr024_hr025_edges(self.root)
        self.assertEqual(first_issue, issue.read_bytes())
        self.assertEqual(first_place, place.read_bytes())


if __name__ == "__main__":
    unittest.main()
