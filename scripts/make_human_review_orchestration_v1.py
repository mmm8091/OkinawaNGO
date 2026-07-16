from __future__ import annotations

"""Build the HR016–HR032 human-review orchestration package.

The script is deliberately read-only with respect to all HR queues and central
research tables. It inventories current blank human-decision rows, derives
report gates from the report assembly manifests, and writes only the dedicated
orchestration output directory.
"""

import csv
from dataclasses import dataclass
from pathlib import Path
from textwrap import dedent

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "human_review_orchestration_v1"
MANIFEST_PATH = ROOT / "outputs" / "report_assembly_v1" / "figure_manifest_v1.csv"
MISSING_PATH = ROOT / "outputs" / "report_assembly_v1" / "missing_assets_v1.csv"

INVENTORY_PATH = OUT / "task_inventory_v1.csv"
BATCH_PATH = OUT / "recommended_batches_v1.csv"
GRAPH_SVG_PATH = OUT / "dependency_graph_v1.svg"
GRAPH_PNG_PATH = OUT / "dependency_graph_v1.png"
README_PATH = OUT / "README.md"


@dataclass(frozen=True)
class FileSpec:
    path: str
    decision_mode: str = "field"
    decision_fields: tuple[str, ...] = ()
    local_field: str = ""
    local_value: str = ""


