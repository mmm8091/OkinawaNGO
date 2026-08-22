from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "us_presence_network_wave2_w2_b_v1"
ART = OUT / "artifacts"
UNEXPECTED_TEMPLATE = ROOT / "data" / "metadata" / "unexpected_findings_register_template_v1.csv"

REVIEW_STATUS = "ai_seeded"
PACKAGE_SCOPE = "research_only"
FRONTEND_STATUS = "not_frontend_ready"
CENTRAL_WRITEBACK = "no"
BUILD_DATE = "2026-08-22"

LEGAL_REVIEW_STATUSES = {
    "ai_seeded",
    "human_checked",
    "human_revised",
    "needs_second_source",
    "needs_local_retrieval",
    "rejected",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_csv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for raw in rows:
            row = {field: raw.get(field, "") for field in fields}
            writer.writerow(row)


def write_empty_unexpected_findings_register() -> None:
    """Create the package-local lead-only register with the canonical 19 columns."""
    with UNEXPECTED_TEMPLATE.open(encoding="utf-8-sig", newline="") as handle:
        fields = csv.DictReader(handle).fieldnames or []
    if len(fields) != 19:
        raise ValueError(f"unexpected-findings template must have 19 columns, got {len(fields)}")
    write_csv(OUT / "unexpected_findings_register_v1.csv", fields, [])


def split_ids(value: object) -> list[str]:
    return [item.strip() for item in str(value or "").replace("|", ";").split(";") if item.strip()]


def common(row: dict[str, object]) -> dict[str, object]:
    return {
        **row,
        "review_status": REVIEW_STATUS,
        "package_scope": PACKAGE_SCOPE,
        "frontend_status": FRONTEND_STATUS,
        "central_writeback": CENTRAL_WRITEBACK,
    }


RECEIPT_FIELDS = [
    "receipt_id",
    "publisher",
    "title",
    "source_family",
    "url",
    "retrieved_at",
    "artifact_path",
    "sha256",
    "mime_type",
    "exact_locator",
    "supports_row_ids",
    "archive_status",
    "notes",
    "review_status",
    "package_scope",
    "frontend_status",
    "central_writeback",
]

HIERARCHY_FIELDS = [
    "row_id",
    "observation_date",
    "period_semantics",
    "parent_level",
    "parent_name",
    "child_level",
    "child_name",
    "site_type",
    "location",
    "operating_status",
    "quantity",
    "quantity_unit",
    "source_receipt_ids",
    "exact_locator",
    "allowed_claim",
    "prohibited_inference",
    "review_status",
    "package_scope",
    "frontend_status",
    "central_writeback",
    "notes",
]

CAPACITY_FIELDS = [
    "observation_id",
    "actor_or_unit",
    "site_or_scope",
    "observation_date",
    "period_semantics",
    "metric",
    "value",
    "value_text",
    "unit",
    "service_family",
    "beneficiary_or_partner",
    "geography",
    "source_receipt_ids",
    "exact_locator",
    "allowed_claim",
    "prohibited_inference",
    "review_status",
    "package_scope",
    "frontend_status",
    "central_writeback",
    "notes",
]

SPONSOR_FIELDS = [
    "flow_id",
    "source_name",
    "target_name",
    "scope",
    "flow_type",
    "amount",
    "value_text",
    "currency",
    "date_start",
    "date_end",
    "period_semantics",
    "purpose",
    "in_kind_detail",
    "sponsor_tier",
    "source_receipt_ids",
    "exact_locator",
    "existing_crosswalk",
    "claim_status",
    "prohibited_inference",
    "review_status",
    "package_scope",
    "frontend_status",
    "central_writeback",
    "notes",
]

FEDERAL_FIELDS = [
    "audit_id",
    "layer",
    "record_type",
    "metric",
    "value",
    "value_text",
    "currency",
    "period",
    "geography_or_endpoint",
    "source_receipt_ids",
    "exact_locator",
    "status",
    "semantic_conflict_id",
    "allowed_claim",
    "prohibited_inference",
    "review_status",
    "package_scope",
    "frontend_status",
    "central_writeback",
    "notes",
]

BOUNDARY_FIELDS = [
    "boundary_id",
    "function_family",
    "uso_status",
    "uso_evidence",
    "arc_status",
    "arc_evidence",
    "nmcrs_status",
    "nmcrs_evidence",
    "geographic_scope",
    "relation_or_boundary",
    "claim_status",
    "source_receipt_ids",
    "exact_locator",
    "allowed_claim",
    "prohibited_inference",
    "review_status",
    "package_scope",
    "frontend_status",
    "central_writeback",
    "notes",
]

WATERFALL_FIELDS = [
    "stage_order",
    "stage_id",
    "lane",
    "stage_label",
    "organizational_level",
    "known_amount",
    "value_text",
    "currency",
    "period",
    "measurement_type",
    "visibility_status",
    "source_receipt_ids",
    "reason_not_additive",
    "next_gap",
    "allowed_claim",
    "review_status",
    "package_scope",
    "frontend_status",
    "central_writeback",
]

NEGATIVE_FIELDS = [
    "search_id",
    "question",
    "source_scope",
    "search_date",
    "result",
    "gap_type",
    "source_receipt_ids",
    "next_best_material",
    "allowed_claim",
    "prohibited_inference",
    "review_status",
    "package_scope",
    "frontend_status",
    "central_writeback",
]

CHANGE_FIELDS = [
    "change_note_id",
    "topic",
    "original_assumption",
    "failure_reason",
    "revised_approach",
    "affected_row_ids",
    "source_receipt_ids",
    "effect_on_numbers",
    "effect_on_claims",
    "principal_decision_requirement",
    "decision_status",
    "review_status",
    "package_scope",
    "frontend_status",
    "central_writeback",
]

PRINCIPAL_FIELDS = [
    "decision_id",
    "decision_type",
    "question",
    "recommended_decision",
    "alternative_or_competing_explanation",
    "affected_row_ids",
    "source_receipt_ids",
    "what_this_unlocks",
    "principal_decision",
    "principal_note",
    "principal_reviewer",
    "principal_decision_date",
    "status",
    "review_status",
    "package_scope",
    "frontend_status",
    "central_writeback",
]

W2D_ENDPOINT_FIELDS = [
    "endpoint_id",
    "endpoint_type",
    "canonical_label",
    "registry_or_provisional_id",
    "linked_actor_or_endpoint",
    "person_name_raw",
    "role_or_relation_type",
    "observed_start",
    "observed_end",
    "time_semantics",
    "source_receipt_ids",
    "exact_locator",
    "identity_status",
    "bridge_eligibility",
    "w2_d_use",
    "allowed_claim",
    "prohibited_inference",
    "review_status",
    "package_scope",
    "frontend_status",
    "central_writeback",
    "notes",
]


def source_receipts() -> list[dict[str, object]]:
    reused = ROOT / "outputs" / "us_presence_network_wave2_w2_00_uso_v1" / "artifacts"
    archive = ROOT / "source_docs" / "source_archive"
    specs = [
        ("W2B2-SR001", "United Service Organizations", "2024 Global Impact Report", "official_impact_report", "https://myimpact.uso.org/wp-content/uploads/sites/95/2025/08/USO-Impact-Report.pdf", reused / "uso_2024_global_impact_report.pdf", "application/pdf", "pp.12-14 impact counts; pp.26-27 Indo-Pacific narrative", "W2B2-HS001;W2B2-SC005;W2B2-SC006;W2B2-SC007", "reused_w2_00_frozen"),
        ("W2B2-SR002", "United Service Organizations", "USO Okinawa homepage and current directory", "official_website", "https://okinawa.uso.org/", reused / "uso_okinawa_homepage.html", "text/html", "Locations, Programs and Sponsors sections", "W2B2-HS004;W2B2-HS005;W2B2-HS006;W2B2-HS007;W2B2-HS008;W2B2-HS009;W2B2-HS010;W2B2-HS011;W2B2-HS012;W2B2-SC008;W2B2-SP001;W2B2-SP002;W2B2-SP003;W2B2-SP004;W2B2-SP005;W2B2-SP006", "reused_w2_00_frozen"),
        ("W2B2-SR003", "United Service Organizations", "Volunteer Spotlight: USO Okinawa", "official_website", "https://pacific.uso.org/stories/800", reused / "uso_pacific_volunteer_spotlight_okinawa.html", "text/html", "Published 2025-04-24; paragraph beginning 'The USO Okinawa team'", "W2B2-HS004;W2B2-SC001;W2B2-SC002;W2B2-SC003", "reused_w2_00_frozen"),
        ("W2B2-SR004", "United Service Organizations", "Scott P. Maskery, Regional Vice President", "official_website", "https://pacific.uso.org/about/scott-p-maskery-regional-vice-president", reused / "uso_pacific_regional_vp.html", "text/html", "First biography paragraph", "W2B2-HS002", "reused_w2_00_frozen"),
        ("W2B2-SR005", "United Service Organizations", "USO Japan homepage and location directory", "official_website", "https://japan.uso.org/", reused / "uso_japan_homepage.html", "text/html", "Site title, locations and Japan Area Office", "W2B2-HS003", "reused_w2_00_frozen"),
        ("W2B2-SR006", "USAspending.gov", "Award overview API: ASST_NON_HQ00342310002_097", "official_federal_award_api", "https://api.usaspending.gov/api/v2/awards/ASST_NON_HQ00342310002_097/", reused / "usaspending_award_overview.json", "application/json", "JSON root: total_obligation, period_of_performance, recipient, place_of_performance, cfda_info", "W2B2-FA001;W2B2-FA002;W2B2-FA003;W2B2-FA018;W2B2-FA019;W2B2-WF001", "reused_w2_00_frozen"),
        ("W2B2-SR007", "USAspending.gov", "Award transaction history API response", "official_federal_award_api", "https://api.usaspending.gov/api/v2/transactions/", reused / "usaspending_transactions_response.json", "application/json", "$.results, five award actions", "W2B2-FA004;W2B2-FA005;W2B2-FA006;W2B2-FA007;W2B2-FA008", "reused_w2_00_frozen"),
        ("W2B2-SR008", "USAspending.gov", "Bounded subaward search for FAIN HQ00342310002", "official_federal_award_api", "https://api.usaspending.gov/api/v2/search/spending_by_award/", reused / "usaspending_subawards_response.json", "application/json", "$.results and $.page_metadata", "W2B2-FA016;W2B2-FA017", "reused_w2_00_frozen"),
        ("W2B2-SR009", "United Service Organizations", "USO Okinawa Recognizes Service Members of the Year", "official_website", "https://okinawa.uso.org/stories/123", ART / "uso_okinawa_story_2021_service_salute.html", "text/html", "Paragraph naming seven Okinawa locations and ten outreach sites; event identifies 2021 honorees", "W2B2-HS013;W2B2-HS014", "local_frozen_research_only"),
        ("W2B2-SR010", "United Service Organizations", "Here For Those Who Serve: How USO Okinawa Centers Are Uplifting Units Across The Island", "official_website", "https://pacific.uso.org/stories/1097", ART / "uso_pacific_story_center_service_examples.html", "text/html", "Published 2025-07-10; opening six-center statement and six center subsections", "W2B2-HS017;W2B2-SC009;W2B2-SC010;W2B2-SC011;W2B2-SC012;W2B2-SC013;W2B2-SC014;W2B2-FB006", "local_frozen_research_only"),
        ("W2B2-SR011", "United Service Organizations", "USO Okinawa Furthers Support of Soldiers During Milestone Birthday", "official_website", "https://pacific.uso.org/stories/998", ART / "uso_pacific_okinawa_outreach_torii.html", "text/html", "Published 2025-06-13; six physical-center statement and Torii/White Beach outreach paragraphs", "W2B2-HS015;W2B2-HS016;W2B2-HS017;W2B2-SC015", "local_frozen_research_only"),
        ("W2B2-SR012", "United Service Organizations", "USO Schwab Welcomes UDP Volunteer and Family", "official_website", "https://okinawa.uso.org/stories/130", ART / "uso_okinawa_schwab_volunteers.html", "text/html", "Published 2022-09-30; opening paragraph", "W2B2-SC004", "local_frozen_research_only"),
        ("W2B2-SR013", "United Service Organizations", "AEC latest USD 16,000 donation and Futenma center refresh", "official_website", "https://okinawa.uso.org/stories/336", ART / "uso_okinawa_aec_2025_16000.html", "text/html", "Published 2025-11-25; donation ceremony dated 2025-11-17", "W2B2-SP013;W2B2-SP014;W2B2-WF006;W2B2-WF007", "local_frozen_research_only"),
        ("W2B2-SR014", "United Service Organizations", "AEC Continues Support of USO Okinawa", "official_website", "https://okinawa.uso.org/stories/129", ART / "uso_okinawa_aec_18000.html", "text/html", "Published 2024-10-16; single article body", "W2B2-SP011;W2B2-HS005;W2B2-HS006;W2B2-HS007;W2B2-HS008;W2B2-HS009;W2B2-HS010", "local_frozen_research_only"),
        ("W2B2-SR015", "United Service Organizations", "AK Kogyo: Proud supporter of USO Okinawa", "official_website", "https://okinawa.uso.org/stories/171", ART / "uso_okinawa_ak_kogyo_1000000jpy.html", "text/html", "Published 2025-03-12; first body paragraph", "W2B2-SP012;W2B2-WF006", "local_frozen_research_only"),
        ("W2B2-SR016", "United Service Organizations", "Over a Decade of Support: Thank you Mediatti Broadband Communications", "official_website", "https://okinawa.uso.org/stories/468", ART / "uso_okinawa_mbc_12_years.html", "text/html", "Published 2026-02-24; paragraph on 12 consecutive years and cash/in-kind support", "W2B2-SP016;W2B2-SP017;W2B2-WF007", "local_frozen_research_only"),
        ("W2B2-SR017", "United Service Organizations", "Mediatti Broadband Communications makes USD 40K USO donation", "official_website", "https://okinawa.uso.org/stories/56", ART / "uso_okinawa_mbc_2018_40000.html", "text/html", "Published 2018-02-09; page title and body", "W2B2-SP007", "local_frozen_research_only"),
        ("W2B2-SR018", "United Service Organizations", "American Engineering Corporation makes USD 18K donation", "official_website", "https://okinawa.uso.org/stories/57", ART / "uso_okinawa_aec_2018_18000.html", "text/html", "Published 2018-03-01; first body paragraph", "W2B2-SP008", "local_frozen_research_only"),
        ("W2B2-SR019", "United Service Organizations", "CHUBB Insurance Japan makes one million yen donation", "official_website", "https://okinawa.uso.org/stories/58", ART / "uso_okinawa_chubb_1000000jpy.html", "text/html", "Published 2018-03-15; page title and body", "W2B2-SP009", "local_frozen_research_only"),
        ("W2B2-SR020", "American Red Cross", "Overseas Military Community Support", "official_website", "https://www.redcross.org/get-help/military-families/overseas-military-community-support.html", ART / "redcross_overseas_military_support.html", "text/html", "Service sections and Typhoon Khanun Okinawa mission example", "W2B2-FB001;W2B2-FB002;W2B2-FB003;W2B2-FB004;W2B2-FB006;W2B2-FB007;W2B2-FB009", "local_frozen_research_only"),
        ("W2B2-SR021", "American Red Cross", "Volunteer with Red Cross Service to the Armed Forces", "official_website", "https://www.redcross.org/volunteer/become-a-volunteer/service-to-the-armed-forces.html", ART / "redcross_armed_forces_volunteer.html", "text/html", "Opening program description and volunteer role list", "W2B2-FB003;W2B2-FB006", "local_frozen_research_only"),
        ("W2B2-SR022", "Navy-Marine Corps Relief Society", "Okinawa, Japan office", "official_website", "https://www.nmcrs.org/locations/okinawa-japan", ART / "nmcrs_okinawa_location.html", "text/html", "Contact, available services, nearby Camp Hansen and after-hours liaison callout", "W2B2-FB003;W2B2-FB004;W2B2-FB005;W2B2-FB007;W2B2-FB008;W2B2-FB010", "local_frozen_research_only"),
        ("W2B2-SR023", "Navy-Marine Corps Relief Society", "Get help", "official_website", "https://www.nmcrs.org/get-help", ART / "nmcrs_get_help.html", "text/html", "After-hours FAQ and financial-assistance/education sections", "W2B2-FB003;W2B2-FB004;W2B2-FB005;W2B2-FB007;W2B2-FB008", "local_frozen_research_only"),
        ("W2B2-SR024", "Navy-Marine Corps Relief Society", "Annual reports and financials", "official_website", "https://www.nmcrs.org/about-us/annual-reports-financials", ART / "nmcrs_annual_reports_financials.html", "text/html", "Corporate documents paragraph: private donations and no Department of Defense funds", "W2B2-FB004;W2B2-FB005", "local_frozen_research_only"),
        ("W2B2-SR025", "USAspending.gov", "Award Federal Account Funding API response", "official_federal_award_api", "https://api.usaspending.gov/api/v2/awards/funding/", ART / "usaspending_funding_response.json", "application/json", "POST request frozen beside response; $.results", "W2B2-FA011;W2B2-FA012;W2B2-FA013;W2B2-FA014;W2B2-FA015;W2B2-WF002", "local_frozen_research_only"),
        ("W2B2-SR026", "USAspending.gov", "Award Federal Account Funding Rollup API response", "official_federal_award_api", "https://api.usaspending.gov/api/v2/awards/funding_rollup/", ART / "usaspending_funding_rollup_response.json", "application/json", "POST request frozen beside response; JSON root", "W2B2-FA009;W2B2-WF002", "local_frozen_research_only"),
        ("W2B2-SR027", "USAspending.gov", "Award Federal Accounts API response", "official_federal_award_api", "https://api.usaspending.gov/api/v2/awards/accounts/", ART / "usaspending_accounts_response.json", "application/json", "POST request frozen beside response; $.results[0]", "W2B2-FA010;W2B2-WF002", "local_frozen_research_only"),
        ("W2B2-SR028", "USAspending API", "Award Funding endpoint contract", "official_api_documentation", "https://github.com/fedspendingtransparency/usaspending-api/blob/master/usaspending_api/api_contracts/contracts/v2/awards/funding.md", ART / "usaspending_api_contract_funding.md", "text/markdown", "AwardFundingResponse field definitions", "W2B2-FA011;W2B2-FA012;W2B2-FA013;W2B2-FA014;W2B2-FA015", "local_frozen_research_only"),
        ("W2B2-SR029", "USAspending API", "Award Funding Rollup endpoint contract", "official_api_documentation", "https://github.com/fedspendingtransparency/usaspending-api/blob/master/usaspending_api/api_contracts/contracts/v2/awards/funding_rollup.md", ART / "usaspending_api_contract_funding_rollup.md", "text/markdown", "Response field definition", "W2B2-FA009", "local_frozen_research_only"),
        ("W2B2-SR030", "USAspending API", "Award Federal Accounts endpoint contract", "official_api_documentation", "https://github.com/fedspendingtransparency/usaspending-api/blob/master/usaspending_api/api_contracts/contracts/v2/awards/accounts.md", ART / "usaspending_api_contract_accounts.md", "text/markdown", "AccountListing field definitions", "W2B2-FA010", "local_frozen_research_only"),
        ("W2B2-SR031", "U.S. Naval Hospital Okinawa", "Volunteer/Red Cross", "official_military_health_page", "https://okinawa.tricare.mil/About-Us/Employment-Opportunities/Volunteer-Red-Cross", None, "text/html", "Page text found through official index; direct archive returned HTTP 403 on 2026-08-22", "W2B2-FB006;W2B2-FB010", "blocked_403_logged"),
        ("W2B2-SR032", "Stars and Stripes Okinawa", "OESC donates USD 3,250 to USO Okinawa", "military_community_news", "https://okinawa.stripes.com/community-news/okinawa-enlisted-spouses-club-uso-okinawa.html", archive / "S053" / "raw.html", "text/html", "Article title and dated donation paragraph", "W2B2-SP015;W2B2-WF006", "reused_central_archive_secondary"),
        ("W2B2-SR033", "United Service Organizations", "AWWA grant to USO Kinser kitchen refresh", "official_website", "https://okinawa.uso.org/stories/81", archive / "S077" / "raw.html", "text/html", "August 2020 grant story; amount not stated", "W2B2-SP010", "reused_central_archive_official"),
        ("W2B2-SR034", "United Service Organizations", "2024 audited consolidated financial statements", "official_audited_financial_statement", "https://www.uso.org/document/513", reused / "uso_2024_financial_statement.pdf", "application/pdf", "p.8, Consolidated Statement of Functional Expenses, Year ended December 31, 2024, Program Services Total column (table in thousands of dollars): Functional expenses, gross 204,912; Note: In-kind expenses included in expenses listed above (105,538); Functional expenses, net 99,374", "W2B2-WF009;W2B2-WF010;W2B2-WF011", "reused_w2_00_frozen"),
    ]
    rows = []
    for receipt_id, publisher, title, family, url, artifact, mime, locator, supports, status in specs:
        artifact_path = ""
        artifact_hash = ""
        if artifact is not None:
            artifact_path = artifact.relative_to(ROOT).as_posix()
            if not artifact.exists():
                raise FileNotFoundError(artifact)
            artifact_hash = sha256(artifact)
        rows.append(
            common(
                {
                    "receipt_id": receipt_id,
                    "publisher": publisher,
                    "title": title,
                    "source_family": family,
                    "url": url,
                    "retrieved_at": "2026-08-22T09:00:00Z",
                    "artifact_path": artifact_path,
                    "sha256": artifact_hash,
                    "mime_type": mime,
                    "exact_locator": locator,
                    "supports_row_ids": supports,
                    "archive_status": status,
                    "notes": "Research receipt only; it does not create a central source ID or approve a central relation.",
                }
            )
        )
    return rows


def hierarchy_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(row_id: str, date: str, semantics: str, parent_level: str, parent: str, child_level: str, child: str, site_type: str, location: str, status: str, quantity: object, unit: str, receipts: str, locator: str, allowed: str, prohibited: str, notes: str = "") -> None:
        rows.append(common({
            "row_id": row_id, "observation_date": date, "period_semantics": semantics,
            "parent_level": parent_level, "parent_name": parent, "child_level": child_level,
            "child_name": child, "site_type": site_type, "location": location,
            "operating_status": status, "quantity": quantity, "quantity_unit": unit,
            "source_receipt_ids": receipts, "exact_locator": locator,
            "allowed_claim": allowed, "prohibited_inference": prohibited, "notes": notes,
        }))

    add("W2B2-HS001", "2024-12-31", "annual_report_footprint", "region", "USO Indo-Pacific", "footprint", "mainland Japan; Okinawa; South Korea; Guam; Hawaii", "permanent_location_geographies", "Indo-Pacific", "reported", 5, "named_geographies", "W2B2-SR001", "Impact report pp.26-27", "The 2024 report identifies five geographies with permanent Indo-Pacific locations.", "Do not infer center counts, budgets or equal allocation from this footprint.")
    add("W2B2-HS002", "2026-08-21", "current_biography_snapshot", "region", "USO Indo-Pacific", "center_network", "Alaska; Hawaii; Guam; mainland Japan; Okinawa; Korea", "regional_center_network", "Indo-Pacific", "reported", 24, "centers", "W2B2-SR004", "First biography paragraph", "A current USO biography describes a 24-center regional network across six named geographies.", "Do not reconcile the 24 centers to country totals without an annual site roster.")
    add("W2B2-HS003", "2026-08-21", "current_directory_snapshot", "region", "USO Indo-Pacific", "area", "USO Japan", "mainland_japan_area", "mainland Japan", "listed", "", "", "W2B2-SR005", "Site title and Japan Area Office", "USO Japan is a sibling area/site system under the Indo-Pacific region.", "Do not merge mainland USO Japan with USO Okinawa.")
    add("W2B2-HS004", "2026-08-21", "current_directory_snapshot", "region", "USO Indo-Pacific", "area", "USO Okinawa", "okinawa_area", "Okinawa", "listed", 8, "directory_entries", "W2B2-SR002", "Homepage Locations section and Area Office entry", "The current directory has 8 entries: six centers + one terminal entry + one area office.", "Do not call the 8 directory entries eight sites or eight centers, and do not infer lifecycle change or separate legal entities.")
    centers = [
        ("W2B2-HS005", "USO Camp Foster", "Camp Foster"),
        ("W2B2-HS006", "USO Camp Hansen", "Camp Hansen"),
        ("W2B2-HS007", "USO Camp Kinser", "Camp Kinser"),
        ("W2B2-HS008", "USO Camp Schwab", "Camp Schwab"),
        ("W2B2-HS009", "USO Futenma", "MCAS Futenma"),
        ("W2B2-HS010", "USO Kadena", "Kadena Air Base"),
    ]
    for row_id, child, location in centers:
        add(row_id, "2026-08-21", "current_directory_and_2025_narrative", "area", "USO Okinawa", "site", child, "operating_center", location, "listed", 1, "center", "W2B2-SR002;W2B2-SR003", "Current directory and 2025 six-physical-center statement", "This is one of the six named operating centers.", "Do not assign a center-level budget, service count or separate法人格.")
    add("W2B2-HS011", "2026-08-21", "current_directory_snapshot", "area", "USO Okinawa", "site", "USO Kadena AMC Terminal", "transport_terminal_presence", "Kadena Air Base", "listed", 1, "presence", "W2B2-SR002", "Homepage locations section", "The AMC terminal is a separately listed presence in the current directory.", "Do not add it to the six operating-center count.")
    add("W2B2-HS012", "2026-08-21", "current_directory_snapshot", "area", "USO Okinawa", "office", "USO Okinawa Area Office", "administrative_area_office", "Okinawa", "listed", 1, "office", "W2B2-SR002", "Homepage locations and contact sections", "The area office is an administrative presence.", "Do not count the area office as a public service center.")
    add("W2B2-HS013", "2021-12-31", "event_year_site_vocabulary", "area", "USO Okinawa", "listed_location_set", "Schwab; Hansen; Kadena; Kadena Air Terminal; Foster; Futenma; Kinser", "historical_location_set", "Okinawa", "reported", 7, "listed_locations", "W2B2-SR009", "Final paragraph", "A 2021-event story lists 7 listed locations, including Kadena Air Terminal.", "Do not relabel these as seven homogeneous operating centers or infer opening, closure, dissolution or any other lifecycle change.")
    add("W2B2-HS014", "2021-12-31", "event_year_outreach_vocabulary", "area", "USO Okinawa", "outreach_set", "Torii Station; White Beach; Camp Courtney; Camp McTureous; Camp Lester; Fort Buckner; Plaza Housing; Ie Shima; Camp Shields; Jungle Warfare Training Center", "historical_outreach_sites", "Okinawa", "reported", 10, "named_outreach_sites", "W2B2-SR009", "Final paragraph", "The same story names ten outreach sites outside its 7 listed locations.", "Outreach does not establish a permanent center or continuous annual activity at every site.")
    add("W2B2-HS015", "2025-06-06", "dated_outreach_event", "area", "USO Okinawa", "outreach_site", "Torii Station", "outreach_without_dedicated_center", "Torii Station", "event_confirmed", 1, "event_site", "W2B2-SR011", "Torii Station paragraph", "USO Okinawa explicitly described Torii as lacking a dedicated center while receiving outreach.", "Do not turn the event into a permanent site or infer annual volume.")
    add("W2B2-HS016", "2025-06-13", "current_story_outreach_statement", "area", "USO Okinawa", "outreach_site", "White Beach Naval Facility", "outreach_without_directory_center", "White Beach", "reported", "", "", "W2B2-SR011", "Ongoing outreach paragraph", "The 2025 story identifies staff/volunteer travel to White Beach as outreach.", "Do not infer frequency, staffing or budget.")
    add("W2B2-HS017", "2025-07-10", "dated_2025_center_count", "area", "USO Okinawa", "center_count", "Foster; Hansen; Kinser; Schwab; Futenma; Kadena", "historical_physical_center_count", "Okinawa", "reported", 6, "physical_centers", "W2B2-SR010;W2B2-SR011", "SR010 opening paragraph ('six centers'); SR011 opening paragraph ('six physical locations')", "The selected 2025 official stories describe 6 physical centers.", "Do not compare this count with 2021 or the current directory to infer opening, closure, dissolution or any other lifecycle change.")
    return rows


def capacity_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(observation_id: str, actor: str, site: str, date: str, semantics: str, metric: str, value: object, value_text: str, unit: str, family: str, beneficiary: str, geography: str, receipts: str, locator: str, allowed: str, prohibited: str, notes: str = "") -> None:
        rows.append(common({
            "observation_id": observation_id, "actor_or_unit": actor, "site_or_scope": site,
            "observation_date": date, "period_semantics": semantics, "metric": metric,
            "value": value, "value_text": value_text, "unit": unit, "service_family": family,
            "beneficiary_or_partner": beneficiary, "geography": geography,
            "source_receipt_ids": receipts, "exact_locator": locator,
            "allowed_claim": allowed, "prohibited_inference": prohibited, "notes": notes,
        }))

    add("W2B2-SC001", "USO Okinawa", "area", "2025-04-24", "current_story_snapshot", "employees", 21, "21 employees", "people", "staff_capacity", "USO Okinawa operations", "Okinawa", "W2B2-SR003", "Paragraph beginning 'The USO Okinawa team'", "USO reported 21 employees in the April 2025 snapshot.", "Do not infer full-time equivalents, payroll or annual staffing continuity.")
    add("W2B2-SC002", "USO Okinawa", "area", "2025-04-24", "current_service_population_statement", "supported_population_scale", 47000, "approximately 47,000 service members and their families", "people_approximate", "service_population", "service members and families", "Okinawa", "W2B2-SR003", "Same paragraph", "The 2025 USO self-reported service-coverage scale for USO Okinawa was approximately 47,000 service members and their families.", "This self-reported service-coverage scale is not a population denominator; do not treat it as annual unique users, service uses, visits, a census or an allocation weight.")
    add("W2B2-SC003", "USO Okinawa", "area", "2025-04-24", "current_story_snapshot", "volunteers", 780, "780 plus volunteers", "people_minimum_reported", "volunteer_capacity", "USO Okinawa operations", "Okinawa", "W2B2-SR003", "Same paragraph", "USO reported an area volunteer force of more than 780.", "Do not infer volunteer hours, active-at-one-time roster or unique annual volunteers.")
    add("W2B2-SC004", "USO Camp Schwab", "Camp Schwab", "2022-09-30", "organization_general_annual_statement", "volunteers_onboarded_annually", 100, "around one hundred annually", "people_approximate", "volunteer_turnover", "mostly Unit Deployment Program personnel", "Camp Schwab", "W2B2-SR012", "Opening paragraph", "USO Camp Schwab described onboarding around 100 volunteers annually, mostly short-tour UDP personnel.", "Do not add this to the 780-area snapshot or infer a stable 100-person roster.")
    add("W2B2-SC005", "United Service Organizations", "global", "2024-12-31", "annual_impact_metric", "program_or_service_uses", 11300000, "more than 11.3 million", "uses_minimum_reported", "global_program_delivery", "military community", "134 countries", "W2B2-SR001", "Impact report 2024 metrics", "The global report records more than 11.3 million program/service uses.", "Do not convert uses into unique people or allocate them to Okinawa.")
    add("W2B2-SC006", "United Service Organizations", "global", "2024-12-31", "annual_impact_metric", "center_visits", 7200000, "more than 7.2 million", "visits_minimum_reported", "center_access", "military community", "global", "W2B2-SR001", "Impact report 2024 metrics", "The global report records more than 7.2 million center visits.", "Do not substitute visits for uses or unique people, and do not allocate to Okinawa.")
    add("W2B2-SC007", "United Service Organizations", "global", "2024-12-31", "annual_impact_metric", "people_reached", 950000, "more than 950,000", "people_minimum_reported", "global_reach", "military community", "global", "W2B2-SR001", "Impact report 2024 metrics", "The global report records more than 950,000 people reached/provided programs.", "Do not use this as an Okinawa denominator or equate it with visits/uses.")
    add("W2B2-SC008", "USO Okinawa", "current website", "2026-08-21", "current_program_menu_snapshot", "program_families", 5, "Transitions; Reading; Gaming; Canine; Coffee Connections", "named_programs", "program_menu", "service members and families", "Okinawa", "W2B2-SR002", "Programs section", "The current local site exposes five named program families.", "The menu does not supply local participant counts, expense allocation or annual continuity.")
    add("W2B2-SC009", "USO Kadena", "Kadena", "2025-07-10", "selected_story_episode", "people_supported_in_episode", 70, "70 members", "people", "travel_disruption_support", "repatriation mission team and 733rd Air Mobility Squadron", "Kadena", "W2B2-SR010", "USO Kadena subsection", "A selected episode records pizza and snack bags for 70 stranded team members.", "Do not interpret this as annual site volume or unique users.")
    add("W2B2-SC010", "USO Kinser", "Camp Kinser", "2025-07-10", "selected_story_episode", "event_participants_exposed_to_support", 2500, "more than 2,500", "people_minimum_reported", "hydration_and_event_support", "3D Marine Logistics Group field meet", "Camp Kinser", "W2B2-SR010", "USO Kinser subsection", "A selected event reports more than 2,500 attendees and USO hydration/snack support.", "Do not count every attendee as a distinct service recipient or annual total.")
    add("W2B2-SC011", "USO Schwab", "Jungle Warfare Training Center", "2025-07-10", "selected_story_episode", "people_supported_in_episode", 204, "204 plus other Marines stationed at JWTC", "people_minimum_reported", "field_morale_and_hydration", "Marines and Navy Corpsmen", "Camp Gonsalves/JWTC", "W2B2-SR010", "USO Schwab subsection", "A selected field-support episode names 204 members plus locally stationed Marines.", "Do not infer total event size or annual outreach volume.")
    add("W2B2-SC012", "USO Foster", "U.S. Naval Hospital Okinawa", "2025-07-10", "selected_story_episode", "nurses_in_episode", 104, "104 military and Okinawa Nurses Association nurses", "people_combined_total", "workforce_appreciation", "military nurses and Okinawa Nurses Association nurses", "Camp Foster", "W2B2-SR010", "USO Foster subsection", "A selected episode reports coffee/pastries delivered to a combined group of 104 nurses.", "Do not split the 104 between military and association members or infer organizational partnership continuity.")
    add("W2B2-SC013", "USO Futenma", "MCAS Futenma", "2025-07-10", "selected_story_episode", "service_members_supported", 400, "more than 400", "people_minimum_reported", "predeployment_support", "VMM-265 service members", "MCAS Futenma", "W2B2-SR010", "USO Futenma subsection", "A selected predeployment episode reports snacks/drinks for more than 400 service members.", "Do not infer annual site users or operational effect.")
    add("W2B2-SC014", "USO Hansen", "Camp Hansen", "2025-07-10", "selected_story_episode", "event_participants", 1000, "more than 1,000", "people_minimum_reported", "bilateral_field_event_support", "U.S. military and Japan Ground Self-Defense Force engineers", "Camp Hansen", "W2B2-SR010", "USO Hansen subsection", "A selected field event brought together more than 1,000 U.S. and JGSDF engineers with USO support.", "Do not infer a durable interorganizational alliance, participant identity or attitude effect.")
    add("W2B2-SC015", "USO Okinawa", "Torii Station", "2025-06-06", "selected_outreach_episode", "dedicated_center", 0, "no dedicated USO center", "binary_site_status", "outreach", "U.S. Army community", "Torii Station", "W2B2-SR011", "Torii Station paragraph", "The event demonstrates service delivery beyond the six physical centers.", "Do not use food-item quantities as an annual service total or create a permanent Torii center.")
    return rows


def sponsor_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(flow_id: str, source: str, target: str, scope: str, flow_type: str, amount: object, value_text: str, currency: str, start: str, end: str, semantics: str, purpose: str, in_kind: str, tier: str, receipts: str, locator: str, crosswalk: str, claim_status: str, prohibited: str, notes: str = "") -> None:
        rows.append(common({
            "flow_id": flow_id, "source_name": source, "target_name": target,
            "scope": scope, "flow_type": flow_type, "amount": amount, "value_text": value_text,
            "currency": currency, "date_start": start, "date_end": end,
            "period_semantics": semantics, "purpose": purpose, "in_kind_detail": in_kind,
            "sponsor_tier": tier, "source_receipt_ids": receipts, "exact_locator": locator,
            "existing_crosswalk": crosswalk, "claim_status": claim_status,
            "prohibited_inference": prohibited, "notes": notes,
        }))

    current = [
        ("W2B2-SP001", "Matson", "USO Indo-Pacific", "regional", "Mission Partner"),
        ("W2B2-SP002", "University of Maryland Global Campus", "USO Indo-Pacific", "regional", "Mission Partner"),
        ("W2B2-SP003", "AIG Auto Insurance", "USO Indo-Pacific", "regional", "Community Partner"),
        ("W2B2-SP004", "Mediatti Broadband Communications", "USO Okinawa", "local_area", "Platinum Sponsor"),
        ("W2B2-SP005", "American Engineering Corporation", "USO Okinawa", "local_area", "Silver Sponsor"),
        ("W2B2-SP006", "Billabong", "USO Okinawa", "local_area", "Bronze Sponsor"),
    ]
    for row_id, source, target, scope, tier in current:
        add(row_id, source, target, scope, "current_sponsor_roster", "", "amount not stated", "", "2026-08-21", "2026-08-21", "current_page_snapshot", "general sponsorship", "", tier, "W2B2-SR002", "Sponsors section", "", "official_current_roster_bounded", "Sponsor tier does not disclose amount, start date, governance or political position.")
    add("W2B2-SP007", "Mediatti Broadband Communications Okinawa", "USO Okinawa", "local_area", "cash_sponsorship", 40000, "USD 40,000", "USD", "2018-02-09", "2018-02-09", "dated_publication_and_2018_sponsorship", "2018 sponsorship", "", "", "W2B2-SR017", "Page title and first body paragraph", "", "official_self_report_exact_amount", "Do not treat this as a recurring annual amount or add it to another year.")
    add("W2B2-SP008", "American Engineering Corporation", "USO Okinawa", "local_area", "cash_sponsorship", 18000, "USD 18,000", "USD", "2018-03-01", "2018-03-01", "dated_2018_sponsorship", "Service Salute, Color Run and Kadena golf event", "", "Silver Sponsorship", "W2B2-SR018", "First body paragraph", "", "official_self_report_exact_amount", "This is distinct from the 2024 USD 18,000 story; identical amounts must not be deduplicated solely by value.")
    add("W2B2-SP009", "CHUBB Insurance Japan", "USO Okinawa", "local_area", "cash_donation", 1000000, "JPY 1,000,000", "JPY", "2018-03-15", "2018-03-15", "dated_donation", "general USO mission", "", "", "W2B2-SR019", "Page title and body", "", "official_self_report_exact_amount", "Do not convert currency without an explicit rate/date or infer recurring support.")
    add("W2B2-SP010", "American Welfare & Works Association", "USO Kinser", "center_project", "grant_or_project_support", "", "amount not stated", "", "2020-08-01", "2020-08-31", "month_bounded_story", "indoor/outdoor kitchen refresh", "project materials/support not itemized", "", "W2B2-SR033", "August 2020 grant story", "S077; existing research relation", "official_self_report_no_amount", "Do not infer the full AWWA grant program, amount or annual continuity.")
    add("W2B2-SP011", "American Engineering Corporation", "USO Okinawa", "local_area", "cash_sponsorship", 18000, "USD 18,000", "USD", "2024-10-16", "2024-10-16", "publication_date_snapshot", "general center and program support", "", "Silver Sponsorship", "W2B2-SR014", "Single article body", "", "official_self_report_exact_amount", "Do not merge with the separate 2018 USD 18,000 sponsorship.")
    add("W2B2-SP012", "AK Kogyo", "USO Okinawa", "local_area", "cash_donation", 1000000, "JPY 1,000,000", "JPY", "2025-03-12", "2025-03-12", "publication_date_snapshot", "center operations and outreach", "", "Proud Supporter", "W2B2-SR015", "First body paragraph", "", "official_self_report_exact_amount", "Do not convert currency or infer an annual series from the statement of support since 2020.")
    add("W2B2-SP013", "American Engineering Corporation", "USO Okinawa", "local_area", "cash_sponsorship", 16000, "USD 16,000", "USD", "2025-11-17", "2025-11-17", "ceremony_date", "six-center programming and services", "", "Silver Sponsorship", "W2B2-SR013", "Donation ceremony paragraph", "F002; S098 amount corroboration", "official_self_report_exact_amount", "Do not treat the sponsorship level as an additional amount.")
    add("W2B2-SP014", "American Engineering Corporation", "USO Futenma", "center_project", "in_kind_facility_support", "", "amount not stated", "", "2025-01-01", "2025-11-17", "story_year_project", "Futenma center refresh", "facility refresh completed by AEC", "", "W2B2-SR013", "Donation ceremony and project paragraphs", "F002 project context", "official_self_report_in_kind_no_amount", "Do not price the refresh or add it to the USD 16,000 cash donation.")
    add("W2B2-SP015", "Okinawa Enlisted Spouses' Club", "USO Okinawa", "local_area", "cash_donation", 3250, "USD 3,250", "USD", "2025-12-02", "2025-12-02", "dated_secondary_report", "general USO Okinawa support", "", "", "W2B2-SR032", "Article title and dated donation", "F021; S053", "existing_reviewed_flow_secondary_source", "Do not use this secondary report to infer a recurring annual pattern.")
    add("W2B2-SP016", "Mediatti Broadband Communications", "USO Okinawa", "local_area", "cash_sponsorship", "", "financial contributions; amount not stated", "", "2026-02-24", "2026-02-24", "current_story_snapshot", "center connectivity and operations", "", "Platinum Sponsor", "W2B2-SR016", "Paragraph on financial and in-kind contributions", "", "official_self_report_no_amount", "Do not infer an amount from sponsor tier or the 2018 USD 40,000 flow.")
    add("W2B2-SP017", "Mediatti Broadband Communications", "USO Okinawa", "local_area", "in_kind_connectivity", "", "amount not stated", "", "2026-02-24", "2026-02-24", "current_story_snapshot", "center connectivity", "high-speed WiFi; HD cable; technical support; fiber network management", "Platinum Sponsor", "W2B2-SR016", "Paragraphs following 12-year statement", "", "official_self_report_in_kind_no_amount", "Do not monetize in-kind services or treat a 12-year self-description as a complete annual ledger.")
    return rows


def federal_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(audit_id: str, layer: str, record_type: str, metric: str, value: object, value_text: str, currency: str, period: str, endpoint: str, receipts: str, locator: str, status: str, conflict: str, allowed: str, prohibited: str, notes: str = "") -> None:
        rows.append(common({
            "audit_id": audit_id, "layer": layer, "record_type": record_type,
            "metric": metric, "value": value, "value_text": value_text,
            "currency": currency, "period": period, "geography_or_endpoint": endpoint,
            "source_receipt_ids": receipts, "exact_locator": locator, "status": status,
            "semantic_conflict_id": conflict, "allowed_claim": allowed,
            "prohibited_inference": prohibited, "notes": notes,
        }))

    conflict = "USO_SAME_AWARD_PARALLEL_REPORTING_VIEWS_72M_41_21246329M"
    add("W2B2-FA001", "award", "award_overview", "total_obligation", 72000000, "USD 72,000,000", "USD", "2023-09-30/2028-09-29", "DoD/WHS -> United Service Organizations, Inc.", "W2B2-SR006", "$.total_obligation; $.recipient", "official_award_level", conflict, "The award-level cumulative obligation is USD 72 million to the national prime recipient.", "Do not call it cash paid, expenditure, Indo-Pacific allocation or USO Okinawa funding.")
    add("W2B2-FA002", "award", "place_of_performance", "place_of_performance", "", "United States / MULTI-STATE", "", "award overview current", "USA/MULTI-STATE", "W2B2-SR006", "$.place_of_performance", "official_award_level", "", "The public award record codes place of performance as U.S. multi-state.", "This field neither proves nor disproves overseas use within USO's internal program operations.")
    add("W2B2-FA003", "award", "assistance_listing", "applicant_and_beneficiary_eligibility", "", "generic organization eligibility; no award-specific geography", "", "current catalog text", "Assistance Listing 12.599", "W2B2-SR006", "$.cfda_info[0].applicant_eligibility and beneficiary_eligibility", "official_generic_program_field", "", "The catalog text supplies generic applicant/beneficiary categories, not a Japan/Okinawa allocation rule.", "Do not convert generic eligibility into an overseas eligible-geography finding.")
    transactions = [
        ("W2B2-FA004", "2023-07-14", "NEW", "0", 24000000, "program services description"),
        ("W2B2-FA005", "2024-02-13", "REVISION", "P00001", 0, "zero-dollar revision"),
        ("W2B2-FA006", "2024-05-28", "REVISION", "P00002", 0, "zero-dollar revision"),
        ("W2B2-FA007", "2024-07-26", "CONTINUATION", "P00003", 24000000, "exercises option one"),
        ("W2B2-FA008", "2025-07-31", "CONTINUATION", "P00004", 24000000, "USO support to members of the military"),
    ]
    for audit_id, date, action, mod, amount, description in transactions:
        add(audit_id, "transaction_history", "award_action", "federal_action_obligation", amount, f"USD {amount:,.0f}", "USD", date, f"USO, Inc.; modification {mod}", "W2B2-SR007", f"$.results[action_date={date}]", "official_transaction_history", conflict, f"The transaction history reports a {action.lower()} action of USD {amount:,.0f}.", "Do not infer action-level geography, cash outlay or Okinawa share.", description)
    add("W2B2-FA009", "federal_account_reporting", "funding_rollup", "total_transaction_obligated_amount", 41212463.29, "USD 41,212,463.29", "USD", "reporting records through FY2024 in retrieved endpoint", "same award; one funding/awarding agency and one federal account", "W2B2-SR026;W2B2-SR029", "JSON root", "official_same_award_account_reporting_view", conflict, "For the same award, the account-linked reporting view reports USD 41.21246329m in transaction obligations for its reporting perimeter.", "Do not relabel this as a second award, the award total, cash paid, a downstream funding stage or an amount available to Okinawa.")
    add("W2B2-FA010", "federal_account_reporting", "account_listing", "account_linked_obligation", 41212463.29, "USD 41,212,463.29", "USD", "retrieved current", "same award; 097-0100 Operation and Maintenance, Defense-Wide, Defense", "W2B2-SR027;W2B2-SR030", "$.results[0]", "official_same_award_account_linked_record", conflict, "The parallel account-reporting view associates the same award with federal account 097-0100.", "Do not infer a separate award, a sequential money-flow stage or a geographic program allocation.")
    funding = [
        ("W2B2-FA011", "2023/FY month 12", "transaction_obligated_amount", 24000000, "USD 24,000,000"),
        ("W2B2-FA012", "2024/FY month 6", "gross_outlay_amount", 7611993.84, "USD 7,611,993.84"),
        ("W2B2-FA013", "2024/FY month 9", "gross_outlay_amount", 6787536.71, "USD 6,787,536.71"),
        ("W2B2-FA014", "2024/FY month 9", "transaction_obligated_amount", -6787536.71, "USD -6,787,536.71"),
        ("W2B2-FA015", "2024/FY month 12", "transaction_obligated_amount", 24000000, "USD 24,000,000"),
    ]
    for audit_id, period, metric, amount, text in funding:
        add(audit_id, "federal_account_reporting", "periodic_funding_record", metric, amount, text, "USD", period, "097-0100; object class 41.0; program activity 0004", "W2B2-SR025;W2B2-SR028", f"$.results[{period}; {metric}]", "official_periodic_account_record", conflict, "This is one typed periodic account-reporting record.", "Do not sum gross-outlay snapshots across periods or equate periodic account records with transaction-history actions.")
    add("W2B2-FA016", "subaward", "award_overview", "subaward_count", 0, "0", "count", "retrieved current", "prime award", "W2B2-SR006", "$.subaward_count", "bounded_official_zero", "", "The award overview reports zero subawards.", "Zero public subawards does not mean zero internal allocation, procurement, reimbursement or interoffice transfer.")
    add("W2B2-FA017", "subaward", "bounded_search", "matching_subaward_rows", 0, "0", "rows", "2023-01-01/2026-12-31", "FAIN HQ00342310002", "W2B2-SR008", "$.results", "bounded_search_empty", "", "The saved bounded search returned no public subaward rows.", "Do not generalize the empty result beyond this public subaward data route and period.")
    add("W2B2-FA018", "regional_allocation", "negative_allocation_result", "Japan_IndoPacific_Okinawa_allocation", "", "not disclosed in inspected award/transaction/account/subaward fields", "", "award period and current records", "Indo-Pacific / Japan / Okinawa", "W2B2-SR006;W2B2-SR007;W2B2-SR008;W2B2-SR025;W2B2-SR026;W2B2-SR027", "Cross-endpoint audit", "allocation_layer_missing", conflict, "The public award chain closes at USO, Inc. and does not disclose a regional or Okinawa amount.", "Do not estimate a local share by centers, population, uses or equal division.")
    add("W2B2-FA019", "award", "period_of_performance", "performance_period", "", "2023-09-30 to 2028-09-29", "date_range", "2023-09-30/2028-09-29", "national prime award", "W2B2-SR006", "$.period_of_performance", "official_award_level", "", "The award record gives a five-year performance period.", "Do not call the USD 72 million an annual budget.")
    return rows


def boundary_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(boundary_id: str, family: str, uso_status: str, uso: str, arc_status: str, arc: str, nm_status: str, nm: str, geography: str, relation: str, receipts: str, locator: str, allowed: str, prohibited: str, notes: str = "") -> None:
        rows.append(common({
            "boundary_id": boundary_id, "function_family": family,
            "uso_status": uso_status, "uso_evidence": uso,
            "arc_status": arc_status, "arc_evidence": arc,
            "nmcrs_status": nm_status, "nmcrs_evidence": nm,
            "geographic_scope": geography, "relation_or_boundary": relation,
            "claim_status": "official_source_supported_candidate_pending_principal" if boundary_id == "W2B2-FB005" else "observation_ai_seeded",
            "source_receipt_ids": receipts, "exact_locator": locator,
            "allowed_claim": allowed, "prohibited_inference": prohibited, "notes": notes,
        }))

    none = "not_observed_in_selected_official_scope"
    add("W2B2-FB001", "morale_connection_center_hospitality", "direct", "Six centers, outreach, snacks, connectivity and morale programming.", "partial_overlap", "Overseas care packages and wellness support are described, but not a USO-style center network.", none, "No comparable center-hospitality function listed on the Okinawa location page.", "Okinawa and overseas military settings", "overlap_with_distinct_delivery_models", "W2B2-SR002;W2B2-SR010;W2B2-SR020;W2B2-SR022", "USO program/location pages; Red Cross care packages; NMCRS available services", "USO's distinctive observed infrastructure is a center/outreach network; Red Cross has narrower overlapping morale/wellness services.", "Do not interpret unobserved functions as proof an organization never performs them.")
    add("W2B2-FB002", "transition_and_career_support", "direct", "Current USO menu includes Transitions and sponsor stories mention transition assistance.", "direct_adjacent", "Overseas career-enhancement health-profession training is described.", "adjacent", "Education assistance and financial education are described, not the same transition program.", "overseas military communities", "adjacent_not_identical", "W2B2-SR002;W2B2-SR020;W2B2-SR023", "Program menus", "All three can address transition-related needs through different instruments.", "Do not collapse distinct programs into a shared organization or stable partnership.")
    add("W2B2-FB003", "emergency_communications_and_after_hours_access", none, "No emergency-family-communication role located in the selected USO materials.", "direct", "Emergency communications are a core Service to the Armed Forces function.", "handoff_to_arc", "The Okinawa office directs after-hours users to the Red Cross.", "global and Okinawa", "formal_after_hours_handoff", "W2B2-SR020;W2B2-SR021;W2B2-SR022;W2B2-SR023", "Emergency Communications and after-hours callouts", "The Red Cross is the after-hours communication/access interface for NMCRS assistance.", "Do not code USO as part of this handoff from co-location or common beneficiaries.")
    add("W2B2-FB004", "emergency_financial_assistance", none, "No direct emergency-loan/grant function located in selected USO sources.", "direct_event", "The Okinawa Red Cross response reports more than USD 82,000 in Typhoon Khanun financial assistance.", "direct", "Okinawa lists interest-free loans/grants, emergency travel and disaster relief.", "Okinawa", "overlap_with_different_funding_mechanisms", "W2B2-SR020;W2B2-SR022;W2B2-SR023;W2B2-SR024", "Typhoon example and NMCRS assistance menu", "Both Red Cross and NMCRS provide financial assistance, with different programs and funding provenance.", "Do not treat the Red Cross aggregate as a grant to an Okinawan NGO or NMCRS money unless the liaison condition applies.")
    add("W2B2-FB005", "after_hours_nmcrs_financial_liaison", none, "No role observed.", "delegated_after_hours_intake_and_disbursement", "ARC acts as the non-business-hours intake/disbursement interface delegated by NMCRS.", "delegating_program_and_fund_source", "NMCRS delegates the after-hours intake/disbursement function to ARC; ARC acts on NMCRS's behalf using NMCRS funds.", "Okinawa and global after-hours access", "directed_nmcrs_to_arc_after_hours_intake_disbursement_delegation", "W2B2-SR022;W2B2-SR023;W2B2-SR024", "NMCRS Okinawa after-hours callout and Get Help after-hours FAQ; corporate funding paragraph", "NMCRS delegates after-hours intake/disbursement to ARC; ARC acts on NMCRS's behalf using NMCRS funds. Official sources support this candidate; principal review remains pending.", "Do not code the delegation as an interorganizational grant, joint grant, merger, affiliation or political alliance.", "Status is official_source_supported_candidate_pending_principal; NMCRS also states it receives no Department of Defense funds.")
    add("W2B2-FB006", "hospital_and_health_setting_support", "episode", "USO Foster delivered coffee/pastries to 104 military and Okinawa Nurses Association nurses.", "direct_local_program", "The Naval Hospital page says Red Cross manages the hospital volunteer program; overseas page describes hospital visitation.", none, "No Okinawa hospital program identified on the selected location page.", "U.S. Naval Hospital Okinawa / Camp Foster", "shared_setting_different_functions", "W2B2-SR010;W2B2-SR020;W2B2-SR021;W2B2-SR031", "USO Foster episode; Hospital Visitation; TRICARE page (archive blocked 403)", "USO and Red Cross appear in the same hospital setting through different bounded activities.", "Shared setting is not an organizational relationship; the USO event is not the Red Cross volunteer program.")
    add("W2B2-FB007", "disaster_and_critical_event_support", none, "No disaster-relief function identified in selected USO materials.", "direct", "The Okinawa response distributed kits and financial assistance after Typhoon Khanun.", "direct", "Okinawa lists Disaster & Critical Event Relief.", "Okinawa", "parallel_functions_with_possible_after_hours_handoff", "W2B2-SR020;W2B2-SR022;W2B2-SR023", "Disaster Support and available services", "Red Cross and NMCRS both have observed disaster-support functions.", "Do not infer that they co-managed the Typhoon Khanun response without a source-specific relation.")
    add("W2B2-FB008", "financial_education_and_household_budgeting", none, "No household financial-education program identified in selected local menu.", none, "No matching financial-education program identified in selected overseas page.", "direct", "Budget for Baby and Money Ops are listed.", "Okinawa / eligible Navy-Marine community", "distinct_nmcrs_function", "W2B2-SR022;W2B2-SR023", "Available services and financial education section", "Financial education is a distinct observed NMCRS function in this comparison.", "Do not infer absence from organizations whose selected pages do not list the function.")
    add("W2B2-FB009", "care_packages_and_field_outreach", "direct", "USO describes remote morale drops, care packages and unit support beyond centers.", "direct", "Red Cross describes care packages in the field and during exercises.", none, "No matching care-package function identified in selected Okinawa page.", "Okinawa and overseas deployments", "functional_overlap_no_relation", "W2B2-SR010;W2B2-SR011;W2B2-SR020", "USO outreach paragraphs; Red Cross Care Packages", "USO and Red Cross overlap in field-care delivery functions.", "Functional overlap does not establish co-delivery, funding, shared personnel or alliance.")
    add("W2B2-FB010", "okinawa_physical_presence", "typed_network", "Six centers, AMC terminal presence and area office; outreach is separate.", "official_subunit_prior_decision", "Camp Foster main office and Naval Hospital satellite were principal-accepted from the official health page; direct archive remained blocked.", "typed_offices", "Camp Foster office with Camp Hansen nearby location.", "Okinawa", "co_location_and_separate_service_presence", "W2B2-SR002;W2B2-SR022;W2B2-SR031", "Current directories", "The three organizations maintain distinguishable Okinawa service presences.", "Co-location on bases is background infrastructure, not a cross-organization bridge by itself.")
    return rows


def waterfall_rows() -> list[dict[str, object]]:
    rows = [
        common({"stage_order": 1, "stage_id": "W2B2-WF001", "lane": "same_award_parallel_reporting_views", "stage_label": "View A: award-level record", "organizational_level": "national_prime_award_view", "known_amount": 72000000, "value_text": "USD 72.000m award-level cumulative obligation", "currency": "USD", "period": "2023-09-30/2028-09-29", "measurement_type": "award_obligation", "visibility_status": "known_same_award_view", "source_receipt_ids": "W2B2-SR006", "reason_not_additive": "One reporting view of the same award; not cash expenditure, a sequential upstream stage or local allocation.", "next_gap": "regional_allocation_not_disclosed", "allowed_claim": "The award-level view reports a USD 72.000m cumulative obligation to the national prime recipient."}),
        common({"stage_order": 2, "stage_id": "W2B2-WF002", "lane": "same_award_parallel_reporting_views", "stage_label": "View B: federal-account reporting", "organizational_level": "national_account_reporting_view", "known_amount": 41212463.29, "value_text": "USD 41.21246329m account-linked rollup", "currency": "USD", "period": "retrieved reporting records through FY2024", "measurement_type": "account_linked_transaction_obligation", "visibility_status": "known_same_award_parallel_view", "source_receipt_ids": "W2B2-SR025;W2B2-SR026;W2B2-SR027", "reason_not_additive": "A parallel reporting view of the same award; its perimeter includes a -USD 6.78753671m adjustment and does not include the visible 2025 continuation in the inspected account records.", "next_gap": "regional_allocation_not_disclosed", "allowed_claim": "The same award's account-reporting view reports USD 41.21246329m; it is not a second award or the next step of a cash-flow chain."}),
        common({"stage_order": 3, "stage_id": "W2B2-WF003", "lane": "federal_award_chain", "stage_label": "USO, Inc. -> Indo-Pacific", "organizational_level": "regional_internal_allocation", "known_amount": "", "value_text": "not publicly disclosed", "currency": "", "period": "award period", "measurement_type": "internal_region_allocation", "visibility_status": "allocation_gap", "source_receipt_ids": "W2B2-SR001;W2B2-SR006;W2B2-SR007;W2B2-SR025", "reason_not_additive": "No official region-allocation field located.", "next_gap": "Japan/Okinawa share unavailable.", "allowed_claim": "The public monetary chain stops before the Indo-Pacific operating layer."}),
        common({"stage_order": 4, "stage_id": "W2B2-WF004", "lane": "federal_award_chain", "stage_label": "Indo-Pacific -> Japan/Okinawa", "organizational_level": "area_internal_allocation", "known_amount": "", "value_text": "not publicly disclosed", "currency": "", "period": "award/current reporting period", "measurement_type": "area_allocation", "visibility_status": "allocation_gap", "source_receipt_ids": "W2B2-SR001;W2B2-SR002;W2B2-SR004;W2B2-SR005", "reason_not_additive": "Hierarchy is visible but money is not allocated by area.", "next_gap": "No Okinawa budget or service-use denominator.", "allowed_claim": "The operating hierarchy does not close the monetary allocation chain."}),
        common({"stage_order": 5, "stage_id": "W2B2-WF005", "lane": "federal_award_chain", "stage_label": "USO Okinawa annual operating budget", "organizational_level": "okinawa_area", "known_amount": "", "value_text": "not publicly disclosed", "currency": "", "period": "current", "measurement_type": "local_budget", "visibility_status": "allocation_gap", "source_receipt_ids": "W2B2-SR002;W2B2-SR003", "reason_not_additive": "Local staff, volunteers and directory composition are non-money facts.", "next_gap": "Regional finance or center-level annual report required.", "allowed_claim": "USO Okinawa's service presence is visible while its annual budget is not."}),
        common({"stage_order": 6, "stage_id": "W2B2-WF006", "lane": "local_visible_inputs", "stage_label": "Dated local cash observations", "organizational_level": "local_area_and_center", "known_amount": "", "value_text": "USD 18k (AEC 2024); JPY 1m (AK 2025); USD 16k (AEC 2025); USD 3.25k (OESC 2025)", "currency": "mixed", "period": "2024-2025 examples", "measurement_type": "dated_named_flows_not_total", "visibility_status": "known_bounded_examples", "source_receipt_ids": "W2B2-SR013;W2B2-SR014;W2B2-SR015;W2B2-SR032", "reason_not_additive": "Mixed dates/currencies and non-exhaustive source set; not the local budget.", "next_gap": "Complete local income ledger and recipient-side records unavailable.", "allowed_claim": "Several exact local sponsor/donor flows are visible independently of the national award."}),
        common({"stage_order": 7, "stage_id": "W2B2-WF007", "lane": "local_visible_inputs", "stage_label": "Local in-kind support", "organizational_level": "local_area_and_center", "known_amount": "", "value_text": "AEC facility refresh; MBC WiFi/cable/technical support; values unstated", "currency": "", "period": "2025-2026", "measurement_type": "in_kind_support", "visibility_status": "known_nonmoney_fact_value_unknown", "source_receipt_ids": "W2B2-SR013;W2B2-SR016", "reason_not_additive": "No valuation; some support accompanies cash sponsorship but is not priced.", "next_gap": "Contracts/invoices or donor valuation required.", "allowed_claim": "Official stories identify in-kind operational support without a defensible monetary value."}),
        common({"stage_order": 8, "stage_id": "W2B2-WF008", "lane": "local_service_capacity", "stage_label": "USO Okinawa operating scale", "organizational_level": "okinawa_area", "known_amount": "", "value_text": "current 8 directory entries = 6 centers + 1 terminal entry + 1 area office; 21 employees; 780+ volunteers", "currency": "", "period": "2025/current", "measurement_type": "nonmoney_capacity", "visibility_status": "known_nonmoney_facts", "source_receipt_ids": "W2B2-SR002;W2B2-SR003", "reason_not_additive": "Different units, dates and definitions; none is a financial denominator or lifecycle series.", "next_gap": "Same-definition local uses/visits/people and annual expenses missing.", "allowed_claim": "The current directory composition and local organizational capacity are visible despite missing finances."}),
        common({"stage_order": 9, "stage_id": "W2B2-WF009", "lane": "national_financial_context", "stage_label": "USO 2024 gross program services / functional expenses", "organizational_level": "national_consolidated", "known_amount": 204912000, "value_text": "USD 204.912m gross", "currency": "USD", "period": "year ended 2024-12-31", "measurement_type": "consolidated_gross_program_services_functional_expenses", "visibility_status": "known_separate_financial_perimeter", "source_receipt_ids": "W2B2-SR034", "reason_not_additive": "Organization-wide gross program-services functional expenses; includes USD 105.538m in-kind and is neither an award allocation nor an Okinawa budget.", "next_gap": "No regional expense schedule.", "allowed_claim": "The audited 2024 functional-expense statement reports USD 204.912m gross program services, including USD 105.538m in-kind expenses."}),
        common({"stage_order": 10, "stage_id": "W2B2-WF010", "lane": "national_financial_context", "stage_label": "In-kind program services included in gross", "organizational_level": "national_consolidated", "known_amount": 105538000, "value_text": "USD 105.538m included in gross", "currency": "USD", "period": "year ended 2024-12-31", "measurement_type": "in_kind_program_services_included_in_gross", "visibility_status": "known_component_of_gross_not_additive", "source_receipt_ids": "W2B2-SR034", "reason_not_additive": "This is already included in the USD 204.912m gross figure; do not add it again.", "next_gap": "No regional expense schedule.", "allowed_claim": "The audited statement identifies USD 105.538m of in-kind expenses inside gross program services."}),
        common({"stage_order": 11, "stage_id": "W2B2-WF011", "lane": "national_financial_context", "stage_label": "USO 2024 net program services", "organizational_level": "national_consolidated", "known_amount": 99374000, "value_text": "USD 99.374m net", "currency": "USD", "period": "year ended 2024-12-31", "measurement_type": "consolidated_net_program_services_after_in_kind", "visibility_status": "known_separate_financial_perimeter", "source_receipt_ids": "W2B2-SR034", "reason_not_additive": "Net program services equal gross USD 204.912m less included in-kind USD 105.538m; this remains a national consolidated perimeter.", "next_gap": "No regional expense schedule.", "allowed_claim": "The audited 2024 functional-expense statement reports USD 99.374m net program services."}),
    ]
    return rows


def negative_rows() -> list[dict[str, object]]:
    base = [
        ("W2B2-NS001", "Does USO publish a 2024 Indo-Pacific/Japan/Okinawa financial allocation?", "USO audited statement, Form 990, Global Impact Report, Pacific/Okinawa pages", "No region/area/center expense or award-allocation schedule located.", "regional_finance_not_public", "W2B2-SR001;W2B2-SR002;W2B2-SR003;W2B2-SR034", "USO regional management report, internal budget or grant schedule", "Public national finance cannot be closed to Okinawa.", "Do not estimate from center count, population or global uses."),
        ("W2B2-NS002", "Does USO publish Okinawa service uses, visits and unique people in the same definitions as the global report?", "USO 2024 impact report and Okinawa official pages/stories", "A 2025 USO self-report gives an approximate service-coverage scale of 47,000 service members and their families, plus selected event counts; no same-definition local annual metrics were found.", "local_metric_definition_gap", "W2B2-SR001;W2B2-SR003;W2B2-SR010;W2B2-SR011", "Okinawa annual impact dashboard or area report", "The 47,000 figure is a bounded 2025 USO self-report about service coverage, not a local-use count or allocation weight.", "The self-reported service-coverage scale is not a population denominator; do not treat it as annual users, uses, visits, a census or an allocation weight."),
        ("W2B2-NS003", "Does award HQ00342310002 specify Japan/Okinawa eligible geography?", "USAspending award overview, Assistance Listing fields and transaction history", "Place of performance is U.S. multi-state; eligibility text is generic; no award-specific overseas geography located.", "award_geography_unresolved", "W2B2-SR006;W2B2-SR007", "award terms and conditions, grant agreement or WHS congressional direction", "Award-specific overseas eligibility remains unresolved.", "Do not infer that Okinawa is included or excluded from generic program text."),
        ("W2B2-NS004", "Are public subawards or region recipients attached to the award?", "Award overview and bounded FAIN subaward search", "Overview reports zero and bounded search returned no rows.", "bounded_subaward_zero", "W2B2-SR006;W2B2-SR008", "prime-recipient internal allocation and procurement records", "No public subaward bridge to Okinawa was confirmed.", "Do not treat this as zero internal transfers or services."),
        ("W2B2-NS005", "How should the USD 72m and USD 41.21246329m views of the same award be compared?", "USAspending overview, transactions, funding rollup, accounts and periodic funding records", "They are parallel reporting views of the same award. The account rollup equals 24m - 6.78753671m + 24m; the visible 2025 24m continuation is not closed in the inspected account rows.", "same_award_reporting_perimeter_or_timing_gap", "W2B2-SR006;W2B2-SR007;W2B2-SR025;W2B2-SR026;W2B2-SR027", "later File C submissions or downloadable award/account records with availability periods", "Both views jointly expose the regional allocation gap while remaining separately typed.", "Do not draw them as sequential money-flow stages, add them, substitute one for the other or present either as cash paid."),
        ("W2B2-NS006", "Is there a complete annual Okinawa center roster with opening/closing dates?", "2021 story, 2024 impact report, 2025 stories and current directory", "The sources provide 2021 '7 listed locations', 2025 '6 physical centers' and current '8 directory entries = 6 centers + 1 terminal entry + 1 area office', but annual start/end dates are incomplete.", "site_history_incomplete", "W2B2-SR001;W2B2-SR002;W2B2-SR009;W2B2-SR010;W2B2-SR011", "archived annual directories, leases, center opening/closure announcements", "The three dated vocabularies can be recorded but not turned into a complete lifecycle.", "Do not call eight directory entries eight sites or infer openings, closures or dissolutions from count changes."),
        ("W2B2-NS007", "Do current sponsor tiers disclose amounts or start dates?", "Current USO Okinawa sponsor directory and sponsor pages", "Tier labels are visible; amounts and complete start dates are not.", "sponsor_roster_amount_gap", "W2B2-SR002", "sponsorship agreements, donor schedules or annual reports", "Current sponsor identity/scope can be recorded without money.", "Do not infer tier value or recurring payment."),
        ("W2B2-NS008", "Is there a complete USO Okinawa local sponsor ledger?", "Official USO stories plus existing OESC report", "Several exact dated flows were found, but the story corpus is not an annual exhaustive ledger.", "local_income_coverage_unknown", "W2B2-SR013;W2B2-SR014;W2B2-SR015;W2B2-SR016;W2B2-SR017;W2B2-SR018;W2B2-SR019;W2B2-SR032", "USO Okinawa annual donor schedule or internal ledger", "Exact flows are bounded examples only.", "Do not sum mixed years/currencies into a local budget."),
        ("W2B2-NS009", "Can the current American Red Cross Okinawa local page be frozen?", "U.S. Naval Hospital Okinawa TRICARE page", "Direct page/PDF download returned HTTP 403; the prior principal accepted the official-subunit interpretation from the accessible official page text.", "official_page_archive_blocked", "W2B2-SR031", "manual browser save or official PDF/print view", "The local-office fact remains externally controlled; this package does not create a new central source.", "Do not replace the failed archive with an unverified mirror."),
        ("W2B2-NS010", "Does NMCRS publish Okinawa-specific annual financial assistance totals?", "NMCRS Okinawa page and annual reports index", "Local services and offices are visible, but no Okinawa annual amount was located in the inspected pages.", "local_nmcrs_finance_gap", "W2B2-SR022;W2B2-SR024", "NMCRS location report or internal area ledger", "Functional comparison is possible without a local amount.", "Do not allocate national NMCRS totals to Okinawa."),
    ]
    return [common({"search_id": rid, "question": q, "source_scope": scope, "search_date": BUILD_DATE, "result": result, "gap_type": gap, "source_receipt_ids": receipts, "next_best_material": next_material, "allowed_claim": allowed, "prohibited_inference": prohibited}) for rid, q, scope, result, gap, receipts, next_material, allowed, prohibited in base]


def change_rows() -> list[dict[str, object]]:
    rows = [
        ("W2B2-CN001", "site_count_semantics", "Treat 6 vs 8 as a count discrepancy.", "Official pages use center, location, terminal entry, area office and outreach with different dates.", "Use fixed dated wording: 2021 '7 listed locations'; 2025 '6 physical centers'; current '8 directory entries = 6 centers + 1 terminal entry + 1 area office'.", "W2B2-HS004;W2B2-HS013;W2B2-HS014;W2B2-HS017", "W2B2-SR002;W2B2-SR009;W2B2-SR010;W2B2-SR011", "No dated vocabulary is discarded; three distinct units remain.", "Eight directory entries are not called eight sites, and count differences do not imply lifecycle change.", "Confirm typed interpretation.", "ready_for_principal_review"),
        ("W2B2-CN002", "award_account_semantics", "Treat USD 41.21246329m as a downstream stage or unexplained duplicate of USD 72m.", "The endpoints show two reporting perimeters for the same award: award-level USD 72m and account-linked 24m - 6.78753671m + 24m, while transaction history also includes a 2025 24m continuation.", "Preserve USD 72m and USD 41.21246329m as parallel reporting views of the same award; point both to the regional allocation gap.", "W2B2-FA001;W2B2-FA004;W2B2-FA007;W2B2-FA008;W2B2-FA009;W2B2-FA010;W2B2-FA011;W2B2-FA014;W2B2-FA015;W2B2-WF001;W2B2-WF002", "W2B2-SR006;W2B2-SR007;W2B2-SR025;W2B2-SR026;W2B2-SR027", "The account view is decomposed but not forced to reconcile with the award-level view.", "Neither view is a second award, local share or sequential money-flow stage.", "Approve wording and whether later File C recheck is needed.", "ready_for_principal_review"),
        ("W2B2-CN003", "local_sponsorship", "Use the current sponsor roster as the local funding picture.", "Current tiers omit amounts; official dated stories expose some cash and in-kind actions across years.", "Keep roster relations and dated resource flows in separate rows; never total mixed years/currencies.", "W2B2-SP001;W2B2-SP002;W2B2-SP003;W2B2-SP004;W2B2-SP005;W2B2-SP006;W2B2-SP007;W2B2-SP008;W2B2-SP009;W2B2-SP011;W2B2-SP012;W2B2-SP013;W2B2-SP014;W2B2-SP016;W2B2-SP017", "W2B2-SR002;W2B2-SR013;W2B2-SR014;W2B2-SR015;W2B2-SR016;W2B2-SR017;W2B2-SR018;W2B2-SR019", "Exact flows increase, but no Okinawa budget is calculated.", "Local sponsor visibility is demonstrated as bounded episodes.", "Decide which rows merit later resource-ledger promotion.", "ready_for_principal_review"),
        ("W2B2-CN004", "service_metric_types", "Use all USO counts as service volume.", "Uses, visits, people reached, the 2025 USO self-reported service-coverage scale, volunteers and selected-event participants are different units.", "Keep every metric typed and prohibit conversion across definitions; the self-reported service-coverage scale is not a population denominator.", "W2B2-SC001;W2B2-SC002;W2B2-SC003;W2B2-SC005;W2B2-SC006;W2B2-SC007;W2B2-SC009;W2B2-SC010;W2B2-SC011;W2B2-SC012;W2B2-SC013;W2B2-SC014", "W2B2-SR001;W2B2-SR003;W2B2-SR010", "No local-use weighting is produced.", "Capacity can be described without a fabricated denominator.", "No additional decision unless a local annual metric appears.", "method_change_applied"),
        ("W2B2-CN005", "service_ecology_boundary", "Describe USO, Red Cross and NMCRS as parallel generic welfare services.", "Official pages reveal distinct cores and support one directional NMCRS -> ARC after-hours intake/disbursement delegation candidate using NMCRS funds.", "Build a function matrix and keep the directed NMCRS delegation to ARC at official_source_supported_candidate_pending_principal, not confirmed, funding or alliance.", "W2B2-FB001;W2B2-FB002;W2B2-FB003;W2B2-FB004;W2B2-FB005;W2B2-FB006;W2B2-FB007;W2B2-FB008;W2B2-FB009;W2B2-FB010;W2B2-DE028", "W2B2-SR020;W2B2-SR021;W2B2-SR022;W2B2-SR023;W2B2-SR024", "One directional service-interface candidate is queued; no relation is confirmed by AI.", "NMCRS delegates after-hours intake/disbursement to ARC; ARC acts on NMCRS's behalf using NMCRS funds, pending principal review.", "Principal must decide relation semantics before any central proposal.", "ready_for_principal_review"),
        ("W2B2-CN006", "allocation_visibility_design", "Draw a single numeric national-to-local waterfall.", "The same award has two reporting views, no region allocation is disclosed, local observations mix dates/currencies, and national organizational expenses use another perimeter.", "Draw USD 72m and USD 41.21246329m as parallel same-award reporting views that jointly point to the regional allocation gap; list gross, included in-kind and net program services separately.", "W2B2-WF001;W2B2-WF002;W2B2-WF003;W2B2-WF004;W2B2-WF005;W2B2-WF006;W2B2-WF007;W2B2-WF008;W2B2-WF009;W2B2-WF010;W2B2-WF011", "W2B2-SR006;W2B2-SR013;W2B2-SR016;W2B2-SR025;W2B2-SR026;W2B2-SR027;W2B2-SR034", "No synthetic Okinawa amount is generated and no national amount is made additive.", "The shared regional allocation gap, not a funds-flow chain, is the visual finding.", "Approve as W2-B closing figure.", "ready_for_principal_review"),
    ]
    return [common({"change_note_id": rid, "topic": topic, "original_assumption": original, "failure_reason": failure, "revised_approach": revised, "affected_row_ids": affected, "source_receipt_ids": receipts, "effect_on_numbers": numbers, "effect_on_claims": claims, "principal_decision_requirement": decision, "decision_status": status}) for rid, topic, original, failure, revised, affected, receipts, numbers, claims, decision, status in rows]


def principal_rows() -> list[dict[str, object]]:
    rows = [
        ("W2B2-PR001", "hierarchy_semantics", "Approve the dated wording: 2021 '7 listed locations'; 2025 '6 physical centers'; current '8 directory entries = 6 centers + 1 terminal entry + 1 area office'?", "accept_typed_dated_directory_semantics_without_lifecycle", "The count difference could reflect unrecorded lifecycle changes, but the present evidence only resolves each source's dated vocabulary.", "W2B2-HS004;W2B2-HS013;W2B2-HS014;W2B2-HS017", "W2B2-SR002;W2B2-SR009;W2B2-SR010;W2B2-SR011", "Allows dated directory wording without calling eight entries eight sites or inferring lifecycle."),
        ("W2B2-PR002", "federal_amount_semantics", "Approve USD 72m and USD 41.21246329m as parallel reporting views of the same award that jointly point to a regional allocation gap?", "accept_same_award_parallel_reporting_views", "Later reporting may reconcile the account view with the award-level view; the current endpoint snapshot may be timing-lagged.", "W2B2-FA001;W2B2-FA009;W2B2-FA010;W2B2-FA011;W2B2-FA014;W2B2-FA015;W2B2-WF001;W2B2-WF002", "W2B2-SR006;W2B2-SR025;W2B2-SR026;W2B2-SR027", "Allows a defensible shared regional-allocation-gap statement without depicting sequential fund flow."),
        ("W2B2-PR003", "local_resource_flows", "Which official dated sponsor/resource rows should later enter the shared resource-flow ledger?", "accept_exact_amount_and_typed_in_kind_candidates_subject_to_duplicate_check", "Official USO self-reports may be selective and some exact flows already exist under secondary source IDs.", "W2B2-SP007;W2B2-SP008;W2B2-SP009;W2B2-SP010;W2B2-SP011;W2B2-SP012;W2B2-SP013;W2B2-SP014;W2B2-SP015;W2B2-SP016;W2B2-SP017", "W2B2-SR013;W2B2-SR014;W2B2-SR015;W2B2-SR016;W2B2-SR017;W2B2-SR018;W2B2-SR019;W2B2-SR032;W2B2-SR033", "Defines the W2-B contribution to the common resource-flow ledger."),
        ("W2B2-PR004", "sponsor_roster_scope", "Approve separating current regional sponsor tiers from local Okinawa sponsor tiers?", "accept_scope_as_printed_on_current_page", "Corporate branding may span both levels even when the page places a name in one tier.", "W2B2-SP001;W2B2-SP002;W2B2-SP003;W2B2-SP004;W2B2-SP005;W2B2-SP006", "W2B2-SR002", "Prevents Matson/UMGC/AIG from being misreported as Okinawa-directed amounts."),
        ("W2B2-PR005", "service_function_relation", "Approve the directional NMCRS -> American Red Cross delegation of non-business-hours intake/disbursement, with ARC acting on NMCRS's behalf using NMCRS funds?", "review_directional_candidate_not_funding_or_alliance", "Operational practice may vary after the page snapshot; the official sources support the candidate, but this AI-built package cannot confirm it.", "W2B2-FB003;W2B2-FB004;W2B2-FB005;W2B2-DE028", "W2B2-SR022;W2B2-SR023;W2B2-SR024", "Would decide one precise service-interface candidate while preserving delegation direction and money provenance."),
        ("W2B2-PR006", "allocation_gap_claim", "Approve closing W2-B with 'two same-award national reporting views and local service presence are visible, but the regional monetary allocation layer is not public'?", "accept_bounded_shared_regional_allocation_gap", "A grant agreement or regional annual report could later close the gap.", "W2B2-FA018;W2B2-WF001;W2B2-WF002;W2B2-WF003;W2B2-WF004;W2B2-WF005", "W2B2-SR001;W2B2-SR006;W2B2-SR025;W2B2-SR026;W2B2-SR027", "Provides the W2-B strongest conclusion without depicting a funds-flow waterfall or estimating an Okinawa budget."),
        ("W2B2-PR007", "legitimation_boundary", "Should selected USO/Japanese-partner event rows remain LEG0/LEG1 research observations rather than LEG2 local response?", "keep_at_leg0_or_action_side_leg1", "Participants quoted in an organization story may express experience, but the source is still USO-controlled and not an independent recipient-side response.", "W2B2-SC012;W2B2-SC014", "W2B2-SR010", "Prevents service episodes from being overread as local acceptance or legitimation."),
    ]
    return [common({"decision_id": rid, "decision_type": kind, "question": question, "recommended_decision": recommendation, "alternative_or_competing_explanation": alternative, "affected_row_ids": affected, "source_receipt_ids": receipts, "what_this_unlocks": unlocks, "principal_decision": "", "principal_note": "", "principal_reviewer": "", "principal_decision_date": "", "status": "awaiting_principal_review"}) for rid, kind, question, recommendation, alternative, affected, receipts, unlocks in rows]


def w2d_endpoint_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(endpoint_id: str, endpoint_type: str, label: str, registry_id: str, linked: str, person: str, role: str, start: str, end: str, semantics: str, receipts: str, locator: str, identity: str, eligibility: str, use: str, allowed: str, prohibited: str, notes: str = "") -> None:
        rows.append(common({
            "endpoint_id": endpoint_id,
            "endpoint_type": endpoint_type,
            "canonical_label": label,
            "registry_or_provisional_id": registry_id,
            "linked_actor_or_endpoint": linked,
            "person_name_raw": person,
            "role_or_relation_type": role,
            "observed_start": start,
            "observed_end": end,
            "time_semantics": semantics,
            "source_receipt_ids": receipts,
            "exact_locator": locator,
            "identity_status": identity,
            "bridge_eligibility": eligibility,
            "w2_d_use": use,
            "allowed_claim": allowed,
            "prohibited_inference": prohibited,
            "notes": notes,
        }))

    # Organization and institutional endpoints.  They are endpoints for later audit,
    # not automatic actor additions or organization bridges.
    organizations = [
        ("W2B2-DE001", "United Service Organizations, Inc.", "", "USO Indo-Pacific; USO Okinawa (X001)", "national_prime_organization", "2023-09-30", "2028-09-29", "award_period_not_organization_lifecycle", "W2B2-SR006;W2B2-SR034", "Award recipient and consolidated statement perimeter", "official_national_legal_entity", "organization_endpoint", "National money/organization anchor", "The national prime and consolidated reporting entity are identifiable.", "Do not turn parent/area naming into a centrally approved control edge or allocate the award locally."),
        ("W2B2-DE002", "USO Indo-Pacific", "", "United Service Organizations, Inc.; USO Japan; USO Okinawa", "regional_operating_layer", "2021-06", "2026-08-21", "named_role_start_to_current_page_snapshot", "W2B2-SR001;W2B2-SR004", "Impact report region section and Regional VP biography", "official_operating_region", "organization_endpoint", "Region-level bridge and hierarchy audit", "The Indo-Pacific operating layer and its regional leadership are visible.", "Do not infer a separate法人格, budget or authority beyond the official operating description."),
        ("W2B2-DE003", "USO Japan", "", "USO Indo-Pacific", "mainland_japan_area", "", "2026-08-21", "current_directory_snapshot", "W2B2-SR005", "Japan homepage and area office", "official_area_endpoint", "organization_endpoint", "Keep mainland Japan distinct from Okinawa", "USO Japan is a separately presented area/site system.", "Do not merge it with USO Okinawa or infer money between the areas."),
        ("W2B2-DE004", "USO Okinawa", "X001", "USO Indo-Pacific", "okinawa_area", "", "2026-08-21", "current_directory_snapshot", "W2B2-SR002;W2B2-SR003", "Okinawa homepage and six-center statement", "registered_actor", "organization_endpoint", "Primary service-side W2-D actor", "X001 is the local service-area endpoint for people, sponsor and service-interface rows.", "Do not convert its presence into a pro-base stance or an independently incorporated local法人格."),
        ("W2B2-DE005", "American Engineering Corporation", "X003", "USO Okinawa (X001)", "sponsor_and_in_kind_provider", "2018-03-01", "2025-11-17", "multiple_dated_actions_not_full_relationship_term", "W2B2-SR013;W2B2-SR014;W2B2-SR018", "Three dated USO stories", "registered_actor", "organization_endpoint", "Sponsor/person bridge tracer", "AEC has multiple dated cash and in-kind support observations tied to named representatives.", "Do not infer complete annual giving, political stance or that every company officer served for the whole span."),
        ("W2B2-DE006", "Mediatti Broadband Communications Okinawa", "Mediatti_Broadband_MBC", "USO Okinawa (X001)", "sponsor_and_connectivity_provider", "2018-02-09", "2026-02-24", "multiple_observations_with_claimed_12_year_support", "W2B2-SR016;W2B2-SR017", "2018 and 2026 official stories", "existing_provisional_endpoint", "organization_endpoint", "Sponsor/person continuity tracer", "MBC has dated cash and connectivity-support observations with a recurring named executive.", "Do not infer annual amounts during the 12-year claim or a central actor approval."),
        ("W2B2-DE007", "AK Kogyo", "", "USO Okinawa (X001)", "donor_and_local_business_partner", "2020-12", "2025-03-12", "support_start_claim_and_dated_donation", "W2B2-SR015", "Official story metadata and body", "provisional_organization_endpoint", "organization_endpoint", "Local business/person tracer", "The official story identifies the business, two officers and one dated donation.", "Do not infer all services, annual donations or registry admission."),
        ("W2B2-DE008", "American Welfare & Works Association", "X004", "USO Kinser / USO Okinawa (X001)", "grant_provider", "2020-08-28", "2020-08-28", "single_dated_grant_event", "W2B2-SR033", "Grant presentation paragraph", "registered_actor", "organization_endpoint", "AWWA-to-USO channel tracer", "AWWA is a registered service-ecology endpoint in one bounded USO Kinser grant event.", "Do not infer the full AWWA recipient network or grant amount."),
        ("W2B2-DE009", "Okinawa Enlisted Spouses' Club", "X007", "USO Okinawa (X001)", "donor", "2025-12-02", "2025-12-02", "single_dated_donation_event", "W2B2-SR032", "Donation and president paragraph", "registered_actor", "organization_endpoint", "Spouse-club-to-USO tracer", "OESC is a registered actor in one dated USD 3,250 donation event.", "Do not infer long-term sponsorship, alliance or bridge to the accountability ecology."),
        ("W2B2-DE010", "American Red Cross Okinawa", "X008", "Navy-Marine Corps Relief Society Okinawa (X009)", "after_hours_service_interface", "", "2026-08-22", "current_page_snapshot", "W2B2-SR020;W2B2-SR021;W2B2-SR022;W2B2-SR023", "Overseas services and NMCRS after-hours callout", "registered_actor", "service_interface_endpoint", "Typed service intermediary", "Red Cross is the public after-hours interface for NMCRS assistance in the inspected official pages.", "Do not infer funding by Red Cross, shared governance or a political alliance."),
        ("W2B2-DE011", "Navy-Marine Corps Relief Society Okinawa", "X009", "American Red Cross Okinawa (X008)", "program_and_fund_source_for_after_hours_handoff", "", "2026-08-22", "current_page_snapshot", "W2B2-SR022;W2B2-SR023;W2B2-SR024", "Okinawa office, FAQ and financial statement policy", "registered_actor", "service_interface_endpoint", "Typed service and money-provenance endpoint", "NMCRS owns the assistance program/funds used through the Red Cross after-hours interface.", "Do not convert the handoff into a Red Cross grant or organizational affiliation."),
        ("W2B2-DE012", "Okinawa Nurses Association", "", "USO Foster / U.S. Naval Hospital Okinawa", "event_participant_institution", "2025", "2025", "selected_episode_only", "W2B2-SR010", "Foster National Nurses Week paragraph", "event_only_institutional_endpoint", "event_only_endpoint", "Recipient/participant-side follow-up lead", "The name appears as participants in one USO-controlled event story.", "Do not add it as a registry actor, alliance, recipient institution or LEG2 response without independent confirmation."),
    ]
    for row in organizations:
        add(row[0], "organization_or_institution", row[1], row[2], row[3], "", row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14])

    people = [
        ("W2B2-DE013", "Scott P. Maskery", "USO Indo-Pacific", "Regional Vice President", "2021-06", "2026-08-21", "role_start_and_current_biography_snapshot", "W2B2-SR004", "Biography first paragraph", "identity_specific_official_bio", "Regional hierarchy/person–actor–time tracer"),
        ("W2B2-DE014", "J. Phil VanEtten / Phil VanEtten", "USO Okinawa (X001)", "Area Director", "2018-02-09", "2025-03-12", "multiple_observed_role_dates_not_full_term", "W2B2-SR009;W2B2-SR014;W2B2-SR015;W2B2-SR017;W2B2-SR018;W2B2-SR019", "Named recipient/quoted role across official stories", "alias_and_role_span_need_human_check", "High-value repeated sponsor–USO person tracer"),
        ("W2B2-DE015", "Henry Hughes", "USO Okinawa (X001)", "Area Director", "2025-11-17", "2026-02-24", "multiple_observed_role_dates_not_full_term", "W2B2-SR013;W2B2-SR016", "Named recipient/quoted role", "identity_specific_official_story", "Current-period sponsor–USO person tracer"),
        ("W2B2-DE016", "Kenneth Exsterstein", "American Engineering Corporation (X003)", "CEO", "2024-10-16", "2025-11-17", "multiple_observed_role_dates_not_full_term", "W2B2-SR013;W2B2-SR014", "Donation paragraphs", "identity_specific_official_story", "AEC–USO person-event tracer"),
        ("W2B2-DE017", "Scot Garner", "American Engineering Corporation (X003)", "General Manager of Construction", "2018-03-01", "2024-10-16", "multiple_observed_role_dates_not_full_term", "W2B2-SR014;W2B2-SR018", "Donation story and later quoted role", "identity_specific_official_story", "AEC role-continuity tracer"),
        ("W2B2-DE018", "Keith A. Kirkman", "Mediatti Broadband Communications Okinawa", "President and Chief Executive Officer", "2018-02-09", "2026-02-24", "multiple_observed_role_dates_not_full_term", "W2B2-SR016;W2B2-SR017", "Story metadata/body", "identity_specific_official_story", "Long-duration sponsor-role tracer"),
        ("W2B2-DE019", "Eugene Bourderault", "AK Kogyo", "Owner and President", "2025-03-12", "2025-03-12", "single_observed_role_date", "W2B2-SR015", "Donation paragraph", "identity_specific_official_story", "Local donor person tracer"),
        ("W2B2-DE020", "Hawari Habrawi", "AK Kogyo", "General Manager", "2025-03-12", "2025-03-12", "single_observed_role_date", "W2B2-SR015", "Donation paragraph", "identity_specific_official_story", "Local donor person tracer"),
        ("W2B2-DE021", "Naoki Satoh", "CHUBB Insurance Japan", "Military Segment Manager, Auto Department", "2018-03-15", "2018-03-15", "single_observed_role_date", "W2B2-SR019", "Donation paragraph", "identity_specific_official_story", "Local donor person tracer"),
        ("W2B2-DE022", "Kayla Sprinkel", "Okinawa Enlisted Spouses' Club (X007)", "President", "2025-12-02", "2025-12-02", "single_observed_role_date", "W2B2-SR032", "Paragraph naming OESC president", "identity_specific_secondary_story", "Spouse-club-to-USO person tracer"),
        ("W2B2-DE023", "E.J. Schulz / Shultz", "American Welfare & Works Association (X004)", "President", "2020-08-28", "2020-08-28", "single_event_with_internal_spelling_conflict", "W2B2-SR033", "Paragraph uses Schulz then Shultz", "name_spelling_unresolved", "AWWA-to-USO person tracer requiring spelling decision"),
        ("W2B2-DE024", "Kayla Stamey", "USO Kinser / USO Okinawa (X001)", "Center Manager", "2020-08-28", "2020-08-28", "single_observed_role_date", "W2B2-SR033", "Grant presentation paragraph", "identity_specific_official_story", "USO receiving-side person tracer"),
        ("W2B2-DE025", "Christi Brent", "USO Foster / USO Okinawa (X001)", "Center Operations Manager", "2025", "2025", "story_year_observation", "W2B2-SR010", "Foster paragraph", "identity_specific_official_story", "Center-level person tracer"),
        ("W2B2-DE026", "Will Stanley", "USO Futenma / USO Okinawa (X001)", "Center Operations Manager", "2025", "2025", "story_year_observation", "W2B2-SR010", "Futenma paragraph", "identity_specific_official_story", "Center-level person tracer"),
        ("W2B2-DE027", "Maria Paige", "USO Schwab / USO Okinawa (X001)", "Center Manager", "2022-09-30", "2022-09-30", "story_byline_observation", "W2B2-SR012", "Story byline", "identity_specific_official_story", "Historical center-level person tracer"),
    ]
    for endpoint_id, person, actor, role, start, end, semantics, receipts, locator, identity, use in people:
        add(endpoint_id, "person_actor_time_candidate", person, "", actor, person, role, start, end, semantics, receipts, locator, identity, "person_role_candidate", use, f"The source observes {person} in the stated role at the stated date(s).", "Do not extend the observed dates into a complete tenure, merge similar names, or infer a cross-ecology bridge without independent matching.")

    add(
        "W2B2-DE028", "service_intermediary_relation", "NMCRS after-hours delegation to American Red Cross",
        "", "X009 Navy-Marine Corps Relief Society Okinawa -> X008 American Red Cross Okinawa", "",
        "directed_nmcrs_to_arc_after_hours_intake_disbursement_delegation_using_nmcrs_funds", "", "2026-08-22", "current_page_snapshot",
        "W2B2-SR022;W2B2-SR023;W2B2-SR024", "NMCRS Okinawa and Get Help after-hours callouts",
        "official_source_supported_candidate_pending_principal", "service_interface_candidate_pending_principal", "Typed directional service candidate for W2-D",
        "NMCRS delegates after-hours intake/disbursement to ARC; ARC acts on NMCRS's behalf using NMCRS funds. Official sources support this candidate; principal review remains pending.",
        "Do not code co-location, general referral, common beneficiaries or functional overlap as additional organization bridges; do not code this relation as funding or alliance.",
    )
    return rows


