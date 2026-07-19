from __future__ import annotations

import csv
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.merge_identity_spatial_repairs_v1 import apply_identity_spatial_repairs


ROOT = Path(__file__).resolve().parents[1]


def read_rows(path: Path, key: str) -> dict[str, dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return {row[key]: row for row in csv.DictReader(handle)}


class MergeIdentitySpatialRepairsV1Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        for relative in (
            "data/interim/01_actor_registry_initial_v0.csv",
            "data/interim/02_actor_aliases_initial_v0.csv",
            "data/interim/04_place_registry_v0.csv",
            "data/interim/07_actor_issue_edges_initial_v0.csv",
            "data/interim/08_actor_place_edges_initial_v0.csv",
            "data/interim/09_actor_event_venue_edges_v0.csv",
            "data/interim/human_review_log_v0.csv",
        ):
            destination = self.root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / relative, destination)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_applies_principal_identity_and_scope_decisions(self) -> None:
        summary = apply_identity_spatial_repairs(self.root)

        actors = read_rows(
            self.root / "data/interim/01_actor_registry_initial_v0.csv",
            "actor_id",
        )
        self.assertEqual(summary["registry_rows"], 122)
        self.assertEqual(summary["active_actor_rows"], 121)
        self.assertEqual(actors["A026"]["actor_class"], "citizen_group")
        self.assertEqual(actors["A057"]["origin_type"], "japan_domestic")
        self.assertEqual(
            actors["A058"]["canonical_name"],
            "安保廃棄・くらしと民主主義を守る沖縄県統一行動連絡会議",
        )
        self.assertEqual(
            actors["A059"]["canonical_name"],
            "沖縄「建白書」を実現し未来を拓く島ぐるみ会議",
        )
        self.assertEqual(
            actors["A067"]["canonical_name"],
            "辺野古土砂搬出反対全国連絡協議会",
        )
        self.assertEqual(
            actors["A068"]["canonical_name"],
            "ヘリポート基地建設の是非を問う名護市民投票推進協議会",
        )
        self.assertEqual(
            actors["A070"]["canonical_name"],
            "Veterans For Peace Ryukyu/Okinawa Chapter Kokusai (VFP-ROCK)",
        )
        self.assertEqual(
            actors["A071"]["canonical_name"],
            "沖縄から基地をなくし世界の平和を求める市民連絡会",
        )
        self.assertEqual(actors["A072"]["scope_status"], "merged_duplicate")
        self.assertEqual(actors["A072"]["merged_duplicate_of"], "A071")
        self.assertEqual(actors["A072"]["review_status"], "rejected")

        for actor_id in ("A089", "A090", "A091", "A092", "A093", "A114"):
            self.assertEqual(actors[actor_id]["actor_class"], "labor_union")
        for actor_id in ("A105", "A107", "A111", "A115"):
            self.assertEqual(actors[actor_id]["actor_class"], "womens_organization")

        self.assertEqual(actors["X014"]["review_status"], "human_checked")
        self.assertEqual(actors["X014"]["scope_status"], "watchlist_only")
        self.assertEqual(actors["X015"]["review_status"], "human_checked")
        self.assertEqual(actors["X015"]["scope_status"], "in_scope_limited")

    def test_repairs_places_and_preserves_retired_provenance(self) -> None:
        apply_identity_spatial_repairs(self.root)

        places = read_rows(
            self.root / "data/interim/04_place_registry_v0.csv",
            "place_id",
        )
        self.assertEqual(places["P021"]["place_name"], "Sakishima Islands")
        self.assertIn("不得自动", places["P021"]["notes"])

        edges = read_rows(
            self.root / "data/interim/08_actor_place_edges_initial_v0.csv",
            "edge_id",
        )
        self.assertEqual(edges["AP123"]["place_id"], "P007")
        self.assertEqual(edges["AP123"]["place_name"], "Camp Foster")
        self.assertEqual(edges["AP123"]["place_semantic"], "site_presence")
        self.assertEqual(edges["AP123"]["review_status"], "human_revised")

        self.assertEqual(edges["AP048"]["review_status"], "rejected")
        self.assertEqual(edges["AP048"]["scope_status"], "retired_candidate")
        self.assertEqual(edges["AP049"]["place_id"], "P021")
        self.assertEqual(edges["AP049"]["place_semantic"], "site_presence")
        self.assertEqual(edges["AP049"]["review_status"], "needs_second_source")
        self.assertEqual(edges["AP118"]["review_status"], "rejected")
        self.assertEqual(edges["AP118"]["superseded_by_edge_id"], "AP117")
        self.assertEqual(edges["AP118"]["original_actor_id"], "A072")

        issue_edges = read_rows(
            self.root / "data/interim/07_actor_issue_edges_initial_v0.csv",
            "edge_id",
        )
        self.assertEqual(issue_edges["AI174"]["actor_id"], "A071")
        self.assertEqual(issue_edges["AI174"]["original_actor_id"], "A072")
        self.assertEqual(issue_edges["AI174"]["review_status"], "rejected")
        self.assertEqual(issue_edges["AI174"]["superseded_by_edge_id"], "AI173")
        self.assertEqual(issue_edges["AI175"]["superseded_by_edge_id"], "AI172")

    def test_does_not_decide_lifecycle_candidates_and_is_idempotent(self) -> None:
        first = apply_identity_spatial_repairs(self.root)
        first_registry = (
            self.root / "data/interim/01_actor_registry_initial_v0.csv"
        ).read_bytes()
        first_places = (
            self.root / "data/interim/04_place_registry_v0.csv"
        ).read_bytes()

        second = apply_identity_spatial_repairs(self.root)
        self.assertEqual(first, second)
        self.assertEqual(
            first_registry,
            (self.root / "data/interim/01_actor_registry_initial_v0.csv").read_bytes(),
        )
        self.assertEqual(
            first_places,
            (self.root / "data/interim/04_place_registry_v0.csv").read_bytes(),
        )

        actors = read_rows(
            self.root / "data/interim/01_actor_registry_initial_v0.csv",
            "actor_id",
        )
        self.assertNotIn(
            actors["A068"].get("lifecycle_status", ""),
            {"dissolved", "reorganized"},
        )


if __name__ == "__main__":
    unittest.main()
