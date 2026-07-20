from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "make_research_wave_h3_frontline_memory_v2",
    ROOT / "scripts" / "make_research_wave_h3_frontline_memory_v2.py",
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class H3FrontlineMemoryV2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.before = {
            path.relative_to(ROOT).as_posix(): sha256(path)
            for path in MODULE.PROTECTED_INPUTS
        }
        cls.temporary = tempfile.TemporaryDirectory()
        cls.output = Path(cls.temporary.name)
        cls.counts = MODULE.build_package(cls.output)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temporary.cleanup()

    def test_builder_is_additive_and_protected_inputs_are_unchanged(self) -> None:
        self.assertEqual(
            self.before,
            {
                path.relative_to(ROOT).as_posix(): sha256(path)
                for path in MODULE.PROTECTED_INPUTS
            },
        )
        report = (self.output / "validation_report_v2.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Result: **PASS**", report)
        self.assertIn("Protected central/v1 inputs unchanged: **yes**", report)

    def test_rosters_counts_crosswalks_and_role_boundaries(self) -> None:
        members = read_rows(self.output / "network_membership_candidates_v2.csv")
        petition = read_rows(self.output / "four_island_petition_entities_v2.csv")
        self.assertEqual(35, len(members))
        self.assertEqual(
            35, len({row["organization_name_as_listed"] for row in members})
        )
        self.assertEqual(35, len(petition))
        self.assertEqual(
            35, len({row["organization_name_as_listed"] for row in petition})
        )
        self.assertEqual(
            14, sum(bool(row["actor_id"]) for row in petition)
        )
        self.assertTrue(
            all(row["stable_alliance_claim"] == "no" for row in members)
        )
        self.assertTrue(
            all(row["stable_alliance_claim"] == "no" for row in petition)
        )

    def test_overlap_counts_and_role_warning_are_exact(self) -> None:
        overlaps = {
            row["overlap_id"]: row
            for row in read_rows(self.output / "event_roster_overlap_v2.csv")
        }
        self.assertEqual(
            {"OV01": "3", "OV02": "7", "OV03": "5", "OV04": "3"},
            {key: row["overlap_n"] for key, row in overlaps.items()},
        )
        self.assertEqual(
            "A018;A056;A071;A099;A100;A101;KADENA_PEACE_ACTION",
            overlaps["OV02"]["entity_keys"],
        )
        self.assertTrue(
            all("roles differ" in row["role_warning"] or "not centrality" in row["role_warning"] for row in overlaps.values())
        )

    def test_common_frame_object_and_diffusion_claims_stay_separate(self) -> None:
        hypotheses = {
            row["hypothesis_id"]: row
            for row in read_rows(self.output / "hypothesis_tests_v2.csv")
        }
        self.assertEqual(7, len(hypotheses))
        self.assertEqual(
            "not_testable_with_current_unbalanced_corpus",
            hypotheses["H3a"]["current_assessment"],
        )
        self.assertEqual(
            "strong_candidate_in_2025_declaration_and_2026_petition",
            hypotheses["H3c"]["current_assessment"],
        )
        self.assertEqual(
            "unconfirmed_and_aggregation_is_equally_plausible",
            hypotheses["H3e"]["current_assessment"],
        )
        frame_objects = read_rows(
            self.output / "frame_object_observations_v2.csv"
        )
        self.assertTrue(
            all(row["common_frame"] and row["common_object"] for row in frame_objects)
        )

    def test_miyako_boundary_and_A010_scale_shift_are_preserved(self) -> None:
        members = {
            row["actor_id"]
            for row in read_rows(
                self.output / "network_membership_candidates_v2.csv"
            )
        }
        petition = {
            row["actor_id"]
            for row in read_rows(
                self.output / "four_island_petition_entities_v2.csv"
            )
        }
        self.assertNotIn("A013", members)
        self.assertIn("A013", petition)

        stages = read_rows(self.output / "scale_shift_case_A010_v2.csv")
        scopes = {row["object_scope"] for row in stages}
        self.assertIn("distributed missile deployment beyond Ishigaki", scopes)
        self.assertIn(
            "local requests plus distributed war-preparation system", scopes
        )
        self.assertTrue(
            any("requires HR" in row["interpretation_limit"] for row in stages)
        )

    def test_all_guarded_rows_and_manifest_are_non_integrating(self) -> None:
        for path in self.output.glob("*.csv"):
            rows = read_rows(path)
            for row in rows:
                self.assertEqual("research_only", row["data_layer"], path.name)
                self.assertEqual(
                    "not_frontend_ready", row["frontend_eligibility"], path.name
                )
                self.assertEqual("no", row["central_writeback"], path.name)

        manifest = json.loads(
            (self.output / "manifest.json").read_text(encoding="utf-8")
        )
        self.assertEqual("research_only_not_frontend_ready", manifest["status"])
        self.assertEqual("no", manifest["central_writeback"])
        self.assertEqual(35, manifest["counts"]["network_members"])
        self.assertEqual(35, manifest["counts"]["petition_signatories"])
        self.assertEqual(14, manifest["counts"]["petition_registry_crosswalks"])
        self.assertTrue(
            any("No diffusion direction" in item for item in manifest["hard_boundaries"])
        )

    def test_three_svg_figures_are_well_formed(self) -> None:
        figures = sorted(self.output.glob("fig*.svg"))
        self.assertEqual(3, len(figures))
        for figure in figures:
            root = ET.parse(figure).getroot()
            self.assertTrue(root.tag.endswith("svg"), figure.name)
            self.assertGreater(figure.stat().st_size, 1000)

        timeline = (self.output / "fig1_carrier_and_object_timeline_v2.svg").read_text(
            encoding="utf-8"
        )
        self.assertIn('width="2200"', timeline)
        self.assertIn("横向按事件顺序等距排列", timeline)
        self.assertIn("不是扩散方向图", timeline)


if __name__ == "__main__":
    unittest.main()
