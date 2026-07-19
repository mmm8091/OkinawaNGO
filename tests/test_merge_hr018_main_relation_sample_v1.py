from __future__ import annotations

import csv
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.merge_hr018_main_relation_sample_v1 import (
    apply_hr018_main_relation_sample,
)


ROOT = Path(__file__).resolve().parents[1]
PROTECTED_HR033 = {"F006", "F007", "F021", "F022", "F023", "F025"}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


class MergeHr018MainRelationSampleV1Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        for relative in (
            "data/interim/15_funding_or_support_edges_sample_v0.csv",
            "data/interim/21_admin_collaboration_relations_v0.csv",
            "outputs/R10_administrative_collaboration_v0/"
            "HR018_relation_review_v0.csv",
        ):
            destination = self.root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / relative, destination)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_syncs_main_sample_and_preserves_hr033(self) -> None:
        central = (
            self.root / "data/interim/15_funding_or_support_edges_sample_v0.csv"
        )
        before = {row["edge_id"]: row for row in read_rows(central)}
        protected_before = {
            edge_id: before[edge_id].copy() for edge_id in PROTECTED_HR033
        }

        summary = apply_hr018_main_relation_sample(self.root)

        rows = read_rows(central)
        by_id = {row["edge_id"]: row for row in rows}
        self.assertEqual(43, len(rows))
        self.assertEqual(11, summary["updated_main_edges"])
        for edge_id in PROTECTED_HR033:
            for field, value in protected_before[edge_id].items():
                self.assertEqual(value, by_id[edge_id][field])

        for edge_id in ("F031", "F032", "F033", "F034"):
            self.assertEqual("human_checked", by_id[edge_id]["review_status"])
        self.assertEqual("human_revised", by_id["F035"]["review_status"])
        self.assertEqual(
            "P_R10_USO_INDO_PACIFIC", by_id["F035"]["target_actor_id"]
        )
        self.assertEqual("research_lead", by_id["F035"]["graph_eligibility"])

        self.assertEqual("human_revised", by_id["F024"]["review_status"])
        self.assertEqual(
            "historical_membership", by_id["F024"]["temporal_status"]
        )
        self.assertEqual("2012;2015", by_id["F024"]["observed_active_at"])
        self.assertEqual("no", by_id["F024"]["needs_local_retrieval"])

        self.assertEqual("よみたん救護園", by_id["F028"]["target_display_name"])
        self.assertEqual("2000000", by_id["F028"]["amount"])
        self.assertEqual(
            "in_kind_item_value_not_cash", by_id["F028"]["amount_semantics"]
        )
        self.assertEqual(
            "社会福祉法人うるま市社会福祉協議会",
            by_id["F029"]["target_display_name"],
        )
        self.assertEqual("", by_id["F029"]["amount"])
        self.assertEqual(
            "in_kind_acquisition_assistance", by_id["F030"]["relation_type"]
        )
        self.assertEqual("", by_id["F030"]["event_date"])
        self.assertEqual(
            "joint_in_kind_contribution", by_id["F036"]["relation_type"]
        )
        self.assertEqual(
            "one_of_four_named_contributing_groups", by_id["F036"]["source_role"]
        )

        self.assertEqual(
            "needs_local_retrieval", by_id["F027"]["review_status"]
        )
        self.assertEqual(
            "aggregate_observation", by_id["F027"]["graph_eligibility"]
        )
        self.assertEqual("800000000", by_id["F027"]["amount"])

    def test_is_idempotent(self) -> None:
        apply_hr018_main_relation_sample(self.root)
        central = (
            self.root / "data/interim/15_funding_or_support_edges_sample_v0.csv"
        )
        first = central.read_bytes()
        apply_hr018_main_relation_sample(self.root)
        self.assertEqual(first, central.read_bytes())


if __name__ == "__main__":
    unittest.main()