def svg_text(x: int, y: int, value: str, size: int = 18, weight: int = 400, fill: str = "#173b3f", anchor: str = "start") -> str:
    return (
        f'<text x="{x}" y="{y}" font-family="Inter, Arial, Microsoft YaHei, sans-serif" '
        f'font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">'
        f'{escape(value)}</text>'
    )


def svg_card(x: int, y: int, width: int, height: int, title: str, body: list[str], *, tone: str = "teal", dashed: bool = False) -> str:
    palette = {
        "teal": ("#e8f2f0", "#0d6b6e", "#0d5357"),
        "amber": ("#fff4dc", "#ca8c25", "#7a5312"),
        "gray": ("#f4f5f2", "#9ca8a4", "#536360"),
        "blue": ("#eef3f8", "#718ea7", "#35556d"),
    }
    background, stroke, text_fill = palette[tone]
    dash = ' stroke-dasharray="9 7"' if dashed else ""
    parts = [
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="16" fill="{background}" '
        f'stroke="{stroke}" stroke-width="2"{dash}/>',
        svg_text(x + 20, y + 34, title, 18, 700, text_fill),
    ]
    for index, line in enumerate(body):
        parts.append(svg_text(x + 20, y + 64 + index * 24, line, 15, 400, "#415a5e"))
    return "\n".join(parts)


