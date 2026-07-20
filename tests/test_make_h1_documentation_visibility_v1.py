from __future__ import annotations

import csv
import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "make_h1_documentation_visibility_v1",
    ROOT / "scripts" / "make_h1_documentation_visibility_v1.py",
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class H1DocumentationVisibilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.actors, cls.edges, cls.sources = MODULE.load_current_inputs()
        cls.scenarios = MODULE.build_scenarios(cls.actors, cls.edges)
        cls.by_id = {row["scenario_id"]: row for row in cls.scenarios}

    def test_current_gate_uses_121_actors_and_238_active_edges(self) -> None:
        self.assertEqual(len(self.actors), 121)
        self.assertEqual(len(self.edges), 238)
        self.assertNotIn("A072", {row["actor_id"] for row in self.actors})
        self.assertTrue(
            all(row["analysis_inclusion"] == "active" for row in self.edges)
        )

        baseline = self.by_id["BASE_CURRENT_E3PLUS"]
        self.assertEqual(baseline["edge_count"], "234")
        self.assertEqual(baseline["observed_actor_count"], "101")

    def test_source_and_actor_deletion_scenarios_are_paired(self) -> None:
        expected = {
            "SOURCE_DROP_S003": ("227", "97"),
            "SOURCE_DROP_S004": ("193", "76"),
            "SOURCE_DROP_S006": ("234", "101"),
            "SOURCE_DROP_BIG3": ("185", "71"),
            "ACTOR_DROP_A005": ("232", "100"),
            "ACTOR_DROP_A004": ("232", "100"),
            "ACTOR_DROP_A001": ("231", "100"),
            "ACTOR_DROP_BIG3": ("227", "98"),
        }
        for scenario_id, (edges, actors) in expected.items():
            with self.subTest(scenario_id=scenario_id):
                row = self.by_id[scenario_id]
                self.assertEqual(row["edge_count"], edges)
                self.assertEqual(row["observed_actor_count"], actors)
                self.assertEqual(row["display_tier"], "research")
                self.assertEqual(row["claim_status"], "candidate")

    def test_source_deletion_preserves_multi_source_and_no_source_edges(self) -> None:
        fixtures = [
            {
                "edge_id": "E1",
                "actor_id": "A1",
                "evidence_level": "E4",
                "source_ref": "S004",
            },
            {
                "edge_id": "E2",
                "actor_id": "A2",
                "evidence_level": "E4",
                "source_ref": "S004;S999",
            },
            {
                "edge_id": "E3",
                "actor_id": "A3",
                "evidence_level": "E4",
                "source_ref": "",
            },
        ]
        selected = MODULE.select_scenario_edges(
            fixtures,
            evidence_gate=MODULE.E3PLUS,
            dropped_sources={"S004"},
        )
        self.assertEqual({"E2", "E3"}, {row["edge_id"] for row in selected})

    def test_all_source_leave_one_out_and_drilldown_expose_s004_dominance(self) -> None:
        loo = MODULE.build_leave_one_source_out(self.edges, self.sources)
        by_source = {row["source_id"]: row for row in loo}
        self.assertEqual("41", by_source["S004"]["removed_edge_count"])
        self.assertEqual("25", by_source["S004"]["lost_observed_actor_count"])
        self.assertEqual("1", by_source["S004"]["removed_edge_rank_desc"])
        self.assertEqual("0", by_source["S006"]["removed_edge_count"])
        self.assertTrue(
            all(row["comparison_unit"] == "one_source_id" for row in loo)
        )

        removed = MODULE.build_scenario_removed_edges(self.edges)
        s004 = [
            row for row in removed if row["scenario_id"] == "SOURCE_DROP_S004"
        ]
        self.assertEqual(41, len(s004))
        self.assertEqual(25, len({row["actor_id"] for row in s004}))
        self.assertTrue(
            all(row["removal_reason"] == "all_stated_support_exhausted" for row in s004)
        )

    def test_unknown_and_proposal_fields_are_not_promoted_to_facts(self) -> None:
        proposals = MODULE.build_source_host_proposals(self.actors, self.sources)
        self.assertEqual(
            {
                (row["source_id"], row["proposed_host_actor_id"])
                for row in proposals
            },
            {("S003", "A005"), ("S004", "A004"), ("S006", "A001")},
        )
        self.assertTrue(
            all(
                row["mapping_status"] == "proposal_not_human_reviewed"
                and row["producer_role_status"] == "unknown"
                and row["self_produced_or_external"] == "unknown"
                and row["source_language"] == "unknown"
                for row in proposals
            )
        )

        incidence = MODULE.build_actor_source_incidence(
            self.actors,
            self.sources,
            proposals,
        )
        self.assertEqual(len(incidence), 212)
        self.assertEqual(
            sum(row["source_resolution_status"] == "resolved_source_id" for row in incidence),
            204,
        )
        self.assertTrue(
            all(
                row["producer_role_status"] in {"unknown", "proposal_not_human_reviewed"}
                and row["self_produced_or_external"] == "unknown"
                and row["source_language"] == "unknown"
                for row in incidence
            )
        )

    def test_main_writes_research_only_metrics_and_roundtrips(self) -> None:
        MODULE.main()
        output = ROOT / "outputs" / "research_wave_h1_documentation_visibility_v1"
        with (output / "metrics_v1.json").open(encoding="utf-8") as handle:
            metrics = json.load(handle)
        self.assertEqual(metrics["layer"]["display_tier"], "research")
        self.assertEqual(metrics["layer"]["claim_status"], "candidate")
        self.assertEqual(metrics["current_gate"]["actor_count"], 121)
        self.assertEqual(metrics["current_gate"]["active_actor_issue_edge_count"], 238)
        self.assertEqual(
            12,
            metrics["actor_issue_edge_source_incidence"][
                "edge_without_resolved_source_id_count"
            ],
        )
        brief = (output / "brief_v1.md").read_text(encoding="utf-8")
        self.assertIn(
            "有 12 条没有可解析的 `S` 来源",
            brief,
        )

        with (output / "sensitivity_scenarios_v1.csv").open(
            encoding="utf-8-sig",
            newline="",
        ) as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(rows, MODULE.build_scenarios(self.actors, self.edges))
        with (output / "further_research_queue_v1.csv").open(
            encoding="utf-8-sig",
            newline="",
        ) as handle:
            tasks = list(csv.DictReader(handle))
        self.assertGreaterEqual(len(tasks), 5)
        self.assertTrue(all(row["status"] == "open" for row in tasks))


if __name__ == "__main__":
    unittest.main()
