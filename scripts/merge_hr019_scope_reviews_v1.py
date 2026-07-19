from __future__ import annotations

"""Merge HR-019 actor-issue scope and bridge interpretation decisions.

Scope review is deliberately separate from factual edge review. A
human-checked scope classification does not automatically turn an
``ai_seeded`` actor-issue edge into a human-checked fact. Seven edges whose
current sources do not support the issue mapping are explicitly deactivated.
"""

import csv
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CENTRAL = Path("data/interim/07_actor_issue_edges_initial_v0.csv")
PACKAGE = Path("outputs/R01_R02_actor_issue_v1/HR019")
SCOPE_QUEUE = PACKAGE / "HR019_edge_scope_review_queue_v0.csv"
BRIDGE_QUEUE = PACKAGE / "HR019_bridge_actor_review_queue_v0.csv"
BRIDGE_OUTPUT = PACKAGE / "bridge_actor_human_v1.csv"

SCOPE_FIELDS = [
    "scope_kind",
    "scope_review_status",
    "scope_human_decision",
    "scope_review_task_id",
    "scope_human_reviewer",
    "scope_review_date",
    "scope_reviewed_fields",
    "scope_claim_status",
    "scope_approved_formulation",
    "scope_boundary",
    "scope_decision_source_report",
    "invalidated_source_ref",
    "claim_status",
    "graph_eligibility",
    "review_scope",
    "confirmed_scope",
    "missing_scope",
]

BRIDGE_FIELDS = [
    "actor_id",
    "canonical_name",
    "issue_ids_all",
    "issue_count_all",
    "bridge_classification_v1",
    "review_decision",
    "narrative_eligibility",
    "claim_status",
    "approved_formulation",
    "scope_boundary",
    "review_status",
    "human_reviewer",
    "review_date",
    "decision_source_report",
    "interpretation_limit",
]

UNCLEAR_CANDIDATE = {"AI116", "AI118", "AI176"}
UNCLEAR_UNSUPPORTED = {"AI038", "AI063", "AI134", "AI067"}

SPECIAL_SCOPE_STATUS = {
    "AI038": "deactivated_until_direct_evidence",
    "AI063": "deactivated_until_taxonomy_revision_or_direct_evidence",
    "AI067": "retired_external_watchlist_only",
    "AI116": "deactivated_pending_actor_unit_repair",
    "AI118": "deactivated_pending_actor_unit_repair",
    "AI134": "deactivated_until_direct_evidence",
    "AI176": "deactivated_pending_direct_department_evidence",
    "AI068": "event_specific_excluded_from_default_okinawa_narrative",
}


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


def unique_index(
    rows: list[dict[str, str]], key: str
) -> dict[str, dict[str, str]]:
    result = {row[key]: row for row in rows}
    if len(result) != len(rows):
        raise ValueError(f"duplicate {key}")
    return result


def normalize_main_review_for_unclear(row: dict[str, str], edge_id: str) -> None:
    original_source = row.get("invalidated_source_ref", "") or row.get(
        "source_ref", ""
    )
    row.update(
        {
            "invalidated_source_ref": original_source,
            "source_ref": "",
            "review_status": (
                "rejected" if edge_id == "AI067" else "needs_second_source"
            ),
            "human_decision": "reject" if edge_id == "AI067" else "defer",
            "review_task_id": f"HR019-SCOPE-{edge_id}",
            "human_reviewer": "project_principal_user",
            "review_date": "2026-07-20",
            "reviewed_fields": (
                "issue_relation_support;source_ref;scope_status;"
                "interpretation_limit"
            ),
            "claim_status": (
                "candidate" if edge_id in UNCLEAR_CANDIDATE else "unsupported"
            ),
            "graph_eligibility": (
                "research_lead" if edge_id in UNCLEAR_CANDIDATE else "excluded"
            ),
            "review_scope": "relation_existence;interpretation_boundary",
            "confirmed_scope": (
                "Adjacent organizational, procedural or institutional context may "
                "be documented; the exact actor-issue mapping is not confirmed."
            ),
            "missing_scope": (
                "Direct evidence attributable to this exact actor unit and issue "
                "definition."
            ),
        }
    )


def bridge_disposition(decision: str) -> tuple[str, str]:
    if decision == "include_with_scope":
        return "narrative_with_scope", "supported_bounded"
    if decision == "candidate_only":
        return "research_candidate_only", "candidate"
    if decision == "exclude_from_narrative":
        return "excluded_from_narrative", "unsupported"
    raise ValueError(f"unknown bridge decision: {decision}")


