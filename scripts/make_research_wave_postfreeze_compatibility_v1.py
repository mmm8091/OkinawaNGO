from __future__ import annotations

"""Build a read-only post-freeze compatibility overlay for H1/H2/H3.

The historical research-wave packages are provenance snapshots.  This builder
does not regenerate or overwrite them.  It reuses their public calculation
functions in memory, compares them with the frozen central layer, and writes a
new research-only compatibility package.
"""

import csv
import hashlib
import importlib.util
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "research_wave_postfreeze_compatibility_v1"
AUDIT_DATE = "2026-07-20"

ACTORS = ROOT / "data" / "interim" / "01_actor_registry_initial_v0.csv"
SOURCES = ROOT / "data" / "interim" / "05_source_log_initial_v0.csv"
EDGES = ROOT / "data" / "interim" / "24_r01_r02_actor_issue_layered_v0.csv"
TRIPLES = (
    ROOT
    / "outputs"
    / "R03_strict_place_issue_v1"
    / "same_source_actor_place_issue_triples_v1.csv"
)
EVENTS = ROOT / "data" / "interim" / "09_actor_event_venue_edges_v0.csv"
CASE_ROLES = ROOT / "data" / "interim" / "18_legal_policy_actor_roles_v0.csv"
LIFECYCLE = (
    ROOT / "outputs" / "actor_lifecycle_v1" / "actor_lifecycle_v0.csv"
)

H1_V1_DIR = ROOT / "outputs" / "research_wave_h1_documentation_visibility_v1"
H1_V2_DIR = ROOT / "outputs" / "research_wave_h1_documentation_visibility_v2"
H2_V1_DIR = ROOT / "outputs" / "research_wave_h2_two_ecologies_v1"
H2_SERVICE_DIR = ROOT / "outputs" / "research_wave_h2_service_universe_v1"
H2_RECIPIENT_DIR = (
    ROOT / "outputs" / "research_wave_h2_recipient_permeability_v1"
)
H3_V1_DIR = ROOT / "outputs" / "research_wave_h3_frontline_memory_v1"
H3_V2_DIR = ROOT / "outputs" / "research_wave_h3_frontline_memory_v2"
TOPIC_DIR = ROOT / "outputs" / "research_wave_topic_selection_v1"

H1_V1_SCRIPT = ROOT / "scripts" / "make_h1_documentation_visibility_v1.py"
H1_V2_SCRIPT = ROOT / "scripts" / "make_h1_documentation_visibility_v2.py"
H2_V1_SCRIPT = ROOT / "scripts" / "make_h2_two_ecologies_v1.py"
H3_V1_SCRIPT = ROOT / "scripts" / "make_h3_frontline_memory_v1.py"
H3_V2_SCRIPT = (
    ROOT / "scripts" / "make_research_wave_h3_frontline_memory_v2.py"
)

