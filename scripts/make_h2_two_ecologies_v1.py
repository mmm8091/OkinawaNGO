from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "outputs" / "research_wave_h2_two_ecologies_v1"
AS_OF_DATE = "2026-07-20"
PACKAGE_ID = "research_wave_h2_two_ecologies_v1"

REGISTRY_PATH = Path("data/interim/01_actor_registry_initial_v0.csv")
ISSUE_PATH = Path("data/interim/24_r01_r02_actor_issue_layered_v0.csv")
PLACE_PATH = Path("data/interim/32_actor_place_semantic_candidates_v1.csv")
PLACE_REGISTRY_PATH = Path("data/interim/04_place_registry_v0.csv")
SOURCE_LOG_PATH = Path("data/interim/05_source_log_initial_v0.csv")
REVIEWED_DYADIC_PATH = Path(
    "outputs/exploration_system_data_v1/demo/dyadic_relations.json"
)
RESEARCH_CANDIDATES_PATH = Path(
    "outputs/exploration_system_data_v1/research/candidates.json"
)
CASE_ROLES_PATH = Path("outputs/exploration_system_data_v1/demo/case_roles.json")
TYPED_EVENTS_PATH = Path(
    "outputs/exploration_system_data_v1/demo/typed_event_participation.json"
)
R10_RELATIONS_PATH = Path("data/interim/21_admin_collaboration_relations_v0.csv")
R10_UNIVERSE_PATH = Path(
    "outputs/R10_official_collaboration_universe_v1/"
    "official_collaboration_source_universe_v1.csv"
)
R10_IDENTITY_CROSSWALK_PATH = Path(
    "outputs/R10_official_collaboration_universe_v1/"
    "partner_identity_crosswalk_human_v1.csv"
)

INPUT_PATHS = (
    REGISTRY_PATH,
    ISSUE_PATH,
    PLACE_PATH,
    PLACE_REGISTRY_PATH,
    SOURCE_LOG_PATH,
    REVIEWED_DYADIC_PATH,
    RESEARCH_CANDIDATES_PATH,
    CASE_ROLES_PATH,
    TYPED_EVENTS_PATH,
    R10_RELATIONS_PATH,
    R10_UNIVERSE_PATH,
    R10_IDENTITY_CROSSWALK_PATH,
)

SERVICE_CORE_CLASSES = frozenset(
    {
        "base_community_service_actor",
        "base_spouse_charity_network",
        "base_spouse_club",
    }
)
SERVICE_PERIPHERY_CLASSES = frozenset(
    {
        "corporate_sponsor",
        "local_business_sponsor",
    }
)
EXPECTED_SERVICE_CORE_IDS = (
    "X001",
    "X004",
    "X005",
    "X006",
    "X007",
    "X008",
    "X009",
    "X016",
    "X017",
)

# These are issue-specific anchors for construction, operation, deployment, or
# their directly observed local harms/procedures. Broad labels such as peace,
# women, human rights, solidarity, or generic environment do not independently
# select an actor into the comparison group.
ACCOUNTABILITY_ANCHOR_ISSUE_IDS = frozenset(
    {
        "I001",  # anti_base
        "I002",  # anti_military
        "I003",  # Henoko
        "I004",  # dugong
        "I006",  # groundwater
        "I007",  # life_safety
        "I008",  # health_risk
        "I010",  # referendum
        "I017",  # frontline_prevention
        "I018",  # Taiwan_contingency
        "I021",  # noise
        "I025",  # anti_war
    }
)
NON_CIVIC_COMPARISON_CLASSES = frozenset(
    {
        "public_institution_partner",
        "public_diplomacy_grant_program",
        "public_diplomacy_or_exchange_actor",
        "funder_or_intermediary",
        "corporate_sponsor",
        "local_business_sponsor",
    }
)

PACKAGE_METADATA = {
    "package_scope": "research_only",
    "package_claim_status": "candidate_analysis",
    "frontend_eligibility": "excluded_research_only",
}

