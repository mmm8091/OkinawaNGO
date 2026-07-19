from __future__ import annotations

import csv
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.merge_source_metadata_reviews_v1 import apply_source_metadata_reviews


ROOT = Path(__file__).resolve().parents[1]


def read_rows(path: Path, key: str) -> dict[str, dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return {row[key]: row for row in csv.DictReader(handle)}


class MergeSourceMetadataReviewsV1Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        for relative in (
            "data/interim/05_source_log_initial_v0.csv",
            "outputs/principal_review_merge_v1/source_metadata_overlay_v1.csv",
        ):
            destination = self.root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / relative, destination)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_applies_71_metadata_decisions_without_approving_claims(self) -> None:
        summary = apply_source_metadata_reviews(self.root)
        rows = read_rows(
            self.root / "data/interim/05_source_log_initial_v0.csv",
            "source_id",
        )

        self.assertEqual(295, summary["source_rows"])
        self.assertEqual(71, summary["reviewed_sources"])
        self.assertEqual(69, summary["human_revised"])
        self.assertEqual(2, summary["preserved_human_checked"])
        self.assertEqual("human_checked", rows["S158"]["review_status"])
        self.assertEqual("human_checked", rows["S204"]["review_status"])
        self.assertEqual("human_revised", rows["S071"]["review_status"])
        reviewed_ids = {
            row["source_id"]
            for row in read_rows(
                self.root
                / "outputs/principal_review_merge_v1/source_metadata_overlay_v1.csv",
                "review_item_id",
            ).values()
        }
        self.assertNotIn(
            "human_verified",
            {rows[source_id]["review_status"] for source_id in reviewed_ids},
        )

        self.assertEqual(
            "https://www.courts.go.jp/assets/hanrei/hanrei-pdf-89731.pdf",
            rows["S137"]["url"],
        )
        self.assertEqual(
            "https://www2.pref.okinawa.jp/oki/Gikairep1.nsf/GoZentai/20180702000000",
            rows["S197"]["url"],
        )
        self.assertEqual(
            "https://www2.pref.okinawa.jp/oki/Gikairep1.nsf/"
            "bf76642d1ed57158492581ed00348311/"
            "6cc4b1801bbb16124925861e00087c7a?OpenDocument",
            rows["S198"]["url"],
        )
        self.assertEqual("academic_presentation", rows["S294"]["source_type"])
        self.assertEqual("2019", rows["S294"]["year"])
        self.assertEqual("no", rows["S294"]["relation_or_claim_approved"])
        self.assertIn("官方roster", rows["S294"]["what_it_supports"])

    def test_is_idempotent(self) -> None:
        first = apply_source_metadata_reviews(self.root)
        path = self.root / "data/interim/05_source_log_initial_v0.csv"
        first_bytes = path.read_bytes()
        second = apply_source_metadata_reviews(self.root)
        self.assertEqual(first, second)
        self.assertEqual(first_bytes, path.read_bytes())


if __name__ == "__main__":
    unittest.main()
