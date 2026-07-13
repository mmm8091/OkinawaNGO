from __future__ import annotations

"""Merge the user-reviewed HR-011 and HR-012 decisions.

The merge is deliberately idempotent and conservative:

* add A107-A110, while rejecting C015 as a registry actor;
* treat C026/C027 as litigation-round names of A052/A053;
* treat C028 as a dated predecessor of A010;
* add only source-backed issue and organizational/legal-role edges;
* mark every inter-actor edge as non-funding and explicitly non-alliance.

No source-log identifiers are allocated here. Existing S identifiers and the
registry-expansion SC candidate identifiers are retained for later source-log
normalization by the main thread.
"""

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "interim"
OUTPUT = ROOT / "outputs" / "registry_expansion_v1"


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def by_key(rows: list[dict[str, str]], fields: tuple[str, ...]) -> dict[tuple[str, ...], dict[str, str]]:
    result: dict[tuple[str, ...], dict[str, str]] = {}
    for row in rows:
        key = tuple(row[field] for field in fields)
        if key in result:
            raise ValueError(f"Duplicate key {fields}={key}")
        result[key] = row
    return result


def upsert_rows(
    rows: list[dict[str, str]],
    additions: list[dict[str, str]],
    key_fields: tuple[str, ...],
) -> None:
    index = by_key(rows, key_fields)
    for addition in additions:
        key = tuple(addition[field] for field in key_fields)
        if key in index:
            index[key].update(addition)
        else:
            new_row = dict(addition)
            rows.append(new_row)
            index[key] = new_row


def replace_row(rows: list[dict[str, str]], key_field: str, key_value: str, values: dict[str, str]) -> None:
    matches = [row for row in rows if row[key_field] == key_value]
    if len(matches) != 1:
        raise ValueError(f"Expected one {key_field}={key_value}, found {len(matches)}")
    matches[0].update(values)


NEW_ACTORS = [
    {
        "actor_id": "A107",
        "canonical_name": "沖縄YWCA",
        "actor_class": "womens_or_human_rights_ngo",
        "origin_type": "okinawa_local",
        "legal_status_guess": "association_or_regional_ywca",
        "primary_places": "Okinawa",
        "issue_tags": "women;human_rights;peace",
        "source_refs": "SC010",
        "evidence_level": "E3",
        "review_status": "human_checked",
        "needs_local_retrieval": "no",
        "review_priority": "P1",
        "notes": (
            "HR-011 user decision: add Okinawa YWCA as a local/regional YWCA actor, distinct from "
            "A105 Japan YWCA. The A105-to-A107 organizational affiliation is not funding or a "
            "movement alliance. Parent-body Okinawa/Henoko statements are not automatically coded "
            "as A107 actions. No person registry entry was created."
        ),
    },
    {
        "actor_id": "A108",
        "canonical_name": "沖縄を再び戦場にさせない県民の会",
        "actor_class": "citizen_network",
        "origin_type": "okinawa_local",
        "legal_status_guess": "informal_network",
        "primary_places": "Okinawa",
        "issue_tags": "frontline_prevention;Taiwan_contingency;peace",
        "source_refs": "SC013",
        "evidence_level": "E3",
        "review_status": "human_checked",
        "needs_local_retrieval": "no",
        "review_priority": "P1",
        "notes": (
            "HR-011 user decision: add the prefectural anti-war/frontline-prevention network formed "
            "in 2023. Public mobilization is event-level evidence, not proof of stable alliances. "
            "Named conveners remain source-level notes; no person registry entry was created."
        ),
    },
    {
        "actor_id": "A109",
        "canonical_name": "第4次嘉手納基地爆音差止訴訟弁護団",
        "actor_class": "lawyers_network",
        "origin_type": "okinawa_local",
        "legal_status_guess": "litigation_team",
        "primary_places": "Kadena;Okinawa",
        "issue_tags": "noise;life_safety;legal;anti_base",
        "source_refs": "SC026",
        "evidence_level": "E3",
        "review_status": "human_checked",
        "needs_local_retrieval": "no",
        "review_priority": "P1",
        "notes": (
            "HR-011 user decision: add the case-specific fourth Kadena counsel team. It is distinct "
            "from plaintiff-group A052; F042 records only the source-backed legal-counsel role, not "
            "funding or alliance. Do not infer a complete individual-lawyer roster."
        ),
    },
    {
        "actor_id": "A110",
        "canonical_name": "辺野古に基地を絶対つくらせない大阪行動",
        "actor_class": "citizen_group",
        "origin_type": "japan_domestic",
        "legal_status_guess": "informal_association",
        "primary_places": "Osaka;Henoko",
        "issue_tags": "Henoko;anti_base;solidarity",
        "source_refs": "SC041;SC042",
        "evidence_level": "E3",
        "review_status": "human_checked",
        "needs_local_retrieval": "no",
        "review_priority": "P2",
        "notes": (
            "HR-011 user decision: add as a sustained mainland-solidarity action actor. Keep it in "
            "the mainland solidarity layer rather than the Okinawa-local core. Public actions and "
            "solidarity do not establish a stable alliance or funding relation."
        ),
    },
]


