#!/usr/bin/env python3
"""Build W2-D: bounded bridge audit for the two U.S.-presence ecologies.

This builder is deliberately additive and research-only.  It joins the frozen
W2-00 selection frames with W2-A/W2-B endpoint handoffs and the current typed
research inputs.  It writes only ``outputs/us_presence_network_wave2_w2_d_v1``.
It never writes the central fact tables, publication adapter, frontend, or
control documents.

The central methodological distinction is preserved in the data model:

* a confirmed cross-ecology bridge is a sourced relation between two actors;
* a shared institutional interface (for example DoD as USO prime funder and
  defendant in the Dugong case) is useful system context, but not an NGO bridge;
* shared place is context only;
* a no-hit becomes ``audited_public_record_zero`` only for the declared tracer
  window, actor pair, relation family and source corpus.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "us_presence_network_wave2_w2_d_v1"
UNEXPECTED_FINDINGS_TEMPLATE = (
    ROOT / "data" / "metadata" / "unexpected_findings_register_template_v1.csv"
)
ART = OUT / "artifacts" / "a0_official"
BUILD_DATE = "2026-08-22"
WINDOW_START = "2023-01-01"
WINDOW_END = "2025-12-31"

REVIEW_STATUS = "ai_seeded"
PACKAGE_SCOPE = "research_only"
FRONTEND_STATUS = "not_frontend_ready"
CENTRAL_WRITEBACK = "no"

LEGAL_REVIEW_STATUSES = {
    "ai_seeded",
    "human_checked",
    "human_revised",
    "needs_second_source",
    "needs_local_retrieval",
    "rejected",
}

FRAME_TRACER = "USF-W2D-BRIDGE-TRACER15-2026-08-22"
FRAME_A1R = "USF-W2D-ECOLOGY-S0-A1R-2026-08-22"
FRAME_A1C = "USF-W2D-SENSITIVITY-S0-A1C-2026-08-22"

RELATION_FAMILIES = [
    "direct_organization_relation",
    "shared_person",
    "shared_recipient_or_intermediary",
    "shared_funder_or_sponsor",
    "same_public_event",
    "shared_place_background",
]

SOURCE_FAMILIES = [
    "official_roster_or_team",
    "applicable_990_part_vii_schedule_i",
    "annual_report_or_financial",
    "case_or_event_role",
    "recipient_or_partner_announcement",
]

PROTECTED = [
    ROOT / "data" / "interim" / "01_actor_registry_initial_v0.csv",
    ROOT / "data" / "interim" / "05_source_log_initial_v0.csv",
    ROOT / "data" / "interim" / "07_actor_issue_edges_initial_v0.csv",
    ROOT / "data" / "interim" / "08_actor_place_edges_initial_v0.csv",
    ROOT / "data" / "interim" / "09_actor_event_venue_edges_v0.csv",
    ROOT / "data" / "interim" / "15_funding_or_support_edges_sample_v0.csv",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for raw in rows:
            writer.writerow({field: raw.get(field, "") for field in fields})


def unexpected_findings_fields() -> list[str]:
    with UNEXPECTED_FINDINGS_TEMPLATE.open("r", encoding="utf-8-sig", newline="") as handle:
        return next(csv.reader(handle))


def common(row: dict[str, object]) -> dict[str, object]:
    return {
        **row,
        "review_status": REVIEW_STATUS,
        "package_scope": PACKAGE_SCOPE,
        "frontend_status": FRONTEND_STATUS,
        "central_writeback": CENTRAL_WRITEBACK,
    }


def split_ids(value: object) -> list[str]:
    return [
        item.strip()
        for item in str(value or "").replace("|", ";").split(";")
        if item.strip()
    ]


def normalize_name(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.lower())


def year_in_window(value: object) -> bool:
    match = re.search(r"(20\d{2})", str(value or ""))
    return bool(match and 2023 <= int(match.group(1)) <= 2025)


def get_frame_members() -> tuple[
    dict[str, str], dict[str, str], dict[str, str], dict[str, str]
]:
    path = (
        ROOT
        / "outputs"
        / "us_presence_network_wave2_w2_00_v1"
        / "selection_frame_actor_members_v1.csv"
    )
    rows = read_csv(path)

    def select(frame: str, group_prefix: str) -> dict[str, str]:
        return {
            row["actor_id"]: row["actor_name"]
            for row in rows
            if row["selection_frame_id"] == frame
            and row["analytical_group"].startswith(group_prefix)
        }

    s0 = select(FRAME_TRACER, "S0_")
    a0 = select(FRAME_TRACER, "A0_")
    a1r = select(FRAME_A1R, "A1R_")
    a1c = select(FRAME_A1C, "A1C_")
    assert len(s0) == 9
    assert len(a0) == 6
    assert len(a1r) == 41
    assert len(a1c) == 36
    return s0, a0, a1r, a1c


# Manual A0 audit rows are a source-bounded reading of official materials.
# Every no-hit preserves its source-family and observation-window boundary.
A0_AUDIT = {
    "A009": {
        "activity": ("observed_in_window_general_org", "FY2024 annual report/990"),
        "official_roster_or_team": ("snapshot_2026_only", "https://earthjustice.org/about/staff", "Current staff page; Abigail Dillen listed as President; not backdated"),
        "applicable_990_part_vii_schedule_i": ("found_in_window", "https://earthjustice.org/document/irs-form-990-fy2024", "FY2024 Form 990; Schedule I pp. 46-48"),
        "annual_report_or_financial": ("found_in_window", "https://earthjustice.org/about/financial-statements", "FY2023/FY2024 reports and filings index"),
        "case_or_event_role": ("historical_only_no_window_action", "https://earthjustice.org/case/okinawa-dugong-proposed-airbase", "Dugong case page names CBD and TIRN as clients; no 2023-2025 event date"),
        "recipient_or_partner_announcement": ("not_found_bounded", "https://earthjustice.org/about/financial-statements", "No S0 organization named in reviewed Schedule I or exact official-site probes"),
    },
    "A033": {
        "activity": ("observed_in_window_general_org", "2024 annual report"),
        "official_roster_or_team": ("snapshot_2026_only", "https://foe.org/about-us/our-president/", "Current president/board pages; not backdated"),
        "applicable_990_part_vii_schedule_i": ("partial_schedule_i_unresolved", "https://foe.org/about-us/accountability/", "FY2024 filing listed; Schedule I requires page-level extraction"),
        "annual_report_or_financial": ("found_in_window", "https://foe.org/report/2024-annual-report/", "2024 annual report"),
        "case_or_event_role": ("not_found_bounded", "https://foe.org/about-us/accountability/", "No 2023-2025 Okinawa or S0 event role in reviewed official entries"),
        "recipient_or_partner_announcement": ("not_found_bounded", "https://foe.org/about-us/accountability/", "No S0 name in reviewed official financial/report entries"),
    },
    "A042": {
        "activity": ("observed_in_window_general_org", "2025-05-15 IMO commentary"),
        "official_roster_or_team": ("snapshot_2026_only", "https://www.pacificenvironment.org/about-us/who-we-are/leadership/", "Current leadership entry; not backdated"),
        "applicable_990_part_vii_schedule_i": ("found_in_window_schedule_i_not_applicable", "https://www.pacificenvironment.org/wp-content/uploads/2026/01/Pacific-Environment_990_23-24.pdf", "FY2024 Form 990; Part IV lines 21/22 No"),
        "annual_report_or_financial": ("found_in_window", "https://www.pacificenvironment.org/about-us/financials/", "FY2024 financial statements and 990"),
        "case_or_event_role": ("not_found_bounded", "https://www.pacificenvironment.org/about-us/financials/", "No 2023-2025 Okinawa/S0 action in reviewed official materials"),
        "recipient_or_partner_announcement": ("not_found_bounded", "https://www.pacificenvironment.org/about-us/financials/", "No S0 recipient/funder/partner in reviewed official materials"),
    },
    "A045": {
        "activity": ("observed_in_window_general_org", "2024-12-26 organization review"),
        "official_roster_or_team": ("snapshot_2026_only", "https://www.biologicaldiversity.org/about/staff/", "Current staff directory; not backdated"),
        "applicable_990_part_vii_schedule_i": ("found_in_window", "https://www.biologicaldiversity.org/support/pdfs/Center-for-Biological-Diversity-form-990-2023.pdf", "2023 Form 990; Schedule I pp. 29-30"),
        "annual_report_or_financial": ("found_in_window", "https://www.biologicaldiversity.org/support/financials.html", "2023/2024 990 and audited financials index"),
        "case_or_event_role": ("historical_page_no_window_action", "https://www.biologicaldiversity.org/programs/international/japan.html", "Current Japan program page lacks 2023-2025 Okinawa action date"),
        "recipient_or_partner_announcement": ("not_found_bounded", "https://www.biologicaldiversity.org/support/financials.html", "No S0 name in reviewed Schedule I/official probes"),
    },
    "A070": {
        "activity": ("observed_in_window_okinawa_action", "2023 and 2025 VFP resolutions"),
        "official_roster_or_team": ("found_in_window_document_roles", "https://www.veteransforpeace.org/who-we-are/2025-online-business-meeting/resolution-2025-1-us-military-expansion-and-environmental-destruction-okinawa", "2025 resolution names Makishi Yoshikazu, Pete Shimazaki Doktor and Douglas Lummis"),
        "applicable_990_part_vii_schedule_i": ("not_applicable_standalone_chapter", "https://www.veteransforpeace.org/who-we-are/2025-online-business-meeting", "No separate chapter EIN/990 located; national 990 cannot substitute"),
        "annual_report_or_financial": ("not_found_bounded", "https://www.veteransforpeace.org/who-we-are/member-highlights/2024/08/08/2024-vfp-okinawajapan-peace-speaking-tour-report-1", "No chapter-specific annual report found"),
        "case_or_event_role": ("found_in_window", "https://www.veteransforpeace.org/who-we-are/2025-online-business-meeting/resolution-2025-1-us-military-expansion-and-environmental-destruction-okinawa", "2023/2025 official resolution and action records"),
        "recipient_or_partner_announcement": ("not_found_bounded", "https://www.veteransforpeace.org/who-we-are/2025-online-business-meeting", "No S0 organization named in reviewed official resolutions/pages"),
    },
    "A086": {
        "activity": ("observed_in_window_general_org", "2025 named activity roles"),
        "official_roster_or_team": ("found_in_window_document_roles", "https://seaturtles.org/category/eastern-tropical-pacific/", "2025 release names Todd Steiner and Ken Bouley"),
        "applicable_990_part_vii_schedule_i": ("partial_schedule_i_unresolved", "https://seaturtles.org/wp-content/uploads/2025/01/TIRN-6.30.2024-Public-Disclosure-Copy-2.pdf", "FY2024 Form 990 found; Schedule I page-level status unresolved"),
        "annual_report_or_financial": ("found_in_window", "https://seaturtles.org/wp-content/uploads/2025/01/TIRN-2024-Audit-FS-Final.pdf", "FY2024 audited financial statements"),
        "case_or_event_role": ("historical_only_no_window_action", "https://earthjustice.org/case/okinawa-dugong-proposed-airbase", "Historical Dugong case role; no 2023-2025 Okinawa action found"),
        "recipient_or_partner_announcement": ("not_found_bounded", "https://seaturtles.org/category/eastern-tropical-pacific/", "No S0 recipient/partner in reviewed official news/audit/990 entries"),
    },
}


S0_AUDIT = {
    "X001": {
        "activity": ("observed_in_window", "2025 USO Okinawa official stories and staffing snapshot"),
        "official_roster_or_team": ("found_in_window", "W2B2-DE014;W2B2-DE015;W2B2-DE025;W2B2-DE026", "Official stories name area/center managers"),
        "applicable_990_part_vii_schedule_i": ("found_parent_national", "W2B-A005;W2B2-SR034", "USO Inc. 2024 filing; local allocation absent"),
        "annual_report_or_financial": ("found_parent_national", "W2B-A001;W2B2-SR001", "2024 consolidated statements/impact report"),
        "case_or_event_role": ("found_in_window", "W2B2-SR010;W2B2-SR011", "2025 official Okinawa service episodes"),
        "recipient_or_partner_announcement": ("found_in_window", "W2B2-SR013;W2B2-SR032", "Official sponsor stories and OESC gift record"),
    },
    "X004": {
        "activity": ("observed_in_window", "FY2023/FY2024 official IRS filings"),
        "official_roster_or_team": ("found_in_window_filing_roles", "W2A-SR001;W2A-SR002", "Part VII/filing role strings"),
        "applicable_990_part_vii_schedule_i": ("found_in_window", "W2A-SR001;W2A-SR002", "Official IRS XML"),
        "annual_report_or_financial": ("not_found_bounded", "W2A-NS001:W2A-NS006", "No separate annual report in bounded W2-A corpus"),
        "case_or_event_role": ("found_in_window_recipient_actions", "W2A2-SR004:W2A2-SR013", "Recipient-side donation/use episodes"),
        "recipient_or_partner_announcement": ("partial_named_endpoint_coverage", "EH0110:EH0121", "Six descriptors; three local responses; zero exact transaction closure"),
    },
    "X005": {
        "activity": ("observed_in_window", "FY2023-FY2025 official IRS filings"),
        "official_roster_or_team": ("found_in_window_filing_roles", "W2A-SR009:W2A-SR011", "Part VII filing roles"),
        "applicable_990_part_vii_schedule_i": ("found_in_window", "W2A-SR009:W2A-SR011", "Official IRS XML"),
        "annual_report_or_financial": ("not_found_bounded", "W2A package", "No separate annual report in bounded corpus"),
        "case_or_event_role": ("found_in_window", "F036", "2025 joint in-kind delivery episode"),
        "recipient_or_partner_announcement": ("partial_filing_recipient_coverage", "W2A-SR009:W2A-SR011", "Filing recipients do not form exhaustive public ledger"),
    },
    "X006": {
        "activity": ("observed_in_window", "FY2023-FY2025 official IRS filings"),
        "official_roster_or_team": ("found_in_window_filing_roles", "W2A-SR003:W2A-SR005", "Part VII filing roles"),
        "applicable_990_part_vii_schedule_i": ("found_in_window", "W2A-SR003:W2A-SR005", "Official IRS XML"),
        "annual_report_or_financial": ("not_found_bounded", "W2A package", "No separate annual report in bounded corpus"),
        "case_or_event_role": ("not_found_bounded", "W2A package", "No exhaustive event archive; filing actions only"),
        "recipient_or_partner_announcement": ("partial_filing_recipient_coverage", "W2A-SR003:W2A-SR005", "Schedule I/aggregate recipients are incomplete"),
    },
    "X007": {
        "activity": ("observed_in_window", "FY2023-FY2025 filings and 2025 USO gift"),
        "official_roster_or_team": ("found_in_window_filing_roles", "W2A-SR012:W2A-SR014", "Part VII filing roles"),
        "applicable_990_part_vii_schedule_i": ("found_in_window", "W2A-SR012:W2A-SR014", "Official IRS XML"),
        "annual_report_or_financial": ("not_found_bounded", "W2A package", "No separate annual report in bounded corpus"),
        "case_or_event_role": ("found_in_window", "F021;W2B2-SR032", "2025 donation to USO Okinawa"),
        "recipient_or_partner_announcement": ("partial_filing_recipient_coverage", "W2A-SR012:W2A-SR014", "Named filing recipients, not exhaustive donor ledger"),
    },
    "X008": {
        "activity": ("observed_in_window", "2023 Typhoon Khanun official response"),
        "official_roster_or_team": ("not_found_bounded", "W2B2-SR020;W2B2-SR031", "Local office/function pages, no dated local roster"),
        "applicable_990_part_vii_schedule_i": ("not_examined_parent_filing_gap", "", "National filing not extracted in W2-B"),
        "annual_report_or_financial": ("not_examined_parent_report_gap", "", "National annual report not extracted in W2-B"),
        "case_or_event_role": ("found_in_window", "W2B2-SR020", "2023 Okinawa disaster response"),
        "recipient_or_partner_announcement": ("found_service_interface", "W2B2-SR022;W2B2-SR023", "NMCRS after-hours liaison interface"),
    },
    "X009": {
        "activity": ("observed_in_window_or_current_service", "W2B2 official Okinawa location/service records"),
        "official_roster_or_team": ("not_found_bounded", "W2B2-SR022;W2B2-SR023", "No dated local roster in selected pages"),
        "applicable_990_part_vii_schedule_i": ("not_examined_parent_filing_gap", "", "National filing not extracted in W2-B"),
        "annual_report_or_financial": ("parent_report_index_only", "W2B2-SR024", "Annual reports index, no Okinawa allocation"),
        "case_or_event_role": ("found_service_page", "W2B2-SR022", "Okinawa office/services"),
        "recipient_or_partner_announcement": ("found_service_interface", "W2B2-SR022;W2B2-SR023", "ARC after-hours liaison using NMCRS funds"),
    },
    "X016": {
        "activity": ("observed_in_window", "FY2023-FY2025 official IRS filings"),
        "official_roster_or_team": ("found_in_window_filing_roles", "W2A-SR006:W2A-SR008", "Part VII filing roles"),
        "applicable_990_part_vii_schedule_i": ("found_in_window", "W2A-SR006:W2A-SR008", "Official IRS XML"),
        "annual_report_or_financial": ("not_found_bounded", "W2A package", "No separate annual report in bounded corpus"),
        "case_or_event_role": ("not_found_bounded", "W2A package", "No exhaustive event archive; filing actions only"),
        "recipient_or_partner_announcement": ("partial_schedule_o_coverage", "W2A-SR006:W2A-SR008", "Schedule O commitments are not always paid grants"),
    },
    "X017": {
        "activity": ("not_observable_in_window", "Latest filing/activity anchors are historical"),
        "official_roster_or_team": ("not_found_window", "", "No 2023-2025 roster"),
        "applicable_990_part_vii_schedule_i": ("historical_outside_window", "SR-HR-007", "FY2018 filing only"),
        "annual_report_or_financial": ("not_found_window", "", "No 2023-2025 report"),
        "case_or_event_role": ("not_found_window", "", "No 2023-2025 event record"),
        "recipient_or_partner_announcement": ("not_found_window", "", "No 2023-2025 recipient record"),
    },
}


A0_URL_ARTIFACT = {
    "https://earthjustice.org/about/financial-statements": "a009_financial_statements.html",
    "https://earthjustice.org/case/okinawa-dugong-proposed-airbase": "a009_okinawa_dugong_case.html",
    "https://foe.org/about-us/accountability/": "",
    "https://foe.org/report/2024-annual-report/": "",
    "https://www.pacificenvironment.org/about-us/financials/": "a042_financials.html",
    "https://www.pacificenvironment.org/wp-content/uploads/2026/01/Pacific-Environment_990_23-24.pdf": "a042_fy24_990.pdf",
    "https://www.biologicaldiversity.org/support/financials.html": "a045_financials.html",
    "https://www.biologicaldiversity.org/support/pdfs/Center-for-Biological-Diversity-form-990-2023.pdf": "a045_2023_990.pdf",
    "https://www.biologicaldiversity.org/programs/international/japan.html": "a045_japan_program.html",
    "https://www.veteransforpeace.org/who-we-are/2025-online-business-meeting/resolution-2025-1-us-military-expansion-and-environmental-destruction-okinawa": "a070_2025_resolution.html",
    "https://www.veteransforpeace.org/who-we-are/member-highlights/2024/08/08/2024-vfp-okinawajapan-peace-speaking-tour-report-1": "a070_2024_peace_tour.html",
    "https://seaturtles.org/category/eastern-tropical-pacific/": "a086_2025_activity.html",
    "https://seaturtles.org/wp-content/uploads/2025/01/TIRN-6.30.2024-Public-Disclosure-Copy-2.pdf": "a086_fy24_990.pdf",
    "https://seaturtles.org/wp-content/uploads/2025/01/TIRN-2024-Audit-FS-Final.pdf": "a086_fy24_audit.pdf",
}


def build_activity_status(
    s0: dict[str, str], a0: dict[str, str], a1r: dict[str, str], a1c: dict[str, str]
) -> list[dict[str, object]]:
    registry = {row["actor_id"]: row for row in read_csv(PROTECTED[0])}
    source_year = {
        row["source_id"]: row.get("year", "")
        for row in read_csv(ROOT / "data" / "interim" / "05_source_log_initial_v0.csv")
    }
    refs: dict[str, set[str]] = defaultdict(set)
    evidence: dict[str, set[str]] = defaultdict(set)

    for actor_id, row in registry.items():
        for ref in split_ids(row.get("source_refs", "")):
            if year_in_window(source_year.get(ref, "")):
                refs[actor_id].add(ref)
                evidence[actor_id].add(f"source_year:{source_year.get(ref)}")

    for path, actor_field, ref_field in [
        (ROOT / "data" / "interim" / "07_actor_issue_edges_initial_v0.csv", "actor_id", "source_ref"),
        (ROOT / "data" / "interim" / "08_actor_place_edges_initial_v0.csv", "actor_id", "source_ref"),
    ]:
        for row in read_csv(path):
            actor_id = row.get(actor_field, "")
            for ref in split_ids(row.get(ref_field, "")):
                if year_in_window(source_year.get(ref, "")):
                    refs[actor_id].add(ref)
                    evidence[actor_id].add(f"source_year:{source_year.get(ref)}")

    for row in read_csv(ROOT / "data" / "interim" / "09_actor_event_venue_edges_v0.csv"):
        actor_id = row.get("actor_or_counterpart_id", "")
        if year_in_window(row.get("event_year", "")):
            refs[actor_id].add(row.get("record_id", ""))
            evidence[actor_id].add(f"event_year:{row.get('event_year', '')}")

    actor_groups: dict[str, set[str]] = defaultdict(set)
    actor_names: dict[str, str] = {}
    for label, members in [("S0", s0), ("A0", a0), ("A1R", a1r), ("A1C", a1c)]:
        for actor_id, name in members.items():
            actor_groups[actor_id].add(label)
            actor_names[actor_id] = name

    rows: list[dict[str, object]] = []
    for index, actor_id in enumerate(sorted(actor_groups), 1):
        if actor_id in S0_AUDIT:
            status, basis = S0_AUDIT[actor_id]["activity"]
        elif actor_id in A0_AUDIT:
            status, basis = A0_AUDIT[actor_id]["activity"]
        elif refs.get(actor_id):
            status = "observed_in_window_source_or_event_anchor"
            basis = ";".join(sorted(evidence[actor_id]))
        else:
            status = "not_observable_in_window_from_bounded_inputs"
            basis = "No 2023-2025 source-year or event-year anchor in the selected central inputs"
        rows.append(
            common(
                {
                    "activity_row_id": f"W2D-ACT{index:03d}",
                    "actor_id": actor_id,
                    "actor_name": actor_names[actor_id],
                    "analytical_groups": ";".join(sorted(actor_groups[actor_id])),
                    "window_start": WINDOW_START,
                    "window_end": WINDOW_END,
                    "activity_status": status,
                    "activity_anchor_refs": ";".join(sorted(refs.get(actor_id, set()))),
                    "activity_anchor_basis": basis,
                    "interpretation_limit": "An in-window source publication or event anchor supports observability in the bounded inputs, not uninterrupted real-world activity.",
                }
            )
        )
    return rows


def build_source_family_audit(s0: dict[str, str], a0: dict[str, str]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    index = 1
    for side, members, audit in [("S0_service", s0, S0_AUDIT), ("A0_accountability", a0, A0_AUDIT)]:
        for actor_id, actor_name in members.items():
            for family in SOURCE_FAMILIES:
                status, source_ref_or_url, locator = audit[actor_id][family]
                rows.append(
                    common(
                        {
                            "coverage_row_id": f"W2D-SC{index:03d}",
                            "actor_id": actor_id,
                            "actor_name": actor_name,
                            "analytical_side": side,
                            "source_family": family,
                            "window_start": WINDOW_START,
                            "window_end": WINDOW_END,
                            "coverage_status": status,
                            "source_ref_or_url": source_ref_or_url,
                            "exact_locator_or_result": locator,
                            "s0_name_hit": "no_confirmed_hit",
                            "completion_semantics": "bounded_source_family_result",
                            "allowed_claim": "The declared source family was checked to the stated depth and status.",
                            "prohibited_inference": "A not-found or incomplete status is not evidence that the relationship does not exist in reality.",
                        }
                    )
                )
                index += 1
    return rows


def active_place_rows() -> list[dict[str, str]]:
    rows = read_csv(ROOT / "data" / "interim" / "08_actor_place_edges_initial_v0.csv")
    return [
        row
        for row in rows
        if row.get("review_status") != "rejected"
        and row.get("place_review_status") != "rejected"
        and not row.get("superseded_by_edge_id")
        and "retired" not in row.get("scope_status", "")
    ]


def shared_places_by_pair() -> dict[tuple[str, str], list[str]]:
    per_actor: dict[str, set[tuple[str, str]]] = defaultdict(set)
    for row in active_place_rows():
        per_actor[row["actor_id"]].add((row["place_id"], row["place_name"]))
    result: dict[tuple[str, str], list[str]] = {}
    for left, left_places in per_actor.items():
        for right, right_places in per_actor.items():
            if left >= right:
                continue
            overlap = sorted(left_places & right_places)
            if overlap:
                result[(left, right)] = [f"{place_id}:{name}" for place_id, name in overlap]
    return result


DIRECT_ZERO_ELIGIBLE_S0 = {"X001", "X004", "X005", "X006", "X007", "X016"}


def build_bridge_matrix(
    s0: dict[str, str],
    a0: dict[str, str],
    a1r: dict[str, str],
    a1c: dict[str, str],
    activity_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    activity = {str(row["actor_id"]): str(row["activity_status"]) for row in activity_rows}
    place_overlap = shared_places_by_pair()
    frames = [
        (FRAME_TRACER, "deep_tracer", a0),
        (FRAME_A1R, "confirmatory_reviewed_anchor_ecology", a1r),
        (FRAME_A1C, "candidate_sensitivity_ecology", a1c),
    ]
    rows: list[dict[str, object]] = []
    index = 1
    for frame_id, frame_role, accountability_members in frames:
        for service_id, service_name in s0.items():
            for account_id, account_name in accountability_members.items():
                service_observed = not activity.get(service_id, "").startswith("not_observable")
                account_observed = not activity.get(account_id, "").startswith("not_observable")
                pair_key = tuple(sorted((service_id, account_id)))
                shared_places = place_overlap.get(pair_key, [])
                for family in RELATION_FAMILIES:
                    pair_observability = (
                        "both_endpoints_observed_in_window"
                        if service_observed and account_observed
                        else "not_observable_in_window"
                    )
                    audit_result = "unresolved"
                    screening = "no_confirmed_bridge_in_bounded_inputs"
                    coverage = "ecology_screen_only_not_symmetric_source_audit"
                    refs = ""
                    reason = "No confirmed cross-ecology endpoint match in the bounded typed inputs; source-family coverage is insufficient for a negative result."

                    if frame_id == FRAME_TRACER:
                        coverage = "tracer_source_family_audit"
                        reason = "No confirmed S0-A0 relation in the declared official-source and endpoint corpus."
                        if not (service_observed and account_observed):
                            screening = "not_observable_in_window"
                            reason = "At least one endpoint lacks a 2023-2025 activity anchor in the bounded inputs."
                        elif family == "direct_organization_relation" and service_id in DIRECT_ZERO_ELIGIBLE_S0:
                            audit_result = "audited_public_record_zero"
                            screening = "bounded_symmetric_name_and_relation_search_complete"
                            coverage = "declared_source_corpus_complete_for_direct_relation"
                            reason = "Both endpoints are observable; A0 official sources and the service-side W2-A/W2-B corpus were searched symmetrically for names and direct relations with no confirmed hit."
                        elif family == "shared_funder_or_sponsor":
                            screening = "structurally_unobservable_or_incomplete"
                            coverage = "schedule_b_anonymity_and_funder_extraction_gap"
                            reason = "Donor anonymity and incomplete funder extraction prevent a shared-funder zero."
                        elif family == "shared_person":
                            screening = "no_identity_resolved_cross_side_match"
                            coverage = "dated_roles_partial_not_full_roster"
                            reason = "No exact identity-resolved match appears in extracted roles, but roster coverage is incomplete."
                        elif family == "shared_recipient_or_intermediary":
                            screening = "no_confirmed_endpoint_crosswalk"
                            coverage = "recipient_endpoint_and_transaction_closure_incomplete"
                            reason = "No recipient/intermediary is closed to both sides; W2-A has six candidate recipients and zero exact transaction closure."
                        elif family == "same_public_event":
                            screening = "no_confirmed_same_event"
                            coverage = "event_corpora_bounded_not_exhaustive"
                            reason = "No same event is confirmed in the bounded records; event archives are not exhaustive."

                    if family == "shared_place_background" and shared_places:
                        screening = "context_only_shared_place_not_bridge"
                        coverage = "central_actor_place_exact_id_overlap_time_unbounded"
                        refs = ";".join(shared_places)
                        reason = "The actors share an exact coded place, but the place rows are historical/undated context and do not constitute a bridge."

                    rows.append(
                        common(
                            {
                                "matrix_row_id": f"W2D-BM{index:05d}",
                                "selection_frame_id": frame_id,
                                "frame_role": frame_role,
                                "service_actor_id": service_id,
                                "service_actor_name": service_name,
                                "accountability_actor_id": account_id,
                                "accountability_actor_name": account_name,
                                "relation_family": family,
                                "window_start": WINDOW_START,
                                "window_end": WINDOW_END,
                                "service_activity_status": activity.get(service_id, "unknown"),
                                "accountability_activity_status": activity.get(account_id, "unknown"),
                                "pair_observability": pair_observability,
                                "source_coverage_status": coverage,
                                "observed_endpoint_refs": refs,
                                "audit_result": audit_result,
                                "screening_disposition": screening,
                                "reason": reason,
                                "allowed_claim": "Report only the pair, family, window and source-bound result encoded in this row.",
                                "prohibited_inference": "Do not generalize an unresolved or bounded zero row to all real-world relationships; shared place is not a bridge and same-event participation is not an alliance.",
                            }
                        )
                    )
                    index += 1
    return rows


def build_person_queue() -> list[dict[str, object]]:
    w2a = read_csv(OUT.parent / "us_presence_network_wave2_w2_a_v1" / "w2d_endpoint_handoff_v1.csv")
    pair_rows = [row for row in w2a if row["endpoint_family"] == "person_identity_pair_candidate"]
    rows: list[dict[str, object]] = []
    index = 1
    for row in pair_rows:
        rows.append(
            common(
                {
                    "disambiguation_id": f"W2D-PD{index:03d}",
                    "candidate_scope": "within_service_ecology",
                    "name_a": row["subject_name"],
                    "actor_a": row["subject_name"].split("[")[-1].rstrip("]") if "[" in row["subject_name"] else "",
                    "name_b": row["counterpart_name"],
                    "actor_b": row["counterpart_id"],
                    "period_a_or_joint": f"{row['period_start']}/{row['period_end']}",
                    "period_b": "",
                    "source_refs": row["source_receipt_ids"],
                    "candidate_type": row["identity_status"],
                    "current_decision": "unresolved",
                    "cross_ecology_bridge_eligibility": "no_until_identity_and_cross_side_role_close",
                    "principal_question": "Are the two source strings the same person during overlapping role periods?",
                    "allowed_claim": row["allowed_claim"],
                    "prohibited_inference": row["prohibited_inference"],
                }
            )
        )
        index += 1

    extras = [
        ("E.J. Schulz", "X004", "E.J. Shultz", "X004", "2020-08-28", "W2B2-DE023", "within_actor_spelling_conflict", "Resolve spelling before a person node is created."),
        ("J. Phil VanEtten", "X001", "Phil VanEtten", "X001", "2018-02-09/2025-03-12", "W2B2-DE014", "within_actor_alias_candidate", "Confirm that the two official story forms refer to one person."),
        ("Charles Douglas Lummis / Doug Lummis", "A070", "Douglas Lummis", "A070", "2020/2021/2025 observations", "USAPN006;USAPN011;A0 official audit", "within_actor_alias_candidate", "Normalize only after chapter role/date review."),
        ("Pete Doktor / Pete Shimazaki Doktor", "A070", "Pete Shimazaki Doktor", "A070", "2020/2021/2025 observations", "USAPN007;USAPN010;A0 official audit", "within_actor_alias_candidate", "Normalize only after chapter role/date review."),
    ]
    for name_a, actor_a, name_b, actor_b, period, refs, ctype, question in extras:
        rows.append(
            common(
                {
                    "disambiguation_id": f"W2D-PD{index:03d}",
                    "candidate_scope": "within_ecology_not_cross_ecology",
                    "name_a": name_a,
                    "actor_a": actor_a,
                    "name_b": name_b,
                    "actor_b": actor_b,
                    "period_a_or_joint": period,
                    "period_b": "",
                    "source_refs": refs,
                    "candidate_type": ctype,
                    "current_decision": "unresolved",
                    "cross_ecology_bridge_eligibility": "no",
                    "principal_question": question,
                    "allowed_claim": "The source strings form a bounded identity-normalization candidate.",
                    "prohibited_inference": "Do not create a shared-person node or cross-organization bridge before identity and overlapping roles are confirmed.",
                }
            )
        )
        index += 1
    return rows


def build_negative_search_log() -> list[dict[str, object]]:
    rows = [
        ("service_side_artifact_corpus", "W2-A IRS/recipient artifacts; W2-B USO/ARC/NMCRS artifacts", "Earthjustice; Friends of the Earth; Pacific Environment; Center for Biological Diversity; Veterans for Peace; Turtle Island Restoration Network; SeaTurtles.org", "no_exact_name_hit", "The service-side artifact corpus contains no exact A0 organization-name hit.", "The corpus is bounded and cannot prove no relationship exists."),
        ("A009 Earthjustice", "official FY2024 filing/report and Dugong case page", "S0 nine organization names and known aliases", "no_confirmed_s0_hit", "No S0 organization is named in the reviewed entries.", "The case page is historical and the negative result is source-bounded."),
        ("A033 Friends of the Earth U.S.", "official accountability and 2024 report entries", "S0 nine organization names", "no_confirmed_s0_hit", "No S0 name in reviewed official entries.", "FY2024 Schedule I extraction remains incomplete."),
        ("A042 Pacific Environment", "official FY2024 filing/financial pages", "S0 nine organization names", "no_confirmed_s0_hit", "No S0 name in reviewed official entries.", "Brand/legal-name and shared-address observations are not bridges."),
        ("A045 Center for Biological Diversity", "official 2023 filing and Japan program page", "S0 nine organization names", "no_confirmed_s0_hit", "No S0 name in reviewed Schedule I/official entries.", "Historical Dugong relations are not current S0 bridges."),
        ("A070 VFP-ROCK", "official 2023/2025 resolutions and 2024 report", "S0 nine organization names", "no_confirmed_s0_hit", "No S0 name in reviewed official event records.", "Same-event participation, if later found, would remain event-level."),
        ("A086 TIRN", "official FY2024 filing/audit and 2025 activity page", "S0 nine organization names", "no_confirmed_s0_hit", "No S0 name in reviewed official entries.", "Schedule I page-level status is unresolved."),
        ("cross_side_people", "104 W2-A filing roles; 15 W2-B role endpoints; available A0 named roles", "normalized exact names", "no_exact_cross_side_person_match", "No exact identity-resolved cross-side person match is present.", "A0/S0 roster coverage is incomplete; this is not a shared-person zero."),
        ("recipient_crosswalk", "six W2-A candidate recipients plus A1R/A1C actor names", "exact normalized organization labels", "no_confirmed_cross_ecology_recipient", "No recipient closes to an accountability actor or both sides.", "Three local responses and zero exact transaction closures do not define a complete recipient universe."),
        ("typed_direct_relations", "43-row legacy typed relation sample; W2-A/B handoffs; accountability actions", "S0-to-A0/A1R/A1C dyads", "no_confirmed_cross_ecology_direct_dyad", "No direct organization dyad is confirmed in these inputs.", "Ecology-wide nonexistence is not established."),
        ("same_event", "central AEV plus W2-B service episodes and A0 official event audit", "same event id/date and named participation", "no_confirmed_same_event", "No same public event is confirmed across sides in the bounded inputs.", "Event corpora are incomplete and co-participation would not be an alliance."),
        ("shared_funder", "available 990/financial and sponsor observations", "named funders/sponsors", "not_testable_to_zero", "No confirmed shared funder is closed; donor anonymity/incomplete extraction prevents a zero.", "A future shared funder would show source intersection, not coordination."),
        ("X017 current observability", "registry, historical AWWA and filing leads", "2023-2025 roster/filing/report/event/recipient", "not_observable_in_window", "No current activity anchor is available in the bounded inputs.", "Historical membership cannot be treated as a current organization relation."),
    ]
    return [
        common(
            {
                "search_id": f"W2D-NS{index:03d}",
                "subject": subject,
                "source_scope": scope,
                "query_or_match_rule": query,
                "search_date": BUILD_DATE,
                "bounded_result": result,
                "allowed_claim": allowed,
                "prohibited_inference": prohibited,
            }
        )
        for index, (subject, scope, query, result, allowed, prohibited) in enumerate(rows, 1)
    ]


def build_relation_family_coverage(matrix: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    for row in matrix:
        grouped[(str(row["selection_frame_id"]), str(row["relation_family"]))].append(row)
    rows: list[dict[str, object]] = []
    for index, ((frame, family), items) in enumerate(sorted(grouped.items()), 1):
        counts = defaultdict(int)
        service_actors = set()
        account_actors = set()
        observable_pairs = set()
        for row in items:
            counts[str(row["audit_result"])] += 1
            counts[f"screen:{row['screening_disposition']}"] += 1
            service_actors.add(str(row["service_actor_id"]))
            account_actors.add(str(row["accountability_actor_id"]))
            if row["pair_observability"] == "both_endpoints_observed_in_window":
                observable_pairs.add((row["service_actor_id"], row["accountability_actor_id"]))
        rows.append(
            common(
                {
                    "coverage_id": f"W2D-RC{index:03d}",
                    "selection_frame_id": frame,
                    "relation_family": family,
                    "service_actor_count": len(service_actors),
                    "accountability_actor_count": len(account_actors),
                    "pair_count": len(items),
                    "observable_pair_count": len(observable_pairs),
                    "confirmed_bridge_count": counts["confirmed_bridge"],
                    "audited_public_record_zero_count": counts["audited_public_record_zero"],
                    "unresolved_count": counts["unresolved"],
                    "shared_place_context_count": counts["screen:context_only_shared_place_not_bridge"],
                    "coverage_summary": "Tracer rows use the declared symmetric source audit; A1R/A1C rows are bounded typed-input screens and cannot produce ecology-wide zeros.",
                    "interpretation_limit": "Counts are pair-family audit states, not relationship prevalence or real-world separation rates.",
                }
            )
        )
    return rows


def build_graph() -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    nodes_raw = [
        ("X001", "USO Okinawa", "service_actor"),
        ("X004", "AWWA", "service_actor"),
        ("X005", "NOSCO", "service_actor"),
        ("X006", "KOSC", "service_actor"),
        ("X007", "OESC", "service_actor"),
        ("X008", "American Red Cross Okinawa", "service_actor"),
        ("X009", "NMCRS Okinawa", "service_actor"),
        ("X016", "MOSCO", "service_actor"),
        ("X017", "ACGO", "service_actor_unobservable"),
        ("X018", "Marine Thrift Shop", "s1_candidate"),
        ("USO_NATIONAL", "United Service Organizations, Inc.", "system_or_parent"),
        ("DOD", "U.S. Department of Defense", "system_interface"),
        ("R8C01", "Okinawa Dugong litigation", "case_endpoint"),
        ("A009", "Earthjustice", "accountability_actor"),
        ("A033", "Friends of the Earth U.S.", "accountability_actor"),
        ("A042", "Pacific Environment", "accountability_actor"),
        ("A045", "Center for Biological Diversity", "accountability_actor"),
        ("A070", "VFP-ROCK", "accountability_actor"),
        ("A086", "Turtle Island Restoration Network", "accountability_actor"),
        ("LOCAL_RECIPIENTS", "Named Okinawa welfare/medical recipients", "recipient_cluster"),
    ]
    nodes = [
        common({"node_id": node_id, "label": label, "node_type": node_type, "selection_status": "research_endpoint"})
        for node_id, label, node_type in nodes_raw
    ]
    edges_raw = [
        ("X004", "X005", "affiliation_membership", "historical_and_current_bounded", "F006", "AWWA umbrella membership; not control/funding"),
        ("X004", "X006", "affiliation_membership", "bounded", "F007", "AWWA umbrella membership"),
        ("X004", "X007", "affiliation_membership", "bounded", "F022", "AWWA umbrella membership"),
        ("X004", "X016", "affiliation_membership", "bounded", "F023", "AWWA umbrella membership"),
        ("X004", "X017", "historical_membership", "out_of_window", "F024", "Current continuity unconfirmed"),
        ("X007", "X004", "money_flow", "confirmed_dated", "EH0122;EH0123;EH0124", "Three dated filing flows; no downstream earmarking"),
        ("X018", "X004", "money_flow", "candidate", "EH0125;EH0131", "S1 candidate, not confirmatory frame"),
        ("X007", "X001", "money_flow", "confirmed_dated", "F021", "USD 3,250 donation on 2025-12-02"),
        ("X004", "LOCAL_RECIPIENTS", "service_recipient", "candidate_partial", "EH0110:EH0121", "Six descriptors; 3 local responses; 0 exact transaction closure"),
        (
            "X009", "X008", "service_intermediation",
            "official_source_supported_candidate_pending_principal", "W2B2-DE028",
            "Directed delegation/interface candidate: NMCRS funds and authority flow to ARC, which provides after-hours intake on NMCRS's behalf; pending principal review",
        ),
        ("USO_NATIONAL", "X001", "organization_hierarchy", "official_operating_structure", "W2B2-DE001:W2B2-DE004", "Hierarchy visible; local allocation not visible"),
        (
            "DOD", "USO_NATIONAL", "official_award", "national_prime",
            "W2B2-FA001;W2B-A021;W2B-A022;W2B-A024;W2B-A026;W2B-A032",
            "USD 72m national cumulative obligation; not cash paid or Okinawa receipt",
        ),
        ("A045", "R8C01", "case_role", "historical_human_checked", "R8R001", "Named plaintiff"),
        ("A086", "R8C01", "case_role", "historical_human_checked", "R8R002", "Named plaintiff"),
        ("A009", "R8C01", "case_role", "historical_human_checked", "R8R005", "Counsel"),
        ("R8C01", "DOD", "action_institution", "historical_human_checked", "R8C01", "DoD defendant/target; case did not stop project"),
        ("A033", "A045", "same_event", "historical_event_only", "EV2015_NACSJ_31", "Co-signing only; not alliance"),
        ("A042", "A045", "same_event", "historical_event_only", "EV2015_NACSJ_31", "Co-signing only; not alliance"),
        ("A070", "DOD", "action_institution_context", "window_event", "USAP006;USAP007", "Okinawa military-expansion resolutions/actions"),
    ]
    edges = []
    for index, (source, target, family, status, refs, limit) in enumerate(edges_raw, 1):
        cross_org_bridge = (
            source.startswith("X") and target.startswith("A")
        ) or (source.startswith("A") and target.startswith("X"))
        edges.append(
            common(
                {
                    "edge_id": f"W2D-EG{index:03d}",
                    "source_node_id": source,
                    "target_node_id": target,
                    "relation_family": family,
                    "edge_status": status,
                    "source_refs": refs,
                    "direction_semantics": (
                        "NMCRS delegates after-hours intake/disbursement to ARC; ARC acts on NMCRS's behalf using NMCRS funds"
                        if family == "service_intermediation" else ""
                    ),
                    "counts_as_cross_ecology_actor_bridge": "yes" if cross_org_bridge else "no",
                    "interpretation_limit": limit,
                }
            )
        )
    return nodes, edges


def render_graph_svg(nodes: list[dict[str, object]], edges: list[dict[str, object]]) -> str:
    # This is a directly-labelled explanatory egonet, not a metric centrality graph.
    positions = {
        "X004": (190, 215), "X005": (70, 115), "X006": (70, 165), "X007": (70, 215),
        "X016": (70, 265), "X017": (70, 325), "X018": (190, 100), "X001": (350, 215),
        "X008": (190, 355), "X009": (350, 355), "LOCAL_RECIPIENTS": (350, 100),
        "USO_NATIONAL": (500, 215), "DOD": (650, 250), "R8C01": (790, 250),
        "A009": (900, 90), "A033": (900, 140), "A045": (900, 190),
        "A042": (900, 240), "A086": (900, 290), "A070": (900, 340),
    }
    label_positions = {
        "X005": (58, 119, "end"), "X006": (58, 169, "end"), "X007": (58, 219, "end"),
        "X016": (58, 269, "end"), "X017": (58, 329, "end"), "X004": (190, 199, "middle"),
        "X018": (190, 82, "middle"), "LOCAL_RECIPIENTS": (350, 82, "middle"),
        "X001": (350, 199, "middle"), "X008": (190, 379, "middle"), "X009": (350, 379, "middle"),
        "USO_NATIONAL": (500, 198, "middle"), "DOD": (650, 276, "middle"),
        "R8C01": (790, 276, "middle"), "A009": (914, 94, "start"),
        "A033": (914, 144, "start"), "A045": (914, 194, "start"),
        "A042": (914, 244, "start"), "A086": (914, 294, "start"), "A070": (914, 344, "start"),
    }
    display_labels = {
        "LOCAL_RECIPIENTS": "冲绳地方受赠方",
        "USO_NATIONAL": "USO 全国组织",
        "DOD": "美国国防部（DoD）",
        "R8C01": "冲绳儒艮诉讼",
        "X008": "Red Cross Okinawa",
    }
    node_by_id = {str(row["node_id"]): row for row in nodes}
    def node_color(node_type: str) -> str:
        return {
            "service_actor": "#0f766e", "service_actor_unobservable": "#94a3b8",
            "s1_candidate": "#d97706", "accountability_actor": "#be185d",
            "system_interface": "#334155", "system_or_parent": "#475569",
            "case_endpoint": "#7c3aed", "recipient_cluster": "#ca8a04",
        }.get(node_type, "#64748b")

    lines = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1120" height="500" viewBox="0 0 1120 500" role="img" aria-labelledby="title desc">',
        '<title id="title">W2-D bounded typed egonet</title>',
        '<desc id="desc">Service-side internal relations and accountability-side case relations connect to a shared Department of Defense institutional interface, while no direct service-to-accountability organization edge is drawn.</desc>',
        '<defs><marker id="arrow-candidate" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#94a3b8"/></marker></defs>',
        '<rect width="1120" height="500" fill="#fffdf8"/>',
        '<text x="32" y="38" font-family="Arial,sans-serif" font-size="22" font-weight="700" fill="#172554">同一制度核心，不等于两套 NGO 已经相连</text>',
        '<text x="32" y="64" font-family="Arial,sans-serif" font-size="13" fill="#475569">2023–2025 tracer audit；实线=已核/官方结构，虚线=候选或历史；图中没有 S0→A0 组织桥</text>',
        '<text x="70" y="480" font-family="Arial,sans-serif" font-size="14" font-weight="700" fill="#0f766e">驻军服务／慈善侧</text>',
        '<text x="495" y="480" font-family="Arial,sans-serif" font-size="14" font-weight="700" fill="#334155">共同制度接口</text>',
        '<text x="850" y="480" font-family="Arial,sans-serif" font-size="14" font-weight="700" fill="#be185d">问责／倡议侧</text>',
    ]
    dashed_status = {"candidate", "candidate_partial", "historical_event_only", "historical_human_checked", "out_of_window"}
    for edge in edges:
        source = str(edge["source_node_id"]); target = str(edge["target_node_id"])
        if source not in positions or target not in positions:
            continue
        x1, y1 = positions[source]; x2, y2 = positions[target]
        candidate_service = edge["edge_status"] == "official_source_supported_candidate_pending_principal"
        dash = ' stroke-dasharray="6 5"' if edge["edge_status"] in dashed_status or candidate_service else ""
        stroke = "#94a3b8" if edge["edge_status"] in dashed_status or candidate_service else "#64748b"
        arrow = ' marker-end="url(#arrow-candidate)"' if edge["relation_family"] == "service_intermediation" else ""
        if edge["relation_family"] == "service_intermediation":
            # Keep the arrowhead outside the target node so direction remains visible.
            delta_x, delta_y = x2 - x1, y2 - y1
            length = (delta_x ** 2 + delta_y ** 2) ** 0.5
            x2 -= delta_x / length * 11
            y2 -= delta_y / length * 11
        lines.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="1.7"{dash}{arrow}/>' )
    for node_id, (x, y) in positions.items():
        node = node_by_id[node_id]
        color = node_color(str(node["node_type"]))
        label = escape(display_labels.get(node_id, str(node["label"])))
        lines.append(f'<circle cx="{x}" cy="{y}" r="7" fill="{color}"/>')
        label_x, label_y, anchor = label_positions[node_id]
        lines.append(
            f'<text x="{label_x}" y="{label_y}" text-anchor="{anchor}" '
            'font-family="Arial,sans-serif" font-size="11.5" fill="#1e293b" '
            'paint-order="stroke" stroke="#fffdf8" stroke-width="3" stroke-linejoin="round">'
            f'{label}</text>'
        )
    lines.extend([
        '<text x="270" y="347" text-anchor="middle" font-family="Arial,sans-serif" font-size="10.5" fill="#64748b" paint-order="stroke" stroke="#fffdf8" stroke-width="3">NMCRS→ARC（待审）</text>',
        '<rect x="470" y="82" width="330" height="44" rx="4" fill="#f1f5f9" stroke="#cbd5e1"/>',
        '<text x="635" y="100" text-anchor="middle" font-family="Arial,sans-serif" font-size="12" font-weight="700" fill="#334155">DoD 是共同制度端点</text>',
        '<text x="635" y="117" text-anchor="middle" font-family="Arial,sans-serif" font-size="11" fill="#475569">对 USO：全国 prime award；在儒艮案：被告／问责对象</text>',
        '<rect x="450" y="405" width="380" height="39" rx="4" fill="#fff7ed" stroke="#fdba74"/>',
        '<text x="640" y="421" text-anchor="middle" font-family="Arial,sans-serif" font-size="11" fill="#9a3412">这是一条“共同制度接口”，不是两家 NGO 的关系边</text>',
        '<text x="640" y="437" text-anchor="middle" font-family="Arial,sans-serif" font-size="10.5" fill="#9a3412">共享地点、同场和共同资助方也分别保留，不自动升级为联盟</text>',
        '</svg>',
    ])
    return "\n".join(lines) + "\n"


def build_claims(matrix: list[dict[str, object]]) -> list[dict[str, object]]:
    tracer_direct = [row for row in matrix if row["selection_frame_id"] == FRAME_TRACER and row["relation_family"] == "direct_organization_relation"]
    zero = sum(row["audit_result"] == "audited_public_record_zero" for row in tracer_direct)
    not_observed = sum(row["pair_observability"] == "not_observable_in_window" for row in tracer_direct)
    unresolved = len(tracer_direct) - zero
    claims = [
        ("direct_relation", "bounded_supported", f"S0×A0 的 54 个直接组织配对中，{zero} 个达到有界公开资料零；其余 {unresolved} 个仍因来源覆盖或同期可观察性不足而未决，其中 {not_observed} 个涉及 X017 的同期不可观察。", "bridge_audit_matrix_v1.csv", "可写‘在声明的 2023–2025 来源窗口中未确认直接组织关系’，不可写现实中不存在关系。"),
        ("shared_person", "unresolved", "现有 104 条军属申报角色、15 条 USO/赞助人物端点与已提取的 A0 人名之间没有身份闭合的跨侧同名人物。", "person_disambiguation_queue_v1.csv;negative_search_log_v1.csv", "人物披露结构不对称，不能写 shared-person zero 或做全网中心性。"),
        ("shared_recipient", "unresolved", "六个 AWWA recipient 候选中三项有地方侧回应，但没有一项闭合到同一金额与税期，也没有一项确认同时连接问责侧 actor。", "W2-A EH0110-EH0121", "不把地方福利 recipient 自动改成问责组织或桥。"),
        ("shared_funder", "not_testable_to_zero", "尚未确认共同资助方；Schedule B 匿名性和部分 Schedule I/资助方提取缺口使负面判断不可成立。", "source_family_actor_coverage_v1.csv", "未来若命中共同资助方，也只表示资源来源相交，不表示协调。"),
        ("same_event", "unresolved", "所审 2023–2025 记录没有确认 S0 与 A0 同一公开事件。", "negative_search_log_v1.csv", "事件材料不穷尽；共同出现也不升格为联盟。"),
        ("shared_place", "context_only", "中央 actor-place 表出现若干同地点编码，但缺少同一时间、行动或组织关系闭合。", "bridge_audit_matrix_v1.csv", "地点只作背景，绝不计入 bridge。"),
        (
            "system_interface", "bounded_supported",
            "DoD／WHS 是 USO 全国 prime award 的 awarding/funding agency，公开记录的累计 obligation 为 USD 72m；DoD 同时是儒艮诉讼中的被告／问责对象。这是同一驻军体系的共同制度端点。",
            "W2D-EG012;W2D-EG016;W2B-A024;R8C01",
            "这是系统接口，不是 USO Okinawa 与 Earthjustice/CBD/TIRN 的组织桥；USD 72m 是全国 award 的累计 obligation，不是现金支出或冲绳分配。",
        ),
        ("service_internal_structure", "bounded_with_pending_relation", "服务侧已确认 AWWA 伞状成员、反复输入与部分再分配；另有一条官方来源支持的有向候选：NMCRS 委托 ARC 提供非营业时段入口，并使用 NMCRS 资金，仍待负责人审定。", "W2-A/W2-B endpoint handoffs", "ARC—NMCRS 关系在审定前不得写成已确认服务中介；内部结构也不能自动解释政治立场、地方接受或合法性效果。"),
        ("ecology_screen", "exploratory_only", "S0×A1R 与 S0×A1C 的现行 typed-input screen 没有产生确认的跨侧组织桥，但没有完成逐 actor 的对称来源审计。", "relation_family_coverage_v1.csv", "不能把探索屏幕写成 41/36 actor 生态的零连接率。"),
        ("s1_status", "frame_gap", "Marine Thrift Shop 有充分的渠道 tracer 材料，但仍是 X018 admission/selection-frame 候选，不进入 S1 确认计数。", "W2-A handoff;integration plan hold", "不得用它悄悄扩充 S0/S1 分母。"),
    ]
    return [
        common(
            {
                "claim_id": f"W2D-CL{index:03d}",
                "claim_family": family,
                "claim_status": status,
                "proposed_claim": claim,
                "evidence_refs": refs,
                "interpretation_limit": limit,
                "principal_decision_needed": "yes" if family in {"direct_relation", "service_internal_structure"} or status in {"unresolved", "not_testable_to_zero", "frame_gap"} else "no",
            }
        )
        for index, (family, status, claim, refs, limit) in enumerate(claims, 1)
    ]


def build_principal_queue() -> list[dict[str, object]]:
    items = [
        ("direct_zero_wording", "Accept the 36 direct-pair bounded zeros for the wording 'no confirmed direct organization relation in the declared public-record window'?", "approve_bounded_wording", "If rejected, retain only 'no confirmed dyad in current typed inputs'."),
        ("w2a_person_pairs", "Resolve Brooke Epps/Epp, Jen Yapsing/Yapshing, Amber Tracy and Trinicia Kloepper identity pairs.", "review_all_four_cross_actor_candidates", "Until then they remain within-service candidates and never cross-ecology bridges."),
        ("a070_aliases", "Are VFP-ROCK, VFP ROC, Ryukyu/Okinawa Chapter Kokusai, Ryukyu-Okinawa Chapter and Chapter 1003 one continuous chapter identity?", "review_charter_or_official_roster", "Current official resolutions support events/roles but not full lineage."),
        ("shared_dod_interface", "Approve DoD as a system-interface node with different relation types, outside the six NGO-bridge counts?", "approve_separate_interface_layer", "Rejecting this removes the node from synthesis but does not alter underlying award/case facts."),
        ("x018_s1_frame", "Should Marine Thrift Shop X018 enter a newly versioned S1 frame?", "defer_until_actor_admission_and_frame_version", "Current W2-A tracer findings remain usable without changing the confirmatory denominator."),
        ("person_network_gate", "Person-role coverage is asymmetric. Keep W2-D at tracer egonet rather than full-network centrality?", "keep_tracer_only", "Full person centrality requires a separately approved coverage threshold and dated roles."),
        ("service_gaps", "Prioritize local/current rosters and financial reports for ARC Okinawa, NMCRS Okinawa and ACGO?", "target_x008_x009_x017", "These three actors account for the unresolved/not-observable direct-pair rows."),
        ("recipient_crosswalks", "Carry W2-A's six recipient identity/transaction questions into the principal review packet?", "yes_preserve_separate_decisions", "No recipient bridge or LEG2 strength should be upgraded here."),
        ("arc_nmcrs_direction", "Approve the directed candidate NMCRS→ARC after-hours service interface, with NMCRS funds and ARC acting on NMCRS's behalf?", "review_W2B2_DE028_as_directed_service_interface", "Until approved, keep the edge as official-source-supported candidate and do not call it confirmed service intermediation."),
    ]
    return [
        common(
            {
                "review_item_id": f"W2D-PR{index:03d}",
                "topic": topic,
                "question": question,
                "recommended_decision": recommendation,
                "impact_if_unresolved": impact,
                "priority": "P0" if index <= 5 else "P1",
                "decision_status": "principal_confirmed" if topic == "shared_dod_interface" else "principal_review_pending",
            }
        )
        for index, (topic, question, recommendation, impact) in enumerate(items, 1)
    ]


def build_principal_interpretive_overlay() -> list[dict[str, object]]:
    """Record the principal's synthesis decision without approving underlying fact rows."""
    return [
        {
            "decision_id": "W2D-ID001",
            "decision_date": "2026-08-23",
            "principal": "project_principal_user",
            "target_claim_id": "W2D-CL007",
            "decision_status": "principal_confirmed",
            "review_scope": "interpretive_position_only",
            "approved_position": "report_main_finding",
            "approved_wording": (
                "DoD／WHS 是 USO 全国 prime award 的 awarding/funding agency，公开记录的累计 obligation 为 USD 72m；"
                "DoD 同时是儒艮诉讼中的被告／问责对象。这是同一驻军体系的共同制度端点。"
            ),
            "evidence_refs": "W2D-EG012;W2D-EG016;W2B-A024;R8C01",
            "interpretation_limit": (
                "解释性升格不批准底层事实行，不把系统接口写成 NGO 桥、USO Okinawa 收款、全生态中心性或合法性效果。"
            ),
            "underlying_fact_rows_approved": "no",
            "underlying_fact_review_status": "unchanged",
            "w2f_status": "blocked",
            "w2g_status": "not_authorized",
            "package_scope": "research_only",
            "frontend_status": "not_frontend_ready",
            "central_writeback": "no",
        }
    ]


