"""Audit and crosswalk the NW2-B/NW2-C source proposals without merging them.

This script is deliberately read-only with respect to the central source log,
archive manifest, archive artifacts, and documentation.  It writes only:

* data/interim/37_next_wave_source_proposal_crosswalk_v1.csv
* outputs/next_wave_source_proposal_audit_v1/

Suggested S numbers are ordering aids only.  They are not reservations and do
not authorize source-log insertion, archiving, actors, relations, or claims.
"""

from __future__ import annotations

import csv
import hashlib
import re
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


ROOT = Path(__file__).resolve().parents[1]
R9_PROPOSALS = (
    ROOT
    / "outputs"
    / "R09_election_civic_interface_v1"
    / "source_proposals_v1.csv"
)
REGISTRY_PROPOSALS = (
    ROOT / "outputs" / "registry_value_gate_v2" / "source_proposals_v2.csv"
)
SOURCE_LOG = ROOT / "data" / "interim" / "05_source_log_initial_v0.csv"
ARCHIVE_MANIFEST = (
    ROOT / "source_docs" / "source_archive" / "source_archive_manifest.csv"
)

OUT = ROOT / "outputs" / "next_wave_source_proposal_audit_v1"
INTERIM_CROSSWALK = (
    ROOT / "data" / "interim" / "37_next_wave_source_proposal_crosswalk_v1.csv"
)
OUT_CROSSWALK = OUT / "unique_url_crosswalk_v1.csv"
RECORD_AUDIT = OUT / "proposal_record_audit_v1.csv"
SEQUENCE = OUT / "suggested_new_source_sequence_v1.csv"
TYPE_CROSSWALK = OUT / "source_type_crosswalk_v1.csv"
METADATA_QUEUE = OUT / "metadata_review_queue_v1.csv"
WEB_QUEUE = OUT / "web_archive_review_queue_v1.csv"
BOUNDARY_AUDIT = OUT / "sensitive_claim_boundary_audit_v1.csv"
README = OUT / "README.md"
VALIDATION = OUT / "validation_report_v1.md"


TRACKING_QUERY_PREFIXES = ("utm_",)
TRACKING_QUERY_KEYS = {"fbclid", "gclid", "mc_cid", "mc_eid"}
NW2H_MARKER = "NW2-H controlled source integration 2026-07-13"

# Existing central vocabulary is deliberately reused where a mechanical map is
# safe.  Three heterogeneous formats retain a human-choice flag below.
TYPE_MAP = {
    "academic_participant_record": "academic_article",
    "academic_presentation_material": "academic_article",
    "broadcast_news": "news",
    "event_report": "event_report",
    "local_broadcast_news": "local_news",
    "local_chronology": "community_site",
    "local_news": "local_news",
    "magazine_news": "magazine_news",
    "municipal_legislative_record": "official_legislative_record",
    "municipal_official_response": "local_official",
    "municipal_resolution": "official_legislative_record",
    "national_news": "news",
    "official_election_record": "official_data",
    "official_labor_decision": "legal_source",
    "official_parliamentary_record": "official_legislative_record",
    "organization_campaign_statement": "organization_statement",
    "organization_event_record": "organization_event_record",
    "organization_event_report": "organization_action_record",
    "organization_issue_page": "organization_site",
    "organization_newsletter": "organization_report",
    "organization_policy_document": "organization_program_document",
    "organization_request": "organization_statement",
    "organization_statement": "organization_statement",
    "organization_website": "organization_website",
    "participant_account": "community_site",
    "party_media": "party_news",
    "party_news": "party_news",
    "prefectural_administrative_record": "prefectural_official",
    "prefectural_labor_record": "prefectural_official",
    "union_activity_report": "organization_report",
}

TYPE_HUMAN_CHOICE = {
    "participant_account": (
        "Proposed community_site, but retain first-person participant provenance "
        "in bias_note/notes."
    ),
    "local_chronology": (
        "Proposed community_site; confirm whether the entry reproduces a local-"
        "newspaper item before freezing type/date."
    ),
    "academic_presentation_material": (
        "Proposed academic_article only for vocabulary compatibility; a dedicated "
        "presentation-material type may be preferable."
    ),
}

# Curated exception audit.  These are metadata decisions, not evidence or claim
# decisions.  The rules make the audit reproducible and keep ordinary dated
# HTML locators out of an inflated review queue.
EXPLICIT_METADATA_ISSUES = {
    "R9EC_S006": ["source_type_human_choice"],
    "RV2SP001": ["existing_source_metadata_diff"],
    "RV2SP002": [
        "existing_source_metadata_diff",
        "activity_range_vs_access_year",
        "locator_is_broad_index",
    ],
    "RV2SP003": ["publication_date_unavailable_access_date_only"],
    "RV2SP005": ["pdf_locator_needs_page_pinpoint"],
    "RV2SP007": ["hearing_date_vs_report_date_choose_source_log_year"],
    "RV2SP014": ["publication_date_unavailable_access_date_only"],
    "RV2SP020": [
        "rolling_record_range_vs_access_year",
        "locator_needs_named_entry_or_snapshot_date",
    ],
    "RV2SP025": [
        "source_type_human_choice",
        "archive_path_date_alignment_needs_confirmation",
    ],
    "RV2SP029": [
        "source_type_human_choice",
        "undated_attachment_use_access_year_only",
    ],
}

YEAR_OVERRIDE = {
    "RV2SP003": "2026",
    "RV2SP007": "2023",
    "RV2SP014": "2026",
    "RV2SP020": "2026",
    "RV2SP029": "2026",
}

WEB_REVIEW_FLAGS = {
    "R9EC_S012": ["verify_pdf_content_type_for_extensionless_jstage_endpoint"],
    "R9EC_S018": ["verify_accessible_text_and_paywall_boundary"],
    "RV2SP003": ["snapshot_current_page_and_record_access_date"],
    "RV2SP009": ["preserve_visible_locator_under_paywall_boundary"],
    "RV2SP012": ["verify_dynamic_query_page_and_final_url"],
    "RV2SP014": ["snapshot_current_page_and_record_access_date"],
    "RV2SP017": ["domain_archive_history_has_material_failure_share"],
    "RV2SP020": [
        "snapshot_rolling_official_page",
        "domain_archive_history_has_material_failure_share",
    ],
    "RV2SP023": ["verify_dynamic_query_page_and_final_url"],
    "RV2SP025": ["verify_unusual_archive_path_against_displayed_event_date"],
    "RV2SP029": ["verify_attachment_date_and_parent_presentation_metadata"],
}

