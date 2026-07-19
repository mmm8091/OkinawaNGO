import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "make_r01_r02_actor_issue",
    ROOT / "scripts" / "make_r01_r02_actor_issue.py",
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


class ScopeClassificationTests(unittest.TestCase):
    def test_human_reviewed_case_scope_overrides_text_heuristic(self):
        scope, rule = MODULE.classify_scope(
            {
                "scope_kind": "case",
                "scope_review_status": "human_checked",
                "relation_basis": "mission and long-running activity",
            }
        )
        self.assertEqual(scope, "institutional_or_case_role")
        self.assertIn("human-reviewed", rule)

    def test_human_reviewed_remain_unclear_stays_unclear(self):
        scope, _ = MODULE.classify_scope(
            {
                "scope_kind": "remain_unclear",
                "scope_review_status": "human_checked",
                "relation_basis": "mission",
            }
        )
        self.assertEqual(scope, "mixed_or_unclear")


if __name__ == "__main__":
    unittest.main()