def render_waterfall_svg(path: Path) -> None:
    """Render parallel national reporting views and their shared allocation gap."""
    width, height = 1440, 1040
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="1440" height="1040" fill="#fbfaf5"/>',
        svg_text(60, 58, "USO 全国-冲绳：公开分配信息在哪里中断", 30, 700, "#0b3d42"),
        svg_text(60, 92, "金额框是不同报送或财务口径；框宽不编码金额", 17, 400, "#617579"),
        svg_text(60, 136, "同一 award 的两个并列报送视图", 19, 700, "#0d6b6e"),
        svg_card(60, 160, 580, 148, "视图 A · award-level record", ["USD 72.000m cumulative obligation", "prime recipient: USO, Inc.", "2023-09-30 to 2028-09-29", "不是现金支付或地区份额"], tone="teal"),
        svg_card(800, 160, 580, 148, "视图 B · federal-account reporting", ["USD 41.21246329m", "24m - 6.78753671m + 24m", "同一 award 的账户报送口径", "不是第二笔 award 或下一层现金流"], tone="amber"),
        '<path d="M350 308 V338 H610 V374" stroke="#718184" stroke-width="3" stroke-dasharray="8 7" fill="none" marker-end="url(#arrowGray)"/>',
        '<path d="M1090 308 V338 H830 V374" stroke="#718184" stroke-width="3" stroke-dasharray="8 7" fill="none" marker-end="url(#arrowGray)"/>',
        svg_text(720, 362, "连线表示共同的信息缺口，不表示资金逐层流下", 15, 600, "#617579", "middle"),
        svg_card(450, 380, 540, 150, "Regional allocation gap", ["USO, Inc. -> Indo-Pacific: not disclosed", "Indo-Pacific -> Japan/Okinawa: not disclosed", "USO Okinawa annual budget: not disclosed", "两种报送视图都没有地区分配字段"], tone="gray", dashed=True),
        svg_text(60, 574, "全国组织财务背景（与 award 分配分开）", 18, 700, "#35556d"),
        svg_card(60, 598, 610, 154, "USO 2024 program services", ["Gross functional expenses: USD 204.912m", "In-kind included in gross: USD 105.538m", "Net program services: USD 99.374m", "全国合并口径，不是冲绳预算"], tone="blue"),
        svg_text(730, 574, "冲绳层可见的独立事实", 18, 700, "#0d6b6e"),
        svg_card(730, 598, 650, 154, "具名本地资源流与运作规模", ["AEC USD 18k (2024); AK Kogyo JPY 1m (2025)", "AEC USD 16k; OESC USD 3.25k (2025)", "6 centers + terminal entry + area office", "21 employees / 780+ volunteers"], tone="teal"),
        svg_text(60, 796, "服务生态边界", 18, 700, "#0d6b6e"),
        svg_card(60, 820, 415, 150, "USO", ["中心、连接、士气与外展", "部分转衔与家庭项目", "本地年度同口径服务量缺失"], tone="blue"),
        svg_card(512, 820, 415, 150, "American Red Cross", ["紧急通信、医院志愿、灾害支援", "接受 NMCRS 非营业时段委托", "代表 NMCRS 处理 intake/disbursement"], tone="blue"),
        svg_card(964, 820, 416, 150, "NMCRS", ["无息贷款/补助、应急旅行", "NMCRS -> ARC 委托候选", "ARC 使用 NMCRS funds"], tone="blue"),
        svg_text(60, 1008, "最强可支持结论：全国报送与冲绳服务存在可见，但连接二者的地区分配层没有公开闭合。", 18, 700, "#0b3d42"),
        svg_text(1380, 1024, "W2-B · research_only · 2026-08-22", 13, 400, "#718184", "end"),
        '<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L0,6 L9,3 z" fill="#0d6b6e"/></marker><marker id="arrowAmber" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L0,6 L9,3 z" fill="#ca8c25"/></marker><marker id="arrowGray" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L0,6 L9,3 z" fill="#9ca8a4"/></marker></defs>',
        "</svg>",
    ]
    path.write_text("\n".join(parts) + "\n", encoding="utf-8")


