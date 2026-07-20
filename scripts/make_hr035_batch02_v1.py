from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "outputs" / "actor_issue_claim_freeze_v1"

# Batch 2 is the complete current set satisfying all four conditions:
# active edge; E4; HR-019 scope reviewed; actor-issue fact still ai_seeded.
# IDs are frozen so later central changes fail loudly instead of silently
# changing an already dispatched human-review assignment.
BATCH_02_EDGE_IDS = [
    "AI016",
    "AI040",
    "AI042",
    "AI044",
    "AI119",
    "AI121",
    "AI157",
    "AI158",
    "AI159",
    "AI223",
    "AI225",
    "AI226",
    "AI232",
    "AI233",
    "AI234",
    "AI236",
    "AI237",
    "AI240",
]

# These actors would newly rely on accepted edge facts while their registry
# identity remains ai_seeded. Review them once each; do not repeat an identity
# decision on every issue edge.
IDENTITY_COMPANION_ACTOR_IDS = ["A007", "A017", "A018", "A049", "A066"]

SPECIAL_EDGE_WARNINGS = {
    "AI016": (
        "S005 虽标 E4，但既有 scope 已指出单次声明不足以支持长期定位；"
        "须补持续项目材料，或收窄为事件性边。"
    ),
    "AI044": (
        "当前 edge 仅引 S024（E2），且既有 scope 已指出来源错位；"
        "S023 可辅助组织成立／身份，但仍须判断是否需要组织自身材料。"
    ),
    "AI119": "当前直接来源最高 E3，不得仅因 edge 当前标 E4 而保留 E4。",
    "AI121": "当前直接来源最高 E3，不得仅因 edge 当前标 E4 而保留 E4。",
    "AI232": "当前直接来源最高 E3，不得仅因 edge 当前标 E4 而保留 E4。",
    "AI234": "当前直接来源最高 E3，不得仅因 edge 当前标 E4 而保留 E4。",
}

EDGE_TASK_FIELDS = [
    "review_item_id",
    "task_id",
    "batch_id",
    "workstream",
    "batch_order",
    "edge_id",
    "actor_id",
    "actor_name",
    "actor_identity_review_status_current",
    "actor_identity_evidence_level_current",
    "actor_identity_source_refs",
    "actor_identity_gate",
    "identity_companion_item_id",
    "default_graph_activation_condition",
    "issue_id",
    "issue_label",
    "relation_basis",
    "evidence_level_current",
    "review_status_current",
    "source_ref",
    "source_titles",
    "source_urls",
    "source_archive_paths",
    "source_archive_statuses",
    "source_level_ceiling_current",
    "source_gap_flag",
    "existing_scope_kind",
    "existing_scope_claim_status",
    "existing_scope_approved_formulation",
    "existing_scope_boundary",
    "existing_scope_decision_source_report",
    "attention_flag",
    "precise_fact_question",
    "required_review_scope",
    "allowed_decisions",
    "human_decision",
    "revised_review_status",
    "evidence_level_final",
    "approved_formulation",
    "review_scope_final",
    "reviewed_fields",
    "claim_status",
    "confirmed_scope",
    "missing_scope",
    "interpretation_limit",
    "scope_revision_required",
    "human_reviewer",
    "review_date",
    "review_note",
]

IDENTITY_TASK_FIELDS = [
    "review_item_id",
    "task_id",
    "batch_id",
    "workstream",
    "batch_order",
    "actor_id",
    "canonical_name_current",
    "actor_class_current",
    "origin_type_current",
    "legal_status_current",
    "evidence_level_current",
    "review_status_current",
    "source_ref",
    "source_titles",
    "source_urls",
    "source_archive_paths",
    "source_archive_statuses",
    "linked_batch02_edge_ids",
    "precise_identity_question",
    "required_review_scope",
    "allowed_decisions",
    "human_decision",
    "revised_review_status",
    "evidence_level_final",
    "canonical_name_final",
    "actor_class_final",
    "origin_type_final",
    "legal_status_final",
    "approved_identity_formulation",
    "reviewed_fields",
    "identity_interpretation_limit",
    "human_reviewer",
    "review_date",
    "review_note",
]

SOURCE_FIELDS = [
    "review_item_id",
    "item_type",
    "edge_id",
    "actor_id",
    "source_id",
    "source_title",
    "source_url",
    "source_type",
    "source_year",
    "source_evidence_level",
    "source_review_status",
    "what_it_supports",
    "support_scope",
    "locator",
    "archive_status",
    "local_path",
]

