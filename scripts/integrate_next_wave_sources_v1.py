"""Integrate and validate the NW2-F source proposal batch.

Authorized central writes are intentionally narrow: this script may update only
``data/interim/05_source_log_initial_v0.csv``.  Archive artifacts and the
archive manifest are written separately by the existing ``archive_sources.py``
command for S248--S294.  All other writes stay under
``outputs/next_wave_source_integration_v1``.

The 47 new rows remain ``ai_seeded`` and proposal-derived.  Source inclusion
does not approve an actor, relation, alliance, funding flow, causal claim,
legal conclusion, electoral effect, or organizational classification.
"""

from __future__ import annotations

import csv
import hashlib
import json
import os
import re
import tempfile
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data" / "interim" / "37_next_wave_source_proposal_crosswalk_v1.csv"
RECORD_AUDIT = (
    ROOT
    / "outputs"
    / "next_wave_source_proposal_audit_v1"
    / "proposal_record_audit_v1.csv"
)
METADATA_REVIEW = (
    ROOT
    / "outputs"
    / "next_wave_source_proposal_audit_v1"
    / "metadata_review_queue_v1.csv"
)
WEB_REVIEW = (
    ROOT
    / "outputs"
    / "next_wave_source_proposal_audit_v1"
    / "web_archive_review_queue_v1.csv"
)
SOURCE_LOG = ROOT / "data" / "interim" / "05_source_log_initial_v0.csv"
MANIFEST = ROOT / "source_docs" / "source_archive" / "source_archive_manifest.csv"
OUT = ROOT / "outputs" / "next_wave_source_integration_v1"

MERGE_MANIFEST = OUT / "source_merge_manifest_v1.csv"
PROPOSAL_CROSSWALK = OUT / "proposal_to_source_crosswalk_v1.csv"
NEW_SOURCE_ROWS = OUT / "integrated_source_rows_S248_S294_v1.csv"
HR030 = OUT / "HR030_source_metadata_archive_review_v0.csv"
PROTECTED_SHA = OUT / "protected_actor_edge_sha_v1.csv"
README = OUT / "README.md"
VALIDATION = OUT / "validation_report_v1.md"

TRACKING_QUERY_PREFIXES = ("utm_",)
TRACKING_QUERY_KEYS = {"fbclid", "gclid", "mc_cid", "mc_eid"}
INTEGRATION_MARKER = "NW2-H controlled source integration 2026-07-13"
HUMAN_REVIEW_FIELDS = (
    "decision",
    "revised_title",
    "revised_source_type",
    "revised_year",
    "revised_locator",
    "revised_support_scope",
    "revised_evidence_level",
    "archive_resolution",
    "reviewer",
    "review_date",
    "review_note",
)

SOURCE_FIELDS = [
    "source_id",
    "source_type",
    "title",
    "year",
    "url",
    "what_it_supports",
    "evidence_level",
    "bias_note",
    "review_status",
    "notes",
]

PROTECTED_CENTRAL_TABLES = [
    ROOT / "data" / "interim" / "01_actor_registry_initial_v0.csv",
    ROOT / "data" / "interim" / "02_actor_aliases_initial_v0.csv",
    ROOT / "data" / "interim" / "07_actor_issue_edges_initial_v0.csv",
    ROOT / "data" / "interim" / "08_actor_place_edges_initial_v0.csv",
    ROOT / "data" / "interim" / "09_actor_event_venue_edges_v0.csv",
    ROOT / "data" / "interim" / "15_funding_or_support_edges_sample_v0.csv",
    ROOT / "data" / "interim" / "18_legal_policy_actor_roles_v0.csv",
    ROOT / "data" / "interim" / "21_admin_collaboration_relations_v0.csv",
    ROOT / "data" / "interim" / "22_admin_amount_observations_v0.csv",
    ROOT / "data" / "interim" / "23_admin_function_observations_v0.csv",
    ROOT / "data" / "interim" / "24_r01_r02_actor_issue_layered_v0.csv",
    ROOT / "data" / "interim" / "25_coaction_event_participation_v0.csv",
    ROOT / "data" / "interim" / "26_actor_event_venue_target_entry_modes_v0.csv",
    ROOT / "data" / "interim" / "28_edge_activation_candidates_v1.csv",
]

MERGE_FIELDS = [
    "audit_row_id",
    "source_id",
    "integration_status",
    "proposal_refs",
    "candidate_refs",
    "normalized_url",
    "source_review_status",
    "archive_status",
    "archive_local_path",
    "archive_sha256",
    "archive_http_status",
    "archive_note",
    "metadata_review_required",
    "web_review_required",
    "hr030_item_id",
    "relation_or_claim_approved",
    "boundary_note",
]

