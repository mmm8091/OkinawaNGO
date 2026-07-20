from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "outputs" / "actor_issue_claim_freeze_v1"

# HR-035 batch 1 deliberately starts with case-, referendum-, and procedure-bounded
# actor–issue claims. These rows already received HR-019 scope decisions, but their
# underlying actor–issue facts have not been accepted or rejected by the principal.
BATCH_01_EDGE_IDS = [
    "AI021",
    "AI025",
    "AI027",
    "AI048",
    "AI049",
    "AI050",
    "AI106",
    "AI126",
    "AI127",
    "AI129",
    "AI132",
    "AI164",
    "AI178",
    "AI231",
    "AI241",
]

ATTENTION_FLAGS = {
    "AI021": "只审儒艮案中的美国法律渠道；Earthjustice 是 counsel，不是 plaintiff。",
    "AI025": "只审石垣住民投票请求／程序角色；requester 不等于诉讼 plaintiff。",
    "AI027": "只审石垣陆自部署公投语境，不外推为一般性反军事定位。",
    "AI048": "JELF 角色逐案变化：Dugong 案为 plaintiff，泡瀬材料中为 supporter／host。",
    "AI049": "现有材料最多支持 2020 MMC 事件语境，不支持长期 biodiversity 定位。",
    "AI050": "Dugong 诉讼角色与 2020 MMC 请求是两个事件，不得合并成稳定联盟。",
    "AI106": "当前 source_ref=S004 不足以单独证明诉讼法律角色；须核 R8C01 caption 并修订来源。",
    "AI126": "限定 2018–2019 辺野古县民投票；临时组织的解散／存续不得省略。",
    "AI127": "地方自治只通过该次直接请求／投票程序表达，不是无限期组织定位。",
    "AI129": "限定嘉手纳各轮噪音诉讼；认赔不等于运行停止或差止获准。",
    "AI132": "限定普天间各轮噪音诉讼；部分赔偿不等于噪音停止或运行禁令。",
    "AI164": "1997 名护市民投票 actor 单位／谱系仍需保守处理，不得凭相近名称扩期。",
    "AI178": "沖縄防衛局是工程／行政争议端点，不得把 anti_base 编成该机构的政治立场。",
    "AI231": "限定 2022 请愿与 2025–2026 公害调停等程序，不是一般法律组织定位。",
    "AI241": "只审冲绳县本部在 2018–2019 县民投票中的签名动员，不转嫁全国本部行动。",
}