def apply_hr019_scope_reviews(root: Path = ROOT) -> dict[str, int]:
    central_fields, central_rows = read_csv(root / CENTRAL)
    central_fields = ensure_fields(central_fields, SCOPE_FIELDS)
    _, scope_rows = read_csv(root / SCOPE_QUEUE)
    _, bridge_rows = read_csv(root / BRIDGE_QUEUE)

    central_by_id = unique_index(central_rows, "edge_id")
    scope_by_id = unique_index(scope_rows, "edge_id")
    missing = set(scope_by_id) - set(central_by_id)
    if missing:
        raise ValueError(f"HR-019 edges absent from central table: {sorted(missing)}")
    if len(scope_rows) != 76:
        raise ValueError(f"expected 76 HR-019 scope decisions, found {len(scope_rows)}")
    if len(bridge_rows) != 30:
        raise ValueError(f"expected 30 bridge decisions, found {len(bridge_rows)}")
    if any(not row["review_decision"] for row in scope_rows + bridge_rows):
        raise ValueError("HR-019 contains an undecided item")

    for edge_id, review in scope_by_id.items():
        edge = central_by_id[edge_id]
        kind = review["review_decision"]
        edge.update(
            {
                "scope_kind": kind,
                "scope_review_status": "human_checked",
                "scope_human_decision": "accept",
                "scope_review_task_id": f"HR019-SCOPE-{edge_id}",
                "scope_human_reviewer": "project_principal_user",
                "scope_review_date": review["review_date"],
                "scope_reviewed_fields": (
                    "scope_kind;scope_status;scope_approved_formulation;"
                    "scope_boundary"
                ),
                "scope_claim_status": (
                    "candidate" if kind == "remain_unclear" else "supported_bounded"
                ),
                "scope_approved_formulation": review["approved_formulation"],
                "scope_boundary": review["scope_boundary"],
                "scope_decision_source_report": review[
                    "decision_source_report"
                ],
                "scope_status": SPECIAL_SCOPE_STATUS.get(
                    edge_id, f"scope_reviewed_{kind}"
                ),
                "interpretation_limit": review["scope_boundary"],
            }
        )
        if kind == "remain_unclear":
            normalize_main_review_for_unclear(edge, edge_id)

    write_csv(root / CENTRAL, central_fields, central_rows)

    human_bridges: list[dict[str, str]] = []
    for row in bridge_rows:
        eligibility, claim_status = bridge_disposition(row["review_decision"])
        human_bridges.append(
            {
                "actor_id": row["actor_id"],
                "canonical_name": row["canonical_name"],
                "issue_ids_all": row["issue_ids_all"],
                "issue_count_all": row["issue_count_all"],
                "bridge_classification_v1": row["bridge_classification_v1"],
                "review_decision": row["review_decision"],
                "narrative_eligibility": eligibility,
                "claim_status": claim_status,
                "approved_formulation": row["approved_formulation"],
                "scope_boundary": row["scope_boundary"],
                "review_status": "human_checked",
                "human_reviewer": "project_principal_user",
                "review_date": row["review_date"],
                "decision_source_report": row["decision_source_report"],
                "interpretation_limit": (
                    "Bridge means a bounded issue, venue or institutional "
                    "translation only; it does not measure influence, centrality, "
                    "stable alliance or policy effect."
                ),
            }
        )
    write_csv(root / BRIDGE_OUTPUT, BRIDGE_FIELDS, human_bridges)

    scope_counts = Counter(row["review_decision"] for row in scope_rows)
    bridge_counts = Counter(row["review_decision"] for row in bridge_rows)
    summary = {
        "central_actor_issue_rows": len(central_rows),
        "scope_reviewed_edges": len(scope_rows),
        "organizational_positioning": scope_counts["organizational_positioning"],
        "institutional_or_case_role": scope_counts["institutional_or_case_role"],
        "event_specific": scope_counts["event_specific"],
        "remain_unclear_edges": scope_counts["remain_unclear"],
        "bridge_reviewed_actors": len(bridge_rows),
        "bridge_include_with_scope": bridge_counts["include_with_scope"],
        "bridge_candidate_only": bridge_counts["candidate_only"],
        "bridge_excluded": bridge_counts["exclude_from_narrative"],
    }
    write_csv(
        root / PACKAGE / "HR019_scope_merge_summary_v1.csv",
        ["metric", "value"],
        [
            {"metric": metric, "value": str(value)}
            for metric, value in summary.items()
        ],
    )
    (root / PACKAGE / "HR019_scope_merge_readme_v1.md").write_text(
        "# HR-019 scope review merge\n\n"
        "- All 76 selected actor-issue edges now carry a principal-reviewed scope "
        "classification.\n"
        "- Scope review does not automatically elevate an AI-seeded factual edge "
        "to `human_checked`.\n"
        "- Seven `remain_unclear` mappings are deactivated; their prior source "
        "references are preserved in `invalidated_source_ref` rather than left as "
        "apparent support.\n"
        "- Thirty bridge interpretations are stored in a separate analytical "
        "layer. They do not create actor relations, alliances or influence scores.\n",
        encoding="utf-8",
    )
    return summary


if __name__ == "__main__":
    result = apply_hr019_scope_reviews()
    print(
        "HR-019 scope merge complete: "
        f"{result['scope_reviewed_edges']} edges and "
        f"{result['bridge_reviewed_actors']} bridge actors."
    )
