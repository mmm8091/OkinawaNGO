from __future__ import annotations

import csv
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.reconcile_rca063_post_hr018 import reconcile_rca063


ROOT = Path(__file__).resolve().parents[1]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


class ReconcileRCA063PostHR018Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        for relative in (
            "data/interim/38_report_claim_evidence_audit_v1.csv",
            "data/interim/21_admin_collaboration_relations_v0.csv",
            "outputs/report_claim_audit_v1/publication_blockers_v1.csv",
            "outputs/report_claim_audit_v1/red_line_scan_v1.csv",
            "outputs/report_claim_audit_v1/report_claim_audit_summary_v1.md",
            "outputs/report_claim_audit_v1/validation_report_v1.json",
            "outputs/report_claim_audit_v1/fig_claim_publish_status_v1.svg",
            "outputs/report_claim_audit_v1/README.md",
            "outputs/phase1_visuals_v1/fig3_support_service_layers_strict.svg",
            "outputs/R10_administrative_collaboration_v0/fig_r10_mechanism_ecology.svg",
            "outputs/R10_administrative_collaboration_v0/fig_r10_amount_evidence_boundary.svg",
        ):
            destination = self.root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / relative, destination)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_reconciles_only_released_blocker_and_preserves_other_claims(self) -> None:
        claims_path = (
            self.root / "data/interim/38_report_claim_evidence_audit_v1.csv"
        )
        before = {
            row["claim_id"]: row
            for row in read_rows(claims_path)
            if row["claim_id"] != "RCA063"
        }

        result = reconcile_rca063(self.root)

        claims = read_rows(claims_path)
        after = {
            row["claim_id"]: row
            for row in claims
            if row["claim_id"] != "RCA063"
        }
        self.assertEqual(before, after)
        rca063 = next(row for row in claims if row["claim_id"] == "RCA063")
        self.assertEqual("revise", rca063["publish_status"])
        self.assertEqual("post_HR018_current_render", rca063["review_layer"])
        self.assertIn("7 dyadic", rca063["claim_text"])
        self.assertIn("16 displayed records", rca063["claim_text"])
        self.assertIn("not a funding network", rca063["limitations"])

        self.assertEqual(
            {"safe": 71, "revise": 7, "block": 0},
            result["publish_status"],
        )
        self.assertEqual([], read_rows(
            self.root
            / "outputs/report_claim_audit_v1/publication_blockers_v1.csv"
        ))
        red_lines = {
            row["scan_id"]: row
            for row in read_rows(
                self.root / "outputs/report_claim_audit_v1/red_line_scan_v1.csv"
            )
        }
        self.assertEqual("pass", red_lines["RCR006"]["result"])

        validation = json.loads(
            (
                self.root
                / "outputs/report_claim_audit_v1/validation_report_v1.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(0, validation["publication_blocker_count"])
        self.assertEqual(
            {"safe": 71, "revise": 7, "block": 0},
            validation["publish_status"],
        )
        summary = (
            self.root
            / "outputs/report_claim_audit_v1/report_claim_audit_summary_v1.md"
        ).read_text(encoding="utf-8")
        self.assertIn("safe 71 / revise 7 / block 0", summary)
        self.assertIn("16 条记录不是 16 条组织关系边", summary)

    def test_is_idempotent(self) -> None:
        reconcile_rca063(self.root)
        tracked = (
            "data/interim/38_report_claim_evidence_audit_v1.csv",
            "outputs/report_claim_audit_v1/publication_blockers_v1.csv",
            "outputs/report_claim_audit_v1/red_line_scan_v1.csv",
            "outputs/report_claim_audit_v1/report_claim_audit_summary_v1.md",
            "outputs/report_claim_audit_v1/validation_report_v1.json",
            "outputs/report_claim_audit_v1/fig_claim_publish_status_v1.svg",
            "outputs/report_claim_audit_v1/README.md",
        )
        first = {
            relative: (self.root / relative).read_bytes()
            for relative in tracked
        }
        reconcile_rca063(self.root)
        self.assertEqual(
            first,
            {
                relative: (self.root / relative).read_bytes()
                for relative in tracked
            },
        )


if __name__ == "__main__":
    unittest.main()