TASKS: dict[str, dict[str, object]] = {
    "HR016": {
        "name": "先岛框架语义与来源定位",
        "priority": "P1",
        "work_lane": "online_human",
        "files": [FileSpec(
            "outputs/R04_sakishima_frame_corpus_v0/hr016_review_items_v0.csv",
            decision_fields=("review_decision",),
        )],
        "hard": "none",
        "recommended": "before final Sakishima dossier assembly",
        "central": "R4 formal safe-fact/entity–frame/source-locator layer; no automatic registry merge",
        "module_figures": "R4 entity–frame figure; three-place source/frame figure; R4 brief",
        "rerun": "merge accepted/revised R4 facts and locators, then regenerate R4 figures/brief and MA020",
        "issue": "none",
        "boundary": "Named legislators, anonymous residents, administrative nodes and persistent organizations remain distinct.",
    },
    "HR017": {
        "name": "公投程序阶段与角色扩展层",
        "priority": "P1",
        "work_lane": "mixed_online_local",
        "files": [FileSpec(
            "outputs/R09_referendum_process_v0/hr017_review_queue_v0.csv",
            decision_fields=("decision",),
            local_field="needs_local_retrieval",
            local_value="yes",
        )],
        "hard": "per-row local evidence for 9 flagged rows",
        "recommended": "review online half before optional expanded R9 regeneration; local half may remain queued",
        "central": "R9 formal stage/role tables only if accepted; reviewed-all provenance retained",
        "module_figures": "optional expanded R9 timeline/gate layer only; accepted-only F027/F028 remain ready and unblocked",
        "rerun": "if rows are accepted/revised, merge bounded stages/roles and regenerate only the expanded R9 layer",
        "issue": "none",
        "boundary": "Opinion ads or opposition movements are not referendum initiators/administrators; person and organization roles stay separate.",
    },
    "HR018": {
        "name": "行政协作、金额与服务关系",
        "priority": "P0",
        "work_lane": "mixed_online_local",
        "files": [
            FileSpec(
                "outputs/R10_administrative_collaboration_v0/HR018_relation_review_v0.csv",
                decision_mode="tri_state",
                decision_fields=("accept", "revise", "reject"),
                local_field="current_review_status",
                local_value="needs_local_retrieval",
            ),
            FileSpec(
                "outputs/R10_administrative_collaboration_v0/HR018_source_prerequisites_v0.csv",
                decision_mode="ancillary",
            ),
        ],
        "hard": "resolve 8 HR018 source prerequisites before their affected relation rows",
        "recommended": "complete before HR021 items 001–007 and before final R10/schema freeze",
        "central": "R10 annual relation layer and approved proposals to central support/relation sample; source-log prerequisites",
        "module_figures": "F008; F031; F032; R10 mechanism/amount figures and brief",
        "rerun": "merge only human-accepted/revised relation rows, then regenerate R10 tables/figures; release HR021-001–007",
        "issue": "decision schema uses three blank accept/revise/reject columns rather than one decision field; 8 source rows are prerequisites, not extra decisions",
        "boundary": "Project cost, aggregate, NOFO, sponsor tier, membership and service presence are not actor payments or political stance evidence.",
    },
    "HR019": {
        "name": "R1/R2 分类词、桥梁机制与议题边范围",
        "priority": "P0",
        "work_lane": "mixed_online_local",
        "files": [
            FileSpec(
                "outputs/R01_R02_actor_issue_v1/HR019/HR019_review_v0.csv",
                decision_fields=("review_decision",),
            ),
            FileSpec(
                "outputs/R01_R02_actor_issue_v1/HR019/HR019_bridge_actor_review_queue_v0.csv",
                decision_fields=("review_decision",),
                local_field="actor_review_status",
                local_value="needs_local_retrieval",
            ),
            FileSpec(
                "outputs/R01_R02_actor_issue_v1/HR019/HR019_edge_scope_review_queue_v0.csv",
                decision_fields=("review_decision",),
                local_field="review_status",
                local_value="needs_local_retrieval",
            ),
        ],
        "hard": "none within HR016–032; external HR010 decisions remain part of final central freeze",
        "recommended": "decide 9 controlled-term rules before 30 bridge and 76 scope rows; merge before the final HR029 regeneration",
        "central": "actor_class controlled mapping; actor–issue scope/classification and accepted edge layer",
        "module_figures": "F009–F012; R1/R2 tables and explanatory brief",
        "rerun": "merge rules and accepted/revised edge scopes, regenerate R1/R2, then regenerate HR029 candidate packet",
        "issue": "docs/human_review_tasks_v0.md preserves a pre-HR027 63-row task description; the live regenerated scope queue contains 76",
        "boundary": "Cross-issue appearance is not stable brokerage; actor–issue edges do not become actor–actor alliances.",
    },
    "HR020": {
        "name": "R5 名称、别名与名单切分",
        "priority": "P1",
        "work_lane": "online_human",
        "files": [FileSpec(
            "outputs/R05_coaction_v1/hr020_review_queue_v0.csv",
            decision_fields=("decision",),
        )],
        "hard": "none",
        "recommended": "complete before final alias/schema freeze to avoid a second entity-crosswalk rerun",
        "central": "event-participant entity crosswalk and alias/segmentation layer; no automatic actor-registry additions",
        "module_figures": "F018/F019 participation, repeat-bridge and overlap outputs",
        "rerun": "regenerate participation edges, overlap/repeat counts, figures and brief while preserving source_name",
        "issue": "task book review-package list omits the live hr020_review_queue_v0.csv path even though it is the 14-row decision queue",
        "boundary": "Alias acceptance changes crosswalk/counts only; co-signing and repeat appearance are not alliances.",
    },
    "HR021": {
        "name": "R6/R7/R11 下游纳入与 analytical seed",
        "priority": "P1",
        "work_lane": "dependent_online_human",
        "files": [FileSpec(
            "outputs/R06_R07_R11_pathways_v1/HR021_review_items_v0.csv",
            decision_fields=("review_decision",),
        )],
        "hard": "HR018 for items HR021-001–007; item HR021-008 has no HR018 dependency",
        "recommended": "review seed item 008 independently; hold items 001–007 until HR018 merge",
        "central": "R6/R11 entry-mode inclusion layer and analytical-seed disposition; no re-review of HR018 facts",
        "module_figures": "optional R6/R7 pathway and R11 entry expansion; current accepted figures remain bounded",
        "rerun": "after HR018, include/revise/exclude downstream observations and regenerate affected pathway/entry outputs",
        "issue": "none",
        "boundary": "Analytical seeds require independent factual directed-edge evidence before promotion.",
    },
    "HR022": {
        "name": "跨模块来源元数据与支持范围",
        "priority": "P0",
        "work_lane": "online_human",
        "files": [FileSpec(
            "outputs/phase1_source_integration_v1/HR022_source_metadata_review_v0.csv",
            decision_fields=("decision",),
        )],
        "hard": "none",
        "recommended": "complete before source/public-data/report freeze; may run parallel with fact review",
        "central": "source-log metadata, evidence level and bounded support scope only",
        "module_figures": "no fact figure approval; downstream citations/locators only",
        "rerun": "merge metadata/support-scope decisions, refresh source crosswalks and public-data/report indexes",
        "issue": "none",
        "boundary": "Archive success or source inclusion does not approve an actor, edge, amount, role or interpretation.",
    },
    "HR023": {
        "name": "覆盖审计（保留编号，无人审任务）",
        "priority": "no_task",
        "work_lane": "mechanical_only",
        "files": [],
        "hard": "none",
        "recommended": "none",
        "central": "none; coverage audit is mechanical aggregation",
        "module_figures": "coverage figures may be regenerated mechanically after final data freeze",
        "rerun": "no human decision merge",
        "issue": "intentional reserved namespace; status artifact exists, but no live CSV queue",
        "boundary": "Do not invent blank review items for mechanical aggregation.",
    },
    "HR024": {
        "name": "既有 actor 议题边补证",
        "priority": "P0",
        "work_lane": "online_human_with_exhausted_item",
        "files": [FileSpec(
            "outputs/edge_activation_v1/HR024_edge_activation_review_v0.csv",
            decision_fields=("decision",),
        )],
        "hard": "prior HR014 anchors already satisfied for A076/A086; A073 still lacks identity closure",
        "recommended": "merge before R1/R2 final regeneration and before regenerating HR029",
        "central": "accepted/revised actor–issue edge evidence for A073/A076/A086",
        "module_figures": "R1/R2 and place–issue downstream figures after central edge merge",
        "rerun": "merge accepted/revised edges only; keep A073 inactive unless identity evidence closes; regenerate R1/R2 and HR029 inputs",
        "issue": "none",
        "boundary": "A073 is online_exhausted/E0 and cannot be activated from name similarity or legacy-list appearance.",
    },
    "HR025": {
        "name": "actor–place 语义与 AP123 键冲突",
        "priority": "P0",
        "work_lane": "online_human",
        "files": [FileSpec(
            "outputs/R03_spatial_dossier_v1/HR025_actor_place_semantics_review_v0.csv",
            decision_fields=("decision",),
        )],
        "hard": "none",
        "recommended": "complete AP123 and all 47 semantics before the final HR029/place regeneration",
        "central": "actor–place semantic field and AP123 place key (P006 Camp Schwab vs P007 Camp Foster)",
        "module_figures": "F013–F015; R3 semantic tables/dossier; MA020",
        "rerun": "apply human decision to AP123 and accepted semantics, regenerate R3 outputs, then regenerate HR029; HR029 must not repair AP123",
        "issue": "exclusive decision authority for AP123; any HR029 mechanical correction would be a task-scope conflict",
        "boundary": "Target, site presence, event location, headquarters and institutional scope remain distinct.",
    },
    "HR026": {
        "name": "三届县知事选—市民组织接口",
        "priority": "P0",
        "work_lane": "online_human",
        "files": [FileSpec(
            "outputs/R09_election_civic_interface_v1/HR026_election_civic_role_review_v0.csv",
            decision_fields=("decision",),
        )],
        "hard": "none; HR030 metadata cleanup is recommended but does not approve roles",
        "recommended": "review after/alongside HR030 source cleanup, before R9 election figure/report freeze",
        "central": "accepted bounded election-civic actor–event role observations only",
        "module_figures": "F029/F030; A029–A031; MA006/MA011",
        "rerun": "regenerate election-window tables, intervention-mode figures and brief from accepted/revised rows only",
        "issue": "R08 directory contains HR026_status_v0.md, but control docs state R8 created no live HR026; the only live HR026 queue is this R9 election CSV",
        "boundary": "No vote, turnout, outcome, policy-causality or party/candidate-to-registry inference.",
    },
    "HR027": {
        "name": "registry 价值门槛 v2",
        "priority": "completed_2026-07-16",
        "work_lane": "online_human",
        "files": [FileSpec(
            "outputs/registry_value_gate_v2/HR027_registry_value_review_v0.csv",
            decision_fields=("decision",),
        )],
        "hard": "none",
        "recommended": "completed: four accepted actors were assigned A112-A115 and merged before HR029 regeneration",
        "central": "actor registry and registry count; source/alias crosswalk; no automatic central edges",
        "module_figures": "global R1/R2/R3 counts and figures after merge",
        "rerun": "completed; retain as an audit batch and do not reopen without a new human decision",
        "issue": "four decisions are populated and must remain preserved by later orchestration regeneration",
        "boundary": "Module repair/value, not reaching 120 by itself, is the acceptance basis.",
    },
    "HR028": {
        "name": "R5/R7 异质行动（保留编号，无人审任务）",
        "priority": "no_task",
        "work_lane": "mechanical_only",
        "files": [],
        "hard": "none",
        "recommended": "none",
        "central": "none; package reorganizes existing formal observations",
        "module_figures": "heterogeneous repertoire figures are mechanically derived from accepted facts",
        "rerun": "no human decision merge",
        "issue": "intentional reserved namespace; status artifact exists, but no live CSV queue",
        "boundary": "Do not create an HR queue unless future work introduces genuinely new facts.",
    },
    "HR029": {
        "name": "schema 与 alias 冻结",
        "priority": "P0_after_regeneration",
        "work_lane": "online_human_after_dependencies",
        "files": [FileSpec(
            "outputs/schema_alias_freeze_v1/HR029_schema_alias_freeze_review_v0.csv",
            decision_fields=("decision",),
        )],
        "hard": "HR027 merge and first regeneration are complete; final freeze still requires HR019/HR024/HR025 merges and external HR010",
        "recommended": "also finish HR018 relation vocabulary and HR020 alias crosswalk before the one final freeze",
        "central": "coding schema; actor_class/legal_status; alias; place/venue/relation/action vocabularies",
        "module_figures": "F009/F010/F012/F013/F031 and all schema-sensitive tables",
        "rerun": "after HR019/HR024/HR025/external HR010 merge, regenerate the current 122-actor HR029 packet again, then review 36 rows and freeze/lint",
        "issue": "current HR029 is a valid post-HR027 intermediate snapshot, but not the final post-edge/place freeze packet",
        "boundary": "AP123 is excluded from mechanical HR029 correction and remains exclusively HR025.",
    },
    "HR030": {
        "name": "下一波来源元数据与归档",
        "priority": "P0",
        "work_lane": "online_human",
        "files": [FileSpec(
            "outputs/next_wave_source_integration_v1/HR030_source_metadata_archive_review_v0.csv",
            decision_fields=("decision",),
        )],
        "hard": "none",
        "recommended": "complete early/parallel before HR026/HR027 citations and final source/public-data freeze",
        "central": "S248–S294 source metadata, locator, archive resolution and bounded support scope only",
        "module_figures": "no fact approval; affects citation/source indexes and public-data package",
        "rerun": "merge source metadata/archive resolutions; refresh archive/source crosswalk without approving candidate facts",
        "issue": "none",
        "boundary": "Archive failure is not evidence absence; source inclusion is not candidate-role or actor approval.",
    },
    "HR031": {
        "name": "报告解释强度",
        "priority": "P0_final_wording",
        "work_lane": "principal_investigator_judgment",
        "files": [FileSpec(
            "outputs/report_claim_audit_v1/HR031_report_claim_review_v0.csv",
            decision_fields=("decision",),
        )],
        "hard": "none for the judgment itself; use only after factual gates for final report wording",
        "recommended": "last decision batch before MA017/MA018 prose lock",
        "central": "none; report-claim interpretation strength and wording only",
        "module_figures": "none; does not approve data, edges, roles, funding or causality",
        "rerun": "apply wording-strength choices to report/paper claims only; rerun claim audit, not central data merges",
        "issue": "none",
        "boundary": "HR031 is interpretation-only and must never be used as a substitute for fact/relationship review.",
    },
    "HR032": {
        "name": "S002 合作对象名称、JV 与 registry crosswalk",
        "priority": "P1",
        "work_lane": "online_human",
        "files": [FileSpec(
            "outputs/R10_official_collaboration_universe_v1/HR032_partner_alias_crosswalk_review_v1.csv",
            decision_fields=("decision",),
        )],
        "hard": "none; current R10 source-label figures are ready and do not depend on HR032",
        "recommended": "review with HR016/HR020 before any future canonical actor/JV/member crosswalk or registry freeze",
        "central": "future S002 source-label→canonical actor/JV/member crosswalk only; no automatic registry, relation or resource-edge merge",
        "module_figures": "current R10 source-universe source-label figures remain ready/unblocked; accepted decisions may support a future actor-level redraw",
        "rerun": "apply only accepted/revised alias, legal-identity, JV/member and registry crosswalk decisions to future actor-level R10 outputs; do not gate the current source-label figures",
        "issue": "none; eight live decision rows are intentionally separate from current source-label aggregation",
        "boundary": "Machine display aliases, legal-prefix variants and JV/member strings are not verified actor identities; project costs must not be apportioned to a named member.",
    },
}


