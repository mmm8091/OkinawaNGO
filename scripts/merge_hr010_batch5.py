from __future__ import annotations

"""Merge the user-reviewed HR-010 batch 5 decisions (A102-A106).

The merge is deliberately idempotent. It updates the actor review state, adds
reviewed issue taxonomy/edges, records one unresolved canonical-name variant,
adds non-funding organizational/action relations, and appends the human review
log. It does not turn event participation into an alliance.
"""

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "interim"


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


ACTOR_UPDATES = {
    "A102": {
        "review_status": "human_checked",
        "notes": (
            "HR-010 batch 5: E4 identity and background/support role confirmed. "
            "National pollution-litigation lawyers coordination network founded 1972-01; "
            "connects environmental litigation practice with airport/base-noise legal teams. "
            "Use in R8 as a national legal support layer, not an Okinawa core organization."
        ),
    },
    "A103": {
        "review_status": "human_checked",
        "notes": (
            "HR-010 batch 5: E4 identity and background/support role confirmed. "
            "National plaintiffs network founded 2008-12-07 with seven member groups; "
            "A052 Kadena and A053 Futenma memberships are recorded as non-funding network relations."
        ),
    },
    "A104": {
        "review_status": "human_checked",
        "notes": (
            "HR-010 batch 5: E4 core/support legal-procedure actor confirmed. "
            "Futenma noise-litigation counsel team (about 30 mainly Okinawa lawyers), distinct from "
            "A053 plaintiff group; counsel relation recorded. Litigation generations remain linked "
            "to HR-011/HR-012 review."
        ),
    },
    "A105": {
        "review_status": "human_checked",
        "notes": (
            "HR-010 batch 5: E4 national YWCA identity and background/solidarity role confirmed. "
            "Henoko relevance is limited to the 2020 formal statement; do not infer a stable alliance. "
            "Keep distinct from local Okinawa YWCA candidate C009."
        ),
    },
    "A106": {
        "review_status": "human_checked",
        "notes": (
            "HR-010 batch 5: E4 mainland solidarity actor confirmed, active from 2018-06 in the "
            "Tokyo metropolitan area. Relations to A025 and A062 are event/partner-action links, "
            "not a stable alliance. Sources often use 首都圏キャンペーン; canonical-name choice "
            "remains a targeted alias check."
        ),
    },
}


NEW_ISSUES = [
    {
        "issue_id": "I020",
        "issue_label": "environment",
        "issue_group": "environment",
        "definition": "General environmental protection or pollution framing not limited to biodiversity",
        "include_in_phase1": "yes",
        "notes": "Added through HR-010 batch 5; keep distinct from biodiversity and specific pollution media.",
    },
    {
        "issue_id": "I021",
        "issue_label": "noise",
        "issue_group": "life_safety",
        "definition": "Aircraft and base noise as daily-life harm and litigation subject",
        "include_in_phase1": "yes",
        "notes": "Added through HR-010 batch 5 for Kadena/Futenma legal coordination.",
    },
    {
        "issue_id": "I022",
        "issue_label": "women",
        "issue_group": "peace_human_rights",
        "definition": "Women's organizations, gendered civic participation, and women-focused advocacy",
        "include_in_phase1": "yes",
        "notes": "Added through HR-010 batch 5; organization type alone does not imply political stance.",
    },
    {
        "issue_id": "I023",
        "issue_label": "human_rights",
        "issue_group": "peace_human_rights",
        "definition": "Human-rights framing in civic, legal, peace, or international advocacy",
        "include_in_phase1": "yes",
        "notes": "Added through HR-010 batch 5; code only when source-backed.",
    },
    {
        "issue_id": "I024",
        "issue_label": "solidarity",
        "issue_group": "collective_action",
        "definition": "Public solidarity or support action outside the Okinawa-local core",
        "include_in_phase1": "yes",
        "notes": "Added through HR-010 batch 5; solidarity action is not a stable alliance.",
    },
]


ISSUE_ID = {
    "anti_base": "I001",
    "Henoko": "I003",
    "life_safety": "I007",
    "legal": "I011",
    "peace": "I019",
    "environment": "I020",
    "noise": "I021",
    "women": "I022",
    "human_rights": "I023",
    "solidarity": "I024",
}


ACTOR_ISSUES = {
    "A102": ("legal", "environment", "noise", "life_safety"),
    "A103": ("noise", "life_safety", "legal", "anti_base"),
    "A104": ("noise", "life_safety", "legal", "anti_base"),
    "A105": ("women", "human_rights", "peace", "Henoko"),
    "A106": ("Henoko", "environment", "anti_base", "solidarity"),
}


