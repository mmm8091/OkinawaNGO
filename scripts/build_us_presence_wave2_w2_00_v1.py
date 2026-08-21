from __future__ import annotations

import csv
import hashlib
import json
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "us_presence_network_wave2_w2_00_v1"

SUBPACKAGES = [
    (
        "W2-A",
        ROOT / "outputs" / "us_presence_network_wave2_w2_00_spouse_990_v1",
    ),
    (
        "W2-B",
        ROOT / "outputs" / "us_presence_network_wave2_w2_00_uso_v1",
    ),
    (
        "W2-C",
        ROOT
        / "outputs"
        / "us_presence_network_wave2_w2_00_system_accountability_v1",
    ),
]

SELECTION_SOURCE_FILES = [
    ROOT / "outputs" / "us_presence_network_wave1_v1" / "us_origin_actor_scope_v1.csv",
    ROOT
    / "outputs"
    / "research_wave_postfreeze_compatibility_v1"
    / "h2_accountability_actor_delta_v1.csv",
    ROOT
    / "outputs"
    / "translation_episode_comparison_v1"
    / "translation_episode_candidates_v1.csv",
]

ANCHOR_FIELDS = [
    "anchor_id",
    "work_package",
    "case_id",
    "metric",
    "level",
    "period_start",
    "period_end",
    "period_semantics",
    "value",
    "value_text",
    "unit",
    "currency",
    "definition",
    "denominator_id",
    "source_receipt_ids",
    "exact_locator",
    "anchor_status",
    "observed_local",
    "gap_type",
    "null_model",
    "allowed_claim",
    "prohibited_inference",
    "review_status",
    "package_scope",
    "frontend_eligibility",
    "central_writeback",
]

RECEIPT_FIELDS = [
    "receipt_id",
    "work_package",
    "publisher",
    "title",
    "source_family",
    "url",
    "retrieved_at",
    "artifact_path",
    "sha256",
    "mime_type",
    "exact_locator",
    "supports_anchor_ids",
    "archive_status",
    "notes",
    "package_scope",
    "frontend_eligibility",
    "central_writeback",
]

CHANGE_FIELDS = [
    "change_note_id",
    "work_package",
    "case_id",
    "topic",
    "changed_on",
    "original_assumption",
    "failure_reason",
    "revised_approach",
    "affected_anchor_ids",
    "source_receipt_ids",
    "effect_on_numbers",
    "effect_on_claims",
    "principal_decision_requirement",
    "status",
    "review_status",
    "package_scope",
]

LEGAL_REVIEW_STATUSES = {
    "ai_seeded",
    "human_checked",
    "human_revised",
    "needs_second_source",
    "needs_local_retrieval",
    "rejected",
}

FRAME_FIELDS = [
    "selection_frame_id",
    "research_question",
    "unit_of_analysis",
    "actor_universe_rule",
    "relation_families",
    "period_start",
    "period_end",
    "place_scope",
    "source_family_scope",
    "inclusion_rule",
    "exclusion_rule",
    "search_completion_status",
    "owner",
    "version",
    "principal_status",
    "package_scope",
    "frontend_eligibility",
    "central_writeback",
    "interpretation_limit",
]

