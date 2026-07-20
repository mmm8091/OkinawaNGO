from __future__ import annotations

"""Apply the principal-confirmed HR-035 Batch 2 review decisions.

The public interface is :func:`apply_hr035_batch02`.  It validates the complete
23-item return, updates only the five reviewed actor identities and eighteen
reviewed actor--issue facts, emits an auditable manifest/report, and is
byte-idempotent.

This merge does not regenerate any downstream package and does not approve
actor--actor relations, funding, event edges, place edges, alliances or causal
claims.
"""

import csv
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

ACTOR_PATH = Path("data/interim/01_actor_registry_initial_v0.csv")
EDGE_PATH = Path("data/interim/07_actor_issue_edges_initial_v0.csv")
SOURCE_PATH = Path("data/interim/05_source_log_initial_v0.csv")
EDGE_REVIEW_PATH = Path(
    "outputs/actor_issue_claim_freeze_v1/"
    "HR035_actor_issue_fact_review_batch02_v1.csv"
)
IDENTITY_REVIEW_PATH = Path(
    "outputs/actor_issue_claim_freeze_v1/"
    "HR035_actor_identity_companion_batch02_v1.csv"
)
OUT_DIR = Path("outputs/hr035_batch02_integration_v1")
RETURN_REPORT = "docs/human_review_return_HR035_batch02_v1.md"

PRINCIPAL = "project_principal_user"
REVIEW_DATE = "2026-07-20"

EXPECTED_EDGE_IDS = (
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
)
EXPECTED_ACTOR_IDS = ("A007", "A017", "A018", "A049", "A066")

EDGE_DECISION_TO_STATUS = {
    "accept": "human_checked",
    "revise": "human_revised",
    "defer_second_source": "needs_second_source",
    "defer_local": "needs_local_retrieval",
    "reject": "rejected",
}
IDENTITY_DECISION_TO_STATUS = {
    "accept_identity": "human_checked",
    "revise_identity": "human_revised",
    "defer_second_source": "needs_second_source",
    "defer_local": "needs_local_retrieval",
    "reject_identity": "rejected",
}

MANIFEST_FIELDS = [
    "review_item_id",
    "object_type",
    "object_id",
    "principal_decision",
    "central_human_decision",
    "final_review_status",
    "final_evidence_level",
    "claim_status",
    "scope_kind",
    "central_action",
    "decision_source_report",
]


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fields,
            extrasaction="ignore",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def unique_index(
    rows: list[dict[str, str]], key: str
) -> dict[str, dict[str, str]]:
    indexed = {row[key]: row for row in rows}
    if len(indexed) != len(rows):
        raise ValueError(f"duplicate {key}")
    return indexed


def append_note(current: str, addition: str) -> str:
    current = current.strip()
    addition = addition.strip()
    if not addition or addition in current:
        return current
    return f"{current} {addition}".strip()


def central_decision(principal_decision: str) -> str:
    if principal_decision in {"accept", "accept_identity"}:
        return "accept"
    if principal_decision in {"revise", "revise_identity"}:
        return "revise"
    if principal_decision in {"defer_second_source", "defer_local"}:
        return "defer"
    return "reject"


def split_refs(value: str) -> list[str]:
    return [
        item.strip()
        for item in value.replace(",", ";").split(";")
        if item.strip()
    ]