TASK_FIELDS = [
    "review_item_id",
    "task_id",
    "batch_id",
    "workstream",
    "batch_order",
    "edge_id",
    "actor_id",
    "actor_name",
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

EVIDENCE_FIELDS = [
    "review_item_id",
    "edge_id",
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

    missing_edges = [edge_id for edge_id in BATCH_01_EDGE_IDS if edge_id not in edges]
    if missing_edges:
        raise ValueError(f"Missing HR-035 edge IDs: {missing_edges}")

    task_rows: list[dict[str, str]] = []
    evidence_rows: list[dict[str, str]] = []
    unique_source_ids: set[str] = set()

    for order, edge_id in enumerate(BATCH_01_EDGE_IDS, start=1):
        edge = edges[edge_id]
        if edge_id not in active_edges:
            raise ValueError(f"{edge_id} is not in the current active actor–issue layer")
        if edge["review_status"] != "ai_seeded":
            raise ValueError(
                f"{edge_id} review_status changed from ai_seeded to {edge['review_status']!r}"
            )
        if edge["scope_review_status"] not in {"human_checked", "human_revised"}:
            raise ValueError(
                f"{edge_id} lacks a completed HR-019 scope review: "
                f"{edge['scope_review_status']!r}"
            )

        actor = actors[edge["actor_id"]]
        issue = issues[edge["issue_id"]]
        source_ids = split_refs(edge["source_ref"])
        if not source_ids:
            raise ValueError(f"{edge_id} has no source_ref")
        if "S051" in source_ids:
            raise ValueError(f"{edge_id} improperly relies on rejected source S051")

        source_rows: list[dict[str, str]] = []
        archive_rows: list[dict[str, str]] = []
        for source_id in source_ids:
            if source_id not in sources:
                raise ValueError(f"{edge_id} has unresolved source ID {source_id}")
            if source_id not in archives:
                raise ValueError(f"{edge_id} source {source_id} lacks an archive record")
            source_row = sources[source_id]
            archive_row = archives[source_id]
            if archive_row["archive_status"] not in {"archived", "manual_archived"}:
                raise ValueError(
                    f"{edge_id} source {source_id} is not reviewable from the archive: "
                    f"{archive_row['archive_status']!r}"
                )
            source_rows.append(source_row)
            archive_rows.append(archive_row)
            unique_source_ids.add(source_id)
            evidence_rows.append(
                {
                    "review_item_id": f"HR035-B01-{edge_id}",
                    "edge_id": edge_id,
                    "source_id": source_id,
                    "source_title": source_row["title"],
                    "source_url": source_row["url"],
                    "source_type": source_row["source_type"],
                    "source_year": source_row["year"],
                    "source_evidence_level": source_row["evidence_level"],
                    "source_review_status": source_row["review_status"],
                    "what_it_supports": source_row["what_it_supports"],
                    "support_scope": source_row.get("support_scope", ""),
                    "locator": source_row.get("locator", ""),
                    "archive_status": archive_row["archive_status"],
                    "local_path": archive_row["local_path"],
                }
            )

        actor_name = actor["canonical_name"]
        issue_label = issue["issue_label"]
        task_rows.append(
            {
                "review_item_id": f"HR035-B01-{edge_id}",
                "task_id": "HR-035",
                "batch_id": "B01_case_referendum_procedure",
                "workstream": "factual_actor_issue_review",
                "batch_order": str(order),
                "edge_id": edge_id,
                "actor_id": edge["actor_id"],
                "actor_name": actor_name,
                "issue_id": edge["issue_id"],
                "issue_label": issue_label,
                "relation_basis": edge["relation_basis"],
                "evidence_level_current": edge["evidence_level"],
                "review_status_current": edge["review_status"],
                "source_ref": edge["source_ref"],
                "source_titles": " || ".join(
                    f"{row['source_id']} {row['title']}" for row in source_rows
                ),
                "source_urls": " || ".join(row["url"] for row in source_rows),
                "source_archive_paths": " || ".join(
                    row["local_path"] for row in archive_rows
                ),
                "source_archive_statuses": " || ".join(
                    f"{row['source_id']}:{row['archive_status']}" for row in archive_rows
                ),
                "existing_scope_kind": edge["scope_kind"],
                "existing_scope_claim_status": edge["scope_claim_status"],
                "existing_scope_approved_formulation": edge[
                    "scope_approved_formulation"
                ],
                "existing_scope_boundary": edge["scope_boundary"],
                "existing_scope_decision_source_report": edge[
                    "scope_decision_source_report"
                ],
                "attention_flag": ATTENTION_FLAGS[edge_id],
                "precise_fact_question": (
                    f"现有来源是否足以确认 {actor_name} 与 {issue_label} 的关系，"
                    f"且只支持到既有范围：{edge['scope_approved_formulation']}？"
                ),
                "required_review_scope": "relation_existence;interpretation_boundary",
                "allowed_decisions": "accept;revise;defer_second_source;defer_local;reject",
                "human_decision": "",
                "revised_review_status": "",
                "evidence_level_final": "",
                "approved_formulation": "",
                "review_scope_final": "",
                "reviewed_fields": "",
                "claim_status": "",
                "confirmed_scope": "",
                "missing_scope": "",
                "interpretation_limit": "",
                "scope_revision_required": "",
                "human_reviewer": "",
                "review_date": "",
                "review_note": "",
            }
        )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_rows(
        OUTPUT_DIR / "HR035_actor_issue_fact_review_batch01_v1.csv",
        task_rows,
        TASK_FIELDS,
    )
    write_rows(
        OUTPUT_DIR / "HR035_source_bundle_batch01_v1.csv",
        evidence_rows,
        EVIDENCE_FIELDS,
    )

    blank_fields = [
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
    if any(row[field] for row in task_rows for field in blank_fields):
        raise ValueError("HR-035 decision fields must remain blank in the assignment")

    validation_lines = [
        "# HR-035 batch 1 validation",
        "",
        "- PASS — 15 current actor–issue facts selected.",
        "- PASS — all 15 have completed HR-019 scope review and retain `ai_seeded` fact status.",
        f"- PASS — {len(unique_source_ids)} unique central source IDs resolved.",
        (
            "- PASS — all source artifacts are `archived` or `manual_archived`; "
            "rejected S051 is absent."
        ),
        "- PASS — every human decision/output field is blank.",
        "- PASS — central tables and frontend artifacts were not modified.",
        "",
        "This package reviews actor–issue fact existence only. It does not reopen the",
        "HR-019 scope decisions and cannot create actor–actor, funding, alliance,",
        "causal, place, or event relations.",
        "",
    ]
    (OUTPUT_DIR / "validation_report_v1.md").write_text(
        "\n".join(validation_lines), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
