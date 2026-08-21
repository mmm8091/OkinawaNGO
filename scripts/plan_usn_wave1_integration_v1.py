#!/usr/bin/env python3
"""Build a read-only USN wave-1 integration plan and verify it in a sandbox.

This module intentionally has no production apply interface.  The current source
admission plan is not frozen, central writeback is not authorized, and the
sandbox path only materializes an immutable *projection* outside the repository.
"""

from __future__ import annotations

import copy
import csv
import argparse
import hashlib
import json
import os
import re
import shutil
import tempfile
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


ROOT = Path(__file__).resolve().parents[1]
PLAN_ID = "USN-W1-PLAN-2026-08-21"
PARENT_DESIGN_COMMIT = "6e7bd51"
DESIGN_DIR = Path("outputs/us_presence_controlled_integration_design_v1")
AUTHORITATIVE_MANIFEST = Path(
    "outputs/us_presence_network_wave1_v1/post_principal_manifest_v1.json"
)
DESIGN_MANIFEST = DESIGN_DIR / "manifest.json"

CENTRAL_PATHS = (
    "data/interim/01_actor_registry_initial_v0.csv",
    "data/interim/02_actor_aliases_initial_v0.csv",
    "data/interim/05_source_log_initial_v0.csv",
    "data/interim/15_funding_or_support_edges_sample_v0.csv",
)

DECISION_MAPS = {
    "service": (
        "outputs/us_presence_service_recon_v1/human_review_queue_v1.csv",
        "hr_id",
        "principal_decision",
        13,
        "94676e4f19d06d697d0c42e8d9316b17757f67bc18a38b34f8a7b76612ccbc2d",
    ),
    "accountability": (
        "outputs/us_presence_accountability_recon_v1/human_review_queue_v1.csv",
        "review_item_id",
        "principal_decision",
        9,
        "74a5c861cff5086463670a15e3e23848e65a6545c38e8769b7e7250b2b46522b",
    ),
    "directory": (
        "outputs/actor_directory_v1/HR_USN_actor_directory_decisions_v1.csv",
        "review_item_id",
        "decision",
        65,
        "3456b50fbb659a94810ab0f57d1f608206b1b04aee8e16661a4769039f85191b",
    ),
    "relation_rules": (
        "outputs/us_presence_relation_retype_v1/HR_USN_relation_retype_rules_v1.csv",
        "mapping_rule_id",
        "decision",
        6,
        "3d5f643c3d7ca1b51c1f077da2dcad70fa58bcad2b568816ca2c40a837e22629",
    ),
}

ARCHITECTURE_DECISION_HASH = (
    "77deaa00e36d71768fa653b34373094ae0fadb7452e9a4b1fc5123e73c9f28df"
)
RESERVED_ACTORS = ("X018", "X019", "X020", "X021", "X022", "X023")
RELATION_PATH = Path(
    "outputs/us_presence_relation_retype_v1/relation_retype_crosswalk_v1.csv"
)
RELATION_RULE_PATH = Path(
    "outputs/us_presence_relation_retype_v1/HR_USN_relation_retype_rules_v1.csv"
)
DIRECTORY_DECISION_PATH = Path(
    "outputs/actor_directory_v1/HR_USN_actor_directory_decisions_v1.csv"
)
FRAME_PATH = Path("outputs/us_presence_network_wave1_v1/us_origin_actor_scope_v1.csv")
FRAME_SUMMARY_PATH = Path(
    "outputs/us_presence_network_wave1_v1/us_origin_actor_scope_summary_v1.csv"
)

ACTOR_ADMISSION_PREVIEW = (
    {
        "actor_id": "X018",
        "canonical_name": "Marine Thrift Shop Okinawa",
        "actor_class": "base_community_service_actor",
        "origin_type": "us_origin",
        "legal_or_scope_status": "us_501c3_nonprofit",
        "decision_ref": "SR-HR-001",
    },
    {
        "actor_id": "X019",
        "canonical_name": "Marine Gift Shop",
        "actor_class": "base_community_service_actor",
        "origin_type": "us_origin",
        "legal_or_scope_status": "legal_status_unresolved",
        "decision_ref": "SR-HR-002",
    },
    {
        "actor_id": "X020",
        "canonical_name": "Neighborhood Pantry – Camp Butler",
        "actor_class": "base_community_service_actor",
        "origin_type": "us_origin",
        "legal_or_scope_status": "legal_status_unknown",
        "decision_ref": "SR-HR-003",
    },
    {
        "actor_id": "X021",
        "canonical_name": "North Island Okinawa Spouses Club",
        "actor_class": "base_spouse_club",
        "origin_type": "us_origin",
        "legal_or_scope_status": "status_not_encoded",
        "decision_ref": "SR-HR-004",
    },
    {
        "actor_id": "X022",
        "canonical_name": "Army Emergency Relief",
        "actor_class": "military_family_relief_actor",
        "origin_type": "us_origin",
        "legal_or_scope_status": "national_actor_local_presence_at_torii",
        "decision_ref": "SR-HR-005A",
    },
    {
        "actor_id": "X023",
        "canonical_name": "Air & Space Forces Aid Society",
        "actor_class": "military_family_relief_actor",
        "origin_type": "us_origin",
        "legal_or_scope_status": "national_actor_local_presence_at_kadena",
        "decision_ref": "SR-HR-005B",
    },
)

ACTOR_DEFER_PREVIEW = (
    {
        "upstream_id": "SA016",
        "canonical_name": "Helping Japan International",
        "decision_ref": "SR-HR-006A",
        "human_decision": "defer_second_source",
        "disposition": "hold",
        "hold_code": "DEFER_SECOND_SOURCE",
        "non_inference": "Do not infer an Okinawa service role from legal identity or name similarity.",
    },
    {
        "upstream_id": "SA017",
        "canonical_name": "OAO Civilian Welfare Council",
        "decision_ref": "SR-HR-006B",
        "human_decision": "defer_second_source",
        "disposition": "hold",
        "hold_code": "DEFER_SECOND_SOURCE",
        "non_inference": "A roster name alone does not establish identity, function or relation.",
    },
)

DERIVED_SOURCE_REQUIREMENTS = (
    {
        "requirement_id": "USNDSR-001",
        "supports": "RF002 OESC to AWWA USD 8479",
        "required_record": "official IRS bulk XML or official filing receipt",
        "source_plan_status": "missing_from_57_cluster_union",
        "disposition": "hold",
    },
    {
        "requirement_id": "USNDSR-002",
        "supports": "USAR001-JF Treasury USD 280000 payment mechanism",
        "required_record": "Treasury Judgment Fund XLSX/API receipt",
        "source_plan_status": "missing_from_57_cluster_union",
        "disposition": "hold",
    },
    {
        "requirement_id": "USNDSR-003",
        "supports": "A033 2019 Henoko petition role",
        "required_record": "FoE 2019 event source receipt",
        "source_plan_status": "missing_from_57_cluster_union",
        "disposition": "hold",
    },
    {
        "requirement_id": "USNDSR-004",
        "supports": "A070 2018 observation",
        "required_record": "dated official or organization source receipt",
        "source_plan_status": "design_action_gap",
        "disposition": "hold",
    },
    {
        "requirement_id": "USNDSR-005",
        "supports": "A070 2025 observation",
        "required_record": "dated official or organization source receipt",
        "source_plan_status": "design_action_gap",
        "disposition": "hold",
    },
    {
        "requirement_id": "USNDSR-006",
        "supports": "A070 2026 observation",
        "required_record": "dated official or organization source receipt",
        "source_plan_status": "design_action_gap",
        "disposition": "hold",
    },
    {
        "requirement_id": "USNDSR-007",
        "supports": "X014 NED bounded negative search",
        "required_record": "dated official listing/search-scope receipts",
        "source_plan_status": "missing_from_57_cluster_union",
        "disposition": "hold",
    },
    {
        "requirement_id": "USNDSR-008",
        "supports": "event-only and research endpoint identity crosswalks",
        "required_record": "endpoint-specific identity receipts",
        "source_plan_status": "missing_from_57_cluster_union",
        "disposition": "hold",
    },
)

