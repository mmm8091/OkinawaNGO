from __future__ import annotations

import csv
import hashlib
import json
import shutil
import tempfile
import unittest
from collections import Counter
from pathlib import Path
from unittest import mock

import scripts.build_exploration_system_data_v1 as builder
from scripts.build_exploration_system_data_v1 import (
    TYPED_RELATION_FIELDS,
    build_exploration_system_data,
    exploration_input_paths,
)


ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def copy_inputs_to_workspace(workspace: Path) -> Path:
    """Mirror every build input into a throwaway project root."""
    root = workspace / "root"
    for path in exploration_input_paths(ROOT).values():
        target = root / path.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
    return root


def rewrite_csv_row(path: Path, row_id: str, **changes: str) -> None:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = list(reader.fieldnames or [])
        rows = list(reader)
    matched = False
    for row in rows:
        if (row.get("id") or row.get("edge_id")) == row_id:
            row.update(changes)
            matched = True
    if not matched:
        raise AssertionError(f"row {row_id} not found in {path}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def typed_handoff_path(root: Path) -> Path:
    return root / "outputs/hr033_integration_v1/typed_relation_observations_v1.csv"


def funding_relations_path(root: Path) -> Path:
    return root / "data/interim/15_funding_or_support_edges_sample_v0.csv"


def actor_issue_path(root: Path) -> Path:
    return root / "data/interim/07_actor_issue_edges_initial_v0.csv"


def episode_display_path(root: Path) -> Path:
    return root / "data/metadata/episode_display_trilingual_v1.csv"


def rewrite_episode_display_row(
    path: Path,
    episode_id: str,
    field: str,
    **changes: str,
) -> None:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = list(reader.fieldnames or [])
        rows = list(reader)
    matched = False
    for row in rows:
        if row.get("episode_id") == episode_id and row.get("field") == field:
            row.update(changes)
            matched = True
    if not matched:
        raise AssertionError(f"row {episode_id}:{field} not found in {path}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)



class BuildExplorationSystemDataV1Tests(unittest.TestCase):
    def test_actor_view_and_manifest_distinguish_current_actors_from_provenance(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "exploration"
            manifest = build_exploration_system_data(ROOT, output_dir)
            actors = json.loads(
                (output_dir / "demo" / "actors.json").read_text(encoding="utf-8")
            )
            actor_view = json.loads(
                (output_dir / "views" / "actors.json").read_text(encoding="utf-8")
            )

        self.assertEqual("2026-07-20", manifest["as_of_date"])
        self.assertEqual(122, len(actors))
        self.assertEqual(121, len(actor_view["actor_ids"]))
        self.assertNotIn("A072", actor_view["actor_ids"])
        self.assertEqual(
            {
                "provenance_rows": 122,
                "current_visible": 121,
                "hidden_provenance_rows": 1,
            },
            manifest["counts"]["actor_registry"],
        )
        self.assertEqual(121, manifest["counts"]["demo"]["actors"])

    def test_builds_registry_actors_without_changing_the_central_table(self) -> None:
        central = ROOT / "data" / "interim" / "01_actor_registry_initial_v0.csv"
        before = sha256(central)

        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "exploration"
            report = build_exploration_system_data(ROOT, output_dir)
            actors = json.loads((output_dir / "demo" / "actors.json").read_text(encoding="utf-8"))

        self.assertEqual(122, len(actors))
        self.assertEqual(121, report["counts"]["demo"]["actors"])
        self.assertEqual(122, report["counts"]["actor_registry"]["provenance_rows"])
        a072 = next(row for row in actors if row["id"] == "A072")
        self.assertEqual("hidden", a072["display_status"])
        self.assertEqual("A071", a072["merged_duplicate_of"])
        self.assertEqual(before, sha256(central))

    def test_actor_aliases_are_attached_to_registry_objects(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "exploration"
            build_exploration_system_data(ROOT, output_dir)
            actors = json.loads((output_dir / "demo/actors.json").read_text(encoding="utf-8"))

        self.assertEqual(39, sum(len(actor["aliases"]) for actor in actors))
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

    def test_episode_display_overlay_localizes_every_field_without_mutating_facts(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "exploration"
            manifest = build_exploration_system_data(ROOT, output_dir)
            episodes = json.loads(
                (output_dir / "demo/episodes.json").read_text(encoding="utf-8")
            )
            candidates = json.loads(
                (output_dir / "research/candidates.json").read_text(encoding="utf-8")
            )
            outcomes = json.loads(
                (output_dir / "demo/outcomes.json").read_text(encoding="utf-8")
            )

        all_episodes = episodes + candidates["episodes"]
        self.assertEqual(13, len(all_episodes))
        self.assertEqual(
            {"TE10", "TE11", "TE12", "TE13"},
            {row["id"] for row in candidates["episodes"]},
        )
        self.assertEqual(
            {"analytic_candidate_event_pending"},
            {row["review_status"] for row in candidates["episodes"]},
        )
        self.assertEqual("1.1.0", manifest["schema_version"])
        self.assertEqual(
            {
                "episodes": 13,
                "fields_per_episode": 7,
                "approved_translation_cells": 273,
                "source_text_fallbacks": 0,
            },
            manifest["counts"]["episode_display"],
        )
        te01 = next(row for row in all_episodes if row["id"] == "TE01")
        self.assertEqual("儒艮海外诉讼", te01["display_label"])
        self.assertEqual("儒艮海外诉讼", te01["display_label_zh"])
        self.assertEqual("ジュゴン米国訴訟", te01["display_label_ja"])
        self.assertEqual(
            "Okinawa dugong litigation in U.S. federal court",
            te01["display_label_en"],
        )
        for episode in all_episodes:
            for field in builder.EPISODE_DISPLAY_FIELDS:
                self.assertEqual(episode[field], episode[f"{field}_zh"])
                self.assertTrue(episode[f"{field}_ja"])
                self.assertTrue(episode[f"{field}_en"])
        te01_outcome = next(
            row
            for row in outcomes
            if row["id"] == "TE01:intermediate_output"
        )
        self.assertEqual(
            "Section 402 applicability, reviewable standards, public record",
            te01_outcome["display_label_en"],
        )

    def test_episode_display_overlay_rejects_missing_approved_language(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = copy_inputs_to_workspace(Path(temp_dir))
            rewrite_episode_display_row(
                episode_display_path(root),
                "TE01",
                "display_label",
                ja="",
            )
            with self.assertRaisesRegex(ValueError, "non-empty zh/ja/en"):
                build_exploration_system_data(root, Path(temp_dir) / "out")

    def test_episode_display_overlay_rejects_semantic_rewrites_and_duplicate_keys(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = copy_inputs_to_workspace(Path(temp_dir))
            path = episode_display_path(root)
            rewrite_episode_display_row(
                path,
                "TE01",
                "display_label",
                zh="不是中央原文",
            )
            with self.assertRaisesRegex(ValueError, "must equal the source text"):
                build_exploration_system_data(root, Path(temp_dir) / "out")

        with tempfile.TemporaryDirectory() as temp_dir:
            root = copy_inputs_to_workspace(Path(temp_dir))
            path = episode_display_path(root)
            with path.open(encoding="utf-8-sig", newline="") as handle:
                reader = csv.DictReader(handle)
                fields = list(reader.fieldnames or [])
                rows = list(reader)
            rows.append(dict(rows[0]))
            with path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=fields)
                writer.writeheader()
                writer.writerows(rows)
            with self.assertRaisesRegex(ValueError, "duplicate keys"):
                build_exploration_system_data(root, Path(temp_dir) / "out")

    def test_episode_display_overlay_rejects_missing_or_unknown_pairs(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = copy_inputs_to_workspace(Path(temp_dir))
            path = episode_display_path(root)
            with path.open(encoding="utf-8-sig", newline="") as handle:
                reader = csv.DictReader(handle)
                fields = list(reader.fieldnames or [])
                rows = list(reader)
            rows[0]["episode_id"] = "TE99"
            with path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=fields)
                writer.writeheader()
                writer.writerows(rows)
            with self.assertRaisesRegex(
                ValueError,
                "exact episode/field grid.*missing=.*unexpected=",
            ):
                build_exploration_system_data(root, Path(temp_dir) / "out")

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

    def test_default_actor_issue_graph_excludes_deactivated_and_event_only_rows(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "exploration"
            build_exploration_system_data(ROOT, output_dir)
            relations = json.loads(
                (output_dir / "demo/relations.json").read_text(encoding="utf-8")
            )
            candidates = json.loads(
                (output_dir / "research/candidates.json").read_text(encoding="utf-8")
            )

        active_ids = {row["id"] for row in relations["actor_issue"]} | {
            row["id"] for row in candidates["relations"]["actor_issue"]
        }
        self.assertEqual(283, len(active_ids))
        self.assertNotIn("AI068", active_ids)
        self.assertNotIn("AI116", active_ids)
        self.assertNotIn("AI038", active_ids)

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
        self.assertEqual(21, len(views["overview"]["place_ids"]))
        self.assertEqual(53, len(views["overview"]["actor_place_relation_ids"]))
        self.assertEqual(81, len(views["overview"]["strict_place_issue_relation_ids"]))
        self.assertEqual("P2", views["actors"]["view_id"])
        self.assertEqual(121, len(views["actors"]["actor_ids"]))
        self.assertNotIn("A072", views["actors"]["actor_ids"])
        self.assertEqual(141, len(views["actors"]["actor_issue_relation_ids"]))
        self.assertEqual("P3", views["pathways"]["view_id"])
        self.assertEqual(9, len(views["pathways"]["episode_ids"]))
        self.assertEqual("P4", views["evidence_coverage"]["view_id"])
        coverage_cells = views["evidence_coverage"]["cells"]
        coverage_implications = views["evidence_coverage"]["implications"]
        self.assertGreater(len(coverage_cells), 6)
        self.assertEqual(
            {"D1", "D2", "D3", "D4", "D5", "D6"},
            {row["dimension_id"] for row in coverage_cells},
        )
        self.assertEqual(
            {"D1", "D2", "D3", "D4", "D5", "D6"},
            {row["dimension_id"] for row in coverage_implications},
        )
        self.assertEqual(
            {130},
            {
                row["denominator"]
                for row in coverage_cells
                if row["dimension_id"] == "D2"
            },
        )
        self.assertEqual(
            {121},
            {
                row["denominator"]
                for row in coverage_cells
                if row["dimension_id"] in {"D3", "D4"}
            },
        )
        self.assertEqual(
            {283},
            {
                row["denominator"]
                for row in coverage_cells
                if row["facet"].startswith("actor_issue_observations_")
            },
        )
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

    def test_uses_repaired_ap123_and_hides_retired_place_edges(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "exploration"
            build_exploration_system_data(ROOT, output_dir)
            demo = json.loads((output_dir / "demo/relations.json").read_text(encoding="utf-8"))
            candidates = json.loads(
                (output_dir / "research/candidates.json").read_text(encoding="utf-8")
            )

        demo_by_id = {row["id"]: row for row in demo["actor_place"]}
        self.assertEqual("P007", demo_by_id["AP123"]["place_id"])
        self.assertEqual("Camp Foster", demo_by_id["AP123"]["canonical_place_label"])
        self.assertEqual("", demo_by_id["AP123"]["quarantine_reason"])
        all_place_ids = set(demo_by_id) | {
            row["id"] for row in candidates["relations"]["actor_place"]
        }
        self.assertNotIn("AP048", all_place_ids)
        self.assertNotIn("AP118", all_place_ids)

    def test_manifest_and_validation_are_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            first = Path(temp_dir) / "first"
            second = Path(temp_dir) / "second"
            build_exploration_system_data(ROOT, first)
            build_exploration_system_data(ROOT, second)

            first_manifest = json.loads((first / "manifest.json").read_text(encoding="utf-8"))
            second_manifest = json.loads((second / "manifest.json").read_text(encoding="utf-8"))
            validation = (first / "validation_report.md").read_text(encoding="utf-8")
            actual_output_hashes = {
                relative: sha256(first / relative)
                for relative in first_manifest["output_hashes"]
            }

        self.assertEqual(first_manifest, second_manifest)
        self.assertEqual("pass", first_manifest["validation"]["status"])
        self.assertEqual(0, first_manifest["validation"]["error_count"])
        self.assertTrue(first_manifest["deterministic"])
        self.assertIn("PASS", validation)
        self.assertEqual(
            first_manifest["output_hashes"],
            second_manifest["output_hashes"],
        )
        self.assertEqual(22, len(first_manifest["input_hashes"]))
        self.assertEqual(
            {
                key: sha256(path)
                for key, path in sorted(exploration_input_paths(ROOT).items())
            },
            first_manifest["input_hashes"],
        )
        self.assertEqual(actual_output_hashes, first_manifest["output_hashes"])

    def test_typed_relation_collections_match_control_cases(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "exploration"
            report = build_exploration_system_data(ROOT, output_dir)
            demo = {
                name: json.loads(
                    (output_dir / "demo" / f"{name}.json").read_text(encoding="utf-8")
                )
                for name in (
                    "dyadic_relations",
                    "administrative_records",
                    "aggregate_observations",
                    "relation_leads",
                    "case_roles",
                    "genealogy_anchors",
                    "typed_event_participation",
                )
            }
            relations = json.loads(
                (output_dir / "demo/relations.json").read_text(encoding="utf-8")
            )

        dyadic_by_id = {row["id"]: row for row in demo["dyadic_relations"]}
        self.assertEqual(14, len(dyadic_by_id))

        f021 = dyadic_by_id["F021"]
        self.assertEqual("3250", f021["amount"])
        self.assertEqual("direct_charitable_donation", f021["amount_semantics"])
        self.assertEqual("resources_funding", f021["relation_family"])
        self.assertEqual("supported", f021["claim_status"])
        self.assertEqual("reviewed", f021["display_tier"])
        self.assertEqual("revise", f021["human_decision"])

        f025 = dyadic_by_id["F025"]
        self.assertEqual("supported_bounded", f025["claim_status"])
        self.assertEqual("", f025["amount"])
        self.assertTrue(f025["missing_scope"])
        self.assertTrue(f025["confirmed_scope"])
        self.assertTrue(f025["interpretation_limit"])

        aggregate_ids = {row["id"] for row in demo["aggregate_observations"]}
        self.assertEqual({"F027", "R10R029"}, aggregate_ids)
        self.assertNotIn("R10R029", dyadic_by_id)
        r10r029 = next(
            row for row in demo["aggregate_observations"] if row["id"] == "R10R029"
        )
        self.assertEqual("102000", r10r029["amount"])
        self.assertEqual("supported_bounded", r10r029["claim_status"])
        self.assertEqual("aggregate_observation", r10r029["graph_eligibility"])

        self.assertEqual(
            {"F028", "F029", "F030", "F031", "F032", "F033"},
            {row["id"] for row in demo["administrative_records"]},
        )
        self.assertEqual([], demo["relation_leads"])
        self.assertEqual([], demo["genealogy_anchors"])
        self.assertEqual(
            {"F011", "F036", "F040", "F041"},
            {row["id"] for row in demo["typed_event_participation"]},
        )
        f036 = next(
            row for row in demo["typed_event_participation"] if row["id"] == "F036"
        )
        self.assertEqual("event_participation", f036["graph_eligibility"])
        self.assertEqual(
            "no_amount_no_contributor_share_allocation",
            f036["amount_semantics"],
        )

        typed_rows = [
            row
            for name, rows in demo.items()
            if name != "case_roles"
            for row in rows
        ]
        self.assertNotIn("F008", {row["id"] for row in typed_rows})
        for row in typed_rows:
            self.assertTrue(set(TYPED_RELATION_FIELDS) <= set(row), row["id"])

        case_roles = demo["case_roles"]
        self.assertEqual(27, len(case_roles))
        self.assertEqual(
            [row["id"] for row in relations["legal_roles"]],
            [row["id"] for row in case_roles],
        )
        self.assertTrue(any(row["role"] == "non_party" for row in case_roles))
        self.assertTrue(
            all(row["observation_kind"] != "case_role" for row in demo["dyadic_relations"])
        )

        typed_counts = report["counts"]["typed_relations"]
        self.assertEqual(44, typed_counts["input_observations"])
        self.assertEqual(1, typed_counts["excluded"])
        self.assertEqual(14, typed_counts["demo"]["dyadic_relations"])
        self.assertEqual(2, typed_counts["demo"]["aggregate_observations"])
        self.assertEqual(4, typed_counts["demo"]["event_participation"])
        self.assertEqual(27, typed_counts["demo"]["case_roles"])

    def test_typed_relation_research_layer_and_source_refs(self) -> None:
        central = ROOT / "data" / "interim" / "15_funding_or_support_edges_sample_v0.csv"
        before = sha256(central)

        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "exploration"
            build_exploration_system_data(ROOT, output_dir)
            candidates = json.loads(
                (output_dir / "research/candidates.json").read_text(encoding="utf-8")
            )
            demo_dyadic = json.loads(
                (output_dir / "demo/dyadic_relations.json").read_text(encoding="utf-8")
            )
            typed_events = json.loads(
                (output_dir / "demo/typed_event_participation.json").read_text(
                    encoding="utf-8"
                )
            )

        self.assertEqual(before, sha256(central))
        for key in (
            "dyadic_relations",
            "administrative_records",
            "aggregate_observations",
            "relation_leads",
            "event_participation",
            "genealogy_anchors",
        ):
            self.assertIn(key, candidates)
        self.assertEqual(8, len(candidates["dyadic_relations"]))
        self.assertEqual(5, len(candidates["administrative_records"]))
        self.assertEqual(0, len(candidates["aggregate_observations"]))
        self.assertEqual(4, len(candidates["relation_leads"]))
        self.assertEqual(0, len(candidates["event_participation"]))
        self.assertEqual([], candidates["genealogy_anchors"])

        leads_by_id = {row["id"]: row for row in candidates["relation_leads"]}
        self.assertEqual({"F012", "F013", "F034", "F035"}, set(leads_by_id))
        for lead in leads_by_id.values():
            self.assertEqual("research_lead", lead["graph_eligibility"])
            self.assertEqual("research", lead["display_tier"])
        self.assertEqual("lead", leads_by_id["F012"]["claim_status"])
        self.assertEqual("supported_bounded", leads_by_id["F034"]["claim_status"])
        self.assertEqual("unknown_recipient", leads_by_id["F012"]["scope_kind"])
        # F013 has two registry endpoints but stays a lead, never dyadic.
        research_dyadic_ids = {row["id"] for row in candidates["dyadic_relations"]}
        demo_dyadic_by_id = {row["id"]: row for row in demo_dyadic}
        self.assertNotIn("F013", research_dyadic_ids | set(demo_dyadic_by_id))

        # Legacy X-code references never enter source_ids; they stay explicit.
        f001 = next(
            row for row in candidates["dyadic_relations"] if row["id"] == "F001"
        )
        self.assertEqual("candidate", f001["claim_status"])
        self.assertEqual([], f001["source_ids"])
        self.assertEqual(["X002"], f001["unresolved_source_refs"])
        f011 = next(row for row in typed_events if row["id"] == "F011")
        self.assertEqual(["S095"], f011["source_ids"])
        self.assertEqual(["X011"], f011["unresolved_source_refs"])

    def test_gate_rejects_legacy_review_status(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = copy_inputs_to_workspace(Path(temp_dir))
            rewrite_csv_row(
                funding_relations_path(root), "F006", review_status="verified"
            )
            with self.assertRaisesRegex(ValueError, "requires a human crosswalk"):
                build_exploration_system_data(root, Path(temp_dir) / "out")

    def test_gate_rejects_unresolvable_dyadic_endpoint(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = copy_inputs_to_workspace(Path(temp_dir))
            rewrite_csv_row(
                funding_relations_path(root), "F006", target_actor_id="A999"
            )
            with self.assertRaisesRegex(ValueError, "resolve to registry actors"):
                build_exploration_system_data(root, Path(temp_dir) / "out")

    def test_gate_rejects_lead_in_dyadic_relations(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = copy_inputs_to_workspace(Path(temp_dir))
            rewrite_csv_row(funding_relations_path(root), "F006", claim_status="lead")
            with self.assertRaisesRegex(ValueError, "no leads enter dyadic relations"):
                build_exploration_system_data(root, Path(temp_dir) / "out")

    def test_gate_hides_rejected_rows(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = copy_inputs_to_workspace(Path(temp_dir))
            rewrite_csv_row(
                funding_relations_path(root), "F006", review_status="rejected"
            )
            output = Path(temp_dir) / "out"
            build_exploration_system_data(root, output)
            serialized = "\n".join(
                path.read_text(encoding="utf-8") for path in output.rglob("*.json")
            )
            self.assertNotIn('"id": "F006"', serialized)

    def test_controlled_derivation_fills_missing_scope_boundaries(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = copy_inputs_to_workspace(Path(temp_dir))
            rewrite_csv_row(funding_relations_path(root), "F025", missing_scope="")
            rewrite_csv_row(typed_handoff_path(root), "F025", missing_scope="")
            output = Path(temp_dir) / "out"
            build_exploration_system_data(root, output)
            dyadic = json.loads(
                (output / "demo/dyadic_relations.json").read_text(encoding="utf-8")
            )
            f025 = next(row for row in dyadic if row["id"] == "F025")
            self.assertTrue(f025["missing_scope"])

    def test_central_reviewed_fields_override_handoff_and_derivation(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = copy_inputs_to_workspace(Path(temp_dir))
            rewrite_csv_row(
                typed_handoff_path(root),
                "F025",
                claim_status="candidate",
                graph_eligibility="research_lead",
                amount="102000",
            )
            output = Path(temp_dir) / "out"
            build_exploration_system_data(root, output)
            dyadic = json.loads(
                (output / "demo/dyadic_relations.json").read_text(encoding="utf-8")
            )
            f025 = next(row for row in dyadic if row["id"] == "F025")
            self.assertEqual("supported_bounded", f025["claim_status"])
            self.assertEqual("dyadic_relation", f025["graph_eligibility"])
            self.assertEqual("", f025["amount"])

    def test_actor_issue_display_states_match_handoff_counts(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "exploration"
            manifest = build_exploration_system_data(ROOT, output_dir)
            demo = json.loads(
                (output_dir / "demo/relations.json").read_text(encoding="utf-8")
            )
            candidates = json.loads(
                (output_dir / "research/candidates.json").read_text(encoding="utf-8")
            )

        demo_ai = demo["actor_issue"]
        research_ai = candidates["relations"]["actor_issue"]
        self.assertEqual(141, len(demo_ai))
        self.assertEqual(142, len(research_ai))
        all_rows = demo_ai + research_ai
        display_counts = Counter(row["display_state"] for row in all_rows)
        self.assertEqual(
            {
                "frozen_bounded": 83,
                "accepted_unfrozen": 58,
                "scope_reviewed_fact_pending": 28,
                "fact_pending": 114,
            },
            dict(display_counts),
        )
        fact_counts = Counter(row["fact_gate_status"] for row in research_ai)
        self.assertEqual(27, fact_counts["needs_second_source"])
        self.assertEqual(5, fact_counts["needs_local_retrieval"])
        self.assertEqual(110, fact_counts["fact_pending"])

        states_block = manifest["counts"]["actor_issue_states"]
        self.assertEqual(283, states_block["valid_edges"])
        self.assertEqual(dict(display_counts), states_block["display_state_counts"])
        self.assertEqual(
            dict(fact_counts), states_block["research_fact_gate_counts"]
        )

        # The reviewed fact layer holds only accepted states.
        self.assertEqual(
            {"frozen_bounded", "accepted_unfrozen"},
            {row["display_state"] for row in demo_ai},
        )
        # Scope-reviewed but fact-pending rows never enter the reviewed fact layer.
        self.assertTrue(
            all(
                row["scope_gate_status"] == "scope_reviewed"
                for row in research_ai
                if row["display_state"] == "scope_reviewed_fact_pending"
            )
        )
        # All currently accepted-and-bounded central rows carry the frozen field set.
        frozen = [row for row in demo_ai if row["display_state"] == "frozen_bounded"]
        with (ROOT / "data/interim/07_actor_issue_edges_initial_v0.csv").open(
            encoding="utf-8-sig", newline=""
        ) as handle:
            expected_frozen = {
                row["edge_id"]
                for row in csv.DictReader(handle)
                if row["review_status"] in {"human_checked", "human_revised"}
                and row["claim_status"] == "supported_bounded"
                and row["graph_eligibility"] != "excluded"
                and not any(
                    token in row["scope_status"]
                    for token in ("excluded", "retired", "deactivated")
                )
            }
        self.assertEqual(
            expected_frozen,
            {row["id"] for row in frozen},
        )
        for row in frozen:
            self.assertEqual("supported_bounded", row["claim_status"])
            self.assertEqual("field_frozen", row["schema_freeze_status"])
            self.assertTrue(row["missing_scope"])
        # Legacy accepted rows stay unfrozen and are never auto-filled to supported.
        legacy = [row for row in demo_ai if row["display_state"] == "accepted_unfrozen"]
        self.assertTrue(
            all(
                row["schema_freeze_status"] == "legacy_field_freeze_pending"
                for row in legacy
            )
        )
        self.assertNotIn("supported", {row["claim_status"] for row in all_rows})
        # Pass-through and derived fields exist on every actor-issue row.
        for row in all_rows:
            for field in (
                "claim_status",
                "review_scope",
                "reviewed_fields",
                "scope_kind",
                "scope_claim_status",
                "scope_approved_formulation",
                "scope_boundary",
                "confirmed_scope",
                "missing_scope",
                "approved_formulation",
                "fact_gate_status",
                "scope_gate_status",
                "schema_freeze_status",
                "display_state",
            ):
                self.assertIn(field, row)
        # A073 generates no edge.
        self.assertNotIn("A073", {row["actor_id"] for row in all_rows})

    def test_gate_actor_issue_frozen_rows_require_missing_scope(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = copy_inputs_to_workspace(Path(temp_dir))
            rewrite_csv_row(actor_issue_path(root), "AI242", missing_scope="")
            with self.assertRaisesRegex(ValueError, "missing_scope"):
                build_exploration_system_data(root, Path(temp_dir) / "out")

    def test_gate_actor_issue_display_state_must_be_legal(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            with mock.patch.object(
                builder,
                "derive_actor_issue_gate_states",
                side_effect=lambda row: {
                    "fact_gate_status": "fact_pending",
                    "scope_gate_status": "scope_pending",
                    "schema_freeze_status": "",
                    "display_state": "",
                },
            ):
                with self.assertRaisesRegex(
                    ValueError, "display_state values are legal"
                ):
                    build_exploration_system_data(ROOT, Path(temp_dir) / "out")

    def test_gate_actor_issue_demo_layer_rejects_fact_pending(self) -> None:
        original = builder.derive_actor_issue_gate_states

        def pending_for_accepted(row: dict) -> dict:
            states = original(row)
            if states["fact_gate_status"] == "human_accepted":
                states["display_state"] = "fact_pending"
            return states

        with tempfile.TemporaryDirectory() as temp_dir:
            with mock.patch.object(
                builder,
                "derive_actor_issue_gate_states",
                side_effect=pending_for_accepted,
            ):
                with self.assertRaisesRegex(ValueError, "fact-pending"):
                    build_exploration_system_data(ROOT, Path(temp_dir) / "out")



if __name__ == "__main__":
    unittest.main()
