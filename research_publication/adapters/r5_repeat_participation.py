from __future__ import annotations

"""Publication adapter for R5 sampled public-list participation.

The external interface is deliberately one function.  All identity-tier
handling, repeat derivation, formal-table cross-checks, and interpretation
limits stay behind this seam so a frontend cannot accidentally turn
co-appearance into an actor relation.
"""

import csv
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path
from typing import Any, Iterable


R5_DIR = Path("outputs/R05_coaction_v1")
PARTICIPATION_FILE = "actor_event_bipartite_edges_v0.csv"
EVENT_FILE = "event_catalog_v0.csv"
BRIDGE_FILE = "repeat_participation_bridges_v0.csv"
OVERLAP_FILE = "event_overlap_v0.csv"
SOURCE_FILE = "source_register_v0.csv"

IDENTITY_STATUSES = {
    "registry_actor",
    "event_only_identity_human_checked",
    "event_only_name",
}
PARTICIPANT_TIERS = {
    "registry_actor": "registry_actor",
    "event_only_identity_human_checked": "human_reviewed_event_only_identity",
    "event_only_name": "other_event_only_name",
}
REPEAT_INTERPRETATION_LIMIT = (
    "Strict repeated identity across the sampled public actions only; it is "
    "not evidence of a stable alliance, membership, funding, hierarchy, "
    "continuous coordination, organizational continuity, or influence."
)
OBSERVATION_INTERPRETATION_LIMIT = (
    "One source-list row records publicly listed participation in one sampled "
    "event only; it is not an actor-to-actor relation."
)


class R5PublicationAdapterError(ValueError):
    """Raised when the current formal R5 tables disagree at the publication seam."""


