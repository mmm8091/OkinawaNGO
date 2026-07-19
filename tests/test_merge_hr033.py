from __future__ import annotations

import csv
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.merge_hr033 import apply_hr033


ROOT = Path(__file__).resolve().parents[1]


def read_rows(path: Path, key: str) -> dict[str, dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return {row[key]: row for row in csv.DictReader(handle)}


class MergeHR033Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        for relative in (
            "data/interim/15_funding_or_support_edges_sample_v0.csv",
            "data/interim/21_admin_collaboration_relations_v0.csv",
            "data/interim/22_admin_amount_observations_v0.csv",
            "data/interim/23_admin_function_observations_v0.csv",
            "data/interim/human_review_log_v0.csv",
        ):
            destination = self.root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / relative, destination)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_merges_six_decisions_and_splits_f025_amount(self) -> None:
        summary = apply_hr033(self.root)

        relations = read_rows(
            self.root / "data/interim/15_funding_or_support_edges_sample_v0.csv",
            "edge_id",
        )
        self.assertEqual(summary["accepted"], 4)
        self.assertEqual(summary["revised"], 2)
        self.assertEqual(relations["F006"]["review_status"], "human_checked")
        self.assertEqual(relations["F006"]["source_role"], "umbrella_coordination_association")
        self.assertEqual(relations["F006"]["target_role"], "member_club")
        self.assertEqual(relations["F021"]["review_status"], "human_revised")
        self.assertEqual(relations["F021"]["funding_relation_confidence"], "confirmed_donation")
        self.assertEqual(relations["F021"]["amount"], "3250")
        self.assertEqual(relations["F021"]["event_date"], "2025-12-02")
        self.assertEqual(relations["F021"]["publication_date"], "2025-12-12")
        self.assertEqual(relations["F025"]["review_status"], "human_revised")
        self.assertEqual(relations["F025"]["claim_status"], "supported_bounded")
        self.assertEqual(relations["F025"]["amount"], "")
        self.assertEqual(relations["F025"]["amount_semantics"], "named_contribution_amount_unknown")
        self.assertEqual(relations["F025"]["needs_local_retrieval"], "no")
        self.assertNotIn(
            "verified",
            {relations[edge_id]["review_status"] for edge_id in ("F006", "F007", "F021", "F022", "F023", "F025")},
        )

        r10_relations = read_rows(
            self.root / "data/interim/21_admin_collaboration_relations_v0.csv",
            "relation_observation_id",
        )
        r10_amounts = read_rows(
            self.root / "data/interim/22_admin_amount_observations_v0.csv",
            "amount_observation_id",
        )
        self.assertEqual(r10_relations["R10R029"]["relation_type"], "aggregate_financial_contribution")
        self.assertEqual(r10_relations["R10R029"]["review_status"], "human_revised")
        self.assertEqual(r10_amounts["R10AM024"]["amount_value"], "102000")
        self.assertEqual(r10_amounts["R10AM024"]["review_status"], "human_revised")
        self.assertIn("不能", r10_amounts["R10AM024"]["interpretation_limit"])

    def test_is_idempotent(self) -> None:
        apply_hr033(self.root)
        first_relations = read_rows(
            self.root / "data/interim/15_funding_or_support_edges_sample_v0.csv",
            "edge_id",
        )
        first_log = read_rows(
            self.root / "data/interim/human_review_log_v0.csv",
            "task_id",
        )

        apply_hr033(self.root)
        second_relations = read_rows(
            self.root / "data/interim/15_funding_or_support_edges_sample_v0.csv",
            "edge_id",
        )
        second_log = read_rows(
            self.root / "data/interim/human_review_log_v0.csv",
            "task_id",
        )
        self.assertEqual(first_relations, second_relations)
        self.assertEqual(first_log, second_log)
        self.assertIn("HR-033", second_log)


if __name__ == "__main__":
    unittest.main()