SELECTION_FRAME_HOLDS = (
    {
        "candidate_frame": "USF-ACTIVE121-DIRECTORY-CANDIDATE",
        "intended_scope": "121 active-actor official-site directory",
        "status": "hold_selection_frame",
        "reason": "membership and denominator have not received a separate frame approval",
    },
    {
        "candidate_frame": "USF-USN-PERSON-TRACER-CANDIDATE",
        "intended_scope": "reviewed person-role tracer including A001 and A002",
        "status": "hold_selection_frame",
        "reason": "A001 and A002 are outside the frozen US-origin17 comparison frame",
    },
    {
        "candidate_frame": "USF-USN-RESOURCE-PATH-CANDIDATE",
        "intended_scope": "MTS/AWWA and Earthjustice resource paths",
        "status": "hold_selection_frame",
        "reason": "new actors and resource observations cannot be backfilled into the frozen 9/6/2 frame",
    },
)


class PlanValidationError(RuntimeError):
    """Raised when a frozen receipt or an integration invariant has drifted."""


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise PlanValidationError(message)


def _canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def _with_plan_hash(plan: dict[str, Any]) -> dict[str, Any]:
    payload = copy.deepcopy(plan)
    payload.pop("plan_hash", None)
    payload["plan_hash"] = hashlib.sha256(
        _canonical_json(payload).encode("utf-8")
    ).hexdigest()
    return payload


def _validate_plan_hash(plan: dict[str, Any]) -> None:
    expected = plan.get("plan_hash", "")
    actual = _with_plan_hash(plan)["plan_hash"]
    _require(bool(expected) and expected == actual, "plan hash mismatch")


def _validate_authoritative_receipt(root: Path) -> dict[str, Any]:
    manifest_path = root / AUTHORITATIVE_MANIFEST
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    files = manifest.get("files", [])
    _require(len(files) == 23, f"authoritative manifest expected 23 files, found {len(files)}")
    for item in files:
        path = root / item["path"]
        _require(path.is_file(), f"missing authoritative file: {item['path']}")
        _require(
            _sha256(path) == item["sha256"],
            f"authoritative hash drift: {item['path']}",
        )
        _require(
            path.stat().st_size == item["bytes"],
            f"authoritative byte drift: {item['path']}",
        )
    _require(
        manifest.get("central_writeback_performed") is False,
        "upstream receipt unexpectedly reports central writeback",
    )
    _require(
        manifest.get("relation_crosswalk_expanded") is False,
        "upstream receipt unexpectedly reports relation expansion",
    )
    return manifest


def _validate_design_receipt(root: Path) -> dict[str, Any]:
    """Validate immutable design artifacts, leaving mutable control docs commit-bound."""

    path = root / DESIGN_MANIFEST
    manifest = json.loads(path.read_text(encoding="utf-8"))
    _require(
        manifest.get("status") == "design_only_no_central_writeback",
        "unexpected parent design status",
    )
    mutable_control_paths = {"AGENTS.md", "CONTEXT.md", "docs/phase1_workbench.md"}
    for item in manifest.get("files", []):
        relative = item["path"]
        if relative in mutable_control_paths:
            continue
        target = root / relative
        _require(target.is_file(), f"missing design artifact: {relative}")
        _require(_sha256(target) == item["sha256"], f"design artifact drift: {relative}")
        _require(target.stat().st_size == item["bytes"], f"design byte drift: {relative}")
    return manifest


def _validate_decision_maps(root: Path) -> dict[str, int]:
    counts: dict[str, int] = {}
    for label, (relative, id_col, decision_col, expected_count, expected_hash) in DECISION_MAPS.items():
        _, rows = _read_csv(root / relative)
        _require(len(rows) == expected_count, f"{label} decision count drift")
        pairs = sorted(f"{row[id_col]}={row[decision_col]}" for row in rows)
        _require(len(pairs) == len(set(pairs)), f"{label} duplicate decision IDs")
        digest = hashlib.sha256("\n".join(pairs).encode("utf-8")).hexdigest()
        _require(digest == expected_hash, f"{label} exact decision mapping drift")
        counts[label] = len(rows)

    arch = json.loads(
        (
            root
            / "outputs/us_presence_network_architecture_v1/"
            "principal_checkpoint_return_v1.json"
        ).read_text(encoding="utf-8")
    )
    pairs = sorted(
        f"{item['item_id']}={item['decision']}" for item in arch["decisions"]
    )
    digest = hashlib.sha256("\n".join(pairs).encode("utf-8")).hexdigest()
    _require(len(pairs) == 5, "architecture decision count drift")
    _require(digest == ARCHITECTURE_DECISION_HASH, "architecture decision mapping drift")
    for field in (
        "central_writeback_authorized",
        "publication_adapter_authorized",
        "frontend_writeback_authorized",
    ):
        _require(arch.get(field) is False, f"unexpected authorization: {field}")
    counts["architecture"] = len(pairs)
    return counts


def _validate_central_baseline(
    root: Path, expected_hashes: dict[str, str]
) -> dict[str, str]:
    actual: dict[str, str] = {}
    for relative in CENTRAL_PATHS:
        path = root / relative
        digest = _sha256(path)
        actual[relative] = digest
        _require(
            digest == expected_hashes[relative],
            f"central baseline hash drift: {relative}; expected "
            f"{expected_hashes[relative]}, got {digest}",
        )
    _, actors = _read_csv(root / CENTRAL_PATHS[0])
    actor_ids = {row["actor_id"] for row in actors}
    collisions = sorted(set(RESERVED_ACTORS) & actor_ids)
    _require(not collisions, f"reserved actor ID collision: {','.join(collisions)}")
    return actual


def _validate_frozen_frame(root: Path) -> dict[str, Any]:
    _, rows = _read_csv(root / FRAME_PATH)
    _, summary_rows = _read_csv(root / FRAME_SUMMARY_PATH)
    _require(len(rows) == 17, "frozen US-origin frame row count drift")
    _require(
        {row["selection_frame_id"] for row in rows}
        == {"USF-US-ORIGIN17-2026-08-19"},
        "frozen frame ID drift",
    )
    counts = {row["analytical_group"]: int(row["actor_count"]) for row in summary_rows}
    _require(counts.get("service_charity_comparison") == 9, "service denominator drift")
    _require(counts.get("accountability_comparison") == 6, "accountability denominator drift")
    _require(
        counts.get("public_diplomacy_program_node", 0)
        + counts.get("funder_watchlist_node", 0)
        == 2,
        "standalone denominator drift",
    )
    return {
        "selection_frame_id": "USF-US-ORIGIN17-2026-08-19",
        "rows": 17,
        "service": 9,
        "accountability": 6,
        "standalone": 2,
        "sha256": _sha256(root / FRAME_PATH),
    }