def _read_csv(path: Path) -> list[dict[str, str]]:
    try:
        with path.open(encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
    except FileNotFoundError as exc:
        raise R5PublicationAdapterError(
            f"Required formal R5 table is missing: {path}"
        ) from exc
    if not rows:
        raise R5PublicationAdapterError(f"Required formal R5 table is empty: {path}")
    return rows


def _split(value: str) -> list[str]:
    return [item.strip() for item in value.split(";") if item.strip()]


def _integer(value: str, *, field: str, row_id: str) -> int:
    try:
        return int(value)
    except (TypeError, ValueError) as exc:
        raise R5PublicationAdapterError(
            f"{row_id} has a non-integer {field}: {value!r}"
        ) from exc


def _unique_lookup(
    rows: Iterable[dict[str, str]], key: str, *, table: str
) -> dict[str, dict[str, str]]:
    lookup: dict[str, dict[str, str]] = {}
    for row in rows:
        value = row.get(key, "")
        if not value:
            raise R5PublicationAdapterError(f"{table} contains a blank {key}")
        if value in lookup:
            raise R5PublicationAdapterError(
                f"{table} contains duplicate {key}: {value}"
            )
        lookup[value] = row
    return lookup


def _strict_identity_key(row: dict[str, str]) -> str | None:
    status = row["identity_status"]
    if status == "registry_actor":
        actor_id = row["actor_id"]
        if not actor_id or row["entity_key"] != f"ACTOR:{actor_id}":
            raise R5PublicationAdapterError(
                f"{row['participant_key']} has an invalid registry identity key"
            )
        if row["identity_group_id"]:
            raise R5PublicationAdapterError(
                f"{row['participant_key']} mixes registry and event-only identity keys"
            )
        return row["entity_key"]
    if status == "event_only_identity_human_checked":
        identity_group_id = row["identity_group_id"]
        if (
            row["actor_id"]
            or not identity_group_id
            or row["entity_key"] != f"EVENT_ONLY:{identity_group_id}"
        ):
            raise R5PublicationAdapterError(
                f"{row['participant_key']} has an invalid reviewed event-only identity"
            )
        return row["entity_key"]
    if status == "event_only_name":
        if (
            row["actor_id"]
            or row["identity_group_id"]
            or not row["entity_key"].startswith("NAME:")
        ):
            raise R5PublicationAdapterError(
                f"{row['participant_key']} improperly promotes an event-only name"
            )
        return None
    raise R5PublicationAdapterError(
        f"{row['participant_key']} has an unsupported identity status: {status}"
    )


def _jaccard(left: set[str], right: set[str]) -> float:
    union = left | right
    return round(len(left & right) / len(union), 4) if union else 0.0


def _validate_sources(
    source_rows: list[dict[str, str]],
    referenced_source_ids: set[str],
) -> dict[str, dict[str, str]]:
    source_lookup = _unique_lookup(source_rows, "source_ref", table=SOURCE_FILE)
    missing = sorted(referenced_source_ids - set(source_lookup))
    if missing:
        raise R5PublicationAdapterError(
            f"Formal R5 rows reference sources absent from {SOURCE_FILE}: {missing}"
        )
    return source_lookup


def _derive_identity_events(
    observations: list[dict[str, str]],
) -> tuple[
    dict[str, set[str]],
    dict[str, list[dict[str, str]]],
    dict[str, str],
]:
    identity_events: dict[str, set[str]] = defaultdict(set)
    identity_rows: dict[str, list[dict[str, str]]] = defaultdict(list)
    identity_status: dict[str, str] = {}
    seen_identity_event: set[tuple[str, str]] = set()
    for row in observations:
        key = _strict_identity_key(row)
        if key is None:
            continue
        pair = (key, row["event_id"])
        if pair in seen_identity_event:
            raise R5PublicationAdapterError(
                f"Strict identity {key} occurs more than once in {row['event_id']}"
            )
        seen_identity_event.add(pair)
        previous = identity_status.setdefault(key, row["identity_status"])
        if previous != row["identity_status"]:
            raise R5PublicationAdapterError(
                f"Strict identity {key} crosses incompatible identity tiers"
            )
        identity_events[key].add(row["event_id"])
        identity_rows[key].append(row)
    return dict(identity_events), dict(identity_rows), identity_status


def _validate_event_catalog(
    observations: list[dict[str, str]],
    events: list[dict[str, str]],
) -> tuple[list[str], dict[str, Counter[str]]]:
    event_lookup = _unique_lookup(events, "event_id", table=EVENT_FILE)
    observed_event_ids = {row["event_id"] for row in observations}
    if observed_event_ids != set(event_lookup):
        raise R5PublicationAdapterError(
            "Participation and event-catalog event IDs do not match: "
            f"participation_only={sorted(observed_event_ids - set(event_lookup))}, "
            f"catalog_only={sorted(set(event_lookup) - observed_event_ids)}"
        )
    event_order = [
        row["event_id"]
        for row in sorted(
            events, key=lambda row: (row["event_date"], row["event_id"])
        )
    ]
    counts: dict[str, Counter[str]] = {}
    for event_id in event_order:
        event_rows = [row for row in observations if row["event_id"] == event_id]
        identity_counts = Counter(row["identity_status"] for row in event_rows)
        event = event_lookup[event_id]
        expected = {
            "structured_participant_count": len(event_rows),
            "registry_actor_rows": identity_counts["registry_actor"],
            "human_reviewed_event_only_rows": identity_counts[
                "event_only_identity_human_checked"
            ],
            "event_only_name_rows": identity_counts["event_only_name"],
            "alias_pending_rows": 0,
        }
        for field, derived in expected.items():
            recorded = _integer(event[field], field=field, row_id=event_id)
            if recorded != derived:
                raise R5PublicationAdapterError(
                    f"{event_id} {field} disagrees with row-level observations: "
                    f"recorded={recorded}, derived={derived}"
                )
        if any(row["action_type"] != event["action_type"] for row in event_rows):
            raise R5PublicationAdapterError(
                f"{event_id} has participant rows outside its catalog action type"
            )
        counts[event_id] = identity_counts
    return event_order, counts


def _validate_bridges(
    formal_bridges: list[dict[str, str]],
    identity_events: dict[str, set[str]],
    identity_rows: dict[str, list[dict[str, str]]],
    identity_statuses: dict[str, str],
) -> dict[str, dict[str, str]]:
    computed_repeats = {
        key: event_ids
        for key, event_ids in identity_events.items()
        if len(event_ids) >= 2
    }
    bridge_lookup = _unique_lookup(
        formal_bridges, "entity_key", table=BRIDGE_FILE
    )
    if set(bridge_lookup) != set(computed_repeats):
        raise R5PublicationAdapterError(
            "Formal repeat bridges disagree with repeats recomputed from "
            "row-level participation"
        )
    expected_scopes = {
        "registry_actor": "registry_actor",
        "event_only_identity_human_checked": "human_reviewed_event_only",
    }
    for key, event_ids in computed_repeats.items():
        bridge = bridge_lookup[key]
        if _integer(
            bridge["event_count"], field="event_count", row_id=bridge["bridge_id"]
        ) != len(event_ids):
            raise R5PublicationAdapterError(
                f"{bridge['bridge_id']} has a stale event_count"
            )
        if set(_split(bridge["event_ids"])) != event_ids:
            raise R5PublicationAdapterError(
                f"{bridge['bridge_id']} has stale event_ids"
            )
        if bridge["identity_scope"] != expected_scopes[identity_statuses[key]]:
            raise R5PublicationAdapterError(
                f"{bridge['bridge_id']} has an incompatible identity_scope"
            )
        derived_sources = {
            source_ref
            for row in identity_rows[key]
            for source_ref in _split(row["source_refs"])
        }
        if set(_split(bridge["evidence_basis"])) != derived_sources:
            raise R5PublicationAdapterError(
                f"{bridge['bridge_id']} has stale evidence_basis"
            )
    return bridge_lookup


def _derive_overlaps(
    event_order: list[str],
    identity_events: dict[str, set[str]],
    identity_statuses: dict[str, str],
) -> list[dict[str, Any]]:
    strict_by_event = {
        event_id: {
            key for key, event_ids in identity_events.items() if event_id in event_ids
        }
        for event_id in event_order
    }
    registry_by_event = {
        event_id: {
            key
            for key in strict_by_event[event_id]
            if identity_statuses[key] == "registry_actor"
        }
        for event_id in event_order
    }
    return [
        {
            "event_a": event_a,
            "event_b": event_b,
            "registry_denominator_a": len(registry_by_event[event_a]),
            "registry_denominator_b": len(registry_by_event[event_b]),
            "shared_registry_actor_count": len(
                registry_by_event[event_a] & registry_by_event[event_b]
            ),
            "jaccard_registry": _jaccard(
                registry_by_event[event_a], registry_by_event[event_b]
            ),
            "shared_actor_ids": sorted(
                key.removeprefix("ACTOR:")
                for key in registry_by_event[event_a] & registry_by_event[event_b]
            ),
            "strict_identity_denominator_a": len(strict_by_event[event_a]),
            "strict_identity_denominator_b": len(strict_by_event[event_b]),
            "shared_strict_identity_count": len(
                strict_by_event[event_a] & strict_by_event[event_b]
            ),
            "jaccard_strict_identity": _jaccard(
                strict_by_event[event_a], strict_by_event[event_b]
            ),
            "shared_strict_identity_keys": sorted(
                strict_by_event[event_a] & strict_by_event[event_b]
            ),
            "interpretation_limit": (
                "Pairwise overlap is a descriptive comparison of strict identities "
                "in two purposively selected source lists, not an alliance measure."
            ),
        }
        for event_a, event_b in combinations(event_order, 2)
    ]


def _validate_overlaps(
    formal_overlaps: list[dict[str, str]],
    derived_overlaps: list[dict[str, Any]],
) -> None:
    formal_lookup = _unique_lookup(
        (
            {**row, "pair_id": f"{row['event_a']}|{row['event_b']}"}
            for row in formal_overlaps
        ),
        "pair_id",
        table=OVERLAP_FILE,
    )
    derived_lookup = {
        f"{row['event_a']}|{row['event_b']}": row for row in derived_overlaps
    }
    if set(formal_lookup) != set(derived_lookup):
        raise R5PublicationAdapterError(
            "Formal overlap pairs disagree with event pairs recomputed from the catalog"
        )
    comparisons = {
        "confirmed_registry_actors_a": "registry_denominator_a",
        "confirmed_registry_actors_b": "registry_denominator_b",
        "shared_confirmed_registry_actors": "shared_registry_actor_count",
        "strict_identities_a": "strict_identity_denominator_a",
        "strict_identities_b": "strict_identity_denominator_b",
        "shared_strict_identities": "shared_strict_identity_count",
    }
    for pair_id, formal in formal_lookup.items():
        derived = derived_lookup[pair_id]
        for formal_field, derived_field in comparisons.items():
            recorded = _integer(
                formal[formal_field], field=formal_field, row_id=pair_id
            )
            if recorded != derived[derived_field]:
                raise R5PublicationAdapterError(
                    f"{pair_id} {formal_field} disagrees with row-level identities"
                )
        if set(_split(formal["shared_actor_ids"])) != set(
            derived["shared_actor_ids"]
        ):
            raise R5PublicationAdapterError(
                f"{pair_id} shared_actor_ids disagree with row-level identities"
            )
        if set(_split(formal["shared_entity_keys"])) != set(
            derived["shared_strict_identity_keys"]
        ):
            raise R5PublicationAdapterError(
                f"{pair_id} shared_entity_keys disagree with row-level identities"
            )


def _public_source(row: dict[str, str]) -> dict[str, Any]:
    return {
        "source_ref": row["source_ref"],
        "existing_source_id": row["existing_source_id"] or None,
        "source_type": row["source_type"],
        "title": row["title"],
        "year": int(row["year"]) if row["year"].isdigit() else row["year"],
        "url": row["url"],
        "archive_status": row["archive_status"],
        "source_locator": row["source_locator"],
        "supports": row["supports"],
        "interpretation_limit": row["interpretation_limit"],
    }


def build_r5_repeat_participation_exhibit(
    project_root: str | Path,
) -> dict[str, Any]:
    """Build the PUB-MR-005 row-level publication exhibit.

    The returned object is deterministic for a fixed formal R5 package.  It
    contains no actor-to-actor edge collection: observations connect a listed
    name or strict identity only to the sampled event in which it appeared.
    """

    project_root = Path(project_root).resolve()
    r5_dir = project_root / R5_DIR
    observations = _read_csv(r5_dir / PARTICIPATION_FILE)
    events = _read_csv(r5_dir / EVENT_FILE)
    formal_bridges = _read_csv(r5_dir / BRIDGE_FILE)
    formal_overlaps = _read_csv(r5_dir / OVERLAP_FILE)
    source_rows = _read_csv(r5_dir / SOURCE_FILE)

    _unique_lookup(observations, "edge_id", table=PARTICIPATION_FILE)
    _unique_lookup(observations, "participant_key", table=PARTICIPATION_FILE)
    observed_statuses = {row["identity_status"] for row in observations}
    if not observed_statuses <= IDENTITY_STATUSES:
        raise R5PublicationAdapterError(
            f"Unsupported R5 identity statuses: {sorted(observed_statuses - IDENTITY_STATUSES)}"
        )

    event_order, event_identity_counts = _validate_event_catalog(
        observations, events
    )
    event_lookup = {row["event_id"]: row for row in events}
    identity_events, identity_rows, identity_statuses = _derive_identity_events(
        observations
    )
    bridge_lookup = _validate_bridges(
        formal_bridges, identity_events, identity_rows, identity_statuses
    )
    derived_overlaps = _derive_overlaps(
        event_order, identity_events, identity_statuses
    )
    _validate_overlaps(formal_overlaps, derived_overlaps)

    all_source_refs = {
        source_ref
        for row in observations
        for source_ref in _split(row["source_refs"])
    } | {
        source_ref for row in events for source_ref in _split(row["source_refs"])
    } | {
        source_ref
        for row in formal_bridges
        for source_ref in _split(row["evidence_basis"])
    }
    source_lookup = _validate_sources(source_rows, all_source_refs)

    repeated_keys = {
        key for key, event_ids in identity_events.items() if len(event_ids) >= 2
    }
    event_index = {event_id: index for index, event_id in enumerate(event_order)}
    observation_rows: list[dict[str, Any]] = []
    for row in sorted(
        observations,
        key=lambda item: (event_index[item["event_id"]], item["participant_key"]),
    ):
        strict_key = _strict_identity_key(row)
        strict_event_count = len(identity_events[strict_key]) if strict_key else 0
        observation_rows.append(
            {
                "observation_id": row["edge_id"],
                "event_id": row["event_id"],
                "participant_key": row["participant_key"],
                "participant_tier": PARTICIPANT_TIERS[row["identity_status"]],
                "identity_status": row["identity_status"],
                "strict_identity_key": strict_key,
                "entity_key": row["entity_key"],
                "actor_id": row["actor_id"] or None,
                "identity_group_id": row["identity_group_id"] or None,
                "canonical_name": row["canonical_name"] or None,
                "source_name": row["source_name"],
                "display_name": row["canonical_name"] or row["source_name"],
                "identity_decision_id": row["identity_decision_id"] or None,
                "action_type": row["action_type"],
                "role": row["role"],
                "is_strict_repeat": bool(
                    strict_key is not None and strict_key in repeated_keys
                ),
                "strict_event_count": strict_event_count,
                "source_refs": _split(row["source_refs"]),
                "review_status": row["review_status"],
                "interpretation_limit": OBSERVATION_INTERPRETATION_LIMIT,
            }
        )

    event_rows: list[dict[str, Any]] = []
    for event_id in event_order:
        row = event_lookup[event_id]
        counts = event_identity_counts[event_id]
        event_observations = [
            item for item in observation_rows if item["event_id"] == event_id
        ]
        event_rows.append(
            {
                "event_id": event_id,
                "event_name": row["event_name"],
                "event_date": row["event_date"],
                "event_year": int(row["event_year"]),
                "action_type": row["action_type"],
                "role_vocabulary": _split(row["role_vocabulary"]),
                "target_institution": _split(row["target_institution"]),
                "issue_tags": _split(row["issue_tags"]),
                "place_tags": _split(row["place_tags"]),
                "denominator": {
                    "unit": "source_list_participant_row",
                    "declared_participant_count": _integer(
                        row["declared_participant_count"],
                        field="declared_participant_count",
                        row_id=event_id,
                    ),
                    "structured_participant_count": _integer(
                        row["structured_participant_count"],
                        field="structured_participant_count",
                        row_id=event_id,
                    ),
                    "derived_observation_count": len(event_observations),
                },
                "observation_count_by_participant_tier": {
                    PARTICIPANT_TIERS[status]: counts[status]
                    for status in sorted(IDENTITY_STATUSES)
                },
                "source_refs": _split(row["source_refs"]),
                "source_locator": row["source_locator"],
                "interpretation_limit": row["interpretation_limit"],
            }
        )

    repeat_rows: list[dict[str, Any]] = []
    for key in sorted(
        repeated_keys,
        key=lambda item: (
            -len(identity_events[item]),
            0 if identity_statuses[item] == "registry_actor" else 1,
            item,
        ),
    ):
        rows = identity_rows[key]
        bridge = bridge_lookup[key]
        ordered_event_ids = sorted(identity_events[key], key=event_index.__getitem__)
        repeat_rows.append(
            {
                "repeat_identity_id": bridge["bridge_id"],
                "strict_identity_key": key,
                "participant_tier": PARTICIPANT_TIERS[identity_statuses[key]],
                "identity_scope": bridge["identity_scope"],
                "actor_id": bridge["actor_id"] or None,
                "identity_group_id": bridge["identity_group_id"] or None,
                "canonical_name": bridge["canonical_name"],
                "origin_type": bridge["origin_type"] or None,
                "actor_class": bridge["actor_class"] or None,
                "event_count": len(ordered_event_ids),
                "event_ids": ordered_event_ids,
                "event_years": [
                    int(event_lookup[event_id]["event_year"])
                    for event_id in ordered_event_ids
                ],
                "action_types": sorted({row["action_type"] for row in rows}),
                "roles": sorted({row["role"] for row in rows}),
                "source_refs": sorted(
                    {
                        source_ref
                        for row in rows
                        for source_ref in _split(row["source_refs"])
                    }
                ),
                "interpretation_limit": REPEAT_INTERPRETATION_LIMIT,
            }
        )

    identity_observation_counts = Counter(
        row["identity_status"] for row in observations
    )
    repeat_tier_counts = Counter(
        row["participant_tier"] for row in repeat_rows
    )
    all_event_repeat_count = sum(
        row["event_count"] == len(event_order) for row in repeat_rows
    )
    registry_all_event_repeat_count = sum(
        row["event_count"] == len(event_order)
        and row["participant_tier"] == "registry_actor"
        for row in repeat_rows
    )

    return {
        "schema_version": "publication_exhibit_r5_repeat_participation_v1",
        "exhibit_id": "PUB-MR-005",
        "title": "R5 三次公开名单与严格重复参与",
        "display": {
            "title": {
                "zh": "重复参与，不是组织联盟",
                "ja": "反復参加であり、組織間同盟ではない",
                "en": "Repeated participation, not an alliance",
            },
            "subtitle": {
                "zh": (
                    "三张完整公开名单按“事件 × 名称／严格身份”逐行统计。"
                    "只有 registry ID 或经人工确认的 event-only identity 才能跨事件匹配。"
                ),
                "ja": (
                    "3つの完全な公開名簿を「イベント × 名称／厳格な同一性」で"
                    "行単位に集計。イベント間照合は registry ID または人審済み"
                    " event-only identity に限ります。"
                ),
                "en": (
                    "Three complete public lists are counted row by row as "
                    "event × name/strict identity. Cross-event matching is "
                    "limited to registry IDs and human-reviewed event-only identities."
                ),
            },
            "interpretation_limit": {
                "zh": (
                    "共同署名或重复出现只能说明公开参与；不能据此推定成员关系、"
                    "稳定联盟、持续协调、资金或影响力。"
                ),
                "ja": (
                    "共同署名や反復出現が示すのは公開参加のみで、加盟、安定した同盟、"
                    "継続的調整、資金、影響力は推定できません。"
                ),
                "en": (
                    "Co-signing or repeated appearance shows public participation "
                    "only. It does not establish membership, a stable alliance, "
                    "continuing coordination, funding, or influence."
                ),
            },
        },
        "analysis_unit": "source_list_participant_row",
        "selection_boundary": {
            "events": event_order,
            "event_count": len(event_order),
            "rule": (
                "Complete participant rows within the formal 2010, 2015, and "
                "2020 R5 source-list sample; this is a purposive event sample, "
                "not a census of post-1972 public action."
            ),
            "identity_rule": (
                "Strict repeat matching uses registry actor IDs or HR-020 "
                "human-reviewed event-only identity groups. Other event-only "
                "names remain event-scoped and are never string-matched across events."
            ),
        },
        "participant_tier_definitions": {
            "registry_actor": (
                "The source-list row has a current actor-registry crosswalk."
            ),
            "human_reviewed_event_only_identity": (
                "HR-020 confirmed the identity across sampled events, but the "
                "entity remains outside the actor registry."
            ),
            "other_event_only_name": (
                "A literal source-list name with no approved cross-event or "
                "actor-registry identity."
            ),
        },
        "relation_semantics": {
            "creates_actor_relation_edges": False,
            "creates_alliance_edges": False,
            "creates_membership_edges": False,
            "allowed_edge_type": "participant_to_event_observation_only",
            "allowed_claim": (
                "A strict identity appeared publicly in two or more of the "
                "sampled source lists."
            ),
            "prohibited_claims": [
                "stable alliance",
                "membership",
                "continuous coordination",
                "organizational continuity",
                "funding",
                "hierarchy",
                "influence or causal effect",
            ],
        },
        "summary": {
            "observation_count": len(observation_rows),
            "event_count": len(event_rows),
            "observation_count_by_participant_tier": {
                PARTICIPANT_TIERS[status]: identity_observation_counts[status]
                for status in sorted(IDENTITY_STATUSES)
            },
            "strict_identity_count": len(identity_events),
            "strict_repeat_identity_count": len(repeat_rows),
            "strict_repeat_count_by_participant_tier": {
                tier: repeat_tier_counts[tier]
                for tier in PARTICIPANT_TIERS.values()
            },
            "all_sampled_events_repeat_identity_count": all_event_repeat_count,
            "registry_all_sampled_events_repeat_identity_count": (
                registry_all_event_repeat_count
            ),
        },
        "events": event_rows,
        "observations": observation_rows,
        "repeat_identities": repeat_rows,
        "pairwise_overlaps": derived_overlaps,
        "sources": [
            _public_source(source_lookup[source_ref])
            for source_ref in sorted(source_lookup)
        ],
        "interpretation_limits": [
            "The three events are a purposive public-list sample, not a census.",
            "Participant counts are source-list rows, not membership counts.",
            "Event-only identities do not enter the actor registry.",
            "Other event-only names are not matched across events by name similarity.",
            "Co-signing and repeated participation are not stable actor relations or alliances.",
        ],
    }
