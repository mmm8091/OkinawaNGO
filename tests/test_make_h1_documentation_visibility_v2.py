from __future__ import annotations

import csv
import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "research_wave_h1_documentation_visibility_v2"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


class H1DocumentationVisibilityV2Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        subprocess.run(
            [sys.executable, "scripts/make_h1_documentation_visibility_v2.py"],
            cwd=ROOT,
            check=True,
        )

    def test_current_input_boundaries(self) -> None:
        metrics = json.loads((OUT / "metrics_v2.json").read_text(encoding="utf-8"))
        counts = metrics["counts"]
        self.assertEqual(counts["current_actors"], 121)
        self.assertEqual(counts["sources"], 295)
        self.assertEqual(counts["active_actor_issue_edges"], 238)
        self.assertEqual(counts["reviewed_actor_issue_edges"], 65)
        self.assertEqual(counts["candidate_actor_issue_edges"], 173)
        self.assertEqual(counts["e3plus_actor_issue_edges"], 234)
        self.assertEqual(counts["strict_triples"], 312)
        self.assertEqual(counts["human_checked_registered_actor_event_rows"], 50)
        self.assertEqual(counts["accepted_registered_actor_case_roles"], 13)
        self.assertEqual(counts["reviewed_typed_dyadic_relations"], 14)
        self.assertEqual(counts["unresolved_reference_actors"], 9)
        self.assertEqual(counts["unresolved_zero_linked_s_source_actors"], 6)

    def test_research_gate_and_actor_uniqueness(self) -> None:
        actors = read_csv(OUT / "actor_documentation_visibility_v2.csv")
        self.assertEqual(len(actors), 121)
        self.assertEqual(len({row["actor_id"] for row in actors}), 121)
        self.assertNotIn("A072", {row["actor_id"] for row in actors})
        for row in actors:
            self.assertEqual(row["research_status"], "research_only")
            self.assertEqual(row["frontend_eligibility"], "not_frontend_ready")
            self.assertIn("must not be summed", row["graph_object_boundary"])

    def test_graph_objects_are_separate(self) -> None:
        rows = read_csv(OUT / "graph_object_summary_v2.csv")
        self.assertEqual(
            {row["graph_object"] for row in rows},
            {
                "actor_issue_bipartite",
                "strict_same_source_triples",
                "event_hyperedge_incidence",
                "reviewed_typed_dyadic",
                "accepted_case_role_incidence",
            },
        )
        event = next(
            row for row in rows if row["graph_object"] == "event_hyperedge_incidence"
        )
        case = next(
            row
            for row in rows
            if row["graph_object"] == "accepted_case_role_incidence"
        )
        self.assertIn("projection prohibited", event["projection_status"])
        self.assertIn("no co-party", case["projection_status"])

    def test_construction_diagnostic_and_primary_proxies(self) -> None:
        rows = read_csv(OUT / "association_estimates_v2.csv")
        degree = next(row for row in rows if row["analysis_id"] == "H1A001")
        between = next(row for row in rows if row["analysis_id"] == "H1A002")
        registry = next(row for row in rows if row["analysis_id"] == "H1A016")
        excluded = next(row for row in rows if row["analysis_id"] == "H1A017")
        self.assertEqual(degree["spearman_rho"], "0.331")
        self.assertEqual(between["spearman_rho"], "0.215")
        self.assertEqual(degree["diagnostic_role"], "construction_diagnostic")
        self.assertEqual(registry["spearman_rho"], "0.257")
        self.assertEqual(registry["diagnostic_role"], "primary_registry_proxy")
        self.assertEqual(excluded["spearman_rho"], "-0.138")
        self.assertEqual(
            excluded["diagnostic_role"], "primary_outcome_excluded_proxy"
        )
        self.assertEqual(
            registry["subset"], "resolved_reference_actors_only"
        )
        svg = (OUT / "fig_graph_objects_v2.svg").read_text(encoding="utf-8")
        self.assertIn("outcome-excluded ρ = -0.138", svg)
        self.assertIn("全层 238；图内 228", svg)
        self.assertIn('transform="translate(37,350.0) rotate(-90)"', svg)
        self.assertIn('transform="translate(37,895.0) rotate(-90)"', svg)
        self.assertIn(
            "construction diagnostic",
            (OUT / "method_brief_v2.md").read_text(encoding="utf-8"),
        )

    def test_review_layers_and_unresolved_crosswalk_are_explicit(self) -> None:
        rows = read_csv(OUT / "review_layer_sensitivity_v2.csv")
        all_rows = [
            row for row in rows if row["subset"] == "all_current_actors"
        ]
        resolved = [
            row
            for row in rows
            if row["subset"] == "resolved_reference_actors_only"
        ]
        self.assertEqual(len(all_rows), 9)
        self.assertEqual(len(resolved), 9)
        self.assertEqual(
            {row["actor_issue_layer"] for row in all_rows},
            {"active_238", "reviewed_65", "candidate_173"},
        )
        self.assertEqual(
            next(
                row
                for row in resolved
                if row["actor_issue_layer"] == "reviewed_65"
                and row["x_measure"] == "registry_source_count"
            )["spearman_rho"],
            "0.525",
        )
        self.assertEqual(
            next(
                row
                for row in resolved
                if row["actor_issue_layer"] == "candidate_173"
                and row["x_measure"] == "registry_source_count"
            )["spearman_rho"],
            "-0.169",
        )
        unresolved = read_csv(OUT / "unresolved_reference_audit_v2.csv")
        self.assertEqual(len(unresolved), 9)
        self.assertEqual(
            sum(int(row["linked_s_source_count"]) == 0 for row in unresolved),
            6,
        )
        self.assertTrue(
            all(
                row["resolution_decision"]
                == "exclude_from_primary_source-proxy sensitivity"
                for row in unresolved
            )
        )
        svg = (OUT / "fig_actor_issue_strata_v2.svg").read_text(
            encoding="utf-8"
        )
        self.assertIn("已核 65＋候选 173", svg)
        self.assertIn("全层 173", svg)

    def test_s004_and_deletion_units(self) -> None:
        rows = read_csv(OUT / "sensitivity_scenarios_v2.csv")
        s004 = next(row for row in rows if row["scenario_id"] == "SRC_NO_S004")
        self.assertEqual(
            int(s004["baseline_edge_count"]) - int(s004["edge_count"]),
            41,
        )
        families = {row["scenario_family"] for row in rows}
        self.assertEqual(
            families, {"source_support_deletion", "actor_node_deletion"}
        )
        self.assertTrue(
            all(
                row["graph_object"] == "actor_issue_e3plus_bipartite"
                for row in rows
                if row["scenario_family"] == "source_support_deletion"
            )
        )
        self.assertTrue(
            all(
                row["graph_object"] == "actor_issue_active_bipartite"
                for row in rows
                if row["scenario_family"] == "actor_node_deletion"
            )
        )

    def test_matched_and_negative_cases_are_bounded(self) -> None:
        pairs = read_csv(OUT / "matched_actor_pairs_v2.csv")
        summaries = read_csv(OUT / "matched_pair_summary_v2.csv")
        negatives = read_csv(OUT / "negative_case_audit_v2.csv")
        self.assertEqual(
            len(
                [
                    row
                    for row in pairs
                    if row["match_universe"] == "resolved_reference_actors"
                ]
            ),
            12,
        )
        connected = next(
            row
            for row in summaries
            if row["match_universe"]
            == "resolved_actor_issue_connected_only"
            and row["outcome_measure"] == "active_actor_issue_degree"
        )
        self.assertEqual(connected["pair_count"], "10")
        self.assertEqual(connected["mean_dense_minus_thin"], "0.7")
        contrast_types = {row["contrast_type"] for row in negatives}
        self.assertEqual(
            contrast_types,
            {
                "dense_registry_trace_low_actor_issue_degree",
                "thin_registry_trace_high_actor_issue_visibility",
            },
        )
        self.assertTrue(
            all(
                "registry_source_count" in row["match_selection_rule"]
                for row in pairs
            )
        )

    def test_method_literature_has_non_transfer_boundaries(self) -> None:
        rows = read_csv(OUT / "method_literature_v2.csv")
        self.assertEqual(len(rows), 2)
        self.assertEqual(
            {row["doi"] for row in rows},
            {
                "10.1371/journal.pcsy.0000042",
                "10.1093/acprof:oso/9780198719571.003.0016",
            },
        )
        self.assertTrue(all(row["non_transfer_boundary"] for row in rows))

    def test_figures_and_docs_exist(self) -> None:
        for stem in (
            "fig_graph_objects_v2",
            "fig_actor_issue_strata_v2",
            "fig_actor_issue_sensitivity_v2",
        ):
            self.assertGreater((OUT / f"{stem}.svg").stat().st_size, 4_000)
            self.assertGreater((OUT / f"{stem}.html").stat().st_size, 5_000)
        for name in (
            "README.md",
            "method_brief_v2.md",
            "principal_checkpoint_v2.md",
            "validation_report_v2.md",
        ):
            self.assertGreater((OUT / name).stat().st_size, 500)

    def test_every_row_level_output_keeps_research_gate(self) -> None:
        for path in OUT.glob("*.csv"):
            rows = read_csv(path)
            self.assertTrue(rows, path.name)
            self.assertTrue(
                all(row.get("research_status") == "research_only" for row in rows),
                path.name,
            )
            self.assertTrue(
                all(
                    row.get("frontend_eligibility") == "not_frontend_ready"
                    for row in rows
                ),
                path.name,
            )


if __name__ == "__main__":
    unittest.main()
