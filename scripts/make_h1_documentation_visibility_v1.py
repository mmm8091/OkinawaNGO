from __future__ import annotations

"""Build the H1 documentation-mediated visibility sensitivity package.

This is a research-only diagnostic.  It compares two interventions on the
current actor--issue evidence layer:

1. remove actor nodes A001/A004/A005 while retaining everybody else's stated
   source support; and
2. remove edges whose stated support is exhausted by S003/S004/S006.

The paired source/actor mapping is a research proposal, not an approved fact
about authorship, production, coordination, or influence.  Source removal
measures dependency of the *observed evidence layer*; it does not claim that an
organization, relationship, or activity disappears from the social world.
"""

import csv
import hashlib
import json
import math
from collections import Counter, defaultdict, deque
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "interim"
OUT = ROOT / "outputs" / "research_wave_h1_documentation_visibility_v1"

ACTORS_PATH = DATA / "01_actor_registry_initial_v0.csv"
SOURCES_PATH = DATA / "05_source_log_initial_v0.csv"
LAYERED_EDGES_PATH = DATA / "24_r01_r02_actor_issue_layered_v0.csv"

AUDIT_DATE = "2026-07-20"
E3PLUS = {"E3", "E4"}
RESEARCH_LIMIT = (
    "Research-only sensitivity of documented actor-issue visibility; it does "
    "not establish social-network centrality, alliance, influence, activity "
    "strength, organizational lifespan, or a causal documentation effect."
)

# The user-approved H1 audit asks for these pairings.  They remain proposals
# because the central source log does not encode producer/host/authorship roles.
SOURCE_HOST_PROPOSALS = (
    ("S003", "A005"),
    ("S004", "A004"),
    ("S006", "A001"),
)

FRAME_MAP = {
    "F1_base": {"anti_base", "anti_military", "Henoko"},
    "F2_ecology": {"environment", "biodiversity", "dugong", "groundwater"},
    "F3_life_health": {
        "life_safety",
        "health_risk",
        "noise",
        "base_community_welfare",
        "military_family_service",
    },
    "F4_autonomy": {"local_autonomy", "referendum"},
    "F5_legal": {"legal"},
    "F6_international": {
        "international_advocacy",
        "public_diplomacy",
        "international_cooperation",
    },
    "F7_frontline": {"frontline_prevention", "Taiwan_contingency", "anti_war"},
    "F8_rights_peace": {
        "women",
        "human_rights",
        "peace",
        "solidarity",
        "mobilization",
    },
}

SCENARIO_FIELDS = [
    "scenario_id",
    "scenario_label",
    "scenario_family",
    "paired_group",
    "dropped_source_ids",
    "dropped_actor_ids",
    "evidence_gate",
    "edge_count",
    "observed_actor_count",
    "remaining_registry_actor_count",
    "registry_isolated_actor_count",
    "issue_count",
    "cross_frame_actor_count",
    "ecology_international_bridge_count",
    "ecology_base_bridge_count",
    "legal_base_bridge_count",
    "component_count",
    "largest_component_actor_count",
    "largest_component_total_node_count",
    "edge_retention_pct",
    "actor_retention_pct",
    "retention_reference",
    "selection_rule",
    "source_host_mapping_status",
    "research_status",
    "display_tier",
    "claim_status",
    "review_status",
    "interpretation_limit",
]

PAIR_FIELDS = [
    "pair_id",
    "source_id",
    "actor_id",
    "source_scenario_id",
    "actor_scenario_id",
    "source_deletion_edge_count",
    "actor_deletion_edge_count",
    "additional_edge_loss_under_source_deletion",
    "source_deletion_observed_actor_count",
    "actor_deletion_observed_actor_count",
    "additional_actor_loss_under_source_deletion",
    "mapping_status",
    "producer_role_status",
    "self_produced_or_external",
    "source_language",
    "comparison_validity",
    "research_status",
    "display_tier",
    "claim_status",
    "review_status",
    "interpretation_limit",
]

INCIDENCE_FIELDS = [
    "incidence_id",
    "actor_id",
    "actor_name",
    "source_ref_token",
    "source_id",
    "source_title",
    "source_type",
    "source_year",
    "source_resolution_status",
    "incidence_basis",
    "proposed_host_role",
    "host_mapping_status",
    "producer_role_status",
    "self_produced_or_external",
    "source_language",
    "research_status",
    "display_tier",
    "claim_status",
    "review_status",
    "interpretation_limit",
]

PROPOSAL_FIELDS = [
    "proposal_id",
    "source_id",
    "source_title",
    "source_url",
    "proposed_host_actor_id",
    "proposed_host_actor_name",
    "proposed_host_role",
    "mapping_status",
    "proposal_basis",
    "producer_role_status",
    "self_produced_or_external",
    "source_language",
    "research_status",
    "display_tier",
    "claim_status",
    "review_status",
    "interpretation_limit",
]

ACTOR_DIAGNOSTIC_FIELDS = [
    "actor_id",
    "actor_name",
    "actor_class",
    "origin_type",
    "actor_review_status",
    "resolved_registry_source_ref_count",
    "unresolved_registry_source_ref_count",
    "active_issue_edge_count",
    "active_e3plus_issue_edge_count",
    "own_website_status",
    "english_material_capacity",
    "staff_capacity",
    "legal_support_capacity",
    "lifecycle_status_for_h1",
    "research_status",
    "display_tier",
    "claim_status",
    "review_status",
    "interpretation_limit",
]

EDGE_SOURCE_FIELDS = [
    "incidence_id",
    "edge_id",
    "actor_id",
    "issue_id",
    "issue_label",
    "evidence_level",
    "source_ref_token",
    "source_id",
    "source_resolution_status",
    "stated_support_ref_count",
    "removed_if_this_source_dropped_alone",
    "research_status",
    "display_tier",
    "claim_status",
    "review_status",
    "interpretation_limit",
]

REMOVED_EDGE_FIELDS = [
    "removal_id",
    "scenario_id",
    "dropped_source_ids",
    "edge_id",
    "actor_id",
    "issue_id",
    "issue_label",
    "evidence_level",
    "source_ref",
    "stated_support_ref_count",
    "removal_reason",
    "research_status",
    "display_tier",
    "claim_status",
    "review_status",
    "interpretation_limit",
]

LEAVE_ONE_SOURCE_OUT_FIELDS = [
    "source_id",
    "source_title",
    "source_type",
    "source_year",
    "used_by_e3plus_edge",
    "declared_e3plus_edge_count",
    "exclusively_supported_e3plus_edge_count",
    "removed_edge_count",
    "lost_observed_actor_count",
    "remaining_edge_count",
    "remaining_observed_actor_count",
    "removed_edge_rank_desc",
    "comparison_unit",
    "research_status",
    "display_tier",
    "claim_status",
    "review_status",
    "interpretation_limit",
]

