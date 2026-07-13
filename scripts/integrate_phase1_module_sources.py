"""Integrate vetted-online module source candidates into the main source log.

This is deliberately a source-layer operation.  New records remain ``ai_seeded``
and do not approve any actor relation, amount observation, procedural role, or
interpretive claim.  The human queues in HR-016--018 remain the decision gates.
"""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROPOSAL = (
    ROOT
    / "outputs"
    / "phase1_source_integration_v1"
    / "source_merge_candidates_v0.csv"
)
SOURCE_LOG = ROOT / "data" / "interim" / "05_source_log_initial_v0.csv"
MANIFEST = ROOT / "source_docs" / "source_archive" / "source_archive_manifest.csv"
OUT_DIR = ROOT / "outputs" / "phase1_source_integration_v1"
CROSSWALK = OUT_DIR / "module_source_crosswalk_v1.csv"
NOTE = OUT_DIR / "integration_note_v1.md"
HR022 = OUT_DIR / "HR022_source_metadata_review_v0.csv"
HR022_GUIDE = OUT_DIR / "HR022_review_guide_v0.md"

SOURCE_FIELDS = [
    "source_id",
    "source_type",
    "title",
    "year",
    "url",
    "what_it_supports",
    "evidence_level",
    "bias_note",
    "review_status",
    "notes",
]

CROSSWALK_FIELDS = [
    "module",
    "module_source_id",
    "proposal_row_id",
    "main_source_id",
    "merge_status",
    "normalized_url",
    "source_review_status",
    "archive_status",
    "relation_or_claim_approved",
    "review_boundary",
]