EDGE_DECISION_FIELDS = [
    "human_decision",
    "revised_review_status",
    "evidence_level_final",
    "approved_formulation",
    "review_scope_final",
    "reviewed_fields",
    "claim_status",
    "confirmed_scope",
    "missing_scope",
    "interpretation_limit",
    "scope_revision_required",
    "human_reviewer",
    "review_date",
    "review_note",
]

IDENTITY_DECISION_FIELDS = [
    "human_decision",
    "revised_review_status",
    "evidence_level_final",
    "canonical_name_final",
    "actor_class_final",
    "origin_type_final",
    "legal_status_final",
    "approved_identity_formulation",
    "reviewed_fields",
    "identity_interpretation_limit",
    "human_reviewer",
    "review_date",
    "review_note",
]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_rows(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def split_refs(value: str) -> list[str]:
    return [token.strip() for token in value.replace("；", ";").split(";") if token.strip()]


def resolve_sources(
    *,
    review_item_id: str,
    item_type: str,
    edge_id: str,
    actor_id: str,
    source_ref: str,
    sources: dict[str, dict[str, str]],
    archives: dict[str, dict[str, str]],
) -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]]:
    source_ids = split_refs(source_ref)
    if not source_ids:
        raise ValueError(f"{review_item_id} has no source_ref")
    if "S051" in source_ids:
        raise ValueError(f"{review_item_id} improperly relies on rejected S051")

    source_rows: list[dict[str, str]] = []
    archive_rows: list[dict[str, str]] = []
    bundle_rows: list[dict[str, str]] = []
    for source_id in source_ids:
        if source_id not in sources:
            raise ValueError(f"{review_item_id} has unresolved source ID {source_id}")
        if source_id not in archives:
            raise ValueError(f"{review_item_id} source {source_id} lacks an archive record")
        source = sources[source_id]
        archive = archives[source_id]
        if archive["archive_status"] not in {"archived", "manual_archived"}:
            raise ValueError(
                f"{review_item_id} source {source_id} is not reviewable: "
                f"{archive['archive_status']!r}"
            )
        source_rows.append(source)
        archive_rows.append(archive)
        bundle_rows.append(
            {
                "review_item_id": review_item_id,
                "item_type": item_type,
                "edge_id": edge_id,
                "actor_id": actor_id,
                "source_id": source_id,
                "source_title": source["title"],
                "source_url": source["url"],
                "source_type": source["source_type"],
                "source_year": source["year"],
                "source_evidence_level": source["evidence_level"],
                "source_review_status": source["review_status"],
                "what_it_supports": source["what_it_supports"],
                "support_scope": source.get("support_scope", ""),
                "locator": source.get("locator", ""),
                "archive_status": archive["archive_status"],
                "local_path": archive["local_path"],
            }
        )
    return source_rows, archive_rows, bundle_rows


def source_summary(
    source_rows: list[dict[str, str]], archive_rows: list[dict[str, str]]
) -> dict[str, str]:
    return {
        "source_titles": " || ".join(
            f"{row['source_id']} {row['title']}" for row in source_rows
        ),
        "source_urls": " || ".join(row["url"] for row in source_rows),
        "source_archive_paths": " || ".join(row["local_path"] for row in archive_rows),
        "source_archive_statuses": " || ".join(
            f"{row['source_id']}:{row['archive_status']}" for row in archive_rows
        ),
    }


def evidence_ceiling(source_rows: list[dict[str, str]]) -> str:
    levels = []
    for row in source_rows:
        value = row["evidence_level"].strip()
        if len(value) == 2 and value.startswith("E") and value[1].isdigit():
            levels.append(int(value[1]))
    if not levels:
        return ""
    return f"E{max(levels)}"


