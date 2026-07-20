import csv
import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "make_h2_two_ecologies_v1",
    ROOT / "scripts" / "make_h2_two_ecologies_v1.py",
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def hash_tree(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(
            path.read_bytes()
        ).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


class H2TwoEcologiesResearchPackageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.inputs = MODULE.load_inputs()
        cls.analysis = MODULE.build_analysis(cls.inputs)
        MODULE.validate_analysis(cls.analysis)

    def test_service_core_is_rule_derived_and_exactly_nine_existing_ids(self):
        observed = MODULE.derive_service_core(self.inputs["registry"])
        self.assertEqual(MODULE.EXPECTED_SERVICE_CORE_IDS, observed)
        self.assertEqual(9, len(observed))

        registry = {row["actor_id"]: row for row in self.inputs["registry"]}
        for actor_id in observed:
            self.assertIn(actor_id, registry)
            self.assertIn(
                registry[actor_id]["actor_class"],
                MODULE.SERVICE_CORE_CLASSES,
            )
            self.assertEqual("us_origin", registry[actor_id]["origin_type"])
            self.assertTrue(MODULE.is_active_actor(registry[actor_id]))

    def test_accountability_group_is_rule_based_and_excludes_non_civic_nodes(self):
        metrics = self.analysis["metrics"]
        self.assertEqual(65, metrics["accountability_comparison_actor_count"])
        self.assertEqual(
            18,
            metrics["accountability_human_reviewed_anchor_actor_count"],
        )
        self.assertEqual(
            47,
            metrics["accountability_candidate_only_anchor_actor_count"],
        )
        self.assertEqual(0, metrics["actor_set_overlap_count"])

        selected = {
            row["actor_id"] for row in self.analysis["accountability"]
        }
        registry = {row["actor_id"]: row for row in self.inputs["registry"]}
        current_issues = [
            row
            for row in self.inputs["issues"]
            if row["analysis_inclusion"] == "active"
        ]
        for actor_id in selected:
            self.assertNotIn(
                registry[actor_id]["actor_class"],
                MODULE.NON_CIVIC_COMPARISON_CLASSES,
            )
            self.assertNotIn(
                registry[actor_id]["actor_class"],
                MODULE.SERVICE_CORE_CLASSES,
            )
            self.assertTrue(
                any(
                    row["actor_id"] == actor_id
                    and row["issue_id"]
                    in MODULE.ACCOUNTABILITY_ANCHOR_ISSUE_IDS
                    for row in current_issues
                )
            )
        self.assertNotIn("A074", selected)
        self.assertNotIn("A075", selected)

    def test_current_counts_and_zero_record_boundaries_are_locked(self):
        metrics = self.analysis["metrics"]
        self.assertEqual(122, metrics["registry_history_rows"])
        self.assertEqual(121, metrics["active_registry_actors"])
        self.assertEqual(11, metrics["service_active_issue_edge_count"])
        self.assertEqual(
            ["I014", "I016"], metrics["service_active_issue_ids"]
        )
        self.assertEqual(6, metrics["service_human_reviewed_issue_edge_count"])
        self.assertEqual(5, metrics["service_candidate_issue_edge_count"])
        self.assertEqual(0, metrics["service_anchor_issue_edge_count"])
        self.assertEqual(14, metrics["reviewed_dyadic_relation_count"])
        self.assertEqual(8, metrics["candidate_dyadic_relation_count"])
        self.assertEqual(0, metrics["cross_ecology_dyadic_observed_count"])
        self.assertEqual(27, metrics["case_role_count"])
        self.assertEqual(0, metrics["service_core_case_role_count"])
        self.assertEqual(4, metrics["typed_event_observation_count"])
        self.assertEqual(0, metrics["cross_ecology_event_observed_count"])
        self.assertEqual(35, metrics["r10_purposive_relation_count"])
        self.assertEqual(0, metrics["r10_cross_ecology_observed_count"])
        self.assertEqual(616, metrics["r10_official_source_universe_row_count"])

    def test_people_and_recipient_gaps_are_not_encoded_as_absence(self):
        metrics = self.analysis["metrics"]
        self.assertEqual(
            "not_measured_no_person_role_table",
            metrics["public_person_overlap_status"],
        )
        self.assertEqual(
            "not_measured_incomplete_records",
            metrics["complete_recipient_network_status"],
        )
        gaps = {row["gap_family"]: row for row in self.analysis["gaps"]}
        self.assertEqual("not_measured", gaps["public_person_roles"]["current_status"])
        self.assertEqual(
            "incomplete", gaps["service_recipient_universe"]["current_status"]
        )
        self.assertIn(
            "Do not report zero shared people",
            gaps["public_person_roles"]["claim_boundary"],
        )
        self.assertFalse(
            any(row["human_decision"] for row in self.analysis["human_review_queue"])
        )

    def test_place_and_source_overlap_keep_non_relation_boundaries(self):
        metrics = self.analysis["metrics"]
        self.assertEqual(2, metrics["shared_place_node_count"])
        self.assertEqual(["P001", "P005"], metrics["shared_place_node_ids"])
        self.assertEqual(0, metrics["shared_issue_source_id_count"])
        for row in self.analysis["places"]:
            if row["overlap_status"] == "same_place_node_observed":
                self.assertIn("not a relationship", row["interpretation_limit"])
        for row in self.analysis["sources"]:
            self.assertIn(
                "documentation-channel measure",
                row["interpretation_limit"],
            )

    def test_every_csv_row_is_research_only_and_frontend_excluded(self):
        for key, rows in self.analysis.items():
            if not isinstance(rows, list):
                continue
            for row in rows:
                self.assertEqual("research_only", row["package_scope"], key)
                self.assertEqual(
                    "candidate_analysis",
                    row["package_claim_status"],
                    key,
                )
                self.assertEqual(
                    "excluded_research_only",
                    row["frontend_eligibility"],
                    key,
                )

    def test_brief_uses_bounded_negative_wording(self):
        brief = MODULE.render_brief(self.analysis)
        self.assertIn("18 个至少有一条人审锚点边", brief)
        self.assertIn("47 个只由候选锚点边选入", brief)
        self.assertIn("未观测到", brief)
        self.assertIn("人物共享**尚未测量**", brief)
        self.assertIn("不能写“没有共享人员”", brief)
        self.assertIn("27 条法律案件角色中没有服务侧 actor", brief)
        self.assertIn("因果假设", brief)
        self.assertNotIn("不存在共享人员", brief)
        self.assertNotIn("已经证实完全隔绝", brief)

    def test_build_is_deterministic_and_writes_only_contract_files(self):
        protected = {
            relative: hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
            for relative in MODULE.INPUT_PATHS
        }
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            first_dir = Path(first)
            second_dir = Path(second)
            first_written = MODULE.build_package(first_dir)
            second_written = MODULE.build_package(second_dir)
            self.assertEqual(
                MODULE.OUTPUT_FILENAMES,
                {path.name for path in first_written},
            )
            self.assertEqual(
                MODULE.OUTPUT_FILENAMES,
                {
                    path.name
                    for path in first_dir.rglob("*")
                    if path.is_file()
                },
            )
            self.assertEqual(hash_tree(first_dir), hash_tree(second_dir))

            manifest = json.loads((first_dir / "manifest.json").read_text("utf-8"))
            self.assertEqual("research_only", manifest["package_scope"])
            self.assertEqual(
                "excluded_research_only", manifest["frontend_eligibility"]
            )
            self.assertEqual(
                sorted(MODULE.OUTPUT_FILENAMES), manifest["outputs"]
            )

            with (
                first_dir / "human_review_queue_v1.csv"
            ).open(encoding="utf-8-sig", newline="") as handle:
                review_rows = list(csv.DictReader(handle))
            self.assertEqual(7, len(review_rows))
            self.assertTrue(all(not row["human_decision"] for row in review_rows))

        self.assertEqual(
            protected,
            {
                relative: hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
                for relative in MODULE.INPUT_PATHS
            },
        )


if __name__ == "__main__":
    unittest.main()