HUMAN = {"human_checked", "human_revised"}
E3PLUS = {"E3", "E4"}
PACKAGE_META = {
    "research_status": "research_only",
    "claim_status": "candidate_analysis",
    "review_status": "ai_seeded",
    "frontend_eligibility": "not_frontend_ready",
    "central_writeback": "no",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_csv(
    path: Path,
    rows: Sequence[Mapping[str, Any]],
    fieldnames: Sequence[str] | None = None,
) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    if fieldnames is None:
        ordered: list[str] = []
        seen: set[str] = set()
        for row in rows:
            for key in row:
                if key not in seen:
                    seen.add(key)
                    ordered.append(key)
        fieldnames = ordered
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(fieldnames),
            extrasaction="ignore",
        )
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_sha256(directory: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in directory.rglob("*") if item.is_file()):
        digest.update(path.relative_to(directory).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def import_script(path: Path, module_name: str) -> Any:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def canon_rows(rows: Iterable[Mapping[str, Any]]) -> list[str]:
    return sorted(
        json.dumps(
            {key: str(value) for key, value in row.items()},
            ensure_ascii=False,
            sort_keys=True,
        )
        for row in rows
    )


def current_inputs(h1: Any) -> dict[str, Any]:
    actor_history = read_csv(ACTORS)
    actors = [row for row in actor_history if h1.current_actor(row)]
    actor_ids = {row["actor_id"] for row in actors}
    edge_history = read_csv(EDGES)
    edges = [
        row
        for row in edge_history
        if row["analysis_inclusion"] == "active"
        and row["actor_id"] in actor_ids
    ]
    triples = [
        row for row in read_csv(TRIPLES) if row["actor_id"] in actor_ids
    ]
    sources = read_csv(SOURCES)
    events = [
        row
        for row in read_csv(EVENTS)
        if row["reviewer_status"] == "human_checked"
        and row["entity_type"] == "registry_actor"
        and row["actor_or_counterpart_id"] in actor_ids
        and row["event_id"]
    ]
    roles = [
        row
        for row in read_csv(CASE_ROLES)
        if row["actor_id"] in actor_ids
        and row["review_status"] == "human_checked"
        and row["human_decision"] == "accept"
    ]
    return {
        "actor_history": actor_history,
        "actors": actors,
        "actor_ids": actor_ids,
        "edge_history": edge_history,
        "edges": edges,
        "triples": triples,
        "sources": sources,
        "events": events,
        "roles": roles,
    }


def strict_counts(triples: Sequence[Mapping[str, str]]) -> dict[str, int]:
    e3plus_rows = [
        row
        for row in triples
        if row["place_evidence_level"] in E3PLUS
        and row["issue_evidence_level"] in E3PLUS
    ]
    return {
        "active_same_source_triples": len(triples),
        "e3plus_triples": len(e3plus_rows),
        "dual_human_reviewed_triples": sum(
            row["place_review_status"] in HUMAN
            and row["issue_review_status"] in HUMAN
            for row in triples
        ),
        "event_attached_triples": sum(
            bool(row["event_ids"]) for row in e3plus_rows
        ),
    }


def current_snapshot(data: Mapping[str, Any]) -> dict[str, Any]:
    edges = data["edges"]
    reviewed = [row for row in edges if row["review_status"] in HUMAN]
    candidate = [row for row in edges if row["review_status"] not in HUMAN]
    e3plus = [row for row in edges if row["evidence_level"] in E3PLUS]
    e3plus_reviewed = [
        row for row in e3plus if row["review_status"] in HUMAN
    ]
    e3plus_candidate = [
        row for row in e3plus if row["review_status"] not in HUMAN
    ]
    connected = {row["actor_id"] for row in edges}
    return {
        "as_of_date": AUDIT_DATE,
        "layer": PACKAGE_META,
        "actor_registry": {
            "history_rows": len(data["actor_history"]),
            "current_actors": len(data["actors"]),
        },
        "actor_issue": {
            "history_rows": len(data["edge_history"]),
            "active_edges": len(edges),
            "reviewed_edges": len(reviewed),
            "candidate_edges": len(candidate),
            "connected_actors": len(connected),
            "isolated_current_actors": len(data["actors"]) - len(connected),
            "evidence_level_counts": dict(
                sorted(Counter(row["evidence_level"] for row in edges).items())
            ),
            "review_status_counts": dict(
                sorted(Counter(row["review_status"] for row in edges).items())
            ),
            "e3plus_edges": len(e3plus),
            "e3plus_connected_actors": len(
                {row["actor_id"] for row in e3plus}
            ),
            "e3plus_reviewed_edges": len(e3plus_reviewed),
            "e3plus_reviewed_actors": len(
                {row["actor_id"] for row in e3plus_reviewed}
            ),
            "e3plus_candidate_edges": len(e3plus_candidate),
            "e3plus_candidate_actors": len(
                {row["actor_id"] for row in e3plus_candidate}
            ),
        },
        "strict_place_issue": strict_counts(data["triples"]),
        "other_current_objects": {
            "human_checked_registered_actor_event_rows": len(data["events"]),
            "accepted_registered_actor_case_roles": len(data["roles"]),
            "source_rows": len(data["sources"]),
        },
        "interpretation_limit": (
            "Mechanical state of the frozen project coding layer; counts are "
            "not population estimates, alliance measures, activity strength, "
            "or causal findings."
        ),
    }


def build_h1_actor_rows(h1: Any, data: Mapping[str, Any]) -> list[dict[str, Any]]:
    archive_rows = read_csv(h1.ARCHIVE)
    source_features = h1.source_feature_rows(data["sources"], archive_rows)
    lifecycle = read_csv(h1.LIFECYCLE)
    class_map = {
        row["actor_class_original"]: row["analysis_family_v1"]
        for row in read_csv(h1.CLASS_MAP)
    }
    with h1.DYADIC.open(encoding="utf-8") as handle:
        dyadic_all = json.load(handle)
    dyadic = [
        row
        for row in dyadic_all
        if row.get("display_tier") == "reviewed"
        and row.get("graph_eligibility") == "dyadic_relation"
        and row.get("source_endpoint") in data["actor_ids"]
        and row.get("target_endpoint") in data["actor_ids"]
    ]
    actor_rows, _ = h1.build_actor_rows(
        data["actors"],
        data["sources"],
        source_features,
        data["edges"],
        data["triples"],
        data["events"],
        data["roles"],
        lifecycle,
        class_map,
        dyadic,
    )
    return actor_rows


def dynamic_review_sensitivity(
    h1: Any,
    actor_rows: Sequence[Mapping[str, Any]],
    edges: Sequence[Mapping[str, str]],
) -> list[dict[str, Any]]:
    resolved = [
        row
        for row in actor_rows
        if int(row["unresolved_reference_count"]) == 0
    ]
    reviewed_statuses = Counter(
        row["review_status"]
        for row in edges
        if row["review_status"] in HUMAN
    )
    candidate_statuses = Counter(
        row["review_status"]
        for row in edges
        if row["review_status"] not in HUMAN
    )
    reviewed_n = sum(reviewed_statuses.values())
    candidate_n = sum(candidate_statuses.values())
    layers = [
        (
            f"active_{len(edges)}",
            "active_actor_issue_degree",
            f"{reviewed_n} reviewed + {candidate_n} candidate edges",
        ),
        (
            f"reviewed_{reviewed_n}",
            "reviewed_actor_issue_degree",
            " + ".join(
                f"{count} {status}"
                for status, count in sorted(reviewed_statuses.items())
            )
            + " edges",
        ),
        (
            f"candidate_{candidate_n}",
            "candidate_actor_issue_degree",
            " + ".join(
                f"{count} {status}"
                for status, count in sorted(candidate_statuses.items())
            )
            + " edges",
        ),
    ]
    proxies = [
        (
            "linked_source_count",
            "construction_diagnostic",
            "includes sources used by the actor-issue outcome",
        ),
        (
            "registry_source_count",
            "primary_registry_proxy",
            "identity-layer S-source refs only",
        ),
        (
            "non_issue_linked_source_count",
            "primary_outcome_excluded_proxy",
            "all linked S-sources minus actor-issue support sources",
        ),
    ]
    rows: list[dict[str, Any]] = []
    index = 1
    unresolved_n = len(actor_rows) - len(resolved)
    for subset, members in (
        ("all_current_actors", actor_rows),
        ("resolved_reference_actors_only", resolved),
    ):
        for layer, outcome, boundary in layers:
            for proxy, role, proxy_boundary in proxies:
                rho = h1.spearman(
                    [float(row[proxy]) for row in members],
                    [float(row[outcome]) for row in members],
                )
                rows.append(
                    {
                        "review_sensitivity_id": f"PFH1R{index:03d}",
                        "subset": subset,
                        "actor_count": len(members),
                        "actor_issue_layer": layer,
                        "edge_count_in_subset": sum(
                            int(row[outcome]) for row in members
                        ),
                        "x_measure": proxy,
                        "y_measure": outcome,
                        "spearman_rho": (
                            "" if rho is None else round(rho, 3)
                        ),
                        "diagnostic_role": role,
                        "layer_review_boundary": boundary,
                        "proxy_boundary": proxy_boundary,
                        "crosswalk_boundary": (
                            f"{unresolved_n} unresolved legacy-token actors "
                            + (
                                "retained"
                                if subset == "all_current_actors"
                                else "excluded"
                            )
                        ),
                        **PACKAGE_META,
                        "interpretation_limit": (
                            "Review-layer sensitivity of the encoded actor--"
                            "issue object only; review selection is endogenous "
                            "and documentation proxies do not measure staff "
                            "capacity."
                        ),
                    }
                )
                index += 1
    return rows


def build_h1_outputs(
    h1: Any,
    data: Mapping[str, Any],
    snapshot: Mapping[str, Any],
) -> dict[str, Any]:
    actor_rows = build_h1_actor_rows(h1, data)
    associations = h1.build_associations(actor_rows)
    review_rows = dynamic_review_sensitivity(h1, actor_rows, data["edges"])
    source_dependency = h1.build_source_dependency(
        data["edges"],
        data["sources"],
    )
    source_features = h1.source_feature_rows(
        data["sources"],
        read_csv(h1.ARCHIVE),
    )
    scenarios = h1.build_sensitivity(
        actor_rows,
        data["edges"],
        source_features,
    )
    s004 = next(
        row for row in source_dependency if row["source_id"] == "S004"
    )
    big3 = next(
        row for row in scenarios if row["scenario_id"] == "SRC_NO_BIG3"
    )
    s004_scenario = next(
        row for row in scenarios if row["scenario_id"] == "SRC_NO_S004"
    )
    e3plus = [
        row for row in data["edges"] if row["evidence_level"] in E3PLUS
    ]
    removed_s004 = [
        row
        for row in e3plus
        if h1.source_refs(row.get("source_ref", ""))
        and not (
            h1.source_refs(row.get("source_ref", "")) - {"S004"}
        )
    ]
    s004_incident_actors = {
        row["actor_id"] for row in removed_s004
    }
    remaining_s004 = h1.select_edges_after_source_deletion(
        e3plus,
        {"S004"},
    )
    fully_lost_s004 = (
        {row["actor_id"] for row in e3plus}
        - {row["actor_id"] for row in remaining_s004}
    )
    old_metrics = read_json(H1_V2_DIR / "metrics_v2.json")
    old_associations = {
        row["analysis_id"]: row
        for row in read_csv(H1_V2_DIR / "association_estimates_v2.csv")
    }
    association_delta: list[dict[str, Any]] = []
    for row in associations:
        old = old_associations.get(row["analysis_id"], {})
        association_delta.append(
            {
                "analysis_id": row["analysis_id"],
                "graph_object": row["graph_object"],
                "subset": row["subset"],
                "x_measure": row["x_measure"],
                "y_measure": row["y_measure"],
                "old_actor_count": old.get("actor_count", ""),
                "current_actor_count": row["actor_count"],
                "old_spearman_rho": old.get("spearman_rho", ""),
                "current_spearman_rho": row["spearman_rho"],
                "compatibility_status": "recompute_required",
                "impact": (
                    "high"
                    if row["graph_object"].startswith("actor_issue")
                    else "low"
                ),
                **PACKAGE_META,
                "interpretation_limit": row["interpretation_limit"],
            }
        )
    metrics = {
        "as_of_date": AUDIT_DATE,
        "layer": PACKAGE_META,
        "old_h1_v2_counts": old_metrics["counts"],
        "current_counts": {
            "current_actors": snapshot["actor_registry"]["current_actors"],
            "sources": len(data["sources"]),
            "active_actor_issue_edges": len(data["edges"]),
            "reviewed_actor_issue_edges": snapshot["actor_issue"][
                "reviewed_edges"
            ],
            "candidate_actor_issue_edges": snapshot["actor_issue"][
                "candidate_edges"
            ],
            "e3plus_actor_issue_edges": snapshot["actor_issue"][
                "e3plus_edges"
            ],
            "e3plus_actor_issue_actors": snapshot["actor_issue"][
                "e3plus_connected_actors"
            ],
            "strict_triples": snapshot["strict_place_issue"][
                "active_same_source_triples"
            ],
        },
        "e3plus_review_split": {
            "reviewed_edges": snapshot["actor_issue"][
                "e3plus_reviewed_edges"
            ],
            "reviewed_actors": snapshot["actor_issue"][
                "e3plus_reviewed_actors"
            ],
            "candidate_edges": snapshot["actor_issue"][
                "e3plus_candidate_edges"
            ],
            "candidate_actors": snapshot["actor_issue"][
                "e3plus_candidate_actors"
            ],
        },
        "s004_support_deletion": {
            "baseline_edges": len(e3plus),
            "baseline_observed_actors": len(
                {row["actor_id"] for row in e3plus}
            ),
            "removed_edges": len(removed_s004),
            "incident_actor_count": len(s004_incident_actors),
            "fully_lost_actor_count": len(fully_lost_s004),
            "remaining_edges": int(s004_scenario["edge_count"]),
            "remaining_observed_actors": int(
                s004_scenario["observed_actor_count"]
            ),
            "distinction": (
                "incident_actor_count counts actors touching a removed edge; "
                "fully_lost_actor_count counts actors whose entire E3/E4 "
                "degree becomes zero."
            ),
            "source_dependency_row_lost_actor_count": int(
                s004["lost_observed_actor_count"]
            ),
        },
        "big3_support_deletion": {
            "removed_edges": len(e3plus) - int(big3["edge_count"]),
            "fully_lost_actor_count": (
                len({row["actor_id"] for row in e3plus})
                - int(big3["observed_actor_count"])
            ),
            "remaining_edges": int(big3["edge_count"]),
            "remaining_observed_actors": int(big3["observed_actor_count"]),
            "s004_share_of_big3_removed_edges": round(
                len(removed_s004)
                / (len(e3plus) - int(big3["edge_count"])),
                3,
            ),
        },
        "selected_associations": {
            row["analysis_id"]: {
                "graph_object": row["graph_object"],
                "subset": row["subset"],
                "x_measure": row["x_measure"],
                "y_measure": row["y_measure"],
                "actor_count": row["actor_count"],
                "spearman_rho": row["spearman_rho"],
            }
            for row in associations
            if row["analysis_id"]
            in {"H1A001", "H1A016", "H1A017", "H1A023", "H1A024", "H1A025"}
        },
        "unresolved_reference_actor_count": sum(
            int(row["unresolved_reference_count"]) > 0
            for row in actor_rows
        ),
        "input_hashes": {
            relative(path): sha256(path)
            for path in (
                ACTORS,
                SOURCES,
                EDGES,
                TRIPLES,
                EVENTS,
                CASE_ROLES,
                LIFECYCLE,
            )
        },
        "hard_boundary": (
            "Recomputed encoded visibility only.  No causal documentation "
            "effect, real social-network centrality, staff capacity, alliance, "
            "activity strength, or lifespan inference."
        ),
    }
    return {
        "metrics": metrics,
        "actor_rows": actor_rows,
        "associations": associations,
        "association_delta": association_delta,
        "review_rows": review_rows,
        "source_dependency": source_dependency,
        "scenarios": scenarios,
    }


def build_h2_outputs(h2: Any) -> dict[str, Any]:
    analysis = h2.build_analysis(h2.load_inputs(ROOT))
    old_metrics = read_json(H2_V1_DIR / "metrics_v1.json")
    current_metrics = analysis["metrics"]
    metric_delta: list[dict[str, Any]] = []
    for key in sorted(set(old_metrics) | set(current_metrics)):
        old = old_metrics.get(key)
        current = current_metrics.get(key)
        equal = old == current
        metric_delta.append(
            {
                "metric": key,
                "old_value": json.dumps(
                    old,
                    ensure_ascii=False,
                    sort_keys=True,
                ),
                "current_value": json.dumps(
                    current,
                    ensure_ascii=False,
                    sort_keys=True,
                ),
                "compatibility_status": (
                    "invariant" if equal else "recompute_required"
                ),
                "impact": (
                    "high"
                    if key
                    in {
                        "accountability_comparison_actor_count",
                        "accountability_human_reviewed_anchor_actor_count",
                        "accountability_candidate_only_anchor_actor_count",
                        "accountability_active_issue_edge_count",
                    }
                    else "medium"
                    if not equal
                    else "none"
                ),
                **PACKAGE_META,
                "interpretation_limit": (
                    "A changed project comparison set does not estimate the "
                    "population size of either ecology."
                ),
            }
        )

    old_actor_rows = {
        row["actor_id"]: row
        for row in read_csv(
            H2_V1_DIR / "accountability_comparison_actors_v1.csv"
        )
    }
    current_actor_rows = {
        row["actor_id"]: row for row in analysis["accountability"]
    }
    actor_delta: list[dict[str, Any]] = []
    for actor_id in sorted(set(old_actor_rows) | set(current_actor_rows)):
        old = old_actor_rows.get(actor_id, {})
        current = current_actor_rows.get(actor_id, {})
        actor_delta.append(
            {
                "actor_id": actor_id,
                "actor_name": current.get(
                    "canonical_name",
                    old.get("canonical_name", ""),
                ),
                "membership_change": (
                    "added_postfreeze"
                    if actor_id not in old_actor_rows
                    else "removed_postfreeze"
                    if actor_id not in current_actor_rows
                    else "retained"
                ),
                "old_anchor_selection_evidence_status": old.get(
                    "anchor_selection_evidence_status",
                    "",
                ),
                "current_anchor_selection_evidence_status": current.get(
                    "anchor_selection_evidence_status",
                    "",
                ),
                "old_active_issue_edge_count": old.get(
                    "active_issue_edge_count",
                    "",
                ),
                "current_active_issue_edge_count": current.get(
                    "active_issue_edge_count",
                    "",
                ),
                "old_active_anchor_issue_edge_count": old.get(
                    "active_anchor_issue_edge_count",
                    "",
                ),
                "current_active_anchor_issue_edge_count": current.get(
                    "active_anchor_issue_edge_count",
                    "",
                ),
                **PACKAGE_META,
                "interpretation_limit": (
                    "Mechanical membership in a research comparison selected "
                    "by anchor issue edges; not a political identity, alliance, "
                    "or census."
                ),
            }
        )

    file_map = {
        "service_core_actors_v1.csv": "service_core",
        "accountability_comparison_actors_v1.csv": "accountability",
        "issue_ecology_profile_v1.csv": "issue_profiles",
        "dyadic_relation_ecology_audit_v1.csv": "dyadic",
        "case_role_ecology_audit_v1.csv": "case_roles",
        "typed_event_ecology_audit_v1.csv": "typed_events",
        "r10_interface_audit_v1.csv": "r10",
        "place_overlap_v1.csv": "places",
        "source_overlap_v1.csv": "sources",
        "coverage_gaps_v1.csv": "gaps",
        "human_review_queue_v1.csv": "human_review_queue",
        "further_search_queue_v1.csv": "search_queue",
    }
    asset_comparison: list[dict[str, Any]] = []
    for filename, key in file_map.items():
        old_rows = read_csv(H2_V1_DIR / filename)
        current_rows = analysis[key]
        equal = canon_rows(old_rows) == canon_rows(current_rows)
        asset_comparison.append(
            {
                "asset": relative(H2_V1_DIR / filename),
                "old_row_count": len(old_rows),
                "current_row_count": len(current_rows),
                "row_content_equal": "yes" if equal else "no",
                "compatibility_status": (
                    "invariant" if equal else "recompute_required"
                ),
                "impact": (
                    "high"
                    if filename
                    in {
                        "accountability_comparison_actors_v1.csv",
                        "issue_ecology_profile_v1.csv",
                    }
                    else "medium"
                    if not equal
                    else "none"
                ),
                **PACKAGE_META,
                "interpretation_limit": (
                    "Row equality is a deterministic package comparison, not "
                    "human approval of identities, relations, or claims."
                ),
            }
        )
    return {
        "analysis": analysis,
        "metrics": current_metrics,
        "metric_delta": metric_delta,
        "actor_delta": actor_delta,
        "asset_comparison": asset_comparison,
    }


def build_h3_outputs(
    h3v1: Any,
    h3v2: Any,
    data: Mapping[str, Any],
) -> dict[str, Any]:
    current_counts, current_actors, current_reviewed = (
        h3v1.current_actor_issue_metrics(data["edges"])
    )
    old_manifest = read_json(H3_V1_DIR / "manifest.json")
    old_counts = old_manifest["current_actor_issue_counts"]
    old_actors = old_manifest["current_actor_issue_actor_ids"]
    old_reviewed = old_manifest["current_human_reviewed_edge_counts"]
    issue_rows: list[dict[str, Any]] = []
    for issue in h3v1.TARGET_ISSUES:
        old_actor_set = set(old_actors[issue])
        current_actor_set = set(current_actors[issue])
        issue_rows.append(
            {
                "issue_label": issue,
                "old_active_edge_count": old_counts[issue],
                "current_active_edge_count": current_counts[issue],
                "old_human_reviewed_edge_count": old_reviewed[issue],
                "current_human_reviewed_edge_count": current_reviewed[issue],
                "old_actor_ids": ";".join(sorted(old_actor_set)),
                "current_actor_ids": ";".join(sorted(current_actor_set)),
                "added_actor_ids": ";".join(
                    sorted(current_actor_set - old_actor_set)
                ),
                "removed_actor_ids": ";".join(
                    sorted(old_actor_set - current_actor_set)
                ),
                "compatibility_status": "recompute_required",
                "impact": "high",
                **PACKAGE_META,
                "interpretation_limit": (
                    "Schema-tag counts are a current coding snapshot and "
                    "cannot establish historical vocabulary growth, diffusion, "
                    "or durable mobilization."
                ),
            }
        )

    current_governance = h3v1.build_source_governance()
    old_governance = read_csv(H3_V1_DIR / "source_governance_v1.csv")
    governance_equal = canon_rows(current_governance) == canon_rows(
        old_governance
    )

    h3v2_manifest = read_json(H3_V2_DIR / "manifest.json")
    protected_old = {
        item["path"]: item["sha256"]
        for item in h3v2_manifest["protected_inputs"]
    }
    input_rows: list[dict[str, Any]] = []
    for path in h3v2.PROTECTED_INPUTS:
        key = relative(path)
        old_hash = protected_old.get(key, "")
        current_hash = sha256(path)
        same = old_hash == current_hash
        semantic_check = (
            "registry IDs/crosswalks checked separately"
            if path == ACTORS
            else "H3 v1 source rows unchanged"
            if path.parent == H3_V1_DIR
            else "source-governance rows checked separately"
            if path == SOURCES
            else "hash-only"
        )
        input_rows.append(
            {
                "package_id": "research_wave_h3_frontline_memory_v2",
                "input_path": key,
                "old_hash": old_hash,
                "current_hash": current_hash,
                "hash_status": "unchanged" if same else "changed",
                "semantic_check": semantic_check,
                "compatibility_status": (
                    "invariant"
                    if same
                    else "recompute_required"
                ),
                "impact": (
                    "low"
                    if path in {ACTORS, SOURCES}
                    else "none"
                ),
                **PACKAGE_META,
                "interpretation_limit": (
                    "A hash change requires a manifest refresh; it does not by "
                    "itself invalidate source-level observations."
                ),
            }
        )

    active_actor_ids = data["actor_ids"]
    h3v2_crosswalk_ids = {
        actor_id
        for row in (
            list(h3v2.NETWORK_PARTICIPATING_GROUPS)
            + list(h3v2.PETITION_ENDORSING_GROUPS)
        )
        for actor_id in [row[2]]
        if actor_id
    }
    missing_crosswalk_ids = sorted(h3v2_crosswalk_ids - active_actor_ids)
    a010_lifecycle = [
        row for row in read_csv(LIFECYCLE) if row["actor_id"] == "A010"
    ]
    metrics = {
        "as_of_date": AUDIT_DATE,
        "layer": PACKAGE_META,
        "target_issue_counts": current_counts,
        "target_issue_actor_ids": current_actors,
        "target_issue_human_reviewed_counts": current_reviewed,
        "h3v1_source_governance_content_equal": governance_equal,
        "h3v1_source_governance_blocker_count": sum(
            row["metadata_or_archive_correction_needed"] == "yes"
            for row in current_governance
        ),
        "h3v2_crosswalk_actor_id_count": len(h3v2_crosswalk_ids),
        "h3v2_missing_current_crosswalk_actor_ids": missing_crosswalk_ids,
        "h3v2_a010_lifecycle_row_count": len(a010_lifecycle),
        "h3v2_a010_central_gate": (
            "still_human_pending_no_central_lifecycle_row"
            if not a010_lifecycle
            else "central_lifecycle_row_now_exists_recheck_required"
        ),
        "h3v2_source_corpus_compatibility": (
            "invariant_source_level_rows; refresh protected input hashes and "
            "validate registry crosswalks in a versioned generator"
        ),
        "hard_boundary": (
            "No vocabulary-growth, diffusion-direction, independent-adoption, "
            "or stable-alliance upgrade is made by this compatibility audit."
        ),
    }
    return {
        "metrics": metrics,
        "issue_rows": issue_rows,
        "input_rows": input_rows,
        "governance_equal": governance_equal,
    }


def compatibility_overlay(
    h1: Mapping[str, Any],
    h2: Mapping[str, Any],
    h3: Mapping[str, Any],
) -> list[dict[str, Any]]:
    h2m = h2["metrics"]
    h3m = h3["metrics"]
    h1m = h1["metrics"]
    rows = [
        (
            "H1C01",
            "H1_v1_v2",
            "actor_issue_current_gate",
            "central actor-issue counts and connected actors",
            "238 active / 103 connected",
            "283 active / 116 connected",
            "recompute_required",
            "high",
            "All H1 degree, review-layer and graph-size denominators changed.",
            "Use the overlay; keep v1/v2 as historical snapshots.",
        ),
        (
            "H1C02",
            "H1_v1_v2",
            "review_layer_split",
            "reviewed versus candidate actor-issue edges",
            "65 reviewed / 173 candidate",
            "125 reviewed / 158 candidate",
            "recompute_required",
            "high",
            "The human-review selection layer changed materially.",
            "Generate dynamic layer labels in H1 v3.",
        ),
        (
            "H1C03",
            "H1_v1_v2",
            "source_dependency_s004",
            "E3/E4 S004 support deletion",
            "234 baseline; 41 removed; 25 fully lost",
            (
                f"{h1m['s004_support_deletion']['baseline_edges']} baseline; "
                f"{h1m['s004_support_deletion']['removed_edges']} removed; "
                f"{h1m['s004_support_deletion']['incident_actor_count']} "
                "incident; "
                f"{h1m['s004_support_deletion']['fully_lost_actor_count']} "
                "fully lost"
            ),
            "recompute_required",
            "high",
            "Edge loss and actor incidence must be kept separate.",
            "Use current source-dependency and scenario tables.",
        ),
        (
            "H1C04",
            "H1_v1_v2",
            "method_literature_and_noninference",
            "method references and source/actor deletion boundary",
            "fixed",
            "unchanged",
            "invariant",
            "none",
            "No central count is embedded in the non-inference rule.",
            "Carry forward unchanged.",
        ),
        (
            "H1C05",
            "H1_v2",
            "strict_triple_graph_object",
            "same-source actor-place-issue triples",
            "312 rows",
            "305 rows; 298 E3/E4; 71 dual-reviewed; 97 event-attached",
            "recompute_required",
            "medium",
            "The graph-object denominator and input hash changed.",
            "Refresh H1 graph-object table in v3.",
        ),
        (
            "H2C01",
            "H2_two_ecologies_v1",
            "service_core",
            "registry-defined service comparison subset",
            "9 actors / 11 issue edges",
            (
                f"{h2m['service_core_actor_count']} actors / "
                f"{h2m['service_active_issue_edge_count']} issue edges"
            ),
            "invariant",
            "none",
            "The service-core rule and its issue rows are byte-equivalent.",
            "Retain as a bounded registry subset, not a census.",
        ),
        (
            "H2C02",
            "H2_two_ecologies_v1",
            "accountability_comparison",
            "anchor-selected comparison actors",
            "65 total / 18 reviewed-anchor / 47 candidate-only",
            (
                f"{h2m['accountability_comparison_actor_count']} total / "
                f"{h2m['accountability_human_reviewed_anchor_actor_count']} "
                "reviewed-anchor / "
                f"{h2m['accountability_candidate_only_anchor_actor_count']} "
                "candidate-only"
            ),
            "recompute_required",
            "high",
            "Twelve actors entered through newly active anchor edges.",
            "Issue H2 v2 with a new comparison table; do not overwrite v1.",
        ),
        (
            "H2C03",
            "H2_two_ecologies_v1",
            "encoded_cross_ecology_relations",
            "typed dyadic/event/R10 bounded inputs",
            "0 direct encoded cross-group organization relations",
            (
                f"{h2m['cross_ecology_dyadic_observed_count']} dyadic / "
                f"{h2m['cross_ecology_event_observed_count']} event / "
                f"{h2m['r10_cross_ecology_observed_count']} R10"
            ),
            "invariant",
            "low",
            (
                "The bounded relation observation remains zero after the "
                "comparison-set recomputation."
            ),
            (
                "Keep the wording 'unencoded in bounded inputs'; do not infer "
                "no shared people or no relation."
            ),
        ),
        (
            "H2C04",
            "H2_service_universe_v1",
            "official_directory_and_person_rows",
            "source-defined service universe and person-role observations",
            "82 PO rows / 55 person-role rows",
            "unchanged source-bound research rows",
            "invariant",
            "none",
            "These rows do not derive from the actor-issue review split.",
            "Preserve as a separate research-only input.",
        ),
        (
            "H2C05",
            "H2_service_universe_v1",
            "accountability_reverse_search_coverage",
            "bounded nonrandom search denominator",
            "18 nonrandom accountability anchors",
            (
                f"18 searched anchors versus current "
                f"{h2m['accountability_comparison_actor_count']}-actor "
                "comparison set"
            ),
            "not_comparable",
            "medium",
            "The search was deliberately bounded and is not a full denominator.",
            "Do not relabel 18 searches as coverage of the current group.",
        ),
        (
            "H2C06",
            "H2_recipient_permeability_v1",
            "recipient_and_co_mention_package",
            "source-defined recipients plus bounded search denominator",
            "fixed recipient rows plus 18 nonrandom searches",
            "recipient rows invariant; current-group coverage not comparable",
            "not_comparable",
            "medium",
            "Recipient observations remain valid candidates, but the search is not symmetric or closed.",
            "Keep recipient rows; version any expanded search separately.",
        ),
        (
            "H3C01",
            "H3_frontline_memory_v1",
            "target_issue_snapshot",
            "central actor-issue tag counts",
            "frontline=4 / Taiwan=4 / anti_war=1",
            (
                "frontline="
                f"{h3m['target_issue_counts']['frontline_prevention']} / "
                "Taiwan="
                f"{h3m['target_issue_counts']['Taiwan_contingency']} / "
                f"anti_war={h3m['target_issue_counts']['anti_war']}"
            ),
            "recompute_required",
            "high",
            "HR-010 added reviewed edges and actors in all three tags.",
            "Use current issue snapshot; do not infer vocabulary growth.",
        ),
        (
            "H3C02",
            "H3_frontline_memory_v1",
            "source_observations_carriers_participants",
            "source/event-bounded research rows",
            "12 observations / 6 carriers / 17 participant candidates",
            "unchanged source-level rows",
            "invariant",
            "none",
            "The rows are source/event bounded and do not derive from current tag totals.",
            "Retain with original candidate gates.",
        ),
        (
            "H3C03",
            "H3_frontline_memory_v1",
            "source_governance",
            "six selected source-log/archive rows",
            "3 correction/reconciliation blockers",
            (
                f"{h3m['h3v1_source_governance_blocker_count']} blockers; "
                "row content unchanged"
            ),
            "invariant",
            "low",
            "Relevant six source-governance rows are unchanged despite the whole source-log hash changing.",
            "Refresh manifest hash only in a versioned package.",
        ),
        (
            "H3C04",
            "H3_frontline_memory_v2",
            "common_document_corpus_and_rosters",
            "source-defined corpus and event rosters",
            "28 corpus / 35 participating / 35 endorsing",
            "unchanged source-level package counts",
            "invariant",
            "none",
            "The v2 corpus is source-defined rather than central-count-defined.",
            "Keep v2 as the source-level evidence snapshot.",
        ),
        (
            "H3C05",
            "H3_frontline_memory_v2",
            "protected_input_manifest",
            "input hashes and registry/source-log compatibility",
            "old registry/source-log hashes",
            "registry/source-log hashes changed; v1 row inputs unchanged",
            "recompute_required",
            "low",
            "The manifest is stale even though current crosswalk IDs still resolve.",
            "Refresh hashes and add dynamic registry/lifecycle validation in H3 v3.",
        ),
        (
            "H3C06",
            "H3_frontline_memory_v2",
            "vocabulary_growth_or_diffusion",
            "historically unmatched text/adoption inference",
            "not established",
            "still not established",
            "not_comparable",
            "none",
            "More coded tags are not a matched historical text corpus.",
            "No interpretation upgrade.",
        ),
    ]
    return [
        {
            "compatibility_id": row[0],
            "package_id": row[1],
            "component": row[2],
            "dependency_type": row[3],
            "old_snapshot": row[4],
            "current_snapshot": row[5],
            "compatibility_status": row[6],
            "impact": row[7],
            "reason": row[8],
            "required_action": row[9],
            **PACKAGE_META,
            "interpretation_limit": (
                "Compatibility classification only; no fact, relation, or "
                "interpretive claim is promoted."
            ),
        }
        for row in rows
    ]


def marker_occurrences() -> list[dict[str, Any]]:
    scopes = [
        H1_V1_DIR,
        H1_V2_DIR,
        H2_V1_DIR,
        H3_V1_DIR,
        H3_V2_DIR,
        TOPIC_DIR,
        H1_V1_SCRIPT,
        H1_V2_SCRIPT,
        H2_V1_SCRIPT,
        H3_V1_SCRIPT,
        ROOT / "tests" / "test_make_h1_documentation_visibility_v1.py",
        ROOT / "tests" / "test_make_h1_documentation_visibility_v2.py",
        ROOT / "tests" / "test_make_h2_two_ecologies_v1.py",
        ROOT / "tests" / "test_make_h3_frontline_memory_v1.py",
        ROOT / "docs" / "research_wave_topic_selection_v1.md",
        ROOT / "docs" / "research_wave_v1_handoff.md",
        ROOT / "docs" / "research_wave_v2_principal_checkpoint.md",
    ]
    patterns = [
        (
            "h1_old_layer_id",
            re.compile(r"\b(?:active_238|reviewed_65|candidate_173)\b"),
        ),
        (
            "h1_old_split_phrase",
            re.compile(
                r"(?:238\s+(?:active|条)|65\s+(?:reviewed|条\s*reviewed)|"
                r"173\s+(?:candidate|条\s*candidate)|"
                r"已核\s*65|候选\s*173|238/65/173)"
            ),
        ),
        (
            "h1_old_e3plus_or_triple",
            re.compile(
                r"(?:234\s+条\s*E3/E4|"
                r'"e3plus_actor_issue_edges"\s*:\s*234|'
                r'"strict_triples"\s*:\s*312)'
            ),
        ),
        (
            "h2_old_group_phrase",
            re.compile(
                r"(?:65\s*个(?:问责|限制)|"
                r"18\s*个(?:至少有一条人审|人审锚点)|"
                r"47\s*个(?:只由候选|仅有候选|候选锚点)|"
                r'"accountability_comparison_actor_count"\s*:\s*65)'
            ),
        ),
        (
            "h3_old_target_metric",
            re.compile(
                r'(?:"frontline_prevention"\s*:\s*4|'
                r'"Taiwan_contingency"\s*:\s*4|'
                r'"anti_war"\s*:\s*1)'
            ),
        ),
        (
            "old_actor_registry_hash",
            re.compile(
                r"03653fe12665abc754ef09d9d30e76c6e53dd495eaceba0fef4bc5ce5540b0a3"
            ),
        ),
        (
            "old_actor_issue_hash",
            re.compile(
                r"61302c3bfbd42df53a3679c1dc41fe4247376598d8ab7220839cc326e30b8cbe"
            ),
        ),
        (
            "old_strict_triple_hash",
            re.compile(
                r"a13bb162cd1f855c9a3db38f7875cb59081d4cbd989c9325d9d6592510d8c7ec"
            ),
        ),
        (
            "old_source_log_hash",
            re.compile(
                r"ea5c34a2785cfede7f8eedc0420c56968c17fdca112b38d168ec5df5a87ee3a4"
            ),
        ),
    ]
    paths: list[Path] = []
    for scope in scopes:
        if scope.is_file():
            paths.append(scope)
        elif scope.is_dir():
            paths.extend(
                path
                for path in scope.rglob("*")
                if path.is_file()
                and path.suffix.lower()
                in {".md", ".json", ".csv", ".svg", ".html", ".py"}
            )
    rows: list[dict[str, Any]] = []
    index = 1
    for path in sorted(set(paths)):
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        for line_number, line in enumerate(text.splitlines(), 1):
            for marker_id, pattern in patterns:
                if pattern.search(line):
                    rows.append(
                        {
                            "occurrence_id": f"SM{index:04d}",
                            "asset": relative(path),
                            "marker_id": marker_id,
                            "line_number": line_number,
                            "excerpt": line.strip()[:320],
                            "mechanical_status": "stale_marker_found",
                            "manual_context_rule": (
                                "Historical snapshots may retain old values; "
                                "they must not be presented as current."
                            ),
                            **PACKAGE_META,
                            "interpretation_limit": (
                                "String occurrence identifies a compatibility "
                                "risk, not a substantive research error."
                            ),
                        }
                    )
                    index += 1
    return rows


def stale_asset_inventory(
    h2_asset_comparison: Sequence[Mapping[str, Any]],
    occurrences: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    inventory: dict[str, dict[str, Any]] = {}

    def add(
        path: Path,
        package: str,
        asset_kind: str,
        status: str,
        impact: str,
        reason: str,
        action: str,
    ) -> None:
        inventory[relative(path)] = {
            "asset": relative(path),
            "package_id": package,
            "asset_kind": asset_kind,
            "compatibility_status": status,
            "impact": impact,
            "reason": reason,
            "required_action": action,
            **PACKAGE_META,
            "interpretation_limit": (
                "Inventory status concerns current-count compatibility only; "
                "historical provenance remains valid."
            ),
        }

    for filename in (
        "metrics_v1.json",
        "sensitivity_scenarios_v1.csv",
        "scenario_removed_edges_v1.csv",
        "leave_one_source_out_v1.csv",
        "paired_deletion_comparison_v1.csv",
        "actor_visibility_diagnostics_v1.csv",
        "actor_issue_edge_source_incidence_v1.csv",
        "brief_v1.md",
        "validation_report.md",
    ):
        add(
            H1_V1_DIR / filename,
            "H1_v1",
            "metric_or_analysis_asset",
            "recompute_required",
            "high",
            "Depends on the 238-edge / 234-E3+ snapshot.",
            "Use post-freeze overlay; do not overwrite v1.",
        )
    add(
        H1_V1_SCRIPT,
        "H1_v1",
        "generator",
        "recompute_required",
        "high",
        "Hard-coded validation expects 238 active edges.",
        "Create H1 v3 with dynamic count labels and validators.",
    )
    add(
        ROOT / "tests" / "test_make_h1_documentation_visibility_v1.py",
        "H1_v1",
        "test",
        "recompute_required",
        "high",
        "Assertions encode the historical 238/234 scenario.",
        "Keep as provenance or replace with versioned current tests.",
    )

    h1v2_files = [
        "metrics_v2.json",
        "actor_documentation_visibility_v2.csv",
        "association_estimates_v2.csv",
        "review_layer_sensitivity_v2.csv",
        "stratified_associations_v2.csv",
        "matched_actor_pairs_v2.csv",
        "matched_pair_summary_v2.csv",
        "negative_case_audit_v2.csv",
        "source_dependency_v2.csv",
        "sensitivity_scenarios_v2.csv",
        "graph_object_summary_v2.csv",
        "source_feature_audit_v2.csv",
        "unresolved_reference_audit_v2.csv",
        "method_brief_v2.md",
        "principal_checkpoint_v2.md",
        "validation_report_v2.md",
        "fig_graph_objects_v2.svg",
        "fig_graph_objects_v2.html",
        "fig_actor_issue_strata_v2.svg",
        "fig_actor_issue_strata_v2.html",
        "fig_actor_issue_sensitivity_v2.svg",
        "fig_actor_issue_sensitivity_v2.html",
    ]
    for filename in h1v2_files:
        add(
            H1_V2_DIR / filename,
            "H1_v2",
            (
                "figure"
                if filename.endswith((".svg", ".html"))
                else "metric_or_analysis_asset"
            ),
            "recompute_required",
            "high" if "actor_issue" in filename or "metrics" in filename else "medium",
            "Uses old actor-issue/review/triple counts or stale input hashes.",
            "Regenerate only as a new H1 v3 package.",
        )
    add(
        H1_V2_SCRIPT,
        "H1_v2",
        "generator",
        "recompute_required",
        "high",
        "Hard-coded 238/65/173/312 labels and validation gates remain.",
        "Version the generator; do not patch historical v2 outputs in place.",
    )
    add(
        ROOT / "tests" / "test_make_h1_documentation_visibility_v2.py",
        "H1_v2",
        "test",
        "recompute_required",
        "high",
        "Assertions and SVG text checks encode 238/65/173/234/312.",
        "Add current-version tests rather than rewriting provenance tests.",
    )

    for row in h2_asset_comparison:
        if row["compatibility_status"] == "recompute_required":
            path = ROOT / row["asset"]
            add(
                path,
                "H2_two_ecologies_v1",
                "analysis_table",
                "recompute_required",
                str(row["impact"]),
                "Row-level output differs under the current anchor-selected group.",
                "Emit a versioned H2 v2 table.",
            )
    for filename in (
        "metrics_v1.json",
        "manifest.json",
        "H2_two_ecologies_brief_v1.md",
        "README.md",
    ):
        add(
            H2_V1_DIR / filename,
            "H2_two_ecologies_v1",
            "metric_or_documentation_asset",
            "recompute_required",
            "high",
            "Still reports the 65/18/47 accountability comparison.",
            "Generate H2 v2; retain v1 unchanged.",
        )
    add(
        H2_V1_SCRIPT,
        "H2_two_ecologies_v1",
        "generator",
        "recompute_required",
        "medium",
        "Analysis is dynamic, but rendered brief text hard-codes 65/18/47.",
        "Move all rendered counts to current metrics in H2 v2.",
    )
    add(
        ROOT / "tests" / "test_make_h2_two_ecologies_v1.py",
        "H2_two_ecologies_v1",
        "test",
        "recompute_required",
        "high",
        "Assertions and brief checks encode 65/18/47.",
        "Keep provenance test or issue H2 v2 tests.",
    )
    add(
        H2_SERVICE_DIR / "accountability_reverse_interface_search_v1.csv",
        "H2_service_universe_v1",
        "bounded_search_asset",
        "not_comparable",
        "medium",
        "Eighteen nonrandom searches are not a full current 77-actor denominator.",
        "Retain rows; version any expanded search.",
    )
    add(
        H2_RECIPIENT_DIR / "accountability_limited_co_mention_search_v2.csv",
        "H2_recipient_permeability_v1",
        "bounded_search_asset",
        "not_comparable",
        "medium",
        "The bounded 18-anchor search is not symmetric or closed.",
        "Do not relabel it as current-group coverage.",
    )

    for filename in ("manifest.json", "brief_v1.md"):
        add(
            H3_V1_DIR / filename,
            "H3_frontline_memory_v1",
            "metric_or_documentation_asset",
            "recompute_required",
            "high",
            "Reports the old 4/4/1 target-tag snapshot.",
            "Use current H3 issue overlay; preserve v1 source rows.",
        )
    add(
        ROOT / "tests" / "test_make_h3_frontline_memory_v1.py",
        "H3_frontline_memory_v1",
        "test",
        "recompute_required",
        "high",
        "Assertions encode target-tag counts 4/4/1.",
        "Create versioned current-snapshot tests.",
    )
    add(
        H3_V2_DIR / "manifest.json",
        "H3_frontline_memory_v2",
        "manifest",
        "recompute_required",
        "low",
        "Protected registry and source-log hashes no longer match current files.",
        "Refresh hashes only in H3 v3; source-level rows remain historical.",
    )
    add(
        TOPIC_DIR / "frontend_research_modules_v1.json",
        "research_wave_topic_selection_v1",
        "module_index",
        "recompute_required",
        "high",
        "Carries H1 234/185 and H2 65/18/47 snapshot metrics.",
        "Do not expose; issue a versioned module index after interpretation gates.",
    )
    for path in (
        ROOT / "docs" / "research_wave_topic_selection_v1.md",
        ROOT / "docs" / "research_wave_v1_handoff.md",
        ROOT / "docs" / "research_wave_v2_principal_checkpoint.md",
    ):
        add(
            path,
            "research_wave_historical_communication",
            "documentation",
            "recompute_required",
            "medium",
            "Contains historical H1/H2 count statements.",
            "Cite as historical or accompany with this overlay.",
        )

    occurrence_assets = {row["asset"] for row in occurrences}
    for asset in sorted(occurrence_assets):
        if asset not in inventory:
            add(
                ROOT / asset,
                "mechanical_marker_scan",
                "text_asset",
                "recompute_required",
                "medium",
                "High-confidence old snapshot marker found mechanically.",
                "Review against the compatibility overlay before reuse.",
            )
    return [inventory[key] for key in sorted(inventory)]


def generator_recommendations() -> list[dict[str, Any]]:
    rows = [
        (
            "GEN01",
            "H1_v3",
            "scripts/make_h1_documentation_visibility_v3.py",
            "Read current central actor/issue/triple inputs; derive labels and validators from counts; preserve source versus actor deletion units.",
            "New v3 output only; no overwrite of H1 v1/v2.",
            "high",
        ),
        (
            "GEN02",
            "H2_v2",
            "scripts/make_h2_two_ecologies_v2.py",
            "Rebuild the 77-actor accountability comparison and every dependent row; render brief from metrics; keep service/recipient packages separate.",
            "No people/recipient relation promotion and no political-stance inference.",
            "high",
        ),
        (
            "GEN03",
            "H3_v3",
            "scripts/make_h3_frontline_memory_v3.py",
            "Carry forward v2 source corpus; add dynamic current tag snapshot, registry ID validation, lifecycle gate checks and refreshed hashes.",
            "Tag changes remain non-comparable for vocabulary growth.",
            "medium",
        ),
        (
            "GEN04",
            "topic_selection_v2",
            "outputs/research_wave_topic_selection_v2/",
            "Consume versioned H1/H2/H3 manifests and this compatibility overlay; keep modules research_only/not_frontend_ready.",
            "Do not update the frontend module contract before principal evidence reading.",
            "medium",
        ),
    ]
    return [
        {
            "recommendation_id": row[0],
            "target_version": row[1],
            "suggested_generator_or_output": row[2],
            "required_change": row[3],
            "hard_boundary": row[4],
            "priority": row[5],
            "status": "recommendation_only",
            **PACKAGE_META,
            "interpretation_limit": (
                "A generator recommendation is not authorization to run a new "
                "research wave or write to central data."
            ),
        }
        for row in rows
    ]


def render_readme(
    snapshot: Mapping[str, Any],
    h1: Mapping[str, Any],
    h2: Mapping[str, Any],
    h3: Mapping[str, Any],
) -> str:
    h1m = h1["metrics"]
    h2m = h2["metrics"]
    h3m = h3["metrics"]
    return f"""# 冻结后 H1／H2／H3 兼容性复算 v1

日期：{AUDIT_DATE}
状态：`research_only / candidate_analysis / not_frontend_ready / central_writeback=no`

本包不覆盖 H1/H2/H3 既有研究包。它只给历史快照加一层冻结后兼容 overlay。

## 当前机械基线

- Registry：{snapshot['actor_registry']['history_rows']} 历史／{snapshot['actor_registry']['current_actors']} current。
- Actor–issue：{snapshot['actor_issue']['active_edges']} active＝{snapshot['actor_issue']['reviewed_edges']} reviewed＋{snapshot['actor_issue']['candidate_edges']} candidate；{snapshot['actor_issue']['connected_actors']} connected＋{snapshot['actor_issue']['isolated_current_actors']} isolated。
- E3/E4：{snapshot['actor_issue']['e3plus_edges']} 边／{snapshot['actor_issue']['e3plus_connected_actors']} actor；其中 reviewed {snapshot['actor_issue']['e3plus_reviewed_edges']} 边／{snapshot['actor_issue']['e3plus_reviewed_actors']} actor，candidate {snapshot['actor_issue']['e3plus_candidate_edges']}／{snapshot['actor_issue']['e3plus_candidate_actors']}。
- Strict triple：{snapshot['strict_place_issue']['active_same_source_triples']} 总数／{snapshot['strict_place_issue']['e3plus_triples']} E3/E4／{snapshot['strict_place_issue']['dual_human_reviewed_triples']} dual-reviewed／{snapshot['strict_place_issue']['event_attached_triples']} event-attached。

## H1

旧 H1 的 `238/65/173`、234 条 E3/E4 和 312 strict triples 都必须视为历史快照。
当前 E3/E4 删除仅由 S004 可解析支持的 {h1m['s004_support_deletion']['removed_edges']} 条边后，
保留 {h1m['s004_support_deletion']['remaining_edges']} 条／{h1m['s004_support_deletion']['remaining_observed_actors']} actor。

必须区分两个分母：

- {h1m['s004_support_deletion']['incident_actor_count']} 个 actor 至少碰到一条被删边；
- 其中 {h1m['s004_support_deletion']['fully_lost_actor_count']} 个 actor 失去全部 E3/E4 边。

S003/S004/S006 合计删除 {h1m['big3_support_deletion']['removed_edges']} 条，S004 占
{h1m['big3_support_deletion']['s004_share_of_big3_removed_edges']:.1%}。这仍只描述当前编码支持集中，
不证明真实网络中心性或组织能力。

## H2

服务侧 registry 子集仍为 {h2m['service_core_actor_count']} 个 actor。问责侧按同一锚点规则由
65 扩至 {h2m['accountability_comparison_actor_count']} 个，其中
{h2m['accountability_human_reviewed_anchor_actor_count']} 个有 reviewed anchor，
{h2m['accountability_candidate_only_anchor_actor_count']} 个仅有 candidate anchor。
当前有界 typed-dyadic／event／R10 输入中的直接跨组组织关系仍为
{h2m['cross_ecology_dyadic_observed_count']}/
{h2m['cross_ecology_event_observed_count']}/
{h2m['r10_cross_ecology_observed_count']}；只能写“当前有界输入未编码”，不能写“没有共享人员”。

服务 universe 与 recipient 包的来源行仍可使用，但两个 18-anchor 搜索不是当前
{h2m['accountability_comparison_actor_count']}-actor 比较组的完整分母，状态为 `not_comparable`。

## H3

中央 tag snapshot 由 `4/4/1` 变为：

- `frontline_prevention={h3m['target_issue_counts']['frontline_prevention']}`；
- `Taiwan_contingency={h3m['target_issue_counts']['Taiwan_contingency']}`；
- `anti_war={h3m['target_issue_counts']['anti_war']}`。

H3 v1 的来源观察／载体／参与候选和 H3 v2 的共同文件语料保持 source-level invariant；
旧 manifest 的 registry/source-log hash 需要刷新。标签增加仍不能证明历史词汇增长、
传播方向、独立采用或持续共同动员。

## 复现

```powershell
python scripts\\make_research_wave_postfreeze_compatibility_v1.py
python -m unittest tests.test_make_research_wave_postfreeze_compatibility_v1
```

## 阅读顺序

1. `package_compatibility_overlay_v1.csv`
2. `stale_asset_inventory_v1.csv`
3. `h1_recomputed_metrics_v1.json`
4. `h2_recomputed_metrics_v1.json`
5. `h3_recomputed_metrics_v1.json`
6. `next_generator_recommendations_v1.csv`
7. `handoff_v1.md`

本包不进入中央表，不进入前端，不升级任何解释性命题。
"""


def render_handoff(
    snapshot: Mapping[str, Any],
    overlay: Sequence[Mapping[str, Any]],
    inventory: Sequence[Mapping[str, Any]],
    occurrences: Sequence[Mapping[str, Any]],
) -> str:
    status_counts = Counter(row["compatibility_status"] for row in overlay)
    return f"""# H1／H2／H3 冻结后兼容性复算换手

日期：{AUDIT_DATE}

## 完成

- 中央基线锁定为 actor–issue {snapshot['actor_issue']['active_edges']} active／
  {snapshot['actor_issue']['reviewed_edges']} reviewed／
  {snapshot['actor_issue']['candidate_edges']} candidate；
  strict triples {snapshot['strict_place_issue']['active_same_source_triples']}。
- 兼容判定 {len(overlay)} 项：
  `invariant={status_counts['invariant']}`、
  `recompute_required={status_counts['recompute_required']}`、
  `not_comparable={status_counts['not_comparable']}`。
- 识别 {len(inventory)} 个需版本化处理或限定使用的资产，
  {len(occurrences)} 个高置信旧快照字符串位置。
- H1 当前来源依赖／审核层／actor 计数已复算；
  H2 当前比较组与逐资产变化已复算；
  H3 当前目标 tag 与输入 hash／source-governance 已复核。

## 关键边界

- 既有 H1/H2/H3 目录均未改动，它们仍是历史 provenance snapshot。
- `invariant` 只表示对本次冻结变化不敏感，不等于人工确认或 publication-ready。
- `not_comparable` 表示原任务分母不同，不能用新总数给旧搜索补一个覆盖率。
- S004 的 25 个受影响 actor 与 24 个完全掉出 E3/E4 层 actor 已明确分列。
- H2 的跨组关系仍只是在有界输入中未编码；人物、完整 recipient 与非公开接触仍不完整。
- H3 的 tag 增加不构成词汇增长或扩散证据。

## 建议接手

1. H1 新建 v3 generator，删除硬编码计数与图中文字。
2. H2 新建 v2 generator，重生 77-actor 比较组及所有依赖表；recipient/service 包保持独立。
3. H3 新建 v3 manifest/crosswalk 层；保留 v2 共同文件语料，不升级解释。
4. 负责人分别阅读 H2/H3 原文后，再决定是否启动更深研究；本包不替代解释检查点。

## 禁止误读

- 本包不是新的中央事实层、人工复核结果或前端数据契约。
- 不得用本包把 candidate 边提升为已核边。
- 不得静默覆盖旧包、旧图、旧测试或历史沟通材料。
"""


def validate(
    snapshot: Mapping[str, Any],
    h1: Mapping[str, Any],
    h2: Mapping[str, Any],
    h3: Mapping[str, Any],
    overlay: Sequence[Mapping[str, Any]],
    inventory: Sequence[Mapping[str, Any]],
    occurrences: Sequence[Mapping[str, Any]],
    protected_package_rows: Sequence[Mapping[str, Any]],
) -> list[str]:
    checks: list[str] = []
    if snapshot["actor_registry"] != {
        "history_rows": 122,
        "current_actors": 121,
    }:
        raise ValueError("actor registry gate drifted")
    checks.append("actor registry = 122 history / 121 current")
    ai = snapshot["actor_issue"]
    expected_ai = {
        "history_rows": 294,
        "active_edges": 283,
        "reviewed_edges": 125,
        "candidate_edges": 158,
        "connected_actors": 116,
        "isolated_current_actors": 5,
        "e3plus_edges": 271,
        "e3plus_connected_actors": 114,
        "e3plus_reviewed_edges": 117,
        "e3plus_reviewed_actors": 47,
        "e3plus_candidate_edges": 154,
        "e3plus_candidate_actors": 76,
    }
    for key, value in expected_ai.items():
        if ai[key] != value:
            raise ValueError(
                f"actor-issue gate {key}: expected {value}, got {ai[key]}"
            )
    checks.append(
        "actor-issue = 294 history / 283 active / 125 reviewed / 158 candidate"
    )
    expected_strict = {
        "active_same_source_triples": 305,
        "e3plus_triples": 298,
        "dual_human_reviewed_triples": 71,
        "event_attached_triples": 97,
    }
    if snapshot["strict_place_issue"] != expected_strict:
        raise ValueError(
            f"strict triple gate drifted: {snapshot['strict_place_issue']}"
        )
    checks.append("strict triples = 305 / 298 E3+ / 71 dual / 97 event")

    s004 = h1["metrics"]["s004_support_deletion"]
    expected_s004 = {
        "baseline_edges": 271,
        "baseline_observed_actors": 114,
        "removed_edges": 40,
        "incident_actor_count": 25,
        "fully_lost_actor_count": 24,
        "remaining_edges": 231,
        "remaining_observed_actors": 90,
    }
    for key, value in expected_s004.items():
        if s004[key] != value:
            raise ValueError(
                f"S004 gate {key}: expected {value}, got {s004[key]}"
            )
    checks.append(
        "S004 deletion = 40 edges / 25 incident actors / 24 fully lost / 231 edges / 90 actors remain"
    )
    h2m = h2["metrics"]
    for key, value in {
        "service_core_actor_count": 9,
        "accountability_comparison_actor_count": 77,
        "accountability_human_reviewed_anchor_actor_count": 35,
        "accountability_candidate_only_anchor_actor_count": 42,
        "accountability_active_issue_edge_count": 231,
        "cross_ecology_dyadic_observed_count": 0,
        "cross_ecology_event_observed_count": 0,
        "r10_cross_ecology_observed_count": 0,
    }.items():
        if h2m[key] != value:
            raise ValueError(f"H2 gate {key}: {h2m[key]} != {value}")
    checks.append("H2 comparison = 9 service / 77 accountability / 35+42")
    h3m = h3["metrics"]
    if h3m["target_issue_counts"] != {
        "frontline_prevention": 6,
        "Taiwan_contingency": 6,
        "anti_war": 5,
    }:
        raise ValueError("H3 target issue count gate drifted")
    if h3m["target_issue_human_reviewed_counts"] != {
        "frontline_prevention": 3,
        "Taiwan_contingency": 3,
        "anti_war": 5,
    }:
        raise ValueError("H3 reviewed target issue gate drifted")
    if h3m["h3v2_missing_current_crosswalk_actor_ids"]:
        raise ValueError("H3 v2 crosswalk points to missing current actor")
    if h3m["h3v2_a010_central_gate"] != (
        "still_human_pending_no_central_lifecycle_row"
    ):
        raise ValueError("H3 A010 lifecycle gate changed")
    checks.append("H3 target tags = 6/6/5; reviewed = 3/3/5")
    allowed = {"invariant", "recompute_required", "not_comparable"}
    if {row["compatibility_status"] for row in overlay} - allowed:
        raise ValueError("unknown compatibility status")
    if any(
        row["research_status"] != "research_only"
        or row["frontend_eligibility"] != "not_frontend_ready"
        or row["central_writeback"] != "no"
        for collection in (overlay, inventory, occurrences)
        for row in collection
    ):
        raise ValueError("research-only gate failed")
    checks.append("all overlay/inventory/marker rows are research_only")
    if not occurrences:
        raise ValueError("stale marker scan unexpectedly empty")
    checks.append(f"stale marker scan = {len(occurrences)} occurrences")
    if not any(
        row["asset"].endswith(
            "tests/test_make_h1_documentation_visibility_v2.py"
        )
        for row in inventory
    ):
        raise ValueError("stale H1 v2 test missing from inventory")
    checks.append(f"stale/not-comparable inventory = {len(inventory)} assets")
    if any(
        row["unchanged_during_build"] != "yes"
        for row in protected_package_rows
    ):
        raise ValueError("a protected historical package changed during build")
    checks.append(
        f"protected historical package trees unchanged = "
        f"{len(protected_package_rows)}/{len(protected_package_rows)}"
    )
    return checks


def output_manifest(inputs: Sequence[Path]) -> dict[str, Any]:
    output_files = [
        path
        for path in OUT.iterdir()
        if path.is_file() and path.name != "manifest.json"
    ]
    return {
        "package_id": "research_wave_postfreeze_compatibility_v1",
        "as_of_date": AUDIT_DATE,
        "layer": PACKAGE_META,
        "input_hashes": {
            relative(path): sha256(path) for path in sorted(set(inputs))
        },
        "output_hashes": {
            path.name: sha256(path) for path in sorted(output_files)
        },
        "protected_historical_packages": [
            relative(path)
            for path in (
                H1_V1_DIR,
                H1_V2_DIR,
                H2_V1_DIR,
                H2_SERVICE_DIR,
                H2_RECIPIENT_DIR,
                H3_V1_DIR,
                H3_V2_DIR,
                TOPIC_DIR,
            )
        ],
        "central_writeback": False,
        "frontend_writeback": False,
        "interpretation_upgrade": False,
    }


def main() -> None:
    protected_directories = (
        H1_V1_DIR,
        H1_V2_DIR,
        H2_V1_DIR,
        H2_SERVICE_DIR,
        H2_RECIPIENT_DIR,
        H3_V1_DIR,
        H3_V2_DIR,
        TOPIC_DIR,
    )
    protected_before = {
        directory: tree_sha256(directory)
        for directory in protected_directories
    }
    h1 = import_script(H1_V2_SCRIPT, "compat_h1_v2")
    h2 = import_script(H2_V1_SCRIPT, "compat_h2_v1")
    h3v1 = import_script(H3_V1_SCRIPT, "compat_h3_v1")
    h3v2 = import_script(H3_V2_SCRIPT, "compat_h3_v2")

    data = current_inputs(h1)
    snapshot = current_snapshot(data)
    h1_outputs = build_h1_outputs(h1, data, snapshot)
    h2_outputs = build_h2_outputs(h2)
    h3_outputs = build_h3_outputs(h3v1, h3v2, data)
    overlay = compatibility_overlay(h1_outputs, h2_outputs, h3_outputs)
    occurrences = marker_occurrences()
    inventory = stale_asset_inventory(
        h2_outputs["asset_comparison"],
        occurrences,
    )
    recommendations = generator_recommendations()
    protected_package_rows = [
        {
            "package_path": relative(directory),
            "before_tree_sha256": protected_before[directory],
            "after_tree_sha256": tree_sha256(directory),
            "unchanged_during_build": (
                "yes"
                if protected_before[directory] == tree_sha256(directory)
                else "no"
            ),
            **PACKAGE_META,
            "interpretation_limit": (
                "Tree hash verifies read-only handling during this builder "
                "run; it does not approve historical package claims."
            ),
        }
        for directory in protected_directories
    ]
    checks = validate(
        snapshot,
        h1_outputs,
        h2_outputs,
        h3_outputs,
        overlay,
        inventory,
        occurrences,
        protected_package_rows,
    )

    OUT.mkdir(parents=True, exist_ok=True)
    write_json(OUT / "central_snapshot_v1.json", snapshot)
    write_csv(OUT / "package_compatibility_overlay_v1.csv", overlay)
    write_csv(OUT / "stale_asset_inventory_v1.csv", inventory)
    write_csv(OUT / "stale_marker_occurrences_v1.csv", occurrences)
    write_json(
        OUT / "h1_recomputed_metrics_v1.json",
        h1_outputs["metrics"],
    )
    write_csv(
        OUT / "h1_review_layer_sensitivity_v1.csv",
        h1_outputs["review_rows"],
    )
    write_csv(
        OUT / "h1_source_dependency_v1.csv",
        h1_outputs["source_dependency"],
    )
    write_csv(
        OUT / "h1_sensitivity_scenarios_v1.csv",
        h1_outputs["scenarios"],
    )
    write_csv(
        OUT / "h1_association_delta_v1.csv",
        h1_outputs["association_delta"],
    )
    write_json(
        OUT / "h2_recomputed_metrics_v1.json",
        h2_outputs["metrics"],
    )
    write_csv(
        OUT / "h2_metric_delta_v1.csv",
        h2_outputs["metric_delta"],
    )
    write_csv(
        OUT / "h2_accountability_actor_delta_v1.csv",
        h2_outputs["actor_delta"],
    )
    write_csv(
        OUT / "h2_asset_comparison_v1.csv",
        h2_outputs["asset_comparison"],
    )
    write_json(
        OUT / "h3_recomputed_metrics_v1.json",
        h3_outputs["metrics"],
    )
    write_csv(
        OUT / "h3_target_issue_snapshot_v1.csv",
        h3_outputs["issue_rows"],
    )
    write_csv(
        OUT / "h3_input_compatibility_v1.csv",
        h3_outputs["input_rows"],
    )
    write_csv(
        OUT / "next_generator_recommendations_v1.csv",
        recommendations,
    )
    write_csv(
        OUT / "protected_legacy_package_hashes_v1.csv",
        protected_package_rows,
    )
    (OUT / "README.md").write_text(
        render_readme(snapshot, h1_outputs, h2_outputs, h3_outputs),
        encoding="utf-8",
    )
    (OUT / "handoff_v1.md").write_text(
        render_handoff(snapshot, overlay, inventory, occurrences),
        encoding="utf-8",
    )
    (OUT / "validation_report_v1.md").write_text(
        "# Post-freeze H1/H2/H3 compatibility validation\n\n"
        + "\n".join(f"- PASS: {check}" for check in checks)
        + "\n- PASS: historical H1/H2/H3 packages were read-only inputs.\n"
        + "- PASS: no central-table or frontend writeback.\n"
        + "- PASS: no interpretive claim was upgraded.\n",
        encoding="utf-8",
    )
    manifest_inputs = [
        ACTORS,
        SOURCES,
        EDGES,
        TRIPLES,
        EVENTS,
        CASE_ROLES,
        LIFECYCLE,
        H1_V1_DIR / "metrics_v1.json",
        H1_V2_DIR / "metrics_v2.json",
        H2_V1_DIR / "metrics_v1.json",
        H2_V1_DIR / "manifest.json",
        H3_V1_DIR / "manifest.json",
        H3_V2_DIR / "manifest.json",
        H1_V1_SCRIPT,
        H1_V2_SCRIPT,
        H2_V1_SCRIPT,
        H3_V1_SCRIPT,
        H3_V2_SCRIPT,
    ]
    write_json(OUT / "manifest.json", output_manifest(manifest_inputs))
    print(
        "Post-freeze compatibility OK: "
        f"{len(overlay)} classifications; "
        f"{len(inventory)} stale/not-comparable assets; "
        f"{len(occurrences)} marker occurrences"
    )


if __name__ == "__main__":
    main()
