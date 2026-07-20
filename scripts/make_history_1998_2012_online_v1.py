#!/usr/bin/env python3
"""Build the isolated NR-05 1998-2012 online-history research package.

This builder is intentionally self-contained.  It writes only to the requested
output directory, never mutates central registries/source logs/edge tables, and
keeps every empirical row outside the frontend and central writeback gates.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
from collections import Counter
from html import escape
from pathlib import Path
from typing import Iterable, Mapping


DEFAULT_OUTPUT_DIR = Path("outputs/history_1998_2012_online_v1")
PACKAGE_DATE = "2026-07-20"
CONSTANTS = {
    "package_scope": "research_only",
    "claim_status": "candidate",
    "review_status": "ai_seeded",
    "frontend_eligibility": "not_frontend_ready",
    "central_writeback": "no",
}
ALLOWED_SOURCE_RELATIONSHIPS = {
    "contemporaneous_primary",
    "retrospective",
    "secondary",
    "lead",
}


ANCHOR_FIELDS = [
    "anchor_id",
    "anchor_type",
    "event_subtype",
    "actor_ids",
    "actor_names",
    "place",
    "domain_tags",
    "source_candidate_ids",
    "source_publication_date",
    "source_publication_date_precision",
    "event_date_start",
    "event_date_end",
    "event_date_precision",
    "actor_active_period",
    "claim_period",
    "source_relationship",
    "source_role_detail",
    "claim_text_candidate",
    "evidence_level_proposed",
    "relation_semantics_candidate",
    "relation_boundary",
    "competing_explanation",
    "continuity_boundary",
    "online_exhaustion_status",
    "local_or_new_primary_need",
    *CONSTANTS,
]

STATUS_FIELDS = [
    "status_candidate_id",
    "actor_id",
    "actor_name",
    "status_type",
    "status_value_candidate",
    "effective_date_start",
    "effective_date_end",
    "date_precision",
    "source_candidate_ids",
    "source_relationship",
    "legal_status_semantics",
    "competing_status_or_date",
    "continuity_boundary",
    "review_question",
    "needs_local_retrieval",
    *CONSTANTS,
]

SOURCE_FIELDS = [
    "source_candidate_id",
    "existing_source_id",
    "title",
    "publisher",
    "source_type",
    "url",
    "source_publication_date",
    "source_publication_date_precision",
    "document_coverage_period",
    "source_relationship",
    "exact_locator",
    "supports_anchor_ids",
    "supports_status_candidate_ids",
    "evidence_level_proposed",
    "support_scope",
    "interpretation_limit",
    "archive_or_access_status",
    "retrieval_date",
    *CONSTANTS,
]

GAP_FIELDS = [
    "gap_id",
    "actor_or_topic",
    "related_anchor_ids",
    "exhausted_question",
    "queries_and_domains_checked",
    "online_result",
    "why_not_closed",
    "needed_material",
    "priority",
    "task_destination",
    *CONSTANTS,
]

REVIEW_FIELDS = [
    "review_item_id",
    "object_type",
    "object_ids",
    "queue_role",
    "formal_hr_dispatch_status",
    "decision_scope",
    "review_question",
    "source_candidate_ids",
    "recommended_options",
    "ai_recommendation",
    "risk_if_overread",
    "human_decision",
    "reviewer",
    "review_date",
    "revision_note",
    *CONSTANTS,
]


def with_constants(row: Mapping[str, str]) -> dict[str, str]:
    merged = dict(row)
    merged.update(CONSTANTS)
    return merged


def historical_anchors() -> list[dict[str, str]]:
    rows = [
        {
            "anchor_id": "H98_001",
            "anchor_type": "contextual_baseline",
            "event_subtype": "course_fieldwork_interpretation",
            "actor_ids": "",
            "actor_names": "沖縄のNGO/NPO（調査対象集合）",
            "place": "Okinawa",
            "domain_tags": "history;documentation;organizational_capacity;anti_base;women;environment",
            "source_candidate_ids": "NR05S001",
            "source_publication_date": "1998",
            "source_publication_date_precision": "year",
            "event_date_start": "1996",
            "event_date_end": "1998",
            "event_date_precision": "fieldwork_year_to_publication_year",
            "actor_active_period": "not_applicable_population_commentary",
            "claim_period": "mid-1990s Okinawa as interpreted in a 1998 course-fieldwork article",
            "source_relationship": "secondary",
            "source_role_detail": "contemporaneous course-fieldwork commentary edited by the instructor",
            "claim_text_candidate": (
                "A 1998 Ryukyu University course-fieldwork article described weak financial/personnel "
                "bases, episodic activity and a missing intermediary-NGO layer, while interpreting many "
                "civic activities as converging on anti-base movements."
            ),
            "evidence_level_proposed": "E2",
            "relation_semantics_candidate": "contextual_baseline_not_actor_edge",
            "relation_boundary": "This is not a census; no organization, alliance, prevalence or population edge is created.",
            "competing_explanation": (
                "A 2001 survey of general environmental volunteer groups already found heterogeneous "
                "non-base activity and administrative collaboration; the 1998 article is not a census."
            ),
            "continuity_boundary": "Does not establish conditions after 1998 or a single lineage from anti-base to all NGOs.",
            "online_exhaustion_status": "online_context_located_needs_literature_comparison",
            "local_or_new_primary_need": "Original course instruments, interview roster and comparable 1990s surveys.",
        },
        {
            "anchor_id": "H98_002",
            "anchor_type": "institutional_context_series",
            "event_subtype": "prefecture_wide_npo_certification_counts",
            "actor_ids": "",
            "actor_names": "沖縄県内認証NPO法人（全分野）",
            "place": "Okinawa Prefecture",
            "domain_tags": "NPO_law;legal_status;documentation;institutionalization",
            "source_candidate_ids": "NR05S002;NR05S003;NR05S004",
            "source_publication_date": "2005-12-31;2012-10-31",
            "source_publication_date_precision": "day;day",
            "event_date_start": "1999",
            "event_date_end": "2012-10-31",
            "event_date_precision": "annual_series_with_exact_2012_endpoint",
            "actor_active_period": "not_applicable_aggregate_official_universe",
            "claim_period": "1999-2012-10-31",
            "source_relationship": "secondary",
            "source_role_detail": "RIETI compilation from Cabinet Office plus contemporaneous Okinawa official newsletter",
            "claim_text_candidate": (
                "The prefecture-wide cumulative certified-NPO-corporation count rose from 6 (1999) to 20, 37, 84, "
                "127 and 163 (2000-2004), reaching 550 corporations on 2012-10-31."
            ),
            "evidence_level_proposed": "E4 for 2012 official endpoint; E3 for compiled 1999-2004 series",
            "relation_semantics_candidate": "aggregate_context_not_actor_edge",
            "relation_boundary": "Counts cover all certified NPO corporations, not this project's base-accountability actors.",
            "competing_explanation": (
                "Rapid legal-NPO growth may reflect a broader welfare/service/administrative ecology, while "
                "base-accountability carriers remain informal, union-based or case-specific."
            ),
            "continuity_boundary": "Certification count is not organizational activity, survival, issue orientation or causal professionalization.",
            "online_exhaustion_status": "online_series_partially_closed",
            "local_or_new_primary_need": "Annual Okinawa certification/dissolution microdata for every year 1998-2012.",
        },
        {
            "anchor_id": "H98_003",
            "anchor_type": "organization_transition",
            "event_subtype": "intermediary_ngo_formation_to_npo_incorporation",
            "actor_ids": "X010",
            "actor_names": "沖縄NGOセンター（旧・沖縄NGO活動推進協議会）",
            "place": "Okinawa; Ginowan",
            "domain_tags": "international_cooperation;intermediary_support;NPO_law;multicultural",
            "source_candidate_ids": "NR05S005;NR05S006;NR05S007;NR05S031",
            "source_publication_date": ";2022;2006;",
            "source_publication_date_precision": "undated;year;year;current_database",
            "event_date_start": "1999-06",
            "event_date_end": "2009-05-14",
            "event_date_precision": "month_start_to_day_end_with_disputed_2008_intermediate_claim",
            "actor_active_period": "1999-06 onward claimed by current organization sources",
            "claim_period": "1999 formation; 2008 retrospective transition claim; official certification 2009-05-14",
            "source_relationship": "retrospective",
            "source_role_detail": "current organization profile plus later institutional interview and JICA program report",
            "claim_text_candidate": (
                "ONC reports a June 1999 start; a 2022 institutional interview says it began as "
                "沖縄NGO活動推進協議会 and obtained NPO法人 status/current name in 2008; the official "
                "NPO portal instead records the legal certification date as 2009-05-14."
            ),
            "evidence_level_proposed": "E4 for official certification date; E3 for retrospective lineage/2008 claim",
            "relation_semantics_candidate": "predecessor_name_and_legal_transition_candidate",
            "relation_boundary": "Do not encode simple rename/same-actor continuity until charter and certification records are checked.",
            "competing_explanation": (
                "The 2008 account may refer to an internal resolution, application or name-transition stage, "
                "while 2009-05-14 is the official legal-certification date. This is also a non-base "
                "international-cooperation/intermediary trajectory."
            ),
            "continuity_boundary": "No claim that the 1998 course article caused ONC's formation or that staff/membership stayed constant.",
            "online_exhaustion_status": "online_retrospective_sources_located",
            "local_or_new_primary_need": "1999 founding charter/minutes; 2008 internal transition/application record; 2009 certification file.",
        },
        {
            "anchor_id": "H98_004",
            "anchor_type": "litigation_round",
            "event_subtype": "futenma_first_noise_litigation",
            "actor_ids": "A053",
            "actor_names": "普天間基地爆音訴訟団",
            "place": "Futenma; Ginowan",
            "domain_tags": "noise;life_safety;legal;anti_base",
            "source_candidate_ids": "NR05S008;NR05S009",
            "source_publication_date": ";2022-03-10",
            "source_publication_date_precision": "undated;day",
            "event_date_start": "2002",
            "event_date_end": "2003",
            "event_date_precision": "year_range",
            "actor_active_period": "round-specific participation; organizational continuity not re-adjudicated here",
            "claim_period": "first Futenma noise-litigation filing period 2002-2003",
            "source_relationship": "retrospective",
            "source_role_detail": "current plaintiff-group chronology cross-checked against later court judgment",
            "claim_text_candidate": (
                "The current plaintiff-group page compresses the first round to 2002, while the 2022 court "
                "judgment records filings by residents in 2002 and 2003."
            ),
            "evidence_level_proposed": "E4 for case chronology; E3 for organization-round crosswalk in this package",
            "relation_semantics_candidate": "round_of_candidate",
            "relation_boundary": "A litigation round is not a new actor and does not imply identical plaintiffs across dates.",
            "competing_explanation": "Website chronology may use launch year while court chronology records multiple filings.",
            "continuity_boundary": "Central HR-012 remains authoritative; NR-05 does not reapprove cross-round continuity.",
            "online_exhaustion_status": "online_case_chronology_located",
            "local_or_new_primary_need": "Original complaints and first-round plaintiff-group charter/roster.",
        },
        {
            "anchor_id": "H98_005",
            "anchor_type": "legal_case_entry",
            "event_subtype": "okinawa_dugong_us_federal_filing",
            "actor_ids": "A009;A020;A045;A076;A086",
            "actor_names": "Okinawa Dugong v. Rumsfeld named organizational parties/counsel",
            "place": "Henoko; Oura Bay; U.S. federal court",
            "domain_tags": "dugong;environment;legal;international;Henoko",
            "source_candidate_ids": "NR05S010;NR05S011",
            "source_publication_date": "2003-09-25;2003-09-25",
            "source_publication_date_precision": "day;day",
            "event_date_start": "2003-09-25",
            "event_date_end": "2003-09-25",
            "event_date_precision": "day",
            "actor_active_period": "case-specific roles only",
            "claim_period": "filing date",
            "source_relationship": "contemporaneous_primary",
            "source_role_detail": "same-day counsel release and filed complaint",
            "claim_text_candidate": "Named plaintiffs and counsel entered a U.S. federal NHPA venue on 2003-09-25.",
            "evidence_level_proposed": "E4",
            "relation_semantics_candidate": "case_role_not_alliance",
            "relation_boundary": "Joint case presence is case-specific; A002 and A019 remain organizational non-parties.",
            "competing_explanation": "International visibility may reflect legal-document survival and English-language publication capacity.",
            "continuity_boundary": "No stable alliance, causal pathway or role transfer to affiliated individuals/organizations.",
            "online_exhaustion_status": "online_primary_case_entry_closed",
            "local_or_new_primary_need": "None for filing occurrence; local materials needed for movement-side deliberation before filing.",
        },
        {
            "anchor_id": "H98_006",
            "anchor_type": "institutional_nonentry",
            "event_subtype": "pollution_mediation_jurisdictional_exclusion",
            "actor_ids": "",
            "actor_names": "913名申請人（個人集合；組織化禁止）",
            "place": "Henoko/Oura Bay; Okinawa Prefecture Pollution Review Board",
            "domain_tags": "environment;legal;administrative_procedure;nonentry;Henoko",
            "source_candidate_ids": "NR05S012",
            "source_publication_date": "",
            "source_publication_date_precision": "undated",
            "event_date_start": "2004-02-03",
            "event_date_end": "2004-03-30",
            "event_date_precision": "day_range",
            "actor_active_period": "not_applicable_anonymous_applicant_collective",
            "claim_period": "administrative mediation intake and dismissal",
            "source_relationship": "retrospective",
            "source_role_detail": "current official terminated-case record",
            "claim_text_candidate": (
                "An official record lists 913 applicants, acceptance on 2004-02-03, three mediation sessions, "
                "and dismissal on 2004-03-30 because the defense-facility dispute was outside the statutory venue."
            ),
            "evidence_level_proposed": "E4",
            "relation_semantics_candidate": "procedural_nonentry_not_actor_edge",
            "relation_boundary": "The 913 applicants are not converted into an organization or registry actor.",
            "competing_explanation": "Nonentry may arise from venue design rather than claim weakness or movement failure.",
            "continuity_boundary": "No link to a named organization without an application/case file.",
            "online_exhaustion_status": "online_official_outcome_located",
            "local_or_new_primary_need": "Application, applicant representation documents and mediation minutes.",
        },
        {
            "anchor_id": "H98_007",
            "anchor_type": "onsite_action",
            "event_subtype": "henoko_sit_in_and_maritime_obstruction_start",
            "actor_ids": "A019",
            "actor_names": "ヘリ基地反対協議会",
            "place": "Henoko fishing port",
            "domain_tags": "Henoko;anti_base;direct_action;maritime_action",
            "source_candidate_ids": "NR05S013;NR05S014",
            "source_publication_date": ";2007-03-10",
            "source_publication_date_precision": "undated;day",
            "event_date_start": "2004-04-19",
            "event_date_end": "2004-04-19",
            "event_date_precision": "day",
            "actor_active_period": "event role on 2004-04-19; later duration not inferred here",
            "claim_period": "start of documented sit-in/obstruction episode",
            "source_relationship": "secondary",
            "source_role_detail": "current organization chronology plus near-period participant-observation reconstruction",
            "claim_text_candidate": "A sit-in/obstruction episode at Henoko began on 2004-04-19.",
            "evidence_level_proposed": "E3",
            "relation_semantics_candidate": "event_role_not_membership",
            "relation_boundary": "Participants at the site are not automatically A019 members or partner organizations.",
            "competing_explanation": "The event may have involved several carriers; present organizational pages can simplify attribution.",
            "continuity_boundary": "Do not backfill the entire 2004-present site history into one unchanged organization.",
            "online_exhaustion_status": "online_date_corroborated",
            "local_or_new_primary_need": "Contemporaneous tent log, flyers, roster and local newspaper coverage.",
        },
        {
            "anchor_id": "H98_008",
            "anchor_type": "procedural_entry",
            "event_subtype": "eia_method_statement_comment",
            "actor_ids": "A004",
            "actor_names": "日本自然保護協会（NACS-J）",
            "place": "Henoko/Oura Bay; Japanese EIA procedure",
            "domain_tags": "environment;EIA;Henoko;legal_procedure",
            "source_candidate_ids": "NR05S015",
            "source_publication_date": "2004-06-10",
            "source_publication_date_precision": "day",
            "event_date_start": "2004-06-10",
            "event_date_end": "2004-06-10",
            "event_date_precision": "day",
            "actor_active_period": "commenter role on dated submission",
            "claim_period": "method-statement comment stage",
            "source_relationship": "contemporaneous_primary",
            "source_role_detail": "dated organization statement/formal opinion",
            "claim_text_candidate": "NACS-J submitted a dated opinion on the EIA method statement on 2004-06-10.",
            "evidence_level_proposed": "E4",
            "relation_semantics_candidate": "procedural_commenter",
            "relation_boundary": "Formal comment does not imply alliance, project suspension or acceptance of the opinion.",
            "competing_explanation": "The durable trace comes from a formal procedure and an organization-hosted archive.",
            "continuity_boundary": "No generalized EIA role beyond the named submission.",
            "online_exhaustion_status": "online_primary_submission_closed",
            "local_or_new_primary_need": "Agency receipt register and contemporaneous local-group submissions for comparison.",
        },
        {
            "anchor_id": "H98_009",
            "anchor_type": "legal_case_entry",
            "event_subtype": "awase_first_wave_public_funds_litigation",
            "actor_ids": "",
            "actor_names": "個人住民原告；A055は後続報道でsupport/movement roleのみ",
            "place": "Awase; Naha District Court",
            "domain_tags": "Awase;environment;public_funds;legal",
            "source_candidate_ids": "NR05S016;NR05S017",
            "source_publication_date": ";2005-07-21",
            "source_publication_date_precision": "unknown;day",
            "event_date_start": "2005-05-20",
            "event_date_end": "2005-05-20",
            "event_date_precision": "day",
            "actor_active_period": "movement/support role around first-wave filing",
            "claim_period": "first-wave filing",
            "source_relationship": "retrospective",
            "source_role_detail": "later court judgment cross-checked with near-period hearing report",
            "claim_text_candidate": (
                "Individual resident plaintiffs filed the first-wave Awase public-funds litigation on "
                "2005-05-20. A055 appears only through its co-representatives' later public movement/support "
                "role and is not the organizational plaintiff."
            ),
            "evidence_level_proposed": "E4 for filing; E3 for A055 supporter role",
            "relation_semantics_candidate": "supporter_not_organizational_plaintiff",
            "relation_boundary": "A055 is not encoded as the named organizational plaintiff.",
            "competing_explanation": "Movement spokespeople appearing at hearings can be mistaken for a corporate plaintiff.",
            "continuity_boundary": "First- and second-wave results and plaintiff sets remain separate.",
            "online_exhaustion_status": "online_filing_date_closed_role_bounded",
            "local_or_new_primary_need": "Original complaints and movement minutes identifying supporter/counsel/plaintiff boundaries.",
        },
        {
            "anchor_id": "H98_010",
            "anchor_type": "request_action",
            "event_subtype": "women_human_rights_prefectural_request",
            "actor_ids": "A115",
            "actor_names": "新日本婦人の会沖縄県本部",
            "place": "Okinawa Prefectural Government",
            "domain_tags": "women;human_rights;sexual_violence;anti_base;request",
            "source_candidate_ids": "NR05S018",
            "source_publication_date": "2008",
            "source_publication_date_precision": "year_document",
            "event_date_start": "2008-02-14",
            "event_date_end": "2008-02-14",
            "event_date_precision": "day",
            "actor_active_period": "branch-level dated action only",
            "claim_period": "2008-02-14 request",
            "source_relationship": "contemporaneous_primary",
            "source_role_detail": "prefectural administrative diary",
            "claim_text_candidate": "The Okinawa prefectural branch made a request concerning a U.S.-Marine sexual-assault case on 2008-02-14.",
            "evidence_level_proposed": "E4 for occurrence; content beyond diary entry unverified",
            "relation_semantics_candidate": "requester_to_public_authority",
            "relation_boundary": "The diary confirms a request, not its full text, government response, outcome or alliance.",
            "competing_explanation": "Branch action must not be transferred to the national parent organization.",
            "continuity_boundary": "No claim about uninterrupted branch activity before or after this date.",
            "online_exhaustion_status": "online_occurrence_closed_content_open",
            "local_or_new_primary_need": "Request text, branch newsletter and prefectural response file.",
        },
        {
            "anchor_id": "H98_011",
            "anchor_type": "joint_statement_event",
            "event_subtype": "wwf_67_group_henoko_statement",
            "actor_ids": "A005",
            "actor_names": "WWF Japan and 67 listed domestic organizations",
            "place": "Henoko/Oura Bay; national ministries",
            "domain_tags": "dugong;environment;Henoko;co_signing;request",
            "source_candidate_ids": "NR05S019",
            "source_publication_date": "2010-05-14",
            "source_publication_date_precision": "day",
            "event_date_start": "2010-05-14",
            "event_date_end": "2010-05-14",
            "event_date_precision": "day",
            "actor_active_period": "event-level participation only",
            "claim_period": "dated statement/submission",
            "source_relationship": "contemporaneous_primary",
            "source_role_detail": "same-day organization statement and participant list",
            "claim_text_candidate": "A 67-organization domestic statement was issued/submitted on 2010-05-14.",
            "evidence_level_proposed": "E4 for listed event participation",
            "relation_semantics_candidate": "event_hyperedge_co_signing",
            "relation_boundary": "Co-signing is not a stable alliance, membership, coordination edge or shared organization.",
            "competing_explanation": "A durable WWF-hosted list can inflate apparent bridge centrality relative to undocumented local events.",
            "continuity_boundary": "No persistence before or after the statement.",
            "online_exhaustion_status": "online_primary_event_list_closed",
            "local_or_new_primary_need": "Organizer correspondence only if coordination mechanism is studied.",
        },
        {
            "anchor_id": "H98_012",
            "anchor_type": "litigation_round",
            "event_subtype": "kadena_third_noise_litigation",
            "actor_ids": "A052",
            "actor_names": "嘉手納基地爆音差止訴訟原告団",
            "place": "Kadena; Naha District Court Okinawa Branch",
            "domain_tags": "noise;life_safety;legal;anti_base",
            "source_candidate_ids": "NR05S020",
            "source_publication_date": "",
            "source_publication_date_precision": "undated",
            "event_date_start": "2011-04-28",
            "event_date_end": "2011-04-28",
            "event_date_precision": "day",
            "actor_active_period": "third-round role; participant identity varies",
            "claim_period": "third-round filing",
            "source_relationship": "retrospective",
            "source_role_detail": "current official plaintiff-group history",
            "claim_text_candidate": "The third Kadena noise-litigation round was filed on 2011-04-28.",
            "evidence_level_proposed": "E4 for chronology; E3 for this package's round relation",
            "relation_semantics_candidate": "round_of_candidate",
            "relation_boundary": "Round label is not a separate actor and does not imply identical plaintiffs.",
            "competing_explanation": "Current group history may emphasize institutional continuity over participant turnover.",
            "continuity_boundary": "Central HR-012 remains authoritative; no lifecycle rewrite from NR-05.",
            "online_exhaustion_status": "online_official_chronology_closed",
            "local_or_new_primary_need": "Third-round complaint, plaintiff-group bylaws and roster change documentation.",
        },
        {
            "anchor_id": "H98_013",
            "anchor_type": "public_meeting",
            "event_subtype": "miyako_shimojishima_anti_deployment_meeting",
            "actor_ids": "A096",
            "actor_names": "下地島空港の軍事利用に反対する会",
            "place": "Miyako; Shimojishima",
            "domain_tags": "Sakishima;self_defense;anti_militarization;peace;public_meeting",
            "source_candidate_ids": "NR05S021",
            "source_publication_date": "2011-06-25",
            "source_publication_date_precision": "day",
            "event_date_start": "2011-06-23",
            "event_date_end": "2011-06-23",
            "event_date_precision": "day",
            "actor_active_period": "event role only",
            "claim_period": "meeting date",
            "source_relationship": "secondary",
            "source_role_detail": "near-contemporaneous local newspaper report",
            "claim_text_candidate": "A096 hosted a meeting opposing a Shimojishima SDF-use proposal on 2011-06-23.",
            "evidence_level_proposed": "E3 for event; organization continuity remains E2/E3",
            "relation_semantics_candidate": "event_host_not_coalition",
            "relation_boundary": "Attendance and shared views do not generate membership or stable alliance edges.",
            "competing_explanation": "The article may capture an event carrier without establishing an enduring organization.",
            "continuity_boundary": "Formation, officers and post-event survival are unknown.",
            "online_exhaustion_status": "online_event_date_closed_identity_open",
            "local_or_new_primary_need": "Flyer, minutes, organizer contact and subsequent local press.",
        },
        {
            "anchor_id": "H98_014",
            "anchor_type": "litigation_round",
            "event_subtype": "futenma_second_noise_litigation",
            "actor_ids": "A053",
            "actor_names": "普天間基地爆音訴訟団",
            "place": "Futenma; Ginowan",
            "domain_tags": "noise;life_safety;legal;anti_base",
            "source_candidate_ids": "NR05S008;NR05S009",
            "source_publication_date": ";2022-03-10",
            "source_publication_date_precision": "undated;day",
            "event_date_start": "2012",
            "event_date_end": "2013",
            "event_date_precision": "year_range_with_2012_launch_label",
            "actor_active_period": "second-round label; participant identity varies",
            "claim_period": "2012 launch claim; later court chronology records 2012-2013 filings",
            "source_relationship": "retrospective",
            "source_role_detail": "current plaintiff-group chronology cross-checked against later court judgment",
            "claim_text_candidate": (
                "The organization history labels the second round as 2012; the court judgment records two "
                "plaintiff groups filing related Futenma cases across 2012 and 2013."
            ),
            "evidence_level_proposed": "E4 for case chronology; E3 for organization-round crosswalk here",
            "relation_semantics_candidate": "round_of_candidate_with_parallel_case_warning",
            "relation_boundary": "Do not collapse two plaintiff groups/case forms or infer identical participants.",
            "competing_explanation": "A simplified public round label can hide parallel compensation-only and injunction/damages cases.",
            "continuity_boundary": "Central HR-012 remains authoritative; NR-05 does not create or merge actors.",
            "online_exhaustion_status": "online_case_structure_partially_closed",
            "local_or_new_primary_need": "2012/2013 complaints and official plaintiff-group organizational records.",
        },
        {
            "anchor_id": "H98_015",
            "anchor_type": "temporary_committee_formation",
            "event_subtype": "yonaguni_opinion_ad_committee",
            "actor_ids": "A015",
            "actor_names": "与那国島への自衛隊配備に反対する意見広告実行委員会",
            "place": "Yonaguni; Yaeyama",
            "domain_tags": "Sakishima;Yonaguni;self_defense;opinion_ad;labor;peace",
            "source_candidate_ids": "NR05S022",
            "source_publication_date": "2012-08-31",
            "source_publication_date_precision": "day",
            "event_date_start": "2012-08-25",
            "event_date_end": "2012-08-25",
            "event_date_precision": "day",
            "actor_active_period": "founding-event claim only",
            "claim_period": "founding press conference and planned opinion ad",
            "source_relationship": "lead",
            "source_role_detail": "party newspaper report; original ad and organization records not found online",
            "claim_text_candidate": "A party newspaper reports a founding press conference on 2012-08-25 for an anti-deployment opinion-ad committee.",
            "evidence_level_proposed": "E2",
            "relation_semantics_candidate": "temporary_event_carrier_not_alliance",
            "relation_boundary": "Mention of peace groups/unions does not create membership or stable-alliance edges.",
            "competing_explanation": "The committee may have been a one-off event vehicle rather than a continuing organization.",
            "continuity_boundary": "Identity, officers beyond reported co-representatives, ad execution and survival remain unverified.",
            "online_exhaustion_status": "online_exhausted_single_nonindependent_source",
            "local_or_new_primary_need": "Original opinion ad, Yaeyama newspapers, committee materials and local archive.",
        },
    ]
    return [with_constants(row) for row in rows]


def organization_status_candidates() -> list[dict[str, str]]:
    rows = [
        {
            "status_candidate_id": "NR05OS001",
            "actor_id": "X010",
            "actor_name": "沖縄NGOセンター",
            "status_type": "formation_and_legal_transition",
            "status_value_candidate": (
                "1999-06 voluntary intermediary body; retrospective account places NPO/current-name "
                "transition in 2008; official certification date is 2009-05-14"
            ),
            "effective_date_start": "1999-06",
            "effective_date_end": "2009-05-14",
            "date_precision": "month_start_to_day_end_with_disputed_2008_stage",
            "source_candidate_ids": "NR05S005;NR05S006;NR05S007;NR05S031",
            "source_relationship": "retrospective",
            "legal_status_semantics": "Formation date and NPO certification date are distinct.",
            "competing_status_or_date": (
                "2022 interview says NPO status/current-name transition in 2008; official portal records "
                "設立認証年月日 2009-05-14. Internal resolution/application/name stage must be separated "
                "from legal certification."
            ),
            "continuity_boundary": "Do not encode simple rename or unchanged membership without charter/certification records.",
            "review_question": "How should 1999 formation, the 2008 retrospective transition claim and 2009-05-14 official certification be separated?",
            "needs_local_retrieval": "yes_new_primary",
        },
        {
            "status_candidate_id": "NR05OS002",
            "actor_id": "A076",
            "actor_name": "ジュゴン保護基金委員会（Save the Dugong Foundation）",
            "status_type": "formation_claim",
            "status_value_candidate": "informal Okinawa-based nonprofit formed in 1999",
            "effective_date_start": "1999",
            "effective_date_end": "1999",
            "date_precision": "year",
            "source_candidate_ids": "NR05S011;NR05S023",
            "source_relationship": "retrospective",
            "legal_status_semantics": "The complaint's 'nonprofit' wording does not establish Japanese法人格.",
            "competing_status_or_date": "A newspaper dictionary suggests October 1999; exact month remains unclosed.",
            "continuity_boundary": "A party pleading supports self-description at filing, not present continuity.",
            "review_question": "Is 1999 sufficient as a bounded formation year, with legal form unresolved?",
            "needs_local_retrieval": "yes_local_charter",
        },
        {
            "status_candidate_id": "NR05OS003",
            "actor_id": "A055",
            "actor_name": "泡瀬干潟を守る連絡会",
            "status_type": "formation_claim",
            "status_value_candidate": "informal organization formed 2001-01",
            "effective_date_start": "2001-01",
            "effective_date_end": "2001-01",
            "date_precision": "month",
            "source_candidate_ids": "NR05S024",
            "source_relationship": "retrospective",
            "legal_status_semantics": "Current institutional directory labels an organization; no法人格 claimed.",
            "competing_status_or_date": "Contemporaneous charter/date not found online.",
            "continuity_boundary": "Formation does not make A055 an organizational plaintiff in Awase litigation.",
            "review_question": "Accept month-level formation while preserving supporter/plaintiff separation?",
            "needs_local_retrieval": "yes_local_charter",
        },
        {
            "status_candidate_id": "NR05OS004",
            "actor_id": "A088",
            "actor_name": "特定非営利活動法人沖縄平和協力センター",
            "status_type": "npo_certification",
            "status_value_candidate": "specified nonprofit corporation certified 2002-10-17",
            "effective_date_start": "2002-10-17",
            "effective_date_end": "2002-10-17",
            "date_precision": "day",
            "source_candidate_ids": "NR05S025",
            "source_relationship": "retrospective",
            "legal_status_semantics": "Certification is a legal-status event, not necessarily the organization's start.",
            "competing_status_or_date": "Pre-certification organizational activity not established by the portal.",
            "continuity_boundary": "Current portal presence does not prove uninterrupted activity since certification.",
            "review_question": "Accept certification date while leaving formation/continuity blank?",
            "needs_local_retrieval": "yes_historical_annual_reports",
        },
        {
            "status_candidate_id": "NR05OS005",
            "actor_id": "A069",
            "actor_name": "沖縄ジュゴン環境アセスメント監視団",
            "status_type": "formation_claim",
            "status_value_candidate": "informal monitoring group formed 2003-09",
            "effective_date_start": "2003-09",
            "effective_date_end": "2003-09",
            "date_precision": "month",
            "source_candidate_ids": "NR05S014;NR05S026",
            "source_relationship": "secondary",
            "legal_status_semantics": "Academic reconstruction/catalog locator does not establish法人格 or exact roster.",
            "competing_status_or_date": "A later chronology suggests 2003-09-23, but primary formation record is absent.",
            "continuity_boundary": "Do not infer activity after the sourced period from name persistence.",
            "review_question": "Keep month-level formation as E2/E3 candidate or defer to local primary material?",
            "needs_local_retrieval": "yes_local_charter",
        },
        {
            "status_candidate_id": "NR05OS006",
            "actor_id": "C034_background",
            "actor_name": "沖縄県サンゴ礁保全推進協議会",
            "status_type": "platform_formation",
            "status_value_candidate": "administrative-civic coral platform formed in 2008",
            "effective_date_start": "2008-05-18",
            "effective_date_end": "2008-06-28",
            "date_precision": "two_documented_milestones",
            "source_candidate_ids": "NR05S027;NR05S028",
            "source_relationship": "retrospective",
            "legal_status_semantics": "Charter date and establishment-meeting date must be stored separately.",
            "competing_status_or_date": "Prefecture page says May 2008; organization history identifies 2008-06-28 establishment meeting.",
            "continuity_boundary": "Administrative collaboration does not imply an anti-base stance.",
            "review_question": "Which milestone should define formed_date, and should the other be an event anchor?",
            "needs_local_retrieval": "no_online_primary_report_available",
        },
        {
            "status_candidate_id": "NR05OS007",
            "actor_id": "A052",
            "actor_name": "嘉手納基地爆音差止訴訟原告団",
            "status_type": "case_round_label",
            "status_value_candidate": "third litigation round filed 2011-04-28",
            "effective_date_start": "2011-04-28",
            "effective_date_end": "2011-04-28",
            "date_precision": "day",
            "source_candidate_ids": "NR05S020",
            "source_relationship": "retrospective",
            "legal_status_semantics": "Round label is a nonidentity relation, not a new法人/actor.",
            "competing_status_or_date": "Participant composition can change even when the public organization claims continuity.",
            "continuity_boundary": "Central HR-012 governs; NR-05 does not alter lifecycle or membership.",
            "review_question": "Retain as a round anchor only, with no new actor?",
            "needs_local_retrieval": "yes_if_membership_change_is_studied",
        },
        {
            "status_candidate_id": "NR05OS008",
            "actor_id": "A053",
            "actor_name": "普天間基地爆音訴訟団",
            "status_type": "case_round_labels",
            "status_value_candidate": "first-round 2002-2003; second-round launch 2012 with related 2013 filings",
            "effective_date_start": "2002",
            "effective_date_end": "2013",
            "date_precision": "year_ranges",
            "source_candidate_ids": "NR05S008;NR05S009",
            "source_relationship": "retrospective",
            "legal_status_semantics": "Round/case labels do not create separate actors or identical memberships.",
            "competing_status_or_date": "Current site compresses chronology; court record distinguishes multiple filings/groups.",
            "continuity_boundary": "Central HR-012 governs; parallel cases remain visible.",
            "review_question": "Approve only the date/range correction without reopening the actor crosswalk?",
            "needs_local_retrieval": "yes_original_complaints",
        },
        {
            "status_candidate_id": "NR05OS009",
            "actor_id": "A096",
            "actor_name": "下地島空港の軍事利用に反対する会",
            "status_type": "minimum_active_date",
            "status_value_candidate": "publicly active by 2011-06-23",
            "effective_date_start": "2011-06-23",
            "effective_date_end": "2011-06-23",
            "date_precision": "day_event_only",
            "source_candidate_ids": "NR05S021",
            "source_relationship": "secondary",
            "legal_status_semantics": "Event hosting is not a legal-status or formation record.",
            "competing_status_or_date": "Group may predate the event or have been a temporary carrier.",
            "continuity_boundary": "No before/after continuity inferred.",
            "review_question": "Use as minimum_active_date only?",
            "needs_local_retrieval": "yes_local_materials",
        },
        {
            "status_candidate_id": "NR05OS010",
            "actor_id": "A015",
            "actor_name": "与那国島への自衛隊配備に反対する意見広告実行委員会",
            "status_type": "temporary_committee_formation_claim",
            "status_value_candidate": "reported founding press conference 2012-08-25",
            "effective_date_start": "2012-08-25",
            "effective_date_end": "2012-08-25",
            "date_precision": "day",
            "source_candidate_ids": "NR05S022",
            "source_relationship": "lead",
            "legal_status_semantics": "Implementation committee presumed temporary until primary records show continuity.",
            "competing_status_or_date": "Only one party-newspaper source; original ad unavailable online.",
            "continuity_boundary": "No merger with referendum body or later anti-deployment groups.",
            "review_question": "Defer identity/continuity until local newspaper and ad are retrieved?",
            "needs_local_retrieval": "yes_tier2",
        },
        {
            "status_candidate_id": "NR05OS011",
            "actor_id": "A115",
            "actor_name": "新日本婦人の会沖縄県本部",
            "status_type": "minimum_active_date",
            "status_value_candidate": "prefectural branch publicly active by 2008-02-14",
            "effective_date_start": "2008-02-14",
            "effective_date_end": "2008-02-14",
            "date_precision": "day_event_only",
            "source_candidate_ids": "NR05S018",
            "source_relationship": "contemporaneous_primary",
            "legal_status_semantics": "Branch action confirms local presence, not formation or independent法人格.",
            "competing_status_or_date": "Earlier branch history may exist offline.",
            "continuity_boundary": "National actions are not transferred to the prefectural branch.",
            "review_question": "Use as minimum_active_date and request occurrence only?",
            "needs_local_retrieval": "yes_branch_archive",
        },
    ]
    return [with_constants(row) for row in rows]


def source_candidates() -> list[dict[str, str]]:
    rows = [
        {
            "source_candidate_id": "NR05S001",
            "existing_source_id": "",
            "title": "政策科学・国際関係論専攻における社会学的フィールドワークの可能性",
            "publisher": "琉球大学法文学部",
            "source_type": "academic_course_fieldwork_article",
            "url": "https://u-ryukyu.repo.nii.ac.jp/record/2002381/files/No1p109.pdf",
            "source_publication_date": "1998",
            "source_publication_date_precision": "year",
            "document_coverage_period": "1996 fieldwork; 1998 publication",
            "source_relationship": "secondary",
            "exact_locator": "printed pp.132-133 / PDF pp.24-25, section 3「沖縄のNGO」",
            "supports_anchor_ids": "H98_001",
            "supports_status_candidate_ids": "",
            "evidence_level_proposed": "E2",
            "support_scope": "Contemporaneous interpretive baseline on perceived NGO capacity and intermediary gap.",
            "interpretation_limit": "Instructor-edited student/course fieldwork; not a prefecture-wide census or neutral prevalence estimate.",
            "archive_or_access_status": "online_pdf_read",
            "retrieval_date": PACKAGE_DATE,
        },
        {
            "source_candidate_id": "NR05S002",
            "existing_source_id": "",
            "title": "NPO法人の累計認証団体数の推移（全体／地域別）",
            "publisher": "RIETI",
            "source_type": "policy_research_data_table",
            "url": "https://www.rieti.go.jp/jp/projects/npo/2004/4_1.pdf",
            "source_publication_date": "2005-12-31",
            "source_publication_date_precision": "day_as_document_header",
            "document_coverage_period": "1999-2005",
            "source_relationship": "secondary",
            "exact_locator": "PDF p.1, Okinawa row: 1999-2004 values 6,20,37,84,127,163",
            "supports_anchor_ids": "H98_002",
            "supports_status_candidate_ids": "",
            "evidence_level_proposed": "E3",
            "support_scope": "Prefecture-wide cumulative certified-NPO-corporation counts compiled from Cabinet Office.",
            "interpretation_limit": "All fields/issues; not project registry, base actors, activity, survival or causal effect.",
            "archive_or_access_status": "online_pdf_read",
            "retrieval_date": PACKAGE_DATE,
        },
        {
            "source_candidate_id": "NR05S003",
            "existing_source_id": "",
            "title": "沖縄県NPOプラザ ばなな通信 第45号",
            "publisher": "沖縄県NPOプラザ",
            "source_type": "prefectural_official_newsletter",
            "url": "https://www.pref.okinawa.lg.jp/_res/projects/default_project/_page_/001/004/891/45gou.pdf",
            "source_publication_date": "2012-10-31",
            "source_publication_date_precision": "day",
            "document_coverage_period": "2012-10-31 status",
            "source_relationship": "contemporaneous_primary",
            "exact_locator": (
                "PDF p.1 header: 県内のNPO法人数 550; 15 applications pending; p.5 on annual reports, "
                "registration/tax burdens, dissolution and return-to-voluntary-group options"
            ),
            "supports_anchor_ids": "H98_002",
            "supports_status_candidate_ids": "",
            "evidence_level_proposed": "E4",
            "support_scope": "Exact official Okinawa-wide legal-NPO count plus contemporaneous maintenance/exit-rule context.",
            "interpretation_limit": (
                "The count does not indicate issue, political stance, activity or relation to bases; the "
                "maintenance/exit discussion gives mechanisms, not their prefecture-wide prevalence."
            ),
            "archive_or_access_status": "online_pdf_read",
            "retrieval_date": PACKAGE_DATE,
        },
        {
            "source_candidate_id": "NR05S004",
            "existing_source_id": "",
            "title": "NPO法改正関連資料（所轄庁別認証法人数表）",
            "publisher": "内閣府NPOホームページ",
            "source_type": "national_official_report",
            "url": "https://www.npo-homepage.go.jp/uploads/20111011-hou.pdf",
            "source_publication_date": "2012",
            "source_publication_date_precision": "year",
            "document_coverage_period": "through 2012-09",
            "source_relationship": "contemporaneous_primary",
            "exact_locator": "table of certified NPO corporations by competent authority; Okinawa=550 through 2012-09",
            "supports_anchor_ids": "H98_002",
            "supports_status_candidate_ids": "",
            "evidence_level_proposed": "E4",
            "support_scope": "Independent official cross-check for the 2012 Okinawa endpoint.",
            "interpretation_limit": "Aggregate legal count only.",
            "archive_or_access_status": "online_pdf_read",
            "retrieval_date": PACKAGE_DATE,
        },
        {
            "source_candidate_id": "NR05S005",
            "existing_source_id": "S095",
            "title": "団体概要 / 役員",
            "publisher": "NPO法人 沖縄NGOセンター",
            "source_type": "organization_profile",
            "url": "https://www.oki-ngo.org/about/directors",
            "source_publication_date": "",
            "source_publication_date_precision": "undated_current_page",
            "document_coverage_period": "1999-06 formation claim; current profile",
            "source_relationship": "retrospective",
            "exact_locator": "団体概要: 設立年月日 1999年6月; activities items 1 and 6-7",
            "supports_anchor_ids": "H98_003",
            "supports_status_candidate_ids": "NR05OS001",
            "evidence_level_proposed": "E3",
            "support_scope": "Organization self-description of formation month and intermediary/support functions.",
            "interpretation_limit": "Current self-description; no direct proof of original legal form or uninterrupted activity.",
            "archive_or_access_status": "online_html_read",
            "retrieval_date": PACKAGE_DATE,
        },
        {
            "source_candidate_id": "NR05S006",
            "existing_source_id": "",
            "title": "特定非営利活動法人沖縄NGOセンター インタビュー",
            "publisher": "市民国際プラザ（自治体国際化協会/JANIC）",
            "source_type": "institutional_interview",
            "url": "https://www.plaza-clair.jp/interview/contents/00115921.html",
            "source_publication_date": "2022",
            "source_publication_date_precision": "year",
            "document_coverage_period": "1999-2022 retrospective",
            "source_relationship": "retrospective",
            "exact_locator": "opening profile paragraph: 1999 former name; 2008 NPO status/current-name transition",
            "supports_anchor_ids": "H98_003",
            "supports_status_candidate_ids": "NR05OS001",
            "evidence_level_proposed": "E3",
            "support_scope": "Later institutional interview on ONC's claimed lineage and legal transition.",
            "interpretation_limit": (
                "Not the 1999 charter or a 2008 internal application/resolution record; the official portal's "
                "legal-certification date is 2009-05-14. No causal link to the 1998 fieldwork article."
            ),
            "archive_or_access_status": "online_html_read",
            "retrieval_date": PACKAGE_DATE,
        },
        {
            "source_candidate_id": "NR05S007",
            "existing_source_id": "",
            "title": "沖縄におけるNGO-JICA連携ワークショップ関連報告",
            "publisher": "JICA",
            "source_type": "official_program_report",
            "url": "https://openjicareport.jica.go.jp/pdf/11712098.pdf",
            "source_publication_date": "2006",
            "source_publication_date_precision": "year",
            "document_coverage_period": "1999-2006",
            "source_relationship": "retrospective",
            "exact_locator": "sections describing NGO-JICA joint workshops beginning in 1999",
            "supports_anchor_ids": "H98_003",
            "supports_status_candidate_ids": "NR05OS001",
            "evidence_level_proposed": "E3",
            "support_scope": "Near-period institutional corroboration of an intermediary/international-cooperation path.",
            "interpretation_limit": "Program participation does not prove organizational formation, funding or base-related positioning.",
            "archive_or_access_status": "online_pdf_locator_read",
            "retrieval_date": PACKAGE_DATE,
        },
        {
            "source_candidate_id": "NR05S008",
            "existing_source_id": "S156",
            "title": "普天間基地爆音訴訟について",
            "publisher": "普天間基地爆音訴訟団",
            "source_type": "organization_history",
            "url": "https://futenma-bakuon.jp/introduction/",
            "source_publication_date": "",
            "source_publication_date_precision": "undated_current_page",
            "document_coverage_period": "2002-present retrospective",
            "source_relationship": "retrospective",
            "exact_locator": "chronology paragraph listing first 2002 and second 2012 rounds",
            "supports_anchor_ids": "H98_004;H98_014",
            "supports_status_candidate_ids": "NR05OS008",
            "evidence_level_proposed": "E4 for self-identity; E3 for compressed chronology",
            "support_scope": "Current plaintiff-group self-history.",
            "interpretation_limit": "Round year labels do not resolve separate filings/groups or identical membership.",
            "archive_or_access_status": "online_html_read",
            "retrieval_date": PACKAGE_DATE,
        },
        {
            "source_candidate_id": "NR05S009",
            "existing_source_id": "S135",
            "title": "令和4年3月10日 普天間飛行場周辺損害賠償請求事件判決",
            "publisher": "那覇地方裁判所沖縄支部",
            "source_type": "court_record",
            "url": "https://www.courts.go.jp/assets/hanrei/hanrei-pdf-91354.pdf",
            "source_publication_date": "2022-03-10",
            "source_publication_date_precision": "day",
            "document_coverage_period": "2002-2022 case history",
            "source_relationship": "retrospective",
            "exact_locator": "printed pp.13-14 / PDF pp.13-14, section 8「普天間飛行場の騒音に関する訴訟の経緯」",
            "supports_anchor_ids": "H98_004;H98_014",
            "supports_status_candidate_ids": "NR05OS008",
            "evidence_level_proposed": "E4",
            "support_scope": "Formal case chronology distinguishing 2002-2003 and 2012-2013 filings/groups.",
            "interpretation_limit": "Case chronology does not itself establish stable organization identity across rounds.",
            "archive_or_access_status": "central_archive_pdf_read",
            "retrieval_date": PACKAGE_DATE,
        },
        {
            "source_candidate_id": "NR05S010",
            "existing_source_id": "S060",
            "title": "U.S., Japanese conservation groups join legal effort to save Okinawa dugong",
            "publisher": "Earthjustice",
            "source_type": "same_day_legal_press_release",
            "url": "https://earthjustice.org/press/2003/us-japanese-conservation-groups-join-in-legal-effort-to-save-okinawa-dugong-from-extinction",
            "source_publication_date": "2003-09-25",
            "source_publication_date_precision": "day",
            "document_coverage_period": "2003-09-25 filing",
            "source_relationship": "contemporaneous_primary",
            "exact_locator": "dated release; paragraphs naming case number, plaintiffs and counsel",
            "supports_anchor_ids": "H98_005",
            "supports_status_candidate_ids": "",
            "evidence_level_proposed": "E4",
            "support_scope": "Same-day case entry and attributed roles.",
            "interpretation_limit": "Advocacy release; use complaint/caption for formal party identities.",
            "archive_or_access_status": "central_archive_html_available",
            "retrieval_date": PACKAGE_DATE,
        },
        {
            "source_candidate_id": "NR05S011",
            "existing_source_id": "",
            "title": "Complaint, Okinawa Dugong v. Rumsfeld",
            "publisher": "U.S. District Court, Northern District of California (party filing)",
            "source_type": "filed_complaint",
            "url": "https://www.biologicaldiversity.org/species/mammals/Okinawa_dugong/pdfs/complaint9-25-03.pdf",
            "source_publication_date": "2003-09-25",
            "source_publication_date_precision": "day",
            "document_coverage_period": "2003 filing; party background allegations",
            "source_relationship": "contemporaneous_primary",
            "exact_locator": "caption and complaint p.4 ¶13 (Save the Dugong Foundation formation/self-description)",
            "supports_anchor_ids": "H98_005",
            "supports_status_candidate_ids": "NR05OS002",
            "evidence_level_proposed": "E4 for filing/party caption; E3 for formation allegation",
            "support_scope": "Filed party identities and contemporaneous self-description.",
            "interpretation_limit": "A complaint allegation is not adjudication of formation date/legal status.",
            "archive_or_access_status": "online_pdf_read",
            "retrieval_date": PACKAGE_DATE,
        },
        {
            "source_candidate_id": "NR05S012",
            "existing_source_id": "",
            "title": "終結事件一覧：米軍代替飛行場施設建設差止等請求事件（調停）",
            "publisher": "沖縄県公害審査会",
            "source_type": "prefectural_official_case_record",
            "url": "https://www.pref.okinawa.lg.jp/kensei/shingikai/1014397/1014517/1004600/1004603.html",
            "source_publication_date": "",
            "source_publication_date_precision": "undated_current_page",
            "document_coverage_period": "2004-02-03 to 2004-03-30",
            "source_relationship": "retrospective",
            "exact_locator": "2004 case row: 913 applicants, acceptance, three sessions and 2004-03-30 dismissal reason",
            "supports_anchor_ids": "H98_006",
            "supports_status_candidate_ids": "",
            "evidence_level_proposed": "E4",
            "support_scope": "Official procedural intake/nonentry chronology.",
            "interpretation_limit": "Applicants are an anonymous person collective, not an organization.",
            "archive_or_access_status": "online_html_read",
            "retrieval_date": PACKAGE_DATE,
        },
        {
            "source_candidate_id": "NR05S013",
            "existing_source_id": "S049",
            "title": "ヘリ基地反対協議会 闘いの主な経緯",
            "publisher": "ヘリ基地反対協議会",
            "source_type": "organization_history",
            "url": "https://lovehenoko.org/%E9%97%98%E3%81%84%E3%81%AE%E4%B8%BB%E3%81%AA%E7%B5%8C%E7%B7%AF/",
            "source_publication_date": "",
            "source_publication_date_precision": "undated_current_page",
            "document_coverage_period": "1997-present retrospective",
            "source_relationship": "retrospective",
            "exact_locator": "2004 chronology entry for April obstruction/sit-in",
            "supports_anchor_ids": "H98_007",
            "supports_status_candidate_ids": "",
            "evidence_level_proposed": "E3",
            "support_scope": "Organization's current account of onsite action.",
            "interpretation_limit": "Current retrospective attribution; not a roster or sole-organizer proof.",
            "archive_or_access_status": "online_html_read",
            "retrieval_date": PACKAGE_DATE,
        },
        {
            "source_candidate_id": "NR05S014",
            "existing_source_id": "",
            "title": "辺野古沖海上基地建設反対運動の経過と特質",
            "publisher": "専修大学社会科学研究所『社会科学年報』41号",
            "source_type": "academic_participant_observation_reconstruction",
            "url": "https://www.senshu-u.ac.jp/~off1009/PDF/n41_103-124.pdf",
            "source_publication_date": "2007-03-10",
            "source_publication_date_precision": "day",
            "document_coverage_period": "1997-2006",
            "source_relationship": "secondary",
            "exact_locator": "printed pp.104-105 / PDF pp.2-3: 2003 group formation and 2004-04-19 action",
            "supports_anchor_ids": "H98_007",
            "supports_status_candidate_ids": "NR05OS005",
            "evidence_level_proposed": "E3",
            "support_scope": "Near-period academic reconstruction with participant observation.",
            "interpretation_limit": "Secondary chronology; not a charter or official roster.",
            "archive_or_access_status": "online_pdf_read",
            "retrieval_date": PACKAGE_DATE,
        },
        {
            "source_candidate_id": "NR05S015",
            "existing_source_id": "S132",
            "title": "普天間飛行場代替施設建設事業に係る環境影響評価方法書に対する意見",
            "publisher": "日本自然保護協会",
            "source_type": "dated_organization_submission",
            "url": "https://www.nacsj.or.jp/statement/51098/",
            "source_publication_date": "2004-06-10",
            "source_publication_date_precision": "day",
            "document_coverage_period": "2004 method-statement stage",
            "source_relationship": "contemporaneous_primary",
            "exact_locator": "page date and addressees; full opinion text",
            "supports_anchor_ids": "H98_008",
            "supports_status_candidate_ids": "",
            "evidence_level_proposed": "E4",
            "support_scope": "Formal dated EIA commenter role.",
            "interpretation_limit": "Submission does not prove procedural effect or stable coalition.",
            "archive_or_access_status": "central_archive_html_available",
            "retrieval_date": PACKAGE_DATE,
        },
        {
            "source_candidate_id": "NR05S016",
            "existing_source_id": "S140",
            "title": "泡瀬干潟埋立公金支出差止等請求事件判決",
            "publisher": "那覇地方裁判所",
            "source_type": "court_record",
            "url": "https://www.courts.go.jp/assets/hanrei/hanrei-pdf-37115.pdf",
            "source_publication_date": "",
            "source_publication_date_precision": "date_not_printed_in_archived_pdf",
            "document_coverage_period": "2005 filing through first-wave judgment",
            "source_relationship": "retrospective",
            "exact_locator": "printed/PDF p.20, subsection（7）本訴提起: 2005-05-20",
            "supports_anchor_ids": "H98_009",
            "supports_status_candidate_ids": "",
            "evidence_level_proposed": "E4",
            "support_scope": "Formal first-wave filing date and resident-plaintiff case structure.",
            "interpretation_limit": "Does not make A055 a named organizational plaintiff; first/second waves remain separate.",
            "archive_or_access_status": "central_archive_pdf_read",
            "retrieval_date": PACKAGE_DATE,
        },
        {
            "source_candidate_id": "NR05S017",
            "existing_source_id": "",
            "title": "泡瀬干潟埋め立て公金差止訴訟 第一回口頭弁論報道",
            "publisher": "しんぶん赤旗",
            "source_type": "party_news",
            "url": "https://www.jcp.or.jp/akahata/aik4/2005-07-21/2005072104_03_2.html",
            "source_publication_date": "2005-07-21",
            "source_publication_date_precision": "day",
            "document_coverage_period": "2005 hearing",
            "source_relationship": "lead",
            "exact_locator": "article body on first oral argument and A055 co-representatives' public role",
            "supports_anchor_ids": "H98_009",
            "supports_status_candidate_ids": "",
            "evidence_level_proposed": "E2",
            "support_scope": "Near-period lead for movement/public-hearing role.",
            "interpretation_limit": "Party media and spokesperson presence do not prove plaintiff status.",
            "archive_or_access_status": "online_html_locator_read",
            "retrieval_date": PACKAGE_DATE,
        },
        {
            "source_candidate_id": "NR05S018",
            "existing_source_id": "S282",
            "title": "沖縄県行政記録 平成20年",
            "publisher": "沖縄県",
            "source_type": "prefectural_official_diary",
            "url": "https://www.pref.okinawa.lg.jp/_res/projects/default_project/_page_/001/014/905/h20gyouseikiroku.pdf",
            "source_publication_date": "2008",
            "source_publication_date_precision": "year_document",
            "document_coverage_period": "2008",
            "source_relationship": "contemporaneous_primary",
            "exact_locator": "printed p.4 / PDF p.5, 2008-02-14 entry",
            "supports_anchor_ids": "H98_010",
            "supports_status_candidate_ids": "NR05OS011",
            "evidence_level_proposed": "E4",
            "support_scope": "Dated occurrence of prefectural-branch request.",
            "interpretation_limit": "No request text, response, result, scale, party affiliation or national-branch transfer.",
            "archive_or_access_status": "central_archive_pdf_read",
            "retrieval_date": PACKAGE_DATE,
        },
        {
            "source_candidate_id": "NR05S019",
            "existing_source_id": "S003",
            "title": "67団体がジュゴンの生息地辺野古への基地建設反対に共同声明",
            "publisher": "WWFジャパン",
            "source_type": "same_day_organization_statement",
            "url": "https://www.wwf.or.jp/activities/statement/3436.html",
            "source_publication_date": "2010-05-14",
            "source_publication_date_precision": "day",
            "document_coverage_period": "2010-05-14 event",
            "source_relationship": "contemporaneous_primary",
            "exact_locator": "dated statement body and domestic 67-organization participant list",
            "supports_anchor_ids": "H98_011",
            "supports_status_candidate_ids": "",
            "evidence_level_proposed": "E4 for event participation",
            "support_scope": "Dated co-signing/submission event.",
            "interpretation_limit": "No stable alliance, membership, coordination or continuity.",
            "archive_or_access_status": "central_archive_html_available",
            "retrieval_date": PACKAGE_DATE,
        },
        {
            "source_candidate_id": "NR05S020",
            "existing_source_id": "S155",
            "title": "嘉手納基地爆音差止訴訟原告団 訴訟の歴史",
            "publisher": "嘉手納基地爆音差止訴訟原告団",
            "source_type": "organization_history",
            "url": "https://kadena-bakuon.jp/trial/history/",
            "source_publication_date": "",
            "source_publication_date_precision": "undated_current_page",
            "document_coverage_period": "1982-present retrospective",
            "source_relationship": "retrospective",
            "exact_locator": "「第3次訴訟」 section: 2011-04-28 filing",
            "supports_anchor_ids": "H98_012",
            "supports_status_candidate_ids": "NR05OS007",
            "evidence_level_proposed": "E4 for self-history/date",
            "support_scope": "Current plaintiff-group case chronology.",
            "interpretation_limit": "Does not establish identical membership across rounds.",
            "archive_or_access_status": "online_html_read",
            "retrieval_date": PACKAGE_DATE,
        },
        {
            "source_candidate_id": "NR05S021",
            "existing_source_id": "S240",
            "title": "下地島への自衛隊配備に反対／平和運動連絡協",
            "publisher": "宮古毎日新聞",
            "source_type": "local_news",
            "url": "https://www.miyakomainichi.com/2011/06/20401/",
            "source_publication_date": "2011-06-25",
            "source_publication_date_precision": "day",
            "document_coverage_period": "2011-06-23 meeting",
            "source_relationship": "secondary",
            "exact_locator": "article lead/body: meeting held 2011-06-23 and hosted by A096",
            "supports_anchor_ids": "H98_013",
            "supports_status_candidate_ids": "NR05OS009",
            "evidence_level_proposed": "E3 event; E2/E3 organization identity",
            "support_scope": "Near-contemporaneous event date, host attribution and issue.",
            "interpretation_limit": "No formation, roster, continuity or alliance proof.",
            "archive_or_access_status": "central_archive_html_available",
            "retrieval_date": PACKAGE_DATE,
        },
        {
            "source_candidate_id": "NR05S022",
            "existing_source_id": "S015",
            "title": "与那国に自衛隊いらない／配備反対の意見広告呼びかけ",
            "publisher": "しんぶん赤旗",
            "source_type": "party_news",
            "url": "https://www.jcp.or.jp/akahata/aik12/2012-08-31/2012083115_02_1.html",
            "source_publication_date": "2012-08-31",
            "source_publication_date_precision": "day",
            "document_coverage_period": "2012-08-25 founding press conference",
            "source_relationship": "lead",
            "exact_locator": "article body: 2012-08-25 founding press conference, reported co-representatives and planned ad",
            "supports_anchor_ids": "H98_015",
            "supports_status_candidate_ids": "NR05OS010",
            "evidence_level_proposed": "E2",
            "support_scope": "Single-source lead for committee formation/opinion-ad plan.",
            "interpretation_limit": "Not independent; original ad, local coverage, exact identity and survival missing.",
            "archive_or_access_status": "central_archive_html_available",
            "retrieval_date": PACKAGE_DATE,
        },
        {
            "source_candidate_id": "NR05S023",
            "existing_source_id": "S063",
            "title": "ジュゴン保護基金委員会（用語辞典）",
            "publisher": "琉球新報",
            "source_type": "newspaper_dictionary",
            "url": "https://ryukyushimpo.jp/okinawa-dic/prentry-41677.html",
            "source_publication_date": "",
            "source_publication_date_precision": "undated_current_entry",
            "document_coverage_period": "1999 formation retrospective",
            "source_relationship": "lead",
            "exact_locator": "entry background line reporting 1999-10 formation",
            "supports_anchor_ids": "",
            "supports_status_candidate_ids": "NR05OS002",
            "evidence_level_proposed": "E2/E3",
            "support_scope": "Secondary month-level formation lead.",
            "interpretation_limit": "Needs charter/contemporaneous corroboration; no legal-status or continuity inference.",
            "archive_or_access_status": "central_archive_status_available",
            "retrieval_date": PACKAGE_DATE,
        },
        {
            "source_candidate_id": "NR05S024",
            "existing_source_id": "",
            "title": "泡瀬干潟を守る連絡会 団体情報",
            "publisher": "沖縄県地域環境センター",
            "source_type": "institutional_directory_profile",
            "url": "https://kankyo-center.okinawa/environmental-organization-facility/%E6%B3%A1%E7%80%AC%E5%B9%B2%E6%BD%9F%E3%82%92%E5%AE%88%E3%82%8B%E9%80%A3%E7%B5%A1%E4%BC%9A",
            "source_publication_date": "",
            "source_publication_date_precision": "undated_current_page",
            "document_coverage_period": "2001-01 formation retrospective",
            "source_relationship": "retrospective",
            "exact_locator": "profile fields: organization type and 設立時期 2001年1月",
            "supports_anchor_ids": "",
            "supports_status_candidate_ids": "NR05OS003",
            "evidence_level_proposed": "E3",
            "support_scope": "Institutional directory formation-month claim.",
            "interpretation_limit": "Not a contemporaneous charter; does not establish litigation party status.",
            "archive_or_access_status": "online_html_read",
            "retrieval_date": PACKAGE_DATE,
        },
        {
            "source_candidate_id": "NR05S025",
            "existing_source_id": "S104",
            "title": "NPO法人情報検索：沖縄平和協力センター",
            "publisher": "内閣府NPOホームページ",
            "source_type": "official_npo_portal",
            "url": "https://www.npo-homepage.go.jp/npoportal/",
            "source_publication_date": "",
            "source_publication_date_precision": "current_database",
            "document_coverage_period": "2002-10-17 certification; current record",
            "source_relationship": "retrospective",
            "exact_locator": "entity record/certification field: 2002-10-17",
            "supports_anchor_ids": "",
            "supports_status_candidate_ids": "NR05OS004",
            "evidence_level_proposed": "E4",
            "support_scope": "Official legal-certification date.",
            "interpretation_limit": "Certification is not formation, activity continuity, issue position or influence.",
            "archive_or_access_status": "central_source_locator; portal may block automated access",
            "retrieval_date": PACKAGE_DATE,
        },
        {
            "source_candidate_id": "NR05S026",
            "existing_source_id": "",
            "title": "法政大学大原社会問題研究所 環境アーカイブズ資料目録（沖縄関連）",
            "publisher": "法政大学大原社会問題研究所",
            "source_type": "archive_catalog",
            "url": "https://k-archives.ws.hosei.ac.jp/wp-content/uploads/2024/09/0007_20240828.pdf",
            "source_publication_date": "2024",
            "source_publication_date_precision": "year",
            "document_coverage_period": "catalogued 2003 material",
            "source_relationship": "lead",
            "exact_locator": "catalog p.66 area listing 2003-07-31 preparatory-committee item",
            "supports_anchor_ids": "",
            "supports_status_candidate_ids": "NR05OS005",
            "evidence_level_proposed": "E2 locator",
            "support_scope": "Locator for contemporaneous A069 preparatory material.",
            "interpretation_limit": "Catalog metadata is not the underlying document, formation record, roster or alliance evidence.",
            "archive_or_access_status": "online_catalog_read_underlying_item_not_retrieved",
            "retrieval_date": PACKAGE_DATE,
        },
        {
            "source_candidate_id": "NR05S027",
            "existing_source_id": "",
            "title": "沖縄県サンゴ礁保全推進協議会 設立趣意書／経緯",
            "publisher": "沖縄県サンゴ礁保全推進協議会",
            "source_type": "organization_history_and_charter",
            "url": "https://ocrcc.sakura.ne.jp/about/keii.html",
            "source_publication_date": "",
            "source_publication_date_precision": "undated_current_page",
            "document_coverage_period": "2007 preparation; 2008 formation",
            "source_relationship": "retrospective",
            "exact_locator": "history paragraph: preparations from FY2007; 2008-06-28 establishment meeting",
            "supports_anchor_ids": "",
            "supports_status_candidate_ids": "NR05OS006",
            "evidence_level_proposed": "E4 for organization self-history",
            "support_scope": "Formation-process milestones.",
            "interpretation_limit": "Multi-stakeholder platform; no anti-base stance inferred.",
            "archive_or_access_status": "online_html_read",
            "retrieval_date": PACKAGE_DATE,
        },
        {
            "source_candidate_id": "NR05S028",
            "existing_source_id": "",
            "title": "平成20年度 民間参加型サンゴ礁生態系保全活動推進事業 報告書",
            "publisher": "沖縄県",
            "source_type": "prefectural_official_report",
            "url": "https://www.pref.okinawa.jp/_res/projects/default_project/_page_/001/004/527/h20houkokusyo_1.pdf",
            "source_publication_date": "2009",
            "source_publication_date_precision": "year_inferred_from_fiscal_report",
            "document_coverage_period": "FY2007-FY2008 formation process",
            "source_relationship": "retrospective",
            "exact_locator": "chapter 2, section 2-1 establishment meeting; attached charter dates",
            "supports_anchor_ids": "",
            "supports_status_candidate_ids": "NR05OS006",
            "evidence_level_proposed": "E4",
            "support_scope": "Official report on the platform's preparation/establishment process.",
            "interpretation_limit": "Charter date, meeting date and first general meeting are distinct milestones.",
            "archive_or_access_status": "online_pdf_read",
            "retrieval_date": PACKAGE_DATE,
        },
        {
            "source_candidate_id": "NR05S029",
            "existing_source_id": "",
            "title": "Meeting of the dugongs and the cooking pots: Anti-military base citizens' groups on Okinawa",
            "publisher": "Japanese Studies",
            "source_type": "academic_article",
            "url": "https://www.tandfonline.com/doi/abs/10.1080/1037139032000129676",
            "source_publication_date": "2003",
            "source_publication_date_precision": "year",
            "document_coverage_period": "1995-2003 movement framing",
            "source_relationship": "secondary",
            "exact_locator": "abstract/article scope: six anti-base citizens' groups; environmentalism, feminism and anti-militarism",
            "supports_anchor_ids": "",
            "supports_status_candidate_ids": "",
            "evidence_level_proposed": "literature_context",
            "support_scope": "Prior scholarship establishing that multi-issue framing is not a novel project finding.",
            "interpretation_limit": "Use for literature positioning, not as a registry, relation or event source without full-text review.",
            "archive_or_access_status": "abstract_metadata_only_full_text_not_retrieved",
            "retrieval_date": PACKAGE_DATE,
        },
        {
            "source_candidate_id": "NR05S030",
            "existing_source_id": "",
            "title": "沖縄地域における参加型環境保全活動の実態と支援方策上の課題",
            "publisher": "日本造園学会『ランドスケープ研究』",
            "source_type": "academic_survey_article",
            "url": "https://www.jstage.jst.go.jp/article/jila1994/64/5/64_5_849/_article/-char/ja",
            "source_publication_date": "2001-03-30",
            "source_publication_date_precision": "day",
            "document_coverage_period": "1996 survey; 2001 publication",
            "source_relationship": "secondary",
            "exact_locator": "abstract and full PDF methods/results; 45 mailed groups/29 valid responses require full-table check",
            "supports_anchor_ids": "H98_001",
            "supports_status_candidate_ids": "",
            "evidence_level_proposed": "E3 contextual",
            "support_scope": "Competing pre-NPO-law baseline for heterogeneous environmental civic activity/support needs.",
            "interpretation_limit": "Not a base-movement census; administrative-collaboration counts require table-level human verification.",
            "archive_or_access_status": "article_metadata_and_abstract_read_full_pdf_locator",
            "retrieval_date": PACKAGE_DATE,
        },
        {
            "source_candidate_id": "NR05S031",
            "existing_source_id": "",
            "title": "特定非営利活動法人沖縄NGOセンター 行政入力情報",
            "publisher": "内閣府NPO法人ポータルサイト（所轄庁：沖縄県）",
            "source_type": "official_npo_portal_entity_record",
            "url": "https://www.npo-homepage.go.jp/npoportal/detail/047021403",
            "source_publication_date": "",
            "source_publication_date_precision": "current_database_updated_2024-12-12",
            "document_coverage_period": "legal certification event 2009-05-14; current entity record",
            "source_relationship": "retrospective",
            "exact_locator": "行政入力情報, lines/fields「設立認証年月日 2009年05月14日」「設立年月日 －」",
            "supports_anchor_ids": "H98_003",
            "supports_status_candidate_ids": "NR05OS001",
            "evidence_level_proposed": "E4",
            "support_scope": "Official competent-authority legal-certification date.",
            "interpretation_limit": (
                "Certification date is not the 1999 voluntary-body formation date; it does not by itself "
                "resolve whether a 2008 internal resolution, application or name-change stage occurred."
            ),
            "archive_or_access_status": "online_html_read",
            "retrieval_date": PACKAGE_DATE,
        },
        {
            "source_candidate_id": "NR05S032",
            "existing_source_id": "",
            "title": "沖縄県 NPO法人一覧／解散・取消・移管一覧 公開ハブ",
            "publisher": "沖縄県",
            "source_type": "prefectural_official_data_hub",
            "url": "https://www.pref.okinawa.jp/kurashikankyo/katsudo/1004889/1004890.html",
            "source_publication_date": "2026-04-13",
            "source_publication_date_precision": "day_current_list_update",
            "document_coverage_period": "current surviving corporations plus historical exit events",
            "source_relationship": "retrospective",
            "exact_locator": "page links 157/161: current法人 list with certification date/20 fields; dissolution/cancellation/transfer list with exit dates",
            "supports_anchor_ids": "",
            "supports_status_candidate_ids": "",
            "evidence_level_proposed": "E4 data opportunity",
            "support_scope": "Online material-rich follow-up for surviving cohorts and exit-event lower bounds.",
            "interpretation_limit": (
                "Current survivors plus exit events do not by themselves reconstruct complete annual historical "
                "stock; certification dates for exited corporations still need portal/entity recovery."
            ),
            "archive_or_access_status": "hub_read_linked_tables_not_extracted_in_NR05",
            "retrieval_date": PACKAGE_DATE,
        },
    ]
    return [with_constants(row) for row in rows]


def online_exhausted_gaps() -> list[dict[str, str]]:
    rows = [
        {
            "gap_id": "NR05G001",
            "actor_or_topic": "A076 formation/legal form",
            "related_anchor_ids": "H98_005;NR05OS002",
            "exhausted_question": "Exact 1999 formation month, charter, representatives and Japanese legal form.",
            "queries_and_domains_checked": "complaint; Ryukyu dictionary; organization/legal case pages; general web",
            "online_result": "Year supported; October is a secondary lead; legal form unresolved.",
            "why_not_closed": "Party pleading and dictionary are not the founding record.",
            "needed_material": "Founding charter/minutes, early newsletter or local newspaper report.",
            "priority": "high",
            "task_destination": "local_retrieval_or_new_primary",
        },
        {
            "gap_id": "NR05G002",
            "actor_or_topic": "A055 formation and Awase role boundary",
            "related_anchor_ids": "H98_009;NR05OS003",
            "exhausted_question": "Contemporaneous formation proof and exact organization/plaintiff/supporter relationship.",
            "queries_and_domains_checked": "environment center; court judgment; JELF/JAWAN/Jichiro; newspaper",
            "online_result": "2001-01 formation directory claim and 2005 filing date found; organizational plaintiff status not found.",
            "why_not_closed": "Public coverage names spokespeople and movement, while caption uses residents/individuals.",
            "needed_material": "Original complaints, movement minutes and founding charter.",
            "priority": "high",
            "task_destination": "local_retrieval_or_case_file",
        },
        {
            "gap_id": "NR05G003",
            "actor_or_topic": "A069 formation/continuity",
            "related_anchor_ids": "NR05OS005",
            "exhausted_question": "Exact formation day, roster, legal status and activity after the early EIA period.",
            "queries_and_domains_checked": "academic paper; archive catalog; EIA pages; web search",
            "online_result": "September 2003 secondary claim and a preparatory-material catalog locator.",
            "why_not_closed": "The underlying 2003 item is not online; catalog metadata is not the document.",
            "needed_material": "Hosei archive item, founding statement, roster and subsequent newsletters.",
            "priority": "high",
            "task_destination": "archive_or_local_retrieval",
        },
        {
            "gap_id": "NR05G004",
            "actor_or_topic": "A015 Yonaguni opinion-ad committee",
            "related_anchor_ids": "H98_015;NR05OS010",
            "exhausted_question": "Original ad, exact committee name, officers, participating organizations and survival.",
            "queries_and_domains_checked": "JCP; Ryukyu/Okinawa/QAB; Yonaguni/Yaeyama web search; existing source archive",
            "online_result": "One party-newspaper report only.",
            "why_not_closed": "No independent local source or primary ad found online.",
            "needed_material": "Yaeyama Mainichi/Yaeyama Nippo issue, ad image, committee material and town records.",
            "priority": "highest",
            "task_destination": "local_retrieval_tier2",
        },
        {
            "gap_id": "NR05G005",
            "actor_or_topic": "A096 Miyako early anti-deployment carrier",
            "related_anchor_ids": "H98_013;NR05OS009",
            "exhausted_question": "Formation, officers, structure and continuity around/after the 2011 meeting.",
            "queries_and_domains_checked": "Miyako Mainichi; group-name variants; current web",
            "online_result": "Near-contemporaneous event report found; organization history absent.",
            "why_not_closed": "Event hosting is not a formation/continuity record.",
            "needed_material": "Flyer, minutes, local press sequence and organizer archive.",
            "priority": "high",
            "task_destination": "local_retrieval_tier2",
        },
        {
            "gap_id": "NR05G006",
            "actor_or_topic": "X010 ONC 1999 formation／2008 retrospective stage／2009 certification",
            "related_anchor_ids": "H98_003;NR05OS001",
            "exhausted_question": "Exact predecessor-name continuity and the semantics of the 2008 internal stage before 2009 certification.",
            "queries_and_domains_checked": "ONC official; CLAIR interview; JICA report; NPO portal",
            "online_result": "Official certification is 2009-05-14; a later interview attributes NPO/current-name transition to 2008.",
            "why_not_closed": "2008 may denote resolution, application, name use or an imprecise retrospective date.",
            "needed_material": "1999 charter/minutes; 2008 application/resolution/name-change records; 2009 certification file.",
            "priority": "medium_high",
            "task_destination": "new_primary_or_organization_archive",
        },
        {
            "gap_id": "NR05G007",
            "actor_or_topic": "A115 2008 request content and branch history",
            "related_anchor_ids": "H98_010;NR05OS011",
            "exhausted_question": "Request text, prefectural response and 2000s Okinawa-branch continuity.",
            "queries_and_domains_checked": "prefectural diary; national organization archive; web/news search",
            "online_result": "Exact occurrence found; content/outcome absent.",
            "why_not_closed": "Administrative diary is an index entry, not the submitted document.",
            "needed_material": "Request, response, branch newsletter and meeting records.",
            "priority": "medium_high",
            "task_destination": "prefectural_file_or_branch_archive",
        },
        {
            "gap_id": "NR05G008",
            "actor_or_topic": "Okinawa NPO legal-status universe 1998-2012",
            "related_anchor_ids": "H98_002",
            "exhausted_question": "Complete annual certifications, dissolutions/transfers and issue fields in Okinawa.",
            "queries_and_domains_checked": "RIETI; Cabinet Office; Okinawa NPO Plaza newsletters, current法人 list and exit-event list",
            "online_result": (
                "1999-2004 cumulative series and exact 2012 endpoint found. Current Okinawa hub also exposes "
                "a surviving-corporation table with certification dates/20 fields and a dissolution/cancellation/"
                "transfer table with exit dates."
            ),
            "why_not_closed": (
                "These online tables can build surviving cohorts and exit-event lower bounds, but exited "
                "corporations' certification dates are not complete in one table, so historical stock still "
                "requires entity-level portal recovery."
            ),
            "needed_material": (
                "Next online wave: extract the two official tables, join surviving cohorts, then recover exited "
                "corporations' certification dates from NPO portal/entity records. Local retrieval is not yet justified."
            ),
            "priority": "high_online",
            "task_destination": "online_followup_material_rich",
        },
        {
            "gap_id": "NR05G009",
            "actor_or_topic": "1998 fieldwork baseline replication",
            "related_anchor_ids": "H98_001",
            "exhausted_question": "Whether intermediary weakness/episodic activity characterized the wider Okinawa civic universe.",
            "queries_and_domains_checked": "Ryukyu repository; J-STAGE; CiNii/J-STAGE literature leads",
            "online_result": "One contemporaneous course-fieldwork interpretation plus one heterogeneous environmental survey comparator.",
            "why_not_closed": "Neither source is a population census; samples/questions differ.",
            "needed_material": "Comparable 1990s surveys, original instruments and NGO directories.",
            "priority": "medium_high",
            "task_destination": "literature_review_and_local_library",
        },
        {
            "gap_id": "NR05G010",
            "actor_or_topic": "A068→A019 lifecycle date",
            "related_anchor_ids": "",
            "exhausted_question": "Search-summary claim incorrectly attaching 2000 to the 1997 reorganization.",
            "queries_and_domains_checked": "Senshu PDF full text; current organization page; central lifecycle table",
            "online_result": "PDF正文 states June 1997 推進協 and October 1997 developmental dissolution/new A019 carrier.",
            "why_not_closed": "Closed as a known exclusion, not an NR-05 anchor.",
            "needed_material": "None for NR-05; do not reopen central LC002 absent new primary evidence.",
            "priority": "do_not_dispatch",
            "task_destination": "known_exclusion_only",
        },
    ]
    return [with_constants(row) for row in rows]


def human_review_queue(
    anchors: Iterable[Mapping[str, str]], statuses: Iterable[Mapping[str, str]]
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for anchor in anchors:
        aid = anchor["anchor_id"]
        rows.append(
            with_constants(
                {
                    "review_item_id": f"NR05HR-A-{aid}",
                    "object_type": "historical_anchor",
                    "object_ids": aid,
                    "queue_role": "research_candidate_pool",
                    "formal_hr_dispatch_status": "not_dispatched",
                    "decision_scope": "fact_date_source_relation_interpretation_boundary",
                    "review_question": (
                        f"Does the cited evidence support {aid} with the stated source/event/activity/claim "
                        "date separation and relation boundary?"
                    ),
                    "source_candidate_ids": anchor["source_candidate_ids"],
                    "recommended_options": "accept;revise;defer_second_source;defer_local;reject",
                    "ai_recommendation": (
                        "accept_bounded"
                        if anchor["evidence_level_proposed"].startswith(("E3", "E4"))
                        else "defer_or_accept_context_only"
                    ),
                    "risk_if_overread": (
                        f"{anchor['relation_boundary']} {anchor['continuity_boundary']}"
                    ),
                    "human_decision": "",
                    "reviewer": "",
                    "review_date": "",
                    "revision_note": "",
                }
            )
        )
    anchor_status_ids = {
        "NR05OS001",
        "NR05OS007",
        "NR05OS008",
        "NR05OS009",
        "NR05OS010",
        "NR05OS011",
    }
    for status in statuses:
        sid = status["status_candidate_id"]
        if sid in anchor_status_ids:
            continue
        rows.append(
            with_constants(
                {
                    "review_item_id": f"NR05HR-S-{sid}",
                    "object_type": "organization_status_candidate",
                    "object_ids": sid,
                    "queue_role": "research_candidate_pool",
                    "formal_hr_dispatch_status": "not_dispatched",
                    "decision_scope": "status_date_legal_semantics_continuity_boundary",
                    "review_question": status["review_question"],
                    "source_candidate_ids": status["source_candidate_ids"],
                    "recommended_options": "accept;revise;defer_second_source;defer_local;reject",
                    "ai_recommendation": "defer_local"
                    if status["needs_local_retrieval"].startswith("yes")
                    else "accept_bounded",
                    "risk_if_overread": (
                        f"{status['legal_status_semantics']} {status['continuity_boundary']}"
                    ),
                    "human_decision": "",
                    "reviewer": "",
                    "review_date": "",
                    "revision_note": "",
                }
            )
        )
    return rows


def write_csv(path: Path, fieldnames: list[str], rows: Iterable[Mapping[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_rows(
    anchors: list[dict[str, str]],
    statuses: list[dict[str, str]],
    sources: list[dict[str, str]],
    gaps: list[dict[str, str]],
    reviews: list[dict[str, str]],
) -> list[str]:
    checks: list[str] = []

    assert 10 <= len(anchors) <= 15, f"expected 10-15 anchors, got {len(anchors)}"
    assert len({row["anchor_id"] for row in anchors}) == len(anchors)
    checks.append(f"PASS anchor count: {len(anchors)} (contract 10-15)")

    all_rows = [*anchors, *statuses, *sources, *gaps, *reviews]
    for row in all_rows:
        for key, value in CONSTANTS.items():
            assert row.get(key) == value, f"{row} missing constant {key}={value}"
    checks.append(f"PASS research-only constants on {len(all_rows)} CSV rows")

    for row in [*anchors, *statuses, *sources]:
        assert row["source_relationship"] in ALLOWED_SOURCE_RELATIONSHIPS
    checks.append("PASS source_relationship vocabulary")

    required_date_fields = {
        "source_publication_date",
        "source_publication_date_precision",
        "event_date_start",
        "event_date_end",
        "event_date_precision",
        "actor_active_period",
        "claim_period",
    }
    for row in anchors:
        assert required_date_fields.issubset(row)
        assert row["source_publication_date_precision"]
        assert row["event_date_start"]
        assert row["event_date_end"]
        assert row["event_date_precision"]
        assert row["actor_active_period"]
        assert row["claim_period"]
    checks.append("PASS separate source/event/activity/claim date semantics")

    source_ids = {row["source_candidate_id"] for row in sources}
    for row in anchors:
        refs = set(row["source_candidate_ids"].split(";"))
        assert refs and refs <= source_ids, f"unknown source refs for {row['anchor_id']}: {refs-source_ids}"
    for row in statuses:
        refs = set(row["source_candidate_ids"].split(";"))
        assert refs and refs <= source_ids, f"unknown source refs for {row['status_candidate_id']}"
    checks.append("PASS source crosswalk integrity")

    for source in sources:
        assert source["exact_locator"], source["source_candidate_id"]
        assert source["interpretation_limit"], source["source_candidate_id"]
    checks.append("PASS exact locator and interpretation limit on every source")

    domain_blob = ";".join(row["domain_tags"] for row in anchors)
    required_tokens = {
        "NPO_law",
        "Henoko",
        "noise",
        "Awase",
        "women",
        "human_rights",
        "co_signing",
        "Sakishima",
        "labor",
        "opinion_ad",
    }
    assert required_tokens <= set(domain_blob.split(";"))
    checks.append("PASS required domain coverage")

    relation_types = {row["relation_semantics_candidate"] for row in anchors}
    assert "round_of_candidate" in relation_types
    assert "case_role_not_alliance" in relation_types
    assert "procedural_commenter" in relation_types
    assert "event_hyperedge_co_signing" in relation_types
    checks.append("PASS structured relation-type candidates")

    by_anchor = {row["anchor_id"]: row for row in anchors}
    assert by_anchor["H98_015"]["source_relationship"] == "lead"
    assert by_anchor["H98_015"]["evidence_level_proposed"] == "E2"
    assert by_anchor["H98_009"]["actor_ids"] == ""
    assert by_anchor["H98_011"]["actor_ids"] == "A005"
    assert by_anchor["H98_003"]["event_date_end"] == "2009-05-14"
    assert "not a stable alliance" in by_anchor["H98_011"]["relation_boundary"]
    assert "not encoded as the named organizational plaintiff" in by_anchor["H98_009"]["relation_boundary"]
    assert "not converted into an organization" in by_anchor["H98_006"]["relation_boundary"]
    checks.append("PASS sensitive ONC/A015/co-signing/Awase/person-collective gates")

    baseline = by_anchor["H98_001"]
    assert baseline["source_relationship"] == "secondary"
    assert "course-fieldwork" in baseline["source_role_detail"]
    assert "not a census" in baseline["relation_boundary"].lower()
    checks.append("PASS 1998 course-fieldwork/secondary boundary")

    npo = by_anchor["H98_002"]
    assert "all certified NPO corporations" in npo["relation_boundary"]
    assert "not this project's base-accountability actors" in npo["relation_boundary"]
    checks.append("PASS NPO-universe-to-base-actor noninference gate")

    assert all(not row["human_decision"] for row in reviews)
    assert all(not row["reviewer"] for row in reviews)
    assert all(not row["review_date"] for row in reviews)
    assert all(row["queue_role"] == "research_candidate_pool" for row in reviews)
    assert all(row["formal_hr_dispatch_status"] == "not_dispatched" for row in reviews)
    checks.append("PASS blank decisions and not-dispatched candidate-pool status")

    gap_by_id = {row["gap_id"]: row for row in gaps}
    assert gap_by_id["NR05G010"]["task_destination"] == "known_exclusion_only"
    assert "1997" in gap_by_id["NR05G010"]["online_result"]
    checks.append("PASS 1997 A068→A019 correction retained as known exclusion")

    catalog = next(row for row in sources if row["source_candidate_id"] == "NR05S026")
    assert catalog["source_relationship"] == "lead"
    assert "not the underlying document" in catalog["interpretation_limit"]
    checks.append("PASS archive catalog is locator-only")

    spencer = next(row for row in sources if row["source_candidate_id"] == "NR05S029")
    assert "not a novel project finding" in spencer["support_scope"]
    checks.append("PASS literature novelty boundary")

    onc_portal = next(row for row in sources if row["source_candidate_id"] == "NR05S031")
    assert "2009-05-14" in onc_portal["document_coverage_period"]
    material_rich_gap = next(row for row in gaps if row["gap_id"] == "NR05G008")
    assert material_rich_gap["task_destination"] == "online_followup_material_rich"
    checks.append("PASS ONC official-certification conflict and G008 online-rich gates")
    return checks


def build_search_log() -> str:
    return """# NR-05 search log — 1998–2012 online history

