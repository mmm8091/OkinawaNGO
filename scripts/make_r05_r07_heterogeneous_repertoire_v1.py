from __future__ import annotations

"""Build the R5/R7 heterogeneous action and venue comparison package.

The package only reuses existing human-reviewed or formally accepted facts.
It does not create event facts, mutate central tables, infer stable alliances,
or turn an observed sequence into a causal pathway.  Role/stage rows are kept
for audit, while figures count deduplicated event/case x action x venue units
so that cases with many parties do not appear more frequent by construction.
"""

import csv
import hashlib
import html
import textwrap
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Patch


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "interim"
META = ROOT / "data" / "metadata"
OUT = ROOT / "outputs" / "R05_R07_heterogeneous_repertoire_v1"

AEV = DATA / "09_actor_event_venue_edges_v0.csv"
R8_CASES = DATA / "17_legal_policy_procedure_cases_v0.csv"
R8_ROLES = DATA / "18_legal_policy_actor_roles_v0.csv"
R9_STAGES = ROOT / "outputs" / "R09_referendum_process_v0" / "process_stages_reviewed_all_v0.csv"
R9_ROLES = ROOT / "outputs" / "R09_referendum_process_v0" / "actor_process_roles_v0.csv"
R9_SOURCES = ROOT / "outputs" / "R09_referendum_process_v0" / "source_register_v0.csv"
R10_RELATIONS = DATA / "21_admin_collaboration_relations_v0.csv"
R10_PATHWAYS = DATA / "26_actor_event_venue_target_entry_modes_v0.csv"
R10_SOURCES = ROOT / "outputs" / "R10_administrative_collaboration_v0" / "source_crosswalk_v1.csv"
R7_SEQUENCES = ROOT / "outputs" / "R06_R07_R11_pathways_v1" / "r07_venue_shift_stages_v0.csv"
VENUES = META / "venue_taxonomy_v0.csv"
SOURCES = DATA / "05_source_log_initial_v0.csv"

DERIVED = DATA / "35_heterogeneous_event_repertoire_v1.csv"
UNITS = OUT / "repertoire_event_action_venue_units_v1.csv"
SEQUENCES = OUT / "cross_case_sequence_v1.csv"
SOURCE_CROSSWALK = OUT / "source_crosswalk_v1.csv"
INPUT_AUDIT = OUT / "input_layer_audit_v1.csv"
OVERLAP_AUDIT = OUT / "canonical_event_overlap_audit_v1.csv"
BRIEF = OUT / "R05_R07_heterogeneous_repertoire_brief_v1.md"
README = OUT / "README.md"
HR028_STATUS = OUT / "HR028_status_v0.md"
VALIDATION = OUT / "validation_report_v1.md"

FIG1_PNG = OUT / "fig1_repertoire_action_venue_matrix_v1.png"
FIG1_SVG = OUT / "fig1_repertoire_action_venue_matrix_v1.svg"
FIG1_HTML = OUT / "fig1_repertoire_action_venue_matrix_v1.html"
FIG2_PNG = OUT / "fig2_cross_case_venue_small_multiples_v1.png"
FIG2_SVG = OUT / "fig2_cross_case_venue_small_multiples_v1.svg"
FIG2_HTML = OUT / "fig2_cross_case_venue_small_multiples_v1.html"

HUMAN_STATUSES = {"human_checked", "human_revised"}

ACTION_ZH = {
    "joint_statement": "共同声明／署名",
    "institutional_request": "正式请求／请愿",
    "legal_action": "司法／诉讼行动",
    "referendum_process": "公投动员／参与",
    "opinion_ad": "意见广告",
    "public_rally": "公共集会／动员",
    "administrative_comment": "环评／行政意见",
    "signature_direct_request": "签名／直接请求",
    "council_or_ordinance_gate": "议会／条例门槛",
    "referendum_vote_result": "投票／结果程序",
    "executive_interpretation": "行政解释／后续决定",
    "organizational_transition": "组织阶段转换",
    "administrative_collaboration": "行政／公共活动协作",
    "service_charity_support": "服务／慈善支持",
    "service_network_membership": "服务网络成员关系",
    "public_diplomacy_opportunity": "公共外交机会公告",
}

ACTION_COLORS = {
    "joint_statement": "#B14E55",
    "institutional_request": "#C87539",
    "legal_action": "#4D648D",
    "referendum_process": "#7D6B3D",
    "opinion_ad": "#9A6B88",
    "public_rally": "#B95F4D",
    "administrative_comment": "#497E76",
    "signature_direct_request": "#8A7340",
    "council_or_ordinance_gate": "#70654E",
    "referendum_vote_result": "#A08749",
    "executive_interpretation": "#746A60",
    "organizational_transition": "#8B8F91",
    "administrative_collaboration": "#3E7C70",
    "service_charity_support": "#A6783B",
    "service_network_membership": "#8C7454",
    "public_diplomacy_opportunity": "#78619B",
}

VENUE_GROUP_ZH = {
    "field_site": "现场／争议地点",
    "civic_public_communication": "公民公开传播",
    "administrative_advocacy": "行政请求渠道",
    "international_institution": "国际／美国机构",
    "legal_judicial": "法院／司法",
    "electoral_referendum": "公投／选举程序",
    "media_public_opinion": "媒体／公共意见",
    "administrative_government": "政府行政",
    "legal_administrative_procedure": "法律／行政程序",
    "transnational_civic": "跨国公民倡议",
    "civic_policy_forum": "公共政策论坛",
    "service_charity": "服务／慈善场域",
    "public_diplomacy_program": "公共外交项目",
}

VENUE_GROUP_COLORS = {
    "field_site": "#7D9B88",
    "civic_public_communication": "#B85A60",
    "administrative_advocacy": "#D18445",
    "international_institution": "#6F64A2",
    "legal_judicial": "#4A648E",
    "electoral_referendum": "#9A803B",
    "media_public_opinion": "#9B6D8D",
    "administrative_government": "#4E8478",
    "legal_administrative_procedure": "#5E8B82",
    "transnational_civic": "#76659B",
    "civic_policy_forum": "#637D76",
    "service_charity": "#A57A42",
    "public_diplomacy_program": "#8068A0",
}

AEV_ACTION_MAP = {
    "co_signing": "joint_statement",
    "request_letter": "institutional_request",
    "litigation": "legal_action",
    "referendum": "referendum_process",
    "opinion_ad": "opinion_ad",
    "public_rally": "public_rally",
}

R9_STAGE_ACTION_MAP = {
    "initiation": "signature_direct_request",
    "signature_request": "signature_direct_request",
    "signature_collection": "signature_direct_request",
    "direct_request": "signature_direct_request",
    "council_ordinance": "council_or_ordinance_gate",
    "assembly_ordinance": "council_or_ordinance_gate",
    "ordinance_amendment": "council_or_ordinance_gate",
    "council_rejection": "council_or_ordinance_gate",
    "second_council_rejection": "council_or_ordinance_gate",
    "ordinance_framework_change": "council_or_ordinance_gate",
    "vote": "referendum_vote_result",
    "result": "referendum_vote_result",
    "result_notification": "referendum_vote_result",
    "post_result_executive": "executive_interpretation",
    "judicial_filing": "legal_action",
    "district_court_result": "legal_action",
    "second_chain_filing": "legal_action",
    "first_chain_appeal": "legal_action",
    "status_confirmation_district_result": "legal_action",
    "status_confirmation_high_court_result": "legal_action",
    "supreme_court_finalization": "legal_action",
    "opinion_ad_mobilization": "opinion_ad",
    "campaign_mobilization": "public_rally",
    "organizational_close": "organizational_transition",
}

