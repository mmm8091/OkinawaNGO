from __future__ import annotations

import csv
import json
import shutil
import tempfile
import unittest
from collections import Counter, defaultdict
from pathlib import Path

from research_publication.adapters.r5_repeat_participation import (
    R5PublicationAdapterError,
    build_r5_repeat_participation_exhibit,
)


ROOT = Path(__file__).resolve().parents[1]
R5_DIR = ROOT / "outputs" / "R05_coaction_v1"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def derive_strict_repeats(
    observations: list[dict[str, str]],
) -> dict[str, set[str]]:
    events: dict[str, set[str]] = defaultdict(set)
    for row in observations:
        if row["identity_status"] == "registry_actor":
            events[f"ACTOR:{row['actor_id']}"].add(row["event_id"])
        elif row["identity_status"] == "event_only_identity_human_checked":
            events[f"EVENT_ONLY:{row['identity_group_id']}"].add(row["event_id"])
    return {key: event_ids for key, event_ids in events.items() if len(event_ids) >= 2}


class R5RepeatParticipationPublicationAdapterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.exhibit = build_r5_repeat_participation_exhibit(ROOT)
        cls.formal_observations = read_rows(
            R5_DIR / "actor_event_bipartite_edges_v0.csv"
        )

    def test_recomputes_current_observation_and_repeat_totals_from_formal_rows(self) -> None:
        independently_derived_repeats = derive_strict_repeats(
            self.formal_observations
        )
        self.assertIn("不是组织联盟", self.exhibit["display"]["title"]["zh"])
        self.assertIn(
            "stable alliance",
            self.exhibit["display"]["interpretation_limit"]["en"],
        )
        self.assertEqual(169, len(self.formal_observations))
        self.assertEqual(
            len(self.formal_observations),
            self.exhibit["summary"]["observation_count"],
        )
        self.assertEqual(21, len(independently_derived_repeats))
        self.assertEqual(
            len(independently_derived_repeats),
            self.exhibit["summary"]["strict_repeat_identity_count"],
        )
        self.assertEqual(
            set(independently_derived_repeats),
            {
                row["strict_identity_key"]
                for row in self.exhibit["repeat_identities"]
            },
        )
        self.assertEqual(
            {
                "registry_actor": 15,
                "human_reviewed_event_only_identity": 6,
                "other_event_only_name": 0,
            },
            self.exhibit["summary"][
                "strict_repeat_count_by_participant_tier"
            ],
        )
        self.assertEqual(
            3,
            self.exhibit["summary"][
                "registry_all_sampled_events_repeat_identity_count"
            ],
        )

    def test_preserves_event_denominators_and_all_three_participant_tiers(self) -> None:
        by_event = {row["event_id"]: row for row in self.exhibit["events"]}
        self.assertEqual(
            {
                "EV2010_WWF_67": {
                    "registry_actor": 16,
                    "human_reviewed_event_only_identity": 11,
                    "other_event_only_name": 40,
                },
                "EV2015_NACSJ_31": {
                    "registry_actor": 31,
                    "human_reviewed_event_only_identity": 0,
                    "other_event_only_name": 0,
                },
                "EV2020_OEJP_MMC_71": {
                    "registry_actor": 17,
                    "human_reviewed_event_only_identity": 11,
                    "other_event_only_name": 43,
                },
            },
            {
                event_id: row["observation_count_by_participant_tier"]
                for event_id, row in by_event.items()
            },
        )
        for event in by_event.values():
            denominator = event["denominator"]
            self.assertEqual(
                denominator["structured_participant_count"],
                denominator["derived_observation_count"],
            )
            self.assertEqual("source_list_participant_row", denominator["unit"])
            self.assertTrue(event["source_refs"])

    def test_event_only_names_never_become_strict_identities_or_relations(self) -> None:
        event_only_names = [
            row
            for row in self.exhibit["observations"]
            if row["participant_tier"] == "other_event_only_name"
        ]
        self.assertEqual(83, len(event_only_names))
        self.assertTrue(
            all(row["strict_identity_key"] is None for row in event_only_names)
        )
        self.assertTrue(
            all(not row["is_strict_repeat"] for row in event_only_names)
        )
        self.assertTrue(all(row["actor_id"] is None for row in event_only_names))

        semantics = self.exhibit["relation_semantics"]
        self.assertFalse(semantics["creates_actor_relation_edges"])
        self.assertFalse(semantics["creates_alliance_edges"])
        self.assertEqual(
            "participant_to_event_observation_only",
            semantics["allowed_edge_type"],
        )
        self.assertNotIn("actor_relations", self.exhibit)
        self.assertIn("stable alliance", semantics["prohibited_claims"])

    def test_reviewed_event_only_repeats_remain_outside_registry(self) -> None:
        reviewed_event_only = [
            row
            for row in self.exhibit["repeat_identities"]
            if row["participant_tier"] == "human_reviewed_event_only_identity"
        ]
        self.assertEqual(6, len(reviewed_event_only))
        self.assertTrue(all(row["actor_id"] is None for row in reviewed_event_only))
        self.assertTrue(
            all(row["identity_group_id"] for row in reviewed_event_only)
        )
        self.assertTrue(
            all(
                row["strict_identity_key"].startswith("EVENT_ONLY:")
                for row in reviewed_event_only
            )
        )

    def test_pairwise_overlap_has_explicit_denominators_and_is_recomputed(self) -> None:
        by_pair = {
            (row["event_a"], row["event_b"]): row
            for row in self.exhibit["pairwise_overlaps"]
        }
        self.assertEqual(
            {
                ("EV2010_WWF_67", "EV2015_NACSJ_31"): (10, 10),
                ("EV2010_WWF_67", "EV2020_OEJP_MMC_71"): (8, 14),
                ("EV2015_NACSJ_31", "EV2020_OEJP_MMC_71"): (3, 3),
            },
            {
                pair: (
                    row["shared_registry_actor_count"],
                    row["shared_strict_identity_count"],
                )
                for pair, row in by_pair.items()
            },
        )
        self.assertTrue(
            all(row["registry_denominator_a"] > 0 for row in by_pair.values())
        )
        self.assertTrue(
            all(
                "not an alliance measure" in row["interpretation_limit"]
                for row in by_pair.values()
            )
        )

    def test_every_row_and_repeat_can_descend_to_public_source_metadata(self) -> None:
        source_ids = {row["source_ref"] for row in self.exhibit["sources"]}
        self.assertTrue({"S003", "S004", "S005", "S006"} <= source_ids)
        for collection in (
            self.exhibit["events"],
            self.exhibit["observations"],
            self.exhibit["repeat_identities"],
        ):
            for row in collection:
                self.assertTrue(set(row["source_refs"]) <= source_ids)
        self.assertTrue(
            all("url" in row and "source_locator" in row for row in self.exhibit["sources"])
        )
        self.assertTrue(
            all("sha256" not in row and "local_path" not in row for row in self.exhibit["sources"])
        )

    def test_adapter_is_deterministic_for_the_same_formal_package(self) -> None:
        first = json.dumps(self.exhibit, ensure_ascii=False, sort_keys=True)
        second = json.dumps(
            build_r5_repeat_participation_exhibit(ROOT),
            ensure_ascii=False,
            sort_keys=True,
        )
        self.assertEqual(first, second)

    def test_rejects_stale_catalog_counts_instead_of_publishing_mixed_data(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project_root = Path(temporary)
            destination = project_root / "outputs" / "R05_coaction_v1"
            shutil.copytree(R5_DIR, destination)
            event_path = destination / "event_catalog_v0.csv"
            events = read_rows(event_path)
            events[0]["structured_participant_count"] = str(
                int(events[0]["structured_participant_count"]) - 1
            )
            write_rows(event_path, events)
            with self.assertRaisesRegex(
                R5PublicationAdapterError,
                "structured_participant_count disagrees",
            ):
                build_r5_repeat_participation_exhibit(project_root)

    def test_rejects_a_stale_formal_bridge_instead_of_rederiving_silently(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project_root = Path(temporary)
            destination = project_root / "outputs" / "R05_coaction_v1"
            shutil.copytree(R5_DIR, destination)
            bridge_path = destination / "repeat_participation_bridges_v0.csv"
            bridges = read_rows(bridge_path)
            write_rows(bridge_path, bridges[:-1])
            with self.assertRaisesRegex(
                R5PublicationAdapterError,
                "Formal repeat bridges disagree",
            ):
                build_r5_repeat_participation_exhibit(project_root)


if __name__ == "__main__":
    unittest.main()
