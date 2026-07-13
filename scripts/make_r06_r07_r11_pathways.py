"""Build the online explanatory layer shared by R6, R7 and R11.

Writes only the module output directory and the formal data/interim/26 table.
Facts and analytical seeds remain separate. HR-018 reviews R10 relation facts;
HR-021 reviews their downstream R6/R11 scope and analytical-seed promotion.
"""

from __future__ import annotations

import csv
import html
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "R06_R07_R11_pathways_v1"
DATA = ROOT / "data" / "interim"

AEV = DATA / "09_actor_event_venue_edges_v0.csv"
R8_ROLES = DATA / "18_legal_policy_actor_roles_v0.csv"
R8_CASES = DATA / "17_legal_policy_procedure_cases_v0.csv"
R10_REL = DATA / "21_admin_collaboration_relations_v0.csv"
ACTORS = DATA / "01_actor_registry_initial_v0.csv"
SOURCES = DATA / "05_source_log_initial_v0.csv"
VENUES = ROOT / "outputs" / "phase1_foundation_v1" / "venue_taxonomy_v0.csv"
LEGACY_PATHS = ROOT / "outputs" / "module_completion_v0" / "transnational_pathway_nodes_v0.csv"
HR018 = ROOT / "outputs" / "R10_administrative_collaboration_v0" / "HR018_relation_review_v0.csv"

FORMAL_FACTS = DATA / "26_actor_event_venue_target_entry_modes_v0.csv"
SEEDS = OUT / "analytical_seeds_v0.csv"
R6_TABLE = OUT / "r06_pathway_comparison_v0.csv"
R7_TABLE = OUT / "r07_venue_shift_stages_v0.csv"
R11_TABLE = OUT / "r11_external_entry_matrix_v0.csv"
HR021 = OUT / "HR021_review_items_v0.csv"
HR021_MD = OUT / "HR021_review_packet.md"
BRIEF = OUT / "R06_R07_R11_explanatory_brief_v1.md"
NOTE = OUT / "validation_note_v0.md"

R6_SVG = OUT / "fig_r06_target_pathways_v0.svg"
R6_HTML = OUT / "fig_r06_target_pathways_v0.html"
R7_SVG = OUT / "fig_r07_venue_shift_small_multiples_v0.svg"
R7_HTML = OUT / "fig_r07_venue_shift_small_multiples_v0.html"
R11_SVG = OUT / "fig_r11_external_entry_matrix_v0.svg"
R11_HTML = OUT / "fig_r11_external_entry_matrix_v0.html"