def _build_relation_overlay(root: Path) -> list[dict[str, str]]:
    fields, rows = _read_csv(root / RELATION_PATH)
    _, rule_rows = _read_csv(root / RELATION_RULE_PATH)
    decisions = {row["mapping_rule_id"]: row["decision"] for row in rule_rows}
    _require(len(rows) == 43, "relation overlay no longer has 43 rows")
    ids = [row["edge_id"] for row in rows]
    _require(len(ids) == len(set(ids)), "relation overlay edge IDs are not unique")
    _require(all(not row["mapping_decision"] for row in rows), "legacy relation overlay was already expanded")

    projected: list[dict[str, str]] = []
    for row in rows:
        mapped = dict(row)
        _require(row["mapping_rule_id"] in decisions, f"unknown mapping rule: {row['mapping_rule_id']}")
        if row["edge_id"] in {"F017", "F043"}:
            mapped["approved_record_family"] = "regional_branch"
            mapped["mapping_decision"] = "revise"
            mapped["mapping_review_status"] = "human_revised"
        else:
            mapped["approved_record_family"] = row["proposed_record_family"]
            mapped["mapping_decision"] = "accept"
            mapped["mapping_review_status"] = "human_checked"
        projected.append(mapped)

    changed = {
        row["edge_id"]
        for row in projected
        if row["approved_record_family"] != row["proposed_record_family"]
    }
    _require(changed == {"F017", "F043"}, "unapproved relation-family projection drift")
    _require(fields == list(rows[0]), "relation crosswalk header/order drift")
    return projected


def _build_directory_overlay(root: Path) -> list[dict[str, str]]:
    _, rows = _read_csv(root / DIRECTORY_DECISION_PATH)
    _require(len(rows) == 65, "directory decision count drift")
    counts: dict[str, int] = {}
    for row in rows:
        counts[row["decision"]] = counts.get(row["decision"], 0) + 1
    _require(
        counts == {"accept": 54, "revise": 4, "defer": 5, "reject": 2},
        f"directory decision distribution drift: {counts}",
    )
    projected: list[dict[str, str]] = []
    for row in rows:
        item = dict(row)
        unresolved = row["decision"] == "revise" or not row["source_id"]
        item["source_resolution"] = (
            "new_or_revised_source_required" if unresolved else "existing_source_resolved"
        )
        item["future_directory_eligibility"] = (
            "eligible_after_controlled_integration"
            if row["decision"] in {"accept", "revise"}
            else "not_eligible"
        )
        item["central_writeback"] = "no"
        projected.append(item)
    resolution_counts: dict[str, int] = {}
    for row in projected:
        resolution_counts[row["source_resolution"]] = (
            resolution_counts.get(row["source_resolution"], 0) + 1
        )
    _require(
        resolution_counts
        == {
            "existing_source_resolved": 51,
            "new_or_revised_source_required": 14,
        },
        f"directory source-resolution drift: {resolution_counts}",
    )
    return projected


def _normalize_url(value: str) -> str:
    parts = urlsplit(value.strip())
    _require(parts.scheme.lower() in {"http", "https"} and bool(parts.hostname), f"invalid source URL: {value}")
    scheme = parts.scheme.lower()
    host = (parts.hostname or "").lower()
    port = parts.port
    netloc = host
    if port and not ((scheme == "http" and port == 80) or (scheme == "https" and port == 443)):
        netloc = f"{host}:{port}"
    path = parts.path or "/"
    if path != "/" and path.endswith("/"):
        path = path[:-1]
    query = urlencode(
        sorted(
            (key, item)
            for key, item in parse_qsl(parts.query, keep_blank_values=True)
            if not key.lower().startswith("utm_")
        )
    )
    return urlunsplit((scheme, netloc, path, query, ""))


def _build_source_clusters(root: Path) -> list[dict[str, str]]:
    references: list[dict[str, str]] = []
    _, service = _read_csv(
        root / "outputs/us_presence_service_recon_v1/source_proposals_v1.csv"
    )
    for row in service:
        references.append(
            {
                "origin": "service_proposal",
                "proposal_id": row["proposal_id"],
                "title": row["source_title"],
                "url": row["url"],
            }
        )
    _, accountability = _read_csv(
        root
        / "outputs/us_presence_accountability_recon_v1/official_source_proposals_v1.csv"
    )
    for row in accountability:
        references.append(
            {
                "origin": "accountability_proposal",
                "proposal_id": row["proposal_id"],
                "title": row["source_owner"],
                "url": row["url"],
            }
        )
    _, directory = _read_csv(root / DIRECTORY_DECISION_PATH)
    for row in directory:
        if row["decision"] == "revise" or (
            row["decision"] == "accept" and not row["source_id"]
        ):
            url = row["revised_url"] if row["decision"] == "revise" else row["candidate_url"]
            references.append(
                {
                    "origin": "directory_new_source_needed",
                    "proposal_id": row["review_item_id"],
                    "title": row["canonical_name_original"],
                    "url": url,
                }
            )
    _require(len(references) == 58, f"source union expected 58 references, found {len(references)}")

    clusters: dict[str, list[dict[str, str]]] = {}
    for row in references:
        normalized = _normalize_url(row["url"])
        clusters.setdefault(normalized, []).append(row)
    _require(len(clusters) == 57, f"source union expected 57 normalized URLs, found {len(clusters)}")

    _, central_sources = _read_csv(root / CENTRAL_PATHS[2])
    central_by_url: dict[str, str] = {}
    for row in central_sources:
        parts = urlsplit(row["url"].strip())
        if parts.scheme.lower() not in {"http", "https"} or not parts.hostname:
            continue
        central_by_url[_normalize_url(row["url"])] = row["source_id"]
    result: list[dict[str, str]] = []
    for normalized_url in sorted(clusters):
        members = clusters[normalized_url]
        existing = central_by_url.get(normalized_url, "")
        if existing:
            resolution = "reuse_existing"
            disposition = "reference_existing"
        elif "propublica.org" in (urlsplit(normalized_url).hostname or ""):
            resolution = "hold_official_irs_receipt"
            disposition = "hold"
        else:
            resolution = "candidate_new_non_propublica"
            disposition = "project"
        cluster_key = "USNSC-" + hashlib.sha256(normalized_url.encode("utf-8")).hexdigest()[:12].upper()
        result.append(
            {
                "source_cluster_key": cluster_key,
                "normalized_url": normalized_url,
                "proposal_refs": ";".join(sorted(row["proposal_id"] for row in members)),
                "proposal_origins": ";".join(sorted({row["origin"] for row in members})),
                "titles": ";".join(sorted({row["title"] for row in members})),
                "reference_count": str(len(members)),
                "existing_source_id": existing,
                "source_resolution": resolution,
                "disposition": disposition,
                "final_source_id": "",
                "review_status_for_future_new_row": "ai_seeded" if not existing else "",
                "relation_or_claim_approved_for_future_new_row": "no" if not existing else "",
            }
        )
    counts: dict[str, int] = {}
    for row in result:
        counts[row["source_resolution"]] = counts.get(row["source_resolution"], 0) + 1
    _require(
        counts
        == {
            "reuse_existing": 4,
            "candidate_new_non_propublica": 44,
            "hold_official_irs_receipt": 9,
        },
        f"source-cluster resolution drift: {counts}",
    )
    _require(
        {
            row["proposal_refs"]: row["existing_source_id"]
            for row in result
            if row["existing_source_id"]
        }
        == {"SP013": "S076", "SP015": "S054", "SP017": "S080", "SP034": "S055"},
        "exact source-reuse mapping drift",
    )
    return result


