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
            "hierarchy_and_site_year_v1.csv": 17,
            "service_capacity_observations_v1.csv": 15,
            "sponsor_and_local_flow_observations_v1.csv": 17,
            "federal_award_allocation_audit_v1.csv": 19,
            "service_function_boundary_v1.csv": 10,
            "allocation_waterfall_v1.csv": 11,
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
        by_id = {row["row_id"]: row for row in rows}
        self.assertEqual(sum(row["site_type"] == "operating_center" for row in rows), 6)
        current_ids = {f"W2B2-HS{number:03d}" for number in range(5, 13)}
        current = [row for row in rows if row["row_id"] in current_ids]
        self.assertEqual(len(current), 8)
        self.assertEqual({row["site_type"] for row in current}, {"operating_center", "transport_terminal_presence", "administrative_area_office"})
        self.assertEqual(by_id["W2B2-HS004"]["quantity"], "8")
        self.assertEqual(by_id["W2B2-HS004"]["quantity_unit"], "directory_entries")
        self.assertIn("six centers + one terminal entry + one area office", by_id["W2B2-HS004"]["allowed_claim"])

    def test_dated_location_vocabularies_do_not_imply_lifecycle(self) -> None:
        rows = {row["row_id"]: row for row in read_csv("hierarchy_and_site_year_v1.csv")}
        self.assertEqual((rows["W2B2-HS013"]["quantity"], rows["W2B2-HS013"]["quantity_unit"]), ("7", "listed_locations"))
        self.assertIn("7 listed locations", rows["W2B2-HS013"]["allowed_claim"])
        self.assertEqual((rows["W2B2-HS017"]["quantity"], rows["W2B2-HS017"]["quantity_unit"]), ("6", "physical_centers"))
        self.assertIn("6 physical centers", rows["W2B2-HS017"]["allowed_claim"])
        for row_id in ("W2B2-HS004", "W2B2-HS013", "W2B2-HS017"):
            self.assertIn("lifecycle", rows[row_id]["prohibited_inference"].lower())

        prose = (OUT / "README.md").read_text(encoding="utf-8").lower()
        self.assertNotIn("8 sites", prose)
        self.assertNotIn("eight sites", prose)

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
        self.assertEqual(rows["W2B2-FA009"]["status"], "official_same_award_account_reporting_view")
        self.assertEqual(rows["W2B2-FA001"]["semantic_conflict_id"], rows["W2B2-FA009"]["semantic_conflict_id"])

    def test_2024_program_services_keep_gross_in_kind_and_net_typed(self) -> None:
        rows = {row["stage_id"]: row for row in read_csv("allocation_waterfall_v1.csv")}
        gross = rows["W2B2-WF009"]
        in_kind = rows["W2B2-WF010"]
        net = rows["W2B2-WF011"]
        self.assertEqual(gross["known_amount"], "204912000")
        self.assertEqual(gross["measurement_type"], "consolidated_gross_program_services_functional_expenses")
        self.assertEqual(in_kind["known_amount"], "105538000")
        self.assertEqual(in_kind["measurement_type"], "in_kind_program_services_included_in_gross")
        self.assertEqual(net["known_amount"], "99374000")
        self.assertEqual(net["measurement_type"], "consolidated_net_program_services_after_in_kind")
        self.assertEqual(204_912_000 - 105_538_000, 99_374_000)

        receipts = {row["receipt_id"]: row for row in read_csv("source_receipts_v1.csv")}
        locator = receipts["W2B2-SR034"]["exact_locator"]
        self.assertIn("p.8", locator)
        self.assertIn("Functional expenses, gross", locator)
        self.assertIn("105,538", locator)
        self.assertIn("Functional expenses, net", locator)

    def test_no_synthetic_region_or_okinawa_amount(self) -> None:
        rows = {row["stage_id"]: row for row in read_csv("allocation_waterfall_v1.csv")}
        for row_id in ("W2B2-WF003", "W2B2-WF004", "W2B2-WF005"):
            self.assertEqual(rows[row_id]["known_amount"], "")
            self.assertEqual(rows[row_id]["visibility_status"], "allocation_gap")

    def test_same_award_reporting_views_are_parallel_not_a_money_chain(self) -> None:
        rows = {row["stage_id"]: row for row in read_csv("allocation_waterfall_v1.csv")}
        award = rows["W2B2-WF001"]
        account = rows["W2B2-WF002"]
        self.assertEqual(award["lane"], "same_award_parallel_reporting_views")
        self.assertEqual(account["lane"], "same_award_parallel_reporting_views")
        self.assertEqual(award["next_gap"], "regional_allocation_not_disclosed")
        self.assertEqual(account["next_gap"], "regional_allocation_not_disclosed")
        self.assertIn("same award", award["reason_not_additive"].lower())
        self.assertIn("same award", account["reason_not_additive"].lower())

        svg = (OUT / "fig_allocation_visibility_waterfall_v1.svg").read_text(encoding="utf-8")
        self.assertIn("同一 award 的两个并列报送视图", svg)
        self.assertIn("连线表示共同的信息缺口，不表示资金逐层流下", svg)
        self.assertNotIn('d="M350 236 H405"', svg)

    def test_named_local_flows_are_not_a_budget(self) -> None:
        rows = read_csv("sponsor_and_local_flow_observations_v1.csv")
        aec = [row for row in rows if row["source_name"] == "American Engineering Corporation" and row["amount"] == "18000"]
        self.assertEqual({row["date_start"] for row in aec}, {"2018-03-01", "2024-10-16"})
        self.assertFalse(any(row["source_name"] in {"United Service Organizations, Inc.", "Department of Defense"} for row in rows))

    def test_nmcrs_to_red_cross_relation_is_directional_candidate(self) -> None:
        rows = {row["boundary_id"]: row for row in read_csv("service_function_boundary_v1.csv")}
        handoff = rows["W2B2-FB005"]
        self.assertEqual(handoff["relation_or_boundary"], "directed_nmcrs_to_arc_after_hours_intake_disbursement_delegation")
        self.assertEqual(handoff["claim_status"], "official_source_supported_candidate_pending_principal")
        self.assertIn("NMCRS delegates after-hours intake/disbursement to ARC", handoff["allowed_claim"])
        self.assertIn("ARC acts on NMCRS's behalf using NMCRS funds", handoff["allowed_claim"])
        self.assertIn("NMCRS funds", handoff["nmcrs_evidence"])
        self.assertNotIn("confirmed", " ".join(handoff.values()).lower())
        self.assertIn("do not code the delegation as an interorganizational grant", handoff["prohibited_inference"].lower())
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
        by_id = {row["decision_id"]: row for row in rows}
        self.assertIn("parallel reporting views of the same award", by_id["W2B2-PR002"]["question"])
        self.assertIn("NMCRS -> American Red Cross", by_id["W2B2-PR005"]["question"])
        self.assertIn("candidate", by_id["W2B2-PR005"]["recommended_decision"])

    def test_w2d_endpoints_keep_people_and_service_relation_typed(self) -> None:
        rows = read_csv("w2_d_endpoint_candidates_v1.csv")
        people = [row for row in rows if row["endpoint_type"] == "person_actor_time_candidate"]
        interface = [row for row in rows if row["endpoint_type"] == "service_intermediary_relation"]
        self.assertEqual(len(people), 15)
        self.assertEqual(len(interface), 1)
        self.assertEqual(interface[0]["role_or_relation_type"], "directed_nmcrs_to_arc_after_hours_intake_disbursement_delegation_using_nmcrs_funds")
        self.assertIn("X009 Navy-Marine Corps Relief Society Okinawa -> X008 American Red Cross Okinawa", interface[0]["linked_actor_or_endpoint"])
        self.assertEqual(interface[0]["identity_status"], "official_source_supported_candidate_pending_principal")
        self.assertIn("NMCRS delegates after-hours intake/disbursement to ARC", interface[0]["allowed_claim"])
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
        self.assertGreaterEqual(validation["check_count"], 50)
        manifest = json.loads((OUT / "manifest_v1.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["scope"], "research_only")
        self.assertGreaterEqual(manifest["file_count"], 30)
        for item in manifest["files"]:
            self.assertEqual(file_hash(ROOT / item["path"]), item["sha256"])

    def test_build_is_deterministic_and_protected_central_is_unchanged(self) -> None:
        protected = [
            *sorted((ROOT / "data" / "interim").glob("*.csv")),
            *sorted((ROOT / "data" / "metadata").glob("*")),
            *sorted((ROOT / "outputs" / "exploration_system_data_v1").glob("*")),
            *sorted((ROOT / "prototypes" / "nr3_explorer" / "src").rglob("*")),
        ]
        protected = [path for path in protected if path.is_file()]
        before = {path.relative_to(ROOT).as_posix(): file_hash(path) for path in protected}
        self.assertEqual(BUILD.main(), 0)
        first_manifest = file_hash(OUT / "manifest_v1.json")
        self.assertEqual(BUILD.main(), 0)
        second_manifest = file_hash(OUT / "manifest_v1.json")
        after = {path.relative_to(ROOT).as_posix(): file_hash(path) for path in protected}
        self.assertEqual(first_manifest, second_manifest)
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
