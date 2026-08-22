from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path

from scripts.validate_research_work_package_v1 import REQUIRED_COLUMNS, validate_package


class ResearchWorkPackageProtocolTests(unittest.TestCase):
    def make_package(self, rows: list[dict[str, str]]) -> Path:
        root = Path(tempfile.mkdtemp())
        (root / "README.md").write_text("# Package\n\n## 意外发现登记\n\n本轮登记。\n", encoding="utf-8")
        with (root / "unexpected_findings_register_v1.csv").open(
            "w", encoding="utf-8", newline=""
        ) as handle:
            writer = csv.DictWriter(handle, fieldnames=REQUIRED_COLUMNS)
            writer.writeheader()
            writer.writerows(rows)
        return root

    def row(self, lead_id: str, kind: str, step: int, parent: str = "") -> dict[str, str]:
        return {
            "lead_id": lead_id,
            "package_id": "TEST",
            "record_kind": kind,
            "chain_id": "CHAIN-1",
            "parent_lead_id": parent,
            "recon_step": str(step),
            "discovered_on": "2026-08-22",
            "lead_title": "Unexpected item",
            "observation": "A bounded observation.",
            "why_unexpected": "Outside the package question.",
            "source_or_query_locator": "S001 p.1",
            "next_test": "Check an independent record.",
            "potential_value": "Could motivate a separate comparison.",
            "stop_reason": "The current bounded check is complete.",
            "workflow_status": "lead_only",
            "claim_eligibility": "no",
            "central_writeback": "no",
            "human_review_trigger": "no",
            "publication_eligibility": "no",
        }

    def test_header_only_register_is_valid(self) -> None:
        self.assertEqual(validate_package(self.make_package([])), [])

    def test_three_step_chain_is_valid(self) -> None:
        rows = [
            self.row("L0", "origin_observation", 0),
            self.row("L1", "followup_observation", 1, "L0"),
            self.row("L2", "followup_observation", 2, "L1"),
            self.row("L3", "followup_observation", 3, "L2"),
        ]
        self.assertEqual(validate_package(self.make_package(rows)), [])

    def test_fourth_step_and_publishable_lead_are_rejected(self) -> None:
        rows = [
            self.row("L0", "origin_observation", 0),
            self.row("L1", "followup_observation", 1, "L0"),
            self.row("L2", "followup_observation", 2, "L1"),
            self.row("L3", "followup_observation", 3, "L2"),
            self.row("L4", "followup_observation", 4, "L3"),
        ]
        rows[-1]["publication_eligibility"] = "yes"
        errors = validate_package(self.make_package(rows))
        self.assertTrue(any("outside 0..3" in error for error in errors))
        self.assertTrue(any("publication_eligibility" in error for error in errors))

    def test_more_than_ten_rows_is_rejected(self) -> None:
        rows = [self.row(f"L{i}", "origin_observation", 0) for i in range(11)]
        errors = validate_package(self.make_package(rows))
        self.assertTrue(any("maximum 10" in error for error in errors))

    def test_non_integer_step_reports_error_without_crashing(self) -> None:
        rows = [
            self.row("L0", "origin_observation", 0),
            self.row("L1", "followup_observation", 1, "L0"),
        ]
        rows[1]["recon_step"] = "unknown"
        errors = validate_package(self.make_package(rows))
        self.assertTrue(any("must be an integer" in error for error in errors))

    def test_terminal_observation_requires_stop_reason(self) -> None:
        rows = [self.row("L0", "origin_observation", 0)]
        rows[0]["stop_reason"] = ""
        errors = validate_package(self.make_package(rows))
        self.assertTrue(any("requires stop_reason" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