R9_REQUIRED = [
    "proposal_id",
    "title",
    "url",
    "publisher",
    "source_type",
    "publication_or_record_date",
    "locator",
    "support_scope",
    "suggested_evidence_level",
    "source_log_state",
    "relation_or_claim_approved",
    "caveat",
]

REGISTRY_REQUIRED = [
    "proposal_id",
    "candidate_id",
    "title",
    "url",
    "publisher",
    "source_type",
    "publication_or_record_date",
    "locator",
    "support_scope",
    "suggested_evidence_level",
    "source_log_match",
    "relation_or_claim_approved",
    "caveat",
]

CROSSWALK_FIELDS = [
    "audit_row_id",
    "normalized_url",
    "input_record_count",
    "input_batches",
    "proposal_refs",
    "candidate_refs",
    "original_urls",
    "merge_disposition",
    "cross_batch_duplicate",
    "current_source_match",
    "current_source_ids",
    "current_archive_status",
    "suggested_source_id_if_merged",
    "suggested_id_status",
    "snapshot_state",
    "source_log_observed_count",
    "provisional_merged_source_ids",
    "provisional_archive_status",
    "proposed_title",
    "publisher_labels",
    "input_source_types",
    "suggested_source_type",
    "source_type_status",
    "publication_or_record_dates",
    "suggested_year",
    "date_status",
    "locators",
    "locator_status",
    "support_scopes",
    "input_evidence_levels",
    "suggested_evidence_level",
    "caveats",
    "sensitive_boundary_tags",
    "sensitive_boundary_status",
    "relation_or_claim_approved",
    "archive_eligibility",
    "archive_access_risk",
    "metadata_issue_codes",
    "human_metadata_review_required",
    "web_review_required",
    "recommended_action",
]

RECORD_FIELDS = [
    "record_audit_id",
    "input_batch",
    "proposal_id",
    "candidate_id",
    "normalized_url",
    "url_group_id",
    "cross_batch_duplicate",
    "current_source_ids",
    "merge_disposition",
    "suggested_source_id_if_merged",
    "snapshot_state",
    "provisional_merged_source_ids",
    "title",
    "publisher",
    "input_source_type",
    "suggested_source_type",
    "publication_or_record_date",
    "suggested_year",
    "locator",
    "support_scope",
    "suggested_evidence_level",
    "input_approval_field",
    "relation_or_claim_approved",
    "caveat",
    "metadata_issue_codes",
    "web_review_flags",
]

SEQUENCE_FIELDS = [
    "sequence_rank",
    "suggested_source_id_if_merged",
    "numbering_status",
    "machine_provisional_status",
    "claim_approval_requirement",
    "snapshot_state",
    "provisional_merged_source_id",
    "audit_row_id",
    "proposal_refs",
    "normalized_url",
    "proposed_title",
    "suggested_source_type",
    "suggested_year",
    "archive_prerequisite",
    "relation_or_claim_approved",
]

TYPE_FIELDS = [
    "input_source_type",
    "record_count",
    "already_in_current_vocabulary",
    "suggested_source_type",
    "normalization_status",
    "human_review_note",
]

QUEUE_FIELDS = [
    "queue_id",
    "audit_row_id",
    "suggested_source_id_if_merged",
    "proposal_refs",
    "normalized_url",
    "issue_codes",
    "review_question",
    "relation_or_claim_approved",
]

BOUNDARY_FIELDS = [
    "audit_row_id",
    "proposal_refs",
    "normalized_url",
    "sensitive_boundary_tags",
    "caveats",
    "boundary_status",
    "relation_or_claim_approved",
    "safe_use_instruction",
]


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


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalize_url(value: str) -> str:
    """Conservatively normalize URL identity for proposal deduplication."""
    raw = (value or "").strip()
    parts = urlsplit(raw)
    if parts.scheme.lower() not in {"http", "https"} or not parts.hostname:
        raise ValueError(f"not an archive-eligible HTTP(S) URL: {value}")
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
    query_items = [
        (key, value)
        for key, value in parse_qsl(parts.query, keep_blank_values=True)
        if key.lower() not in TRACKING_QUERY_KEYS
        and not key.lower().startswith(TRACKING_QUERY_PREFIXES)
    ]
    query = urlencode(sorted(query_items))
    return urlunsplit((scheme, netloc, path, query, ""))


def is_http_url(value: str) -> bool:
    parts = urlsplit((value or "").strip())
    return parts.scheme.lower() in {"http", "https"} and bool(parts.hostname)


def unique(values: list[str]) -> list[str]:
    return list(dict.fromkeys(value.strip() for value in values if value and value.strip()))


def joined(values: list[str], separator: str = ";") -> str:
    return separator.join(unique(values))


def first_year(value: str, title: str = "") -> str:
    for text in (value or "", title or ""):
        match = re.search(r"(?:19|20)\d{2}", text)
        if match:
            return match.group(0)
    return "undated"


def evidence_max(values: list[str]) -> str:
    order = {"E0": 0, "E1": 1, "E2": 2, "E3": 3, "E4": 4}
    clean = unique(values)
    if not clean:
        return ""
    return max(clean, key=lambda value: order.get(value, -1))


def ensure_schema(actual: list[str], expected: list[str], label: str) -> None:
    if actual != expected:
        raise ValueError(f"{label} schema changed: {actual}")


