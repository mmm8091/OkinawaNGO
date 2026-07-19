from __future__ import annotations

import csv
import hashlib
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from tempfile import TemporaryDirectory
from textwrap import dedent

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "interim"
META = ROOT / "data" / "metadata"
OUT = ROOT / "outputs" / "schema_alias_freeze_v1"

ACTOR_FILE = DATA / "01_actor_registry_initial_v0.csv"
ALIAS_FILE = DATA / "02_actor_aliases_initial_v0.csv"
PLACE_FILE = DATA / "04_place_registry_v0.csv"
ACTOR_PLACE_FILE = DATA / "08_actor_place_edges_initial_v0.csv"
AEV_FILE = DATA / "09_actor_event_venue_edges_v0.csv"
PATHWAY_FILE = DATA / "26_actor_event_venue_target_entry_modes_v0.csv"
VENUE_FILE = META / "venue_taxonomy_v0.csv"

MAIN_FILE = DATA / "36_schema_alias_freeze_candidates_v1.csv"
ACTOR_AUDIT_FILE = OUT / "actor_field_audit_v1.csv"
ACTOR_MAPPING_FILE = OUT / "actor_value_mapping_v1.csv"
ALIAS_AUDIT_FILE = OUT / "alias_audit_v1.csv"
ALIAS_BOUNDARY_FILE = OUT / "alias_boundary_audit_v1.csv"
PLACE_AUDIT_FILE = OUT / "place_hierarchy_alias_audit_v1.csv"
PLACE_CONFLICT_FILE = OUT / "place_crosskey_conflicts_v1.csv"
VENUE_AUDIT_FILE = OUT / "venue_taxonomy_audit_v1.csv"
VENUE_CONFLICT_FILE = OUT / "venue_reference_conflicts_v1.csv"
REL_ACTION_FILE = OUT / "relation_action_value_mapping_v1.csv"
LINT_FILE = OUT / "lint_rules_v1.csv"
IMPACT_FILE = OUT / "impact_counts_v1.csv"
HR_FILE = OUT / "HR029_schema_alias_freeze_review_v0.csv"
BRIEF_FILE = OUT / "schema_alias_freeze_brief_v1.md"
README_FILE = OUT / "README.md"
VALIDATION_FILE = OUT / "validation_report_v1.md"
FIG_READINESS_PNG = OUT / "fig_schema_freeze_readiness_v1.png"
FIG_READINESS_SVG = OUT / "fig_schema_freeze_readiness_v1.svg"
FIG_VOCAB_PNG = OUT / "fig_vocabulary_consolidation_v1.png"
FIG_VOCAB_SVG = OUT / "fig_vocabulary_consolidation_v1.svg"


MAIN_FIELDS = [
    "candidate_id", "domain", "object_id", "object_name", "field_name",
    "current_value", "proposed_value", "candidate_disposition",
    "affected_row_count", "source_tables", "reason", "risk_if_wrong",
    "requires_human_review", "hr_item_id", "machine_status",
    "interpretation_limit",
]

HR_FIELDS = [
    "review_item_id", "task_id", "candidate_id", "domain", "object_id",
    "object_name", "field_name", "current_value", "proposed_value",
    "source_context", "review_question", "accept_effect",
    "required_boundary", "decision", "human_reviewer", "review_date",
    "review_note",
]
HUMAN_FIELDS = ("decision", "human_reviewer", "review_date", "review_note")

PLACE_CONFLICT_FIELDS = [
    "candidate_id", "edge_id", "actor_id", "current_place_id",
    "current_place_name", "registry_name_for_current_id",
    "proposed_resolution", "requires_human_review", "hr_item_id",
    "source_ref", "notes",
]


IDENTITY_ONLY_CLASS_ACTORS = {
    "A087", "A088", "A089", "A090", "A091", "A092", "A093",
    "A095", "A096", "A097", "A098", "A099", "A100", "A101",
}


ACTOR_CLASS_MAP = {
    "base_community_service_actor": ("base_community_service_actor", "freeze_as_is", False),
    "base_spouse_charity_network": ("base_spouse_charity_network", "freeze_as_is", False),
    "base_spouse_club": ("base_spouse_club", "freeze_as_is", False),
    "citizen_group": ("citizen_group", "freeze_as_is", False),
    "citizen_network": ("citizen_network", "freeze_as_is", False),
    "corporate_sponsor": ("corporate_sponsor", "freeze_as_is", False),
    "domestic_japan_ngo": ("domestic_japan_ngo", "freeze_as_is", False),
    "executive_committee": ("executive_committee", "freeze_as_is", False),
    "funder_or_intermediary": ("funder_or_intermediary", "freeze_as_is", False),
    "international_advocacy_actor": ("international_advocacy_actor", "freeze_as_is", False),
    "international_ngo": ("international_ngo", "freeze_as_is", False),
    "labor_or_education_union": ("labor_union", "human_review", True),
    "labor_union": ("labor_union", "freeze_as_is", False),
    "labor_union_federation": ("labor_union_federation", "freeze_as_is", False),
    "lawyers_network": ("lawyers_network", "freeze_as_is", False),
    "local_business_sponsor": ("local_business_sponsor", "freeze_as_is", False),
    "local_civic_actor": ("local_civic_actor", "freeze_as_is", False),
    "local_international_cooperation_ngo": ("local_international_cooperation_ngo", "freeze_as_is", False),
    "local_npo": ("local_npo", "freeze_as_is", False),
    "media_or_advocacy_actor": ("media_advocacy_actor", "mechanical_normalize", False),
    "public_diplomacy_grant_program": ("public_diplomacy_grant_program", "freeze_as_is", False),
    "public_diplomacy_or_exchange_actor": ("public_diplomacy_or_exchange_actor", "freeze_as_is", False),
    "public_institution_partner": ("public_institution_partner", "freeze_as_is", False),
    "womens_organization": ("womens_organization", "freeze_as_is", False),
    "womens_or_community_organization": ("womens_network", "human_review", True),
    "womens_or_human_rights_ngo": ("womens_human_rights_ngo", "mechanical_normalize", False),
}


ORIGIN_MAP = {
    value: (value, "freeze_as_is", False)
    for value in (
        "okinawa_local", "japan_domestic", "us_origin", "international",
        "mixed_or_network", "public_institution", "corporate",
    )
}


LEGAL_STATUS_MAP = {
    "ngo": ("nongovernmental_nonprofit", "mechanical_normalize", False),
    "informal": ("informal_association", "mechanical_normalize", False),
    "informal_network": ("informal_network", "freeze_as_is", False),
    "informal_association": ("informal_association", "freeze_as_is", False),
    "unclear": ("legal_form_unresolved", "freeze_as_unresolved", False),
    "public_interest_foundation": ("public_interest_incorporated_foundation", "mechanical_normalize", False),
    "network": ("legal_form_unresolved_network", "freeze_as_unresolved", False),
    "NPO法人": ("specified_nonprofit_corporation", "mechanical_normalize", False),
    "labor_union": ("labor_union", "freeze_as_is", False),
    "informal_or_project": ("legal_form_unresolved", "freeze_as_unresolved", False),
    "任意団体": ("informal_association", "mechanical_normalize", False),
    "company": ("for_profit_company", "mechanical_normalize", False),
    "nonprofit_or_base_office": ("nonprofit_or_branch_office_unresolved", "freeze_as_unresolved", False),
    "npo": ("specified_nonprofit_corporation", "mechanical_normalize", False),
    "citizen_group": ("legal_form_unresolved_citizen_group", "freeze_as_unresolved", False),
    "litigation_group": ("litigation_group", "freeze_as_is", False),
    "government_office": ("government_office", "freeze_as_is", False),
    "labor_union_federation": ("labor_union_federation", "freeze_as_is", False),
    "litigation_team": ("litigation_team", "freeze_as_is", False),
    "not_for_profit": ("not_for_profit_organization", "mechanical_normalize", False),
    "public_interest_foundation_or_association": ("public_interest_incorporated_body_unspecified", "freeze_as_unresolved", False),
    "registered_nonprofit（EIN 98-0227149 pending Form 990 check）": ("registered_nonprofit_pending_document_check", "freeze_as_unresolved", False),
    "club/private_org": ("private_membership_organization_status_unresolved", "freeze_as_unresolved", False),
    "registered_nonprofit（EIN 98-0214323）": ("registered_nonprofit", "mechanical_normalize", False),
    "501c3（EIN 98-0346507）": ("us_501c3_nonprofit", "mechanical_normalize", False),
    "informal_network（任意ネットワーク・国際協力NGO）": ("informal_network", "mechanical_normalize", False),
    "npo_or_ngo": ("nonprofit_form_unresolved", "freeze_as_unresolved", False),
    "public_institution": ("public_institution", "freeze_as_is", False),
    "public_private_partnership": ("public_private_partnership", "freeze_as_is", False),
    "grant_program": ("grant_program", "freeze_as_is", False),
    "informal（任意の実行委員会）": ("informal_executive_committee", "mechanical_normalize", False),
    "foundation": ("foundation_status_unspecified", "freeze_as_unresolved", False),
    "501c3/registered_nonprofit（EIN 46-0598583）": ("us_501c3_nonprofit", "mechanical_normalize", False),
    "ngo_or_association": ("nonprofit_form_unresolved", "freeze_as_unresolved", False),
    "informal_or_npo": ("legal_form_unresolved", "freeze_as_unresolved", False),
    "project_or_network": ("legal_form_unresolved", "freeze_as_unresolved", False),
    "social_movement_center": ("legal_form_unresolved_social_movement_center", "freeze_as_unresolved", False),
    "professional_association": ("professional_association", "freeze_as_is", False),
    "npo_or_association": ("nonprofit_form_unresolved", "freeze_as_unresolved", False),
    "chapter": ("organizational_chapter", "mechanical_normalize", False),
    "npo_or_project": ("legal_form_unresolved", "freeze_as_unresolved", False),
    "任意団体（法人格待核实）": ("informal_association_pending_legal_check", "freeze_as_unresolved", False),
    "lawyers_network": ("legal_form_unresolved_professional_network", "freeze_as_unresolved", False),
    "association_or_regional_ywca": ("regional_association_or_chapter", "freeze_as_unresolved", False),
    "association_or_unclear": ("legal_form_unresolved_association", "freeze_as_unresolved", False),
}


ALIAS_TYPE_MAP = {
    "acronym": ("acronym", "freeze_as_is", False),
    "canonical_variant": ("orthographic_variant", "mechanical_normalize", False),
    "context_limited_alias": ("context_limited_alias", "human_review", True),
    "chapter_listing_variant": ("chapter_listing_variant", "freeze_from_human_anchor", False),
    "deprecated_working_name": ("deprecated_search_label", "freeze_from_human_anchor", False),
    "descriptive_variant": ("descriptive_variant", "freeze_as_is", False),
    "former_canonical": ("former_registry_canonical", "mechanical_normalize", False),
    "former_name": ("former_name", "freeze_as_is", False),
    "japanese_name": ("language_name", "mechanical_normalize", False),
    "media_short_name": ("media_short_name", "freeze_from_human_anchor", False),
    "network_name": ("network_name", "freeze_from_human_anchor", False),
    "name_variant": ("documented_name_variant", "freeze_from_human_anchor", False),
    "original_name": ("former_name", "mechanical_normalize", False),
    "possible_canonical_variant": ("unresolved_canonical_variant", "human_review", True),
    "predecessor_of": ("predecessor_name_nonidentity", "human_review", True),
    "round_of": ("case_round_label_nonidentity", "human_review", True),
    "short_name": ("short_name", "freeze_as_is", False),
    "signatory_name": ("event_list_name", "mechanical_normalize", False),
    "tax_name": ("registered_name_variant", "mechanical_normalize", False),
    "variant": ("orthographic_variant", "mechanical_normalize", False),
}