def read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def validate_package(tables: dict[str, list[dict[str, object]]], receipts: list[dict[str, object]]) -> dict[str, object]:
    checks: list[dict[str, object]] = []

    def check(check_id: str, condition: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "status": "PASS" if condition else "FAIL", "detail": detail})

    expected_counts = {
        "hierarchy_and_site_year_v1.csv": 17,
        "service_capacity_observations_v1.csv": 15,
        "sponsor_and_local_flow_observations_v1.csv": 17,
        "federal_award_allocation_audit_v1.csv": 19,
        "service_function_boundary_v1.csv": 10,
        "allocation_waterfall_v1.csv": 11,
        "negative_search_log_v1.csv": 10,
        "change_notes_v1.csv": 6,
        "principal_review_queue_v1.csv": 7,
        "w2_d_endpoint_candidates_v1.csv": 28,
    }
    check("W2B-V001", len(receipts) == 34, f"source receipts={len(receipts)}; expected=34")
    for filename, expected in expected_counts.items():
        check(f"W2B-V-COUNT-{filename}", len(tables[filename]) == expected, f"{filename}: {len(tables[filename])} rows; expected={expected}")

    id_fields = {
        "hierarchy_and_site_year_v1.csv": "row_id",
        "service_capacity_observations_v1.csv": "observation_id",
        "sponsor_and_local_flow_observations_v1.csv": "flow_id",
        "federal_award_allocation_audit_v1.csv": "audit_id",
        "service_function_boundary_v1.csv": "boundary_id",
        "allocation_waterfall_v1.csv": "stage_id",
        "negative_search_log_v1.csv": "search_id",
        "change_notes_v1.csv": "change_note_id",
        "principal_review_queue_v1.csv": "decision_id",
        "w2_d_endpoint_candidates_v1.csv": "endpoint_id",
    }
    all_row_ids: set[str] = set()
    for filename, id_field in id_fields.items():
        ids = [str(row[id_field]) for row in tables[filename]]
        check(f"W2B-V-UNIQUE-{filename}", len(ids) == len(set(ids)), f"{filename}: {len(set(ids))}/{len(ids)} unique IDs")
        all_row_ids.update(ids)

    receipt_ids = {str(row["receipt_id"]) for row in receipts}
    all_status_rows = receipts + [row for rows in tables.values() for row in rows]
    illegal = sorted({str(row.get("review_status", "")) for row in all_status_rows if str(row.get("review_status", "")) not in LEGAL_REVIEW_STATUSES})
    check("W2B-V002", not illegal, f"illegal review_status values={illegal}")
    check("W2B-V003", all(row.get("package_scope") == PACKAGE_SCOPE for row in all_status_rows), "all rows are research_only")
    check("W2B-V004", all(row.get("central_writeback") == CENTRAL_WRITEBACK for row in all_status_rows), "all rows prohibit central writeback")

    missing_receipts: set[str] = set()
    for row in [row for rows in tables.values() for row in rows]:
        for receipt_id in split_ids(row.get("source_receipt_ids")):
            if receipt_id not in receipt_ids:
                missing_receipts.add(receipt_id)
    check("W2B-V005", not missing_receipts, f"missing receipt references={sorted(missing_receipts)}")

    bad_support_ids: set[str] = set()
    for receipt in receipts:
        for row_id in split_ids(receipt.get("supports_row_ids")):
            if row_id not in all_row_ids:
                bad_support_ids.add(row_id)
    check("W2B-V006", not bad_support_ids, f"receipt supports unknown row IDs={sorted(bad_support_ids)}")

    artifact_errors: list[str] = []
    for receipt in receipts:
        artifact_path = str(receipt.get("artifact_path") or "")
        expected_hash = str(receipt.get("sha256") or "")
        if artifact_path:
            artifact = ROOT / artifact_path
            if not artifact.exists():
                artifact_errors.append(f"missing:{artifact_path}")
            elif sha256(artifact) != expected_hash:
                artifact_errors.append(f"hash:{artifact_path}")
        elif receipt["archive_status"] != "blocked_403_logged":
            artifact_errors.append(f"blank:{receipt['receipt_id']}")
    check("W2B-V007", not artifact_errors, f"artifact errors={artifact_errors}")

    prior_art = ROOT / "outputs" / "us_presence_network_wave2_w2_00_uso_v1" / "artifacts"
    overview = read_json(prior_art / "usaspending_award_overview.json")
    transactions = read_json(prior_art / "usaspending_transactions_response.json")
    subawards = read_json(prior_art / "usaspending_subawards_response.json")
    funding = read_json(ART / "usaspending_funding_response.json")
    rollup = read_json(ART / "usaspending_funding_rollup_response.json")
    accounts = read_json(ART / "usaspending_accounts_response.json")
    transaction_total = sum(float(row.get("federal_action_obligation") or 0) for row in transactions["results"])
    account_record_total = sum(float(row.get("transaction_obligated_amount") or 0) for row in funding["results"])
    check("W2B-V008", overview["total_obligation"] == 72000000.0, f"award total={overview['total_obligation']}")
    check("W2B-V009", len(transactions["results"]) == 5 and transaction_total == 72000000.0, f"transactions={len(transactions['results'])}; sum={transaction_total}")
    check("W2B-V010", abs(rollup["total_transaction_obligated_amount"] - 41212463.29) < 0.001, f"rollup={rollup['total_transaction_obligated_amount']}")
    check("W2B-V011", abs(accounts["results"][0]["total_transaction_obligated_amount"] - 41212463.29) < 0.001, f"accounts={accounts['results'][0]['total_transaction_obligated_amount']}")
    check("W2B-V012", abs(account_record_total - 41212463.29) < 0.001, f"typed obligation records sum={account_record_total}")
    check("W2B-V013", overview["subaward_count"] == 0 and subawards["results"] == [], "award overview and bounded search both expose zero public subaward rows")

    hierarchy = tables["hierarchy_and_site_year_v1.csv"]
    hierarchy_by_id = {str(row["row_id"]): row for row in hierarchy}
    current_centers = [row for row in hierarchy if row["site_type"] == "operating_center"]
    current_presence_rows = [row for row in hierarchy if row["row_id"] in {f"W2B2-HS{number:03d}" for number in range(5, 13)}]
    check("W2B-V014", len(current_centers) == 6, f"current operating centers={len(current_centers)}")
    check("W2B-V015", len(current_presence_rows) == 8, f"current typed presences represented={len(current_presence_rows)}")
    check("W2B-V025", hierarchy_by_id["W2B2-HS013"]["quantity_unit"] == "listed_locations" and hierarchy_by_id["W2B2-HS017"]["quantity_unit"] == "physical_centers" and hierarchy_by_id["W2B2-HS004"]["quantity_unit"] == "directory_entries", "site vocabularies are fixed as 2021 listed locations, 2025 physical centers and current directory entries")
    check("W2B-V026", all("lifecycle" in str(hierarchy_by_id[row_id]["prohibited_inference"]).lower() for row_id in ("W2B2-HS004", "W2B2-HS013", "W2B2-HS017")), "dated site vocabularies prohibit lifecycle inference")
    waterfall = tables["allocation_waterfall_v1.csv"]
    waterfall_by_id = {str(row["stage_id"]): row for row in waterfall}
    local_budget = next(row for row in waterfall if row["stage_id"] == "W2B2-WF005")
    check("W2B-V016", local_budget["known_amount"] == "" and local_budget["visibility_status"] == "allocation_gap", "Okinawa budget remains blank and typed as an allocation gap")
    check("W2B-V017", all(row["known_amount"] == "" for row in waterfall if row["stage_id"] in {"W2B2-WF003", "W2B2-WF004", "W2B2-WF005"}), "region, area and Okinawa allocation stages contain no synthetic amounts")
    check("W2B-V027", all(waterfall_by_id[row_id]["lane"] == "same_award_parallel_reporting_views" and waterfall_by_id[row_id]["next_gap"] == "regional_allocation_not_disclosed" for row_id in ("W2B2-WF001", "W2B2-WF002")), "USD72m and USD41.21246329m are parallel same-award views with one regional allocation gap")
    gross = waterfall_by_id["W2B2-WF009"]
    in_kind = waterfall_by_id["W2B2-WF010"]
    net = waterfall_by_id["W2B2-WF011"]
    check("W2B-V028", gross["known_amount"] == 204912000 and in_kind["known_amount"] == 105538000 and net["known_amount"] == 99374000 and gross["known_amount"] - in_kind["known_amount"] == net["known_amount"], "2024 gross program services USD204.912m includes USD105.538m in-kind and yields USD99.374m net")
    receipt_by_id = {str(row["receipt_id"]): row for row in receipts}
    finance_locator = str(receipt_by_id["W2B2-SR034"]["exact_locator"])
    check("W2B-V029", all(token in finance_locator for token in ("p.8", "Functional expenses, gross", "105,538", "Functional expenses, net", "99,374")), "official audited PDF locator names the exact p.8 gross, in-kind and net cells")
    sponsor = tables["sponsor_and_local_flow_observations_v1.csv"]
    aec_18k = [row for row in sponsor if row["source_name"] == "American Engineering Corporation" and str(row["amount"]) == "18000"]
    check("W2B-V018", sorted(row["date_start"] for row in aec_18k) == ["2018-03-01", "2024-10-16"], f"distinct AEC USD18k rows={[(row['flow_id'], row['date_start']) for row in aec_18k]}")
    handoff = next(row for row in tables["service_function_boundary_v1.csv"] if row["boundary_id"] == "W2B2-FB005")
    check("W2B-V019", handoff["relation_or_boundary"] == "directed_nmcrs_to_arc_after_hours_intake_disbursement_delegation" and handoff["claim_status"] == "official_source_supported_candidate_pending_principal" and "NMCRS funds" in handoff["nmcrs_evidence"], "NMCRS -> ARC after-hours intake/disbursement delegation is directional, uses NMCRS funds and remains pending principal review")
    check("W2B-V030", "confirmed" not in " ".join(str(value) for value in handoff.values()).lower(), "NMCRS -> ARC candidate row contains no confirmed wording")
    check("W2B-V020", all(row["status"] == "awaiting_principal_review" and not row["principal_decision"] for row in tables["principal_review_queue_v1.csv"]), "all seven principal decisions remain open")
    queue_by_id = {str(row["decision_id"]): row for row in tables["principal_review_queue_v1.csv"]}
    check("W2B-V031", "parallel reporting views of the same award" in str(queue_by_id["W2B2-PR002"]["question"]) and "NMCRS -> American Red Cross" in str(queue_by_id["W2B2-PR005"]["question"]), "principal queue carries the corrected award and directional service-interface questions")

    endpoints = tables["w2_d_endpoint_candidates_v1.csv"]
    person_endpoints = [row for row in endpoints if row["endpoint_type"] == "person_actor_time_candidate"]
    interface_endpoints = [row for row in endpoints if row["endpoint_type"] == "service_intermediary_relation"]
    check("W2B-V022", len(person_endpoints) == 15, f"W2-D person-role candidates={len(person_endpoints)}")
    check("W2B-V023", len(interface_endpoints) == 1 and interface_endpoints[0]["role_or_relation_type"] == "directed_nmcrs_to_arc_after_hours_intake_disbursement_delegation_using_nmcrs_funds" and interface_endpoints[0]["identity_status"] == "official_source_supported_candidate_pending_principal", "W2-D exposes one precisely typed directional NMCRS -> ARC delegation candidate pending principal review")
    check("W2B-V024", "not code this relation as funding or alliance" in interface_endpoints[0]["prohibited_inference"], "co-location/referral does not auto-promote to organization bridge")
    svg = (OUT / "fig_allocation_visibility_waterfall_v1.svg").read_text(encoding="utf-8")
    check("W2B-V032", "同一 award 的两个并列报送视图" in svg and "连线表示共同的信息缺口，不表示资金逐层流下" in svg and 'd="M350 236 H405"' not in svg, "SVG uses parallel same-award views rather than the retired sequential arrow")
    local_scale_text = " ".join(str(value) for value in waterfall_by_id["W2B2-WF008"].values()).lower()
    svg_lower = svg.lower()
    removed_allocation_tokens = ("47k", "47,000", "47000")
    check("W2B-V033", all(token not in local_scale_text and token not in svg_lower for token in removed_allocation_tokens), "47,000 self-reported service coverage is absent from WF008 and the public allocation figure")
    capacity_by_id = {str(row["observation_id"]): row for row in tables["service_capacity_observations_v1.csv"]}
    bounded_coverage = capacity_by_id["W2B2-SC002"]
    check("W2B-V034", bounded_coverage["value"] == 47000 and "2025 USO" in str(bounded_coverage["allowed_claim"]) and "self-reported service-coverage scale" in str(bounded_coverage["allowed_claim"]) and "not a population denominator" in str(bounded_coverage["prohibited_inference"]), "SC002 retains 47,000 only as a bounded 2025 USO self-reported service-coverage scale, not a population denominator")
    negative_by_id = {str(row["search_id"]): row for row in tables["negative_search_log_v1.csv"]}
    negative_boundary = " ".join(str(value) for value in negative_by_id["W2B2-NS002"].values()).lower()
    readme_lower = (OUT / "README.md").read_text(encoding="utf-8").lower()
    check("W2B-V035", "2025 uso self-report" in negative_boundary and "not a population denominator" in negative_boundary and "2025 uso self-reported service-coverage scale" in readme_lower and "not a population denominator" in readme_lower, "negative log and README preserve the 2025 USO self-report boundary and reject use as a population denominator")

    synthetic_rows = [
        row for row in sponsor
        if row["target_name"] == "USO Okinawa"
        and row["source_name"] in {"United Service Organizations, Inc.", "Department of Defense", "Washington Headquarters Services"}
    ]
    check("W2B-V021", not synthetic_rows, f"synthetic national-to-Okinawa money rows={[(row['flow_id'], row['amount']) for row in synthetic_rows]}")

    failures = [item for item in checks if item["status"] != "PASS"]
    return {
        "package": "us_presence_network_wave2_w2_b_v1",
        "build_date": BUILD_DATE,
        "status": "PASS_RESEARCH_ONLY" if not failures else "FAIL",
        "check_count": len(checks),
        "pass_count": len(checks) - len(failures),
        "fail_count": len(failures),
        "checks": checks,
        "scope": PACKAGE_SCOPE,
        "central_writeback": CENTRAL_WRITEBACK,
        "frontend_status": FRONTEND_STATUS,
    }