def sensitive_tags(record: dict[str, str]) -> list[str]:
    proposal_id = record["proposal_id"]
    if record["input_batch"] == "NW2-B_R09":
        tags = ["election_causality_not_inferred"]
        if proposal_id in {"R9EC_S002"}:
            tags.append("actor_crosswalk_requires_human_review")
        if proposal_id in {
            "R9EC_S003",
            "R9EC_S004",
            "R9EC_S005",
            "R9EC_S015",
            "R9EC_S021",
        }:
            tags.append("ad_hoc_body_or_roster_not_generalized")
        if proposal_id in {"R9EC_S006", "R9EC_S012", "R9EC_S020"}:
            tags.append("person_or_masked_actor_not_transferred")
        if proposal_id in {
            "R9EC_S007",
            "R9EC_S013",
            "R9EC_S016",
            "R9EC_S019",
        }:
            tags.append("self_report_reach_or_effect_not_inferred")
        if proposal_id in {
            "R9EC_S009",
            "R9EC_S010",
            "R9EC_S017",
            "R9EC_S018",
        }:
            tags.append("issue_event_not_automatic_endorsement")
        if proposal_id == "R9EC_S011":
            tags.append("temporary_coalition_not_stable_alliance")
        return tags

    candidate_id = record["candidate_id"]
    if candidate_id == "RV2C001":
        return [
            "stated_environmental_risk_not_proven_contamination",
            "administrative_contact_not_agreement",
        ]
    if candidate_id == "RV2C002":
        return [
            "PFAS_health_or_source_causality_not_inferred",
            "request_or_coparticipation_not_partnership",
        ]
    if candidate_id == "RV2C003":
        return [
            "branch_parent_action_not_automatically_transferred",
            "party_affiliation_not_inferred",
        ]
    if candidate_id == "RV2C004":
        return [
            "strike_legality_or_effect_not_adjudicated",
            "common_event_not_stable_alliance",
        ]
    if candidate_id == "RV2C005":
        return [
            "component_or_coorganization_not_stable_alliance",
            "historical_continuity_not_inferred",
        ]
    raise ValueError(f"unmapped candidate for sensitive boundary: {candidate_id}")


def collect_records() -> list[dict[str, str]]:
    r9_fields, r9_rows = read_csv(R9_PROPOSALS)
    registry_fields, registry_rows = read_csv(REGISTRY_PROPOSALS)
    ensure_schema(r9_fields, R9_REQUIRED, "NW2-B R09 proposals")
    ensure_schema(registry_fields, REGISTRY_REQUIRED, "NW2-C registry proposals")
    if len(r9_rows) != 21 or len(registry_rows) != 29:
        raise ValueError(
            f"input coverage changed: R09={len(r9_rows)}, registry={len(registry_rows)}"
        )

    records: list[dict[str, str]] = []
    for batch_order, (batch, rows) in enumerate(
        [("NW2-B_R09", r9_rows), ("NW2-C_registry_gate", registry_rows)]
    ):
        for input_order, source in enumerate(rows, start=1):
            approval_field = "relation_or_claim_approved"
            approval = source[approval_field].strip().lower()
            if approval != "no":
                raise ValueError(
                    f"{source['proposal_id']}: approval must remain no, got {approval!r}"
                )
            required_nonempty = [
                "proposal_id",
                "title",
                "url",
                "publisher",
                "source_type",
                "publication_or_record_date",
                "locator",
                "support_scope",
                "suggested_evidence_level",
                "caveat",
            ]
            missing = [field for field in required_nonempty if not source[field].strip()]
            if missing:
                raise ValueError(f"{source['proposal_id']}: missing fields {missing}")
            source_type = source["source_type"].strip()
            if source_type not in TYPE_MAP:
                raise ValueError(
                    f"{source['proposal_id']}: unmapped input source type {source_type}"
                )
            record = {
                "input_batch": batch,
                "batch_order": str(batch_order),
                "input_order": str(input_order),
                "proposal_id": source["proposal_id"].strip(),
                "candidate_id": source.get("candidate_id", "").strip(),
                "title": source["title"].strip(),
                "url": source["url"].strip(),
                "publisher": source["publisher"].strip(),
                "source_type": source_type,
                "suggested_source_type": TYPE_MAP[source_type],
                "publication_or_record_date": source[
                    "publication_or_record_date"
                ].strip(),
                "locator": source["locator"].strip(),
                "support_scope": source["support_scope"].strip(),
                "suggested_evidence_level": source[
                    "suggested_evidence_level"
                ].strip(),
                "declared_source_log_match": source.get(
                    "source_log_match", ""
                ).strip(),
                "input_approval_field": approval_field,
                "relation_or_claim_approved": "no",
                "caveat": source["caveat"].strip(),
            }
            record["normalized_url"] = normalize_url(record["url"])
            record["metadata_issue_codes"] = joined(
                EXPLICIT_METADATA_ISSUES.get(record["proposal_id"], [])
            )
            record["web_review_flags"] = joined(
                WEB_REVIEW_FLAGS.get(record["proposal_id"], [])
            )
            record["sensitive_boundary_tags"] = joined(sensitive_tags(record))
            records.append(record)
    return records


def classify_date(records: list[dict[str, str]], existing: bool) -> str:
    values = " | ".join(record["publication_or_record_date"] for record in records).lower()
    if existing:
        return "reuse_existing_year_review_proposal_period"
    if "undated" in values:
        return "undated_access_year_proposed"
    if "current page" in values:
        return "access_date_only"
    if "hearings" in values and "report dated" in values:
        return "multiple_record_dates"
    if "records" in values or "activity archive" in values:
        return "rolling_or_range_record"
    if " to " in values:
        return "bounded_event_date_range"
    if all(re.search(r"(?:19|20)\d{2}", value) for value in values.split(" | ")):
        return "complete_year_or_date"
    return "needs_review"


def choose_year(records: list[dict[str, str]], current_rows: list[dict[str, str]]) -> str:
    if current_rows:
        return current_rows[0]["year"].strip()
    for record in records:
        override = YEAR_OVERRIDE.get(record["proposal_id"])
        if override:
            return override
    return first_year(records[0]["publication_or_record_date"], records[0]["title"])


