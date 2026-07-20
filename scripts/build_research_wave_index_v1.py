from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "outputs" / "research_wave_topic_selection_v1"
H1_DIR = ROOT / "outputs" / "research_wave_h1_documentation_visibility_v1"
H2_DIR = ROOT / "outputs" / "research_wave_h2_two_ecologies_v1"
H3_DIR = ROOT / "outputs" / "research_wave_h3_frontline_memory_v1"

OUTPUT_FILENAMES = (
    "frontend_research_modules_v1.json",
    "wave_manifest_v1.json",
    "validation_report_v1.md",
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def build_modules() -> list[dict[str, Any]]:
    h1_metrics = load_json(H1_DIR / "metrics_v1.json")
    h2_metrics = load_json(H2_DIR / "metrics_v1.json")
    h3_manifest = load_json(H3_DIR / "manifest.json")
    h3_layers = {
        row["hypothesis_id"]: row
        for row in load_csv(H3_DIR / "hypothesis_layers_v1.csv")
    }
    h2_human = load_csv(H2_DIR / "human_review_queue_v1.csv")
    h2_search = load_csv(H2_DIR / "further_search_queue_v1.csv")
    h1_followup = load_csv(H1_DIR / "further_research_queue_v1.csv")
    h3_human = load_csv(H3_DIR / "human_review_queue_v1.csv")
    h3_local = load_csv(H3_DIR / "local_retrieval_queue_v1.csv")

    h1_assets = [
        H1_DIR / "brief_v1.md",
        H1_DIR / "sensitivity_scenarios_v1.csv",
        H1_DIR / "actor_issue_edge_source_incidence_v1.csv",
        H1_DIR / "scenario_removed_edges_v1.csv",
        H1_DIR / "leave_one_source_out_v1.csv",
        H1_DIR / "paired_deletion_comparison_v1.csv",
        H1_DIR / "source_host_mapping_proposals_v1.csv",
        H1_DIR / "further_research_queue_v1.csv",
    ]
    h2_assets = [
        H2_DIR / "H2_two_ecologies_brief_v1.md",
        H2_DIR / "service_core_actors_v1.csv",
        H2_DIR / "accountability_comparison_actors_v1.csv",
        H2_DIR / "dyadic_relation_ecology_audit_v1.csv",
        H2_DIR / "case_role_ecology_audit_v1.csv",
        H2_DIR / "typed_event_ecology_audit_v1.csv",
        H2_DIR / "r10_interface_audit_v1.csv",
        H2_DIR / "place_overlap_v1.csv",
        H2_DIR / "coverage_gaps_v1.csv",
        H2_DIR / "human_review_queue_v1.csv",
        H2_DIR / "further_search_queue_v1.csv",
        H2_DIR / "metrics_v1.json",
    ]
    h3_assets = [
        H3_DIR / "brief_v1.md",
        H3_DIR / "source_observations_v1.csv",
        H3_DIR / "diffusion_carrier_candidates_v1.csv",
        H3_DIR / "event_participant_candidates_v1.csv",
        H3_DIR / "hypothesis_layers_v1.csv",
        H3_DIR / "human_review_queue_v1.csv",
        H3_DIR / "local_retrieval_queue_v1.csv",
        H3_DIR / "source_governance_v1.csv",
    ]
    for path in [*h1_assets, *h2_assets, *h3_assets]:
        if not path.is_file():
            raise FileNotFoundError(path)

    h1_summary = h1_metrics["current_result_summary"]
    h2_local_or_internal = sum(
        "local" in row["mode"] or "internal" in row["mode"]
        for row in h2_search
    )
    h1_human_gate_count = sum(
        "human_review" in row["mode"] or "principal" in row["mode"]
        for row in h1_followup
    )
    h1_local_component_count = sum(
        "local" in row["mode"] for row in h1_followup
    )
    modules = [
        {
            "module_id": "H1_DOCUMENTATION_VISIBILITY_V1",
            "hypothesis_id": "H1",
            "title": "少数高承载名单对 actor–issue 可见层的来源依赖",
            "data_layer": "research_only",
            "claim_status": "candidate",
            "review_status": "ai_seeded",
            "frontend_eligibility": "not_frontend_ready",
            "integration_status": "indexed_not_integrated",
            "row_contract_status": "heterogeneous_drilldowns_not_normalized",
            "summary": (
                "移除 S003/S004/S006 的独占证据支持后，E3/E4 可见层由 "
                f"{h1_summary['baseline_e3plus_edges']} 条边／"
                f"{h1_summary['baseline_e3plus_observed_actors']} 个有边 actor 降至 "
                f"{h1_summary['source_drop_big3_edges']}／"
                f"{h1_summary['source_drop_big3_observed_actors']}；"
                "其中约 84% 的边与 actor 损失由 S004 单源造成。"
                "这只支持来源集中／可见层依赖；source 删除与 actor 删除"
                "不是匹配反事实，也不证明真实社会网络中心性。"
            ),
            "interpretation_limits": [
                "source deletion is an evidence-layer sensitivity test, not a social intervention",
                "S004 dominates the current effect; three sources do not establish a repeated documentation-capacity mechanism",
                "source deletion and actor deletion are unmatched units, not a counterfactual",
                "source-host mappings remain proposal_not_human_reviewed",
                "registry source_refs are not a complete actor×source incidence universe",
                "issue degree is not influence, activity strength, or organizational lifespan",
            ],
            "open_human_or_principal_gate_count": h1_human_gate_count,
            "open_followup_task_count": len(h1_followup),
            "contains_local_retrieval_component_count": (
                h1_local_component_count
            ),
            "primary_metrics": {
                "baseline_e3plus_edges": h1_summary["baseline_e3plus_edges"],
                "baseline_e3plus_observed_actors": h1_summary[
                    "baseline_e3plus_observed_actors"
                ],
                "source_drop_big3_edges": h1_summary["source_drop_big3_edges"],
                "source_drop_big3_observed_actors": h1_summary[
                    "source_drop_big3_observed_actors"
                ],
                "actor_drop_big3_edges": h1_summary["actor_drop_big3_edges"],
                "actor_drop_big3_observed_actors": h1_summary[
                    "actor_drop_big3_observed_actors"
                ],
                "s004_removed_edge_count": h1_metrics["leave_one_source_out"][
                    "s004"
                ]["removed_edge_count"],
                "s004_lost_observed_actor_count": h1_metrics[
                    "leave_one_source_out"
                ]["s004"]["lost_observed_actor_count"],
                "source_ref_degree_spearman": h1_metrics["diagnostics"][
                    "spearman_resolved_registry_source_ref_count_vs_active_issue_degree"
                ],
            },
            "assets": [relative(path) for path in h1_assets],
        },
        {
            "module_id": "H2_TWO_ECOLOGIES_V1",
            "hypothesis_id": "H2",
            "title": "基地周边两套功能生态及其未测接口",
            "data_layer": "research_only",
            "claim_status": "candidate",
            "review_status": "ai_seeded",
            "frontend_eligibility": "not_frontend_ready",
            "integration_status": "indexed_not_integrated",
            "row_contract_status": "heterogeneous_audit_rows_not_normalized",
            "summary": (
                f"按当前 registry 规则得到 {h2_metrics['service_core_actor_count']} 个"
                "服务侧比较 actor；按候选锚点规则得到 "
                f"{h2_metrics['accountability_comparison_actor_count']} 个问责侧"
                "候选 actor，其中 "
                f"{h2_metrics['accountability_human_reviewed_anchor_actor_count']} 个"
                "至少有一条人审锚点边、"
                f"{h2_metrics['accountability_candidate_only_anchor_actor_count']} 个"
                "仅有候选锚点。14+8 条 dyadic、4 条 typed-event 与"
                "35 条 R10 目的性记录中尚未编码直接跨组组织关系；"
                "27 条案件角色中没有服务侧 actor。人物未测，recipient "
                "不完整。"
            ),
            "interpretation_limits": [
                "zero encoded cross relations means absence in current inputs only",
                h2_metrics["public_person_overlap_status"],
                h2_metrics["complete_recipient_network_status"],
                "same place does not prove contact; P001 is a prefecture-wide broad node",
                "service function does not establish a pro-base or anti-base stance",
                "base production remains hypothesis_only rather than a causal finding",
            ],
            "open_human_gate_count": len(h2_human),
            "open_search_task_count": len(h2_search),
            "contains_local_or_internal_component_count": (
                h2_local_or_internal
            ),
            "primary_metrics": {
                "service_core_actor_count": h2_metrics[
                    "service_core_actor_count"
                ],
                "accountability_comparison_actor_count": h2_metrics[
                    "accountability_comparison_actor_count"
                ],
                "accountability_human_reviewed_anchor_actor_count": (
                    h2_metrics[
                        "accountability_human_reviewed_anchor_actor_count"
                    ]
                ),
                "accountability_candidate_only_anchor_actor_count": (
                    h2_metrics[
                        "accountability_candidate_only_anchor_actor_count"
                    ]
                ),
                "reviewed_dyadic_relation_count": h2_metrics[
                    "reviewed_dyadic_relation_count"
                ],
                "candidate_dyadic_relation_count": h2_metrics[
                    "candidate_dyadic_relation_count"
                ],
                "cross_ecology_dyadic_observed_count": h2_metrics[
                    "cross_ecology_dyadic_observed_count"
                ],
                "cross_ecology_event_observed_count": h2_metrics[
                    "cross_ecology_event_observed_count"
                ],
                "specific_shared_place_node_ids": [
                    place_id
                    for place_id in h2_metrics["shared_place_node_ids"]
                    if place_id != "P001"
                ],
            },
            "assets": [relative(path) for path in h2_assets],
        },
        {
            "module_id": "H3_FRONTLINE_MEMORY_V1",
            "hypothesis_id": "H3",
            "title": "前线化／战争记忆能否成为跨议题共同语言",
            "data_layer": "research_only",
            "claim_status": "candidate",
            "review_status": "ai_seeded",
            "frontend_eligibility": "not_frontend_ready",
            "integration_status": "indexed_not_integrated",
            "row_contract_status": (
                "h3_rows_normalized_but_human_and_source_governance_gated"
            ),
            "summary": (
                f"现有档案形成 {h3_manifest['package_counts']['source_observations']} "
                "条具定位观察与若干事件级接触／载体路径候选；传播方向、"
                "目标组织独立采用及持续共同动员均未确认。由于年代和文体"
                "不平衡，词汇增长仍不可检验。"
            ),
            "interpretation_limits": [
                "schema tag growth is not evidence of social vocabulary growth",
                "event participation or endorsement is not a stable alliance",
                "contact, speaking, endorsement, and organizing are not interchangeable with independent frame adoption",
                "carrier endpoints do not establish diffusion direction",
                "a common language is not the same as a common organization",
                "Japan-wide war-memory sensitivity is outside the present evidence",
            ],
            "open_human_gate_count": len(h3_human),
            "open_local_retrieval_task_count": len(h3_local),
            "primary_metrics": {
                "source_observation_count": h3_manifest["package_counts"][
                    "source_observations"
                ],
                "diffusion_carrier_count": h3_manifest["package_counts"][
                    "diffusion_carriers"
                ],
                "event_participant_count": h3_manifest["package_counts"][
                    "event_participants"
                ],
                "source_governance_blocker_count": h3_manifest[
                    "source_governance_blocker_count"
                ],
                "vocabulary_growth_status": h3_layers["H3a"][
                    "current_assessment"
                ],
                "diffusion_status": h3_layers["H3b"]["current_assessment"],
                "mobilization_status": h3_layers["H3c"][
                    "current_assessment"
                ],
            },
            "assets": [relative(path) for path in h3_assets],
        },
    ]
    return modules


def build_index(output_dir: Path = DEFAULT_OUTPUT) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    modules = build_modules()
    result = {
        "schema_version": "research_wave_module_index_v1",
        "as_of_date": "2026-07-20",
        "adapter_kind": (
            "module_directory_index_not_row_level_observation_contract"
        ),
        "data_scope": "additive_research_only",
        "central_tables_mutated": False,
        "current_frontend_contract_mutated": False,
        "integration_status": (
            "module_index_ready_observation_exports_gated"
        ),
        "allowed_surface": (
            "future_explicit_research_module_after_separate_approval"
        ),
        "required_gate_before_integration": (
            "principal selects a module, approves bounded claim wording, "
            "closes module-specific human/source gates, and approves a "
            "separate row-level frontend export"
        ),
        "modules": modules,
    }
    frontend_path = output_dir / "frontend_research_modules_v1.json"
    write_json(frontend_path, result)

    asset_paths = [
        ROOT / asset
        for module in modules
        for asset in module["assets"]
    ]
    manifest = {
        "schema_version": "research_wave_module_index_manifest_v1",
        "as_of_date": "2026-07-20",
        "module_count": len(modules),
        "module_ids": [module["module_id"] for module in modules],
        "all_assets_exist": all(path.is_file() for path in asset_paths),
        "all_modules_research_only": all(
            module["data_layer"] == "research_only" for module in modules
        ),
        "central_tables_mutated": False,
        "current_frontend_contract_mutated": False,
        "frontend_adapter_sha256": sha256(frontend_path),
        "asset_hashes": {
            relative(path): sha256(path)
            for path in sorted(asset_paths, key=lambda item: relative(item))
        },
    }
    write_json(output_dir / "wave_manifest_v1.json", manifest)

    report = """# Research wave index validation v1

- Three research-only modules indexed: PASS
- Current central tables mutated: NO
- Current exploration-system contract mutated: NO
- Existing frontend bundle mutated: NO
- Asset paths present and hashed: PASS
- Integration state: `module_index_ready_observation_exports_gated`
- Allowed future surface: a separately approved explicit research module

This file is a module directory and asset index only. It does not claim that
heterogeneous package rows satisfy a shared frontend observation contract.
Candidate interpretations remain outside the current reviewed and research
frontend layers until a separate row-level export and human gate are approved.
"""
    (output_dir / "validation_report_v1.md").write_text(
        report,
        encoding="utf-8",
    )
    return result


if __name__ == "__main__":
    built = build_index()
    print(
        "Research-wave module index: "
        f"{len(built['modules'])} modules; "
        f"integration={built['integration_status']}"
    )