Date: 2026-07-20
Scope: online-only, research-only candidates; no central writeback.

## Search tracks and outcomes

| Track | Query/domain families | Result | Residual |
|---|---|---|---|
| NPO legal context | RIETI, Cabinet Office NPO portal, Okinawa NPO Plaza newsletters | 1999–2004 cumulative Okinawa series and exact 2012 endpoint found | annual certifications/dissolutions microdata incomplete |
| Intermediary organization | ONC official, CLAIR/JANIC interview, JICA report, NPO portal | 1999-06 start; retrospective 2008 transition claim; official certification 2009-05-14 | founding charter and 2008 internal-stage record missing |
| Henoko/Oura | Earthjustice, filed complaint, NACS-J, A019, Senshu academic reconstruction | 2003 legal entry, 2004 onsite start and EIA comment dated | local deliberation, rosters and contemporaneous movement files thin |
| Formal nonentry | Okinawa Pollution Review Board | 2004 intake→three sessions→dismissal exact chronology found | application and applicant representation missing |
| Noise litigation | Futenma/Kadena official histories, court judgments | round dates and parallel-case warning structured | original complaints/round rosters needed |
| Awase | court judgment, near-period press/JAWAN/Jichiro leads | 2005-05-20 filing date closed; A055 kept supporter, not org plaintiff | original complaint and movement minutes needed |
| Women/human rights | Okinawa administrative diary, branch/national organization search | 2008-02-14 request occurrence closed | request text, response and branch archive missing |
| 2010 co-signing | WWF dated statement/list | 67-group event participation closed | coordination mechanism deliberately not inferred |
| Early Sakishima | Miyako Mainichi, JCP, local-name variants | 2011 Miyako event and 2012 Yonaguni lead found | organization identity/continuity and original ad need local retrieval |
| Literature positioning | Ryukyu repository, J-STAGE, Taylor & Francis | 1998 baseline, 2001 environment comparator, Spencer 2003 novelty boundary found | fuller literature synthesis requires principal reading |

