from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (
    ROOT / "scripts" / "make_research_wave_postfreeze_compatibility_v1.py"
)
SPEC = importlib.util.spec_from_file_location(
    "make_research_wave_postfreeze_compatibility_v1",
    SCRIPT,
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)
OUT = ROOT / "outputs" / "research_wave_postfreeze_compatibility_v1"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def digest_tree() -> dict[str, str]:
    return {
        path.name: hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(OUT.iterdir())
        if path.is_file()
    }


class PostFreezeCompatibilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        MODULE.main()

    def test_current_central_snapshot_gate(self) -> None:
        snapshot = json.loads(
            (OUT / "central_snapshot_v1.json").read_text(encoding="utf-8")
        )
        self.assertEqual(
            snapshot["actor_registry"],
            {"history_rows": 122, "current_actors": 121},
        )
        actor_issue = snapshot["actor_issue"]
        self.assertEqual(actor_issue["history_rows"], 294)
        self.assertEqual(actor_issue["active_edges"], 283)
        self.assertEqual(actor_issue["reviewed_edges"], 141)
        self.assertEqual(actor_issue["candidate_edges"], 142)
        self.assertEqual(actor_issue["connected_actors"], 116)
        self.assertEqual(actor_issue["isolated_current_actors"], 5)
        self.assertEqual(actor_issue["e3plus_edges"], 271)
        self.assertEqual(actor_issue["e3plus_connected_actors"], 114)
        self.assertEqual(actor_issue["e3plus_reviewed_edges"], 133)
        self.assertEqual(actor_issue["e3plus_reviewed_actors"], 54)
        self.assertEqual(actor_issue["e3plus_candidate_edges"], 138)
        self.assertEqual(actor_issue["e3plus_candidate_actors"], 76)
        self.assertEqual(
            snapshot["strict_place_issue"],
            {
                "active_same_source_triples": 306,
                "e3plus_triples": 299,
                "dual_human_reviewed_triples": 81,
                "event_attached_triples": 97,
            },
        )

    def test_h1_recompute_distinguishes_incident_and_fully_lost_actors(self) -> None:
        metrics = json.loads(
            (OUT / "h1_recomputed_metrics_v1.json").read_text(
                encoding="utf-8"
            )
        )
        s004 = metrics["s004_support_deletion"]
        self.assertEqual(s004["baseline_edges"], 271)
        self.assertEqual(s004["removed_edges"], 40)
        self.assertEqual(s004["incident_actor_count"], 25)
        self.assertEqual(s004["fully_lost_actor_count"], 24)
        self.assertEqual(s004["remaining_edges"], 231)
        self.assertEqual(s004["remaining_observed_actors"], 90)
        self.assertEqual(
            metrics["big3_support_deletion"]["remaining_edges"],
            223,
        )
        self.assertEqual(
            metrics["big3_support_deletion"][
                "remaining_observed_actors"
            ],
            85,
        )

        review_rows = read_csv(
            OUT / "h1_review_layer_sensitivity_v1.csv"
        )
        self.assertEqual(
            {
                row["actor_issue_layer"]
                for row in review_rows
                if row["subset"] == "all_current_actors"
            },
            {"active_283", "reviewed_141", "candidate_142"},
        )

    def test_h2_current_group_and_bounded_zero_are_separate(self) -> None:
        metrics = json.loads(
            (OUT / "h2_recomputed_metrics_v1.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(metrics["service_core_actor_count"], 9)
        self.assertEqual(metrics["accountability_comparison_actor_count"], 77)
        self.assertEqual(
            metrics["accountability_human_reviewed_anchor_actor_count"],
            41,
        )
        self.assertEqual(
            metrics["accountability_candidate_only_anchor_actor_count"],
            36,
        )
        self.assertEqual(metrics["accountability_active_issue_edge_count"], 231)
        self.assertEqual(metrics["cross_ecology_dyadic_observed_count"], 0)
        self.assertEqual(metrics["cross_ecology_event_observed_count"], 0)
        self.assertEqual(metrics["r10_cross_ecology_observed_count"], 0)

        delta = read_csv(OUT / "h2_accountability_actor_delta_v1.csv")
        added = {
            row["actor_id"]
            for row in delta
            if row["membership_change"] == "added_postfreeze"
        }
        self.assertEqual(
            added,
            {
                "A087",
                "A089",
                "A090",
                "A091",
                "A092",
                "A093",
                "A095",
                "A096",
                "A097",
                "A099",
                "A100",
                "A101",
            },
        )

    def test_h3_current_tag_snapshot_does_not_upgrade_interpretation(self) -> None:
        metrics = json.loads(
            (OUT / "h3_recomputed_metrics_v1.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(
            metrics["target_issue_counts"],
            {
                "frontline_prevention": 6,
                "Taiwan_contingency": 6,
                "anti_war": 5,
            },
        )
        self.assertEqual(
            metrics["target_issue_human_reviewed_counts"],
            {
                "frontline_prevention": 3,
                "Taiwan_contingency": 5,
                "anti_war": 5,
            },
        )
        self.assertEqual(
            metrics["h3v2_missing_current_crosswalk_actor_ids"],
            [],
        )
        self.assertEqual(
            metrics["h3v2_a010_central_gate"],
            "still_human_pending_no_central_lifecycle_row",
        )
        issue_rows = read_csv(OUT / "h3_target_issue_snapshot_v1.csv")
        self.assertTrue(
            all(
                "cannot establish historical vocabulary growth"
                in row["interpretation_limit"]
                for row in issue_rows
            )
        )

    def test_compatibility_and_stale_inventory_gates(self) -> None:
        overlay = read_csv(OUT / "package_compatibility_overlay_v1.csv")
        self.assertEqual(
            {row["compatibility_status"] for row in overlay},
            {"invariant", "recompute_required", "not_comparable"},
        )
        self.assertTrue(
            all(
                row["research_status"] == "research_only"
                and row["frontend_eligibility"] == "not_frontend_ready"
                and row["central_writeback"] == "no"
                for row in overlay
            )
        )
        inventory = read_csv(OUT / "stale_asset_inventory_v1.csv")
        assets = {row["asset"] for row in inventory}
        self.assertIn(
            "scripts/make_h1_documentation_visibility_v2.py",
            assets,
        )
        self.assertIn(
            "tests/test_make_h2_two_ecologies_v1.py",
            assets,
        )
        self.assertIn(
            "outputs/research_wave_h3_frontline_memory_v1/manifest.json",
            assets,
        )
        self.assertIn(
            "outputs/research_wave_h2_recipient_permeability_v1/"
            "accountability_limited_co_mention_search_v2.csv",
            assets,
        )
        marker_rows = read_csv(OUT / "stale_marker_occurrences_v1.csv")
        self.assertGreater(len(marker_rows), 20)
        protected = read_csv(
            OUT / "protected_legacy_package_hashes_v1.csv"
        )
        self.assertEqual(len(protected), 8)
        self.assertTrue(
            all(row["unchanged_during_build"] == "yes" for row in protected)
        )

    def test_build_is_byte_deterministic(self) -> None:
        before = digest_tree()
        MODULE.main()
        after = digest_tree()
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
