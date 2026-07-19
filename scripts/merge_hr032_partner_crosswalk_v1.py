from __future__ import annotations

"""Materialize the principal-approved HR-032 identity crosswalk.

The 616-row S002 source universe remains immutable. This script writes a
separate, human-reviewed identity layer and a separate member-of-composite
layer. Neither layer approves an administrative/funding relation edge or
allocates a whole-program project cost to a named organization.
"""

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path("outputs/R10_official_collaboration_universe_v1")
UNIVERSE = PACKAGE / "official_collaboration_source_universe_v1.csv"
REVIEW_QUEUE = PACKAGE / "HR032_partner_alias_crosswalk_review_v1.csv"
IDENTITY_OUTPUT = PACKAGE / "partner_identity_crosswalk_human_v1.csv"
MEMBER_OUTPUT = PACKAGE / "member_of_composite_crosswalk_human_v1.csv"


IDENTITY_FIELDS = [
    "source_row_uid",
    "source_row_number",
    "review_item_id",
    "source_partner_name",
    "source_partner_kind_code",
    "source_partner_kind_label",
    "approved_display_name",
    "canonical_identity_key",
    "entity_scope",
    "registry_actor_id",
    "registry_crosswalk_decision",
    "approved_english_name",
    "approved_acronym",
    "partner_kind_review",
    "role_review",
    "review_status",
    "human_reviewer",
    "review_date",
    "decision_source_report",
    "actor_relation_edge_approved",
    "amount_allocation_approved",
    "scope_boundary",
]

MEMBER_FIELDS = [
    "composite_source_row_uid",
    "review_item_id",
    "composite_identity_key",
    "composite_display_name",
    "member_identity_key",
    "member_display_name",
    "member_scope",
    "relation_type",
    "member_identity_crosswalk_approved",
    "actor_relation_edge_approved",
    "amount_allocation_approved",
    "review_status",
    "human_reviewer",
    "review_date",
    "decision_source_report",
    "scope_boundary",
]


def number_range(start: int, end: int) -> list[int]:
    return list(range(start, end + 1))


SOCIAL_WELFARE_ROWS = (
    number_range(60, 71)
    + [73]
    + number_range(79, 83)
    + [163, 191, 292, 314, 317, 521]
)


