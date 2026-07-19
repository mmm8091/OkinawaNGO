from __future__ import annotations

import csv
import hashlib
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.merge_hr032_partner_crosswalk_v1 import apply_hr032_partner_crosswalk


ROOT = Path(__file__).resolve().parents[1]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class MergeHr032PartnerCrosswalkV1Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        for relative in (
            "outputs/R10_official_collaboration_universe_v1/"
            "official_collaboration_source_universe_v1.csv",
            "outputs/R10_official_collaboration_universe_v1/"
            "HR032_partner_alias_crosswalk_review_v1.csv",
        ):
            destination = self.root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / relative, destination)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_builds_bounded_crosswalk_without_changing_source_universe(self) -> None:
        universe = (
            self.root
            / "outputs/R10_official_collaboration_universe_v1/"
            "official_collaboration_source_universe_v1.csv"
        )
        original_hash = sha256(universe)

        summary = apply_hr032_partner_crosswalk(self.root)

        self.assertEqual(original_hash, sha256(universe))
        self.assertEqual(48, summary["identity_crosswalk_rows"])
        self.assertEqual(5, summary["member_crosswalk_rows"])
        self.assertEqual(3, summary["registry_crosswalk_rows"])

        output = universe.parent
        identity_rows = read_rows(
            output / "partner_identity_crosswalk_human_v1.csv"
        )
        member_rows = read_rows(
            output / "member_of_composite_crosswalk_human_v1.csv"
        )
        self.assertEqual(48, len(identity_rows))
        self.assertEqual(
            48, len({row["source_row_uid"] for row in identity_rows})
        )
        self.assertEqual(
            {"S002-R0010", "S002-R0011", "S002-R0501"},
            {
                row["source_row_uid"]
                for row in identity_rows
                if row["registry_actor_id"] == "A088"
            },
        )
        self.assertTrue(
            all(row["actor_relation_edge_approved"] == "no" for row in identity_rows)
        )
        self.assertTrue(
            all(row["amount_allocation_approved"] == "no" for row in identity_rows)
        )

        by_uid = {row["source_row_uid"]: row for row in identity_rows}
        self.assertEqual(
            "source_partner_kind_conflict",
            by_uid["S002-R0496"]["partner_kind_review"],
        )
        self.assertEqual(
            "source_kind_conflict_probable_miscoding",
            by_uid["S002-R0545"]["partner_kind_review"],
        )
        self.assertEqual(
            "unexplained_other_or_advisory_candidate",
            by_uid["S002-R0466"]["role_review"],
        )
        self.assertEqual(5, len(member_rows))
        self.assertTrue(
            all(
                row["member_identity_crosswalk_approved"] == "yes"
                for row in member_rows
            )
        )
        self.assertTrue(
            all(row["actor_relation_edge_approved"] == "no" for row in member_rows)
        )
        self.assertTrue(
            all(row["amount_allocation_approved"] == "no" for row in member_rows)
        )

    def test_is_idempotent(self) -> None:
        apply_hr032_partner_crosswalk(self.root)
        output = (
            self.root
            / "outputs/R10_official_collaboration_universe_v1/"
            "partner_identity_crosswalk_human_v1.csv"
        )
        member_output = output.parent / "member_of_composite_crosswalk_human_v1.csv"
        first_identity = output.read_bytes()
        first_member = member_output.read_bytes()

        apply_hr032_partner_crosswalk(self.root)

        self.assertEqual(first_identity, output.read_bytes())
        self.assertEqual(first_member, member_output.read_bytes())


if __name__ == "__main__":
    unittest.main()