def readme_text(counts: dict[str, int]) -> str:
    return f"""# W2-B：USO 全国—地区—冲绳层级研究包 v1

日期：{BUILD_DATE}

状态：`research_only`／`ai_seeded`／`not_frontend_ready`。本包没有修改中央事实表、publication adapter、前端或控制文档。

## 1. 本包回答什么

本包沿着三条相互分开的链调查：

1. USO 全国组织、Indo-Pacific、Japan 与 Okinawa 的组织／站点层级；
2. DoD/WHS award、USO 全国财务与冲绳本地赞助／服务事实之间能否闭合；
3. USO、American Red Cross 与 Navy-Marine Corps Relief Society 在冲绳服务体系中的功能边界。

结论先行：**公开记录能同时看见同一 award 的两个全国报送视图、地区组织层级、冲绳目录条目和若干本地赞助，但没有公开连接 USO, Inc. 与 Indo-Pacific／Japan／Okinawa 的地区金额分配层。** 因而本包支持的是“并列报送口径可见、地区分配缺口未闭合”，不是资金逐层流下的链条或冲绳预算估计。

## 2. 交付计数

| 文件 | 行数 | 内容 |
|---|---:|---|
| `hierarchy_and_site_year_v1.csv` | {counts['hierarchy_and_site_year_v1.csv']} | dated 层级、center／terminal／office／outreach 类型 |
| `service_capacity_observations_v1.csv` | {counts['service_capacity_observations_v1.csv']} | 全国 impact、本地人员／志愿者、选定活动人数 |
| `sponsor_and_local_flow_observations_v1.csv` | {counts['sponsor_and_local_flow_observations_v1.csv']} | sponsor roster、现金／实物的具名事件 |
| `federal_award_allocation_audit_v1.csv` | {counts['federal_award_allocation_audit_v1.csv']} | award／transaction／account／subaward／allocation gap |
| `service_function_boundary_v1.csv` | {counts['service_function_boundary_v1.csv']} | USO／Red Cross／NMCRS 十类功能对照 |
| `allocation_waterfall_v1.csv` | {counts['allocation_waterfall_v1.csv']} | 并列 award/account 视图、共同分配缺口及 gross/in-kind/net 财务口径 |
| `source_receipts_v1.csv` | {counts['source_receipts_v1.csv']} | 来源收据；33 件本地哈希归档，1 件 403 日志 |
| `negative_search_log_v1.csv` | {counts['negative_search_log_v1.csv']} | 十项有界负检索与下一材料入口 |
| `change_notes_v1.csv` | {counts['change_notes_v1.csv']} | 六项口径调整 |
| `principal_review_queue_v1.csv` | {counts['principal_review_queue_v1.csv']} | 七项负责人判断 |
| `w2_d_endpoint_candidates_v1.csv` | {counts['w2_d_endpoint_candidates_v1.csv']} | 12 个组织／机构端点、15 个人物角色候选、1 条服务中介接口 |

图：`fig_allocation_visibility_waterfall_v1.svg`。文件名保留旧契约；图内 USD 72m 与 USD 41.21246329m 是同一 award 的并列报送视图，共同指向 regional allocation gap，连线不表示资金逐层流下。框宽不编码金额。

## 3. 精确发现

### 3.1 站点数不是一个口径

- 2021 年官方故事是 **7 listed locations**：Schwab、Hansen、Kadena、Kadena Air Terminal、Foster、Futenma、Kinser；另列 10 个 outreach sites。
- 2025 年官方材料是 **6 physical centers**。
- 当前是 **8 directory entries = 6 centers + 1 terminal entry + 1 area office**。Torii Station 被官方材料明确写成没有 dedicated center 的 outreach site。

这三组数可以并存。不将 8 directory entries 称为 8 个站点；三个时间截面也不能推出中心开闭、组织解散或任何生命周期变化。

`47,000` 仅保留在 `service_capacity_observations_v1.csv` 中，其语义是 **2025 USO self-reported service-coverage scale**（USO 2025 年自述的服务覆盖规模），**not a population denominator**。它不进入 `allocation_waterfall_v1.csv` 或对外解释图，也不能转换为年度唯一用户、uses、visits、人口普查数或地区分配权重。

### 3.2 已知金额与未知金额

已知：

- `HQ00342310002` 有两个并列报送视图：award-level cumulative obligation 为 USD 72m，而 federal-account reporting 视图为 USD 41.21246329m（USD 24m - USD 6.78753671m + USD 24m）。两者都是同一 award 的全国报送口径，不是先后流动的两层资金；两者共同指向未公开的 regional allocation gap。
- USO 2024 审计合并财务表 p.8 列出 **gross program services / functional expenses USD 204.912m**，其中已包含 **in-kind USD 105.538m**，并同时列出 **net program services USD 99.374m**。这是全国组织合并财务口径，不是上述 award 的分配表。
- 冲绳层存在若干具名、具日的独立流入个案，包括 AEC USD 18k（2024）、AK Kogyo JPY 1m（2025）、AEC USD 16k（2025）与 OESC USD 3.25k（2025）。这些记录不是完整本地收入表。

未知：

- national prime → Indo-Pacific 的分配；
- Indo-Pacific → Japan/Okinawa 的分配；
- USO Okinawa 年度预算和中心费用；
- 与全球 `uses／visits／people reached` 同定义的冲绳年度分母；
- current sponsor tier 的金额；
- 具名实物支持的货币估值。

因此 USD 72m 和 USD 41.21246329m 不能相加；USD 105.538m 已包在 USD 204.912m gross 中，也不能再加一次。这些全国口径与本地个案金额都不能按中心数、人口或全球服务使用次数机械分配。

### 3.3 服务生态不是三家同质机构

- USO 的可见核心是 center/outreach、连接、士气与生活服务。
- American Red Cross 的可见核心包括紧急通信、医院志愿、灾害与海外军事社区支持。
- NMCRS 的可见核心包括无息贷款／补助、应急旅行、预算教育与灾害救助。
- 官方材料支持一条有方向的候选接口：**NMCRS -> American Red Cross (ARC)**。NMCRS 委托 ARC 处理非营业时段的 intake/disbursement；ARC 代表 NMCRS 并使用 **NMCRS funds**。状态为 `official_source_supported_candidate_pending_principal`，不是 confirmed，也不是组织间 funding、joint grant、合并或政治联盟。

## 4. 最强可支持表述

> 同一 award 的两个全国报送视图、Indo-Pacific／Japan／Okinawa 组织层级、冲绳目录条目和部分本地赞助分别可见，但公开记录没有披露连接全国与地区层的金额分配。由此可以确认服务基础设施的存在和若干本地资源输入，不能据此估算 USO Okinawa 的联邦资金额度或年度预算。

服务侧进一步显示出功能分工与有限接口，而不是单一同质网络；现有材料仍只到行动／组织自述和服务结构层，不能证明地方接受、态度改变或军事存在获得合法性。

## 5. 可改变判断的材料

1. award agreement／terms、WHS 项目报告或 later File C submissions，能解释 USD 72m 与 USD 41.21246329m 两个并列报送视图的时序／范围差异；
2. USO Indo-Pacific／Japan／Okinawa 年报、area budget 或 center-level expense schedule，能闭合地区金额层；
3. 与全球口径一致的 Okinawa `uses／visits／people reached` 年度表，能支持 service-use weighting；
4. USO Okinawa 的完整 donor schedule、sponsor agreement、in-kind valuation 或内部收入表，能判断本地个案覆盖；
5. Red Cross Okinawa 官方页面的人工归档件，可替代本轮 HTTP 403 日志；
6. recipient／使用者或独立地方来源对具体服务的回应，才可能把 LEG0／行动方 LEG1 推向 LEG2。

## 6. 负责人需要判断

七项判断已集中在 `principal_review_queue_v1.csv`：站点语义、两组联邦金额、哪些本地资源流进入共享 ledger、regional/local sponsor scope、Red Cross—NMCRS service interface、层级缺口结论，以及 LEG0/LEG1 边界。没有任何一项在本包内代替负责人完成。

供 W2-D 使用的端点另列在 `w2_d_endpoint_candidates_v1.csv`。人物行只保留资料中实际观察到的职务日期；`J. Phil VanEtten / Phil VanEtten` 与 `E.J. Schulz / Shultz` 仍需要姓名规范化。唯一进入关系复核的服务接口候选是 NMCRS -> ARC 的非营业时段 intake/disbursement 委托；ARC 代表 NMCRS 并使用 NMCRS funds。它仍是 `official_source_supported_candidate_pending_principal`。同址、一般转介、共同服务对象或功能重叠都没有自动升格为组织桥。

## 意外发现登记

本轮 **0 条**。`unexpected_findings_register_v1.csv` 仅保留规范表头。未来若在本包中遇到题外线索，只能以 `lead_only` 留在包内：不进入结论、中央事实、人工复核队列、publication snapshot 或前端；有限侦察最多沿线索三步、全包最多十条观察。

## 7. 复现与验证

```powershell
python scripts\\build_us_presence_wave2_w2_b_v1.py
python -m unittest tests.test_build_us_presence_wave2_w2_b_v1
python scripts\\validate_research_work_package_v1.py outputs\\us_presence_network_wave2_w2_b_v1
```

`validation_report_v1.json` 必须为 `PASS_RESEARCH_ONLY`。`manifest_v1.json` 给出本包表格、图、README、验证报告与来源下载件的 SHA-256。构建只读取已经冻结的官方／既有归档件，不联网，也不分配中央 S-ID。
"""