def main() -> None:
    edges = {
        row["edge_id"]: row
        for row in read_rows(ROOT / "data" / "interim" / "07_actor_issue_edges_initial_v0.csv")
    }
    active_edges = {
        row["edge_id"]
        for row in read_rows(
            ROOT / "outputs" / "R01_R02_actor_issue_v1" / "active_actor_issue_edges_v1.csv"
        )
    }
    actors = {
        row["actor_id"]: row
        for row in read_rows(ROOT / "data" / "interim" / "01_actor_registry_initial_v0.csv")
    }
    issues = {
        row["issue_id"]: row
        for row in read_rows(ROOT / "data" / "interim" / "03_issue_taxonomy_v0.csv")
    }
    sources = {
        row["source_id"]: row
        for row in read_rows(ROOT / "data" / "interim" / "05_source_log_initial_v0.csv")
    }
    archives = {
        row["source_id"]: row
        for row in read_rows(
            ROOT / "source_docs" / "source_archive" / "source_archive_manifest.csv"
        )
    }

    eligible_edge_ids = {
        edge_id
        for edge_id, edge in edges.items()
        if edge_id in active_edges
        and edge["evidence_level"] == "E4"
        and edge["review_status"] == "ai_seeded"
        and edge["scope_review_status"] in {"human_checked", "human_revised"}
    }
    if eligible_edge_ids != set(BATCH_02_EDGE_IDS):
        missing = sorted(set(BATCH_02_EDGE_IDS) - eligible_edge_ids)
        unexpected = sorted(eligible_edge_ids - set(BATCH_02_EDGE_IDS))
        raise ValueError(
            "HR-035 Batch 2 eligibility drifted; "
            f"missing={missing}, unexpected={unexpected}"
        )

    edge_rows: list[dict[str, str]] = []
    identity_rows: list[dict[str, str]] = []
    source_bundle: list[dict[str, str]] = []

    for order, edge_id in enumerate(BATCH_02_EDGE_IDS, start=1):
        edge = edges[edge_id]
        actor = actors[edge["actor_id"]]
        issue = issues[edge["issue_id"]]
        review_item_id = f"HR035-B02-{edge_id}"
        source_rows, archive_rows, bundle_rows = resolve_sources(
            review_item_id=review_item_id,
            item_type="edge_fact",
            edge_id=edge_id,
            actor_id=edge["actor_id"],
            source_ref=edge["source_ref"],
            sources=sources,
            archives=archives,
        )
        source_bundle.extend(bundle_rows)
        identity_item_id = (
            f"HR035-B02-ID-{edge['actor_id']}"
            if edge["actor_id"] in IDENTITY_COMPANION_ACTOR_IDS
            else ""
        )
        ceiling = evidence_ceiling(source_rows)
        source_gap = (
            f"edge_E4_exceeds_direct_source_ceiling_{ceiling}"
            if ceiling and ceiling != "E4"
            else ""
        )
        attention_parts = [
            "只判断组织自身的公开定位；不得从一次共同文件扩成稳定联盟或全部时期定位。"
        ]
        if identity_item_id:
            attention_parts.append(
                "该组织身份仍为 ai_seeded，默认已核图激活还需配套身份决定。"
            )
        if edge_id in SPECIAL_EDGE_WARNINGS:
            attention_parts.append(SPECIAL_EDGE_WARNINGS[edge_id])
        edge_rows.append(
            {
                "review_item_id": review_item_id,
                "task_id": "HR-035",
                "batch_id": "B02_E4_scope_reviewed_fact_pending",
                "workstream": "factual_actor_issue_review",
                "batch_order": str(order),
                "edge_id": edge_id,
                "actor_id": edge["actor_id"],
                "actor_name": actor["canonical_name"],
                "actor_identity_review_status_current": actor["review_status"],
                "actor_identity_evidence_level_current": actor["evidence_level"],
                "actor_identity_source_refs": actor["source_refs"],
                "actor_identity_gate": (
                    "companion_review_required"
                    if identity_item_id
                    else "already_human_reviewed"
                ),
                "identity_companion_item_id": identity_item_id,
                "default_graph_activation_condition": (
                    "edge_accept_or_revise_and_identity_companion_accept_or_revise"
                    if identity_item_id
                    else "edge_accept_or_revise"
                ),
                "issue_id": edge["issue_id"],
                "issue_label": issue["issue_label"],
                "relation_basis": edge["relation_basis"],
                "evidence_level_current": edge["evidence_level"],
                "review_status_current": edge["review_status"],
                "source_ref": edge["source_ref"],
                **source_summary(source_rows, archive_rows),
                "source_level_ceiling_current": ceiling,
                "source_gap_flag": source_gap,
                "existing_scope_kind": edge["scope_kind"],
                "existing_scope_claim_status": edge["scope_claim_status"],
                "existing_scope_approved_formulation": edge[
                    "scope_approved_formulation"
                ],
                "existing_scope_boundary": edge["scope_boundary"],
                "existing_scope_decision_source_report": edge[
                    "scope_decision_source_report"
                ],
                "attention_flag": " ".join(attention_parts),
                "precise_fact_question": (
                    f"现有归档来源是否足以确认 {actor['canonical_name']} 与 "
                    f"{issue['issue_label']} 的关系，且只支持到既有范围："
                    f"{edge['scope_approved_formulation']}？"
                ),
                "required_review_scope": (
                    "relation_existence;issue_mapping;source_ref;evidence_level;"
                    "interpretation_boundary"
                ),
                "allowed_decisions": (
                    "accept;revise;defer_second_source;defer_local;reject"
                ),
                **{field: "" for field in EDGE_DECISION_FIELDS},
            }
        )

    linked_edges_by_actor = {
        actor_id: [
            edge_id
            for edge_id in BATCH_02_EDGE_IDS
            if edges[edge_id]["actor_id"] == actor_id
        ]
        for actor_id in IDENTITY_COMPANION_ACTOR_IDS
    }
    for order, actor_id in enumerate(IDENTITY_COMPANION_ACTOR_IDS, start=1):
        actor = actors[actor_id]
        if actor["review_status"] != "ai_seeded":
            raise ValueError(
                f"{actor_id} identity no longer requires companion review: "
                f"{actor['review_status']!r}"
            )
        review_item_id = f"HR035-B02-ID-{actor_id}"
        source_rows, archive_rows, bundle_rows = resolve_sources(
            review_item_id=review_item_id,
            item_type="actor_identity",
            edge_id="",
            actor_id=actor_id,
            source_ref=actor["source_refs"],
            sources=sources,
            archives=archives,
        )
        source_bundle.extend(bundle_rows)
        identity_rows.append(
            {
                "review_item_id": review_item_id,
                "task_id": "HR-035",
                "batch_id": "B02_identity_companion",
                "workstream": "actor_identity_companion_review",
                "batch_order": str(order),
                "actor_id": actor_id,
                "canonical_name_current": actor["canonical_name"],
                "actor_class_current": actor["actor_class"],
                "origin_type_current": actor["origin_type"],
                "legal_status_current": actor["legal_status_guess"],
                "evidence_level_current": actor["evidence_level"],
                "review_status_current": actor["review_status"],
                "source_ref": actor["source_refs"],
                **source_summary(source_rows, archive_rows),
                "linked_batch02_edge_ids": ";".join(linked_edges_by_actor[actor_id]),
                "precise_identity_question": (
                    f"现有归档来源是否足以确认 {actor['canonical_name']} 是可独立识别、"
                    "名称和组织类型可按当前字段使用的 actor，并与同名个人、母体／分支或"
                    "一次性活动载体相区分？"
                ),
                "required_review_scope": (
                    "actor_identity;canonical_name;actor_class;origin_type;"
                    "legal_status;source_ref;evidence_level"
                ),
                "allowed_decisions": (
                    "accept_identity;revise_identity;defer_second_source;"
                    "defer_local;reject_identity"
                ),
                **{field: "" for field in IDENTITY_DECISION_FIELDS},
            }
        )

    if any(row[field] for row in edge_rows for field in EDGE_DECISION_FIELDS):
        raise ValueError("HR-035 Batch 2 edge decision fields must remain blank")
    if any(row[field] for row in identity_rows for field in IDENTITY_DECISION_FIELDS):
        raise ValueError("HR-035 Batch 2 identity decision fields must remain blank")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_rows(
        OUTPUT_DIR / "HR035_actor_issue_fact_review_batch02_v1.csv",
        edge_rows,
        EDGE_TASK_FIELDS,
    )
    write_rows(
        OUTPUT_DIR / "HR035_actor_identity_companion_batch02_v1.csv",
        identity_rows,
        IDENTITY_TASK_FIELDS,
    )
    write_rows(
        OUTPUT_DIR / "HR035_source_bundle_batch02_v1.csv",
        source_bundle,
        SOURCE_FIELDS,
    )

    unique_sources = {row["source_id"] for row in source_bundle}
    edge_unique_sources = {
        row["source_id"] for row in source_bundle if row["item_type"] == "edge_fact"
    }
    validation_lines = [
        "# HR-035 Batch 2 validation",
        "",
        "- PASS — 18 active E4 actor–issue facts selected.",
        (
            "- PASS — all 18 retain `ai_seeded` fact status and have completed "
            "human scope review."
        ),
        (
            "- PASS — 5 `ai_seeded` actor identities receive one companion "
            "decision each; no identity decision is duplicated per edge."
        ),
        (
            f"- PASS — {len(edge_unique_sources)} unique edge-source IDs and "
            f"{len(unique_sources)} unique package source IDs resolved."
        ),
        (
            "- PASS — AI044/AI119/AI121/AI232/AI234 carry source-level ceiling "
            "warnings; AI016 carries the single-statement continuity warning."
        ),
        (
            "- PASS — all source artifacts are `archived` or `manual_archived`; "
            "rejected S051 is absent."
        ),
        "- PASS — all 23 human decision rows are blank.",
        "- PASS — central tables and frontend artifacts were not modified.",
        "",
        "This assignment does not reopen HR-019 scope decisions. Edge acceptance",
        "does not create actor–actor, funding, alliance, causal, place or event",
        "relations. For the five companion actors, default reviewed-graph activation",
        "requires both an accepted/revised identity decision and an accepted/revised",
        "edge decision.",
        "",
    ]
    (OUTPUT_DIR / "validation_report_batch02_v1.md").write_text(
        "\n".join(validation_lines), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