## Date-semantics protocol

- `source_publication_date` records when the source/document was published, never the historical event merely described.
- `event_date_start/end` records the historical occurrence or bounded range.
- `actor_active_period` records only the minimum activity window supported by the source.
- `claim_period` records the temporal reach of the proposed statement.
- `source_relationship` is one of: `contemporaneous_primary`, `retrospective`, `secondary`, `lead`.
- Access/retrieval date is never substituted for publication date.

## Known exclusion / corrected search trap

The Senshu PDF full text says the Nago referendum promotion council formed in June 1997 and was
developmentally dissolved/reorganized in October 1997 into the later A019 carrier. Search snippets can
incorrectly glue the subsequent 2000 action years to that 1997 reorganization. NR-05 therefore excludes a
“2000 lifecycle” anchor and does not reopen or rewrite central `LC002`.

The RIETI cumulative-certification table used here has one consistent denominator (all certified NPO
corporations). A different RIETI table reports smaller 1999/2000 counts for a business-report/data-available
sample. Those values are deliberately excluded from the cumulative series because their denominator differs.

## Online exhaustion rule

“Online exhausted” means directed searches across organization, government/court, local-news, academic and
archive-catalog channels failed to locate the needed primary field. It does not mean the event/organization did
not exist. Catalog records remain locators only until the underlying item is read.
"""


def build_brief(
    anchors: list[dict[str, str]],
    statuses: list[dict[str, str]],
    sources: list[dict[str, str]],
    gaps: list[dict[str, str]],
) -> str:
    relation_counts = Counter(row["source_relationship"] for row in sources)
    relation_summary = ", ".join(
        f"{key}={relation_counts.get(key, 0)}"
        for key in ["contemporaneous_primary", "retrospective", "secondary", "lead"]
    )
    return f"""# NR-05 brief — 1998–2012 online historical gap fill