def _enrich_action_dispositions(actions: list[dict[str, str]]) -> list[dict[str, str]]:
    reference = {"USI-001", "USI-002", "USI-003", "USI-004", "USI-013", "USI-029", "USI-030"}
    project = {"USI-014", "USI-015", "USI-016", "USI-031", "USI-032", "USI-034", "USI-036"}
    exclude = {"USI-037"}
    hold_codes = {
        **{f"USI-{number:03d}": "SOURCE_PLAN_NOT_FROZEN" for number in range(5, 11)},
        "USI-011": "DEFER_SECOND_SOURCE",
        "USI-012": "SOURCE_PLAN_NOT_FROZEN",
        "USI-017": "SOURCE_PLAN_NOT_FROZEN",
        "USI-018": "DEFER_UNDERLYING_FILING_OR_CROSSWALK",
        "USI-019": "ACTOR_SOURCE_AND_SELECTION_FRAME_PENDING",
        "USI-020": "ACTOR_SOURCE_AND_SELECTION_FRAME_PENDING",
        "USI-021": "SOURCE_AND_SELECTION_FRAME_PENDING",
        "USI-022": "FORMAL_SOURCE_RECEIPT_AND_SELECTION_FRAME_PENDING",
        "USI-023": "SELECTION_FRAME_PENDING",
        "USI-024": "SELECTION_FRAME_PENDING",
        "USI-025": "EVENT_ONLY_ENDPOINT_AND_SELECTION_FRAME_PENDING",
        "USI-026": "RESEARCH_ENDPOINT_AND_SELECTION_FRAME_PENDING",
        "USI-027": "ENDPOINT_CROSSWALK_AND_SELECTION_FRAME_PENDING",
        "USI-028": "SOURCE_PLAN_NOT_FROZEN",
        "USI-033": "SPONSOR_SNAPSHOT_SCHEMA_SEAM_MISSING",
        "USI-035": "SOURCE_PLAN_NOT_FROZEN",
    }
    enriched: list[dict[str, str]] = []
    for row in actions:
        item = dict(row)
        action_id = row["action_id"]
        if action_id in reference:
            disposition, hold_code = "reference_existing", ""
        elif action_id in project:
            disposition, hold_code = "project", ""
        elif action_id in exclude:
            disposition, hold_code = "exclude", "PUBLICATION_NOT_AUTHORIZED"
        else:
            disposition, hold_code = "hold", hold_codes[action_id]
        item["disposition"] = disposition
        item["hold_code"] = hold_code
        item["write_eligible"] = "no"
        enriched.append(item)
    _require(len(enriched) == 37, "action disposition coverage drift")
    _require(all(row["write_eligible"] == "no" for row in enriched), "plan exposed a write-eligible action")
    return enriched


def _build_typed_fact_projection(root: Path) -> dict[str, list[dict[str, str]]]:
    _, resource_flows = _read_csv(
        root / "outputs/us_presence_service_recon_v1/resource_flow_candidates_v1.csv"
    )
    money: list[dict[str, str]] = []
    for row in resource_flows:
        item = {
            "upstream_id": row["flow_id"],
            "source_endpoint": row["source_actor_id_or_candidate"],
            "target_endpoint": row["target_actor_id_or_candidate"],
            "amount": row["amount"],
            "currency": row["currency"],
            "amount_semantics": row["amount_semantics"],
            "period_start": "",
            "period_end": "",
            "filing_date": "",
            "human_decision": "not_reviewed_in_this_return",
            "source_resolution": "hold_fact_review",
            "disposition": "hold",
            "non_inference": row["interpretation_limit"],
        }
        if row["flow_id"] == "RF001":
            item.update(
                {
                    "human_decision": "defer_underlying_filing_or_crosswalk",
                    "source_resolution": "deferred",
                    "disposition": "hold_no_flow",
                }
            )
        elif row["flow_id"] == "RF002":
            item.update(
                {
                    "period_start": "2024-07-01",
                    "period_end": "2025-06-30",
                    "filing_date": "2025-10-27",
                    "human_decision": "accept_new_dated_flow",
                    "source_resolution": "hold_source_freeze",
                    "disposition": "hold",
                }
            )
            _require(
                (
                    item["source_endpoint"],
                    item["target_endpoint"],
                    item["amount"],
                    item["currency"],
                    item["amount_semantics"],
                )
                == ("X007", "X004", "8479", "USD", "exact_reported"),
                "RF002 approved money semantics drift",
            )
        money.append(item)
    _require(len(money) == 14, "resource-flow projection count drift")
    _require(
        sum(row["human_decision"] == "accept_new_dated_flow" for row in money) == 1,
        "RF002 must be the only accepted new dated flow",
    )

    _, accounting_source = _read_csv(
        root / "outputs/us_presence_accountability_recon_v1/resource_observations_v1.csv"
    )
    _require(len(accounting_source) == 2, "accountability resource source count drift")
    source_usar = next(
        row for row in accounting_source if row["resource_observation_id"] == "USAR001"
    )
    accounting = [
        {
            "record_id": "USAR001",
            "receiver_endpoint": "A009",
            "amount": "276345.50",
            "currency": "USD",
            "period_or_date": "2020-07-01/2021-06-30",
            "semantics": "court_award_amount_reported_on_accrual_filing",
            "directed_money_edge": "no",
            "source_resolution": "hold_selection_frame",
            "disposition": "hold",
            "non_inference": source_usar["interpretation_limit"],
        },
        {
            "record_id": "USAR001-JF",
            "receiver_endpoint": "payment_mechanism_record_not_simple_receiver_edge",
            "amount": "280000",
            "currency": "USD",
            "period_or_date": "2021-03-05",
            "semantics": "Judgment_Fund_payment_mechanism_record",
            "directed_money_edge": "no",
            "source_resolution": "hold_formal_source_receipt_and_selection_frame",
            "disposition": "hold",
            "non_inference": "Do not merge this payment mechanism with the USD 276345.50 accrual-filing observation or infer a simple OSD-to-Earthjustice edge.",
        },
    ]

    _, person_source = _read_csv(
        root / "outputs/us_presence_accountability_recon_v1/person_role_observations_v1.csv"
    )
    person_index = {row["person_role_observation_id"]: row for row in person_source}
    person_identity = {
        "USAPN006": "PERSON_CAND_LUMMIS",
        "USAPN007": "PERSON_CAND_DOKTOR",
        "USAPN008": "PERSON_CAND_YOSHIKAWA",
        "USAPN009": "PERSON_CAND_YOSHIKAWA",
        "USAPN010": "PERSON_CAND_DOKTOR",
        "USAPN011": "PERSON_CAND_LUMMIS",
    }
    person_roles: list[dict[str, str]] = []
    for role_id in person_identity:
        row = person_index[role_id]
        person_roles.append(
            {
                "role_id": role_id,
                "person_identity_key": person_identity[role_id],
                "person_name_as_source": row["person_name_as_source"],
                "actor_id": row["actor_id_candidate"],
                "role_title": row["role_title_as_source"],
                "role_start": "",
                "role_observed_at": row["role_observed_at"],
                "derived_actor_dyad": "no",
                "source_resolution": "hold_selection_frame",
                "disposition": "hold",
            }
        )
    _require(len(person_roles) == 6, "reviewed person-role projection count drift")
    _require(all(not row["role_start"] for row in person_roles), "observed dates leaked into role_start")

    _, action_source = _read_csv(
        root / "outputs/us_presence_accountability_recon_v1/action_relation_observations_v1.csv"
    )
    action_index = {row["observation_id"]: row for row in action_source}
    target_updates = {
        "USAA004": ("Network for Okinawa", "research_endpoint_off_graph"),
        "USAA005": ("EO_R5_FUTAMI_TEN_DISTRICTS", "event_only_off_graph"),
        "USAA006": ("Protect Henoko and Takae! NGO Network", "event_only_off_graph"),
        "USAA007": ("ZHAP / ZENKO Henoko Anti-base Project", "provisional_research_endpoint_off_graph"),
    }
    actions: list[dict[str, str]] = []
    for observation_id, (target, endpoint_status) in target_updates.items():
        row = action_index[observation_id]
        actions.append(
            {
                "observation_id": observation_id,
                "source_actor_id": row["source_actor_id"],
                "target_endpoint": target,
                "endpoint_status": endpoint_status,
                "relation_type": row["relation_type"],
                "graph_eligibility": "off_graph",
                "source_resolution": "hold_selection_frame",
                "disposition": "hold",
                "non_inference": row["interpretation_limit"],
            }
        )
    _require(
        next(row for row in actions if row["observation_id"] == "USAA005")["target_endpoint"]
        != "A019",
        "USAA005 retained the rejected A019 endpoint",
    )

    affiliation = [
        {
            "record_id": "SA010-X004-MEM",
            "source_endpoint": "X004",
            "target_endpoint": "X018",
            "relation_type": "network_membership",
            "source_resolution": "hold_actor_source_and_selection_frame",
            "disposition": "hold",
            "non_inference": "Membership does not establish control, funding or political alignment.",
        },
        {
            "record_id": "SA010-X004-CHANNEL",
            "source_endpoint": "X018",
            "target_endpoint": "X004",
            "relation_type": "contributing_member_to_grant_selection_distribution_channel",
            "source_resolution": "hold_actor_source_and_selection_frame",
            "disposition": "hold",
            "non_inference": "The channel is neither exclusive nor permanent; annual amounts belong in separate flow rows.",
        },
    ]

    sponsor = [
        ("Matson", "USO Indo-Pacific", "Mission Partner", "reference_existing:F035"),
        ("University of Maryland Global Campus", "USO Indo-Pacific", "Mission Partner", "provisional_endpoint"),
        ("AIG Japan / AIG Auto Insurance", "USO Indo-Pacific", "Community Partner", "provisional_endpoint"),
        ("Mediatti Broadband Communications / MBC", "USO Okinawa", "Platinum", "reference_existing:F034"),
        ("X003", "USO Okinawa", "Silver", "reference_existing:F002"),
        ("BILLABONG STORE Okinawa Rycom", "USO Okinawa", "Bronze", "provisional_endpoint"),
    ]
    sponsor_snapshots = [
        {
            "snapshot_id": f"SA001-{number:02d}",
            "sponsor_endpoint": sponsor_endpoint,
            "program_endpoint": program_endpoint,
            "reported_tier": tier,
            "observed_at": "2026-08-19",
            "endpoint_or_reuse_status": endpoint_status,
            "amount": "",
            "source_resolution": "hold_schema_sponsor_snapshot",
            "disposition": "hold",
            "non_inference": "A dated tier does not establish amount, start date, governance, affiliation or political stance.",
        }
        for number, (sponsor_endpoint, program_endpoint, tier, endpoint_status) in enumerate(
            sponsor, start=1
        )
    ]

    endpoint_crosswalks = [
        ("SR006", "NPO/ARU halfway house for teenage girls", "defer_raw_label"),
        ("SR007", "沖縄小児在宅医療基金 てぃんさぐの会", "accepted_canonical_crosswalk"),
        ("SR009", "Far East Council / R_BSA_FAR_EAST", "accepted_existing_endpoint_crosswalk"),
        ("SR010", "一般社団法人Oki Hands Oki Hearts", "accepted_canonical_crosswalk"),
        ("USAA004", "Network for Okinawa", "research_endpoint_not_A028"),
        ("USAA005", "EO_R5_FUTAMI_TEN_DISTRICTS", "event_only_endpoint"),
        ("USAA006", "Protect Henoko and Takae! NGO Network", "event_only_endpoint"),
        ("USAA007", "ZHAP / ZENKO Henoko Anti-base Project", "provisional_research_endpoint"),
    ]
    endpoint_rows = [
        {
            "upstream_id": upstream_id,
            "approved_label_or_key": label,
            "endpoint_status": status,
            "actor_admission": "no",
            "relation_fact_approved": "no",
            "disposition": "hold" if upstream_id == "SR006" else "project_identity_only",
        }
        for upstream_id, label, status in endpoint_crosswalks
    ]

    return {
        "money": money,
        "accounting": accounting,
        "person_roles": person_roles,
        "actions": actions,
        "affiliation": affiliation,
        "sponsor_snapshots": sponsor_snapshots,
        "endpoint_crosswalks": endpoint_rows,
    }


