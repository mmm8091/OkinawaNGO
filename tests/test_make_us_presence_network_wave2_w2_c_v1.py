from __future__ import annotations

import csv
import importlib.util
import io
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "make_us_presence_network_wave2_w2_c_v1.py"
TEMPLATE = ROOT / "data" / "metadata" / "unexpected_findings_register_template_v1.csv"
VALIDATOR = ROOT / "scripts" / "validate_research_work_package_v1.py"
OUT = ROOT / "outputs" / "us_presence_network_wave2_w2_c_v1"
SPEC = importlib.util.spec_from_file_location("w2c_builder", SCRIPT)
assert SPEC and SPEC.loader
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)


class W2CBuilderTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tables = BUILDER.build_tables()
        cls.checks = BUILDER.validate(cls.tables)

    def test_selected_comparison_frame_and_parallel_axes(self) -> None:
        comparisons = self.tables["selected_episode_comparison_frame_v1.csv"][0]
        outcomes = self.tables["accountability_outcome_ledger_v1.csv"][0]
        self.assertEqual(13, len(comparisons))
        self.assertEqual({f"TE{i:02d}" for i in range(1, 14)}, {row["episode_id"] for row in comparisons})
        self.assertEqual(14, len({row["analysis_unit_id"] for row in outcomes}))
        self.assertEqual(126, len(outcomes))
        self.assertEqual(set(BUILDER.AXES), {row["axis"] for row in outcomes})
        self.assertEqual({"selected_comparison_axis"}, {row["selection_condition"] for row in outcomes})
        self.assertTrue(all(row["entry_status_at_selection"] for row in outcomes))

    def test_te10_to_te13_review_and_entry_boundaries(self) -> None:
        comparisons = {row["episode_id"]: row for row in self.tables["selected_episode_comparison_frame_v1.csv"][0]}
        outcomes = self.tables["accountability_outcome_ledger_v1.csv"][0]
        for episode_id in {"TE10", "TE11", "TE12", "TE13"}:
            self.assertEqual("pending_event_human_review", comparisons[episode_id]["event_review_gate"])
            self.assertTrue(all(row["evidence_status"] == "candidate_event_pending_human_review" for row in outcomes if row["episode_id"] == episode_id))
        for episode_id in {"TE12", "TE13"}:
            self.assertIn("without_independent_institutional_entry", comparisons[episode_id]["episode_frame_role"])

    def test_awase_is_split_and_judgment_level_candidate_is_bounded(self) -> None:
        outcomes = self.tables["accountability_outcome_ledger_v1.csv"][0]
        te06_units = {row["analysis_unit_id"] for row in outcomes if row["episode_id"] == "TE06"}
        self.assertEqual({"TE06-W1", "TE06-W2"}, te06_units)
        yes_axes = {
            row["axis"]
            for row in outcomes
            if row["analysis_unit_id"] == "TE06-W1" and row["axis_status"] == "yes_bounded"
        }
        self.assertEqual({"PROJECT_BUDGET", "PROJECT_AUTHORITY"}, yes_axes)
        awase_rows = [
            row
            for row in outcomes
            if row["analysis_unit_id"] == "TE06-W1" and row["axis"] in yes_axes
        ]
        self.assertTrue(all("Judgment-level outcome only" in row["allowed_claim"] for row in awase_rows))
        self.assertTrue(all("pending principal confirmation" in row["allowed_claim"] for row in awase_rows))

    def test_gate_control_frame_is_not_a_matched_nonentry_arm(self) -> None:
        controls = {row["control_id"]: row for row in self.tables["gate_control_frame_v1.csv"][0]}
        self.assertEqual(6, len(controls))
        self.assertTrue(all(row["true_matched_nonentry_arm_status"] == "not_established" for row in controls.values()))
        self.assertEqual("yes_heard", controls["W2C-GC003"]["entry_status"])
        self.assertEqual("route_matched_judicial_gate_control", controls["W2C-GC006"]["frame_fit"])

    def test_project_change_and_attribution_are_independent(self) -> None:
        projects = {row["project_change_id"]: row for row in self.tables["project_change_attribution_frame_v1.csv"][0]}
        self.assertEqual("candidate_judgment_level_link_pending_principal", projects["W2C-PC001"]["attribution_status"])
        self.assertEqual("candidate_bounded_judgment_outcome_pending_principal", projects["W2C-PC001"]["candidate_disposition"])
        self.assertEqual("chronology_not_causal", projects["W2C-PC002"]["attribution_status"])
        self.assertEqual("no_civic_change_confirmed", projects["W2C-PC006"]["attribution_status"])
        self.assertIn("Do not infer", projects["W2C-PC002"]["prohibited_inference"])

    def test_resource_semantics_remain_unreconciled(self) -> None:
        rows = {row["w2_00_anchor_ids"]: row for row in self.tables["resource_anchor_crosswalk_v1.csv"][0]}
        self.assertEqual("USD 276,345.50", rows["W2C-A020"]["value_text"])
        self.assertEqual("USD 280,000.00", rows["W2C-A021"]["value_text"])
        self.assertEqual("USD 3,654.50", rows["W2C-A022"]["value_text"])
        self.assertEqual("about JPY 930bn", rows["W2C-A030"]["value_text"])
        self.assertIn("not expenditure", rows["W2C-A030"]["preserved_semantics"])
        self.assertIn("Reporter premise only", rows["W2C-A041"]["preserved_semantics"])

    def test_receipt_crosswalk_and_hashes_close(self) -> None:
        self.assertTrue(any("bidirectionally" in item for item in self.checks))

    def test_review_queue_has_no_prefilled_human_decision(self) -> None:
        queue = self.tables["principal_review_queue_v1.csv"][0]
        self.assertTrue(queue)
        for row in queue:
            self.assertEqual("", row["human_decision"])
            self.assertEqual("", row["human_reviewer"])
            self.assertEqual("", row["review_date"])
            self.assertEqual("no", row["central_writeback"])
        self.assertTrue(any(row["unit_ids"] == "FRAME-DESIGN" for row in queue))
        awase = next(row for row in queue if row["unit_ids"] == "TE06-W1")
        self.assertIn("judgment-level outcome candidates", awase["review_question"])

    def test_obsolete_misleading_frames_are_not_generated(self) -> None:
        self.assertFalse(set(BUILDER.OBSOLETE_OUTPUTS) & set(self.tables))
        text = "\n".join(
            str(value)
            for rows, _ in self.tables.values()
            for row in rows
            for value in row.values()
        )
        for prohibited in ("direct_official_bounded", "confirmed_bounded_counterexample", "real counterexample", "USF-W2C-ENTRY13"):
            self.assertNotIn(prohibited, text)

    def test_unexpected_findings_register_is_header_only_and_protocol_valid(self) -> None:
        payloads = BUILDER.payloads()
        register = payloads["unexpected_findings_register_v1.csv"]
        generated_rows = list(csv.reader(io.StringIO(register)))
        with TEMPLATE.open("r", encoding="utf-8-sig", newline="") as handle:
            template_rows = list(csv.reader(handle))
        self.assertEqual(template_rows, generated_rows)
        self.assertEqual(1, len(generated_rows))
        self.assertIn("## 意外发现登记", payloads["README.md"])
        self.assertIn("validate_research_work_package_v1.py", payloads["README.md"])

        subprocess.run([sys.executable, str(SCRIPT)], cwd=ROOT, check=True, capture_output=True, text=True)
        result = subprocess.run(
            [sys.executable, str(VALIDATOR), str(OUT)],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, result.returncode, result.stderr)


if __name__ == "__main__":
    unittest.main()