def build_source_receipts() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    index = 1
    seen = set()
    for actor_id, audit in A0_AUDIT.items():
        for family in SOURCE_FAMILIES:
            _, url, locator = audit[family]
            if not url.startswith("http") or url in seen:
                continue
            seen.add(url)
            filename = A0_URL_ARTIFACT.get(url, "")
            artifact = ART / filename if filename else None
            archived = bool(artifact and artifact.exists())
            rows.append(
                common(
                    {
                        "receipt_id": f"W2D-SR{index:03d}",
                        "publisher": actor_id,
                        "title": f"{actor_id} official {family}",
                        "source_family": family,
                        "url": url,
                        "retrieved_at": BUILD_DATE,
                        "artifact_path": str(artifact.relative_to(ROOT)).replace("\\", "/") if archived else "",
                        "sha256": sha256(artifact) if archived else "",
                        "mime_type": "application/pdf" if filename.endswith(".pdf") else "text/html",
                        "exact_locator": locator,
                        "supports_row_ids": actor_id,
                        "archive_status": "archived_local" if archived else "blocked_403_or_external_only",
                        "notes": "Official source; no central S-ID assigned.",
                    }
                )
            )
            index += 1

    internal = [
        ("W2-00 selection members", OUT.parent / "us_presence_network_wave2_w2_00_v1" / "selection_frame_actor_members_v1.csv"),
        ("W2-A endpoint handoff", OUT.parent / "us_presence_network_wave2_w2_a_v1" / "w2d_endpoint_handoff_v1.csv"),
        ("W2-B endpoint handoff", OUT.parent / "us_presence_network_wave2_w2_b_v1" / "w2_d_endpoint_candidates_v1.csv"),
        ("Wave1 accountability people", OUT.parent / "us_presence_accountability_recon_v1" / "person_role_observations_v1.csv"),
        ("Current typed relations", ROOT / "data" / "interim" / "15_funding_or_support_edges_sample_v0.csv"),
        ("Current actor-place", ROOT / "data" / "interim" / "08_actor_place_edges_initial_v0.csv"),
        ("Current actor-event", ROOT / "data" / "interim" / "09_actor_event_venue_edges_v0.csv"),
        ("W2-00 anchor ledger", OUT.parent / "us_presence_network_wave2_w2_00_v1" / "anchor_ledger_v1.csv"),
        ("W2-B federal award audit", OUT.parent / "us_presence_network_wave2_w2_b_v1" / "federal_award_allocation_audit_v1.csv"),
    ]
    for title, path in internal:
        exact_locator = "whole controlled input"
        supports_row_ids = "W2-D package"
        if title == "W2-00 anchor ledger":
            exact_locator = "rows W2B-A021;W2B-A022;W2B-A024;W2B-A026;W2B-A032"
            supports_row_ids = "W2D-EG012;W2D-CL007"
        elif title == "W2-B federal award audit":
            exact_locator = "row W2B2-FA001"
            supports_row_ids = "W2D-EG012"
        rows.append(
            common(
                {
                    "receipt_id": f"W2D-SR{index:03d}",
                    "publisher": "project_controlled_input",
                    "title": title,
                    "source_family": "internal_hashed_input",
                    "url": "",
                    "retrieved_at": BUILD_DATE,
                    "artifact_path": str(path.relative_to(ROOT)).replace("\\", "/"),
                    "sha256": sha256(path),
                    "mime_type": "text/csv",
                    "exact_locator": exact_locator,
                    "supports_row_ids": supports_row_ids,
                    "archive_status": "internal_hashed_reference",
                    "notes": "Referenced in place; source package remains immutable.",
                }
            )
        )
        index += 1
    return rows


