from __future__ import annotations

"""Merge HR-024 case-scoped issue edges and HR-025 place semantics."""

import csv
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ISSUE_TAXONOMY = Path("data/interim/03_issue_taxonomy_v0.csv")
PLACE_REGISTRY = Path("data/interim/04_place_registry_v0.csv")
ISSUE_EDGES = Path("data/interim/07_actor_issue_edges_initial_v0.csv")
PLACE_EDGES = Path("data/interim/08_actor_place_edges_initial_v0.csv")
HR024_QUEUE = Path("outputs/edge_activation_v1/HR024_edge_activation_review_v0.csv")
HR025_QUEUE = Path(
    "outputs/R03_spatial_dossier_v1/HR025_actor_place_semantics_review_v0.csv"
)
OUT = Path("outputs/hr024_hr025_edge_merge_v1")

HR024_SOURCE_CROSSWALK = {
    "EA-S001": "S060",
    "EA-S002": "S093",
    "EA-S004": "S228",
    "EA-S005": "S060",
    "EA-S006": "S229",
}

PLACE_ID_OVERRIDES = {
    "AP036": "P018",
    "AP044": "P018",
    "AP049": "P021",
    "AP123": "P007",
}

PLACE_SEMANTIC_OVERRIDES = {
    "AP095": "advocacy_target",
    "AP107": "event_site",
    "AP114": "advocacy_target",
    "AP115": "advocacy_target",
}

RETIRED_PLACE_EDGES = {
    "AP048": "retired_unsubstantiated",
    "AP088": "retired_wrong_place",
    "AP093": "retired_redundant_parent_place",
    "AP106": "retired_unsubstantiated",
    "AP118": "retired_duplicate",
}

ISSUE_EXTRA_FIELDS = [
    "scope_kind",
    "case_id",
    "package_source_keys",
    "approved_formulation",
    "review_scope",
    "claim_status",
    "confirmed_scope",
    "missing_scope",
    "graph_eligibility",
]

PLACE_EXTRA_FIELDS = [
    "original_place_id",
    "original_place_name",
    "place_review_task_id",
    "place_review_status",
    "place_human_decision",
    "place_review_scope",
    "place_reviewed_fields",
    "place_approved_formulation",
    "place_scope_boundary",
    "place_decision_source_report",
    "approved_formulation",
    "review_scope",
    "claim_status",
    "confirmed_scope",
    "missing_scope",
    "graph_eligibility",
]


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


def normalized_decision(decision: str) -> str:
    return "accept" if decision == "accept" else "revise"


def hr024_edge_id(task_id: str) -> str:
    number = int(task_id.rsplit("-", 1)[1])
    return f"AI{240 + number:03d}"


def central_source_refs(package_keys: str) -> tuple[str, str]:
    mapped: list[str] = []
    gaps: list[str] = []
    for key in package_keys.split(";"):
        key = key.strip()
        if not key:
            continue
        source_id = HR024_SOURCE_CROSSWALK.get(key)
        if source_id and source_id not in mapped:
            mapped.append(source_id)
        elif not source_id:
            gaps.append(key)
    return ";".join(mapped), ";".join(gaps)