FACT_FIELDS = [
    "observation_id", "source_layer", "source_record_ids", "event_or_project_id",
    "event_or_project_name", "date_or_period", "actor_id", "legacy_candidate_id",
    "actor_name", "actor_category", "origin_type", "role", "entry_mode",
    "venue_id", "venue_label", "target_type", "target_id_or_name", "local_object",
    "place", "observation_type", "evidence_level", "source_refs", "review_status",
    "interpretation_limit",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows({field: row.get(field, "") for field in fields} for row in rows)


def split_refs(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def unique_join(values: list[str], separator: str = ";") -> str:
    return separator.join(dict.fromkeys(value for value in values if value))


def event_place(event_id: str) -> str:
    if event_id in {"EV2010_WWF_67", "EV2015_NACSJ_31", "EV2020_OEJP_MMC_71", "EV2003_DUGONG_LAWSUIT"}:
        return "Henoko; Oura Bay"
    if "YONAGUNI" in event_id:
        return "Yonaguni"
    if "ISHIGAKI" in event_id:
        return "Ishigaki"
    if "NAGO" in event_id or "PREF_REFERENDUM" in event_id:
        return "Nago; Okinawa"
    return "Okinawa"


def local_object(event_id: str, target: str) -> str:
    if event_id in {"EV2010_WWF_67", "EV2015_NACSJ_31", "EV2020_OEJP_MMC_71", "EV2003_DUGONG_LAWSUIT"}:
        return "Henoko/Oura Bay base-construction and dugong issue"
    return target


def aev_entry_mode(row: dict[str, str]) -> str:
    return {
        "co_signing": "advocacy_joint_statement",
        "request_letter": "international_institution_request",
        "litigation": "international_legal",
        "referendum": "local_democratic_procedure",
        "opinion_ad": "public_opinion_advocacy",
    }[row["action_type"]]


def r10_entry_mode(relation_type: str) -> str:
    return {
        "event_collaboration": "administrative_event_collaboration",
        "sponsorship": "service_sponsorship",
        "donation": "charitable_donation",
        "grant": "charitable_grant",
        "network_membership": "service_network_coordination",
        "grant_opportunity": "public_diplomacy_opportunity",
    }[relation_type]


def build_facts() -> list[dict[str, str]]:
    actor_by_id = {row["actor_id"]: row for row in read_csv(ACTORS)}
    venue_by_id = {row["venue_id"]: row["venue_label"] for row in read_csv(VENUES)}
    facts: list[dict[str, str]] = []

    for row in read_csv(AEV):
        if row["reviewer_status"] == "analytical_seed":
            continue
        if row["action_type"] == "litigation" and row["entity_type"] == "registry_actor":
            # Canonical registered-actor legal roles come from the HR-014 R8 role table.
            continue
        actor_id = row["actor_or_counterpart_id"]
        actor = actor_by_id.get(actor_id, {})
        facts.append(
            {
                "observation_id": f"OBS_{row['record_id']}",
                "source_layer": "formal_AEV",
                "source_record_ids": row["record_id"],
                "event_or_project_id": row["event_id"],
                "event_or_project_name": row["event_name"],
                "date_or_period": row["event_year"],
                "actor_id": actor_id,
                "legacy_candidate_id": row.get("legacy_candidate_id", ""),
                "actor_name": row["actor_or_counterpart_name"],
                "actor_category": row["entity_type"],
                "origin_type": actor.get("origin_type", "unverified_or_not_applicable"),
                "role": row["role"],
                "entry_mode": aev_entry_mode(row),
                "venue_id": row["venue_id"],
                "venue_label": venue_by_id[row["venue_id"]],
                "target_type": row["target_type"],
                "target_id_or_name": row["target_id_or_name"],
                "local_object": local_object(row["event_id"], row["target_id_or_name"]),
                "place": event_place(row["event_id"]),
                "observation_type": "event_or_role_fact",
                "evidence_level": row["evidence_level"],
                "source_refs": row["source_id"],
                "review_status": row["reviewer_status"],
                "interpretation_limit": row["interpretation_limit"],
            }
        )

    case_by_id = {row["case_id"]: row for row in read_csv(R8_CASES)}
    for row in read_csv(R8_ROLES):
        if row["case_id"] != "R8C01":
            continue
        case = case_by_id[row["case_id"]]
        actor_id = row["actor_id"]
        actor = actor_by_id.get(actor_id, {})
        facts.append(
            {
                "observation_id": f"OBS_{row['role_id']}",
                "source_layer": "R8_human_checked_role",
                "source_record_ids": row["role_id"],
                "event_or_project_id": row["case_id"],
                "event_or_project_name": case["case_name"],
                "date_or_period": f"{case['start_date']}–{case['end_or_decision_date']}",
                "actor_id": actor_id or row["provisional_entity_id"],
                "legacy_candidate_id": "",
                "actor_name": row["actor_name"],
                "actor_category": row["entity_kind"],
                "origin_type": actor.get("origin_type", "provisional_or_institution"),
                "role": row["role"],
                "entry_mode": "international_legal",
                "venue_id": "V005",
                "venue_label": venue_by_id["V005"],
                "target_type": "defendant_institution",
                "target_id_or_name": row["target_or_recipient"],
                "local_object": "Henoko/Oura Bay base-construction and dugong issue",
                "place": case["place"],
                "observation_type": "case_specific_legal_role_fact",
                "evidence_level": row["evidence_level"],
                "source_refs": row["source_refs"],
                "review_status": row["review_status"],
                "interpretation_limit": row["interpretation_limit"],
            }
        )

    for row in read_csv(R10_REL):
        if row["review_status"] not in {"human_checked", "human_revised"}:
            continue
        actor = actor_by_id.get(row["source_entity_id"], {})
        place = (
            "Camp Schwab / USO Okinawa"
            if row["relation_type"] == "sponsorship"
            else "Okinawa base-community service field"
            if row["relation_type"] in {"donation", "grant", "network_membership"}
            else "Okinawa international-cooperation field"
            if row["relation_type"] == "event_collaboration"
            else "Okinawa public-diplomacy field"
        )
        venue_label = (
            "JICA/international-cooperation event"
            if row["relation_type"] == "event_collaboration"
            else "USO/base-community service venue"
            if row["relation_type"] in {"sponsorship", "donation", "grant"}
            else "military-spouse umbrella network"
            if row["relation_type"] == "network_membership"
            else "U.S. public-diplomacy opportunity"
        )
        facts.append(
            {
                "observation_id": f"OBS_{row['relation_observation_id']}",
                "source_layer": "R10_human_reviewed_relation",
                "source_record_ids": row["relation_observation_id"],
                "event_or_project_id": row["relation_observation_id"],
                "event_or_project_name": row["program_name"],
                "date_or_period": row["fiscal_year"] or row["period_start"],
                "actor_id": row["source_entity_id"],
                "legacy_candidate_id": "",
                "actor_name": row["source_entity_name"],
                "actor_category": row["source_entity_kind"],
                "origin_type": actor.get("origin_type", "institution_or_unknown"),
                "role": row["relation_type"],
                "entry_mode": r10_entry_mode(row["relation_type"]),
                "venue_id": "R10_VENUE",
                "venue_label": venue_label,
                "target_type": row["target_entity_kind"],
                "target_id_or_name": row["target_entity_name"],
                "local_object": row["target_entity_name"],
                "place": place,
                "observation_type": "human_reviewed_function_or_resource_relation",
                "evidence_level": row["evidence_level"],
                "source_refs": row["source_refs"],
                "review_status": row["review_status"],
                "interpretation_limit": row["interpretation_limit"],
            }
        )
    return facts


def build_seeds() -> list[dict[str, str]]:
    legacy_ids = {row["node_id"] for row in read_csv(LEGACY_PATHS)}
    legacy_map = {
        "AEV0061": "A019;P002/P003",
        "AEV0062": "A003;F_DUGONG",
        "AEV0063": "A004;F_EIA",
        "AEV0064": "A005;EV2015_2020",
    }
    seeds: list[dict[str, str]] = []
    for row in read_csv(AEV):
        if row["reviewer_status"] != "analytical_seed":
            continue
        refs = legacy_map[row["record_id"]]
        if any(ref not in legacy_ids for ref in refs.split(";")):
            raise ValueError(f"legacy pathway node missing for {row['record_id']}")
        seeds.append(
            {
                "seed_id": f"SEED_{row['record_id']}",
                "source_record_id": row["record_id"],
                "actor_id": row["actor_or_counterpart_id"],
                "actor_name": row["actor_or_counterpart_name"],
                "proposed_pathway_stage": row["pathway_stage"],
                "venue_id": row["venue_id"],
                "target_id_or_name": row["target_id_or_name"],
                "source_refs": row["source_id"],
                "evidence_level": row["evidence_level"],
                "review_status": "analytical_seed",
                "legacy_context_node_ids": refs,
                "interpretation_limit": row["interpretation_limit"],
            }
        )
    return seeds


def ids_for(facts: list[dict[str, str]], predicate) -> list[str]:
    return [row["observation_id"] for row in facts if predicate(row)]


def build_r6(facts: list[dict[str, str]]) -> list[dict[str, str]]:
    case = next(row for row in read_csv(R8_CASES) if row["case_id"] == "R8C01")
    definitions = [
        (
            "R6P01", "international_legal", "named plaintiffs/counsel and non-party boundary",
            lambda r: r["entry_mode"] == "international_legal",
            "U.S. federal courts", "U.S. Department of Defense",
            "A reviewable NHPA Section 402 standard and information record were produced; the 2020 outcome favored DoD.",
            case["interpretation_limit"], "A009;A020;A045;A076;F_DUGONG;F_EIA",
        ),
        (
            "R6P02", "international_institution_request", "request participants",
            lambda r: r["event_or_project_id"] == "EV2020_OEJP_MMC_71",
            "U.S. Marine Mammal Commission", "U.S. Marine Mammal Commission",
            "The 2020 request and its participants are documented; this table does not establish an institutional response or policy change.",
            "Nine labels remain unverified event participants outside the actor registry; request participation is not alliance membership.",
            "A001;A020;EV2015_2020",
        ),
        (
            "R6P03", "domestic_environmental_solidarity", "statement hosts and Japan-based co-signers",
            lambda r: r["entry_mode"] == "advocacy_joint_statement" and r["origin_type"] == "japan_domestic",
            "public statement venue", "Henoko base-construction plan",
            "Japan-based organizations publicly joined 2010/2015 statements.",
            "Event-specific co-signing does not establish a stable alliance or policy response.",
            "A004;A005;F_DUGONG;F_EIA",
        ),
        (
            "R6P04", "overseas_solidarity", "overseas co-signers",
            lambda r: r["entry_mode"] == "advocacy_joint_statement" and r["origin_type"] in {"us_origin", "international", "mixed_or_network"},
            "transnational public statement field", "Henoko base-construction plan",
            "Overseas organizations are visible as event-specific co-signers in the 2015 statement.",
            "A signature is not proof of continuing coordination, local representation, or causal influence.",
            "EV2015_2020;F_DUGONG",
        ),
        (
            "R6P05", "administrative_cooperation", "publicly named event collaborators",
            lambda r: r["source_record_ids"] == "R10R017",
            "JICA/international-cooperation event", "ONC–JICA public collaboration context",
            "ONC and JICA Okinawa are publicly named in an international-cooperation event context.",
            "Co-participation is non-funding and does not establish a stable alliance or a base-policy stance.",
            "",
        ),
        (
            "R6P06", "public_diplomacy_opportunity", "program publisher; recipient unknown",
            lambda r: r["source_record_ids"] == "R10R035",
            "U.S. public-diplomacy opportunity", "unknown Okinawa Youth Council recipient",
            "A NOFO/opportunity is documented.",
            "No award or recipient is established; do not treat the opportunity as a funding edge.",
            "",
        ),
    ]
    rows: list[dict[str, str]] = []
    for pathway_id, family, roles, predicate, venue, target, result, limit, legacy in definitions:
        observation_ids = ids_for(facts, predicate)
        selected = [row for row in facts if row["observation_id"] in observation_ids]
        verified = sum(row["actor_category"] != "unverified_event_participant" for row in selected)
        unverified = len(selected) - verified
        rows.append(
            {
                "pathway_id": pathway_id,
                "pathway_family": family,
                "observed_actor_roles": roles,
                "venue_or_entry_point": venue,
                "target": target,
                "fact_observation_ids": ";".join(observation_ids),
                "fact_count": str(len(observation_ids)),
                "verified_actor_or_entity_count": str(verified),
                "unverified_event_participant_count": str(unverified),
                "source_refs": unique_join(
                    [
                        source_ref
                        for row in selected
                        for source_ref in split_refs(row["source_refs"])
                    ]
                ),
                "observed_result": result,
                "interpretation_limit": limit,
                "legacy_context_node_ids": legacy,
            }
        )
    return rows


def build_r7(facts: list[dict[str, str]]) -> list[dict[str, str]]:
    fact_ids = {row["observation_id"] for row in facts}
    rows = [
        ("R7C01", "Dugong international litigation", 1, "2003", "Henoko/Oura Bay", "Dugong/base project translated into an NHPA Section 402 claim", "OBS_R8R001;OBS_R8R003", "procedural chronology"),
        ("R7C01", "Dugong international litigation", 2, "2003", "U.S. District Court", "Named plaintiffs and counsel entered a U.S. federal legal venue", "OBS_R8R001;OBS_R8R002;OBS_R8R003;OBS_R8R004;OBS_R8R005", "procedural chronology"),
        ("R7C01", "Dugong international litigation", 3, "2020", "Ninth Circuit", "Opinion articulated a Section 402 standard and affirmed judgment for DoD", "OBS_R8R001;OBS_R8R005", "procedural chronology"),
        ("R7C02", "2020 MMC request", 1, "2020", "Henoko/Oura Bay issue", "Dugong and construction issue stated in the request context", "OBS_AEV0034", "within-event role order"),
        ("R7C02", "2020 MMC request", 2, "2020", "civil-society request", "OEJP, JELF and event participants appear on the request", "OBS_AEV0034;OBS_AEV0035", "within-event role order"),
        ("R7C02", "2020 MMC request", 3, "2020", "U.S. Marine Mammal Commission", "Request was directed to a U.S. federal institution", "OBS_AEV0034;OBS_AEV0035", "within-event role order"),
        ("R7C03", "2015 transnational statement", 1, "2015", "Henoko/Oura Bay", "Local policy/ecology object anchors the statement", "OBS_AEV0006", "event composition order"),
        ("R7C03", "2015 transnational statement", 2, "2015", "NACSJ/Peace Boat statement venue", "Statement hosts organized a public advocacy venue", "OBS_AEV0006", "event composition order"),
        ("R7C03", "2015 transnational statement", 3, "2015", "domestic and overseas signatory field", "Public participation spans local, Japan-based and overseas organizations", "OBS_AEV0006;OBS_AEV0019;OBS_AEV0031", "event composition order"),
    ]
    output: list[dict[str, str]] = []
    for case_id, case_name, stage, date, venue, observation, refs, sequence in rows:
        ref_ids = split_refs(refs)
        if not set(ref_ids).issubset(fact_ids):
            raise ValueError(f"R7 stage references missing facts: {case_id}/{stage}")
        source_refs = unique_join(
            [
                source_ref
                for row in facts
                if row["observation_id"] in ref_ids
                for source_ref in split_refs(row["source_refs"])
            ]
        )
        output.append(
            {
                "case_id": case_id,
                "case_name": case_name,
                "stage_order": str(stage),
                "date_or_period": date,
                "venue_or_field": venue,
                "observed_stage": observation,
                "fact_observation_ids": refs,
                "source_refs": source_refs,
                "sequence_basis": sequence,
                "arrow_semantics": "ordered observation only; no causal inference",
            }
        )
    return output


def external_origin(origin: str) -> bool:
    return origin not in {"", "okinawa_local", "unverified_or_not_applicable", "provisional_or_institution"}


def build_r11(facts: list[dict[str, str]]) -> list[dict[str, str]]:
    actor_by_id = {row["actor_id"]: row for row in read_csv(ACTORS)}
    rows: list[dict[str, str]] = []

    def add(fact: dict[str, str], domain: str, entry_actor_id: str | None = None,
            entry_actor_name: str | None = None, origin: str | None = None,
            local_object_name: str | None = None, stance: str = "event_or_case_specific_only") -> None:
        rows.append(
            {
                "matrix_row_id": f"R11M{len(rows) + 1:03d}",
                "fact_observation_id": fact["observation_id"],
                "entry_domain": domain,
                "entry_mode": fact["entry_mode"],
                "entry_actor_id": entry_actor_id or fact["actor_id"],
                "entry_actor_name": entry_actor_name or fact["actor_name"],
                "origin_type": origin or fact["origin_type"],
                "local_object": local_object_name or fact["local_object"],
                "event_or_project": fact["event_or_project_name"],
                "venue_or_entry_point": fact["venue_label"],
                "target": fact["target_id_or_name"],
                "place": fact["place"],
                "role": fact["role"],
                "evidence_level": fact["evidence_level"],
                "source_refs": fact["source_refs"],
                "review_status": fact["review_status"],
                "directionality": "observed role/relation only; no causal direction beyond source",
                "political_stance_boundary": stance,
                "interpretation_limit": fact["interpretation_limit"],
            }
        )

    for fact in facts:
        if fact["entry_mode"] in {"advocacy_joint_statement", "international_institution_request"}:
            if fact["actor_category"] == "unverified_event_participant" or not external_origin(fact["origin_type"]):
                continue
            add(fact, "advocacy")
        elif fact["source_layer"] == "R8_human_checked_role" and fact["entry_mode"] == "international_legal":
            if external_origin(fact["origin_type"]):
                add(fact, "legal", stance="case_specific_legal_role_only")

    r10 = {row["source_record_ids"]: row for row in facts if row["source_layer"] == "R10_human_reviewed_relation"}
    jica_actor = actor_by_id["X011"]
    add(
        r10["R10R017"], "administrative", entry_actor_id="X011",
        entry_actor_name=jica_actor["canonical_name"], origin=jica_actor["origin_type"],
        local_object_name="Okinawa NGO Center (ONC)",
        stance="co-participation_only; no funding direction or base-policy stance",
    )
    add(r10["R10R019"], "service", stance="service sponsorship does not establish a base-policy stance")
    add(r10["R10R022"], "charity", stance="charitable donation does not establish a political stance")
    add(r10["R10R023"], "charity", stance="named grant only; no wider recipient network or political stance")
    for relation_id in ("R10R024", "R10R025", "R10R026", "R10R027"):
        add(r10[relation_id], "service", stance="membership/coordination only; no funding or political stance")
    add(
        r10["R10R035"], "public_diplomacy",
        local_object_name="unknown Okinawa Youth Council recipient/applicant field",
        stance="opportunity only; no award, recipient, or political alignment",
    )
    return rows


def build_hr021() -> list[dict[str, str]]:
    relations = {row["relation_observation_id"]: row for row in read_csv(R10_REL)}
    specs = [
        ("R10R001", "HR-018-01", "After HR-018 accepts or revises R10R001, should the resulting relation enter the R6 administrative comparison and R11 matrix, and with what no-public-amount boundary?", "R6 administrative comparison; R11 administrative entry matrix"),
        ("R10R004", "HR-018-04", "After HR-018 accepts or revises R10R004, should the resulting relation enter R11, and how must the 16.662m flow, 2.196m observation and 16.040m project cost remain separated in that downstream scope?", "R11 administrative/service entry"),
        ("R10R005", "HR-018-05", "After HR-018 accepts or revises R10R005, should the resulting relation enter R11, and should its downstream scope remain administrative support without movement-funding inference?", "R11 administrative entry"),
        ("R10R006;R10R007", "HR-018-06;HR-018-07", "After HR-018 accepts or revises R10R006/R10R007, which accepted period and role observations should enter R11, with what no-disclosed-contract-amount and no-base-movement-relation boundaries?", "R11 administrative/public-service entry"),
        ("R10R008", "HR-018-08", "After HR-018 accepts or revises R10R008, should the resulting relation enter the R6/R11 advocacy-administration boundary, and with what limits on payment, stable-alliance and government-endorsement claims?", "R6/R11 advocacy-administration boundary"),
        ("R10R018", "HR-018-17", "After HR-018 accepts or revises R10R018, should the resulting service-presence relation enter R11, and with what explicit prohibition on anti-base/pro-base stance inference?", "R11 service entry"),
        ("R10R020;R10R021", "HR-018-18;HR-018-19", "After HR-018 accepts or revises R10R020/R10R021, should either sponsor-tier observation enter R11, and with what no-amount, no-year and no-political-stance boundaries?", "R11 service sponsorship"),
        ("AEV0061;AEV0062;AEV0063;AEV0064", "", "Does independent factual directed-edge evidence exist for any of the four analytical pathway seeds? Cite that evidence before promotion; otherwise retain analytical_seed.", "R6/R7 pathway diagrams and R11 entry interpretation"),
    ]
    items: list[dict[str, str]] = []
    for index, (record_ids, hr018_ids, question, affected) in enumerate(specs, start=1):
        if record_ids.startswith("AEV"):
            selected = [row for row in read_csv(AEV) if row["record_id"] in split_refs(record_ids)]
            source_refs = unique_join([row["source_id"] for row in selected])
            locator = "formal AEV analytical_seed rows"
            boundary = "Retain as analytical_seed; no observed stable chain or causal arrow."
            dependency_type = "independent_evidence_review"
            prerequisite_status = "not_applicable"
            decision_options = "promote_with_independent_evidence|retain_analytical_seed|exclude_seed"
        else:
            selected = [relations[record_id] for record_id in split_refs(record_ids)]
            source_refs = unique_join(
                [
                    source_ref
                    for row in selected
                    for source_ref in split_refs(row["source_refs"])
                ]
            )
            locator = unique_join([row["source_locators"] for row in selected], " | ")
            boundary = unique_join([row["interpretation_limit"] for row in selected], " | ")
            dependency_type = "dependent_on_hr018"
            prerequisite_status = "pending_hr018_completion"
            decision_options = "include_after_hr018|revise_scope_after_hr018|exclude"
        items.append(
            {
                "review_item_id": f"HR021-{index:03d}",
                "relation_or_seed_ids": record_ids,
                "dependency_type": dependency_type,
                "prerequisite_review_item_ids": hr018_ids,
                "prerequisite_relation_ids": record_ids if hr018_ids else "",
                "prerequisite_status": prerequisite_status,
                "precise_question": question,
                "source_refs": source_refs,
                "source_locators": locator,
                "affected_outputs": affected,
                "default_boundary": boundary,
                "decision_options": decision_options,
                "review_decision": "",
                "human_reviewer": "",
                "review_date": "",
                "review_note": "",
            }
        )
    return items


def svg_page(title: str, subtitle: str, body: str, width: int, height: int) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">'
        '<rect width="100%" height="100%" fill="#FAF9F5"/>'
        '<style>text{font-family:"Noto Sans CJK SC","Microsoft YaHei",Arial,sans-serif;fill:#17231F}.title{font-size:30px;font-weight:700}.sub{font-size:14px;fill:#53615B}.head{font-size:16px;font-weight:700}.label{font-size:14px}.small{font-size:12px;fill:#53615B}.num{font-size:24px;font-weight:700}</style>'
        f'<text x="55" y="52" class="title">{html.escape(title)}</text>'
        f'<text x="55" y="80" class="sub">{html.escape(subtitle)}</text>'
        + body + "</svg>"
    )


def render_r6(rows: list[dict[str, str]]) -> str:
    body = ""
    colors = ["#D7E8E1", "#DDE5F0", "#F0DFC9", "#E8D8E8", "#DDE8CF", "#F2D9D2"]
    for index, row in enumerate(rows):
        y = 130 + index * 112
        body += f'<rect x="55" y="{y}" width="1390" height="92" rx="12" fill="{colors[index]}"/>'
        body += f'<text x="75" y="{y + 28}" class="head">{html.escape(row["pathway_family"])}</text>'
        body += f'<text x="75" y="{y + 55}" class="small">角色：{html.escape(row["observed_actor_roles"])}</text>'
        body += f'<text x="470" y="{y + 34}" class="label">入口：{html.escape(row["venue_or_entry_point"])}</text>'
        body += f'<text x="900" y="{y + 34}" class="label">目标：{html.escape(row["target"])}</text>'
        body += f'<text x="1325" y="{y + 49}" text-anchor="middle" class="num">{row["fact_count"]}</text>'
        body += f'<text x="1325" y="{y + 72}" text-anchor="middle" class="small">事实观察</text>'
    body += '<text x="55" y="820" class="small">六类入口并不构成一条统一国际网络；法律当事人、请求参与者、署名者、行政协作者与机会发布者角色不可互换。</text>'
    return svg_page("R6：目标路径比较", "比较法律、机构请求、国内／海外声援、行政协作与公共外交机会；数字不是影响力", body, 1500, 860)


def render_r7(rows: list[dict[str, str]]) -> str:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row["case_id"]].append(row)
    body = ""
    colors = ["#D7E8E1", "#DDE5F0", "#F0DFC9"]
    for case_index, case_id in enumerate(sorted(grouped)):
        stages = sorted(grouped[case_id], key=lambda row: int(row["stage_order"]))
        y = 145 + case_index * 235
        body += f'<text x="55" y="{y}" class="head">{html.escape(stages[0]["case_name"])}</text>'
        for stage_index, stage in enumerate(stages):
            x = 80 + stage_index * 465
            body += f'<rect x="{x}" y="{y + 25}" width="380" height="125" rx="13" fill="{colors[case_index]}"/>'
            body += f'<text x="{x + 18}" y="{y + 52}" class="small">{html.escape(stage["date_or_period"])} · stage {stage["stage_order"]}</text>'
            body += f'<text x="{x + 18}" y="{y + 78}" class="head">{html.escape(stage["venue_or_field"])}</text>'
            observation = html.escape(stage["observed_stage"])
            body += f'<foreignObject x="{x + 18}" y="{y + 88}" width="345" height="55"><div xmlns="http://www.w3.org/1999/xhtml" style="font:13px Microsoft YaHei;color:#33413b">{observation}</div></foreignObject>'
            if stage_index < len(stages) - 1:
                body += f'<line x1="{x + 390}" y1="{y + 88}" x2="{x + 450}" y2="{y + 88}" stroke="#7C8983" stroke-width="2" stroke-dasharray="6 5"/>'
                body += f'<text x="{x + 420}" y="{y + 75}" text-anchor="middle" class="small">顺序</text>'
    body += '<text x="55" y="855" class="small">虚线仅表示程序时间或同一事件中的展示顺序；不表示前一场域导致后一场域，也不证明政策效果。</text>'
    return svg_page("R7：三案例场域转移小倍图", "法律程序按时间排序；请求与声明按同一事件的角色／场域构成排序", body, 1500, 900)