ACTOR_REVISIONS = {
    "A010": {
        "source_refs": "S016;S017;SC032",
        "review_status": "human_checked",
        "notes": (
            "HR-012 user decision: 石垣島への自衛隊配備を止める住民の会 began on "
            "2015-08-20 and is recorded as predecessor_of A010. A010 was organized in 2016-09 as "
            "a wider coalition including that group, neighborhood associations, unions, peace/civic "
            "groups, councillors and individuals. This lineage does not make every predecessor member "
            "or action interchangeable with A010."
        ),
    },
    "A052": {
        "canonical_name": "嘉手納基地爆音差止訴訟原告団",
        "issue_tags": "legal;life_safety;noise;anti_base",
        "source_refs": "S026;SC029;SC030",
        "evidence_level": "E4",
        "review_status": "human_checked",
        "notes": (
            "HR-012 user decision: canonicalized as the cross-round Kadena base-noise injunction "
            "plaintiff-group actor. 第4次嘉手納基地爆音差止訴訟原告団 is a round_of A052, not a "
            "new actor. Litigation-round participants must not be assumed identical across time."
        ),
    },
    "A053": {
        "canonical_name": "普天間基地爆音訴訟原告団",
        "issue_tags": "legal;life_safety;noise;anti_base",
        "source_refs": "S027;SC031",
        "evidence_level": "E4",
        "review_status": "human_checked",
        "notes": (
            "HR-012 user decision: canonicalized as the cross-round Futenma base-noise plaintiff-group "
            "actor. 普天間基地第2次爆音訴訟原告団 is a round_of A053, not a new actor. Litigation-"
            "round participants must not be assumed identical across time."
        ),
    },
}


ALIASES = [
    {
        "actor_id": "A052",
        "alias": "嘉手納爆音訴訟原告団",
        "alias_type": "former_canonical",
        "source_ref": "S026",
        "notes": "HR-012: previous registry canonical name; retained for lookup after canonical-name normalization.",
    },
    {
        "actor_id": "A052",
        "alias": "第4次嘉手納基地爆音差止訴訟原告団",
        "alias_type": "round_of",
        "source_ref": "SC029;SC030",
        "notes": "HR-012: fourth-round case designation of A052; no separate actor created and cross-round membership is not assumed identical.",
    },
    {
        "actor_id": "A053",
        "alias": "普天間爆音訴訟団",
        "alias_type": "former_canonical",
        "source_ref": "S027",
        "notes": "HR-012: previous registry canonical name; retained for lookup after canonical-name normalization.",
    },
    {
        "actor_id": "A053",
        "alias": "普天間基地第2次爆音訴訟原告団",
        "alias_type": "round_of",
        "source_ref": "SC031",
        "notes": "HR-012: second-round case designation of A053; no separate actor created and cross-round membership is not assumed identical.",
    },
    {
        "actor_id": "A010",
        "alias": "石垣島への自衛隊配備を止める住民の会",
        "alias_type": "predecessor_of",
        "source_ref": "SC032",
        "notes": (
            "HR-012: predecessor formed 2015-08-20; A010 emerged as a wider coalition in 2016-09. "
            "This is lineage metadata, not a claim that both names denote an identical organization."
        ),
    },
]


