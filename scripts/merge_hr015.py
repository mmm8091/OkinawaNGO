"""Merge the user-reviewed HR-015 evidence and actor-event-venue tables.

The seed tables remain readable review artifacts; the formal copies in
data/interim are the only rows intended for downstream use.  This script is
deliberately deterministic so rerunning it does not append review text or
change row order.
"""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FOUNDATION = ROOT / "outputs" / "phase1_foundation_v1"
DATA = ROOT / "data" / "interim"

NOTE_SEED = FOUNDATION / "evidence_notes_seed_v0.csv"
AEV_SEED = FOUNDATION / "actor_event_venue_seed_v0.csv"
NOTE_FORMAL = DATA / "06_evidence_notes_v0.csv"
AEV_FORMAL = DATA / "09_actor_event_venue_edges_v0.csv"

REVIEW_TASK = "HR-015"
REVIEWER = "project_principal_user"
REVIEW_DATE = "2026-07-13"

NOTE_BASE_FIELDS = [
    "evidence_id",
    "object_type",
    "object_id",
    "claim",
    "source_id",
    "evidence_summary_or_short_quote",
    "source_locator",
    "evidence_level",
    "reviewer_status",
    "notes",
]
NOTE_REVIEW_FIELDS = [
    "review_decision",
    "human_reviewer",
    "review_date",
    "review_task_id",
    "locator_status",
    "interpretation_limit",
]
AEV_BASE_FIELDS = [
    "record_id",
    "record_scope",
    "event_id",
    "event_name",
    "event_year",
    "actor_or_counterpart_id",
    "legacy_candidate_id",
    "actor_or_counterpart_name",
    "entity_type",
    "action_type",
    "venue_id",
    "target_type",
    "target_id_or_name",
    "role",
    "pathway_stage",
    "evidence_level",
    "source_id",
    "reviewer_status",
    "interpretation_limit",
    "notes",
]
AEV_REVIEW_FIELDS = [
    "review_decision",
    "human_reviewer",
    "review_date",
    "review_task_id",
]

# The source gives the correct document but not a verified pinpoint.  HR-015
# explicitly forbids guessing the missing PDF page or HTML section.
LOCATOR_PENDING = {
    "EN0021",
    "EN0033",
    "EN0038",
    "EN0039",
    "EN0040",
}

S129_ROLE_LOCATORS = {
    "EN0025": "source_docs/source_archive/S129/raw.pdf — opinion p. 1 (PDF index 0), caption",
    "EN0026": "source_docs/source_archive/S129/raw.pdf — opinion p. 1 (PDF index 0), caption",
    "EN0027": "source_docs/source_archive/S129/raw.pdf — opinion p. 1 (PDF index 0), caption",
    "EN0028": "source_docs/source_archive/S129/raw.pdf — opinion p. 1 (PDF index 0), caption",
    "EN0029": "source_docs/source_archive/S129/raw.pdf — opinion p. 4 (PDF index 3), counsel section",
    "EN0030": "source_docs/source_archive/S129/raw.pdf — opinion p. 1 (PDF index 0), caption",
}

DUGONG_NOTES = {f"EN{i:04d}" for i in range(25, 33)}
REQUIRED_HUMAN_CHECKED_AEV = {f"AEV{i:04d}" for i in range(45, 61)}
LEGAL_ROLE_AEV = (
    {f"AEV{i:04d}" for i in range(45, 50)}
    | {f"AEV{i:04d}" for i in range(55, 61)}
)
MMC_E2_AEV = {f"AEV{i:04d}" for i in range(36, 45)}
MMC_LEGACY_BY_RECORD = {
    f"AEV{record_number:04d}": f"A{actor_number:03d}"
    for record_number, actor_number in zip(range(36, 45), range(77, 86))
}
UNVERIFIED_MMC_CANDIDATES = set(MMC_LEGACY_BY_RECORD.values())
YONAGUNI_E2_AEV = {"AEV0053", "AEV0054"}
REFERENDUM_AEV = {"AEV0050", "AEV0051", "AEV0052"}
PATHWAY_AEV = {f"AEV{i:04d}" for i in range(61, 65)}