def merge_hr024(
    root: Path,
) -> tuple[list[str], list[dict[str, str]], int]:
    fields, edges = read_csv(root / ISSUE_EDGES)
    fields = ensure_fields(fields, ISSUE_EXTRA_FIELDS)
    _, queue = read_csv(root / HR024_QUEUE)
    _, taxonomy = read_csv(root / ISSUE_TAXONOMY)
    labels = {row["issue_id"]: row["issue_label"] for row in taxonomy}

    decisions = [
        row
        for row in queue
        if row["review_object"] == "actor_issue_edge_mapping"
    ]
    if len(decisions) != 7 or any(not row["decision"] for row in decisions):
        raise ValueError("HR-024 must contain seven decided actor-issue mappings")
    if queue[0]["task_id"] != "HR024-001" or queue[0]["decision"]:
        raise ValueError("HR024-001 A073 identity decision must remain open")

    by_task = {
        row.get("review_task_id", ""): row
        for row in edges
        if row.get("review_task_id", "").startswith("HR024-")
    }
    by_edge_id = unique_index(edges, "edge_id")

    for review in decisions:
        task_id = review["task_id"]
        edge_id = hr024_edge_id(task_id)
        edge = by_task.get(task_id)
        if edge is None:
            if edge_id in by_edge_id:
                raise ValueError(f"{edge_id} already used by another edge")
            edge = {field: "" for field in fields}
            edge["edge_id"] = edge_id
            edges.append(edge)
            by_edge_id[edge_id] = edge
            by_task[task_id] = edge

        source_ref, source_gap = central_source_refs(review["source_keys"])
        decision = normalized_decision(review["decision"])
        scope_boundary = review["scope_boundary"]
        edge.update(
            {
                "actor_id": review["actor_id"],
                "issue_id": review["issue_id"],
                "issue_label": labels[review["issue_id"]],
                "relation_basis": review["approved_formulation"],
                "source_ref": source_ref,
                "evidence_level": review["evidence_level"],
                "review_status": "human_checked",
                "notes": (
                    "HR-024 case-specific actor-issue mapping. "
                    f"{scope_boundary}"
                    + (
                        f" Package-local source keys not centralized: {source_gap}."
                        if source_gap
                        else ""
                    )
                ),
                "human_decision": decision,
                "review_task_id": task_id,
                "human_reviewer": "project_principal_user",
                "review_date": review["review_date"],
                "reviewed_fields": (
                    "actor_id;issue_id;relation_basis;source_ref;scope_kind;"
                    "case_id;interpretation_limit"
                ),
                "scope_status": "active_case_specific",
                "decision_source_report": review["decision_source_report"],
                "interpretation_limit": scope_boundary,
                "scope_kind": "case",
                "case_id": "R8C01",
                "package_source_keys": review["source_keys"],
                "approved_formulation": review["approved_formulation"],
                "review_scope": (
                    "relation_existence;case_role;interpretation_boundary"
                ),
                "claim_status": "supported_bounded",
                "confirmed_scope": (
                    "Actor-issue connection within R8C01 Okinawa Dugong litigation."
                ),
                "missing_scope": (
                    "Organization continuity and any activity outside R8C01 are "
                    "not established by this edge."
                ),
                "graph_eligibility": "case_role",
                "scope_review_status": "human_checked",
                "scope_human_decision": decision,
                "scope_review_task_id": task_id,
                "scope_human_reviewer": "project_principal_user",
                "scope_review_date": review["review_date"],
                "scope_reviewed_fields": "scope_kind;case_id;scope_boundary",
                "scope_claim_status": "supported_bounded",
                "scope_approved_formulation": review["approved_formulation"],
                "scope_boundary": scope_boundary,
                "scope_decision_source_report": review[
                    "decision_source_report"
                ],
            }
        )

    edges.sort(key=lambda row: int(row["edge_id"][2:]))
    write_csv(root / ISSUE_EDGES, fields, edges)
    return fields, edges, len(decisions)


def place_main_status(edge_id: str, decision: str) -> tuple[str, str, str]:
    if edge_id in RETIRED_PLACE_EDGES:
        return "rejected", "reject", "unsupported"
    if edge_id == "AP049":
        return "needs_second_source", "revise", "candidate"
    if decision == "accept":
        return "human_checked", "accept", "supported_bounded"
    return "human_revised", "revise", "supported_bounded"


def place_review_status(edge_id: str, decision: str) -> str:
    if edge_id in RETIRED_PLACE_EDGES or decision == "accept":
        return "human_checked"
    return "human_revised"