ISSUE_EDGES = [
    ("AI201", "A107", "I022", "women", "Okinawa YWCA regional identity and women-focused mission", "SC010", "E3"),
    ("AI202", "A107", "I023", "human_rights", "Okinawa YWCA regional identity and human-rights mission", "SC010", "E3"),
    ("AI203", "A107", "I019", "peace", "Okinawa YWCA regional identity and peace mission", "SC010", "E3"),
    ("AI204", "A108", "I017", "frontline_prevention", "2023 prefectural network formed to oppose Okinawa becoming a battlefield again", "SC013", "E3"),
    ("AI205", "A108", "I018", "Taiwan_contingency", "Public framing connects Okinawa frontline risk to regional contingency debates", "SC013", "E3"),
    ("AI206", "A108", "I019", "peace", "Prefectural anti-war and peace mobilization", "SC013", "E3"),
    ("AI207", "A109", "I021", "noise", "Fourth Kadena base-noise injunction litigation counsel role", "SC026", "E3"),
    ("AI208", "A109", "I007", "life_safety", "Fourth Kadena litigation addresses residents' daily noise harm", "SC026", "E3"),
    ("AI209", "A109", "I011", "legal", "Case-specific legal representation in fourth Kadena litigation", "SC026", "E3"),
    ("AI210", "A109", "I001", "anti_base", "Flight-injunction claim concerning Kadena base-noise burden", "SC026", "E3"),
    ("AI211", "A110", "I003", "Henoko", "Sustained Osaka public actions opposing Henoko base construction", "SC041;SC042", "E3"),
    ("AI212", "A110", "I001", "anti_base", "Sustained Osaka public actions opposing Henoko base construction", "SC041;SC042", "E3"),
    ("AI213", "A110", "I024", "solidarity", "Mainland public solidarity actions concerning Henoko", "SC041;SC042", "E3"),
    ("AI214", "A052", "I021", "noise", "Cross-round Kadena base-noise plaintiff-group role", "S026;SC029;SC030", "E4"),
    ("AI215", "A053", "I021", "noise", "Cross-round Futenma base-noise plaintiff-group role", "S027;SC031", "E4"),
]


ISSUE_EDGE_ROWS = [
    {
        "edge_id": edge_id,
        "actor_id": actor_id,
        "issue_id": issue_id,
        "issue_label": issue_label,
        "relation_basis": basis,
        "source_ref": source_ref,
        "evidence_level": evidence_level,
        "review_status": "human_checked",
        "notes": (
            "HR-011/HR-012 user-reviewed issue coding. Issue association does not imply a stable "
            "inter-organizational alliance or funding relation."
        ),
    }
    for edge_id, actor_id, issue_id, issue_label, basis, source_ref, evidence_level in ISSUE_EDGES
]


RELATIONS = [
    {
        "edge_id": "F042",
        "source_actor_id": "A109",
        "target_actor_id": "A052",
        "relation_type": "legal_counsel",
        "event_or_program": "Fourth Kadena Base Noise Injunction Lawsuit",
        "place": "Kadena;Okinawa",
        "evidence_level": "E3",
        "funding_relation_confidence": "not_funding_relation",
        "source_ref": "SC026",
        "review_status": "human_checked",
        "needs_local_retrieval": "no",
        "notes": (
            "HR-011/HR-012: source-backed case-specific counsel-team to plaintiff-group role. "
            "This is neither a funding relation nor evidence of a stable alliance."
        ),
    },
    {
        "edge_id": "F043",
        "source_actor_id": "A105",
        "target_actor_id": "A107",
        "relation_type": "organizational_affiliation",
        "event_or_program": "Japan YWCA regional-YWCA structure — Okinawa YWCA",
        "place": "Japan;Okinawa",
        "evidence_level": "E3",
        "funding_relation_confidence": "not_funding_relation",
        "source_ref": "SC010",
        "review_status": "human_checked",
        "needs_local_retrieval": "no",
        "notes": (
            "HR-011: umbrella-to-regional-organization direction. Organizational affiliation is "
            "not funding and does not transfer every A105 statement/action to A107 or prove a "
            "movement alliance."
        ),
    },
]