PLACE_PLAN = {
    "P001": ("Okinawa Prefecture", "prefecture", "", "Okinawa Prefecture;Okinawa;沖縄県", False, "Project-wide container; not an event site."),
    "P002": ("Henoko", "site", "P017", "Henoko;辺野古", False, "Conflict locality nested under Nago for Phase-1 hierarchy."),
    "P003": ("Oura Bay", "site", "P017", "Oura Bay;Ōura Bay;大浦湾", False, "Marine conflict site nested under Nago for Phase-1 hierarchy."),
    "P004": ("Futenma", "site", "P018", "Futenma;普天間", True, "Must denote the Futenma issue/locality layer, not duplicate MCAS Futenma P010."),
    "P005": ("Kadena Air Base", "base_site", "P001", "Kadena;Kadena Air Base;嘉手納基地", True, "Current name Kadena can mean municipality or air base; current notes indicate the base."),
    "P006": ("Camp Schwab", "base_site", "P017", "Camp Schwab;キャンプ・シュワブ", False, "Military installation nested under Nago."),
    "P007": ("Camp Foster", "base_site", "P001", "Camp Foster;キャンプ・フォスター", False, "Installation spans the central-island field; prefecture is the safe parent."),
    "P008": ("Camp Hansen", "base_site", "P001", "Camp Hansen;キャンプ・ハンセン", False, "Installation spans multiple local areas; prefecture is the safe parent."),
    "P009": ("Camp Kinser", "base_site", "P001", "Camp Kinser;キャンプ・キンザー", False, "Urasoe is not a current place node; prefecture is the available parent."),
    "P010": ("MCAS Futenma", "base_site", "P018", "MCAS Futenma;Marine Corps Air Station Futenma;普天間飛行場", False, "Physical installation distinct from P004 Futenma issue/locality layer."),
    "P011": ("Yonaguni Town", "municipality", "P001", "Yonaguni;Yonaguni Town;与那国町;与那国島", True, "Town, island and shorthand labels must remain queryable but not silently treated as identical spatial levels."),
    "P012": ("Ishigaki City", "municipality", "P001", "Ishigaki;Ishigaki City;石垣市;石垣島", True, "City and island labels overlap in sources and need an explicit alias-scope decision."),
    "P013": ("Miyakojima City", "municipality", "P001", "Miyako;Miyakojima City;宮古島市;宮古島", True, "Miyako can denote city, island or regional field; the current row is typed municipality."),
    "P014": ("JICA Okinawa", "institutional_site", "P001", "JICA Okinawa;JICA Okinawa Center;JICA沖縄;沖縄国際センター", False, "Institutional facility; Urasoe is not a current parent node."),
    "P015": ("U.S. Consulate General Naha", "institutional_site", "P020", "U.S. Consulate General Naha;在沖米国総領事館", False, "Institutional facility nested under Naha."),
    "P016": ("Takae", "site", "P001", "Takae;高江", False, "Local site; Higashi municipality is not a current parent node."),
    "P017": ("Nago", "municipality", "P001", "Nago;Nago City;名護市", False, "Municipality under Okinawa Prefecture."),
    "P018": ("Ginowan", "municipality", "P001", "Ginowan;Ginowan City;宜野湾市", False, "Municipality under Okinawa Prefecture."),
    "P019": ("Awase", "site", "P001", "Awase;泡瀬;泡瀬干潟", False, "Conflict site; Okinawa City is not a current parent node."),
    "P020": ("Naha", "municipality", "P001", "Naha;Naha City;那覇市", False, "Municipality and prefectural capital."),
    "P021": (
        "Sakishima Islands", "region", "P001",
        "Sakishima Islands;先島諸島;先島", False,
        "HR-025-approved regional node for sources explicitly naming Sakishima as a whole; never fan out to P011/P012/P013.",
    ),
}


ORPHAN_VENUE_PLAN = {
    "OBS_R10R001": ("V011_or_V015", True, "A JICA commissioned program may be coded by the commissioning agency or by a bounded policy-program forum; relation review did not settle venue semantics."),
    "OBS_R10R004": ("V010", True, "Okinawa City public-facility commission is a local-government administrative channel, subject to human venue confirmation."),
    "OBS_R10R005": ("V010", True, "Okinawa Prefecture multicultural-policy commission is a local-government administrative channel, subject to human venue confirmation."),
    "OBS_R10R006": ("V011", True, "MOFA NGO consultation commission is a national-ministry administrative channel, subject to human venue confirmation."),
    "OBS_R10R007": ("V011", True, "MOFA annual designation is a national-ministry administrative channel, subject to human venue confirmation."),
    "OBS_R10R008": ("V010", True, "The Okinawa Prefecture proposal-selected symposium contract is a local-government administrative channel, not government endorsement."),
    "OBS_R10R017": ("V015", True, "International-cooperation event may fit public_policy_meeting_or_forum, but event versus administrative venue needs a human choice."),
    "OBS_R10R018": ("V016", False, "USO Okinawa service presence is observed at a service/charity program site."),
    "OBS_R10R019": ("V016", False, "USO service sponsorship is observed at a service/charity program venue."),
    "OBS_R10R020": ("V016", False, "A direct USO Okinawa sponsor tier is observed in the service/charity program layer."),
    "OBS_R10R021": ("V016_or_no_applicable_venue", True, "A regional USO Indo-Pacific sponsor perimeter is not necessarily an Okinawa program-site occurrence."),
    "OBS_R10R022": ("V016", False, "Donation to USO is observed in the service/charity program field."),
    "OBS_R10R023": ("V016", False, "USO kitchen grant is a service/charity program-site observation."),
    "OBS_R10R024": ("no_applicable_venue_or_V016", True, "Umbrella membership is a relation, not necessarily a venue occurrence."),
    "OBS_R10R025": ("no_applicable_venue_or_V016", True, "Umbrella membership is a relation, not necessarily a venue occurrence."),
    "OBS_R10R026": ("no_applicable_venue_or_V016", True, "Umbrella membership is a relation, not necessarily a venue occurrence."),
    "OBS_R10R027": ("no_applicable_venue_or_V016", True, "Umbrella membership is a relation, not necessarily a venue occurrence."),
    "OBS_R10R035": ("new_public_diplomacy_program_channel_or_no_venue", True, "A grant opportunity is a program channel, not an awarded relation or obvious existing venue."),
}


RELATION_TYPE_MAP = {
    "administrative_collaboration": ("administrative_collaboration", "freeze_as_is", False),
    "aggregate_financial_contribution": ("aggregate_financial_contribution", "freeze_from_human_anchor", False),
    "aggregate_history": ("aggregate_financial_history_observation", "human_review", True),
    "co_presence_lead": ("co_presence_observation", "human_review", True),
    "commission": ("commission", "freeze_as_is", False),
    "coordination": ("coordination", "freeze_as_is", False),
    "designated_role": ("institutional_designation", "mechanical_normalize", False),
    "donation": ("donation", "freeze_as_is", False),
    "duplicate_replaced_by_F022": ("deprecated_nonrelation", "deprecate_exclude", False),
    "event_affiliation": ("event_affiliation", "freeze_as_is", False),
    "event_collaboration": ("event_collaboration", "freeze_as_is", False),
    "funding_contribution": ("aggregate_financial_contribution", "human_review", True),
    "grant": ("grant", "freeze_as_is", False),
    "grant_opportunity": ("grant_opportunity", "freeze_as_is", False),
    "in_kind_acquisition_assistance": ("in_kind_acquisition_assistance", "freeze_from_human_anchor", False),
    "in_kind_donation": ("in_kind_donation", "freeze_as_is", False),
    "joint_in_kind_contribution": ("joint_in_kind_contribution", "freeze_as_is", False),
    "legal_counsel": ("legal_counsel", "freeze_as_is", False),
    "legal_support": ("legal_support", "freeze_as_is", False),
    "network_membership": ("network_membership", "freeze_as_is", False),
    "ngo_consultant_commission": ("commission", "mechanical_normalize", False),
    "organizational_affiliation": ("organizational_affiliation", "freeze_as_is", False),
    "partner_action": ("partner_action", "freeze_as_is", False),
    "partnership": ("partnership", "freeze_as_is", False),
    "service": ("service", "freeze_as_is", False),
    "service_presence": ("service_presence", "freeze_as_is", False),
    "site_presence": ("site_presence", "freeze_as_is", False),
    "solidarity_branch": ("organizational_affiliation", "human_review", True),
    "sponsorship": ("sponsorship", "freeze_as_is", False),
}


