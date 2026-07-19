from __future__ import annotations

"""Build HR-034 without changing any research table.

The package turns legacy ``review_status`` values into blank human-review
questions.  It deliberately does not guess that ``verified``,
``human_verified``, ``accepted`` or workflow-specific labels mean
``human_checked``.
"""

import csv
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT_REL = Path("outputs/review_status_crosswalk_v1")

SOURCE_REL = Path("data/interim/05_source_log_initial_v0.csv")
ISSUE_REL = Path("data/interim/07_actor_issue_edges_initial_v0.csv")
R4_REL = Path("data/interim/19_sakishima_frame_corpus_v0.csv")
R9_REL = Path("data/interim/20_referendum_process_stages_v0.csv")
HET_REL = Path("data/interim/35_heterogeneous_event_repertoire_v1.csv")
LIFECYCLE_REL = Path("outputs/actor_lifecycle_v1/actor_lifecycle_v0.csv")

LEGAL_REVIEW_STATUSES = {
    "ai_seeded",
    "human_checked",
    "human_revised",
    "needs_second_source",
    "needs_local_retrieval",
    "rejected",
}

DECISION_FIELDS = (
    "decision",
    "revised_review_status",
    "human_reviewer",
    "review_date",
    "review_note",
)

TASK_FIELDS = [
    "review_item_id",
    "task_id",
    "task_kind",
    "upstream_table",
    "record_id_field",
    "object_id",
    "object_label",
    "field_name",
    "current_value",
    "affected_row_count",
    "observed_context",
    "review_question",
    "allowed_review_status_values",
    "required_boundary",
    "decision",
    "revised_review_status",
    "human_reviewer",
    "review_date",
    "review_note",
]