def build_readme(counts: dict[str, int]) -> str:
    return f"""# W2-D Bridge audit v1

日期：2026-08-22  
状态：`research_only / W2D-CL007_interpretive_position_principal_confirmed / other_items_pending / not_frontend_ready`。

## 1. 审计对象与计数

- 深描 tracer：S0 9 个服务 actor × A0 6 个问责 actor × 6 类关系 = **324** 条 pair-family 审计行。
- 确认性生态屏幕：S0 9 × A1R 41 × 6 = **2,214** 条；只表示现行 typed inputs 的覆盖，不产生生态级零关系。
- 候选敏感性屏幕：S0 9 × A1C 36 × 6 = **1,944** 条；绝不升级 candidate actor-issue 事实。
- 总矩阵：**{counts['matrix']}** 条。
- 15 个 tracer × 5 个来源族 = **{counts['source_coverage']}** 条对称来源覆盖记录。
- 人物消歧队列 **{counts['person_queue']}** 条；负检索 **{counts['negative_search']}** 条；负责人判断 **{counts['principal_queue']}** 条。
- 通过 actor identity/function admission 且进入新版本选择框的 S1 actor 当前为 **0**。Marine Thrift Shop（X018）仍是 tracer/admission 候选。

## 2. 当前最强发现

### 直接组织关系：有界零，不是现实零

S0×A0 的 54 个直接组织配对中，**36 个**满足本轮 `audited_public_record_zero`：两端在 2023–2025 有活动锚点，A0 官方材料与服务侧 W2-A/W2-B corpus 已作对称名称／关系检索，没有确认命中。其余 18 个不进入零关系计数：X008/X009 的全国财务／roster 来源族不完整，X017 缺同期活动锚点。

因此可写：**“在声明的 2023–2025 公开资料窗口中，尚未确认两侧 actor 的直接组织关系。”** 不能写“两套生态现实中没有共享组织和人员”。

### 人物、recipient 与资助方仍是三种不同的缺口

- 现有提取人物没有 identity-resolved 的跨侧命中，但人物披露结构不对称，不能给 shared-person zero。
- W2-A 的六个 AWWA recipient 候选中三项有地方侧回应，零项闭合同一金额／税期，也没有确认问责侧端点。
- Schedule B 匿名性与部分 funder extraction 缺口，使“没有共同资助方”不可检验；未来即使命中，也只表示来源相交，不表示组织协调。

### 真正闭合的是共同制度接口

DoD／WHS 一边是 USO 全国 `HQ00342310002` prime award 的 awarding/funding agency，公开记录的 USD 72m 是全国 award 的累计 obligation；DoD 另一边是 Okinawa Dugong 诉讼的被告／问责对象。它说明两套组织生态围绕同一制度核心运作，但**不是 USO Okinawa 与 Earthjustice／CBD／TIRN 的组织桥**，也不能把全国 award 分配给冲绳或改写成现金支出。

2026-08-23，负责人已把 `W2D-CL007` 升为报告主发现。该决定只确认它在合成中的**解释性位置**：底层事实行及其审核状态不变，W2-F 仍 blocked，W2-G、中央写回和前端发布仍未授权。决定收据单独保存在 `principal_interpretive_overlay_v1.csv`。

服务侧另有一条官方来源支持、但尚未过负责人审定的有向候选：**NMCRS→ARC**。它表示 NMCRS 委托 ARC 在非营业时段提供入口，并使用 NMCRS 资金；审定前不写成已确认服务中介。

## 3. 关系语法

六类桥分别保存：直接组织、人物、recipient／中介、共同资助方、同一事件、同一地点。共享地点永不计 bridge；同场参与永不升联盟；共同资助方永不自动解释为协调。

`audited_public_record_zero` 只在 tracer frame 的直接组织关系中使用。A1R/A1C 仍是覆盖屏幕；没有经过逐 actor 对称来源审计的 pair 一律 `unresolved`。

## 4. 文件

| 文件 | 用途 |
|---|---|
| `bridge_audit_matrix_v1.csv` | 4,482 条 pair×关系族审计矩阵 |
| `actor_window_observability_v1.csv` | actor 在主窗口的可观察性与锚点 |
| `source_family_actor_coverage_v1.csv` | 15 tracer × 5 来源族 |
| `relation_family_coverage_v1.csv` | 三个 frame 的关系族覆盖摘要 |
| `person_disambiguation_queue_v1.csv` | 人物／拼写／别名人工消歧 |
| `negative_search_log_v1.csv` | no-hit、不可观察和结构性缺口 |
| `typed_egonet_nodes_v1.csv` / `typed_egonet_edges_v1.csv` | 不混关系类型的解释性 egonet 数据 |
| `fig_bounded_bridge_egonet_v1.svg` / `.png` | 共同制度接口与两侧内部关系图及 QA 预览 |
| `claim_table_v1.csv` | 可写／不可写的结论表 |
| `principal_review_queue_v1.csv` | 负责人判断队列 |
| `principal_interpretive_overlay_v1.csv` | W2D-CL007 的负责人解释性位置决定；不批准底层事实行 |
| `source_receipts_v1.csv` | 官方与内部输入的 URL／哈希收据 |
| `unexpected_findings_register_v1.csv` | 包内 `lead_only` 线索登记；本轮仅保留 19 列表头 |
| `validation_report_v1.json` / `manifest_v1.json` | 验证与文件清单 |

## 意外发现登记

本轮登记 **0 条**。`unexpected_findings_register_v1.csv` 只保留统一表头。以后如出现超出本包既定问题的观察，可以标为 `lead_only` 并沿单条线索追查最多三步，单包起点与跟进合计最多十条。这些记录不进入本包结论、中央事实、人工复核队列、publication snapshot 或前端。

## 6. 负责人当前需要决定

1. 是否接受 36 个 direct pair 的有界零措辞；
2. W2-A 四组跨组织姓名候选和 A070 chapter／人物别名；
3. **已决定（2026-08-23）**：DoD 作为独立 `system_interface` 层进入合成且不进入 bridge 计数；这是解释性位置决定，不改变底层事实审核；
4. X018 是否在 actor admission 后进入新版本 S1 frame；
5. 是否维持人物层 tracer egonet，而不做覆盖不足的全网中心性。
6. 是否按 `NMCRS→ARC` 批准非营业时段入口／资金方向；批准前保持 candidate。

## 7. 不得误读为

- 不是现实中“两套生态零连接”的证明；
- 不是人物网络、资助网络或 recipient 网络已经穷尽；
- 不是共享地点／同场／共同资助方自动构成组织联盟；
- 不是把 DoD award、诉讼角色或系统接口写成 NGO 间资金边；
- 负责人对 `W2D-CL007` 的解释性升格，不是对其底层 award／case 行的人工事实批准，也不解除 W2-F 阻断；
- 不是中央写回、publication adapter 或前端发布授权。

## 8. 复现

```powershell
python scripts/build_us_presence_network_wave2_w2_d_v1.py
python -m unittest tests.test_build_us_presence_network_wave2_w2_d_v1
python scripts/validate_research_work_package_v1.py outputs/us_presence_network_wave2_w2_d_v1
```
"""