_LEG_TOKEN = re.compile(r"(?<![A-Z])L([0-3])(?![A-Z0-9])")


def _migrate_leg_value(value: str) -> str:
    migrated = _LEG_TOKEN.sub(lambda match: f"LEG{match.group(1)}", value)
    return migrated.replace("L-level", "LEG-level")


def _build_leg_projection(root: Path) -> dict[str, Any]:
    specs = (
        (
            "vocabulary",
            Path("outputs/us_presence_network_architecture_v1/coding_vocabulary_v1.csv"),
            70,
        ),
        (
            "validation_rules",
            Path("outputs/us_presence_network_architecture_v1/validation_rules_v1.csv"),
            44,
        ),
        (
            "vertical_slices",
            Path("outputs/us_presence_network_architecture_v1/vertical_slice_register_v1.csv"),
            10,
        ),
        (
            "legitimation_observations",
            Path("outputs/us_presence_service_recon_v1/legitimation_claim_observations_v1.csv"),
            12,
        ),
        (
            "table_contracts",
            Path("outputs/us_presence_network_architecture_v1/proposed_table_contracts_v1.csv"),
            10,
        ),
    )
    projected: dict[str, Any] = {"tables": {}, "distribution": {}, "field_diffs": []}
    id_fields = {
        "vocabulary": "code",
        "validation_rules": "rule_id",
        "vertical_slices": "slice_id",
        "legitimation_observations": "observation_id",
        "table_contracts": "table_id",
    }
    for label, relative, expected_count in specs:
        fields, rows = _read_csv(root / relative)
        _require(len(rows) == expected_count, f"LEG source count drift: {label}")
        migrated = [
            {field: _migrate_leg_value(row[field]) for field in fields}
            for row in rows
        ]
        for source_row, migrated_row in zip(rows, migrated, strict=True):
            for field in fields:
                if source_row[field] != migrated_row[field]:
                    projected["field_diffs"].append(
                        {
                            "table": label,
                            "record_id": source_row[id_fields[label]],
                            "field": field,
                            "before": source_row[field],
                            "after": migrated_row[field],
                        }
                    )
        projected["tables"][label] = {
            "source_path": relative.as_posix(),
            "source_sha256": _sha256(root / relative),
            "fields": fields,
            "rows": migrated,
        }
    lc_rows = projected["tables"]["legitimation_observations"]["rows"]
    for row in lc_rows:
        level = row["legitimation_level"].split("_", 1)[0]
        projected["distribution"][level] = projected["distribution"].get(level, 0) + 1
    _require(
        projected["distribution"] == {"LEG0": 3, "LEG1": 9},
        f"LEG distribution drift: {projected['distribution']}",
    )
    projected["distribution"].update({"LEG2": 0, "LEG3": 0})
    _require(
        len(projected["field_diffs"]) == 33,
        f"LEG migration expected 33 field cells, found {len(projected['field_diffs'])}",
    )
    return projected


