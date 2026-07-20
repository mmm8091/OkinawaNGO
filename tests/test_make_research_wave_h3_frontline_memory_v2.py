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

    def test_dated_group_lists_counts_crosswalks_and_role_boundaries(self) -> None:
        participating = read_rows(
            self.output / "network_participating_group_candidates_v2.csv"
        )
        endorsers = read_rows(
            self.output
            / "three_island_request_four_place_event_entities_v2.csv"
        )
        self.assertEqual(35, len(participating))
        self.assertEqual(
            35,
            len(
                {
                    row["organization_name_as_listed"]
                    for row in participating
                }
            ),
        )
        self.assertEqual(35, len(endorsers))
        self.assertEqual(
            35,
            len({row["organization_name_as_listed"] for row in endorsers}),
        )
        self.assertEqual(14, sum(bool(row["actor_id"]) for row in endorsers))
        self.assertTrue(
            all(
                row["evidence_role"]
                == "participating_or_constituent_group_as_listed"
                for row in participating
            )
        )
        self.assertTrue(
            all(
                row["retention_claim"] == "unmeasured"
                and row["active_division_of_labor_claim"] == "unmeasured"
                and row["governance_execution_claim"] == "unmeasured"
                for row in participating
            )
        )
        self.assertTrue(
            all(row["stable_alliance_claim"] == "no" for row in participating)
        )
        self.assertTrue(
            all(row["stable_alliance_claim"] == "no" for row in endorsers)
        )
        self.assertTrue(
            all(
                row["event_date"] == "2026-05-07"
                and row["publication_date"] == "2026-05-16"
                for row in endorsers
            )
        )
        self.assertTrue(
            all(
                row["first_joint_action_claim_status"]
                == "publisher_and_party_press_attribution_not_independently_established"
                for row in endorsers
            )
        )
        self.assertTrue(
            all(
                "local_request_subject_candidate" not in row["event_role"]
                for row in endorsers
            )
        )

        sections = read_rows(
            self.output / "three_island_request_sections_v2.csv"
        )
        self.assertEqual(3, len(sections))
        self.assertEqual(
            {"Yonaguni": "3", "Ishigaki": "9", "Miyako": "6"},
            {row["island"]: row["request_item_count"] for row in sections},
        )
        self.assertTrue(
            all(
                row["document_author_or_drafter"] == "unknown"
                and row["representative_organization"] == "unknown"
                and row["organization_authorship_claim"] == "unconfirmed"
                for row in sections
            )
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
        self.assertEqual(
            "normalized_name_candidate", overlaps["OV03"]["overlap_basis"]
        )
        self.assertEqual("4", overlaps["OV03"]["raw_exact_surface_overlap_n"])
        self.assertEqual("3", overlaps["OV03"]["exact_registry_overlap_n"])
        self.assertEqual(
            "2", overlaps["OV03"]["conditional_crosswalk_overlap_n"]
        )
        self.assertEqual(
            "CANDIDATE_ALIAS_A016;CANDIDATE_LIFECYCLE_A010",
            overlaps["OV03"]["conditional_entity_keys"],
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
            "supported_at_common_document_layer_only",
            hypotheses["H3c"]["current_assessment"],
        )
        self.assertEqual(
            "unconfirmed_and_aggregation_is_equally_plausible",
            hypotheses["H3e"]["current_assessment"],
        )
        self.assertEqual(
            "reported_exact_rename_central_lifecycle_human_pending_no_scale_shift_claim",
            hypotheses["H3f"]["current_assessment"],
        )
        frame_objects = read_rows(
            self.output / "frame_object_observations_v2.csv"
        )
        self.assertTrue(
            all(row["common_frame"] and row["common_object"] for row in frame_objects)
        )
        self.assertTrue(
            all(row["text_ownership_status"] for row in frame_objects)
        )

    def test_miyako_attribution_and_A010_identity_gate_are_preserved(self) -> None:
        participating = {
            row["actor_id"]
            for row in read_rows(
                self.output / "network_participating_group_candidates_v2.csv"
            )
        }
        endorsers = {
            row["actor_id"]
            for row in read_rows(
                self.output
                / "three_island_request_four_place_event_entities_v2.csv"
            )
        }
        self.assertNotIn("A013", participating)
        self.assertIn("A013", endorsers)

        adoption = {
            row["actor_id"]: row
            for row in read_rows(
                self.output / "independent_adoption_panel_v2.csv"
            )
            if row["actor_id"]
        }
        self.assertEqual(
            "media_attributed_not_organization_authored",
            adoption["A013"]["pre_2025_independent_evidence_status"],
        )
        self.assertEqual(
            "battlefield_prevention;dialogue",
            adoption["A013"]["frame_codes"],
        )
        self.assertNotIn("H3V2S020", adoption["A013"]["source_ids"])

        stages = read_rows(
            self.output / "ishigaki_name_lifecycle_candidate_v2.csv"
        )
        post_name_rows = [
            row for row in stages if row["stage_id"] >= "LC04"
        ]
        self.assertTrue(post_name_rows)
        self.assertTrue(
            all(
                row["identity_continuity_status"]
                == "reported_exact_rename_central_lifecycle_human_pending"
                for row in post_name_rows
            )
        )
        self.assertEqual(
            "H3V2S015;H3V2S025",
            next(row for row in stages if row["stage_id"] == "LC04")[
                "source_ids"
            ],
        )

        sources = {
            row["source_id"]: row
            for row in read_rows(self.output / "source_log_v2.csv")
        }
        self.assertEqual(
            "independent_news_reported_exact_rename",
            sources["H3V2S025"]["attribution_status"],
        )
        self.assertEqual(
            "official_request_submission_record_not_attendance",
            sources["H3V2S020"]["attribution_status"],
        )

    def test_miyako_speaker_attributions_do_not_transfer_frames(self) -> None:
        speakers = read_rows(
            self.output / "event_speaker_attributions_v2.csv"
        )
        self.assertEqual(3, len(speakers))
        self.assertTrue(
            all(
                row["attribution_status"]
                == "speaker_specific_media_attribution"
                and row["organization_frame_transfer"] == "no"
                for row in speakers
            )
        )
        a013 = next(row for row in speakers if row["actor_id_crosswalk"] == "A013")
        self.assertEqual(
            "battlefield_prevention;dialogue",
            a013["frame_codes_attributed_to_this_speaker"],
        )
        other_frames = ";".join(
            row["frame_codes_attributed_to_this_speaker"]
            for row in speakers
            if not row["actor_id_crosswalk"]
        )
        self.assertIn("evacuation", other_frames)
        self.assertIn("life_safety", other_frames)

    def test_event_issue_families_are_analyst_candidates(self) -> None:
        rows = read_rows(
            self.output / "event_endorser_issue_family_candidates_v2.csv"
        )
        self.assertTrue(rows)
        self.assertTrue(
            all(
                row["classification_status"]
                == "analyst_candidate_not_source_label"
                for row in rows
            )
        )
        self.assertTrue(
            all("pending human review" in row["classification_method"] for row in rows)
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
        self.assertEqual(
            35, manifest["counts"]["network_participating_groups"]
        )
        self.assertEqual(35, manifest["counts"]["petition_endorsing_groups"])
        self.assertEqual(14, manifest["counts"]["petition_registry_crosswalks"])
        self.assertEqual(3, manifest["counts"]["request_sections"])
        self.assertEqual(3, manifest["counts"]["speaker_attributions"])
        self.assertTrue(
            any("No diffusion direction" in item for item in manifest["hard_boundaries"])
        )
        self.assertTrue(
            any(
                "common object at document level" in item
                for item in manifest["hard_boundaries"]
            )
        )
        self.assertTrue(
            any(
                "News sources report an exact A010 rename" in item
                for item in manifest["hard_boundaries"]
            )
        )

    def test_boss_facing_text_contains_no_redteam_blockers(self) -> None:
        text = "\n".join(
            path.read_text(encoding="utf-8", errors="replace")
            for path in self.output.iterdir()
            if path.suffix.lower() in {".md", ".csv", ".svg"}
        )
        for forbidden in (
            "一个正式跨区域载体已经制度化",
            "A010 安装后尺度转换",
            "共同对象发生上移",
            "35 个正式成员",
            "四地地方请求",
        ):
            self.assertNotIn(forbidden, text)
        self.assertIn(
            "共同文件层",
            (self.output / "frontline_memory_brief_v2.md").read_text(
                encoding="utf-8"
            ),
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
        self.assertIn("5/7提交·四地行动", timeline)
        self.assertIn("5/16发布·三岛请求", timeline)

        overlap = (
            self.output / "fig2_roster_overlap_v2.svg"
        ).read_text(encoding="utf-8")
        self.assertIn("名称归一化候选", overlap)
        self.assertIn("精确registry 3", overlap)

        common_object = (
            self.output / "fig3_common_frame_vs_common_object_v2.svg"
        ).read_text(encoding="utf-8")
        self.assertIn("共同文件如何构造共同对象", common_object)
        self.assertIn("不证明参加团体独立采用", common_object)


if __name__ == "__main__":
    unittest.main()
