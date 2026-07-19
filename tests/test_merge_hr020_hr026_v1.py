from __future__ import annotations

import csv
import shutil
import tempfile
import unittest
from collections import Counter
from pathlib import Path

from scripts.merge_hr020_hr026_v1 import merge_hr020_hr026


ROOT = Path(__file__).resolve().parents[1]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


class MergeHr020Hr026V1Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        for relative in (
            "data/interim/01_actor_registry_initial_v0.csv",
            "data/interim/25_coaction_event_participation_v0.csv",
            "data/interim/33_r09_election_civic_events_v1.csv",
            "outputs/R05_coaction_v1/hr020_review_queue_v0.csv",
            "outputs/R09_election_civic_interface_v1/HR026_election_civic_role_review_v0.csv",
            "outputs/R09_election_civic_interface_v1/source_proposals_v1.csv",
            "outputs/R09_election_civic_interface_v1/online_gap_register_v1.csv",
            "outputs/principal_review_merge_v1/principal_decision_overlay_v1.csv",
        ):
            destination = self.root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / relative, destination)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_hr020_applies_identity_decisions_without_actorizing_event_only_names(
        self,
    ) -> None:
        summary = merge_hr020_hr026(self.root, render_figures=False)
        self.assertEqual(14, summary["hr020_decisions"])
        self.assertEqual(169, summary["r5_participation_rows"])
        self.assertEqual(6, summary["r5_event_only_repeat_bridges"])
        self.assertEqual(21, summary["r5_strict_repeat_bridges"])

        rows = read_rows(
            self.root / "data/interim/25_coaction_event_participation_v0.csv"
        )
        by_key = {row["participant_key"]: row for row in rows}
        self.assertEqual(
            "沖縄国際人権法研究会",
            by_key["EV2020_OEJP_MMC_71:P012"]["canonical_name"],
        )
        self.assertEqual(
            "All Okinawa Council for Human Rights (AOCHR)",
            by_key["EV2020_OEJP_MMC_71:P012"]["source_name"],
        )
        self.assertEqual("", by_key["EV2020_OEJP_MMC_71:P012"]["actor_id"])
        self.assertEqual("", by_key["EV2020_OEJP_MMC_71:P044"]["actor_id"])
        self.assertEqual("", by_key["EV2020_OEJP_MMC_71:P065"]["actor_id"])
        self.assertEqual("", by_key["EV2020_OEJP_MMC_71:P068"]["actor_id"])
        self.assertEqual("A110", by_key["EV2020_OEJP_MMC_71:P051"]["actor_id"])

        osaka_2010 = by_key["EV2010_WWF_67:P018"]
        osaka_2020 = by_key["EV2020_OEJP_MMC_71:P068"]
        self.assertEqual(
            "The Association for Military Base Free Peaceful Okinawa",
            osaka_2020["source_name"],
        )
        self.assertEqual(osaka_2010["identity_group_id"], osaka_2020["identity_group_id"])
        self.assertTrue(osaka_2010["identity_group_id"].startswith("EO_R5_"))

        parent = by_key["EV2010_WWF_67:P013"]
        team = by_key["EV2020_OEJP_MMC_71:P009"]
        self.assertNotEqual(parent["identity_group_id"], team["identity_group_id"])
        self.assertEqual(
            "北限のジュゴン調査チーム・ザン", team["canonical_name"]
        )
        self.assertEqual(
            "human_checked_source_segmentation",
            by_key["EV2010_WWF_67:P060"]["event_observation_status"],
        )
        self.assertEqual(
            "human_checked_source_segmentation",
            by_key["EV2010_WWF_67:P061"]["event_observation_status"],
        )
        self.assertFalse(any(row["identity_status"] == "alias_pending" for row in rows))

        bridges = read_rows(
            self.root
            / "outputs/R05_coaction_v1/repeat_participation_bridges_v0.csv"
        )
        self.assertEqual(
            6,
            sum(row["identity_scope"] == "human_reviewed_event_only" for row in bridges),
        )
        self.assertFalse(any(row["actor_id"] in {"A008", "A054", "A072", "A106"} for row in bridges))

    def test_hr026_applies_all_decisions_and_keeps_announced_event_out_of_held_count(
        self,
    ) -> None:
        summary = merge_hr020_hr026(self.root, render_figures=False)
        self.assertEqual(19, summary["hr026_decisions"])
        self.assertEqual(18, summary["r9_confirmed_observed_actions"])
        self.assertEqual(1, summary["r9_announced_not_occurrence_verified"])

        rows = read_rows(
            self.root / "data/interim/33_r09_election_civic_events_v1.csv"
        )
        by_id = {row["record_id"]: row for row in rows}
        self.assertEqual(
            Counter(
                {
                    "endorsement": 4,
                    "issue_campaign": 4,
                    "observation": 5,
                    "public_meeting": 2,
                    "request": 4,
                }
            ),
            Counter(row["action_type"] for row in rows),
        )
        self.assertTrue(all(row["review_status"] == "human_checked" for row in rows))
        self.assertEqual("A059", by_id["R9EC001"]["registry_crosswalk"])
        self.assertIn("R9EC_S022", by_id["R9EC001"]["source_proposal_ids"])
        self.assertEqual("2018-09-12", by_id["R9EC011"]["event_date_start"])
        self.assertEqual("2018-09-19", by_id["R9EC011"]["event_date_end"])
        self.assertEqual("day_range", by_id["R9EC011"]["date_precision"])
        self.assertEqual(
            "announced_not_occurrence_verified", by_id["R9EC018"]["event_status"]
        )
        self.assertNotIn("Held", by_id["R9EC018"]["observable_action"])
        self.assertEqual("主催者未確認", by_id["R9EC019"]["actor_name"])
        self.assertEqual(
            "unidentified_organizer_event_record",
            by_id["R9EC019"]["entity_boundary"],
        )
        self.assertFalse(any(row["registry_crosswalk"] == "A115" for row in rows))

        sources = read_rows(
            self.root
            / "outputs/R09_election_civic_interface_v1/source_proposals_v1.csv"
        )
        source = next(row for row in sources if row["proposal_id"] == "R9EC_S022")
        self.assertEqual("no", source["relation_or_claim_approved"])

    def test_merge_is_idempotent(self) -> None:
        first = merge_hr020_hr026(self.root, render_figures=False)
        paths = (
            self.root / "data/interim/25_coaction_event_participation_v0.csv",
            self.root / "outputs/R05_coaction_v1/repeat_participation_bridges_v0.csv",
            self.root / "data/interim/33_r09_election_civic_events_v1.csv",
            self.root
            / "outputs/R09_election_civic_interface_v1/intervention_mode_counts_v1.csv",
            self.root
            / "outputs/principal_review_merge_v1/HR020_HR026_merge_report_v1.md",
        )
        first_bytes = {path: path.read_bytes() for path in paths}
        second = merge_hr020_hr026(self.root, render_figures=False)
        self.assertEqual(first, second)
        self.assertEqual(first_bytes, {path: path.read_bytes() for path in paths})


if __name__ == "__main__":
    unittest.main()