ISSUE_BASIS = {
    "A102": "National pollution-litigation legal coordination includes airport/base-noise practice",
    "A103": "National base-noise plaintiff-group coordination and mutual support",
    "A104": "Futenma noise-litigation counsel role",
    "A105": "National YWCA women/human-rights/peace mission and 2020 Henoko statement",
    "A106": "Metropolitan-area public action opposing Henoko soil reclamation",
}


SOURCE_REFS = {
    "A102": "S121",
    "A103": "S122;S123",
    "A104": "S124",
    "A105": "S125",
    "A106": "S126;S127",
}


NEW_RELATIONS = [
    {
        "edge_id": "F037",
        "source_actor_id": "A103",
        "target_actor_id": "A052",
        "relation_type": "network_membership",
        "event_or_program": "全国基地爆音訴訟原告団連絡会議 membership — Kadena plaintiffs",
        "place": "Japan;Kadena",
        "evidence_level": "E4",
        "funding_relation_confidence": "not_funding_relation",
        "source_ref": "S122;S123",
        "review_status": "human_checked",
        "needs_local_retrieval": "no",
        "notes": "HR-010 batch 5: named member-group relationship; organizational coordination, not funding or alliance inference.",
    },
    {
        "edge_id": "F038",
        "source_actor_id": "A103",
        "target_actor_id": "A053",
        "relation_type": "network_membership",
        "event_or_program": "全国基地爆音訴訟原告団連絡会議 membership — Futenma plaintiffs",
        "place": "Japan;Futenma",
        "evidence_level": "E4",
        "funding_relation_confidence": "not_funding_relation",
        "source_ref": "S122;S123",
        "review_status": "human_checked",
        "needs_local_retrieval": "no",
        "notes": "HR-010 batch 5: named member-group relationship; organizational coordination, not funding or alliance inference.",
    },
    {
        "edge_id": "F039",
        "source_actor_id": "A104",
        "target_actor_id": "A053",
        "relation_type": "legal_counsel",
        "event_or_program": "Futenma base noise litigation",
        "place": "Futenma;Ginowan",
        "evidence_level": "E4",
        "funding_relation_confidence": "not_funding_relation",
        "source_ref": "S124",
        "review_status": "human_checked",
        "needs_local_retrieval": "no",
        "notes": "HR-010 batch 5: counsel-team to plaintiff-group role; A104 and A053 are distinct actors. Litigation generation crosswalk remains HR-011/HR-012.",
    },
    {
        "edge_id": "F040",
        "source_actor_id": "A106",
        "target_actor_id": "A025",
        "relation_type": "event_affiliation",
        "event_or_program": "Metropolitan Henoko soil-reclamation opposition actions from 2018",
        "place": "Tokyo;Henoko",
        "evidence_level": "E4",
        "funding_relation_confidence": "not_funding_relation",
        "source_ref": "S126",
        "review_status": "human_checked",
        "needs_local_retrieval": "no",
        "notes": "HR-010 batch 5: publicly described action linkage; event-level affiliation only, not a stable alliance.",
    },
    {
        "edge_id": "F041",
        "source_actor_id": "A106",
        "target_actor_id": "A062",
        "relation_type": "partner_action",
        "event_or_program": "JAWAN-recorded metropolitan Henoko campaign action",
        "place": "Tokyo;Henoko",
        "evidence_level": "E4",
        "funding_relation_confidence": "not_funding_relation",
        "source_ref": "S127",
        "review_status": "human_checked",
        "needs_local_retrieval": "no",
        "notes": "HR-010 batch 5: partner-action record; event-level public cooperation, not a stable alliance.",
    },
]


LOG_ROWS = [
    {
        "task_id": "HR-010",
        "object_id": actor_id,
        "review_date": "2026-07-13",
        "human_reviewer": "user",
        "review_status": "human_checked",
        "evidence_level_final": "E4",
        "publishable_claim": claim,
        "decision": decision,
        "review_note": ACTOR_UPDATES[actor_id]["notes"],
        "next_steps": next_steps,
    }
    for actor_id, claim, decision, next_steps in [
        ("A102", "National legal coordination network with base-noise relevance", "background_support", "Use in R8; do not present as Okinawa-local core."),
        ("A103", "National base-noise plaintiff network includes A052 and A053", "background_support", "Retain F037/F038 as membership, not funding."),
        ("A104", "Futenma counsel team is distinct from A053 plaintiff group", "core_support", "Reconcile litigation generations in HR-011/HR-012."),
        ("A105", "National YWCA issued a 2020 Henoko statement", "background_solidarity", "Keep statement-level; distinguish C009 Okinawa YWCA."),
        ("A106", "Metropolitan mainland solidarity campaign active from 2018", "background_solidarity", "Confirm whether 首都圏キャンペーン should replace or alias current canonical name."),
    ]
]