def write_manifest(paths: list[Path]) -> None:
    items = []
    for path in sorted(paths, key=lambda value: value.relative_to(ROOT).as_posix()):
        items.append({
            "path": path.relative_to(ROOT).as_posix(),
            "sha256": sha256(path),
            "bytes": path.stat().st_size,
        })
    manifest = {
        "package": "us_presence_network_wave2_w2_b_v1",
        "build_date": BUILD_DATE,
        "scope": PACKAGE_SCOPE,
        "central_writeback": CENTRAL_WRITEBACK,
        "frontend_status": FRONTEND_STATUS,
        "file_count": len(items),
        "files": items,
    }
    (OUT / "manifest_v1.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    receipts = source_receipts()
    tables: dict[str, list[dict[str, object]]] = {
        "hierarchy_and_site_year_v1.csv": hierarchy_rows(),
        "service_capacity_observations_v1.csv": capacity_rows(),
        "sponsor_and_local_flow_observations_v1.csv": sponsor_rows(),
        "federal_award_allocation_audit_v1.csv": federal_rows(),
        "service_function_boundary_v1.csv": boundary_rows(),
        "allocation_waterfall_v1.csv": waterfall_rows(),
        "negative_search_log_v1.csv": negative_rows(),
        "change_notes_v1.csv": change_rows(),
        "principal_review_queue_v1.csv": principal_rows(),
        "w2_d_endpoint_candidates_v1.csv": w2d_endpoint_rows(),
    }
    fieldsets = {
        "hierarchy_and_site_year_v1.csv": HIERARCHY_FIELDS,
        "service_capacity_observations_v1.csv": CAPACITY_FIELDS,
        "sponsor_and_local_flow_observations_v1.csv": SPONSOR_FIELDS,
        "federal_award_allocation_audit_v1.csv": FEDERAL_FIELDS,
        "service_function_boundary_v1.csv": BOUNDARY_FIELDS,
        "allocation_waterfall_v1.csv": WATERFALL_FIELDS,
        "negative_search_log_v1.csv": NEGATIVE_FIELDS,
        "change_notes_v1.csv": CHANGE_FIELDS,
        "principal_review_queue_v1.csv": PRINCIPAL_FIELDS,
        "w2_d_endpoint_candidates_v1.csv": W2D_ENDPOINT_FIELDS,
    }
    for filename, rows in tables.items():
        write_csv(OUT / filename, fieldsets[filename], rows)
    write_csv(OUT / "source_receipts_v1.csv", RECEIPT_FIELDS, receipts)
    write_empty_unexpected_findings_register()
    render_waterfall_svg(OUT / "fig_allocation_visibility_waterfall_v1.svg")

    counts = {filename: len(rows) for filename, rows in tables.items()}
    counts["source_receipts_v1.csv"] = len(receipts)
    (OUT / "README.md").write_text(readme_text(counts), encoding="utf-8")
    validation = validate_package(tables, receipts)
    (OUT / "validation_report_v1.json").write_text(json.dumps(validation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    deliverables = [OUT / filename for filename in tables]
    deliverables.extend([
        OUT / "source_receipts_v1.csv",
        OUT / "fig_allocation_visibility_waterfall_v1.svg",
        OUT / "unexpected_findings_register_v1.csv",
        OUT / "README.md",
        OUT / "validation_report_v1.json",
    ])
    deliverables.extend(path for path in ART.iterdir() if path.is_file())
    write_manifest(deliverables)
    print(json.dumps({"status": validation["status"], "counts": counts, "check_count": validation["check_count"]}, ensure_ascii=False))
    return 0 if validation["status"] == "PASS_RESEARCH_ONLY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
