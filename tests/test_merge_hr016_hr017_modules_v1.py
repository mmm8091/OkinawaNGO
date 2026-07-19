from __future__ import annotations

import csv
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.merge_hr016_hr017_modules_v1 import merge_hr016_hr017_modules


ROOT = Path(__file__).resolve().parents[1]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def clear_fields(path: Path, fields_to_clear: set[str]) -> None:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = list(reader.fieldnames or [])
        rows = list(reader)
    for row in rows:
        for field in fields_to_clear:
            if field in row:
                row[field] = ""
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


class MergeHR016HR017ModulesV1Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        for relative in (
            "outputs/principal_review_merge_v1/principal_decision_overlay_v1.csv",
            "outputs/R04_sakishima_frame_corpus_v0/actor_frame_event_candidates_v0.csv",
            "outputs/R04_sakishima_frame_corpus_v0/source_excerpt_locators_v0.csv",
            "outputs/R04_sakishima_frame_corpus_v0/online_evidence_safe_sources_v0.csv",
            "outputs/R04_sakishima_frame_corpus_v0/human_review_queue_v0.csv",
            "outputs/R04_sakishima_frame_corpus_v0/source_review_queue_v0.csv",
            "outputs/R04_sakishima_frame_corpus_v0/reject_log_v0.csv",
            "outputs/R04_sakishima_frame_corpus_v0/source_reject_log_v0.csv",
            "outputs/R04_sakishima_frame_corpus_v0/hr016_review_items_v0.csv",
            "data/interim/19_sakishima_frame_corpus_v0.csv",
            "outputs/R09_referendum_process_v0/process_stages_reviewed_all_v0.csv",
            "outputs/R09_referendum_process_v0/actor_process_roles_reviewed_all_v0.csv",
            "outputs/R09_referendum_process_v0/source_register_v0.csv",
            "outputs/R09_referendum_process_v0/case_summary_v0.csv",
            "outputs/R09_referendum_process_v0/hr017_review_queue_v0.csv",
            "data/interim/20_referendum_process_stages_v0.csv",
            "outputs/R09_referendum_process_v0/actor_process_roles_v0.csv",
        ):
            destination = self.root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / relative, destination)
        clear_fields(
            self.root
            / "outputs/R04_sakishima_frame_corpus_v0/hr016_review_items_v0.csv",
            {
                "review_decision",
                "human_reviewer",
                "review_date",
                "review_note",
                "approved_formulation",
                "scope_boundary",
                "decision_source_report",
            },
        )
        clear_fields(
            self.root
            / "outputs/R09_referendum_process_v0/hr017_review_queue_v0.csv",
            {
                "decision",
                "human_reviewer",
                "review_date",
                "decision_note",
                "approved_formulation",
                "scope_boundary",
                "decision_source_report",
            },
        )

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_merges_hr016_semantics_without_actorizing_bounded_speakers(self) -> None:
        summary = merge_hr016_hr017_modules(self.root, render_figures=False)
        self.assertEqual(19, summary["r04_formal_facts"])
        self.assertEqual(24, summary["r04_safe_sources"])
        self.assertEqual(0, summary["r04_open_fact_items"])
        self.assertEqual(0, summary["r04_open_source_items"])
        ledger = read_rows(
            self.root
            / "outputs/R04_sakishima_frame_corpus_v0/hr016_review_items_v0.csv"
        )
        self.assertEqual(12, sum(bool(row["review_decision"]) for row in ledger))

        facts = read_rows(self.root / "data/interim/19_sakishima_frame_corpus_v0.csv")
        by_id = {row["fact_id"]: row for row in facts}
        self.assertEqual(
            "PROV_R4_611_EXECUTIVE_COMMITTEE",
            by_id["R4E001"]["entity_id_or_provisional"],
        )
        self.assertNotEqual("A012", by_id["R4E001"]["entity_id_or_provisional"])
        self.assertEqual(
            "EVENT_R4S015_ANONYMOUS_COMMENT_UNITS",
            by_id["R4E016"]["entity_id_or_provisional"],
        )
        self.assertEqual("non_actor_event_evidence", by_id["R4E016"]["entity_status"])
        self.assertEqual("Sakishima", by_id["R4E025"]["place"])
        self.assertEqual("F_FTE", by_id["R4E024"]["frame_code"])
        self.assertEqual(
            {"R4E009A", "R4E009B"},
            {row["fact_id"] for row in facts if row["fact_id"].startswith("R4E009")},
        )
        self.assertNotIn(
            "RESIDENTS_ISHIGAKI",
            {row["entity_id_or_provisional"] for row in facts},
        )

        r4e007 = by_id["R4E007"]
        self.assertIn("R4S007", r4e007["source_ref"].split(";"))
        sources = {
            row["corpus_source_id"]: row
            for row in read_rows(
                self.root
                / "outputs/R04_sakishima_frame_corpus_v0/online_evidence_safe_sources_v0.csv"
            )
        }
        self.assertEqual(
            "印刷 pp.27–29；Pattern 1 摘要 p.27，正文 p.28，实施要领记载例 p.29",
            sources["R4S007"]["locator"],
        )
        self.assertNotIn("procedural_fairness", sources["R4S024"]["frame_candidates"])
        self.assertIn("government response", sources["R4S002"]["speaker_or_owner"])

    def test_merges_only_online_hr017_and_preserves_nine_local_items(self) -> None:
        summary = merge_hr016_hr017_modules(self.root, render_figures=False)
        self.assertEqual(29, summary["r09_formal_stages"])
        self.assertEqual(29, summary["r09_formal_roles"])
        self.assertEqual(9, summary["r09_open_local_items"])

        stages = read_rows(
            self.root / "outputs/R09_referendum_process_v0/process_stages_reviewed_all_v0.csv"
        )
        by_id = {row["stage_id"]: row for row in stages}
        self.assertEqual("2021-04-26", by_id["R9ST027"]["date_start"])
        self.assertEqual("day", by_id["R9ST027"]["date_precision"])
        self.assertIn("三名", by_id["R9ST027"]["process_action"])
        self.assertIn("全部却下", by_id["R9ST030"]["outcome"])
        self.assertIn("各控诉", by_id["R9ST031"]["outcome"])
        self.assertNotIn("不受理", by_id["R9ST032"]["outcome"])
        self.assertNotIn("棄却", by_id["R9ST032"]["outcome"])

        roles = read_rows(
            self.root
            / "outputs/R09_referendum_process_v0/actor_process_roles_reviewed_all_v0.csv"
        )
        role_by_id = {row["role_id"]: row for row in roles}
        self.assertEqual("A068", role_by_id["R9R001"]["actor_id"])
        self.assertEqual("registry_actor", role_by_id["R9R001"]["entity_kind"])
        self.assertEqual("", role_by_id["R9R030"]["actor_id"])
        self.assertNotEqual("A011", role_by_id["R9R030"]["actor_id"])

        queue = read_rows(
            self.root / "outputs/R09_referendum_process_v0/hr017_review_queue_v0.csv"
        )
        self.assertEqual(9, sum(bool(row["decision"]) for row in queue))
        self.assertEqual(
            {
                "R9ST007",
                "R9ST010",
                "R9ST012",
                "R9ST033",
                "R9R006",
                "R9R007",
                "R9R008",
                "R9R020",
                "R9R029",
            },
            {row["object_id"] for row in queue if not row["decision"]},
        )

    def test_is_idempotent(self) -> None:
        first = merge_hr016_hr017_modules(self.root, render_figures=False)
        tracked = (
            "data/interim/19_sakishima_frame_corpus_v0.csv",
            "outputs/R04_sakishima_frame_corpus_v0/online_evidence_safe_sources_v0.csv",
            "data/interim/20_referendum_process_stages_v0.csv",
            "outputs/R09_referendum_process_v0/actor_process_roles_v0.csv",
            "outputs/R09_referendum_process_v0/hr017_review_queue_v0.csv",
        )
        first_bytes = {path: (self.root / path).read_bytes() for path in tracked}
        second = merge_hr016_hr017_modules(self.root, render_figures=False)
        self.assertEqual(first, second)
        self.assertEqual(
            first_bytes,
            {path: (self.root / path).read_bytes() for path in tracked},
        )


if __name__ == "__main__":
    unittest.main()
