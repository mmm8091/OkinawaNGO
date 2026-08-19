import importlib.util
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "us_origin_scope",
    ROOT / "scripts/make_us_origin_scope_overlay_v1.py",
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


class UsOriginScopeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = MODULE.build_rows()

    def test_exact_scope(self):
        self.assertEqual(len(self.rows), 17)
        self.assertEqual(len({row["actor_id"] for row in self.rows}), 17)

    def test_expected_group_counts(self):
        self.assertEqual(
            Counter(row["analytical_group"] for row in self.rows),
            Counter(
                {
                    "service_charity_comparison": 9,
                    "accountability_comparison": 6,
                    "public_diplomacy_program_node": 1,
                    "funder_watchlist_node": 1,
                }
            ),
        )

    def test_registry_origin_and_tombstone_boundary(self):
        self.assertTrue(all(row["origin_type"] == "us_origin" for row in self.rows))
        self.assertNotIn("A072", {row["actor_id"] for row in self.rows})

    def test_no_actor_stance_or_human_decision(self):
        self.assertTrue(all(not row["human_decision"] for row in self.rows))
        self.assertTrue(all("not a fixed pro-/anti-U.S." in row["interpretation_limit"] for row in self.rows))


if __name__ == "__main__":
    unittest.main()
