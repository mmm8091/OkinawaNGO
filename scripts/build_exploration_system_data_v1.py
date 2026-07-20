from __future__ import annotations

"""Build the single frontend data adapter for the exploration system.

The public interface is ``build_exploration_system_data(project_root,
output_dir)``. Callers do not interpret central CSV files themselves.

Typed relation collections follow ``data/metadata/coding_schema_v1.md``:
the HR-033 typed handoff rows are authoritative for their ids, the
remaining funding-sample rows are derived without inventing human
decisions, and rejected/duplicate rows never reach any output layer.
"""

import csv
import hashlib
import json
from pathlib import Path
from typing import Any


ARTIFACT_AS_OF_DATE = "2026-07-20"
DEMO_RELATION_STATUSES = {"human_checked", "human_revised"}
DEMO_EPISODE_STATUSES = {
    "human_checked",
    "accepted_process",
    "accepted_process_with_local_gap",
}
EPISODE_DISPLAY_FIELDS = (
    "display_label",
    "local_problem",
    "translation_frame",
    "venue_label",
    "observable_output",
    "substantive_result",
    "interpretation_limit",
)
EPISODE_DISPLAY_LANGUAGES = ("zh", "ja", "en")
EPISODE_SOURCE_FIELDS = {
    "display_label": "short_label",
    "local_problem": "local_problem",
    "translation_frame": "translation_frame",
    "venue_label": "venue",
    "observable_output": "observable_output",
    "substantive_result": "substantive_result",
    "interpretation_limit": "interpretation_limit",
}
EPISODE_DISPLAY_COLUMNS = {
    "episode_id",
    "field",
    *EPISODE_DISPLAY_LANGUAGES,
    "review_note",
}
COVERAGE_IMPLICATION_FIELDS = (
    "observed_skew",
    "visibility_mechanism",
    "impact_on_q1_q3",
    "interpretation_limit",
    "online_gap_action",
    "local_gap_action",
)
COVERAGE_IMPLICATION_SOURCE_FIELDS = {
    "observed_skew": "observed_skew",
    "visibility_mechanism": "visibility_mechanism",
    "impact_on_q1_q3": "impact_on_q1_q3",
    "interpretation_limit": "interpretation_boundary",
    "online_gap_action": "online_gap_action",
    "local_gap_action": "local_gap_action",
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

# --- Typed relation observations (coding_schema_v1) ---

LEGAL_RELATION_REVIEW_STATUSES = {
    "ai_seeded",
    "human_checked",
    "human_revised",
    "needs_second_source",
    "needs_local_retrieval",
    "rejected",
}
LEGACY_RELATION_REVIEW_STATUSES = {"verified", "human_verified", "accepted"}

# coding_schema_v1 section 9 display fields, in the HR-033 handoff column order.
TYPED_RELATION_FIELDS = [
    "id",
    "observation_kind",
    "relation_family",
    "relation_type",
    "source_endpoint",
    "target_endpoint",
    "source_role",
    "target_role",
    "scope_kind",
    "scope_id",
    "evidence_level",
    "review_status",
    "human_decision",
    "review_scope",
    "reviewed_fields",
    "claim_status",
    "confirmed_scope",
    "missing_scope",
    "graph_eligibility",
    "display_tier",
    "source_ids",
    "interpretation_limit",
    "amount",
    "currency",
    "amount_semantics",
    "date_or_period",
]
TYPED_REQUIRED_NONEMPTY_FIELDS = (
    "id",
    "observation_kind",
    "relation_family",
    "relation_type",
    "source_endpoint",
    "target_endpoint",
    "evidence_level",
    "review_status",
    "claim_status",
    "graph_eligibility",
    "display_tier",
)

RELATION_FAMILY_BY_TYPE = {
    "donation": "resources_funding",
    "sponsorship": "resources_funding",
    "grant": "resources_funding",
    "funding_contribution": "resources_funding",
    "aggregate_history": "resources_funding",
    "aggregate_financial_history_observation": "resources_funding",
    "aggregate_financial_contribution": "resources_funding",
    "in_kind_donation": "resources_funding",
    "in_kind_acquisition_assistance": "resources_funding",
    "joint_in_kind_contribution": "resources_funding",
    "commission": "commission_service",
    "ngo_consultant_commission": "commission_service",
    "service": "commission_service",
    "site_presence": "commission_service",
    "legal_counsel": "legal_collaboration",
    "legal_support": "legal_collaboration",
    "organizational_affiliation": "structural_affiliation",
    "network_membership": "structural_affiliation",
    "solidarity_branch": "structural_affiliation",
    "coordination": "coordination",
    "partnership": "coordination",
    "partner_action": "coordination",
    "administrative_collaboration": "coordination",
    "event_collaboration": "coordination",
    "event_affiliation": "coordination",
    "grant_opportunity": "lead",
    "co_presence_lead": "lead",
    "co_presence_observation": "lead",
}
LEAD_RELATION_TYPES = {
    "grant_opportunity",
    "co_presence_lead",
    "co_presence_observation",
}

TYPED_INTERPRETATION_LIMITS = {
    "resources_funding": (
        "A documented donation, sponsorship, grant, or contribution is not evidence "
        "of a stable alliance, control, influence, or a base-policy position; sponsor "
        "tiers and project costs are not payment amounts."
    ),
    "commission_service": (
        "A commission, service, or site-presence record is an administrative or "
        "service relation; it is not movement-network membership, a political "
        "stance, or a funding chain beyond the stated mechanism."
    ),
    "legal_collaboration": (
        "A legal counsel or legal support relation is case-specific and does not by "
        "itself prove a stable alliance."
    ),
    "structural_affiliation": (
        "Membership or organizational affiliation does not show control, funding, "
        "political alliance, or a common policy position."
    ),
    "coordination": (
        "A documented coordination, partnership, or joint action record is not a "
        "stable alliance, a funding relation, or a shared policy position."
    ),
    "research_lead": (
        "This row is a research lead (opportunity, co-presence, or unknown "
        "recipient), not a confirmed relation or funding fact; it never enters the "
        "organization relation graph."
    ),
    "aggregate_observation": (
        "An aggregate observation cannot be allocated to individual recipients and "
        "does not enter the organization relation graph."
    ),
}

COLLECTION_BY_GRAPH_ELIGIBILITY = {
    "dyadic_relation": "dyadic_relations",
    "administrative_record": "administrative_records",
    "aggregate_observation": "aggregate_observations",
    "research_lead": "relation_leads",
    "event_participation": "event_participation",
}

LIFECYCLE_REVIEW_STATUSES = {"human_checked", "human_revised"}
LIFECYCLE_INTERPRETATION_LIMITS = {
    "dissolved": (
        "Dissolution applies only to the named organization and date shown; later "
        "activity by former participants must not be attributed back to it."
    ),
    "reorganized": (
        "A reorganization/successor anchor records a bounded lineage transition, "
        "not identity, merger, or uninterrupted organizational continuity."
    ),
    "continuity_unverified": (
        "The last observed activity date is a lower bound only; absence of later "
        "public records is not evidence of dissolution or inactivity."
    ),
}
LIFECYCLE_LOCALIZED_TEXT = {
    "dissolved": {
        "confirmed_scope": {
            "zh": "该组织于 {date} 解散。",
            "ja": "当該団体は {date} に解散。",
            "en": "The organization dissolved on {date}.",
        },
        "missing_scope": {"zh": "", "ja": "", "en": ""},
        "interpretation_limit": {
            "zh": "解散只适用于该具名组织和所示日期；原参与者此后的行动不能回填给该组织。",
            "ja": "解散は表示された団体と日付に限る。元参加者の後日の活動を当該団体へ遡及帰属させない。",
            "en": LIFECYCLE_INTERPRETATION_LIMITS["dissolved"],
        },
    },
    "reorganized": {
        "confirmed_scope": {
            "zh": "{date} 出现向后继载体过渡的重组边界。",
            "ja": "{date} に後継組織への再編境界を記録。",
            "en": "A transition to a successor vehicle is recorded at {date}.",
        },
        "missing_scope": {
            "zh": "精确解散日，以及前身与后继是否具有不间断的同一身份，仍未确认。",
            "ja": "正確な解散日と、前身・後継間の切れ目のない同一性は未確認。",
            "en": "Exact dissolution date and uninterrupted identity with the successor are not established.",
        },
        "interpretation_limit": {
            "zh": "重组／后继锚点只记录有界的谱系过渡，不表示两个组织同一、合并或连续性不间断。",
            "ja": "再編・後継アンカーは限定的な系譜移行を示すだけで、同一性、合併、連続性を意味しない。",
            "en": LIFECYCLE_INTERPRETATION_LIMITS["reorganized"],
        },
    },
    "continuity_unverified": {
        "confirmed_scope": {
            "zh": "公开材料至少可将该组织的活动追踪至 {date}。",
            "ja": "公開資料では当該団体の活動を少なくとも {date} まで追跡できる。",
            "en": "Public records trace the organization at least through {date}.",
        },
        "missing_scope": {
            "zh": "此后的持续性、当前状态及任何解散日期仍未确认。",
            "ja": "その後の継続性、現在の状態、解散日は未確認。",
            "en": "Current continuity, later activity, and any dissolution date remain unverified.",
        },
        "interpretation_limit": {
            "zh": "最后观察日只是活动可见性的下限；没有更晚公开记录，不等于组织已解散或停止活动。",
            "ja": "最終確認日は活動可視性の下限にすぎず、その後の公開記録がないことは解散や活動停止の証拠ではない。",
            "en": LIFECYCLE_INTERPRETATION_LIMITS["continuity_unverified"],
        },
    },
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


def normalize_presentation_rules(
    raw: dict[str, Any],
    actors: list[dict[str, Any]],
    places: list[dict[str, Any]],
) -> dict[str, Any]:
    """Validate versioned presentation mappings consumed by the frontend.

    Research classification and place-display mappings live in data, not React.
    This function rejects duplicate or orphaned mappings before they can affect
    the public view.
    """

    groups = raw.get("actor_class_groups", [])
    regions = raw.get("regions", [])
    periods = raw.get("time_periods", [])
    group_ids = [row.get("id", "") for row in groups]
    region_ids = [row.get("id", "") for row in regions]
    if not group_ids or len(group_ids) != len(set(group_ids)):
        raise ValueError("Presentation actor_class_groups require unique IDs")
    if "unknown" not in group_ids:
        raise ValueError("Presentation actor_class_groups require an unknown fallback")
    if not region_ids or len(region_ids) != len(set(region_ids)):
        raise ValueError("Presentation regions require unique IDs")

    actor_class_to_group: dict[str, str] = {}
    for group in groups:
        if not group.get("color"):
            raise ValueError(f"Presentation group {group['id']} lacks color")
        for actor_class in group.get("actor_classes", []):
            if actor_class in actor_class_to_group:
                raise ValueError(
                    f"Actor class {actor_class} appears in multiple presentation groups"
                )
            actor_class_to_group[actor_class] = group["id"]

    active_actor_classes = {
        row["actor_class"]
        for row in actors
        if row["display_status"] != "hidden" and row["actor_class"]
    }
    unmapped_actor_classes = sorted(active_actor_classes - set(actor_class_to_group))
    if unmapped_actor_classes:
        raise ValueError(
            "Presentation rules do not map current actor classes: "
            + ";".join(unmapped_actor_classes)
        )

    place_ids = {row["id"] for row in places}
    place_display_regions = raw.get("place_display_regions", {})
    orphan_place_ids = sorted(set(place_display_regions) - place_ids)
    invalid_display_regions = sorted(
        {
            region
            for region in place_display_regions.values()
            if region not in set(region_ids)
        }
    )
    if orphan_place_ids or invalid_display_regions:
        raise ValueError(
            "Invalid presentation place mappings: orphan_places="
            + ";".join(orphan_place_ids)
            + " invalid_regions="
            + ";".join(invalid_display_regions)
        )
    default_region = raw.get("default_place_display_region", "")
    if default_region not in set(region_ids):
        raise ValueError("Presentation default_place_display_region is invalid")

    period_ids = [row.get("id", "") for row in periods]
    if not period_ids or len(period_ids) != len(set(period_ids)):
        raise ValueError("Presentation time_periods require unique IDs")
    ordered_periods = sorted(periods, key=lambda row: int(row["from"]))
    for index, period in enumerate(ordered_periods):
        if int(period["from"]) > int(period["to"]):
            raise ValueError(f"Presentation period {period['id']} has reversed dates")
        if index and int(ordered_periods[index - 1]["to"]) >= int(period["from"]):
            raise ValueError("Presentation time_periods overlap")

    return {
        "schema_version": raw.get("schema_version", ""),
        "actor_class_groups": sorted(groups, key=lambda row: row["id"]),
        "actor_class_to_group": dict(sorted(actor_class_to_group.items())),
        "regions": sorted(regions, key=lambda row: row["id"]),
        "default_place_display_region": default_region,
        "place_display_regions": dict(sorted(place_display_regions.items())),
        "time_periods": ordered_periods,
    }


def normalize_genealogy_anchors(
    rows: list[dict[str, str]],
    actor_ids: set[str],
    source_aliases: dict[str, str],
) -> list[dict[str, Any]]:
    """Export only principal-reviewed, central-registry lifecycle anchors."""

    anchors: list[dict[str, Any]] = []
    for row in rows:
        if (
            row.get("registry_scope") != "central_registry"
            or row.get("lifecycle_workflow_status") != "resolved"
            or row.get("review_status") not in LIFECYCLE_REVIEW_STATUSES
        ):
            continue
        actor_id = row.get("actor_id", "")
        successor_actor_id = row.get("successor_actor_id", "")
        if actor_id not in actor_ids:
            raise ValueError(f"Lifecycle row {row['lifecycle_record_id']} has orphan actor")
        if successor_actor_id and successor_actor_id not in actor_ids:
            raise ValueError(
                f"Lifecycle row {row['lifecycle_record_id']} has orphan successor"
            )

        source_ids, unresolved_refs = resolve_source_refs(
            split_refs(row.get("source_refs", "")), source_aliases
        )
        direct_source_urls = sorted(
            ref for ref in unresolved_refs if ref.startswith(("http://", "https://"))
        )
        unresolved_source_refs = sorted(
            ref for ref in unresolved_refs if ref not in direct_source_urls
        )
        status = row.get("lifecycle_status", "")
        event_date = (
            row.get("status_date", "")
            or row.get("last_observed_activity_date", "")
        )
        if not event_date:
            raise ValueError(
                f"Lifecycle row {row['lifecycle_record_id']} lacks a bounded date"
            )
        bounded = status in {"reorganized", "continuity_unverified"}
        missing_scope = ""
        if status == "reorganized":
            missing_scope = (
                "Exact dissolution date and uninterrupted identity with the successor "
                "are not established."
            )
        elif status == "continuity_unverified":
            missing_scope = (
                "Current continuity, later activity, and any dissolution date remain "
                "unverified."
            )
        localized = LIFECYCLE_LOCALIZED_TEXT.get(status, {})
        localized_fields = {
            f"{field}_{language}": template.format(date=event_date)
            for field in (
                "confirmed_scope",
                "missing_scope",
                "interpretation_limit",
            )
            for language, template in localized.get(field, {}).items()
        }
        anchors.append(
            {
                "id": row["lifecycle_record_id"],
                "actor_id": actor_id,
                "display_label": row["canonical_name"],
                "lifecycle_status": status,
                "anchor_type": (
                    "last_observed_activity"
                    if status == "continuity_unverified"
                    else status
                ),
                "event_date": event_date,
                "status_date": row.get("status_date", ""),
                "last_observed_activity_date": row.get(
                    "last_observed_activity_date", ""
                ),
                "successor_actor_id": successor_actor_id,
                "status_basis": row.get("status_basis", ""),
                "evidence_level": row.get("evidence_level", ""),
                "review_status": row.get("review_status", ""),
                "claim_status": "supported_bounded" if bounded else "supported",
                "confirmed_scope": (
                    f"{status} lifecycle observation for {actor_id} at {event_date}"
                ),
                "missing_scope": missing_scope,
                "graph_eligibility": "genealogy_anchor",
                "display_tier": "reviewed",
                "display_status": "demo",
                "source_ids": source_ids,
                "direct_source_urls": direct_source_urls,
                "unresolved_source_refs": unresolved_source_refs,
                "interpretation_limit": LIFECYCLE_INTERPRETATION_LIMITS.get(
                    status,
                    "This lifecycle anchor is bounded to the reviewed status and date.",
                ),
                **localized_fields,
            }
        )
    return sorted(anchors, key=lambda row: (row["event_date"], row["id"]))


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


def validate_episode_display_overrides(
    episode_rows: list[dict[str, str]],
    display_rows: list[dict[str, str]],
) -> dict[tuple[str, str], dict[str, str]]:
    """Validate the translation-only episode display overlay.

    The Chinese display string is required to equal the central episode source
    field byte-for-byte.  This prevents presentation copy from silently
    rewriting a fact.  All three languages are required and non-empty; the
    normalizer keeps a defensive source-text fallback for older in-memory data.
    """
    episode_ids = [row["episode_id"] for row in episode_rows]
    if len(episode_ids) != len(set(episode_ids)):
        raise ValueError("Episode source contains duplicate episode IDs")
    expected_keys = {
        (episode_id, field)
        for episode_id in episode_ids
        for field in EPISODE_DISPLAY_FIELDS
    }
    malformed_rows = [
        index
        for index, row in enumerate(display_rows, start=2)
        if set(row) != EPISODE_DISPLAY_COLUMNS or None in row
    ]
    if malformed_rows:
        raise ValueError(
            "Episode display overlay has malformed columns or unquoted commas "
            f"on rows: {','.join(map(str, malformed_rows))}"
        )
    keys = [(row["episode_id"], row["field"]) for row in display_rows]
    duplicate_keys = sorted(
        {
            key
            for key in keys
            if keys.count(key) > 1
        }
    )
    if duplicate_keys:
        raise ValueError(
            "Episode display overlay has duplicate keys: "
            + ";".join(f"{episode_id}:{field}" for episode_id, field in duplicate_keys)
        )
    actual_keys = set(keys)
    missing = sorted(expected_keys - actual_keys)
    unexpected = sorted(actual_keys - expected_keys)
    if missing or unexpected:
        detail = []
        if missing:
            detail.append(
                "missing="
                + ";".join(f"{episode_id}:{field}" for episode_id, field in missing)
            )
        if unexpected:
            detail.append(
                "unexpected="
                + ";".join(
                    f"{episode_id}:{field}" for episode_id, field in unexpected
                )
            )
        raise ValueError(
            "Episode display overlay must cover the exact episode/field grid: "
            + " ".join(detail)
        )
    blank_translations = sorted(
        f"{row['episode_id']}:{row['field']}:{language}"
        for row in display_rows
        for language in EPISODE_DISPLAY_LANGUAGES
        if not row[language].strip()
    )
    if blank_translations:
        raise ValueError(
            "Episode display overlay requires non-empty zh/ja/en translations: "
            + ";".join(blank_translations)
        )
    source_by_id = {row["episode_id"]: row for row in episode_rows}
    overrides: dict[tuple[str, str], dict[str, str]] = {}
    for row in display_rows:
        key = (row["episode_id"], row["field"])
        source_text = source_by_id[row["episode_id"]][
            EPISODE_SOURCE_FIELDS[row["field"]]
        ]
        if row["zh"] != source_text:
            raise ValueError(
                "Episode display zh must equal the source text for "
                f"{row['episode_id']}:{row['field']}"
            )
        overrides[key] = {
            language: row[language]
            for language in EPISODE_DISPLAY_LANGUAGES
        }
    return overrides


def normalize_episodes(
    rows: list[dict[str, str]],
    source_aliases: dict[str, str],
    display_overrides: dict[tuple[str, str], dict[str, str]],
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
        translation_fallbacks = []
        for field in EPISODE_DISPLAY_FIELDS:
            source_text = normalized[field]
            translations = display_overrides[(row["episode_id"], field)]
            for language in EPISODE_DISPLAY_LANGUAGES:
                translated = translations[language]
                if not translated:
                    translated = source_text
                    translation_fallbacks.append(f"{field}:{language}")
                normalized[f"{field}_{language}"] = translated
        normalized["display_translation_fallbacks"] = translation_fallbacks
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
                    **{
                        f"display_label_{language}": episode[
                            f"{text_key}_{language}"
                        ]
                        for language in EPISODE_DISPLAY_LANGUAGES
                    },
                    "source_ids": episode["source_ids"],
                    "evidence_level": episode["evidence_level"],
                    "review_status": episode["review_status"],
                    "display_status": episode["display_status"],
                    "interpretation_limit": episode["interpretation_limit"],
                    **{
                        f"interpretation_limit_{language}": episode[
                            f"interpretation_limit_{language}"
                        ]
                        for language in EPISODE_DISPLAY_LANGUAGES
                    },
                }
            )
    return outcomes


# --- Actor-issue three-gate state derivation (frontend_actor_issue_state_handoff_v1) ---

ACTOR_ISSUE_DISPLAY_STATES = {
    "frozen_bounded",
    "accepted_unfrozen",
    "scope_reviewed_fact_pending",
    "fact_pending",
}
ACTOR_ISSUE_ACCEPTED_DISPLAY_STATES = {"frozen_bounded", "accepted_unfrozen"}
ACTOR_ISSUE_PASSTHROUGH_FIELDS = (
    "claim_status",
    "review_scope",
    "reviewed_fields",
    "scope_kind",
    "scope_claim_status",
    "scope_approved_formulation",
    "scope_boundary",
    "confirmed_scope",
    "missing_scope",
    "approved_formulation",
)


def derive_actor_issue_gate_states(row: dict[str, str]) -> dict[str, str]:
    """Derive the three independent actor-issue gates and the display state.

    The gates never substitute for each other: a scope review does not accept
    the fact edge, and a legacy accepted edge is never auto-filled to
    ``supported`` (frontend_actor_issue_state_handoff_v1, schema v1 section 1).
    """
    review_status = row["review_status"]
    if review_status in {"human_checked", "human_revised"}:
        fact_gate = "human_accepted"
    elif review_status == "needs_second_source":
        fact_gate = "needs_second_source"
    elif review_status == "needs_local_retrieval":
        fact_gate = "needs_local_retrieval"
    else:
        fact_gate = "fact_pending"
    scope_gate = (
        "scope_reviewed"
        if row.get("scope_review_status") == "human_checked"
        else "scope_pending"
    )
    if row.get("claim_status") == "supported_bounded":
        schema_freeze = "field_frozen"
    elif fact_gate == "human_accepted":
        schema_freeze = "legacy_field_freeze_pending"
    else:
        schema_freeze = ""
    if fact_gate == "human_accepted" and schema_freeze == "field_frozen":
        display_state = "frozen_bounded"
    elif fact_gate == "human_accepted":
        display_state = "accepted_unfrozen"
    elif scope_gate == "scope_reviewed":
        display_state = "scope_reviewed_fact_pending"
    else:
        display_state = "fact_pending"
    return {
        "fact_gate_status": fact_gate,
        "scope_gate_status": scope_gate,
        "schema_freeze_status": schema_freeze,
        "display_state": display_state,
    }


def normalize_actor_issue(
    rows: list[dict[str, str]],
    source_aliases: dict[str, str],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    demo: list[dict[str, Any]] = []
    research: list[dict[str, Any]] = []
    for row in rows:
        scope_status = row.get("scope_status", "")
        graph_eligibility = row.get("graph_eligibility", "")
        if (
            row["review_status"] == "rejected"
            or scope_status.startswith("retired")
            or "excluded" in scope_status
            or graph_eligibility in {"excluded", "research_lead"}
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
        normalized.update(derive_actor_issue_gate_states(row))
        for field in ACTOR_ISSUE_PASSTHROUGH_FIELDS:
            normalized[field] = row.get(field, "")
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


def normalize_typed_handoff_row(
    row: dict[str, str],
    source_aliases: dict[str, str],
) -> dict[str, Any]:
    """Pass an HR-033 typed handoff row through with resolved source IDs.

    The handoff is human-controlled; the row keeps its own review, claim,
    graph eligibility, and display tier values. Validation gates, not this
    function, reject illegal or inconsistent values.
    """
    missing = [field for field in TYPED_RELATION_FIELDS if field not in row]
    if missing:
        raise ValueError(
            f"HR-033 typed handoff row {row.get('id', '?')} misses fields: "
            + ";".join(missing)
        )
    source_ids, unresolved_source_refs = resolve_source_refs(
        split_refs(row["source_ids"]), source_aliases
    )
    normalized = {field: row[field] for field in TYPED_RELATION_FIELDS}
    normalized["source_ids"] = source_ids
    normalized["unresolved_source_refs"] = unresolved_source_refs
    normalized["event_or_program"] = ""
    normalized["place_label"] = ""
    normalized["funding_relation_confidence"] = ""
    normalized["review_notes"] = ""
    return normalized


def derive_funding_relation_row(
    row: dict[str, str],
    handoff_row: dict[str, str] | None,
    actor_ids: set[str],
    place_ids: set[str],
    source_aliases: dict[str, str],
) -> dict[str, Any] | None:
    """Derive one typed observation from a funding-sample row.

    Returns ``None`` for rejected rows, which are excluded from every output
    layer. Legacy review values raise instead of being silently migrated;
    only a human crosswalk (schema v1 section 12) may clear them.
    """
    edge_id = row["edge_id"]
    handoff_row = handoff_row or {}
    centrally_reviewed_fields = set(split_refs(row.get("reviewed_fields", "")))

    def preferred(field: str, central_field: str | None = None) -> str:
        """Use reviewed central metadata first, then the HR-033 handoff."""
        central_key = central_field or field
        central_value = row.get(central_key, "")
        if central_key in centrally_reviewed_fields:
            return central_value
        return central_value or handoff_row.get(field, "")

    review_status = row["review_status"]
    if review_status in LEGACY_RELATION_REVIEW_STATUSES:
        raise ValueError(
            f"Legacy review_status {review_status!r} on {edge_id}; schema v1 "
            "section 12 requires a human crosswalk before build."
        )
    if review_status not in LEGAL_RELATION_REVIEW_STATUSES:
        raise ValueError(f"Illegal review_status {review_status!r} on {edge_id}")
    if review_status == "rejected":
        return None
    relation_type = row["relation_type"]
    if relation_type not in RELATION_FAMILY_BY_TYPE:
        raise ValueError(f"Unmapped relation_type {relation_type!r} on {edge_id}")
    relation_family = RELATION_FAMILY_BY_TYPE[relation_type]
    is_lead = (
        relation_type in LEAD_RELATION_TYPES
        or preferred("graph_eligibility") == "research_lead"
    )
    source_endpoint = row["source_actor_id"]
    target_endpoint = row["target_actor_id"]
    source_resolved = source_endpoint in actor_ids
    target_resolved = target_endpoint in actor_ids

    # Human-reviewed central fields are authoritative. The handoff may fill a
    # central blank; only then may the adapter derive a conservative value.
    recorded_claim_status = preferred("claim_status")
    if recorded_claim_status:
        claim_status = recorded_claim_status
    elif is_lead:
        claim_status = "lead"
    elif review_status in {"human_checked", "human_revised"}:
        # A human-reviewed funding relation without a recorded amount is bounded:
        # the relation stands, the amount gap must stay visible.
        claim_status = (
            "supported_bounded"
            if relation_family == "resources_funding" and not row["amount"]
            else "supported"
        )
    else:
        claim_status = "candidate"

    recorded_graph_eligibility = preferred("graph_eligibility")
    if recorded_graph_eligibility:
        graph_eligibility = recorded_graph_eligibility
    elif is_lead:
        graph_eligibility = "research_lead"
    elif relation_type in {
        "aggregate_history",
        "aggregate_financial_history_observation",
    }:
        graph_eligibility = "aggregate_observation"
    elif relation_type in {
        "event_affiliation",
        "event_collaboration",
        "joint_in_kind_contribution",
        "partner_action",
    }:
        graph_eligibility = "event_participation"
    elif source_resolved and target_resolved:
        graph_eligibility = "dyadic_relation"
    elif target_endpoint.startswith("unknown") or target_endpoint.startswith("P_R10_"):
        graph_eligibility = "aggregate_observation"
    else:
        graph_eligibility = "administrative_record"

    display_tier = preferred("display_tier") or (
        "reviewed"
        if claim_status in {"supported", "supported_bounded"}
        and graph_eligibility != "research_lead"
        else "research"
    )

    if graph_eligibility == "dyadic_relation":
        scope_kind, scope_id = "relation", ""
    elif graph_eligibility == "aggregate_observation":
        scope_kind, scope_id = "aggregate_recipient_scope", target_endpoint
    elif graph_eligibility == "research_lead":
        scope_kind, scope_id = (
            ("unknown_recipient", "")
            if target_endpoint.startswith("unknown")
            else ("relation", "")
        )
    elif target_endpoint in place_ids:
        scope_kind, scope_id = "place", target_endpoint
    else:
        scope_kind = "non_registry_counterpart"
        scope_id = source_endpoint if not source_resolved else target_endpoint

    confirmed_scope = preferred("confirmed_scope")
    if not confirmed_scope and review_status in {"human_checked", "human_revised"}:
        confirmed_scope = (
            f"The {relation_type} relation between {source_endpoint} and "
            f"{target_endpoint} is recorded as human-reviewed in the central "
            "relation table; the stated proposition stands as reviewed."
        )
    missing_scope = preferred("missing_scope")
    if not missing_scope and claim_status == "supported_bounded":
        gaps = []
        if relation_family == "resources_funding" and not row["amount"]:
            gaps.append("the amount is not recorded on the relation row")
        if not (source_resolved and target_resolved):
            gaps.append(
                "recipient/counterpart scope is not itemized to named registry actors"
            )
        gaps.append(
            "v1 field-level review metadata (review_scope, reviewed_fields) is "
            "not recorded on the central row"
        )
        missing_scope = "; ".join(gaps) + "."

    limit_key = (
        graph_eligibility
        if graph_eligibility in {"research_lead", "aggregate_observation"}
        else relation_family
    )
    interpretation_limit = preferred("interpretation_limit") or (
        TYPED_INTERPRETATION_LIMITS[limit_key]
    )

    source_ids, unresolved_source_refs = resolve_source_refs(
        split_refs(row["source_ref"] or handoff_row.get("source_ids", "")),
        source_aliases,
    )
    return {
        "id": edge_id,
        "observation_kind": graph_eligibility,
        "relation_family": relation_family,
        "relation_type": relation_type,
        "source_endpoint": source_endpoint,
        "target_endpoint": target_endpoint,
        "source_role": preferred("source_role"),
        "target_role": preferred("target_role"),
        "scope_kind": scope_kind,
        "scope_id": scope_id,
        "evidence_level": row["evidence_level"],
        "review_status": review_status,
        "human_decision": preferred("human_decision"),
        "review_scope": preferred("review_scope"),
        "reviewed_fields": preferred("reviewed_fields"),
        "claim_status": claim_status,
        "confirmed_scope": confirmed_scope,
        "missing_scope": missing_scope,
        "graph_eligibility": graph_eligibility,
        "display_tier": display_tier,
        "source_ids": source_ids,
        "interpretation_limit": interpretation_limit,
        "amount": preferred("amount"),
        "currency": preferred("currency"),
        "amount_semantics": preferred("amount_semantics"),
        "date_or_period": (
            row["event_date"]
            or row["publication_date"]
            or handoff_row.get("date_or_period", "")
        ),
        "unresolved_source_refs": unresolved_source_refs,
        "event_or_program": row["event_or_program"],
        "place_label": row["place"],
        "funding_relation_confidence": row["funding_relation_confidence"],
        "review_notes": row["notes"],
    }


def build_typed_relation_collections(
    funding_rows: list[dict[str, str]],
    handoff_rows: list[dict[str, str]],
    actor_ids: set[str],
    place_ids: set[str],
    source_aliases: dict[str, str],
) -> tuple[
    dict[str, list[dict[str, Any]]],
    dict[str, list[dict[str, Any]]],
    list[str],
    int,
]:
    """Split typed observations into reviewed and research collections.

    HR-033 handoff rows override same-id funding rows. Rejected funding rows
    are counted as excluded and never serialized.
    """
    observations: list[dict[str, Any]] = []
    handoff_by_id = {row["id"]: row for row in handoff_rows}
    funding_ids = {row["edge_id"] for row in funding_rows}
    orphan_handoff_ids = sorted(set(handoff_by_id) - funding_ids)
    excluded_ids: list[str] = []
    for row in funding_rows:
        derived = derive_funding_relation_row(
            row,
            handoff_by_id.get(row["edge_id"]),
            actor_ids,
            place_ids,
            source_aliases,
        )
        if derived is None:
            excluded_ids.append(row["edge_id"])
            continue
        observations.append(derived)
    # HR-033 also contains R10R029, an approved aggregate observation whose
    # authoritative central home is the R10 amount layer rather than the
    # 43-row relation sample. Keep such explicitly typed handoff-only rows.
    for edge_id in orphan_handoff_ids:
        observations.append(
            normalize_typed_handoff_row(handoff_by_id[edge_id], source_aliases)
        )

    demo: dict[str, list[dict[str, Any]]] = {
        "dyadic_relations": [],
        "administrative_records": [],
        "aggregate_observations": [],
        "relation_leads": [],
        "event_participation": [],
    }
    research: dict[str, list[dict[str, Any]]] = {
        "dyadic_relations": [],
        "administrative_records": [],
        "aggregate_observations": [],
        "relation_leads": [],
        "event_participation": [],
        "genealogy_anchors": [],
    }
    for observation in observations:
        collection = COLLECTION_BY_GRAPH_ELIGIBILITY.get(
            observation["graph_eligibility"]
        )
        if collection is None:
            raise ValueError(
                f"Illegal graph_eligibility {observation['graph_eligibility']!r} "
                f"on {observation['id']}"
            )
        layer = demo if observation["display_tier"] == "reviewed" else research
        layer[collection].append(observation)
    for layer in (demo, research):
        for rows in layer.values():
            rows.sort(key=lambda row: row["id"])
    input_count = len(observations) + len(excluded_ids)
    return demo, research, sorted(excluded_ids), input_count


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
    display_overrides: dict[str, dict[str, dict[str, str]]],
) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []
    for row in rows:
        dimension_id = row["dimension_id"]
        item = {
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
        for field in COVERAGE_IMPLICATION_FIELDS:
            item.update(
                {
                    f"{field}_{language}": display_overrides[dimension_id][field][
                        language
                    ]
                    for language in EPISODE_DISPLAY_LANGUAGES
                }
            )
        normalized.append(item)
    return normalized


def validate_coverage_implication_display_overrides(
    implication_rows: list[dict[str, str]],
    raw: dict[str, Any],
) -> dict[str, dict[str, dict[str, str]]]:
    """Validate the research-semantic locale layer for coverage implications.

    The canonical source table remains unchanged and its English text must be
    reproduced byte-for-byte in the display metadata.  Chinese and Japanese
    renderings therefore cannot silently rewrite the audited research object,
    and React never has to invent or translate research meaning.
    """

    if raw.get("schema_version") != "1.0.0":
        raise ValueError("Coverage display metadata has an unsupported schema")
    if raw.get("source", {}).get("path") != (
        "outputs/coverage_audit_v1/coverage_bias_implications_v1.csv"
    ):
        raise ValueError("Coverage display metadata points to the wrong source table")
    if raw.get("languages") != list(EPISODE_DISPLAY_LANGUAGES):
        raise ValueError("Coverage display metadata must declare zh/ja/en in order")
    dimensions = raw.get("dimensions")
    if not isinstance(dimensions, list):
        raise ValueError("Coverage display metadata requires a dimensions array")

    source_ids = [row["dimension_id"] for row in implication_rows]
    if len(source_ids) != len(set(source_ids)):
        raise ValueError("Coverage implication source contains duplicate dimensions")
    actual_ids = [
        row.get("dimension_id", "") for row in dimensions if isinstance(row, dict)
    ]
    if len(actual_ids) != len(dimensions) or len(actual_ids) != len(set(actual_ids)):
        raise ValueError("Coverage display dimensions must be unique objects")
    missing = sorted(set(source_ids) - set(actual_ids))
    unexpected = sorted(set(actual_ids) - set(source_ids))
    if missing or unexpected:
        raise ValueError(
            "Coverage display metadata must cover the exact dimension set: "
            f"missing={';'.join(missing)} unexpected={';'.join(unexpected)}"
        )

    source_by_id = {row["dimension_id"]: row for row in implication_rows}
    overrides: dict[str, dict[str, dict[str, str]]] = {}
    for dimension in dimensions:
        dimension_id = dimension["dimension_id"]
        fields = dimension.get("fields")
        if not isinstance(fields, dict) or set(fields) != set(
            COVERAGE_IMPLICATION_FIELDS
        ):
            raise ValueError(
                f"Coverage display {dimension_id} must contain the exact field grid"
            )
        overrides[dimension_id] = {}
        for field in COVERAGE_IMPLICATION_FIELDS:
            translations = fields[field]
            if not isinstance(translations, dict) or set(translations) != set(
                EPISODE_DISPLAY_LANGUAGES
            ):
                raise ValueError(
                    f"Coverage display {dimension_id}:{field} requires zh/ja/en"
                )
            if any(
                not isinstance(translations[language], str)
                or not translations[language].strip()
                for language in EPISODE_DISPLAY_LANGUAGES
            ):
                raise ValueError(
                    f"Coverage display {dimension_id}:{field} has a blank translation"
                )
            source_text = source_by_id[dimension_id][
                COVERAGE_IMPLICATION_SOURCE_FIELDS[field]
            ]
            if translations["en"] != source_text:
                raise ValueError(
                    "Coverage display English must equal the audited source text for "
                    f"{dimension_id}:{field}"
                )
            overrides[dimension_id][field] = {
                language: translations[language]
                for language in EPISODE_DISPLAY_LANGUAGES
            }
    return overrides


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
    genealogy_anchors: list[dict[str, Any]],
    presentation: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    current_actor_ids = [
        row["id"] for row in actors if row["display_status"] != "hidden"
    ]
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
            "visual_states": ["all_regions", "sakishima_focus", "compare"],
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
                "Human-reviewed same-source triples appear in the region detail panel; "
                "they are not a separate map-density layer.",
            ],
        },
        "actors": {
            "view_id": "P2",
            "route": "/actors",
            "question": "谁在参与，以什么功能参与？",
            "visual_engine": "V2 组织—议题生态图",
            "visual_states": ["ecology", "issue_links", "focus", "compare"],
            "actor_ids": current_actor_ids,
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
        "time": {
            "view_id": "P5",
            "route": "/time",
            "question": "组织与事件在时间上如何出现、转变或停止？",
            "visual_engine": "V5 事件时间轴与有界组织谱系",
            "periods": presentation["time_periods"],
            "historical_anchor_ids": [row["id"] for row in genealogy_anchors],
            "event_anchors": [
                event_anchors[key] for key in sorted(event_anchors)
            ],
            "interpretation_limits": [
                "A lifecycle anchor records only the reviewed status and date shown.",
                "Last-observed activity is not proof of present continuity or dissolution.",
                "Event years do not establish organizational formation or lifespan.",
            ],
        },
        "global": {
            "view_id": "G1+G2",
            "time_layer": {
                "historical_anchor_ids": [row["id"] for row in genealogy_anchors],
                "event_anchors": [
                    event_anchors[key] for key in sorted(event_anchors)
                ],
                "coverage_periods": coverage_periods,
                "interpretation_limit": (
                    "Lifecycle anchors are bounded reviewed observations. Event and source "
                    "dates must not be used to fabricate organizational continuity."
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
            "presentation_path": "presentation.json",
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
    typed_demo_relations: dict[str, list[dict[str, Any]]],
    typed_research_relations: dict[str, list[dict[str, Any]]],
    case_roles: list[dict[str, Any]],
    typed_excluded_ids: list[str],
    coverage_cells: list[dict[str, Any]],
    case_ids: set[str],
    map_geometry: dict[str, Any],
    genealogy_anchors: list[dict[str, Any]],
    presentation: dict[str, Any],
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
    genealogy_anchor_ids = unique_ids(
        "unique genealogy anchor IDs", genealogy_anchors
    )
    check(
        "episode layers disjoint",
        demo_episode_ids.isdisjoint(research_episode_ids),
        f"demo={len(demo_episode_ids)} research={len(research_episode_ids)}",
    )
    check(
        "genealogy anchors are reviewed and actor-bounded",
        bool(genealogy_anchor_ids)
        and all(
            row["actor_id"] in actor_ids
            and (
                not row["successor_actor_id"]
                or row["successor_actor_id"] in actor_ids
            )
            and row["review_status"] in LIFECYCLE_REVIEW_STATUSES
            and row["claim_status"] in {"supported", "supported_bounded"}
            and row["graph_eligibility"] == "genealogy_anchor"
            and row["event_date"]
            for row in genealogy_anchors
        ),
        f"{len(genealogy_anchors)} reviewed lifecycle rows",
    )
    check(
        "bounded genealogy anchors carry explicit gaps",
        all(
            row["claim_status"] != "supported_bounded"
            or (
                row["confirmed_scope"]
                and row["missing_scope"]
                and row["interpretation_limit"]
            )
            for row in genealogy_anchors
        ),
        "supported_bounded lifecycle rows have confirmed and missing scope",
    )
    all_episodes = demo_episodes + research_episodes
    episode_display_gaps = sorted(
        f"{row['id']}:{field}:{language}"
        for row in all_episodes
        for field in EPISODE_DISPLAY_FIELDS
        for language in EPISODE_DISPLAY_LANGUAGES
        if not row.get(f"{field}_{language}")
    )
    episode_display_rewrites = sorted(
        f"{row['id']}:{field}"
        for row in all_episodes
        for field in EPISODE_DISPLAY_FIELDS
        if row.get(f"{field}_zh") != row.get(field)
    )
    check(
        "episode display overlay is complete and translation-only",
        not episode_display_gaps and not episode_display_rewrites,
        (
            f"episodes={len(all_episodes)} fields={len(EPISODE_DISPLAY_FIELDS)} "
            f"languages={len(EPISODE_DISPLAY_LANGUAGES)} "
            f"gaps={len(episode_display_gaps)} rewrites={len(episode_display_rewrites)}"
        ),
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
    actor_issue_rows = (
        demo_relations["actor_issue"] + research_relations["actor_issue"]
    )
    illegal_display_states = sorted(
        row["id"]
        for row in actor_issue_rows
        if row.get("display_state") not in ACTOR_ISSUE_DISPLAY_STATES
    )
    check(
        "actor-issue display_state values are legal",
        not illegal_display_states,
        "illegal="
        + (";".join(illegal_display_states) if illegal_display_states else "0"),
    )
    frozen_without_missing_scope = sorted(
        row["id"]
        for row in actor_issue_rows
        if row.get("display_state") == "frozen_bounded"
        and not row.get("missing_scope")
    )
    check(
        "frozen_bounded actor-issue rows carry missing_scope",
        not frozen_without_missing_scope,
        "missing="
        + (
            ";".join(frozen_without_missing_scope)
            if frozen_without_missing_scope
            else "0"
        ),
    )
    demo_fact_pending = sorted(
        row["id"]
        for row in demo_relations["actor_issue"]
        if row.get("display_state") not in ACTOR_ISSUE_ACCEPTED_DISPLAY_STATES
    )
    check(
        "no fact-pending rows enter the demo actor-issue layer",
        not demo_fact_pending,
        "pending=" + (";".join(demo_fact_pending) if demo_fact_pending else "0"),
    )
    display_state_counts: dict[str, int] = {}
    for row in actor_issue_rows:
        state = row.get("display_state", "")
        display_state_counts[state] = display_state_counts.get(state, 0) + 1
    check(
        "actor-issue display_state counts cover every edge",
        all(
            row.get("display_state") in ACTOR_ISSUE_ACCEPTED_DISPLAY_STATES
            for row in demo_relations["actor_issue"]
        )
        and all(
            row.get("display_state")
            in {"scope_reviewed_fact_pending", "fact_pending"}
            for row in research_relations["actor_issue"]
        ),
        " ".join(
            f"{state}={display_state_counts[state]}"
            for state in sorted(display_state_counts)
        ),
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

    typed_all = [
        row
        for layer in (typed_demo_relations, typed_research_relations)
        for rows in layer.values()
        for row in rows
    ]
    typed_dyadic = (
        typed_demo_relations["dyadic_relations"]
        + typed_research_relations["dyadic_relations"]
    )
    check(
        "typed relation review_status values are legal",
        all(
            row["review_status"] in LEGAL_RELATION_REVIEW_STATUSES
            and row["review_status"] not in LEGACY_RELATION_REVIEW_STATUSES
            for row in typed_all
        ),
        f"{len(typed_all)} typed rows",
    )
    check(
        "dyadic relation endpoints resolve to registry actors",
        all(
            row["source_endpoint"] in actor_ids
            and row["target_endpoint"] in actor_ids
            for row in typed_dyadic
        ),
        f"{len(typed_dyadic)} dyadic rows",
    )
    check(
        "no leads enter dyadic relations",
        not any(
            row["claim_status"] == "lead"
            or row["graph_eligibility"] == "research_lead"
            or row["observation_kind"] == "research_lead"
            for row in typed_dyadic
        ),
        f"{len(typed_dyadic)} dyadic rows",
    )
    bounded = [
        row for row in typed_all if row["claim_status"] == "supported_bounded"
    ]
    check(
        "supported_bounded rows carry scope boundaries",
        all(
            row["confirmed_scope"]
            and row["missing_scope"]
            and row["interpretation_limit"]
            for row in bounded
        ),
        f"{len(bounded)} supported_bounded rows",
    )
    leaked_hidden = [
        row["id"]
        for row in typed_all + case_roles
        if row["review_status"] == "rejected"
        or row["evidence_level"] == "E0"
        or row.get("graph_eligibility") == "excluded"
        or (
            row.get("claim_status") in {"unsupported", "lead"}
            and row.get("graph_eligibility") != "research_lead"
        )
        or "duplicate" in row["relation_type"]
    ]
    check(
        "rejected, duplicate, and E0 rows stay hidden",
        not leaked_hidden,
        "leaked=" + (";".join(leaked_hidden) if leaked_hidden else "0"),
    )
    missing_typed_fields = sorted(
        f"{row['id']}:{field}"
        for row in typed_all
        for field in TYPED_RELATION_FIELDS
        if field not in row
    ) + sorted(
        f"{row['id']}:{field}"
        for row in typed_all
        for field in TYPED_REQUIRED_NONEMPTY_FIELDS
        if not row.get(field)
    )
    check(
        "typed relation rows carry schema v1 section 9 fields",
        not missing_typed_fields,
        "missing=" + (";".join(missing_typed_fields) if missing_typed_fields else "0"),
    )
    check(
        "R10R029 stays out of dyadic relations",
        not any(row["id"] == "R10R029" for row in typed_dyadic)
        and any(
            row["id"] == "R10R029"
            for row in typed_demo_relations["aggregate_observations"]
        ),
        "aggregate observation only",
    )
    f025 = [row for row in typed_dyadic if row["id"] == "F025"]
    check(
        "F025 keeps an empty amount",
        len(f025) == 1
        and f025[0]["amount"] == ""
        and f025[0]["claim_status"] == "supported_bounded"
        and bool(f025[0]["missing_scope"]),
        "bounded KOSC to AWWA contribution without amount",
    )
    check(
        "demo typed collections are reviewed tier only",
        all(
            row["display_tier"] == "reviewed"
            and row["claim_status"] in {"supported", "supported_bounded"}
            for rows in typed_demo_relations.values()
            for row in rows
        ),
        "candidates and leads stay out of the reviewed layer",
    )
    check(
        "research typed collections contain candidates or explicitly gated leads",
        all(
            row["display_tier"] == "research"
            and (
                row["claim_status"] in {"candidate", "lead"}
                or row["graph_eligibility"] == "research_lead"
            )
            for key, rows in typed_research_relations.items()
            if key != "genealogy_anchors"
            for row in rows
        ),
        "reviewed relation facts may remain research-only when endpoint graphing is gated",
    )
    case_role_ids = {row["id"] for row in case_roles}
    check(
        "case roles preserved without edge derivation",
        [row["id"] for row in case_roles]
        == [row["id"] for row in demo_relations["legal_roles"]]
        and all(row["case_id"] and row["role"] for row in case_roles)
        and not any(row["observation_kind"] == "case_role" for row in typed_dyadic)
        and case_role_ids.isdisjoint(row["id"] for row in typed_dyadic),
        f"{len(case_roles)} case roles; non_party never derives edges",
    )

    source_ref_rows: list[dict[str, Any]] = (
        actors
        + demo_episodes
        + research_episodes
        + genealogy_anchors
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
    nonlegacy_demo_unresolved_refs = [
        ref
        for ref in demo_unresolved_refs
        if not (ref.startswith("X") and ref[1:].isdigit())
    ]
    check(
        "demo rows have no unclassified unresolved source references",
        not nonlegacy_demo_unresolved_refs,
        "unresolved="
        + (
            ";".join(nonlegacy_demo_unresolved_refs)
            if nonlegacy_demo_unresolved_refs
            else "0"
        ),
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
    presentation_regions = {row["id"] for row in presentation["regions"]}
    presentation_groups = {row["id"] for row in presentation["actor_class_groups"]}
    check(
        "presentation mappings cover current research objects",
        all(
            row["actor_class"] in presentation["actor_class_to_group"]
            for row in actors
            if row["display_status"] != "hidden"
        )
        and presentation["default_place_display_region"] in presentation_regions
        and all(
            region in presentation_regions
            for region in presentation["place_display_regions"].values()
        )
        and "unknown" in presentation_groups,
        (
            f"actor_classes={len(presentation['actor_class_to_group'])} "
            f"regions={len(presentation_regions)} "
            f"periods={len(presentation['time_periods'])}"
        ),
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
        f"{len(genealogy_anchors)} principal-reviewed lifecycle anchors are exported. "
        "They are bounded observations, not a complete post-1972 genealogy."
    )
    warnings.append(
        f"The packaged GeoJSON supports municipality/region rendering, but the {len(places)} place "
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
    if demo_unresolved_refs:
        warnings.append(
            f"{len(demo_unresolved_refs)} legacy X-code references remain explicit "
            "on human-reviewed demo rows and are not promoted to central source IDs: "
            f"{';'.join(demo_unresolved_refs)}."
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
    typed_unresolved_refs = sorted(
        {
            ref
            for row in typed_all
            for ref in row.get("unresolved_source_refs", [])
        }
    )
    if typed_unresolved_refs:
        warnings.append(
            f"{len(typed_unresolved_refs)} legacy typed-relation source "
            "references are not central source IDs and stay explicit on the "
            f"rows: {';'.join(typed_unresolved_refs)}."
        )
    if typed_excluded_ids:
        warnings.append(
            f"{len(typed_excluded_ids)} rejected or duplicate funding rows are "
            "excluded from every typed relation collection: "
            + ";".join(typed_excluded_ids)
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


def exploration_input_paths(project_root: Path) -> dict[str, Path]:
    """Central input files for the build, resolved against ``project_root``."""
    return {
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
        "funding_relations": project_root
        / "data/interim/15_funding_or_support_edges_sample_v0.csv",
        "typed_relation_handoff": project_root
        / "outputs/hr033_integration_v1/typed_relation_observations_v1.csv",
        "venues": project_root / "data/metadata/venue_taxonomy_v0.csv",
        "episodes": project_root
        / "outputs/translation_episode_comparison_v1/translation_episode_candidates_v1.csv",
        "episode_display_translations": project_root
        / "data/metadata/episode_display_trilingual_v1.csv",
        "strict_triples": project_root
        / "outputs/R03_strict_place_issue_v1/same_source_actor_place_issue_triples_v1.csv",
        "source_crosswalk": project_root
        / "outputs/phase1_source_integration_v1/module_source_crosswalk_v1.csv",
        "coverage_cells": project_root
        / "data/interim/27_coverage_audit_cells_v1.csv",
        "coverage_implications": project_root
        / "outputs/coverage_audit_v1/coverage_bias_implications_v1.csv",
        "coverage_implication_display": project_root
        / "data/metadata/coverage_implication_display_trilingual_v1.json",
        "archive_manifest": project_root
        / "source_docs/source_archive/source_archive_manifest.csv",
        "legal_cases": project_root
        / "data/interim/17_legal_policy_procedure_cases_v0.csv",
        "map_geometry": project_root
        / "outputs/learning_v1/okinawa_municipal_boundaries_simplified_v1.geojson",
        "actor_lifecycle": project_root
        / "outputs/actor_lifecycle_v1/actor_lifecycle_v0.csv",
        "presentation_rules": project_root
        / "data/metadata/frontend_presentation_rules_v1.json",
    }


def build_exploration_system_data(project_root: Path, output_dir: Path) -> dict[str, Any]:
    project_root = project_root.resolve()
    output_dir = output_dir.resolve()
    inputs = exploration_input_paths(project_root)
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
    presentation = normalize_presentation_rules(
        read_json(inputs["presentation_rules"]), actors, places
    )
    genealogy_anchors = normalize_genealogy_anchors(
        read_csv(inputs["actor_lifecycle"]),
        {row["id"] for row in actors},
        source_aliases,
    )
    sources = normalize_sources(
        source_rows, read_csv(inputs["archive_manifest"])
    )
    evidence_notes = normalize_evidence_notes(read_csv(inputs["evidence_notes"]))
    episode_rows = read_csv(inputs["episodes"])
    episode_display_overrides = validate_episode_display_overrides(
        episode_rows,
        read_csv(inputs["episode_display_translations"]),
    )
    demo_episodes, research_episodes = normalize_episodes(
        episode_rows,
        source_aliases,
        episode_display_overrides,
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
    typed_demo, typed_research, typed_excluded_ids, typed_input_count = (
        build_typed_relation_collections(
            read_csv(inputs["funding_relations"]),
            read_csv(inputs["typed_relation_handoff"]),
            {row["id"] for row in actors},
            {row["id"] for row in places},
            source_aliases,
        )
    )
    # Typed case-role copy: identical rows to relations.json legal_roles.
    case_roles = [dict(row) for row in legal_roles]
    demo_actor_episode = build_actor_episode_relations(demo_episodes)
    research_actor_episode = build_actor_episode_relations(research_episodes)
    coverage_cells = normalize_coverage_cells(read_csv(inputs["coverage_cells"]))
    coverage_implication_rows = read_csv(inputs["coverage_implications"])
    coverage_implication_display = (
        validate_coverage_implication_display_overrides(
            coverage_implication_rows,
            read_json(inputs["coverage_implication_display"]),
        )
    )
    coverage_implications = normalize_coverage_implications(
        coverage_implication_rows,
        coverage_implication_display,
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
        "dyadic_relations": typed_research["dyadic_relations"],
        "administrative_records": typed_research["administrative_records"],
        "aggregate_observations": typed_research["aggregate_observations"],
        "relation_leads": typed_research["relation_leads"],
        "event_participation": typed_research["event_participation"],
        "genealogy_anchors": typed_research["genealogy_anchors"],
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
    write_json(output_dir / "demo/historical_anchors.json", genealogy_anchors)
    write_json(output_dir / "demo/relations.json", demo_relations)
    write_json(output_dir / "demo/dyadic_relations.json", typed_demo["dyadic_relations"])
    write_json(
        output_dir / "demo/administrative_records.json",
        typed_demo["administrative_records"],
    )
    write_json(
        output_dir / "demo/aggregate_observations.json",
        typed_demo["aggregate_observations"],
    )
    write_json(
        output_dir / "demo/typed_event_participation.json",
        typed_demo["event_participation"],
    )
    write_json(output_dir / "demo/relation_leads.json", typed_demo["relation_leads"])
    write_json(output_dir / "demo/case_roles.json", case_roles)
    write_json(output_dir / "demo/genealogy_anchors.json", genealogy_anchors)
    write_json(output_dir / "demo/map_geometry.geojson", map_geometry)
    write_json(output_dir / "views/presentation.json", presentation)
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
        genealogy_anchors,
        presentation,
    )
    for name, view in views.items():
        write_json(output_dir / f"views/{name}.json", view)

    typed_claim_counts: dict[str, int] = {}
    for layer in (typed_demo, typed_research):
        for collection, rows in layer.items():
            if collection == "genealogy_anchors":
                continue
            for row in rows:
                typed_claim_counts[row["claim_status"]] = (
                    typed_claim_counts.get(row["claim_status"], 0) + 1
                )
    visible_actor_count = sum(
        row["display_status"] != "hidden" for row in actors
    )
    actor_issue_display_counts: dict[str, int] = {}
    for row in demo_actor_issue + research_actor_issue:
        state = row["display_state"]
        actor_issue_display_counts[state] = (
            actor_issue_display_counts.get(state, 0) + 1
        )
    research_fact_gate_counts: dict[str, int] = {}
    for row in research_actor_issue:
        gate = row["fact_gate_status"]
        research_fact_gate_counts[gate] = research_fact_gate_counts.get(gate, 0) + 1
    counts = {
        "actor_registry": {
            "provenance_rows": len(actors),
            "current_visible": visible_actor_count,
            "hidden_provenance_rows": len(actors) - visible_actor_count,
        },
        "demo": {
            "actors": visible_actor_count,
            "actor_aliases": sum(len(row["aliases"]) for row in actors),
            "places": len(places),
            "issues": len(issues),
            "episodes": len(demo_episodes),
            "venues": len(venues),
            "outcomes": len(demo_outcomes),
            "sources": len(sources),
            "evidence_notes": len(evidence_notes),
            "historical_anchors": len(genealogy_anchors),
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
        "episode_display": {
            "episodes": len(demo_episodes) + len(research_episodes),
            "fields_per_episode": len(EPISODE_DISPLAY_FIELDS),
            "approved_translation_cells": (
                (len(demo_episodes) + len(research_episodes))
                * len(EPISODE_DISPLAY_FIELDS)
                * len(EPISODE_DISPLAY_LANGUAGES)
            ),
            "source_text_fallbacks": sum(
                len(row["display_translation_fallbacks"])
                for row in demo_episodes + research_episodes
            ),
        },
        "coverage_implication_display": {
            "dimensions": len(coverage_implications),
            "fields_per_dimension": len(COVERAGE_IMPLICATION_FIELDS),
            "approved_translation_cells": (
                len(coverage_implications)
                * len(COVERAGE_IMPLICATION_FIELDS)
                * len(EPISODE_DISPLAY_LANGUAGES)
            ),
            "source_text_fallbacks": 0,
        },
        "actor_issue_states": {
            "valid_edges": len(demo_actor_issue) + len(research_actor_issue),
            "display_state_counts": dict(sorted(actor_issue_display_counts.items())),
            "research_fact_gate_counts": dict(
                sorted(research_fact_gate_counts.items())
            ),
        },
        "typed_relations": {
            "input_observations": typed_input_count,
            "claim_status_counts": dict(sorted(typed_claim_counts.items())),
            "demo": {
                **{
                    key: len(value)
                    for key, value in sorted(typed_demo.items())
                },
                "case_roles": len(case_roles),
                "genealogy_anchors": len(genealogy_anchors),
            },
            "research": {
                key: len(value) for key, value in sorted(typed_research.items())
            },
            "excluded": len(typed_excluded_ids),
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
        typed_demo_relations=typed_demo,
        typed_research_relations=typed_research,
        case_roles=case_roles,
        typed_excluded_ids=typed_excluded_ids,
        coverage_cells=coverage_cells,
        case_ids={row["case_id"] for row in read_csv(inputs["legal_cases"])},
        map_geometry=map_geometry,
        genealogy_anchors=genealogy_anchors,
        presentation=presentation,
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
            "demo/dyadic_relations.json",
            "demo/administrative_records.json",
            "demo/aggregate_observations.json",
            "demo/typed_event_participation.json",
            "demo/relation_leads.json",
            "demo/case_roles.json",
            "demo/genealogy_anchors.json",
            "demo/map_geometry.geojson",
            "research/candidates.json",
            "views/overview.json",
            "views/actors.json",
            "views/pathways.json",
            "views/evidence_coverage.json",
            "views/time.json",
            "views/global.json",
            "views/presentation.json",
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
        "schema_version": "1.2.0",
        "as_of_date": ARTIFACT_AS_OF_DATE,
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
