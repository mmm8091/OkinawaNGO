from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from typing import Iterable, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "outputs" / "us_presence_accountability_recon_v1"
AS_OF_DATE = "2026-08-19"
PACKAGE_ID = "us_presence_accountability_recon_v1"

REGISTRY_PATH = Path("data/interim/01_actor_registry_initial_v0.csv")
SOURCE_LOG_PATH = Path("data/interim/05_source_log_initial_v0.csv")
CASE_ROLES_PATH = Path("data/interim/18_legal_policy_actor_roles_v0.csv")
INPUT_PATHS = (REGISTRY_PATH, SOURCE_LOG_PATH, CASE_ROLES_PATH)

SCOPE_IDS = (
    "A009",
    "A033",
    "A042",
    "A045",
    "A070",
    "A086",
    "X013",
    "X014",
)
ACCOUNTABILITY_IDS = ("A009", "A033", "A042", "A045", "A070", "A086")

COMMON = {
    "package_scope": "research_only",
    "claim_status": "candidate_fact",
    "frontend_eligibility": "excluded_pending_human_review",
    "central_writeback": "no",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with (ROOT / path).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def add_common(rows: Iterable[Mapping[str, str]]) -> list[dict[str, str]]:
    return [{**row, **COMMON} for row in rows]


def build_actor_scope(
    registry: Sequence[Mapping[str, str]],
) -> list[dict[str, str]]:
    by_id = {row["actor_id"]: row for row in registry}
    missing = sorted(set(SCOPE_IDS) - set(by_id))
    if missing:
        raise ValueError(f"Missing scope actors: {missing}")

    positions = {
        "A009": (
            "accountability_legal_counsel",
            "Human-reviewed counsel role in R8C01; official FY2021 Form 990 adds a case-level court-awarded fee/cost observation.",
            "Trace Okinawa-case staffing, court-award record, and any disclosed restricted support without inferring donor identity.",
        ),
        "A033": (
            "accountability_event_participant",
            "Current Okinawa-specific support is the 2015 NACSJ joint-statement listing.",
            "Find an organization-authored Okinawa page, annual-report entry, staff role, or archive record before treating this as a continuing Okinawa program.",
        ),
        "A042": (
            "accountability_event_participant",
            "Current Okinawa-specific support is the 2015 NACSJ joint-statement listing.",
            "Find an organization-authored Okinawa page, annual-report entry, staff role, or archive record before treating this as a continuing Okinawa program.",
        ),
        "A045": (
            "accountability_plaintiff_and_campaign_carrier",
            "Human-reviewed plaintiff role in R8C01; official organization pages describe coalition leadership, scientific mobilization, and work with Network for Okinawa.",
            "Separate litigation role, campaign coordination, scientific mobilization, and organization-wide fundraising.",
        ),
        "A070": (
            "accountability_veteran_chapter",
            "Registry identity was needs_second_source; VFP official chapter lists and 2021/2023 materials now provide organization, people, and recurring Okinawa-action evidence.",
            "Human-review chapter identity, continuity, and bounded coordination claims; resolve named coalition endpoints one by one.",
        ),
        "A086": (
            "accountability_plaintiff",
            "Human-reviewed plaintiff role in R8C01; current registry sources establish the case role but do not yet expose Okinawa-specific funding or staff allocation.",
            "Search official annual reports, Form 990 attachments, declarations, and case files for staff/time/resource observations.",
        ),
        "X013": (
            "us_public_diplomacy_opportunity",
            "Official records establish an Okinawa Youth Council funding opportunity, not an award or recipient.",
            "Search award announcements and federal spending records by opportunity number; retain opportunity-only status until a recipient is named.",
        ),
        "X014": (
            "us_funder_watchlist",
            "The checked NED FY2024 Asia list did not identify a Japan/Okinawa/Ryukyu recipient.",
            "Extend year-by-year official grant-list search; do not convert the watchlist into a funding edge without a named award.",
        ),
    }

    rows: list[dict[str, str]] = []
    for actor_id in SCOPE_IDS:
        actor = by_id[actor_id]
        position, current_basis, next_question = positions[actor_id]
        rows.append(
            {
                "actor_id": actor_id,
                "canonical_name": actor["canonical_name"],
                "actor_class": actor["actor_class"],
                "origin_type": actor["origin_type"],
                "current_review_status": actor["review_status"],
                "current_source_refs": actor["source_refs"],
                "functional_position": position,
                "counts_in_six_actor_accountability_subset": (
                    "yes" if actor_id in ACCOUNTABILITY_IDS else "no"
                ),
                "current_evidence_basis": current_basis,
                "next_database_question": next_question,
            }
        )
    return add_common(rows)


def build_source_proposals() -> list[dict[str, str]]:
    rows = [
        {
            "proposal_id": "USAP001",
            "url": "https://earthjustice.org/document/irs-form-990-fy2021",
            "source_owner": "Earthjustice",
            "source_type": "official_form_990",
            "document_date_or_tax_period": "2020-07-01/2021-06-30",
            "locator": "PDF page 54; Schedule O; lines 5613-5617 in text extraction",
            "supports": "Earthjustice lists project 1272 OKINAWA DUGONG with USD 276345.50 in its schedule of top ten court-awarded attorney fees and costs.",
            "does_not_support": "Donor identity; grant income; project expenditure; payment by an Okinawa organization; unrestricted funding source.",
            "evidence_level_proposed": "E4",
            "archive_priority": "P0",
        },
        {
            "proposal_id": "USAP002",
            "url": "https://www.biologicaldiversity.org/species/mammals/Okinawa_dugong/",
            "source_owner": "Center for Biological Diversity",
            "source_type": "official_campaign_page",
            "document_date_or_tax_period": "undated_current_page_observed_2026-08-19",
            "locator": "Saving the Okinawa Dugong paragraphs 2-5",
            "supports": "CBD describes leading the 2003 coalition lawsuit, organizing the 889-expert resolution, international group appeals, and work with Network for Okinawa.",
            "does_not_support": "Funding; durable relation to every named coalition participant; present-day activity intensity.",
            "evidence_level_proposed": "E4",
            "archive_priority": "P0",
        },
        {
            "proposal_id": "USAP003",
            "url": "https://www.biologicaldiversity.org/news/press_releases/dugong9-25-03.html",
            "source_owner": "Center for Biological Diversity",
            "source_type": "official_press_release",
            "document_date_or_tax_period": "2003-09-25",
            "locator": "contacts and paragraphs naming plaintiffs, counsel, and speakers",
            "supports": "Named U.S./Japanese plaintiffs, Earthjustice counsel, and five public person-role observations at lawsuit filing.",
            "does_not_support": "Continuing staff roles after 2003; funding; stable alliance beyond the case/action.",
            "evidence_level_proposed": "E4",
            "archive_priority": "P0",
        },
        {
            "proposal_id": "USAP004",
            "url": "https://www.veteransforpeace.org/files/1415/8938/5791/20.05.13.ChapterContact.pdf",
            "source_owner": "Veterans For Peace",
            "source_type": "official_chapter_directory",
            "document_date_or_tax_period": "2020-05-13",
            "locator": "PDF page 8; chapter 1003 Ryukyu Okinawa",
            "supports": "VFP chapter 1003 identity and chapter contacts Charles Douglas Lummis and Pete Doktor.",
            "does_not_support": "Earlier formation date; continuous officeholding outside the directory date; coalition relations.",
            "evidence_level_proposed": "E4",
            "archive_priority": "P0",
        },
        {
            "proposal_id": "USAP005",
            "url": "https://www.veteransforpeace.org/who-we-are/member-highlights/2021/02/08/okinawa-understanding-history-and-resistance-us-militarism",
            "source_owner": "Veterans For Peace",
            "source_type": "official_event_page",
            "document_date_or_tax_period": "2021-02-08",
            "locator": "webinar description and speaker biographies",
            "supports": "VFP-ROCK event carrier role; Lummis and Doktor chapter roles; Hideki Yoshikawa's simultaneous SDCC and OEJP roles.",
            "does_not_support": "Stable alliance among all event speakers; organization-level funding; membership of every speaker.",
            "evidence_level_proposed": "E4",
            "archive_priority": "P0",
        },
        {
            "proposal_id": "USAP006",
            "url": "https://www.veteransforpeace.org/files/8616/8433/7175/VFPNews_2023.Spring-FULL_SMALL_FIN.pdf",
            "source_owner": "Veterans For Peace",
            "source_type": "official_newsletter",
            "document_date_or_tax_period": "2023_spring",
            "locator": "PDF page 23; chapter 1003 report",
            "supports": "VFP chapter 1003 reports continuing work with a coalition including No Heliport Base Association and two other named Okinawa action groups.",
            "does_not_support": "Funding; legal membership in each group; automatic crosswalk of the two unresolved English labels.",
            "evidence_level_proposed": "E4",
            "archive_priority": "P0",
        },
        {
            "proposal_id": "USAP007",
            "url": "https://www.veteransforpeace.org/who-we-are/2025-online-business-meeting",
            "source_owner": "Veterans For Peace",
            "source_type": "official_governance_page",
            "document_date_or_tax_period": "2025",
            "locator": "Resolution 2025-1 listing",
            "supports": "National VFP governance agenda includes a resolution on U.S. military expansion and environmental destruction in Okinawa.",
            "does_not_support": "Chapter authorship or adoption outcome without the resolution record; funding.",
            "evidence_level_proposed": "E4",
            "archive_priority": "P1",
        },
    ]
    return add_common(rows)


def build_resource_observations() -> list[dict[str, str]]:
    return add_common(
        [
            {
                "resource_observation_id": "USAR001",
                "provider_actor_id": "",
                "receiver_actor_id": "A009",
                "associated_case_or_program": "R8C01 / project 1272 OKINAWA DUGONG",
                "amount": "276345.50",
                "currency": "USD",
                "year_or_period": "tax_year_2020",
                "resource_type": "court_awarded_attorney_fees_and_costs",
                "amount_semantics": "case-level receipt category reported by Earthjustice",
                "source_ref": "USAP001",
                "provider_identity_status": "not_stated_in_source",
                "receiver_identity_status": "registry_actor",
                "interpretation_limit": "Do not encode as a donation, grant, project budget, litigation expenditure, or payment from an Okinawa civic actor. Identify payer and award order separately before creating a directed money edge.",
                "review_priority": "P0",
            },
            {
                "resource_observation_id": "USAR002",
                "provider_actor_id": "X013",
                "receiver_actor_id": "",
                "associated_case_or_program": "Okinawa Youth Council Program / NAHA-PAS-02",
                "amount": "5000-10000",
                "currency": "USD",
                "year_or_period": "2024_opportunity",
                "resource_type": "grant_opportunity_ceiling_range",
                "amount_semantics": "opportunity range; no recipient or award observed",
                "source_ref": "S056;S082",
                "provider_identity_status": "program_node",
                "receiver_identity_status": "unknown_no_award_record",
                "interpretation_limit": "Keep outside directed funding graph until an official award and named recipient are found.",
                "review_priority": "P1",
            },
        ]
    )


def build_person_roles() -> list[dict[str, str]]:
    rows = [
        ("USAPN001", "Peter Galvin", "A045", "Pacific Director / public contact", "2003-09-25", "2003-09-25", "USAP003", "organization-authored filing announcement"),
        ("USAPN002", "Martin Wagner", "A009", "U.S. counsel / public contact", "2003-09-25", "2003-09-25", "USAP003", "case-specific role; not general organization leadership"),
        ("USAPN003", "Takenobu Tsuchida", "A003", "organization speaker", "2003-09-25", "2003-09-25", "USAP003", "identity crosswalk to A003 requires human confirmation"),
        ("USAPN004", "Takaaki Kagohashi", "A020", "organization speaker / legal collaborator", "2003-09-25", "2003-09-25", "USAP003", "does not make A020 counsel in R8C01; A020 remains plaintiff in the formal role table"),
        ("USAPN005", "Takuma Higashionna", "A076", "organization speaker", "2003-09-25", "2003-09-25", "USAP003", "person role does not transfer plaintiff status to similarly named A002"),
        ("USAPN006", "Charles Douglas Lummis", "A070", "chapter contact", "2020-05-13", "2020-05-13", "USAP004", "directory-date observation only"),
        ("USAPN007", "Pete Doktor", "A070", "chapter contact", "2020-05-13", "2020-05-13", "USAP004", "directory-date observation only"),
        ("USAPN008", "Hideki Yoshikawa", "A002", "International Director", "2021-02-08", "2021-02-08", "USAP005", "same public biography also names A001 role; candidate person bridge"),
        ("USAPN009", "Hideki Yoshikawa", "A001", "Director", "2021-02-08", "2021-02-08", "USAP005", "same public biography also names A002 role; candidate person bridge"),
        ("USAPN010", "Pete Shimazaki Doktor", "A070", "chapter 1003 co-founder", "", "2021-02-08", "USAP005", "formation date not stated; public biography observed in 2021"),
        ("USAPN011", "Doug Lummis", "A070", "chapter coordinator", "", "2021-02-08", "USAP005", "role observed in 2021; normalize person identity with USAPN006 only after human check"),
    ]
    return add_common(
        [
            {
                "person_role_observation_id": row[0],
                "person_name_as_source": row[1],
                "actor_id_candidate": row[2],
                "role_title_as_source": row[3],
                "role_start": row[4],
                "role_observed_at": row[5],
                "source_ref": row[6],
                "identity_or_time_limit": row[7],
                "review_priority": "P0" if row[2] in {"A001", "A002", "A070"} else "P1",
            }
            for row in rows
        ]
    )


def build_action_relations() -> list[dict[str, str]]:
    return add_common(
        [
            {
                "observation_id": "USAA001",
                "source_actor_id": "A045",
                "target_actor_id_or_label": "R8C01",
                "relation_family": "legal_case_role",
                "relation_type": "plaintiff",
                "event_or_program": "Okinawa Dugong litigation",
                "start_or_event_date": "2003-09-25",
                "end_or_last_observed": "2020-05-06",
                "source_ref": "R8R001;USAP002;USAP003",
                "status": "crosswalk_existing_human_checked_case_role",
                "graph_gate": "case_role_layer_only",
                "interpretation_limit": "Case role is not a stable alliance edge.",
            },
            {
                "observation_id": "USAA002",
                "source_actor_id": "A009",
                "target_actor_id_or_label": "R8C01",
                "relation_family": "legal_case_role",
                "relation_type": "counsel",
                "event_or_program": "Okinawa Dugong litigation",
                "start_or_event_date": "2003-09-25",
                "end_or_last_observed": "2020-05-06",
                "source_ref": "R8R005;USAP003",
                "status": "crosswalk_existing_human_checked_case_role",
                "graph_gate": "case_role_layer_only",
                "interpretation_limit": "Counsel role is case-specific; it is not a funder or plaintiff edge.",
            },
            {
                "observation_id": "USAA003",
                "source_actor_id": "A086",
                "target_actor_id_or_label": "R8C01",
                "relation_family": "legal_case_role",
                "relation_type": "plaintiff",
                "event_or_program": "Okinawa Dugong litigation",
                "start_or_event_date": "2003-09-25",
                "end_or_last_observed": "2020-05-06",
                "source_ref": "R8R002;USAP003",
                "status": "crosswalk_existing_human_checked_case_role",
                "graph_gate": "case_role_layer_only",
                "interpretation_limit": "Case role is not a stable alliance edge.",
            },
            {
                "observation_id": "USAA004",
                "source_actor_id": "A045",
                "target_actor_id_or_label": "Network for Okinawa (possible A028/JUCON crosswalk)",
                "relation_family": "coordination",
                "relation_type": "works_with",
                "event_or_program": "Okinawa dugong awareness campaign",
                "start_or_event_date": "",
                "end_or_last_observed": "page_observed_2026-08-19",
                "source_ref": "USAP002",
                "status": "candidate_endpoint_crosswalk_required",
                "graph_gate": "off_graph_until_endpoint_review",
                "interpretation_limit": "Do not map Network for Okinawa to A028 solely from name similarity.",
            },
            {
                "observation_id": "USAA005",
                "source_actor_id": "A070",
                "target_actor_id_or_label": "A019",
                "relation_family": "coordination",
                "relation_type": "recurring_coalition_work",
                "event_or_program": "Henoko/Camp Schwab opposition",
                "start_or_event_date": "",
                "end_or_last_observed": "2023_spring",
                "source_ref": "USAP006",
                "status": "candidate_human_review_required",
                "graph_gate": "research_relation_layer_after_identity_review",
                "interpretation_limit": "Official newsletter supports recurring work with a named coalition; it does not establish membership, funding, or a complete partner list.",
            },
            {
                "observation_id": "USAA006",
                "source_actor_id": "A070",
                "target_actor_id_or_label": "Protect Henoko/Takae (unresolved endpoint)",
                "relation_family": "coordination",
                "relation_type": "recurring_coalition_work",
                "event_or_program": "Henoko/Camp Schwab opposition",
                "start_or_event_date": "",
                "end_or_last_observed": "2023_spring",
                "source_ref": "USAP006",
                "status": "candidate_endpoint_unresolved",
                "graph_gate": "off_graph_until_endpoint_review",
                "interpretation_limit": "Do not force-map to A060 or another registry actor without identity evidence.",
            },
            {
                "observation_id": "USAA007",
                "source_actor_id": "A070",
                "target_actor_id_or_label": "Henoko Anti-Base Project (unresolved endpoint)",
                "relation_family": "coordination",
                "relation_type": "recurring_coalition_work",
                "event_or_program": "Henoko/Camp Schwab opposition",
                "start_or_event_date": "",
                "end_or_last_observed": "2023_spring",
                "source_ref": "USAP006",
                "status": "candidate_endpoint_unresolved",
                "graph_gate": "off_graph_until_endpoint_review",
                "interpretation_limit": "Keep the source label until an independent identity crosswalk exists.",
            },
            {
                "observation_id": "USAA008",
                "source_actor_id": "A070",
                "target_actor_id_or_label": "A001;A002",
                "relation_family": "event_participation",
                "relation_type": "webinar_carrier_and_speakers",
                "event_or_program": "Okinawa: Understanding the History and Resistance to U.S. Militarism",
                "start_or_event_date": "2021-02-15_Okinawa_time",
                "end_or_last_observed": "2021-02-15_Okinawa_time",
                "source_ref": "USAP005",
                "status": "candidate_event_observation",
                "graph_gate": "event_layer_only_after_review",
                "interpretation_limit": "Shared webinar participation does not prove a stable organization alliance.",
            },
            {
                "observation_id": "USAA009",
                "source_actor_id": "A033;A042;A045",
                "target_actor_id_or_label": "2015 NACSJ 31-NGO statement",
                "relation_family": "event_participation",
                "relation_type": "co_signing",
                "event_or_program": "Joint Urgent Statement Opposing Henoko New Base",
                "start_or_event_date": "2015-03-25",
                "end_or_last_observed": "2015-03-25",
                "source_ref": "S004",
                "status": "existing_event_level_evidence",
                "graph_gate": "event_layer_only",
                "interpretation_limit": "For A033 and A042 this remains the only located Okinawa-specific organization evidence in the bounded search; do not call it an ongoing program or alliance.",
            },
        ]
    )


def build_search_log() -> list[dict[str, str]]:
    rows = [
        ("USAS001", "A033", "site:foe.org Okinawa Henoko dugong Friends of the Earth U.S.", "official_domain_search", "No organization-authored Okinawa/Henoko page located in the bounded search; current annual-report results were organization-wide.", "not_found_bounded_search"),
        ("USAS002", "A042", "site:pacificenvironment.org Okinawa Henoko dugong", "official_domain_search", "No organization-authored Okinawa/Henoko page located in the bounded search.", "not_found_bounded_search"),
        ("USAS003", "A070", "site:veteransforpeace.org Okinawa chapter Doug Lummis", "official_domain_search", "Located official chapter directory, 2021 webinar, 2023 newsletter, and national governance records.", "positive_multiple_official_records"),
        ("USAS004", "X014", "site:ned.org Okinawa Japan grant", "official_domain_search", "No named Okinawa/Japan grant recipient located; current central evidence remains FY2024 list check only.", "not_found_bounded_search"),
        ("USAS005", "X013", "Grants.gov/USASpending award search by Okinawa Youth Council opportunity", "federal_award_search", "Existing records identify a notice of funding opportunity; no named award recipient is in the current evidence package.", "award_not_located_current_package"),
        ("USAS006", "A009", "official Form 990 search for Okinawa Dugong project", "official_financial_search", "Located FY2021 Form 990 Schedule O case-level court-awarded fee/cost amount.", "positive_case_level_amount"),
    ]
    return add_common(
        [
            {
                "search_id": row[0],
                "actor_id": row[1],
                "query_or_target": row[2],
                "search_scope": row[3],
                "result_summary": row[4],
                "result_status": row[5],
                "searched_at": AS_OF_DATE,
                "negative_result_limit": "A bounded search result describes the searched corpus, not real-world absence.",
            }
            for row in rows
        ]
    )


def build_review_queue() -> list[dict[str, str]]:
    rows = [
        ("USHR001", "P0", "resource_semantics", "USAR001", "Does the Form 990 wording support a case-level receipt observation exactly as coded, and can the payer/award order be identified?"),
        ("USHR002", "P0", "actor_identity_continuity", "A070;USAP004;USAP005;USAP006", "Approve A070 identity/continuity upgrade and the 2020/2021/2023 person-role observations?"),
        ("USHR003", "P0", "coordination_relation", "USAA005", "Approve A070→A019 as recurring coordination observed in the 2023 official VFP newsletter, without membership/funding semantics?"),
        ("USHR004", "P0", "person_bridge", "USAPN008;USAPN009", "Approve Hideki Yoshikawa's same-date A002/A001 roles as a person bridge?"),
        ("USHR005", "P1", "endpoint_crosswalk", "USAA004", "Is CBD's Network for Okinawa the same entity as A028/JUCON?"),
        ("USHR006", "P1", "endpoint_crosswalk", "USAA006;USAA007", "Resolve the two English coalition labels before any actor-to-actor edge is created."),
        ("USHR007", "P1", "scope_continuity", "A033;A042", "Keep both as event-level 2015 international participants unless organization-authored Okinawa continuity evidence is found?"),
        ("USHR008", "P1", "opportunity_award_boundary", "X013;USAR002", "Retain opportunity-only status and no directed funding edge?"),
        ("USHR009", "P1", "funder_negative_search", "X014", "Retain watchlist/no-public-evidence status after the bounded official grant-list search?"),
    ]
    return add_common(
        [
            {
                "review_item_id": row[0],
                "priority": row[1],
                "decision_family": row[2],
                "linked_rows": row[3],
                "decision_question": row[4],
                "principal_decision": "",
                "principal_note": "",
            }
            for row in rows
        ]
    )


def validate(
    actor_scope: Sequence[Mapping[str, str]],
    source_proposals: Sequence[Mapping[str, str]],
    resources: Sequence[Mapping[str, str]],
    people: Sequence[Mapping[str, str]],
    actions: Sequence[Mapping[str, str]],
    review_queue: Sequence[Mapping[str, str]],
    source_log: Sequence[Mapping[str, str]],
    case_roles: Sequence[Mapping[str, str]],
) -> None:
    assert [row["actor_id"] for row in actor_scope] == list(SCOPE_IDS)
    assert sum(
        row["counts_in_six_actor_accountability_subset"] == "yes"
        for row in actor_scope
    ) == 6
    assert len({row["proposal_id"] for row in source_proposals}) == len(
        source_proposals
    )
    earthjustice = next(
        row for row in resources if row["resource_observation_id"] == "USAR001"
    )
    assert earthjustice["resource_type"] == "court_awarded_attorney_fees_and_costs"
    assert earthjustice["provider_actor_id"] == ""
    assert "Do not encode as a donation" in earthjustice["interpretation_limit"]
    nofo = next(
        row for row in resources if row["resource_observation_id"] == "USAR002"
    )
    assert nofo["receiver_actor_id"] == ""
    assert "opportunity" in nofo["resource_type"]
    assert sum(row["person_name_as_source"] == "Hideki Yoshikawa" for row in people) == 2
    a070_a019 = next(row for row in actions if row["observation_id"] == "USAA005")
    assert a070_a019["status"] == "candidate_human_review_required"
    assert a070_a019["central_writeback"] == "no"
    assert all(row["principal_decision"] == "" for row in review_queue)
    existing_source_ids = {row["source_id"] for row in source_log}
    assert {"S004", "S056", "S082"}.issubset(existing_source_ids)
    existing_role_ids = {row["role_id"] for row in case_roles}
    assert {"R8R001", "R8R002", "R8R005"}.issubset(existing_role_ids)
    for rows in (actor_scope, source_proposals, resources, people, actions, review_queue):
        for row in rows:
            assert row["package_scope"] == "research_only"
            assert row["central_writeback"] == "no"


def write_csv(path: Path, rows: Sequence[Mapping[str, str]]) -> None:
    if not rows:
        raise ValueError(f"No rows for {path.name}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def render_readme(counts: Mapping[str, int]) -> str:
    return f"""# U.S.-presence accountability reconnaissance v1

Date: {AS_OF_DATE}

Status: `research_only / candidate_fact / no central writeback / not frontend-ready`

This package extends the U.S.-origin accountability/public-diplomacy side of the current database. It does not replace the six human-checked R8 case-role facts, and it does not approve any new actor, person bridge, coordination edge, award, recipient, or causal interpretation.

## Counts

- scoped U.S.-origin actors: {counts['actor_scope']} (six accountability actors plus one public-diplomacy program and one funder watchlist);
- new official-source proposals: {counts['sources']};
- typed resource observations: {counts['resources']};
- public person-role observations: {counts['people']};
- action/relation observations or existing-role crosswalks: {counts['actions']};
- bounded searches: {counts['searches']};
- principal review items: {counts['reviews']}.

## Reading order

1. `accountability_actor_scope_v1.csv`
2. `resource_observations_v1.csv`
3. `person_role_observations_v1.csv`
4. `action_relation_observations_v1.csv`
5. `official_source_proposals_v1.csv`
6. `bounded_search_log_v1.csv`
7. `human_review_queue_v1.csv`
8. `../../docs/us_presence_accountability_recon_brief_v1.md`

## Strongest new candidate facts

1. Earthjustice's official FY2021 Form 990 lists `1272 OKINAWA DUGONG` at USD 276,345.50 under court-awarded attorney fees and costs. It is not coded as a grant, donation, project budget, expenditure, or payment from an Okinawa group.
2. Official Veterans For Peace records identify chapter 1003 Ryukyu/Okinawa, named chapter contacts, a 2021 Okinawa webinar, and a 2023 report of continuing coalition work with named Okinawa anti-base groups. These can support a much denser people/coordination layer after human review.
3. Friends of the Earth U.S. and Pacific Environment remain visible in the bounded Okinawa corpus through the 2015 NACSJ statement; this wave did not locate organization-authored Okinawa continuity material on their official domains.

## Hard boundaries

- A case-level fee/cost amount is not a donor or funding-source identification.
- A funding opportunity is not an award.
- Shared event participation is not an alliance.
- Named coalition work is not membership or funding.
- A bounded negative search is not evidence of real-world absence.
- New source URLs stay in this proposal package until source-log/archive review.
"""


def render_brief() -> str:
    return """# 对美问责侧第一轮补强：从“参与过”到“谁在组织、谁在办案、资源如何进入”

日期：2026-08-19

状态：`research_only / principal review required`

## 本轮回答了什么

当前 database 的六个美国来源问责 actor，并不是同一种参与。

- Earthjustice、Center for Biological Diversity、Turtle Island Restoration Network 进入的是同一个可编号诉讼：两家是原告，一家是律师。案件角色已有 R8 人审支持。
- Veterans For Peace Ryukyu/Okinawa Chapter 是本地化的美国退伍军人反军事化节点。新找到的 VFP 官方目录、活动页和会报，已经能给出章节编号、负责人、公开活动和具名协调对象。
- Friends of the Earth U.S. 与 Pacific Environment 在当前冲绳语料中仍主要是 2015 年一次共同声明的参与者；第一轮官方域名检索没有把它们推进为可证明持续性的冲绳项目。

这使原来的“六个参与反基地行动的美国 NGO”可以拆成三种位置：案件型问责、在地化退伍军人行动、国际声明外围。以后画网络时不能把三类都画成同强度的组织节点。

## 新增的资源事实

Earthjustice 的官方 FY2021 Form 990 在“十大法院判给律师费及成本”中列出 `Okinawa Dugong`，金额 276,345.50 美元。这个数值说明诉讼不仅留下案件与判决，也留下了案件级资源记录。

但当前表故意不填资金提供者：990 本身没有在该行说明付款人，也没有把它写成捐赠、grant 或项目预算。下一步应从案件 docket 和 fee order 追出付款依据，再决定能否形成“付款方 → Earthjustice → 案件”的资金边。

## 新增的人物与组织接口

2003 年 CBD 官方起诉公告可以提取 Peter Galvin、Martin Wagner、土田 Takenobu、籠橋 Takaaki、東恩納 Takuma 五个案件公开角色。2021 年 VFP 官方活动页又明确写出：吉川秀樹同时担任 SDCC 国际事务负责人和 OEJP 负责人；Pete Doktor 是 VFP-ROCK 的共同创办人；Doug Lummis 是协调人。

这类人物记录比“组织共同署名”更接近甲方要求的社会网络分析，因为它能解释谁把美国法律组织、冲绳环保组织和退伍军人网络接在一起。现阶段它们仍是待人审人物—职务—时间观察，不直接进中央关系图。

## 对下一轮 database 的直接要求

1. 反基地侧要从 actor—issue 图升级为 `person → organization → role → time → source` 与 `organization → case/event → role → time → source`。
2. 资金层必须把 court award、grant、donation、sponsorship、contract、project cost 分表或至少分语义，不能再共用一个“支持关系”。
3. 美国来源 actor 需要一项 `Okinawa-specific continuity` 测量：一次署名、持续项目、本地章节、案件角色必须分开。
4. 对 Friends of the Earth U.S.、Pacific Environment 的当前定位应降为“事件参与可证，持续冲绳项目待证”，而不是仅凭国际知名度赋予中心性。
5. VFP-ROCK 值得成为第一个社会网络 tracer case：官方材料同时提供人物、章节、活动、跨组织协调和全国组织接口。

## 交负责人判断

`human_review_queue_v1.csv` 有 9 项。优先判断四项：Earthjustice 金额语义；A070 身份与连续性；A070→A019 协调边；吉川秀樹 A001/A002 双重职务。只有这四项通过，才值得把问责侧第一张“人物—组织—案件”图接入 database 与前端。
"""


def generate(output_dir: Path = OUTPUT_DIR) -> dict[str, int]:
    registry = read_csv(REGISTRY_PATH)
    source_log = read_csv(SOURCE_LOG_PATH)
    case_roles = read_csv(CASE_ROLES_PATH)

    actor_scope = build_actor_scope(registry)
    source_proposals = build_source_proposals()
    resources = build_resource_observations()
    people = build_person_roles()
    actions = build_action_relations()
    searches = build_search_log()
    reviews = build_review_queue()

    validate(
        actor_scope,
        source_proposals,
        resources,
        people,
        actions,
        reviews,
        source_log,
        case_roles,
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    outputs = {
        "accountability_actor_scope_v1.csv": actor_scope,
        "official_source_proposals_v1.csv": source_proposals,
        "resource_observations_v1.csv": resources,
        "person_role_observations_v1.csv": people,
        "action_relation_observations_v1.csv": actions,
        "bounded_search_log_v1.csv": searches,
        "human_review_queue_v1.csv": reviews,
    }
    for name, rows in outputs.items():
        write_csv(output_dir / name, rows)

    counts = {
        "actor_scope": len(actor_scope),
        "sources": len(source_proposals),
        "resources": len(resources),
        "people": len(people),
        "actions": len(actions),
        "searches": len(searches),
        "reviews": len(reviews),
    }
    (output_dir / "README.md").write_text(
        render_readme(counts), encoding="utf-8"
    )
    if output_dir.resolve() == OUTPUT_DIR.resolve():
        docs_path = ROOT / "docs" / "us_presence_accountability_recon_brief_v1.md"
        docs_path.write_text(render_brief(), encoding="utf-8")

    manifest_files = sorted(
        path for path in output_dir.iterdir() if path.is_file() and path.name != "manifest.json"
    )
    manifest = {
        "package_id": PACKAGE_ID,
        "as_of_date": AS_OF_DATE,
        "status": COMMON,
        "input_files": [
            {
                "path": path.as_posix(),
                "sha256": sha256(ROOT / path),
            }
            for path in INPUT_PATHS
        ],
        "counts": counts,
        "output_files": [
            {
                "path": f"outputs/{PACKAGE_ID}/{path.name}",
                "sha256": sha256(path),
            }
            for path in manifest_files
        ],
    }
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return counts


if __name__ == "__main__":
    print(json.dumps(generate(), ensure_ascii=False, indent=2))