def build() -> tuple[
    list[dict[str, str]],
    list[dict[str, str]],
    list[dict[str, str]],
    list[dict[str, str]],
    list[dict[str, str]],
    list[dict[str, str]],
    list[dict[str, str]],
    dict[str, int],
]:
    records = collect_records()
    _, source_rows = read_csv(SOURCE_LOG)
    _, manifest_rows = read_csv(ARCHIVE_MANIFEST)
    if len(source_rows) not in {247, 294, 295}:
        raise ValueError(
            f"expected pre-merge 247, post-NW2-H 294, or current 295 sources, got {len(source_rows)}"
        )

    baseline_rows = [row for row in source_rows if int(row["source_id"][1:]) <= 247]
    provisional_rows = [row for row in source_rows if 248 <= int(row["source_id"][1:]) <= 294]
    supplemental_rows = [row for row in source_rows if int(row["source_id"][1:]) > 294]
    if len(baseline_rows) != 247:
        raise ValueError("historical S001-S247 source baseline is incomplete")
    if provisional_rows:
        expected_provisional_ids = [f"S{number:03d}" for number in range(248, 295)]
        if [row["source_id"] for row in provisional_rows] != expected_provisional_ids:
            raise ValueError("post-merge overlay is not the expected S248-S294 range")
        if any(NW2H_MARKER not in row["notes"] for row in provisional_rows):
            raise ValueError("S248-S294 contains a row outside the NW2-H provisional batch")
    if [row["source_id"] for row in supplemental_rows] not in ([], ["S295"]):
        raise ValueError("unexpected post-NW2-H supplemental source range")

    current_ids = [row["source_id"] for row in baseline_rows]
    numeric_ids = sorted(
        int(match.group(1))
        for source_id in current_ids
        if (match := re.fullmatch(r"S(\d+)", source_id))
    )
    if len(numeric_ids) != len(baseline_rows) or numeric_ids != list(range(1, 248)):
        raise ValueError("central source IDs are not the expected S001-S247 baseline")

    current_by_url: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in baseline_rows:
        # The 247-row source log intentionally contains two bibliographic
        # ``book_reference`` rows.  They are part of the baseline but cannot
        # collide with this batch's HTTP(S)-only proposals.
        if is_http_url(row["url"]):
            current_by_url[normalize_url(row["url"])].append(row)
    provisional_by_url: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in provisional_rows:
        provisional_by_url[normalize_url(row["url"])].append(row)
    manifest_by_id = {row["source_id"]: row for row in manifest_rows}

    domain_archive: dict[str, Counter[str]] = defaultdict(Counter)
    for row in manifest_rows:
        # Preserve the NW2-F risk snapshot.  S248-S294 archive outcomes are a
        # later overlay and must not retroactively change the original queue.
        if int(row["source_id"][1:]) > 247:
            continue
        hostname = (urlsplit(row["url"]).hostname or "").lower()
        if hostname:
            domain_archive[hostname][row["archive_status"]] += 1

    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    group_order: list[str] = []
    for record in records:
        normalized = record["normalized_url"]
        if normalized not in grouped:
            group_order.append(normalized)
        grouped[normalized].append(record)

    crosswalk: list[dict[str, str]] = []
    new_rows: list[dict[str, str]] = []
    for index, normalized in enumerate(group_order, start=1):
        group = grouped[normalized]
        current = current_by_url.get(normalized, [])
        batches = unique([record["input_batch"] for record in group])
        cross_batch = len(batches) > 1
        if current:
            merge_disposition = "reuse_existing_source"
        elif cross_batch:
            merge_disposition = "cross_batch_duplicate_proposed_new"
        else:
            merge_disposition = "unique_proposed_new"

        metadata_issues = unique(
            [
                code
                for record in group
                for code in record["metadata_issue_codes"].split(";")
                if code
            ]
        )
        if cross_batch:
            if len(unique([record["title"] for record in group])) > 1:
                metadata_issues.append("cross_batch_title_variant")
            if len(unique([record["publisher"] for record in group])) > 1:
                metadata_issues.append("cross_batch_publisher_label_variant")
        metadata_issues = unique(metadata_issues)

        input_types = unique([record["source_type"] for record in group])
        suggested_types = unique([record["suggested_source_type"] for record in group])
        human_type = any(source_type in TYPE_HUMAN_CHOICE for source_type in input_types)
        if len(suggested_types) > 1:
            metadata_issues.append("cross_record_source_type_conflict")
            source_type_status = "human_choice_required"
        elif human_type:
            source_type_status = "human_choice_required"
        elif input_types == suggested_types:
            source_type_status = "already_in_current_vocabulary"
        else:
            source_type_status = "mechanical_vocabulary_normalization"

        if current:
            central_titles = unique([row["title"] for row in current])
            central_types = unique([row["source_type"] for row in current])
            if set(central_titles) != set(unique([record["title"] for record in group])):
                metadata_issues.append("existing_title_diff_preserve_current")
            if set(central_types) != set(suggested_types):
                metadata_issues.append("existing_type_diff_preserve_current")
            proposed_title = current[0]["title"]
            suggested_type = current[0]["source_type"]
        else:
            proposed_title = group[0]["title"]
            suggested_type = suggested_types[0] if len(suggested_types) == 1 else joined(suggested_types)

        web_flags = unique(
            [
                flag
                for record in group
                for flag in record["web_review_flags"].split(";")
                if flag
            ]
        )
        hostname = (urlsplit(normalized).hostname or "").lower()
        domain_counts = domain_archive.get(hostname, Counter())
        domain_total = sum(domain_counts.values())
        domain_failed = domain_counts.get("failed", 0)
        if domain_total and domain_failed / domain_total >= 0.20:
            if "domain_archive_history_has_material_failure_share" not in web_flags:
                web_flags.append("domain_archive_history_has_material_failure_share")

        archive_statuses = unique(
            [
                manifest_by_id[row["source_id"]]["archive_status"]
                for row in current
                if row["source_id"] in manifest_by_id
            ]
        )
        if current:
            archive_eligibility = "already_registered_reuse_existing_archive"
            archive_access_risk = joined(archive_statuses) or "manifest_missing"
        else:
            archive_eligibility = "eligible_http_archive;provisional_index_does_not_require_success"
            if web_flags:
                archive_access_risk = joined(web_flags)
            elif domain_total:
                archive_access_risk = (
                    f"no_specific_flag;domain_history="
                    f"{domain_counts.get('archived', 0)}_archived_"
                    f"{domain_failed}_failed"
                )
            else:
                archive_access_risk = "no_specific_flag;domain_not_yet_in_manifest"

        sensitive = unique(
            [
                tag
                for record in group
                for tag in record["sensitive_boundary_tags"].split(";")
                if tag
            ]
        )
        caveats = unique([record["caveat"] for record in group])
        locator_status = (
            "needs_pinpoint"
            if any(
                code in metadata_issues
                for code in {
                    "pdf_locator_needs_page_pinpoint",
                    "locator_is_broad_index",
                    "locator_needs_named_entry_or_snapshot_date",
                }
            )
            else "complete"
        )
        current_source_ids = joined([row["source_id"] for row in current])
        current_archive_status = joined(archive_statuses) if current else "not_applicable"

        row = {
            "audit_row_id": f"NW2FS{index:03d}",
            "normalized_url": normalized,
            "input_record_count": str(len(group)),
            "input_batches": joined(batches),
            "proposal_refs": joined(
                [f"{record['input_batch']}:{record['proposal_id']}" for record in group]
            ),
            "candidate_refs": joined([record["candidate_id"] for record in group]),
            "original_urls": joined([record["url"] for record in group]),
            "merge_disposition": merge_disposition,
            "cross_batch_duplicate": "yes" if cross_batch else "no",
            "current_source_match": "yes" if current else "no",
            "current_source_ids": current_source_ids,
            "current_archive_status": current_archive_status,
            "suggested_source_id_if_merged": "",
            "suggested_id_status": (
                "not_applicable_reuse_existing"
                if current
                else "proposal_only_not_reserved"
            ),
            "snapshot_state": (
                "postmerge_reuse_existing"
                if current and provisional_rows
                else "premerge_reuse_existing"
                if current
                else "pending_provisional_overlay_check"
            ),
            "source_log_observed_count": str(len(source_rows)),
            "provisional_merged_source_ids": "",
            "provisional_archive_status": "not_applicable",
            "proposed_title": proposed_title,
            "publisher_labels": joined([record["publisher"] for record in group]),
            "input_source_types": joined(input_types),
            "suggested_source_type": suggested_type,
            "source_type_status": source_type_status,
            "publication_or_record_dates": joined(
                [record["publication_or_record_date"] for record in group], " | "
            ),
            "suggested_year": choose_year(group, current),
            "date_status": classify_date(group, bool(current)),
            "locators": joined([record["locator"] for record in group], " | "),
            "locator_status": locator_status,
            "support_scopes": joined([record["support_scope"] for record in group], " | "),
            "input_evidence_levels": joined(
                [record["suggested_evidence_level"] for record in group]
            ),
            "suggested_evidence_level": evidence_max(
                [record["suggested_evidence_level"] for record in group]
            ),
            "caveats": joined(caveats, " | "),
            "sensitive_boundary_tags": joined(sensitive),
            "sensitive_boundary_status": "pass_no_approval_and_caveat_present",
            "relation_or_claim_approved": "no",
            "archive_eligibility": archive_eligibility,
            "archive_access_risk": archive_access_risk,
            "metadata_issue_codes": joined(metadata_issues),
            "human_metadata_review_required": "yes" if metadata_issues else "no",
            "web_review_required": "yes" if web_flags else "no",
            "recommended_action": (
                "reuse existing source ID; human-review support-scope enrichment only"
                if current
                else "provisional source indexing may proceed; complete metadata/archive review before formal claim use"
            ),
        }
        crosswalk.append(row)
        if not current:
            new_rows.append(row)

    next_source_number = 248
    for offset, row in enumerate(new_rows):
        row["suggested_source_id_if_merged"] = f"S{next_source_number + offset:03d}"
        overlay = provisional_by_url.get(row["normalized_url"], [])
        if provisional_rows:
            if len(overlay) != 1:
                raise ValueError(
                    f"{row['audit_row_id']}: expected one provisional NW2-H overlay row"
                )
            if overlay[0]["source_id"] != row["suggested_source_id_if_merged"]:
                raise ValueError(
                    f"{row['audit_row_id']}: historical suggested ID does not match NW2-H overlay"
                )
            row["snapshot_state"] = "postmerge_provisional_batch_match"
            row["provisional_merged_source_ids"] = overlay[0]["source_id"]
            manifest = manifest_by_id.get(overlay[0]["source_id"], {})
            row["provisional_archive_status"] = manifest.get(
                "archive_status", "not_in_manifest"
            )
            row["recommended_action"] = (
                "provisional source-log merge observed; retain ai_seeded status and "
                "complete HR-030 metadata/archive review before formal claim use"
            )
        else:
            if overlay:
                raise ValueError("pre-merge snapshot unexpectedly has a provisional overlay")
            row["snapshot_state"] = "premerge_proposed_new"

    group_by_url = {row["normalized_url"]: row for row in crosswalk}
    record_audit: list[dict[str, str]] = []
    for index, record in enumerate(records, start=1):
        group_row = group_by_url[record["normalized_url"]]
        record_audit.append(
            {
                "record_audit_id": f"NW2FR{index:03d}",
                "input_batch": record["input_batch"],
                "proposal_id": record["proposal_id"],
                "candidate_id": record["candidate_id"],
                "normalized_url": record["normalized_url"],
                "url_group_id": group_row["audit_row_id"],
                "cross_batch_duplicate": group_row["cross_batch_duplicate"],
                "current_source_ids": group_row["current_source_ids"],
                "merge_disposition": group_row["merge_disposition"],
                "suggested_source_id_if_merged": group_row[
                    "suggested_source_id_if_merged"
                ],
                "snapshot_state": group_row["snapshot_state"],
                "provisional_merged_source_ids": group_row[
                    "provisional_merged_source_ids"
                ],
                "title": record["title"],
                "publisher": record["publisher"],
                "input_source_type": record["source_type"],
                "suggested_source_type": record["suggested_source_type"],
                "publication_or_record_date": record["publication_or_record_date"],
                "suggested_year": YEAR_OVERRIDE.get(
                    record["proposal_id"],
                    first_year(record["publication_or_record_date"], record["title"]),
                ),
                "locator": record["locator"],
                "support_scope": record["support_scope"],
                "suggested_evidence_level": record["suggested_evidence_level"],
                "input_approval_field": record["input_approval_field"],
                "relation_or_claim_approved": "no",
                "caveat": record["caveat"],
                "metadata_issue_codes": record["metadata_issue_codes"],
                "web_review_flags": record["web_review_flags"],
            }
        )

    sequence = [
        {
            "sequence_rank": str(index),
            "suggested_source_id_if_merged": row["suggested_source_id_if_merged"],
            "numbering_status": "historical_proposal_sequence",
            "machine_provisional_status": (
                "provisionally_indexed_in_source_log"
                if row["snapshot_state"] == "postmerge_provisional_batch_match"
                else "machine_proposal_not_yet_indexed"
            ),
            "claim_approval_requirement": (
                "no_human_claim_approval_required_for_provisional_indexing;claims_remain_unapproved"
            ),
            "snapshot_state": row["snapshot_state"],
            "provisional_merged_source_id": row["provisional_merged_source_ids"],
            "audit_row_id": row["audit_row_id"],
            "proposal_refs": row["proposal_refs"],
            "normalized_url": row["normalized_url"],
            "proposed_title": row["proposed_title"],
            "suggested_source_type": row["suggested_source_type"],
            "suggested_year": row["suggested_year"],
            "archive_prerequisite": "archive_and_metadata_review_before_formal_claim_use",
            "relation_or_claim_approved": "no",
        }
        for index, row in enumerate(new_rows, start=1)
    ]

    current_type_vocab = {row["source_type"] for row in source_rows}
    type_counts = Counter(record["source_type"] for record in records)
    type_rows = []
    for input_type in sorted(type_counts):
        human_note = TYPE_HUMAN_CHOICE.get(input_type, "")
        suggested = TYPE_MAP[input_type]
        if human_note:
            status = "human_choice_required"
        elif input_type == suggested and input_type in current_type_vocab:
            status = "already_in_current_vocabulary"
        else:
            status = "mechanical_vocabulary_normalization"
        type_rows.append(
            {
                "input_source_type": input_type,
                "record_count": str(type_counts[input_type]),
                "already_in_current_vocabulary": (
                    "yes" if input_type in current_type_vocab else "no"
                ),
                "suggested_source_type": suggested,
                "normalization_status": status,
                "human_review_note": human_note,
            }
        )

    metadata_queue = []
    for index, row in enumerate(
        [row for row in crosswalk if row["human_metadata_review_required"] == "yes"],
        start=1,
    ):
        metadata_queue.append(
            {
                "queue_id": f"NW2FM{index:03d}",
                "audit_row_id": row["audit_row_id"],
                "suggested_source_id_if_merged": row[
                    "suggested_source_id_if_merged"
                ],
                "proposal_refs": row["proposal_refs"],
                "normalized_url": row["normalized_url"],
                "issue_codes": row["metadata_issue_codes"],
                "review_question": (
                    "Confirm canonical title/publisher/type/year/locator as flagged; "
                    "for existing matches preserve the current S row unless a deliberate "
                    "metadata revision is approved."
                ),
                "relation_or_claim_approved": "no",
            }
        )

    web_queue = []
    for index, row in enumerate(
        [row for row in crosswalk if row["web_review_required"] == "yes"],
        start=1,
    ):
        web_queue.append(
            {
                "queue_id": f"NW2FW{index:03d}",
                "audit_row_id": row["audit_row_id"],
                "suggested_source_id_if_merged": row[
                    "suggested_source_id_if_merged"
                ],
                "proposal_refs": row["proposal_refs"],
                "normalized_url": row["normalized_url"],
                "issue_codes": row["archive_access_risk"],
                "review_question": (
                    "Open/fetch the final URL, confirm displayed title/date/locator and "
                    "content type, and record the archive outcome. A failed archive may "
                    "retain a provisional S ID but cannot support formal claim use."
                ),
                "relation_or_claim_approved": "no",
            }
        )

    boundary_rows = [
        {
            "audit_row_id": row["audit_row_id"],
            "proposal_refs": row["proposal_refs"],
            "normalized_url": row["normalized_url"],
            "sensitive_boundary_tags": row["sensitive_boundary_tags"],
            "caveats": row["caveats"],
            "boundary_status": row["sensitive_boundary_status"],
            "relation_or_claim_approved": "no",
            "safe_use_instruction": (
                "Source inclusion may support only the bounded metadata/observation after "
                "claim-level review; it does not approve an actor, relation, alliance, "
                "funding flow, causal effect, legal conclusion, or electoral effect."
            ),
        }
        for row in crosswalk
    ]

    counts = {
        "input_records": len(records),
        "r9_records": sum(record["input_batch"] == "NW2-B_R09" for record in records),
        "registry_records": sum(
            record["input_batch"] == "NW2-C_registry_gate" for record in records
        ),
        "unique_urls": len(crosswalk),
        "cross_batch_duplicates": sum(
            row["cross_batch_duplicate"] == "yes" for row in crosswalk
        ),
        "existing_urls": sum(row["current_source_match"] == "yes" for row in crosswalk),
        "new_urls": len(new_rows),
        "source_log_observed_count": len(source_rows),
        "provisional_batch_matches": sum(
            row["snapshot_state"] == "postmerge_provisional_batch_match"
            for row in crosswalk
        ),
        "metadata_issue_urls": len(metadata_queue),
        "web_review_urls": len(web_queue),
        "type_human_choice_categories": sum(
            row["normalization_status"] == "human_choice_required" for row in type_rows
        ),
        "type_mechanical_categories": sum(
            row["normalization_status"] == "mechanical_vocabulary_normalization"
            for row in type_rows
        ),
    }
    return (
        crosswalk,
        record_audit,
        sequence,
        type_rows,
        metadata_queue,
        web_queue,
        boundary_rows,
        counts,
    )


