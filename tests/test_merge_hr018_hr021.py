from __future__ import annotations

import csv
import hashlib
import importlib.util
import shutil
import tempfile
import unittest
from collections import Counter
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "merge_hr018_hr021.py"


def load_module():
    spec = importlib.util.spec_from_file_location("merge_hr018_hr021", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class MergeHR018HR021Test(unittest.TestCase):
    maxDiff = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_module()

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        relative_files = [
            "outputs/principal_review_merge_v1/principal_decision_overlay_v1.csv",
            "outputs/R10_administrative_collaboration_v0/HR018_relation_review_v0.csv",
            "outputs/R10_administrative_collaboration_v0/HR018_source_prerequisites_v0.csv",
            "outputs/R10_administrative_collaboration_v0/annual_relations_v0.csv",
            "outputs/R10_administrative_collaboration_v0/mechanism_matrix_v0.csv",
            "outputs/R10_administrative_collaboration_v0/source_candidates_v0.csv",
            "outputs/R10_administrative_collaboration_v0/source_crosswalk_v1.csv",
            "outputs/R10_administrative_collaboration_v0/visualization_edges_v0.csv",
            "outputs/R10_administrative_collaboration_v0/figure_metrics_v1.csv",
            "outputs/R10_administrative_collaboration_v0/main_merge_proposal_v1.csv",
            "outputs/R10_administrative_collaboration_v0/R10_explanatory_brief_v1.md",
            "outputs/R06_R07_R11_pathways_v1/HR021_review_items_v0.csv",
            "outputs/R06_R07_R11_pathways_v1/analytical_seeds_v0.csv",
            "outputs/R06_R07_R11_pathways_v1/r06_pathway_comparison_v0.csv",
            "outputs/R06_R07_R11_pathways_v1/r11_external_entry_matrix_v0.csv",
            "outputs/R06_R07_R11_pathways_v1/R06_R07_R11_explanatory_brief_v1.md",
            "outputs/R06_R07_R11_pathways_v1/validation_note_v0.md",
            "data/interim/21_admin_collaboration_relations_v0.csv",
            "data/interim/22_admin_amount_observations_v0.csv",
            "data/interim/23_admin_function_observations_v0.csv",
            "data/interim/26_actor_event_venue_target_entry_modes_v0.csv",
        ]
        for relative in relative_files:
            source = REPO / relative
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_merge_applies_reviewed_counts_and_keeps_hr033_boundary(self) -> None:
        self.module.merge(self.root)

        relations = read_csv(
            self.root / "data/interim/21_admin_collaboration_relations_v0.csv"
        )
        amounts = read_csv(
            self.root / "data/interim/22_admin_amount_observations_v0.csv"
        )
        functions = read_csv(
            self.root / "data/interim/23_admin_function_observations_v0.csv"
        )

        self.assertEqual(
            Counter(row["review_status"] for row in relations),
            Counter({"human_checked": 24, "human_revised": 10, "needs_local_retrieval": 1}),
        )
        self.assertEqual(
            Counter(row["review_status"] for row in amounts),
            Counter({"human_checked": 21, "human_revised": 6, "needs_local_retrieval": 1}),
        )
        self.assertEqual(
            Counter(row["review_status"] for row in functions),
            Counter({"human_checked": 29, "human_revised": 13, "needs_local_retrieval": 1}),
        )
        self.assertEqual(len(amounts), 28)

        by_relation = {row["relation_observation_id"]: row for row in relations}
        by_amount = {row["amount_observation_id"]: row for row in amounts}
        self.assertEqual(
            by_relation["R10R029"]["merge_disposition"],
            "hr033_accepted_aggregate_observation",
        )
        self.assertEqual(by_relation["R10R029"]["review_status"], "human_revised")
        self.assertEqual(by_amount["R10AM024"]["amount_value"], "102000")
        self.assertEqual(
            by_amount["R10AM024"]["actor_payment_status"],
            "not_allocable_to_named_actor",
        )
        self.assertEqual(by_relation["R10R030"]["review_status"], "needs_local_retrieval")

        self.assertEqual(by_amount["R10AM027"]["amount_value"], "27199000")
        self.assertEqual(by_amount["R10AM028"]["amount_value"], "37220999")
        self.assertEqual(
            by_relation["R10R011"]["financial_semantics"],
            "confirmed_contract_plus_project_cost",
        )
        self.assertEqual(
            by_relation["R10R013"]["financial_semantics"],
            "confirmed_contract_plus_project_cost",
        )

    def test_revisions_preserve_scope_and_identity_limits(self) -> None:
        self.module.merge(self.root)
        relations = {
            row["relation_observation_id"]: row
            for row in read_csv(
                self.root / "data/interim/21_admin_collaboration_relations_v0.csv"
            )
        }

        self.assertEqual(relations["R10R021"]["target_entity_name"], "USO Indo-Pacific")
        self.assertEqual(
            relations["R10R021"]["relation_scope"],
            "regional_context_not_okinawa_direct",
        )
        self.assertEqual(relations["R10R028"]["source_entity_id"], "X017")
        self.assertEqual(relations["R10R028"]["target_entity_id"], "X004")
        self.assertEqual(relations["R10R028"]["period_start"], "2012")
        self.assertEqual(relations["R10R028"]["period_end"], "2015")
        self.assertEqual(relations["R10R031"]["target_entity_name"], "よみたん救護園")
        self.assertEqual(
            relations["R10R032"]["target_entity_name"],
            "社会福祉法人うるま市社会福祉協議会",
        )
        self.assertEqual(relations["R10R033"]["fiscal_year"], "")
        self.assertEqual(
            relations["R10R033"]["relation_type"],
            "in_kind_acquisition_assistance",
        )
        self.assertEqual(
            relations["R10R034"]["target_entity_name"],
            "平敷屋地区の放課後児童クラブ（正式名称未確認）",
        )
        self.assertEqual(relations["R10R034"]["period_start"], "2025-08-15")

    def test_hr021_adds_only_nine_downstream_facts_and_retains_seeds(self) -> None:
        self.module.merge(self.root)

        facts = read_csv(
            self.root / "data/interim/26_actor_event_venue_target_entry_modes_v0.csv"
        )
        r11 = read_csv(
            self.root
            / "outputs/R06_R07_R11_pathways_v1/r11_external_entry_matrix_v0.csv"
        )
        seeds = read_csv(
            self.root / "outputs/R06_R07_R11_pathways_v1/analytical_seeds_v0.csv"
        )
        new_ids = {
            "OBS_R10R001",
            "OBS_R10R004",
            "OBS_R10R005",
            "OBS_R10R006",
            "OBS_R10R007",
            "OBS_R10R008",
            "OBS_R10R018",
            "OBS_R10R020",
            "OBS_R10R021",
        }

        self.assertEqual(len(facts), 80)
        self.assertEqual(
            {row["observation_id"] for row in facts if row["observation_id"] in new_ids},
            new_ids,
        )
        self.assertNotIn("OBS_R10R029", {row["observation_id"] for row in facts})
        self.assertEqual(len(r11), 53)
        self.assertEqual(
            {row["fact_observation_id"] for row in r11 if row["fact_observation_id"] in new_ids},
            new_ids,
        )
        self.assertEqual(len(seeds), 4)
        self.assertTrue(
            all(row["hr021_disposition"] == "retain_analytical_seed" for row in seeds)
        )
        self.assertTrue(
            all(row["review_status"] == "analytical_seed" for row in seeds)
        )

    def test_merge_is_idempotent(self) -> None:
        self.module.merge(self.root)
        tracked = [
            self.root / "data/interim/21_admin_collaboration_relations_v0.csv",
            self.root / "data/interim/22_admin_amount_observations_v0.csv",
            self.root / "data/interim/23_admin_function_observations_v0.csv",
            self.root / "data/interim/26_actor_event_venue_target_entry_modes_v0.csv",
            self.root
            / "outputs/R06_R07_R11_pathways_v1/r11_external_entry_matrix_v0.csv",
        ]
        before = {path: file_hash(path) for path in tracked}
        self.module.merge(self.root)
        after = {path: file_hash(path) for path in tracked}
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