def require_complete_returns(
    edge_reviews: list[dict[str, str]],
    identity_reviews: list[dict[str, str]],
) -> None:
    if [row["edge_id"] for row in edge_reviews] != list(EXPECTED_EDGE_IDS):
        raise ValueError("HR-035 Batch 2 edge set or order drifted")
    if [row["actor_id"] for row in identity_reviews] != list(EXPECTED_ACTOR_IDS):
        raise ValueError("HR-035 Batch 2 identity set or order drifted")

    required_edge_fields = (
        "human_decision",
        "revised_review_status",
        "evidence_level_final",
        "source_ref",
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
    )
    required_identity_fields = (
        "human_decision",
        "revised_review_status",
        "evidence_level_final",
        "source_ref",
        "canonical_name_final",
        "actor_class_final",
        "origin_type_final",
        "legal_status_final",
        "approved_identity_formulation",
        "reviewed_fields",
        "identity_interpretation_limit",
        "human_reviewer",
        "review_date",
    )
    for row in edge_reviews:
        missing = [field for field in required_edge_fields if not row.get(field, "")]
        if missing:
            raise ValueError(
                f"{row.get('review_item_id', '<edge>')} incomplete fields: {missing}"
            )
        decision = row["human_decision"]
        if decision not in EDGE_DECISION_TO_STATUS:
            raise ValueError(f"illegal edge decision {decision!r}")
        if row["revised_review_status"] != EDGE_DECISION_TO_STATUS[decision]:
            raise ValueError(
                f"{row['edge_id']} decision/status mismatch: "
                f"{decision}/{row['revised_review_status']}"
            )
    for row in identity_reviews:
        missing = [
            field for field in required_identity_fields if not row.get(field, "")
        ]
        if missing:
            raise ValueError(
                f"{row.get('review_item_id', '<identity>')} incomplete fields: {missing}"
            )
        decision = row["human_decision"]
        if decision not in IDENTITY_DECISION_TO_STATUS:
            raise ValueError(f"illegal identity decision {decision!r}")
        if row["revised_review_status"] != IDENTITY_DECISION_TO_STATUS[decision]:
            raise ValueError(
                f"{row['actor_id']} identity decision/status mismatch: "
                f"{decision}/{row['revised_review_status']}"
            )

    all_reviews = edge_reviews + identity_reviews
    if any(row["human_reviewer"] != PRINCIPAL for row in all_reviews):
        raise ValueError("all 23 decisions must be principal-confirmed")
    if any(row["review_date"] != REVIEW_DATE for row in all_reviews):
        raise ValueError("all 23 decisions must use the confirmed review date")

    edge_counts = Counter(row["human_decision"] for row in edge_reviews)
    identity_counts = Counter(row["human_decision"] for row in identity_reviews)
    if edge_counts != Counter(
        {"accept": 7, "revise": 9, "defer_second_source": 2}
    ):
        raise ValueError(f"unexpected edge decision distribution: {edge_counts}")
    if identity_counts != Counter(
        {"accept_identity": 1, "revise_identity": 4}
    ):
        raise ValueError(
            f"unexpected identity decision distribution: {identity_counts}"
        )


def require_central_crosswalks(
    edges: dict[str, dict[str, str]],
    edge_reviews: list[dict[str, str]],
    identity_reviews: list[dict[str, str]],
    source_ids: set[str],
) -> None:
    for review in edge_reviews:
        edge_id = review["edge_id"]
        if review["review_item_id"] != f"HR035-B02-{edge_id}":
            raise ValueError(f"{edge_id} review_item_id drifted")
        central = edges[edge_id]
        if (
            review["actor_id"] != central["actor_id"]
            or review["issue_id"] != central["issue_id"]
        ):
            raise ValueError(
                f"{edge_id} edge review crosswalk mismatch: "
                f"{review['actor_id']}/{review['issue_id']} != "
                f"{central['actor_id']}/{central['issue_id']}"
            )
    for review in identity_reviews:
        actor_id = review["actor_id"]
        if review["review_item_id"] != f"HR035-B02-ID-{actor_id}":
            raise ValueError(f"{actor_id} identity review_item_id drifted")

    unknown_sources = sorted(
        {
            source_id
            for review in edge_reviews + identity_reviews
            for source_id in split_refs(review["source_ref"])
            if source_id not in source_ids
        }
    )
    if unknown_sources:
        raise ValueError(
            "HR-035 Batch 2 review contains unknown source refs: "
            + ";".join(unknown_sources)
        )


