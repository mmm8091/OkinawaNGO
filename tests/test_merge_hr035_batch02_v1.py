from __future__ import annotations

import csv
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.merge_hr035_batch02_v1 import apply_hr035_batch02


ROOT = Path(__file__).resolve().parents[1]


def read_index(path: Path, key: str) -> dict[str, dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return {row[key]: row for row in csv.DictReader(handle)}


def rewrite_cell(
    path: Path, key: str, key_value: str, field: str, value: str
) -> None:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = list(reader.fieldnames or [])
        rows = list(reader)
    for row in rows:
        if row[key] == key_value:
            row[field] = value
            break
    else:
        raise AssertionError(f"{key_value} not found")
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


class MergeHr035Batch02V1Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        for relative in (
            "data/interim/01_actor_registry_initial_v0.csv",
            "data/interim/07_actor_issue_edges_initial_v0.csv",
            "data/interim/05_source_log_initial_v0.csv",
            "outputs/actor_issue_claim_freeze_v1/"
            "HR035_actor_issue_fact_review_batch02_v1.csv",
            "outputs/actor_issue_claim_freeze_v1/"
            "HR035_actor_identity_companion_batch02_v1.csv",
        ):
            destination = self.root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / relative, destination)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_merges_principal_confirmed_identity_and_fact_decisions(self) -> None:
        summary = apply_hr035_batch02(self.root)

        actors = read_index(
            self.root / "data/interim/01_actor_registry_initial_v0.csv",
            "actor_id",
        )
        edges = read_index(
            self.root / "data/interim/07_actor_issue_edges_initial_v0.csv",
            "edge_id",
        )

        self.assertEqual(23, summary["principal_decisions"])
        self.assertEqual("human_revised", actors["A007"]["review_status"])
        self.assertEqual(
            "nonprofit_form_unresolved", actors["A007"]["legal_status_guess"]
        )
        self.assertEqual("human_checked", edges["AI040"]["review_status"])
        self.assertEqual("supported_bounded", edges["AI040"]["claim_status"])
        self.assertEqual("project_principal_user", edges["AI040"]["human_reviewer"])

    def test_preserves_deferred_facts_and_applies_source_and_scope_corrections(
        self,
    ) -> None:
        apply_hr035_batch02(self.root)

        actors = read_index(
            self.root / "data/interim/01_actor_registry_initial_v0.csv",
            "actor_id",
        )
        edges = read_index(
            self.root / "data/interim/07_actor_issue_edges_initial_v0.csv",
            "edge_id",
        )
        self.assertEqual(
            {
                "A007": "S005",
                "A017": "S022",
                "A018": "S023",
                "A049": "S039",
                "A066": "S032",
            },
            {
                actor_id: actors[actor_id]["source_refs"]
                for actor_id in ("A007", "A017", "A018", "A049", "A066")
            },
        )
        for edge_id in ("AI157", "AI158"):
            self.assertEqual("needs_second_source", edges[edge_id]["review_status"])
            self.assertEqual("defer", edges[edge_id]["human_decision"])
            self.assertEqual("candidate", edges[edge_id]["claim_status"])
            self.assertNotEqual(
                "reviewed_actor_issue", edges[edge_id]["graph_eligibility"]
            )

        self.assertEqual("S023", edges["AI044"]["source_ref"])
        self.assertEqual("S024", edges["AI044"]["invalidated_source_ref"])
        for edge_id in ("AI016", "AI233"):
            self.assertEqual("event_specific", edges[edge_id]["scope_kind"])
            self.assertEqual("human_revised", edges[edge_id]["scope_review_status"])
            self.assertEqual(
                f"HR035-B02-{edge_id}", edges[edge_id]["scope_review_task_id"]
            )

    def test_refuses_an_incomplete_or_unconfirmed_return_before_writing(self) -> None:
        actor_path = self.root / "data/interim/01_actor_registry_initial_v0.csv"
        edge_path = self.root / "data/interim/07_actor_issue_edges_initial_v0.csv"
        actor_before = actor_path.read_bytes()
        edge_before = edge_path.read_bytes()
        review_path = (
            self.root
            / "outputs/actor_issue_claim_freeze_v1/"
            "HR035_actor_issue_fact_review_batch02_v1.csv"
        )
        rewrite_cell(
            review_path,
            "edge_id",
            "AI040",
            "reviewed_fields",
            "",
        )

        with self.assertRaisesRegex(ValueError, "incomplete fields"):
            apply_hr035_batch02(self.root)

        self.assertEqual(actor_before, actor_path.read_bytes())
        self.assertEqual(edge_before, edge_path.read_bytes())

    def test_is_byte_idempotent_and_leaves_every_non_target_row_unchanged(
        self,
    ) -> None:
        actor_path = self.root / "data/interim/01_actor_registry_initial_v0.csv"
        edge_path = self.root / "data/interim/07_actor_issue_edges_initial_v0.csv"
        actors_before = read_index(actor_path, "actor_id")
        edges_before = read_index(edge_path, "edge_id")

        apply_hr035_batch02(self.root)
        actors_after = read_index(actor_path, "actor_id")
        edges_after = read_index(edge_path, "edge_id")
        for actor_id in set(actors_before) - {"A007", "A017", "A018", "A049", "A066"}:
            self.assertEqual(actors_before[actor_id], actors_after[actor_id])
        for edge_id in set(edges_before) - {
            "AI016",
            "AI040",
            "AI042",
            "AI044",
            "AI119",
            "AI121",
            "AI157",
            "AI158",
            "AI159",
            "AI223",
            "AI225",
            "AI226",
            "AI232",
            "AI233",
            "AI234",
            "AI236",
            "AI237",
            "AI240",
        }:
            self.assertEqual(edges_before[edge_id], edges_after[edge_id])

        tracked = (
            actor_path,
            edge_path,
            self.root
            / "outputs/hr035_batch02_integration_v1/merge_manifest_v1.csv",
            self.root
            / "outputs/hr035_batch02_integration_v1/validation_report_v1.md",
        )
        first_bytes = {path: path.read_bytes() for path in tracked}
        apply_hr035_batch02(self.root)
        self.assertEqual(first_bytes, {path: path.read_bytes() for path in tracked})

    def test_refuses_crosswalk_or_source_drift_before_writing(self) -> None:
        actor_path = self.root / "data/interim/01_actor_registry_initial_v0.csv"
        edge_path = self.root / "data/interim/07_actor_issue_edges_initial_v0.csv"
        actor_before = actor_path.read_bytes()
        edge_before = edge_path.read_bytes()
        review_path = (
            self.root
            / "outputs/actor_issue_claim_freeze_v1/"
            "HR035_actor_issue_fact_review_batch02_v1.csv"
        )

        rewrite_cell(review_path, "edge_id", "AI040", "actor_id", "A999")
        with self.assertRaisesRegex(ValueError, "crosswalk mismatch"):
            apply_hr035_batch02(self.root)
        self.assertEqual(actor_before, actor_path.read_bytes())
        self.assertEqual(edge_before, edge_path.read_bytes())

        rewrite_cell(review_path, "edge_id", "AI040", "actor_id", "A017")
        rewrite_cell(review_path, "edge_id", "AI040", "source_ref", "S999")
        with self.assertRaisesRegex(ValueError, "unknown source refs"):
            apply_hr035_batch02(self.root)
        self.assertEqual(actor_before, actor_path.read_bytes())
        self.assertEqual(edge_before, edge_path.read_bytes())

    def test_validation_report_uses_the_current_active_edge_gate(self) -> None:
        apply_hr035_batch02(self.root)
        report = (
            self.root
            / "outputs/hr035_batch02_integration_v1/validation_report_v1.md"
        ).read_text(encoding="utf-8")

        self.assertIn("283 active rows", report)
        self.assertIn("141 human-reviewed / 142 candidate", report)


if __name__ == "__main__":
    unittest.main()