def validate(
    crosswalk: list[dict[str, str]],
    records: list[dict[str, str]],
    sequence: list[dict[str, str]],
    metadata_queue: list[dict[str, str]],
    web_queue: list[dict[str, str]],
    boundaries: list[dict[str, str]],
    counts: dict[str, int],
) -> None:
    expected_counts = {
        "input_records": 50,
        "r9_records": 21,
        "registry_records": 29,
        "unique_urls": 49,
        "cross_batch_duplicates": 1,
        "existing_urls": 2,
        "new_urls": 47,
    }
    for key, expected in expected_counts.items():
        if counts[key] != expected:
            raise ValueError(f"{key}: expected {expected}, got {counts[key]}")
    if len({row["normalized_url"] for row in crosswalk}) != 49:
        raise ValueError("unique URL crosswalk is not unique")
    if len(records) != 50 or len({row["proposal_id"] for row in records}) != 50:
        raise ValueError("proposal-record coverage is incomplete or duplicated")
    if len(boundaries) != 49:
        raise ValueError("sensitive-boundary audit does not cover every unique URL")
    if any(row["relation_or_claim_approved"] != "no" for row in crosswalk):
        raise ValueError("a unique URL row approved a relation or claim")
    if any(row["relation_or_claim_approved"] != "no" for row in records):
        raise ValueError("an input proposal approved a relation or claim")
    if any(row["relation_or_claim_approved"] != "no" for row in boundaries):
        raise ValueError("a boundary row approved a relation or claim")
    if any(not row["caveats"].strip() for row in crosswalk):
        raise ValueError("a unique URL is missing its caveat")
    if any(not row["sensitive_boundary_tags"].strip() for row in crosswalk):
        raise ValueError("a unique URL is missing sensitive-boundary tags")
    existing = [row for row in crosswalk if row["current_source_match"] == "yes"]
    if {row["current_source_ids"] for row in existing} != {"S158", "S204"}:
        raise ValueError("current-source dedup matches changed")
    if any(row["suggested_source_id_if_merged"] for row in existing):
        raise ValueError("existing source match received a suggested new S number")
    expected_sequence = [f"S{number:03d}" for number in range(248, 295)]
    if [row["suggested_source_id_if_merged"] for row in sequence] != expected_sequence:
        raise ValueError("suggested S sequence must be the unreserved S248-S294 ordering")
    if any(row["numbering_status"] != "historical_proposal_sequence" for row in sequence):
        raise ValueError("suggested S sequence lost its historical machine status")
    if any(
        row["claim_approval_requirement"]
        != "no_human_claim_approval_required_for_provisional_indexing;claims_remain_unapproved"
        for row in sequence
    ):
        raise ValueError("provisional indexing was incorrectly made a human claim-approval gate")
    if any(row["relation_or_claim_approved"] != "no" for row in sequence):
        raise ValueError("sequence row approved a relation or claim")
    if counts["source_log_observed_count"] == 247:
        if counts["provisional_batch_matches"] != 0:
            raise ValueError("pre-merge snapshot cannot contain provisional batch matches")
        if any(
            row["snapshot_state"] != "premerge_proposed_new"
            for row in crosswalk
            if row["current_source_match"] == "no"
        ):
            raise ValueError("pre-merge proposed rows have an invalid snapshot state")
        if any(
            row["machine_provisional_status"] != "machine_proposal_not_yet_indexed"
            for row in sequence
        ):
            raise ValueError("pre-merge sequence has an invalid machine provisional status")
    elif counts["source_log_observed_count"] in {294, 295}:
        if counts["provisional_batch_matches"] != 47:
            raise ValueError("post-merge snapshot must recognize all 47 S248-S294 rows")
        if any(
            row["provisional_merged_source_ids"]
            != row["suggested_source_id_if_merged"]
            for row in crosswalk
            if row["current_source_match"] == "no"
        ):
            raise ValueError("post-merge provisional IDs drifted from the audit sequence")
        if any(
            row["machine_provisional_status"] != "provisionally_indexed_in_source_log"
            for row in sequence
        ):
            raise ValueError("post-merge sequence lacks machine provisional status")
    else:
        raise ValueError("unsupported source-log snapshot count")
    if any(
        row["archive_eligibility"]
        != "eligible_http_archive;provisional_index_does_not_require_success"
        for row in crosswalk
        if row["current_source_match"] == "no"
    ):
        raise ValueError("a new URL lacks the provisional-index/archive boundary")
    if len(metadata_queue) != counts["metadata_issue_urls"]:
        raise ValueError("metadata review count mismatch")
    if len(web_queue) != counts["web_review_urls"]:
        raise ValueError("web review count mismatch")
    duplicate = [row for row in crosswalk if row["cross_batch_duplicate"] == "yes"]
    if len(duplicate) != 1 or set(duplicate[0]["proposal_refs"].split(";")) != {
        "NW2-B_R09:R9EC_S007",
        "NW2-C_registry_gate:RV2SP015",
    }:
        raise ValueError("the expected Shinfujin cross-batch duplicate changed")