def render_r11(rows: list[dict[str, str]]) -> str:
    domains = ["advocacy", "legal", "administrative", "service", "charity", "public_diplomacy"]
    objects = ["Henoko/Oura", "ONC/JICA", "USO/service", "spouse network", "unknown recipient"]
    counts: Counter[tuple[str, str]] = Counter()
    for row in rows:
        local = row["local_object"]
        obj = (
            "Henoko/Oura" if "Henoko/Oura" in local
            else "ONC/JICA" if "ONC" in local
            else "unknown recipient" if "unknown" in local
            else "spouse network" if row["entry_mode"] == "service_network_coordination"
            else "USO/service"
        )
        counts[(row["entry_domain"], obj)] += 1
    body = ""
    left, top, cell_w, cell_h = 300, 150, 220, 92
    for index, obj in enumerate(objects):
        body += f'<text x="{left + index * cell_w + cell_w/2}" y="125" text-anchor="middle" class="head">{html.escape(obj)}</text>'
    for r_index, domain in enumerate(domains):
        y = top + r_index * cell_h
        body += f'<text x="55" y="{y + 48}" class="head">{domain}</text>'
        for c_index, obj in enumerate(objects):
            value = counts[(domain, obj)]
            x = left + c_index * cell_w
            fill = "#17624F" if value else "#FFFFFF"
            color = "#FFFFFF" if value else "#A4ACA8"
            body += f'<rect x="{x + 10}" y="{y + 8}" width="{cell_w - 20}" height="70" rx="10" fill="{fill}" stroke="#D0D6D2"/>'
            body += f'<text x="{x + cell_w/2}" y="{y + 53}" text-anchor="middle" class="num" style="fill:{color}">{value}</text>'
    body += '<text x="55" y="735" class="small">倡议／法律只支持特定事件或案件角色；行政、服务、慈善与公共外交行均禁止外推基地政策立场。NOFO 不等于 award 或 recipient。</text>'
    return svg_page("R11：外来 actor 进入方式 × 本地对象", "单元格为由已人审正式事实派生的进入观察数；类别不可互换，也不是组织间联盟强度", body, 1500, 780)


