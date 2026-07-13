from __future__ import annotations

"""Merge the user-reviewed HR-014 legal/procedure decisions.

The merge is deliberately idempotent and narrow:

* mark the six reviewed cases as ``human_checked`` without changing their
  case-specific claims or outcomes;
* accept all 27 candidate case roles while preserving the distinction among
  plaintiff, counsel, requester, supporter, and non-party roles;
* publish a normalized role table with main source-log IDs and provisional
  identifiers for non-registry procedural/public nodes;
* never write to the actor registry, source log, control documents, or the
  general funding/support relation table.

Provisional identifiers in this file are role-table identifiers only. They do
not create actors and must not be joined to the actor registry as actor IDs.
"""

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "interim"
OUTPUT = ROOT / "outputs" / "R08_legal_procedure_v0"

CASE_PATH = DATA / "17_legal_policy_procedure_cases_v0.csv"
CANDIDATE_ROLE_PATH = OUTPUT / "case_actor_roles_v0.csv"
MAIN_ROLE_PATH = DATA / "18_legal_policy_actor_roles_v0.csv"
ACTOR_PATH = DATA / "01_actor_registry_initial_v0.csv"
SOURCE_PATH = DATA / "05_source_log_initial_v0.csv"

REVIEW_DATE = "2026-07-13"
HUMAN_REVIEWER = "user"


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def unique_index(
    rows: list[dict[str, str]], fields: tuple[str, ...]
) -> dict[tuple[str, ...], dict[str, str]]:
    result: dict[tuple[str, ...], dict[str, str]] = {}
    for row in rows:
        key = tuple(row[field] for field in fields)
        if key in result:
            raise ValueError(f"Duplicate key {fields}={key}")
        result[key] = row
    return result


CASE_LIMITS = {
    "R8C01": (
        "HR-014 human check: the procedural route and information-production effect are accepted "
        "even though plaintiffs did not stop construction. Party roles are case-specific: A020 is "
        "a plaintiff and A009 is counsel here; A002 and A019 remain non-parties and must not inherit "
        "a plaintiff role from associated people or advocacy activity."
    ),
    "R8C02": (
        "HR-014 human check: the EIA procedure and NACSJ's dated commenter role are accepted. The "
        "existence of the procedure does not prove that every civic actor used it, and a formal "
        "comment does not establish that the proponent or review authority adopted the comment."
    ),
    "R8C03": (
        "HR-014 human check: the resident-plaintiff claims and case-specific outcome are accepted. "
        "A052 is accepted as the Third Kadena plaintiff-group crosswalk, but individual membership "
        "and participant identity must not be generalized across litigation rounds. The Third Kadena "
        "counsel group remains a role-table procedural collective and is not an actor-registry entry."
    ),
    "R8C04": (
        "HR-014 human check: the resident-plaintiff claims and partial-damages outcome are accepted. "
        "A053 is accepted as the Futenma plaintiff-group crosswalk, but the two joined actions and "
        "other litigation rounds do not imply identical individual membership. Counsel and plaintiff "
        "group remain distinct roles."
    ),
    "R8C05": (
        "HR-014 human check: the mandatory-order dismissal and anonymized individual-plaintiff "
        "category are accepted. A011 is the referendum requester/campaign body, not a named "
        "organizational plaintiff. Council rejection and the mayoral implementation-duty claim are "
        "distinct procedural steps."
    ),
    "R8C06": (
        "HR-014 human check: first- and second-wave outcomes remain separate and must not be reduced "
        "to one win/loss. A055 and A020 are accepted as case-specific supporters/material hosts, not "
        "organizational plaintiffs or counsel. A020's plaintiff role in the Dugong case must not be "
        "generalized to the Awase case."
    ),
}


