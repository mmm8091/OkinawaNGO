from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from scripts.build_exploration_system_data_v1 import build_exploration_system_data


ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class BuildExplorationSystemDataV1Tests(unittest.TestCase):
    def test_builds_registry_actors_without_changing_the_central_table(self) -> None:
        central = ROOT / "data" / "interim" / "01_actor_registry_initial_v0.csv"
        before = sha256(central)

        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "exploration"
            report = build_exploration_system_data(ROOT, output_dir)
            actors = json.loads((output_dir / "demo" / "actors.json").read_text(encoding="utf-8"))

        self.assertEqual(122, len(actors))
        self.assertEqual(122, report["counts"]["demo"]["actors"])
        self.assertEqual(before, sha256(central))

    def test_actor_aliases_are_attached_to_registry_objects(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "exploration"
            build_exploration_system_data(ROOT, output_dir)
            actors = json.loads((output_dir / "demo/actors.json").read_text(encoding="utf-8"))

        self.assertEqual(27, sum(len(actor["aliases"]) for actor in actors))
        self.assertTrue(all({"label", "type", "source_ids"} <= set(alias) for actor in actors for alias in actor["aliases"]))

    def test_builds_all_core_collections_and_separates_candidate_episodes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "exploration"
            build_exploration_system_data(ROOT, output_dir)

            expected_demo_files = {
                "actors.json",
                "places.json",
                "issues.json",
                "episodes.json",
                "venues.json",
                "outcomes.json",
                "evidence.json",
                "historical_anchors.json",
                "relations.json",
            }
            actual_demo_files = {path.name for path in (output_dir / "demo").glob("*.json")}
            episodes = json.loads((output_dir / "demo" / "episodes.json").read_text(encoding="utf-8"))
            candidates = json.loads(
                (output_dir / "research" / "candidates.json").read_text(encoding="utf-8")
            )

        self.assertTrue(expected_demo_files.issubset(actual_demo_files))
        self.assertEqual(9, len(episodes))
        self.assertEqual(4, len(candidates["episodes"]))
        self.assertNotIn(
            "analytic_candidate_event_pending",
            {episode["review_status"] for episode in episodes},
        )

    def test_demo_relations_are_review_gated_and_source_refs_resolve(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "exploration"
            build_exploration_system_data(ROOT, output_dir)
            episodes = json.loads((output_dir / "demo/episodes.json").read_text(encoding="utf-8"))
            actors = json.loads((output_dir / "demo/actors.json").read_text(encoding="utf-8"))
            relations = json.loads((output_dir / "demo/relations.json").read_text(encoding="utf-8"))
            evidence = json.loads((output_dir / "demo/evidence.json").read_text(encoding="utf-8"))

        source_ids = {source["id"] for source in evidence["sources"]}
        for episode in episodes:
            self.assertTrue(episode["source_ids"])
            self.assertTrue(set(episode["source_ids"]).issubset(source_ids))
        for actor in actors:
            self.assertTrue(set(actor["source_ids"]).issubset(source_ids))
        for relation_group in relations.values():
            for relation in relation_group:
                self.assertEqual("demo", relation["display_status"])
                self.assertTrue(set(relation["source_ids"]).issubset(source_ids))

        rejected = next(source for source in evidence["sources"] if source["id"] == "S051")
        self.assertFalse(rejected["can_support_claim"])
        self.assertNotIn(
            "analytical_seed",
            {row["review_status"] for row in relations["event_participation"]},
        )

    def test_builds_four_page_view_models_and_global_layers(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "exploration"
            build_exploration_system_data(ROOT, output_dir)
            views = {
                path.stem: json.loads(path.read_text(encoding="utf-8"))
                for path in (output_dir / "views").glob("*.json")
            }

        self.assertEqual(
            {"overview", "actors", "pathways", "evidence_coverage", "global"},
            set(views),
        )
        self.assertEqual("P1", views["overview"]["view_id"])
        self.assertEqual(20, len(views["overview"]["place_ids"]))
        self.assertEqual(16, len(views["overview"]["actor_place_relation_ids"]))
        self.assertEqual(67, len(views["overview"]["strict_place_issue_relation_ids"]))
        self.assertEqual("P2", views["actors"]["view_id"])
        self.assertEqual(122, len(views["actors"]["actor_ids"]))
        self.assertEqual(59, len(views["actors"]["actor_issue_relation_ids"]))
        self.assertEqual("P3", views["pathways"]["view_id"])
        self.assertEqual(9, len(views["pathways"]["episode_ids"]))
        self.assertEqual("P4", views["evidence_coverage"]["view_id"])
        self.assertEqual(125, len(views["evidence_coverage"]["cells"]))
        self.assertEqual(6, len(views["evidence_coverage"]["implications"]))
        self.assertEqual("G1+G2", views["global"]["view_id"])

    def test_packages_map_geometry_for_the_overview_view(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "exploration"
            build_exploration_system_data(ROOT, output_dir)
            geometry = json.loads(
                (output_dir / "demo/map_geometry.geojson").read_text(encoding="utf-8")
            )
            overview = json.loads(
                (output_dir / "views/overview.json").read_text(encoding="utf-8")
            )

        self.assertEqual("FeatureCollection", geometry["type"])
        self.assertEqual(42, len(geometry["features"]))
        self.assertEqual("../demo/map_geometry.geojson", overview["map_geometry"]["path"])
        self.assertEqual(42, overview["map_geometry"]["feature_count"])

    def test_quarantines_actor_place_key_label_conflicts(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "exploration"
            build_exploration_system_data(ROOT, output_dir)
            demo = json.loads((output_dir / "demo/relations.json").read_text(encoding="utf-8"))
            candidates = json.loads(
                (output_dir / "research/candidates.json").read_text(encoding="utf-8")
            )

        self.assertNotIn("AP123", {row["id"] for row in demo["actor_place"]})
        ap123 = next(
            row for row in candidates["relations"]["actor_place"] if row["id"] == "AP123"
        )
        self.assertEqual("place_key_label_conflict", ap123["quarantine_reason"])

    def test_manifest_and_validation_are_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            first = Path(temp_dir) / "first"
            second = Path(temp_dir) / "second"
            build_exploration_system_data(ROOT, first)
            build_exploration_system_data(ROOT, second)

            first_manifest = json.loads((first / "manifest.json").read_text(encoding="utf-8"))
            second_manifest = json.loads((second / "manifest.json").read_text(encoding="utf-8"))
            validation = (first / "validation_report.md").read_text(encoding="utf-8")

        self.assertEqual(first_manifest, second_manifest)
        self.assertEqual("pass", first_manifest["validation"]["status"])
        self.assertEqual(0, first_manifest["validation"]["error_count"])
        self.assertTrue(first_manifest["deterministic"])
        self.assertIn("PASS", validation)
        self.assertEqual(
            first_manifest["output_hashes"],
            second_manifest["output_hashes"],
        )


if __name__ == "__main__":
    unittest.main()