LOG_ROWS = [
    {
        "task_id": "HR-011",
        "object_id": "A107",
        "review_date": "2026-07-13",
        "human_reviewer": "user",
        "review_status": "human_checked",
        "evidence_level_final": "E3",
        "publishable_claim": "Okinawa YWCA is a distinct local/regional YWCA actor",
        "decision": "add",
        "review_note": "Add A107; keep distinct from A105 and record only umbrella-to-regional organizational affiliation.",
        "next_steps": "Main thread may normalize SC010 to a source-log ID; do not create person actors from named participants.",
    },
    {
        "task_id": "HR-011",
        "object_id": "A108",
        "review_date": "2026-07-13",
        "human_reviewer": "user",
        "review_status": "human_checked",
        "evidence_level_final": "E3",
        "publishable_claim": "Prefectural network publicly mobilizes against Okinawa becoming a battlefield again",
        "decision": "add",
        "review_note": "Add A108; event participation and mobilization do not establish stable alliances.",
        "next_steps": "Main thread may normalize SC013; named conveners remain outside the organization registry.",
    },
    {
        "task_id": "HR-011",
        "object_id": "C015",
        "review_date": "2026-07-13",
        "human_reviewer": "user",
        "review_status": "human_checked",
        "evidence_level_final": "insufficient_for_actor_entry",
        "publishable_claim": "No registry-level identity claim approved",
        "decision": "reject_no_actor",
        "review_note": "Do not add C015; current material does not safely close the named organization identity and issue attribution.",
        "next_steps": "Retain only in rejected-candidate provenance; reconsider only with direct organization or local primary material.",
    },
    {
        "task_id": "HR-011",
        "object_id": "A109",
        "review_date": "2026-07-13",
        "human_reviewer": "user",
        "review_status": "human_checked",
        "evidence_level_final": "E3",
        "publishable_claim": "Fourth Kadena lawsuit counsel team is distinct from the plaintiff group",
        "decision": "add",
        "review_note": "Add A109 and legal-counsel edge to A052; no complete person roster is inferred.",
        "next_steps": "Normalize SC026 later; do not create person-registry entries from counsel names.",
    },
    {
        "task_id": "HR-011",
        "object_id": "A110",
        "review_date": "2026-07-13",
        "human_reviewer": "user",
        "review_status": "human_checked",
        "evidence_level_final": "E3",
        "publishable_claim": "Osaka group conducts sustained mainland solidarity actions concerning Henoko",
        "decision": "add_background_solidarity",
        "review_note": "Add A110 in the mainland-solidarity layer; public action is not a stable alliance or funding relation.",
        "next_steps": "Normalize SC041/SC042 later and preserve Okinawa-local versus mainland-layer distinction.",
    },
    {
        "task_id": "HR-012",
        "object_id": "C026",
        "review_date": "2026-07-13",
        "human_reviewer": "user",
        "review_status": "human_checked",
        "evidence_level_final": "E4",
        "publishable_claim": "Fourth Kadena plaintiff-group name is a litigation round of A052",
        "decision": "round_of_A052",
        "review_note": "Do not create a new actor; store the fourth-round name as round_of A052.",
        "next_steps": "Do not infer identical plaintiff membership across litigation rounds.",
    },
    {
        "task_id": "HR-012",
        "object_id": "C027",
        "review_date": "2026-07-13",
        "human_reviewer": "user",
        "review_status": "human_checked",
        "evidence_level_final": "E4",
        "publishable_claim": "Second Futenma plaintiff-group name is a litigation round of A053",
        "decision": "round_of_A053",
        "review_note": "Do not create a new actor; store the second-round name as round_of A053.",
        "next_steps": "Do not infer identical plaintiff membership across litigation rounds.",
    },
    {
        "task_id": "HR-012",
        "object_id": "C028",
        "review_date": "2026-07-13",
        "human_reviewer": "user",
        "review_status": "human_checked",
        "evidence_level_final": "E3",
        "publishable_claim": "2015 Ishigaki residents group is a predecessor of A010",
        "decision": "predecessor_of_A010",
        "review_note": "No new actor; group formed 2015-08-20 and A010 emerged as a wider coalition in 2016-09.",
        "next_steps": "Keep lineage distinct from identity; named organizers remain source-level pending a person table.",
    },
]


def validate_source_refs(source_refs: set[str]) -> None:
    _, source_rows = read_csv(DATA / "05_source_log_initial_v0.csv")
    source_ids = {row["source_id"] for row in source_rows}
    _, candidate_rows = read_csv(OUTPUT / "source_candidates_v1.csv")
    candidate_ids = {row["source_candidate_id"] for row in candidate_rows}
    allowed = source_ids | candidate_ids
    missing: set[str] = set()
    for refs in source_refs:
        for ref in refs.split(";"):
            ref = ref.strip()
            if ref and ref not in allowed and not ref.startswith(("http://", "https://")):
                missing.add(ref)
    if missing:
        raise ValueError(f"Unknown source refs: {sorted(missing)}")