ROLE_FAMILY = {
    "plaintiff": "plaintiff",
    "plaintiff_group": "plaintiff",
    "counsel": "counsel",
    "counsel_secretariat": "counsel",
    "requester": "requester",
    "supporter": "supporter",
    "non_party": "non_party",
    "commenter": "commenter",
    "procedure_proponent": "proponent",
    "comment_recipient_and_review_authority": "institutional_recipient",
    "defendant": "defendant",
    "defendant_and_target": "defendant",
    "defendant_officials_and_targets": "defendant",
}


SOURCE_MAP = {
    "R8S01": "S093",
    "R8S02": "S128",
    "R8S03": "S129",
    "R8S04": "S062",
    "R8S05": "S130",
    "R8S06": "S131",
    "R8S07": "S132",
    "R8S08": "S133",
    "R8S09": "S134",
    "R8S10": "S135",
    "R8S11": "S136",
    "R8S12": "S137",
    "R8S13": "S138",
    "R8S14": "S139",
    "R8S15": "S140",
    "R8S16": "S141",
    "R8S17": "S142",
    "R8S18": "S143",
}


# Provisional entities are scoped to the case-role table and are not actors.
PROVISIONAL = {
    "R8R009": ("P8E001", "public_institution"),
    "R8R010": ("P8E002", "public_institution"),
    "R8R011": ("P8E003", "procedural_collective"),
    "R8R013": ("P8E004", "procedural_collective"),
    "R8R014": ("P8E005", "public_institution"),
    "R8R015": ("P8E006", "procedural_collective"),
    "R8R017": ("P8E007", "external_organization"),
    "R8R018": ("P8E005", "public_institution"),
    "R8R019": ("P8E008", "procedural_collective"),
    "R8R021": ("P8E009", "person"),
    "R8R022": ("P8E010", "public_institution_set"),
    "R8R023": ("P8E011", "procedural_collective"),
    "R8R024": ("P8E012", "procedural_collective"),
    "R8R027": ("P8E013", "public_institution_set"),
}


ROLE_LIMIT_UPDATES = {
    "R8R003": (
        "HR-014: A020 is a named plaintiff in this Dugong case, not counsel. This case-specific "
        "plaintiff role does not transfer to Awase or other litigation."
    ),
    "R8R005": "HR-014: Earthjustice is counsel in this case and is not a named plaintiff.",
    "R8R006": (
        "HR-014: A002 remains a non-party here. The negative role prevents a false plaintiff label "
        "and does not deny advocacy outside the case."
    ),
    "R8R007": (
        "HR-014: A019 remains a non-party. An associated individual's personal role must not be "
        "transferred to the organization."
    ),
    "R8R012": (
        "HR-014: A052 is accepted as the case-specific plaintiff-group crosswalk. Do not infer that "
        "every named resident was a formal member or that participant identity is constant across rounds."
    ),
    "R8R013": (
        "HR-014: counsel role accepted as a Third Kadena procedural collective. No actor-registry "
        "entry or complete individual-lawyer roster is created."
    ),
    "R8R016": (
        "HR-014: A053 is accepted as the case-specific Futenma plaintiff-group crosswalk. The joined "
        "actions and other rounds do not imply identical individual membership."
    ),
    "R8R017": (
        "HR-014: the office's counsel-secretariat role is accepted; it does not make the office the "
        "sole counsel or a plaintiff."
    ),
    "R8R020": (
        "HR-014: A011 is accepted as requester/campaign body and is explicitly not a named "
        "organizational plaintiff without a pleading."
    ),
    "R8R021": (
        "HR-014: counsel role is limited to the related later status-confirmation phase and is not "
        "automatically transferred to every claim in the 2020 mandatory-order judgment."
    ),
    "R8R025": (
        "HR-014: A055 is a case-specific supporter, not an organizational plaintiff or counsel."
    ),
    "R8R026": (
        "HR-014: A020 is a supporter/formal-material host in Awase, not plaintiff or counsel. Its "
        "Dugong-case plaintiff role must not be generalized across cases."
    ),
}