R10_ENTRY_ACTION_MAP = {
    "administrative_event_collaboration": "administrative_collaboration",
    "service_sponsorship": "service_charity_support",
    "charitable_donation": "service_charity_support",
    "charitable_grant": "service_charity_support",
    "service_network_coordination": "service_network_membership",
    "public_diplomacy_opportunity": "public_diplomacy_opportunity",
}

CANONICAL_EVENT_MAP = {
    "EV2003_DUGONG_LAWSUIT": "R8C01",
    "EV1997_NAGO_REFERENDUM": "R9C_NAGO_1997",
    "EV2015_YONAGUNI_REFERENDUM": "R9C_YONAGUNI_2015",
    "EV2019_PREF_REFERENDUM": "R9C_PREF_2019",
    "EV_ISHIGAKI_REFERENDUM": "R9C_ISHIGAKI_2018_2024",
}

AEV_FALLBACK_PLACE = {
    "EV2010_WWF_67": "Henoko; Oura Bay",
    "EV2015_NACSJ_31": "Henoko; Oura Bay",
    "EV2020_OEJP_MMC_71": "Henoko; Oura Bay",
    "EV2003_DUGONG_LAWSUIT": "Henoko; Oura Bay; U.S. federal court",
    "EV2019_PREF_REFERENDUM": "Okinawa Prefecture",
    "EV1997_NAGO_REFERENDUM": "Nago",
    "EV_ISHIGAKI_REFERENDUM": "Ishigaki",
    "EV2015_YONAGUNI_REFERENDUM": "Yonaguni",
    "EV2012_YONAGUNI_OPINION_AD": "Yaeyama; Yonaguni",
    "EV2024_WOMEN_ANTI_VIOLENCE_RALLY": "Okinawa Prefecture",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8")


def normalize_generated_svg(path: Path) -> None:
    """Remove Matplotlib path-line trailing spaces deterministically."""
    lines = path.read_text(encoding="utf-8").splitlines()
    path.write_text(
        "\n".join(line.rstrip(" \t") for line in lines) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def split_refs(value: str) -> list[str]:
    return [item.strip() for item in value.split(";") if item.strip()]


def configure_fonts() -> None:
    candidates = [
        "Microsoft YaHei", "Yu Gothic", "Meiryo", "Noto Sans CJK SC",
        "Noto Sans CJK JP", "SimHei", "Arial Unicode MS", "DejaVu Sans",
    ]
    available = {font.name for font in font_manager.fontManager.ttflist}
    for name in candidates:
        if name in available:
            plt.rcParams["font.family"] = name
            break
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["figure.facecolor"] = "white"
    plt.rcParams["svg.hashsalt"] = "r05-r07-heterogeneous-repertoire-v1"


def action_scope(action: str) -> str:
    if action in {
        "administrative_collaboration", "service_charity_support",
        "service_network_membership", "public_diplomacy_opportunity",
    }:
        return "function_or_resource_relation"
    return "event_or_process_action"


def r9_action(stage_type: str) -> str:
    if stage_type not in R9_STAGE_ACTION_MAP:
        raise ValueError(f"unmapped R9 stage type: {stage_type}")
    return R9_STAGE_ACTION_MAP[stage_type]


def r9_venue(
    stage: dict[str, str],
    venue_by_id: dict[str, dict[str, str]],
) -> tuple[str, str, str]:
    stage_type = stage["stage_type"]
    if "judicial" in stage_type or "court" in stage_type or stage_type in {
        "second_chain_filing", "first_chain_appeal",
        "status_confirmation_district_result", "status_confirmation_high_court_result",
        "supreme_court_finalization",
    }:
        venue_id = "V006"
    elif stage_type == "opinion_ad_mobilization":
        venue_id = "V009"
    elif stage_type == "campaign_mobilization":
        venue_id = "V015"
    elif stage["case_id"] == "R9C_PREF_2019":
        venue_id = "V007"
    else:
        venue_id = "V008"
    venue = venue_by_id[venue_id]
    return venue_id, venue["venue_label"], venue["venue_group"]


def canonical_event_id(event_id: str) -> str:
    return CANONICAL_EVENT_MAP.get(event_id, event_id)


def unit_id(canonical_id: str, action: str, venue_group: str) -> str:
    safe = f"{canonical_id}|{action}|{venue_group}"
    digest = hashlib.sha1(safe.encode("utf-8")).hexdigest()[:10].upper()
    return f"RU_{digest}"


def base_row(
    *,
    observation_id: str,
    source_module: str,
    source_record_id: str,
    observation_scope: str,
    canonical_id: str,
    name: str,
    date_start: str,
    date_end: str,
    stage_order: str,
    entity_id: str,
    entity_name: str,
    entity_kind: str,
    role: str,
    action: str,
    action_detail: str,
    venue_id: str,
    venue_label: str,
    venue_group: str,
    place: str,
    target_type: str,
    target_name: str,
    evidence_level: str,
    source_refs: str,
    review_status: str,
    interpretation_limit: str,
) -> dict[str, object]:
    return {
        "observation_id": observation_id,
        "source_module": source_module,
        "source_record_id": source_record_id,
        "observation_scope": observation_scope,
        "canonical_case_or_event_id": canonical_id,
        "event_or_case_name": name,
        "date_start": date_start,
        "date_end": date_end,
        "stage_order": stage_order,
        "actor_or_entity_id": entity_id,
        "actor_or_entity_name": entity_name,
        "entity_kind": entity_kind,
        "role": role,
        "action_family": action,
        "action_family_zh": ACTION_ZH[action],
        "action_scope": action_scope(action),
        "action_detail": action_detail,
        "venue_id": venue_id,
        "venue_label": venue_label,
        "venue_group": venue_group,
        "venue_group_zh": VENUE_GROUP_ZH[venue_group],
        "place": place,
        "target_type": target_type,
        "target_id_or_name": target_name,
        "repertoire_unit_id": unit_id(canonical_id, action, venue_group),
        "counting_unit_rule": "unique canonical_case_or_event_id x action_family x venue_group",
        "evidence_level": evidence_level,
        "source_refs": source_refs,
        "review_status": review_status,
        "review_layer": "human_reviewed" if review_status in HUMAN_STATUSES else "formal_accepted",
        "new_fact_status": "existing_formal_fact_only",
        "sequence_limit": "ordered display, when used, is chronology/composition only and does not establish causal effect",
        "interpretation_limit": interpretation_limit,
    }


def build_rows(
    aev: list[dict[str, str]],
    r8_cases: list[dict[str, str]],
    r8_roles: list[dict[str, str]],
    r9_stages: list[dict[str, str]],
    r9_roles: list[dict[str, str]],
    r10_pathways: list[dict[str, str]],
    venue_by_id: dict[str, dict[str, str]],
) -> list[dict[str, object]]:
    output: list[dict[str, object]] = []
    pathway_by_source: dict[str, dict[str, str]] = {}
    for row in r10_pathways:
        if row["source_layer"] == "formal_AEV":
            for ref in split_refs(row["source_record_ids"]):
                pathway_by_source[ref] = row

    # 63 human-checked AEV facts after HR-011/013 normalization. Analytical seeds are excluded.
    for row in aev:
        if row["reviewer_status"] != "human_checked":
            continue
        action = AEV_ACTION_MAP[row["action_type"]]
        venue = venue_by_id[row["venue_id"]]
        cross = pathway_by_source.get(row["record_id"], {})
        place = cross.get("place", AEV_FALLBACK_PLACE.get(row["event_id"], ""))
        output.append(base_row(
            observation_id=f"HET_{row['record_id']}",
            source_module="AEV_HR015",
            source_record_id=row["record_id"],
            observation_scope="actor_event_role",
            canonical_id=canonical_event_id(row["event_id"]),
            name=row["event_name"],
            date_start=row["event_year"],
            date_end="",
            stage_order="",
            entity_id=row["actor_or_counterpart_id"] or row["legacy_candidate_id"],
            entity_name=row["actor_or_counterpart_name"],
            entity_kind=row["entity_type"],
            role=row["role"],
            action=action,
            action_detail=row["pathway_stage"],
            venue_id=row["venue_id"],
            venue_label=venue["venue_label"],
            venue_group=venue["venue_group"],
            place=place,
            target_type=row["target_type"],
            target_name=row["target_id_or_name"],
            evidence_level=row["evidence_level"],
            source_refs=row["source_id"],
            review_status=row["reviewer_status"],
            interpretation_limit=row["interpretation_limit"],
        ))

    cases_by_id = {row["case_id"]: row for row in r8_cases}
    for role in r8_roles:
        if role["review_status"] != "human_checked" or role["human_decision"] != "accept":
            continue
        case = cases_by_id[role["case_id"]]
        action = "administrative_comment" if role["case_id"] == "R8C02" else "legal_action"
        venue_id = "V005" if role["case_id"] == "R8C01" else "V012" if role["case_id"] == "R8C02" else "V006"
        venue = venue_by_id[venue_id]
        entity_id = role["actor_id"] or role["provisional_entity_id"]
        output.append(base_row(
            observation_id=f"HET_{role['role_id']}",
            source_module="R8_HR014",
            source_record_id=role["role_id"],
            observation_scope="case_specific_role",
            canonical_id=role["case_id"],
            name=case["case_name"],
            date_start=case["start_date"],
            date_end=case["end_or_decision_date"],
            stage_order="",
            entity_id=entity_id,
            entity_name=role["actor_name"],
            entity_kind=role["entity_kind"],
            role=role["role"],
            action=action,
            action_detail=role["role_evidence_summary"],
            venue_id=venue_id,
            venue_label=venue["venue_label"],
            venue_group=venue["venue_group"],
            place=case["place"],
            target_type="institution_or_recipient",
            target_name=role["target_or_recipient"] or case["target_actor_or_institution"],
            evidence_level=role["evidence_level"],
            source_refs=role["source_refs"],
            review_status=role["review_status"],
            interpretation_limit=role["interpretation_limit"],
        ))

    all_stages_by_id = {row["stage_id"]: row for row in r9_stages}
    accepted_stages = [row for row in r9_stages if row["review_status"] == "accepted"]
    for stage in accepted_stages:
        action = r9_action(stage["stage_type"])
        venue_id, venue_label, venue_group = r9_venue(stage, venue_by_id)
        output.append(base_row(
            observation_id=f"HET_{stage['stage_id']}",
            source_module="R9_FORMAL_STAGE",
            source_record_id=stage["stage_id"],
            observation_scope="institutional_process_stage",
            canonical_id=stage["case_id"],
            name=stage["case_name"],
            date_start=stage["date_start"],
            date_end=stage["date_end"],
            stage_order=stage["stage_order"],
            entity_id="",
            entity_name=stage["decision_body_or_forum"],
            entity_kind="institutional_forum_or_process",
            role=f"process_stage:{stage['stage_type']}",
            action=action,
            action_detail=stage["process_action"],
            venue_id=venue_id,
            venue_label=venue_label,
            venue_group=venue_group,
            place=stage["place"],
            target_type="decision_body_or_forum",
            target_name=stage["decision_body_or_forum"],
            evidence_level=stage["evidence_level"],
            source_refs=stage["source_refs"],
            review_status=stage["review_status"],
            interpretation_limit=stage["interpretation_limit"],
        ))

    for role in r9_roles:
        if role["review_status"] != "accepted":
            continue
        stage = all_stages_by_id[role["stage_id"]]
        action = r9_action(stage["stage_type"])
        venue_id, venue_label, venue_group = r9_venue(stage, venue_by_id)
        output.append(base_row(
            observation_id=f"HET_{role['role_id']}",
            source_module="R9_FORMAL_ROLE",
            source_record_id=role["role_id"],
            observation_scope="institutional_process_role",
            canonical_id=role["case_id"],
            name=stage["case_name"],
            date_start=stage["date_start"],
            date_end=stage["date_end"],
            stage_order=stage["stage_order"],
            entity_id=role["actor_id"] or role["entity_id"],
            entity_name=role["entity_name"],
            entity_kind=role["entity_kind"],
            role=role["role_type"],
            action=action,
            action_detail=role["role_scope"],
            venue_id=venue_id,
            venue_label=venue_label,
            venue_group=venue_group,
            place=stage["place"],
            target_type="process_stage",
            target_name=stage["short_label"],
            evidence_level=role["evidence_level"],
            source_refs=role["source_refs"],
            review_status=role["review_status"],
            interpretation_limit=role["interpretation_limit"],
        ))

    for row in r10_pathways:
        if row["source_layer"] != "R10_human_reviewed_relation":
            continue
        action = R10_ENTRY_ACTION_MAP[row["entry_mode"]]
        if action == "administrative_collaboration":
            venue_id, venue_label, venue_group = "V015", "public_policy_meeting_or_forum", "civic_policy_forum"
        elif action in {"service_charity_support", "service_network_membership"}:
            venue_id, venue_label, venue_group = "V016", "service_charity_program_site", "service_charity"
        else:
            venue_id, venue_label, venue_group = "VX_PD", "public_diplomacy_program", "public_diplomacy_program"
        output.append(base_row(
            observation_id=f"HET_{row['source_record_ids']}",
            source_module="R10_HUMAN_RELATION",
            source_record_id=row["source_record_ids"],
            observation_scope="function_or_resource_relation",
            canonical_id=row["event_or_project_id"],
            name=row["event_or_project_name"],
            date_start=row["date_or_period"],
            date_end="",
            stage_order="",
            entity_id=row["actor_id"],
            entity_name=row["actor_name"],
            entity_kind=row["actor_category"],
            role=row["role"],
            action=action,
            action_detail=row["entry_mode"],
            venue_id=venue_id,
            venue_label=venue_label,
            venue_group=venue_group,
            place=row["place"],
            target_type=row["target_type"],
            target_name=row["target_id_or_name"],
            evidence_level=row["evidence_level"],
            source_refs=row["source_refs"],
            review_status=row["review_status"],
            interpretation_limit=row["interpretation_limit"],
        ))
    return output


def build_units(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[str(row["repertoire_unit_id"])].append(row)
    output: list[dict[str, object]] = []
    for unit, items in sorted(grouped.items()):
        first = items[0]
        entity_ids = sorted({str(r["actor_or_entity_id"]) for r in items if r["actor_or_entity_id"]})
        source_refs = sorted({ref for r in items for ref in split_refs(str(r["source_refs"]))})
        modules = sorted({str(r["source_module"]) for r in items})
        output.append({
            "repertoire_unit_id": unit,
            "canonical_case_or_event_id": first["canonical_case_or_event_id"],
            "event_or_case_name": first["event_or_case_name"],
            "action_family": first["action_family"],
            "action_family_zh": first["action_family_zh"],
            "action_scope": first["action_scope"],
            "venue_group": first["venue_group"],
            "venue_group_zh": first["venue_group_zh"],
            "place": ";".join(sorted({str(r["place"]) for r in items if r["place"]})),
            "observation_row_count": len(items),
            "distinct_entity_count": len(entity_ids),
            "entity_ids": ";".join(entity_ids),
            "source_modules": ";".join(modules),
            "source_refs": ";".join(source_refs),
            "review_layers": ";".join(sorted({str(r["review_layer"]) for r in items})),
            "counting_status": "one_unit_for_figure",
            "interpretation_limit": "One deduplicated event/case-action-venue unit; not an estimate of real-world frequency, scale, alliance, or causal effect.",
        })
    return output


def build_overlap_audit(rows: list[dict[str, object]], units: list[dict[str, object]]) -> list[dict[str, object]]:
    by_case: dict[str, list[dict[str, object]]] = defaultdict(list)
    unit_by_case: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        by_case[str(row["canonical_case_or_event_id"])].append(row)
    for unit in units:
        unit_by_case[str(unit["canonical_case_or_event_id"])].append(unit)
    output: list[dict[str, object]] = []
    for case_id, items in sorted(by_case.items()):
        modules = sorted({str(r["source_module"]) for r in items})
        output.append({
            "canonical_case_or_event_id": case_id,
            "event_or_case_names": ";".join(sorted({str(r["event_or_case_name"]) for r in items})),
            "source_modules": ";".join(modules),
            "formal_observation_rows": len(items),
            "deduplicated_repertoire_units": len(unit_by_case[case_id]),
            "action_families": ";".join(sorted({str(r["action_family"]) for r in items})),
            "venue_groups": ";".join(sorted({str(r["venue_group"]) for r in items})),
            "parallel_formal_layers": "yes" if len(modules) > 1 else "no",
            "counting_rule": "parallel role/stage layers remain auditable but collapse inside the same case-action-venue unit",
            "interpretation_limit": "Parallel layers do not mean repeated independent events or a stable alliance.",
        })
    return output


def build_input_audit(
    aev: list[dict[str, str]],
    r8_roles: list[dict[str, str]],
    r9_stages: list[dict[str, str]],
    r9_roles: list[dict[str, str]],
    r10_relations: list[dict[str, str]],
) -> list[dict[str, object]]:
    specs = [
        ("AEV_HR015", len(aev), sum(r["reviewer_status"] == "human_checked" for r in aev), "reviewer_status=human_checked", "4 analytical_seed rows excluded"),
        ("R8_HR014", len(r8_roles), sum(r["review_status"] == "human_checked" and r["human_decision"] == "accept" for r in r8_roles), "review_status=human_checked and decision=accept", "all 27 accepted roles included"),
        ("R9_FORMAL_STAGE", len(r9_stages), sum(r["review_status"] == "accepted" for r in r9_stages), "review_status=accepted", "9 needs_human_review stages excluded"),
        ("R9_FORMAL_ROLE", len(r9_roles), sum(r["review_status"] == "accepted" for r in r9_roles), "review_status=accepted", "all 25 formal roles included; three point to stages whose result text remains pending"),
        ("R10_HUMAN_RELATION", len(r10_relations), sum(r["review_status"] in HUMAN_STATUSES for r in r10_relations), "review_status=human_checked or human_revised", "26 pending R10 relations excluded"),
    ]
    return [
        {
            "source_module": module,
            "input_row_count": total,
            "included_formal_row_count": included,
            "excluded_row_count": total - included,
            "inclusion_rule": rule,
            "boundary_note": note,
        }
        for module, total, included, rule, note in specs
    ]


def build_sequences(
    r8_cases: list[dict[str, str]],
    r9_stages: list[dict[str, str]],
    r10_pathways: list[dict[str, str]],
) -> list[dict[str, object]]:
    output: list[dict[str, object]] = []
    r7_field_zh = {
        "Henoko/Oura Bay": "边野古／大浦湾",
        "Henoko/Oura Bay issue": "边野古／大浦湾议题",
        "civil-society request": "市民社会请求",
        "U.S. Marine Mammal Commission": "美国海洋哺乳动物委员会",
        "U.S. District Court": "美国联邦地区法院",
        "Ninth Circuit": "第九巡回上诉法院",
        "NACSJ/Peace Boat statement venue": "NACSJ／Peace Boat 声明场域",
        "domestic and overseas signatory field": "日本国内与海外署名场",
    }
    r7_stage_zh = {
        "Dugong/base project translated into an NHPA Section 402 claim": "儒艮／基地工程争议被转译为 NHPA 第402条程序请求",
        "Named plaintiffs and counsel entered a U.S. federal legal venue": "具名原告与律师进入美国联邦司法场域",
        "Opinion articulated a Section 402 standard and affirmed judgment for DoD": "判决阐明第402条审查标准，并维持 DoD 胜诉",
        "Dugong and construction issue stated in the request context": "请求文本提出儒艮与施工影响议题",
        "OEJP, JELF and event participants appear on the request": "OEJP、JELF 与事件参与者进入请求书",
        "Request was directed to a U.S. federal institution": "请求提交至美国联邦机构",
        "Local policy/ecology object anchors the statement": "地方工程与生态对象构成声明议题锚点",
        "Statement hosts organized a public advocacy venue": "主办方形成公开倡议场域",
        "Public participation spans local, Japan-based and overseas organizations": "公开参与跨越本地、日本国内与海外组织",
    }
    venue_group_for_field = {
        "Henoko/Oura Bay": "field_site",
        "Henoko/Oura Bay issue": "field_site",
        "civil-society request": "civic_public_communication",
        "U.S. Marine Mammal Commission": "international_institution",
        "U.S. District Court": "legal_judicial",
        "Ninth Circuit": "legal_judicial",
        "NACSJ/Peace Boat statement venue": "civic_public_communication",
        "domestic and overseas signatory field": "transnational_civic",
    }
    for row in read_csv(R7_SEQUENCES):
        venue_group = venue_group_for_field[row["venue_or_field"]]
        output.append({
            "case_id": row["case_id"],
            "case_name": row["case_name"],
            "stage_order": row["stage_order"],
            "date_or_period": row["date_or_period"],
            "venue_or_field": r7_field_zh[row["venue_or_field"]],
            "venue_group": venue_group,
            "venue_group_zh": VENUE_GROUP_ZH[venue_group],
            "observed_stage": r7_stage_zh[row["observed_stage"]],
            "source_record_ids": row["fact_observation_ids"],
            "source_refs": row["source_refs"],
            "sequence_basis": row["sequence_basis"],
            "arrow_semantics": row["arrow_semantics"],
            "new_fact_status": "existing_analytical_sequence_from_formal_facts",
        })

    cases = {row["case_id"]: row for row in r8_cases}
    kadena = cases["R8C03"]
    kadena_stages = [
        (1, kadena["start_date"][:4], "嘉手纳受影响地区", "field_site", "A052／受影响居民以原告团层进入案件"),
        (2, "2011–2019", "那霸地裁／福冈高裁那霸支部", "legal_judicial", "噪音请求进入日本地裁／高裁程序"),
        (3, kadena["end_or_decision_date"][:4], "司法处分", "legal_judicial", "维持既往噪音赔偿，同时驳回差止与将来损害请求"),
    ]
    for order, period, field, group, observed in kadena_stages:
        output.append({
            "case_id": "R7C04", "case_name": "Kadena third noise litigation",
            "stage_order": order, "date_or_period": period, "venue_or_field": field,
            "venue_group": group, "venue_group_zh": VENUE_GROUP_ZH[group],
            "observed_stage": observed, "source_record_ids": "R8C03",
            "source_refs": kadena["primary_source_refs"],
            "sequence_basis": "case chronology and human-checked outcome summary",
            "arrow_semantics": "ordered observation only; no causal inference",
            "new_fact_status": "analytical_arrangement_of_existing_human_checked_case",
        })

    accepted_ishigaki = {
        row["stage_id"]: row for row in r9_stages
        if row["case_id"] == "R9C_ISHIGAKI_2018_2024" and row["review_status"] == "accepted"
    }
    for order, stage_id, label, group in [
        (1, "R9ST021", "签名／直接请求入口", "electoral_referendum"),
        (2, "R9ST023", "市议会条例门槛", "electoral_referendum"),
        (3, "R9ST026", "那霸地裁程序处分", "legal_judicial"),
    ]:
        stage = accepted_ishigaki[stage_id]
        output.append({
            "case_id": "R7C05", "case_name": "Ishigaki referendum request and judicial turn",
            "stage_order": order, "date_or_period": stage["date_start"] or stage["date_end"],
            "venue_or_field": label, "venue_group": group,
            "venue_group_zh": VENUE_GROUP_ZH[group],
            "observed_stage": f"{stage['process_action']}；{stage['outcome']}",
            "source_record_ids": stage_id, "source_refs": stage["source_refs"],
            "sequence_basis": "accepted R9 process chronology",
            "arrow_semantics": "ordered observation only; no causal inference",
            "new_fact_status": "analytical_arrangement_of_existing_formal_stages",
        })

    r10 = next(row for row in r10_pathways if row["source_record_ids"] == "R10R022")
    service_stages = [
        (1, "2025", "OESC 捐赠记录", "service_charity", "既有人审记录确认一笔直接慈善捐赠"),
        (2, "2025", "USO Okinawa 服务场域", "service_charity", "USO Okinawa 为具名 recipient；不推定政治效果"),
    ]
    for order, period, field, group, observed in service_stages:
        output.append({
            "case_id": "R7C06", "case_name": "OESC to USO charitable donation",
            "stage_order": order, "date_or_period": period, "venue_or_field": field,
            "venue_group": group, "venue_group_zh": VENUE_GROUP_ZH[group],
            "observed_stage": observed, "source_record_ids": "R10R022",
            "source_refs": r10["source_refs"],
            "sequence_basis": "two-sided display of one human-reviewed relation",
            "arrow_semantics": "relation direction only; no causal or political inference",
            "new_fact_status": "analytical_arrangement_of_existing_human_checked_relation",
        })
    return output


def build_source_crosswalk(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    main_sources = {row["source_id"]: row for row in read_csv(SOURCES)}
    r9_sources = {row["source_id"]: row for row in read_csv(R9_SOURCES)}
    r10_sources = {row["source_ref"]: row for row in read_csv(R10_SOURCES)}
    output: list[dict[str, object]] = []
    for row in rows:
        for ref in split_refs(str(row["source_refs"])):
            main = main_sources.get(ref, {})
            r9 = r9_sources.get(ref, {})
            r10 = r10_sources.get(ref, {})
            existing_main = ref if main else r9.get("existing_source_id", "")
            output.append({
                "observation_id": row["observation_id"],
                "source_module": row["source_module"],
                "source_record_id": row["source_record_id"],
                "reference_id": ref,
                "reference_kind": "main_source" if main else "r9_module_source" if r9 else "r10_module_source" if r10 else "unresolved_reference",
                "existing_main_source_id": existing_main,
                "title": main.get("title", r9.get("title", r10.get("title", ""))),
                "url": main.get("url", r9.get("url", r10.get("url", ""))),
                "evidence_level": main.get("evidence_level", r9.get("evidence_level", row["evidence_level"])),
                "metadata_review_status": main.get("review_status", r9.get("review_status", r10.get("status", "module_reference"))),
                "relation_or_claim_approved": "no",
                "approval_provenance_scope": "reused_existing_formal_observation__no_new_approval",
                "interpretation_limit": "Provenance crosswalk only; source presence does not create a new event, alliance, causal claim, funding relation, or political stance.",
            })
    return output


def save_figure(fig: plt.Figure, png: Path, svg: Path) -> None:
    fig.savefig(png, dpi=180, bbox_inches="tight", facecolor="white", metadata={"Software": "make_r05_r07_heterogeneous_repertoire_v1.py"})
    fig.savefig(svg, bbox_inches="tight", facecolor="white", metadata={"Date": None, "Creator": "make_r05_r07_heterogeneous_repertoire_v1.py"})
    plt.close(fig)


def html_wrapper(svg_name: str, title: str) -> str:
    return f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)}</title><style>body{{margin:0;background:#eceae4}}main{{max-width:1800px;margin:24px auto;background:white;box-shadow:0 8px 28px #0002}}img{{display:block;width:100%;height:auto}}</style></head><body><main><img src="{html.escape(svg_name)}" alt="{html.escape(title)}"></main></body></html>"""


def plot_repertoire(rows: list[dict[str, object]], units: list[dict[str, object]]) -> None:
    unit_counts = Counter(str(row["action_family"]) for row in units)
    observation_counts = Counter(str(row["action_family"]) for row in rows)
    actions = sorted(unit_counts, key=lambda a: (action_scope(a), -unit_counts[a], ACTION_ZH[a]))
    venues = sorted(
        {str(row["venue_group"]) for row in units},
        key=lambda v: (-sum(str(r["venue_group"]) == v for r in units), VENUE_GROUP_ZH[v]),
    )
    matrix = np.zeros((len(actions), len(venues)), dtype=int)
    ai = {action: index for index, action in enumerate(actions)}
    vi = {venue: index for index, venue in enumerate(venues)}
    for row in units:
        matrix[ai[str(row["action_family"])], vi[str(row["venue_group"])]] += 1

    fig, axes = plt.subplots(1, 2, figsize=(20, 11.5), gridspec_kw={"width_ratios": [1.55, 0.85]})
    ax = axes[0]
    image = ax.imshow(matrix, cmap="YlGnBu", aspect="auto", vmin=0, vmax=max(1, int(matrix.max())))
    for y in range(len(actions)):
        for x in range(len(venues)):
            if matrix[y, x]:
                ax.text(x, y, str(matrix[y, x]), ha="center", va="center", fontsize=9.5, fontweight="bold", color="white" if matrix[y, x] > matrix.max() * 0.55 else "#263630")
    labels = [ACTION_ZH[a] + ("〔关系层〕" if action_scope(a) == "function_or_resource_relation" else "") for a in actions]
    ax.set_yticks(range(len(actions)), labels, fontsize=9.3)
    ax.set_xticks(range(len(venues)), [VENUE_GROUP_ZH[v] for v in venues], rotation=45, ha="right", fontsize=9)
    ax.set_title("去重 repertoire 单元：行动 × 场域", loc="left", fontsize=15, fontweight="bold")
    ax.set_xlabel("每格 = unique case/event × action × venue；不是参与者数")
    ax.tick_params(length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)
    cbar = fig.colorbar(image, ax=ax, fraction=0.025, pad=0.02)
    cbar.set_label("去重单元数")

    ax = axes[1]
    y = np.arange(len(actions))
    unit_values = np.array([unit_counts[a] for a in actions])
    obs_values = np.array([observation_counts[a] for a in actions])
    ax.barh(y + 0.16, obs_values, height=0.30, color="#D9D6CF", label="正式观察行")
    ax.barh(y - 0.16, unit_values, height=0.30, color=[ACTION_COLORS[a] for a in actions], label="去重 repertoire 单元")
    ax.set_yticks(y, [ACTION_ZH[a] for a in actions], fontsize=8.7)
    ax.invert_yaxis()
    ax.set_xlabel("计数")
    ax.set_title("角色行数 ≠ 行动次数", loc="left", fontsize=15, fontweight="bold")
    ax.grid(axis="x", color="#E3E1DC", linewidth=0.7)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.legend(frameon=False, loc="lower right")

    fig.suptitle("R5/R7 异质行动 repertoire 与场域", x=0.045, y=0.99, ha="left", fontsize=22, fontweight="bold")
    fig.text(0.045, 0.947, "只复用现有正式／人审事实。共同署名、同案角色、程序阶段和服务关系分别编码；图中单元不表示稳定联盟、现实频率或政策效果。", fontsize=10.7, color="#4E5A56")
    fig.subplots_adjust(left=0.18, right=0.98, top=0.86, bottom=0.19, wspace=0.30)
    save_figure(fig, FIG1_PNG, FIG1_SVG)


def plot_sequences(sequences: list[dict[str, object]]) -> None:
    by_case: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in sequences:
        by_case[str(row["case_id"])].append(row)
    case_order = ["R7C03", "R7C02", "R7C01", "R7C04", "R7C05", "R7C06"]
    case_labels = {
        "R7C03": "2015 跨国声明",
        "R7C02": "2020 MMC 请求",
        "R7C01": "儒艮国际诉讼",
        "R7C04": "嘉手纳噪音诉讼",
        "R7C05": "石垣公投请求",
        "R7C06": "OESC→USO 慈善",
    }
    fig, ax = plt.subplots(figsize=(19, 11))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, len(case_order) + 0.2)
    ax.axis("off")
    x_positions = [0.24, 0.52, 0.80]
    box_w, box_h = 0.22, 0.57

    for row_index, case_id in enumerate(case_order):
        y = len(case_order) - row_index - 0.55
        items = sorted(by_case[case_id], key=lambda r: int(r["stage_order"]))
        ax.text(0.015, y, case_labels[case_id], va="center", fontsize=12.5, fontweight="bold")
        ax.text(0.015, y - 0.23, "顺序观察，不作因果", va="center", fontsize=8.6, color="#8A5555")
        for index, item in enumerate(items):
            x = x_positions[index]
            group = str(item["venue_group"])
            color = VENUE_GROUP_COLORS[group]
            box = FancyBboxPatch((x - box_w / 2, y - box_h / 2), box_w, box_h, boxstyle="round,pad=0.012,rounding_size=0.018", facecolor=color, alpha=0.18, edgecolor=color, linewidth=1.5)
            ax.add_patch(box)
            title = str(item["venue_or_field"])
            detail = str(item["observed_stage"])
            ax.text(x, y + 0.13, "\n".join(textwrap.wrap(title, 25)), ha="center", va="center", fontsize=9.2, fontweight="bold", color="#24322E")
            ax.text(x, y - 0.105, "\n".join(textwrap.wrap(detail, 34))[:210], ha="center", va="center", fontsize=7.4, color="#45514D")
            if index < len(items) - 1:
                arrow = FancyArrowPatch((x + box_w / 2 + 0.008, y), (x_positions[index + 1] - box_w / 2 - 0.008, y), arrowstyle="-|>", mutation_scale=12, color="#9A9D99", linewidth=1.0)
                ax.add_patch(arrow)
        ax.axhline(y - 0.47, xmin=0.01, xmax=0.99, color="#E4E2DD", linewidth=0.7)

    legend_groups = ["field_site", "civic_public_communication", "international_institution", "legal_judicial", "electoral_referendum", "service_charity", "transnational_civic"]
    handles = [Patch(facecolor=VENUE_GROUP_COLORS[g], edgecolor=VENUE_GROUP_COLORS[g], alpha=0.35, label=VENUE_GROUP_ZH[g]) for g in legend_groups]
    ax.legend(handles=handles, ncol=4, frameon=False, loc="lower center", bbox_to_anchor=(0.58, -0.01), fontsize=8.6)
    fig.suptitle("R7 跨案例场域小倍图：顺序不等于因果", x=0.04, y=0.99, ha="left", fontsize=22, fontweight="bold")
    fig.text(0.04, 0.95, "箭头只表示正式记录中的时间／构成顺序或一条关系的方向；不表示前一环节导致后一结果，也不把同场主体画成联盟。", fontsize=10.8, color="#4E5A56")
    fig.subplots_adjust(left=0.03, right=0.985, top=0.90, bottom=0.06)
    save_figure(fig, FIG2_PNG, FIG2_SVG)


def render_brief(
    rows: list[dict[str, object]],
    units: list[dict[str, object]],
    sequences: list[dict[str, object]],
    source_crosswalk: list[dict[str, object]],
    input_audit: list[dict[str, object]],
) -> str:
    module_counts = Counter(str(row["source_module"]) for row in rows)
    action_obs = Counter(str(row["action_family"]) for row in rows)
    action_units = Counter(str(row["action_family"]) for row in units)
    venues = Counter(str(row["venue_group"]) for row in units)
    canonical_events = {str(row["canonical_case_or_event_id"]) for row in rows}
    joint_events = {str(row["canonical_case_or_event_id"]) for row in rows if row["action_family"] == "joint_statement"}
    unresolved_sources = sum(row["reference_kind"] == "unresolved_reference" for row in source_crosswalk)
    accepted_stage_count = module_counts["R9_FORMAL_STAGE"]
    accepted_role_count = module_counts["R9_FORMAL_ROLE"]
    action_summary = "、".join(f"{ACTION_ZH[action]} {count}" for action, count in action_units.most_common())
    venue_summary = "、".join(f"{VENUE_GROUP_ZH[venue]} {count}" for venue, count in venues.most_common())

    return f"""# R5/R7 异质行动与场域比较 v1

日期：2026-07-13

口径：只复用 HR-015 AEV、HR-014 R8、R9 formal accepted 及 R10 既有人审关系；不新增事实，不修改基础中央表，只重生派生 interim35。

## 规模与计数单位

统一表共有 **{len(rows)}** 条正式观察：

- AEV／HR-015：{module_counts['AEV_HR015']}；
- R8／HR-014 案件角色：{module_counts['R8_HR014']}；
- R9 accepted 阶段：{accepted_stage_count}；
- R9 accepted 角色：{accepted_role_count}；
- R10 人审功能／资源关系：{module_counts['R10_HUMAN_RELATION']}。

这些是角色、阶段和关系的**审计行**，不是行动次数。为避免一个案件因原告、律师、机关或阶段较多而被人为放大，本包另以 `canonical case/event × action family × venue group` 去重，形成 **{len(units)}** 个 repertoire 单元，覆盖 **{len(canonical_events)}** 个既有事件／案件／项目关系。当前有 **{len(action_units)}** 类行动／关系语法和 **{len(venues)}** 类场域。

去重行动单元：{action_summary}。

去重场域单元：{venue_summary}。

## 解释性发现

1. **共同署名是公开传播行动，不是组织联盟。** 统一表中的 {action_obs['joint_statement']} 条共同声明角色行只对应 {len(joint_events)} 个声明事件；参与者多并不等于事件多，更不等于稳定合作网络。
2. **同一争议会进入不同制度场域。** 边野古／大浦湾可出现在公开声明、美国海洋哺乳动物委员会请求、美国联邦诉讼和日本 EIA 意见渠道；同一地点对象不意味着这些渠道的角色可互换。
3. **法律行动内部也不相同。** 儒艮案、嘉手纳／普天间噪音、石垣义务付け和泡濑公金诉讼分别进入不同法院、提出不同请求并产生不同处分。原告、律师、requester、supporter 与 non-party 保持案件特定。
4. **公投不是一个点，而是门槛链。** R9 的 {accepted_stage_count} 个 accepted 阶段显示签名／直接请求、条例／议会、投票／结果、行政解释和司法路径可依次或并行出现。图中箭头只表示已记录顺序，不能写成前一阶段造成后一结果，也不能声称组织导致票数或胜负。
5. **行政／服务／慈善是另一种关系语法。** R10 的 9 条既有人审关系只说明活动协作、赞助、捐赠、特定 grant、伞状成员关系或 NOFO。成员不等于资助，NOFO 不等于 award／recipient，服务对象不产生亲基地／反基地立场。
6. **观察行数必须与事件／案件单元分开。** 角色密集的声明和诉讼会产生很多行；本包的右侧条形图故意并列“正式观察行”和“去重单元”，防止用表格行数代替现实行动强度。

## 跨案例小倍图怎么读

六个小倍案例覆盖共同声明、国际机构请求、美国诉讼、日本噪音诉讼、公投／司法转向和基地社区慈善。前三个直接复用现有 R7 顺序表；后三个只把 HR-014、R9 accepted 及 R10 human_checked 事实排成阅读顺序。所有行都标注 `ordered observation only; no causal inference` 或等价边界。

## HR-028 与来源边界

- 本包没有新增事件事实，因此 **HR-028 = 0**；未创建需要人工决定的事实行。
- source crosswalk 共 {len(source_crosswalk)} 行，未解析 reference 为 {unresolved_sources} 行；来源映射不新增关系批准。
- R9 的 3 个 accepted role 指向结果文本仍待复核的阶段；本包只使用其已接受的法院／角色事实，不把相应阶段结果纳入 accepted stage 计数。
- 共同出现、同案角色、程序相邻和服务关系均不升级为稳定联盟。
- 金额、资助、委托与赞助只沿用原模块边界，本包不作新的资金判断。

## 文件

- 统一表：`data/interim/35_heterogeneous_event_repertoire_v1.csv`
- 去重单元：`repertoire_event_action_venue_units_v1.csv`
- 六案例顺序表：`cross_case_sequence_v1.csv`
- 输入审计：`input_layer_audit_v1.csv`
- 重叠审计：`canonical_event_overlap_audit_v1.csv`
- 来源交叉表：`source_crosswalk_v1.csv`
- 图 1：`fig1_repertoire_action_venue_matrix_v1.*`
- 图 2：`fig2_cross_case_venue_small_multiples_v1.*`
"""


def validate(
    rows: list[dict[str, object]],
    units: list[dict[str, object]],
    sequences: list[dict[str, object]],
    source_crosswalk: list[dict[str, object]],
    input_audit: list[dict[str, object]],
) -> None:
    def require(condition: bool, message: str) -> None:
        if not condition:
            raise ValueError(message)

    require(len(rows) == 148, f"expected 148 formal observations, found {len(rows)}")
    require(len({str(r['observation_id']) for r in rows}) == 148, "observation IDs are not unique")
    counts = Counter(str(r["source_module"]) for r in rows)
    require(counts == Counter({"AEV_HR015": 63, "R8_HR014": 27, "R9_FORMAL_STAGE": 24, "R9_FORMAL_ROLE": 25, "R10_HUMAN_RELATION": 9}), f"source-layer counts changed: {counts}")
    require(all(r["new_fact_status"] == "existing_formal_fact_only" for r in rows), "new fact leaked into unified table")
    require(all(r["action_family"] in ACTION_ZH for r in rows), "unmapped action family")
    require(all(r["venue_group"] in VENUE_GROUP_ZH for r in rows), "unmapped venue group")
    require(len({str(r["action_family"]) for r in rows}) >= 5, "fewer than five action families")
    require(len({str(r["venue_group"]) for r in rows}) >= 4, "fewer than four venue groups")
    require(all("causal" in str(r["sequence_limit"]) for r in rows), "sequence causality boundary missing")

    unit_ids = {str(r["repertoire_unit_id"]) for r in rows}
    require(unit_ids == {str(r["repertoire_unit_id"]) for r in units}, "unit coverage mismatch")
    require(sum(int(r["observation_row_count"]) for r in units) == 148, "unit observation counts do not sum to table")
    require(len([r for r in rows if r["action_family"] == "joint_statement"]) == 33, "expected 33 co-signing role rows")
    require(len({r["canonical_case_or_event_id"] for r in units if r["action_family"] == "joint_statement"}) == 2, "joint statements should collapse to two events")

    require(len(sequences) == 17, f"expected 17 sequence stages, found {len(sequences)}")
    require(len({str(r["case_id"]) for r in sequences}) == 6, "expected six small-multiple cases")
    require(all("no causal" in str(r["arrow_semantics"]) or "no causal" in str(r["arrow_semantics"]).lower() or "no causal or political" in str(r["arrow_semantics"]).lower() for r in sequences), "sequence arrow boundary missing")
    require(all(r["new_fact_status"] != "new_fact" for r in sequences), "new sequence fact requires HR028")

    expected_ref_count = sum(len(split_refs(str(r["source_refs"]))) for r in rows)
    require(len(source_crosswalk) == expected_ref_count, "source crosswalk does not expand all refs")
    require({str(r["observation_id"]) for r in source_crosswalk} == {str(r["observation_id"]) for r in rows}, "source crosswalk misses observations")
    require(all(r["relation_or_claim_approved"] == "no" for r in source_crosswalk), "source crosswalk contains implicit approval")
    require(all(r["approval_provenance_scope"] == "reused_existing_formal_observation__no_new_approval" for r in source_crosswalk), "source approval provenance scope changed")
    require(sum(int(r["included_formal_row_count"]) for r in input_audit) == 148, "input audit does not sum to 148")


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    configure_fonts()
    aev = read_csv(AEV)
    r8_cases = read_csv(R8_CASES)
    r8_roles = read_csv(R8_ROLES)
    r9_stages = read_csv(R9_STAGES)
    r9_roles = read_csv(R9_ROLES)
    r10_relations = read_csv(R10_RELATIONS)
    r10_pathways = read_csv(R10_PATHWAYS)
    venue_by_id = {row["venue_id"]: row for row in read_csv(VENUES)}

    rows = build_rows(aev, r8_cases, r8_roles, r9_stages, r9_roles, r10_pathways, venue_by_id)
    units = build_units(rows)
    overlap = build_overlap_audit(rows, units)
    input_audit = build_input_audit(aev, r8_roles, r9_stages, r9_roles, r10_relations)
    sequences = build_sequences(r8_cases, r9_stages, r10_pathways)
    source_crosswalk = build_source_crosswalk(rows)
    validate(rows, units, sequences, source_crosswalk, input_audit)

    write_csv(DERIVED, rows, list(rows[0].keys()))
    write_csv(UNITS, units, list(units[0].keys()))
    write_csv(OVERLAP_AUDIT, overlap, list(overlap[0].keys()))
    write_csv(INPUT_AUDIT, input_audit, list(input_audit[0].keys()))
    write_csv(SEQUENCES, sequences, list(sequences[0].keys()))
    write_csv(SOURCE_CROSSWALK, source_crosswalk, list(source_crosswalk[0].keys()))

    plot_repertoire(rows, units)
    plot_sequences(sequences)
    for svg in [FIG1_SVG, FIG2_SVG]:
        normalize_generated_svg(svg)
    write_text(FIG1_HTML, html_wrapper(FIG1_SVG.name, "R5/R7 异质行动 repertoire 与场域"))
    write_text(FIG2_HTML, html_wrapper(FIG2_SVG.name, "R7 跨案例场域小倍图"))
    write_text(BRIEF, render_brief(rows, units, sequences, source_crosswalk, input_audit))
    write_text(
        HR028_STATUS,
        """# HR-028 status

No HR-028 fact-review rows were created.

This package introduces no new event, role, relation, venue, target, result, or
funding fact. It only normalizes existing human-reviewed/formally accepted
records and creates analytical counting/sequence views. Consequently HR-028
has 0 items. If a later revision adds a fact outside those formal layers, it
must create a blank HR-028 task before the fact can enter this package.
""",
    )
    write_text(
        README,
        f"""# R05/R07 heterogeneous repertoire v1

Generated by `python scripts/make_r05_r07_heterogeneous_repertoire_v1.py`.

- Formal observations: {len(rows)} (63 human-checked AEV + 27 R8 roles + 24 R9 stages + 25 R9 roles + 9 R10 relations).
- Deduplicated event/case-action-venue units: {len(units)}.
- Action/relation families: {len({r['action_family'] for r in rows})}; venue groups: {len({r['venue_group'] for r in rows})}.
- Cross-case sequence display: 17 stages across 6 cases.
- HR-028: 0; no new facts were added.

Observation-row counts are not action frequencies. Co-signing, shared cases,
adjacent process stages, service relations, and shared venues do not establish
stable alliances or causal effects.
""",
    )

    # Round-trip and visual checks.
    roundtrip = read_csv(DERIVED)
    if len(roundtrip) != len(rows) or {r["observation_id"] for r in roundtrip} != {str(r["observation_id"]) for r in rows}:
        raise ValueError("unified CSV round-trip failed")
    for svg in [FIG1_SVG, FIG2_SVG]:
        ET.parse(svg)
        if svg.stat().st_size < 10_000:
            raise ValueError(f"SVG unexpectedly small: {svg}")
        if any(line.endswith((" ", "\t")) for line in svg.read_text(encoding="utf-8").splitlines()):
            raise ValueError(f"SVG contains trailing whitespace: {svg}")
    for png in [FIG1_PNG, FIG2_PNG]:
        if png.stat().st_size < 20_000:
            raise ValueError(f"PNG unexpectedly small: {png}")
    if "HR-028 = 0" not in BRIEF.read_text(encoding="utf-8"):
        raise ValueError("brief HR028 status missing")

    artifacts = [DERIVED, UNITS, OVERLAP_AUDIT, INPUT_AUDIT, SEQUENCES, SOURCE_CROSSWALK, BRIEF, README, HR028_STATUS, FIG1_PNG, FIG1_SVG, FIG2_PNG, FIG2_SVG]
    hashes = [file_sha(path) for path in artifacts]
    if not all(hashes):
        raise ValueError("artifact hash failure")
    write_text(
        VALIDATION,
        f"""# R5/R7 heterogeneous repertoire validation v1

- Unified formal observations: {len(rows)}; source-layer split 63/27/24/25/9 verified.
- New facts: 0; HR-028 items: 0.
- Deduplicated repertoire units: {len(units)}; their observation counts sum to {len(rows)}.
- Action/relation families: {len({r['action_family'] for r in rows})} (minimum 5 passed).
- Venue groups: {len({r['venue_group'] for r in rows})} (minimum 4 passed).
- Co-signing boundary: 33 formal role rows collapse to 2 statement-event units; no alliance inference.
- Cross-case small multiples: 17 stages / 6 cases; all arrows explicitly non-causal.
- Source refs: {len(source_crosswalk)} expanded rows; every formal observation covered; all approval flags remain `no`; provenance scope records that no new approval is created.
- Figure checks: 2/2 SVG XML parse and trailing-whitespace checks; 2/2 PNG size checks pass.
- Base central tables and documents were not modified; derived interim35 was regenerated.
""",
    )
    print(
        f"R5/R7 heterogeneous repertoire OK: {len(rows)} observations; "
        f"{len(units)} units; {len({r['action_family'] for r in rows})} action families; "
        f"{len({r['venue_group'] for r in rows})} venue groups; HR028=0."
    )


if __name__ == "__main__":
    main()