def write_html(path: Path, title: str, svg: str, max_width: int) -> None:
    path.write_text(
        "<!doctype html><html lang='zh-CN'><head><meta charset='utf-8'>"
        f"<title>{html.escape(title)}</title><style>body{{margin:0;background:#eceae4}}"
        f"main{{max-width:{max_width}px;margin:24px auto;background:white;box-shadow:0 8px 28px #0002}}"
        "svg{display:block;width:100%;height:auto}</style></head><body><main>"
        + svg + "</main></body></html>",
        encoding="utf-8",
    )


def render_brief(facts, seeds, r6, r7, r11, hr021) -> str:
    r11_counts = Counter(row["entry_domain"] for row in r11)
    return f"""# R6 / R7 / R11 线上解释层 brief v1

日期：2026-07-13

## 共享底盘

- 正式 actor–event–venue–target/entry-mode 事实：**{len(facts)}** 条。
- `analytical_seed`：**{len(seeds)}** 条，未混入事实表。
- HR-021：**{len(hr021)}** 项下游纳入／seed 决策，决定栏均为空；前 7 项依赖 HR-018 完成关系事实复核。

底盘把 AEV 事件角色、R8 已人审法律角色及 R10 已人审／修订的行政—服务关系放在同一口径下，但不把它们写成同一种网络边。

## R6：不同目标路径

R6 比较 {len(r6)} 类入口，而不是复制单一边野古国际化链：

1. **国际法律**依赖具名 plaintiff、counsel、non-party 与 defendant 边界，产生程序标准和信息记录，但 2020 结果支持 DoD。
2. **国际机构请求**证明请求及事件参与者进入 MMC 入口；不证明 MMC 回应、政策改变或九个 E2 名称的稳定组织身份。
3. **国内／海外声援**是公开声明中的事件参与。日本国内署名与海外署名均不能写成持续联盟或地方代表权。
4. **行政协作**只确认公开活动协作，不自动产生资金方向或基地政治立场。
5. **公共外交机会**只确认 NOFO；recipient 与 award 均未知。

## R7：场域转移

三组小倍图覆盖国际法律、MMC 请求和跨国声明。法律案例可按程序时间排序；MMC 与声明案例只能按同一事件中的角色／入口构成排序。所有虚线都表示**展示顺序**，不是因果箭头，也不证明前一场域造成后一场域或带来政策效果。

## R11：外来 actor 的进入方式

R11 矩阵含 {len(r11)} 条由已人审正式事实派生的进入观察：倡议 {r11_counts['advocacy']}、法律 {r11_counts['legal']}、行政 {r11_counts['administrative']}、服务 {r11_counts['service']}、慈善 {r11_counts['charity']}、公共外交 {r11_counts['public_diplomacy']}。

- 倡议和法律角色只在特定 statement/request/case 中成立。
- 行政协作不等于资助方向或政府认同；共同列名不等于稳定联盟。
- 服务组织、企业 sponsor、军属慈善网络按观察到的服务／赞助／捐赠／成员功能编码，不推断反基地或亲基地立场。
- 公共外交 opportunity 不得写成 award、recipient 或政治结盟。

## 合并边界

- `26_actor_event_venue_target_entry_modes_v0.csv` 可作为解释图底盘；它仍是角色／事件／项目观察，不是稳定关系网。
- `analytical_seeds_v0.csv` 只能用于提出路径假说，不能作为事实边或因果链。
- R10 关系事实由 HR-018 复核；HR-021 前 7 项只在 HR-018 accept/revise 后决定是否及以何种边界进入 R6/R11，不重复判断关系事实。HR-018 未完成时不得填写 HR-021 决定。
- HR-021 第 8 项只审 analytical seed 是否具备独立事实边证据。
- 来源存在不等于结论充分；共同事件、共同签名、服务、慈善、行政和法律角色必须保持分层。
"""