def _test_results() -> list[dict[str, str]]:
    results: list[dict[str, str]] = []
    for number in range(1, 36):
        test_id = f"UST-{number:03d}"
        if test_id == "UST-027":
            status = "blocked"
            observed = "9 ProPublica filing interfaces still require official IRS receipt review"
        elif test_id in {"UST-029", "UST-030", "UST-031"}:
            status = "not_run_real_source_plan_blocked"
            observed = "reserved for explicitly synthetic sandbox verification"
        else:
            status = "pass_plan_gate"
            observed = "validated or preserved as a no-write constraint"
        results.append({"test_id": test_id, "status": status, "observed": observed})
    return results


def plan_usn_wave1_integration(root: Path = ROOT) -> dict[str, Any]:
    """Return a deterministic, read-only integration plan for the current base."""

    root = root.resolve()
    _validate_authoritative_receipt(root)
    design_manifest = _validate_design_receipt(root)
    decision_counts = _validate_decision_maps(root)
    central_hashes = _validate_central_baseline(root, design_manifest["central_baseline"])
    frame = _validate_frozen_frame(root)
    relation_overlay = _build_relation_overlay(root)
    directory_overlay = _build_directory_overlay(root)
    source_clusters = _build_source_clusters(root)
    leg_projection = _build_leg_projection(root)
    typed_fact_projection = _build_typed_fact_projection(root)
    _, actions = _read_csv(root / DESIGN_DIR / "expected_central_actions_v1.csv")
    actions = _enrich_action_dispositions(actions)
    _, deltas = _read_csv(root / DESIGN_DIR / "expected_table_deltas_v1.csv")
    _, source_steps = _read_csv(root / DESIGN_DIR / "source_admission_plan_v1.csv")
    _, tests = _read_csv(root / DESIGN_DIR / "test_matrix_v1.csv")
    _require(len(actions) == 37, "expected-action count drift")
    _require(len(deltas) == 18, "expected-delta count drift")
    _require(len(source_steps) == 10, "source-step count drift")
    _require(len(tests) == 35, "test-matrix count drift")

    plan: dict[str, Any] = {
        "schema_version": "1.0.0",
        "plan_id": PLAN_ID,
        "parent_design_commit": PARENT_DESIGN_COMMIT,
        "parent_design_manifest_sha256": _sha256(root / DESIGN_MANIFEST),
        "mode": "plan_only",
        "status": "blocked_pending_source_freeze",
        "authority": {
            "plan_generation": True,
            "synthetic_sandbox_verification": True,
            "central_writeback": False,
            "relation_crosswalk_expansion": False,
            "publication_adapter": False,
            "frontend_writeback": False,
        },
        "central_baseline": central_hashes,
        "decision_counts": decision_counts,
        "selection_frame": frame,
        "source_admission": {
            "status": "pending_official_receipt_review",
            "candidate_references": 58,
            "normalized_urls": 57,
            "existing_exact_urls": 4,
            "new_candidate_upper_bound": 53,
            "propublica_interfaces": 9,
            "allocated_source_ids": [],
            "cluster_resolution_counts": {
                "reuse_existing": 4,
                "candidate_new_non_propublica": 44,
                "hold_official_irs_receipt": 9,
            },
            "steps": source_steps,
        },
        "blockers": [
            {
                "blocker_id": "USB-001",
                "kind": "SOURCE_PLAN_NOT_FROZEN",
                "scope": "9 ProPublica filing interfaces",
                "required_resolution": "pair with or replace by official IRS receipts; then freeze exact URL-to-source plan before allocating S-IDs",
            },
            {
                "blocker_id": "USB-002",
                "kind": "SELECTION_FRAMES_NOT_APPROVED",
                "scope": "directory, person tracer and resource-path candidate frames",
                "required_resolution": "approve each frame membership and denominator separately; do not rewrite the frozen 9/6/2 frame",
            },
            {
                "blocker_id": "USB-003",
                "kind": "SPONSOR_SNAPSHOT_SCHEMA_SEAM_MISSING",
                "scope": "six dated sponsor-tier observations",
                "required_resolution": "add a no-amount dated sponsor-snapshot contract instead of forcing rows into money or affiliation tables",
            },
            {
                "blocker_id": "USB-004",
                "kind": "CENTRAL_WRITEBACK_NOT_AUTHORIZED",
                "scope": "all central and typed fact tables",
                "required_resolution": "obtain a separate principal approval after the real source plan and plan diff are frozen",
            },
        ],
        "actor_admission_preview": [
            {
                **dict(row),
                "source_resolution": "hold_source_freeze",
                "disposition": "hold",
                "write_eligible": "no",
            }
            for row in ACTOR_ADMISSION_PREVIEW
        ],
        "actor_defer_preview": [dict(row) for row in ACTOR_DEFER_PREVIEW],
        "relation_overlay_preview": relation_overlay,
        "directory_overlay_preview": directory_overlay,
        "source_clusters": source_clusters,
        "derived_source_requirements": [
            dict(row) for row in DERIVED_SOURCE_REQUIREMENTS
        ],
        "selection_frame_holds": [dict(row) for row in SELECTION_FRAME_HOLDS],
        "design_gap_holds": [
            {
                "gap_id": "USNDG-001",
                "scope": "A070 dated observations in 2018, 2025 and 2026",
                "reason": "principal return approved bounded observations, but the 37-action design did not declare their exact target rows",
                "disposition": "hold_design_gap",
            },
            {
                "gap_id": "USNDG-002",
                "scope": "six dated sponsor-tier observations",
                "reason": "no approved table contract preserves sponsor tier without implying amount or control",
                "disposition": "hold_schema_sponsor_snapshot",
            },
        ],
        "leg_projection": leg_projection,
        "typed_fact_projection": typed_fact_projection,
        "actions": actions,
        "table_deltas": deltas,
        "test_results": _test_results(),
        "interpretation_limits": [
            "This plan approves no central writeback and exposes no production apply command.",
            "The 43-row legacy relation table remains byte-identical; retyping is an overlay preview only.",
            "A source proposal, official URL, person role, shared event or service observation does not by itself approve a relation, alliance, funding claim, political stance or legitimacy effect.",
            "Synthetic sandbox success is a software-behavior check, not evidence that the real source plan or central writeback is ready.",
        ],
    }
    return _with_plan_hash(plan)


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(
            json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        )


def _field_order(rows: list[dict[str, Any]]) -> list[str]:
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    return fields


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = _field_order(rows)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fields,
            lineterminator="\n",
            extrasaction="raise",
        )
        writer.writeheader()
        writer.writerows(rows)


def _write_tree_manifest(root: Path, name: str = "manifest.json") -> None:
    files = []
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        if path.name == name and path.parent == root:
            continue
        files.append(
            {
                "path": path.relative_to(root).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": _sha256(path),
            }
        )
    _write_json(
        root / name,
        {
            "schema_version": "1.0.0",
            "hash_algorithm": "sha256",
            "files": files,
        },
    )