HR022_FIELDS = [
    "review_item_id",
    "proposal_row_id",
    "main_source_id",
    "support_modules",
    "module_source_refs",
    "url",
    "archive_status",
    "current_title",
    "current_source_type",
    "current_year_or_period",
    "current_evidence_level",
    "metadata_conflicts",
    "review_boundary",
    "human_review_prerequisite",
    "decision",
    "revised_title",
    "revised_source_type",
    "revised_year_or_period",
    "revised_evidence_level",
    "revised_support_scope",
    "reviewer",
    "review_date",
    "review_note",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_sort_key(row: dict[str, str]) -> int:
    source_id = row["source_id"]
    if not source_id.startswith("S") or not source_id[1:].isdigit():
        raise ValueError(f"Invalid source ID: {source_id}")
    return int(source_id[1:])


def build_new_source(row: dict[str, str]) -> dict[str, str]:
    source_id = row["proposed_source_id"].strip()
    if not source_id:
        raise ValueError(f"Missing proposed source ID in {row['proposal_row_id']}")
    boundary = row["review_boundary"].strip()
    prerequisite = row["human_review_prerequisite"].strip()
    notes = (
        f"Phase-1 module source integration {row['proposal_row_id']}; "
        f"module refs={row['module_source_refs']}. "
        "Source metadata remains AI-seeded; source inclusion does not approve "
        "the supported relation or interpretation."
    )
    if prerequisite:
        notes += f" Review prerequisite: {prerequisite}."
    return {
        "source_id": source_id,
        "source_type": row["proposed_source_type"].strip(),
        "title": row["proposed_title"].strip(),
        "year": row["proposed_year_or_period"].strip(),
        "url": row["normalized_url"].strip(),
        "what_it_supports": row["what_it_supports"].strip(),
        "evidence_level": row["proposed_evidence_level"].strip(),
        "bias_note": boundary or "Module-specific source; support scope must remain bounded.",
        "review_status": "ai_seeded",
        "notes": notes,
    }


def choose_main_id(row: dict[str, str]) -> str:
    if row["merge_status"] == "proposed_new":
        return row["proposed_source_id"].strip()
    current_ids = [
        value.strip()
        for value in row["current_main_source_ids"].split(";")
        if value.strip()
    ]
    if len(current_ids) != 1:
        raise ValueError(
            f"Expected one current source ID for {row['proposal_row_id']}, got {current_ids}"
        )
    return current_ids[0]


def build_crosswalk(
    proposal_rows: list[dict[str, str]], archive_by_id: dict[str, str]
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for proposal in proposal_rows:
        main_id = choose_main_id(proposal)
        for module_ref in proposal["module_source_refs"].split(";"):
            module, module_source_id = module_ref.split(":", 1)
            rows.append(
                {
                    "module": module,
                    "module_source_id": module_source_id,
                    "proposal_row_id": proposal["proposal_row_id"],
                    "main_source_id": main_id,
                    "merge_status": proposal["merge_status"],
                    "normalized_url": proposal["normalized_url"],
                    "source_review_status": (
                        "ai_seeded"
                        if proposal["merge_status"] == "proposed_new"
                        else "preserve_existing_main_status"
                    ),
                    "archive_status": archive_by_id.get(main_id, "not_in_manifest"),
                    "relation_or_claim_approved": "no",
                    "review_boundary": proposal["review_boundary"],
                }
            )
    return sorted(rows, key=lambda row: (row["module"], row["module_source_id"]))


def build_hr022(
    proposal_rows: list[dict[str, str]], archive_by_id: dict[str, str]
) -> list[dict[str, str]]:
    queue: list[dict[str, str]] = []
    for proposal in proposal_rows:
        if proposal["human_review_required"] != "yes":
            continue
        main_id = choose_main_id(proposal)
        queue.append(
            {
                "review_item_id": f"HR022-{len(queue) + 1:03d}",
                "proposal_row_id": proposal["proposal_row_id"],
                "main_source_id": main_id,
                "support_modules": proposal["support_modules"],
                "module_source_refs": proposal["module_source_refs"],
                "url": proposal["normalized_url"],
                "archive_status": archive_by_id.get(main_id, "not_in_manifest"),
                "current_title": proposal["proposed_title"],
                "current_source_type": proposal["proposed_source_type"],
                "current_year_or_period": proposal["proposed_year_or_period"],
                "current_evidence_level": proposal["proposed_evidence_level"],
                "metadata_conflicts": proposal["metadata_conflicts"],
                "review_boundary": proposal["review_boundary"],
                "human_review_prerequisite": proposal["human_review_prerequisite"],
                "decision": "",
                "revised_title": "",
                "revised_source_type": "",
                "revised_year_or_period": "",
                "revised_evidence_level": "",
                "revised_support_scope": "",
                "reviewer": "",
                "review_date": "",
                "review_note": "",
            }
        )
    return queue


def validate(
    proposal_rows: list[dict[str, str]],
    source_rows: list[dict[str, str]],
    crosswalk_rows: list[dict[str, str]],
) -> None:
    proposed = [row for row in proposal_rows if row["merge_status"] == "proposed_new"]
    if len(proposal_rows) != 54 or len(proposed) != 39:
        raise ValueError(
            f"Unexpected proposal shape: {len(proposal_rows)} rows, {len(proposed)} proposed"
        )
    if len(crosswalk_rows) != 57:
        raise ValueError(f"Expected 57 module-source crosswalk rows, got {len(crosswalk_rows)}")

    ids = [row["source_id"] for row in source_rows]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate source IDs after integration")

    expected_new_ids = {f"S{number:03d}" for number in range(160, 199)}
    actual_new_ids = {row["proposed_source_id"] for row in proposed}
    if actual_new_ids != expected_new_ids:
        raise ValueError("Proposed IDs are not the expected continuous S160--S198 range")
    by_id = {row["source_id"]: row for row in source_rows}
    old_urls = {
        row["url"].strip()
        for row in source_rows
        if row["source_id"] not in expected_new_ids and row["url"].strip()
    }
    new_urls = [by_id[source_id]["url"].strip() for source_id in expected_new_ids]
    if len(new_urls) != len(set(new_urls)):
        raise ValueError("New integration rows contain duplicate exact URLs")
    if old_urls & set(new_urls):
        raise ValueError("New integration rows duplicate an existing exact URL")
    for source_id in expected_new_ids:
        if by_id[source_id]["review_status"] != "ai_seeded":
            raise ValueError(f"New source was upgraded without human review: {source_id}")
    if any(row["relation_or_claim_approved"] != "no" for row in crosswalk_rows):
        raise ValueError("Crosswalk must not approve module relations or claims")


def write_hr022_guide(queue_count: int) -> None:
    HR022_GUIDE.write_text(
        "\n".join(
            [
                "# HR-022 跨模块来源元数据与支持范围复核",
                "",
                f"待审：{queue_count} 项。所有决定、修订、复核人和日期栏均为空。",
                "",
                "逐项打开 URL 或本地归档，核对标题、来源类型、年份／期间、证据等级和可支持范围。",
                "`archive_status=archived` 只证明本地保存成功，不证明元数据或模块解释已获人工认可。",
                "`accept`／`revise`／`reject` 只处理来源层；actor relation、金额、角色和分析结论仍由 HR-016～021 等模块任务控制。",
                "R9 `usable_with_limit`、R4 locator/speaker 边界和 R10 type/year 推定不得因来源进入主表而自动升级。",
                "若 URL 失败但可由其他权威副本核实，记录替代 URL 和定位；不得删除失败日志来伪装归档成功。",
                "",
            ]
        ),
        encoding="utf-8",
    )


def write_note(
    source_count: int,
    integrated_count: int,
    crosswalk_count: int,
    archive_by_id: dict[str, str],
) -> None:
    integrated_ids = [f"S{number:03d}" for number in range(160, 199)]
    archive_counts: dict[str, int] = {}
    for source_id in integrated_ids:
        status = archive_by_id.get(source_id, "not_in_manifest")
        archive_counts[status] = archive_counts.get(status, 0) + 1
    archive_summary = "、".join(
        f"{status} {count}" for status, count in sorted(archive_counts.items())
    )
    failed_ids = [
        source_id for source_id in integrated_ids if archive_by_id.get(source_id) == "failed"
    ]
    NOTE.write_text(
        "\n".join(
            [
                "# Phase-1 module source integration v1",
                "",
                f"- 主来源表当前共 {source_count} 条；本轮集成 {integrated_count} 条（S160–S198）。",
                f"- 模块来源交叉表共 {crosswalk_count} 条，覆盖 R4／R9／R10 的全部 57 条可用来源记录。",
                f"- S160–S198 归档结果：{archive_summary}。",
                (
                    f"- 当前失败项：{', '.join(failed_ids)}；保留失败状态，不作为来源失效或证据否定。"
                    if failed_ids
                    else "- S160–S198 当前无归档失败项。"
                ),
                "- 新来源统一保持 `ai_seeded`；已有来源保留原 review status 与元数据。",
                "- `relation_or_claim_approved=no`：来源入表与归档不批准 actor relation、金额、角色或解释性结论。",
                "- HR-016、HR-017、HR-018 仍分别控制语义／角色／敏感行政与资金关系；HR-022 控制 49 个来源元数据／支持范围项。",
                "",
                "运行 `python scripts/integrate_phase1_module_sources.py` 可幂等复现。",
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    proposal_rows = read_csv(PROPOSAL)
    source_rows = read_csv(SOURCE_LOG)
    archive_by_id = (
        {row["source_id"]: row["archive_status"] for row in read_csv(MANIFEST)}
        if MANIFEST.exists()
        else {}
    )
    existing_by_id = {row["source_id"]: row for row in source_rows}
    added = 0

    for proposal in proposal_rows:
        if proposal["merge_status"] != "proposed_new":
            continue
        candidate = build_new_source(proposal)
        source_id = candidate["source_id"]
        existing = existing_by_id.get(source_id)
        if existing is None:
            source_rows.append(candidate)
            existing_by_id[source_id] = candidate
            added += 1
        elif existing != candidate:
            raise ValueError(f"Existing {source_id} differs from the integration proposal")

    source_rows.sort(key=source_sort_key)
    crosswalk_rows = build_crosswalk(proposal_rows, archive_by_id)
    hr022_rows = build_hr022(proposal_rows, archive_by_id)
    validate(proposal_rows, source_rows, crosswalk_rows)
    if len(hr022_rows) != 49:
        raise ValueError(f"Expected 49 HR-022 items, got {len(hr022_rows)}")
    if any(
        row[field]
        for row in hr022_rows
        for field in ("decision", "reviewer", "review_date", "review_note")
    ):
        raise ValueError("HR-022 decision fields must remain blank")
    write_csv(SOURCE_LOG, SOURCE_FIELDS, source_rows)
    write_csv(CROSSWALK, CROSSWALK_FIELDS, crosswalk_rows)
    write_csv(HR022, HR022_FIELDS, hr022_rows)
    write_hr022_guide(len(hr022_rows))
    integrated_count = sum(
        proposal["merge_status"] == "proposed_new" for proposal in proposal_rows
    )
    write_note(
        len(source_rows), integrated_count, len(crosswalk_rows), archive_by_id
    )
    print(
        f"Integrated {added} new sources; main={len(source_rows)}; "
        f"crosswalk={len(crosswalk_rows)}"
    )


if __name__ == "__main__":
    main()