## Outcome

The package supplies **{len(anchors)} dated historical anchors**, **{len(statuses)} organization-status
candidates**, **{len(sources)} source candidates**, and **{len(gaps)} explicitly bounded gaps**. Every row is
`research_only / candidate / ai_seeded / not_frontend_ready / central_writeback=no`.

The empirical judgment is: **post-1998 Okinawa civic activity is more traceable online, but the gain is
selective and institution-produced.** Legal-NPO certification, court rounds, formal EIA submissions and
official administrative diaries create stable dates and records. Informal action committees, local meeting
carriers and movement deliberation remain dependent on current retrospective pages, party/local news and
archive catalogs. “More traceable” therefore cannot be equated with “more active,” “more central,” or “more
durable.”

Source-relation mix: {relation_summary}.

## High-value interpretation candidates

1. **The NPO legal environment expanded quickly without demonstrating that base-accountability actors
   incorporated.** Okinawa's all-field certified-NPO-corporation count rose from 6 in 1999 to 163 in 2004 and 550 by
   2012-10-31. This is an official/near-official institutional context, not a count of this project's actors.
   The same 2012 official newsletter describes annual-report, registration and local-tax obligations and notes
   that inactive/under-resourced corporations may dissolve or return to voluntary-group form. Legal status
   therefore produces both visible records and maintenance/exit costs; it cannot be treated as longevity.