def validate(
    actors: list[dict[str, str]],
    aliases: list[dict[str, str]],
    issues: list[dict[str, str]],
    issue_edges: list[dict[str, str]],
    relations: list[dict[str, str]],
    logs: list[dict[str, str]],
) -> None:
    actor_index = by_key(actors, ("actor_id",))
    by_key(actors, ("canonical_name",))
    by_key(aliases, ("actor_id", "alias"))
    issue_index = by_key(issues, ("issue_id",))
    by_key(issue_edges, ("edge_id",))
    by_key(issue_edges, ("actor_id", "issue_id"))
    by_key(relations, ("edge_id",))
    by_key(logs, ("task_id", "object_id"))

    for actor_id in ("A107", "A108", "A109", "A110"):
        if (actor_id,) not in actor_index:
            raise ValueError(f"Missing reviewed actor {actor_id}")
    rejected_name = "宮古島・命の水・自衛隊配備について考える会"
    if any(row["canonical_name"] == rejected_name for row in actors):
        raise ValueError("C015 was rejected but appears in the actor registry")
    forbidden_ids = {"A112", "A113", "A114"}
    if forbidden_ids & {key[0] for key in actor_index}:
        raise ValueError("HR-012 round/predecessor candidates must not create actors")

    expected_aliases = {
        ("A052", "第4次嘉手納基地爆音差止訴訟原告団", "round_of"),
        ("A053", "普天間基地第2次爆音訴訟原告団", "round_of"),
        ("A010", "石垣島への自衛隊配備を止める住民の会", "predecessor_of"),
    }
    actual_aliases = {(row["actor_id"], row["alias"], row["alias_type"]) for row in aliases}
    if not expected_aliases <= actual_aliases:
        raise ValueError("Missing HR-012 round/predecessor alias metadata")

    for edge in issue_edges:
        if (edge["actor_id"],) not in actor_index or (edge["issue_id"],) not in issue_index:
            raise ValueError(f"Broken actor-issue FK: {edge}")
    for relation in relations:
        for field in ("source_actor_id", "target_actor_id"):
            value = relation[field]
            if value.startswith("A") and (value,) not in actor_index:
                raise ValueError(f"Broken relation actor FK: {field}={value}")
    for edge_id in ("F042", "F043"):
        row = next((row for row in relations if row["edge_id"] == edge_id), None)
        if not row or row["funding_relation_confidence"] != "not_funding_relation":
            raise ValueError(f"{edge_id} must be explicitly non-funding")
        if "alliance" not in row["notes"].lower():
            raise ValueError(f"{edge_id} must include an explicit non-alliance limit")

    expected_logs = {
        ("HR-011", "A107"), ("HR-011", "A108"), ("HR-011", "C015"),
        ("HR-011", "A109"), ("HR-011", "A110"), ("HR-012", "C026"),
        ("HR-012", "C027"), ("HR-012", "C028"),
    }
    if not expected_logs <= {(row["task_id"], row["object_id"]) for row in logs}:
        raise ValueError("Missing HR-011/HR-012 human-review log rows")

    refs = {row["source_refs"] for row in actors if row["actor_id"] in {"A010", "A052", "A053", "A107", "A108", "A109", "A110"}}
    refs |= {row["source_ref"] for row in ALIASES + ISSUE_EDGE_ROWS + RELATIONS}
    validate_source_refs(refs)


def main() -> None:
    actor_path = DATA / "01_actor_registry_initial_v0.csv"
    actor_fields, actors = read_csv(actor_path)
    for actor_id, revision in ACTOR_REVISIONS.items():
        replace_row(actors, "actor_id", actor_id, revision)
    upsert_rows(actors, NEW_ACTORS, ("actor_id",))

    alias_path = DATA / "02_actor_aliases_initial_v0.csv"
    alias_fields, aliases = read_csv(alias_path)
    upsert_rows(aliases, ALIASES, ("actor_id", "alias"))

    issue_path = DATA / "03_issue_taxonomy_v0.csv"
    _, issues = read_csv(issue_path)

    issue_edge_path = DATA / "07_actor_issue_edges_initial_v0.csv"
    issue_edge_fields, issue_edges = read_csv(issue_edge_path)
    upsert_rows(issue_edges, ISSUE_EDGE_ROWS, ("actor_id", "issue_id"))

    relation_path = DATA / "15_funding_or_support_edges_sample_v0.csv"
    relation_fields, relations = read_csv(relation_path)
    upsert_rows(relations, RELATIONS, ("source_actor_id", "target_actor_id", "relation_type"))

    log_path = DATA / "human_review_log_v0.csv"
    log_fields, logs = read_csv(log_path)
    upsert_rows(logs, LOG_ROWS, ("task_id", "object_id"))

    validate(actors, aliases, issues, issue_edges, relations, logs)

    write_csv(actor_path, actor_fields, actors)
    write_csv(alias_path, alias_fields, aliases)
    write_csv(issue_edge_path, issue_edge_fields, issue_edges)
    write_csv(relation_path, relation_fields, relations)
    write_csv(log_path, log_fields, logs)

    print(
        "Merged HR-011/HR-012: added A107-A110, rejected C015, normalized A052/A053, "
        "recorded three round/lineage dispositions, 15 issue edges, 2 non-funding relations, "
        "and 8 human-review log rows. Validation passed."
    )


if __name__ == "__main__":
    main()
