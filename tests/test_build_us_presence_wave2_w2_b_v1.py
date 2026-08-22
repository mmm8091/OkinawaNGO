from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_us_presence_wave2_w2_b_v1.py"
SPEC = importlib.util.spec_from_file_location("build_w2_b", SCRIPT)
assert SPEC and SPEC.loader
BUILD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILD)
OUT = BUILD.OUT


def read_csv(name: str) -> list[dict[str, str]]:
    with (OUT / name).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


class W2BPackageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        result = BUILD.main()
        if result != 0:
            raise AssertionError("W2-B builder did not pass its own validation")

    def test_expected_row_counts(self) -> None:
        expected = {
            "hierarchy_and_site_year_v1.csv": 16,
            "service_capacity_observations_v1.csv": 15,
            "sponsor_and_local_flow_observations_v1.csv": 17,
            "federal_award_allocation_audit_v1.csv": 19,
            "service_function_boundary_v1.csv": 10,
            "allocation_waterfall_v1.csv": 9,
            "source_receipts_v1.csv": 34,
            "negative_search_log_v1.csv": 10,
            "change_notes_v1.csv": 6,
            "principal_review_queue_v1.csv": 7,
            "w2_d_endpoint_candidates_v1.csv": 28,
        }
        self.assertEqual({name: len(read_csv(name)) for name in expected}, expected)

    def test_all_rows_are_research_only_ai_seeded(self) -> None:
        for path in OUT.glob("*.csv"):
            for row in read_csv(path.name):
                self.assertEqual(row["review_status"], "ai_seeded", path.name)
                self.assertEqual(row["package_scope"], "research_only", path.name)
                self.assertEqual(row["frontend_status"], "not_frontend_ready", path.name)
                self.assertEqual(row["central_writeback"], "no", path.name)

    def test_current_site_types_resolve_six_vs_eight(self) -> None:
        rows = read_csv("hierarchy_and_site_year_v1.csv")
        self.assertEqual(sum(row["site_type"] == "operating_center" for row in rows), 6)
        current_ids = {f"W2B2-HS{number:03d}" for number in range(5, 13)}
        current = [row for row in rows if row["row_id"] in current_ids]
        self.assertEqual(len(current), 8)
        self.assertEqual({row["site_type"] for row in current}, {"operating_center", "transport_terminal_presence", "administrative_area_office"})

    def test_historical_locations_and_outreach_remain_separate(self) -> None:
        rows = {row["row_id"]: row for row in read_csv("hierarchy_and_site_year_v1.csv")}
        self.assertEqual(rows["W2B2-HS013"]["quantity"], "7")
        self.assertEqual(rows["W2B2-HS014"]["quantity"], "10")
        self.assertNotEqual(rows["W2B2-HS013"]["site_type"], rows["W2B2-HS014"]["site_type"])

    def test_award_and_account_figures_remain_typed(self) -> None:
        rows = {row["audit_id"]: row for row in read_csv("federal_award_allocation_audit_v1.csv")}
        self.assertEqual(rows["W2B2-FA001"]["value"], "72000000")
        self.assertEqual(rows["W2B2-FA009"]["value"], "41212463.29")
        self.assertEqual(rows["W2B2-FA001"]["status"], "official_award_level")
        self.assertEqual(rows["W2B2-FA009"]["status"], "official_account_linked_rollup_semantic_conflict")
        self.assertEqual(rows["W2B2-FA001"]["semantic_conflict_id"], rows["W2B2-FA009"]["semantic_conflict_id"])

    def test_no_synthetic_region_or_okinawa_amount(self) -> None:
        rows = {row["stage_id"]: row for row in read_csv("allocation_waterfall_v1.csv")}
        for row_id in ("W2B2-WF003", "W2B2-WF004", "W2B2-WF005"):
            self.assertEqual(rows[row_id]["known_amount"], "")
            self.assertEqual(rows[row_id]["visibility_status"], "allocation_gap")

    def test_named_local_flows_are_not_a_budget(self) -> None:
        rows = read_csv("sponsor_and_local_flow_observations_v1.csv")
        aec = [row for row in rows if row["source_name"] == "American Engineering Corporation" and row["amount"] == "18000"]
        self.assertEqual({row["date_start"] for row in aec}, {"2018-03-01", "2024-10-16"})
        self.assertFalse(any(row["source_name"] in {"United Service Organizations, Inc.", "Department of Defense"} for row in rows))

    def test_red_cross_nmcrs_relation_is_service_intermediation(self) -> None:
        rows = {row["boundary_id"]: row for row in read_csv("service_function_boundary_v1.csv")}
        handoff = rows["W2B2-FB005"]
        self.assertEqual(handoff["relation_or_boundary"], "confirmed_service_intermediation")
        self.assertIn("NMCRS funds", handoff["nmcrs_evidence"])
        self.assertIn("do not code it as red cross funding", handoff["prohibited_inference"].lower())
        co_location = rows["W2B2-FB010"]
        self.assertIn("not a cross-organization bridge", co_location["prohibited_inference"])

    def test_source_hashes_and_blocked_receipt(self) -> None:
        rows = read_csv("source_receipts_v1.csv")
        blocked = [row for row in rows if row["archive_status"] == "blocked_403_logged"]
        self.assertEqual([row["receipt_id"] for row in blocked], ["W2B2-SR031"])
        self.assertEqual(blocked[0]["artifact_path"], "")
        archived = [row for row in rows if row["artifact_path"]]
        self.assertEqual(len(archived), 33)
        for row in archived:
            self.assertEqual(file_hash(ROOT / row["artifact_path"]), row["sha256"])

    def test_principal_queue_remains_open(self) -> None:
        rows = read_csv("principal_review_queue_v1.csv")
        self.assertEqual(len(rows), 7)
        self.assertTrue(all(row["status"] == "awaiting_principal_review" for row in rows))
        self.assertTrue(all(not row["principal_decision"] for row in rows))

    def test_w2d_endpoints_keep_people_and_service_relation_typed(self) -> None:
        rows = read_csv("w2_d_endpoint_candidates_v1.csv")
        people = [row for row in rows if row["endpoint_type"] == "person_actor_time_candidate"]
        interface = [row for row in rows if row["endpoint_type"] == "service_intermediary_relation"]
        self.assertEqual(len(people), 15)
        self.assertEqual(len(interface), 1)
        self.assertEqual(interface[0]["role_or_relation_type"], "after_hours_service_intermediation_using_nmcrs_funds")
        self.assertIn("do not code this relation as funding or alliance", interface[0]["prohibited_inference"])
        unresolved = {row["canonical_label"] for row in people if "unresolved" in row["identity_status"]}
        self.assertEqual(unresolved, {"E.J. Schulz / Shultz"})

    def test_svg_is_valid_xml(self) -> None:
        root = ET.parse(OUT / "fig_allocation_visibility_waterfall_v1.svg").getroot()
        self.assertTrue(root.tag.endswith("svg"))

    def test_validation_and_manifest(self) -> None:
        validation = json.loads((OUT / "validation_report_v1.json").read_text(encoding="utf-8"))
        self.assertEqual(validation["status"], "PASS_RESEARCH_ONLY")
        self.assertEqual(validation["fail_count"], 0)
        manifest = json.loads((OUT / "manifest_v1.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["scope"], "research_only")
        self.assertGreaterEqual(manifest["file_count"], 30)
        for item in manifest["files"]:
            self.assertEqual(file_hash(ROOT / item["path"]), item["sha256"])


if __name__ == "__main__":
    unittest.main()