MAIN_ROLE_FIELDS = [
    "role_id",
    "case_id",
    "actor_id",
    "provisional_entity_id",
    "entity_kind",
    "actor_name",
    "role",
    "role_family",
    "side",
    "target_or_recipient",
    "role_evidence_summary",
    "source_refs",
    "evidence_level",
    "review_status",
    "human_decision",
    "human_reviewer",
    "review_date",
    "interpretation_limit",
]


def normalize_source_refs(refs: str) -> str:
    normalized: list[str] = []
    for ref in refs.split(";"):
        ref = ref.strip()
        if not ref:
            continue
        if ref not in SOURCE_MAP:
            raise ValueError(f"Unknown R08 source reference: {ref}")
        mapped = SOURCE_MAP[ref]
        if mapped not in normalized:
            normalized.append(mapped)
    return ";".join(normalized)


def update_cases(rows: list[dict[str, str]]) -> None:
    index = unique_index(rows, ("case_id",))
    actual = {key[0] for key in index}
    if actual != set(CASE_LIMITS):
        raise ValueError(f"Expected cases {sorted(CASE_LIMITS)}, found {sorted(actual)}")
    for case_id, limit in CASE_LIMITS.items():
        index[(case_id,)]["review_status"] = "human_checked"
        index[(case_id,)]["interpretation_limit"] = limit


def update_candidate_roles(rows: list[dict[str, str]]) -> None:
    index = unique_index(rows, ("role_id",))
    expected = {f"R8R{i:03d}" for i in range(1, 28)}
    actual = {key[0] for key in index}
    if actual != expected:
        raise ValueError(f"Expected 27 roles, missing={sorted(expected-actual)}, extra={sorted(actual-expected)}")
    for role_id, row in ((key[0], value) for key, value in index.items()):
        if row["role"] not in ROLE_FAMILY:
            raise ValueError(f"Unmapped role on {role_id}: {row['role']}")
        row["review_status"] = "human_checked"
        if role_id in ROLE_LIMIT_UPDATES:
            row["interpretation_limit"] = ROLE_LIMIT_UPDATES[role_id]