2. **The sharper hypothesis is a division of organizational labor, not generic “issue diversification.”**
   After 1998 the all-field legal-NPO universe expanded rapidly, while local base-accountability carriers may
   have remained mainly informal/event/case organizations and obtained professional capacity through lawyers,
   outside incorporated NGOs and procedural venues. ONC's 1999 formation, retrospectively claimed 2008
   transition and official 2009-05-14 certification form a useful non-base comparator. This is a comparison
   hypothesis, not a causal finding.
3. **The strongest historical unit is often the case/event/round, not a timeless organization.** Futenma's
   current history compresses dates that the court record separates into 2002–2003 and 2012–2013 filings;
   round labels do not prove identical plaintiffs.
4. **Formal venues also produce negative records.** The 2004 pollution-mediation case records intake,
   sessions and jurisdictional dismissal. That is evidence about venue design, not proof of a failed or weak
   movement, and its 913 applicants are not actorized.
5. **Observed historical “bridges” are partly archival artifacts.** Earthjustice, WWF, courts and NACS-J leave
   dated and often English/formal traces. Their online visibility cannot be read directly as social-network
   centrality.
6. **Sakishima remains the clearest online limit.** The 2011 Miyako meeting is event-verifiable, while the
   2012 Yonaguni opinion-ad committee remains one E2 party-news lead requiring the original ad and local press.