PROPOSAL_FIELDS = [
    "record_audit_id",
    "input_batch",
    "proposal_id",
    "candidate_id",
    "audit_row_id",
    "source_id",
    "integration_status",
    "normalized_url",
    "source_review_status",
    "archive_status",
    "relation_or_claim_approved",
    "caveat",
]

HR030_FIELDS = [
    "review_item_id",
    "audit_row_id",
    "source_id",
    "integration_status",
    "proposal_refs",
    "url",
    "archive_status",
    "archive_note",
    "metadata_issue_codes",
    "web_archive_issue_codes",
    "actual_archive_failure",
    "current_title",
    "current_source_type",
    "current_year",
    "current_locator",
    "current_support_scope",
    "current_evidence_level",
    "caveat_and_boundary",
    "decision",
    "revised_title",
    "revised_source_type",
    "revised_year",
    "revised_locator",
    "revised_support_scope",
    "revised_evidence_level",
    "archive_resolution",
    "reviewer",
    "review_date",
    "review_note",
]

PROTECTED_FIELDS = ["path", "sha256_before_run", "sha256_after_run", "unchanged"]


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def atomic_write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    """Write a validated temporary CSV and atomically replace ``path``.

    The failure-injection environment variable is used only by the acceptance
    test.  It raises after the temporary file has been written and parsed but
    before ``os.replace``, proving that the destination remains untouched.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8-sig",
            newline="",
            prefix=f".{path.name}.",
            suffix=".tmp",
            dir=path.parent,
            delete=False,
        ) as handle:
            temp_path = Path(handle.name)
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
            handle.flush()
            os.fsync(handle.fileno())
        temp_fields, temp_rows = read_csv(temp_path)
        if temp_fields != fields or temp_rows != rows:
            raise RuntimeError("temporary source-log serialization failed round-trip validation")
        if os.environ.get("NW2H_FAIL_BEFORE_ATOMIC_REPLACE") == "1":
            raise RuntimeError("injected failure before atomic source-log replace")
        os.replace(temp_path, path)
        temp_path = None
    finally:
        if temp_path is not None and temp_path.exists():
            temp_path.unlink()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def is_http_url(value: str) -> bool:
    parts = urlsplit((value or "").strip())
    return parts.scheme.lower() in {"http", "https"} and bool(parts.hostname)


def normalize_url(value: str) -> str:
    raw = (value or "").strip()
    parts = urlsplit(raw)
    if parts.scheme.lower() not in {"http", "https"} or not parts.hostname:
        raise ValueError(f"not an HTTP(S) URL: {value}")
    scheme = parts.scheme.lower()
    hostname = parts.hostname.lower()
    port = parts.port
    if port and not (
        (scheme == "http" and port == 80)
        or (scheme == "https" and port == 443)
    ):
        netloc = f"{hostname}:{port}"
    else:
        netloc = hostname
    path = re.sub(r"/{2,}", "/", parts.path or "/")
    if path != "/":
        path = path.rstrip("/")
    query = urlencode(
        sorted(
            (key, item)
            for key, item in parse_qsl(parts.query, keep_blank_values=True)
            if key.lower() not in TRACKING_QUERY_KEYS
            and not key.lower().startswith(TRACKING_QUERY_PREFIXES)
        )
    )
    return urlunsplit((scheme, netloc, path, query, ""))


def unique(values: list[str]) -> list[str]:
    return list(dict.fromkeys(value.strip() for value in values if value and value.strip()))


def joined(values: list[str], separator: str = ";") -> str:
    return separator.join(unique(values))


def source_number(source_id: str) -> int:
    match = re.fullmatch(r"S(\d+)", source_id)
    if not match:
        raise ValueError(f"invalid source ID: {source_id}")
    return int(match.group(1))


def protected_hashes() -> dict[str, str]:
    return {
        str(path.relative_to(ROOT)).replace("\\", "/"): sha256_file(path)
        for path in PROTECTED_CENTRAL_TABLES
    }


def build_source(audit: dict[str, str]) -> dict[str, str]:
    source_id = audit["suggested_source_id_if_merged"].strip()
    if not source_id:
        raise ValueError(f"{audit['audit_row_id']} is new but lacks a suggested S ID")
    if audit["suggested_id_status"] != "proposal_only_not_reserved":
        raise ValueError(f"{audit['audit_row_id']} was not an unreserved proposal")
    notes_parts = [
        f"{INTEGRATION_MARKER}; audit={audit['audit_row_id']}; proposal refs={audit['proposal_refs']}.",
        "Metadata is proposal-derived and remains ai_seeded.",
        "Source inclusion does not approve actor entry, relation, alliance, funding, causal interpretation, legal conclusion, electoral effect, or organization classification.",
    ]
    if audit["metadata_issue_codes"].strip():
        notes_parts.append(f"HR-030 metadata flags={audit['metadata_issue_codes']}.")
    if audit["web_review_required"] == "yes":
        notes_parts.append(f"HR-030 web/archive flags={audit['archive_access_risk']}.")
    notes_parts.append(f"Sensitive boundary tags={audit['sensitive_boundary_tags']}.")
    return {
        "source_id": source_id,
        "source_type": audit["suggested_source_type"].strip(),
        "title": audit["proposed_title"].strip(),
        "year": audit["suggested_year"].strip(),
        "url": audit["normalized_url"].strip(),
        "what_it_supports": audit["support_scopes"].strip(),
        "evidence_level": audit["suggested_evidence_level"].strip(),
        "bias_note": audit["caveats"].strip(),
        "review_status": "ai_seeded",
        "notes": " ".join(notes_parts),
    }


def load_authoritative_audit() -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    _, audit_rows = read_csv(AUDIT)
    _, record_rows = read_csv(RECORD_AUDIT)
    if len(audit_rows) != 49 or len(record_rows) != 50:
        raise ValueError(
            f"NW2-F authority changed: unique={len(audit_rows)}, records={len(record_rows)}"
        )
    if any(row["relation_or_claim_approved"] != "no" for row in audit_rows):
        raise ValueError("NW2-F contains an approved relation or claim")
    if len({row["normalized_url"] for row in audit_rows}) != 49:
        raise ValueError("NW2-F unique URL authority is not unique")
    new_rows = [row for row in audit_rows if row["current_source_match"] == "no"]
    reused = [row for row in audit_rows if row["current_source_match"] == "yes"]
    if len(new_rows) != 47 or len(reused) != 2:
        raise ValueError("NW2-F must contain 47 new and 2 reused unique URLs")
    expected_ids = [f"S{number:03d}" for number in range(248, 295)]
    if [row["suggested_source_id_if_merged"] for row in new_rows] != expected_ids:
        raise ValueError("NW2-F suggested ID order is not S248-S294")
    if {row["current_source_ids"] for row in reused} != {"S158", "S204"}:
        raise ValueError("NW2-F reused source IDs changed")
    return audit_rows, record_rows


def prepare_source_log(
    audit_rows: list[dict[str, str]],
) -> tuple[list[dict[str, str]], list[dict[str, str]], int]:
    fields, source_rows = read_csv(SOURCE_LOG)
    if fields != SOURCE_FIELDS:
        raise ValueError(f"central source schema changed: {fields}")
    by_id = {row["source_id"]: row for row in source_rows}
    if len(by_id) != len(source_rows):
        raise ValueError("duplicate source IDs exist before NW2-H integration")
    if {source_number(row["source_id"]) for row in source_rows if source_number(row["source_id"]) <= 247} != set(range(1, 248)):
        raise ValueError("S001-S247 baseline is incomplete")
    unexpected = [row["source_id"] for row in source_rows if source_number(row["source_id"]) > 294]
    if unexpected not in ([], ["S295"]):
        raise ValueError(f"unexpected post-batch source IDs already exist: {unexpected}")

    new_audit = [row for row in audit_rows if row["current_source_match"] == "no"]
    candidates = [build_source(row) for row in new_audit]
    added = 0
    for candidate in candidates:
        source_id = candidate["source_id"]
        existing = by_id.get(source_id)
        if existing is None:
            source_rows.append(candidate)
            by_id[source_id] = candidate
            added += 1
        elif existing != candidate:
            raise ValueError(f"existing {source_id} differs from NW2-H proposal-derived row")

    source_rows.sort(key=lambda row: source_number(row["source_id"]))
    return source_rows, candidates, added


def duplicate_url_groups(rows: list[dict[str, str]]) -> dict[str, list[str]]:
    groups: dict[str, list[str]] = defaultdict(list)
    for row in rows:
        if is_http_url(row["url"]):
            groups[normalize_url(row["url"])].append(row["source_id"])
    return {
        url: ids for url, ids in groups.items() if len(ids) > 1
    }


def validate_source_log(
    source_rows: list[dict[str, str]],
    audit_rows: list[dict[str, str]],
    candidates: list[dict[str, str]],
) -> dict[str, object]:
    if len(source_rows) not in {294, 295}:
        raise ValueError(f"source log must contain the 294-row NW2-H state plus at most S295, got {len(source_rows)}")
    ids = [row["source_id"] for row in source_rows]
    if len(ids) != len(set(ids)) or ids != [f"S{number:03d}" for number in range(1, len(ids) + 1)]:
        raise ValueError("source IDs are not unique and continuous through the current maximum")
    by_id = {row["source_id"]: row for row in source_rows}
    for candidate in candidates:
        if by_id[candidate["source_id"]] != candidate:
            raise ValueError(f"central row drift for {candidate['source_id']}")
        if candidate["review_status"] != "ai_seeded":
            raise ValueError(f"{candidate['source_id']} was upgraded without human review")

    audit_by_id = {
        row["suggested_source_id_if_merged"]: row
        for row in audit_rows
        if row["current_source_match"] == "no"
    }
    new_norms = [normalize_url(by_id[source_id]["url"]) for source_id in audit_by_id]
    if len(new_norms) != len(set(new_norms)):
        raise ValueError("S248-S294 contain a normalized URL duplicate")
    old_norms = {
        normalize_url(row["url"])
        for row in source_rows
        if source_number(row["source_id"]) <= 247 and is_http_url(row["url"])
    }
    if old_norms & set(new_norms):
        raise ValueError("a new S248-S294 URL duplicates an S001-S247 URL")

    reused = {
        row["current_source_ids"]: row["normalized_url"]
        for row in audit_rows
        if row["current_source_match"] == "yes"
    }
    for source_id, normalized in reused.items():
        if normalize_url(by_id[source_id]["url"]) != normalized:
            raise ValueError(f"reused URL mismatch for {source_id}")

    duplicates = duplicate_url_groups(source_rows)
    if duplicates != {"https://okinawataiwa.net/": ["S022", "S024"]}:
        raise ValueError(f"normalized URL duplicate set changed: {duplicates}")
    return {
        "source_count": len(source_rows),
        "new_unique_urls": len(new_norms),
        "grandfathered_duplicate_groups": len(duplicates),
    }


def load_manifest() -> tuple[dict[str, dict[str, str]], list[dict[str, str]]]:
    _, rows = read_csv(MANIFEST)
    by_id = {row["source_id"]: row for row in rows}
    if len(by_id) != len(rows):
        raise ValueError("archive manifest contains duplicate source IDs")
    return by_id, rows


def validate_archives(
    source_rows: list[dict[str, str]], manifest_by_id: dict[str, dict[str, str]], manifest_rows: list[dict[str, str]]
) -> dict[str, object]:
    source_by_id = {row["source_id"]: row for row in source_rows}
    if len(manifest_rows) not in {247, 294, 295}:
        raise ValueError(f"manifest must be pre-archive 247, NW2-H 294, or current 295 rows, got {len(manifest_rows)}")
    artifact_checked = 0
    artifact_mismatches: list[str] = []
    for row in manifest_rows:
        if row["source_id"] not in source_by_id:
            raise ValueError(f"manifest source absent from source log: {row['source_id']}")
        if row["url"].strip() != source_by_id[row["source_id"]]["url"].strip():
            raise ValueError(f"manifest/source URL mismatch: {row['source_id']}")
        if row["archive_status"] in {"archived", "manual_archived"}:
            local = ROOT / row["local_path"]
            if not local.exists():
                artifact_mismatches.append(f"{row['source_id']}:missing_local_path")
                continue
            actual = sha256_file(local)
            if actual != row["sha256"]:
                artifact_mismatches.append(f"{row['source_id']}:sha_mismatch")
            artifact_checked += 1
    if artifact_mismatches:
        raise ValueError(f"preserved artifact validation failed: {artifact_mismatches}")

    batch_rows = [
        manifest_by_id[source_id]
        for source_id in (f"S{number:03d}" for number in range(248, 295))
        if source_id in manifest_by_id
    ]
    for row in batch_rows:
        if row["archive_status"] not in {"archived", "failed"}:
            raise ValueError(f"unexpected NW2-H archive status: {row['source_id']}={row['archive_status']}")
        metadata_path = ROOT / row["metadata_path"]
        if not metadata_path.exists():
            raise ValueError(f"missing archive metadata: {row['source_id']}")
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        for field in ("source_id", "url", "archive_status", "local_path", "sha256"):
            if str(metadata.get(field, "")) != row[field]:
                raise ValueError(f"metadata/manifest {field} mismatch: {row['source_id']}")

    batch_counts = Counter(row["archive_status"] for row in batch_rows)
    return {
        "manifest_count": len(manifest_rows),
        "manifest_complete": len(manifest_rows) == len(source_rows),
        "artifact_checked": artifact_checked,
        "batch_archived": batch_counts.get("archived", 0),
        "batch_failed": batch_counts.get("failed", 0),
        "batch_not_in_manifest": 47 - len(batch_rows),
    }


def source_id_for(audit: dict[str, str]) -> str:
    if audit["current_source_match"] == "yes":
        return audit["current_source_ids"]
    return audit["suggested_source_id_if_merged"]


def stable_hr030_id(source_id: str, audit_row_id: str) -> str:
    return f"HR030-{source_id}-{audit_row_id}"


def merge_hr030_human_fields(
    generated: list[dict[str, str]],
    existing: list[dict[str, str]],
) -> list[dict[str, str]]:
    """Preserve HR-030 human work by the stable source/audit composite key."""
    existing_by_key: dict[tuple[str, str], dict[str, str]] = {}
    for row in existing:
        key = (row.get("source_id", "").strip(), row.get("audit_row_id", "").strip())
        if not all(key):
            raise ValueError(f"existing HR-030 row lacks stable key: {row.get('review_item_id', '')}")
        if key in existing_by_key:
            raise ValueError(f"duplicate existing HR-030 stable key: {key}")
        existing_by_key[key] = row

    generated_keys = {(row["source_id"], row["audit_row_id"]) for row in generated}
    orphaned_human = [
        key
        for key, row in existing_by_key.items()
        if key not in generated_keys and any(row.get(field, "") for field in HUMAN_REVIEW_FIELDS)
    ]
    if orphaned_human:
        raise ValueError(
            "existing reviewed HR-030 rows would be orphaned; preserve/migrate them first: "
            f"{orphaned_human}"
        )

    merged: list[dict[str, str]] = []
    for seed in generated:
        key = (seed["source_id"], seed["audit_row_id"])
        row = dict(seed)
        prior = existing_by_key.get(key)
        if prior:
            for field in HUMAN_REVIEW_FIELDS:
                row[field] = prior.get(field, "")
        merged.append(row)
    return merged


def build_hr030(
    audit_rows: list[dict[str, str]],
    source_by_id: dict[str, dict[str, str]],
    manifest_by_id: dict[str, dict[str, str]],
    metadata_queue: dict[str, dict[str, str]],
    web_queue: dict[str, dict[str, str]],
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for audit in audit_rows:
        source_id = source_id_for(audit)
        manifest = manifest_by_id.get(source_id, {})
        status = manifest.get("archive_status", "not_in_manifest")
        actual_failure = status == "failed"
        metadata = metadata_queue.get(audit["audit_row_id"])
        web = web_queue.get(audit["audit_row_id"])
        if metadata is None and web is None and not actual_failure:
            continue
        issue_web = web["issue_codes"] if web else ""
        if actual_failure:
            issue_web = joined([issue_web, "actual_archive_failed"])
        source = source_by_id[source_id]
        rows.append(
            {
                "review_item_id": stable_hr030_id(source_id, audit["audit_row_id"]),
                "audit_row_id": audit["audit_row_id"],
                "source_id": source_id,
                "integration_status": (
                    "provisional_source_log_reuse_existing"
                    if audit["current_source_match"] == "yes"
                    else "provisional_source_log_new"
                ),
                "proposal_refs": audit["proposal_refs"],
                "url": audit["normalized_url"],
                "archive_status": status,
                "archive_note": manifest.get("note", ""),
                "metadata_issue_codes": metadata["issue_codes"] if metadata else "",
                "web_archive_issue_codes": issue_web,
                "actual_archive_failure": "yes" if actual_failure else "no",
                "current_title": source["title"],
                "current_source_type": source["source_type"],
                "current_year": source["year"],
                "current_locator": audit["locators"],
                "current_support_scope": source["what_it_supports"],
                "current_evidence_level": source["evidence_level"],
                "caveat_and_boundary": joined(
                    [audit["caveats"], audit["sensitive_boundary_tags"]], " | "
                ),
                "decision": "",
                "revised_title": "",
                "revised_source_type": "",
                "revised_year": "",
                "revised_locator": "",
                "revised_support_scope": "",
                "revised_evidence_level": "",
                "archive_resolution": "",
                "reviewer": "",
                "review_date": "",
                "review_note": "",
            }
        )
    return rows


def build_outputs(
    audit_rows: list[dict[str, str]],
    record_rows: list[dict[str, str]],
    source_rows: list[dict[str, str]],
    manifest_by_id: dict[str, dict[str, str]],
    hr030_rows: list[dict[str, str]],
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    source_by_id = {row["source_id"]: row for row in source_rows}
    hr_by_audit = {row["audit_row_id"]: row["review_item_id"] for row in hr030_rows}
    merge_rows: list[dict[str, str]] = []
    for audit in audit_rows:
        source_id = source_id_for(audit)
        archive = manifest_by_id.get(source_id, {})
        merge_rows.append(
            {
                "audit_row_id": audit["audit_row_id"],
                "source_id": source_id,
                "integration_status": (
                    "provisional_source_log_reuse_existing"
                    if audit["current_source_match"] == "yes"
                    else "provisional_source_log_new"
                ),
                "proposal_refs": audit["proposal_refs"],
                "candidate_refs": audit["candidate_refs"],
                "normalized_url": audit["normalized_url"],
                "source_review_status": source_by_id[source_id]["review_status"],
                "archive_status": archive.get("archive_status", "not_in_manifest"),
                "archive_local_path": archive.get("local_path", ""),
                "archive_sha256": archive.get("sha256", ""),
                "archive_http_status": archive.get("http_status", ""),
                "archive_note": archive.get("note", ""),
                "metadata_review_required": audit["human_metadata_review_required"],
                "web_review_required": audit["web_review_required"],
                "hr030_item_id": hr_by_audit.get(audit["audit_row_id"], ""),
                "relation_or_claim_approved": "no",
                "boundary_note": (
                    "Provisional source-log index only: metadata is not human-reviewed; "
                    "archive failure does not withdraw the provisional S ID; actor/relation/"
                    "alliance/funding/causal/legal/electoral claims remain unapproved and "
                    "must not be used as formal relationship findings."
                ),
            }
        )

    merge_by_audit = {row["audit_row_id"]: row for row in merge_rows}
    proposal_rows: list[dict[str, str]] = []
    for record in record_rows:
        merge = merge_by_audit[record["url_group_id"]]
        proposal_rows.append(
            {
                "record_audit_id": record["record_audit_id"],
                "input_batch": record["input_batch"],
                "proposal_id": record["proposal_id"],
                "candidate_id": record["candidate_id"],
                "audit_row_id": record["url_group_id"],
                "source_id": merge["source_id"],
                "integration_status": merge["integration_status"],
                "normalized_url": record["normalized_url"],
                "source_review_status": merge["source_review_status"],
                "archive_status": merge["archive_status"],
                "relation_or_claim_approved": "no",
                "caveat": record["caveat"],
            }
        )
    return merge_rows, proposal_rows


def validate_outputs(
    merge_rows: list[dict[str, str]],
    proposal_rows: list[dict[str, str]],
    hr030_rows: list[dict[str, str]],
    archive_stats: dict[str, object],
) -> None:
    if len(merge_rows) != 49 or len(proposal_rows) != 50:
        raise ValueError("integration crosswalk coverage changed")
    if sum(row["integration_status"] == "provisional_source_log_new" for row in merge_rows) != 47:
        raise ValueError("merge manifest does not contain 47 new sources")
    if sum(
        row["integration_status"] == "provisional_source_log_reuse_existing"
        for row in merge_rows
    ) != 2:
        raise ValueError("merge manifest does not contain two reused sources")
    if any(row["relation_or_claim_approved"] != "no" for row in merge_rows + proposal_rows):
        raise ValueError("integration output approved a relation or claim")
    if len({row["review_item_id"] for row in hr030_rows}) != len(hr030_rows):
        raise ValueError("HR-030 review item IDs are not unique")
    for row in hr030_rows:
        expected_id = stable_hr030_id(row["source_id"], row["audit_row_id"])
        if row["review_item_id"] != expected_id:
            raise ValueError(f"unstable HR-030 item ID: {row['review_item_id']}")
        if any(field not in row for field in HUMAN_REVIEW_FIELDS):
            raise ValueError(f"HR-030 row lacks a human field: {row['review_item_id']}")
    required_audits = {
        row["audit_row_id"]
        for row in merge_rows
        if row["metadata_review_required"] == "yes" or row["web_review_required"] == "yes"
    }
    queued_audits = {row["audit_row_id"] for row in hr030_rows}
    if not required_audits <= queued_audits:
        raise ValueError("HR-030 omitted an NW2-F metadata/web review item")
    failed_ids = {
        row["source_id"] for row in merge_rows if row["archive_status"] == "failed"
    }
    queued_failed_ids = {
        row["source_id"] for row in hr030_rows if row["actual_archive_failure"] == "yes"
    }
    if failed_ids != queued_failed_ids:
        raise ValueError("HR-030 actual archive failure coverage mismatch")
    if archive_stats["manifest_complete"] and (
        int(archive_stats["batch_archived"]) + int(archive_stats["batch_failed"]) != 47
    ):
        raise ValueError("complete manifest does not resolve all 47 NW2-H sources")


def render_readme(
    source_stats: dict[str, object],
    archive_stats: dict[str, object], hr030_rows: list[dict[str, str]], protected_count: int
) -> str:
    failed_ids = [
        row["source_id"] for row in hr030_rows if row["actual_archive_failure"] == "yes"
    ]
    archive_summary = (
        f"archived {archive_stats['batch_archived']} / failed {archive_stats['batch_failed']}"
        if archive_stats["manifest_complete"]
        else f"not_in_manifest {archive_stats['batch_not_in_manifest']}（归档命令尚未完成）"
    )
    populated_decisions = sum(bool(row["decision"].strip()) for row in hr030_rows)
    return "\n".join(
        [
            "# Next-wave source integration v1",
            "",
            "日期：2026-07-13",
            "",
            "## 合并结果",
            "",
            "- NW2-F 的 49 个唯一 URL 是本轮唯一权威输入：复用 S158/S204，新增 47 条 S248–S294。",
            f"- 中央 source log 当前为 {source_stats['source_count']} 条；S248–S294 全部保持 `review_status=ai_seeded` 和 proposal-derived 元数据；若存在 S295，它是 HR-011 后续定位补充，不属于 NW2-H 波次。",
            "- S248–S294 只是 provisional source-log index：metadata 尚未经人工认可；archive failed 不撤销 provisional S 号，也不允许把该来源用于正式关系结论。",
            f"- S248–S294 归档状态：{archive_summary}。",
            f"- HR-030：{len(hr030_rows)} 个唯一 URL。去重规则为 `source_id + audit_row_id`；合并 NW2-F 的 11 个 metadata 与 11 个 web/archive 队列（5 个交集），并追加任何实际 archive failure。review item ID 稳定使用该复合键，当前已填写 decision {populated_decisions} 条。",
            f"- 当前实际归档失败：{', '.join(failed_ids) if failed_ids else '无'}。失败状态原样保留、不伪造 artifact，也不阻断 provisional source ID；其 metadata/可用性仍由 HR-030 决定。",
            "- 50 条原始提案仍可经 `proposal_to_source_crosswalk_v1.csv` 追溯；跨批重复 R9EC_S007/RV2SP015 共同映射一个 S 号。",
            "",
            "## 验证边界",
            "",
            f"- source ID 为唯一连续 S001–S{int(source_stats['source_count']):03d}；47 个 NW2-H 新 URL 无任何新旧或批内重复。",
            "- 历史遗留 S022/S024 共用同一 URL，因下游引用不同而原样保留；本轮没有扩大或修改这一既有重复组。",
            f"- {protected_count} 张 actor/alias/edge/role 中央表在脚本运行前后 SHA-256 一致。",
            f"- 已保存 artifact 共核验 {archive_stats['artifact_checked']} 个，manifest SHA 与本地文件一致。",
            "- 中央 source log 在所有内存校验、archive 校验、HR-030 合并和受保护表 SHA 校验完成后，才通过同目录临时文件与 `os.replace` 原子更新；失败注入不得改变原文件。",
            "- 所有 crosswalk 均为 `relation_or_claim_approved=no`。来源入表与归档不批准 actor、edge、联盟、资金、污染/健康因果、罢工合法性、选举效果或组织分类。",
            "",
            "## 文件",
            "",
            "- `source_merge_manifest_v1.csv`：49 个唯一 URL 的最终 S 号与归档状态。",
            "- `proposal_to_source_crosswalk_v1.csv`：50 条输入提案到中央来源的映射。",
            "- `integrated_source_rows_S248_S294_v1.csv`：47 条新增中央来源行的可核副本。",
            "- `HR030_source_metadata_archive_review_v0.csv`：元数据／归档人工复核；既有人审字段按稳定复合键保留。",
            "- `protected_actor_edge_sha_v1.csv`：受保护中央表的运行前后 SHA。",
            "- `validation_report_v1.md`：机械校验结果。",
            "",
            "## 可重复命令",
            "",
            "```powershell",
            "python scripts\\integrate_next_wave_sources_v1.py",
            "python scripts\\archive_sources.py --from-id 248 --to-id 294",
            "python scripts\\integrate_next_wave_sources_v1.py",
            "```",
        ]
    )


def render_validation(
    source_stats: dict[str, object],
    archive_stats: dict[str, object],
    hr030_rows: list[dict[str, str]],
    protected_rows: list[dict[str, str]],
) -> str:
    populated_human_rows = sum(
        any(row[field] for field in HUMAN_REVIEW_FIELDS) for row in hr030_rows
    )
    return "\n".join(
        [
            "# NW2-H validation report",
            "",
            f"- central source rows: {source_stats['source_count']}",
            f"- source IDs: unique continuous S001-S{int(source_stats['source_count']):03d}",
            f"- integrated new unique URLs: {source_stats['new_unique_urls']} (S248-S294)",
            "- reused existing URLs: 2 (S158, S204)",
            "- new-to-new or new-to-old normalized URL collisions: 0",
            f"- grandfathered pre-NW2 duplicate URL groups: {source_stats['grandfathered_duplicate_groups']} (S022/S024 only; unchanged)",
            f"- archive manifest rows: {archive_stats['manifest_count']}",
            f"- S248-S294 archived: {archive_stats['batch_archived']}",
            f"- S248-S294 failed: {archive_stats['batch_failed']}",
            f"- S248-S294 not yet in manifest: {archive_stats['batch_not_in_manifest']}",
            f"- preserved artifacts hash-checked: {archive_stats['artifact_checked']}; mismatches: 0",
            f"- HR-030 unique URL rows: {len(hr030_rows)}; stable source/audit IDs: yes; rows with populated human fields preserved: {populated_human_rows}",
            "- central source-log commit: prevalidated temporary CSV + atomic os.replace; no validation occurs after commit",
            "- relation_or_claim_approved: 0 yes / 49 no unique URLs / 50 no proposal rows",
            f"- protected actor/edge tables: {len(protected_rows)}; SHA changes: {sum(row['unchanged'] != 'yes' for row in protected_rows)}",
            "- unauthorized actor/edge/event writes by this integration script: 0",
        ]
    )


def main() -> None:
    protected_before = protected_hashes()
    audit_rows, record_rows = load_authoritative_audit()
    source_rows, candidates, added = prepare_source_log(audit_rows)
    source_stats = validate_source_log(source_rows, audit_rows, candidates)
    if os.environ.get("NW2H_FAIL_AFTER_SOURCE_VALIDATION") == "1":
        raise RuntimeError("injected failure after in-memory source-log validation")

    manifest_by_id, manifest_rows = load_manifest()
    archive_stats = validate_archives(source_rows, manifest_by_id, manifest_rows)
    source_by_id = {row["source_id"]: row for row in source_rows}
    _, metadata_rows = read_csv(METADATA_REVIEW)
    _, web_rows = read_csv(WEB_REVIEW)
    metadata_by_audit = {row["audit_row_id"]: row for row in metadata_rows}
    web_by_audit = {row["audit_row_id"]: row for row in web_rows}
    if len(metadata_by_audit) != 11 or len(web_by_audit) != 11:
        raise ValueError("NW2-F review queue counts changed")

    generated_hr030_rows = build_hr030(
        audit_rows,
        source_by_id,
        manifest_by_id,
        metadata_by_audit,
        web_by_audit,
    )
    _, existing_hr030_rows = read_csv(HR030) if HR030.exists() else (HR030_FIELDS, [])
    hr030_rows = merge_hr030_human_fields(generated_hr030_rows, existing_hr030_rows)
    merge_rows, proposal_rows = build_outputs(
        audit_rows, record_rows, source_rows, manifest_by_id, hr030_rows
    )
    validate_outputs(merge_rows, proposal_rows, hr030_rows, archive_stats)

    protected_after = protected_hashes()
    protected_rows = [
        {
            "path": path,
            "sha256_before_run": protected_before[path],
            "sha256_after_run": protected_after[path],
            "unchanged": "yes" if protected_before[path] == protected_after[path] else "no",
        }
        for path in protected_before
    ]
    if any(row["unchanged"] != "yes" for row in protected_rows):
        raise RuntimeError("an actor/edge protected table changed during NW2-H")

    write_csv(MERGE_MANIFEST, MERGE_FIELDS, merge_rows)
    write_csv(PROPOSAL_CROSSWALK, PROPOSAL_FIELDS, proposal_rows)
    write_csv(NEW_SOURCE_ROWS, SOURCE_FIELDS, candidates)
    write_csv(HR030, HR030_FIELDS, hr030_rows)
    write_csv(PROTECTED_SHA, PROTECTED_FIELDS, protected_rows)
    write_text(README, render_readme(source_stats, archive_stats, hr030_rows, len(protected_rows)))
    write_text(
        VALIDATION,
        render_validation(source_stats, archive_stats, hr030_rows, protected_rows),
    )
    # Central commit is deliberately last.  No validation that can raise is
    # performed after this atomic replacement.
    atomic_write_csv(SOURCE_LOG, SOURCE_FIELDS, source_rows)

    print("# NW2-H controlled source integration")
    print(f"- added this run: {added}; central source rows: {len(source_rows)}")
    print("- reused: S158, S204; integrated: S248-S294")
    print(
        f"- archive batch: archived={archive_stats['batch_archived']} "
        f"failed={archive_stats['batch_failed']} "
        f"not_in_manifest={archive_stats['batch_not_in_manifest']}"
    )
    print(f"- HR-030 unique URL rows: {len(hr030_rows)}")
    print(f"- protected actor/edge SHA unchanged: {len(protected_rows)}/{len(protected_rows)}")
    print(f"- preserved artifact hashes verified: {archive_stats['artifact_checked']}")
    print("- relation_or_claim_approved: all no")


if __name__ == "__main__":
    main()