def render_readme(counts: dict[str, int], sequence: list[dict[str, str]]) -> str:
    first_id = sequence[0]["suggested_source_id_if_merged"]
    last_id = sequence[-1]["suggested_source_id_if_merged"]
    return "\n".join(
        [
            "# Next-wave source proposal audit v1",
            "",
            "日期：2026-07-13",
            "",
            "本包合并审计 NW2-B（R9 election–civic interface）与 NW2-C（registry value gate）的来源提案。它不是中央 source-log merge，也没有下载、归档或批准任何事实关系。",
            "",
            "## 核心结果",
            "",
            f"- 输入：{counts['input_records']} 条（R9 {counts['r9_records']}；registry gate {counts['registry_records']}）。",
            f"- URL 规范化后：{counts['unique_urls']} 个唯一 URL；两批之间有 {counts['cross_batch_duplicates']} 个重复 URL。",
            f"- 相对于历史 S001–S247 基线，既有 URL 为 {counts['existing_urls']} 个，即 S158、S204；都已有 archived artifact。",
            f"- 历史审计判为新候选：{counts['new_urls']} 个唯一 URL；原建议顺序固定为 {first_id}–{last_id}。",
            f"- 当前观察到中央 source log {counts['source_log_observed_count']} 条；其中识别出 {counts['provisional_batch_matches']} 个 NW2-H provisional batch match。即使已合并，历史 `proposal_only_not_reserved` 字段仍只描述合并前审计，不表示 metadata 已获认可。",
            "- provisional source indexing 是机器／来源层状态，不需要人工 claim approval；这不等于任何 claim 获批。49/49 URL 与 50/50 proposal 仍保持 `relation_or_claim_approved=no`。",
            f"- 元数据例外：{counts['metadata_issue_urls']} 个唯一 URL 进入人工队列；没有 title/publisher/URL/type/date/locator/support/caveat 的空字段。",
            f"- Web／归档前复核：{counts['web_review_urls']} 个唯一 URL，原因包括动态页面、付费墙边界、滚动页面、未定年附件或既有域名归档风险。",
            "- 49/49 唯一 URL 均保持 `relation_or_claim_approved=no`；caveat 与敏感边界标签均非空。",
            "",
            "## 唯一重复与既有来源",
            "",
            "- 跨批重复：R9EC_S007 与 RV2SP015 指向同一新日本婦人の会 2014-11-19 声明；只建议一个来源行，两个模块引用并存。",
            "- S158：宮古島地下水研究会 `about_us.html`；复用现有来源，不新增。",
            "- S204：宮古島地下水研究会主页；复用现有来源，不新增。",
            "",
            "## 文件",
            "",
            "- `unique_url_crosswalk_v1.csv`：49 个唯一 URL 的总审计；与 `data/interim/37_next_wave_source_proposal_crosswalk_v1.csv` 字节一致。",
            "- `proposal_record_audit_v1.csv`：保留全部 50 条输入提案及其去重归属。",
            "- `suggested_new_source_sequence_v1.csv`：47 条建议编号顺序；编号未预留。",
            "- `source_type_crosswalk_v1.csv`：输入类型到当前中央词汇的建议映射；三类保留人工选择。",
            "- `metadata_review_queue_v1.csv`：规范化元数据例外。",
            "- `web_archive_review_queue_v1.csv`：打开／归档前需确认的 URL。",
            "- `sensitive_claim_boundary_audit_v1.csv`：49 条敏感解释边界；全部不批准 claim/relation。",
            "- `validation_report_v1.md`：机械校验与中央只读证明。",
            "",
            "## 强制边界",
            "",
            "- S248–S294 的原建议顺序已由 NW2-H 受控 provisional merge 采用；`snapshot_state=postmerge_provisional_batch_match` 明示当前状态。",
            "- source inclusion 不批准 actor 入表、alias、edge、联盟、资金、污染或健康因果、罢工合法性、选举效果或临时动员体的持续性。",
            "- NW2-H 的 provisional source-log merge 不等于 metadata 已审；11 个 metadata 问题仍须 HR-030。archive failed 不撤销 provisional S 号，但该来源不得用于正式关系结论。",
        ]
    )