def build_main_roles(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    result: list[dict[str, str]] = []
    for row in rows:
        role_id = row["role_id"]
        actor_id = row["actor_id"]
        if actor_id:
            provisional_id = ""
            entity_kind = "registered_actor"
        else:
            if role_id not in PROVISIONAL:
                raise ValueError(f"Missing provisional entity for {role_id}")
            provisional_id, entity_kind = PROVISIONAL[role_id]
        result.append(
            {
                "role_id": role_id,
                "case_id": row["case_id"],
                "actor_id": actor_id,
                "provisional_entity_id": provisional_id,
                "entity_kind": entity_kind,
                "actor_name": row["actor_name"],
                "role": row["role"],
                "role_family": ROLE_FAMILY[row["role"]],
                "side": row["side"],
                "target_or_recipient": row["target_or_recipient"],
                "role_evidence_summary": row["role_evidence_summary"],
                "source_refs": normalize_source_refs(row["source_refs"]),
                "evidence_level": row["evidence_level"],
                "review_status": "human_checked",
                "human_decision": "accept",
                "human_reviewer": HUMAN_REVIEWER,
                "review_date": REVIEW_DATE,
                "interpretation_limit": row["interpretation_limit"],
            }
        )
    return result


def validate(
    cases: list[dict[str, str]],
    candidates: list[dict[str, str]],
    main_roles: list[dict[str, str]],
) -> None:
    case_index = unique_index(cases, ("case_id",))
    candidate_index = unique_index(candidates, ("role_id",))
    main_index = unique_index(main_roles, ("role_id",))
    if len(case_index) != 6 or len(candidate_index) != 27 or len(main_index) != 27:
        raise ValueError("HR-014 row-count invariant failed")
    if any(row["review_status"] != "human_checked" for row in cases + candidates + main_roles):
        raise ValueError("Every HR-014 case and role must be human_checked")
    if any(row["human_decision"] != "accept" for row in main_roles):
        raise ValueError("All 27 role decisions must be accept")

    _, actors = read_csv(ACTOR_PATH)
    actor_ids = {row["actor_id"] for row in actors}
    for row in main_roles:
        actor_id = row["actor_id"]
        provisional_id = row["provisional_entity_id"]
        if actor_id and actor_id not in actor_ids:
            raise ValueError(f"Broken actor FK on {row['role_id']}: {actor_id}")
        if bool(actor_id) == bool(provisional_id):
            raise ValueError(f"Exactly one entity identifier is required on {row['role_id']}")
        if provisional_id and provisional_id in actor_ids:
            raise ValueError(f"Provisional ID leaked into actor namespace: {provisional_id}")
        if row["case_id"] not in {key[0] for key in case_index}:
            raise ValueError(f"Broken case FK on {row['role_id']}: {row['case_id']}")

    _, sources = read_csv(SOURCE_PATH)
    source_ids = {row["source_id"] for row in sources}
    for row in cases:
        for ref in filter(None, row["primary_source_refs"].split(";")):
            if ref not in source_ids:
                raise ValueError(f"Unknown case source {ref} on {row['case_id']}")
    for row in main_roles:
        for ref in filter(None, row["source_refs"].split(";")):
            if ref not in source_ids:
                raise ValueError(f"Unknown role source {ref} on {row['role_id']}")

    expected_key_roles = {
        "R8R003": ("A020", "plaintiff"),
        "R8R005": ("A009", "counsel"),
        "R8R006": ("A002", "non_party"),
        "R8R007": ("A019", "non_party"),
        "R8R012": ("A052", "plaintiff"),
        "R8R013": ("", "counsel"),
        "R8R016": ("A053", "plaintiff"),
        "R8R020": ("A011", "requester"),
        "R8R025": ("A055", "supporter"),
        "R8R026": ("A020", "supporter"),
    }
    for role_id, (actor_id, family) in expected_key_roles.items():
        row = main_index[(role_id,)]
        if (row["actor_id"], row["role_family"]) != (actor_id, family):
            raise ValueError(f"Role-boundary invariant failed for {role_id}")

    a020 = {
        row["case_id"]: row["role_family"]
        for row in main_roles
        if row["actor_id"] == "A020"
    }
    if a020 != {"R8C01": "plaintiff", "R8C06": "supporter"}:
        raise ValueError(f"A020 cross-case roles were generalized: {a020}")
    if main_index[("R8R013",)]["provisional_entity_id"] != "P8E004":
        raise ValueError("Third Kadena counsel must remain a provisional procedural collective")

    required_case_phrases = {
        "R8C01": ("A002", "A019", "non-parties"),
        "R8C05": ("A011", "requester", "not a named"),
        "R8C06": ("first- and second-wave", "A055", "A020"),
    }
    for case_id, phrases in required_case_phrases.items():
        limit = case_index[(case_id,)]["interpretation_limit"]
        if not all(phrase in limit for phrase in phrases):
            raise ValueError(f"Missing interpretation boundary on {case_id}")


def main() -> None:
    case_fields, cases = read_csv(CASE_PATH)
    candidate_fields, candidates = read_csv(CANDIDATE_ROLE_PATH)

    update_cases(cases)
    update_candidate_roles(candidates)
    main_roles = build_main_roles(candidates)
    validate(cases, candidates, main_roles)

    write_csv(CASE_PATH, case_fields, cases)
    write_csv(CANDIDATE_ROLE_PATH, candidate_fields, candidates)
    write_csv(MAIN_ROLE_PATH, MAIN_ROLE_FIELDS, main_roles)

    print(
        "Merged HR-014: 6 cases human_checked; 27/27 roles accepted; "
        "registered-actor and provisional procedural nodes separated; validation passed."
    )


if __name__ == "__main__":
    main()
