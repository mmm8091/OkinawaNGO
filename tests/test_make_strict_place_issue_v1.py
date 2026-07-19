import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "make_strict_place_issue_v1",
    ROOT / "scripts" / "make_strict_place_issue_v1.py",
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


class StrictPlaceIssueGateTests(unittest.TestCase):
    def test_rejected_or_deactivated_rows_are_excluded(self):
        for row in (
            {"review_status": "rejected"},
            {"claim_status": "unsupported"},
            {"graph_eligibility": "excluded"},
            {"scope_status": "retired_duplicate"},
            {"scope_status": "deactivated_until_direct_evidence"},
            {"scope_status": "event_specific_excluded_from_default_okinawa_narrative"},
        ):
            self.assertFalse(MODULE.active_edge(row))

    def test_bounded_candidate_remains_available(self):
        self.assertTrue(
            MODULE.active_edge(
                {
                    "review_status": "needs_second_source",
                    "claim_status": "candidate",
                    "graph_eligibility": "research_lead",
                    "scope_status": "source_id_integration_pending",
                }
            )
        )


if __name__ == "__main__":
    unittest.main()