def render_validation(
    counts: dict[str, int], central_sha_before: str, manifest_sha_before: str
) -> str:
    return "\n".join(
        [
            "# NW2-F validation report",
            "",
            f"- input proposal rows: {counts['input_records']} = 21 R9 + 29 registry gate",
            f"- normalized unique URLs: {counts['unique_urls']}",
            f"- cross-batch duplicate URL groups: {counts['cross_batch_duplicates']}",
            f"- current source-log matches: {counts['existing_urls']} (S158, S204)",
            f"- proposed new unique URLs: {counts['new_urls']}",
            "- suggested source sequence: S248-S294; historical_proposal_sequence",
            "- provisional indexing requires human claim approval: no; claims approved by indexing: 0",
            f"- observed source-log snapshot: {counts['source_log_observed_count']} rows",
            f"- recognized NW2-H provisional batch matches: {counts['provisional_batch_matches']}",
            f"- metadata-review URL groups: {counts['metadata_issue_urls']}",
            f"- web/archive-review URL groups: {counts['web_review_urls']}",
            f"- source-type categories needing human choice: {counts['type_human_choice_categories']}",
            f"- source-type categories mechanically normalized: {counts['type_mechanical_categories']}",
            "- relation_or_claim_approved: 0 yes / 49 no",
            "- missing required proposal metadata: 0",
            "- new URLs without provisional-index/archive boundary: 0",
            "- central source-log writes: 0",
            "- archive manifest/artifact writes: 0",
            f"- central source-log SHA-256 (read-only baseline): `{central_sha_before}`",
            f"- archive manifest SHA-256 (read-only baseline): `{manifest_sha_before}`",
            "- output/interim unique crosswalk SHA-256 match: yes",
        ]
    )