FOLLOWUP_FIELDS = [
    "task_id",
    "priority",
    "mode",
    "target",
    "task",
    "done_when",
    "status",
    "claim_boundary",
    "research_status",
    "display_tier",
    "claim_status",
    "review_status",
    "frontend_eligibility",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(
    path: Path,
    rows: list[dict[str, str]],
    fields: list[str],
) -> None:
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


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def split_refs(value: str) -> set[str]:
    return {item.strip() for item in value.split(";") if item.strip()}


def is_current_actor(row: dict[str, str]) -> bool:
    """Apply the explicit current-registry gate used by this package."""

    actor_id = row.get("actor_id", "")
    review_status = row.get("review_status", "").strip().lower()
    scope_status = row.get("scope_status", "").strip().lower()
    if actor_id == "A072" or row.get("merged_duplicate_of", "").strip():
        return False
    if review_status == "rejected":
        return False
    if scope_status == "merged_duplicate":
        return False
    if scope_status.startswith(("retired_", "deactivated_")):
        return False
    if "excluded" in scope_status:
        return False
    return True


def load_current_inputs() -> tuple[
    list[dict[str, str]],
    list[dict[str, str]],
    list[dict[str, str]],
]:
    """Load current actors and the authoritative layered active edge view."""

    actor_history = read_csv(ACTORS_PATH)
    edge_history = read_csv(LAYERED_EDGES_PATH)
    sources = read_csv(SOURCES_PATH)

    actors = [row for row in actor_history if is_current_actor(row)]
    actor_ids = {row["actor_id"] for row in actors}
    edges = [
        row
        for row in edge_history
        if row.get("analysis_inclusion") == "active"
        and row.get("actor_id") in actor_ids
    ]

    if len(actor_ids) != len(actors):
        raise ValueError("current actor layer contains duplicate actor IDs")
    if len({row["edge_id"] for row in edges}) != len(edges):
        raise ValueError("current actor-issue layer contains duplicate edge IDs")
    if len({row["source_id"] for row in sources}) != len(sources):
        raise ValueError("source log contains duplicate source IDs")
    if "A072" in actor_ids:
        raise ValueError("A072 tombstone must not enter the current H1 layer")
    if any(row["analysis_inclusion"] != "active" for row in edges):
        raise ValueError("non-active edge leaked into the current H1 layer")
    return actors, edges, sources


def build_source_host_proposals(
    actors: list[dict[str, str]],
    sources: list[dict[str, str]],
) -> list[dict[str, str]]:
    actor_by_id = {row["actor_id"]: row for row in actors}
    source_by_id = {row["source_id"]: row for row in sources}
    rows: list[dict[str, str]] = []
    for index, (source_id, actor_id) in enumerate(SOURCE_HOST_PROPOSALS, 1):
        if source_id not in source_by_id or actor_id not in actor_by_id:
            raise ValueError(f"proposal endpoint missing: {source_id}/{actor_id}")
        source = source_by_id[source_id]
        actor = actor_by_id[actor_id]
        rows.append(
            {
                "proposal_id": f"H1HP{index:03d}",
                "source_id": source_id,
                "source_title": source["title"],
                "source_url": source["url"],
                "proposed_host_actor_id": actor_id,
                "proposed_host_actor_name": actor["canonical_name"],
                "proposed_host_role": "source_page_host_candidate",
                "mapping_status": "proposal_not_human_reviewed",
                "proposal_basis": (
                    "bounded_H1_pairing_for_sensitivity_only; central source log "
                    "does not encode producer/host/authorship"
                ),
                "producer_role_status": "unknown",
                "self_produced_or_external": "unknown",
                "source_language": "unknown",
                "research_status": "research_only",
                "display_tier": "research",
                "claim_status": "candidate",
                "review_status": "ai_seeded",
                "interpretation_limit": (
                    "Proposed page-host pairing for sensitivity analysis only; "
                    "not authorship, production, coordination, or influence."
                ),
            }
        )
    return rows


def build_actor_source_incidence(
    actors: list[dict[str, str]],
    sources: list[dict[str, str]],
    proposals: list[dict[str, str]],
) -> list[dict[str, str]]:
    """Expand registry source_refs without inferring the actor's source role."""

    source_by_id = {row["source_id"]: row for row in sources}
    proposal_pairs = {
        (row["proposed_host_actor_id"], row["source_id"]): row
        for row in proposals
    }
    rows: list[dict[str, str]] = []
    incidence_index = 1
    for actor in sorted(actors, key=lambda row: row["actor_id"]):
        for token in sorted(split_refs(actor.get("source_refs", ""))):
            source = source_by_id.get(token)
            proposal = proposal_pairs.get((actor["actor_id"], token))
            rows.append(
                {
                    "incidence_id": f"H1AS{incidence_index:04d}",
                    "actor_id": actor["actor_id"],
                    "actor_name": actor["canonical_name"],
                    "source_ref_token": token,
                    "source_id": token if source else "",
                    "source_title": source["title"] if source else "",
                    "source_type": source["source_type"] if source else "",
                    "source_year": source["year"] if source else "",
                    "source_resolution_status": (
                        "resolved_source_id"
                        if source
                        else "unresolved_legacy_reference_token"
                    ),
                    "incidence_basis": "actor_registry.source_refs",
                    "proposed_host_role": (
                        proposal["proposed_host_role"] if proposal else ""
                    ),
                    "host_mapping_status": (
                        "proposal_not_human_reviewed" if proposal else "unknown"
                    ),
                    "producer_role_status": "unknown",
                    "self_produced_or_external": "unknown",
                    "source_language": "unknown",
                    "research_status": "research_only",
                    "display_tier": "research",
                    "claim_status": "candidate",
                    "review_status": "ai_seeded",
                    "interpretation_limit": (
                        "Registry citation incidence only. It does not establish "
                        "authorship, hosting, self-production, external mention, "
                        "language capacity, activity level, or influence."
                    ),
                }
            )
            incidence_index += 1
    return rows


def issue_frame(issue_label: str) -> str | None:
    for frame, labels in FRAME_MAP.items():
        if issue_label in labels:
            return frame
    return None


def component_metrics(edges: list[dict[str, str]]) -> tuple[int, int, int]:
    """Return component count and largest actor/node counts in the bipartite graph."""

    adjacency: dict[str, set[str]] = defaultdict(set)
    for row in edges:
        actor_node = f"actor:{row['actor_id']}"
        issue_node = f"issue:{row['issue_id']}"
        adjacency[actor_node].add(issue_node)
        adjacency[issue_node].add(actor_node)
    seen: set[str] = set()
    components: list[tuple[int, int]] = []
    for node in sorted(adjacency):
        if node in seen:
            continue
        queue = deque([node])
        seen.add(node)
        actor_count = 0
        total_count = 0
        while queue:
            current = queue.popleft()
            total_count += 1
            actor_count += current.startswith("actor:")
            for neighbor in adjacency[current]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    queue.append(neighbor)
        components.append((actor_count, total_count))
    if not components:
        return 0, 0, 0
    largest = max(components, key=lambda value: (value[0], value[1]))
    return len(components), largest[0], largest[1]


def network_metrics(edges: list[dict[str, str]]) -> dict[str, int]:
    actor_frames: dict[str, set[str]] = defaultdict(set)
    actors: set[str] = set()
    issues: set[str] = set()
    for row in edges:
        actors.add(row["actor_id"])
        issues.add(row["issue_id"])
        frame = issue_frame(row["issue_label"])
        if frame:
            actor_frames[row["actor_id"]].add(frame)
    cross = {
        actor_id
        for actor_id, frames in actor_frames.items()
        if len(frames) >= 2
    }
    eco_int = {
        actor_id
        for actor_id, frames in actor_frames.items()
        if {"F2_ecology", "F6_international"}.issubset(frames)
    }
    eco_base = {
        actor_id
        for actor_id, frames in actor_frames.items()
        if {"F2_ecology", "F1_base"}.issubset(frames)
    }
    legal_base = {
        actor_id
        for actor_id, frames in actor_frames.items()
        if {"F5_legal", "F1_base"}.issubset(frames)
    }
    component_count, largest_actors, largest_nodes = component_metrics(edges)
    return {
        "edge_count": len(edges),
        "observed_actor_count": len(actors),
        "issue_count": len(issues),
        "cross_frame_actor_count": len(cross),
        "ecology_international_bridge_count": len(eco_int),
        "ecology_base_bridge_count": len(eco_base),
        "legal_base_bridge_count": len(legal_base),
        "component_count": component_count,
        "largest_component_actor_count": largest_actors,
        "largest_component_total_node_count": largest_nodes,
    }


def select_scenario_edges(
    active_edges: list[dict[str, str]],
    *,
    evidence_gate: set[str] | None,
    dropped_sources: set[str] | None = None,
    dropped_actors: set[str] | None = None,
) -> list[dict[str, str]]:
    dropped_sources = dropped_sources or set()
    dropped_actors = dropped_actors or set()
    selected: list[dict[str, str]] = []
    for row in active_edges:
        if evidence_gate is not None and row["evidence_level"] not in evidence_gate:
            continue
        if row["actor_id"] in dropped_actors:
            continue
        refs = split_refs(row.get("source_ref", ""))
        # Conservative leave-source-out: remove an edge only when all stated
        # support refs are exhausted by the dropped set.  No-source rows survive.
        if dropped_sources and refs and not (refs - dropped_sources):
            continue
        selected.append(row)
    return selected


def build_actor_issue_edge_source_incidence(
    active_edges: list[dict[str, str]],
    sources: list[dict[str, str]],
) -> list[dict[str, str]]:
    """Expand current E3/E4 edge support without inferring source roles."""

    source_by_id = {row["source_id"]: row for row in sources}
    baseline = select_scenario_edges(active_edges, evidence_gate=E3PLUS)
    rows: list[dict[str, str]] = []
    index = 1
    for edge in sorted(baseline, key=lambda row: row["edge_id"]):
        refs = sorted(split_refs(edge.get("source_ref", "")))
        tokens = refs or [""]
        for token in tokens:
            if not token:
                resolution = "no_stated_source_ref"
            elif token in source_by_id:
                resolution = "resolved_source_id"
            elif token.startswith("S"):
                resolution = "unresolved_source_id"
            else:
                resolution = "non_source_reference_token"
            rows.append(
                {
                    "incidence_id": f"H1ES{index:04d}",
                    "edge_id": edge["edge_id"],
                    "actor_id": edge["actor_id"],
                    "issue_id": edge["issue_id"],
                    "issue_label": edge["issue_label"],
                    "evidence_level": edge["evidence_level"],
                    "source_ref_token": token,
                    "source_id": token if token in source_by_id else "",
                    "source_resolution_status": resolution,
                    "stated_support_ref_count": str(len(refs)),
                    "removed_if_this_source_dropped_alone": (
                        "yes" if token and len(refs) == 1 else "no"
                    ),
                    "research_status": "research_only",
                    "display_tier": "research",
                    "claim_status": "candidate",
                    "review_status": "ai_seeded",
                    "interpretation_limit": (
                        "This row records a stated actor-issue support token. "
                        "It does not establish authorship, hosting, event "
                        "coordination, or social influence."
                    ),
                }
            )
            index += 1
    return rows


def build_scenario_removed_edges(
    active_edges: list[dict[str, str]],
) -> list[dict[str, str]]:
    """Expose every edge removed in the four declared source scenarios."""

    baseline = select_scenario_edges(active_edges, evidence_gate=E3PLUS)
    definitions = (
        ("SOURCE_DROP_S003", {"S003"}),
        ("SOURCE_DROP_S004", {"S004"}),
        ("SOURCE_DROP_S006", {"S006"}),
        ("SOURCE_DROP_BIG3", {"S003", "S004", "S006"}),
    )
    rows: list[dict[str, str]] = []
    index = 1
    for scenario_id, dropped_sources in definitions:
        selected = select_scenario_edges(
            active_edges,
            evidence_gate=E3PLUS,
            dropped_sources=dropped_sources,
        )
        selected_ids = {row["edge_id"] for row in selected}
        for edge in baseline:
            if edge["edge_id"] in selected_ids:
                continue
            refs = split_refs(edge.get("source_ref", ""))
            rows.append(
                {
                    "removal_id": f"H1RE{index:04d}",
                    "scenario_id": scenario_id,
                    "dropped_source_ids": ";".join(sorted(dropped_sources)),
                    "edge_id": edge["edge_id"],
                    "actor_id": edge["actor_id"],
                    "issue_id": edge["issue_id"],
                    "issue_label": edge["issue_label"],
                    "evidence_level": edge["evidence_level"],
                    "source_ref": edge.get("source_ref", ""),
                    "stated_support_ref_count": str(len(refs)),
                    "removal_reason": "all_stated_support_exhausted",
                    "research_status": "research_only",
                    "display_tier": "research",
                    "claim_status": "candidate",
                    "review_status": "ai_seeded",
                    "interpretation_limit": (
                        "Removed from the documented E3/E4 layer only; this "
                        "does not mean the actor, issue, or activity ceased to "
                        "exist."
                    ),
                }
            )
            index += 1
    return rows


def build_leave_one_source_out(
    active_edges: list[dict[str, str]],
    sources: list[dict[str, str]],
) -> list[dict[str, str]]:
    """Compare every source ID under the same one-source deletion unit."""

    baseline = select_scenario_edges(active_edges, evidence_gate=E3PLUS)
    baseline_metrics = network_metrics(baseline)
    source_by_id = {row["source_id"]: row for row in sources}
    used_source_ids = {
        token
        for edge in baseline
        for token in split_refs(edge.get("source_ref", ""))
        if token.startswith("S")
    }
    source_ids = sorted(set(source_by_id) | used_source_ids)
    provisional: list[dict[str, str]] = []
    for source_id in source_ids:
        selected = select_scenario_edges(
            active_edges,
            evidence_gate=E3PLUS,
            dropped_sources={source_id},
        )
        metrics = network_metrics(selected)
        declared = [
            edge
            for edge in baseline
            if source_id in split_refs(edge.get("source_ref", ""))
        ]
        exclusive = [
            edge
            for edge in declared
            if split_refs(edge.get("source_ref", "")) == {source_id}
        ]
        source = source_by_id.get(source_id, {})
        provisional.append(
            {
                "source_id": source_id,
                "source_title": source.get("title", ""),
                "source_type": source.get("source_type", ""),
                "source_year": source.get("year", ""),
                "used_by_e3plus_edge": "yes" if declared else "no",
                "declared_e3plus_edge_count": str(len(declared)),
                "exclusively_supported_e3plus_edge_count": str(len(exclusive)),
                "removed_edge_count": str(
                    baseline_metrics["edge_count"] - metrics["edge_count"]
                ),
                "lost_observed_actor_count": str(
                    baseline_metrics["observed_actor_count"]
                    - metrics["observed_actor_count"]
                ),
                "remaining_edge_count": str(metrics["edge_count"]),
                "remaining_observed_actor_count": str(
                    metrics["observed_actor_count"]
                ),
                "comparison_unit": "one_source_id",
                "research_status": "research_only",
                "display_tier": "research",
                "claim_status": "candidate",
                "review_status": "ai_seeded",
                "interpretation_limit": (
                    "One-source leave-out measures dependence of the coded "
                    "evidence layer on a source ID. It does not measure the "
                    "source's authorship, organizational capacity, or social "
                    "centrality."
                ),
            }
        )
    removed_counts = [
        int(row["removed_edge_count"]) for row in provisional
    ]
    for row in provisional:
        count = int(row["removed_edge_count"])
        row["removed_edge_rank_desc"] = str(
            1 + sum(other > count for other in removed_counts)
        )
    return provisional


def build_followup_tasks() -> list[dict[str, str]]:
    definitions = [
        (
            "H1FR001",
            "P0",
            "human_review",
            "S003/S004/S006 and top leave-one-out sources",
            "Confirm producer, page host, author/editor, self-produced versus external mention, and language for each high-removal source.",
            "Every top source has a cited role decision or explicit unresolved status.",
            "A webpage domain or actor citation is not authorship or coordination.",
        ),
        (
            "H1FR002",
            "P0",
            "mechanical_then_human_review",
            "all-source leave-one-out distribution",
            "Classify high-removal sources by document family, event-list structure, year, and source-selection route.",
            "S004 is compared with sources of similar document form and coverage, not only with actor-node deletion.",
            "Document coverage and actor deletion are different units and not matched counterfactuals.",
        ),
        (
            "H1FR003",
            "P1",
            "online_then_human_review",
            "documentation-capacity fields",
            "Collect own-site, archived-site, bilingual material, legal/professional support, staff and publication-history indicators for a matched actor sample.",
            "Each field has dated source evidence, missingness, and a human-reviewed coding rule.",
            "Do not infer capacity from actor class, source count, or issue degree alone.",
        ),
        (
            "H1FR004",
            "P1",
            "local_and_online",
            "lifecycle matched sample",
            "Build formed/active/renamed/merged/dissolved/last-observed intervals with right-censoring and task-completion exits.",
            "Matched cases distinguish dissolution, planned sunset, merger, renaming, archival silence and current activity.",
            "Online silence is not organizational death; temporary committees are not failed organizations.",
        ),
        (
            "H1FR005",
            "P1",
            "mechanical",
            "event-list hyperedges",
            "Re-estimate visibility after separating co-signing/event rosters from independently sourced actor-issue observations.",
            "Sensitivity is reported by source family and event rather than projecting lists into stable organization ties.",
            "Co-listing is event participation, not alliance or coordination.",
        ),
        (
            "H1FR006",
            "P0",
            "principal_interpretive_gate",
            "H1 conclusion strength",
            "Decide whether H1 remains a Phase-1 methods correction or merits a second-wave methods paper pilot.",
            "Decision cites leave-one-out concentration, unit mismatch, source-role review and lifecycle feasibility.",
            "Current evidence supports source dependence, not documentation capacity causing centrality.",
        ),
    ]
    return [
        {
            "task_id": task_id,
            "priority": priority,
            "mode": mode,
            "target": target,
            "task": task,
            "done_when": done_when,
            "status": "open",
            "claim_boundary": boundary,
            "research_status": "research_only",
            "display_tier": "research",
            "claim_status": "candidate",
            "review_status": "ai_seeded",
            "frontend_eligibility": "not_frontend_ready",
        }
        for (
            task_id,
            priority,
            mode,
            target,
            task,
            done_when,
            boundary,
        ) in definitions
    ]


def pct_ratio(numerator: int, denominator: int) -> str:
    return f"{numerator / denominator * 100:.1f}" if denominator else ""


def build_scenarios(
    actors: list[dict[str, str]],
    active_edges: list[dict[str, str]],
) -> list[dict[str, str]]:
    definitions = [
        {
            "scenario_id": "BASE_CURRENT_ACTIVE_ALL",
            "scenario_label": "Current active edges, all evidence levels",
            "scenario_family": "baseline",
            "paired_group": "",
            "sources": set(),
            "actors": set(),
            "gate": None,
            "rule": "analysis_inclusion=active; no evidence-level restriction",
            "mapping": "not_applicable",
        },
        {
            "scenario_id": "BASE_CURRENT_E3PLUS",
            "scenario_label": "Current active E3/E4 baseline",
            "scenario_family": "baseline",
            "paired_group": "",
            "sources": set(),
            "actors": set(),
            "gate": E3PLUS,
            "rule": "analysis_inclusion=active and evidence_level in E3/E4",
            "mapping": "not_applicable",
        },
        {
            "scenario_id": "SOURCE_DROP_S003",
            "scenario_label": "Remove support exhausted by S003",
            "scenario_family": "source_support_deletion",
            "paired_group": "S003_A005",
            "sources": {"S003"},
            "actors": set(),
            "gate": E3PLUS,
            "rule": "remove edge only if every stated source_ref is in S003",
            "mapping": "proposal_not_human_reviewed",
        },
        {
            "scenario_id": "SOURCE_DROP_S004",
            "scenario_label": "Remove support exhausted by S004",
            "scenario_family": "source_support_deletion",
            "paired_group": "S004_A004",
            "sources": {"S004"},
            "actors": set(),
            "gate": E3PLUS,
            "rule": "remove edge only if every stated source_ref is in S004",
            "mapping": "proposal_not_human_reviewed",
        },
        {
            "scenario_id": "SOURCE_DROP_S006",
            "scenario_label": "Remove support exhausted by S006",
            "scenario_family": "source_support_deletion",
            "paired_group": "S006_A001",
            "sources": {"S006"},
            "actors": set(),
            "gate": E3PLUS,
            "rule": "remove edge only if every stated source_ref is in S006",
            "mapping": "proposal_not_human_reviewed",
        },
        {
            "scenario_id": "SOURCE_DROP_BIG3",
            "scenario_label": "Remove support exhausted by S003/S004/S006",
            "scenario_family": "source_support_deletion",
            "paired_group": "BIG3",
            "sources": {"S003", "S004", "S006"},
            "actors": set(),
            "gate": E3PLUS,
            "rule": (
                "remove edge only if every stated source_ref is in "
                "S003/S004/S006"
            ),
            "mapping": "proposal_not_human_reviewed",
        },
        {
            "scenario_id": "ACTOR_DROP_A005",
            "scenario_label": "Remove actor node A005",
            "scenario_family": "actor_node_deletion",
            "paired_group": "S003_A005",
            "sources": set(),
            "actors": {"A005"},
            "gate": E3PLUS,
            "rule": "remove actor endpoint A005; retain all other stated support",
            "mapping": "not_applicable_to_node_deletion",
        },
        {
            "scenario_id": "ACTOR_DROP_A004",
            "scenario_label": "Remove actor node A004",
            "scenario_family": "actor_node_deletion",
            "paired_group": "S004_A004",
            "sources": set(),
            "actors": {"A004"},
            "gate": E3PLUS,
            "rule": "remove actor endpoint A004; retain all other stated support",
            "mapping": "not_applicable_to_node_deletion",
        },
        {
            "scenario_id": "ACTOR_DROP_A001",
            "scenario_label": "Remove actor node A001",
            "scenario_family": "actor_node_deletion",
            "paired_group": "S006_A001",
            "sources": set(),
            "actors": {"A001"},
            "gate": E3PLUS,
            "rule": "remove actor endpoint A001; retain all other stated support",
            "mapping": "not_applicable_to_node_deletion",
        },
        {
            "scenario_id": "ACTOR_DROP_BIG3",
            "scenario_label": "Remove actor nodes A001/A004/A005",
            "scenario_family": "actor_node_deletion",
            "paired_group": "BIG3",
            "sources": set(),
            "actors": {"A001", "A004", "A005"},
            "gate": E3PLUS,
            "rule": (
                "remove actor endpoints A001/A004/A005; retain all other "
                "stated support"
            ),
            "mapping": "not_applicable_to_node_deletion",
        },
    ]

    selected_by_id: dict[str, list[dict[str, str]]] = {}
    for definition in definitions:
        selected_by_id[definition["scenario_id"]] = select_scenario_edges(
            active_edges,
            evidence_gate=definition["gate"],
            dropped_sources=definition["sources"],
            dropped_actors=definition["actors"],
        )
    all_baseline = network_metrics(selected_by_id["BASE_CURRENT_ACTIVE_ALL"])
    e3_baseline = network_metrics(selected_by_id["BASE_CURRENT_E3PLUS"])

    rows: list[dict[str, str]] = []
    for definition in definitions:
        selected = selected_by_id[definition["scenario_id"]]
        metrics = network_metrics(selected)
        if definition["scenario_id"] == "BASE_CURRENT_ACTIVE_ALL":
            reference = all_baseline
            reference_id = "BASE_CURRENT_ACTIVE_ALL"
        else:
            reference = e3_baseline
            reference_id = "BASE_CURRENT_E3PLUS"
        remaining_registry = len(actors) - len(definition["actors"])
        rows.append(
            {
                "scenario_id": definition["scenario_id"],
                "scenario_label": definition["scenario_label"],
                "scenario_family": definition["scenario_family"],
                "paired_group": definition["paired_group"],
                "dropped_source_ids": ";".join(sorted(definition["sources"])),
                "dropped_actor_ids": ";".join(sorted(definition["actors"])),
                "evidence_gate": (
                    "all_current"
                    if definition["gate"] is None
                    else "E3;E4"
                ),
                **{key: str(value) for key, value in metrics.items()},
                "remaining_registry_actor_count": str(remaining_registry),
                "registry_isolated_actor_count": str(
                    remaining_registry - metrics["observed_actor_count"]
                ),
                "edge_retention_pct": pct_ratio(
                    metrics["edge_count"],
                    reference["edge_count"],
                ),
                "actor_retention_pct": pct_ratio(
                    metrics["observed_actor_count"],
                    reference["observed_actor_count"],
                ),
                "retention_reference": reference_id,
                "selection_rule": definition["rule"],
                "source_host_mapping_status": definition["mapping"],
                "research_status": "research_only",
                "display_tier": "research",
                "claim_status": "candidate",
                "review_status": "ai_seeded",
                "interpretation_limit": RESEARCH_LIMIT,
            }
        )
    return rows


def build_pair_comparison(
    scenarios: list[dict[str, str]],
) -> list[dict[str, str]]:
    by_id = {row["scenario_id"]: row for row in scenarios}
    definitions = [
        ("S003_A005", "S003", "A005", "SOURCE_DROP_S003", "ACTOR_DROP_A005"),
        ("S004_A004", "S004", "A004", "SOURCE_DROP_S004", "ACTOR_DROP_A004"),
        ("S006_A001", "S006", "A001", "SOURCE_DROP_S006", "ACTOR_DROP_A001"),
        ("BIG3", "S003;S004;S006", "A001;A004;A005", "SOURCE_DROP_BIG3", "ACTOR_DROP_BIG3"),
    ]
    rows: list[dict[str, str]] = []
    for pair_id, source_id, actor_id, source_scenario, actor_scenario in definitions:
        source = by_id[source_scenario]
        actor = by_id[actor_scenario]
        rows.append(
            {
                "pair_id": pair_id,
                "source_id": source_id,
                "actor_id": actor_id,
                "source_scenario_id": source_scenario,
                "actor_scenario_id": actor_scenario,
                "source_deletion_edge_count": source["edge_count"],
                "actor_deletion_edge_count": actor["edge_count"],
                "additional_edge_loss_under_source_deletion": str(
                    int(actor["edge_count"]) - int(source["edge_count"])
                ),
                "source_deletion_observed_actor_count": source[
                    "observed_actor_count"
                ],
                "actor_deletion_observed_actor_count": actor[
                    "observed_actor_count"
                ],
                "additional_actor_loss_under_source_deletion": str(
                    int(actor["observed_actor_count"])
                    - int(source["observed_actor_count"])
                ),
                "mapping_status": "proposal_not_human_reviewed",
                "producer_role_status": "unknown",
                "self_produced_or_external": "unknown",
                "source_language": "unknown",
                "comparison_validity": (
                    "descriptive_unmatched_units_not_a_counterfactual"
                ),
                "research_status": "research_only",
                "display_tier": "research",
                "claim_status": "candidate",
                "review_status": "ai_seeded",
                "interpretation_limit": (
                    "Source deletion and actor-node deletion have different "
                    "units and maximum reach. Their difference is descriptive, "
                    "not a matched counterfactual or evidence that a source "
                    "producer created social centrality."
                ),
            }
        )
    return rows


def rankdata(values: list[int]) -> list[float]:
    ranked = [0.0] * len(values)
    ordered = sorted(range(len(values)), key=lambda index: values[index])
    cursor = 0
    while cursor < len(ordered):
        end = cursor + 1
        while (
            end < len(ordered)
            and values[ordered[end]] == values[ordered[cursor]]
        ):
            end += 1
        average = (cursor + end - 1) / 2 + 1
        for position in range(cursor, end):
            ranked[ordered[position]] = average
        cursor = end
    return ranked


def pearson(values_a: list[float], values_b: list[float]) -> float:
    mean_a = sum(values_a) / len(values_a)
    mean_b = sum(values_b) / len(values_b)
    numerator = sum(
        (value_a - mean_a) * (value_b - mean_b)
        for value_a, value_b in zip(values_a, values_b)
    )
    denominator = math.sqrt(
        sum((value - mean_a) ** 2 for value in values_a)
        * sum((value - mean_b) ** 2 for value in values_b)
    )
    return numerator / denominator if denominator else float("nan")


def build_actor_diagnostics(
    actors: list[dict[str, str]],
    active_edges: list[dict[str, str]],
    sources: list[dict[str, str]],
) -> list[dict[str, str]]:
    source_ids = {row["source_id"] for row in sources}
    all_degree = Counter(row["actor_id"] for row in active_edges)
    e3_degree = Counter(
        row["actor_id"]
        for row in active_edges
        if row["evidence_level"] in E3PLUS
    )
    rows: list[dict[str, str]] = []
    for actor in sorted(actors, key=lambda row: row["actor_id"]):
        refs = split_refs(actor.get("source_refs", ""))
        rows.append(
            {
                "actor_id": actor["actor_id"],
                "actor_name": actor["canonical_name"],
                "actor_class": actor["actor_class"],
                "origin_type": actor["origin_type"],
                "actor_review_status": actor["review_status"],
                "resolved_registry_source_ref_count": str(
                    len(refs & source_ids)
                ),
                "unresolved_registry_source_ref_count": str(
                    len(refs - source_ids)
                ),
                "active_issue_edge_count": str(all_degree[actor["actor_id"]]),
                "active_e3plus_issue_edge_count": str(
                    e3_degree[actor["actor_id"]]
                ),
                "own_website_status": "unknown",
                "english_material_capacity": "unknown",
                "staff_capacity": "unknown",
                "legal_support_capacity": "unknown",
                "lifecycle_status_for_h1": (
                    "unknown_not_joined_in_this_package"
                ),
                "research_status": "research_only",
                "display_tier": "research",
                "claim_status": "candidate",
                "review_status": "ai_seeded",
                "interpretation_limit": (
                    "Counts describe current registry citations and coded "
                    "actor-issue edges. They do not measure organizational "
                    "capacity, activity, influence, or lifespan."
                ),
            }
        )
    return rows


def diagnostic_summary(
    actor_diagnostics: list[dict[str, str]],
) -> dict[str, object]:
    source_counts = [
        int(row["resolved_registry_source_ref_count"])
        for row in actor_diagnostics
    ]
    issue_degrees = [
        int(row["active_issue_edge_count"])
        for row in actor_diagnostics
    ]
    rho = pearson(rankdata(source_counts), rankdata(issue_degrees))
    groups: dict[str, list[int]] = {
        "zero_resolved_refs": [],
        "one_resolved_ref": [],
        "two_or_more_resolved_refs": [],
        "three_or_more_resolved_refs": [],
    }
    for source_count, degree in zip(source_counts, issue_degrees):
        if source_count == 0:
            groups["zero_resolved_refs"].append(degree)
        if source_count == 1:
            groups["one_resolved_ref"].append(degree)
        if source_count >= 2:
            groups["two_or_more_resolved_refs"].append(degree)
        if source_count >= 3:
            groups["three_or_more_resolved_refs"].append(degree)
    return {
        "spearman_resolved_registry_source_ref_count_vs_active_issue_degree": round(
            rho,
            3,
        ),
        "groups": {
            label: {
                "actor_count": len(values),
                "mean_active_issue_degree": round(
                    sum(values) / len(values),
                    2,
                )
                if values
                else None,
                "zero_issue_edge_actor_count": sum(value == 0 for value in values),
            }
            for label, values in groups.items()
        },
        "interpretation_limit": (
            "This is a mechanical association between two project-coded "
            "quantities. Source-ref count and issue degree are not independent "
            "measures of real documentation capacity or social centrality."
        ),
    }


def render_brief(
    scenarios: list[dict[str, str]],
    pair_rows: list[dict[str, str]],
    incidence: list[dict[str, str]],
    edge_source_incidence: list[dict[str, str]],
    diagnostics: dict[str, object],
    leave_one_out: list[dict[str, str]],
) -> str:
    by_id = {row["scenario_id"]: row for row in scenarios}
    baseline_all = by_id["BASE_CURRENT_ACTIVE_ALL"]
    baseline_e3 = by_id["BASE_CURRENT_E3PLUS"]
    big_source = by_id["SOURCE_DROP_BIG3"]
    big_actor = by_id["ACTOR_DROP_BIG3"]
    s004 = by_id["SOURCE_DROP_S004"]
    resolved = sum(
        row["source_resolution_status"] == "resolved_source_id"
        for row in incidence
    )
    unresolved = len(incidence) - resolved
    edge_ids_with_resolved_source = {
        row["edge_id"]
        for row in edge_source_incidence
        if row["source_resolution_status"] == "resolved_source_id"
    }
    edge_ids = {row["edge_id"] for row in edge_source_incidence}
    edges_without_resolved_source = len(
        edge_ids - edge_ids_with_resolved_source
    )
    used_source_count = sum(
        row["used_by_e3plus_edge"] == "yes" for row in leave_one_out
    )
    s004_loo = next(
        row for row in leave_one_out if row["source_id"] == "S004"
    )
    big_edge_loss = int(baseline_e3["edge_count"]) - int(
        big_source["edge_count"]
    )
    s004_edge_loss = int(baseline_e3["edge_count"]) - int(
        s004["edge_count"]
    )
    big_actor_loss = int(baseline_e3["observed_actor_count"]) - int(
        big_source["observed_actor_count"]
    )
    s004_actor_loss = int(baseline_e3["observed_actor_count"]) - int(
        s004["observed_actor_count"]
    )
    s004_edge_share = s004_edge_loss / big_edge_loss * 100
    s004_actor_share = s004_actor_loss / big_actor_loss * 100
    pair_lines = "\n".join(
        "| {pair_id} | {source_deletion_edge_count} / "
        "{source_deletion_observed_actor_count} | {actor_deletion_edge_count} / "
        "{actor_deletion_observed_actor_count} | "
        "{additional_actor_loss_under_source_deletion} |".format(**row)
        for row in pair_rows
    )
    rho = diagnostics[
        "spearman_resolved_registry_source_ref_count_vs_active_issue_degree"
    ]
    return f"""# H1：高承载名单对 actor–issue 可见层的来源依赖 v1

日期：{AUDIT_DATE}
状态：**research-only / candidate / not_frontend_ready**

## 当前可复算边界

- current gate：121 个有效 actor；`analysis_inclusion=active` 的 {baseline_all['edge_count']} 条 actor–issue 边。
- 敏感性 evidence gate：E3/E4，共 {baseline_e3['edge_count']} 条边、{baseline_e3['observed_actor_count']} 个有边 actor。
- actor–source incidence：{len(incidence)} 个 registry 引用 token，其中 {resolved} 个解析到 source log、{unresolved} 个为显式 legacy unresolved token。
- E3/E4 的 {baseline_e3['edge_count']} 条边中，有 {edges_without_resolved_source} 条没有可解析的 `S` 来源（空值或仅非 `S` token），按保守规则不会被 source-ID 删除实验移除。
- 全来源 leave-one-out 覆盖 source log 和 E3/E4 边中的 source ID；其中 {used_source_count} 个 source ID 实际出现在该层。
- 所有 source-host 配对均为 `proposal_not_human_reviewed`；producer、self/external、source language 均保持 `unknown`。

## 成对删除结果

| 配对 | 删 source support：边 / 有边 actor | 删 actor node：边 / 有边 actor | 两种不匹配单位的 actor 差值 |
|---|---:|---:|---:|
{pair_lines}

最强的单源敏感性来自 S004，在全来源 leave-one-out 中按删除边数列第 {s004_loo['removed_edge_rank_desc']}：E3/E4 观测层由 {baseline_e3['edge_count']} 边／{baseline_e3['observed_actor_count']} 个有边 actor 降至 {s004['edge_count']}／{s004['observed_actor_count']}。三份来源同时删除造成 {big_edge_loss} 条边、{big_actor_loss} 个有边 actor 的损失，其中 S004 单独贡献 {s004_edge_loss} 条边（{s004_edge_share:.1f}%）和 {s004_actor_loss} 个 actor（{s004_actor_share:.1f}%）。因此当前效应主要是一份 2015 年高承载名单的来源集中，而不是三类组织反复呈现相同机制。

“删 source support”和“删 actor node”具有不同单位和最大影响范围：一份名单可以支撑几十个 actor–issue 编码，删除一个 actor 只能直接去掉该节点。上表只保留为描述性尺度对照，**不是匹配反事实**。

这支持的弱命题是：

> 当前 E3/E4 actor–issue 可见层对 S004 等高承载名单存在显著来源依赖；研究者看到的组织—议题覆盖会随少数列表材料的可得性明显收缩。

它不支持：

- 这些拟配对 actor 已被确认是材料作者、唯一生产者或真实协调中心；
- 三份材料共同证明“官网、律师或英文能力”反复制造中心性；
- 社会网络本身会因文件不可见而断裂；
- 官网、英文能力、律师或专职人员已经造成中心性；
- 资料较少的组织寿命更短。

## 辅助诊断

Registry 已解析 source-ref 数与 active issue degree 的 Spearman 为 {rho}。这是两个项目编码量之间的机械相关，不是组织能力或社会中心性的因果估计。

## 替代解释

1. 专业组织可能真实承担协调角色，同时也更容易留下材料。
2. 法律、国际倡议和大型联署场域本身会强制或鼓励文档生产。
3. 当前样本由 2010／2015／2020 三份名单播种，存在研究设计内生性。
4. 组织规模、法人身份、年代和地点可能同时影响材料存续与可观察议题数。
5. 临时实行委员会可能按任务设计解散，不能等同于能力不足或短寿失败。

## 下一步验证门槛

需要完成 `further_research_queue_v1.csv`：先确认 producer/host 与材料类型，再用同单位、同覆盖度来源作比较；另补官网、人员／法律支援、语言和右删失生命周期字段。事件名单应继续作为 hyperedge，不投影成稳定联盟。

## 强制解释边界

{RESEARCH_LIMIT}
"""


def render_readme() -> str:
    return f"""# research_wave_h1_documentation_visibility_v1

独立、可复算的 H1 研究外挂包。它不修改中央 registry、source、edge、前端或现有 robustness 包。

## 复现

```powershell
python scripts\\make_h1_documentation_visibility_v1.py
python -m unittest tests.test_make_h1_documentation_visibility_v1
```

## 输入

- `data/interim/01_actor_registry_initial_v0.csv`
- `data/interim/05_source_log_initial_v0.csv`
- `data/interim/24_r01_r02_actor_issue_layered_v0.csv`

## 输出

- `actor_source_incidence_v1.csv`：registry source-ref token 展开；角色未知不推断。
- `actor_issue_edge_source_incidence_v1.csv`：E3/E4 actor–issue edge×support-token 下钻。
- `source_host_mapping_proposals_v1.csv`：S003/S004/S006 与 A005/A004/A001 的研究配对提案。
- `actor_visibility_diagnostics_v1.csv`：每 actor 的引用／议题机械计数；capacity 与 lifecycle 均未知。
- `sensitivity_scenarios_v1.csv`：current gate、source-support deletion 与 actor-node deletion。
- `scenario_removed_edges_v1.csv`：四个 source scenario 逐边删除明细。
- `leave_one_source_out_v1.csv`：所有 source ID 在相同单源删除单位下的分布。
- `paired_deletion_comparison_v1.csv`：四组不同单位的描述性对照；不是匹配反事实。
- `further_research_queue_v1.csv`：6 项未闭合验证任务。
- `metrics_v1.json`：机器可读指标、输入 hash 与解释边界。
- `brief_v1.md`：研究解释。
- `validation_report.md`：构建门禁。

## 状态

全包固定为：

- `research_status=research_only`
- `display_tier=research`
- `claim_status=candidate`
- `review_status=ai_seeded`

不得进入已核视图。source 删除表示当前编码支持被耗尽，不表示真实组织或社会关系消失。
"""


def main() -> None:
    actors, edges, sources = load_current_inputs()
    proposals = build_source_host_proposals(actors, sources)
    incidence = build_actor_source_incidence(actors, sources, proposals)
    edge_source_incidence = build_actor_issue_edge_source_incidence(
        edges,
        sources,
    )
    scenarios = build_scenarios(actors, edges)
    removed_edges = build_scenario_removed_edges(edges)
    leave_one_out = build_leave_one_source_out(edges, sources)
    pairs = build_pair_comparison(scenarios)
    actor_diagnostics = build_actor_diagnostics(actors, edges, sources)
    diagnostics = diagnostic_summary(actor_diagnostics)
    followup_tasks = build_followup_tasks()
    by_id = {row["scenario_id"]: row for row in scenarios}
    s004_loo = next(
        row for row in leave_one_out if row["source_id"] == "S004"
    )

    if len(actors) != 121 or len(edges) != 238:
        raise ValueError(
            "current H1 gate drifted; expected 121 actors and 238 active edges"
        )
    if len(proposals) != 3:
        raise ValueError("expected three bounded source-host proposals")
    if any(
        row["mapping_status"] != "proposal_not_human_reviewed"
        or row["producer_role_status"] != "unknown"
        or row["self_produced_or_external"] != "unknown"
        or row["source_language"] != "unknown"
        for row in proposals
    ):
        raise ValueError("proposal/unknown fields were promoted beyond evidence")
    if any(
        row["display_tier"] != "research"
        or row["claim_status"] != "candidate"
        or row["review_status"] != "ai_seeded"
        for rows in (
            incidence,
            edge_source_incidence,
            proposals,
            scenarios,
            removed_edges,
            leave_one_out,
            pairs,
            actor_diagnostics,
            followup_tasks,
        )
        for row in rows
    ):
        raise ValueError("research-only output leaked into a reviewed status")

    OUT.mkdir(parents=True, exist_ok=True)
    write_csv(
        OUT / "actor_source_incidence_v1.csv",
        incidence,
        INCIDENCE_FIELDS,
    )
    write_csv(
        OUT / "actor_issue_edge_source_incidence_v1.csv",
        edge_source_incidence,
        EDGE_SOURCE_FIELDS,
    )
    write_csv(
        OUT / "source_host_mapping_proposals_v1.csv",
        proposals,
        PROPOSAL_FIELDS,
    )
    write_csv(
        OUT / "actor_visibility_diagnostics_v1.csv",
        actor_diagnostics,
        ACTOR_DIAGNOSTIC_FIELDS,
    )
    write_csv(
        OUT / "sensitivity_scenarios_v1.csv",
        scenarios,
        SCENARIO_FIELDS,
    )
    write_csv(
        OUT / "paired_deletion_comparison_v1.csv",
        pairs,
        PAIR_FIELDS,
    )
    write_csv(
        OUT / "scenario_removed_edges_v1.csv",
        removed_edges,
        REMOVED_EDGE_FIELDS,
    )
    write_csv(
        OUT / "leave_one_source_out_v1.csv",
        leave_one_out,
        LEAVE_ONE_SOURCE_OUT_FIELDS,
    )
    write_csv(
        OUT / "further_research_queue_v1.csv",
        followup_tasks,
        FOLLOWUP_FIELDS,
    )

    resolved_incidence = sum(
        row["source_resolution_status"] == "resolved_source_id"
        for row in incidence
    )
    edge_ids_with_resolved_source = {
        row["edge_id"]
        for row in edge_source_incidence
        if row["source_resolution_status"] == "resolved_source_id"
    }
    edge_ids_without_resolved_source = {
        row["edge_id"] for row in edge_source_incidence
    } - edge_ids_with_resolved_source
    metrics = {
        "artifact": "research_wave_h1_documentation_visibility_v1",
        "as_of_date": AUDIT_DATE,
        "layer": {
            "research_status": "research_only",
            "display_tier": "research",
            "claim_status": "candidate",
            "review_status": "ai_seeded",
            "frontend_eligibility": "not_frontend_ready",
        },
        "current_gate": {
            "actor_rule": (
                "exclude A072, merged_duplicate_of, rejected, "
                "retired/deactivated/excluded scope"
            ),
            "actor_count": len(actors),
            "edge_rule": (
                "24_r01_r02_actor_issue_layered_v0.csv where "
                "analysis_inclusion=active and endpoint is a current actor"
            ),
            "active_actor_issue_edge_count": len(edges),
            "active_actor_with_edge_count": len(
                {row["actor_id"] for row in edges}
            ),
        },
        "sensitivity_gate": {
            "evidence_levels": sorted(E3PLUS),
            "source_deletion_rule": (
                "remove edge only when all stated source_ref tokens are "
                "exhausted by the dropped source set"
            ),
            "actor_deletion_rule": (
                "remove edges whose actor endpoint is in the dropped actor set"
            ),
        },
        "actor_source_incidence": {
            "row_count": len(incidence),
            "resolved_source_id_count": resolved_incidence,
            "unresolved_legacy_reference_token_count": (
                len(incidence) - resolved_incidence
            ),
        },
        "actor_issue_edge_source_incidence": {
            "row_count": len(edge_source_incidence),
            "edge_count": len(
                {row["edge_id"] for row in edge_source_incidence}
            ),
            "edge_with_resolved_source_id_count": len(
                edge_ids_with_resolved_source
            ),
            "edge_without_resolved_source_id_count": len(
                edge_ids_without_resolved_source
            ),
            "basis": "active E3/E4 actor-issue edge stated source_ref tokens",
        },
        "source_host_mapping": {
            "status": "proposal_not_human_reviewed",
            "pairs": [
                {
                    "source_id": row["source_id"],
                    "actor_id": row["proposed_host_actor_id"],
                    "producer_role_status": "unknown",
                    "self_produced_or_external": "unknown",
                    "source_language": "unknown",
                }
                for row in proposals
            ],
        },
        "scenario_metrics": [
            {
                key: (
                    int(value)
                    if key
                    in {
                        "edge_count",
                        "observed_actor_count",
                        "remaining_registry_actor_count",
                        "registry_isolated_actor_count",
                        "issue_count",
                        "cross_frame_actor_count",
                        "ecology_international_bridge_count",
                        "ecology_base_bridge_count",
                        "legal_base_bridge_count",
                        "component_count",
                        "largest_component_actor_count",
                        "largest_component_total_node_count",
                    }
                    else value
                )
                for key, value in row.items()
            }
            for row in scenarios
        ],
        "paired_comparison": pairs,
        "paired_comparison_validity": (
            "descriptive_unmatched_units_not_a_counterfactual"
        ),
        "leave_one_source_out": {
            "source_id_count": len(leave_one_out),
            "used_source_id_count": sum(
                row["used_by_e3plus_edge"] == "yes"
                for row in leave_one_out
            ),
            "s004": {
                "removed_edge_count": int(
                    s004_loo["removed_edge_count"]
                ),
                "lost_observed_actor_count": int(
                    s004_loo["lost_observed_actor_count"]
                ),
                "removed_edge_rank_desc": int(
                    s004_loo["removed_edge_rank_desc"]
                ),
            },
            "interpretation_limit": (
                "Same-unit source concentration audit only; it does not "
                "identify source roles or documentation capacity."
            ),
        },
        "open_followup_task_count": len(followup_tasks),
        "diagnostics": diagnostics,
        "current_result_summary": {
            "baseline_e3plus_edges": int(
                by_id["BASE_CURRENT_E3PLUS"]["edge_count"]
            ),
            "baseline_e3plus_observed_actors": int(
                by_id["BASE_CURRENT_E3PLUS"]["observed_actor_count"]
            ),
            "source_drop_big3_edges": int(
                by_id["SOURCE_DROP_BIG3"]["edge_count"]
            ),
            "source_drop_big3_observed_actors": int(
                by_id["SOURCE_DROP_BIG3"]["observed_actor_count"]
            ),
            "actor_drop_big3_edges": int(
                by_id["ACTOR_DROP_BIG3"]["edge_count"]
            ),
            "actor_drop_big3_observed_actors": int(
                by_id["ACTOR_DROP_BIG3"]["observed_actor_count"]
            ),
            "source_drop_s004_edges": int(
                by_id["SOURCE_DROP_S004"]["edge_count"]
            ),
            "source_drop_s004_observed_actors": int(
                by_id["SOURCE_DROP_S004"]["observed_actor_count"]
            ),
        },
        "input_hashes": {
            "actors": sha256(ACTORS_PATH),
            "sources": sha256(SOURCES_PATH),
            "layered_actor_issue": sha256(LAYERED_EDGES_PATH),
        },
        "interpretation_limit": RESEARCH_LIMIT,
    }
    (OUT / "metrics_v1.json").write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (OUT / "brief_v1.md").write_text(
        render_brief(
            scenarios,
            pairs,
            incidence,
            edge_source_incidence,
            diagnostics,
            leave_one_out,
        ),
        encoding="utf-8",
    )
    (OUT / "README.md").write_text(render_readme(), encoding="utf-8")
    (OUT / "validation_report.md").write_text(
        "# H1 documentation visibility validation\n\n"
        f"- status: PASS\n"
        f"- as_of_date: {AUDIT_DATE}\n"
        f"- current actors: {len(actors)}\n"
        f"- current active actor-issue edges: {len(edges)}\n"
        f"- current E3/E4 actor-issue edges: "
        f"{by_id['BASE_CURRENT_E3PLUS']['edge_count']}\n"
        f"- actor-source incidence: {len(incidence)} "
        f"({resolved_incidence} resolved; "
        f"{len(incidence) - resolved_incidence} unresolved legacy tokens)\n"
        "- source-host mappings: 3 proposals; producer/self-external/language "
        "remain unknown\n"
        f"- actor-issue edge×support rows: {len(edge_source_incidence)}\n"
        f"- E3/E4 edges without a resolved S source: "
        f"{len(edge_ids_without_resolved_source)}\n"
        f"- leave-one-source-out rows: {len(leave_one_out)}; "
        f"S004 removes {s004_loo['removed_edge_count']} edges and "
        f"{s004_loo['lost_observed_actor_count']} observed actors\n"
        f"- open follow-up tasks: {len(followup_tasks)}\n"
        "- display gate: research_only / research / candidate / ai_seeded / "
        "not_frontend_ready\n"
        "- central data writes: none\n",
        encoding="utf-8",
    )

    # Deterministic roundtrip checks.
    if read_csv(OUT / "sensitivity_scenarios_v1.csv") != scenarios:
        raise ValueError("scenario CSV roundtrip mismatch")
    if read_csv(OUT / "actor_source_incidence_v1.csv") != incidence:
        raise ValueError("incidence CSV roundtrip mismatch")
    if read_csv(OUT / "leave_one_source_out_v1.csv") != leave_one_out:
        raise ValueError("leave-one-source-out CSV roundtrip mismatch")
    print(
        "H1 documentation visibility OK: "
        f"{len(actors)} actors/{len(edges)} active edges; "
        f"E3+={by_id['BASE_CURRENT_E3PLUS']['edge_count']} edges/"
        f"{by_id['BASE_CURRENT_E3PLUS']['observed_actor_count']} actors; "
        f"source-big3={by_id['SOURCE_DROP_BIG3']['edge_count']}/"
        f"{by_id['SOURCE_DROP_BIG3']['observed_actor_count']}; "
        f"actor-big3={by_id['ACTOR_DROP_BIG3']['edge_count']}/"
        f"{by_id['ACTOR_DROP_BIG3']['observed_actor_count']}"
    )


if __name__ == "__main__":
    main()
