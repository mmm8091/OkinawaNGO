from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import research_publication.compiler as compiler
from research_publication import (
    PublicationError,
    compile_publication_snapshot,
    verify_publication_channel,
    verify_publication_snapshot,
)
from scripts.build_publication_snapshot_v1 import default_channel_path


ROOT = Path(__file__).resolve().parents[1]


class ResearchPublicationCompilerV1Tests(unittest.TestCase):
    def test_default_channel_is_profile_specific(self) -> None:
        self.assertEqual(
            Path("outputs/publication_channels_v1/reviewed.json"),
            default_channel_path("reviewed"),
        )
        self.assertEqual(
            Path("outputs/publication_channels_v1/client_preview.json"),
            default_channel_path("client_preview"),
        )
        self.assertEqual(
            Path("outputs/publication_channels_v1/internal.json"),
            default_channel_path("internal"),
        )

    def test_client_preview_is_deterministic_and_strips_internal_fields(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            first = Path(temp_dir) / "first"
            second = Path(temp_dir) / "second"
            first_manifest = compile_publication_snapshot(
                ROOT, first, profile="client_preview"
            )
            second_manifest = compile_publication_snapshot(
                ROOT, second, profile="client_preview"
            )
            first_release = (
                first / "client_preview" / first_manifest["release_id"]
            )
            second_release = (
                second / "client_preview" / second_manifest["release_id"]
            )
            evidence = json.loads(
                (first_release / "core/evidence/sources.json").read_text(
                    encoding="utf-8"
                )
            )
            catalog = json.loads(
                (first_release / "views/publication_catalog.json").read_text(
                    encoding="utf-8"
                )
            )
            object_index = json.loads(
                (first_release / "views/exhibits.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(first_manifest, second_manifest)
            self.assertEqual(
                first_manifest["release_id"],
                second_manifest["release_id"],
            )
            self.assertTrue(first_manifest["public"])
            self.assertTrue(first_manifest["capabilities"]["research_candidates"])
            self.assertTrue((first_release / "research/actor_issue.json").exists())
            self.assertFalse((first_release / "validation_report.md").exists())
            self.assertFalse((first_release / "internal").exists())
            self.assertTrue((second_release / "manifest.json").exists())
            self.assertNotIn("archive_path", evidence["sources"][0])
            self.assertNotIn("archive_sha256", evidence["sources"][0])
            self.assertNotIn("assets", catalog["entries"][0])
            self.assertNotIn("review_status", catalog["entries"][0])
            self.assertNotIn("next_gate", catalog["entries"][0])
            self.assertEqual(
                {
                    "PUB-ARC-001",
                    "PUB-ARC-002",
                    "PUB-ARC-003",
                    "PUB-MR-004",
                    "PUB-MR-005",
                    "PUB-MR-012",
                    "PUB-MR-013",
                    "PUB-MR-014",
                },
                {entry["id"] for entry in catalog["entries"]},
            )
            self.assertEqual(
                {
                    "PUB-ARC-001",
                    "PUB-ARC-002",
                    "PUB-ARC-003",
                    "PUB-MR-004",
                    "PUB-MR-005",
                    "PUB-MR-012",
                    "PUB-MR-013",
                    "PUB-MR-014",
                },
                {entry["catalog_id"] for entry in object_index["entries"]},
            )
            for exhibit_id in ("PUB-MR-004", "PUB-MR-005", "PUB-MR-012"):
                self.assertTrue(
                    (first_release / f"exhibits/{exhibit_id}.json").exists()
                )
                payload = json.loads(
                    (first_release / f"exhibits/{exhibit_id}.json").read_text(
                        encoding="utf-8"
                    )
                )
                self.assertEqual(
                    exhibit_id,
                    payload["publication"]["catalog_id"],
                )
            for core_id in (
                "PUB-ARC-001",
                "PUB-ARC-002",
                "PUB-ARC-003",
                "PUB-MR-013",
                "PUB-MR-014",
            ):
                self.assertTrue(
                    (
                        first_release
                        / f"views/core_surfaces/{core_id}.json"
                    ).exists()
                )

    def test_reviewed_profile_physically_excludes_candidates(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "reviewed"
            manifest = compile_publication_snapshot(
                ROOT, output, profile="reviewed"
            )
            release = output / "reviewed" / manifest["release_id"]
            report = verify_publication_snapshot(release)
            catalog = json.loads(
                (release / "views/publication_catalog.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertFalse(manifest["capabilities"]["research_candidates"])
            self.assertFalse((release / "research").exists())
            self.assertNotIn(
                "PUB-MR-004",
                {entry["id"] for entry in catalog["entries"]},
            )
            self.assertFalse((release / "exhibits/PUB-MR-004.json").exists())
            self.assertEqual("pass", report["status"])

    def test_verifier_rejects_files_missing_from_the_checksum_contract(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "reviewed"
            manifest = compile_publication_snapshot(
                ROOT, output, profile="reviewed"
            )
            release = output / "reviewed" / manifest["release_id"]
            (release / "untracked.txt").write_text("leak", encoding="utf-8")
            leak = release / "research/leak.json"
            leak.parent.mkdir(parents=True)
            leak.write_text("{}\n", encoding="utf-8")

            report = verify_publication_snapshot(release)

        self.assertEqual("fail", report["status"])
        self.assertTrue(
            any("file set differs" in error for error in report["errors"])
        )

    def test_core_builder_contract_rejects_unmanifested_output(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            core = Path(temp_dir) / "core"
            snapshot = Path(temp_dir) / "snapshot"
            core.mkdir()
            (core / "manifest.json").write_text("{}\n", encoding="utf-8")
            (core / "known.json").write_text("{}\n", encoding="utf-8")
            (core / "unknown.json").write_text("{}\n", encoding="utf-8")

            with self.assertRaisesRegex(
                PublicationError,
                "outside its manifest contract",
            ):
                compiler._assert_core_builder_contract(
                    core,
                    manifested_paths={"known.json"},
                )

    def test_public_snapshot_only_contains_registered_core_projections(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "releases"
            manifest = compile_publication_snapshot(
                ROOT,
                output,
                profile="client_preview",
            )
            release = output / "client_preview" / manifest["release_id"]
            self.assertTrue((release / "core/relations/actor_issue.json").exists())
            self.assertTrue((release / "research/actor_issue.json").exists())
            for legacy_path in (
                "demo/relations.json",
                "research/candidates.json",
                "views/global.json",
                "views/overview.json",
                "views/actors.json",
                "demo/historical_anchors.json",
            ):
                self.assertFalse((release / legacy_path).exists(), legacy_path)

    def test_reviewed_profile_filters_deferred_aggregate_record(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            reviewed_output = Path(temp_dir) / "reviewed"
            client_output = Path(temp_dir) / "client"
            reviewed_manifest = compile_publication_snapshot(
                ROOT,
                reviewed_output,
                profile="reviewed",
            )
            client_manifest = compile_publication_snapshot(
                ROOT,
                client_output,
                profile="client_preview",
            )
            reviewed_release = (
                reviewed_output
                / "reviewed"
                / reviewed_manifest["release_id"]
            )
            client_release = (
                client_output
                / "client_preview"
                / client_manifest["release_id"]
            )
            reviewed_rows = json.loads(
                (
                    reviewed_release
                    / "core/typed_relations/aggregate.json"
                ).read_text(encoding="utf-8")
            )
            client_rows = json.loads(
                (
                    client_release
                    / "core/typed_relations/aggregate.json"
                ).read_text(encoding="utf-8")
            )
            self.assertNotIn("F027", {row["id"] for row in reviewed_rows})
            self.assertIn("R10R029", {row["id"] for row in reviewed_rows})
            self.assertIn("F027", {row["id"] for row in client_rows})
            self.assertEqual(
                1,
                reviewed_manifest["core_surface_record_counts"][
                    "ARC002-AGGREGATE"
                ],
            )
            self.assertEqual(
                2,
                client_manifest["core_surface_record_counts"][
                    "ARC002-AGGREGATE"
                ],
            )

    def test_core_surface_cannot_use_an_unacknowledged_catalog_owner(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            registry = json.loads(
                (ROOT / compiler.CORE_SURFACE_PATH).read_text(encoding="utf-8")
            )
            row = next(
                item
                for item in registry["surfaces"]
                if item["surface_id"] == "MR001-ACTOR-ISSUE"
            )
            row["owner_pub_ids"] = ["PUB-MR-002"]
            bad_registry = Path(temp_dir) / "bad_core_surfaces.json"
            bad_registry.write_text(
                json.dumps(registry, ensure_ascii=False),
                encoding="utf-8",
            )
            with mock.patch.object(
                compiler,
                "CORE_SURFACE_PATH",
                bad_registry,
            ):
                with self.assertRaisesRegex(
                    PublicationError,
                    "not integrated or explicitly partial",
                ):
                    compile_publication_snapshot(
                        ROOT,
                        Path(temp_dir) / "releases",
                        profile="client_preview",
                    )

    def test_channel_verifier_checks_profile_release_and_manifest_hash(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT / "outputs") as temp_dir:
            output = Path(temp_dir) / "releases"
            channel = Path(temp_dir) / "client_preview.json"
            manifest = compile_publication_snapshot(
                ROOT,
                output,
                profile="client_preview",
                channel_file=channel,
            )
            report = verify_publication_channel(
                ROOT,
                channel,
                expected_profile="client_preview",
            )
            self.assertEqual("pass", report["status"])
            channel_payload = json.loads(channel.read_text(encoding="utf-8"))
            channel_payload["release_id"] = f"{manifest['release_id']}-tampered"
            channel.write_text(
                json.dumps(channel_payload),
                encoding="utf-8",
            )
            tampered = verify_publication_channel(
                ROOT,
                channel,
                expected_profile="client_preview",
            )
            self.assertEqual("fail", tampered["status"])
            self.assertTrue(
                any(
                    "release_id" in error
                    for error in tampered["errors"]
                )
            )

    def test_invalid_catalog_cannot_replace_last_good_snapshot(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "active"
            output.mkdir()
            marker = output / "last-good.txt"
            marker.write_text("keep", encoding="utf-8")
            bad_catalog = Path(temp_dir) / "bad_catalog.json"
            bad_catalog.write_text(
                json.dumps(
                    {
                        "schema_version": "test",
                        "entries": [{"id": "BROKEN"}],
                    }
                ),
                encoding="utf-8",
            )
            with mock.patch.object(compiler, "CATALOG_PATH", bad_catalog):
                with self.assertRaisesRegex(PublicationError, "is missing"):
                    compile_publication_snapshot(
                        ROOT, output, profile="client_preview"
                    )

            self.assertEqual("keep", marker.read_text(encoding="utf-8"))
            self.assertEqual({"last-good.txt"}, {path.name for path in output.iterdir()})

    def test_retired_asset_can_never_receive_a_release_profile(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            catalog = json.loads(
                (ROOT / compiler.CATALOG_PATH).read_text(encoding="utf-8")
            )
            retired = next(
                entry
                for entry in catalog["entries"]
                if entry["category"] == "retired_prohibited"
            )
            retired["release_profiles"] = ["client_preview"]
            bad_catalog = Path(temp_dir) / "retired_leak.json"
            bad_catalog.write_text(
                json.dumps(catalog, ensure_ascii=False),
                encoding="utf-8",
            )
            with mock.patch.object(compiler, "CATALOG_PATH", bad_catalog):
                with self.assertRaisesRegex(
                    PublicationError, "must have no release profile"
                ):
                    compile_publication_snapshot(
                        ROOT,
                        Path(temp_dir) / "releases",
                        profile="client_preview",
                    )

    def test_integrated_entry_requires_a_physical_publication_object(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            catalog = json.loads(
                (ROOT / compiler.CATALOG_PATH).read_text(encoding="utf-8")
            )
            integrated = next(
                entry
                for entry in catalog["entries"]
                if entry["id"] == "PUB-MR-004"
            )
            integrated.pop("publication_object_path")
            bad_catalog = Path(temp_dir) / "missing_object.json"
            bad_catalog.write_text(
                json.dumps(catalog, ensure_ascii=False),
                encoding="utf-8",
            )
            with mock.patch.object(compiler, "CATALOG_PATH", bad_catalog):
                with self.assertRaisesRegex(
                    PublicationError, "no publication object path"
                ):
                    compile_publication_snapshot(
                        ROOT,
                        Path(temp_dir) / "releases",
                        profile="client_preview",
                    )


if __name__ == "__main__":
    unittest.main()