def main() -> None:
    central_sha_before = file_sha256(SOURCE_LOG)
    manifest_sha_before = file_sha256(ARCHIVE_MANIFEST)
    (
        crosswalk,
        records,
        sequence,
        type_rows,
        metadata_queue,
        web_queue,
        boundaries,
        counts,
    ) = build()
    validate(
        crosswalk,
        records,
        sequence,
        metadata_queue,
        web_queue,
        boundaries,
        counts,
    )

    write_csv(OUT_CROSSWALK, CROSSWALK_FIELDS, crosswalk)
    write_csv(INTERIM_CROSSWALK, CROSSWALK_FIELDS, crosswalk)
    write_csv(RECORD_AUDIT, RECORD_FIELDS, records)
    write_csv(SEQUENCE, SEQUENCE_FIELDS, sequence)
    write_csv(TYPE_CROSSWALK, TYPE_FIELDS, type_rows)
    write_csv(METADATA_QUEUE, QUEUE_FIELDS, metadata_queue)
    write_csv(WEB_QUEUE, QUEUE_FIELDS, web_queue)
    write_csv(BOUNDARY_AUDIT, BOUNDARY_FIELDS, boundaries)
    write_text(README, render_readme(counts, sequence))
    write_text(
        VALIDATION,
        render_validation(counts, central_sha_before, manifest_sha_before),
    )

    if file_sha256(SOURCE_LOG) != central_sha_before:
        raise RuntimeError("central source log changed during a read-only audit")
    if file_sha256(ARCHIVE_MANIFEST) != manifest_sha_before:
        raise RuntimeError("archive manifest changed during a read-only audit")
    if file_sha256(OUT_CROSSWALK) != file_sha256(INTERIM_CROSSWALK):
        raise RuntimeError("output/interim unique crosswalk copies differ")

    print("# NW2-F source proposal audit validation")
    print(f"- input rows: {counts['input_records']} (21 R9 + 29 registry gate)")
    print(f"- normalized unique URLs: {counts['unique_urls']}")
    print(f"- cross-batch duplicate groups: {counts['cross_batch_duplicates']}")
    print(f"- current source matches: {counts['existing_urls']} (S158, S204)")
    print(f"- proposed new unique URLs: {counts['new_urls']} (S248-S294 order only)")
    print(f"- metadata-review URL groups: {counts['metadata_issue_urls']}")
    print(f"- web/archive-review URL groups: {counts['web_review_urls']}")
    print("- relation_or_claim_approved: all no")
    print("- central source/archive writes: 0")
    print("- output/interim crosswalk SHA match: yes")


if __name__ == "__main__":
    main()
