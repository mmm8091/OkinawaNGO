from __future__ import annotations

"""Build the R1/R2 acceptance package from the current Phase-1 data.

This script does not change the actor registry or the source log.  It creates a
derived, review-aware actor--issue layer and module-specific audit outputs.
Candidate edges remain candidate evidence; event participation is never
interpreted as a stable alliance or a long-term organizational position.
"""

import csv
import itertools
import textwrap
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from matplotlib.lines import Line2D


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "interim"
OUT = ROOT / "outputs" / "R01_R02_actor_issue_v1"
HR = OUT / "HR019"
DERIVED = DATA / "24_r01_r02_actor_issue_layered_v0.csv"

REGISTRY = DATA / "01_actor_registry_initial_v0.csv"
ISSUES = DATA / "03_issue_taxonomy_v0.csv"
EDGES = DATA / "07_actor_issue_edges_initial_v0.csv"
EXPANSION = ROOT / "outputs" / "registry_expansion_v1" / "candidate_actors_v1.csv"

SCHEMA_CLASSES = {
    "local_civic_actor", "local_npo", "citizen_group", "citizen_network",
    "executive_committee", "lawyers_network", "domestic_japan_ngo",
    "international_advocacy_actor", "international_ngo",
    "base_community_service_actor", "base_spouse_club",
    "base_spouse_charity_network", "public_diplomacy_or_exchange_actor",
    "public_diplomacy_grant_program", "local_international_cooperation_ngo",
    "public_institution_partner", "corporate_sponsor",
    "local_business_sponsor", "funder_or_intermediary", "labor_union",
    "womens_organization",
}
SCHEMA_REVIEW = {
    "ai_seeded", "human_checked", "human_revised", "needs_second_source",
    "needs_local_retrieval", "rejected",
}

CLASS_FAMILY = {
    "local_civic_actor": "冲绳本地公民行动",
    "local_npo": "冲绳本地公民行动",
    "citizen_group": "冲绳本地公民行动",
    "citizen_network": "冲绳本地公民行动",
    "executive_committee": "冲绳本地公民行动",
    "domestic_japan_ngo": "日本国内 NGO／声援",
    "international_advocacy_actor": "跨国 NGO／国际倡议",
    "international_ngo": "跨国 NGO／国际倡议",
    "lawyers_network": "法律／制度程序",
    "labor_or_education_union": "劳工／教育组织",
    "labor_union_federation": "劳工／教育组织",
    "labor_union": "劳工／教育组织",
    "womens_or_community_organization": "女性／人权／社区",
    "womens_or_human_rights_ngo": "女性／人权／社区",
    "womens_organization": "女性／人权／社区",
    "base_community_service_actor": "基地社区服务／慈善",
    "base_spouse_club": "基地社区服务／慈善",
    "base_spouse_charity_network": "基地社区服务／慈善",
    "local_international_cooperation_ngo": "国际合作／公共外交",
    "public_diplomacy_or_exchange_actor": "国际合作／公共外交",
    "public_diplomacy_grant_program": "国际合作／公共外交",
    "public_institution_partner": "资助／赞助／公共机构",
    "funder_or_intermediary": "资助／赞助／公共机构",
    "corporate_sponsor": "资助／赞助／公共机构",
    "local_business_sponsor": "资助／赞助／公共机构",
    "media_or_advocacy_actor": "媒体／倡议观察节点",
}
FAMILY_ORDER = [
    "冲绳本地公民行动", "劳工／教育组织", "女性／人权／社区",
    "法律／制度程序", "日本国内 NGO／声援", "跨国 NGO／国际倡议",
    "基地社区服务／慈善", "国际合作／公共外交",
    "资助／赞助／公共机构", "媒体／倡议观察节点", "待人工分类",
]
FAMILY_COLORS = {
    "冲绳本地公民行动": "#276b6f",
    "劳工／教育组织": "#9a6542",
    "女性／人权／社区": "#a14f76",
    "法律／制度程序": "#356887",
    "日本国内 NGO／声援": "#6870a6",
    "跨国 NGO／国际倡议": "#56458c",
    "基地社区服务／慈善": "#bc8734",
    "国际合作／公共外交": "#4c8a69",
    "资助／赞助／公共机构": "#8b6f61",
    "媒体／倡议观察节点": "#7d858d",
    "待人工分类": "#c23b3b",
}
ORIGIN_ORDER = [
    "okinawa_local", "japan_domestic", "mixed_or_network", "international",
    "us_origin", "public_institution", "corporate",
]
ORIGIN_CN = {
    "okinawa_local": "冲绳本地", "japan_domestic": "日本国内",
    "mixed_or_network": "混合／网络", "international": "国际",
    "us_origin": "美国来源", "public_institution": "公共机构",
    "corporate": "企业",
}
SCOPE_COLORS = {
    "organizational_positioning": "#276b6f",
    "institutional_or_case_role": "#3f6da1",
    "event_specific": "#d28b3f",
    "mixed_or_unclear": "#9ba3a8",
}
GROUP_COLORS = {
    "base_politics": "#b34d4d", "security_politics": "#a66d3f",
    "place_issue": "#7e5b9d", "environment": "#3d8b64",
    "life_safety": "#c18b32", "governance": "#4c78a8",
    "legal_policy": "#5d6d7e", "transnational": "#6f58a5",
    "external_network": "#45908c", "base_community": "#9a7651",
    "peace_human_rights": "#a44f78", "collective_action": "#7c7f47",
}
HUMAN_STATUSES = {"human_checked", "human_revised"}
EVIDENCE_RANK = {"E0": 0, "E1": 1, "E2": 2, "E3": 3, "E4": 4}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def preserve_completed_hr_queue(
    path: Path, generated_rows: list[dict[str, object]], fields: list[str],
) -> tuple[list[dict[str, str]] | list[dict[str, object]], bool]:
    """Keep a closed human-review ledger intact while regenerating derivatives."""

    if path.exists():
        existing = read_csv(path)
        if existing and all(row.get("review_decision", "").strip() for row in existing):
            return existing, True
    write_csv(path, generated_rows, fields)
    return generated_rows, False


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


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


def short(value: str, width: int = 24) -> str:
    return value if len(value) <= width else value[: width - 1] + "…"


def classify_scope(edge: dict[str, str]) -> tuple[str, str]:
    reviewed_scope = edge.get("scope_kind", "").strip()
    if edge.get("scope_review_status") in HUMAN_STATUSES and reviewed_scope:
        reviewed_map = {
            "organizational_positioning": "organizational_positioning",
            "institutional_or_case_role": "institutional_or_case_role",
            "event_specific": "event_specific",
            "remain_unclear": "mixed_or_unclear",
            "case": "institutional_or_case_role",
        }
        if reviewed_scope not in reviewed_map:
            raise ValueError(f"Unknown reviewed scope_kind: {reviewed_scope}")
        return reviewed_map[reviewed_scope], "human-reviewed scope_kind from central actor-issue edge"

    text = f"{edge.get('relation_basis', '')} {edge.get('notes', '')}".lower()
    issue = edge.get("issue_label", "").lower()
    event_terms = (
        "signator", "statement", "request", "co-sign", "opinion ad",
        "photo-exhibit", "photo exhibit", "public action", "emergency",
        "2010 ", "2015 ", "2020 ", "referendum initiative",
        "referendum solidarity", "vote-process", "on-site sit-in",
    )
    case_terms = (
        "litigation", "counsel", "plaintiff", "injunction", "legal action",
        "legal representation", "service role", "sponsor", "donation",
        "grant opportunity", "consultant", "contractor", "project cost",
        "public-private partnership", "gift shop", "charity role",
        "institutional role", "administrative base burden",
    )
    position_terms = (
        "mission", "purpose", "core ", "sustained", "long-running",
        "movement coordination", "network purpose", "network activities",
        "umbrella network", "protection campaign", "advocacy context",
        "focus", "regional identity", "framing", "base removal",
        "anti-base coordination", "anti-military deployment coordination",
        "opposition coordination", "civic coordination", "movement",
    )
    # Some legacy edges combine a broad organizational mission with one dated
    # statement in the same relation_basis.  Keep mission-backed issue labels
    # as positioning, while the Henoko/base statement edge remains event-level.
    if "mission" in text and issue in {"women", "human_rights", "peace", "international_cooperation"}:
        return "organizational_positioning", "mission marker applies directly to this issue label"
    if any(term in text for term in event_terms):
        return "event_specific", "explicit statement/signatory/request/action marker"
    if any(term in text for term in case_terms):
        return "institutional_or_case_role", "legal/service/program/support role marker"
    if any(term in text for term in position_terms):
        return "organizational_positioning", "mission/purpose/sustained-role marker"
    return "mixed_or_unclear", "no reliable temporal-scope marker in current edge text"


