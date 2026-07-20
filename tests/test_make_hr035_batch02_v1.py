from __future__ import annotations

import csv
import hashlib
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import scripts.make_hr035_batch02_v1 as builder


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "actor_issue_claim_freeze_v1"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class MakeHr035Batch02V1Tests(unittest.TestCase):
    def test_assignment_has_exact_edge_and_identity_decisions(self) -> None:
        edges = read_rows(OUTPUT / "HR035_actor_issue_fact_review_batch02_v1.csv")
        identities = read_rows(
            OUTPUT / "HR035_actor_identity_companion_batch02_v1.csv"
        )

        self.assertEqual(builder.BATCH_02_EDGE_IDS, [row["edge_id"] for row in edges])
        self.assertEqual(
            builder.IDENTITY_COMPANION_ACTOR_IDS,
            [row["actor_id"] for row in identities],
        )
        self.assertEqual(18, len(edges))
        self.assertEqual(5, len(identities))
        self.assertEqual(
            9,
            sum(row["actor_identity_gate"] == "companion_review_required" for row in edges),
        )
        self.assertEqual(
            9,
            sum(row["actor_identity_gate"] == "already_human_reviewed" for row in edges),
        )

    def test_source_ceiling_and_continuity_warnings_are_explicit(self) -> None:
        rows = {
            row["edge_id"]: row
            for row in read_rows(
                OUTPUT / "HR035_actor_issue_fact_review_batch02_v1.csv"
            )
        }

        self.assertEqual(
            {"AI044", "AI119", "AI121", "AI232", "AI234"},
            {edge_id for edge_id, row in rows.items() if row["source_gap_flag"]},
        )
        self.assertIn("单次声明不足", rows["AI016"]["attention_flag"])
        self.assertIn("来源错位", rows["AI044"]["attention_flag"])
        for edge_id in ("AI119", "AI121", "AI232", "AI234"):
            self.assertEqual("E3", rows[edge_id]["source_level_ceiling_current"])
            self.assertIn("不得仅因 edge 当前标 E4", rows[edge_id]["attention_flag"])

    def test_decisions_are_blank_and_sources_are_reviewable(self) -> None:
        edges = read_rows(OUTPUT / "HR035_actor_issue_fact_review_batch02_v1.csv")
        identities = read_rows(
            OUTPUT / "HR035_actor_identity_companion_batch02_v1.csv"
        )
        sources = read_rows(OUTPUT / "HR035_source_bundle_batch02_v1.csv")

        self.assertTrue(
            all(not row[field] for row in edges for field in builder.EDGE_DECISION_FIELDS)
        )
        self.assertTrue(
            all(
                not row[field]
                for row in identities
                for field in builder.IDENTITY_DECISION_FIELDS
            )
        )
        self.assertEqual(20, len({row["source_id"] for row in sources}))
        self.assertEqual(
            19,
            len(
                {
                    row["source_id"]
                    for row in sources
                    if row["item_type"] == "edge_fact"
                }
            ),
        )
        self.assertNotIn("S051", {row["source_id"] for row in sources})
        self.assertTrue(
            all(
                row["archive_status"] in {"archived", "manual_archived"}
                for row in sources
            )
        )

    def test_generation_is_byte_deterministic(self) -> None:
        filenames = (
            "HR035_actor_issue_fact_review_batch02_v1.csv",
            "HR035_actor_identity_companion_batch02_v1.csv",
            "HR035_source_bundle_batch02_v1.csv",
            "validation_report_batch02_v1.md",
        )
        with tempfile.TemporaryDirectory() as first_dir, tempfile.TemporaryDirectory() as second_dir:
            first = Path(first_dir)
            second = Path(second_dir)
            with mock.patch.object(builder, "OUTPUT_DIR", first):
                builder.main()
            with mock.patch.object(builder, "OUTPUT_DIR", second):
                builder.main()

            self.assertEqual(
                {name: sha256(first / name) for name in filenames},
                {name: sha256(second / name) for name in filenames},
            )


if __name__ == "__main__":
    unittest.main()