OUTPUT_FILENAMES = {
    "service_core_actors_v1.csv",
    "accountability_comparison_actors_v1.csv",
    "issue_ecology_profile_v1.csv",
    "dyadic_relation_ecology_audit_v1.csv",
    "case_role_ecology_audit_v1.csv",
    "typed_event_ecology_audit_v1.csv",
    "r10_interface_audit_v1.csv",
    "place_overlap_v1.csv",
    "source_overlap_v1.csv",
    "coverage_gaps_v1.csv",
    "human_review_queue_v1.csv",
    "further_search_queue_v1.csv",
    "metrics_v1.json",
    "manifest.json",
    "H2_two_ecologies_brief_v1.md",
    "README.md",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def split_refs(raw: str | None) -> list[str]:
    if not raw:
        return []
    return sorted({part.strip() for part in raw.split(";") if part.strip()})


def join_sorted(values: Iterable[str]) -> str:
    return ";".join(sorted({value for value in values if value}))


def is_active_actor(row: Mapping[str, str]) -> bool:
    if row.get("actor_id") == "A072":
        return False
    if row.get("merged_duplicate_of"):
        return False
    return row.get("scope_status") not in {
        "merged_duplicate",
        "rejected",
        "out_of_scope",
    }


def derive_service_core(
    registry: Sequence[Mapping[str, str]],
) -> tuple[str, ...]:
    derived = tuple(
        sorted(
            row["actor_id"]
            for row in registry
            if is_active_actor(row)
            and row.get("actor_class") in SERVICE_CORE_CLASSES
            and row.get("origin_type") == "us_origin"
        )
    )
    if derived != EXPECTED_SERVICE_CORE_IDS:
        raise ValueError(
            "Service-core rule drifted. "
            f"Expected {EXPECTED_SERVICE_CORE_IDS}, observed {derived}."
        )
    return derived


def derive_accountability_group(
    registry: Sequence[Mapping[str, str]],
    current_issue_rows: Sequence[Mapping[str, str]],
    service_core_ids: Sequence[str],
) -> tuple[str, ...]:
    actors = {
        row["actor_id"]: row
        for row in registry
        if is_active_actor(row)
    }
    anchored = {
        row["actor_id"]
        for row in current_issue_rows
        if row.get("analysis_inclusion") == "active"
        and row.get("issue_id") in ACCOUNTABILITY_ANCHOR_ISSUE_IDS
    }
    selected = tuple(
        sorted(
            actor_id
            for actor_id in anchored
            if actor_id in actors
            and actor_id not in service_core_ids
            and actors[actor_id].get("actor_class")
            not in NON_CIVIC_COMPARISON_CLASSES
            and actors[actor_id].get("actor_class")
            not in SERVICE_CORE_CLASSES
        )
    )
    return selected


def load_inputs(root: Path = ROOT) -> dict[str, Any]:
    return {
        "registry": read_csv(root / REGISTRY_PATH),
        "issues": read_csv(root / ISSUE_PATH),
        "places": read_csv(root / PLACE_PATH),
        "place_registry": read_csv(root / PLACE_REGISTRY_PATH),
        "source_log": read_csv(root / SOURCE_LOG_PATH),
        "reviewed_dyadic": read_json(root / REVIEWED_DYADIC_PATH),
        "research_candidates": read_json(root / RESEARCH_CANDIDATES_PATH),
        "case_roles": read_json(root / CASE_ROLES_PATH),
        "typed_events": read_json(root / TYPED_EVENTS_PATH),
        "r10_relations": read_csv(root / R10_RELATIONS_PATH),
        "r10_universe": read_csv(root / R10_UNIVERSE_PATH),
        "r10_identity_crosswalk": read_csv(root / R10_IDENTITY_CROSSWALK_PATH),
    }


def endpoint_ecology(
    actor_id: str,
    registry_by_id: Mapping[str, Mapping[str, str]],
    service_core_ids: set[str],
    accountability_ids: set[str],
) -> str:
    if actor_id in service_core_ids:
        return "service_core"
    if actor_id in accountability_ids:
        return "accountability_comparison"
    actor = registry_by_id.get(actor_id)
    if actor and actor.get("actor_class") in SERVICE_PERIPHERY_CLASSES:
        return "service_periphery"
    if actor:
        return "other_registry_actor"
    if actor_id:
        return "non_registry_or_provisional"
    return "blank_or_collective_endpoint"


def relation_ecology(
    source_ecology: str,
    target_ecology: str,
) -> str:
    service_labels = {"service_core", "service_periphery"}
    if (
        source_ecology in service_labels
        and target_ecology == "accountability_comparison"
    ) or (
        target_ecology in service_labels
        and source_ecology == "accountability_comparison"
    ):
        return "cross_ecology_observed"
    if source_ecology in service_labels and target_ecology in service_labels:
        return "service_ecology_internal"
    if (
        source_ecology == "accountability_comparison"
        and target_ecology == "accountability_comparison"
    ):
        return "accountability_internal"
    if source_ecology in service_labels or target_ecology in service_labels:
        return "service_to_other_interface"
    if (
        source_ecology == "accountability_comparison"
        or target_ecology == "accountability_comparison"
    ):
        return "accountability_to_other_interface"
    return "outside_two_group_comparison"


def add_metadata(row: Mapping[str, Any]) -> dict[str, Any]:
    return {**row, **PACKAGE_METADATA}


def _actor_rows(
    actor_ids: Sequence[str],
    selection_rule: str,
    registry_by_id: Mapping[str, Mapping[str, str]],
    issues_by_actor: Mapping[str, list[Mapping[str, str]]],
    places_by_actor: Mapping[str, list[Mapping[str, str]]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for actor_id in actor_ids:
        actor = registry_by_id[actor_id]
        actor_issues = issues_by_actor.get(actor_id, [])
        actor_places = places_by_actor.get(actor_id, [])
        source_ids = {
            ref
            for row in actor_issues
            for ref in split_refs(row.get("source_ref"))
            if ref.startswith("S")
        }
        non_source_refs = {
            ref
            for row in actor_issues
            for ref in split_refs(row.get("source_ref"))
            if not ref.startswith("S")
        }
        anchor_rows = [
            row
            for row in actor_issues
            if row.get("issue_id") in ACCOUNTABILITY_ANCHOR_ISSUE_IDS
        ]
        reviewed_anchor_count = sum(
            row.get("review_layer") == "human_reviewed"
            for row in anchor_rows
        )
        candidate_anchor_count = sum(
            row.get("review_layer") == "candidate"
            for row in anchor_rows
        )
        rows.append(
            add_metadata(
                {
                    "actor_id": actor_id,
                    "canonical_name": actor.get("canonical_name", ""),
                    "actor_class": actor.get("actor_class", ""),
                    "origin_type": actor.get("origin_type", ""),
                    "evidence_level": actor.get("evidence_level", ""),
                    "actor_review_status": actor.get("review_status", ""),
                    "scope_status": actor.get("scope_status", ""),
                    "active_issue_edge_count": len(actor_issues),
                    "human_reviewed_issue_edge_count": sum(
                        row.get("review_layer") == "human_reviewed"
                        for row in actor_issues
                    ),
                    "anchor_issue_ids": join_sorted(
                        row.get("issue_id", "")
                        for row in actor_issues
                        if row.get("issue_id")
                        in ACCOUNTABILITY_ANCHOR_ISSUE_IDS
                    ),
                    "active_anchor_issue_edge_count": len(anchor_rows),
                    "human_reviewed_anchor_issue_edge_count": (
                        reviewed_anchor_count
                    ),
                    "candidate_anchor_issue_edge_count": (
                        candidate_anchor_count
                    ),
                    "anchor_selection_evidence_status": (
                        "at_least_one_human_reviewed_anchor"
                        if reviewed_anchor_count
                        else (
                            "candidate_anchor_only"
                            if candidate_anchor_count
                            else "no_anchor_edge"
                        )
                    ),
                    "all_active_issue_ids": join_sorted(
                        row.get("issue_id", "") for row in actor_issues
                    ),
                    "active_place_ids": join_sorted(
                        row.get("place_id", "") for row in actor_places
                    ),
                    "source_ids": join_sorted(source_ids),
                    "non_source_refs": join_sorted(non_source_refs),
                    "selection_rule": selection_rule,
                    "interpretation_limit": (
                        "Selection into this research comparison is not a "
                        "political-identity judgment, alliance claim, or "
                        "population census."
                    ),
                }
            )
        )
    return rows


def build_analysis(inputs: Mapping[str, Any]) -> dict[str, Any]:
    registry = inputs["registry"]
    current_actors = [row for row in registry if is_active_actor(row)]
    registry_by_id = {row["actor_id"]: row for row in current_actors}
    current_issues = [
        row
        for row in inputs["issues"]
        if row.get("analysis_inclusion") == "active"
        and row.get("actor_id") in registry_by_id
    ]
    current_places = [
        row
        for row in inputs["places"]
        if row.get("analysis_inclusion") == "active"
        and row.get("actor_id") in registry_by_id
    ]
    issues_by_actor: dict[str, list[Mapping[str, str]]] = defaultdict(list)
    places_by_actor: dict[str, list[Mapping[str, str]]] = defaultdict(list)
    for row in current_issues:
        issues_by_actor[row["actor_id"]].append(row)
    for row in current_places:
        places_by_actor[row["actor_id"]].append(row)

    service_core = derive_service_core(registry)
    accountability = derive_accountability_group(
        registry,
        current_issues,
        service_core,
    )
    service_set = set(service_core)
    accountability_set = set(accountability)
    if service_set & accountability_set:
        raise ValueError("Service core and accountability comparison overlap.")

    service_rows = _actor_rows(
        service_core,
        (
            "active registry actor; actor_class in "
            "{base_community_service_actor,base_spouse_charity_network,"
            "base_spouse_club}; origin_type=us_origin; exact ID set asserted"
        ),
        registry_by_id,
        issues_by_actor,
        places_by_actor,
    )
    accountability_rows = _actor_rows(
        accountability,
        (
            "active registry actor; at least one active edge in the declared "
            "accountability anchor issue set; service and non-civic "
            "institution/sponsor classes excluded"
        ),
        registry_by_id,
        issues_by_actor,
        places_by_actor,
    )

    issue_profiles: list[dict[str, Any]] = []
    for ecology, actor_ids in (
        ("service_core", service_set),
        ("accountability_comparison", accountability_set),
    ):
        selected = [row for row in current_issues if row["actor_id"] in actor_ids]
        for issue_id in sorted({row["issue_id"] for row in selected}):
            issue_rows = [row for row in selected if row["issue_id"] == issue_id]
            issue_profiles.append(
                add_metadata(
                    {
                        "ecology": ecology,
                        "issue_id": issue_id,
                        "issue_label": issue_rows[0].get("issue_label", ""),
                        "issue_group": issue_rows[0].get("issue_group", ""),
                        "active_edge_count": len(issue_rows),
                        "unique_actor_count": len(
                            {row["actor_id"] for row in issue_rows}
                        ),
                        "human_reviewed_edge_count": sum(
                            row.get("review_layer") == "human_reviewed"
                            for row in issue_rows
                        ),
                        "candidate_edge_count": sum(
                            row.get("review_layer") == "candidate"
                            for row in issue_rows
                        ),
                        "actor_ids": join_sorted(
                            row["actor_id"] for row in issue_rows
                        ),
                        "interpretation_limit": (
                            "Issue-edge counts describe the current curated "
                            "sample; they do not measure political commitment, "
                            "influence, or real-world sector size."
                        ),
                    }
                )
            )

    reviewed_dyadic = [
        {**row, "input_layer": "reviewed"}
        for row in inputs["reviewed_dyadic"]
    ]
    candidate_dyadic = [
        {**row, "input_layer": "research"}
        for row in inputs["research_candidates"].get("dyadic_relations", [])
    ]
    dyadic_rows: list[dict[str, Any]] = []
    for row in reviewed_dyadic + candidate_dyadic:
        source = row.get("source_endpoint", "")
        target = row.get("target_endpoint", "")
        source_ecology = endpoint_ecology(
            source,
            registry_by_id,
            service_set,
            accountability_set,
        )
        target_ecology = endpoint_ecology(
            target,
            registry_by_id,
            service_set,
            accountability_set,
        )
        dyadic_rows.append(
            add_metadata(
                {
                    "relation_id": row.get("id", ""),
                    "input_layer": row["input_layer"],
                    "source_endpoint": source,
                    "source_name": registry_by_id.get(source, {}).get(
                        "canonical_name", ""
                    ),
                    "source_ecology": source_ecology,
                    "target_endpoint": target,
                    "target_name": registry_by_id.get(target, {}).get(
                        "canonical_name", ""
                    ),
                    "target_ecology": target_ecology,
                    "ecology_relation": relation_ecology(
                        source_ecology, target_ecology
                    ),
                    "relation_family": row.get("relation_family", ""),
                    "relation_type": row.get("relation_type", ""),
                    "source_claim_status": row.get("claim_status", ""),
                    "source_review_status": row.get("review_status", ""),
                    "evidence_level": row.get("evidence_level", ""),
                    "source_ids": join_sorted(row.get("source_ids", [])),
                    "interpretation_limit": (
                        "A zero count of cross-ecology rows means only that no "
                        "direct dyadic relation is encoded in these current "
                        "reviewed/research inputs. It does not prove social "
                        "separation or no shared people."
                    ),
                }
            )
        )

    case_rows: list[dict[str, Any]] = []
    for row in inputs["case_roles"]:
        actor_id = row.get("actor_id", "")
        ecology = endpoint_ecology(
            actor_id,
            registry_by_id,
            service_set,
            accountability_set,
        )
        case_rows.append(
            add_metadata(
                {
                    "role_id": row.get("id", ""),
                    "case_id": row.get("case_id", ""),
                    "actor_id": actor_id,
                    "display_label": row.get("display_label", ""),
                    "actor_ecology": ecology,
                    "entity_kind": row.get("entity_kind", ""),
                    "role": row.get("role", ""),
                    "role_family": row.get("role_family", ""),
                    "side": row.get("side", ""),
                    "source_review_status": row.get("review_status", ""),
                    "evidence_level": row.get("evidence_level", ""),
                    "source_ids": join_sorted(row.get("source_ids", [])),
                    "interpretation_limit": (
                        "Case roles are case-specific and do not establish a "
                        "stable alliance or a person-level bridge."
                    ),
                }
            )
        )

    event_rows: list[dict[str, Any]] = []
    for row in inputs["typed_events"]:
        source = row.get("source_endpoint", "")
        target = row.get("target_endpoint", "")
        source_ecology = endpoint_ecology(
            source,
            registry_by_id,
            service_set,
            accountability_set,
        )
        target_ecology = endpoint_ecology(
            target,
            registry_by_id,
            service_set,
            accountability_set,
        )
        event_rows.append(
            add_metadata(
                {
                    "observation_id": row.get("id", ""),
                    "event_or_program": row.get("event_or_program", ""),
                    "source_endpoint": source,
                    "source_ecology": source_ecology,
                    "target_endpoint": target,
                    "target_ecology": target_ecology,
                    "ecology_relation": relation_ecology(
                        source_ecology, target_ecology
                    ),
                    "relation_family": row.get("relation_family", ""),
                    "relation_type": row.get("relation_type", ""),
                    "source_review_status": row.get("review_status", ""),
                    "evidence_level": row.get("evidence_level", ""),
                    "source_ids": join_sorted(row.get("source_ids", [])),
                    "interpretation_limit": (
                        "Event participation is event-specific and is not a "
                        "stable alliance or evidence of shared personnel."
                    ),
                }
            )
        )

    r10_rows: list[dict[str, Any]] = []
    for row in inputs["r10_relations"]:
        source = row.get("source_entity_id", "")
        target = row.get("target_entity_id", "")
        source_ecology = endpoint_ecology(
            source,
            registry_by_id,
            service_set,
            accountability_set,
        )
        target_ecology = endpoint_ecology(
            target,
            registry_by_id,
            service_set,
            accountability_set,
        )
        r10_rows.append(
            add_metadata(
                {
                    "relation_observation_id": row.get(
                        "relation_observation_id", ""
                    ),
                    "source_entity_id": source,
                    "source_entity_name": row.get("source_entity_name", ""),
                    "source_ecology": source_ecology,
                    "target_entity_id": target,
                    "target_entity_name": row.get("target_entity_name", ""),
                    "target_ecology": target_ecology,
                    "ecology_relation": relation_ecology(
                        source_ecology, target_ecology
                    ),
                    "program_name": row.get("program_name", ""),
                    "relation_type": row.get("relation_type", ""),
                    "relation_scope": row.get("relation_scope", ""),
                    "financial_semantics": row.get(
                        "financial_semantics", ""
                    ),
                    "source_review_status": row.get("review_status", ""),
                    "evidence_level": row.get("evidence_level", ""),
                    "source_refs": row.get("source_refs", ""),
                    "interpretation_limit": (
                        row.get("interpretation_limit", "")
                        + " R10 observations do not by themselves establish "
                        "political stance, shared personnel, or movement ties."
                    ).strip(),
                }
            )
        )

    place_registry = {
        row["place_id"]: row for row in inputs["place_registry"]
    }
    service_place_rows = [
        row for row in current_places if row["actor_id"] in service_set
    ]
    accountability_place_rows = [
        row for row in current_places if row["actor_id"] in accountability_set
    ]
    places_union = sorted(
        {
            row["place_id"]
            for row in service_place_rows + accountability_place_rows
        }
    )
    place_rows: list[dict[str, Any]] = []
    for place_id in places_union:
        service_at_place = [
            row for row in service_place_rows if row["place_id"] == place_id
        ]
        accountability_at_place = [
            row
            for row in accountability_place_rows
            if row["place_id"] == place_id
        ]
        place = place_registry.get(place_id, {})
        place_rows.append(
            add_metadata(
                {
                    "place_id": place_id,
                    "place_name": place.get("place_name", ""),
                    "place_type": place.get("place_type", ""),
                    "service_actor_ids": join_sorted(
                        row["actor_id"] for row in service_at_place
                    ),
                    "service_place_edge_count": len(service_at_place),
                    "accountability_actor_ids": join_sorted(
                        row["actor_id"] for row in accountability_at_place
                    ),
                    "accountability_place_edge_count": len(
                        accountability_at_place
                    ),
                    "overlap_status": (
                        "same_place_node_observed"
                        if service_at_place and accountability_at_place
                        else "one_ecology_only_in_current_place_layer"
                    ),
                    "interpretation_limit": (
                        "A shared place node is co-location or shared issue "
                        "geography only; it is not a relationship, meeting, "
                        "shared person, or alliance."
                    ),
                }
            )
        )

    service_source_actor_ids: dict[str, set[str]] = defaultdict(set)
    accountability_source_actor_ids: dict[str, set[str]] = defaultdict(set)
    service_non_source_refs: set[str] = set()
    accountability_non_source_refs: set[str] = set()
    for row in current_issues:
        actor_id = row["actor_id"]
        for ref in split_refs(row.get("source_ref")):
            if ref.startswith("S"):
                if actor_id in service_set:
                    service_source_actor_ids[ref].add(actor_id)
                if actor_id in accountability_set:
                    accountability_source_actor_ids[ref].add(actor_id)
            else:
                if actor_id in service_set:
                    service_non_source_refs.add(ref)
                if actor_id in accountability_set:
                    accountability_non_source_refs.add(ref)
    source_log = {row["source_id"]: row for row in inputs["source_log"]}
    source_union = sorted(
        set(service_source_actor_ids) | set(accountability_source_actor_ids)
    )
    source_rows: list[dict[str, Any]] = []
    for source_id in source_union:
        source = source_log.get(source_id, {})
        service_actors = service_source_actor_ids.get(source_id, set())
        accountability_actors = accountability_source_actor_ids.get(
            source_id, set()
        )
        source_rows.append(
            add_metadata(
                {
                    "source_id": source_id,
                    "source_type": source.get("source_type", ""),
                    "title": source.get("title", ""),
                    "year": source.get("year", ""),
                    "service_actor_ids": join_sorted(service_actors),
                    "accountability_actor_ids": join_sorted(
                        accountability_actors
                    ),
                    "overlap_status": (
                        "same_source_id_used_by_both"
                        if service_actors and accountability_actors
                        else "one_ecology_only_in_current_issue_layer"
                    ),
                    "interpretation_limit": (
                        "Source-ID overlap is a documentation-channel measure, "
                        "not a social tie. No overlap may reflect language, "
                        "archive, source-selection, or module-design bias."
                    ),
                }
            )
        )

    crosswalked_service_universe_rows = [
        row
        for row in inputs["r10_identity_crosswalk"]
        if row.get("registry_actor_id") in service_set
    ]
    r10_cross_rows = [
        row
        for row in r10_rows
        if row["ecology_relation"] == "cross_ecology_observed"
    ]
    dyadic_cross_rows = [
        row
        for row in dyadic_rows
        if row["ecology_relation"] == "cross_ecology_observed"
    ]
    event_cross_rows = [
        row
        for row in event_rows
        if row["ecology_relation"] == "cross_ecology_observed"
    ]

    gaps = [
        add_metadata(
            {
                "gap_id": "H2G001",
                "gap_family": "public_person_roles",
                "current_status": "not_measured",
                "observed_count": "",
                "needed_material": (
                    "time-bounded public officer, board, staff, attorney, "
                    "organizer, and representative role records"
                ),
                "closure_rule": (
                    "Create a person-actor-time table with bilingual aliases, "
                    "role dates, source IDs, and human-reviewed crosswalks."
                ),
                "claim_boundary": (
                    "Do not report zero shared people. The project has no "
                    "systematic person-role input for this comparison."
                ),
            }
        ),
        add_metadata(
            {
                "gap_id": "H2G002",
                "gap_family": "service_recipient_universe",
                "current_status": "incomplete",
                "observed_count": "",
                "needed_material": (
                    "AWWA/KOSC/NOSCO/OESC/MOSCO/ACGO annual reports, Form "
                    "990 Schedule I, grant lists, and activity booklets"
                ),
                "closure_rule": (
                    "Resolve named recipients by year and crosswalk them "
                    "against the actor registry and the S002 source universe."
                ),
                "claim_boundary": (
                    "Named examples and a long-run aggregate are not a "
                    "complete recipient network."
                ),
            }
        ),
        add_metadata(
            {
                "gap_id": "H2G003",
                "gap_family": "public_policy_stance",
                "current_status": "not_systematically_searched",
                "observed_count": "",
                "needed_material": (
                    "symmetric organization-by-keyword searches and archived "
                    "mission/news/statement pages"
                ),
                "closure_rule": (
                    "Record found/not-found search logs by actor, query, "
                    "source family, date range, and archive coverage."
                ),
                "claim_boundary": (
                    "Observed service function does not establish a pro-base, "
                    "anti-base, or apolitical stance."
                ),
            }
        ),
        add_metadata(
            {
                "gap_id": "H2G004",
                "gap_family": "causal_production",
                "current_status": "hypothesis_only",
                "observed_count": "",
                "needed_material": (
                    "formation dates, founding statements, organizational "
                    "histories, base-change chronology, and negative cases"
                ),
                "closure_rule": (
                    "Show a dated mechanism connecting base harms or garrison "
                    "care needs to organizational formation; assess competing "
                    "explanations."
                ),
                "claim_boundary": (
                    "Current coexistence cannot by itself prove that the base "
                    "caused or produced either ecology."
                ),
            }
        ),
        add_metadata(
            {
                "gap_id": "H2G005",
                "gap_family": "historical_coverage",
                "current_status": "online_recent_bias",
                "observed_count": "",
                "needed_material": (
                    "1972-2011 local press, newsletters, directories, "
                    "organizational archives, and leadership rosters"
                ),
                "closure_rule": (
                    "Repeat actor, role, recipient, and relation checks for "
                    "dated historical slices using local/archive sources."
                ),
                "claim_boundary": (
                    "The present research-only snapshot is not a post-1972 "
                    "population history."
                ),
            }
        ),
    ]

    human_review_queue = [
        add_metadata(
            {
                "review_item_id": "H2HR001",
                "decision_scope": "service_core_boundary",
                "question": (
                    "Approve the class+origin rule and the exact nine service "
                    "core actor IDs for H2 only?"
                ),
                "evidence_path": "service_core_actors_v1.csv",
                "allowed_decisions": "accept;revise;defer;reject",
                "human_decision": "",
                "human_rationale": "",
                "reviewer": "",
                "review_date": "",
                "interpretation_limit": (
                    "Approval would freeze this research comparison only, not "
                    "change registry classes."
                ),
            }
        ),
        add_metadata(
            {
                "review_item_id": "H2HR002",
                "decision_scope": "accountability_selection_rule",
                "question": (
                    "Does the declared anchor-issue rule create an interpretable "
                    "comparison without over-including broad peace/environment "
                    "actors?"
                ),
                "evidence_path": "accountability_comparison_actors_v1.csv",
                "allowed_decisions": "accept;revise;defer;reject",
                "human_decision": "",
                "human_rationale": "",
                "reviewer": "",
                "review_date": "",
                "interpretation_limit": (
                    "Do not manually add or remove actors merely to strengthen "
                    "the expected separation."
                ),
            }
        ),
        add_metadata(
            {
                "review_item_id": "H2HR003",
                "decision_scope": "zero_direct_dyadic_interpretation",
                "question": (
                    "May the brief state that no direct cross-ecology dyadic "
                    "relation is observed in the current typed layer?"
                ),
                "evidence_path": "dyadic_relation_ecology_audit_v1.csv",
                "allowed_decisions": "accept_bounded;revise;defer;reject",
                "human_decision": "",
                "human_rationale": "",
                "reviewer": "",
                "review_date": "",
                "interpretation_limit": (
                    "Never convert this observation into no shared people, no "
                    "informal ties, or complete social separation."
                ),
            }
        ),
        add_metadata(
            {
                "review_item_id": "H2HR004",
                "decision_scope": "same_place_interpretation",
                "question": (
                    "Should P001/P005 co-presence be used only as a "
                    "same-environment observation?"
                ),
                "evidence_path": "place_overlap_v1.csv",
                "allowed_decisions": "accept_bounded;revise;defer;reject",
                "human_decision": "",
                "human_rationale": "",
                "reviewer": "",
                "review_date": "",
                "interpretation_limit": (
                    "Same place does not establish contact, collaboration, or "
                    "shared membership."
                ),
            }
        ),
        add_metadata(
            {
                "review_item_id": "H2HR005",
                "decision_scope": "documentation_silo_interpretation",
                "question": (
                    "May source-ID non-overlap be used as evidence of separate "
                    "documentation channels rather than social separation?"
                ),
                "evidence_path": "source_overlap_v1.csv",
                "allowed_decisions": "accept_bounded;revise;defer;reject",
                "human_decision": "",
                "human_rationale": "",
                "reviewer": "",
                "review_date": "",
                "interpretation_limit": (
                    "Source IDs are artifacts of the corpus and research "
                    "workflow."
                ),
            }
        ),
        add_metadata(
            {
                "review_item_id": "H2HR006",
                "decision_scope": "stance_wording",
                "question": (
                    "Freeze wording as 'no source-backed base-policy stance in "
                    "the current corpus', not 'non-political' or 'pro-base'?"
                ),
                "evidence_path": "issue_ecology_profile_v1.csv",
                "allowed_decisions": "accept_bounded;revise;defer;reject",
                "human_decision": "",
                "human_rationale": "",
                "reviewer": "",
                "review_date": "",
                "interpretation_limit": (
                    "A service mission and silence in service/tax sources do "
                    "not prove the absence of political views."
                ),
            }
        ),
        add_metadata(
            {
                "review_item_id": "H2HR007",
                "decision_scope": "causal_language",
                "question": (
                    "Keep 'the base produces two ecologies' as a hypothesis "
                    "until formation mechanisms and negative cases are added?"
                ),
                "evidence_path": "coverage_gaps_v1.csv",
                "allowed_decisions": "accept;revise;defer;reject",
                "human_decision": "",
                "human_rationale": "",
                "reviewer": "",
                "review_date": "",
                "interpretation_limit": (
                    "Coexistence and longevity alone do not identify causal "
                    "production."
                ),
            }
        ),
    ]

    search_queue = [
        add_metadata(
            {
                "search_task_id": "H2SR001",
                "priority": "P0",
                "mode": "online_then_local_if_needed",
                "target": "nine service-core actors",
                "task": (
                    "Build 2012-2026 public person-role rosters from official "
                    "sites, filings, annual reports, DVIDS/Stripes, and local "
                    "news."
                ),
                "done_when": (
                    "Each actor has searched years, role fields, bilingual "
                    "aliases, source IDs, and explicit no-record logs."
                ),
                "claim_boundary": (
                    "Public roles only; no private relationship inference."
                ),
            }
        ),
        add_metadata(
            {
                "search_task_id": "H2SR002",
                "priority": "P0",
                "mode": "online_and_internal_record",
                "target": "AWWA/KOSC",
                "task": (
                    "Retrieve Form 990 Schedule I, annual reports, and named "
                    "recipient/allocation records."
                ),
                "done_when": (
                    "Recipient, year, item/amount semantics, and source locator "
                    "are recorded without allocating aggregates."
                ),
                "claim_boundary": (
                    "F027/R10R029 aggregates remain non-allocable."
                ),
            }
        ),
        add_metadata(
            {
                "search_task_id": "H2SR003",
                "priority": "P1",
                "mode": "online_then_local_if_needed",
                "target": "NOSCO/OESC/MOSCO/ACGO",
                "task": (
                    "Collect annual recipient lists, activity booklets, "
                    "officer rosters, and dated charity/project records."
                ),
                "done_when": (
                    "Every named organization recipient is identity-crosswalked "
                    "or retained as unresolved."
                ),
                "claim_boundary": (
                    "Joint contributions are not attributed wholly to one club."
                ),
            }
        ),
        add_metadata(
            {
                "search_task_id": "H2SR004",
                "priority": "P0",
                "mode": "online",
                "target": "service-core stance corpus",
                "task": (
                    "Run symmetric searches for each service actor with "
                    "Henoko, Futenma, Kadena, PFAS, peace, anti-base, base "
                    "policy, and Japanese equivalents."
                ),
                "done_when": (
                    "Actor×query×source-family×date-range log is complete and "
                    "any organizational statement is separately reviewed."
                ),
                "claim_boundary": (
                    "No result means not found in the searched corpus, not "
                    "apolitical."
                ),
            }
        ),
        add_metadata(
            {
                "search_task_id": "H2SR005",
                "priority": "P1",
                "mode": "online",
                "target": "accountability comparison actors",
                "task": (
                    "Search comparison actor names against USO, AWWA, spouse "
                    "clubs, charity, donation, board, staff, and recipient "
                    "records."
                ),
                "done_when": (
                    "Exact and transliterated name matches are logged and "
                    "human-reviewed."
                ),
                "claim_boundary": (
                    "Name similarity is not a person or organization match."
                ),
            }
        ),
        add_metadata(
            {
                "search_task_id": "H2SR006",
                "priority": "P1",
                "mode": "mechanical_then_human_review",
                "target": "recipient and organization crosswalk",
                "task": (
                    "Crosswalk all named service recipients against the active "
                    "registry and the 616-row S002 source universe."
                ),
                "done_when": (
                    "Legal-entity match, alias evidence, relation type, and "
                    "non-match reason are recorded."
                ),
                "claim_boundary": (
                    "A recipient interface is not automatically a movement tie."
                ),
            }
        ),
        add_metadata(
            {
                "search_task_id": "H2SR007",
                "priority": "P2",
                "mode": "local_archive",
                "target": "1972-2011 historical slices",
                "task": (
                    "Use local press, newsletters, directories, and archives "
                    "to reconstruct service/advocacy roles and interfaces."
                ),
                "done_when": (
                    "At least three dated historical slices have comparable "
                    "actor, person-role, recipient, and relation coverage."
                ),
                "claim_boundary": (
                    "Do not project current organizations or roles backward."
                ),
            }
        ),
        add_metadata(
            {
                "search_task_id": "H2SR008",
                "priority": "P1",
                "mode": "online",
                "target": "formation mechanism and negative cases",
                "task": (
                    "Collect founding statements and chronology linking base "
                    "harms or garrison-care needs to organization formation; "
                    "also collect organizations that did not form or did not "
                    "cross the proposed boundary."
                ),
                "done_when": (
                    "Each causal episode has dated inputs, competing "
                    "explanations, and at least one non-confirming case."
                ),
                "claim_boundary": (
                    "Formation sequence alone is not a causal estimate."
                ),
            }
        ),
        add_metadata(
            {
                "search_task_id": "H2SR009",
                "priority": "P0",
                "mode": "online",
                "target": "current private-organization/service universe",
                "task": (
                    "Audit the official MCIPAC/MCCS private-organization "
                    "directory and the North Island Okinawa Spouses' Club "
                    "site (https://www.okinawa.usmc-mccs.org/more/"
                    "private-organizations; https://www.niosc.org/about-us); "
                    "crosswalk currently active service/charity groups that "
                    "are absent from the registry."
                ),
                "done_when": (
                    "Every potentially relevant current group has an identity "
                    "decision, functional relevance rule, source URL/date, "
                    "and add/background/exclude/defer recommendation."
                ),
                "claim_boundary": (
                    "The current nine actors are a registry-defined comparison "
                    "subset, not a census; do not actorize every authorized "
                    "private organization or infer a political stance."
                ),
            }
        ),
    ]

    service_issue_rows = [
        row for row in current_issues if row["actor_id"] in service_set
    ]
    accountability_issue_rows = [
        row for row in current_issues if row["actor_id"] in accountability_set
    ]
    accountability_reviewed_anchor_actor_ids = {
        row["actor_id"]
        for row in accountability_issue_rows
        if row["issue_id"] in ACCOUNTABILITY_ANCHOR_ISSUE_IDS
        and row.get("review_layer") == "human_reviewed"
    }
    accountability_candidate_only_actor_ids = (
        accountability_set - accountability_reviewed_anchor_actor_ids
    )
    source_overlap_ids = set(service_source_actor_ids) & set(
        accountability_source_actor_ids
    )
    place_overlap_ids = {
        row["place_id"]
        for row in place_rows
        if row["overlap_status"] == "same_place_node_observed"
    }
    r10_relation_categories = Counter(
        row["ecology_relation"] for row in r10_rows
    )
    dyadic_categories = Counter(
        row["ecology_relation"] for row in dyadic_rows
    )
    metrics = {
        "as_of_date": AS_OF_DATE,
        "package_scope": "research_only",
        "package_claim_status": "candidate_analysis",
        "frontend_eligibility": "excluded_research_only",
        "registry_history_rows": len(registry),
        "active_registry_actors": len(current_actors),
        "service_core_actor_count": len(service_core),
        "service_core_actor_ids": list(service_core),
        "accountability_comparison_actor_count": len(accountability),
        "accountability_human_reviewed_anchor_actor_count": len(
            accountability_reviewed_anchor_actor_ids
        ),
        "accountability_candidate_only_anchor_actor_count": len(
            accountability_candidate_only_actor_ids
        ),
        "accountability_anchor_issue_ids": sorted(
            ACCOUNTABILITY_ANCHOR_ISSUE_IDS
        ),
        "actor_set_overlap_count": len(service_set & accountability_set),
        "service_active_issue_edge_count": len(service_issue_rows),
        "service_active_issue_ids": sorted(
            {row["issue_id"] for row in service_issue_rows}
        ),
        "service_human_reviewed_issue_edge_count": sum(
            row.get("review_layer") == "human_reviewed"
            for row in service_issue_rows
        ),
        "service_candidate_issue_edge_count": sum(
            row.get("review_layer") == "candidate"
            for row in service_issue_rows
        ),
        "service_anchor_issue_edge_count": sum(
            row["issue_id"] in ACCOUNTABILITY_ANCHOR_ISSUE_IDS
            for row in service_issue_rows
        ),
        "accountability_active_issue_edge_count": len(
            accountability_issue_rows
        ),
        "reviewed_dyadic_relation_count": len(reviewed_dyadic),
        "candidate_dyadic_relation_count": len(candidate_dyadic),
        "dyadic_relation_categories": dict(sorted(dyadic_categories.items())),
        "cross_ecology_dyadic_observed_count": len(dyadic_cross_rows),
        "case_role_count": len(case_rows),
        "service_core_case_role_count": sum(
            row["actor_ecology"] == "service_core" for row in case_rows
        ),
        "typed_event_observation_count": len(event_rows),
        "cross_ecology_event_observed_count": len(event_cross_rows),
        "r10_purposive_relation_count": len(r10_rows),
        "r10_relation_categories": dict(
            sorted(r10_relation_categories.items())
        ),
        "r10_cross_ecology_observed_count": len(r10_cross_rows),
        "r10_official_source_universe_row_count": len(
            inputs["r10_universe"]
        ),
        "r10_identity_crosswalked_service_core_row_count": len(
            crosswalked_service_universe_rows
        ),
        "service_unique_place_count": len(
            {row["place_id"] for row in service_place_rows}
        ),
        "accountability_unique_place_count": len(
            {row["place_id"] for row in accountability_place_rows}
        ),
        "shared_place_node_count": len(place_overlap_ids),
        "shared_place_node_ids": sorted(place_overlap_ids),
        "service_issue_source_id_count": len(service_source_actor_ids),
        "accountability_issue_source_id_count": len(
            accountability_source_actor_ids
        ),
        "shared_issue_source_id_count": len(source_overlap_ids),
        "shared_issue_source_ids": sorted(source_overlap_ids),
        "service_non_source_ref_count": len(service_non_source_refs),
        "service_non_source_refs": sorted(service_non_source_refs),
        "accountability_non_source_ref_count": len(
            accountability_non_source_refs
        ),
        "public_person_overlap_status": "not_measured_no_person_role_table",
        "complete_recipient_network_status": "not_measured_incomplete_records",
        "base_production_causal_status": "hypothesis_only",
        "publication_status": "not_publication_ready_requires_human_review",
    }

    return {
        "service_core": service_rows,
        "accountability": accountability_rows,
        "issue_profiles": issue_profiles,
        "dyadic": dyadic_rows,
        "case_roles": case_rows,
        "typed_events": event_rows,
        "r10": r10_rows,
        "places": place_rows,
        "sources": source_rows,
        "gaps": gaps,
        "human_review_queue": human_review_queue,
        "search_queue": search_queue,
        "metrics": metrics,
    }


def validate_analysis(analysis: Mapping[str, Any]) -> None:
    metrics = analysis["metrics"]
    if metrics["service_core_actor_ids"] != list(EXPECTED_SERVICE_CORE_IDS):
        raise ValueError("Service core ID order/content drifted.")
    if metrics["service_core_actor_count"] != 9:
        raise ValueError("H2 v1 requires exactly nine service-core actors.")
    if (
        metrics["accountability_human_reviewed_anchor_actor_count"]
        + metrics["accountability_candidate_only_anchor_actor_count"]
        != metrics["accountability_comparison_actor_count"]
    ):
        raise ValueError("Accountability evidence-layer split is incomplete.")
    if metrics["actor_set_overlap_count"] != 0:
        raise ValueError("Comparison groups unexpectedly overlap.")
    if metrics["service_anchor_issue_edge_count"] != 0:
        raise ValueError(
            "A service-core actor now has an accountability-anchor issue edge; "
            "human interpretation is required before rebuilding H2."
        )
    if any(
        row["package_scope"] != "research_only"
        or row["frontend_eligibility"] != "excluded_research_only"
        for key, rows in analysis.items()
        if isinstance(rows, list)
        for row in rows
    ):
        raise ValueError("A research-only metadata boundary is missing.")
    if not any(
        row["gap_family"] == "public_person_roles"
        and row["current_status"] == "not_measured"
        for row in analysis["gaps"]
    ):
        raise ValueError("Public-person gap is not explicit.")
    if not any(
        row["gap_family"] == "service_recipient_universe"
        and row["current_status"] == "incomplete"
        for row in analysis["gaps"]
    ):
        raise ValueError("Recipient-universe gap is not explicit.")
    if any(row["human_decision"] for row in analysis["human_review_queue"]):
        raise ValueError("The script must not make human decisions.")
    if metrics["r10_official_source_universe_row_count"] != 616:
        raise ValueError("R10 official source-universe boundary drifted.")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"Refusing to write empty CSV without a schema: {path}")
    fieldnames: list[str] = []
    seen: set[str] = set()
    for row in rows:
        for key in row:
            if key not in seen:
                fieldnames.append(key)
                seen.add(key)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def render_brief(analysis: Mapping[str, Any]) -> str:
    m = analysis["metrics"]
    dyadic = m["dyadic_relation_categories"]
    return f"""# H2 两套功能生态研究 brief v1

状态：`research_only`／`candidate_analysis`／不进入中央数据与已核前端
数据日期：{AS_OF_DATE}

## 研究命题

候选命题不把服务组织预设为“亲基地”，也不预设两个社会彼此隔绝。本包检验一个更窄的问题：

> 围绕基地建设、运行与部署，当前公开资料是否呈现一套限制／问责型组织生态和一套驻军生活照护／慈善型组织生态？现有可核组织关系中，两者之间记录了什么，尚未测量什么？

“基地生产两套 NGO”仍是待检验的因果假设。当前数据只能描述功能并存、关系记录与资料缺口。

## 机械分组

- 服务核心不是手选结论：从当前 registry 机械选择 `us_origin` 且 actor class 为基地社区服务、军属配偶慈善网络或军属配偶俱乐部的有效 actor，并断言结果必须是既有 9 个 ID：`{";".join(m["service_core_actor_ids"])}`。这 9 个是 **registry 比较子集，不是基地 private organization／服务组织总体**；H2SR009 已记录官方目录与 NIOSC 身份补查。
- 限制／问责比较组不是按组织名挑选：任何当前有效 civic actor 只要至少有一条具体争议锚点议题边便进入；政府、资助、企业赞助和服务 actor 排除。当前为 {m["accountability_comparison_actor_count"]} 个候选比较 actor，其中 {m["accountability_human_reviewed_anchor_actor_count"]} 个至少有一条人审锚点边，{m["accountability_candidate_only_anchor_actor_count"]} 个只由候选锚点边选入。
- 宽泛的 `peace`、`women`、`human_rights`、`solidarity`、一般 `environment` 或 `mobilization` 不单独触发入组，避免为了结论扩大比较组。

## 当前可复算观察

1. 9 个服务核心 actor 有 {m["service_active_issue_edge_count"]} 条当前有效议题边，其中 {m["service_human_reviewed_issue_edge_count"]} 条人审、{m["service_candidate_issue_edge_count"]} 条候选；议题只落在 `{";".join(m["service_active_issue_ids"])}`。当前没有服务核心 actor 的具体限制／问责锚点边。这个结果支持功能分层，不支持推断其现实政治态度。
2. 当前 typed dyadic layer 只有 {m["reviewed_dyadic_relation_count"]} 条已核＋{m["candidate_dyadic_relation_count"]} 条候选。按外挂分组重算，服务生态内部为 {dyadic.get("service_ecology_internal", 0)} 条，限制／问责内部为 {dyadic.get("accountability_internal", 0)} 条；这 {m["reviewed_dyadic_relation_count"] + m["candidate_dyadic_relation_count"]} 条输入中**尚未编码**直接跨生态关系（{m["cross_ecology_dyadic_observed_count"]} 条）。
3. 另有 {m["case_role_count"]} 条法律案件角色和 {m["typed_event_observation_count"]} 条类型化事件记录，服务核心案件角色为 {m["service_core_case_role_count"]}、直接跨生态事件为 {m["cross_ecology_event_observed_count"]}。它们是两个不同目的性小样本，不是独立普查或总体发生率。
4. R10 的 {m["r10_purposive_relation_count"]} 条目的性关系样本中，直接跨生态关系为 {m["r10_cross_ecology_observed_count"]}；S002 的 {m["r10_official_source_universe_row_count"]} 条来源行里，经现成人审 identity crosswalk 明确映射到服务核心的行数为 {m["r10_identity_crosswalked_service_core_row_count"]}。后一个零不表示县域或基地社区没有接口，因为 HR-032 只审了特定 identity/JV 问题，不是服务 actor 全量查找。
5. 两组共享 {m["shared_place_node_count"]} 个地点节点：`{";".join(m["shared_place_node_ids"])}`；P001 是全县宽节点，具体基地共址只有 P005 嘉手纳。P004 Futenma 与 P010 MCAS Futenma 的分点还会低估语义邻近，因此这里只是地点编码下界，不表示接触、共享成员或协作。
6. 服务核心议题边使用 {m["service_issue_source_id_count"]} 个规范 source ID，比较组使用 {m["accountability_issue_source_id_count"]} 个，当前 source-ID 交集为 {m["shared_issue_source_id_count"]}。X001／X008／X009 另有非 S token，因此这个零首先是资料渠道与编码指标，不是社会隔离指标。

因此，本包当前最强的安全陈述是：

> 按当前 registry 与候选锚点规则得到 9 个服务侧比较 actor 和 65 个问责侧候选 actor（18 个至少有一条人审锚点边、47 个仅有候选边）。14 条已核＋8 条候选 dyadic、4 条 typed-event 与 35 条 R10 目的性记录中，尚未编码出直接跨组组织关系；27 条法律案件角色中没有服务侧 actor。人物重叠未测，recipient 网络不完整。

## 不能从零记录推出什么

- 人物共享**尚未测量**。仓库没有可用于该比较的系统 `person–actor–time` 表，因此不能写“没有共享人员”或“共享人员为零”。
- AWWA／KOSC／NOSCO／OESC／MOSCO／ACGO 的完整 recipient 网络**尚未测量**。具名事例和长期累计口径不能替代年度 recipient 表。
- 当前服务／慈善资料没有形成可核的基地政策立场边；这不等于组织“亲基地”“反基地”或“非政治”。
- 两组 ID 不重合部分来自分析定义；真正有信息量的是当前议题边、typed relation、案件／事件角色及 recipient 接口仍未出现直接跨组记录。
- 当前样本偏近期、偏官网／军事公共事务／税务记录与运动／法律材料两套资料渠道，不能代表复归后总体。

## 竞争性解释

1. **真实制度边界**：基地准入、语言、会员资格、军属身份和任务分工可能形成真实的组织隔离。
2. **资料渠道边界**：英文军事／组织／税务资料与日文运动／法律资料彼此不引用，使实际接口不可见。
3. **分类与抽样效应**：registry 是价值驱动样本，服务 actor 和限制 actor 又由不同模块进入，关系零值可能被研究设计放大。
4. **公开沉默**：服务组织可能避免公开基地政策表态；没有声明不等于没有成员态度或非公开社会联系。
5. **recipient 中介**：福利设施、社区团体、供应商或个人可能形成间接接口，而完整 recipient 与人物角色尚缺。
6. **时间错位**：共享人员或组织接口可能发生在不同年份；当前表没有系统领导层任期。

## 最小验证

先完成 `further_search_queue_v1.csv` 的 P0：

- 为 9 个服务核心 actor 建立 2012–2026 公开人物—组织—时间表；
- 取得 AWWA／KOSC 的 Form 990 Schedule I、年报或等价 recipient 记录；
- 对服务侧与限制侧执行双向组织名／关键词检索并保留无结果日志；
- 将具名 recipient 与 121 个有效 actor 及 S002 616 条来源行 crosswalk。

只有完成后，才能把“未观测到直接组织边”升级为带明确年份、组织集合、资料覆盖和分母的负面发现。1972–2011 的历史主张仍需当地报刊、会报、名录与组织档案。

## 人工门禁

`human_review_queue_v1.csv` 的 7 项决定均为空。项目负责人需先判断分组口径、零关系措辞、地点与 source overlap 的解释、立场边界和因果语言。本包不会自动回写中央表，也不会进入“已核视图”。
"""


def render_readme() -> str:
    return f"""# H2 两套功能生态外挂研究包 v1

本目录是 `research_only`／`candidate_analysis` 包。它只读现有 registry、当前 actor–issue／actor–place、typed relations、案件角色、类型化事件和 R10 表，不修改中央数据，不进入探索前端，不批准政治立场、人物重叠或因果结论。

## 复现

```powershell
python scripts\\make_h2_two_ecologies_v1.py
python -m unittest tests.test_make_h2_two_ecologies_v1
```

构建使用固定数据日期 `{AS_OF_DATE}`，不写运行时间；相同输入应产生字节一致的输出。

## 文件

- `service_core_actors_v1.csv`：由 class＋origin 规则推导并断言的 9 个服务核心 actor。
- `accountability_comparison_actors_v1.csv`：由具体争议锚点议题机械选择的比较组。
- `issue_ecology_profile_v1.csv`：两组当前议题边构成。
- `dyadic_relation_ecology_audit_v1.csv`：14 条已核＋8 条候选 typed dyadic relation 的外挂分组。
- `case_role_ecology_audit_v1.csv`：27 条案件角色的外挂分组。
- `typed_event_ecology_audit_v1.csv`：类型化事件关系的外挂分组。
- `r10_interface_audit_v1.csv`：R10 目的性关系样本的外挂分组。
- `place_overlap_v1.csv`：同地点节点审计；同地不等于关系。
- `source_overlap_v1.csv`：议题边 source-ID 渠道审计；来源交集不等于社会联系。
- `coverage_gaps_v1.csv`：人物、recipient、立场、因果与历史覆盖缺口。
- `human_review_queue_v1.csv`：7 项空白人工决定。
- `further_search_queue_v1.csv`：线上／当地进一步检索任务。
- `metrics_v1.json`：机器可读计数与状态。
- `manifest.json`：输入 hash、行数、方法与输出清单。
- `H2_two_ecologies_brief_v1.md`：解释 brief。

## 强制边界

- “未观测到跨生态组织边”不是“不存在共享人员或社会联系”。
- 人物共享没有系统输入，状态只能是 `not_measured`，不能编码为零。
- 完整 recipient 网络没有取得，具名实例和 aggregate 不能补成全量。
- 服务／慈善功能不产生亲基地、反基地或非政治立场。
- “基地生产两套 NGO”仍是需要形成史、负案例与竞争解释的因果假设。
- 所有 CSV 行都带 `package_scope=research_only` 和 `frontend_eligibility=excluded_research_only`。
"""


def make_manifest(
    root: Path,
    analysis: Mapping[str, Any],
) -> dict[str, Any]:
    input_entries = []
    for relative in INPUT_PATHS:
        path = root / relative
        if path.suffix == ".csv":
            row_count = len(read_csv(path))
        else:
            payload = read_json(path)
            if isinstance(payload, list):
                row_count = len(payload)
            elif isinstance(payload, dict):
                row_count = sum(
                    len(value)
                    for value in payload.values()
                    if isinstance(value, list)
                )
            else:
                row_count = 1
        input_entries.append(
            {
                "path": relative.as_posix(),
                "sha256": sha256(path),
                "row_count_or_list_items": row_count,
            }
        )
    return {
        "package_id": PACKAGE_ID,
        "as_of_date": AS_OF_DATE,
        "package_scope": "research_only",
        "package_claim_status": "candidate_analysis",
        "frontend_eligibility": "excluded_research_only",
        "publication_status": "not_publication_ready_requires_human_review",
        "method": {
            "service_core": (
                "active registry + declared service classes + us_origin; "
                "exact nine IDs asserted"
            ),
            "accountability_comparison": (
                "active civic actors with at least one active edge in the "
                "declared specific accountability anchor issue set; non-civic "
                "and service classes excluded"
            ),
            "relations": (
                "read-only recoding of current reviewed/candidate typed "
                "dyadic, case role, typed event, and R10 observations"
            ),
            "people": "not measured; no systematic person-actor-time input",
            "recipients": "incomplete; named examples are not a universe",
        },
        "inputs": input_entries,
        "outputs": sorted(OUTPUT_FILENAMES),
        "metrics": analysis["metrics"],
        "non_inference_boundaries": [
            "candidate relations are not final findings",
            "zero encoded cross relations do not prove no shared people",
            "same place does not prove contact or alliance",
            "service function does not establish political stance",
            "recipient aggregates are not named annual relations",
            "coexistence does not establish causal production",
        ],
    }


def build_package(
    output_dir: Path = OUTPUT_DIR,
    root: Path = ROOT,
) -> set[Path]:
    inputs = load_inputs(root)
    analysis = build_analysis(inputs)
    validate_analysis(analysis)
    output_dir.mkdir(parents=True, exist_ok=True)

    csv_outputs = {
        "service_core_actors_v1.csv": analysis["service_core"],
        "accountability_comparison_actors_v1.csv": analysis[
            "accountability"
        ],
        "issue_ecology_profile_v1.csv": analysis["issue_profiles"],
        "dyadic_relation_ecology_audit_v1.csv": analysis["dyadic"],
        "case_role_ecology_audit_v1.csv": analysis["case_roles"],
        "typed_event_ecology_audit_v1.csv": analysis["typed_events"],
        "r10_interface_audit_v1.csv": analysis["r10"],
        "place_overlap_v1.csv": analysis["places"],
        "source_overlap_v1.csv": analysis["sources"],
        "coverage_gaps_v1.csv": analysis["gaps"],
        "human_review_queue_v1.csv": analysis["human_review_queue"],
        "further_search_queue_v1.csv": analysis["search_queue"],
    }
    written: set[Path] = set()
    for filename, rows in csv_outputs.items():
        path = output_dir / filename
        write_csv(path, rows)
        written.add(path)

    metrics_path = output_dir / "metrics_v1.json"
    metrics_path.write_text(
        json.dumps(
            analysis["metrics"],
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    written.add(metrics_path)

    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(
        json.dumps(
            make_manifest(root, analysis),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    written.add(manifest_path)

    brief_path = output_dir / "H2_two_ecologies_brief_v1.md"
    brief_path.write_text(render_brief(analysis), encoding="utf-8")
    written.add(brief_path)

    readme_path = output_dir / "README.md"
    readme_path.write_text(render_readme(), encoding="utf-8")
    written.add(readme_path)

    observed_names = {path.name for path in written}
    if observed_names != OUTPUT_FILENAMES:
        raise ValueError(
            f"Output contract mismatch: {observed_names ^ OUTPUT_FILENAMES}"
        )
    return written


def main() -> None:
    written = build_package()
    print(
        f"Wrote {len(written)} research-only H2 files to "
        f"{OUTPUT_DIR.relative_to(ROOT)}"
    )


if __name__ == "__main__":
    main()