def actor_class_audit(actors: list[dict[str, str]]) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    audit: list[dict[str, object]] = []
    by_class: dict[str, list[dict[str, str]]] = defaultdict(list)
    for actor in actors:
        by_class[actor["actor_class"]].append(actor)
        family = CLASS_FAMILY.get(actor["actor_class"], "待人工分类")
        class_status = "schema_term" if actor["actor_class"] in SCHEMA_CLASSES else "out_of_schema_term"
        review_term_status = "schema_term" if actor["review_status"] in SCHEMA_REVIEW else "out_of_schema_term"
        audit.append({
            "actor_id": actor["actor_id"], "canonical_name": actor["canonical_name"],
            "actor_class_original": actor["actor_class"],
            "actor_class_term_status": class_status,
            "analysis_family_v1": family,
            "family_mapping_status": "rule_applied" if family != "待人工分类" else "needs_human_taxonomy_decision",
            "origin_type": actor["origin_type"],
            "evidence_level": actor["evidence_level"],
            "review_status_original": actor["review_status"],
            "review_status_term_status": review_term_status,
            "human_decision": "",
            "interpretation_limit": "analysis-only mapping; actor registry is unchanged",
        })

    mapping: list[dict[str, object]] = []
    for cls in sorted(by_class):
        items = by_class[cls]
        mapping.append({
            "actor_class_original": cls,
            "actor_count": len(items),
            "schema_status": "schema_term" if cls in SCHEMA_CLASSES else "out_of_schema_term",
            "analysis_family_v1": CLASS_FAMILY.get(cls, "待人工分类"),
            "actor_ids": ";".join(a["actor_id"] for a in items),
            "human_taxonomy_decision_required": "no" if cls in SCHEMA_CLASSES else "yes",
            "recommended_rule": (
                "retain class term and map to analysis family"
                if cls in SCHEMA_CLASSES else
                "decide whether to extend actor_class vocabulary or collapse to an existing broad class"
            ),
            "review_decision": "",
        })
    return audit, mapping