def merge_identities(
    actors: dict[str, dict[str, str]],
    reviews: list[dict[str, str]],
) -> list[dict[str, str]]:
    manifest: list[dict[str, str]] = []
    for review in reviews:
        actor = actors[review["actor_id"]]
        decision = review["human_decision"]
        actor.update(
            {
                "canonical_name": review["canonical_name_final"],
                "actor_class": review["actor_class_final"],
                "origin_type": review["origin_type_final"],
                "legal_status_guess": review["legal_status_final"],
                "evidence_level": review["evidence_level_final"],
                "review_status": review["revised_review_status"],
                "human_decision": central_decision(decision),
                "review_task_id": review["review_item_id"],
                "human_reviewer": PRINCIPAL,
                "review_date": REVIEW_DATE,
                "reviewed_fields": review["reviewed_fields"],
                "identity_review_ref": RETURN_REPORT,
            }
        )
        # S024 is another project's page and was explicitly excluded as A018
        # identity evidence by the principal-confirmed review.
        if review["actor_id"] == "A018":
            actor["source_refs"] = "S023"
        identity_note = (
            "HR-035 Batch 2 principal-confirmed identity review "
            f"({review['review_item_id']}): "
            f"{review['approved_identity_formulation']} "
            f"Boundary: {review['identity_interpretation_limit']}"
        )
        actor["notes"] = append_note(actor.get("notes", ""), identity_note)
        manifest.append(
            {
                "review_item_id": review["review_item_id"],
                "object_type": "actor_identity",
                "object_id": review["actor_id"],
                "principal_decision": decision,
                "central_human_decision": central_decision(decision),
                "final_review_status": review["revised_review_status"],
                "final_evidence_level": review["evidence_level_final"],
                "claim_status": "",
                "scope_kind": "actor_identity",
                "central_action": "identity_fields_updated",
                "decision_source_report": RETURN_REPORT,
            }
        )
    return manifest


def migrate_revised_scope(
    edge: dict[str, str], review: dict[str, str]
) -> None:
    edge.update(
        {
            "scope_status": f"scope_revised_{review['review_scope_final']}",
            "scope_kind": review["review_scope_final"],
            "scope_review_status": "human_revised",
            "scope_human_decision": "revise",
            "scope_review_task_id": review["review_item_id"],
            "scope_human_reviewer": PRINCIPAL,
            "scope_review_date": REVIEW_DATE,
            "scope_reviewed_fields": (
                "scope_kind;scope_status;scope_approved_formulation;scope_boundary"
            ),
            "scope_claim_status": review["claim_status"],
            "scope_approved_formulation": review["approved_formulation"],
            "scope_boundary": review["interpretation_limit"],
            "scope_decision_source_report": RETURN_REPORT,
        }
    )


def merge_edges(
    edges: dict[str, dict[str, str]],
    reviews: list[dict[str, str]],
) -> list[dict[str, str]]:
    manifest: list[dict[str, str]] = []
    for review in reviews:
        edge = edges[review["edge_id"]]
        decision = review["human_decision"]
        edge.update(
            {
                "relation_basis": review["approved_formulation"],
                "source_ref": review["source_ref"],
                "evidence_level": review["evidence_level_final"],
                "review_status": review["revised_review_status"],
                "human_decision": central_decision(decision),
                "review_task_id": review["review_item_id"],
                "human_reviewer": PRINCIPAL,
                "review_date": REVIEW_DATE,
                "reviewed_fields": review["reviewed_fields"],
                "decision_source_report": RETURN_REPORT,
                "interpretation_limit": review["interpretation_limit"],
                "claim_status": review["claim_status"],
                "review_scope": review["review_scope_final"],
                "confirmed_scope": review["confirmed_scope"],
                "missing_scope": review["missing_scope"],
                "approved_formulation": review["approved_formulation"],
            }
        )
        if decision in {"accept", "revise"}:
            edge["graph_eligibility"] = "reviewed_actor_issue"
        elif decision in {"defer_second_source", "defer_local"}:
            # A completed defer remains an active research candidate, never a
            # reviewed edge.  Blank is the established actor--issue candidate
            # encoding consumed by the current builders.
            edge["graph_eligibility"] = ""
        else:
            edge["graph_eligibility"] = "excluded"
            edge["scope_status"] = "excluded_claim_rejected"

        if review["edge_id"] == "AI044":
            edge["invalidated_source_ref"] = append_note(
                edge.get("invalidated_source_ref", ""), "S024"
            )
        if review["scope_revision_required"] == "yes":
            migrate_revised_scope(edge, review)

        edge["notes"] = append_note(
            edge.get("notes", ""),
            "HR-035 Batch 2 principal-confirmed factual review "
            f"({review['review_item_id']}).",
        )
        manifest.append(
            {
                "review_item_id": review["review_item_id"],
                "object_type": "actor_issue_fact",
                "object_id": review["edge_id"],
                "principal_decision": decision,
                "central_human_decision": central_decision(decision),
                "final_review_status": review["revised_review_status"],
                "final_evidence_level": review["evidence_level_final"],
                "claim_status": review["claim_status"],
                "scope_kind": review["review_scope_final"],
                "central_action": (
                    "kept_as_candidate_needs_second_source"
                    if decision == "defer_second_source"
                    else "fact_fields_updated"
                ),
                "decision_source_report": RETURN_REPORT,
            }
        )
    return manifest