PRINCIPAL_REVIEW_FIELDS = [
    "decision_id",
    "decision_type",
    "question",
    "recommended_decision",
    "alternative_or_competing_explanation",
    "anchor_ids",
    "source_receipt_ids",
    "what_this_unlocks",
    "principal_decision",
    "principal_note",
    "status",
    "package_scope",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def split_ids(value: str) -> list[str]:
    return [item.strip() for item in value.replace("|", ";").split(";") if item.strip()]


def normalize(
    rows: list[dict[str, str]], fields: list[str], work_package: str
) -> list[dict[str, str]]:
    normalized = []
    for raw in rows:
        row = {field: (raw.get(field) or "").strip() for field in fields}
        row["work_package"] = work_package
        if "package_scope" in row:
            row["package_scope"] = "research_only"
        if "frontend_eligibility" in row:
            row["frontend_eligibility"] = "not_frontend_ready"
        if "central_writeback" in row:
            row["central_writeback"] = "no"
        normalized.append(row)
    return normalized


def normalize_changes(rows: list[dict[str, str]], work_package: str) -> list[dict[str, str]]:
    normalized = []
    for raw in rows:
        row = {field: (raw.get(field) or "").strip() for field in CHANGE_FIELDS}
        row["work_package"] = work_package
        row["topic"] = (
            row["topic"]
            or (raw.get("scope") or "").strip()
            or (raw.get("change_type") or "").strip()
        )
        row["changed_on"] = row["changed_on"] or (raw.get("date") or "").strip()
        row["original_assumption"] = row["original_assumption"] or (
            raw.get("previous_assumption") or ""
        ).strip()
        row["failure_reason"] = (
            row["failure_reason"]
            or (raw.get("observed_problem") or "").strip()
            or (raw.get("trigger") or "").strip()
        )
        row["revised_approach"] = (
            row["revised_approach"]
            or (raw.get("revised_handling") or "").strip()
            or (raw.get("revised_rule") or "").strip()
            or (raw.get("revised_treatment") or "").strip()
        )
        row["source_receipt_ids"] = row["source_receipt_ids"] or (
            raw.get("evidence_receipt_ids") or ""
        ).strip()
        row["effect_on_numbers"] = row["effect_on_numbers"] or (
            raw.get("impact_on_outputs") or ""
        ).strip()
        row["principal_decision_requirement"] = row[
            "principal_decision_requirement"
        ] or (raw.get("requires_principal_decision") or "").strip()
        row["status"] = row["status"] or (raw.get("decision_status") or "").strip()
        row["review_status"] = (
            row["review_status"]
            if row["review_status"] in LEGAL_REVIEW_STATUSES
            else "ai_seeded"
        )
        row["package_scope"] = "research_only"
        normalized.append(row)
    return normalized


def selection_frames() -> list[dict[str, str]]:
    common = {
        "owner": "project_principal_user",
        "version": "1.0.0",
        "principal_status": "approved_research_frame",
        "package_scope": "research_only",
        "frontend_eligibility": "not_frontend_ready",
        "central_writeback": "no",
    }
    frames = [
        {
            "selection_frame_id": "USF-W2A-SPOUSE5-2026-08-22",
            "research_question": "五家军属组织如何筹集、分配并把资源送到基地内外 recipient？",
            "unit_of_analysis": "organization-filing;typed resource flow;recipient episode",
            "actor_universe_rule": "exact actor set X004;X005;X006;X007;X016",
            "relation_families": "money_flow;service_recipient;affiliation_control;person_actor_time",
            "period_start": "2021-01-01",
            "period_end": "2026-08-22",
            "place_scope": "Okinawa-based spouse clubs and named recipients",
            "source_family_scope": "IRS official filings;organization reports;recipient-side records",
            "inclusion_rule": "latest three available tax periods per organization when obtainable; each filing keeps its own tax period",
            "exclusion_rule": "no ecosystem total from mismatched tax periods; no unnamed Schedule B donor inference; no KOSC USD 2580 flow upgrade",
            "search_completion_status": "w2_00_initial_anchor_freeze",
            "interpretation_limit": "The five actors are a tracer set, not a census of the garrison service ecology.",
        },
        {
            "selection_frame_id": "USF-W2B-USO-LAYERS-2026-08-22",
            "research_question": "USO 全国财务、联邦 award、地区层和冲绳站点之间在哪一层能够闭合？",
            "unit_of_analysis": "national filing;federal award;regional unit;typed site presence",
            "actor_universe_rule": "USO national organization and X001 Okinawa presence; non-actor sites remain typed endpoints",
            "relation_families": "money_flow;official_award;service_presence;organization_hierarchy",
            "period_start": "2023-01-01",
            "period_end": "2026-08-22",
            "place_scope": "national;Indo-Pacific;Japan;Okinawa",
            "source_family_scope": "USO official financials and site pages;USAspending official award data",
            "inclusion_rule": "retain national, regional and local levels separately; preserve award period and site type",
            "exclusion_rule": "no equal-site allocation as a local estimate; no national award written as an Okinawa receipt",
            "search_completion_status": "w2_00_initial_anchor_freeze",
            "interpretation_limit": "A missing regional allocation is a visibility gap, not evidence of zero local resources.",
        },
        {
            "selection_frame_id": "USF-W2C-ENTRY13-2026-08-22",
            "research_question": "已经进入制度场域的行动分别留下哪些记录、救济和项目变化？",
            "unit_of_analysis": "action-institution episode across parallel outcome axes",
            "actor_universe_rule": "the 13 frozen translation episodes TE01-TE13; actor membership follows each episode",
            "relation_families": "action_institution;case_role;event_role;accountability_outcome",
            "period_start": "1997-01-01",
            "period_end": "2024-12-31",
            "place_scope": "Okinawa cases and their Japanese or international institutional venues",
            "source_family_scope": "court;administrative;referendum;official project and budget records",
            "inclusion_rule": "existing positive-entry sample; ENTRY and RECORD are selection conditions, not findings",
            "exclusion_rule": "no success rate for all civic action; four pending episodes remain visibly pending",
            "search_completion_status": "positive_entry_frame_frozen_negative_and_countercase_search_open",
            "interpretation_limit": "The frame is selected on institutional entry and cannot alone establish a general result ceiling.",
        },
        {
            "selection_frame_id": "USF-W2C-NONENTRY-MATCHED-2026-08-22",
            "research_question": "同类行动中哪些没有进入场域或没有留下制度记录？",
            "unit_of_analysis": "matched attempted action and intended institutional venue",
            "actor_universe_rule": "open matched sample by route, place, period and action type; every inclusion or exclusion is logged rather than retrofitted into TE01-TE13",
            "relation_families": "attempted_entry;venue_gate;accountability_outcome",
            "period_start": "1997-01-01",
            "period_end": "2025-12-31",
            "place_scope": "matched Okinawa base, deployment, environmental, noise and autonomy controversies",
            "source_family_scope": "official venue, docket, council, administrative, referendum or international-institution records plus action-side attempt records",
            "inclusion_rule": "documented attempt refused, blocked at a formal gate or lacking an expected record after a bounded official-source search",
            "exclusion_rule": "no attempted entry evidence; media-only advocacy; database absence treated as a real-world zero",
            "search_completion_status": "search_design_frozen_case_identification_not_started",
            "interpretation_limit": "Zero rows at W2-00 means matched-case identification has not begun, not that non-entry cases do not exist.",
        },
        {
            "selection_frame_id": "USF-W2C-PROJECTCHANGE-COUNTEREX-2026-08-22",
            "research_question": "哪些项目范围、地点、时序、预算或权限变化可能构成当前判断的反例？",
            "unit_of_analysis": "project-change candidate and attribution record",
            "actor_universe_rule": "open counterexample sample; project changes remain separate from NGO attribution",
            "relation_families": "project_change;accountability_outcome;attribution",
            "period_start": "1997-01-01",
            "period_end": "2025-12-31",
            "place_scope": "projects and deployments represented in or matched to the positive-entry frame",
            "source_family_scope": "official project plans, schedules, budgets, permits, authorities and attribution records",
            "inclusion_rule": "officially documented change on at least one PROJECT_* axis; attribution coded separately",
            "exclusion_rule": "technical, budgetary or government-driven change attributed to an NGO without causal evidence",
            "search_completion_status": "search_design_frozen_counterexample_identification_not_started",
            "interpretation_limit": "A project change is not an NGO effect unless ATTRIBUTION is independently supported.",
        },
        {
            "selection_frame_id": "USF-W2D-BRIDGE-TRACER15-2026-08-22",
            "research_question": "9 个服务 actor 与 6 个美国来源问责 actor 之间是否出现六类可核桥接？",
            "unit_of_analysis": "actor pair by relation family and observation window",
            "actor_universe_rule": "exact S0 nine plus A0 six from USF-US-ORIGIN17-2026-08-19",
            "relation_families": "direct_relation;shared_person;shared_recipient;shared_funder;event_coparticipation;shared_place_background",
            "period_start": "2023-01-01",
            "period_end": "2025-12-31",
            "place_scope": "Okinawa and directly linked organization or case records",
            "source_family_scope": "official rosters;applicable 990 filings;annual reports;case and recipient records",
            "inclusion_rule": "both endpoints need an activity anchor in-window before a negative pair result is countable",
            "exclusion_rule": "shared place is not a bridge; name similarity is not a shared person; co-event is not an alliance",
            "search_completion_status": "frame_frozen_audit_not_started",
            "interpretation_limit": "A bounded public-record zero is not a claim about all real-world relationships.",
        },
        {
            "selection_frame_id": "USF-W2D-ECOLOGY-S0-A1R-2026-08-22",
            "research_question": "服务侧 S0 与 41 个有人审议题锚点的问责 actor 在六类关系上的生态结构如何？",
            "unit_of_analysis": "actor and typed relation-family coverage",
            "actor_universe_rule": "exact S0 nine plus the frozen 41 A1R actors in the post-freeze H2 overlay",
            "relation_families": "direct_relation;shared_person;shared_recipient;shared_funder;event_coparticipation;shared_place_background",
            "period_start": "2023-01-01",
            "period_end": "2025-12-31",
            "place_scope": "Okinawa and directly linked organization or case records",
            "source_family_scope": "symmetric official-record source checklist by relation family",
            "inclusion_rule": "A1R requires at least one human-reviewed accountability anchor; S0 is the frozen nine-actor service set",
            "exclusion_rule": "new S1 actors require a new versioned frame; A1C actors stay outside confirmation counts",
            "search_completion_status": "frame_frozen_audit_not_started",
            "interpretation_limit": "The frame tests a reviewed-anchor ecology, not all Okinawa civic organizations.",
        },
        {
            "selection_frame_id": "USF-W2D-SENSITIVITY-S0-A1C-2026-08-22",
            "research_question": "两套生态的结构判断对 36 个 candidate-only 问责 actor 有多敏感？",
            "unit_of_analysis": "actor and typed relation-family exploratory coverage",
            "actor_universe_rule": "exact S0 nine plus frozen 36 A1C candidate-only actors",
            "relation_families": "direct_relation;shared_person;shared_recipient;shared_funder;event_coparticipation;shared_place_background",
            "period_start": "2023-01-01",
            "period_end": "2025-12-31",
            "place_scope": "Okinawa and directly linked organization or case records",
            "source_family_scope": "same source checklist as the confirmation frame where applicable",
            "inclusion_rule": "A1C has candidate accountability anchors but no human-reviewed anchor in the frozen overlay",
            "exclusion_rule": "results never enter confirmation counts without later fact review and a new frame version",
            "search_completion_status": "frame_frozen_exploratory_audit_not_started",
            "interpretation_limit": "This is a sensitivity frame and cannot upgrade candidate actor-issue links.",
        },
        {
            "selection_frame_id": "USF-W2-PUBLIC-RESOURCE-CONTEXT-2026-08-22",
            "research_question": "驻军体系公共支出在哪些官方层级可见，如何作为背景量尺而不被写成 NGO 资金？",
            "unit_of_analysis": "official budget, outlay, award or project-cost anchor",
            "actor_universe_rule": "no NGO universe; government and program endpoints remain research endpoints",
            "relation_families": "public_budget_context;official_award_context;project_cost_context",
            "period_start": "2019-01-01",
            "period_end": "2026-08-22",
            "place_scope": "Japan;Okinawa;Henoko and other named project scopes when officially separable",
            "source_family_scope": "DoD;USAspending;Japan MOD;Okinawa Defense Bureau official records",
            "inclusion_rule": "preserve budget, estimate, outlay, award and project-cost semantics separately",
            "exclusion_rule": "no government-to-NGO money edge without a separate recipient-level transaction record",
            "search_completion_status": "w2_00_initial_anchor_freeze",
            "interpretation_limit": "System-scale amounts are contextual denominators, not measures of NGO influence or funding.",
        },
    ]
    return [{**common, **frame} for frame in frames]


def selection_members() -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    us_scope = read_csv(
        ROOT / "outputs" / "us_presence_network_wave1_v1" / "us_origin_actor_scope_v1.csv"
    )
    h2_delta = read_csv(
        ROOT
        / "outputs"
        / "research_wave_postfreeze_compatibility_v1"
        / "h2_accountability_actor_delta_v1.csv"
    )
    episodes = read_csv(
        ROOT
        / "outputs"
        / "translation_episode_comparison_v1"
        / "translation_episode_candidates_v1.csv"
    )
    names = {
        row["actor_id"]: row["canonical_name"]
        for row in read_csv(ROOT / "data" / "interim" / "01_actor_registry_initial_v0.csv")
    }
    s0 = [row for row in us_scope if row["analytical_group"] == "service_charity_comparison"]
    a0 = [row for row in us_scope if row["analytical_group"] == "accountability_comparison"]
    a1r = [
        row
        for row in h2_delta
        if row["current_anchor_selection_evidence_status"]
        == "at_least_one_human_reviewed_anchor"
    ]
    a1c = [
        row
        for row in h2_delta
        if row["current_anchor_selection_evidence_status"] == "candidate_anchor_only"
    ]

    member_rows: list[dict[str, str]] = []

    def add_members(frame_id: str, rows: list[dict[str, str]], group: str, basis: str) -> None:
        for row in rows:
            actor_id = row["actor_id"]
            member_rows.append(
                {
                    "selection_frame_id": frame_id,
                    "actor_id": actor_id,
                    "actor_name": names.get(actor_id, row.get("canonical_name", row.get("actor_name", ""))),
                    "analytical_group": group,
                    "selection_basis": basis,
                    "membership_status": "frozen_member",
                    "package_scope": "research_only",
                    "frontend_eligibility": "not_frontend_ready",
                    "central_writeback": "no",
                }
            )

    spouse_ids = {"X004", "X005", "X006", "X007", "X016"}
    add_members(
        "USF-W2A-SPOUSE5-2026-08-22",
        [row for row in s0 if row["actor_id"] in spouse_ids],
        "spouse_club_tracer",
        "principal-approved exact five-actor tracer",
    )
    add_members(
        "USF-W2B-USO-LAYERS-2026-08-22",
        [row for row in s0 if row["actor_id"] == "X001"],
        "uso_okinawa_presence",
        "registry actor for the Okinawa presence; sites remain endpoints",
    )
    add_members(
        "USF-W2D-BRIDGE-TRACER15-2026-08-22",
        s0,
        "S0_service",
        "frozen service comparison group",
    )
    add_members(
        "USF-W2D-BRIDGE-TRACER15-2026-08-22",
        a0,
        "A0_accountability",
        "frozen U.S.-origin accountability comparison group",
    )
    add_members(
        "USF-W2D-ECOLOGY-S0-A1R-2026-08-22",
        s0,
        "S0_service",
        "frozen service comparison group",
    )
    add_members(
        "USF-W2D-ECOLOGY-S0-A1R-2026-08-22",
        a1r,
        "A1R_accountability_reviewed_anchor",
        "post-freeze H2 actor with at least one human-reviewed accountability anchor",
    )
    add_members(
        "USF-W2D-SENSITIVITY-S0-A1C-2026-08-22",
        s0,
        "S0_service",
        "frozen service comparison group",
    )
    add_members(
        "USF-W2D-SENSITIVITY-S0-A1C-2026-08-22",
        a1c,
        "A1C_accountability_candidate_anchor",
        "post-freeze H2 actor with candidate-only accountability anchors",
    )

    episode_rows = [
        {
            "selection_frame_id": "USF-W2C-ENTRY13-2026-08-22",
            "episode_id": row["episode_id"],
            "case_id": row["case_id"],
            "short_label": row["short_label"],
            "actor_ids": row["actor_ids"],
            "episode_status": row["review_status"],
            "fact_layer": (
                "candidate_event_layer"
                if row["review_status"] == "analytic_candidate_event_pending"
                else "reviewed_process_layer"
            ),
            "local_gap": (
                "yes"
                if row["review_status"] == "accepted_process_with_local_gap"
                else "no"
            ),
            "selection_basis": "existing positive institutional-entry episode",
            "package_scope": "research_only",
            "frontend_eligibility": "not_frontend_ready",
            "central_writeback": "no",
        }
        for row in episodes
    ]
    return member_rows, episode_rows


def case_scales() -> list[dict[str, str]]:
    return [
        {
            "scale_id": "W2SCALE-A",
            "case_id": "spouse_clubs",
            "target_population": "five selected organizations and their explicit recipients",
            "initial_independent_benchmark": "same-period population if available; per-organization filing revenue, expenses and grants",
            "initial_formula": "disclosed endpoint amount / disclosed outflow total",
            "initial_tolerance_or_band": "single-organization revenue USD 74k-327k; mismatched-period gross five-organization snapshot about USD 1.01m",
            "current_benchmark": "per-organization filing values and disclosed recipient/outflow coverage; no current population-normalized measure",
            "current_formula": "disclosed endpoint amount / same-filing disclosed outflow total; internal transfers deduplicated only for a declared ecology sum",
            "trigger_condition": "year-on-year change over 2x; duplicate internal transfer; endpoint coverage under 70 percent",
            "adaptation_rule": "retain original benchmark and add a change note if filing availability or lawful anonymity invalidates it",
            "status": "initial_scale_registered",
            "package_scope": "research_only",
        },
        {
            "scale_id": "W2SCALE-B",
            "case_id": "uso",
            "target_population": "USO national-region-Okinawa hierarchy",
            "initial_independent_benchmark": "national program expense / same-definition service uses",
            "initial_formula": "national unit benchmark x comparable Okinawa uses, only if comparable local uses exist",
            "initial_tolerance_or_band": "national program services about USD 204.9m and 11.3m uses; local allocation unknown",
            "current_benchmark": "national program-service and service-use anchors plus explicit national-region-local visibility gaps",
            "current_formula": "no Okinawa allocation until a comparable regional or local denominator exists",
            "trigger_condition": "regional allocation absent; site definitions conflict; local uses missing",
            "adaptation_rule": "replace service-use weighting when a superior regional or program denominator is found; preserve the old result in a change note",
            "status": "initial_scale_registered",
            "package_scope": "research_only",
        },
        {
            "scale_id": "W2SCALE-C",
            "case_id": "accountability",
            "target_population": "positive entry episodes plus matched non-entry and project-change countercases",
            "initial_independent_benchmark": "parallel outcome axes against official project and decision records",
            "initial_formula": "no single success score; code ENTRY, RECORD, RELIEF, PROJECT_* and ATTRIBUTION separately",
            "initial_tolerance_or_band": "13 positive-entry episodes and 6 cases/27 roles are the starting frame",
            "current_benchmark": "parallel outcome axes with a separate open matched-negative and project-change frame",
            "current_formula": "retain axis-specific values; do not collapse them into one ordinal success score",
            "trigger_condition": "non-entry match found; project-change countercase found; attribution conflict",
            "adaptation_rule": "expand matched samples with logged inclusion and exclusion changes; do not rewrite the original 13-frame denominator",
            "status": "initial_scale_registered",
            "package_scope": "research_only",
        },
        {
            "scale_id": "W2SCALE-PUBLIC",
            "case_id": "public_resource_context",
            "target_population": "official U.S.-Japan garrison and project public-resource records",
            "initial_independent_benchmark": "DoD/USAspending and Japan MOD/Okinawa Defense Bureau categories kept separate",
            "initial_formula": "none until budget, estimate, outlay, award and project-cost semantics align",
            "initial_tolerance_or_band": "W2-00 freezes official categories rather than producing an NGO funding ratio",
            "current_benchmark": "official category-level amounts with level, period and semantics preserved",
            "current_formula": "none; display the public-record waterfall and the level at which allocation stops",
            "trigger_condition": "national amount cannot resolve to Okinawa; budget/outlay/award semantics conflict",
            "adaptation_rule": "show the level at which public records stop; do not manufacture a local allocation",
            "status": "initial_scale_registered",
            "package_scope": "research_only",
        },
    ]


def principal_review_queue() -> list[dict[str, str]]:
    common = {
        "principal_decision": "",
        "principal_note": "",
        "status": "pending_principal_review",
        "package_scope": "research_only",
    }
    rows = [
        {
            "decision_id": "W2-00-PR001",
            "decision_type": "method_boundary",
            "question": "是否确认当前同年同定义的全冲绳美方相关人口分母尚未闭合，W2-A／W2-B 暂不发布当前人均数？",
            "recommended_decision": "confirm_no_current_per_capita_denominator",
            "alternative_or_competing_explanation": "47,300 是 2011 年历史同口径；47,000 是医疗服务人口；57,100 是未完整列项的机械小计；“接近 80,000”无同口径观察日。",
            "anchor_ids": "W2C-A001;W2C-A002;W2C-A007;W2C-A008;W2C-A017",
            "source_receipt_ids": "W2C-SR001;W2C-SR002;W2C-SR003;W2C-SR004",
            "what_this_unlocks": "W2-A／W2-B 改用总额、申报内覆盖率与端点覆盖率继续。",
        },
        {
            "decision_id": "W2-00-PR002",
            "decision_type": "sensitive_money_relation",
            "question": "是否将 OESC→AWWA 新补的两个税期 USD 16,308 与 USD 14,371 与既有 USD 8,479 一并确认为三税期连续申报的 recipient 关系？",
            "recommended_decision": "accept_two_earlier_schedule_i_rows_as_human_checked",
            "alternative_or_competing_explanation": "三行只证明三个税期的 Schedule I 申报，不证明资金最初来源、AWWA 下游去向或更长期连续性。",
            "anchor_ids": "W2A-A076;W2A-A077;W2A-A078",
            "source_receipt_ids": "W2A-SR012;W2A-SR013;W2A-SR014",
            "what_this_unlocks": "W2-A 可将该关系作为 AWWA 中介结构的时间化主干。",
        },
        {
            "decision_id": "W2-00-PR003",
            "decision_type": "recipient_tracer_scope",
            "question": "AWWA 申报中六个具名日本侧 recipient descriptor 是否全部进入 W2-A 身份、收款端与 LEG2 地方回应补查？",
            "recommended_decision": "advance_all_six_as_research_tracers_not_central_facts",
            "alternative_or_competing_explanation": "申报原文能证明名称描述与金额同列，但仍可能存在正式名称、翻译、机构同一性或金额范围问题。",
            "anchor_ids": "W2A-A070;W2A-A071;W2A-A072;W2A-A073;W2A-A074;W2A-A075",
            "source_receipt_ids": "W2A-SR001;W2A-SR002",
            "what_this_unlocks": "W2-A 的 recipient identity、受赠端反向证据、LEG2 与金额去重。",
        },
        {
            "decision_id": "W2-00-PR004",
            "decision_type": "scale_and_filing_semantics",
            "question": "是否只以“五家最新申报的跨税期毛运作量级”使用四项机械合计，同时继续暂缓 KOSC USD 2,580，并将 MOSCO 最新 grants 元素保持为缺失而非 0？",
            "recommended_decision": "accept_mixed_period_diagnostic_with_exact_label_keep_kosc_deferred_keep_mosco_missing",
            "alternative_or_competing_explanation": "税期错位、OESC→AWWA 内部转移与 990／990-EZ 字段差异都会制造虚假合并总量。",
            "anchor_ids": "W2A-A080;W2A-A081;W2A-A082;W2A-A083",
            "source_receipt_ids": "W2A-SR002;W2A-SR005;W2A-SR008;W2A-SR011;W2A-SR014",
            "what_this_unlocks": "W2-A 可做三税期组织比较，但不得称为年度生态预算。",
        },
        {
            "decision_id": "W2-00-PR005",
            "decision_type": "uso_reporting_and_site_semantics",
            "question": "是否确认 USO 2024 审计合并财报与 USO Inc. Form 990 为两套并列报告边界，并以 6 个 operating centers＋AMC terminal＋area office 解释 8 个 typed presences？",
            "recommended_decision": "accept_two_financial_perimeters_and_six_center_eight_presence_typing",
            "alternative_or_competing_explanation": "两套财务数不同主要来自报告边界；6 与 8 的差异来自站点类型，不是两套组织。",
            "anchor_ids": "W2B-A001;W2B-A003;W2B-A004;W2B-A006;W2B-A007;W2B-A008;W2B-A016;W2B-A020",
            "source_receipt_ids": "W2B-SR002;W2B-SR003;W2B-SR005;W2B-SR006",
            "what_this_unlocks": "W2-B 可比较层级、服务量与站点功能，但不相加财务数，不均分八站点。",
        },
        {
            "decision_id": "W2-00-PR006",
            "decision_type": "official_award_boundary",
            "question": "是否只将 USD 72m 确认为 DoD／WHS→USO Inc. 全国 prime award，将 USD 41.212m 保留为字段语义冲突，不生成 DoD→USO Okinawa 关系？",
            "recommended_decision": "accept_national_prime_award_only_and_preserve_local_allocation_gap",
            "alternative_or_competing_explanation": "0 subaward 不能排除内部地区分配、采购、报销或 interoffice transfer；公开记录缺失也不等于冲绳获得 0。",
            "anchor_ids": "W2B-A021;W2B-A022;W2B-A024;W2B-A025;W2B-A028;W2B-A030;W2B-A032",
            "source_receipt_ids": "W2B-SR007;W2B-SR008;W2B-SR009;W2B-SR010;W2B-SR011",
            "what_this_unlocks": "W2-B 继续查 eligible geography 与地区分配；若仍无，交付全国资金可见／本地分配断裂瀑布图。",
        },
        {
            "decision_id": "W2-00-PR007",
            "decision_type": "accountability_comparison_design",
            "question": "是否正式将问责线从 13 个正向入场 episode 改为“正向入场＋匹配未入场＋项目改变反例”三组并列比较？",
            "recommended_decision": "approve_three_frame_accountability_comparison_and_pause_general_result_ceiling_claim",
            "alternative_or_competing_explanation": "13 例按入场选择；Dugong 两个金额差 USD 3,654.50 原因未明；JPY 930bn 是概算，JPY 648.3bn 在已核记者会中是记者前提；项目变化也可能由技术、预算或政府内部决定导致。",
            "anchor_ids": "W2C-A020;W2C-A021;W2C-A022;W2C-A030;W2C-A041",
            "source_receipt_ids": "W2C-SR010;W2C-SR011;W2C-SR012;W2C-SR013;W2C-SR014",
            "what_this_unlocks": "W2-C 按 ENTRY／RECORD／RELIEF／PROJECT_*／ATTRIBUTION 分轴编码，并启动负案例与反例检索。",
        },
    ]
    return [{**common, **row} for row in rows]


def protected_hashes() -> list[dict[str, str]]:
    paths = [
        "data/interim/01_actor_registry_initial_v0.csv",
        "data/interim/05_source_log_initial_v0.csv",
        "data/interim/07_actor_issue_edges_initial_v0.csv",
        "data/interim/15_funding_or_support_edges_sample_v0.csv",
        "prototypes/nr3_explorer/dist/release.json",
    ]
    rows = []
    for rel in paths:
        path = ROOT / rel
        rows.append(
            {
                "path": rel,
                "exists": "yes" if path.exists() else "no",
                "sha256": sha256(path) if path.exists() else "",
            }
        )
    return rows


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    anchors: list[dict[str, str]] = []
    receipts: list[dict[str, str]] = []
    changes: list[dict[str, str]] = []
    input_files: list[Path] = []
    for work_package, directory in SUBPACKAGES:
        for filename, fields, collector in [
            ("anchor_candidates_v1.csv", ANCHOR_FIELDS, anchors),
            ("source_receipts_v1.csv", RECEIPT_FIELDS, receipts),
        ]:
            path = directory / filename
            if not path.exists():
                raise FileNotFoundError(f"missing W2-00 subpackage input: {path}")
            input_files.append(path)
            collector.extend(normalize(read_csv(path), fields, work_package))
        change_path = directory / "change_notes_v1.csv"
        if not change_path.exists():
            raise FileNotFoundError(f"missing W2-00 subpackage input: {change_path}")
        input_files.append(change_path)
        changes.extend(normalize_changes(read_csv(change_path), work_package))
        for path in sorted(directory.rglob("*")):
            if path.is_file() and path not in input_files:
                input_files.append(path)
    for path in SELECTION_SOURCE_FILES:
        if not path.exists():
            raise FileNotFoundError(f"missing W2-00 selection source input: {path}")
        input_files.append(path)

    frames = selection_frames()
    actor_members, episode_members = selection_members()
    scales = case_scales()
    review_queue = principal_review_queue()

    write_csv(OUT / "selection_frames_v1.csv", FRAME_FIELDS, frames)
    write_csv(
        OUT / "selection_frame_actor_members_v1.csv",
        [
            "selection_frame_id",
            "actor_id",
            "actor_name",
            "analytical_group",
            "selection_basis",
            "membership_status",
            "package_scope",
            "frontend_eligibility",
            "central_writeback",
        ],
        actor_members,
    )
    write_csv(
        OUT / "selection_frame_episode_members_v1.csv",
        [
            "selection_frame_id",
            "episode_id",
            "case_id",
            "short_label",
            "actor_ids",
            "episode_status",
            "fact_layer",
            "local_gap",
            "selection_basis",
            "package_scope",
            "frontend_eligibility",
            "central_writeback",
        ],
        episode_members,
    )
    write_csv(OUT / "anchor_ledger_v1.csv", ANCHOR_FIELDS, anchors)
    write_csv(OUT / "source_receipts_v1.csv", RECEIPT_FIELDS, receipts)
    write_csv(OUT / "change_notes_v1.csv", CHANGE_FIELDS, changes)
    write_csv(
        OUT / "case_scale_registry_v1.csv",
        [
            "scale_id",
            "case_id",
            "target_population",
            "initial_independent_benchmark",
            "initial_formula",
            "initial_tolerance_or_band",
            "current_benchmark",
            "current_formula",
            "trigger_condition",
            "adaptation_rule",
            "status",
            "package_scope",
        ],
        scales,
    )
    write_csv(
        OUT / "principal_review_queue_v1.csv",
        PRINCIPAL_REVIEW_FIELDS,
        review_queue,
    )
    current_protected = protected_hashes()
    write_csv(
        OUT / "protected_input_hashes_v1.csv",
        ["path", "exists", "sha256"],
        current_protected,
    )

    anchor_ids = [row["anchor_id"] for row in anchors]
    receipt_ids = [row["receipt_id"] for row in receipts]
    change_ids = [row["change_note_id"] for row in changes]
    errors: list[str] = []
    preflight_path = OUT / "preflight_protected_hashes_v1.csv"
    if not preflight_path.exists():
        errors.append("missing preflight protected hashes")
    else:
        preflight = {row["path"]: row["sha256"] for row in read_csv(preflight_path)}
        current = {row["path"]: row["sha256"] for row in current_protected}
        for path, expected_hash in preflight.items():
            if current.get(path) != expected_hash:
                errors.append(f"protected input changed during W2-00: {path}")
    if len(anchor_ids) != len(set(anchor_ids)):
        errors.append("duplicate anchor_id")
    if len(receipt_ids) != len(set(receipt_ids)):
        errors.append("duplicate receipt_id")
    if len(change_ids) != len(set(change_ids)):
        errors.append("duplicate change_note_id")
    for row in anchors:
        if row["review_status"] not in LEGAL_REVIEW_STATUSES:
            errors.append(
                f"{row['anchor_id']} illegal review_status: {row['review_status']}"
            )
    anchor_set = set(anchor_ids)
    receipt_set = set(receipt_ids)
    anchor_receipt_pairs: set[tuple[str, str]] = set()
    receipt_anchor_pairs: set[tuple[str, str]] = set()
    for row in anchors:
        row_receipts = set(split_ids(row["source_receipt_ids"]))
        unknown = row_receipts - receipt_set
        if unknown:
            errors.append(f"{row['anchor_id']} unknown source receipts: {sorted(unknown)}")
        anchor_receipt_pairs.update((row["anchor_id"], receipt_id) for receipt_id in row_receipts)
    for row in receipts:
        row_anchors = set(split_ids(row["supports_anchor_ids"]))
        unknown = row_anchors - anchor_set
        if unknown:
            errors.append(f"{row['receipt_id']} unknown anchors: {sorted(unknown)}")
        receipt_anchor_pairs.update((anchor_id, row["receipt_id"]) for anchor_id in row_anchors)
        artifact = row["artifact_path"]
        if artifact:
            path = ROOT / artifact
            if not path.exists():
                errors.append(f"{row['receipt_id']} artifact missing: {artifact}")
            elif not row["sha256"]:
                errors.append(f"{row['receipt_id']} artifact has no SHA-256: {artifact}")
            elif sha256(path) != row["sha256"]:
                errors.append(f"{row['receipt_id']} artifact hash mismatch: {artifact}")
        elif row["sha256"]:
            errors.append(f"{row['receipt_id']} has SHA-256 but no artifact path")
        elif not row["url"] or not row["archive_status"]:
            errors.append(
                f"{row['receipt_id']} has no local artifact and lacks URL/archive status"
            )
    missing_receipt_backlinks = anchor_receipt_pairs - receipt_anchor_pairs
    missing_anchor_backlinks = receipt_anchor_pairs - anchor_receipt_pairs
    if missing_receipt_backlinks:
        errors.append(
            "receipt rows missing supports_anchor_ids backlinks: "
            + repr(sorted(missing_receipt_backlinks))
        )
    if missing_anchor_backlinks:
        errors.append(
            "anchor rows missing source_receipt_ids backlinks: "
            + repr(sorted(missing_anchor_backlinks))
        )
    for row in changes:
        unknown_anchors = set(split_ids(row["affected_anchor_ids"])) - anchor_set
        if unknown_anchors:
            errors.append(
                f"{row['change_note_id']} unknown affected anchors: {sorted(unknown_anchors)}"
            )
        unknown_receipts = set(split_ids(row["source_receipt_ids"])) - receipt_set
        if unknown_receipts:
            errors.append(
                f"{row['change_note_id']} unknown source receipts: {sorted(unknown_receipts)}"
            )
    review_ids = [row["decision_id"] for row in review_queue]
    if len(review_ids) != len(set(review_ids)):
        errors.append("duplicate principal review decision_id")
    for row in review_queue:
        unknown_anchors = set(split_ids(row["anchor_ids"])) - anchor_set
        if unknown_anchors:
            errors.append(
                f"{row['decision_id']} unknown review anchors: {sorted(unknown_anchors)}"
            )
        unknown_receipts = set(split_ids(row["source_receipt_ids"])) - receipt_set
        if unknown_receipts:
            errors.append(
                f"{row['decision_id']} unknown review receipts: {sorted(unknown_receipts)}"
            )

    expected_frame_counts = {
        "USF-W2A-SPOUSE5-2026-08-22": 5,
        "USF-W2B-USO-LAYERS-2026-08-22": 1,
        "USF-W2D-BRIDGE-TRACER15-2026-08-22": 15,
        "USF-W2D-ECOLOGY-S0-A1R-2026-08-22": 50,
        "USF-W2D-SENSITIVITY-S0-A1C-2026-08-22": 45,
    }
    actual_counts = {
        frame_id: sum(row["selection_frame_id"] == frame_id for row in actor_members)
        for frame_id in expected_frame_counts
    }
    for frame_id, expected in expected_frame_counts.items():
        if actual_counts[frame_id] != expected:
            errors.append(
                f"{frame_id} member count {actual_counts[frame_id]} != expected {expected}"
            )
    us_scope = read_csv(SELECTION_SOURCE_FILES[0])
    h2_delta = read_csv(SELECTION_SOURCE_FILES[1])
    expected_s0 = {
        row["actor_id"]
        for row in us_scope
        if row["analytical_group"] == "service_charity_comparison"
    }
    expected_a0 = {
        row["actor_id"]
        for row in us_scope
        if row["analytical_group"] == "accountability_comparison"
    }
    expected_a1r = {
        row["actor_id"]
        for row in h2_delta
        if row["current_anchor_selection_evidence_status"]
        == "at_least_one_human_reviewed_anchor"
    }
    expected_a1c = {
        row["actor_id"]
        for row in h2_delta
        if row["current_anchor_selection_evidence_status"] == "candidate_anchor_only"
    }

    def actual_frame_set(frame_id: str) -> set[str]:
        return {
            row["actor_id"]
            for row in actor_members
            if row["selection_frame_id"] == frame_id
        }

    expected_member_sets = {
        "USF-W2A-SPOUSE5-2026-08-22": {"X004", "X005", "X006", "X007", "X016"},
        "USF-W2B-USO-LAYERS-2026-08-22": {"X001"},
        "USF-W2D-BRIDGE-TRACER15-2026-08-22": expected_s0 | expected_a0,
        "USF-W2D-ECOLOGY-S0-A1R-2026-08-22": expected_s0 | expected_a1r,
        "USF-W2D-SENSITIVITY-S0-A1C-2026-08-22": expected_s0 | expected_a1c,
    }
    for frame_id, expected_set in expected_member_sets.items():
        actual_set = actual_frame_set(frame_id)
        if actual_set != expected_set:
            errors.append(
                f"{frame_id} exact member mismatch: missing={sorted(expected_set - actual_set)} extra={sorted(actual_set - expected_set)}"
            )
    if expected_a1r & expected_a1c:
        errors.append(
            f"A1R and A1C overlap unexpectedly: {sorted(expected_a1r & expected_a1c)}"
        )
    registry = read_csv(ROOT / "data" / "interim" / "01_actor_registry_initial_v0.csv")
    active_registry_ids = {
        row["actor_id"]
        for row in registry
        if row["actor_id"] != "A072" and row.get("scope_status", "") != "merged_duplicate"
    }
    unknown_member_ids = {row["actor_id"] for row in actor_members} - active_registry_ids
    if unknown_member_ids:
        errors.append(
            f"selection members not in active registry: {sorted(unknown_member_ids)}"
        )
    if len(episode_members) != 13:
        errors.append(f"positive-entry episode count {len(episode_members)} != 13")
    episode_actor_ids = {
        actor_id
        for row in episode_members
        for actor_id in split_ids(row["actor_ids"])
    }
    if any(row["actor_id"] == "A072" for row in actor_members) or "A072" in episode_actor_ids:
        errors.append("A072 tombstone leaked into actor or episode selection frames")

    report = {
        "schema_version": "1.0.0",
        "generated_on": str(date.today()),
        "status": "PASS_W2_00_RESEARCH_ONLY" if not errors else "FAIL",
        "counts": {
            "selection_frames": len(frames),
            "selection_frame_actor_members": len(actor_members),
            "selection_frame_episode_members": len(episode_members),
            "anchors": len(anchors),
            "source_receipts": len(receipts),
            "source_receipts_with_local_artifact": sum(
                bool(row["artifact_path"]) for row in receipts
            ),
            "source_receipts_without_local_artifact": sum(
                not bool(row["artifact_path"]) for row in receipts
            ),
            "change_notes": len(changes),
            "case_scales": len(scales),
            "principal_review_items": len(review_queue),
        },
        "frame_actor_counts": actual_counts,
        "checks": {
            "unique_anchor_ids": len(anchor_ids) == len(set(anchor_ids)),
            "unique_receipt_ids": len(receipt_ids) == len(set(receipt_ids)),
            "unique_change_note_ids": len(change_ids) == len(set(change_ids)),
            "receipt_ids_resolve": not any("unknown" in error for error in errors),
            "receipt_crosswalk_closed": not any("unknown" in error for error in errors)
            and not missing_receipt_backlinks
            and not missing_anchor_backlinks,
            "receipt_crosswalk_bidirectional": not missing_receipt_backlinks
            and not missing_anchor_backlinks,
            "available_artifact_hashes_checked": True,
            "selection_frame_counts_checked": True,
            "selection_frame_exact_member_sets_checked": not any(
                "exact member mismatch" in error for error in errors
            ),
            "a1r_a1c_disjoint": not bool(expected_a1r & expected_a1c),
            "active_registry_mapping_checked": not bool(unknown_member_ids),
            "a072_excluded": not any("A072 tombstone" in error for error in errors),
            "principal_review_crosswalk_closed": not any(
                "review anchors" in error or "review receipts" in error
                for error in errors
            ),
            "protected_inputs_unchanged": not any(
                error.startswith("protected input changed") for error in errors
            ),
            "central_writeback": False,
            "frontend_release": False,
        },
        "errors": errors,
    }
    (OUT / "validation_report_v1.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    output_files = sorted(
        path for path in OUT.iterdir() if path.is_file() and path.name != "manifest.json"
    )
    manifest = {
        "schema_version": "1.0.0",
        "package": "us_presence_network_wave2_w2_00_v1",
        "generated_on": str(date.today()),
        "status": report["status"],
        "scope": "research_only",
        "central_writeback": False,
        "frontend_release": False,
        "inputs": [
            {
                "path": path.relative_to(ROOT).as_posix(),
                "sha256": sha256(path),
            }
            for path in input_files
        ],
        "files": [
            {
                "path": path.relative_to(ROOT).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
            for path in output_files
        ],
    }
    (OUT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    if errors:
        raise SystemExit("\n".join(errors))
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