7. **One NPO-history gap remains online-rich, not locally exhausted.** Okinawa's current official hub exposes
   a surviving-corporation table with certification dates/20 fields and a separate dissolution/cancellation/
   transfer table with exit dates. A next online wave can build cohort and exit-event lower bounds before
   considering a prefectural request or local retrieval.

## Literature positioning / novelty boundary

- Caroline Spencer's 2003 study already connected Okinawa anti-base citizens' groups with environmental,
  feminist and anti-militarist frames. **“Issue diversification” or “environment/women entered base politics”
  is not a new finding of this project.**
- The 1998 Ryukyu course-fieldwork article is useful as a contemporaneous interpretation of weak capacity,
  episodic action and a missing intermediary layer, but it is instructor-edited student fieldwork, not a
  prefecture-wide census.
- A 2001 survey of general environmental voluntary activity supplies a competing baseline: heterogeneous
  environmental groups and support/administrative relationships existed before or around NPO-law
  institutionalization. This resists a linear “all environmental NGOs derived from anti-base movements”
  story.
- The defensible research opportunity is narrower: **why legal/administrative document regimes make some
  organization forms and institutional entries visible while informal/event carriers disappear, and why a
  rapidly expanding legal-NPO ecology does not map cleanly onto base-accountability carriers.**