# "Revise" means the seed wording needs an explicit interpretation or locator
# boundary.  It does not mean the evidence level is upgraded.
NOTE_REVISE = (
    {"EN0017", "EN0022", "EN0023", "EN0024"}
    | DUGONG_NOTES
    | LOCATOR_PENDING
    | {f"EN{i:04d}" for i in range(33, 50)}
)
AEV_REVISE = MMC_E2_AEV | YONAGUNI_E2_AEV | LEGAL_ROLE_AEV | PATHWAY_AEV


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_csv_with_fields(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows({field: row.get(field, "") for field in fields} for row in rows)


def ids(path: Path, field: str) -> set[str]:
    return {row[field] for row in read_csv(path) if row.get(field)}


PRIMARY_ACTOR_TABLES = {
    DATA / "01_actor_registry_initial_v0.csv": ("actor_id",),
    DATA / "02_actor_aliases_initial_v0.csv": ("actor_id",),
    DATA / "07_actor_issue_edges_initial_v0.csv": ("actor_id",),
    DATA / "08_actor_place_edges_initial_v0.csv": ("actor_id",),
    DATA / "15_funding_or_support_edges_sample_v0.csv": (
        "source_actor_id",
        "target_actor_id",
    ),
}


def withdraw_unverified_mmc_candidates() -> dict[str, int]:
    """Remove the nine signatory-only labels from actor-entity main tables."""
    removals: dict[str, int] = {}
    for path, actor_fields in PRIMARY_ACTOR_TABLES.items():
        fields, rows = read_csv_with_fields(path)
        kept = [
            row
            for row in rows
            if not any(row.get(field, "") in UNVERIFIED_MMC_CANDIDATES for field in actor_fields)
        ]
        removed = len(rows) - len(kept)
        removals[path.name] = removed
        if removed:
            write_csv(path, fields, kept)
    return removals


def note_limit(row: dict[str, str]) -> str:
    evidence_id = row["evidence_id"]
    object_type = row["object_type"]

    if evidence_id == "EN0017":
        return (
            "E2 event-context evidence only; do not infer a stable organization, "
            "continuity, or a definite actor conclusion without local retrieval."
        )
    if evidence_id in {"EN0022", "EN0023", "EN0024"}:
        return (
            "The source supports publicly visible participation in this event only; "
            "co-occurrence or co-signing is not evidence of a stable alliance."
        )
    if evidence_id in {"EN0025", "EN0026", "EN0027", "EN0028"}:
        return (
            "Named organizational plaintiff role only; keep plaintiff, counsel, "
            "defendant, and non-party roles distinct."
        )
    if evidence_id == "EN0029":
        return "Counsel role only; counsel must not be recoded as a plaintiff or movement alliance."
    if evidence_id == "EN0030":
        return "Defendant role only; keep defendant and plaintiff roles distinct."
    if evidence_id in {"EN0031", "EN0032"}:
        return (
            "The organization is not a named plaintiff in the cited caption; "
            "person-level participation must not be transferred to an organization."
        )
    if object_type == "funding_support_edge":
        return (
            "Retain the row's stated relation type and confidence only: an opportunity, "
            "project cost, sponsorship, membership, service, or in-kind item is not "
            "movement funding or a contract payment unless the cited record says so."
        )
    if evidence_id == "EN0047":
        return "Service-location evidence does not establish an anti-base or pro-base political stance."
    if evidence_id in {"EN0048", "EN0049"}:
        return (
            "Observed functional or service role only; do not infer a political stance, "
            "stable alliance, or unrecorded funding relationship."
        )
    return (
        "Supports only the stated object and claim; do not infer a stable alliance, "
        "causal chain, or relationship beyond the cited evidence."
    )


def merge_notes(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    merged: list[dict[str, str]] = []
    for source_row in rows:
        row = {field: source_row.get(field, "") for field in NOTE_BASE_FIELDS}
        evidence_id = row["evidence_id"]
        if evidence_id in S129_ROLE_LOCATORS:
            row["source_id"] = "S129"
            row["source_locator"] = S129_ROLE_LOCATORS[evidence_id]
            if evidence_id in {"EN0025", "EN0026", "EN0027", "EN0028"}:
                row["evidence_summary_or_short_quote"] = (
                    "The official Ninth Circuit opinion caption names the organization "
                    "among Plaintiffs-Appellants."
                )
            elif evidence_id == "EN0029":
                row["evidence_summary_or_short_quote"] = (
                    "The official Ninth Circuit opinion's counsel section names "
                    "Earthjustice attorneys for Plaintiffs-Appellants."
                )
            else:
                row["evidence_summary_or_short_quote"] = (
                    "The official Ninth Circuit opinion caption names the U.S. Department "
                    "of Defense among Defendants-Appellees."
                )
        row["reviewer_status"] = "human_checked"
        row["review_decision"] = "revise" if evidence_id in NOTE_REVISE else "accept"
        row["human_reviewer"] = REVIEWER
        row["review_date"] = REVIEW_DATE
        row["review_task_id"] = REVIEW_TASK
        row["locator_status"] = (
            "needs_locator_revision" if evidence_id in LOCATOR_PENDING else "verified_as_cited"
        )
        if evidence_id in S129_ROLE_LOCATORS:
            row["locator_status"] = "verified_exact_page"
        row["interpretation_limit"] = note_limit(row)
        stale_note_replacements = {
            "EN0007": "Upstream edge and this evidence note were human-reviewed under HR-015.",
            "EN0031": "HR-015 human review retained the negative party-role boundary.",
            "EN0034": "Upstream edge and this evidence note were human-reviewed under HR-015.",
            "EN0045": "Upstream relation and this evidence note were human-reviewed under HR-015.",
        }
        if evidence_id in stale_note_replacements:
            row["notes"] = stale_note_replacements[evidence_id]
        if evidence_id in S129_ROLE_LOCATORS:
            row["notes"] = (
                "HR-015 role and exact opinion locator confirmed against Ninth Circuit "
                "opinion No. 18-16836 (S129)."
            )
        if evidence_id in LOCATOR_PENDING:
            locator_note = (
                "HR-015: user requested no guessed page/section; "
                "exact locator remains pending."
            )
            if locator_note not in row["notes"]:
                row["notes"] = (
                    row["notes"].rstrip("; ")
                    + ("; " if row["notes"].strip() else "")
                    + locator_note
                )
        merged.append(row)
    return merged


def merge_aev(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    merged: list[dict[str, str]] = []
    for source_row in rows:
        row = {field: source_row.get(field, "") for field in AEV_BASE_FIELDS}
        record_id = row["record_id"]
        if record_id in MMC_E2_AEV:
            legacy_candidate_id = (
                source_row.get("legacy_candidate_id", "")
                or source_row.get("actor_or_counterpart_id", "")
                or MMC_LEGACY_BY_RECORD[record_id]
            )
            require(
                legacy_candidate_id == MMC_LEGACY_BY_RECORD[record_id],
                f"unexpected MMC legacy candidate ID on {record_id}",
            )
            row["actor_or_counterpart_id"] = ""
            row["legacy_candidate_id"] = legacy_candidate_id
            row["entity_type"] = "unverified_event_participant"
        else:
            row["legacy_candidate_id"] = ""
        row["review_decision"] = "revise" if record_id in AEV_REVISE else "accept"
        row["human_reviewer"] = REVIEWER
        row["review_date"] = REVIEW_DATE
        row["review_task_id"] = REVIEW_TASK

        if record_id in PATHWAY_AEV:
            row["reviewer_status"] = "analytical_seed"
            row["interpretation_limit"] = (
                "Analytical pathway seed only: this is not an observed causal chain, "
                "stable alliance, or deterministic finding."
            )
        else:
            row["reviewer_status"] = "human_checked"

        if record_id in MMC_E2_AEV:
            row["interpretation_limit"] = (
                "E2 signatory-only evidence: one-off public participation only; "
                "do not infer organizational continuity, a stable alliance, or a definite conclusion."
            )
        elif record_id in YONAGUNI_E2_AEV:
            row["interpretation_limit"] = (
                "E2 event-context evidence only: organization identity and continuity remain "
                "unresolved pending local retrieval; do not use as a definite conclusion."
            )
        elif record_id in REFERENDUM_AEV:
            row["interpretation_limit"] = (
                "Human-checked referendum-initiator role for this specific process only; "
                "do not infer a stable alliance or wider political causation."
            )
        elif record_id in LEGAL_ROLE_AEV:
            if record_id in {"AEV0059", "AEV0060"}:
                row["interpretation_limit"] = (
                    "Human-checked non-party organization role: person-level participation "
                    "must not be transferred to an organization; not an alliance finding."
                )
            else:
                row["interpretation_limit"] = (
                    "Human-checked case role only; keep named plaintiff, individual, counsel, "
                    "defendant, and non-party roles distinct."
                )
        if "venue/target mapping requires human review" in row["notes"]:
            row["notes"] = (
                "HR-015: venue/target mapping human-reviewed; event role remains "
                "bounded by interpretation_limit."
            )
        if record_id in {"AEV0059", "AEV0060"}:
            row["notes"] = (
                "HR-015: legal role human-reviewed; person/organization boundary retained."
            )
        if record_id in MMC_E2_AEV:
            row["notes"] = (
                "HR-015: unverified event participant retained only under legacy_candidate_id; "
                "not admitted to the main actor registry."
            )
        merged.append(row)
    return merged


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def validate(notes: list[dict[str, str]], aev: list[dict[str, str]]) -> None:
    require(len(notes) == 49, f"expected 49 evidence notes, found {len(notes)}")
    require(len(aev) == 64, f"expected 64 AEV rows, found {len(aev)}")
    require(
        {row["evidence_id"] for row in notes} == {f"EN{i:04d}" for i in range(1, 50)},
        "evidence IDs must be exactly EN0001-EN0049",
    )
    require(
        {row["record_id"] for row in aev} == {f"AEV{i:04d}" for i in range(1, 65)},
        "AEV IDs must be exactly AEV0001-AEV0064",
    )

    source_ids = ids(DATA / "05_source_log_initial_v0.csv", "source_id")
    actor_ids = ids(DATA / "01_actor_registry_initial_v0.csv", "actor_id")
    require(
        actor_ids.isdisjoint(UNVERIFIED_MMC_CANDIDATES),
        "A077-A085 must be absent from the main actor registry",
    )
    venue_ids = ids(FOUNDATION / "venue_taxonomy_v0.csv", "venue_id")
    event_ids = ids(
        ROOT / "outputs" / "module_completion_v0" / "actor_relation_events_v1.csv",
        "event_id",
    )
    object_ids = {
        "actor_issue_edge": ids(DATA / "07_actor_issue_edges_initial_v0.csv", "edge_id"),
        "actor_place_edge": ids(DATA / "08_actor_place_edges_initial_v0.csv", "edge_id"),
        "funding_support_edge": ids(
            DATA / "15_funding_or_support_edges_sample_v0.csv", "edge_id"
        ),
        "event": event_ids,
        "actor_event_role": {row["record_id"] for row in aev},
    }

    for row in notes:
        require(row["source_id"] in source_ids, f"unknown source on {row['evidence_id']}")
        require(row["object_type"] in object_ids, f"unknown object type on {row['evidence_id']}")
        require(
            row["object_id"] in object_ids[row["object_type"]],
            f"unknown object ID on {row['evidence_id']}: {row['object_id']}",
        )
        require(row["review_decision"] != "reject", f"unexpected reject: {row['evidence_id']}")

    for row in aev:
        record_id = row["record_id"]
        require(row["source_id"] in source_ids, f"unknown source on {record_id}")
        require(row["venue_id"] in venue_ids, f"unknown venue on {record_id}")
        if row["event_id"]:
            require(row["event_id"] in event_ids, f"unknown event on {record_id}")
        if row["entity_type"] == "registry_actor":
            require(
                row["actor_or_counterpart_id"] in actor_ids,
                f"unknown actor on {record_id}",
            )
        if record_id in MMC_E2_AEV:
            require(
                not row["actor_or_counterpart_id"]
                and row["legacy_candidate_id"] == MMC_LEGACY_BY_RECORD[record_id]
                and row["entity_type"] == "unverified_event_participant",
                f"MMC row {record_id} must remain an unverified legacy event participant",
            )
        else:
            require(
                not row["legacy_candidate_id"],
                f"unexpected legacy candidate ID on {record_id}",
            )
        require(row["review_decision"] != "reject", f"unexpected reject: {record_id}")

    for path, actor_fields in PRIMARY_ACTOR_TABLES.items():
        for row in read_csv(path):
            require(
                all(row.get(field, "") not in UNVERIFIED_MMC_CANDIDATES for field in actor_fields),
                f"unverified MMC candidate remains in primary table {path.name}",
            )

    note_by_id = {row["evidence_id"]: row for row in notes}
    aev_by_id = {row["record_id"]: row for row in aev}
    require(
        all(note_by_id[item]["reviewer_status"] == "human_checked" for item in DUGONG_NOTES),
        "Dugong evidence notes EN0025-EN0032 must be human_checked",
    )
    require(
        all(
            aev_by_id[item]["reviewer_status"] == "human_checked"
            for item in REQUIRED_HUMAN_CHECKED_AEV
        ),
        "AEV0045-AEV0060 must be human_checked",
    )
    require(
        all(aev_by_id[item]["evidence_level"] == "E2" for item in MMC_E2_AEV | YONAGUNI_E2_AEV),
        "MMC/Yonaguni E2 rows must remain E2",
    )
    pathway = [row for row in aev if row["record_scope"] == "pathway_seed"]
    require(len(pathway) == 4, "expected exactly four pathway seeds")
    require(
        all(
            row["reviewer_status"] == "analytical_seed"
            and not row["event_id"]
            and "not an observed causal chain" in row["interpretation_limit"]
            for row in pathway
        ),
        "pathway rows must be explicit analytical_seed rows, not observed event chains",
    )
    require(
        {row["evidence_id"] for row in notes if row["locator_status"] == "needs_locator_revision"}
        == LOCATOR_PENDING,
        "locator-revision set changed unexpectedly",
    )
    for evidence_id, expected_locator in S129_ROLE_LOCATORS.items():
        row = note_by_id[evidence_id]
        require(row["source_id"] == "S129", f"{evidence_id} must cite S129")
        require(
            row["source_locator"] == expected_locator
            and row["locator_status"] == "verified_exact_page",
            f"{evidence_id} must retain the verified S129 opinion locator",
        )


def main() -> None:
    removals = withdraw_unverified_mmc_candidates()
    notes = merge_notes(read_csv(NOTE_SEED))
    aev = merge_aev(read_csv(AEV_SEED))
    validate(notes, aev)

    note_fields = NOTE_BASE_FIELDS + NOTE_REVIEW_FIELDS
    aev_fields = AEV_BASE_FIELDS + AEV_REVIEW_FIELDS
    write_csv(NOTE_SEED, note_fields, notes)
    write_csv(AEV_SEED, aev_fields, aev)
    write_csv(NOTE_FORMAL, note_fields, notes)
    write_csv(AEV_FORMAL, aev_fields, aev)

    # Validate the serialized formal outputs too, not only the in-memory rows.
    formal_notes = read_csv(NOTE_FORMAL)
    formal_aev = read_csv(AEV_FORMAL)
    validate(formal_notes, formal_aev)
    require(formal_notes == notes, "formal evidence-note serialization mismatch")
    require(formal_aev == aev, "formal AEV serialization mismatch")
    print(
        "HR-015 merge OK: 49 evidence notes; 64 AEV rows; "
        f"0 rejects; {len(LOCATOR_PENDING)} locator revisions; 4 analytical seeds; "
        f"{sum(removals.values())} stale primary-table candidate rows removed this run."
    )


if __name__ == "__main__":
    main()
