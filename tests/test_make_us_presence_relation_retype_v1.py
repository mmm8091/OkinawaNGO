import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "relation_retype",
    ROOT / "scripts/make_us_presence_relation_retype_v1.py",
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


class RelationRetypeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = MODULE.read_csv(MODULE.INPUT)
        cls.rows = MODULE.build_rows(cls.source)

    def test_exact_43_row_crosswalk(self):
        self.assertEqual(len(self.source), 43)
        self.assertEqual(len(self.rows), 43)
        self.assertEqual(len({row["edge_id"] for row in self.rows}), 43)

    def test_no_decision_or_fact_upgrade(self):
        self.assertTrue(all(not row["mapping_decision"] for row in self.rows))
        self.assertTrue(
            all("preserve_original_fact_review" in row["fact_status_carry_rule"] for row in self.rows)
        )

    def test_six_mapping_rules_cover_all_rows(self):
        self.assertEqual(
            {row["mapping_rule_id"] for row in self.rows},
            set(MODULE.RULE_ID_BY_TABLE.values()),
        )

    def test_opportunity_and_rejected_do_not_enter_fact_tables(self):
        by_id = {row["edge_id"]: row for row in self.rows}
        self.assertEqual(by_id["F012"]["proposed_usn_table_id"], "LEAD")
        self.assertEqual(by_id["F008"]["proposed_usn_table_id"], "EXCLUDE")

    def test_in_kind_and_membership_are_separate_layers(self):
        by_id = {row["edge_id"]: row for row in self.rows}
        self.assertEqual(by_id["F028"]["proposed_usn_table_id"], "USN04")
        self.assertEqual(by_id["F006"]["proposed_usn_table_id"], "USN05")

    def test_non_actor_endpoints_are_gated(self):
        by_id = {row["edge_id"]: row for row in self.rows}
        self.assertIn("typed_non_actor_endpoint", by_id["F003"]["endpoint_gate"])
        self.assertIn("resolve_via_USN08", by_id["F027"]["endpoint_gate"])


if __name__ == "__main__":
    unittest.main()