IDENTITY_GROUPS = [
    {
        "review_item_id": "HR032-01",
        "rows": SOCIAL_WELFARE_ROWS,
        "approved_display_name": "社会福祉法人沖縄県社会福祉協議会",
        "canonical_identity_key": "HRE032-01",
        "entity_scope": "legal_entity_no_registry",
        "registry_crosswalk_decision": "display_alias_only_no_registry_entry",
        "scope_boundary": "Legal-prefix alias only; no registry entry or relation edge.",
    },
    {
        "review_item_id": "HR032-02",
        "rows": [9, 496],
        "approved_display_name": "公益財団法人沖縄県平和祈念財団",
        "canonical_identity_key": "HRE032-02",
        "entity_scope": "legal_entity_no_registry",
        "registry_crosswalk_decision": "same_legal_entity_no_registry_entry",
        "scope_boundary": (
            "Distinct from the Himeyuri foundation; project cost is not a payment."
        ),
    },
    {
        "review_item_id": "HR032-03",
        "rows": [197, 205, 206],
        "approved_display_name": "公益財団法人おきなわ女性財団",
        "canonical_identity_key": "HRE032-03",
        "entity_scope": "legal_entity_no_registry",
        "registry_crosswalk_decision": "same_legal_entity_no_registry_entry",
        "scope_boundary": (
            "Do not conflate with A111 or retired A094; composite role is separate."
        ),
    },
    {
        "review_item_id": "HR032-03",
        "rows": [207],
        "approved_display_name": "沖縄県男女共同参画センター管理運営団体",
        "canonical_identity_key": "HRC032-01",
        "entity_scope": "composite_source_entity",
        "registry_crosswalk_decision": "preserve_composite_no_registry_entry",
        "scope_boundary": (
            "Preserve the management composite; member costs are not separable."
        ),
    },
    {
        "review_item_id": "HR032-04",
        "rows": [10, 11, 501],
        "approved_display_name": "特定非営利活動法人沖縄平和協力センター",
        "canonical_identity_key": "A088",
        "entity_scope": "registry_actor",
        "registry_actor_id": "A088",
        "registry_crosswalk_decision": "A088_same_legal_entity",
        "approved_english_name": "Okinawa Peace Assistance Center",
        "approved_acronym": "OPAC",
        "scope_boundary": (
            "Actor identity crosswalk only; the three administrative relations "
            "remain gated separately."
        ),
    },
    {
        "review_item_id": "HR032-05",
        "rows": [435],
        "approved_display_name": "公益社団法人青年海外協力協会沖縄事務所（JOCA沖縄）",
        "canonical_identity_key": "HRE032-05",
        "entity_scope": "office_of_legal_entity",
        "registry_crosswalk_decision": "parent_legal_entity_office_no_registry_entry",
        "approved_english_name": "Japan Overseas Cooperative Association",
        "approved_acronym": "JOCA",
        "scope_boundary": (
            "Okinawa office is not a separate legal person; no cost allocation."
        ),
    },
    {
        "review_item_id": "HR032-05",
        "rows": [432],
        "approved_display_name": "令和６年度おきなわ国際協力人材育成事業共同企業体",
        "canonical_identity_key": "HRC032-02",
        "entity_scope": "composite_source_entity",
        "registry_crosswalk_decision": "preserve_composite_no_registry_entry",
        "scope_boundary": "Distinct project JV; JOCA appears only as a member.",
    },
    {
        "review_item_id": "HR032-05",
        "rows": [436],
        "approved_display_name": "令和６年度ウチナージュニアスタディー事業に係る共同企業体",
        "canonical_identity_key": "HRC032-03",
        "entity_scope": "composite_source_entity",
        "registry_crosswalk_decision": "preserve_composite_no_registry_entry",
        "scope_boundary": "Distinct project JV; JOCA appears only as a member.",
    },
    {
        "review_item_id": "HR032-05",
        "rows": [438],
        "approved_display_name": "令和６年度長野県への生徒派遣交流事業共同企業体",
        "canonical_identity_key": "HRC032-04",
        "entity_scope": "composite_source_entity",
        "registry_crosswalk_decision": "preserve_composite_no_registry_entry",
        "scope_boundary": "Distinct project JV; JOCA appears only as a member.",
    },
    {
        "review_item_id": "HR032-06",
        "rows": [433, 571],
        "approved_display_name": "一般社団法人世界若者ウチナーンチュ連合会",
        "canonical_identity_key": "HRE032-06",
        "entity_scope": "legal_entity_no_registry",
        "registry_crosswalk_decision": "same_legal_entity_no_registry_entry",
        "approved_english_name": "World Youth Uchinanchu Association",
        "approved_acronym": "WYUA",
        "scope_boundary": "Team OKIYUA remains a separate composite.",
    },
    {
        "review_item_id": "HR032-06",
        "rows": [434],
        "approved_display_name": "Team OKIYUA",
        "canonical_identity_key": "HRC032-05",
        "entity_scope": "composite_source_entity",
        "registry_crosswalk_decision": "preserve_composite_no_registry_entry",
        "scope_boundary": "WYUA is a member; composite costs are not allocated.",
    },
    {
        "review_item_id": "HR032-07",
        "rows": [529, 545, 548, 551],
        "approved_display_name": "沖縄県ユネスコ協会",
        "canonical_identity_key": "HRE032-07",
        "entity_scope": "unincorporated_association",
        "registry_crosswalk_decision": "same_continuing_entity_no_registry_entry",
        "scope_boundary": (
            "Keep mechanisms separate; row 545 retains its conflicting raw kind."
        ),
    },
    {
        "review_item_id": "HR032-08",
        "rows": [204, 466, 499, 591],
        "approved_display_name": "特定非営利活動法人レインボーハートokinawa",
        "canonical_identity_key": "HRE032-08",
        "entity_scope": "legal_entity_role_unresolved",
        "registry_crosswalk_decision": "same_legal_entity_no_registry_entry",
        "scope_boundary": (
            "Row 466 is only a source-table fact; no contractor, payment or "
            "cross-department bridge inference."
        ),
    },
]


