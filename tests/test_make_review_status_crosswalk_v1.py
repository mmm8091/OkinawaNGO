from __future__ import annotations

import csv
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.make_review_status_crosswalk_v1 import build


ROOT = Path(__file__).resolve().parents[1]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


class ReviewStatusCrosswalkTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        for relative in (
            "data/interim/05_source_log_initial_v0.csv",
            "data/interim/07_actor_issue_edges_initial_v0.csv",
            "data/interim/19_sakishima_frame_corpus_v0.csv",
            "data/interim/20_referendum_process_stages_v0.csv",
            "data/interim/35_heterogeneous_event_repertoire_v1.csv",
            "outputs/actor_lifecycle_v1/actor_lifecycle_v0.csv",
        ):
            destination = self.root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / relative, destination)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_builds_blank_review_tasks_without_touching_inputs(self) -> None:
        source_before = (self.root / "data/interim/05_source_log_initial_v0.csv").read_bytes()
        summary = build(self.root)
        source_after = (self.root / "data/interim/05_source_log_initial_v0.csv").read_bytes()

        self.assertEqual(source_before, source_after)
        self.assertEqual(summary["total_tasks"], 50)
        self.assertEqual(summary["source_row_tasks"], 45)
        self.assertEqual(summary["actor_issue_row_tasks"], 1)
        self.assertEqual(summary["table_policy_tasks"], 4)

        tasks = read_rows(
            self.root
            / "outputs/review_status_crosswalk_v1/HR034_review_status_crosswalk_v1.csv"
        )
        self.assertEqual(len(tasks), 50)
        self.assertEqual(
            [row["object_id"] for row in tasks if row["upstream_table"].endswith("07_actor_issue_edges_initial_v0.csv")],
            ["AI068"],
        )
        for row in tasks:
            self.assertEqual(row["decision"], "")
            self.assertEqual(row["revised_review_status"], "")
            self.assertEqual(row["human_reviewer"], "")
            self.assertEqual(row["review_date"], "")
            self.assertEqual(row["review_note"], "")

    def test_table_policy_counts_are_not_expanded_to_row_reviews(self) -> None:
        build(self.root)
        tasks = read_rows(
            self.root
            / "outputs/review_status_crosswalk_v1/HR034_review_status_crosswalk_v1.csv"
        )
        policies = {row["object_id"]: row for row in tasks if row["task_kind"] == "table_policy"}
        self.assertEqual(len(policies), 4)
        self.assertEqual(policies["TABLE_R4_QA_SAFE_ONLINE"]["affected_row_count"], "10")
        self.assertEqual(policies["TABLE_R9_ACCEPTED"]["affected_row_count"], "29")
        self.assertEqual(policies["TABLE_HET_ACCEPTED"]["affected_row_count"], "49")
        self.assertEqual(policies["TABLE_LIFECYCLE_WORKFLOW_STATUS"]["affected_row_count"], "4")


if __name__ == "__main__":
    unittest.main()