def build_layered_edges(
    edges: list[dict[str, str]], actors_by_id: dict[str, dict[str, str]],
    issues_by_id: dict[str, dict[str, str]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for edge in edges:
        scope, scope_rule = classify_scope(edge)
        actor = actors_by_id.get(edge["actor_id"], {})
        issue = issues_by_id.get(edge["issue_id"], {})
        human = edge["review_status"] in HUMAN_STATUSES
        rows.append({
            "edge_id": edge["edge_id"], "actor_id": edge["actor_id"],
            "actor_name": actor.get("canonical_name", ""),
            "actor_class": actor.get("actor_class", ""),
            "analysis_family_v1": CLASS_FAMILY.get(actor.get("actor_class", ""), "待人工分类"),
            "origin_type": actor.get("origin_type", ""),
            "issue_id": edge["issue_id"], "issue_label": edge["issue_label"],
            "issue_group": issue.get("issue_group", ""),
            "relation_basis_original": edge["relation_basis"],
            "temporal_scope_v1": scope, "temporal_scope_rule": scope_rule,
            "source_ref": edge["source_ref"],
            "evidence_level": edge["evidence_level"],
            "review_status": edge["review_status"],
            "review_layer": "human_reviewed" if human else "candidate",
            "conclusion_eligibility": (
                "human_reviewed_E3_E4" if human and EVIDENCE_RANK.get(edge["evidence_level"], 0) >= 3
                else "candidate_or_clue"
            ),
            "notes": edge["notes"],
            "interpretation_limit": (
                "actor--issue evidence only; does not establish stable inter-organizational alliance"
            ),
        })
    return rows


def build_cross_issue(
    actors: list[dict[str, str]], layered: list[dict[str, object]],
) -> list[dict[str, object]]:
    by_actor: dict[str, list[dict[str, object]]] = defaultdict(list)
    for edge in layered:
        by_actor[str(edge["actor_id"])].append(edge)
    rows: list[dict[str, object]] = []
    for actor in actors:
        es = by_actor.get(actor["actor_id"], [])
        all_issues = sorted({str(e["issue_id"]) for e in es})
        human_issues = sorted({str(e["issue_id"]) for e in es if e["review_layer"] == "human_reviewed"})
        position_issues = sorted({str(e["issue_id"]) for e in es if e["temporal_scope_v1"] == "organizational_positioning"})
        event_issues = sorted({str(e["issue_id"]) for e in es if e["temporal_scope_v1"] == "event_specific"})
        case_issues = sorted({str(e["issue_id"]) for e in es if e["temporal_scope_v1"] == "institutional_or_case_role"})
        unclear_issues = sorted({str(e["issue_id"]) for e in es if e["temporal_scope_v1"] == "mixed_or_unclear"})
        if len(position_issues) >= 2:
            bridge = "positioning_bridge"
        elif len(case_issues) >= 2:
            bridge = "case_or_institutional_bridge"
        elif len(all_issues) >= 2 and set(all_issues) <= set(event_issues):
            bridge = "event_only_bridge"
        elif len(all_issues) >= 2:
            bridge = "mixed_candidate_bridge"
        elif len(all_issues) == 1:
            bridge = "single_issue_in_edge_table"
        else:
            bridge = "no_actor_issue_edge"
        rows.append({
            "actor_id": actor["actor_id"], "canonical_name": actor["canonical_name"],
            "actor_class": actor["actor_class"],
            "analysis_family_v1": CLASS_FAMILY.get(actor["actor_class"], "待人工分类"),
            "origin_type": actor["origin_type"],
            "actor_review_status": actor["review_status"],
            "issue_count_all": len(all_issues), "issue_ids_all": ";".join(all_issues),
            "issue_count_human_reviewed": len(human_issues),
            "issue_ids_human_reviewed": ";".join(human_issues),
            "issue_count_positioning": len(position_issues),
            "issue_ids_positioning": ";".join(position_issues),
            "issue_count_event_specific": len(event_issues),
            "issue_ids_event_specific": ";".join(event_issues),
            "issue_count_case_or_institutional": len(case_issues),
            "issue_ids_case_or_institutional": ";".join(case_issues),
            "issue_count_mixed_or_unclear": len(unclear_issues),
            "bridge_classification_v1": bridge,
            "narrative_status": (
                "human_reviewed_bridge" if len(human_issues) >= 2
                else "candidate_bridge_needs_review" if len(all_issues) >= 2
                else "not_a_bridge_in_current_edge_table"
            ),
        })
    return rows


def build_cooccurrence(
    layered: list[dict[str, object]], issues: list[dict[str, str]],
) -> list[dict[str, object]]:
    by_actor: dict[str, dict[str, list[dict[str, object]]]] = defaultdict(lambda: defaultdict(list))
    for edge in layered:
        by_actor[str(edge["actor_id"])][str(edge["issue_id"])].append(edge)
    labels = {i["issue_id"]: i["issue_label"] for i in issues}
    rows: list[dict[str, object]] = []
    for i1, i2 in itertools.combinations(labels, 2):
        shared_all: list[str] = []
        shared_human: list[str] = []
        shared_position: list[str] = []
        shared_event_only: list[str] = []
        for actor_id, issue_map in by_actor.items():
            if i1 not in issue_map or i2 not in issue_map:
                continue
            shared_all.append(actor_id)
            e1, e2 = issue_map[i1], issue_map[i2]
            if any(e["review_layer"] == "human_reviewed" for e in e1) and any(e["review_layer"] == "human_reviewed" for e in e2):
                shared_human.append(actor_id)
            if any(e["temporal_scope_v1"] == "organizational_positioning" for e in e1) and any(e["temporal_scope_v1"] == "organizational_positioning" for e in e2):
                shared_position.append(actor_id)
            scopes = {str(e["temporal_scope_v1"]) for e in e1 + e2}
            if scopes == {"event_specific"}:
                shared_event_only.append(actor_id)
        if shared_all:
            rows.append({
                "issue_id_1": i1, "issue_label_1": labels[i1],
                "issue_id_2": i2, "issue_label_2": labels[i2],
                "shared_actor_count_all": len(shared_all),
                "shared_actor_ids_all": ";".join(sorted(shared_all)),
                "shared_actor_count_human_reviewed": len(shared_human),
                "shared_actor_ids_human_reviewed": ";".join(sorted(shared_human)),
                "shared_actor_count_positioning": len(shared_position),
                "shared_actor_ids_positioning": ";".join(sorted(shared_position)),
                "shared_actor_count_event_only": len(shared_event_only),
                "shared_actor_ids_event_only": ";".join(sorted(shared_event_only)),
                "interpretation_limit": "shared actor issue profile; not an organization-to-organization alliance",
            })
    rows.sort(key=lambda x: (-int(x["shared_actor_count_all"]), str(x["issue_id_1"]), str(x["issue_id_2"])))
    return rows


def build_issue_coverage(
    issues: list[dict[str, str]], layered: list[dict[str, object]],
) -> list[dict[str, object]]:
    by_issue: dict[str, list[dict[str, object]]] = defaultdict(list)
    for edge in layered:
        by_issue[str(edge["issue_id"])].append(edge)
    rows: list[dict[str, object]] = []
    for issue in issues:
        es = by_issue.get(issue["issue_id"], [])
        actor_ids = {str(e["actor_id"]) for e in es}
        human_ids = {str(e["actor_id"]) for e in es if e["review_layer"] == "human_reviewed"}
        position_ids = {str(e["actor_id"]) for e in es if e["temporal_scope_v1"] == "organizational_positioning"}
        event_ids = {str(e["actor_id"]) for e in es if e["temporal_scope_v1"] == "event_specific"}
        rows.append({
            "issue_id": issue["issue_id"], "issue_label": issue["issue_label"],
            "issue_group": issue["issue_group"], "actor_count_all": len(actor_ids),
            "actor_count_human_reviewed": len(human_ids),
            "actor_count_positioning": len(position_ids),
            "actor_count_event_specific": len(event_ids),
            "coverage_flag": (
                "no_edge" if not actor_ids else
                "thin_no_human_review" if len(actor_ids) <= 3 and not human_ids else
                "thin" if len(actor_ids) <= 3 else
                "event_heavy" if len(event_ids) > len(actor_ids) / 2 else "usable_sample"
            ),
        })
    return rows


def build_expansion_candidates(
    actors_by_id: dict[str, dict[str, str]],
) -> list[dict[str, object]]:
    """Render the HR-013 disposition ledger for the former R1/R2 shortlist.

    The filename is retained for traceability, but these nine rows are no longer
    an active expansion shortlist.  Their final state must come from the shared
    candidate table rather than from pre-HR-013 heuristics in this generator.
    """
    candidates = read_csv(EXPANSION)
    selected = {"C010", "C011", "C015", "C029", "C030", "C031", "C032", "C033", "C034"}
    expected_dispositions = {
        "C010": ("", "background_only_hr013"),
        "C011": ("A111", "added_hr013"),
        "C015": ("", "defer"),
        "C029": ("", "out_of_scope_hr013"),
        "C030": ("", "out_of_scope_hr013"),
        "C031": ("", "out_of_scope_hr013"),
        "C032": ("", "out_of_scope_hr013"),
        "C033": ("", "out_of_scope_hr013"),
        "C034": ("", "background_only_hr013"),
    }
    module_use = {
        "C010": "R1/R4 background context: war-memory education only",
        "C011": "R1/R2 core-support actor already represented by A111",
        "C015": "possible R2/R3/R4 groundwater-deployment bridge only if identity is resolved",
        "C029": "none: general public-interest function is outside Phase-1 scope",
        "C030": "none: general public-interest function is outside Phase-1 scope",
        "C031": "none: general public-interest function is outside Phase-1 scope",
        "C032": "none: general public-interest function is outside Phase-1 scope",
        "C033": "none: general public-interest function is outside Phase-1 scope",
        "C034": "R4 background context: general coral-conservation platform only",
    }
    state = {
        "added_hr013": (
            "already_in_registry", "closed_merged",
            "No expansion action. Use the central actor row and its reviewed edges.",
            "Already counted once in the registry; this ledger row is not a candidate actor.",
        ),
        "background_only_hr013": (
            "background_only_not_registry", "closed_background_only",
            "No actor-expansion task. Retain only as bounded module context.",
            "Background context only; do not count as a Phase-1 actor or infer a political stance.",
        ),
        "out_of_scope_hr013": (
            "rejected_not_registry", "closed_rejected",
            "No further Phase-1 expansion work unless a new human decision reopens scope.",
            "Human-rejected as out of scope; organization identity does not establish Phase-1 relevance.",
        ),
        "defer": (
            "deferred_not_registry", "deferred_second_source",
            "Resolve exact organization identity and continuity with an independent second source; do not merge with 宮古島地下水研究会.",
            "Deferred identity item, not an active or count-ready expansion candidate.",
        ),
    }
    selected_rows = [c for c in candidates if c["candidate_id"] in selected]
    if {c["candidate_id"] for c in selected_rows} != selected:
        raise ValueError("R1/R2 HR-013 disposition ledger is missing a selected candidate")
    rows: list[dict[str, object]] = []
    for c in selected_rows:
        candidate_id = c["candidate_id"]
        expected_id, expected_disposition = expected_dispositions[candidate_id]
        if c["proposed_id"] != expected_id or c["triage_recommendation"] != expected_disposition:
            raise ValueError(
                f"stale HR-013 candidate state for {candidate_id}: "
                f"{c['proposed_id']!r}/{c['triage_recommendation']!r}"
            )
        registry_status, task_status, next_task, limit = state[expected_disposition]
        if expected_disposition == "added_hr013":
            actor = actors_by_id.get(expected_id)
            if actor is None or actor["canonical_name"] != c["canonical_name"]:
                raise ValueError(f"{candidate_id} does not crosswalk cleanly to {expected_id}")
            limit += " The historical candidate URL is a third-party program record, not A111's official site."
        rows.append({
            "candidate_id": candidate_id, "proposed_id": c["proposed_id"],
            "canonical_name": c["canonical_name"],
            "actor_class_proposed": c["actor_class"], "origin_type": c["origin_type"],
            "primary_places": c["primary_places"], "issue_tags_candidate": c["issue_tags"],
            "module_use_after_hr013": module_use[candidate_id],
            "source_url": c["source_url"], "evidence_level_current": c["evidence_level"],
            "final_review_status": c["review_status"],
            "final_disposition": c["triage_recommendation"],
            "registry_status": registry_status, "remaining_task_status": task_status,
            "recommended_next_task": next_task,
            "decision_basis": c["add_or_defer_reason"],
            "interpretation_limit": limit,
        })
    return rows


def save_ecology_figure(actors: list[dict[str, str]]) -> None:
    cells: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for actor in actors:
        family = CLASS_FAMILY.get(actor["actor_class"], "待人工分类")
        cells[(family, actor["origin_type"])].append(actor)
    fig, ax = plt.subplots(figsize=(14.5, 8.6))
    for yi, family in enumerate(FAMILY_ORDER):
        for xi, origin in enumerate(ORIGIN_ORDER):
            items = cells[(family, origin)]
            if not items:
                continue
            human = sum(a["review_status"] in HUMAN_STATUSES for a in items)
            ax.scatter(
                xi, yi, s=95 + 66 * len(items), color=FAMILY_COLORS[family],
                alpha=0.35 + 0.55 * human / len(items), edgecolor="#26343c", linewidth=0.8,
            )
            ax.text(xi, yi, f"{len(items)}\nH{human}", ha="center", va="center",
                    fontsize=8.5, color="white" if human / len(items) > 0.45 else "#1d2a31",
                    fontweight="bold")
    ax.set_xticks(range(len(ORIGIN_ORDER)), [ORIGIN_CN[x] for x in ORIGIN_ORDER], fontsize=10)
    ax.set_yticks(range(len(FAMILY_ORDER)), FAMILY_ORDER, fontsize=10)
    ax.invert_yaxis()
    ax.grid(color="#dde4e8", linewidth=0.8)
    ax.set_axisbelow(True)
    ax.set_title(f"R1｜{len(actors)} 个 actor 的组织生态：功能层 × 来源层", fontsize=18, loc="left", pad=25, fontweight="bold")
    ax.text(0, 1.035, "气泡面积＝actor 数；H＝actor registry 中 human_checked / human_revised 数。",
            transform=ax.transAxes, fontsize=10, color="#52616b")
    ax.text(0, -0.12,
            "这是公开资料驱动的样本生态，不是总体比例。分析功能层是派生映射；6 个超出 schema 的 actor_class 术语仍待 HR-019 决策。",
            transform=ax.transAxes, fontsize=9.5, color="#66747d")
    for spine in ax.spines.values():
        spine.set_visible(False)
    fig.subplots_adjust(left=0.20, right=0.98, top=0.86, bottom=0.16)
    fig.savefig(OUT / "fig1_r01_actor_ecology.png", dpi=240)
    plt.close(fig)


def save_bipartite_figure(
    actors: list[dict[str, str]], issues: list[dict[str, str]],
    layered: list[dict[str, object]], cross: list[dict[str, object]],
) -> None:
    degree = {str(r["actor_id"]): int(r["issue_count_all"]) for r in cross}
    family_index = {f: i for i, f in enumerate(FAMILY_ORDER)}
    sorted_actors = sorted(
        actors,
        key=lambda a: (family_index.get(CLASS_FAMILY.get(a["actor_class"], "待人工分类"), 999),
                       -degree.get(a["actor_id"], 0), a["actor_id"]),
    )
    group_order = list(GROUP_COLORS)
    group_index = {g: i for i, g in enumerate(group_order)}
    sorted_issues = sorted(issues, key=lambda i: (group_index.get(i["issue_group"], 999), i["issue_id"]))
    ay = {a["actor_id"]: i for i, a in enumerate(sorted_actors)}
    iy = {i["issue_id"]: np.interp(k, [0, max(1, len(sorted_issues) - 1)], [0, len(sorted_actors) - 1])
          for k, i in enumerate(sorted_issues)}

    fig, ax = plt.subplots(figsize=(21, 31))
    for edge in sorted(layered, key=lambda e: str(e["temporal_scope_v1"]) == "mixed_or_unclear"):
        x1, x2 = 0.27, 0.77
        y1, y2 = ay[str(edge["actor_id"])], iy[str(edge["issue_id"])]
        alpha = 0.66 if edge["review_layer"] == "human_reviewed" else 0.20
        width = 1.15 if edge["evidence_level"] == "E4" else 0.75 if edge["evidence_level"] == "E3" else 0.5
        ax.plot([x1, x2], [y1, y2], color=SCOPE_COLORS[str(edge["temporal_scope_v1"])],
                alpha=alpha, linewidth=width, zorder=1)

    for actor in sorted_actors:
        y = ay[actor["actor_id"]]
        family = CLASS_FAMILY.get(actor["actor_class"], "待人工分类")
        edgecolor = "#111111" if actor["review_status"] in HUMAN_STATUSES else "#8c9499"
        ax.scatter(0.27, y, s=25 + 11 * degree.get(actor["actor_id"], 0),
                   color=FAMILY_COLORS[family], edgecolor=edgecolor, linewidth=0.65, zorder=3)
        ax.text(0.255, y, f"{actor['actor_id']} {short(actor['canonical_name'], 29)}",
                ha="right", va="center", fontsize=6.6, color="#26343c")
    for issue in sorted_issues:
        y = iy[issue["issue_id"]]
        color = GROUP_COLORS.get(issue["issue_group"], "#777777")
        ax.scatter(0.77, y, s=88, color=color, edgecolor="#2d3439", linewidth=0.7, zorder=3)
        ax.text(0.785, y, f"{issue['issue_id']} {issue['issue_label']}", ha="left", va="center",
                fontsize=8.2, color="#26343c", fontweight="bold")

    ax.set_xlim(0, 1)
    ax.set_ylim(-2, len(sorted_actors) + 1)
    ax.invert_yaxis()
    ax.axis("off")
    isolated_count = len(actors) - len({str(edge["actor_id"]) for edge in layered})
    ax.set_title(f"R2｜完整 actor–issue 二模网络：{len(actors)} actors × {len(issues)} issues × {len(layered)} edges",
                 fontsize=20, loc="left", pad=24, fontweight="bold")
    ax.text(0.01, 1.002,
            f"左：全部 registry actors（含 {isolated_count} 个当前无 actor–issue edge 的孤立节点）；右：全部议题。深线＝已人审，浅线＝候选。",
            transform=ax.transAxes, fontsize=11, color="#52616b")
    scope_handles = [Line2D([0], [0], color=c, lw=3, label=l) for l, c in [
        ("长期定位／持续角色", SCOPE_COLORS["organizational_positioning"]),
        ("制度／案件角色", SCOPE_COLORS["institutional_or_case_role"]),
        ("事件性声明／署名／行动", SCOPE_COLORS["event_specific"]),
        ("当前文字不足以判断", SCOPE_COLORS["mixed_or_unclear"]),
    ]]
    ax.legend(handles=scope_handles, loc="lower center", bbox_to_anchor=(0.5, -0.018),
              ncol=4, frameon=False, fontsize=9.5)
    ax.text(0.01, -0.031,
            "解释边界：连线只表示来源支持的 actor–issue 关联；共同出现、署名或事件参与不等于组织间稳定联盟。",
            transform=ax.transAxes, fontsize=9.5, color="#66747d")
    fig.subplots_adjust(left=0.04, right=0.96, top=0.965, bottom=0.045)
    fig.savefig(OUT / "fig2_r02_full_bipartite_network.png", dpi=220)
    plt.close(fig)


def save_cooccurrence_figure(issues: list[dict[str, str]], co: list[dict[str, object]]) -> None:
    n = len(issues)
    ids = [i["issue_id"] for i in issues]
    labels = [i["issue_label"] for i in issues]
    idx = {issue_id: k for k, issue_id in enumerate(ids)}
    all_mat = np.zeros((n, n), dtype=int)
    human_mat = np.zeros((n, n), dtype=int)
    for row in co:
        i, j = idx[str(row["issue_id_1"])], idx[str(row["issue_id_2"])]
        all_mat[i, j] = all_mat[j, i] = int(row["shared_actor_count_all"])
        human_mat[i, j] = human_mat[j, i] = int(row["shared_actor_count_human_reviewed"])
    masked = np.ma.masked_where(all_mat == 0, all_mat)
    fig, ax = plt.subplots(figsize=(14.8, 13.6))
    ax.imshow(masked, cmap="YlGnBu", vmin=1, vmax=max(1, int(all_mat.max())), alpha=0.88)
    for i in range(n):
        for j in range(i + 1, n):
            if all_mat[i, j]:
                ax.text(j, i, f"{all_mat[i,j]}\nH{human_mat[i,j]}", ha="center", va="center",
                        fontsize=5.8, color="white" if all_mat[i, j] > all_mat.max() * 0.45 else "#24323a")
    ax.set_xticks(range(n), [f"{ids[i]}\n{labels[i]}" for i in range(n)], rotation=60, ha="right", fontsize=7.2)
    ax.set_yticks(range(n), [f"{ids[i]} {labels[i]}" for i in range(n)], fontsize=7.2)
    ax.set_title("R2｜议题共现：由同一 actor 连接的议题对", fontsize=18, loc="left", pad=24, fontweight="bold")
    ax.text(0, 1.025, "单元格：全部共享 actor 数；H＝两侧 actor–issue edge 均已人审的共享 actor 数。",
            transform=ax.transAxes, fontsize=10, color="#52616b")
    ax.text(0, -0.14,
            "共现反映组织议题组合，不表示组织之间结盟；事件性署名造成的共现需与长期组织定位分开阅读。",
            transform=ax.transAxes, fontsize=9.5, color="#66747d")
    for spine in ax.spines.values():
        spine.set_visible(False)
    fig.subplots_adjust(left=0.18, right=0.97, top=0.91, bottom=0.28)
    fig.savefig(OUT / "fig3_r02_issue_cooccurrence.png", dpi=240)
    plt.close(fig)


def save_bridge_figure(cross: list[dict[str, object]]) -> None:
    bridges = [r for r in cross if int(r["issue_count_all"]) >= 2]
    bridges.sort(key=lambda r: (-int(r["issue_count_human_reviewed"]), -int(r["issue_count_all"]), str(r["actor_id"])))
    top = bridges[:24][::-1]
    labels = [f"{r['actor_id']} {short(str(r['canonical_name']), 25)}" for r in top]
    y = np.arange(len(top))
    pos = np.array([int(r["issue_count_positioning"]) for r in top])
    case = np.array([int(r["issue_count_case_or_institutional"]) for r in top])
    event = np.array([int(r["issue_count_event_specific"]) for r in top])
    unclear = np.array([int(r["issue_count_mixed_or_unclear"]) for r in top])
    fig, ax = plt.subplots(figsize=(13.8, 10.8))
    left = np.zeros(len(top), dtype=int)
    for vals, scope, label in [
        (pos, "organizational_positioning", "长期定位／持续角色"),
        (case, "institutional_or_case_role", "制度／案件角色"),
        (event, "event_specific", "事件性"),
        (unclear, "mixed_or_unclear", "待判定"),
    ]:
        ax.barh(y, vals, left=left, color=SCOPE_COLORS[scope], label=label, height=0.68)
        left += vals
    for i, r in enumerate(top):
        ax.text(left[i] + 0.08, i, f"H{r['issue_count_human_reviewed']}", va="center", fontsize=8, color="#52616b")
    ax.set_yticks(y, labels, fontsize=8.5)
    ax.set_xlabel("不同议题数（同一议题在不同 scope 出现时可能重复分层计数）")
    ax.set_title("R2｜跨议题 actor：桥接机制而非单一排名", fontsize=18, loc="left", pad=24, fontweight="bold")
    ax.text(0, 1.025, "H＝已人审议题数。优先解释长期定位或制度角色；事件性桥接只说明公开参与。",
            transform=ax.transAxes, fontsize=10, color="#52616b")
    ax.grid(axis="x", color="#e1e6e9")
    ax.set_axisbelow(True)
    ax.legend(frameon=False, ncol=4, loc="lower center", bbox_to_anchor=(0.5, -0.14), fontsize=9)
    for spine in ["top", "right", "left"]:
        ax.spines[spine].set_visible(False)
    fig.subplots_adjust(left=0.31, right=0.96, top=0.90, bottom=0.17)
    fig.savefig(OUT / "fig4_r02_cross_issue_actors.png", dpi=240)
    plt.close(fig)


def make_hr019(
    class_mapping: list[dict[str, object]], cross: list[dict[str, object]],
    layered: list[dict[str, object]], actors: list[dict[str, str]],
) -> None:
    tasks: list[dict[str, object]] = []
    for row in class_mapping:
        if row["schema_status"] == "out_of_schema_term":
            tasks.append({
                "review_item_id": f"HR019-CLASS-{len(tasks)+1:02d}",
                "review_type": "actor_class_vocabulary",
                "object_id": row["actor_class_original"],
                "current_value": row["analysis_family_v1"],
                "question": "将该术语加入 actor_class 受控词，还是映射到现有宽类？",
                "recommended_option": "保留原术语并纳入受控词；生态图继续映射到 analysis_family_v1",
                "review_decision": "", "human_reviewer": "", "review_date": "", "review_notes": "",
            })
    off_review = [a for a in actors if a["review_status"] not in SCHEMA_REVIEW]
    for actor in off_review:
        tasks.append({
            "review_item_id": f"HR019-STATUS-{actor['actor_id']}",
            "review_type": "review_status_vocabulary",
            "object_id": actor["actor_id"], "current_value": actor["review_status"],
            "question": "watchlist_only 应作为 review_status，还是另设 watchlist 字段并将状态归入 needs_second_source？",
            "recommended_option": "另设 watchlist 维度；review_status 使用 schema 受控词",
            "review_decision": "", "human_reviewer": "", "review_date": "", "review_notes": "",
        })
    tasks.append({
        "review_item_id": "HR019-FAMILY-01", "review_type": "analysis_family_rule",
        "object_id": "CLASS_FAMILY_v1", "current_value": ";".join(FAMILY_ORDER[:-1]),
        "question": "是否批准本包的 10 个分析功能层用于 R1 图和报告？",
        "recommended_option": "批准为派生分析层；不覆盖 registry 原 actor_class",
        "review_decision": "", "human_reviewer": "", "review_date": "", "review_notes": "",
    })
    tasks, tasks_closed = preserve_completed_hr_queue(
        HR / "HR019_review_v0.csv", tasks,
        ["review_item_id", "review_type", "object_id", "current_value", "question",
         "recommended_option", "review_decision", "human_reviewer", "review_date", "review_notes"],
    )

    bridge_queue = [r for r in cross if r["narrative_status"] == "candidate_bridge_needs_review"]
    bridge_queue.sort(key=lambda r: (-int(r["issue_count_all"]), str(r["actor_id"])))
    bridge_rows = []
    for row in bridge_queue[:30]:
        bridge_rows.append({
            "actor_id": row["actor_id"], "canonical_name": row["canonical_name"],
            "issue_ids_all": row["issue_ids_all"], "issue_count_all": row["issue_count_all"],
            "bridge_classification_v1": row["bridge_classification_v1"],
            "actor_review_status": row["actor_review_status"],
            "review_question": "现有来源是否足以将其写入跨议题组织正文，且是否需限制为事件性／案件性角色？",
            "review_decision": "", "human_reviewer": "", "review_date": "", "review_notes": "",
        })
    bridge_rows, bridges_closed = preserve_completed_hr_queue(
        HR / "HR019_bridge_actor_review_queue_v0.csv", bridge_rows,
        ["actor_id", "canonical_name", "issue_ids_all", "issue_count_all", "bridge_classification_v1",
         "actor_review_status", "review_question", "review_decision", "human_reviewer", "review_date", "review_notes"],
    )

    unclear = [e for e in layered if e["temporal_scope_v1"] == "mixed_or_unclear"]
    unclear.sort(key=lambda e: (-EVIDENCE_RANK.get(str(e["evidence_level"]), 0), str(e["edge_id"])))
    scope_rows = []
    for edge in unclear:
        scope_rows.append({
            "edge_id": edge["edge_id"], "actor_id": edge["actor_id"], "actor_name": edge["actor_name"],
            "issue_id": edge["issue_id"], "issue_label": edge["issue_label"],
            "relation_basis_original": edge["relation_basis_original"],
            "evidence_level": edge["evidence_level"], "review_status": edge["review_status"],
            "review_question": "该 edge 应归为长期定位、制度／案件角色，还是事件性标签？",
            "review_decision": "", "human_reviewer": "", "review_date": "", "review_notes": "",
        })
    scope_rows, scopes_closed = preserve_completed_hr_queue(
        HR / "HR019_edge_scope_review_queue_v0.csv", scope_rows,
        ["edge_id", "actor_id", "actor_name", "issue_id", "issue_label", "relation_basis_original",
         "evidence_level", "review_status", "review_question", "review_decision", "human_reviewer",
         "review_date", "review_notes"],
    )
    closed = tasks_closed and bridges_closed and scopes_closed
    write_text(HR / "HR019_review_guide_v0.md", f"""
# HR-019｜R1/R2 分类与解释边界人工复核包

{"三张任务表均已由负责人完成；本轮重生只保留其历史决定，不重开或覆盖人工字段。" if closed else "本包不包含 AI 代替人审的决定；未完成人工字段保持空白。"}

## 三类复核记录

1. `HR019_review_v0.csv`：{len(tasks)} 个规则／受控词决定。
2. `HR019_bridge_actor_review_queue_v0.csv`：{len(bridge_rows)} 个跨议题 actor 的解释边界决定。
3. `HR019_edge_scope_review_queue_v0.csv`：{len(scope_rows)} 条 actor–issue edge 的时间／案件／事件范围决定；只审核解释层，不把它改写成组织间关系。

## 推荐决策值

- 受控词：`approve_extension` / `map_to_existing` / `needs_more_context`
- bridge：`include_with_scope` / `candidate_only` / `exclude_from_narrative`
- edge scope：`organizational_positioning` / `institutional_or_case_role` / `event_specific` / `remain_unclear`
""")


def make_brief(
    actors: list[dict[str, str]], issues: list[dict[str, str]], layered: list[dict[str, object]],
    class_mapping: list[dict[str, object]], cross: list[dict[str, object]],
    co: list[dict[str, object]], coverage: list[dict[str, object]], expansion: list[dict[str, object]],
) -> None:
    actors_with_edges = {str(e["actor_id"]) for e in layered}
    isolated = [a for a in actors if a["actor_id"] not in actors_with_edges]
    status_counts = Counter(str(e["review_layer"]) for e in layered)
    scope_counts = Counter(str(e["temporal_scope_v1"]) for e in layered)
    out_classes = [r for r in class_mapping if r["schema_status"] == "out_of_schema_term"]
    bridge_all = [r for r in cross if int(r["issue_count_all"]) >= 2]
    bridge_human = [r for r in cross if int(r["issue_count_human_reviewed"]) >= 2]
    bridge_position = [r for r in cross if r["bridge_classification_v1"] == "positioning_bridge"]
    top_co = co[:8]
    top_co_text = "\n".join(
        f"- `{r['issue_label_1']} × {r['issue_label_2']}`：{r['shared_actor_count_all']} 个共享 actor，"
        f"其中 {r['shared_actor_count_human_reviewed']} 个在两侧均已人审，{r['shared_actor_count_positioning']} 个在两侧均有长期定位标记。"
        for r in top_co
    )
    thin = [r for r in coverage if r["coverage_flag"] in {"thin", "thin_no_human_review", "no_edge"}]
    thin_text = "、".join(f"{r['issue_label']}({r['actor_count_all']})" for r in thin)
    isolated_text = "、".join(f"{a['actor_id']} {a['canonical_name']}" for a in isolated)
    top_human = sorted(bridge_human, key=lambda r: (-int(r["issue_count_human_reviewed"]), -int(r["issue_count_all"]), str(r["actor_id"])))[:12]
    top_human_text = "\n".join(
        f"- {r['actor_id']} {r['canonical_name']}：全部 {r['issue_count_all']} 个议题，双侧人审可用 {r['issue_count_human_reviewed']} 个；{r['bridge_classification_v1']}。"
        for r in top_human
    )
    expansion_dispositions = Counter(str(r["final_disposition"]) for r in expansion)
    write_text(OUT / "R01_R02_explanatory_brief_v1.md", f"""
# R1/R2 解释性验收 brief v1

## 验收结论

按《复归后冲绳民间组织 / NGO 分类与议题网络一期研究方案》的原始标准，R1/R2 已从“桥梁组织示例图”推进为可验收的完整 v1 包：R1 有 {len(actors)} 个 actor 的分类审计、标准化分析映射和组织生态图；R2 有 {len(actors)} actors × {len(issues)} issues 的完整二模网络、议题共现图、跨议题 actor 表和证据／时间范围分层。它仍是公开资料驱动的候选网络，不是冲绳组织总体名录，也不是稳定联盟图。

## Q1：冲绳有哪些相关民间组织？

当前 registry 有 {len(actors)} 个 actor，覆盖冲绳本地公民团体与 NPO、日本国内 NGO、国际倡议组织、法律网络、劳工／教育组织、女性／人权组织、基地社区服务与军属慈善、国际合作／公共外交项目，以及资助／赞助／公共机构节点。这个宽生态符合方案“不预设全部 actor 都是反基地阵营”的边界。

但“118”不是完成指标。{len(isolated)} 个 actor 尚无正式 actor–issue edge：{isolated_text}。其中多为最近扩入的宫古、劳工、女性、PFAS 和和平教育组织。它们已有 registry `issue_tags`，但这些标签不能自动当成 edge；必须逐条回到来源建立关系证据。因此，下一轮线上工作的第一优先级是补齐这 {len(isolated)} 个现有 actor 的 edge-level evidence，而不是机械补到 120。

## Q2 / R1：这些组织如何分类？

R1 采用“两层分类”：registry 保留具体 `actor_class`，生态图另建 10 个 `analysis_family_v1` 功能层。这样既能显示组织生态，又不会把法人身份、行动形态和政治立场压成一个标签。

- 当前共有 {len(class_mapping)} 个不同 `actor_class` 值，其中 {len(out_classes)} 个超出 `coding_schema_v0` 的建议词表，涉及 {sum(int(r['actor_count']) for r in out_classes)} 个 actor。它们不是自动错误，而是需要 HR-019 决定“扩充受控词”还是“映射到现有宽类”。
- “劳工／教育”“女性／人权／社区”作为独立分析层有解释价值，因为它们回答方案明确提出的组织类型问题；若直接并入 `local_civic_actor`，会丢失组织生态差异。
- 军属服务、慈善、公共外交和资助节点按实际功能单列，不推断亲基地或反基地立场。

## R2：哪些组织连接了哪些议题？

当前 actor–issue 表有 {len(layered)} 条 edge，连接 {len(actors_with_edges)} 个 actor 与 {len(issues)} 个议题；另有 {len(isolated)} 个 registry actor 在图中保留为孤立节点。按复核层，{status_counts['human_reviewed']} 条已人审，{status_counts['candidate']} 条仍是候选。按解释范围，{scope_counts['organizational_positioning']} 条暂归为长期组织定位／持续角色，{scope_counts['institutional_or_case_role']} 条为制度／案件角色，{scope_counts['event_specific']} 条为事件性声明／署名／行动，{scope_counts['mixed_or_unclear']} 条仍待判定。

这四层解决了旧 R2 的核心缺口：同一个 actor 同时出现于多个议题，并不自动证明它长期以这些议题为组织定位。`event_specific` 只能写成“公开参与某次声明／署名／行动”；`institutional_or_case_role` 只能写成“在某诉讼、服务或项目中承担公开角色”；只有来源支持使命、持续行动或组织目的时，才暂列 `organizational_positioning`。

当前共有 {len(bridge_all)} 个 actor 在 edge 表中连接至少两个议题，但只有 {len(bridge_human)} 个 actor 至少有两个议题在 edge 两侧均已人审，{len(bridge_position)} 个可暂归为长期定位型 bridge。正文优先使用双侧人审者：

{top_human_text or '- 当前没有满足条件的 actor。'}

## 议题转化的当前证据

共现最高的议题对如下。它们说明“同一 actor 的议题组合”，不表示 actor 之间结盟：

{top_co_text}

目前最稳妥的总体解释是：反基地议题不是孤立存在，而是经由三种不同机制被转译。第一，环保／生物多样性与边野古、大浦湾等地点议题结合；第二，噪声、生活安全与法律程序通过原告团和律师网络结合；第三，和平、人权、地方自治与国际倡议通过声明、网络使命或制度渠道结合。三种机制的证据形态不同，不能合并成一个“联盟强度”指标。

## 明显缺口与继续补材料的标准

- **数据联接缺口**：{len(isolated)} 个已登记 actor 没有 actor–issue edge。优先补来源摘录和 edge，不从 registry `issue_tags` 自动生成。
- **薄议题层**：当前 actor 数不超过 3 的议题为：{thin_text or '无'}。薄层中若又没有双侧人审，不能承担核心叙事。
- **分类词表缺口**：6 个超出 schema 的 actor_class 术语和 2 个 `watchlist_only` 状态需 HR-019 决策。
- **时间范围缺口**：{scope_counts['mixed_or_unclear']} 条 edge 仍无法从当前 `relation_basis` 稳妥区分长期／案件／事件；已全部进入 HR-019 scope queue。
- **历史覆盖缺口**：当前网络明显偏向可在线检索的近年行动、2010/2015/2020 联署和现存官网，不能据此描述 1972 年以来各时期的总体组织结构。

## Registry 扩样：数量从属于模块缺层

`registry_expansion_candidates_v1.csv` 现在是这批 **{len(expansion)} 行历史候选的 HR-013 最终处置账**，不是仍待补入的核心候选清单。其中 {expansion_dispositions['added_hr013']} 行已并入 registry（C011→A111），{expansion_dispositions['background_only_hr013']} 行只作背景节点（C010／C034），{expansion_dispositions['out_of_scope_hr013']} 行已因缺少一期直接连接而剔除（C029–C033），另有 {expansion_dispositions['defer']} 行 C015 因组织身份与独立二源不足继续 defer。背景与 rejected 项都没有继续扩表任务，C015 也不是 count-ready actor；它只能在身份、持续性及与“宮古島地下水研究会”的关系厘清后重新提交人审。当前扩表决定应读取独立的价值门槛包，不能把本表九行重新解释成 active shortlist。

## 图件怎么读

1. `fig1_r01_actor_ecology.png`：回答“有哪些组织、如何分类”，同时显示来源层和 actor-level 人审量。
2. `fig2_r02_full_bipartite_network.png`：方案要求的完整组织—议题二模网络；保留全部 {len(actors)} actors 和 {len(issues)} issues。
3. `fig3_r02_issue_cooccurrence.png`：显示同一 actor 连接的议题对，并单列双侧人审计数。
4. `fig4_r02_cross_issue_actors.png`：把 bridge 拆为长期定位、制度／案件、事件性和待判定四种机制。
""")


def main() -> None:
    configure_fonts()
    OUT.mkdir(parents=True, exist_ok=True)
    HR.mkdir(parents=True, exist_ok=True)
    actors = read_csv(REGISTRY)
    issues = read_csv(ISSUES)
    edges = read_csv(EDGES)
    actors_by_id = {a["actor_id"]: a for a in actors}
    issues_by_id = {i["issue_id"]: i for i in issues}

    assert len(actors) == len(actors_by_id), "duplicate actor_id"
    assert len(issues) == len(issues_by_id), "duplicate issue_id"
    assert all(e["actor_id"] in actors_by_id for e in edges), "edge actor missing from registry"
    assert all(e["issue_id"] in issues_by_id for e in edges), "edge issue missing from taxonomy"

    class_audit, class_mapping = actor_class_audit(actors)
    layered = build_layered_edges(edges, actors_by_id, issues_by_id)
    cross = build_cross_issue(actors, layered)
    co = build_cooccurrence(layered, issues)
    coverage = build_issue_coverage(issues, layered)
    expansion = build_expansion_candidates(actors_by_id)

    write_csv(
        DERIVED, layered,
        ["edge_id", "actor_id", "actor_name", "actor_class", "analysis_family_v1", "origin_type",
         "issue_id", "issue_label", "issue_group", "relation_basis_original", "temporal_scope_v1",
         "temporal_scope_rule", "source_ref", "evidence_level", "review_status", "review_layer",
         "conclusion_eligibility", "notes", "interpretation_limit"],
    )
    write_csv(
        OUT / "actor_class_audit_118_v1.csv", class_audit,
        ["actor_id", "canonical_name", "actor_class_original", "actor_class_term_status",
         "analysis_family_v1", "family_mapping_status", "origin_type", "evidence_level",
         "review_status_original", "review_status_term_status", "human_decision", "interpretation_limit"],
    )
    write_csv(
        OUT / "actor_class_controlled_mapping_v1.csv", class_mapping,
        ["actor_class_original", "actor_count", "schema_status", "analysis_family_v1", "actor_ids",
         "human_taxonomy_decision_required", "recommended_rule", "review_decision"],
    )
    write_csv(
        OUT / "cross_issue_actors_v1.csv", cross,
        ["actor_id", "canonical_name", "actor_class", "analysis_family_v1", "origin_type",
         "actor_review_status", "issue_count_all", "issue_ids_all", "issue_count_human_reviewed",
         "issue_ids_human_reviewed", "issue_count_positioning", "issue_ids_positioning",
         "issue_count_event_specific", "issue_ids_event_specific", "issue_count_case_or_institutional",
         "issue_ids_case_or_institutional", "issue_count_mixed_or_unclear", "bridge_classification_v1",
         "narrative_status"],
    )
    write_csv(
        OUT / "issue_cooccurrence_v1.csv", co,
        ["issue_id_1", "issue_label_1", "issue_id_2", "issue_label_2", "shared_actor_count_all",
         "shared_actor_ids_all", "shared_actor_count_human_reviewed", "shared_actor_ids_human_reviewed",
         "shared_actor_count_positioning", "shared_actor_ids_positioning", "shared_actor_count_event_only",
         "shared_actor_ids_event_only", "interpretation_limit"],
    )
    write_csv(
        OUT / "issue_coverage_audit_v1.csv", coverage,
        ["issue_id", "issue_label", "issue_group", "actor_count_all", "actor_count_human_reviewed",
         "actor_count_positioning", "actor_count_event_specific", "coverage_flag"],
    )
    write_csv(
        OUT / "registry_expansion_candidates_v1.csv", expansion,
        ["candidate_id", "proposed_id", "canonical_name", "actor_class_proposed", "origin_type",
         "primary_places", "issue_tags_candidate", "module_use_after_hr013", "source_url",
         "evidence_level_current", "final_review_status", "final_disposition", "registry_status",
         "remaining_task_status", "recommended_next_task", "decision_basis", "interpretation_limit"],
    )
    acceptance = [
        {
            "module": "R1", "plan_output": "组织分类表", "delivery_status": "delivered_v1",
            "deliverable": "actor_class_audit_118_v1.csv; actor_class_controlled_mapping_v1.csv",
            "acceptance_note": f"{len(actors)} actors audited; analysis mapping is separate from registry; HR-019 decisions remain blank",
        },
        {
            "module": "R1", "plan_output": "组织生态图", "delivery_status": "delivered_v1",
            "deliverable": "fig1_r01_actor_ecology.png",
            "acceptance_note": "10 functional layers by origin; human-review counts shown; sample ecology, not population proportions",
        },
        {
            "module": "R1", "plan_output": "重点组织清单", "delivery_status": "delivered_with_scope",
            "deliverable": "cross_issue_actors_v1.csv",
            "acceptance_note": f"priority list is mechanism-aware; {sum(int(r['issue_count_human_reviewed']) >= 2 for r in cross)} actors currently have at least two human-reviewed issues",
        },
        {
            "module": "R2", "plan_output": "组织—议题网络图", "delivery_status": "delivered_v1",
            "deliverable": "fig2_r02_full_bipartite_network.png; data/interim/24_r01_r02_actor_issue_layered_v0.csv",
            "acceptance_note": f"all {len(actors)} actors and all {len(issues)} issues retained; {len(layered)} edges split by review and temporal scope",
        },
        {
            "module": "R2", "plan_output": "议题共现图", "delivery_status": "delivered_v1",
            "deliverable": "fig3_r02_issue_cooccurrence.png; issue_cooccurrence_v1.csv",
            "acceptance_note": f"all {len(co)} observed issue pairs; human-reviewed and positioning counts remain separate",
        },
        {
            "module": "R2", "plan_output": "跨议题组织名单", "delivery_status": "delivered_v1",
            "deliverable": "cross_issue_actors_v1.csv; fig4_r02_cross_issue_actors.png",
            "acceptance_note": f"{sum(int(r['issue_count_all']) >= 2 for r in cross)} actors span at least two issues, but only {sum(int(r['issue_count_human_reviewed']) >= 2 for r in cross)} have at least two human-reviewed issue links",
        },
    ]
    write_csv(
        OUT / "module_acceptance_matrix_v1.csv", acceptance,
        ["module", "plan_output", "delivery_status", "deliverable", "acceptance_note"],
    )

    save_ecology_figure(actors)
    save_bipartite_figure(actors, issues, layered, cross)
    save_cooccurrence_figure(issues, co)
    save_bridge_figure(cross)
    make_hr019(class_mapping, cross, layered, actors)
    make_brief(actors, issues, layered, class_mapping, cross, co, coverage, expansion)

    metrics = [
        {"metric": "registry_actor_count", "value": len(actors)},
        {"metric": "actor_class_distinct_count", "value": len(class_mapping)},
        {"metric": "out_of_schema_actor_class_term_count", "value": sum(r["schema_status"] == "out_of_schema_term" for r in class_mapping)},
        {"metric": "issue_count", "value": len(issues)},
        {"metric": "actor_issue_edge_count", "value": len(layered)},
        {"metric": "actors_with_actor_issue_edge", "value": len({str(e["actor_id"]) for e in layered})},
        {"metric": "actors_without_actor_issue_edge", "value": len(actors) - len({str(e["actor_id"]) for e in layered})},
        {"metric": "human_reviewed_edge_count", "value": sum(e["review_layer"] == "human_reviewed" for e in layered)},
        {"metric": "candidate_edge_count", "value": sum(e["review_layer"] == "candidate" for e in layered)},
        {"metric": "issue_pair_with_shared_actor_count", "value": len(co)},
        {"metric": "cross_issue_actor_count", "value": sum(int(r["issue_count_all"]) >= 2 for r in cross)},
        {"metric": "double_human_reviewed_cross_issue_actor_count", "value": sum(int(r["issue_count_human_reviewed"]) >= 2 for r in cross)},
        {"metric": "expansion_disposition_audit_row_count", "value": len(expansion)},
        {"metric": "expansion_already_added_count", "value": sum(r["final_disposition"] == "added_hr013" for r in expansion)},
        {"metric": "expansion_background_only_count", "value": sum(r["final_disposition"] == "background_only_hr013" for r in expansion)},
        {"metric": "expansion_rejected_count", "value": sum(r["final_disposition"] == "out_of_scope_hr013" for r in expansion)},
        {"metric": "expansion_deferred_identity_count", "value": sum(r["final_disposition"] == "defer" for r in expansion)},
        {"metric": "active_expansion_candidate_count", "value": 0},
    ]
    write_csv(OUT / "validation_metrics_v1.csv", metrics, ["metric", "value"])
    write_text(OUT / "README.md", r"""
# R01/R02 actor–issue v1

This module package implements the original Phase-1 acceptance outputs for R1
and R2 without changing the central registry or source log. Run:

```powershell
python scripts\make_r01_r02_actor_issue.py
```

Primary reading order: `R01_R02_explanatory_brief_v1.md`, figures 1–4,
`validation_metrics_v1.csv`, then `HR019/HR019_review_guide_v0.md`.

All edge-based outputs preserve candidate/human-reviewed status. Event
participation and issue co-occurrence are not treated as stable alliances.
""")
    print(f"R1/R2 package built: {len(actors)} actors, {len(issues)} issues, {len(layered)} edges")


if __name__ == "__main__":
    main()