def merge_hr025(
    root: Path,
) -> tuple[list[str], list[dict[str, str]], Counter[str], int]:
    fields, edges = read_csv(root / PLACE_EDGES)
    fields = ensure_fields(fields, PLACE_EXTRA_FIELDS)
    _, queue = read_csv(root / HR025_QUEUE)
    _, places = read_csv(root / PLACE_REGISTRY)
    place_names = {row["place_id"]: row["place_name"] for row in places}
    by_id = unique_index(edges, "edge_id")

    if len(queue) != 47 or any(not row["decision"] for row in queue):
        raise ValueError("HR-025 must contain 47 decided place-edge items")
    missing = {row["object_id"] for row in queue} - set(by_id)
    if missing:
        raise ValueError(f"HR-025 edges absent from central table: {sorted(missing)}")

    semantic_counts: Counter[str] = Counter()
    for review in queue:
        edge_id = review["object_id"]
        edge = by_id[edge_id]
        original_place_id = review["place_id"]
        place_id = PLACE_ID_OVERRIDES.get(edge_id, original_place_id)
        semantic = PLACE_SEMANTIC_OVERRIDES.get(
            edge_id, review["final_semantic"]
        )
        status, human_decision, claim_status = place_main_status(
            edge_id, review["decision"]
        )
        retired = edge_id in RETIRED_PLACE_EDGES
        if retired:
            semantic = ""
            scope_status = RETIRED_PLACE_EDGES[edge_id]
            graph_eligibility = "excluded"
        elif edge_id == "AP049":
            scope_status = "source_id_integration_pending"
            graph_eligibility = "administrative_record"
            semantic_counts[semantic] += 1
        else:
            scope_status = f"active_reviewed_{semantic}"
            graph_eligibility = "administrative_record"
            semantic_counts[semantic] += 1

        edge.update(
            {
                "place_id": place_id,
                "place_name": place_names[place_id],
                "review_status": status,
                "human_decision": human_decision,
                "review_task_id": review["task_id"],
                "human_reviewer": "project_principal_user",
                "review_date": review["review_date"],
                "reviewed_fields": (
                    "place_id;place_name;place_semantic;relation_existence;"
                    "interpretation_limit"
                ),
                "scope_status": scope_status,
                "place_semantic": semantic,
                "interpretation_limit": review["scope_boundary"],
                "original_place_id": original_place_id,
                "original_place_name": review["place_name_original"],
                "place_review_task_id": review["task_id"],
                "place_review_status": place_review_status(
                    edge_id, review["decision"]
                ),
                "place_human_decision": human_decision,
                "place_review_scope": (
                    "endpoint_identity;relation_existence;"
                    "interpretation_boundary"
                ),
                "place_reviewed_fields": (
                    "place_id;place_name;place_semantic;scope_boundary"
                ),
                "place_approved_formulation": review[
                    "approved_formulation"
                ],
                "place_scope_boundary": review["scope_boundary"],
                "place_decision_source_report": review[
                    "decision_source_report"
                ],
                "approved_formulation": review["approved_formulation"],
                "review_scope": (
                    "endpoint_identity;relation_existence;"
                    "interpretation_boundary"
                ),
                "claim_status": claim_status,
                "confirmed_scope": (
                    review["approved_formulation"] if not retired else ""
                ),
                "missing_scope": (
                    "Direct central source-ID integration remains pending."
                    if edge_id == "AP049"
                    else (
                        "The rejected or redundant place proposition is not "
                        "available for analysis."
                        if retired
                        else "No headquarters, branch, alliance, political stance "
                        "or causal effect beyond the approved place semantic."
                    )
                ),
                "graph_eligibility": graph_eligibility,
            }
        )
        if not edge.get("decision_source_report"):
            edge["decision_source_report"] = review["decision_source_report"]

    write_csv(root / PLACE_EDGES, fields, edges)
    return fields, edges, semantic_counts, len(queue)


def write_summary(
    root: Path,
    issue_count: int,
    place_count: int,
    semantic_counts: Counter[str],
) -> dict[str, int]:
    summary = {
        "hr024_case_issue_edges": issue_count,
        "hr025_reviewed_place_edges": place_count,
        "hr025_site_presence": semantic_counts["site_presence"],
        "hr025_advocacy_target": semantic_counts["advocacy_target"],
        "hr025_event_site": semantic_counts["event_site"],
        "hr025_headquarters": semantic_counts["headquarters"],
        "hr025_retired": len(RETIRED_PLACE_EDGES),
    }
    write_csv(
        root / OUT / "merge_summary_v1.csv",
        ["metric", "value"],
        [
            {"metric": metric, "value": str(value)}
            for metric, value in summary.items()
        ],
    )
    (root / OUT / "README.md").write_text(
        "# HR-024 / HR-025 edge merge\n\n"
        "- Seven HR-024 actor-issue edges are accepted only within Dugong case "
        "R8C01; they do not establish organizational continuity, alliance, "
        "litigation success or project effects.\n"
        "- HR024-001 (A073 identity) remains undecided and creates no edge.\n"
        "- All 47 HR-025 place-edge decisions are applied: 42 active/candidate "
        "semantics and five retired propositions.\n"
        "- Actor-place records are administrative/spatial observations, not "
        "actor-to-actor relations.\n"
        "- AP049 remains `needs_second_source` until its direct annual-report URL "
        "has a central source ID.\n",
        encoding="utf-8",
    )
    return summary


def apply_hr024_hr025_edges(root: Path = ROOT) -> dict[str, int]:
    _, _, issue_count = merge_hr024(root)
    _, _, semantic_counts, place_count = merge_hr025(root)
    expected_semantics = Counter(
        {
            "site_presence": 27,
            "advocacy_target": 7,
            "event_site": 4,
            "headquarters": 4,
        }
    )
    if semantic_counts != expected_semantics:
        raise ValueError(
            f"unexpected HR-025 semantic distribution: {semantic_counts}"
        )
    return write_summary(root, issue_count, place_count, semantic_counts)


if __name__ == "__main__":
    result = apply_hr024_hr025_edges()
    print(
        "HR-024/025 merge complete: "
        f"{result['hr024_case_issue_edges']} case issue edges and "
        f"{result['hr025_reviewed_place_edges']} place reviews."
    )
