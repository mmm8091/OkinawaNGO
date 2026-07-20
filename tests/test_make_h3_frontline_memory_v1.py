from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "make_h3_frontline_memory_v1",
    ROOT / "scripts" / "make_h3_frontline_memory_v1.py",
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class H3FrontlineMemoryResearchPackageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.protected_inputs = [
            *MODULE.SOURCE_PATHS.values(),
            *MODULE.CENTRAL_INPUT_PATHS,
            MODULE.SOURCE_LOG_PATH,
            MODULE.ARCHIVE_MANIFEST_PATH,
        ]
        cls.before = {
            path.relative_to(ROOT).as_posix(): sha256(path)
            for path in cls.protected_inputs
        }
        cls.temporary = tempfile.TemporaryDirectory()
        cls.output = Path(cls.temporary.name)
        cls.result = MODULE.build_package(cls.output)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temporary.cleanup()

    def test_reads_only_six_archived_sources_and_current_central_tables(self) -> None:
        self.assertEqual(
            {"S022", "S023", "S036", "S119", "S148", "S246"},
            set(MODULE.SOURCE_PATHS),
        )
        self.assertEqual(
            self.before,
            {
                path.relative_to(ROOT).as_posix(): sha256(path)
                for path in self.protected_inputs
            },
        )

    def test_three_hypothesis_layers_are_falsifiable_and_not_collapsed(self) -> None:
        rows = {
            row["hypothesis_id"]: row
            for row in read_rows(self.output / "hypothesis_layers_v1.csv")
        }
        self.assertEqual({"H3a", "H3b", "H3c"}, set(rows))
        self.assertEqual(
            "not_testable_with_current_unbalanced_corpus",
            rows["H3a"]["current_assessment"],
        )
        self.assertEqual(
            "candidate_carrier_mechanisms_direction_unconfirmed",
            rows["H3b"]["current_assessment"],
        )
        self.assertEqual(
            "episodic_convergence_not_durable_mobilization",
            rows["H3c"]["current_assessment"],
        )
        self.assertIn("schema", rows["H3a"]["falsification_rule"])
        self.assertIn("repeat", rows["H3c"]["minimum_test"])

    def test_observations_have_verified_short_excerpts_and_locators(self) -> None:
        observations = read_rows(self.output / "source_observations_v1.csv")
        self.assertGreaterEqual(len(observations), 10)
        self.assertEqual(
            {"S022", "S023", "S036", "S119", "S148", "S246"},
            {row["source_id"] for row in observations},
        )
        for row in observations:
            self.assertEqual("research_only", row["data_layer"])
            self.assertEqual("candidate", row["claim_status"])
            self.assertEqual("ai_seeded", row["review_status"])
            self.assertEqual("not_frontend_ready", row["frontend_eligibility"])
            self.assertEqual("no", row["central_writeback"])
            for field in (
                "hypothesis_id",
                "observation_kind",
                "source_ids",
                "context_actor_id",
                "claim_subject_entity_id",
                "claim_subject_kind",
                "target_actor_or_event_id",
                "interpretation_limit",
            ):
                self.assertTrue(row[field], f"{row['observation_id']}:{field}")
            self.assertRegex(row["locator"], r"raw\.html:L\d+")
            self.assertTrue(row["original_excerpt"])
            self.assertLessEqual(len(row["original_excerpt"]), 120)
            source_text = MODULE.SOURCE_PATHS[row["source_id"]].read_text(
                encoding="utf-8",
                errors="replace",
            )
            self.assertIn(row["original_excerpt"], source_text)
            locator_line = int(row["locator"].rsplit("L", 1)[1])
            source_lines = source_text.splitlines()
            self.assertIn(
                row["original_excerpt"],
                source_lines[locator_line - 1],
                msg=f"{row['observation_id']} locator does not pinpoint excerpt",
            )

        by_source = {}
        for row in observations:
            by_source.setdefault(row["source_id"], []).append(row)
        self.assertTrue(
            any("捨て石" in row["original_excerpt"] for row in by_source["S022"])
        )
        self.assertTrue(
            any("台湾有事" in row["original_excerpt"] for row in by_source["S023"])
        )
        self.assertTrue(
            any("避難計画" in row["original_excerpt"] for row in by_source["S036"])
        )
        by_id = {row["observation_id"]: row for row in observations}
        self.assertEqual("A100", by_id["H3O007"]["context_actor_id"])
        self.assertEqual(
            "PROV_ARAKAKI_KUNIO",
            by_id["H3O007"]["claim_subject_entity_id"],
        )
        self.assertEqual("A018", by_id["H3O009"]["claim_subject_entity_id"])
        self.assertEqual(
            "PROV_GUSHIKEN_TAKAMATSU",
            by_id["H3O010"]["claim_subject_entity_id"],
        )
        self.assertEqual(
            "event_endorser_roster",
            by_id["H3O012"]["claim_subject_kind"],
        )
        self.assertEqual(
            "2022-10–2023-09",
            by_id["H3O005"]["event_date"],
        )

    def test_diffusion_carriers_and_event_participants_remain_candidates(self) -> None:
        carriers = read_rows(self.output / "diffusion_carrier_candidates_v1.csv")
        pairs = {
            (row["source_actor_id"], row["target_actor_or_event_id"])
            for row in carriers
        }
        self.assertIn(("A018", "A100"), pairs)
        self.assertIn(("A018", "A108"), pairs)
        self.assertTrue(
            any(row["source_id"] == "S246" for row in carriers)
        )
        for row in carriers:
            self.assertEqual("candidate", row["claim_status"])
            self.assertEqual("event_bounded", row["relation_scope"])
            self.assertEqual("no", row["stable_alliance_claim"])
            self.assertEqual(
                "direction_or_adoption_unconfirmed",
                row["diffusion_claim_status"],
            )
            self.assertTrue(row["diffusion_stage"])
            self.assertTrue(row["direction_status"])
            source_lines = MODULE.SOURCE_PATHS[row["source_id"]].read_text(
                encoding="utf-8",
                errors="replace",
            ).splitlines()
            locator_line = int(row["locator"].rsplit("L", 1)[1])
            self.assertIn(
                row["evidence_excerpt"],
                source_lines[locator_line - 1],
                msg=f"{row['candidate_id']} locator does not pinpoint excerpt",
            )
        carrier_by_id = {row["candidate_id"]: row for row in carriers}
        self.assertEqual(
            "2022-10–2023-09",
            carrier_by_id["H3D006"]["event_date"],
        )
        self.assertEqual(
            "event_endorsement_only",
            carrier_by_id["H3D005"]["diffusion_stage"],
        )

        participants = read_rows(
            self.output / "event_participant_candidates_v1.csv"
        )
        s246_registry_ids = {
            row["actor_id"]
            for row in participants
            if row["source_id"] == "S246" and row["entity_status"] == "registry_actor"
        }
        self.assertTrue(
            {"A002", "A018", "A019", "A049", "A055", "A056", "A099", "A100"}
            <= s246_registry_ids
        )
        self.assertTrue(
            all(row["stable_alliance_claim"] == "no" for row in participants)
        )

    def test_manifest_and_review_queues_keep_package_research_only(self) -> None:
        manifest = json.loads(
            (self.output / "manifest.json").read_text(encoding="utf-8")
        )
        self.assertEqual("research_only", manifest["data_layer"])
        self.assertEqual("candidate", manifest["claim_status"])
        self.assertEqual("not_frontend_ready", manifest["frontend_eligibility"])
        self.assertFalse(manifest["central_writeback"])
        self.assertEqual(
            {"S022", "S023", "S036", "S119", "S148", "S246"},
            {
                row["source_id"]
                for row in manifest["local_source_inputs"]
            },
        )
        self.assertEqual(3, manifest["source_governance_blocker_count"])
        self.assertEqual(4, manifest["current_actor_issue_counts"]["frontline_prevention"])
        self.assertEqual(4, manifest["current_actor_issue_counts"]["Taiwan_contingency"])
        self.assertEqual(1, manifest["current_actor_issue_counts"]["anti_war"])
        self.assertEqual(
            sorted(MODULE.OUTPUT_FILENAMES),
            sorted(path.name for path in self.output.iterdir() if path.is_file()),
        )

        human = read_rows(self.output / "human_review_queue_v1.csv")
        local = read_rows(self.output / "local_retrieval_queue_v1.csv")
        self.assertGreaterEqual(len(human), 9)
        self.assertGreaterEqual(len(local), 3)
        self.assertTrue(all(not row["decision"] for row in human))
        self.assertTrue(all(row["status"] == "open_local" for row in local))
        review_by_id = {row["review_id"]: row for row in human}
        self.assertIn("HR-H3-009", review_by_id)
        self.assertIn(
            "首次发现",
            review_by_id["HR-H3-009"]["question"],
        )

        brief = (self.output / "brief_v1.md").read_text(encoding="utf-8")
        for boundary in (
            "标签增长不等于社会趋势",
            "同场／赞同不等于稳定联盟",
            "共同语言不等于共同组织",
        ):
            self.assertIn(boundary, brief)

        governance = read_rows(self.output / "source_governance_v1.csv")
        governance_by_id = {row["source_id"]: row for row in governance}
        self.assertEqual(
            "yes",
            governance_by_id["S022"][
                "metadata_or_archive_correction_needed"
            ],
        )
        self.assertIn(
            "2022-12-07",
            governance_by_id["S022"]["correction_note"],
        )
        self.assertEqual("failed", governance_by_id["S119"]["archive_status"])
        self.assertEqual(
            "yes",
            governance_by_id["S119"][
                "metadata_or_archive_correction_needed"
            ],
        )


if __name__ == "__main__":
    unittest.main()
