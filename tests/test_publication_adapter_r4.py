from __future__ import annotations

import csv
import shutil
import tempfile
import unittest
from collections import Counter
from pathlib import Path

from research_publication.adapters.r4_sakishima import (
    FORMAL_FACT_PATH,
    SAFE_EXCERPT_PATH,
    R4SakishimaAdapterError,
    build_r4_sakishima_exhibit,
)


ROOT = Path(__file__).resolve().parents[1]


def _copy_inputs(destination_root: Path) -> None:
    for relative in (FORMAL_FACT_PATH, SAFE_EXCERPT_PATH):
        destination = destination_root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / relative, destination)


def _rewrite_csv(
    path: Path,
    transform,
) -> None:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = list(reader.fieldnames or [])
        rows = list(reader)
    rows = transform(rows)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


class PublicationAdapterR4Tests(unittest.TestCase):
    def test_builds_current_bounded_exhibit_from_formal_tables(self) -> None:
        exhibit = build_r4_sakishima_exhibit(ROOT)

        self.assertEqual("PUB-MR-004", exhibit["catalog_id"])
        self.assertIn("限定线上语料", exhibit["display"]["interpretation_limit"]["zh"])
        self.assertIn("18条", exhibit["display"]["interpretation_limit"]["zh"])
        self.assertIn("先島", exhibit["display"]["title"]["ja"])
        self.assertEqual(
            {
                "formal_frame_observations": 19,
                "safe_source_excerpts": 24,
                "bounded_subject_display_units": 14,
                "unique_entity_identifiers": 13,
                "registry_actor_observations": 2,
                "non_registry_or_institution_observations": 17,
                "reviewed_formal_frame_observations": 9,
                "reviewed_safe_source_excerpts": 5,
                "research_layer_formal_frame_observations": 10,
                "research_layer_safe_source_excerpts": 19,
            },
            exhibit["declared_denominators"],
        )
        self.assertEqual(
            {"reviewed": 9, "research": 10},
            dict(
                Counter(
                    row["display_tier"] for row in exhibit["observations"]
                )
            ),
        )
        self.assertEqual(19, len(exhibit["observations"]))
        self.assertEqual(24, len(exhibit["excerpts"]))
        self.assertEqual(4, len(exhibit["place_vocabulary"]))
        self.assertEqual(7, len(exhibit["frame_vocabulary"]))
        frame_labels = {
            row["id"]: row for row in exhibit["frame_vocabulary"]
        }
        self.assertEqual(
            "前线化／台湾邻近／撤离",
            frame_labels["frontline_taiwan_evacuation"]["display_label_zh"],
        )
        self.assertIn("not local prevalence", exhibit["place_aggregates"][0]["measurement_scope"])
        self.assertIn("not organization counts", exhibit["interpretation_limit"])

        places = {row["place"]: row for row in exhibit["place_aggregates"]}
        self.assertEqual(
            (6, 9),
            (
                places["Miyako"]["formal_observation_denominator"],
                places["Miyako"]["safe_excerpt_denominator"],
            ),
        )
        self.assertEqual(
            (6, 6),
            (
                places["Ishigaki"]["formal_observation_denominator"],
                places["Ishigaki"]["safe_excerpt_denominator"],
            ),
        )
        self.assertEqual(
            (6, 8),
            (
                places["Yonaguni"]["formal_observation_denominator"],
                places["Yonaguni"]["safe_excerpt_denominator"],
            ),
        )
        self.assertEqual(
            (1, 1, "regional_context"),
            (
                places["Sakishima"]["formal_observation_denominator"],
                places["Sakishima"]["safe_excerpt_denominator"],
                places["Sakishima"]["place_scope"],
            ),
        )

    def test_preserves_actor_person_institution_and_event_boundaries(self) -> None:
        exhibit = build_r4_sakishima_exhibit(ROOT)
        observations = {
            row["observation_id"]: row for row in exhibit["observations"]
        }

        registry_subjects = {
            row["subject"]["actor_id"]
            for row in exhibit["observations"]
            if row["subject"]["actor_id"]
        }
        self.assertEqual({"A014", "A016"}, registry_subjects)
        self.assertEqual(
            "named_person",
            observations["R4E008"]["subject"]["entity_kind"],
        )
        self.assertIsNone(
            observations["R4E008"]["subject"]["actor_id"]
        )
        self.assertEqual(
            "institution",
            observations["R4E009B"]["subject"]["entity_kind"],
        )
        self.assertEqual(
            "anonymous_event_utterance",
            observations["R4E016"]["subject"]["entity_kind"],
        )
        self.assertEqual(
            "provisional_event_collective",
            observations["R4E001"]["subject"]["entity_kind"],
        )

    def test_every_observation_resolves_to_safe_sources_and_locators(self) -> None:
        exhibit = build_r4_sakishima_exhibit(ROOT)
        observations = {
            row["observation_id"]: row for row in exhibit["observations"]
        }
        excerpt_ids = {
            row["corpus_source_id"] for row in exhibit["excerpts"]
        }
        for observation in exhibit["observations"]:
            evidence = observation["evidence"]
            self.assertTrue(evidence["source_locator_summary"])
            self.assertTrue(evidence["source_ref_ids"])
            self.assertTrue(set(evidence["source_ref_ids"]) <= excerpt_ids)
            self.assertEqual(
                evidence["source_ref_ids"],
                [
                    source["corpus_source_id"]
                    for source in evidence["source_records"]
                ],
            )
            self.assertTrue(
                all(source["locator"] for source in evidence["source_records"])
            )

        r4e007_sources = {
            row["corpus_source_id"]: row
            for row in observations["R4E007"]["evidence"]["source_records"]
        }
        self.assertIn("pp.27–29", r4e007_sources["R4S007"]["locator"])
        self.assertEqual("Sakishima", observations["R4E025"]["place"])
        self.assertEqual(
            ["frontline_taiwan_evacuation"],
            observations["R4E024"]["evidence"]["source_records"][0][
                "frame_labels"
            ],
        )

    def test_is_deterministic_and_does_not_depend_on_module_prose(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            fixture_root = Path(temp_dir)
            _copy_inputs(fixture_root)
            first = build_r4_sakishima_exhibit(fixture_root)
            second = build_r4_sakishima_exhibit(fixture_root)

        self.assertEqual(first, second)
        self.assertFalse(
            (fixture_root / "outputs/R04_sakishima_frame_corpus_v0/README.md").exists()
        )

    def test_rejects_denominator_drift(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            fixture_root = Path(temp_dir)
            _copy_inputs(fixture_root)
            _rewrite_csv(
                fixture_root / FORMAL_FACT_PATH,
                lambda rows: rows[:-1],
            )
            with self.assertRaisesRegex(
                R4SakishimaAdapterError,
                "formal observation denominator changed",
            ):
                build_r4_sakishima_exhibit(fixture_root)

    def test_rejects_actorization_of_a_named_person(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            fixture_root = Path(temp_dir)
            _copy_inputs(fixture_root)

            def actorize_person(rows):
                for row in rows:
                    if row["fact_id"] == "R4E008":
                        row["entity_status"] = "existing_actor"
                return rows

            _rewrite_csv(fixture_root / FORMAL_FACT_PATH, actorize_person)
            with self.assertRaisesRegex(
                R4SakishimaAdapterError,
                "marks a non-registry id as existing_actor",
            ):
                build_r4_sakishima_exhibit(fixture_root)


if __name__ == "__main__":
    unittest.main()