INVENTORY_FIELDS = [
    "hr_id", "task_name_cn", "namespace_state", "priority_lane", "work_lane",
    "csv_paths", "csv_file_count", "actual_row_count_total", "decision_row_count",
    "blank_decision_row_count", "completed_decision_row_count", "ancillary_row_count",
    "local_flagged_row_count", "decision_schema", "hard_prerequisites",
    "recommended_predecessors", "central_tables_or_state_affected",
    "module_figure_or_brief_effects", "report_figure_assets", "report_nonfigure_assets",
    "missing_asset_gates", "rerun_or_merge_after_review", "namespace_or_count_issue",
    "non_inference_boundary",
]

BATCH_FIELDS = [
    "batch_order", "batch_id", "batch_name_cn", "priority_lane", "work_lane",
    "hr_scope", "row_scope", "decision_rows", "ancillary_rows", "entry_condition",
    "why_this_order", "merge_or_rerun_after", "unblocks", "do_not_do",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=fields, extrasaction="ignore", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)


def split_gate(value: str) -> set[str]:
    return {part.strip() for part in value.split("|") if part.strip()}


def namespace_state(hr_id: str) -> str:
    if hr_id in {"HR023", "HR028"}:
        return "reserved_no_live_task"
    if hr_id == "HR026":
        return "one_live_queue__R08_tombstone_filename_present"
    return "active_unique_live_queue"


def inventory_rows() -> list[dict[str, object]]:
    manifest = read_csv(MANIFEST_PATH)
    missing = read_csv(MISSING_PATH)
    result: list[dict[str, object]] = []

    for number in range(16, 33):
        hr_id = f"HR{number:03d}"
        task = TASKS[hr_id]
        file_specs: list[FileSpec] = task["files"]  # type: ignore[assignment]
        total_rows = 0
        decision_rows = 0
        blank_rows = 0
        completed_rows = 0
        ancillary_rows = 0
        local_rows = 0
        schemas: list[str] = []

        for spec in file_specs:
            path = ROOT / spec.path
            if not path.exists():
                raise FileNotFoundError(f"Missing HR CSV: {spec.path}")
            rows = read_csv(path)
            total_rows += len(rows)
            if spec.local_field:
                local_rows += sum(
                    row.get(spec.local_field, "").strip() == spec.local_value for row in rows
                )
            if spec.decision_mode == "ancillary":
                ancillary_rows += len(rows)
                schemas.append(f"{Path(spec.path).name}:ancillary_no_decision")
                continue
            decision_rows += len(rows)
            if spec.decision_mode == "tri_state":
                blank = sum(
                    all(not row.get(field, "").strip() for field in spec.decision_fields)
                    for row in rows
                )
                schemas.append(
                    f"{Path(spec.path).name}:one_of({','.join(spec.decision_fields)})"
                )
            else:
                if len(spec.decision_fields) != 1:
                    raise ValueError(f"Single-field decision spec expected: {spec}")
                field = spec.decision_fields[0]
                blank = sum(not row.get(field, "").strip() for row in rows)
                schemas.append(f"{Path(spec.path).name}:{field}")
            blank_rows += blank
            completed_rows += len(rows) - blank

        report_assets = [
            row for row in manifest
            if hr_id in split_gate(row.get("hr_gate", ""))
            and row.get("formal_use_status") != "superseded_do_not_use"
        ]
        figures = [row["asset_id"] for row in report_assets if row["asset_type"] == "figure"]
        nonfigures = [row["asset_id"] for row in report_assets if row["asset_type"] != "figure"]
        missing_gates = [
            row["missing_id"] for row in missing if hr_id in split_gate(row.get("human_gate", ""))
        ]

        result.append({
            "hr_id": hr_id,
            "task_name_cn": task["name"],
            "namespace_state": namespace_state(hr_id),
            "priority_lane": task["priority"],
            "work_lane": task["work_lane"],
            "csv_paths": ";".join(spec.path for spec in file_specs),
            "csv_file_count": len(file_specs),
            "actual_row_count_total": total_rows,
            "decision_row_count": decision_rows,
            "blank_decision_row_count": blank_rows,
            "completed_decision_row_count": completed_rows,
            "ancillary_row_count": ancillary_rows,
            "local_flagged_row_count": local_rows,
            "decision_schema": ";".join(schemas) or "none",
            "hard_prerequisites": task["hard"],
            "recommended_predecessors": task["recommended"],
            "central_tables_or_state_affected": task["central"],
            "module_figure_or_brief_effects": task["module_figures"],
            "report_figure_assets": ";".join(figures) or "none_current_report_gate",
            "report_nonfigure_assets": ";".join(nonfigures) or "none_current_report_gate",
            "missing_asset_gates": ";".join(missing_gates) or "none",
            "rerun_or_merge_after_review": task["rerun"],
            "namespace_or_count_issue": task["issue"],
            "non_inference_boundary": task["boundary"],
        })
    return result