def main() -> None:
    actor_path = DATA / "01_actor_registry_initial_v0.csv"
    actor_fields, actors = read_csv(actor_path)
    found = set()
    for actor in actors:
        actor_id = actor["actor_id"]
        if actor_id in ACTOR_UPDATES:
            actor.update(ACTOR_UPDATES[actor_id])
            found.add(actor_id)
    missing = set(ACTOR_UPDATES) - found
    if missing:
        raise ValueError(f"Missing actors: {sorted(missing)}")
    write_csv(actor_path, actor_fields, actors)

    issue_path = DATA / "03_issue_taxonomy_v0.csv"
    issue_fields, issues = read_csv(issue_path)
    existing_issue_ids = {row["issue_id"] for row in issues}
    issues.extend(row for row in NEW_ISSUES if row["issue_id"] not in existing_issue_ids)
    write_csv(issue_path, issue_fields, issues)

    edge_path = DATA / "07_actor_issue_edges_initial_v0.csv"
    edge_fields, issue_edges = read_csv(edge_path)
    existing_pairs = {(row["actor_id"], row["issue_id"]) for row in issue_edges}
    used_edge_ids = {row["edge_id"] for row in issue_edges}
    next_id = 181
    for actor_id, labels in ACTOR_ISSUES.items():
        for label in labels:
            issue_id = ISSUE_ID[label]
            if (actor_id, issue_id) in existing_pairs:
                continue
            while f"AI{next_id:03d}" in used_edge_ids:
                next_id += 1
            edge_id = f"AI{next_id:03d}"
            issue_edges.append(
                {
                    "edge_id": edge_id,
                    "actor_id": actor_id,
                    "issue_id": issue_id,
                    "issue_label": label,
                    "relation_basis": ISSUE_BASIS[actor_id],
                    "source_ref": SOURCE_REFS[actor_id],
                    "evidence_level": "E4",
                    "review_status": "human_checked",
                    "notes": "HR-010 batch 5: issue tag and source basis human-confirmed; does not imply stable inter-organizational alliance.",
                }
            )
            existing_pairs.add((actor_id, issue_id))
            used_edge_ids.add(edge_id)
            next_id += 1
    write_csv(edge_path, edge_fields, issue_edges)

    alias_path = DATA / "02_actor_aliases_initial_v0.csv"
    alias_fields, aliases = read_csv(alias_path)
    alias_key = ("A106", "辺野古の海を土砂で埋めるな！首都圏キャンペーン")
    if alias_key not in {(row["actor_id"], row["alias"]) for row in aliases}:
        aliases.append(
            {
                "actor_id": alias_key[0],
                "alias": alias_key[1],
                "alias_type": "possible_canonical_variant",
                "source_ref": "S126",
                "notes": "HR-010 batch 5: source-preferred name; final canonical choice remains a targeted human check.",
            }
        )
    write_csv(alias_path, alias_fields, aliases)

    relation_path = DATA / "15_funding_or_support_edges_sample_v0.csv"
    relation_fields, relations = read_csv(relation_path)
    existing_relation_ids = {row["edge_id"] for row in relations}
    relations.extend(row for row in NEW_RELATIONS if row["edge_id"] not in existing_relation_ids)
    write_csv(relation_path, relation_fields, relations)

    log_path = DATA / "human_review_log_v0.csv"
    log_fields, logs = read_csv(log_path)
    existing_log_keys = {(row["task_id"], row["object_id"]) for row in logs}
    logs.extend(row for row in LOG_ROWS if (row["task_id"], row["object_id"]) not in existing_log_keys)
    write_csv(log_path, log_fields, logs)

    print(
        "Merged HR-010 batch 5: 5 actors, 5 issue categories, 20 actor-issue edges, "
        "1 alias, 5 non-funding relations, and 5 human-review log rows."
    )


if __name__ == "__main__":
    main()
