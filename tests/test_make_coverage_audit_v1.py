import csv
import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "make_coverage_audit_v1",
    ROOT / "scripts" / "make_coverage_audit_v1.py",
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class CoverageCurrentLayerTests(unittest.TestCase):
    def test_select_current_layers_excludes_history_only_rows(self) -> None:
        actor_history = [
            {
                "actor_id": "A001",
                "scope_status": "core",
                "merged_duplicate_of": "",
            },
            {
                "actor_id": "A072",
                "scope_status": "merged_duplicate",
                "merged_duplicate_of": "A071",
            },
        ]
        issue_history = [
            {"actor_id": "A001", "analysis_inclusion": "active"},
            {"actor_id": "A072", "analysis_inclusion": "excluded"},
        ]
        place_history = [
            {
                "actor_id": "A001",
                "place_name": "Henoko",
                "graph_eligibility": "eligible",
            },
            {
                "actor_id": "A072",
                "place_name": "Okinawa Prefecture",
                "graph_eligibility": "excluded",
            },
        ]

        actors, issues, places = MODULE.select_current_layers(
            actor_history,
            issue_history,
            place_history,
        )

        self.assertEqual([row["actor_id"] for row in actors], ["A001"])
        self.assertEqual([row["actor_id"] for row in issues], ["A001"])
        self.assertEqual([row["actor_id"] for row in places], ["A001"])

    def test_a072_is_never_current_even_if_tombstone_fields_are_missing(self) -> None:
        self.assertFalse(
            MODULE.is_active_actor(
                {
                    "actor_id": "A072",
                    "scope_status": "",
                    "merged_duplicate_of": "",
                }
            )
        )

    def test_report_traceability_uses_layered_issue_input_for_coverage(self) -> None:
        trace_spec = importlib.util.spec_from_file_location(
            "make_report_traceability_crosswalk_v1",
            ROOT / "scripts" / "make_report_traceability_crosswalk_v1.py",
        )
        trace_module = importlib.util.module_from_spec(trace_spec)
        assert trace_spec.loader is not None
        trace_spec.loader.exec_module(trace_module)

        route = next(
            row
            for row in trace_module.ROUTES
            if row["prefix"] == "outputs/coverage_audit_v1/"
        )
        self.assertIn("24_r01_r02_actor_issue_layered_v0.csv", route["data"])
        self.assertNotIn("07_actor_issue_edges_initial_v0.csv", route["data"])

    def test_f033_records_current_and_history_boundaries(self) -> None:
        with (
            ROOT / "outputs" / "report_assembly_v1" / "figure_manifest_v1.csv"
        ).open(encoding="utf-8-sig", newline="") as handle:
            row = next(
                item
                for item in csv.DictReader(handle)
                if item["asset_id"] == "F033"
            )

        self.assertIn("121 actors", row["fact_layer"])
        self.assertIn("238 actor-issue", row["fact_layer"])
        self.assertIn("130 actor-place", row["fact_layer"])
        self.assertIn("122／248／135", row["fact_layer"])

        caption = (
            ROOT / "outputs" / "report_assembly_v1" / "caption_bank_v1.md"
        ).read_text(encoding="utf-8-sig")
        start = caption.index("### F033")
        end = caption.index("### F035", start)
        f033 = caption[start:end]
        for value in ("121", "238", "130", "122／248／135"):
            self.assertIn(value, f033)
        self.assertNotIn("118", f033)
        self.assertNotIn("129", f033)


if __name__ == "__main__":
    unittest.main()
