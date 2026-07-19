#!/usr/bin/env python3
"""Build the report figure -> data -> source -> script -> human-gate crosswalk."""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs/report_assembly_v1"
MANIFEST = OUT / "figure_manifest_v1.csv"
CROSSWALK = OUT / "figure_traceability_crosswalk_v1.csv"
GAP_REGISTER = OUT / "missing_assets_v1.csv"


ROUTES = [
    {
        "prefix": "outputs/phase1_visuals_v1/",
        "script": "scripts/make_phase1_visuals.py",
        "data": "data/interim/15_funding_or_support_edges_sample_v0.csv",
        "sources": "data/interim/15_funding_or_support_edges_sample_v0.csv",
    },
    {
        "prefix": "outputs/R01_R02_actor_issue_v1/",
        "script": "scripts/make_r01_r02_actor_issue.py",
        "data": "data/interim/01_actor_registry_initial_v0.csv;data/interim/03_issue_taxonomy_v0.csv;data/interim/07_actor_issue_edges_initial_v0.csv",
        "sources": "data/interim/07_actor_issue_edges_initial_v0.csv",
    },
    {
        "prefix": "outputs/R03_spatial_dossier_v1/",
        "script": "scripts/make_r03_spatial_dossier_v1.py",
        "data": "data/interim/01_actor_registry_initial_v0.csv;data/interim/04_place_registry_v0.csv;data/interim/08_actor_place_edges_initial_v0.csv;data/interim/32_actor_place_semantic_candidates_v1.csv",
        "sources": "outputs/R03_spatial_dossier_v1/source_crosswalk_v1.csv",
    },
    {
        "prefix": "outputs/R04_sakishima_frame_corpus_v0/",
        "script": "scripts/merge_hr016_hr017_modules_v1.py",
        "data": "data/interim/19_sakishima_frame_corpus_v0.csv;outputs/R04_sakishima_frame_corpus_v0/entity_frame_safe_matrix_v0.csv",
        "sources": "outputs/R04_sakishima_frame_corpus_v0/online_evidence_safe_sources_v0.csv",
    },
    {
        "prefix": "outputs/R05_coaction_v1/",
        "script": "scripts/merge_hr020_hr026_v1.py",
        "data": "data/interim/25_coaction_event_participation_v0.csv",
        "sources": "data/interim/25_coaction_event_participation_v0.csv",
    },
    {
        "prefix": "outputs/R05_R07_heterogeneous_repertoire_v1/",
        "script": "scripts/make_r05_r07_heterogeneous_repertoire_v1.py",
        "data": "data/interim/09_actor_event_venue_edges_v0.csv;data/interim/18_legal_policy_actor_roles_v0.csv;data/interim/35_heterogeneous_event_repertoire_v1.csv",
        "sources": "outputs/R05_R07_heterogeneous_repertoire_v1/input_layer_audit_v1.csv;data/interim/18_legal_policy_actor_roles_v0.csv",
    },
    {
        "prefix": "outputs/R06_R07_R11_pathways_v1/",
        "script": "scripts/render_r06_r07_r11_current.py",
        "data": "outputs/R06_R07_R11_pathways_v1/r06_pathway_comparison_v0.csv;outputs/R06_R07_R11_pathways_v1/r07_venue_shift_stages_v0.csv;outputs/R06_R07_R11_pathways_v1/r11_external_entry_matrix_v0.csv",
        "sources": "data/interim/26_actor_event_venue_target_entry_modes_v0.csv",
    },
    {
        "prefix": "outputs/R08_legal_procedure_v1/",
        "script": "scripts/make_r08_legal_procedure_v1.py",
        "data": "data/interim/17_legal_policy_procedure_cases_v0.csv;data/interim/18_legal_policy_actor_roles_v0.csv",
        "sources": "data/interim/17_legal_policy_procedure_cases_v0.csv;data/interim/18_legal_policy_actor_roles_v0.csv",
    },
    {
        "prefix": "outputs/R09_referendum_process_v0/",
        "script": "scripts/merge_hr016_hr017_modules_v1.py",
        "data": "data/interim/20_referendum_process_stages_v0.csv;outputs/R09_referendum_process_v0/actor_process_roles_v0.csv",
        "sources": "outputs/R09_referendum_process_v0/source_register_v0.csv;outputs/R09_referendum_process_v0/source_table_v0.csv",
    },
    {
        "prefix": "outputs/R09_election_civic_interface_v1/fig_r09_noncausal_mechanism_v1.png",
        "script": "scripts/render_r09_election_mechanism_current.py",
        "data": "data/interim/33_r09_election_civic_events_v1.csv",
        "sources": "outputs/R09_election_civic_interface_v1/source_proposals_v1.csv;outputs/next_wave_source_integration_v1/proposal_to_source_crosswalk_v1.csv",
    },
    {
        "prefix": "outputs/R09_election_civic_interface_v1/",
        "script": "scripts/merge_hr020_hr026_v1.py",
        "data": "data/interim/33_r09_election_civic_events_v1.csv",
        "sources": "outputs/R09_election_civic_interface_v1/source_proposals_v1.csv;outputs/next_wave_source_integration_v1/proposal_to_source_crosswalk_v1.csv",
    },
    {
        "prefix": "outputs/R10_administrative_collaboration_v0/",
        "script": "scripts/make_r10_admin_collaboration.py",
        "data": "data/interim/21_admin_collaboration_relations_v0.csv;data/interim/22_admin_amount_observations_v0.csv;data/interim/23_admin_function_observations_v0.csv",
        "sources": "outputs/R10_administrative_collaboration_v0/source_crosswalk_v1.csv",
    },
    {
        "prefix": "outputs/R10_official_collaboration_universe_v1/",
        "script": "scripts/make_r10_official_collaboration_universe_v1.py",
        "data": "outputs/R10_official_collaboration_universe_v1/official_collaboration_source_universe_v1.csv;outputs/R10_official_collaboration_universe_v1/issue_mechanism_matrix_v1.csv;outputs/R10_official_collaboration_universe_v1/department_mechanism_matrix_v1.csv;outputs/R10_official_collaboration_universe_v1/partner_display_alias_summary_v1.csv",
        "sources": "outputs/R10_official_collaboration_universe_v1/official_collaboration_source_universe_v1.csv",
    },
    {
        "prefix": "outputs/coverage_audit_v1/",
        "script": "scripts/make_coverage_audit_v1.py",
        "data": "data/interim/01_actor_registry_initial_v0.csv;data/interim/05_source_log_initial_v0.csv;data/interim/24_r01_r02_actor_issue_layered_v0.csv;data/interim/08_actor_place_edges_initial_v0.csv;data/interim/27_coverage_audit_cells_v1.csv",
        "sources": "data/interim/05_source_log_initial_v0.csv;source_docs/source_archive/source_archive_manifest.csv",
    },
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def split_paths(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def collect_source_ids(paths: list[str], central_ids: set[str]) -> list[str]:
    found: set[str] = set()
    for rel in paths:
        path = ROOT / rel
        if not path.exists() or path.suffix.lower() not in {".csv", ".md", ".txt"}:
            continue
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        found.update(source_id for source_id in re.findall(r"\bS\d{3}\b", text) if source_id in central_ids)
    return sorted(found, key=lambda value: int(value[1:]))


def collect_ids(paths: list[str], pattern: str) -> list[str]:
    found: set[str] = set()
    for rel in paths:
        path = ROOT / rel
        if not path.exists() or path.suffix.lower() not in {".csv", ".md", ".txt"}:
            continue
        found.update(re.findall(pattern, path.read_text(encoding="utf-8-sig", errors="replace")))
    return sorted(found)


def module_numbers(value: str) -> set[int]:
    return {int(number) for number in re.findall(r"R0?(\d+)", value)}


def main() -> None:
    figures = [
        row for row in read_csv(MANIFEST)
        if row["asset_type"] == "figure" and row["formal_use_status"] != "superseded_do_not_use"
    ]
    source_log = read_csv(ROOT / "data/interim/05_source_log_initial_v0.csv")
    central_ids = {row["source_id"] for row in source_log}
    claims = read_csv(ROOT / "data/interim/38_report_claim_evidence_audit_v1.csv")
    rows: list[dict[str, str]] = []
    errors: list[str] = []

    for figure in figures:
        route = next((candidate for candidate in ROUTES if figure["primary_path"].startswith(candidate["prefix"])), None)
        if route is None:
            errors.append(f"{figure['asset_id']}: no route for {figure['primary_path']}")
            continue
        data_paths = split_paths(route["data"])
        source_paths = split_paths(route["sources"])
        checked_paths = [figure["primary_path"], route["script"], *data_paths, *source_paths]
        missing = [rel for rel in checked_paths if not (ROOT / rel).exists()]
        if missing:
            errors.append(f"{figure['asset_id']}: missing {','.join(missing)}")
        source_ids = collect_source_ids(source_paths, central_ids)
        evidence_note_ids = collect_ids(data_paths + source_paths, r"\bEN\d{4}\b")
        figure_modules = module_numbers(figure["module"])
        if figure["asset_id"] in {"F035", "F036"}:
            # The source-universe figures are deliberately actor/relation-free.
            # Do not inherit the HR-018-blocked purposive-sample claim merely
            # because all three assets share the broad R10 module label.
            linked_claims = [
                claim for claim in claims
                if claim["module"] == "R10"
                and (
                    "complete S002 FY2024 source universe" in claim["claim_text"]
                    or "two S002 source-universe figures" in claim["claim_text"]
                )
            ]
        else:
            linked_claims = [
                claim for claim in claims
                if (figure_modules and figure_modules & module_numbers(claim["module"]))
                or (figure["module"] == "基础建设" and claim["module"] in {"coverage", "report_status"})
            ]
        claim_ids = sorted({claim["claim_id"] for claim in linked_claims})
        claim_statuses = Counter(claim["publish_status"] for claim in linked_claims)
        if not claim_ids:
            errors.append(f"{figure['asset_id']}: no linked report claim")
        rows.append({
            "asset_id": figure["asset_id"],
            "module": figure["module"],
            "title_cn": figure["title_cn"],
            "figure_path": figure["primary_path"],
            "generation_script": route["script"],
            "formal_data_paths": ";".join(data_paths),
            "source_crosswalk_paths": ";".join(source_paths),
            "central_source_id_count": str(len(source_ids)),
            "central_source_ids": ";".join(source_ids),
            "report_claim_count": str(len(claim_ids)),
            "report_claim_ids": ";".join(claim_ids),
            "claim_publish_status_counts": ";".join(
                f"{status}:{claim_statuses[status]}" for status in ("safe", "revise", "block") if claim_statuses[status]
            ),
            "evidence_note_ids": ";".join(evidence_note_ids),
            "evidence_note_trace": "linked" if evidence_note_ids else "not_used__formal_table_or_role_layer",
            "locator_trace_status": "indexed_to_central_source_log__residual_precision_MA013",
            "fact_layer": figure["fact_layer"],
            "formal_use_status": figure["formal_use_status"],
            "human_gate": figure["hr_gate"],
            "freeze_action": figure["freeze_action"],
            "all_paths_exist": "yes" if not missing else "no",
            "traceability_status": (
                "complete_pending_gate"
                if figure["formal_use_status"] == "freeze_required"
                else "complete_ready"
            ),
        })

    if errors:
        raise RuntimeError("Traceability validation failed:\n" + "\n".join(errors))
    if len(rows) != 27:
        raise RuntimeError(f"Expected 27 non-superseded report figures, found {len(rows)}")
    if any(row["all_paths_exist"] != "yes" for row in rows):
        raise RuntimeError("A traceability path is missing")

    fields = [
        "asset_id", "module", "title_cn", "figure_path", "generation_script",
        "formal_data_paths", "source_crosswalk_paths", "central_source_id_count",
        "central_source_ids", "report_claim_count", "report_claim_ids",
        "claim_publish_status_counts", "evidence_note_ids", "evidence_note_trace",
        "locator_trace_status", "fact_layer", "formal_use_status", "human_gate",
        "freeze_action", "all_paths_exist", "traceability_status",
    ]
    write_csv(CROSSWALK, rows, fields)

    gaps = read_csv(GAP_REGISTER)
    for gap in gaps:
        if gap["missing_id"] == "MA010":
            gap["status"] = "completed_v1"
            gap["notes"] = "27 张非 superseded 正文图已有 claim→evidence/formal table→locator/source→data→script→human-gate 追溯行；冻结后随最终图和 claim audit 重跑"
    write_csv(GAP_REGISTER, gaps, list(gaps[0]))

    status = Counter(row["traceability_status"] for row in rows)
    report = f"""# 正式报告图件追溯核验 v1

- 纳入非 superseded 正文图：**{len(rows)}**
- 路径完整：**{sum(row['all_paths_exist'] == 'yes' for row in rows)}/{len(rows)}**
- 当前可用：**{status['complete_ready']}**
- 追溯完整、仍待人工 gate 或技术冻结／重生：**{status['complete_pending_gate']}**
- 中央 source log：**{len(central_ids)}** 条
- Claim 链完整：**{sum(bool(row['report_claim_ids']) for row in rows)}/{len(rows)}**
- Evidence-note 直接引用图：**{sum(row['evidence_note_trace'] == 'linked' for row in rows)}**；其余图以正式关系／角色／聚合表为事实层

每行均指向图件、报告 claim、evidence-note 或正式关系／角色表、locator/source crosswalk、生成脚本、当前事实层、人工 gate 与冻结动作。`complete_pending_gate` 包含尚待人工 gate 和“人审已完成但仍须按现行层重绘／冻结”的技术缺口；它只表示追溯链完整，不表示图中候选事实已经获批。残余页码／案号精修继续由 MA013 控制。
"""
    (OUT / "figure_traceability_validation_v1.md").write_text(report, encoding="utf-8")
    print(f"figures={len(rows)} ready={status['complete_ready']} pending_gate={status['complete_pending_gate']}")


if __name__ == "__main__":
    main()