IMPACT_FIELDS = [
    "upstream_review_family",
    "downstream_path",
    "impact_kind",
    "affected_value_or_scope",
    "observed_row_count",
    "post_review_action",
    "repeat_human_review",
    "boundary",
]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_rows(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def blank_decision_fields() -> dict[str, str]:
    return {field: "" for field in DECISION_FIELDS}


def row_task(
    *,
    item_id: str,
    table: Path,
    id_field: str,
    object_id: str,
    label: str,
    current_value: str,
    context: str,
    question: str,
    boundary: str,
) -> dict[str, str]:
    return {
        "review_item_id": item_id,
        "task_id": "HR-034",
        "task_kind": "row_crosswalk",
        "upstream_table": table.as_posix(),
        "record_id_field": id_field,
        "object_id": object_id,
        "object_label": label,
        "field_name": "review_status",
        "current_value": current_value,
        "affected_row_count": "1",
        "observed_context": context,
        "review_question": question,
        "allowed_review_status_values": ";".join(sorted(LEGAL_REVIEW_STATUSES)),
        "required_boundary": boundary,
        **blank_decision_fields(),
    }


def policy_task(
    *,
    item_id: str,
    table: Path,
    object_id: str,
    current_value: str,
    affected_count: int,
    context: str,
    question: str,
    boundary: str,
) -> dict[str, str]:
    return {
        "review_item_id": item_id,
        "task_id": "HR-034",
        "task_kind": "table_policy",
        "upstream_table": table.as_posix(),
        "record_id_field": "",
        "object_id": object_id,
        "object_label": table.name,
        "field_name": "review_status policy",
        "current_value": current_value,
        "affected_row_count": str(affected_count),
        "observed_context": context,
        "review_question": question,
        "allowed_review_status_values": ";".join(sorted(LEGAL_REVIEW_STATUSES)),
        "required_boundary": boundary,
        **blank_decision_fields(),
    }


def count_status(path: Path, value: str) -> int:
    if not path.exists():
        return 0
    rows = read_rows(path)
    return sum(row.get("review_status") == value for row in rows)


def build_tasks(root: Path) -> tuple[list[dict[str, str]], dict[str, int]]:
    source_rows = read_rows(root / SOURCE_REL)
    issue_rows = read_rows(root / ISSUE_REL)
    r4_rows = read_rows(root / R4_REL)
    r9_rows = read_rows(root / R9_REL)
    het_rows = read_rows(root / HET_REL)
    lifecycle_rows = read_rows(root / LIFECYCLE_REL)

    illegal_sources = [
        row for row in source_rows
        if row["review_status"] not in LEGAL_REVIEW_STATUSES
    ]
    illegal_issue_rows = [
        row for row in issue_rows
        if row["review_status"] not in LEGAL_REVIEW_STATUSES
    ]

    tasks: list[dict[str, str]] = []
    for index, row in enumerate(illegal_sources, start=1):
        tasks.append(row_task(
            item_id=f"HR034-SRC-{index:03d}",
            table=SOURCE_REL,
            id_field="source_id",
            object_id=row["source_id"],
            label=row["title"],
            current_value=row["review_status"],
            context=(
                f"evidence_level={row['evidence_level']}; "
                f"human_decision={row.get('human_decision', '') or '(blank)'}; "
                f"reviewer={row.get('human_reviewer', '') or '(blank)'}; "
                f"review_date={row.get('review_date', '') or '(blank)'}"
            ),
            question=(
                "Which legal review_status follows from the actual reviewed fields and "
                "decision record for this source row?"
            ),
            boundary=(
                "Source review never approves an actor, relation, funding flow or "
                "interpretive claim; do not map by string similarity alone."
            ),
        ))

    for index, row in enumerate(illegal_issue_rows, start=1):
        tasks.append(row_task(
            item_id=f"HR034-AI-{index:03d}",
            table=ISSUE_REL,
            id_field="edge_id",
            object_id=row["edge_id"],
            label=f"{row['actor_id']}—{row['issue_label']}",
            current_value=row["review_status"],
            context=(
                f"scope_review_status={row.get('scope_review_status', '')}; "
                f"scope_human_decision={row.get('scope_human_decision', '')}; "
                f"scope_status={row.get('scope_status', '')}; "
                f"claim_status={row.get('claim_status', '') or '(blank)'}"
            ),
            question=(
                "After preserving the HR-019 scope decision, which legal review_status "
                "describes the underlying actor–issue claim?"
            ),
            boundary=(
                "The requested note named AI067, but current data show AI067 already "
                "rejected and AI068 carrying watchlist_only. Review AI068 only; do not "
                "reactivate either edge or infer an Okinawa link."
            ),
        ))

    r4_count = sum(row["review_status"] == "qa_safe_online" for row in r4_rows)
    r9_count = sum(row["review_status"] == "accepted" for row in r9_rows)
    het_count = sum(row["review_status"] == "accepted" for row in het_rows)
    lifecycle_workflow = [
        row for row in lifecycle_rows
        if row["review_status"] not in LEGAL_REVIEW_STATUSES
    ]

    tasks.extend([
        policy_task(
            item_id="HR034-POL-001",
            table=R4_REL,
            object_id="TABLE_R4_QA_SAFE_ONLINE",
            current_value="qa_safe_online",
            affected_count=r4_count,
            context="Online QA/safety label is currently stored in review_status.",
            question=(
                "Which separate field should preserve online-QA usability, and what "
                "review_status should these rows receive without assuming human review?"
            ),
            boundary=(
                "qa_safe_online is a usability/QA label, not evidence of a principal's "
                "acceptance; a table policy must preserve the frame and relationship limits."
            ),
        ),
        policy_task(
            item_id="HR034-POL-002",
            table=R9_REL,
            object_id="TABLE_R9_ACCEPTED",
            current_value="accepted",
            affected_count=r9_count,
            context="Process-stage acceptance is stored in review_status.",
            question=(
                "Does accepted describe formal-layer inclusion, a prior human decision, "
                "or another workflow state, and which legal review_status follows?"
            ),
            boundary=(
                "Do not convert accepted to human_checked without identifying the reviewer, "
                "reviewed fields and decision provenance."
            ),
        ),
        policy_task(
            item_id="HR034-POL-003",
            table=HET_REL,
            object_id="TABLE_HET_ACCEPTED",
            current_value="accepted",
            affected_count=het_count,
            context=(
                "The accepted rows are heterogeneous-repertoire projections of R9 formal "
                "stage/role records, not 49 new facts."
            ),
            question=(
                "Which status field should carry formal-layer inclusion in this derived "
                "table, and how should legal review_status be propagated from upstream?"
            ),
            boundary=(
                "Resolve the upstream policy once, then propagate mechanically by source "
                "record; do not conduct 49 duplicate row reviews."
            ),
        ),
        policy_task(
            item_id="HR034-POL-004",
            table=LIFECYCLE_REL,
            object_id="TABLE_LIFECYCLE_WORKFLOW_STATUS",
            current_value=";".join(sorted({row["review_status"] for row in lifecycle_workflow})),
            affected_count=len(lifecycle_workflow),
            context=(
                "Identity repair, continuity review and human-review queue states are "
                "currently stored in review_status beside legal review statuses."
            ),
            question=(
                "Which lifecycle workflow field should hold these queue states, and which "
                "legal review_status should each unresolved lifecycle row carry?"
            ),
            boundary=(
                "Absence of recent online evidence is not dissolution. LCR001–LCR004 "
                "decisions remain blank and lifecycle status must not be changed by HR-034."
            ),
        ),
    ])

    counts = {
        "source_row_tasks": len(illegal_sources),
        "actor_issue_row_tasks": len(illegal_issue_rows),
        "table_policy_tasks": 4,
        "r4_policy_rows": r4_count,
        "r9_policy_rows": r9_count,
        "heterogeneous_policy_rows": het_count,
        "lifecycle_policy_rows": len(lifecycle_workflow),
    }
    return tasks, counts


def build_impacts(root: Path) -> list[dict[str, str]]:
    specs = [
        (
            "source_log_rows",
            "outputs/R03_spatial_dossier_v1/source_crosswalk_v1.csv",
            "source-status snapshot",
            "verified;human_verified;rejected_archive_mismatch",
            "Rebuild source crosswalk after the 45 upstream source decisions.",
        ),
        (
            "actor_issue_AI068",
            "data/interim/24_r01_r02_actor_issue_layered_v0.csv",
            "derived actor–issue copy",
            "watchlist_only",
            "Propagate the approved AI068 status and exclusion fields by edge_id.",
        ),
        (
            "actor_issue_AI068",
            "outputs/R02_actor_issue_robustness_v1/edge_source_dependency_audit_v1.csv",
            "derived audit copy",
            "watchlist_only",
            "Regenerate from the central actor–issue table; no new edge review.",
        ),
        (
            "R4_table_policy",
            "outputs/R04_sakishima_frame_corpus_v0/online_evidence_safe_sources_v0.csv",
            "module QA/source projection",
            "qa_safe_online_source",
            "Separate QA usability from review_status when rebuilding the R4 package.",
        ),
        (
            "R9_table_policy",
            "outputs/R09_referendum_process_v0/process_stages_reviewed_all_v0.csv",
            "module stage copy",
            "accepted",
            "Propagate the approved table policy by stage_id.",
        ),
        (
            "R9_table_policy",
            "outputs/R09_referendum_process_v0/actor_process_roles_reviewed_all_v0.csv",
            "module role copy",
            "accepted",
            "Propagate the approved table policy by role/record id.",
        ),
        (
            "R9_and_HET_table_policy",
            "data/interim/35_heterogeneous_event_repertoire_v1.csv",
            "derived repertoire projection",
            "accepted",
            "Apply the HET table policy using upstream source_record_id; no 49-row re-review.",
        ),
        (
            "HET_table_policy",
            "outputs/R05_R07_heterogeneous_repertoire_v1/",
            "aggregate figures/tables",
            "formal-layer provenance",
            "Regenerate package after upstream status fields are normalized.",
        ),
        (
            "lifecycle_table_policy",
            "outputs/actor_lifecycle_v1/actor_lifecycle_review_queue_v0.csv",
            "workflow queue",
            "identity/continuity/human-review workflow states",
            "Keep queue decisions blank; move workflow naming only after policy approval.",
        ),
    ]
    impacts: list[dict[str, str]] = []
    for family, relative, kind, value, action in specs:
        path = root / relative
        count = ""
        if path.is_file() and path.suffix.lower() == ".csv":
            rows = read_rows(path)
            count = str(len(rows))
        impacts.append({
            "upstream_review_family": family,
            "downstream_path": relative,
            "impact_kind": kind,
            "affected_value_or_scope": value,
            "observed_row_count": count,
            "post_review_action": action,
            "repeat_human_review": "no",
            "boundary": (
                "This is a downstream mechanical impact only. It must not create a new "
                "human decision or strengthen the underlying claim."
            ),
        })
    return impacts


def validate(tasks: list[dict[str, str]], counts: dict[str, int]) -> None:
    assert len(tasks) == 50, len(tasks)
    assert counts == {
        "source_row_tasks": 45,
        "actor_issue_row_tasks": 1,
        "table_policy_tasks": 4,
        "r4_policy_rows": 10,
        "r9_policy_rows": 29,
        "heterogeneous_policy_rows": 49,
        "lifecycle_policy_rows": 4,
    }, counts
    assert len({row["review_item_id"] for row in tasks}) == len(tasks)
    assert all(not row[field] for row in tasks for field in DECISION_FIELDS)
    assert all(
        not row["revised_review_status"]
        or row["revised_review_status"] in LEGAL_REVIEW_STATUSES
        for row in tasks
    )
    actor_tasks = [row for row in tasks if row["upstream_table"] == ISSUE_REL.as_posix()]
    assert [row["object_id"] for row in actor_tasks] == ["AI068"]
    assert all(row["task_id"] == "HR-034" for row in tasks)


def build(root: Path = ROOT) -> dict[str, int]:
    out = root / OUT_REL
    tasks, counts = build_tasks(root)
    impacts = build_impacts(root)
    validate(tasks, counts)

    write_rows(out / "HR034_review_status_crosswalk_v1.csv", tasks, TASK_FIELDS)
    write_rows(out / "downstream_mechanical_impacts_v1.csv", impacts, IMPACT_FIELDS)

    status_counts = Counter(row["current_value"] for row in tasks if row["task_kind"] == "row_crosswalk")
    readme = f"""# HR-034 review_status crosswalk v1

日期：2026-07-20  
状态：**空白人工任务包；未作任何决定；未修改中央表**

## 交付

- `HR034_review_status_crosswalk_v1.csv`：50 个任务。
  - 45 个中央 source-log 逐行任务；
  - 1 个中央 actor–issue 逐行任务（当前实际为 AI068；AI067 已是 `rejected`）；
  - 4 个表级政策任务。
- `downstream_mechanical_impacts_v1.csv`：9 个派生影响点，只在上游决定后机械重生，不重复人审。
- `validation_report_v1.md`：计数与空白字段门禁。

## 为什么不能自动迁移

`verified`、`human_verified`、`accepted`、`qa_safe_online`、`watchlist_only`
以及 lifecycle 的 queue/workflow 名称分别混合了“资料可用”“模块纳入”“人工流程”
和“展示边界”。它们不能仅凭字符串自动视为 `human_checked`。

中央逐行旧值分布：{dict(sorted(status_counts.items()))}。

## 表级政策范围

- R4：10 行 `qa_safe_online`；
- R9：29 行 `accepted`；
- heterogeneous repertoire：49 行 `accepted`，是上游 R9 记录的派生投影；
- lifecycle：4 行把 identity/continuity queue 状态写进了 `review_status`。

## 强制边界

- 所有 `decision`、`revised_review_status`、`human_reviewer`、`review_date`、
  `review_note` 均为空。
- 来源状态迁移不批准 actor、edge、资金关系或解释性结论。
- AI067 已被 HR-019 拒绝；本包只处理当前仍为 `watchlist_only` 的 AI068，
  且不据此恢复冲绳连接。
- table policy 只决定字段语义与迁移规则；不能把 10/29/49 行批量推定为人审通过。
- lifecycle 的“待身份修复/待连续性核查”应与 `review_status` 分栏；线上未见活动
  不等于解散，既有 LCR001–LCR004 空白决定不受本包影响。
"""
    (out / "README.md").write_text(readme, encoding="utf-8")

    validation = f"""# HR-034 validation report v1

日期：2026-07-20

- PASS — total tasks: {len(tasks)}
- PASS — source-log row tasks: {counts['source_row_tasks']} / 45
- PASS — actor–issue row tasks: {counts['actor_issue_row_tasks']} / 1 (AI068)
- PASS — table-policy tasks: {counts['table_policy_tasks']} / 4
- PASS — policy affected rows: R4={counts['r4_policy_rows']}, R9={counts['r9_policy_rows']}, HET={counts['heterogeneous_policy_rows']}, lifecycle={counts['lifecycle_policy_rows']}
- PASS — unique review_item_id: {len({row['review_item_id'] for row in tasks})}
- PASS — blank decision/reviewer/date/note fields: {len(tasks)} / {len(tasks)}
- PASS — central research tables written: 0
- PASS — downstream impacts are marked repeat_human_review=no: {sum(row['repeat_human_review'] == 'no' for row in impacts)} / {len(impacts)}
"""
    (out / "validation_report_v1.md").write_text(validation, encoding="utf-8")
    return {**counts, "total_tasks": len(tasks), "downstream_impacts": len(impacts)}


if __name__ == "__main__":
    summary = build()
    print(summary)