## Mechanical comparison that requires principal judgment

A current, purposive main-thread registry probe selected 51 Okinawa-local base-accountability actors and
found only one row explicitly labelled `specified_nonprofit_corporation`; most observed carriers were coded
as informal, union/federation or litigation forms. This is an **audit signal, not a population proportion**:
the registry and issue filter are purposive, and `legal_status_guess` is not a verified legal-status census.
It is included only as competing pressure against a simple “NPO-law growth caused base movements to
incorporate” story and must be regenerated after any legal-status review.

## Principal checkpoints before any integration

`human_review_queue.csv` contains 20 row-level research candidates for a later formal HR builder. **It is not a
formally dispatched HR task and the principal should not process all 20 now.** The next checkpoint should ask
only these seven high-leverage bundle decisions:

1. **Baseline use:** H98_001 — retain the 1998 course-fieldwork source as a context box, or literature-only?
2. **Core hypothesis:** H98_002 + H98_003 — pursue divergent institutionalization/division-of-labor, or keep
   the legal-NPO series as background only?
3. **Case chronology:** H98_004 + H98_014 — expose the compressed Futenma round labels and parallel filings?
4. **Negative institutional entry:** H98_006 — include jurisdictional nonentry as a formal comparison case?
5. **Documentation mechanism:** H98_005 + H98_007 + H98_008 — test whether legal/procedural hosting, not
   social centrality, explains historical visibility?
6. **Sakishima local priority:** H98_013 + H98_015 — dispatch Miyako/Yonaguni primary-material retrieval first?
7. **Identity/continuity priority:** NR05OS002 + NR05OS003 + NR05OS005 — spend local/archive effort on
   A076/A055/A069 formation and continuity?

Only after these bundle choices should a formal HR task be generated for the selected row-level candidates.

## Not safe to conclude

- The NPO Law caused Okinawa civic activity or base movements to grow/professionalize.
- Base-accountability actors became NPO corporations at the same rate as the prefecture-wide universe.
- Co-signers, co-parties, meeting attendees or mentioned unions/groups formed stable alliances.
- A lawsuit round is a new actor, or different rounds have identical members.
- A current organization page's historical claim proves uninterrupted activity.
- The absence of an online source proves organizational absence.
"""


def build_timeline_svg() -> str:
    """Render a dependency-free SVG with a separate macro-count panel."""

    width = 1800
    height = 1060
    x0 = 220.0
    x1 = 1670.0
    year_min = 1998.0
    # Keep a small within-2012 tail so the dated August 2012 anchor is not
    # pushed outside the panel. Calendar ticks still stop at 2012.
    year_max = 2012.75

    def year_x(year: float) -> float:
        return x0 + (year - year_min) / (year_max - year_min) * (x1 - x0)

    relation_style = {
        "contemporaneous_primary": ("#2563a6", "#eaf3fb", "同期一手"),
        "retrospective": ("#b9682a", "#fbefe5", "后来回顾／正式追溯"),
        "secondary": ("#2e7d69", "#e9f5f1", "二手重建"),
        "lead": ("#6b7280", "#f1f3f5", "线索"),
    }
    relation_node_label = {
        "contemporaneous_primary": "同期",
        "retrospective": "追溯",
        "secondary": "二手",
        "lead": "线索",
    }

    def multiline_text(
        x: float,
        y: float,
        text: str,
        *,
        size: int = 12,
        weight: int = 500,
        fill: str = "#24313a",
        anchor: str = "middle",
        line_height: int = 15,
    ) -> str:
        parts = text.split("|")
        tspans = []
        for index, part in enumerate(parts):
            dy = "0" if index == 0 else str(line_height)
            tspans.append(
                f'<tspan x="{x:.1f}" dy="{dy}">{escape(part)}</tspan>'
            )
        return (
            f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" '
            f'font-size="{size}" font-weight="{weight}" fill="{fill}">'
            + "".join(tspans)
            + "</text>"
        )

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" '
        'aria-labelledby="title desc">',
        "<title id=\"title\">1998–2012 载体—制度场域—材料留存时间图</title>",
        (
            "<desc id=\"desc\">上方面板是独立数量轴的全县认证NPO背景；下方面板按载体、制度场域、"
            "留存材料三条泳道展示选择性历史锚点，颜色表示来源关系。</desc>"
        ),
        "<style>",
        (
            "text{font-family:'Noto Sans CJK SC','Microsoft YaHei','Yu Gothic',sans-serif}"
            ".panel{fill:#fbfcfd;stroke:#cbd5dc;stroke-width:1.2}"
            ".grid{stroke:#dce3e8;stroke-width:1}"
            ".axis{stroke:#77858f;stroke-width:1.2}"
            ".lane{stroke:#b8c4cb;stroke-width:1.1}"
            ".connector{stroke:#a6b0b7;stroke-width:1.2;fill:none}"
            ".node{stroke-width:1.4}"
        ),
        "</style>",
        '<rect width="1800" height="1060" fill="#f4f6f7"/>',
        multiline_text(80, 48, "NR-05｜1998–2012 载体—制度场域—材料留存", size=25, weight=700, anchor="start"),
        multiline_text(
            80,
            78,
            "研究候选图：宏观认证 NPO 数量与下方组织／事件锚点分面、分母和纵轴；不可相除或合并",
            size=13,
            weight=500,
            fill="#56636c",
            anchor="start",
        ),
        '<rect class="panel" x="70" y="105" width="1660" height="245" rx="12"/>',
        multiline_text(
            92,
            137,
            "A. 全县认证 NPO 法人数量背景（独立数量轴）",
            size=17,
            weight=700,
            anchor="start",
        ),
        multiline_text(
            92,
            161,
            "所有领域的累计认证数；不是本项目 actor 数，也不表示活动、寿命或基地议题",
            size=12,
            fill="#56636c",
            anchor="start",
        ),
    ]

    macro_base_y = 320
    macro_top_y = 185
    for value in [0, 275, 550]:
        y = macro_base_y - value / 550 * (macro_base_y - macro_top_y)
        parts.append(
            f'<line class="grid" x1="{x0:.1f}" y1="{y:.1f}" x2="{x1:.1f}" y2="{y:.1f}"/>'
        )
        parts.append(
            multiline_text(
                x0 - 16,
                y + 4,
                str(value),
                size=10,
                fill="#66747d",
                anchor="end",
            )
        )
    macro_points = [
        (1999, 6, "secondary", "6"),
        (2004, 163, "secondary", "163"),
        (2012, 550, "contemporaneous_primary", "550"),
    ]
    poly_points = []
    for year, value, relationship, label in macro_points:
        x = year_x(float(year))
        y = macro_base_y - value / 550 * (macro_base_y - macro_top_y)
        color, fill, _ = relation_style[relationship]
        poly_points.append(f"{x:.1f},{y:.1f}")
        parts.extend(
            [
                f'<line x1="{x:.1f}" y1="{macro_base_y}" x2="{x:.1f}" y2="{y:.1f}" '
                f'stroke="{color}" stroke-width="16" opacity="0.22"/>',
                f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6.5" fill="{fill}" stroke="{color}" stroke-width="2"/>',
                multiline_text(x, y - 13, label, size=12, weight=700, fill=color),
                multiline_text(x, macro_base_y + 20, str(year), size=11, fill="#4b5962"),
            ]
        )
    parts.append(
        f'<polyline points="{" ".join(poly_points)}" fill="none" stroke="#607784" stroke-width="1.6"/>'
    )
    parts.append(
        multiline_text(
            1275,
            206,
            "1999–2004：RIETI 二手汇编|2012：冲绳县同期官方",
            size=11,
            fill="#53616a",
            anchor="start",
        )
    )
    parts.append(
        multiline_text(
            1275,
            250,
            "独立 count axis|禁止与下方面板节点数相除",
            size=11,
            weight=700,
            fill="#8a4e20",
            anchor="start",
        )
    )

    parts.extend(
        [
            '<rect class="panel" x="70" y="375" width="1660" height="610" rx="12"/>',
            multiline_text(
                92,
                410,
                "B. 选择性历史锚点：谁承载 → 进入何种场域 → 留下什么材料",
                size=17,
                weight=700,
                anchor="start",
            ),
            multiline_text(
                92,
                434,
                "节点是机制例证，不是全量事件计数；竖线只连接同一锚点内部的载体、场域与记录",
                size=12,
                fill="#56636c",
                anchor="start",
            ),
        ]
    )

    lane_y = {"carrier": 550, "venue": 700, "record": 850}
    for label, key in [
        ("载体／组织形式", "carrier"),
        ("制度场域", "venue"),
        ("留存材料", "record"),
    ]:
        y = lane_y[key]
        parts.append(f'<line class="lane" x1="{x0:.1f}" y1="{y}" x2="{x1:.1f}" y2="{y}"/>')
        parts.append(
            multiline_text(92, y + 4, label, size=13, weight=700, anchor="start")
        )
    for year in range(1998, 2013):
        x = year_x(float(year))
        parts.append(
            f'<line class="grid" x1="{x:.1f}" y1="455" x2="{x:.1f}" y2="940" opacity="0.65"/>'
        )
        parts.append(multiline_text(x, 962, str(year), size=10, fill="#65727b"))

    nodes = [
        {
            "anchor": "H98_001",
            "carrier_x": year_x(1998),
            "venue_x": year_x(1998),
            "record_x": year_x(1998),
            "carrier": "课程田野|（非 actor）",
            "venue": "无指定|制度场域",
            "record": "琉大论文|1998",
            "relationship": "secondary",
            "y_offset": 0,
        },
        {
            "anchor": "H98_003",
            "carrier_x": year_x(1999),
            "venue_x": year_x(2009.37),
            "record_x": year_x(2009.37),
            "carrier": "ONC 前身|1999-06",
            "venue": "NPO 认证|2009-05-14",
            "record": "官网＋访谈|＋官方名册",
            "relationship": "retrospective",
            "y_offset": 0,
        },
        {
            "anchor": "H98_004",
            "carrier_x": year_x(2002),
            "venue_x": year_x(2002),
            "record_x": year_x(2002),
            "carrier": "A053／住民|第一轮",
            "venue": "那霸地裁|2002–03",
            "record": "团体沿革|＋法院判决",
            "relationship": "retrospective",
            "y_offset": 0,
        },
        {
            "anchor": "H98_005",
            "carrier_x": year_x(2003.73),
            "venue_x": year_x(2003.73),
            "record_x": year_x(2003.73),
            "carrier": "具名原告|＋律师",
            "venue": "美国联邦法院|2003-09-25",
            "record": "同日起诉状|＋发布",
            "relationship": "contemporaneous_primary",
            "y_offset": -42,
        },
        {
            "anchor": "H98_006",
            "carrier_x": year_x(2004.13),
            "venue_x": year_x(2004.13),
            "record_x": year_x(2004.13),
            "carrier": "913 名个人|非 actor",
            "venue": "公害调停|管辖排除",
            "record": "官方终结|事件记录",
            "relationship": "retrospective",
            "y_offset": 42,
        },
        {
            "anchor": "H98_008",
            "carrier_x": year_x(2004.44),
            "venue_x": year_x(2004.44),
            "record_x": year_x(2004.44),
            "carrier": "A004|NACS-J",
            "venue": "环境评价|意见程序",
            "record": "正式意见|2004-06-10",
            "relationship": "contemporaneous_primary",
            "y_offset": 0,
        },
        {
            "anchor": "H98_009",
            "carrier_x": year_x(2005.38),
            "venue_x": year_x(2005.38),
            "record_x": year_x(2005.38),
            "carrier": "个人住民原告|A055仅支援",
            "venue": "那霸地裁|泡濑公金",
            "record": "法院判决|＋近时报导",
            "relationship": "retrospective",
            "y_offset": 42,
        },
        {
            "anchor": "H98_010",
            "carrier_x": year_x(2008.12),
            "venue_x": year_x(2008.12),
            "record_x": year_x(2008.12),
            "carrier": "A115|冲绳县本部",
            "venue": "冲绳县|请求",
            "record": "行政日志|2008-02-14",
            "relationship": "contemporaneous_primary",
            "y_offset": 0,
        },
        {
            "anchor": "H98_011",
            "carrier_x": year_x(2010.37),
            "venue_x": year_x(2010.37),
            "record_x": year_x(2010.37),
            "carrier": "A005＋名单|事件参与",
            "venue": "中央省厅|共同声明",
            "record": "WWF 同日|67 团体名单",
            "relationship": "contemporaneous_primary",
            "y_offset": -42,
        },
        {
            "anchor": "H98_012",
            "carrier_x": year_x(2011.32),
            "venue_x": year_x(2011.32),
            "record_x": year_x(2011.32),
            "carrier": "A052|第三轮",
            "venue": "那霸地裁|冲绳支部",
            "record": "原告团|现行沿革",
            "relationship": "retrospective",
            "y_offset": 42,
        },
        {
            "anchor": "H98_013",
            "carrier_x": year_x(2011.47),
            "venue_x": year_x(2011.47),
            "record_x": year_x(2011.47),
            "carrier": "A096|集会载体",
            "venue": "公开集会|下地岛",
            "record": "宫古每日|近时报导",
            "relationship": "secondary",
            "y_offset": -42,
        },
        {
            "anchor": "H98_014",
            "carrier_x": year_x(2012.0),
            "venue_x": year_x(2012.0),
            "record_x": year_x(2012.0),
            "carrier": "A053|第二轮标签",
            "venue": "并行案件|2012–13",
            "record": "团体沿革|＋法院判决",
            "relationship": "retrospective",
            "y_offset": 0,
        },
        {
            "anchor": "H98_015",
            "carrier_x": year_x(2012.65),
            "venue_x": year_x(2012.65),
            "record_x": year_x(2012.65),
            "carrier": "A015|一次性实委会?",
            "venue": "意见广告|记者会",
            "record": "政党媒体|单一线索",
            "relationship": "lead",
            "y_offset": 42,
        },
    ]

    carrier_fill = "#f2efe8"
    carrier_stroke = "#8c806d"
    venue_fill = "#eeeaf5"
    venue_stroke = "#76658f"
    box_w = 94
    box_h = 48
    for node in nodes:
        cx = node["carrier_x"]
        vx = node["venue_x"]
        rx = node["record_x"]
        y_offset = node["y_offset"]
        carrier_y = lane_y["carrier"] + y_offset
        venue_y = lane_y["venue"] + y_offset
        record_y = lane_y["record"] + y_offset
        relationship = node["relationship"]
        color, fill, _ = relation_style[relationship]
        relationship_label = relation_node_label[relationship]
        parts.extend(
            [
                f'<path class="connector" d="M {cx:.1f} {carrier_y + box_h / 2:.1f} '
                f'L {vx:.1f} {venue_y - box_h / 2:.1f} '
                f'L {rx:.1f} {record_y - box_h / 2:.1f}"/>',
                f'<rect class="node" x="{cx - box_w / 2:.1f}" y="{carrier_y - box_h / 2:.1f}" '
                f'width="{box_w}" height="{box_h}" rx="8" fill="{carrier_fill}" stroke="{carrier_stroke}"/>',
                f'<rect class="node" x="{vx - box_w / 2:.1f}" y="{venue_y - box_h / 2:.1f}" '
                f'width="{box_w}" height="{box_h}" rx="8" fill="{venue_fill}" stroke="{venue_stroke}"/>',
                f'<rect class="node" x="{rx - box_w / 2:.1f}" y="{record_y - box_h / 2:.1f}" '
                f'width="{box_w}" height="{box_h}" rx="8" fill="{fill}" stroke="{color}"/>',
                multiline_text(cx, carrier_y - 7, node["carrier"], size=10, weight=600, line_height=13),
                multiline_text(vx, venue_y - 7, node["venue"], size=10, weight=600, line_height=13),
                multiline_text(rx, record_y - 7, node["record"], size=10, weight=600, fill=color, line_height=13),
                multiline_text(cx, carrier_y - 34, node["anchor"], size=9, weight=700, fill="#59666f"),
                multiline_text(rx, record_y + 40, relationship_label, size=9, weight=600, fill=color),
            ]
        )

    legend_x = 840
    legend_y = 1014
    parts.append(multiline_text(720, legend_y + 4, "材料来源关系：", size=11, weight=700, anchor="end"))
    for index, relationship in enumerate(
        ["contemporaneous_primary", "retrospective", "secondary", "lead"]
    ):
        color, fill, label = relation_style[relationship]
        x = legend_x + index * 225
        parts.append(
            f'<rect x="{x}" y="{legend_y - 12}" width="18" height="18" rx="4" fill="{fill}" stroke="{color}" stroke-width="1.5"/>'
        )
        parts.append(
            multiline_text(x + 27, legend_y + 2, label, size=10, fill="#45535c", anchor="start")
        )
    parts.append(
        multiline_text(
            70,
            1041,
            "全部为 research_only 候选；竖线不是组织间关系边，来源可见性不是社会影响力。",
            size=11,
            weight=600,
            fill="#8a4e20",
            anchor="start",
        )
    )
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def build_figure_brief() -> str:
    return """# Figure brief — 载体—制度场域—材料留存时间图

