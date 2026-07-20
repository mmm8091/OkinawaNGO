from __future__ import annotations

import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "build_research_wave_index_v1",
    ROOT / "scripts" / "build_research_wave_index_v1.py",
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class ResearchWaveIndexTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.protected_inputs = [
            ROOT / "data" / "interim" / "01_actor_registry_initial_v0.csv",
            ROOT / "data" / "interim" / "24_r01_r02_actor_issue_layered_v0.csv",
            ROOT / "scripts" / "build_exploration_system_data_v1.py",
        ]
        cls.before = {path.as_posix(): sha256(path) for path in cls.protected_inputs}
        cls.temporary = tempfile.TemporaryDirectory()
        cls.output = Path(cls.temporary.name)
        cls.result = MODULE.build_index(cls.output)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temporary.cleanup()

    def test_build_is_additive_and_does_not_touch_current_contract(self) -> None:
        self.assertEqual(
            self.before,
            {path.as_posix(): sha256(path) for path in self.protected_inputs},
        )
        self.assertFalse(self.result["central_tables_mutated"])
        self.assertFalse(self.result["current_frontend_contract_mutated"])
        self.assertEqual(
            "module_index_ready_observation_exports_gated",
            self.result["integration_status"],
        )
        self.assertEqual(
            "future_explicit_research_module_after_separate_approval",
            self.result["allowed_surface"],
        )
        self.assertEqual(
            "module_directory_index_not_row_level_observation_contract",
            self.result["adapter_kind"],
        )

    def test_index_has_three_bounded_research_modules(self) -> None:
        modules = {
            row["module_id"]: row
            for row in self.result["modules"]
        }
        self.assertEqual(
            {
                "H1_DOCUMENTATION_VISIBILITY_V1",
                "H2_TWO_ECOLOGIES_V1",
                "H3_FRONTLINE_MEMORY_V1",
            },
            set(modules),
        )
        for row in modules.values():
            self.assertEqual("research_only", row["data_layer"])
            self.assertEqual("candidate", row["claim_status"])
            self.assertEqual("ai_seeded", row["review_status"])
            self.assertEqual(
                "indexed_not_integrated",
                row["integration_status"],
            )
            self.assertEqual(
                "not_frontend_ready",
                row["frontend_eligibility"],
            )
            self.assertTrue(row["interpretation_limits"])
            for asset in row["assets"]:
                self.assertTrue((ROOT / asset).is_file(), asset)

        self.assertIn(
            "not_measured",
            " ".join(
                modules["H2_TWO_ECOLOGIES_V1"]["interpretation_limits"]
            ),
        )
        self.assertEqual(
            "not_testable_with_current_unbalanced_corpus",
            modules["H3_FRONTLINE_MEMORY_V1"]["primary_metrics"][
                "vocabulary_growth_status"
            ],
        )
        self.assertEqual(
            6,
            modules["H1_DOCUMENTATION_VISIBILITY_V1"][
                "open_followup_task_count"
            ],
        )
        self.assertEqual(
            18,
            modules["H2_TWO_ECOLOGIES_V1"]["primary_metrics"][
                "accountability_human_reviewed_anchor_actor_count"
            ],
        )
        self.assertEqual(
            47,
            modules["H2_TWO_ECOLOGIES_V1"]["primary_metrics"][
                "accountability_candidate_only_anchor_actor_count"
            ],
        )
        self.assertEqual(
            9,
            modules["H2_TWO_ECOLOGIES_V1"]["open_search_task_count"],
        )
        self.assertGreaterEqual(
            modules["H3_FRONTLINE_MEMORY_V1"]["open_human_gate_count"],
            9,
        )
        self.assertEqual(
            3,
            modules["H3_FRONTLINE_MEMORY_V1"]["primary_metrics"][
                "source_governance_blocker_count"
            ],
        )
        h1_assets = modules["H1_DOCUMENTATION_VISIBILITY_V1"]["assets"]
        h2_assets = modules["H2_TWO_ECOLOGIES_V1"]["assets"]
        h3_assets = modules["H3_FRONTLINE_MEMORY_V1"]["assets"]
        self.assertTrue(
            any(path.endswith("scenario_removed_edges_v1.csv") for path in h1_assets)
        )
        self.assertTrue(
            any(path.endswith("further_search_queue_v1.csv") for path in h2_assets)
        )
        self.assertTrue(
            any(
                path.endswith("accountability_comparison_actors_v1.csv")
                for path in h2_assets
            )
        )
        self.assertTrue(
            any(path.endswith("case_role_ecology_audit_v1.csv") for path in h2_assets)
        )
        self.assertTrue(
            any(
                path.endswith("event_participant_candidates_v1.csv")
                for path in h3_assets
            )
        )
        self.assertTrue(
            any(path.endswith("source_governance_v1.csv") for path in h3_assets)
        )

    def test_expected_files_and_json_round_trip(self) -> None:
        expected = {
            "frontend_research_modules_v1.json",
            "wave_manifest_v1.json",
            "validation_report_v1.md",
        }
        self.assertEqual(expected, {path.name for path in self.output.iterdir()})
        frontend = json.loads(
            (self.output / "frontend_research_modules_v1.json").read_text(
                encoding="utf-8"
            )
        )
        manifest = json.loads(
            (self.output / "wave_manifest_v1.json").read_text(encoding="utf-8")
        )
        self.assertEqual(self.result, frontend)
        self.assertEqual(3, manifest["module_count"])
        self.assertTrue(manifest["all_assets_exist"])
        self.assertTrue(manifest["all_modules_research_only"])

    def test_build_is_byte_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as second_directory:
            second = Path(second_directory)
            MODULE.build_index(second)
            for filename in MODULE.OUTPUT_FILENAMES:
                self.assertEqual(
                    (self.output / filename).read_bytes(),
                    (second / filename).read_bytes(),
                    filename,
                )


if __name__ == "__main__":
    unittest.main()