def validate(
    s0: dict[str, str], a0: dict[str, str], a1r: dict[str, str], a1c: dict[str, str],
    matrix: list[dict[str, object]], source_audit: list[dict[str, object]],
    graph_edges: list[dict[str, object]], claims: list[dict[str, object]],
    principal: list[dict[str, object]], principal_overlay: list[dict[str, object]],
    receipts: list[dict[str, object]],
    protected_before: dict[str, str],
) -> dict[str, object]:
    edge_by_id = {str(row["edge_id"]): row for row in graph_edges}
    claim_by_id = {str(row["claim_id"]): row for row in claims}
    principal_by_id = {str(row["review_item_id"]): row for row in principal}
    receipt_by_title = {str(row["title"]): row for row in receipts}
    eg012_refs = set(str(edge_by_id["W2D-EG012"]["source_refs"]).split(";"))
    cl007_refs = set(str(claim_by_id["W2D-CL007"]["evidence_refs"]).split(";"))
    overlay = principal_overlay[0] if len(principal_overlay) == 1 else {}
    checks: dict[str, bool] = {
        "s0_exact_9": len(s0) == 9,
        "a0_exact_6": len(a0) == 6,
        "a1r_exact_41": len(a1r) == 41,
        "a1c_exact_36": len(a1c) == 36,
        "matrix_exact_4482": len(matrix) == 4482,
        "tracer_exact_324": sum(row["selection_frame_id"] == FRAME_TRACER for row in matrix) == 324,
        "a1r_exact_2214": sum(row["selection_frame_id"] == FRAME_A1R for row in matrix) == 2214,
        "a1c_exact_1944": sum(row["selection_frame_id"] == FRAME_A1C for row in matrix) == 1944,
        "source_audit_exact_75": len(source_audit) == 75,
        "six_relation_families_only": {str(row["relation_family"]) for row in matrix} == set(RELATION_FAMILIES),
        "audit_results_legal": all(row["audit_result"] in {"confirmed_bridge", "disproved_alias", "unresolved", "audited_public_record_zero"} for row in matrix),
        "review_status_legal": all(row["review_status"] in LEGAL_REVIEW_STATUSES for row in matrix + source_audit),
        "all_research_only": all(row["package_scope"] == "research_only" for row in matrix + source_audit),
        "all_not_frontend_ready": all(row["frontend_status"] == "not_frontend_ready" for row in matrix + source_audit),
        "no_central_writeback": all(row["central_writeback"] == "no" for row in matrix + source_audit),
        "no_confirmed_cross_ecology_bridge": not any(row["audit_result"] == "confirmed_bridge" for row in matrix),
        "audited_zero_only_tracer_direct": all(row["selection_frame_id"] == FRAME_TRACER and row["relation_family"] == "direct_organization_relation" for row in matrix if row["audit_result"] == "audited_public_record_zero"),
        "audited_zero_both_observable": all(row["pair_observability"] == "both_endpoints_observed_in_window" for row in matrix if row["audit_result"] == "audited_public_record_zero"),
        "audited_zero_exact_36": sum(row["audit_result"] == "audited_public_record_zero" for row in matrix) == 36,
        "shared_place_never_bridge": all(row["audit_result"] != "confirmed_bridge" for row in matrix if row["relation_family"] == "shared_place_background"),
        "shared_funder_never_coordination": all("coordination" not in str(row["reason"]).lower() for row in matrix if row["relation_family"] == "shared_funder_or_sponsor"),
        "graph_no_direct_s0_a0_actor_edge": not any(row["counts_as_cross_ecology_actor_bridge"] == "yes" for row in graph_edges),
        "dod_interface_not_bridge": all(row["counts_as_cross_ecology_actor_bridge"] == "no" for row in graph_edges if "DOD" in {row["source_node_id"], row["target_node_id"]}),
        "eg012_uses_award_anchors_not_form990_revenue": (
            "W2B2-FA001" in eg012_refs
            and {"W2B-A021", "W2B-A022", "W2B-A024", "W2B-A026", "W2B-A032"}.issubset(eg012_refs)
            and "W2B-A006" not in eg012_refs
        ),
        "cl007_evidence_chain_exact": cl007_refs == {"W2D-EG012", "W2D-EG016", "W2B-A024", "R8C01"},
        "pr004_only_principal_confirmed": (
            principal_by_id.get("W2D-PR004", {}).get("decision_status") == "principal_confirmed"
            and all(
                row["decision_status"] == "principal_review_pending"
                for row in principal
                if row["review_item_id"] != "W2D-PR004"
            )
        ),
        "principal_overlay_interpretive_only": (
            len(principal_overlay) == 1
            and overlay.get("target_claim_id") == "W2D-CL007"
            and overlay.get("decision_status") == "principal_confirmed"
            and overlay.get("review_scope") == "interpretive_position_only"
            and overlay.get("approved_position") == "report_main_finding"
            and overlay.get("underlying_fact_rows_approved") == "no"
            and overlay.get("underlying_fact_review_status") == "unchanged"
            and overlay.get("w2f_status") == "blocked"
            and overlay.get("w2g_status") == "not_authorized"
            and overlay.get("package_scope") == "research_only"
            and overlay.get("frontend_status") == "not_frontend_ready"
            and overlay.get("central_writeback") == "no"
        ),
        "award_input_receipts_hashed_and_scoped": (
            receipt_by_title.get("W2-00 anchor ledger", {}).get("supports_row_ids") == "W2D-EG012;W2D-CL007"
            and receipt_by_title.get("W2-B federal award audit", {}).get("supports_row_ids") == "W2D-EG012"
            and all(
                receipt_by_title.get(title, {}).get("sha256")
                for title in ("W2-00 anchor ledger", "W2-B federal award audit")
            )
        ),
        "receipt_hashes_valid": all((not row["artifact_path"]) or sha256(ROOT / str(row["artifact_path"])) == row["sha256"] for row in receipts),
        "protected_files_unchanged": all(sha256(Path(path)) == digest for path, digest in protected_before.items()),
    }
    return {
        "status": "PASS_RESEARCH_ONLY_W2_D" if all(checks.values()) else "FAIL",
        "build_date": BUILD_DATE,
        "counts": {
            "s0": len(s0), "a0": len(a0), "a1r": len(a1r), "a1c": len(a1c),
            "s1_confirmatory": 0, "matrix_rows": len(matrix), "source_family_rows": len(source_audit),
            "audited_public_record_zero_rows": sum(row["audit_result"] == "audited_public_record_zero" for row in matrix),
            "confirmed_cross_ecology_bridge_rows": sum(row["audit_result"] == "confirmed_bridge" for row in matrix),
        },
        "checks": checks,
        "scope": "research_only_no_central_no_adapter_no_frontend",
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    protected_before = {str(path): sha256(path) for path in PROTECTED}
    s0, a0, a1r, a1c = get_frame_members()
    activity = build_activity_status(s0, a0, a1r, a1c)
    source_audit = build_source_family_audit(s0, a0)
    matrix = build_bridge_matrix(s0, a0, a1r, a1c, activity)
    person_queue = build_person_queue()
    negatives = build_negative_search_log()
    coverage = build_relation_family_coverage(matrix)
    graph_nodes, graph_edges = build_graph()
    claims = build_claims(matrix)
    principal = build_principal_queue()
    principal_overlay = build_principal_interpretive_overlay()
    receipts = build_source_receipts()

    write_csv(OUT / "actor_window_observability_v1.csv", [
        "activity_row_id", "actor_id", "actor_name", "analytical_groups", "window_start", "window_end",
        "activity_status", "activity_anchor_refs", "activity_anchor_basis", "interpretation_limit",
        "review_status", "package_scope", "frontend_status", "central_writeback",
    ], activity)
    write_csv(OUT / "source_family_actor_coverage_v1.csv", [
        "coverage_row_id", "actor_id", "actor_name", "analytical_side", "source_family", "window_start", "window_end",
        "coverage_status", "source_ref_or_url", "exact_locator_or_result", "s0_name_hit", "completion_semantics",
        "allowed_claim", "prohibited_inference", "review_status", "package_scope", "frontend_status", "central_writeback",
    ], source_audit)
    write_csv(OUT / "bridge_audit_matrix_v1.csv", [
        "matrix_row_id", "selection_frame_id", "frame_role", "service_actor_id", "service_actor_name",
        "accountability_actor_id", "accountability_actor_name", "relation_family", "window_start", "window_end",
        "service_activity_status", "accountability_activity_status", "pair_observability", "source_coverage_status",
        "observed_endpoint_refs", "audit_result", "screening_disposition", "reason", "allowed_claim",
        "prohibited_inference", "review_status", "package_scope", "frontend_status", "central_writeback",
    ], matrix)
    write_csv(OUT / "person_disambiguation_queue_v1.csv", [
        "disambiguation_id", "candidate_scope", "name_a", "actor_a", "name_b", "actor_b", "period_a_or_joint",
        "period_b", "source_refs", "candidate_type", "current_decision", "cross_ecology_bridge_eligibility",
        "principal_question", "allowed_claim", "prohibited_inference", "review_status", "package_scope",
        "frontend_status", "central_writeback",
    ], person_queue)
    write_csv(OUT / "negative_search_log_v1.csv", [
        "search_id", "subject", "source_scope", "query_or_match_rule", "search_date", "bounded_result",
        "allowed_claim", "prohibited_inference", "review_status", "package_scope", "frontend_status", "central_writeback",
    ], negatives)
    write_csv(OUT / "relation_family_coverage_v1.csv", [
        "coverage_id", "selection_frame_id", "relation_family", "service_actor_count", "accountability_actor_count",
        "pair_count", "observable_pair_count", "confirmed_bridge_count", "audited_public_record_zero_count",
        "unresolved_count", "shared_place_context_count", "coverage_summary", "interpretation_limit", "review_status",
        "package_scope", "frontend_status", "central_writeback",
    ], coverage)
    write_csv(OUT / "typed_egonet_nodes_v1.csv", [
        "node_id", "label", "node_type", "selection_status", "review_status", "package_scope", "frontend_status", "central_writeback",
    ], graph_nodes)
    write_csv(OUT / "typed_egonet_edges_v1.csv", [
        "edge_id", "source_node_id", "target_node_id", "relation_family", "edge_status", "source_refs",
        "direction_semantics", "counts_as_cross_ecology_actor_bridge", "interpretation_limit", "review_status", "package_scope",
        "frontend_status", "central_writeback",
    ], graph_edges)
    (OUT / "fig_bounded_bridge_egonet_v1.svg").write_text(render_graph_svg(graph_nodes, graph_edges), encoding="utf-8")
    write_csv(OUT / "claim_table_v1.csv", [
        "claim_id", "claim_family", "claim_status", "proposed_claim", "evidence_refs", "interpretation_limit",
        "principal_decision_needed", "review_status", "package_scope", "frontend_status", "central_writeback",
    ], claims)
    write_csv(OUT / "principal_review_queue_v1.csv", [
        "review_item_id", "topic", "question", "recommended_decision", "impact_if_unresolved", "priority",
        "decision_status", "review_status", "package_scope", "frontend_status", "central_writeback",
    ], principal)
    write_csv(OUT / "principal_interpretive_overlay_v1.csv", [
        "decision_id", "decision_date", "principal", "target_claim_id", "decision_status", "review_scope",
        "approved_position", "approved_wording", "evidence_refs", "interpretation_limit",
        "underlying_fact_rows_approved", "underlying_fact_review_status", "w2f_status", "w2g_status",
        "package_scope", "frontend_status", "central_writeback",
    ], principal_overlay)
    write_csv(OUT / "source_receipts_v1.csv", [
        "receipt_id", "publisher", "title", "source_family", "url", "retrieved_at", "artifact_path", "sha256",
        "mime_type", "exact_locator", "supports_row_ids", "archive_status", "notes", "review_status", "package_scope",
        "frontend_status", "central_writeback",
    ], receipts)
    write_csv(
        OUT / "unexpected_findings_register_v1.csv",
        unexpected_findings_fields(),
        [],
    )

    counts = {
        "matrix": len(matrix), "source_coverage": len(source_audit), "person_queue": len(person_queue),
        "negative_search": len(negatives), "principal_queue": len(principal),
    }
    (OUT / "README.md").write_text(build_readme(counts), encoding="utf-8")
    validation = validate(
        s0, a0, a1r, a1c, matrix, source_audit, graph_edges, claims,
        principal, principal_overlay, receipts, protected_before,
    )
    (OUT / "validation_report_v1.json").write_text(json.dumps(validation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    manifest_files = [path for path in OUT.rglob("*") if path.is_file() and path.name != "manifest_v1.json"]
    manifest = {
        "package": "us_presence_network_wave2_w2_d_v1",
        "generated_at": BUILD_DATE,
        "scope": "research_only_no_central_no_adapter_no_frontend",
        "files": [
            {"path": str(path.relative_to(ROOT)).replace("\\", "/"), "sha256": sha256(path), "bytes": path.stat().st_size}
            for path in sorted(manifest_files)
        ],
    }
    (OUT / "manifest_v1.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(validation, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