Asset: `fig1_carrier_venue_trace_timeline_v1.svg`
Status: `research_only / candidate / ai_seeded / not_frontend_ready`

## Purpose

This figure visualizes the NR-05 empirical judgment: post-1998 traceability grows selectively through legal,
administrative and organization-hosted document regimes. It is not an actor-network graph and not an event
frequency chart.

## Panel design

- **Panel A** uses its own count axis for all-field Okinawa certified NPO corporations: 1999=6, 2004=163,
  2012=550. It is a macro institutional background and has a different denominator from every item below.
- **Panel B** is a qualitative three-lane timeline: carrier/organizational form → institutional venue →
  surviving record. Vertical or diagonal connectors join fields within one historical anchor only.
- The two panels share calendar position for orientation but **do not share a numeric y-axis**. No ratio,
  subtraction or trend comparison between the panels is valid.

## Source-relationship encoding

- Blue: `contemporaneous_primary`
- Orange: `retrospective`
- Green: `secondary`
- Gray: `lead`

Color applies to the surviving-record node, not to actor ideology, evidence certainty or organizational type.
All items still require the candidate/human-review gate.

## Reading route

1. Read Panel A only as the expansion of a legal/documentary environment.
2. In Panel B compare the materials left by a U.S. complaint, EIA opinion, court judgment, administrative
   diary, organization history, local newspaper and single party-news lead.
3. Notice that ONC's carrier starts in 1999 while the official certification field is 2009-05-14; the later
   interview's 2008 transition claim remains a separate unresolved stage.
4. Notice the explicit negative cases: 913 applicants are not actorized; A055 is support/movement, not the
   organizational plaintiff; co-signing is an event hyperedge, not an alliance.

## Data sources

- Panel A: NR05S002 and NR05S003/NR05S004.
- Panel B: selected H98_001, H98_003–H98_015 anchors. It is selective by design; omitted anchors are not
  absent events.

## Must not be read as

- the number or proportion of base-accountability actors that incorporated;
- a causal effect of the NPO Law;
- a network or alliance structure;
- organizational longevity;
- a complete 1998–2012 event census;
- evidence that actors with better archives were socially more central.

## Reproduce

```powershell
python scripts\\make_history_1998_2012_online_v1.py
```
"""


def build_readme() -> str:
    return """# history_1998_2012_online_v1

Isolated NR-05 research package for the Phase-1 Okinawa NGO/civic-organization project.

## Contract files

- `historical_anchor_candidates.csv` — 15 dated event/context anchors.
- `organization_status_candidates.csv` — formation, legal-status, minimum-active-date and round-label candidates.
- `source_candidates.csv` — exact source/date/locator/support-scope crosswalk.
- `search_log.md` — query tracks, date protocol and known exclusions.
- `online_exhausted_gaps.csv` — online exhaustion and local/new-primary needs.
- `human_review_queue.csv` — 20-row research candidate pool; explicitly **not** a formally dispatched HR task.
- `brief.md` — empirical judgment, interpretation candidates and novelty boundaries.
- `fig1_carrier_venue_trace_timeline_v1.svg` — separated macro-context and carrier/venue/record timeline.
- `fig1_carrier_venue_trace_timeline_v1_brief.md` — figure encoding and non-inference contract.
- `validation_report.md` — machine gates and file hashes.

## Reproduce

```powershell
python scripts\\make_history_1998_2012_online_v1.py
python -m unittest discover -s tests -p "test_make_history_1998_2012_online_v1.py" -v
```

To test in another directory:

```powershell
python scripts\\make_history_1998_2012_online_v1.py --output-dir $env:TEMP\\nr05_check
```

## Hard boundaries

This package does not approve any actor, source, edge, alliance, funding relation, genealogy or continuity
claim. It does not write central tables, source archives, frontend contracts or control documents. Every CSV
row remains `research_only / candidate / ai_seeded / not_frontend_ready / central_writeback=no`.
"""


def write_validation_report(
    output_dir: Path,
    checks: list[str],
    row_counts: Mapping[str, int],
    hashed_files: Iterable[str],
) -> None:
    lines = [
        "# NR-05 validation report",
        "",
        f"Package date: {PACKAGE_DATE}",
        "",
        "## Row counts",
        "",
    ]
    for name, count in row_counts.items():
        lines.append(f"- `{name}`: {count}")
    lines.extend(["", "## Gates", ""])
    lines.extend(f"- {check}" for check in checks)
    lines.extend(
        [
            "",
            "The 20-row `human_review_queue.csv` is a research candidate pool only. It has not entered the "
            "formal HR ledger; the brief reduces the immediate principal checkpoint to seven bundled decisions.",
            "",
            "## Known exclusions",
            "",
            "- Full-text review corrected a search-snippet trap: the A068→A019 developmental reorganization "
            "is a 1997 event, while 2000 refers to later actions. It is excluded from NR-05 anchors and central "
            "`LC002` is not rewritten.",
            "- Archive catalog entries are locator-only and never treated as the underlying primary item.",
            "- Spencer (2003) already covers multi-issue anti-base framing; NR-05 does not claim that theme as novel.",
            "- Prefecture-wide NPO counts do not infer incorporation, activity or survival of project actors.",
            "- Smaller RIETI business-report/data-available sample counts are excluded from the cumulative "
            "certification series because the denominators differ.",
            "",
            "## Deterministic file hashes",
            "",
        ]
    )
    for name in hashed_files:
        lines.append(f"- `{name}`: `{sha256(output_dir / name)}`")
    lines.extend(
        [
            "",
            "## Write boundary",
            "",
            "The generator wrote only this output directory. It has no central-table, source-archive, frontend "
            "or control-document write path.",
            "",
        ]
    )
    (output_dir / "validation_report.md").write_text(
        "\n".join(lines), encoding="utf-8", newline="\n"
    )


def build(output_dir: Path) -> None:
    anchors = historical_anchors()
    statuses = organization_status_candidates()
    sources = source_candidates()
    gaps = online_exhausted_gaps()
    reviews = human_review_queue(anchors, statuses)
    checks = validate_rows(anchors, statuses, sources, gaps, reviews)
    timeline_svg = build_timeline_svg()
    assert "独立数量轴" in timeline_svg
    assert "载体／组织形式" in timeline_svg
    assert "制度场域" in timeline_svg
    assert "留存材料" in timeline_svg
    assert "禁止与下方面板节点数相除" in timeline_svg
    checks.append("PASS separated macro-count and carrier/venue/record SVG contract")

    output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(output_dir / "historical_anchor_candidates.csv", ANCHOR_FIELDS, anchors)
    write_csv(output_dir / "organization_status_candidates.csv", STATUS_FIELDS, statuses)
    write_csv(output_dir / "source_candidates.csv", SOURCE_FIELDS, sources)
    write_csv(output_dir / "online_exhausted_gaps.csv", GAP_FIELDS, gaps)
    write_csv(output_dir / "human_review_queue.csv", REVIEW_FIELDS, reviews)
    (output_dir / "search_log.md").write_text(
        build_search_log(), encoding="utf-8", newline="\n"
    )
    (output_dir / "brief.md").write_text(
        build_brief(anchors, statuses, sources, gaps),
        encoding="utf-8",
        newline="\n",
    )
    (output_dir / "README.md").write_text(
        build_readme(), encoding="utf-8", newline="\n"
    )
    (output_dir / "fig1_carrier_venue_trace_timeline_v1.svg").write_text(
        timeline_svg, encoding="utf-8", newline="\n"
    )
    (
        output_dir / "fig1_carrier_venue_trace_timeline_v1_brief.md"
    ).write_text(build_figure_brief(), encoding="utf-8", newline="\n")

    hashed_files = [
        "historical_anchor_candidates.csv",
        "organization_status_candidates.csv",
        "source_candidates.csv",
        "online_exhausted_gaps.csv",
        "human_review_queue.csv",
        "search_log.md",
        "brief.md",
        "README.md",
        "fig1_carrier_venue_trace_timeline_v1.svg",
        "fig1_carrier_venue_trace_timeline_v1_brief.md",
    ]
    write_validation_report(
        output_dir,
        checks,
        {
            "historical_anchor_candidates.csv": len(anchors),
            "organization_status_candidates.csv": len(statuses),
            "source_candidates.csv": len(sources),
            "online_exhausted_gaps.csv": len(gaps),
            "human_review_queue.csv": len(reviews),
        },
        hashed_files,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Output directory (default: {DEFAULT_OUTPUT_DIR})",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    build(args.output_dir)
    print(f"NR-05 package written to {args.output_dir}")


if __name__ == "__main__":
    main()