def by_hr(rows: list[dict[str, object]]) -> dict[str, dict[str, object]]:
    return {str(row["hr_id"]): row for row in rows}


def batch_rows(inventory: list[dict[str, object]]) -> list[dict[str, object]]:
    lookup = by_hr(inventory)

    def dec(hr: str) -> int:
        return int(lookup[hr]["decision_row_count"])

    def anc(hr: str) -> int:
        return int(lookup[hr]["ancillary_row_count"])

    local17 = int(lookup["HR017"]["local_flagged_row_count"])
    local18 = int(lookup["HR018"]["local_flagged_row_count"])
    local19 = int(lookup["HR019"]["local_flagged_row_count"])
    online17 = dec("HR017") - local17
    online18 = dec("HR018") - local18
    online19 = dec("HR019") - local19
    hr024_ready = dec("HR024") - 1  # A073 remains online-exhausted/E0.

    return [
        {
            "batch_order": "00", "batch_id": "B00_SOURCE_PREFLIGHT",
            "batch_name_cn": "来源前置与元数据清理（可并行）", "priority_lane": "P0",
            "work_lane": "online_human/source_only",
            "hr_scope": "HR018-source;HR022;HR030",
            "row_scope": f"HR018 source prerequisites={anc('HR018')}; HR022={dec('HR022')}; HR030={dec('HR030')}",
            "decision_rows": dec("HR022") + dec("HR030"), "ancillary_rows": anc("HR018"),
            "entry_condition": "now",
            "why_this_order": "fix locators/metadata/archive prerequisites before relation, election and registry citations to avoid reopening source questions",
            "merge_or_rerun_after": "merge source metadata/support-scope and resolve HR018 source prerequisites; refresh source crosswalk only",
            "unblocks": "HR018 affected rows; MA012/MA021 source freeze; cleaner HR026/HR027 review context",
            "do_not_do": "source inclusion/archive success does not approve actors, roles, relations, amounts or interpretations",
        },
        {
            "batch_order": "01", "batch_id": "B01_REGISTRY_GATE",
            "batch_name_cn": "registry 价值门槛先决批", "priority_lane": "P0_first",
            "work_lane": "online_human",
            "hr_scope": "HR027", "row_scope": f"all {dec('HR027')} decision rows",
            "decision_rows": dec("HR027"), "ancillary_rows": 0, "entry_condition": "completed 2026-07-16",
            "why_this_order": "completed prerequisite: HR027 was decided before the 122-actor HR029 snapshot was generated",
            "merge_or_rerun_after": "completed: A112-A115 merged and dynamic registry-dependent packages regenerated",
            "unblocks": "registry minimum decision; dynamic actor/schema audits; MA001/MA002/MA008/MA012/MA021/MA022",
            "do_not_do": "do not accept candidates merely to reach 120; do not auto-create central edges",
        },
        {
            "batch_order": "02", "batch_id": "B02_CORE_FACT_INPUTS",
            "batch_name_cn": "中央 actor／issue／place 冻结输入批", "priority_lane": "P0",
            "work_lane": "online_human with explicit local exceptions",
            "hr_scope": "HR019;HR024;HR025",
            "row_scope": f"HR019 non-local={online19} (rules 9 first); HR024 A076/A086={hr024_ready}; HR025={dec('HR025')} including AP123",
            "decision_rows": online19 + hr024_ready + dec("HR025"), "ancillary_rows": 0,
            "entry_condition": "may start now; HR027 actor-ID assignment is complete",
            "why_this_order": "these decisions change classifications, issue edges, place semantics and the inputs used to regenerate HR029",
            "merge_or_rerun_after": "merge accepted/revised central values once; apply AP123 only from HR025; regenerate R1/R2/R3 and HR029 inputs",
            "unblocks": "MA001–MA004, MA008, MA012, MA020–MA022 and schema regeneration",
            "do_not_do": "HR029 must not repair AP123; candidate issue edges are not stable actor–actor ties",
        },
        {
            "batch_order": "03", "batch_id": "B03_ELECTION_INTERFACE",
            "batch_name_cn": "选举—市民组织接口事实批", "priority_lane": "P0",
            "work_lane": "online_human",
            "hr_scope": "HR026", "row_scope": f"all {dec('HR026')} decision rows",
            "decision_rows": dec("HR026"), "ancillary_rows": 0,
            "entry_condition": "prefer after/alongside HR030 metadata cleanup; no hard fact dependency",
            "why_this_order": "freeze bounded actor–event roles before rebuilding R9 election tables/figures and drafting report claims",
            "merge_or_rerun_after": "regenerate F029/F030 and A029–A031 from accepted/revised rows only",
            "unblocks": "MA006, MA011 and the R9 election part of MA017",
            "do_not_do": "do not infer votes, turnout, winners' causality, policy effects or registry status for candidates/parties",
        },
        {
            "batch_order": "04", "batch_id": "B04_R10_RELATIONS",
            "batch_name_cn": "R10 敏感关系批", "priority_lane": "P0",
            "work_lane": "mixed_online_local",
            "hr_scope": "HR018-relations-online", "row_scope": f"{online18} non-local relation decisions after {anc('HR018')} source prerequisites; 2 local rows move to B07",
            "decision_rows": online18, "ancillary_rows": 0,
            "entry_condition": "affected source prerequisite must be resolved first",
            "why_this_order": "HR018 is the factual gate for R10 and for seven downstream HR021 inclusion decisions",
            "merge_or_rerun_after": "merge only human-accepted/revised relations; regenerate R10 once; then release HR021-001–007",
            "unblocks": "F008/F031/F032, MA007, R10 portion of MA017, HR021-001–007",
            "do_not_do": "do not turn project cost, NOFO, aggregate, service presence or sponsor tier into payment/funding/stance",
        },
        {
            "batch_order": "05A", "batch_id": "B05A_SEED_INDEPENDENT",
            "batch_name_cn": "独立 analytical seed 判断", "priority_lane": "P1",
            "work_lane": "online_human",
            "hr_scope": "HR021-008", "row_scope": "1 independent seed decision",
            "decision_rows": 1, "ancillary_rows": 0, "entry_condition": "now",
            "why_this_order": "item 008 has no HR018 prerequisite and should not be held behind sensitive relation review",
            "merge_or_rerun_after": "retain as seed unless independent factual directed-edge evidence supports promotion",
            "unblocks": "bounded R6/R7 pathway interpretation",
            "do_not_do": "do not promote an analytical construction into a factual or causal edge without independent evidence",
        },
        {
            "batch_order": "05B", "batch_id": "B05B_HR018_DOWNSTREAM",
            "batch_name_cn": "HR018 后的 R6/R11 纳入批", "priority_lane": "P1_dependent",
            "work_lane": "online_human_after_HR018",
            "hr_scope": "HR021-001–007", "row_scope": "7 dependent inclusion decisions",
            "decision_rows": 7, "ancillary_rows": 0, "entry_condition": "corresponding HR018 relation is accepted or revised",
            "why_this_order": "these rows decide downstream use only and must not duplicate or pre-empt the HR018 fact review",
            "merge_or_rerun_after": "include/revise/exclude downstream observations and regenerate affected R6/R11 outputs once",
            "unblocks": "optional R6/R11 expansion layer",
            "do_not_do": "do not re-review the same relation fact or infer funding direction/government endorsement/political stance",
        },
        {
            "batch_order": "06", "batch_id": "B06_MODULE_ALIAS_PRE_FREEZE",
            "batch_name_cn": "模块语义与别名预冻结批", "priority_lane": "P1",
            "work_lane": "online_human",
            "hr_scope": "HR016;HR020;HR032;HR017-online",
            "row_scope": f"HR016={dec('HR016')}; HR020={dec('HR020')}; HR032={dec('HR032')}; HR017 online={online17}",
            "decision_rows": dec("HR016") + dec("HR020") + dec("HR032") + online17, "ancillary_rows": 0,
            "entry_condition": "now; exclude rows lacking required local evidence",
            "why_this_order": "resolve online module semantics and entity crosswalks before one final schema/alias freeze; HR032 remains independent of current R10 source-label figures",
            "merge_or_rerun_after": "regenerate R4/R5 and optional R9 expansion layers; apply HR032 only to a future canonical actor/JV/member crosswalk; feed only accepted alias/crosswalk changes into final freeze",
            "unblocks": "MA009, online portion of MA020, cleaner HR029 alias inputs and future actor-level R10 crosswalks",
            "do_not_do": "do not turn event-only names or S002 source labels into actors, opinion-ad participation into referendum administration, co-signing into alliance, or JV project cost into member payment",
        },
        {
            "batch_order": "07", "batch_id": "B07_LOCAL_LANE",
            "batch_name_cn": "当地／线上耗尽保留队列", "priority_lane": "local",
            "work_lane": "local_or_new_primary_evidence",
            "hr_scope": "HR017-local;HR018-local;HR019-local;HR024-A073",
            "row_scope": f"explicit local flags: HR017={local17}; HR018={local18}; HR019={local19}; plus A073 online-exhausted conditional item",
            "decision_rows": local17 + local18 + local19 + 1, "ancillary_rows": 0,
            "entry_condition": "required local/primary material obtained; A073 identity closure obtained",
            "why_this_order": "keep genuinely local gaps visible without blocking safe accepted-only online figures or forcing unsupported decisions",
            "merge_or_rerun_after": "merge only after source-specific human review; otherwise retain local/online-exhausted status",
            "unblocks": "expanded R9 layer, residual R10/R1/R2 items and fuller local dossier",
            "do_not_do": "do not fill decisions from AI summaries, unavailable archives or name similarity",
        },
        {
            "batch_order": "08", "batch_id": "B08_MERGE_REGENERATE_HR029",
            "batch_name_cn": "中央合并与 HR029 重生闸门", "priority_lane": "P0_process_gate",
            "work_lane": "main_thread_mechanical_merge",
            "hr_scope": "HR027→HR029;HR019;HR024;HR025;external HR010;recommended HR018/HR020",
            "row_scope": "0 human decisions; regeneration step",
            "decision_rows": 0, "ancillary_rows": 0,
            "entry_condition": "HR027 accepted actors assigned/merged; HR019/HR024/HR025 and external HR010 merged; AP123 resolved by HR025",
            "why_this_order": "the 122-actor intermediate snapshot exists; this gate prevents freezing it before AP123 and edge/place decisions are merged",
            "merge_or_rerun_after": "rerun dynamic schema/alias audit and replace the HR029 review packet with the regenerated current-state packet",
            "unblocks": "valid HR029 review; final global count/schema/alias/place/venue/relation/action freeze",
            "do_not_do": "do not execute the current intermediate HR029 decisions before the final dependency merge/regeneration",
        },
        {
            "batch_order": "09", "batch_id": "B09_SCHEMA_FREEZE",
            "batch_name_cn": "重生后的 schema／alias 冻结批", "priority_lane": "P0_after_regeneration",
            "work_lane": "online_human_after_dependencies",
            "hr_scope": "HR029", "row_scope": f"current packet has {dec('HR029')} rows but must be regenerated before review",
            "decision_rows": dec("HR029"), "ancillary_rows": 0,
            "entry_condition": "B08 completed and regenerated packet identity/count verified",
            "why_this_order": "one final controlled-vocabulary and alias decision pass after actor/edge/place state is stable",
            "merge_or_rerun_after": "freeze schema/alias/place/venue/relation/action vocabularies; run cross-table lint; regenerate schema-sensitive figures",
            "unblocks": "MA001–MA004, MA007/MA008, MA012, MA017, MA021/MA022",
            "do_not_do": "do not merge national/local organizations, predecessors/successors, litigation rounds, counsel/plaintiff groups; do not touch AP123",
        },
        {
            "batch_order": "10", "batch_id": "B10_INTERPRETATION_LOCK",
            "batch_name_cn": "报告解释强度终审批", "priority_lane": "P0_final_wording",
            "work_lane": "principal_investigator_judgment",
            "hr_scope": "HR031", "row_scope": f"all {dec('HR031')} interpretation decisions",
            "decision_rows": dec("HR031"), "ancillary_rows": 0,
            "entry_condition": "factual/source/schema gates frozen enough to draft final report wording",
            "why_this_order": "locking interpretive strength last avoids rewriting the report after factual changes",
            "merge_or_rerun_after": "apply to report/paper prose and rerun claim audit only",
            "unblocks": "MA017 and MA018 wording lock",
            "do_not_do": "HR031 changes interpretation strength only; it cannot approve central facts, roles, edges, funding or causality",
        },
        {
            "batch_order": "11", "batch_id": "B11_RESERVED_NO_TASK",
            "batch_name_cn": "保留零任务编号", "priority_lane": "no_task",
            "work_lane": "do_not_schedule",
            "hr_scope": "HR023;HR028", "row_scope": "0 rows",
            "decision_rows": 0, "ancillary_rows": 0,
            "entry_condition": "HR023/HR028 remain no-task unless genuinely new facts arise",
            "why_this_order": "preserves the two mechanical namespaces without fabricating review work",
            "merge_or_rerun_after": "none",
            "unblocks": "none",
            "do_not_do": "do not create blank decisions for mechanical audits",
        },
    ]