def render_hr021(rows: list[dict[str, str]]) -> str:
    lines = [
        "# HR-021：R6/R7/R11 下游纳入与 analytical seed 复核包",
        "",
        "前 7 项均为 `dependent_on_hr018`：HR-018 负责关系事实判断，HR-021 只在对应 HR-018 项 accept/revise 后决定是否及以何种边界进入 R6/R11。前置复核未完成时不得填写决定。",
        "",
        "前 7 项决定选项为 include_after_hr018 / revise_scope_after_hr018 / exclude。第 8 项只审 analytical seed 是否有独立事实边证据。所有决定栏保持空白。",
        "",
    ]
    for row in rows:
        lines.extend(
            [
                f"## {row['review_item_id']} · {row['relation_or_seed_ids']}",
                "",
                f"- 依赖类型：{row['dependency_type']}",
                f"- HR-018 前置项：{row['prerequisite_review_item_ids'] or '不适用'}；状态：{row['prerequisite_status']}",
                f"- 问题：{row['precise_question']}",
                f"- 来源：{row['source_refs']}；定位：{row['source_locators']}",
                f"- 影响：{row['affected_outputs']}",
                f"- 默认边界：{row['default_boundary']}",
                f"- 决定选项：{row['decision_options']}",
                "",
            ]
        )
    return "\n".join(lines)


