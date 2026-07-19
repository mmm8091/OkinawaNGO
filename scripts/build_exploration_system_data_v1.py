from __future__ import annotations

"""Build the single frontend data adapter for the exploration system.

The public interface is ``build_exploration_system_data(project_root,
output_dir)``. Callers do not interpret central CSV files themselves.
"""

import csv
import hashlib
import json
from pathlib import Path
from typing import Any


DEMO_RELATION_STATUSES = {"human_checked", "human_revised"}
DEMO_EPISODE_STATUSES = {
    "human_checked",
    "accepted_process",
    "accepted_process_with_local_gap",
}
INTERPRETATION_LIMITS = {
    "actor": (
        "Registry membership does not imply political stance, influence, alliance, "
        "or approval of every attached relation."
    ),
    "actor_issue": (
        "A documented issue association is not a measure of effort, influence, "
        "public support, or alliance."
    ),
    "actor_place": (
        "A documented place association is not organizational density, activity "
        "frequency, headquarters, or local support unless the relation basis says so."
    ),
    "strict_place_issue": (
        "Same-source coincidence supports a bounded actor-place-issue triple; it "
        "does not establish causality, duration, alliance, or policy effect."
    ),
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def split_refs(value: str) -> list[str]:
    return [item.strip() for item in value.replace(",", ";").split(";") if item.strip()]


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    path.write_text(payload, encoding="utf-8", newline="\n")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_source_aliases(
    source_rows: list[dict[str, str]],
    crosswalk_rows: list[dict[str, str]],
) -> dict[str, str]:
    aliases = {row["source_id"]: row["source_id"] for row in source_rows}
    for row in crosswalk_rows:
        module_id = row["module_source_id"]
        main_id = row["main_source_id"]
        if module_id and main_id:
            aliases[module_id] = main_id
    return aliases


def resolve_source_refs(
    refs: list[str], source_aliases: dict[str, str]
) -> tuple[list[str], list[str]]:
    resolved = sorted({source_aliases[ref] for ref in refs if ref in source_aliases})
    unresolved = sorted({ref for ref in refs if ref not in source_aliases})
    return resolved, unresolved


def build_actor_aliases(
    rows: list[dict[str, str]],
    source_aliases: dict[str, str],
) -> dict[str, list[dict[str, Any]]]:
    aliases_by_actor: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        source_ids, unresolved_source_refs = resolve_source_refs(
            split_refs(row["source_ref"]), source_aliases
        )
        aliases_by_actor.setdefault(row["actor_id"], []).append(
            {
                "label": row["alias"],
                "type": row["alias_type"],
                "source_ids": source_ids,
                "unresolved_source_refs": unresolved_source_refs,
            }
        )
    for aliases in aliases_by_actor.values():
        aliases.sort(key=lambda row: (row["type"], row["label"]))
    return aliases_by_actor


def normalize_actors(
    rows: list[dict[str, str]],
    source_aliases: dict[str, str],
    aliases_by_actor: dict[str, list[dict[str, Any]]],
) -> list[dict[str, Any]]:
    actors = []
    for row in rows:
        source_ids, unresolved_source_refs = resolve_source_refs(
            split_refs(row["source_refs"]), source_aliases
        )
        scope_status = row.get("scope_status", "")
        hidden = row["review_status"] == "rejected" or scope_status in {
            "merged_duplicate",
            "excluded",
        }
        actors.append({
            "id": row["actor_id"],
            "display_label": row["canonical_name"],
            "aliases": aliases_by_actor.get(row["actor_id"], []),
            "actor_class": row["actor_class"],
            "origin_type": row["origin_type"],
            "legal_status": row["legal_status_guess"],
            "primary_places": split_refs(row["primary_places"]),
            "issue_tags": split_refs(row["issue_tags"]),
            "source_ids": source_ids,
            "unresolved_source_refs": unresolved_source_refs,
            "evidence_level": row["evidence_level"],
            "review_status": row["review_status"],
            "scope_status": scope_status,
            "merged_duplicate_of": row.get("merged_duplicate_of", ""),
            "display_status": "hidden" if hidden else "demo",
            "interpretation_limit": INTERPRETATION_LIMITS["actor"],
        })
    return sorted(actors, key=lambda row: row["id"])


def normalize_places(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    places = [
        {
            "id": row["place_id"],
            "display_label": row["place_name"],
            "place_type": row["place_type"],
            "region": row["region"],
            "display_summary": row["why_relevant"],
            "phase1_priority": row["phase1_priority"],
            "display_status": "demo",
            "review_status": "taxonomy",
            "evidence_level": "",
            "source_ids": [],
            "interpretation_limit": (
                "A place node is a navigation and coding object; its visibility or "
                "number of linked records is not activity intensity."
            ),
        }
        for row in rows
    ]
    return sorted(places, key=lambda row: row["id"])


def normalize_issues(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    issues = [
        {
            "id": row["issue_id"],
            "display_label": row["issue_label"],
            "issue_group": row["issue_group"],
            "display_summary": row["definition"],
            "include_in_phase1": row["include_in_phase1"],
            "display_status": "demo",
            "review_status": "taxonomy",
            "evidence_level": "",
            "source_ids": [],
            "interpretation_limit": (
                "An issue label records a bounded documented association; it is not "
                "a measure of salience, effort, public support, or political stance."
            ),
        }
        for row in rows
    ]
    return sorted(issues, key=lambda row: row["id"])


def normalize_venues(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    venues = [
        {
            "id": row["venue_id"],
            "display_label": row["venue_label"],
            "venue_group": row["venue_group"],
            "display_summary": row["definition"],
            "phase1_use": split_refs(row["phase1_use"].replace("/", ";")),
            "display_status": "demo",
            "review_status": "taxonomy",
            "evidence_level": "",
            "source_ids": [],
            "interpretation_limit": row["notes"],
        }
        for row in rows
    ]
    return sorted(venues, key=lambda row: row["id"])


def normalize_sources(
    rows: list[dict[str, str]],
    archive_rows: list[dict[str, str]],
) -> list[dict[str, Any]]:
    archive_by_id = {row["source_id"]: row for row in archive_rows}
    sources = []
    for row in rows:
        archive = archive_by_id.get(row["source_id"], {})
        can_support = (
            row["evidence_level"] != "E0"
            and not row["review_status"].startswith("rejected")
        )
        sources.append(
            {
                "id": row["source_id"],
                "display_label": row["title"],
                "source_type": row["source_type"],
                "source_publication_date": row["year"],
                "event_date": "",
                "url": row["url"],
                "supports": row["what_it_supports"],
                "evidence_level": row["evidence_level"],
                "review_status": row["review_status"],
                "display_status": "infrastructure",
                "can_support_claim": can_support,
                "bias_note": row["bias_note"],
                "interpretation_limit": row["notes"],
                "archive_status": archive.get("archive_status", "missing"),
                "archive_path": archive.get("local_path", ""),
                "archive_sha256": archive.get("sha256", ""),
            }
        )
    return sorted(sources, key=lambda row: row["id"])


def normalize_evidence_notes(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    notes = [
        {
            "id": row["evidence_id"],
            "object_type": row["object_type"],
            "object_id": row["object_id"],
            "claim": row["claim"],
            "source_ids": [row["source_id"]] if row["source_id"] else [],
            "summary": row["evidence_summary_or_short_quote"],
            "locator": row["source_locator"],
            "locator_status": row["locator_status"],
            "evidence_level": row["evidence_level"],
            "review_status": row["reviewer_status"],
            "review_decision": row["review_decision"],
            "display_status": "demo",
            "interpretation_limit": row["interpretation_limit"],
        }
        for row in rows
    ]
    return sorted(notes, key=lambda row: row["id"])


def normalize_episodes(
    rows: list[dict[str, str]],
    source_aliases: dict[str, str],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    demo: list[dict[str, Any]] = []
    research: list[dict[str, Any]] = []
    for row in rows:
        source_refs = split_refs(row["source_refs"])
        source_ids, unresolved_source_refs = resolve_source_refs(
            source_refs, source_aliases
        )
        normalized = {
            "id": row["episode_id"],
            "display_label": row["short_label"],
            "module": row["module"],
            "case_ids": split_refs(row["case_id"].replace("/", ";")),
            "actor_ids": split_refs(row["actor_ids"]),
            "place_labels": split_refs(row["place"]),
            "route_family": row["route_family"],
            "local_problem": row["local_problem"],
            "translation_frame": row["translation_frame"],
            "venue_label": row["venue"],
            "observable_output": row["observable_output"],
            "substantive_result": row["substantive_result"],
            "stage_status": {
                "public_claim": row["public_claim"],
                "venue_entry": row["venue_entry"],
                "intermediate_output": row["intermediate_output"],
                "bounded_gain": row["bounded_gain"],
                "underlying_change": row["underlying_change"],
            },
            "source_ids": source_ids,
            "module_source_refs": sorted(
                ref for ref in source_refs if ref != source_aliases.get(ref)
            ),
            "unresolved_source_refs": unresolved_source_refs,
            "evidence_level": row["evidence_level"],
            "review_status": row["review_status"],
            "display_status": (
                "demo" if row["review_status"] in DEMO_EPISODE_STATUSES else "research"
            ),
            "interpretation_limit": row["interpretation_limit"],
        }
        (demo if normalized["display_status"] == "demo" else research).append(normalized)
    return (
        sorted(demo, key=lambda row: row["id"]),
        sorted(research, key=lambda row: row["id"]),
    )


def build_outcomes(episodes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    outcomes: list[dict[str, Any]] = []
    for episode in episodes:
        for tier, text_key in (
            ("intermediate_output", "observable_output"),
            ("bounded_gain", "substantive_result"),
            ("underlying_change", "substantive_result"),
        ):
            outcomes.append(
                {
                    "id": f"{episode['id']}:{tier}",
                    "episode_id": episode["id"],
                    "tier": tier,
                    "status": episode["stage_status"][tier],
                    "display_label": episode[text_key],
                    "source_ids": episode["source_ids"],
                    "evidence_level": episode["evidence_level"],
                    "review_status": episode["review_status"],
                    "display_status": episode["display_status"],
                    "interpretation_limit": episode["interpretation_limit"],
                }
            )
    return outcomes


def normalize_actor_issue(
    rows: list[dict[str, str]],
    source_aliases: dict[str, str],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    demo: list[dict[str, Any]] = []
    research: list[dict[str, Any]] = []
    for row in rows:
        if row["review_status"] == "rejected" or row.get("scope_status", "").startswith(
            "retired"
        ):
            continue
        source_ids, unresolved_source_refs = resolve_source_refs(
            split_refs(row["source_ref"]), source_aliases
        )
        normalized = {
            "id": row["edge_id"],
            "relation_type": "actor_issue",
            "actor_id": row["actor_id"],
            "issue_id": row["issue_id"],
            "relation_basis": row["relation_basis"],
            "source_ids": source_ids,
            "unresolved_source_refs": unresolved_source_refs,
            "evidence_level": row["evidence_level"],
            "review_status": row["review_status"],
            "display_status": (
                "demo" if row["review_status"] in DEMO_RELATION_STATUSES else "research"
            ),
            "interpretation_limit": INTERPRETATION_LIMITS["actor_issue"],
        }
        (demo if normalized["display_status"] == "demo" else research).append(normalized)
    return (
        sorted(demo, key=lambda row: row["id"]),
        sorted(research, key=lambda row: row["id"]),
    )


def normalize_actor_place(
    rows: list[dict[str, str]],
    source_aliases: dict[str, str],
    place_label_by_id: dict[str, str],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    demo: list[dict[str, Any]] = []
    research: list[dict[str, Any]] = []
    for row in rows:
        if row["review_status"] == "rejected" or row.get("scope_status", "").startswith(
            "retired"
        ):
            continue
        source_ids, unresolved_source_refs = resolve_source_refs(
            split_refs(row["source_ref"]), source_aliases
        )
        canonical_place_label = place_label_by_id.get(row["place_id"], "")
        place_key_label_conflict = bool(
            canonical_place_label
            and row["place_name"]
            and row["place_name"] != canonical_place_label
        )
        display_status = (
            "demo"
            if row["review_status"] in DEMO_RELATION_STATUSES
            and not place_key_label_conflict
            else "research"
        )
        normalized = {
            "id": row["edge_id"],
            "relation_type": "actor_place",
            "actor_id": row["actor_id"],
            "place_id": row["place_id"],
            "place_label": row["place_name"],
            "canonical_place_label": canonical_place_label,
            "relation_basis": row["relation_basis"],
            "source_ids": source_ids,
            "unresolved_source_refs": unresolved_source_refs,
            "evidence_level": row["evidence_level"],
            "review_status": row["review_status"],
            "display_status": display_status,
            "quarantine_reason": (
                "place_key_label_conflict" if place_key_label_conflict else ""
            ),
            "interpretation_limit": INTERPRETATION_LIMITS["actor_place"],
        }
        (demo if normalized["display_status"] == "demo" else research).append(normalized)
    return (
        sorted(demo, key=lambda row: row["id"]),
        sorted(research, key=lambda row: row["id"]),
    )


def normalize_strict_triples(
    rows: list[dict[str, str]],
    source_aliases: dict[str, str],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    demo: list[dict[str, Any]] = []
    research: list[dict[str, Any]] = []
    for row in rows:
        source_ids, unresolved_source_refs = resolve_source_refs(
            [row["shared_source_id"]], source_aliases
        )
        normalized = {
            "id": row["triple_id"],
            "relation_type": "strict_actor_place_issue",
            "actor_id": row["actor_id"],
            "place_id": row["place_id"],
            "issue_id": row["issue_id"],
            "frame_id": row["frame_id"],
            "frame_label": row["frame_name"],
            "source_ids": source_ids,
            "unresolved_source_refs": unresolved_source_refs,
            "event_ids": split_refs(row["event_ids"]),
            "event_dates": split_refs(row["event_dates"]),
            "evidence_level": min(
                row["place_evidence_level"], row["issue_evidence_level"]
            ),
            "review_status": row["triple_layer"],
            "display_status": (
                "demo"
                if row["triple_layer"] == "human_reviewed_same_source"
                else "research"
            ),
            "interpretation_limit": row["interpretation_limit"]
            or INTERPRETATION_LIMITS["strict_place_issue"],
        }
        (demo if normalized["display_status"] == "demo" else research).append(normalized)
    return (
        sorted(demo, key=lambda row: row["id"]),
        sorted(research, key=lambda row: row["id"]),
    )


def normalize_event_participation(
    rows: list[dict[str, str]],
    source_aliases: dict[str, str],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    demo: list[dict[str, Any]] = []
    research: list[dict[str, Any]] = []
    for row in rows:
        is_registry_actor = row["entity_type"] == "registry_actor"
        source_ids, unresolved_source_refs = resolve_source_refs(
            split_refs(row["source_id"]), source_aliases
        )
        normalized = {
            "id": row["record_id"],
            "relation_type": "event_participation",
            "event_id": row["event_id"],
            "event_label": row["event_name"],
            "event_date": row["event_year"],
            "actor_id": row["actor_or_counterpart_id"] if is_registry_actor else "",
            "participant_label": row["actor_or_counterpart_name"],
            "entity_type": row["entity_type"],
            "is_registry_actor": is_registry_actor,
            "action_type": row["action_type"],
            "venue_id": row["venue_id"],
            "target_type": row["target_type"],
            "target_id_or_name": row["target_id_or_name"],
            "role": row["role"],
            "pathway_stage": row["pathway_stage"],
            "source_ids": source_ids,
            "unresolved_source_refs": unresolved_source_refs,
            "evidence_level": row["evidence_level"],
            "review_status": row["reviewer_status"],
            "display_status": (
                "demo" if row["reviewer_status"] == "human_checked" else "research"
            ),
            "interpretation_limit": row["interpretation_limit"],
        }
        (demo if normalized["display_status"] == "demo" else research).append(normalized)
    return (
        sorted(demo, key=lambda row: row["id"]),
        sorted(research, key=lambda row: row["id"]),
    )


def normalize_legal_roles(
    rows: list[dict[str, str]],
    source_aliases: dict[str, str],
) -> list[dict[str, Any]]:
    roles = []
    for row in rows:
        is_registry_actor = bool(row["actor_id"])
        source_ids, unresolved_source_refs = resolve_source_refs(
            split_refs(row["source_refs"]), source_aliases
        )
        roles.append(
            {
                "id": row["role_id"],
                "relation_type": "legal_role",
                "case_id": row["case_id"],
                "actor_id": row["actor_id"],
                "provisional_entity_id": row["provisional_entity_id"],
                "display_label": row["actor_name"],
                "entity_kind": row["entity_kind"],
                "is_registry_actor": is_registry_actor,
                "role": row["role"],
                "role_family": row["role_family"],
                "side": row["side"],
                "target_or_recipient": row["target_or_recipient"],
                "source_ids": source_ids,
                "unresolved_source_refs": unresolved_source_refs,
                "evidence_level": row["evidence_level"],
                "review_status": row["review_status"],
                "display_status": "demo",
                "interpretation_limit": row["interpretation_limit"],
            }
        )
    return sorted(roles, key=lambda row: row["id"])


def build_actor_episode_relations(
    episodes: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows = []
    for episode in episodes:
        for actor_id in episode["actor_ids"]:
            rows.append(
                {
                    "id": f"{episode['id']}:{actor_id}",
                    "relation_type": "actor_episode",
                    "actor_id": actor_id,
                    "episode_id": episode["id"],
                    "source_ids": episode["source_ids"],
                    "evidence_level": episode["evidence_level"],
                    "review_status": episode["review_status"],
                    "display_status": episode["display_status"],
                    "interpretation_limit": episode["interpretation_limit"],
                }
            )
    return sorted(rows, key=lambda row: row["id"])


def normalize_coverage_cells(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    cells = []
    for row in rows:
        cells.append(
            {
                "dimension_id": row["dimension_id"],
                "dimension_label": row["dimension_label"],
                "facet": row["facet"],
                "category": row["category"],
                "subcategory": row["subcategory"],
                "count": int(row["count"]),
                "denominator": int(row["denominator"]),
                "share_pct": float(row["share_pct"]),
                "unit": row["unit"],
                "inclusion_rule": row["inclusion_rule"],
                "interpretation_limit": row["interpretive_limit"],
            }
        )
    return cells


def normalize_coverage_implications(
    rows: list[dict[str, str]],
) -> list[dict[str, Any]]:
    return [
        {
            "dimension_id": row["dimension_id"],
            "dimension_label": row["dimension_label"],
            "observed_skew": row["observed_skew"],
            "visibility_mechanism": row["visibility_mechanism"],
            "impact_on_q1_q3": row["impact_on_q1_q3"],
            "affected_modules": split_refs(row["affected_modules"]),
            "interpretation_limit": row["interpretation_boundary"],
            "online_gap_action": row["online_gap_action"],
            "local_gap_action": row["local_gap_action"],
        }
        for row in rows
    ]


def build_views(
    actors: list[dict[str, Any]],
    places: list[dict[str, Any]],
    issues: list[dict[str, Any]],
    venues: list[dict[str, Any]],
    episodes: list[dict[str, Any]],
    relations: dict[str, list[dict[str, Any]]],
    coverage_cells: list[dict[str, Any]],
    coverage_implications: list[dict[str, Any]],
    map_geometry: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    regions: dict[str, list[str]] = {}
    for place in places:
        regions.setdefault(place["region"] or "unassigned", []).append(place["id"])
    event_anchors: dict[str, dict[str, str]] = {}
    for row in relations["event_participation"]:
        if not row["event_id"]:
            continue
        event_anchors[row["event_id"]] = {
            "id": row["event_id"],
            "display_label": row["event_label"],
            "event_date": row["event_date"],
            "anchor_type": "event",
            "review_status": row["review_status"],
        }
    coverage_periods = [
        cell
        for cell in coverage_cells
        if cell["dimension_id"] == "D1" and cell["facet"] == "source_year_period"
    ]
    return {
        "overview": {
            "view_id": "P1",
            "route": "/",
            "question": "哪里正在发生什么？",
            "visual_engine": "V1 全域地点—议题研究地图",
            "visual_states": ["all_regions", "strict_evidence", "sakishima_focus", "compare"],
            "map_geometry": {
                "path": "../demo/map_geometry.geojson",
                "type": map_geometry.get("type", ""),
                "feature_count": len(map_geometry.get("features", [])),
                "region_codes": sorted(
                    {
                        feature.get("properties", {}).get("region", "")
                        for feature in map_geometry.get("features", [])
                        if feature.get("properties", {}).get("region", "")
                    }
                ),
            },
            "place_ids": [row["id"] for row in places],
            "issue_ids": [row["id"] for row in issues],
            "regions": {key: sorted(value) for key, value in sorted(regions.items())},
            "actor_place_relation_ids": [
                row["id"] for row in relations["actor_place"]
            ],
            "strict_place_issue_relation_ids": [
                row["id"] for row in relations["strict_place_issue"]
            ],
            "interpretation_limits": [
                "The map is a navigation and evidence view, not an estimate of organizational density.",
                "Only human-reviewed same-source triples appear in strict evidence mode.",
            ],
        },
        "actors": {
            "view_id": "P2",
            "route": "/actors",
            "question": "谁在参与，以什么功能参与？",
            "visual_engine": "V2 组织—议题生态图",
            "visual_states": ["ecology", "issue_links", "focus", "compare"],
            "actor_ids": [row["id"] for row in actors],
            "issue_ids": [row["id"] for row in issues],
            "actor_issue_relation_ids": [
                row["id"] for row in relations["actor_issue"]
            ],
            "actor_episode_relation_ids": [
                row["id"] for row in relations["actor_episode"]
            ],
            "filter_fields": [
                "actor_class",
                "origin_type",
                "legal_status",
                "place_id",
                "issue_id",
                "review_status",
            ],
            "interpretation_limits": [
                "Registry composition is a working public-material sample, not a census.",
                "Degree, area, and repeated participation must not be labeled influence or alliance.",
            ],
        },
        "pathways": {
            "view_id": "P3",
            "route": "/pathways",
            "question": "行动如何进入事件与制度场域？",
            "visual_engine": "V3 问题—行动—场域—产出路径图",
            "visual_states": ["case_focus", "route_family", "venue_compare", "object_compare"],
            "episode_ids": [row["id"] for row in episodes],
            "venue_ids": [row["id"] for row in venues],
            "event_participation_relation_ids": [
                row["id"] for row in relations["event_participation"]
            ],
            "legal_role_relation_ids": [
                row["id"] for row in relations["legal_roles"]
            ],
            "route_families": sorted({row["route_family"] for row in episodes}),
            "stage_order": [
                "local_problem",
                "translation_frame",
                "venue_entry",
                "intermediate_output",
                "bounded_gain",
                "underlying_change",
            ],
            "interpretation_limits": [
                "Sequence is not causality; venue entry is not success.",
                "Intermediate output is not automatically policy or project change.",
            ],
        },
        "evidence_coverage": {
            "view_id": "P4",
            "route": "/evidence",
            "question": "当前材料能支持什么、遗漏什么？",
            "visual_engine": "V4 证据覆盖与偏差图",
            "dimensions": sorted(
                {cell["dimension_id"] for cell in coverage_cells}
            ),
            "cells": coverage_cells,
            "implications": coverage_implications,
            "interpretation_limits": [
                "Coverage describes documentary visibility in the working sample, not population coverage.",
                "Source publication date, event date, claim period, and actor active period are distinct.",
            ],
        },
        "global": {
            "view_id": "G1+G2",
            "time_layer": {
                "historical_anchor_ids": [],
                "event_anchors": [
                    event_anchors[key] for key in sorted(event_anchors)
                ],
                "coverage_periods": coverage_periods,
                "interpretation_limit": (
                    "The empty historical-anchor collection is explicit. Event and "
                    "source dates must not be used to fabricate organizational continuity."
                ),
            },
            "evidence_drawer": {
                "required_fields": [
                    "source_id",
                    "source_publication_date",
                    "event_date",
                    "locator",
                    "evidence_level",
                    "review_status",
                    "archive_status",
                    "interpretation_limit",
                ],
                "max_click_depth": 3,
            },
            "cross_page_state": {
                "keys": [
                    "actor_ids",
                    "place_ids",
                    "issue_ids",
                    "episode_ids",
                    "time_range",
                    "display_layer",
                ],
                "display_layer_default": "demo",
            },
        },
    }


def validate_build(
    *,
    actors: list[dict[str, Any]],
    places: list[dict[str, Any]],
    issues: list[dict[str, Any]],
    venues: list[dict[str, Any]],
    sources: list[dict[str, Any]],
    evidence_notes: list[dict[str, Any]],
    demo_episodes: list[dict[str, Any]],
    research_episodes: list[dict[str, Any]],
    demo_relations: dict[str, list[dict[str, Any]]],
    research_relations: dict[str, list[dict[str, Any]]],
    coverage_cells: list[dict[str, Any]],
    case_ids: set[str],
    map_geometry: dict[str, Any],
) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    checks: list[dict[str, str]] = []

    def check(name: str, condition: bool, detail: str) -> None:
        status = "pass" if condition else "fail"
        checks.append({"name": name, "status": status, "detail": detail})
        if not condition:
            errors.append(f"{name}: {detail}")

    def unique_ids(name: str, rows: list[dict[str, Any]]) -> set[str]:
        ids = [row["id"] for row in rows]
        check(name, len(ids) == len(set(ids)), f"{len(ids)} rows")
        return set(ids)

    actor_ids = unique_ids("unique actor IDs", actors)
    place_ids = unique_ids("unique place IDs", places)
    issue_ids = unique_ids("unique issue IDs", issues)
    venue_ids = unique_ids("unique venue IDs", venues)
    source_ids = unique_ids("unique source IDs", sources)
    evidence_ids = unique_ids("unique evidence IDs", evidence_notes)
    demo_episode_ids = unique_ids("unique demo episode IDs", demo_episodes)
    research_episode_ids = unique_ids(
        "unique research episode IDs", research_episodes
    )
    check(
        "episode layers disjoint",
        demo_episode_ids.isdisjoint(research_episode_ids),
        f"demo={len(demo_episode_ids)} research={len(research_episode_ids)}",
    )

    relation_ids: list[str] = []
    for rows in demo_relations.values():
        relation_ids.extend(row["id"] for row in rows)
    check(
        "unique demo relation IDs within relation type",
        all(
            len(rows) == len({row["id"] for row in rows})
            for rows in demo_relations.values()
        ),
        f"{len(relation_ids)} relation rows",
    )

    check(
        "actor-issue references",
        all(
            row["actor_id"] in actor_ids and row["issue_id"] in issue_ids
            for row in demo_relations["actor_issue"]
        ),
        f"{len(demo_relations['actor_issue'])} demo rows",
    )
    check(
        "actor-place references",
        all(
            row["actor_id"] in actor_ids
            and row["place_id"] in place_ids
            and row["place_label"] == row["canonical_place_label"]
            for row in demo_relations["actor_place"]
        ),
        f"{len(demo_relations['actor_place'])} demo rows with matching place key/label",
    )
    check(
        "strict triple references",
        all(
            row["actor_id"] in actor_ids
            and row["place_id"] in place_ids
            and row["issue_id"] in issue_ids
            for row in demo_relations["strict_place_issue"]
        ),
        f"{len(demo_relations['strict_place_issue'])} demo rows",
    )
    check(
        "actor-episode references",
        all(
            row["actor_id"] in actor_ids
            and row["episode_id"] in demo_episode_ids
            for row in demo_relations["actor_episode"]
        ),
        f"{len(demo_relations['actor_episode'])} demo rows",
    )
    check(
        "event participation references",
        all(
            (not row["is_registry_actor"] or row["actor_id"] in actor_ids)
            and row["venue_id"] in venue_ids
            for row in demo_relations["event_participation"]
        ),
        f"{len(demo_relations['event_participation'])} demo rows",
    )
    check(
        "legal role references",
        all(
            (not row["actor_id"] or row["actor_id"] in actor_ids)
            and row["case_id"] in case_ids
            for row in demo_relations["legal_roles"]
        ),
        f"{len(demo_relations['legal_roles'])} demo rows",
    )

    source_ref_rows: list[dict[str, Any]] = (
        actors
        + demo_episodes
        + research_episodes
        + evidence_notes
        + [
            row
            for layer in (demo_relations, research_relations)
            for rows in layer.values()
            for row in rows
        ]
    )
    unresolved = sorted(
        {
            source_id
            for row in source_ref_rows
            for source_id in row.get("source_ids", [])
            if source_id not in source_ids
        }
    )
    check(
        "all normalized source IDs resolve",
        not unresolved,
        "unresolved=" + (";".join(unresolved) if unresolved else "0"),
    )
    demo_unresolved_refs = sorted(
        {
            ref
            for row in demo_episodes
            + [
                relation
                for rows in demo_relations.values()
                for relation in rows
            ]
            for ref in row.get("unresolved_source_refs", [])
        }
    )
    check(
        "demo rows have no unresolved source references",
        not demo_unresolved_refs,
        "unresolved="
        + (";".join(demo_unresolved_refs) if demo_unresolved_refs else "0"),
    )
    check(
        "demo status gate",
        all(
            row["display_status"] == "demo"
            for rows in demo_relations.values()
            for row in rows
        )
        and all(
            row["review_status"] in DEMO_EPISODE_STATUSES
            for row in demo_episodes
        ),
        "candidate and analytical episode layers excluded",
    )
    check(
        "research status isolation",
        all(
            row["display_status"] == "research"
            for rows in research_relations.values()
            for row in rows
        )
        and all(
            row["display_status"] == "research" for row in research_episodes
        ),
        "research rows remain explicitly marked",
    )
    check(
        "event-only names do not enter actor collection",
        all(row["id"] in actor_ids for row in actors)
        and not any(row.get("entity_type") for row in actors),
        f"actors={len(actors)}",
    )
    rejected = [row for row in sources if row["evidence_level"] == "E0"]
    check(
        "E0 sources cannot support claims",
        all(not row["can_support_claim"] for row in rejected),
        f"E0 sources={len(rejected)}",
    )
    check(
        "archive manifest coverage",
        all(row["archive_status"] != "missing" for row in sources),
        f"sources={len(sources)}",
    )
    check(
        "coverage dimensions complete",
        {row["dimension_id"] for row in coverage_cells}
        == {"D1", "D2", "D3", "D4", "D5", "D6"},
        f"cells={len(coverage_cells)}",
    )
    check(
        "map geometry packaged",
        map_geometry.get("type") == "FeatureCollection"
        and bool(map_geometry.get("features"))
        and all(
            feature.get("geometry", {}).get("type") in {"Polygon", "MultiPolygon"}
            and feature.get("properties", {}).get("name")
            and feature.get("properties", {}).get("region")
            for feature in map_geometry.get("features", [])
        ),
        f"features={len(map_geometry.get('features', []))}",
    )

    non_human_actor_status = sum(
        row["review_status"] not in DEMO_RELATION_STATUSES for row in actors
    )
    warnings.append(
        f"{non_human_actor_status} registry actors retain non-human review_status; "
        "registry membership is admitted for identity browsing, while their relations "
        "remain independently gated."
    )
    warnings.append(
        "historical_anchors is intentionally empty until NR-04/NR-05 candidates receive "
        "human continuity decisions."
    )
    warnings.append(
        "The packaged GeoJSON supports municipality/region rendering, but the 20 place "
        "nodes have no approved point coordinates or municipality crosswalk; NR-03 must "
        "not invent precise site markers."
    )
    non_registry_participants = sum(
        not row["is_registry_actor"]
        for row in demo_relations["event_participation"]
    )
    warnings.append(
        f"{non_registry_participants} human-checked event participants are preserved "
        "only as typed participation records and never enter actors.json."
    )
    actor_unresolved_refs = sorted(
        {
            ref
            for row in actors
            for ref in row.get("unresolved_source_refs", [])
        }
    )
    if actor_unresolved_refs:
        warnings.append(
            f"{len(actor_unresolved_refs)} legacy actor identity references are not "
            f"central source IDs and remain explicit on registry objects: "
            f"{';'.join(actor_unresolved_refs)}."
        )
    research_unresolved_refs = sorted(
        {
            ref
            for row in research_episodes
            + [
                relation
                for rows in research_relations.values()
                for relation in rows
            ]
            for ref in row.get("unresolved_source_refs", [])
        }
    )
    if research_unresolved_refs:
        warnings.append(
            f"{len(research_unresolved_refs)} unresolved legacy research references "
            f"remain isolated from demo: {';'.join(research_unresolved_refs)}."
        )
    quarantined_place_edges = [
        row
        for row in research_relations["actor_place"]
        if row.get("quarantine_reason") == "place_key_label_conflict"
    ]
    if quarantined_place_edges:
        warnings.append(
            f"{len(quarantined_place_edges)} human-reviewed actor-place edge is "
            "quarantined for a place key/label conflict: "
            + ";".join(row["id"] for row in quarantined_place_edges)
            + "."
        )
    return {
        "status": "pass" if not errors else "fail",
        "error_count": len(errors),
        "warning_count": len(warnings),
        "checks": checks,
        "errors": errors,
        "warnings": warnings,
        "evidence_ids_checked": len(evidence_ids),
    }


def render_validation_report(
    validation: dict[str, Any], counts: dict[str, Any]
) -> str:
    lines = [
        "# Exploration system data v1 — validation report",
        "",
        f"Status: **{validation['status'].upper()}**",
        "",
        "## Checks",
        "",
    ]
    for item in validation["checks"]:
        marker = "PASS" if item["status"] == "pass" else "FAIL"
        lines.append(f"- {marker} — {item['name']}: {item['detail']}")
    lines.extend(["", "## Warnings", ""])
    lines.extend(f"- {warning}" for warning in validation["warnings"])
    lines.extend(
        [
            "",
            "## Build counts",
            "",
            "```json",
            json.dumps(counts, ensure_ascii=False, indent=2, sort_keys=True),
            "```",
            "",
            "The warnings are explicit research boundaries, not failed validation.",
            "",
        ]
    )
    return "\n".join(lines)


def build_exploration_system_data(project_root: Path, output_dir: Path) -> dict[str, Any]:
    project_root = project_root.resolve()
    output_dir = output_dir.resolve()
    inputs = {
        "actors": project_root / "data/interim/01_actor_registry_initial_v0.csv",
        "actor_aliases": project_root
        / "data/interim/02_actor_aliases_initial_v0.csv",
        "places": project_root / "data/interim/04_place_registry_v0.csv",
        "issues": project_root / "data/interim/03_issue_taxonomy_v0.csv",
        "sources": project_root / "data/interim/05_source_log_initial_v0.csv",
        "evidence_notes": project_root / "data/interim/06_evidence_notes_v0.csv",
        "actor_issue": project_root / "data/interim/07_actor_issue_edges_initial_v0.csv",
        "actor_place": project_root / "data/interim/08_actor_place_edges_initial_v0.csv",
        "event_participation": project_root / "data/interim/09_actor_event_venue_edges_v0.csv",
        "legal_roles": project_root / "data/interim/18_legal_policy_actor_roles_v0.csv",
        "venues": project_root / "data/metadata/venue_taxonomy_v0.csv",
        "episodes": project_root
        / "outputs/translation_episode_comparison_v1/translation_episode_candidates_v1.csv",
        "strict_triples": project_root
        / "outputs/R03_strict_place_issue_v1/same_source_actor_place_issue_triples_v1.csv",
        "source_crosswalk": project_root
        / "outputs/phase1_source_integration_v1/module_source_crosswalk_v1.csv",
        "coverage_cells": project_root
        / "data/interim/27_coverage_audit_cells_v1.csv",
        "coverage_implications": project_root
        / "outputs/coverage_audit_v1/coverage_bias_implications_v1.csv",
        "archive_manifest": project_root
        / "source_docs/source_archive/source_archive_manifest.csv",
        "legal_cases": project_root
        / "data/interim/17_legal_policy_procedure_cases_v0.csv",
        "map_geometry": project_root
        / "outputs/learning_v1/okinawa_municipal_boundaries_simplified_v1.geojson",
    }
    missing = [str(path) for path in inputs.values() if not path.exists()]
    if missing:
        raise FileNotFoundError("Missing NR-02 inputs: " + "; ".join(missing))

    source_rows = read_csv(inputs["sources"])
    source_aliases = build_source_aliases(
        source_rows, read_csv(inputs["source_crosswalk"])
    )
    actor_rows = read_csv(inputs["actors"])
    actor_alias_rows = read_csv(inputs["actor_aliases"])
    actor_ids_from_source = {row["actor_id"] for row in actor_rows}
    orphan_alias_actor_ids = sorted(
        {row["actor_id"] for row in actor_alias_rows} - actor_ids_from_source
    )
    if orphan_alias_actor_ids:
        raise ValueError(
            "Actor aliases reference unknown actor IDs: "
            + ";".join(orphan_alias_actor_ids)
        )
    actor_aliases = build_actor_aliases(actor_alias_rows, source_aliases)
    actors = normalize_actors(
        actor_rows, source_aliases, actor_aliases
    )
    places = normalize_places(read_csv(inputs["places"]))
    issues = normalize_issues(read_csv(inputs["issues"]))
    venues = normalize_venues(read_csv(inputs["venues"]))
    sources = normalize_sources(
        source_rows, read_csv(inputs["archive_manifest"])
    )
    evidence_notes = normalize_evidence_notes(read_csv(inputs["evidence_notes"]))
    demo_episodes, research_episodes = normalize_episodes(
        read_csv(inputs["episodes"]), source_aliases
    )
    demo_outcomes = build_outcomes(demo_episodes)
    research_outcomes = build_outcomes(research_episodes)
    demo_actor_issue, research_actor_issue = normalize_actor_issue(
        read_csv(inputs["actor_issue"]), source_aliases
    )
    demo_actor_place, research_actor_place = normalize_actor_place(
        read_csv(inputs["actor_place"]),
        source_aliases,
        {row["id"]: row["display_label"] for row in places},
    )
    demo_strict, research_strict = normalize_strict_triples(
        read_csv(inputs["strict_triples"]), source_aliases
    )
    demo_events, research_events = normalize_event_participation(
        read_csv(inputs["event_participation"]), source_aliases
    )
    legal_roles = normalize_legal_roles(
        read_csv(inputs["legal_roles"]), source_aliases
    )
    demo_actor_episode = build_actor_episode_relations(demo_episodes)
    research_actor_episode = build_actor_episode_relations(research_episodes)
    coverage_cells = normalize_coverage_cells(read_csv(inputs["coverage_cells"]))
    coverage_implications = normalize_coverage_implications(
        read_csv(inputs["coverage_implications"])
    )
    map_geometry = read_json(inputs["map_geometry"])

    demo_relations = {
        "actor_issue": demo_actor_issue,
        "actor_place": demo_actor_place,
        "strict_place_issue": demo_strict,
        "actor_episode": demo_actor_episode,
        "event_participation": demo_events,
        "legal_roles": legal_roles,
    }
    research_relations = {
        "actor_issue": research_actor_issue,
        "actor_place": research_actor_place,
        "strict_place_issue": research_strict,
        "actor_episode": research_actor_episode,
        "event_participation": research_events,
    }
    candidates = {
        "episodes": research_episodes,
        "outcomes": research_outcomes,
        "relations": research_relations,
    }

    write_json(output_dir / "demo/actors.json", actors)
    write_json(output_dir / "demo/places.json", places)
    write_json(output_dir / "demo/issues.json", issues)
    write_json(output_dir / "demo/episodes.json", demo_episodes)
    write_json(output_dir / "demo/venues.json", venues)
    write_json(output_dir / "demo/outcomes.json", demo_outcomes)
    write_json(
        output_dir / "demo/evidence.json",
        {"sources": sources, "notes": evidence_notes},
    )
    write_json(output_dir / "demo/historical_anchors.json", [])
    write_json(output_dir / "demo/relations.json", demo_relations)
    write_json(output_dir / "demo/map_geometry.geojson", map_geometry)
    write_json(output_dir / "research/candidates.json", candidates)
    views = build_views(
        actors,
        places,
        issues,
        venues,
        demo_episodes,
        demo_relations,
        coverage_cells,
        coverage_implications,
        map_geometry,
    )
    for name, view in views.items():
        write_json(output_dir / f"views/{name}.json", view)

    counts = {
        "demo": {
            "actors": len(actors),
            "actor_aliases": sum(len(row["aliases"]) for row in actors),
            "places": len(places),
            "issues": len(issues),
            "episodes": len(demo_episodes),
            "venues": len(venues),
            "outcomes": len(demo_outcomes),
            "sources": len(sources),
            "evidence_notes": len(evidence_notes),
            "historical_anchors": 0,
            "map_geometry_features": len(map_geometry.get("features", [])),
            "relations": {
                key: len(value) for key, value in sorted(demo_relations.items())
            },
        },
        "research": {
            "episodes": len(research_episodes),
            "outcomes": len(research_outcomes),
            "relations": {
                key: len(value) for key, value in sorted(research_relations.items())
            },
        },
    }
    validation = validate_build(
        actors=actors,
        places=places,
        issues=issues,
        venues=venues,
        sources=sources,
        evidence_notes=evidence_notes,
        demo_episodes=demo_episodes,
        research_episodes=research_episodes,
        demo_relations=demo_relations,
        research_relations=research_relations,
        coverage_cells=coverage_cells,
        case_ids={row["case_id"] for row in read_csv(inputs["legal_cases"])},
        map_geometry=map_geometry,
    )
    validation_report = output_dir / "validation_report.md"
    validation_report.write_text(
        render_validation_report(validation, counts),
        encoding="utf-8",
        newline="\n",
    )
    if validation["status"] != "pass":
        raise ValueError("NR-02 validation failed: " + "; ".join(validation["errors"]))

    input_hashes = {key: sha256(path) for key, path in sorted(inputs.items())}
    generated_files = sorted(
        [
            "demo/actors.json",
            "demo/places.json",
            "demo/issues.json",
            "demo/episodes.json",
            "demo/venues.json",
            "demo/outcomes.json",
            "demo/evidence.json",
            "demo/historical_anchors.json",
            "demo/relations.json",
            "demo/map_geometry.geojson",
            "research/candidates.json",
            "views/overview.json",
            "views/actors.json",
            "views/pathways.json",
            "views/evidence_coverage.json",
            "views/global.json",
            "validation_report.md",
        ]
    )
    output_hashes = {
        relative: sha256(output_dir / relative) for relative in generated_files
    }
    fingerprint_payload = json.dumps(
        input_hashes, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    build_id = hashlib.sha256(fingerprint_payload).hexdigest()[:16]
    manifest = {
        "artifact": "exploration_system_data_v1",
        "schema_version": "1.0.0",
        "as_of_date": "2026-07-18",
        "build_id": build_id,
        "deterministic": True,
        "source_of_truth": "central research tables; derived outputs never write back",
        "counts": counts,
        "input_hashes": input_hashes,
        "output_hashes": output_hashes,
        "validation": {
            "status": validation["status"],
            "error_count": validation["error_count"],
            "warning_count": validation["warning_count"],
        },
    }
    write_json(output_dir / "manifest.json", manifest)
    return manifest


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    report = build_exploration_system_data(root, root / "outputs" / "exploration_system_data_v1")
    print(json.dumps(report["counts"], ensure_ascii=False, sort_keys=True))