def normalize_svg(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    path.write_text(
        "\n".join(line.rstrip() for line in text.splitlines()) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def make_dependency_graph(inventory: list[dict[str, object]]) -> None:
    lookup = by_hr(inventory)
    plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Yu Gothic", "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["svg.hashsalt"] = "human-review-orchestration-v1"

    fig, ax = plt.subplots(figsize=(22, 12.5))
    ax.set_xlim(0, 22)
    ax.set_ylim(0, 12.5)
    ax.axis("off")

    positions = {
        "HR022": (2.0, 10.5), "HR030": (2.0, 9.05), "HR016": (2.0, 7.6),
        "HR017": (2.0, 6.15), "HR020": (2.0, 4.7), "HR023": (2.0, 2.7),
        "HR028": (2.0, 1.25),
        "HR027": (6.2, 10.5), "HR019": (6.2, 9.05), "HR024": (6.2, 7.6),
        "HR025": (6.2, 6.15), "HR026": (6.2, 4.7), "HR018": (6.2, 3.25),
        "HR032": (6.2, 1.25),
        "HR021": (10.5, 3.25), "HR029": (14.7, 6.6), "HR031": (14.7, 4.55),
    }
    process_positions = {
        "source_freeze": (10.5, 9.75), "central_merge": (10.5, 7.6),
        "ap123": (10.5, 6.15), "regen": (14.7, 8.25),
        "final_data": (19.1, 7.25), "report_lock": (19.1, 4.55),
        "local_lane": (10.5, 1.25),
    }
    priority_fill = {
        "P0": "#DCEBFA", "P0_first": "#CBE3F7", "P0_after_regeneration": "#DCEBFA",
        "P0_final_wording": "#FCE8C8", "P1": "#DDF3EC", "no_task": "#ECEFF2",
    }

    def task_label(hr: str) -> str:
        row = lookup[hr]
        total = int(row["actual_row_count_total"])
        blank = int(row["blank_decision_row_count"])
        local = int(row["local_flagged_row_count"])
        priority = str(row["priority_lane"])
        gate = priority
        if local:
            gate += f" · local {local}"
        if hr in {"HR023", "HR028"}:
            gate = "no_task · mechanical"
        short_name = {
            "HR016": "先岛语义/locator", "HR017": "公投扩展层", "HR018": "R10敏感关系",
            "HR019": "分类/bridge/scope", "HR020": "R5别名/切分", "HR021": "R6/R11下游",
            "HR022": "来源元数据", "HR023": "覆盖审计", "HR024": "议题边补证",
            "HR025": "地点语义/AP123", "HR026": "选举接口", "HR027": "registry价值门槛",
            "HR028": "异质行动", "HR029": "schema/alias冻结", "HR030": "新来源/归档",
            "HR031": "解释强度", "HR032": "S002名称/JV crosswalk",
        }[hr]
        if hr == "HR018":
            counts = f"{total}行＝26决定＋8前置｜空白{blank}"
        else:
            counts = f"{total}行｜空白决定{blank}"
        return f"{hr}  {short_name}\n{counts}\n{gate}"

    def add_task(hr: str) -> None:
        x, y = positions[hr]
        priority = str(lookup[hr]["priority_lane"])
        fill = priority_fill.get(priority, "#DCEBFA")
        local = int(lookup[hr]["local_flagged_row_count"])
        edge = "#C97724" if local else "#45647B"
        if priority == "no_task":
            edge = "#8B959E"
        box = FancyBboxPatch(
            (x - 1.72, y - 0.53), 3.44, 1.06,
            boxstyle="round,pad=0.08", facecolor=fill, edgecolor=edge, linewidth=1.5,
        )
        ax.add_patch(box)
        ax.text(x, y, task_label(hr), ha="center", va="center", fontsize=8.6, linespacing=1.25)

    for hr in positions:
        add_task(hr)

    process_labels = {
        "source_freeze": "来源 metadata / locator 冻结\n不批准事实关系",
        "central_merge": "中央 actor / edge / place 合并\n含外部 HR010",
        "ap123": "AP123 专属纠键\n只接受 HR025 决定",
        "regen": "最终重生 HR029 packet\n替换 122-actor 中间快照",
        "final_data": "最终 data / schema / figures 冻结\n运行跨表 lint",
        "report_lock": "报告 / 论文措辞锁定\nMA017 / MA018",
        "local_lane": "当地／新一手材料队列\n不强行填决定",
    }
    for key, (x, y) in process_positions.items():
        width = 3.6 if key not in {"final_data", "report_lock"} else 4.0
        fill = "#FFF6DD" if key in {"ap123", "report_lock", "local_lane"} else "#F4F7F9"
        edge = "#B17B1C" if key in {"ap123", "report_lock", "local_lane"} else "#697B88"
        box = FancyBboxPatch(
            (x - width / 2, y - 0.5), width, 1.0,
            boxstyle="round,pad=0.08", facecolor=fill, edgecolor=edge, linewidth=1.4,
        )
        ax.add_patch(box)
        ax.text(x, y, process_labels[key], ha="center", va="center", fontsize=8.8, linespacing=1.25)

    def edge(source: str, target: str, *, kind: str = "hard", rad: float = 0.0, label: str = "") -> None:
        sx, sy = positions.get(source, process_positions.get(source))  # type: ignore[arg-type]
        tx, ty = positions.get(target, process_positions.get(target))  # type: ignore[arg-type]
        color = {"hard": "#355D7A", "recommended": "#78909C", "report": "#B17B1C"}[kind]
        style = "-" if kind == "hard" else (0, (4, 3))
        arrow = FancyArrowPatch(
            (sx + 1.72, sy), (tx - 1.8, ty), arrowstyle="-|>", mutation_scale=12,
            linewidth=1.35, color=color, linestyle=style,
            connectionstyle=f"arc3,rad={rad}", zorder=0,
        )
        ax.add_patch(arrow)
        if label:
            mx, my = (sx + tx) / 2, (sy + ty) / 2 + (0.25 if rad >= 0 else -0.25)
            ax.text(mx, my, label, fontsize=7.6, ha="center", va="center", color=color,
                    bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.8, "pad": 1})

    edge("HR022", "source_freeze", kind="hard", rad=0.08)
    edge("HR030", "source_freeze", kind="hard", rad=-0.08)
    edge("HR027", "central_merge", kind="hard", rad=0.08, label="先合并A号")
    edge("HR019", "central_merge", kind="hard", rad=0.02)
    edge("HR024", "central_merge", kind="hard", rad=-0.03)
    edge("HR025", "ap123", kind="hard", label="唯一决定权")
    edge("ap123", "central_merge", kind="hard", rad=-0.08)
    edge("HR020", "central_merge", kind="recommended", rad=-0.15, label="alias建议先行")
    edge("HR018", "HR021", kind="hard", label="前7项")
    edge("HR018", "central_merge", kind="recommended", rad=0.18, label="relation词表")
    edge("central_merge", "regen", kind="hard", label="只重生一次")
    edge("regen", "HR029", kind="hard")
    edge("HR029", "final_data", kind="hard")
    edge("HR026", "final_data", kind="hard", rad=-0.16)
    edge("HR016", "final_data", kind="recommended", rad=-0.22)
    edge("HR021", "final_data", kind="recommended", rad=0.12)
    edge("HR032", "final_data", kind="recommended", rad=-0.24, label="未来crosswalk；不gate现图")
    edge("source_freeze", "report_lock", kind="hard", rad=0.18)
    edge("final_data", "report_lock", kind="hard", rad=0.0)
    edge("HR031", "report_lock", kind="report", label="只改解释强度")
    edge("HR017", "local_lane", kind="recommended", rad=0.10)
    edge("HR018", "local_lane", kind="recommended", rad=-0.10)
    edge("HR019", "local_lane", kind="recommended", rad=-0.22)

    ax.text(11, 12.05, "HR016–HR032 人工复核依赖与重跑编排", ha="center", va="center",
            fontsize=18, fontweight="bold", color="#243746")
    ax.text(11, 11.62, "只编排人工作业，不填任何决定；节点显示 CSV 实际行数、空白决定数与 gate。",
            ha="center", va="center", fontsize=10.5, color="#4D5E6C")
    ax.text(0.3, 11.15, "来源／P1并行", fontsize=10, fontweight="bold", color="#45647B")
    ax.text(4.5, 11.15, "P0事实与registry", fontsize=10, fontweight="bold", color="#45647B")
    ax.text(8.7, 11.15, "合并／依赖闸门", fontsize=10, fontweight="bold", color="#45647B")
    ax.text(13.0, 11.15, "重生／人工冻结", fontsize=10, fontweight="bold", color="#45647B")
    ax.text(17.3, 11.15, "最终资产", fontsize=10, fontweight="bold", color="#45647B")
    ax.text(
        0.35, 0.15,
        "实线＝硬依赖；虚线＝为减少重跑的建议顺序；橙边＝含当地材料行。HR023/HR028 为零任务；HR032 只约束未来 crosswalk，不 gate 当前 R10 source-label 图。",
        fontsize=9, color="#44515C",
    )

    fig.savefig(
        GRAPH_PNG_PATH, dpi=180, bbox_inches="tight",
        metadata={"Software": "human-review orchestration v1"},
    )
    fig.savefig(
        GRAPH_SVG_PATH, format="svg", bbox_inches="tight",
        metadata={"Creator": "human-review orchestration v1", "Date": "2026-07-13"},
    )
    plt.close(fig)
    normalize_svg(GRAPH_SVG_PATH)


def make_readme(inventory: list[dict[str, object]], batches: list[dict[str, object]]) -> str:
    total = sum(int(row["actual_row_count_total"]) for row in inventory)
    decisions = sum(int(row["decision_row_count"]) for row in inventory)
    blank = sum(int(row["blank_decision_row_count"]) for row in inventory)
    ancillary = sum(int(row["ancillary_row_count"]) for row in inventory)
    local = sum(int(row["local_flagged_row_count"]) for row in inventory)
    return dedent(f"""
    # HR016–HR032 人工复核编排包 v1

    日期：2026-07-13

    状态：**只做编排与依赖审计，不做 AI 人审，不修改任何 HR CSV。**

    ## 1. 当前盘点

    - HR 范围：HR016–HR032，共 17 个编号。
    - 实际 CSV 行：**{total}**。
    - 真正需要人工决定的行：**{decisions}**；当前空白决定：**{blank}**。
    - HR018 另有 **{ancillary}** 个来源前置行；它们不是额外的 accept/revise/reject 决定。
    - CSV 中明确标注 `needs_local_retrieval` 的行：**{local}**（HR017 9、HR018 2、HR019 3）。A073 另为 online-exhausted/E0 条目，但不冒充结构化 local flag。
    - HR023 与 HR028 均为有意保留的零任务编号；HR032 已成为 **8 行 P1 live queue**，8 个 `decision` 当前均为空。

    两张主表：

    - `task_inventory_v1.csv`：逐 HR 记录真实行数、空白决定数、依赖、中央表／图／报告资产、重跑动作和边界。
    - `recommended_batches_v1.csv`：按“减少全局重跑次数”而非编号顺序编排。

    `dependency_graph_v1.svg/.png` 是同一依赖关系的可视化。实线是硬依赖，虚线是减少重跑的建议顺序；图中没有替任何人填写决定。

    ## 2. 五条不可改写的主依赖

    1. **HR027 已完成并合并 A112–A115；122-actor 的 HR029 中间快照已重生。** 仍须先合并 HR019／024／025 与外部 HR010，再做最后一次 HR029 重生和审查；当前 36 行不能直接作为最终 freeze。
    2. **HR018 的 8 个来源前置 → HR018 的 26 条敏感关系 → HR021-001–007。** HR021 只决定下游是否纳入，不重复审核关系事实；HR021-008 可独立复核。
    3. **AP123 只由 HR025 决定。** Camp Schwab/P006 与 Camp Foster/P007 的键冲突不能由 HR029 或脚本机械覆盖。
    4. **HR031 只管解释强度。** 它可以改变报告／论文措辞，不能批准中央事实、角色、边、金额、资金或因果。
    5. **HR032 只约束未来 canonical／JV／registry crosswalk。** 当前两张 R10 source-label 总体图保持 ready，不以 HR032 为 gate，也不因 HR032 自动生成 actor、关系边或成员付款。

    ## 3. P0、P1、local 与 no-task

    ### P0：先冻结会造成全局重跑的决定

    - 第一优先：HR027。
    - 中央 actor／issue／place：HR019、HR024、HR025；外部仍有 HR010 依赖。
    - 选举接口：HR026。
    - 敏感行政／服务关系：HR018；完成后释放 HR021 前 7 项。
    - 来源与发布层：HR022、HR030。
    - 重生后的全局 schema／alias freeze：HR029。
    - 最终报告解释锁定：HR031。

    ### P1：不应阻塞安全正文层，但应在最终 alias／模块冻结前处理

    - HR016：先岛框架语义与 locator。
    - HR017：公投 reviewed-all 扩展层；新的 accepted-only F027/F028 不依赖 HR017。
    - HR020：R5 名称／别名／切分。
    - HR021：R6/R11 下游纳入；其中 7 项依赖 HR018，1 项独立。
    - HR032：S002 合作对象名称、法律前缀、JV 成员与 registry crosswalk；8 行并入 B06。它不阻断当前 R10 source-label 图，只为未来 actor-level 解释和 crosswalk 冻结提供人工决定。

    ### local：没有材料就保持空白

    - HR017：9 行。
    - HR018：2 行。
    - HR019：3 行。
    - HR024 的 A073 是 online-exhausted/E0；需要新的身份闭合证据，不能用旧名单或名称相似激活。

    local 队列不应反向阻塞现有 accepted-only 安全图，也不能由 AI 摘要代替原件复核。

    ### no-task

    - HR023：coverage mechanical audit，零人审。
    - HR028：异质行动包只重组既有正式事实，零人审。

    ## 4. 推荐执行法

    按 `recommended_batches_v1.csv` 的 B00→B11 执行。每一批内部可以拆成 8–12 行、60–90 分钟的人工作业；批次号只表示依赖与重跑顺序，不表示 AI 已判断重要性或事实真伪。

    最重要的“只重跑一次”节点是 B08：主线程汇总 HR027、HR019、HR024、HR025 与外部 HR010 的人工决定，应用 AP123 的 HR025 决定，随后重生 HR029。为避免第二次 alias／relation freeze，建议同时尽量完成 HR018、HR020 与 HR032，再进入 B09。HR032 只进入未来 canonical/JV/registry crosswalk；当前 R10 source-label 图不等它。

    ## 5. namespace／文档一致性审计

    - **没有发现两个同时有效的同号 CSV 人审队列。**
    - HR026 有表面命名冲突：R08 目录存在 `HR026_status_v0.md`，但控制文档明确 R8 没有新增 HR026，实际有效 HR026 是 R9 选举的 19 行 CSV。该 R8 文件只能视为状态／墓碑文件，不能当成第二个任务。
    - HR019 的任务书仍写 63 条 edge scope；HR-027 合并并重生后，`HR019_edge_scope_review_queue_v0.csv` 实际为 **76**。本包按当前实数计数，不修改原任务书。
    - HR020 的任务书“复核包”清单漏列实际 14 行决定队列 `hr020_review_queue_v0.csv`；本包将其作为唯一 live queue 计数，不修改任务书。
    - HR018 的 26 条关系使用 `accept`／`revise`／`reject` 三列，而不是统一 `decision` 字段；8 条 source prerequisite 没有决定字段。编排时必须避免把 34 行全部误报为 34 个空白决定。
    - HR023／HR028 的状态文件不代表空白人审队列。
    - HR032 的唯一 live queue 是 `outputs/R10_official_collaboration_universe_v1/HR032_partner_alias_crosswalk_review_v1.csv`（8 行、单字段 `decision`）。它审 source-label→canonical/JV/member/registry crosswalk，不追认 source-label 为 actor 身份。

    ## 6. 证据与写作边界

    - 候选 edge、共同署名、共同活动与事件重复参与不是稳定联盟。
    - source/archive 决定只处理元数据、locator、保存状态和可支持范围，不批准 actor、关系、金额或解释。
    - project cost、aggregate、NOFO、sponsor tier、membership、service presence 不得写成 actor payment、funding 或政治立场。
    - S002 的 machine display alias、法律前缀差异与 JV/member 字符串不得直接写成同一法人、registry actor 或独立资源边；HR032 也不得把复合体项目费拆给成员。
    - 选举观察不支持票数贡献、胜负、政策效果或因果。
    - 与那国保持前线／安全环境、地方自治、公投、台湾邻近与生活／健康安全主框架，不强行环境化。

    ## 7. 重生与复核

    生成命令：

    ```powershell
    python scripts/make_human_review_orchestration_v1.py
    ```

    脚本只读取 HR CSV、`figure_manifest_v1.csv` 与 `missing_assets_v1.csv`，只写本目录。当前已完成双跑 SHA-256 零差异与依赖图视觉检查。
    """).strip() + "\n"


def validate(inventory: list[dict[str, object]], batches: list[dict[str, object]]) -> None:
    ids = [str(row["hr_id"]) for row in inventory]
    expected = [f"HR{number:03d}" for number in range(16, 33)]
    if ids != expected:
        raise ValueError(f"Inventory HR sequence mismatch: {ids}")
    if len(batches) != 13:
        raise ValueError(f"Expected 13 orchestration batch rows, found {len(batches)}")
    for row in inventory:
        blank = int(row["blank_decision_row_count"])
        decisions = int(row["decision_row_count"])
        completed = int(row["completed_decision_row_count"])
        if blank + completed != decisions:
            raise ValueError(f"Decision count mismatch for {row['hr_id']}")
    inventory_decisions = sum(int(row["decision_row_count"]) for row in inventory)
    batch_decisions = sum(int(row["decision_rows"]) for row in batches)
    if batch_decisions != inventory_decisions:
        raise ValueError(
            f"Recommended batches must partition every decision row exactly once: "
            f"inventory={inventory_decisions}, batches={batch_decisions}"
        )
    inventory_ancillary = sum(int(row["ancillary_row_count"]) for row in inventory)
    batch_ancillary = sum(int(row["ancillary_rows"]) for row in batches)
    if batch_ancillary != inventory_ancillary:
        raise ValueError(
            f"Recommended batches must partition ancillary rows exactly once: "
            f"inventory={inventory_ancillary}, batches={batch_ancillary}"
        )
    lookup = by_hr(inventory)
    if int(lookup["HR018"]["ancillary_row_count"]) != 8:
        raise ValueError("HR018 must distinguish 8 source prerequisites from decision rows")
    if int(lookup["HR019"]["actual_row_count_total"]) != 115:
        raise ValueError("HR019 live CSV total should be 9+30+76=115 after HR-027")
    if int(lookup["HR032"]["actual_row_count_total"]) != 8:
        raise ValueError("HR032 live partner alias/JV crosswalk queue should contain 8 rows")
    if int(lookup["HR032"]["decision_row_count"]) != 8:
        raise ValueError("HR032 must expose 8 single-field human decisions")
    for hr in ("HR023", "HR028"):
        if int(lookup[hr]["actual_row_count_total"]) != 0:
            raise ValueError(f"{hr} should have no CSV rows in this package")
    if sum(int(row["actual_row_count_total"]) for row in inventory) != 397:
        raise ValueError("Expected 397 current HR016–HR032 CSV rows after HR-027 and dependent package regeneration")
    if inventory_decisions != 389:
        raise ValueError("Expected 389 current HR016–HR032 decision rows after HR-027 and dependent package regeneration")
    if inventory_ancillary != 8:
        raise ValueError("Expected 8 current ancillary source-prerequisite rows")
    required_tokens = (
        "HR027→HR029", "HR018", "HR021-001–007", "AP123", "HR025", "HR031",
        "HR032", "future canonical actor/JV/member crosswalk",
    )
    joined = " ".join(str(value) for row in batches for value in row.values())
    for token in required_tokens:
        if token not in joined:
            raise ValueError(f"Required dependency token missing from batches: {token}")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    inventory = inventory_rows()
    batches = batch_rows(inventory)
    validate(inventory, batches)
    write_csv(INVENTORY_PATH, inventory, INVENTORY_FIELDS)
    write_csv(BATCH_PATH, batches, BATCH_FIELDS)
    make_dependency_graph(inventory)
    README_PATH.write_text(make_readme(inventory, batches), encoding="utf-8", newline="\n")

    for path in (INVENTORY_PATH, BATCH_PATH, GRAPH_SVG_PATH, GRAPH_PNG_PATH, README_PATH):
        if not path.exists() or path.stat().st_size < 500:
            raise ValueError(f"Missing or unexpectedly small output: {path}")
    print(
        "Human-review orchestration generated: "
        f"{sum(int(row['actual_row_count_total']) for row in inventory)} CSV rows / "
        f"{sum(int(row['decision_row_count']) for row in inventory)} decision rows / "
        f"{sum(int(row['blank_decision_row_count']) for row in inventory)} blank decisions / "
        f"{len(batches)} batch rows."
    )


if __name__ == "__main__":
    main()