def build_validation_report(
    actor_rows: list[dict[str, str]],
    edge_rows: list[dict[str, str]],
    manifest: list[dict[str, str]],
) -> str:
    actor_by_id = unique_index(actor_rows, "actor_id")
    edge_by_id = unique_index(edge_rows, "edge_id")
    target_edges = [edge_by_id[edge_id] for edge_id in EXPECTED_EDGE_IDS]
    active_actor_ids: set[str] = set()
    for actor in actor_rows:
        review_status = actor.get("review_status", "").strip().lower()
        scope_status = actor.get("scope_status", "").strip().lower()
        inactive = (
            scope_status in {"merged_duplicate", "out_of_scope", "rejected"}
            or scope_status.startswith(("retired_", "deactivated_"))
            or "excluded" in scope_status
            or review_status == "rejected"
        )
        if not inactive:
            active_actor_ids.add(actor["actor_id"])
    active_edges: list[dict[str, str]] = []
    for edge in edge_rows:
        review_status = edge.get("review_status", "").strip().lower()
        claim_status = edge.get("claim_status", "").strip().lower()
        graph_eligibility = edge.get("graph_eligibility", "").strip().lower()
        scope_status = edge.get("scope_status", "").strip().lower()
        inactive = (
            edge.get("actor_id", "") not in active_actor_ids
            or review_status == "rejected"
            or claim_status == "unsupported"
            or graph_eligibility == "excluded"
            or scope_status.startswith(("retired_", "deactivated_"))
            or "excluded" in scope_status
        )
        if not inactive:
            active_edges.append(edge)
    reviewed = sum(
        row["review_status"] in {"human_checked", "human_revised"}
        for row in active_edges
    )
    candidate = sum(
        row["review_status"] not in {"human_checked", "human_revised", "rejected"}
        for row in active_edges
    )

    checks = [
        ("23 principal decisions applied", len(manifest) == 23),
        (
            "five identity companions are human-reviewed",
            all(
                actor_by_id[actor_id]["review_status"]
                in {"human_checked", "human_revised"}
                for actor_id in EXPECTED_ACTOR_IDS
            ),
        ),
        (
            "sixteen facts entered the reviewed layer",
            sum(
                row["review_status"] in {"human_checked", "human_revised"}
                for row in target_edges
            )
            == 16,
        ),
        (
            "AI157 and AI158 remain second-source candidates",
            all(
                edge_by_id[edge_id]["review_status"] == "needs_second_source"
                and edge_by_id[edge_id]["claim_status"] == "candidate"
                and edge_by_id[edge_id]["graph_eligibility"] != "reviewed_actor_issue"
                for edge_id in ("AI157", "AI158")
            ),
        ),
        (
            "AI044 uses S023 and records S024 as invalidated",
            edge_by_id["AI044"]["source_ref"] == "S023"
            and "S024" in edge_by_id["AI044"]["invalidated_source_ref"].split(),
        ),
        (
            "AI016 and AI233 are explicitly event-scoped",
            all(
                edge_by_id[edge_id]["scope_kind"] == "event_specific"
                and edge_by_id[edge_id]["scope_review_status"] == "human_revised"
                for edge_id in ("AI016", "AI233")
            ),
        ),
    ]
    errors = [label for label, passed in checks if not passed]
    status = "PASS" if not errors else "FAIL"
    lines = [
        "# HR-035 Batch 2 controlled merge validation v1",
        "",
        f"Date: {REVIEW_DATE}",
        "",
        f"Status: **{status}**",
        "",
        "Validated boundaries:",
        "",
        *[
            f"- {'PASS' if passed else 'FAIL'} — {label}."
            for label, passed in checks
        ],
        (
            f"- Central actor registry remains {len(actor_rows)} history rows; "
            "no actor was added or removed."
        ),
        (
            f"- Central actor–issue table remains {len(edge_rows)} history rows; "
            f"the current analytical gate yields {len(active_edges)} active rows "
            f"({reviewed} human-reviewed / {candidate} candidate) before "
            "downstream regeneration."
        ),
        (
            "- The merge changes only five reviewed actor rows and eighteen reviewed "
            "actor–issue rows; all other central rows are protected by the merge."
        ),
        (
            "- AI157 and AI158 are completed human defer decisions and online "
            "second-source leads, not blank review tasks or accepted facts."
        ),
        (
            "- No actor–actor relation, funding relation, event, place, alliance, "
            "continuity or causal claim is approved."
        ),
        "",
        f"Errors: {'none.' if not errors else '; '.join(errors)}",
        "",
    ]
    if errors:
        raise AssertionError("; ".join(errors))
    return "\n".join(lines)


