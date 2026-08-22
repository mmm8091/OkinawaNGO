from __future__ import annotations

import csv
import unittest
from pathlib import Path

from scripts.validate_us_presence_network_wave2_w2_c_nonentry_v1 import OUT, TEMPLATE, validate


def rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


class W2CNonentryPackageTests(unittest.TestCase):
    def test_validator_passes(self) -> None:
        errors, checks = validate()
        self.assertEqual(errors, [])
        self.assertEqual(checks["status"], "PASS")

    def test_arm_is_not_established_and_outcome_has_no_rows(self) -> None:
        arm = rows(OUT / "arm_status_v1.csv")
        self.assertEqual(len(arm), 1)
        self.assertEqual(arm[0]["status"], "arm_not_established")
        self.assertEqual(arm[0]["admitted_rows"], "0")
        self.assertEqual(rows(OUT / "outcome_table_v1.csv"), [])

    def test_2004_case_is_gate_control_not_nonentry(self) -> None:
        candidates = {row["candidate_id"]: row for row in rows(OUT / "candidate_screen_v1.csv")}
        case = candidates["W2CNE-C001"]
        self.assertEqual(case["admission_status"], "exclude_gate_control_only")
        self.assertEqual(case["processing_observed"], "receipt_and_three_committee_meetings")

    def test_2018_refusal_is_not_promoted(self) -> None:
        candidates = {row["candidate_id"]: row for row in rows(OUT / "candidate_screen_v1.csv")}
        self.assertEqual(
            candidates["W2CNE-C002"]["admission_status"],
            "exclude_unmatched_and_source_gate",
        )

    def test_unexpected_findings_header_matches_template(self) -> None:
        with TEMPLATE.open("r", encoding="utf-8-sig", newline="") as handle:
            expected = next(csv.reader(handle))
        with (OUT / "unexpected_findings_register_v1.csv").open(
            "r", encoding="utf-8-sig", newline=""
        ) as handle:
            actual = next(csv.reader(handle))
        self.assertEqual(actual, expected)

    def test_no_scoped_row_can_write_or_publish(self) -> None:
        for name in (
            "selection_rules_v1.csv",
            "candidate_screen_v1.csv",
            "arm_status_v1.csv",
            "gate_control_comparison_v1.csv",
            "negative_search_log_v1.csv",
            "source_receipts_v1.csv",
        ):
            for row in rows(OUT / name):
                self.assertEqual(row["package_scope"], "research_only")
                self.assertEqual(row["frontend_status"], "not_frontend_ready")
                self.assertEqual(row["central_writeback"], "no")


if __name__ == "__main__":
    unittest.main()