def materialize_usn_wave1_plan(plan: dict[str, Any], output_dir: Path) -> None:
    """Serialize the read-only plan without embedding machine-specific paths."""

    _validate_plan_hash(plan)
    output_dir.mkdir(parents=True, exist_ok=True)
    _write_json(output_dir / "integration_plan_v1.json", plan)
    _write_csv(output_dir / "expected_actions_v1.csv", plan["actions"])
    _write_csv(output_dir / "expected_table_deltas_v1.csv", plan["table_deltas"])
    _write_csv(
        output_dir / "actor_admission_preview_v1.csv",
        plan["actor_admission_preview"],
    )
    _write_csv(
        output_dir / "actor_defer_preview_v1.csv",
        plan["actor_defer_preview"],
    )
    _write_csv(
        output_dir / "relation_retype_overlay_preview_v1.csv",
        plan["relation_overlay_preview"],
    )
    _write_csv(
        output_dir / "official_site_decision_overlay_preview_v1.csv",
        plan["directory_overlay_preview"],
    )
    _write_csv(output_dir / "test_results_v1.csv", plan["test_results"])
    _write_csv(output_dir / "source_clusters_v1.csv", plan["source_clusters"])
    _write_csv(
        output_dir / "derived_source_requirements_v1.csv",
        plan["derived_source_requirements"],
    )
    _write_csv(
        output_dir / "selection_frame_holds_v1.csv",
        plan["selection_frame_holds"],
    )
    _write_csv(
        output_dir / "design_gap_holds_v1.csv",
        plan["design_gap_holds"],
    )
    _write_csv(
        output_dir / "leg_migration_field_diff_v1.csv",
        plan["leg_projection"]["field_diffs"],
    )
    _write_json(output_dir / "leg_migration_preview_v1.json", plan["leg_projection"])
    for family, rows in plan["typed_fact_projection"].items():
        _write_csv(output_dir / f"typed_{family}_projection_v1.csv", rows)
    _write_json(output_dir / "source_admission_state_v1.json", plan["source_admission"])
    held = [row for row in plan["actions"] if row["disposition"] in {"hold", "exclude"}]
    _write_csv(output_dir / "held_or_blocked_actions_v1.csv", held)
    with (output_dir / "README.md").open(
        "w", encoding="utf-8", newline="\n"
    ) as handle:
        handle.write(
            "# USN wave-1 controlled integration plan\n\n"
            "Status: `blocked_pending_source_freeze`.\n\n"
            "This package is a deterministic read-only projection. It changes no "
            "central table, legacy relation row, publication adapter or frontend. "
            "The source plan must first resolve nine ProPublica filing interfaces "
            "against official IRS receipts. The 57 normalized URL clusters are the "
            "current proposal union, not the final central-source delta; eight further "
            "source requirements are held separately. Directory, person-tracer and "
            "resource-path selection frames also remain unapproved. Synthetic sandbox "
            "receipts verify code behavior only and are not authority for real writeback.\n"
        )
    _write_tree_manifest(output_dir)


def make_synthetic_frozen_plan(plan: dict[str, Any]) -> dict[str, Any]:
    """Create an explicitly non-committable source fixture for sandbox tests."""

    _validate_plan_hash(plan)
    synthetic = copy.deepcopy(plan)
    synthetic["plan_id"] = f"{plan['plan_id']}-SYNTHETIC"
    synthetic["mode"] = "synthetic_sandbox_fixture_only"
    synthetic["status"] = "sandbox_ready_synthetic_fixture"
    synthetic["blockers"] = []
    synthetic["source_admission"]["status"] = "synthetic_frozen_fixture"
    synthetic["source_admission"]["fixture_scope"] = "test_only_non_committable"
    synthetic["source_admission"]["allocated_source_ids"] = [
        f"SYN-S{number:03d}" for number in range(296, 349)
    ]
    for result in synthetic["test_results"]:
        if result["test_id"] == "UST-027":
            result["status"] = "pass_synthetic_fixture_only"
            result["observed"] = "all nine interfaces represented by synthetic official-receipt pairs"
        elif result["test_id"] in {"UST-029", "UST-030", "UST-031"}:
            result["status"] = "pending_sandbox_execution"
            result["observed"] = "synthetic fixture only"
    return _with_plan_hash(synthetic)


def _is_same_or_nested(path: Path, parent: Path) -> bool:
    return path == parent or path.is_relative_to(parent)


def _validate_generation(root: Path) -> None:
    manifest = json.loads((root / "generation_manifest.json").read_text(encoding="utf-8"))
    for item in manifest["files"]:
        path = root / item["path"]
        _require(path.is_file(), f"sandbox generation missing file: {item['path']}")
        _require(_sha256(path) == item["sha256"], f"sandbox generation hash drift: {item['path']}")
        _require(path.stat().st_size == item["bytes"], f"sandbox generation byte drift: {item['path']}")


def simulate_usn_wave1_integration(
    source_root: Path,
    sandbox_root: Path,
    plan: dict[str, Any],
    *,
    fail_at: str | None = None,
) -> dict[str, Any]:
    """Materialize a synthetic immutable projection outside the source repo."""

    source_root = source_root.resolve()
    sandbox_root = sandbox_root.resolve()
    if _is_same_or_nested(sandbox_root, source_root):
        raise PlanValidationError("sandbox must be outside source root")
    _validate_plan_hash(plan)
    if plan.get("status") != "sandbox_ready_synthetic_fixture":
        raise PlanValidationError("source plan is not frozen; sandbox simulation refused")
    if plan.get("source_admission", {}).get("fixture_scope") != "test_only_non_committable":
        raise PlanValidationError("sandbox source fixture is not explicitly test-only")

    # Re-check the live source receipts; a frozen projection cannot float over drift.
    _validate_authoritative_receipt(source_root)
    design_manifest = _validate_design_receipt(source_root)
    _validate_decision_maps(source_root)
    _validate_central_baseline(source_root, design_manifest["central_baseline"])
    if fail_at == "after_validation":
        raise RuntimeError("injected failure: after_validation")

    generation_name = plan["plan_id"]
    generation = sandbox_root / "generations" / generation_name
    if generation.exists():
        _validate_generation(generation)
        receipt = json.loads(
            (generation / "sandbox_validation_report_v1.json").read_text(
                encoding="utf-8"
            )
        )
        _require(receipt["plan_hash"] == plan["plan_hash"], "existing sandbox plan mismatch")
        return {
            "created": False,
            "changed_files": 0,
            "generation_path": str(generation),
            "status": "NOOP_BYTE_IDENTICAL",
        }

    sandbox_root.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=".usn-wave1-", dir=sandbox_root))
    try:
        materialize_usn_wave1_plan(plan, staging / "plan")
        _write_csv(
            staging / "relation_retype_overlay_v1.csv",
            plan["relation_overlay_preview"],
        )
        _write_csv(
            staging / "actor_admission_preview_v1.csv",
            plan["actor_admission_preview"],
        )
        _write_csv(
            staging / "official_site_decision_overlay_v1.csv",
            plan["directory_overlay_preview"],
        )
        _write_json(staging / "leg_migration_projection_v1.json", plan["leg_projection"])
        _write_json(
            staging / "protected_central_baseline_v1.json",
            plan["central_baseline"],
        )
        if fail_at == "after_projection":
            raise RuntimeError("injected failure: after_projection")

        report = {
            "schema_version": "1.0.0",
            "status": "PASS_SYNTHETIC_SANDBOX_ONLY",
            "plan_id": plan["plan_id"],
            "plan_hash": plan["plan_hash"],
            "fixture_scope": "test_only_non_committable",
            "claims_real_writeback_ready": False,
            "central_writeback_performed": False,
            "legacy_relation_table_modified": False,
            "publication_or_frontend_modified": False,
            "projected_actor_admissions": 6,
            "projected_relation_overlay_rows": 43,
            "projected_directory_decisions": 65,
            "source_note": "Synthetic IDs and receipt pairs test code behavior only; the real source plan remains blocked.",
        }
        _write_json(staging / "sandbox_validation_report_v1.json", report)
        _write_tree_manifest(staging, "generation_manifest.json")
        _validate_generation(staging)
        if fail_at == "before_commit":
            raise RuntimeError("injected failure: before_commit")

        generation.parent.mkdir(parents=True, exist_ok=True)
        os.replace(staging, generation)
        return {
            "created": True,
            "changed_files": len(json.loads((generation / "generation_manifest.json").read_text(encoding="utf-8"))["files"]),
            "generation_path": str(generation),
            "status": "PASS_SYNTHETIC_SANDBOX_ONLY",
        }
    finally:
        if staging.exists():
            shutil.rmtree(staging)