def apply_hr035_batch02(root: Path = ROOT) -> dict[str, int]:
    actor_fields, actor_rows = read_csv(root / ACTOR_PATH)
    edge_fields, edge_rows = read_csv(root / EDGE_PATH)
    _, source_rows = read_csv(root / SOURCE_PATH)
    _, edge_reviews = read_csv(root / EDGE_REVIEW_PATH)
    _, identity_reviews = read_csv(root / IDENTITY_REVIEW_PATH)

    require_complete_returns(edge_reviews, identity_reviews)
    actors = unique_index(actor_rows, "actor_id")
    edges = unique_index(edge_rows, "edge_id")
    missing_actors = set(EXPECTED_ACTOR_IDS) - set(actors)
    missing_edges = set(EXPECTED_EDGE_IDS) - set(edges)
    if missing_actors or missing_edges:
        raise ValueError(
            f"central targets missing: actors={sorted(missing_actors)}, "
            f"edges={sorted(missing_edges)}"
        )
    source_ids = set(unique_index(source_rows, "source_id"))
    require_central_crosswalks(
        edges,
        edge_reviews,
        identity_reviews,
        source_ids,
    )

    untouched_actors_before = {
        actor_id: dict(row)
        for actor_id, row in actors.items()
        if actor_id not in EXPECTED_ACTOR_IDS
    }
    untouched_edges_before = {
        edge_id: dict(row)
        for edge_id, row in edges.items()
        if edge_id not in EXPECTED_EDGE_IDS
    }

    manifest = merge_identities(actors, identity_reviews)
    manifest.extend(merge_edges(edges, edge_reviews))

    untouched_actors_after = {
        actor_id: row
        for actor_id, row in actors.items()
        if actor_id not in EXPECTED_ACTOR_IDS
    }
    untouched_edges_after = {
        edge_id: row
        for edge_id, row in edges.items()
        if edge_id not in EXPECTED_EDGE_IDS
    }
    if untouched_actors_before != untouched_actors_after:
        raise AssertionError("merge modified a non-Batch-2 actor row")
    if untouched_edges_before != untouched_edges_after:
        raise AssertionError("merge modified a non-Batch-2 actor–issue row")

    # Validate the complete in-memory result before mutating any central file.
    validation_report = build_validation_report(actor_rows, edge_rows, manifest)
    write_csv(root / ACTOR_PATH, actor_fields, actor_rows)
    write_csv(root / EDGE_PATH, edge_fields, edge_rows)
    write_csv(root / OUT_DIR / "merge_manifest_v1.csv", MANIFEST_FIELDS, manifest)
    report_path = root / OUT_DIR / "validation_report_v1.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(validation_report, encoding="utf-8")

    return {
        "principal_decisions": len(manifest),
        "identity_accept": 1,
        "identity_revise": 4,
        "edge_accept": 7,
        "edge_revise": 9,
        "edge_defer_second_source": 2,
    }


def main() -> None:
    summary = apply_hr035_batch02(ROOT)
    print(
        "HR-035 Batch 2 merged: "
        f"{summary['principal_decisions']} principal decisions; "
        f"{summary['edge_accept']} accept / {summary['edge_revise']} revise / "
        f"{summary['edge_defer_second_source']} defer_second_source."
    )


if __name__ == "__main__":
    main()
