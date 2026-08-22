from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "make_us_presence_network_wave2_w2_c_v1.py"
SPEC = importlib.util.spec_from_file_location("w2c_builder", SCRIPT)
assert SPEC and SPEC.loader
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)


class W2CBuilderTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tables = BUILDER.build_tables()
        cls.checks = BUILDER.validate(cls.tables)

    def test_fixed_frame_and_parallel_axes(self) -> None:
        positive = self.tables["positive_entry_sample_v1.csv"][0]
        outcomes = self.tables["accountability_outcome_ledger_v1.csv"][0]
        self.assertEqual(13, len(positive))
        self.assertEqual({f"TE{i:02d}" for i in range(1, 14)}, {row["episode_id"] for row in positive})
        self.assertEqual(14, len({row["analysis_unit_id"] for row in outcomes}))
        self.assertEqual(126, len(outcomes))
        self.assertEqual(set(BUILDER.AXES), {row["axis"] for row in outcomes})

    def test_awase_is_split_and_counterexample_is_bounded(self) -> None:
        outcomes = self.tables["accountability_outcome_ledger_v1.csv"][0]
        te06_units = {row["analysis_unit_id"] for row in outcomes if row["episode_id"] == "TE06"}
        self.assertEqual({"TE06-W1", "TE06-W2"}, te06_units)
        yes_axes = {
            row["axis"]
            for row in outcomes
            if row["analysis_unit_id"] == "TE06-W1" and row["axis_status"] == "yes_bounded"
        }
        self.assertEqual({"PROJECT_BUDGET", "PROJECT_AUTHORITY"}, yes_axes)

    def test_negative_frame_does_not_mislabel_entered_cases(self) -> None:
        negative = {row["negative_id"]: row for row in self.tables["nonentry_negative_sample_v1.csv"][0]}
        self.assertTrue(negative["W2C-NEG003"]["inclusion_status"].startswith("excluded_from_strict"))
        self.assertEqual("yes_heard", negative["W2C-NEG003"]["entry_status"])
        self.assertEqual("strict_matched_judicial_gate", negative["W2C-NEG006"]["frame_fit"])

    def test_project_change_and_attribution_are_independent(self) -> None:
        projects = {row["project_change_id"]: row for row in self.tables["project_change_counterexample_sample_v1.csv"][0]}
        self.assertEqual("direct_official_bounded", projects["W2C-PC001"]["attribution_status"])
        self.assertEqual("chronology_not_causal", projects["W2C-PC002"]["attribution_status"])
        self.assertEqual("no_civic_change_confirmed", projects["W2C-PC006"]["attribution_status"])
        self.assertIn("Do not infer", projects["W2C-PC002"]["prohibited_inference"])

    def test_resource_semantics_remain_unreconciled(self) -> None:
        rows = {row["w2_00_anchor_ids"]: row for row in self.tables["resource_anchor_crosswalk_v1.csv"][0]}
        self.assertEqual("USD 276,345.50", rows["W2C-A020"]["value_text"])
        self.assertEqual("USD 280,000.00", rows["W2C-A021"]["value_text"])
        self.assertEqual("USD 3,654.50", rows["W2C-A022"]["value_text"])
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


if __name__ == "__main__":
    unittest.main()