MEMBER_CROSSWALKS = [
    {
        "source_row_number": 207,
        "review_item_id": "HR032-03",
        "composite_identity_key": "HRC032-01",
        "composite_display_name": "沖縄県男女共同参画センター管理運営団体",
        "member_identity_key": "HRE032-03",
        "member_display_name": "公益財団法人おきなわ女性財団",
        "member_scope": "legal_entity_member",
        "scope_boundary": "Composite preserved; project cost is not split to members.",
    },
    {
        "source_row_number": 432,
        "review_item_id": "HR032-05",
        "composite_identity_key": "HRC032-02",
        "composite_display_name": "令和６年度おきなわ国際協力人材育成事業共同企業体",
        "member_identity_key": "HRE032-05",
        "member_display_name": "公益社団法人青年海外協力協会沖縄事務所（JOCA沖縄）",
        "member_scope": "office_member_of_project_jv",
        "scope_boundary": "Member identity only; no allocation of JV project cost.",
    },
    {
        "source_row_number": 436,
        "review_item_id": "HR032-05",
        "composite_identity_key": "HRC032-03",
        "composite_display_name": "令和６年度ウチナージュニアスタディー事業に係る共同企業体",
        "member_identity_key": "HRE032-05",
        "member_display_name": "公益社団法人青年海外協力協会沖縄事務所（JOCA沖縄）",
        "member_scope": "office_member_of_project_jv",
        "scope_boundary": "Member identity only; no allocation of JV project cost.",
    },
    {
        "source_row_number": 438,
        "review_item_id": "HR032-05",
        "composite_identity_key": "HRC032-04",
        "composite_display_name": "令和６年度長野県への生徒派遣交流事業共同企業体",
        "member_identity_key": "HRE032-05",
        "member_display_name": "公益社団法人青年海外協力協会沖縄事務所（JOCA沖縄）",
        "member_scope": "office_member_of_project_jv",
        "scope_boundary": "Member identity only; no allocation of JV project cost.",
    },
    {
        "source_row_number": 434,
        "review_item_id": "HR032-06",
        "composite_identity_key": "HRC032-05",
        "composite_display_name": "Team OKIYUA",
        "member_identity_key": "HRE032-06",
        "member_display_name": "一般社団法人世界若者ウチナーンチュ連合会",
        "member_scope": "legal_entity_member",
        "scope_boundary": "Member identity only; no allocation of composite cost.",
    },
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(
    path: Path, fields: list[str], rows: list[dict[str, str]]
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def row_uid(number: int) -> str:
    return f"S002-R{number:04d}"


def review_status(decision: str) -> str:
    return "human_revised" if decision == "revise" else "human_checked"


def kind_review(number: int) -> str:
    if number == 496:
        return "source_partner_kind_conflict"
    if number == 545:
        return "source_kind_conflict_probable_miscoding"
    if number in {207, 432, 434, 436, 438}:
        return "preserve_source_kind_on_composite"
    return "preserve_source_kind"


def role_review(number: int) -> str:
    if number == 466:
        return "unexplained_other_or_advisory_candidate"
    if number in {207, 432, 434, 436, 438}:
        return "composite_membership_recorded_separately"
    return "identity_crosswalk_only"


def apply_hr032_partner_crosswalk(root: Path = ROOT) -> dict[str, int]:
    package = root / PACKAGE
    universe_rows = read_csv(root / UNIVERSE)
    queue_rows = read_csv(root / REVIEW_QUEUE)
    universe_by_number = {
        int(row["source_row_number"]): row for row in universe_rows
    }
    queue_by_id = {row["review_item_id"]: row for row in queue_rows}

    if len(universe_rows) != 616:
        raise ValueError(f"expected 616 S002 rows, found {len(universe_rows)}")
    if set(queue_by_id) != {f"HR032-{number:02d}" for number in range(1, 9)}:
        raise ValueError("HR-032 review queue must contain exactly HR032-01 through -08")
    if any(not row["decision"] for row in queue_rows):
        raise ValueError("HR-032 has an undecided review item")

    identity_rows: list[dict[str, str]] = []
    seen_numbers: set[int] = set()
    for group in IDENTITY_GROUPS:
        review = queue_by_id[group["review_item_id"]]
        for number in group["rows"]:
            if number in seen_numbers:
                raise ValueError(f"source row {number} appears in two HR-032 groups")
            seen_numbers.add(number)
            source = universe_by_number[number]
            identity_rows.append(
                {
                    "source_row_uid": source["source_row_uid"],
                    "source_row_number": str(number),
                    "review_item_id": group["review_item_id"],
                    "source_partner_name": source["partner_name_source_text"],
                    "source_partner_kind_code": source["partner_kind_code"],
                    "source_partner_kind_label": source["partner_kind_label"],
                    "approved_display_name": group["approved_display_name"],
                    "canonical_identity_key": group["canonical_identity_key"],
                    "entity_scope": group["entity_scope"],
                    "registry_actor_id": group.get("registry_actor_id", ""),
                    "registry_crosswalk_decision": group[
                        "registry_crosswalk_decision"
                    ],
                    "approved_english_name": group.get(
                        "approved_english_name", ""
                    ),
                    "approved_acronym": group.get("approved_acronym", ""),
                    "partner_kind_review": kind_review(number),
                    "role_review": role_review(number),
                    "review_status": review_status(review["decision"]),
                    "human_reviewer": "project_principal_user",
                    "review_date": review["review_date"],
                    "decision_source_report": review["decision_source_report"],
                    "actor_relation_edge_approved": "no",
                    "amount_allocation_approved": "no",
                    "scope_boundary": group["scope_boundary"],
                }
            )

    if len(identity_rows) != 48:
        raise ValueError(f"expected 48 identity rows, found {len(identity_rows)}")

    member_rows: list[dict[str, str]] = []
    for item in MEMBER_CROSSWALKS:
        review = queue_by_id[item["review_item_id"]]
        number = item["source_row_number"]
        member_rows.append(
            {
                "composite_source_row_uid": row_uid(number),
                "review_item_id": item["review_item_id"],
                "composite_identity_key": item["composite_identity_key"],
                "composite_display_name": item["composite_display_name"],
                "member_identity_key": item["member_identity_key"],
                "member_display_name": item["member_display_name"],
                "member_scope": item["member_scope"],
                "relation_type": "member_of_composite",
                "member_identity_crosswalk_approved": "yes",
                "actor_relation_edge_approved": "no",
                "amount_allocation_approved": "no",
                "review_status": review_status(review["decision"]),
                "human_reviewer": "project_principal_user",
                "review_date": review["review_date"],
                "decision_source_report": review["decision_source_report"],
                "scope_boundary": item["scope_boundary"],
            }
        )

    identity_rows.sort(key=lambda row: int(row["source_row_number"]))
    member_rows.sort(key=lambda row: int(row["composite_source_row_uid"][-4:]))
    write_csv(package / IDENTITY_OUTPUT.name, IDENTITY_FIELDS, identity_rows)
    write_csv(package / MEMBER_OUTPUT.name, MEMBER_FIELDS, member_rows)

    summary = {
        "source_universe_rows_unchanged": len(universe_rows),
        "identity_crosswalk_rows": len(identity_rows),
        "member_crosswalk_rows": len(member_rows),
        "registry_crosswalk_rows": sum(
            bool(row["registry_actor_id"]) for row in identity_rows
        ),
        "administrative_relation_edges_approved": 0,
        "amount_allocations_approved": 0,
    }
    write_csv(
        package / "HR032_crosswalk_merge_summary_v1.csv",
        ["metric", "value"],
        [
            {"metric": metric, "value": str(value)}
            for metric, value in summary.items()
        ],
    )
    (package / "HR032_crosswalk_merge_readme_v1.md").write_text(
        "# HR-032 identity and composite crosswalk merge\n\n"
        "The principal-reviewed HR-032 decisions are materialized without "
        "modifying the 616-row S002 source universe.\n\n"
        "- 48 source rows have a bounded identity/display crosswalk.\n"
        "- Five accepted member-of-composite crosswalks are stored separately.\n"
        "- Three source rows map to registry actor A088 for identity only.\n"
        "- No administrative/funding actor edge or amount allocation is approved.\n"
        "- Whole-program project cost remains a source-row attribute and is never "
        "assigned to a member organization by this layer.\n",
        encoding="utf-8",
    )
    return summary


if __name__ == "__main__":
    result = apply_hr032_partner_crosswalk()
    print(
        "HR-032 crosswalk complete: "
        f"{result['identity_crosswalk_rows']} identity rows, "
        f"{result['member_crosswalk_rows']} member rows."
    )