def validate(facts, seeds, r6, r7, r11, hr021) -> None:
    source_ids = {row["source_id"] for row in read_csv(SOURCES)}
    if len(facts) != 69:
        raise ValueError(f"expected 69 formal observations, found {len(facts)}")
    if len({row["observation_id"] for row in facts}) != len(facts):
        raise ValueError("duplicate fact observation ID")
    if any(row["review_status"] == "analytical_seed" for row in facts):
        raise ValueError("analytical seed leaked into facts")
    if len(seeds) != 4 or any(row["review_status"] != "analytical_seed" for row in seeds):
        raise ValueError("expected four separate analytical seeds")
    for row in facts + seeds:
        refs = split_refs(row["source_refs"])
        if not refs or not set(refs).issubset(source_ids):
            raise ValueError(f"invalid source refs on {row.get('observation_id', row.get('seed_id'))}")
    if len(r6) != 6 or any(int(row["fact_count"]) == 0 for row in r6):
        raise ValueError("R6 comparison must contain six evidenced pathways")
    if len(r7) != 9 or Counter(row["case_id"] for row in r7) != Counter({"R7C01": 3, "R7C02": 3, "R7C03": 3}):
        raise ValueError("R7 must contain three three-stage cases")
    if any("no causal inference" not in row["arrow_semantics"] for row in r7):
        raise ValueError("R7 causal-arrow boundary missing")
    required_domains = {"advocacy", "legal", "administrative", "service", "charity", "public_diplomacy"}
    if required_domains - {row["entry_domain"] for row in r11}:
        raise ValueError("R11 entry-domain coverage incomplete")
    if any(row["political_stance_boundary"] == "" for row in r11):
        raise ValueError("R11 political stance boundary missing")
    if len(hr021) != 8 or len({row["review_item_id"] for row in hr021}) != 8:
        raise ValueError("HR-021 must contain eight unique items")
    if any(row["review_decision"] or row["human_reviewer"] for row in hr021):
        raise ValueError("HR-021 must not be pre-decided")
    dependent = hr021[:7]
    seed_review = hr021[7]
    expected_options = "include_after_hr018|revise_scope_after_hr018|exclude"
    if any(row["dependency_type"] != "dependent_on_hr018" for row in dependent):
        raise ValueError("HR-021 items 1-7 must depend on HR-018")
    if any(row["prerequisite_status"] != "pending_hr018_completion" for row in dependent):
        raise ValueError("HR-021 items 1-7 must remain pending until HR-018 completion")
    if any(row["decision_options"] != expected_options for row in dependent):
        raise ValueError("HR-021 downstream decision options are invalid")
    hr018_rows = {row["review_item_id"]: row for row in read_csv(HR018)}
    for row in dependent:
        prerequisite_ids = split_refs(row["prerequisite_review_item_ids"])
        relation_ids = set(split_refs(row["prerequisite_relation_ids"]))
        if not prerequisite_ids or not set(prerequisite_ids).issubset(hr018_rows):
            raise ValueError(f"HR-021 prerequisite does not resolve: {row['review_item_id']}")
        resolved_relations = {
            hr018_rows[review_id]["relation_observation_id"] for review_id in prerequisite_ids
        }
        if resolved_relations != relation_ids:
            raise ValueError(f"HR-021/HR-018 relation mapping mismatch: {row['review_item_id']}")
        if row["prerequisite_status"] != "completed" and row["review_decision"]:
            raise ValueError(f"HR-021 decision filled before prerequisite: {row['review_item_id']}")
    if seed_review["dependency_type"] != "independent_evidence_review":
        raise ValueError("HR-021 item 8 must remain an independent-evidence seed review")
    if seed_review["prerequisite_review_item_ids"] or seed_review["prerequisite_relation_ids"]:
        raise ValueError("HR-021 item 8 must not depend on HR-018")
    formal_ids = {row["source_record_ids"] for row in facts}
    unresolved_r10 = {
        relation_id
        for row in hr021
        for relation_id in split_refs(row["relation_or_seed_ids"])
        if relation_id.startswith("R10")
    }
    if formal_ids & unresolved_r10:
        raise ValueError("unreviewed R10 relationship leaked into formal facts")