ACTION_TYPE_MAP = {
    "co_signing": ("joint_statement_participation", "mechanical_normalize", False),
    "endorsement": ("endorsement", "freeze_as_is", False),
    "issue_campaign": ("issue_campaign", "freeze_as_is", False),
    "joint_statement": ("joint_statement_participation", "mechanical_normalize", False),
    "litigation": ("litigation", "freeze_as_is", False),
    "observation": ("observation", "freeze_as_is", False),
    "opinion_ad": ("opinion_ad", "freeze_as_is", False),
    "pathway_role": ("analytical_pathway_role", "separate_analytical_seed", False),
    "public_meeting": ("public_meeting", "freeze_as_is", False),
    "public_rally": ("public_rally", "freeze_as_is", False),
    "referendum": ("referendum", "freeze_as_is", False),
    "request": ("request", "freeze_as_is", False),
    "request_letter": ("request_submission_participation", "mechanical_normalize", False),
    "request_letter_and_civil_society_report": ("request_submission_participation", "mechanical_normalize", False),
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_csv_with_fields(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.exists():
        return [], []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = list(reader.fieldnames or [])
        return fields, list(reader)


def preserve_human_fields(
    generated_rows: list[dict[str, str]], existing_path: Path,
    generated_fields: list[str], *, identity_fields: tuple[str, ...],
) -> tuple[list[dict[str, str]], list[str], dict[str, int]]:
    """Preserve human-owned HR cells by stable review_item_id on regeneration."""
    existing_fields, existing_rows = read_csv_with_fields(existing_path)
    extra_fields = [field for field in existing_fields if field not in generated_fields]
    output_fields = list(generated_fields) + extra_fields
    human_fields = list(dict.fromkeys([*HUMAN_FIELDS, *extra_fields]))
    existing_by_id = {row.get("review_item_id", ""): row for row in existing_rows if row.get("review_item_id")}
    if len(existing_by_id) != len([row for row in existing_rows if row.get("review_item_id")]):
        raise ValueError(f"Duplicate review_item_id in {existing_path}")
    generated_ids = {row["review_item_id"] for row in generated_rows}

    preserved_rows = 0
    result: list[dict[str, str]] = []
    for generated in generated_rows:
        row = dict(generated)
        old = existing_by_id.get(row["review_item_id"])
        if old:
            changed_identity = [
                field for field in identity_fields
                if old.get(field) and old[field] != row[field]
            ]
            if changed_identity:
                raise ValueError(
                    f"Stable review ID collision {row['review_item_id']}: "
                    f"identity fields changed: {changed_identity}"
                )
            for field in human_fields:
                row[field] = old.get(field, "")
            if any(row.get(field, "") for field in human_fields):
                preserved_rows += 1
        else:
            for field in extra_fields:
                row[field] = ""
        result.append(row)

    populated_orphans = [
        review_id for review_id, row in existing_by_id.items()
        if review_id not in generated_ids and any(row.get(field, "") for field in human_fields)
    ]
    if populated_orphans:
        raise ValueError(f"Refusing to drop populated retired HR rows: {populated_orphans}")
    return result, output_fields, {
        "existing_rows": len(existing_rows),
        "preserved_nonblank_rows": preserved_rows,
        "extra_human_fields": len(extra_fields),
    }


def human_preservation_self_test(generated_rows: list[dict[str, str]]) -> None:
    """Use a temporary HR copy to prove human/final/status cells survive."""
    with TemporaryDirectory(prefix="schema_hr029_preservation_") as temp_dir:
        path = Path(temp_dir) / "HR029_test.csv"
        fields = [*HR_FIELDS, "final_status", "final_note"]
        existing = [dict(row) for row in generated_rows]
        for row in existing:
            row["final_status"] = ""
            row["final_note"] = ""
        existing[0].update({
            "decision": "TEST_HUMAN_DECISION",
            "human_reviewer": "TEST_REVIEWER",
            "review_date": "2099-12-31",
            "review_note": "TEST_REVIEW_NOTE",
            "final_status": "TEST_FINAL_STATUS",
            "final_note": "TEST_FINAL_NOTE",
            "review_question": "STALE_MACHINE_TEXT",
        })
        write_csv(path, existing, fields)
        merged, merged_fields, stats = preserve_human_fields(
            [dict(row) for row in generated_rows], path, HR_FIELDS,
            identity_fields=("domain", "object_id", "field_name"),
        )
        assert merged[0]["decision"] == "TEST_HUMAN_DECISION"
        assert merged[0]["human_reviewer"] == "TEST_REVIEWER"
        assert merged[0]["review_date"] == "2099-12-31"
        assert merged[0]["review_note"] == "TEST_REVIEW_NOTE"
        assert merged[0]["final_status"] == "TEST_FINAL_STATUS"
        assert merged[0]["final_note"] == "TEST_FINAL_NOTE"
        assert merged[0]["review_question"] == generated_rows[0]["review_question"]
        assert "final_status" in merged_fields and stats["preserved_nonblank_rows"] == 1


def normalize_svg_trailing_whitespace(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    normalized = "\n".join(line.rstrip() for line in text.splitlines()) + "\n"
    path.write_text(normalized, encoding="utf-8", newline="\n")


def dynamic_actor_coverage_self_test(actors: list[dict[str, str]]) -> None:
    """Prove a synthetic post-HR027 actor receives all three audit cells."""
    synthetic = dict(actors[0])
    synthetic["actor_id"] = "TEST_POST_HR027_ACTOR"
    synthetic["canonical_name"] = "TEST_POST_HR027_ACTOR"
    test_candidates: list[dict[str, str]] = []
    rows = actor_audit([*actors, synthetic], test_candidates)
    synthetic_rows = [row for row in rows if row["actor_id"] == synthetic["actor_id"]]
    assert len(rows) == (len(actors) + 1) * 3
    assert {row["field_name"] for row in synthetic_rows} == {
        "actor_class", "legal_status_guess", "origin_type",
    }


def normalized_name(value: str) -> str:
    value = unicodedata.normalize("NFKC", value).casefold()
    return "".join(char for char in value if char.isalnum())


def record_key(row: dict[str, str]) -> str:
    for field in (
        "edge_id", "relation_observation_id", "record_id", "observation_id",
        "event_id", "role_id", "stage_id",
    ):
        if row.get(field):
            return row[field]
    return ""


def add_candidate(
    candidates: list[dict[str, str]], *, domain: str, object_id: str,
    object_name: str, field_name: str, current_value: str,
    proposed_value: str, disposition: str, affected: int,
    source_tables: str, reason: str, risk: str, requires_human: bool,
    limit: str, external_review_task: str = "",
) -> dict[str, str]:
    machine_status = "needs_human_review" if requires_human else "freeze_candidate"
    hr_item_id = ""
    if external_review_task:
        if not requires_human:
            raise ValueError("An external review task requires requires_human=True")
        machine_status = f"defer_to_{external_review_task.replace('-', '')}"
        hr_item_id = external_review_task
    row = {
        "candidate_id": f"SF{len(candidates) + 1:04d}",
        "domain": domain,
        "object_id": object_id,
        "object_name": object_name,
        "field_name": field_name,
        "current_value": current_value,
        "proposed_value": proposed_value,
        "candidate_disposition": disposition,
        "affected_row_count": str(affected),
        "source_tables": source_tables,
        "reason": reason,
        "risk_if_wrong": risk,
        "requires_human_review": "yes" if requires_human else "no",
        "hr_item_id": hr_item_id,
        "machine_status": machine_status,
        "interpretation_limit": limit,
    }
    candidates.append(row)
    return row


def actor_audit(
    actors: list[dict[str, str]], candidates: list[dict[str, str]],
) -> list[dict[str, str]]:
    observed = {
        "actor_class": {row["actor_class"] for row in actors},
        "legal_status_guess": {row["legal_status_guess"] for row in actors},
        "origin_type": {row["origin_type"] for row in actors},
    }
    assert observed["actor_class"] <= set(ACTOR_CLASS_MAP), observed["actor_class"] - set(ACTOR_CLASS_MAP)
    assert observed["legal_status_guess"] <= set(LEGAL_STATUS_MAP), observed["legal_status_guess"] - set(LEGAL_STATUS_MAP)
    assert observed["origin_type"] <= set(ORIGIN_MAP), observed["origin_type"] - set(ORIGIN_MAP)

    result = []
    configs = (
        ("actor_class", ACTOR_CLASS_MAP),
        ("legal_status_guess", LEGAL_STATUS_MAP),
        ("origin_type", ORIGIN_MAP),
    )
    for actor in sorted(actors, key=lambda row: row["actor_id"]):
        for field, mapping in configs:
            current = actor[field]
            proposed, disposition, human = mapping[current]
            if field == "actor_class" and actor["actor_id"] in IDENTITY_ONLY_CLASS_ACTORS:
                human = True
                disposition = "human_assignment_review"
            if field == "actor_class" and current == "womens_or_community_organization":
                human = True
                disposition = "human_assignment_review"
            reason = {
                "actor_class": "Freeze the analytical actor-class vocabulary while preserving actor-specific classification review.",
                "legal_status_guess": "Move legal-form surface strings into controlled codes; unresolved codes do not assert法人格.",
                "origin_type": "All seven observed origin codes already form a closed controlled set.",
            }[field]
            risk = {
                "actor_class": "A wrong class changes ecology counts and figure composition.",
                "legal_status_guess": "A wrong normalization could turn a guess into a false legal-status claim.",
                "origin_type": "A wrong origin changes local/mainland/international layer comparisons.",
            }[field]
            limit = (
                "This is a schema/assignment candidate only; it does not approve actor scope, edges or substantive interpretation."
            )
            candidate = add_candidate(
                candidates, domain="actor_field", object_id=actor["actor_id"],
                object_name=actor["canonical_name"], field_name=field,
                current_value=current, proposed_value=proposed,
                disposition=disposition, affected=1,
                source_tables=ACTOR_FILE.name, reason=reason, risk=risk,
                requires_human=human, limit=limit,
            )
            result.append({
                "candidate_id": candidate["candidate_id"],
                "actor_id": actor["actor_id"],
                "canonical_name": actor["canonical_name"],
                "field_name": field,
                "current_value": current,
                "proposed_controlled_value": proposed,
                "candidate_disposition": disposition,
                "requires_human_review": "yes" if human else "no",
                "registry_review_status": actor["review_status"],
                "evidence_level": actor["evidence_level"],
                "interpretation_limit": limit,
            })
    return result


def aggregate_actor_mappings(actor_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    grouped: dict[tuple[str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in actor_rows:
        grouped[(row["field_name"], row["current_value"], row["proposed_controlled_value"])].append(row)
    result = []
    for (field, current, proposed), rows in sorted(grouped.items()):
        human_ids = [row["actor_id"] for row in rows if row["requires_human_review"] == "yes"]
        dispositions = sorted({row["candidate_disposition"] for row in rows})
        result.append({
            "field_name": field,
            "current_value": current,
            "proposed_controlled_value": proposed,
            "affected_actor_count": str(len(rows)),
            "affected_actor_ids": ";".join(row["actor_id"] for row in rows),
            "mapping_disposition": ";".join(dispositions),
            "human_assignment_count": str(len(human_ids)),
            "human_assignment_actor_ids": ";".join(human_ids),
            "interpretation_limit": "A vocabulary mapping does not approve every actor's assignment when human_assignment_count is nonzero.",
        })
    return result


def alias_audit(
    actors: list[dict[str, str]], aliases: list[dict[str, str]],
    candidates: list[dict[str, str]],
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    actor_names = {row["actor_id"]: row["canonical_name"] for row in actors}
    canonical_by_norm: dict[str, list[str]] = defaultdict(list)
    for actor in actors:
        canonical_by_norm[normalized_name(actor["canonical_name"])].append(actor["actor_id"])
    alias_by_norm: dict[str, list[dict[str, str]]] = defaultdict(list)
    for alias in aliases:
        alias_by_norm[normalized_name(alias["alias"])].append(alias)

    result = []
    for alias in aliases:
        proposed, disposition, human = ALIAS_TYPE_MAP[alias["alias_type"]]
        norm_peers = alias_by_norm[normalized_name(alias["alias"])]
        peer_actor_ids = sorted({row["actor_id"] for row in norm_peers})
        if len(peer_actor_ids) > 1:
            collision = "cross_actor_normalized_collision"
            human = True
            disposition = "human_review"
        elif len(norm_peers) > 1:
            collision = "same_actor_source_sensitive_normalized_duplicate"
        else:
            collision = "none"
        canonical_hits = canonical_by_norm.get(normalized_name(alias["alias"]), [])
        cross_canonical_hits = sorted(actor_id for actor_id in canonical_hits if actor_id != alias["actor_id"])
        if cross_canonical_hits:
            human = True
            disposition = "human_review"
        semantics = (
            "nonidentity_lineage_label"
            if proposed in {"predecessor_name_nonidentity", "case_round_label_nonidentity"}
            else "unresolved_identity_candidate"
            if proposed == "unresolved_canonical_variant"
            else "identity_lookup_alias"
        )
        reason = "Normalize alias-type semantics while retaining every source-attested surface form."
        if semantics == "nonidentity_lineage_label":
            reason = "Store lineage/case-round labels for lookup without asserting entity identity or identical membership."
        candidate = add_candidate(
            candidates, domain="alias", object_id=alias["actor_id"],
            object_name=alias["alias"], field_name="alias_type",
            current_value=alias["alias_type"], proposed_value=proposed,
            disposition=disposition, affected=1, source_tables=ALIAS_FILE.name,
            reason=reason,
            risk="Name similarity can collapse distinct organizations, rounds or predecessor relationships.",
            requires_human=human,
            limit="Never merge entities from normalized-name similarity; lineage labels are explicitly nonidentity.",
        )
        result.append({
            "candidate_id": candidate["candidate_id"],
            "actor_id": alias["actor_id"],
            "canonical_name": actor_names.get(alias["actor_id"], ""),
            "alias": alias["alias"],
            "current_alias_type": alias["alias_type"],
            "proposed_alias_type": proposed,
            "identity_semantics": semantics,
            "normalized_alias": normalized_name(alias["alias"]),
            "collision_status": collision,
            "cross_actor_canonical_hits": ";".join(cross_canonical_hits),
            "source_ref": alias["source_ref"],
            "requires_human_review": "yes" if human else "no",
            "hr_item_id": "",
            "notes": alias["notes"],
        })

    boundaries = [
        {
            "boundary_id": "AB001", "object_ids": "A105;A107",
            "labels": "日本YWCA;沖縄YWCA", "boundary_type": "national_local_brand",
            "current_state": "two registry actors plus organizational affiliation",
            "proposed_rule": "distinct_entities_with_affiliation_not_alias",
            "human_anchor": "HR-011;F043",
            "reason": "Parent/national and local/regional YWCA are distinct actors; actions do not automatically transfer.",
        },
        {
            "boundary_id": "AB002", "object_ids": "A111;retired_A094",
            "labels": "女団協;沖女連", "boundary_type": "retired_actor_alias_guard",
            "current_state": "A111 has 女団協; A094 is removed",
            "proposed_rule": "do_not_transfer_retired_alias_or_reinsert_actor",
            "human_anchor": "HR-010;HR-013",
            "reason": "The HR-013 decision explicitly distinguishes A111 from the removed A094 and A049.",
        },
    ]
    for boundary in boundaries:
        candidate = add_candidate(
            candidates, domain="alias_boundary", object_id=boundary["object_ids"],
            object_name=boundary["labels"], field_name="entity_boundary",
            current_value=boundary["current_state"], proposed_value=boundary["proposed_rule"],
            disposition="freeze_from_human_anchor", affected=2,
            source_tables=f"{ACTOR_FILE.name};{ALIAS_FILE.name}",
            reason=boundary["reason"],
            risk="A false alias would merge distinct national/local or retired/current organizations.",
            requires_human=False,
            limit="This preserves an existing human decision; it creates no new relation or identity claim.",
        )
        boundary["candidate_id"] = candidate["candidate_id"]
        boundary["requires_human_review"] = "no"
        boundary["hr_item_id"] = ""
    return result, boundaries


def place_audit(
    places: list[dict[str, str]], actor_place_edges: list[dict[str, str]],
    candidates: list[dict[str, str]],
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    assert {row["place_id"] for row in places} == set(PLACE_PLAN)
    usage = Counter(row["place_id"] for row in actor_place_edges)
    by_id = {row["place_id"]: row for row in places}
    result = []
    for place in sorted(places, key=lambda row: row["place_id"]):
        proposed_name, proposed_type, parent, aliases, human, reason = PLACE_PLAN[place["place_id"]]
        current = f"name={place['place_name']}|type={place['place_type']}|parent=absent|aliases=absent"
        proposed = f"name={proposed_name}|type={proposed_type}|parent={parent or 'ROOT'}|aliases={aliases}"
        disposition = "human_review" if human else "mechanical_hierarchy_alias_enrichment"
        candidate = add_candidate(
            candidates, domain="place_semantics", object_id=place["place_id"],
            object_name=place["place_name"], field_name="place_name_type_parent_aliases",
            current_value=current, proposed_value=proposed, disposition=disposition,
            affected=usage[place["place_id"]], source_tables=f"{PLACE_FILE.name};{ACTOR_PLACE_FILE.name}",
            reason=reason,
            risk="A wrong spatial level can collapse locality, municipality and military installation layers.",
            requires_human=human,
            limit="Aliases support lookup only; island, municipality, locality and installation are not merged by name similarity.",
        )
        result.append({
            "candidate_id": candidate["candidate_id"],
            "place_id": place["place_id"], "current_place_name": place["place_name"],
            "proposed_canonical_name": proposed_name,
            "current_place_type": place["place_type"], "proposed_place_type": proposed_type,
            "current_region_label": place["region"], "proposed_parent_place_id": parent,
            "proposed_aliases": aliases, "actor_place_edge_count": str(usage[place["place_id"]]),
            "requires_human_review": "yes" if human else "no", "hr_item_id": "",
            "reason": reason,
            "interpretation_limit": "Hierarchy is an analytical containment proposal, not proof of jurisdiction or identical spatial extent.",
        })

    conflicts = []
    for edge in actor_place_edges:
        registry = by_id.get(edge["place_id"])
        if registry and edge["place_name"] == registry["place_name"]:
            continue
        proposed = "defer_to_HR025"
        human = True
        disposition = "defer_to_HR025"
        current = f"place_id={edge['place_id']}|place_name={edge['place_name']}"
        candidate = add_candidate(
            candidates, domain="place_edge_crosskey", object_id=edge["edge_id"],
            object_name=edge["actor_id"], field_name="place_id_place_name",
            current_value=current, proposed_value=proposed, disposition=disposition,
            affected=1,
            source_tables=f"{ACTOR_PLACE_FILE.name};outputs/R03_spatial_dossier_v1/HR025_actor_place_semantics_review_v0.csv",
            reason="HR-025 is the authoritative actor-place semantic gate; this schema package must not adjudicate the cross-key conflict.",
            risk="A cross-key mismatch assigns an actor to the wrong military installation.",
            requires_human=human,
            limit="Do not silently choose P007 or any other place ID; retain the conflict until HR-025 decides the source-backed spatial meaning.",
            external_review_task="HR-025",
        )
        conflicts.append({
            "candidate_id": candidate["candidate_id"], "edge_id": edge["edge_id"],
            "actor_id": edge["actor_id"], "current_place_id": edge["place_id"],
            "current_place_name": edge["place_name"],
            "registry_name_for_current_id": registry["place_name"] if registry else "missing_id",
            "proposed_resolution": proposed,
            "requires_human_review": "yes" if human else "no", "hr_item_id": "",
            "source_ref": edge["source_ref"], "notes": edge["notes"],
        })
    return result, conflicts


def venue_audit(
    venues: list[dict[str, str]], aev_rows: list[dict[str, str]],
    pathway_rows: list[dict[str, str]], candidates: list[dict[str, str]],
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    venue_ids = {row["venue_id"] for row in venues}
    usage_by_table: dict[str, Counter[str]] = {
        AEV_FILE.name: Counter(row["venue_id"] for row in aev_rows),
        PATHWAY_FILE.name: Counter(row["venue_id"] for row in pathway_rows),
    }
    result = []
    for venue in sorted(venues, key=lambda row: row["venue_id"]):
        total = sum(counter[venue["venue_id"]] for counter in usage_by_table.values())
        disposition = "freeze_as_is" if total else "defined_zero_use"
        candidate = add_candidate(
            candidates, domain="venue_taxonomy", object_id=venue["venue_id"],
            object_name=venue["venue_label"], field_name="venue_label_group",
            current_value=f"label={venue['venue_label']}|group={venue['venue_group']}",
            proposed_value=f"label={venue['venue_label']}|group={venue['venue_group']}",
            disposition=disposition, affected=total, source_tables=VENUE_FILE.name,
            reason="The 16-row taxonomy has unique IDs/labels; zero-use rows remain legitimate reserved categories.",
            risk="Removing a zero-use category can erase a planned procedural or international venue layer.",
            requires_human=False,
            limit="Taxonomy readiness does not approve any actor-event role or relation.",
        )
        result.append({
            "candidate_id": candidate["candidate_id"], "venue_id": venue["venue_id"],
            "venue_label": venue["venue_label"], "venue_group": venue["venue_group"],
            "usage_09_aev": str(usage_by_table[AEV_FILE.name][venue["venue_id"]]),
            "usage_26_pathways": str(usage_by_table[PATHWAY_FILE.name][venue["venue_id"]]),
            "total_reference_count": str(total),
            "audit_status": "observed" if total else "defined_zero_use",
            "requires_human_review": "no", "hr_item_id": "",
            "notes_audit": "V015 is now used once; its legacy 'future expansion' note is stale but its label/group remain valid." if venue["venue_id"] == "V015" else "",
        })

    conflicts = []
    for row in pathway_rows:
        if row["venue_id"] in venue_ids:
            continue
        assert row["observation_id"] in ORPHAN_VENUE_PLAN, row["observation_id"]
        proposed, human, reason = ORPHAN_VENUE_PLAN[row["observation_id"]]
        disposition = "human_review" if human else "mechanical_fk_resolution"
        candidate = add_candidate(
            candidates, domain="venue_reference", object_id=row["observation_id"],
            object_name=row["venue_label"], field_name="venue_id",
            current_value=row["venue_id"], proposed_value=proposed,
            disposition=disposition, affected=1, source_tables=PATHWAY_FILE.name,
            reason=reason,
            risk="Blind replacement would treat membership, service sites and public-diplomacy opportunities as one venue.",
            requires_human=human,
            limit="Resolving a venue foreign key does not turn a grant opportunity into an award or a membership into an event.",
        )
        conflicts.append({
            "candidate_id": candidate["candidate_id"],
            "observation_id": row["observation_id"], "current_venue_id": row["venue_id"],
            "current_venue_label": row["venue_label"], "role": row["role"],
            "entry_mode": row["entry_mode"], "proposed_venue_resolution": proposed,
            "requires_human_review": "yes" if human else "no", "hr_item_id": "",
            "reason": reason, "interpretation_limit": row["interpretation_limit"],
        })
    return result, conflicts


def collect_value_inventory(column: str) -> tuple[dict[str, Counter[str]], dict[str, list[str]]]:
    counts: dict[str, Counter[str]] = defaultdict(Counter)
    examples: dict[str, list[str]] = defaultdict(list)
    for path in sorted(DATA.glob("*.csv")):
        if path == MAIN_FILE:
            continue
        rows = read_csv(path)
        if not rows or column not in rows[0]:
            continue
        for row in rows:
            value = row[column]
            if not value:
                continue
            counts[value][path.name] += 1
            key = record_key(row)
            if key and len(examples[value]) < 6:
                examples[value].append(f"{path.name}:{key}")
    return counts, examples


def relation_action_audit(candidates: list[dict[str, str]]) -> list[dict[str, str]]:
    result = []
    for field, mapping in (("relation_type", RELATION_TYPE_MAP), ("action_type", ACTION_TYPE_MAP)):
        counts, examples = collect_value_inventory(field)
        assert set(counts) == set(mapping), (field, set(counts) - set(mapping), set(mapping) - set(counts))
        for current in sorted(counts):
            proposed, disposition, human = mapping[current]
            source_tables = ";".join(f"{name}:{count}" for name, count in sorted(counts[current].items()))
            total = sum(counts[current].values())
            if field == "relation_type":
                limit = "Relation vocabulary normalization does not approve candidate edges, funding, alliance or causal interpretation."
                risk = "A bad relation code can turn a lead, aggregate observation or opportunity into a confirmed tie."
            else:
                limit = "Action vocabulary normalization does not turn co-participation into alliance or an analytical seed into fact."
                risk = "A bad action code can conflate endorsement, request, co-signing, litigation and analytical pathways."
            candidate = add_candidate(
                candidates, domain=field, object_id=current, object_name=current,
                field_name=field, current_value=current, proposed_value=proposed,
                disposition=disposition, affected=total, source_tables=source_tables,
                reason="Map every observed value to a closed controlled vocabulary.", risk=risk,
                requires_human=human, limit=limit,
            )
            result.append({
                "candidate_id": candidate["candidate_id"], "field_name": field,
                "current_value": current, "proposed_controlled_value": proposed,
                "candidate_disposition": disposition, "affected_row_count": str(total),
                "source_tables_and_counts": source_tables,
                "example_record_keys": ";".join(examples[current]),
                "requires_human_review": "yes" if human else "no", "hr_item_id": "",
                "interpretation_limit": limit,
            })
    return result


def assign_hr(
    candidates: list[dict[str, str]], existing_path: Path = HR_FILE,
) -> list[dict[str, str]]:
    _, existing_rows = read_csv_with_fields(existing_path)
    existing_by_semantic_key: dict[tuple[str, str, str], str] = {}
    existing_ids = {row["review_item_id"] for row in existing_rows if row.get("review_item_id")}
    for row in existing_rows:
        key = (row.get("domain", ""), row.get("object_id", ""), row.get("field_name", ""))
        if not all(key):
            continue
        if key in existing_by_semantic_key and existing_by_semantic_key[key] != row["review_item_id"]:
            raise ValueError(f"Duplicate semantic HR-029 key: {key}")
        existing_by_semantic_key[key] = row["review_item_id"]
    next_number = max(
        [int(match.group(1)) for review_id in existing_ids if (match := re.fullmatch(r"HR029-(\d+)", review_id))],
        default=0,
    ) + 1
    result = []
    for candidate in candidates:
        if candidate["requires_human_review"] != "yes":
            continue
        if candidate["machine_status"].startswith("defer_to_"):
            continue
        semantic_key = (candidate["domain"], candidate["object_id"], candidate["field_name"])
        hr_id = existing_by_semantic_key.get(semantic_key, "")
        if not hr_id:
            while f"HR029-{next_number:03d}" in existing_ids:
                next_number += 1
            hr_id = f"HR029-{next_number:03d}"
            existing_ids.add(hr_id)
            next_number += 1
        candidate["hr_item_id"] = hr_id
        result.append({
            "review_item_id": hr_id, "task_id": "HR-029",
            "candidate_id": candidate["candidate_id"], "domain": candidate["domain"],
            "object_id": candidate["object_id"], "object_name": candidate["object_name"],
            "field_name": candidate["field_name"], "current_value": candidate["current_value"],
            "proposed_value": candidate["proposed_value"],
            "source_context": candidate["source_tables"],
            "review_question": f"Accept, revise or reject the proposed {candidate['field_name']} freeze for this object?",
            "accept_effect": "Allows a later controlled central merge; does not itself modify central data.",
            "required_boundary": candidate["interpretation_limit"],
            "decision": "", "human_reviewer": "", "review_date": "", "review_note": "",
        })
    return result


def backfill_hr_ids(rows: list[dict[str, str]], candidates: list[dict[str, str]]) -> None:
    by_candidate = {row["candidate_id"]: row["hr_item_id"] for row in candidates}
    for row in rows:
        if "candidate_id" in row and "hr_item_id" in row:
            row["hr_item_id"] = by_candidate.get(row["candidate_id"], "")


def make_lint_rules(
    actors: list[dict[str, str]], aliases: list[dict[str, str]],
    places: list[dict[str, str]], place_conflicts: list[dict[str, str]],
    venues: list[dict[str, str]], venue_conflicts: list[dict[str, str]],
    relation_action_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    actor_ids = [row["actor_id"] for row in actors]
    canonical_norms: dict[str, list[str]] = defaultdict(list)
    for row in actors:
        canonical_norms[normalized_name(row["canonical_name"])].append(row["actor_id"])
    alias_norms: dict[str, list[str]] = defaultdict(list)
    for row in aliases:
        alias_norms[normalized_name(row["alias"])].append(row["actor_id"])
    cross_actor_alias = {key: sorted(set(ids)) for key, ids in alias_norms.items() if len(set(ids)) > 1}
    same_actor_alias = {key: ids for key, ids in alias_norms.items() if len(ids) > 1 and len(set(ids)) == 1}
    venue_ids = {row["venue_id"] for row in venues}

    relation_unmapped = [row for row in relation_action_rows if row["field_name"] == "relation_type" and not row["proposed_controlled_value"]]
    action_unmapped = [row for row in relation_action_rows if row["field_name"] == "action_type" and not row["proposed_controlled_value"]]
    grant_violations = []
    for path in (DATA / "15_funding_or_support_edges_sample_v0.csv", DATA / "21_admin_collaboration_relations_v0.csv"):
        for row in read_csv(path):
            if row.get("relation_type") == "grant_opportunity":
                confidence = row.get("funding_relation_confidence", "")
                semantics = row.get("financial_semantics", "")
                if confidence in {"confirmed_grant", "confirmed_sponsorship"} or "awarded" in semantics:
                    grant_violations.append(f"{path.name}:{record_key(row)}")

    def rule(rule_id: str, domain: str, severity: str, trigger: str, expected: str,
             count: int, examples: str, route: str, limit: str) -> dict[str, str]:
        return {
            "rule_id": rule_id, "domain": domain, "severity": severity,
            "trigger": trigger, "expected_or_fix": expected,
            "detected_count": str(count), "detected_examples": examples,
            "automatic_or_human": route, "interpretation_limit": limit,
        }

    invalid_actor_ids = [value for value in actor_ids if not re.fullmatch(r"[AX]\d{3}", value)]
    duplicate_actor_ids = [value for value, count in Counter(actor_ids).items() if count > 1]
    actor_by_id = {row["actor_id"]: row for row in actors}
    canonical_collisions = {}
    for key, ids in canonical_norms.items():
        if len(ids) <= 1:
            continue
        roots = [actor_id for actor_id in ids if not actor_by_id[actor_id].get("merged_duplicate_of")]
        sanctioned = (
            len(roots) == 1
            and all(
                actor_id == roots[0]
                or actor_by_id[actor_id].get("merged_duplicate_of") == roots[0]
                for actor_id in ids
            )
        )
        if not sanctioned:
            canonical_collisions[key] = ids
    invalid_place_ids = [row["place_id"] for row in places if not re.fullmatch(r"P\d{3}", row["place_id"])]
    duplicate_place_ids = [value for value, count in Counter(row["place_id"] for row in places).items() if count > 1]
    orphan_examples = ";".join(row["observation_id"] for row in venue_conflicts)
    return [
        rule("L001", "actor", "error", "actor_id format", "Unique [AX]### identifier", len(invalid_actor_ids), ";".join(invalid_actor_ids), "automatic", "ID lint says nothing about actor scope."),
        rule("L002", "actor", "error", "duplicate actor_id", "No duplicate IDs", len(duplicate_actor_ids), ";".join(duplicate_actor_ids), "automatic", "Never resolve duplicate IDs by name similarity."),
        rule("L003", "actor", "error", "actor_class outside mapping", "Value must exist in frozen actor_class vocabulary", 0, "", "automatic", "Vocabulary membership does not approve actor assignment."),
        rule("L004", "actor", "error", "legal_status_guess outside mapping", "Use a controlled status or explicit unresolved code", 0, "", "automatic", "Unresolved is preferable to inventing法人格."),
        rule("L005", "actor", "error", "origin_type outside mapping", "Use one of seven origin codes", 0, "", "automatic", "Origin does not imply political stance."),
        rule("L006", "actor_name", "error", "normalized canonical-name collision", "Human entity decision; never auto-merge", len(canonical_collisions), ";".join("/".join(ids) for ids in canonical_collisions.values()), "human", "Similarity is not identity."),
        rule("L007", "alias", "error", "normalized alias assigned to multiple actors", "Human entity-boundary review", len(cross_actor_alias), ";".join("/".join(ids) for ids in cross_actor_alias.values()), "human", "Do not auto-merge aliases or actors."),
        rule("L008", "alias", "info", "same-actor normalized duplicate", "Allow only when source-sensitive spelling/type is documented", len(same_actor_alias), ";".join(same_actor_alias), "human_if_undocumented", "Punctuation variants can coexist for source matching."),
        rule("L009", "alias", "error", "round/predecessor label used as identity alias", "Use nonidentity lineage alias types", 0, "", "automatic", "Round membership and predecessor identity are not transferred."),
        rule("L010", "alias", "error", "national/local brand treated as one actor", "Keep A105/A107 distinct; relation is affiliation", 0, "A105/A107 guarded", "automatic_guard", "Parent actions do not transfer to local chapter."),
        rule("L011", "alias", "error", "retired A094 or 沖女連 reinserted via A111 alias", "Keep A111 distinct; new human decision required for any re-entry", 0, "A111/retired A094 guarded", "automatic_guard", "Do not number-fill the registry."),
        rule("L012", "place", "error", "invalid or duplicate place_id", "Unique P### identifier", len(invalid_place_ids) + len(duplicate_place_ids), ";".join(invalid_place_ids + duplicate_place_ids), "automatic", "Place IDs do not establish jurisdiction."),
        rule("L013", "actor_place", "error", "place_id/place_name cross-key mismatch", "All keys must match the place registry; route future mismatches to a dedicated human spatial gate", len(place_conflicts), ";".join(row["edge_id"] for row in place_conflicts), "human_gate_if_detected", "Never silently repair a spatial key from a similar label."),
        rule("L014", "place", "warning", "island/municipality/locality/installation level ambiguous", "Human hierarchy and alias decision", 5, "P004;P005;P011;P012;P013", "human", "Never merge spatial levels by similar names."),
        rule("L015", "venue", "error", "venue_id absent from 16-row taxonomy", "Resolve row-specific FK or explicitly allow no venue", len(venue_conflicts), orphan_examples, "mixed", "Membership, service sites and program channels need different treatment."),
        rule("L016", "venue", "warning", "defined venue has zero current references", "Keep as reserved category unless human removes it", sum(1 for row in venues if row["venue_id"] not in {r["venue_id"] for r in read_csv(AEV_FILE)} | {r["venue_id"] for r in read_csv(PATHWAY_FILE)}), "", "automatic", "Zero use is not evidence that the venue type is invalid."),
        rule("L017", "relation_type", "error", "unmapped relation type", "Every value maps to a controlled relation or deprecated nonrelation", len(relation_unmapped), "", "automatic", "Mapping does not approve relation facts."),
        rule("L018", "relation_type", "warning", "deprecated duplicate sentinel stored as relation_type", "Exclude F008 from relation analysis", 1, "F008", "automatic", "A rejected duplicate is not an edge type."),
        rule("L019", "funding", "error", "grant_opportunity treated as award", "Opportunity remains non-award/no-recipient", len(grant_violations), ";".join(grant_violations), "automatic", "NOFO does not prove funding or recipient."),
        rule("L020", "action_type", "error", "unmapped action type", "Every value maps to factual or explicitly analytical vocabulary", len(action_unmapped), "", "automatic", "Action mapping does not approve event roles."),
        rule("L021", "action_type", "warning", "pathway_role mixed with factual actions", "Map to analytical_pathway_role and keep analytical_seed status", 4, "AEV0061-AEV0064", "automatic", "Analytical sequence is not a factual relation or causal pathway."),
        rule("L022", "coaction", "error", "co-signing/request participation promoted to stable alliance", "Retain event-level participation only", 0, "", "human_interpretation", "Shared event participation is not stable alliance evidence."),
    ]


def make_impacts(
    actors: list[dict[str, str]], actor_rows: list[dict[str, str]],
    actor_mappings: list[dict[str, str]], aliases: list[dict[str, str]],
    alias_rows: list[dict[str, str]], places: list[dict[str, str]],
    place_conflicts: list[dict[str, str]], venues: list[dict[str, str]],
    venue_conflicts: list[dict[str, str]], relation_action_rows: list[dict[str, str]],
    candidates: list[dict[str, str]], hr_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    def metric(group: str, name: str, count: int, current: str = "", proposed: str = "", note: str = "") -> dict[str, str]:
        return {
            "metric_group": group, "metric": name, "count": str(count),
            "current_distinct_values": current, "proposed_distinct_values": proposed,
            "note": note,
        }

    mapping_distinct = {}
    for field in ("actor_class", "legal_status_guess", "origin_type"):
        rows = [row for row in actor_mappings if row["field_name"] == field]
        mapping_distinct[field] = (len({row["current_value"] for row in rows}), len({row["proposed_controlled_value"] for row in rows}))
    relation_rows = [row for row in relation_action_rows if row["field_name"] == "relation_type"]
    action_rows = [row for row in relation_action_rows if row["field_name"] == "action_type"]
    human_fields = set(HUMAN_FIELDS) | {
        field for row in hr_rows for field in row if field not in HR_FIELDS
    }
    filled_hr_rows = sum(any(row.get(field, "") for field in human_fields) for row in hr_rows)
    return [
        metric("actor", "registry_actors_audited", len(actors), note="All actor_class/legal_status_guess/origin_type cells covered."),
        metric("actor", "actor_field_cells_audited", len(actor_rows)),
        metric("actor", "actor_class_vocabulary", len(actors), str(mapping_distinct["actor_class"][0]), str(mapping_distinct["actor_class"][1])),
        metric("actor", "legal_status_vocabulary", len(actors), str(mapping_distinct["legal_status_guess"][0]), str(mapping_distinct["legal_status_guess"][1]), "Uncertain forms map to explicit unresolved codes."),
        metric("actor", "origin_vocabulary", len(actors), str(mapping_distinct["origin_type"][0]), str(mapping_distinct["origin_type"][1])),
        metric("alias", "alias_rows_audited", len(aliases), str(len({row['alias_type'] for row in aliases})), str(len({row['proposed_alias_type'] for row in alias_rows}))),
        metric("alias", "cross_actor_normalized_alias_collisions", sum(row["collision_status"] == "cross_actor_normalized_collision" for row in alias_rows), note="Zero; similarity guard still remains mandatory."),
        metric(
            "alias", "same_actor_source_sensitive_normalized_duplicates",
            len({
                row["normalized_alias"] for row in alias_rows
                if row["collision_status"] == "same_actor_source_sensitive_normalized_duplicate"
            }),
            note="Counted as normalized collision groups, not alias rows.",
        ),
        metric("place", "place_nodes_audited", len(places), str(len({row['place_type'] for row in places})), str(len({PLACE_PLAN[row['place_id']][1] for row in places}))),
        metric("place", "actor_place_crosskey_mismatches", len(place_conflicts), note="Zero after HR-025 fixed AP123 to P007 Camp Foster; future mismatches require a new spatial gate."),
        metric("venue", "venue_taxonomy_rows", len(venues), str(len({row['venue_group'] for row in venues})), str(len({row['venue_group'] for row in venues}))),
        metric(
            "venue", "orphan_placeholder_references", len(venue_conflicts),
            note=f"All are R10_VENUE; {sum(row['requires_human_review'] == 'yes' for row in venue_conflicts)} need HR-029 and the remainder have bounded mechanical candidates.",
        ),
        metric("relation", "relation_rows_inventoried", sum(int(row["affected_row_count"]) for row in relation_rows), str(len(relation_rows)), str(len({row['proposed_controlled_value'] for row in relation_rows}))),
        metric("action", "action_rows_inventoried", sum(int(row["affected_row_count"]) for row in action_rows), str(len(action_rows)), str(len({row['proposed_controlled_value'] for row in action_rows}))),
        metric("package", "unified_freeze_candidate_rows", len(candidates)),
        metric("package", "HR029_review_items", len(hr_rows), note="Stable IDs; human/final/status fields are preserved on regeneration."),
        metric("package", "HR029_filled_review_items", filled_hr_rows, note="Rows with at least one human-owned value."),
    ]


def setup_plotting() -> None:
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Microsoft YaHei", "Noto Sans CJK SC", "Noto Sans CJK JP", "DejaVu Sans"],
        "axes.unicode_minus": False,
        "figure.facecolor": "#F5F1E8", "axes.facecolor": "#F5F1E8",
        "savefig.facecolor": "#F5F1E8", "svg.hashsalt": "schema-alias-freeze-v1",
    })


def render_readiness(candidates: list[dict[str, str]]) -> None:
    setup_plotting()
    domain_groups = [
        ("actor_field", "Actor字段"),
        ("alias", "Alias条目"),
        ("alias_boundary", "Alias边界"),
        ("place_semantics", "Place层级"),
        ("place_edge_crosskey", "Place交叉键"),
        ("venue_taxonomy", "Venue taxonomy"),
        ("venue_reference", "Venue引用"),
        ("relation_type", "Relation值"),
        ("action_type", "Action值"),
    ]
    values = []
    for domain, label in domain_groups:
        rows = [row for row in candidates if row["domain"] == domain]
        human = sum(row["requires_human_review"] == "yes" for row in rows)
        changed = sum(
            row["requires_human_review"] == "no" and row["current_value"] != row["proposed_value"]
            for row in rows
        )
        frozen = len(rows) - human - changed
        values.append((label, frozen, changed, human))
    fig, ax = plt.subplots(figsize=(12, 7.6))
    y = list(range(len(values)))
    frozen = [row[1] for row in values]
    changed = [row[2] for row in values]
    human = [row[3] for row in values]
    ax.barh(y, frozen, color="#2A6F6B", label="可保持当前值")
    ax.barh(y, changed, left=frozen, color="#D69E2E", label="可机械规范/补层级")
    left_human = [a + b for a, b in zip(frozen, changed)]
    ax.barh(y, human, left=left_human, color="#C45850", label="人工决定（HR-025/029）")
    for idx, (label, a, b, c) in enumerate(values):
        total = a + b + c
        ax.text(total + max(0.5, total * 0.01), idx, str(total), va="center", fontsize=10)
    ax.set_yticks(y, [row[0] for row in values])
    ax.invert_yaxis()
    ax.set_xlabel("冻结候选行数（非实体数）")
    ax.set_title("一期 schema / alias 冻结准备度", loc="left", fontsize=18, fontweight="bold", pad=16)
    ax.text(0, 1.01, "人工项是实体、空间或关系语义决策；机械规范不批准研究事实。", transform=ax.transAxes, fontsize=10, color="#5F625F")
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.grid(axis="x", color="#D4CEC0", linewidth=0.8, alpha=0.8)
    ax.set_axisbelow(True)
    ax.legend(ncol=3, frameon=False, loc="lower right")
    fig.tight_layout()
    fig.savefig(FIG_READINESS_PNG, dpi=180, bbox_inches="tight", metadata={"Software": "NW2-E schema freeze builder"})
    fig.savefig(FIG_READINESS_SVG, bbox_inches="tight", metadata={"Date": "2026-07-20"})
    normalize_svg_trailing_whitespace(FIG_READINESS_SVG)
    plt.close(fig)


def render_vocabulary(
    actor_mappings: list[dict[str, str]], alias_rows: list[dict[str, str]],
    places: list[dict[str, str]], venues: list[dict[str, str]],
    relation_action_rows: list[dict[str, str]],
) -> None:
    setup_plotting()
    rows = []
    for field, label in (
        ("actor_class", "actor_class"), ("legal_status_guess", "legal_status"),
        ("origin_type", "origin_type"),
    ):
        subset = [row for row in actor_mappings if row["field_name"] == field]
        rows.append((label, len({row["current_value"] for row in subset}), len({row["proposed_controlled_value"] for row in subset})))
    rows.append(("alias_type", len(ALIAS_TYPE_MAP), len({value[0] for value in ALIAS_TYPE_MAP.values()})))
    rows.append(("place_type", len({row["place_type"] for row in places}), len({PLACE_PLAN[row["place_id"]][1] for row in places})))
    rows.append(("venue_group", len({row["venue_group"] for row in venues}), len({row["venue_group"] for row in venues})))
    for field, label in (("relation_type", "relation_type"), ("action_type", "action_type")):
        subset = [row for row in relation_action_rows if row["field_name"] == field]
        rows.append((label, len({row["current_value"] for row in subset}), len({row["proposed_controlled_value"] for row in subset})))
    fig, ax = plt.subplots(figsize=(12, 7.2))
    y = list(range(len(rows)))
    current = [row[1] for row in rows]
    proposed = [row[2] for row in rows]
    height = 0.36
    ax.barh([value - height / 2 for value in y], current, height=height, color="#7D8C86", label="当前不同值")
    ax.barh([value + height / 2 for value in y], proposed, height=height, color="#2A6F6B", label="建议受控值")
    for idx, (_, a, b) in enumerate(rows):
        ax.text(a + 0.3, idx - height / 2, str(a), va="center", fontsize=10)
        ax.text(b + 0.3, idx + height / 2, str(b), va="center", fontsize=10)
    ax.set_yticks(y, [row[0] for row in rows])
    ax.invert_yaxis()
    ax.set_xlabel("不同取值数")
    ax.set_title("受控词汇收敛：保留信息，消除表面写法分裂", loc="left", fontsize=18, fontweight="bold", pad=16)
    ax.text(0, 1.01, "legal_status 的“收敛”包含显式 unresolved 值，不把推测升格为法定身份。", transform=ax.transAxes, fontsize=10, color="#5F625F")
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.grid(axis="x", color="#D4CEC0", linewidth=0.8, alpha=0.8)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, loc="lower right")
    fig.tight_layout()
    fig.savefig(FIG_VOCAB_PNG, dpi=180, bbox_inches="tight", metadata={"Software": "NW2-E schema freeze builder"})
    fig.savefig(FIG_VOCAB_SVG, bbox_inches="tight", metadata={"Date": "2026-07-20"})
    normalize_svg_trailing_whitespace(FIG_VOCAB_SVG)
    plt.close(fig)


def make_brief(
    actors: list[dict[str, str]], actor_rows: list[dict[str, str]],
    aliases: list[dict[str, str]], alias_rows: list[dict[str, str]],
    places: list[dict[str, str]], actor_place_edges: list[dict[str, str]],
    place_conflicts: list[dict[str, str]],
    venues: list[dict[str, str]], venue_conflicts: list[dict[str, str]],
    relation_action_rows: list[dict[str, str]], candidates: list[dict[str, str]],
    hr_rows: list[dict[str, str]],
) -> str:
    class_current = len({row["current_value"] for row in actor_rows if row["field_name"] == "actor_class"})
    class_proposed = len({row["proposed_controlled_value"] for row in actor_rows if row["field_name"] == "actor_class"})
    legal_current = len({row["current_value"] for row in actor_rows if row["field_name"] == "legal_status_guess"})
    legal_proposed = len({row["proposed_controlled_value"] for row in actor_rows if row["field_name"] == "legal_status_guess"})
    relation_rows = [row for row in relation_action_rows if row["field_name"] == "relation_type"]
    action_rows = [row for row in relation_action_rows if row["field_name"] == "action_type"]
    venue_human = sum(row["requires_human_review"] == "yes" for row in venue_conflicts)
    human_fields = set(HUMAN_FIELDS) | {
        field for row in hr_rows for field in row if field not in HR_FIELDS
    }
    filled_hr = sum(any(row.get(field, "") for field in human_fields) for row in hr_rows)
    pending_hr = len(hr_rows) - filled_hr
    human_actor_assignments = sum(
        row["requires_human_review"] == "yes" for row in actor_rows
    )
    alias_type_count = len({row["alias_type"] for row in aliases})
    if place_conflicts:
        place_conflict_text = (
            f"{len(actor_place_edges)} 条 actor–place 边仍发现 **{len(place_conflicts)} 个交叉键冲突**。"
            "这些冲突不得在 schema 冻结中静默修补，必须进入新的空间人工闸门。"
        )
    else:
        place_conflict_text = (
            f"{len(actor_place_edges)} 条 actor–place 边目前有 **0 个交叉键冲突**。"
            "HR-025 已将 AP123 固定为 P007 Camp Foster，并批准只在来源明确指称先岛整体时使用 P021；"
            "本包不重复开启这些决定。"
        )
    return dedent(f"""
    # Schema／alias／空间字段冻结审计 brief v1

    日期：2026-07-20

    状态：**冻结前候选包；没有修改中央 schema、registry、alias、place、venue 或关系表。**

    ## 1. 结论先行

    当前 registry 的 {len(actors)} 个 actor，其 `actor_class`、`legal_status_guess`、`origin_type` 共 **{len(actor_rows)} 个字段单元（N×3）**已逐项覆盖。HR-027 与后续身份修订已经受控合并，重生后的每个 actor 均自动进入三字段审计。当前共有 **{len(candidates)} 条统一候选**，其中 **{len(hr_rows)} 条进入 HR-029**；人工字段按稳定 review item ID 保留，当前已填写 {filled_hr} 条、待处理 {pending_hr} 条。

    `origin_type` 的 7 个值已闭合，可原样冻结。`actor_class` 从 {class_current} 个表面值收敛为 {class_proposed} 个建议值；仍有 {human_actor_assignments} 个 actor 字段 assignment 需要人工决定。`legal_status_guess` 从 {legal_current} 种表面写法收敛到 {legal_proposed} 个受控值；无法确认法人格者明确落到 `*_unresolved`，而不是猜成 NPO、基金会或正式网络。

    ![冻结准备度](fig_schema_freeze_readiness_v1.png)

    ## 2. Alias：查找等价不等于实体等价

    现有 {len(aliases)} 条 alias、{alias_type_count} 种 alias_type 全部入审计。没有发现跨 actor 的规范化 alias 冲突；同一 actor 的来源敏感写法仍按各自来源保留。

    三类名称必须和普通 alias 分开：

    - A010 的「石垣島への自衛隊配備を止める住民の会」是 predecessor label，不是 A010 的简单旧名；
    - A052 第4次嘉手纳、A053 第2次普天间是 case-round label，不表示每轮成员完全相同；
    - A105 日本YWCA 与 A107 冲绳YWCA 是全国／地域两个 actor，以 affiliation 连接，不互作 alias，也不转移行动角色。

    A106 的「首都圏連絡会／首都圏キャンペーン」canonical 选择仍需 HR-029。A111 的「女団協」不得转成已剔除 A094 所关联的「沖女連」，也不得借 alias 把 A094 重新放回 registry。

    ## 3. Place 与 venue：空间跨键已修复，venue 占位需分型处理

    {len(places)} 个 place 都获得 parent 与查询 alias 候选。P004 Futenma 与 P010 MCAS Futenma必须分别代表议题／地域层与实体基地层；P005 Kadena 需明确是 Kadena Air Base；P011–P013 的与那国、石垣、宫古必须区分町／市与岛屿／区域写法。这五项进入 HR-029。

    {place_conflict_text}

    16 项 venue taxonomy 的 ID 与 label/group 本身无重复；但 event/pathway 表有 **{len(venue_conflicts)} 条 `R10_VENUE` 占位引用**。其中明确的 USO 服务／捐赠观察可机械候选为 V016；伞状 membership、区域赞助、行政委托、JICA活动与公共外交 opportunity 并非同一种场域，所以 {venue_human} 条进入 HR-029。V015 已实际使用，其“future expansion”旧 note 已过时，但本包不改 note。

    ## 4. Relation / action 受控值

    `relation_type` 覆盖 {sum(int(row['affected_row_count']) for row in relation_rows)} 行、{len(relation_rows)} 个当前值，建议收敛为 {len({row['proposed_controlled_value'] for row in relation_rows})} 个受控值。关键边界：

    - `duplicate_replaced_by_F022` 是被拒绝重复记录，不应继续作为 relation type；
    - `co_presence_lead` 只能候选为 co-presence observation，不能写成 coordination；
    - `aggregate_history` 是金额历史观察，不是可分配给具体 recipient 的普通关系；
    - `grant_opportunity` 保持 opportunity，不能升级为 grant 或 recipient；
    - joint in-kind contribution 保留“共同贡献、份额未拆”的边界。

    `action_type` 覆盖 {sum(int(row['affected_row_count']) for row in action_rows)} 行、{len(action_rows)} 个当前值，建议收敛为 {len({row['proposed_controlled_value'] for row in action_rows})} 个受控值。`co_signing` 与 `joint_statement`统一为事件参与；两种 request-letter 写法统一为 submission participation；`pathway_role`改为显式 analytical seed。共同署名、请求或同场出现仍不是稳定联盟。

    ![受控词汇收敛](fig_vocabulary_consolidation_v1.png)

    ## 5. 冻结后的可写与不可写

    完成 HR-029 并由主线程另行合并后，可以写：本项目使用闭合 actor/origin/legal-status/alias/place/venue/relation/action 词汇；前身、诉讼轮次、全国—地方组织和空间层级各有显式边界；每个关系与行动值可以被 lint。

    仍不可写：名称相似即同一组织；前身与后继是简单改名；不同诉讼轮次成员相同；全国组织行动自动转移到地方组织；`R10_VENUE` 九条可统一替换；NOFO 是已拨款；共同参与是稳定联盟。Schema freeze 也不批准任何候选 actor、edge、funding 或选举角色。

    ## 6. 后续顺序

    1. HR-027、HR-019、HR-024、HR-025 与 HR-032 已完成受控合并，本包是其后的最终重生输入；
    2. 负责人完成 `HR029_schema_alias_freeze_review_v0.csv`；
    3. 主线程再受控合并 class assignment、alias lineage、place/venue 与 relation/action 语义；
    4. 处理 `R10_VENUE` 后运行全库 FK/lint，再冻结正式 codebook；
    5. 最后处理 HR-031 的解释强度决定，并生成报告、论文和 PPT。

    复现命令：`python scripts/make_schema_alias_freeze_v1.py`。
    """).strip() + "\n"


def make_readme() -> str:
    return dedent("""
    # Schema / alias freeze audit v1

    Generated by `python scripts/make_schema_alias_freeze_v1.py`.

    This package is a freeze-candidate audit. It does not modify or approve the central schema, actor registry, aliases, place registry, venue taxonomy, actor-place edges, relations or actions.

    ## Main outputs

    - `../../data/interim/36_schema_alias_freeze_candidates_v1.csv` — unified object/field freeze candidates.
    - `actor_field_audit_v1.csv` and `actor_value_mapping_v1.csv` — current registry N actors × 3 fields and aggregate mappings; actor count is dynamic.
    - `alias_audit_v1.csv` / `alias_boundary_audit_v1.csv` — identity lookup versus nonidentity lineage rules.
    - `place_hierarchy_alias_audit_v1.csv` / `place_crosskey_conflicts_v1.csv` — dynamic place hierarchy proposals and any remaining cross-key mismatch.
    - `venue_taxonomy_audit_v1.csv` / `venue_reference_conflicts_v1.csv` — 16 taxonomy rows and all current orphan references.
    - `relation_action_value_mapping_v1.csv` — complete observed value inventory and controlled mappings.
    - `lint_rules_v1.csv` / `impact_counts_v1.csv` — executable rules and impact summary.
    - `HR029_schema_alias_freeze_review_v0.csv` — stable review items; regeneration preserves all human and added final/status fields by `review_item_id`.
    - Two PNG/SVG figures, explanatory brief and validation report.

    ## Hard boundary

    Similar names never trigger an automatic entity merge. A predecessor label, case-round label, national/local brand relationship or spatial-name overlap remains explicitly typed and bounded. HR-027/019/024/025/032 are already merged; this regenerated package still makes no HR-029 decisions. AP123 and P021 remain frozen from HR-025 and are not reopened here.
    """).strip() + "\n"


def validate(
    actors: list[dict[str, str]], actor_rows: list[dict[str, str]],
    aliases: list[dict[str, str]], alias_rows: list[dict[str, str]],
    places: list[dict[str, str]], actor_place_edges: list[dict[str, str]],
    place_rows: list[dict[str, str]],
    place_conflicts: list[dict[str, str]], venues: list[dict[str, str]],
    venue_rows: list[dict[str, str]], venue_conflicts: list[dict[str, str]],
    relation_action_rows: list[dict[str, str]], candidates: list[dict[str, str]],
    hr_rows: list[dict[str, str]],
) -> None:
    assert actors
    assert len(actor_rows) == len(actors) * 3
    expected_actor_cells = {
        (row["actor_id"], field)
        for row in actors
        for field in ("actor_class", "legal_status_guess", "origin_type")
    }
    assert {(row["actor_id"], row["field_name"]) for row in actor_rows} == expected_actor_cells
    assert aliases and len(alias_rows) == len(aliases)
    assert places and len(place_rows) == len(places)
    assert len({row["edge_id"] for row in actor_place_edges}) == len(actor_place_edges)
    assert {row["place_id"] for row in actor_place_edges} <= {row["place_id"] for row in places}
    assert not place_conflicts
    assert len(venues) == 16 and len(venue_rows) == 16
    known_venue_ids = {row["venue_id"] for row in venues}
    expected_venue_conflicts = [
        row for row in read_csv(PATHWAY_FILE) if row["venue_id"] not in known_venue_ids
    ]
    assert len(venue_conflicts) == len(expected_venue_conflicts)
    assert {row["current_venue_id"] for row in venue_conflicts} == {"R10_VENUE"}
    assert all(row["observation_id"] in ORPHAN_VENUE_PLAN for row in venue_conflicts)
    assert any(row["requires_human_review"] == "yes" for row in venue_conflicts)
    relation_rows = [row for row in relation_action_rows if row["field_name"] == "relation_type"]
    action_rows = [row for row in relation_action_rows if row["field_name"] == "action_type"]
    assert relation_rows and all(int(row["affected_row_count"]) > 0 for row in relation_rows)
    assert action_rows and all(int(row["affected_row_count"]) > 0 for row in action_rows)
    assert len({row["candidate_id"] for row in candidates}) == len(candidates)
    assert all(row["proposed_value"] for row in candidates)
    assert all(row["machine_status"] in {"freeze_candidate", "needs_human_review", "defer_to_HR025"} for row in candidates)
    assert all(field in row for row in hr_rows for field in HUMAN_FIELDS)
    assert len({row["review_item_id"] for row in hr_rows}) == len(hr_rows)
    hr_ids = {row["review_item_id"] for row in hr_rows}
    assert all(
        (row["requires_human_review"] == "yes" and row["hr_item_id"] in hr_ids)
        or (row["machine_status"] == "defer_to_HR025" and row["hr_item_id"] == "HR-025")
        or (row["requires_human_review"] == "no" and not row["hr_item_id"])
        for row in candidates
    )
    assert sum(
        row["requires_human_review"] == "yes" and row["machine_status"] == "needs_human_review"
        for row in candidates
    ) == len(hr_rows)
    assert not any(row["object_id"] == "AP123" for row in hr_rows)
    assert not any("auto_merge" in row["candidate_disposition"] for row in candidates)
    canonical_groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in actors:
        canonical_groups[normalized_name(row["canonical_name"])].append(row)
    for rows in canonical_groups.values():
        if len(rows) <= 1:
            continue
        roots = [row for row in rows if not row.get("merged_duplicate_of")]
        assert len(roots) == 1
        assert all(
            row["actor_id"] == roots[0]["actor_id"]
            or row.get("merged_duplicate_of") == roots[0]["actor_id"]
            for row in rows
        )
    alias_actor_norms: dict[str, set[str]] = defaultdict(set)
    for row in aliases:
        alias_actor_norms[normalized_name(row["alias"])].add(row["actor_id"])
    assert not any(len(actor_ids) > 1 for actor_ids in alias_actor_norms.values())


def validation_text(
    actors: list[dict[str, str]], actor_rows: list[dict[str, str]],
    aliases: list[dict[str, str]], places: list[dict[str, str]],
    actor_place_edges: list[dict[str, str]],
    place_conflicts: list[dict[str, str]], venues: list[dict[str, str]],
    venue_conflicts: list[dict[str, str]], relation_action_rows: list[dict[str, str]],
    candidates: list[dict[str, str]], hr_rows: list[dict[str, str]], digest: str,
    preservation: dict[str, int],
) -> str:
    relation_rows = [row for row in relation_action_rows if row["field_name"] == "relation_type"]
    action_rows = [row for row in relation_action_rows if row["field_name"] == "action_type"]
    human_fields = set(HUMAN_FIELDS) | {
        field for row in hr_rows for field in row if field not in HR_FIELDS
    }
    filled = sum(any(row.get(field, "") for field in human_fields) for row in hr_rows)
    return dedent(f"""
    # Schema / alias freeze validation v1

    Generated: 2026-07-20

    - Actor registry: {len(actors)} actors; {len(actor_rows)} actor-field cells covered exactly as dynamic N×3.
    - Aliases: {len(aliases)} rows; zero normalized cross-actor collisions; one documented same-actor punctuation collision.
    - Places: {len(places)} nodes and {len(actor_place_edges)} actor–place edges; zero cross-key mismatches after HR-025 fixed AP123 to P007 Camp Foster and approved P021 for explicit Sakishima-wide evidence.
    - Venues: {len(venues)} taxonomy rows; {len(venue_conflicts)} orphan `R10_VENUE` references captured; {sum(row['requires_human_review'] == 'yes' for row in venue_conflicts)} require HR-029.
    - Relation types: {len(relation_rows)} values over {sum(int(row['affected_row_count']) for row in relation_rows)} rows; full mapping coverage.
    - Action types: {len(action_rows)} values over {sum(int(row['affected_row_count']) for row in action_rows)} rows; full mapping coverage.
    - Unified candidates: {len(candidates)} unique rows; every row has a proposed value and explicit interpretation boundary.
    - HR-029: {len(hr_rows)} stable rows; {filled} currently contain human/final/status values; cross-linked one-to-one.
    - Stable ID mapping: the `(domain, object_id, field_name)` review item retains its prior `review_item_id`; new items allocate unused suffixes.
    - HR preservation: {preservation['preserved_nonblank_rows']} populated rows restored from the pre-existing file; {preservation['extra_human_fields']} extra human columns retained.
    - Temporary-copy sentinel test (`TEST_HUMAN_DECISION` plus final/status fields): passed; real HR table was not modified by the test.
    - Workflow guard: HR-027/019/024/025/032 decisions are merged before this regeneration; all post-merge actors appear in N×3 audit cells.
    - Synthetic post-HR027 actor coverage test: passed; the added actor receives actor_class, legal_status_guess and origin_type audit rows.
    - No automatic entity-merge disposition exists; predecessor, case-round and national/local brand boundaries are explicit.
    - Two figures generated in PNG/SVG; SVG line-tail whitespace normalized after save; deterministic non-figure digest: `{digest}`.
    """).strip() + "\n"


def sha_digest(paths: list[Path]) -> str:
    digest = hashlib.sha256()
    for path in sorted(paths, key=lambda value: value.as_posix()):
        digest.update(path.name.encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()[:16]


def main() -> None:
    actors = read_csv(ACTOR_FILE)
    aliases = read_csv(ALIAS_FILE)
    places = read_csv(PLACE_FILE)
    actor_place_edges = read_csv(ACTOR_PLACE_FILE)
    aev_rows = read_csv(AEV_FILE)
    pathway_rows = read_csv(PATHWAY_FILE)
    venues = read_csv(VENUE_FILE)
    dynamic_actor_coverage_self_test(actors)

    candidates: list[dict[str, str]] = []
    actor_rows = actor_audit(actors, candidates)
    actor_mappings = aggregate_actor_mappings(actor_rows)
    alias_rows, alias_boundaries = alias_audit(actors, aliases, candidates)
    place_rows, place_conflicts = place_audit(places, actor_place_edges, candidates)
    venue_rows, venue_conflicts = venue_audit(venues, aev_rows, pathway_rows, candidates)
    relation_action_rows = relation_action_audit(candidates)
    generated_hr_rows = assign_hr(candidates)
    human_preservation_self_test(generated_hr_rows)
    hr_rows, hr_fields, preservation = preserve_human_fields(
        generated_hr_rows, HR_FILE, HR_FIELDS,
        identity_fields=("domain", "object_id", "field_name"),
    )

    for rows in (actor_rows, alias_rows, alias_boundaries, place_rows, place_conflicts, venue_rows, venue_conflicts, relation_action_rows):
        backfill_hr_ids(rows, candidates)

    lint_rows = make_lint_rules(
        actors, aliases, places, place_conflicts, venues, venue_conflicts, relation_action_rows,
    )
    impact_rows = make_impacts(
        actors, actor_rows, actor_mappings, aliases, alias_rows, places,
        place_conflicts, venues, venue_conflicts, relation_action_rows,
        candidates, hr_rows,
    )

    validate(
        actors, actor_rows, aliases, alias_rows, places, actor_place_edges,
        place_rows, place_conflicts, venues, venue_rows, venue_conflicts,
        relation_action_rows, candidates, hr_rows,
    )

    write_csv(MAIN_FILE, candidates, MAIN_FIELDS)
    write_csv(ACTOR_AUDIT_FILE, actor_rows, list(actor_rows[0]))
    write_csv(ACTOR_MAPPING_FILE, actor_mappings, list(actor_mappings[0]))
    write_csv(ALIAS_AUDIT_FILE, alias_rows, list(alias_rows[0]))
    write_csv(ALIAS_BOUNDARY_FILE, alias_boundaries, list(alias_boundaries[0]))
    write_csv(PLACE_AUDIT_FILE, place_rows, list(place_rows[0]))
    write_csv(
        PLACE_CONFLICT_FILE, place_conflicts,
        list(place_conflicts[0]) if place_conflicts else PLACE_CONFLICT_FIELDS,
    )
    write_csv(VENUE_AUDIT_FILE, venue_rows, list(venue_rows[0]))
    write_csv(VENUE_CONFLICT_FILE, venue_conflicts, list(venue_conflicts[0]))
    write_csv(REL_ACTION_FILE, relation_action_rows, list(relation_action_rows[0]))
    write_csv(LINT_FILE, lint_rows, list(lint_rows[0]))
    write_csv(IMPACT_FILE, impact_rows, list(impact_rows[0]))
    write_csv(HR_FILE, hr_rows, hr_fields)
    written_hr_fields, written_hr_rows = read_csv_with_fields(HR_FILE)
    assert written_hr_fields == hr_fields and written_hr_rows == hr_rows

    OUT.mkdir(parents=True, exist_ok=True)
    render_readiness(candidates)
    render_vocabulary(actor_mappings, alias_rows, places, venues, relation_action_rows)
    BRIEF_FILE.write_text(
        make_brief(
            actors, actor_rows, aliases, alias_rows, places, actor_place_edges,
            place_conflicts, venues, venue_conflicts, relation_action_rows,
            candidates, hr_rows,
        ),
        encoding="utf-8",
    )
    README_FILE.write_text(make_readme(), encoding="utf-8")

    digest_paths = [
        MAIN_FILE, ACTOR_AUDIT_FILE, ACTOR_MAPPING_FILE, ALIAS_AUDIT_FILE,
        ALIAS_BOUNDARY_FILE, PLACE_AUDIT_FILE, PLACE_CONFLICT_FILE,
        VENUE_AUDIT_FILE, VENUE_CONFLICT_FILE, REL_ACTION_FILE, LINT_FILE,
        IMPACT_FILE, HR_FILE, BRIEF_FILE, README_FILE,
    ]
    digest = sha_digest(digest_paths)
    VALIDATION_FILE.write_text(
        validation_text(
            actors, actor_rows, aliases, places, actor_place_edges,
            place_conflicts, venues, venue_conflicts, relation_action_rows,
            candidates, hr_rows, digest, preservation,
        ),
        encoding="utf-8",
    )
    print(
        f"Schema/alias freeze audit generated: {len(candidates)} candidates / "
        f"{len(hr_rows)} HR-029 items / preserved "
        f"{preservation['preserved_nonblank_rows']} populated rows / digest {digest}"
    )


if __name__ == "__main__":
    main()
