from __future__ import annotations

"""Backfill completed principal decisions into their authoritative task books.

The machine-readable overlays are the stable merge input. This script does
not interpret source material and does not mutate central fact tables. It
only records already-made decisions, formulations, boundaries and provenance
in the original review queues.

Open local-retrieval, A073 and lifecycle items are absent from the overlays
and therefore remain blank.
"""

import csv
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OVERLAY_DIR = Path("outputs/principal_review_merge_v1")


@dataclass(frozen=True)
class QueueSpec:
    family: str
    path: str
    key_field: str
    decision_field: str
    reviewer_field: str
    date_field: str
    note_field: str


QUEUE_SPECS = (
    QueueSpec(
        "HR016",
        "outputs/R04_sakishima_frame_corpus_v0/hr016_review_items_v0.csv",
        "review_item_id",
        "review_decision",
        "human_reviewer",
        "review_date",
        "review_note",
    ),
    QueueSpec(
        "HR017_ONLINE",
        "outputs/R09_referendum_process_v0/hr017_review_queue_v0.csv",
        "object_id",
        "decision",
        "human_reviewer",
        "review_date",
        "decision_note",
    ),
    QueueSpec(
        "HR018_PREREQUISITE",
        "outputs/R10_administrative_collaboration_v0/HR018_source_prerequisites_v0.csv",
        "source_prerequisite_id",
        "decision",
        "human_reviewer",
        "review_date",
        "review_note",
    ),
    QueueSpec(
        "HR018_RELATION",
        "outputs/R10_administrative_collaboration_v0/HR018_relation_review_v0.csv",
        "review_item_id",
        "decision",
        "human_reviewer",
        "review_date",
        "review_note",
    ),
    QueueSpec(
        "HR019_RULE",
        "outputs/R01_R02_actor_issue_v1/HR019/HR019_review_v0.csv",
        "review_item_id",
        "review_decision",
        "human_reviewer",
        "review_date",
        "review_notes",
    ),
    QueueSpec(
        "HR019_BRIDGE",
        "outputs/R01_R02_actor_issue_v1/HR019/HR019_bridge_actor_review_queue_v0.csv",
        "actor_id",
        "review_decision",
        "human_reviewer",
        "review_date",
        "review_notes",
    ),
    QueueSpec(
        "HR019_EDGE_SCOPE",
        "outputs/R01_R02_actor_issue_v1/HR019/HR019_edge_scope_review_queue_v0.csv",
        "edge_id",
        "review_decision",
        "human_reviewer",
        "review_date",
        "review_notes",
    ),
    QueueSpec(
        "HR020",
        "outputs/R05_coaction_v1/hr020_review_queue_v0.csv",
        "queue_id",
        "decision",
        "human_reviewer",
        "review_date",
        "decision_note",
    ),
    QueueSpec(
        "HR021",
        "outputs/R06_R07_R11_pathways_v1/HR021_review_items_v0.csv",
        "review_item_id",
        "review_decision",
        "human_reviewer",
        "review_date",
        "review_note",
    ),
    QueueSpec(
        "HR024",
        "outputs/edge_activation_v1/HR024_edge_activation_review_v0.csv",
        "task_id",
        "decision",
        "reviewer",
        "review_date",
        "review_note",
    ),
    QueueSpec(
        "HR025",
        "outputs/R03_spatial_dossier_v1/HR025_actor_place_semantics_review_v0.csv",
        "object_id",
        "decision",
        "human_reviewer",
        "review_date",
        "review_note",
    ),
    QueueSpec(
        "HR026",
        "outputs/R09_election_civic_interface_v1/HR026_election_civic_role_review_v0.csv",
        "review_item_id",
        "decision",
        "human_reviewer",
        "review_date",
        "review_note",
    ),
    QueueSpec(
        "HR032",
        "outputs/R10_official_collaboration_universe_v1/HR032_partner_alias_crosswalk_review_v1.csv",
        "review_item_id",
        "decision",
        "reviewer",
        "review_date",
        "review_note",
    ),
)

COMMON_PROVENANCE_FIELDS = [
    "approved_formulation",
    "scope_boundary",
    "decision_source_report",
]

SOURCE_QUEUE_SPECS = {
    "HR-022": {
        "path": "outputs/phase1_source_integration_v1/HR022_source_metadata_review_v0.csv",
        "year_field": "revised_year_or_period",
    },
    "HR-030": {
        "path": "outputs/next_wave_source_integration_v1/HR030_source_metadata_archive_review_v0.csv",
        "year_field": "revised_year",
    },
}

SOURCE_FIELDS = [
    "decision",
    "revised_title",
    "revised_source_type",
    "revised_year_or_period",
    "revised_year",
    "revised_locator",
    "revised_support_scope",
    "revised_evidence_level",
    "archive_resolution",
    "reviewer",
    "review_date",
    "review_note",
    "source_report",
]

VALID_PLACE_SEMANTICS = (
    "headquarters",
    "site_presence",
    "event_site",
    "advocacy_target",
    "institutional_venue",
    "unclear",
)


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def ensure_fields(fields: list[str], additions: list[str]) -> list[str]:
    return fields + [field for field in additions if field not in fields]


def index_unique(
    rows: list[dict[str, str]], key_field: str
) -> dict[str, dict[str, str]]:
    result = {row[key_field]: row for row in rows}
    if len(result) != len(rows):
        raise ValueError(f"duplicate {key_field}")
    return result