def main() -> None:
    facts = build_facts()
    seeds = build_seeds()
    r6 = build_r6(facts)
    r7 = build_r7(facts)
    r11 = build_r11(facts)
    hr021 = build_hr021()
    validate(facts, seeds, r6, r7, r11, hr021)

    write_csv(FORMAL_FACTS, FACT_FIELDS, facts)
    write_csv(SEEDS, list(seeds[0].keys()), seeds)
    write_csv(R6_TABLE, list(r6[0].keys()), r6)
    write_csv(R7_TABLE, list(r7[0].keys()), r7)
    write_csv(R11_TABLE, list(r11[0].keys()), r11)
    write_csv(HR021, list(hr021[0].keys()), hr021)

    r6_svg, r7_svg, r11_svg = render_r6(r6), render_r7(r7), render_r11(r11)
    R6_SVG.write_text(r6_svg, encoding="utf-8")
    R7_SVG.write_text(r7_svg, encoding="utf-8")
    R11_SVG.write_text(r11_svg, encoding="utf-8")
    write_html(R6_HTML, "R6 target pathways", r6_svg, 1500)
    write_html(R7_HTML, "R7 venue shifts", r7_svg, 1500)
    write_html(R11_HTML, "R11 external entry matrix", r11_svg, 1500)

    HR021_MD.write_text(render_hr021(hr021), encoding="utf-8")
    BRIEF.write_text(render_brief(facts, seeds, r6, r7, r11, hr021), encoding="utf-8")
    NOTE.write_text(
        f"""# Validation note

- Formal observations: {len(facts)}
- Analytical seeds: {len(seeds)}
- R6 pathway families: {len(r6)}
- R7 cases/stages: 3 / {len(r7)}
- R11 external-entry observations: {len(r11)}
- HR-021 unresolved items: {len(hr021)}; zero pre-decisions
- HR-021 dependency split: 7 `dependent_on_hr018`; 1 independent-evidence seed review

All source references resolve to the current main source log. Fact rows exclude
analytical seeds and unreviewed R10 relationships. Arrows in R7 are ordered
display only and do not encode causality. HR-021 items 1-7 do not re-review R10
relation facts; they remain blank until the mapped HR-018 items are completed.
""",
        encoding="utf-8",
    )

    # CSV roundtrip checks.
    if read_csv(FORMAL_FACTS) != facts:
        raise ValueError("formal facts CSV roundtrip mismatch")
    if read_csv(R11_TABLE) != r11:
        raise ValueError("R11 CSV roundtrip mismatch")
    print(
        f"R6/R7/R11 build OK: {len(facts)} facts; {len(seeds)} seeds; "
        f"6 R6 pathways; 3 R7 cases; {len(r11)} R11 rows; 8 HR-021 items."
    )


if __name__ == "__main__":
    main()
