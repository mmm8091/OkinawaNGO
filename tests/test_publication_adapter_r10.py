from __future__ import annotations

import csv
import shutil
import tempfile
import unittest
from pathlib import Path
from typing import Any

from research_publication.adapters.r10_official_universe import (
    R10OfficialUniverseError,
    build_r10_official_universe_exhibit,
)


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path("outputs/R10_official_collaboration_universe_v1")


def _all_keys(value: Any) -> set[str]:
    if isinstance(value, list):
        result: set[str] = set()
        for item in value:
            result.update(_all_keys(item))
        return result
    if isinstance(value, dict):
        result = set(value)
        for item in value.values():
            result.update(_all_keys(item))
        return result
    return set()


class PublicationAdapterR10Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.exhibit = build_r10_official_universe_exhibit(ROOT)

    def test_exact_denominator_and_complete_official_dimensions(self) -> None:
        exhibit = self.exhibit
        self.assertEqual("PUB-MR-012", exhibit["id"])
        self.assertIn("不等于付款", exhibit["display"]["interpretation_limit"]["zh"])
        self.assertEqual(616, exhibit["denominator"]["value"])
        self.assertEqual("official_source_rows", exhibit["denominator"]["unit"])
        self.assertEqual("S002", exhibit["denominator"]["source_id"])
        self.assertEqual(86, exhibit["denominator"]["pdf_pages"])

        summaries = exhibit["summaries"]
        self.assertEqual(15, len(summaries["departments"]))
        self.assertEqual(19, len(summaries["functions"]))
        self.assertEqual(10, len(summaries["resource_types"]))
        for dimension in ("departments", "functions", "resource_types"):
            self.assertEqual(
                616,
                sum(row["source_row_count"] for row in summaries[dimension]),
            )

        dimensions = exhibit["drilldown"]["dimensions"]
        self.assertEqual(150, dimensions["department_matrix_cells_total"])
        self.assertEqual(72, dimensions["department_matrix_cells_nonzero"])
        self.assertEqual(190, dimensions["function_matrix_cells_total"])
        self.assertEqual(90, dimensions["function_matrix_cells_nonzero"])
        self.assertEqual(
            616,
            sum(
                row["source_row_count"]
                for row in exhibit["drilldown"][
                    "department_by_resource_type_nonzero_cells"
                ]
            ),
        )
        self.assertEqual(
            616,
            sum(
                row["source_row_count"]
                for row in exhibit["drilldown"][
                    "function_by_resource_type_nonzero_cells"
                ]
            ),
        )

    def test_official_counts_and_bounded_headlines_are_preserved(self) -> None:
        departments = self.exhibit["summaries"]["departments"]
        resources = {
            row["code"]: row for row in self.exhibit["summaries"]["resource_types"]
        }
        metrics = {
            row["id"]: row["value"] for row in self.exhibit["headline_metrics"]
        }

        self.assertEqual("保健医療介護部", departments[0]["label"])
        self.assertEqual(121, departments[0]["source_row_count"])
        self.assertEqual(303, resources["1"]["source_row_count"])
        self.assertEqual("委託", resources["1"]["label"])
        self.assertEqual(93, resources["4"]["source_row_count"])
        self.assertFalse(resources["4"]["cash_transfer_inference_allowed"])
        self.assertEqual(
            {
                "M18": 443,
                "M19": 71.9,
                "M11": 469,
                "M12": 76.1,
                "M13": 19,
                "M14": 3.1,
            },
            metrics,
        )

    def test_payload_does_not_actorize_labels_or_publish_amount_rows(self) -> None:
        keys = _all_keys(self.exhibit)
        forbidden = {
            "partner_name_source_text",
            "partner_name_display_alias_machine",
            "partner_display_label_id",
            "project_cost_thousand_jpy_source_text",
            "project_cost_thousand_jpy_numeric",
            "r10_purposive_relation_id",
            "r10_purposive_amount_id",
        }
        self.assertTrue(forbidden.isdisjoint(keys))
        self.assertIn(
            "partner_names_and_machine_display_aliases",
            self.exhibit["selection_boundary"]["excluded_from_public_exhibit"],
        )
        limits = " ".join(self.exhibit["interpretation_limits"]).lower()
        self.assertIn("not actor identities", limits)
        self.assertIn("not an amount paid", limits)
        self.assertIn("not stable", limits)

    def test_cell_trace_is_complete_but_contains_only_compact_references(self) -> None:
        cells = self.exhibit["drilldown"][
            "function_by_resource_type_nonzero_cells"
        ]
        self.assertTrue(cells)
        for cell in cells:
            refs = cell["source_row_refs"]
            self.assertEqual(cell["source_row_count"], refs["count"])
            self.assertRegex(refs["row_numbers_compact"], r"^\d+(?:[-;]\d+)*$")
            self.assertRegex(refs["pdf_pages_compact"], r"^\d+(?:[-;]\d+)*$")
            self.assertNotIn("rows", refs)

    def test_incomplete_source_universe_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project = Path(temp_dir)
            target = project / PACKAGE
            shutil.copytree(ROOT / PACKAGE, target)
            universe_path = target / "official_collaboration_source_universe_v1.csv"
            with universe_path.open("r", encoding="utf-8-sig", newline="") as handle:
                rows = list(csv.DictReader(handle))
                fieldnames = list(rows[0])
            with universe_path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows[:-1])

            with self.assertRaisesRegex(
                R10OfficialUniverseError, "exactly 616 rows"
            ):
                build_r10_official_universe_exhibit(project)


if __name__ == "__main__":
    unittest.main()