def _protected_source_hashes(root: Path) -> dict[str, str]:
    paths = [root / relative for relative in CENTRAL_PATHS]
    paths.extend(
        [
            root / RELATION_PATH,
            root / FRAME_PATH,
            root / DIRECTORY_DECISION_PATH,
            root
            / "outputs/us_presence_network_architecture_v1/coding_vocabulary_v1.csv",
            root
            / "outputs/us_presence_network_architecture_v1/validation_rules_v1.csv",
            root
            / "outputs/us_presence_network_architecture_v1/vertical_slice_register_v1.csv",
            root
            / "outputs/us_presence_service_recon_v1/legitimation_claim_observations_v1.csv",
        ]
    )
    for directory in (
        root / "outputs/exploration_system_data_v1",
        root / "prototypes/nr3_explorer/dist",
    ):
        if directory.is_dir():
            paths.extend(sorted(item for item in directory.rglob("*") if item.is_file()))
    return {
        path.relative_to(root).as_posix(): _sha256(path)
        for path in paths
        if path.is_file()
    }


def verify_usn_wave1_plan_in_sandbox(
    source_root: Path, plan: dict[str, Any]
) -> dict[str, Any]:
    """Run the synthetic sandbox, idempotence and failure-injection checks."""

    source_root = source_root.resolve()
    _validate_plan_hash(plan)
    _require(
        plan.get("status") == "blocked_pending_source_freeze",
        "sandbox verifier expects the current blocked real plan",
    )
    before = _protected_source_hashes(source_root)
    synthetic = make_synthetic_frozen_plan(plan)

    with tempfile.TemporaryDirectory() as sandbox_dir:
        sandbox = Path(sandbox_dir)
        first = simulate_usn_wave1_integration(source_root, sandbox, synthetic)
        generation = Path(first["generation_path"])
        first_files = {
            path.relative_to(generation).as_posix(): _sha256(path)
            for path in sorted(item for item in generation.rglob("*") if item.is_file())
        }
        second = simulate_usn_wave1_integration(source_root, sandbox, synthetic)
        second_files = {
            path.relative_to(generation).as_posix(): _sha256(path)
            for path in sorted(item for item in generation.rglob("*") if item.is_file())
        }
        _require(first["created"] is True, "first sandbox projection was not created")
        _require(second["created"] is False, "second sandbox projection was not a no-op")
        _require(second["changed_files"] == 0, "second sandbox projection changed files")
        _require(first_files == second_files, "second sandbox projection was not byte-identical")

    passed_stages: list[str] = []
    for stage in ("after_validation", "after_projection", "before_commit"):
        with tempfile.TemporaryDirectory() as sandbox_dir:
            sandbox = Path(sandbox_dir)
            try:
                simulate_usn_wave1_integration(
                    source_root,
                    sandbox,
                    synthetic,
                    fail_at=stage,
                )
            except RuntimeError as error:
                _require(str(error) == f"injected failure: {stage}", f"wrong failure receipt for {stage}")
            else:
                raise PlanValidationError(f"failure injection did not fire: {stage}")
            _require(not (sandbox / "generations").exists(), f"failure published a generation: {stage}")
            _require(not list(sandbox.rglob("*.tmp")), f"failure left temporary files: {stage}")
            passed_stages.append(stage)

    after = _protected_source_hashes(source_root)
    changed = sorted(path for path in before if before[path] != after.get(path))
    _require(not changed and before.keys() == after.keys(), "sandbox changed protected source files")
    return {
        "schema_version": "1.0.0",
        "status": "PASS_SYNTHETIC_SANDBOX_ONLY",
        "real_plan_id": plan["plan_id"],
        "real_plan_hash": plan["plan_hash"],
        "real_plan_status": plan["status"],
        "synthetic_plan_id": synthetic["plan_id"],
        "synthetic_fixture_scope": "test_only_non_committable",
        "claims_real_writeback_ready": False,
        "first_projection_created": True,
        "second_projection_byte_noop": True,
        "failure_injection_stages_passed": sorted(passed_stages),
        "protected_source_files": len(before),
        "changed_protected_source_files": 0,
        "central_writeback_performed": False,
        "relation_crosswalk_expanded": False,
        "publication_or_frontend_modified": False,
        "interpretation_limit": "This receipt validates software behavior with a synthetic source-freeze fixture. The real source plan is still blocked and no production apply is authorized.",
    }


def validate_usn_wave1_plan_package(
    source_root: Path, package_root: Path
) -> dict[str, Any]:
    """Validate the persisted plan package against receipts and a fresh plan."""

    source_root = source_root.resolve()
    package_root = package_root.resolve()
    manifest = json.loads((package_root / "manifest.json").read_text(encoding="utf-8"))
    for item in manifest["files"]:
        path = package_root / item["path"]
        _require(path.is_file(), f"plan package missing file: {item['path']}")
        _require(_sha256(path) == item["sha256"], f"plan package hash drift: {item['path']}")
        _require(path.stat().st_size == item["bytes"], f"plan package byte drift: {item['path']}")

    persisted = json.loads(
        (package_root / "integration_plan_v1.json").read_text(encoding="utf-8")
    )
    _validate_plan_hash(persisted)
    fresh = plan_usn_wave1_integration(source_root)
    _require(
        persisted["plan_hash"] == fresh["plan_hash"],
        "persisted plan no longer matches a fresh read-only projection",
    )
    sandbox_receipt = json.loads(
        (package_root / "sandbox_validation_v1.json").read_text(encoding="utf-8")
    )
    _require(
        sandbox_receipt["status"] == "PASS_SYNTHETIC_SANDBOX_ONLY",
        "sandbox receipt status drift",
    )
    _require(
        sandbox_receipt["real_plan_hash"] == persisted["plan_hash"],
        "sandbox receipt plan hash drift",
    )
    _require(
        sandbox_receipt["claims_real_writeback_ready"] is False,
        "sandbox receipt overclaims real writeback readiness",
    )
    return {
        "status": "PASS_PLAN_PACKAGE_BLOCKED",
        "plan_id": persisted["plan_id"],
        "plan_hash": persisted["plan_hash"],
        "actions": len(persisted["actions"]),
        "source_clusters": len(persisted["source_clusters"]),
        "leg_changed_cells": len(persisted["leg_projection"]["field_diffs"]),
        "central_files_changed": 0,
        "real_source_plan_status": persisted["status"],
        "central_writeback_authorized": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build the read-only USN wave-1 integration plan."
    )
    parser.add_argument(
        "--verify-sandbox",
        action="store_true",
        help="also run the explicitly synthetic, non-committable sandbox suite",
    )
    args = parser.parse_args()
    plan = plan_usn_wave1_integration(ROOT)
    output = ROOT / "outputs/us_presence_integration_plan_v1"
    materialize_usn_wave1_plan(plan, output)
    if args.verify_sandbox:
        receipt = verify_usn_wave1_plan_in_sandbox(ROOT, plan)
        _write_json(output / "sandbox_validation_v1.json", receipt)
        _write_tree_manifest(output)
        print(receipt["status"])
    print(plan["status"])
    print(f"plan_id={plan['plan_id']}")
    print(f"actions={len(plan['actions'])}")
    print(f"blockers={len(plan['blockers'])}")
    print("central_writeback=false")


if __name__ == "__main__":
    main()
