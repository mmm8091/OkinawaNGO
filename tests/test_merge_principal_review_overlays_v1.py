from __future__ import annotations

import csv
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.merge_principal_review_overlays_v1 import apply_principal_review_overlays


ROOT = Path(__file__).resolve().parents[1]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


class MergePrincipalReviewOverlaysV1Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        for relative in (
            "outputs/principal_review_merge_v1/principal_decision_overlay_v1.csv",
            "outputs/principal_review_merge_v1/source_metadata_overlay_v1.csv",
            "outputs/R04_sakishima_frame_corpus_v0/hr016_review_items_v0.csv",
            "outputs/R09_referendum_process_v0/hr017_review_queue_v0.csv",
            "outputs/R10_administrative_collaboration_v0/HR018_source_prerequisites_v0.csv",
            "outputs/R10_administrative_collaboration_v0/HR018_relation_review_v0.csv",
            "outputs/R01_R02_actor_issue_v1/HR019/HR019_review_v0.csv",
            "outputs/R01_R02_actor_issue_v1/HR019/HR019_bridge_actor_review_queue_v0.csv",
            "outputs/R01_R02_actor_issue_v1/HR019/HR019_edge_scope_review_queue_v0.csv",
            "outputs/R05_coaction_v1/hr020_review_queue_v0.csv",
            "outputs/R06_R07_R11_pathways_v1/HR021_review_items_v0.csv",
            "outputs/edge_activation_v1/HR024_edge_activation_review_v0.csv",
            "outputs/R03_spatial_dossier_v1/HR025_actor_place_semantics_review_v0.csv",
            "outputs/R09_election_civic_interface_v1/HR026_election_civic_role_review_v0.csv",
            "outputs/R10_official_collaboration_universe_v1/HR032_partner_alias_crosswalk_review_v1.csv",
            "outputs/phase1_source_integration_v1/HR022_source_metadata_review_v0.csv",
            "outputs/next_wave_source_integration_v1/HR030_source_metadata_archive_review_v0.csv",
        ):
            destination = self.root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / relative, destination)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_backfills_all_completed_decisions_and_preserves_open_items(self) -> None:
        summary = apply_principal_review_overlays(self.root)

        self.assertEqual(273, summary["principal_decisions_applied"])
        self.assertEqual(71, summary["source_metadata_decisions_applied"])

        hr017 = read_rows(
            self.root / "outputs/R09_referendum_process_v0/hr017_review_queue_v0.csv"
        )
        self.assertEqual(9, sum(bool(row["decision"]) for row in hr017))
        local_open = {
            "R9ST007",
            "R9ST010",
            "R9ST012",
            "R9ST033",
            "R9R006",
            "R9R007",
            "R9R008",
            "R9R020",
            "R9R029",
        }
        self.assertEqual(
            local_open,
            {row["object_id"] for row in hr017 if not row["decision"]},
        )

        hr024 = read_rows(
            self.root / "outputs/edge_activation_v1/HR024_edge_activation_review_v0.csv"
        )
        self.assertEqual(7, sum(bool(row["decision"]) for row in hr024))
        a073 = next(row for row in hr024 if row["task_id"] == "HR024-001")
        self.assertEqual("", a073["decision"])

        hr025 = read_rows(
            self.root
            / "outputs/R03_spatial_dossier_v1/HR025_actor_place_semantics_review_v0.csv"
        )
        self.assertEqual(47, sum(bool(row["decision"]) for row in hr025))

        hr018_relations = read_rows(
            self.root
            / "outputs/R10_administrative_collaboration_v0/HR018_relation_review_v0.csv"
        )
        row_21 = next(
            row for row in hr018_relations if row["review_item_id"] == "HR-018-21"
        )
        self.assertEqual("deferred_local_or_internal_record", row_21["decision"])
        self.assertIn("HR033", row_21["scope_boundary"])

    def test_source_metadata_overlay_populates_exact_queue_counts(self) -> None:
        apply_principal_review_overlays(self.root)

        hr022 = read_rows(
            self.root
            / "outputs/phase1_source_integration_v1/HR022_source_metadata_review_v0.csv"
        )
        hr030 = read_rows(
            self.root
            / "outputs/next_wave_source_integration_v1/HR030_source_metadata_archive_review_v0.csv"
        )
        self.assertEqual(49, sum(bool(row["decision"]) for row in hr022))
        self.assertEqual(22, sum(bool(row["decision"]) for row in hr030))
        self.assertEqual(
            {"accept_with_revision"},
            {row["decision"] for row in hr022},
        )
        self.assertEqual(
            {"accept", "accept_with_revision"},
            {row["decision"] for row in hr030},
        )

    def test_is_idempotent(self) -> None:
        first = apply_principal_review_overlays(self.root)
        path = (
            self.root
            / "outputs/R01_R02_actor_issue_v1/HR019/HR019_edge_scope_review_queue_v0.csv"
        )
        first_bytes = path.read_bytes()
        second = apply_principal_review_overlays(self.root)
        self.assertEqual(first, second)
        self.assertEqual(first_bytes, path.read_bytes())


if __name__ == "__main__":
    unittest.main()