def final_place_semantic(
    queue_row: dict[str, str],
    overlay_row: dict[str, str],
) -> str:
    decision = overlay_row["decision"]
    if decision.startswith(("reject_edge", "retire_")):
        return ""
    text = f"{decision} {overlay_row['approved_formulation']}"
    for semantic in VALID_PLACE_SEMANTICS:
        if re.search(rf"(?<![A-Za-z_]){re.escape(semantic)}(?![A-Za-z_])", text):
            return semantic
    if decision == "accept":
        return queue_row.get("candidate_semantic_v1", "")
    return queue_row.get("candidate_semantic_v1", "")


def apply_queue_overlay(
    root: Path,
    spec: QueueSpec,
    overlay_rows: list[dict[str, str]],
) -> int:
    path = root / spec.path
    fields, rows = read_csv(path)
    additions = [
        spec.decision_field,
        spec.reviewer_field,
        spec.date_field,
        spec.note_field,
        *COMMON_PROVENANCE_FIELDS,
    ]
    if spec.family == "HR025":
        additions.append("final_semantic")
    fields = ensure_fields(fields, additions)
    by_key = index_unique(rows, spec.key_field)

    applied = 0
    for overlay in overlay_rows:
        key = overlay["object_id"]
        if key not in by_key:
            raise ValueError(f"{spec.family}: overlay key not in queue: {key}")
        row = by_key[key]
        row[spec.decision_field] = overlay["decision"]
        row[spec.reviewer_field] = overlay["human_reviewer"]
        row[spec.date_field] = overlay["review_date"]
        row[spec.note_field] = (
            f"{overlay['approved_formulation']} | 边界：{overlay['scope_boundary']}"
        )
        row["approved_formulation"] = overlay["approved_formulation"]
        row["scope_boundary"] = overlay["scope_boundary"]
        row["decision_source_report"] = overlay["source_report"]

        if spec.family == "HR025":
            row["final_semantic"] = final_place_semantic(row, overlay)
        if spec.family == "HR018_PREREQUISITE":
            row["current_status"] = "prerequisite_satisfied"
            row["archive_verified"] = "yes"
            match = re.search(r"→\s*(S\d+)", overlay["approved_formulation"])
            if not match:
                raise ValueError(
                    f"cannot parse main source ID for {overlay['object_id']}"
                )
            row["main_source_id"] = match.group(1)
            row["human_notes"] = row[spec.note_field]
        applied += 1

    write_csv(path, fields, rows)
    return applied


def apply_source_metadata_overlay(root: Path) -> int:
    overlay_path = root / OVERLAY_DIR / "source_metadata_overlay_v1.csv"
    _, overlays = read_csv(overlay_path)
    grouped: dict[str, list[dict[str, str]]] = {}
    for row in overlays:
        grouped.setdefault(row["task_id"], []).append(row)

    applied = 0
    for task_id, config in SOURCE_QUEUE_SPECS.items():
        path = root / str(config["path"])
        fields, rows = read_csv(path)
        fields = ensure_fields(fields, SOURCE_FIELDS)
        by_key = index_unique(rows, "review_item_id")
        task_rows = grouped.get(task_id, [])
        for overlay in task_rows:
            key = overlay["review_item_id"]
            if key not in by_key:
                raise ValueError(f"{task_id}: overlay key not in queue: {key}")
            row = by_key[key]
            row.update(
                {
                    "decision": overlay["decision"],
                    "revised_title": overlay["revised_title"],
                    "revised_source_type": overlay["revised_source_type"],
                    str(config["year_field"]): overlay["revised_year_or_period"],
                    "revised_locator": overlay["revised_locator"],
                    "revised_support_scope": overlay["revised_support_scope"],
                    "revised_evidence_level": overlay["revised_evidence_level"],
                    "archive_resolution": overlay["archive_resolution"],
                    "reviewer": "项目负责人",
                    "review_date": "2026-07-20",
                    "review_note": overlay["review_note"],
                    "source_report": overlay["source_report"],
                }
            )
            applied += 1
        write_csv(path, fields, rows)
    return applied


def apply_principal_review_overlays(root: Path = ROOT) -> dict[str, int]:
    overlay_path = root / OVERLAY_DIR / "principal_decision_overlay_v1.csv"
    _, overlay_rows = read_csv(overlay_path)
    grouped: dict[str, list[dict[str, str]]] = {}
    for row in overlay_rows:
        grouped.setdefault(row["task_family"], []).append(row)

    applied = 0
    family_counts: dict[str, int] = {}
    for spec in QUEUE_SPECS:
        count = apply_queue_overlay(root, spec, grouped.get(spec.family, []))
        family_counts[spec.family] = count
        applied += count

    if applied != len(overlay_rows):
        unseen = set(grouped) - {spec.family for spec in QUEUE_SPECS}
        raise ValueError(
            f"principal overlay coverage mismatch applied={applied} "
            f"rows={len(overlay_rows)} unseen={sorted(unseen)}"
        )

    source_count = apply_source_metadata_overlay(root)
    summary = {
        "principal_decisions_applied": applied,
        "source_metadata_decisions_applied": source_count,
        **{f"{family}_applied": count for family, count in family_counts.items()},
    }
    return summary


if __name__ == "__main__":
    result = apply_principal_review_overlays()
    print(
        "Principal-review queues updated: "
        f"{result['principal_decisions_applied']} fact/role decisions; "
        f"{result['source_metadata_decisions_applied']} source decisions."
    )
