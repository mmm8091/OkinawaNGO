from __future__ import annotations

"""Merge the project-principal HR-027 registry decisions.

The merge keeps three evidence layers separate:

* A112-A115 are human-checked registry actors;
* issue/place rows are AI-seeded candidates created from the accepted registry
  fields, not publication-approved relationship claims;
* event descriptions remain in a dedicated review queue and are not inserted
  into the central AEV table.

No inter-actor relation or funding edge is created.  The script is idempotent.
"""

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "interim"
GATE = ROOT / "outputs" / "registry_value_gate_v2"
OUT = ROOT / "outputs" / "hr027_integration_v1"


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def upsert(rows: list[dict[str, str]], additions: list[dict[str, str]], keys: tuple[str, ...]) -> None:
    index = {tuple(row[k] for k in keys): row for row in rows}
    if len(index) != len(rows):
        raise ValueError(f"Duplicate existing key for {keys}")
    for addition in additions:
        key = tuple(addition[k] for k in keys)
        if key in index:
            index[key].update(addition)
        else:
            rows.append(dict(addition))
            index[key] = rows[-1]


ACTORS = [
    {
        "actor_id": "A112",
        "canonical_name": "宮古島地下水研究会",
        "actor_class": "citizen_group",
        "origin_type": "okinawa_local",
        "legal_status_guess": "informal_association",
        "primary_places": "Miyako",
        "issue_tags": "groundwater;health_risk;life_safety;environment",
        "source_refs": "S158;S204;S269;S270;S271;S272",
        "evidence_level": "E4",
        "review_status": "human_checked",
        "needs_local_retrieval": "no",
        "review_priority": "P1",
        "notes": (
            "HR-027 project-principal decision (2026-07-16): add. Sustained Miyako civic research/advocacy "
            "actor with rules, named leadership history and a documented municipal response. It frames SDF-facility "
            "wastewater as a groundwater risk and advocates monitoring/regulation; this does not prove contamination "
            "or health damage. Keep C015, A012 and A097 separate; no affiliation or succession edge was approved."
        ),
    },
    {
        "actor_id": "A113",
        "canonical_name": "宜野湾ちゅら水会",
        "actor_class": "citizen_group",
        "origin_type": "okinawa_local",
        "legal_status_guess": "informal",
        "primary_places": "Ginowan;Futenma",
        "issue_tags": "groundwater;health_risk;life_safety;environment;legal",
        "source_refs": "S273;S274;S275;S276;S277;S278;S279",
        "evidence_level": "E4",
        "review_status": "human_checked",
        "needs_local_retrieval": "no",
        "review_priority": "P1",
        "notes": (
            "HR-027 project-principal decision (2026-07-16): add. Documented since no later than 2021-11, with "
            "resident-funded sampling, requests, petition/procedure use and international-mechanism reporting. Claims "
            "are limited to observed actions: do not infer PFAS health causation, source attribution or procedural effect. "
            "A099 is a distinct actor; co-participation and personnel overlap do not establish an alliance."
        ),
    },
    {
        "actor_id": "A114",
        "canonical_name": "全日本港湾労働組合沖縄地方本部",
        "actor_class": "labor_union",
        "origin_type": "okinawa_local",
        "legal_status_guess": "labor_union",
        "primary_places": "Naha;Ishigaki",
        "issue_tags": "anti_base;anti_military;peace;life_safety;mobilization",
        "source_refs": "S284;S285;S286;S287;S288;S289",
        "evidence_level": "E4",
        "review_status": "human_checked",
        "needs_local_retrieval": "no",
        "review_priority": "P1",
        "notes": (
            "HR-027 project-principal decision (2026-07-16): add the Okinawa regional headquarters, distinct from "
            "the national union. Official records support identity/continuity and dated Naha/Ishigaki actions, including "
            "the executed 2024 Ishigaki Port strike. Record occurrence and the union's workplace-safety framing only; "
            "do not adjudicate legality, effect, political impact or stable alliances."
        ),
    },
    {
        "actor_id": "A115",
        "canonical_name": "新日本婦人の会沖縄県本部",
        "actor_class": "womens_or_community_organization",
        "origin_type": "okinawa_local",
        "legal_status_guess": "informal_association",
        "primary_places": "Okinawa",
        "issue_tags": "women;human_rights;peace;anti_base;referendum",
        "source_refs": "S280;S254;S281;S282;S283",
        "evidence_level": "E4",
        "review_status": "human_checked",
        "needs_local_retrieval": "yes",
        "review_priority": "P1",
        "notes": (
            "HR-027 project-principal decision (2026-07-16): add the Okinawa prefectural headquarters as a branch-level "
            "actor. Official and dated records support local requests and the 2018 Henoko-referendum signature campaign. "
            "National-body actions are not transferred automatically; do not infer party affiliation, electoral effect "
            "or alliances with other women's organizations. The 2019-2021 local archive gap is non-blocking Tier-2 work."
        ),
    },
]


ALIASES = [
    {
        "actor_id": "A113",
        "alias": "ちゅら水会",
        "alias_type": "context_limited_alias",
        "source_ref": "S273;S274",
        "notes": "HR-027: valid only in explicit Ginowan context; 名護ちゅら水会 is a separate near-name, so display/search must retain the Ginowan qualifier.",
    },
    {
        "actor_id": "A114",
        "alias": "全港湾沖縄地方本部",
        "alias_type": "short_name",
        "source_ref": "S289",
        "notes": "HR-027 accepted branch-qualified short form; do not collapse into the national 全港湾 organization.",
    },
    {
        "actor_id": "A114",
        "alias": "全港湾沖縄",
        "alias_type": "media_short_name",
        "source_ref": "S286",
        "notes": "HR-027 accepted media headline form; branch context remains mandatory.",
    },
    {
        "actor_id": "A115",
        "alias": "新婦人沖縄県本部",
        "alias_type": "short_name",
        "source_ref": "S283",
        "notes": "HR-027 accepted prefecture-qualified short form. Bare 新婦人 refers to the national organization and is rejected as an unconditional alias.",
    },
]


ISSUE_SPECS = {
    "A112": [
        ("I006", "groundwater", "Research, monitoring and ordinance advocacy concerning Miyako groundwater", "S269;S270;S271"),
        ("I008", "health_risk", "Public risk framing around substances that could affect drinking-water sources", "S269;S270"),
        ("I007", "life_safety", "Drinking-water-source protection and monitoring advocacy", "S270;S271"),
        ("I020", "environment", "Groundwater conservation research and public-policy advocacy", "S158;S204;S270"),
    ],
    "A113": [
        ("I006", "groundwater", "PFAS sampling and groundwater investigation requests in Ginowan/Futenma", "S273;S274;S276;S277"),
        ("I008", "health_risk", "Requests for exposure/health investigation and bounded PFAS risk communication", "S273;S276"),
        ("I007", "life_safety", "Resident-led sampling and requests concerning school/community safety", "S274;S275;S278"),
        ("I020", "environment", "PFAS contamination monitoring and administrative requests", "S273;S274;S277"),
        ("I011", "legal", "Use of petition and pollution-mediation procedures", "S273;S274"),
    ],
    "A114": [
        ("I001", "anti_base", "Dated protest actions opposing Henoko/base-related military use", "S286;S289"),
        ("I002", "anti_military", "Port/workplace actions concerning military port use and exercises", "S287;S288"),
        ("I019", "peace", "Participation in peace-march and anti-security-law activity", "S286;S289"),
        ("I007", "life_safety", "Union's stated port-worker occupational-safety framing", "S287;S288"),
        ("I026", "mobilization", "Union capacity expressed through rally, strike and march repertoires", "S286;S288;S289"),
    ],
    "A115": [
        ("I022", "women", "Prefectural women's membership organization and local-unit activity", "S280;S282;S283"),
        ("I023", "human_rights", "Dated requests concerning U.S.-military sexual violence", "S281;S282"),
        ("I019", "peace", "Local requests and public action framed through peace and women's rights", "S281;S282"),
        ("I001", "anti_base", "Dated Okinawa-headquarters activity concerning Henoko/base burdens", "S254;S281;S283"),
        ("I010", "referendum", "2018 Henoko prefectural-referendum signature mobilization", "S283"),
    ],
}


PLACE_SPECS = [
    ("A112", "P013", "Miyako", "Documented organization location and Miyako municipal/groundwater field", "S158;S204;S271"),
    ("A113", "P018", "Ginowan", "Documented resident group and municipal-request field", "S273;S274;S276;S277"),
    ("A113", "P004", "Futenma", "Issue/action site associated with sampling and base-groundwater requests; not a headquarters claim", "S274;S275;S277"),
    ("A114", "P020", "Naha", "Formal regional-headquarters location in Naha; event venues remain in the separate event queue", "S284;S285"),
    ("A114", "P012", "Ishigaki", "Documented 2024 port strike/action venue; not an organizational headquarters claim", "S287;S288"),
    ("A115", "P001", "Okinawa Prefecture", "Prefectural-headquarters scope and prefecture-wide requests/signature activity", "S280;S282;S283"),
]


EVENTS = [
    ("HR027E001", "A112", "2020-12", "Miyako mayoral-candidate public questionnaire", "questionnaire", "Miyako", "municipal election candidates", "S272"),
    ("HR027E002", "A112", "2022-07/2023-02", "Groundwater opinion and Miyako City written response", "administrative_exchange", "Miyako", "Miyako City", "S271"),
    ("HR027E003", "A112", "2025-02", "6,524-signature submission and request to new mayor", "petition_request", "Miyako", "Miyako mayor/city", "S204"),
    ("HR027E004", "A113", "2022-08/09", "Futenma No.2 Elementary School soil sampling", "resident_sampling", "Ginowan;Futenma", "school/community environment", "S274;S275"),
    ("HR027E005", "A113", "2022-12", "Ginowan City Council Petition No.1 review", "petition", "Ginowan", "Ginowan City Council", "S273;S274"),
    ("HR027E006", "A113", "2024-07/09", "PFAS reporting through EMRIP and CEDAW mechanisms", "international_reporting", "international", "UN mechanisms", "S273"),
    ("HR027E007", "A113", "2025-10-27", "Pollution mediation application", "legal_administrative_procedure", "Okinawa", "Okinawa Pollution Examination Commission", "S273"),
    ("HR027E008", "A113", "2026-01/03", "Isa foam-event sampling and municipal request", "sampling_request", "Ginowan", "Ginowan City", "S278"),
    ("HR027E009", "A114", "2015-09-18", "Naha port-worker protest rally", "rally", "Naha", "security legislation/Henoko policy", "S286"),
    ("HR027E010", "A114", "2024-03-11/13", "Ishigaki Port strike", "strike", "Ishigaki", "military use of civilian port", "S287;S288"),
    ("HR027E011", "A114", "2024-10", "Keen Sword 25 Naha Port protest", "protest", "Naha", "Japan-U.S. exercise port use", "S289"),
    ("HR027E012", "A114", "2025-05", "5.15 Peace March participation", "march", "Okinawa", "base burden/peace public", "S289"),
    ("HR027E013", "A115", "2008-02-14", "Prefectural request concerning U.S.-Marine sexual assault", "request", "Okinawa", "Okinawa governor's office", "S282"),
    ("HR027E014", "A115", "2018-06-17", "Henoko prefectural-referendum signature launch", "signature_mobilization", "Okinawa", "prefectural referendum ordinance process", "S283"),
    ("HR027E015", "A115", "2022-09-20", "Request to 41 municipalities and education heads", "request_letter", "Okinawa", "41 municipalities and education authorities", "S280"),
    ("HR027E016", "A115", "2024-06/07", "National-plus-prefectural joint requests on military sexual violence", "joint_request", "Tokyo/Okinawa", "national ministries", "S281"),
    ("HR027E017", "A115", "2025-10-17", "Protest letter to prefectural assembly speaker", "protest_letter", "Okinawa", "Okinawa Prefectural Assembly speaker", "S280"),
]


NEAR_NAMES = [
    ("NN027-01", "A112", "宮古の地下水を守る会", "separate_unregistered_group", "A 2025 independent group; not an alias of 宮古島地下水研究会 and no merger/personnel-overlap claim is approved."),
    ("NN027-02", "A113", "名護ちゅら水会", "separate_unregistered_group", "A Nago-area group with a globally ambiguous short name; do not resolve bare ちゅら水会 without place context."),
    ("NN027-03", "A115", "新日本婦人の会沖縄県支部", "unresolved_name_form", "A ti-da blog self-title that does not match the verified 県本部 hierarchy; do not merge until independently resolved."),
]


def main() -> None:
    actor_fields, actors = read_csv(DATA / "01_actor_registry_initial_v0.csv")
    alias_fields, aliases = read_csv(DATA / "02_actor_aliases_initial_v0.csv")
    issue_fields, issue_rows = read_csv(DATA / "07_actor_issue_edges_initial_v0.csv")
    place_fields, place_rows = read_csv(DATA / "08_actor_place_edges_initial_v0.csv")
    log_fields, log_rows = read_csv(DATA / "human_review_log_v0.csv")
    review_fields, review_rows = read_csv(GATE / "HR027_registry_value_review_v0.csv")

    upsert(actors, ACTORS, ("actor_id",))
    upsert(aliases, ALIASES, ("actor_id", "alias"))

    new_issue_rows: list[dict[str, str]] = []
    edge_number = 223
    for actor_id in ("A112", "A113", "A114", "A115"):
        for issue_id, label, basis, refs in ISSUE_SPECS[actor_id]:
            new_issue_rows.append(
                {
                    "edge_id": f"AI{edge_number:03d}",
                    "actor_id": actor_id,
                    "issue_id": issue_id,
                    "issue_label": label,
                    "relation_basis": basis,
                    "source_ref": refs,
                    "evidence_level": "E4",
                    "review_status": "ai_seeded",
                    "notes": "HR-027 accepted the registry issue_tags field; this edge-level formulation remains a candidate and is not publication-approved. Apply the actor notes' no-causality/no-alliance boundary.",
                }
            )
            edge_number += 1
    upsert(issue_rows, new_issue_rows, ("edge_id",))

    new_place_rows: list[dict[str, str]] = []
    for number, (actor_id, place_id, place_name, basis, refs) in enumerate(PLACE_SPECS, start=130):
        new_place_rows.append(
            {
                "edge_id": f"AP{number:03d}",
                "actor_id": actor_id,
                "place_id": place_id,
                "place_name": place_name,
                "relation_basis": basis,
                "source_ref": refs,
                "evidence_level": "E4",
                "review_status": "ai_seeded",
                "notes": "HR-027 accepted the primary_places field; this place-edge semantic is a candidate pending dedicated edge review. Venue/issue site is not automatically headquarters or stable presence.",
            }
        )
    upsert(place_rows, new_place_rows, ("edge_id",))

    decision_notes = {
        "HR027-RV2C001": "add as A112; E4 human_checked; bounded Miyako groundwater research/advocacy actor; no contamination-causality or relation-edge inference; see human_review_return_HR027_v1.md §1.",
        "HR027-RV2C002": "add as A113; E4 human_checked; bounded Ginowan/Futenma PFAS sampling/request/procedure actor; keep A099 separate; see return §2.",
        "HR027-RV2C004": "add as A114; E4 human_checked; regional port labor actor; occurrence and stated safety frame only, not strike legality/effect; see return §3.",
        "HR027-RV2C003": "add as A115; E4 human_checked; prefectural women's branch actor and referendum channel; do not transfer national-body actions; see return §4.",
    }
    for row in review_rows:
        if row["task_id"] in decision_notes:
            row.update(
                {
                    "decision": "add",
                    "reviewer": "project_principal_user",
                    "review_date": "2026-07-16",
                    "review_note": decision_notes[row["task_id"]],
                }
            )

    log_additions = [
        {
            "task_id": "HR-027", "object_id": actor["actor_id"], "review_date": "2026-07-16",
            "human_reviewer": "project_principal_user", "review_status": "human_checked",
            "evidence_level_final": "E4", "publishable_claim": actor["notes"].split(". ")[1],
            "decision": "add", "review_note": f"Registry admission approved for {actor['canonical_name']}; issue/place edges remain candidates and events remain outside central AEV.",
            "next_steps": "Review candidate issue/place semantics and event rows; do not create inter-actor relations from co-participation.",
        }
        for actor in ACTORS
    ]
    upsert(log_rows, log_additions, ("task_id", "object_id"))

    write_csv(DATA / "01_actor_registry_initial_v0.csv", actor_fields, actors)
    write_csv(DATA / "02_actor_aliases_initial_v0.csv", alias_fields, aliases)
    write_csv(DATA / "07_actor_issue_edges_initial_v0.csv", issue_fields, issue_rows)
    write_csv(DATA / "08_actor_place_edges_initial_v0.csv", place_fields, place_rows)
    write_csv(DATA / "human_review_log_v0.csv", log_fields, log_rows)
    write_csv(GATE / "HR027_registry_value_review_v0.csv", review_fields, review_rows)

    event_fields = ["candidate_event_id", "actor_id", "date_or_period", "event_name", "action_type", "place", "target_or_recipient", "source_refs", "review_status", "central_aev_status", "interpretation_limit"]
    event_rows = [
        {
            "candidate_event_id": event_id, "actor_id": actor_id, "date_or_period": date,
            "event_name": name, "action_type": action, "place": place, "target_or_recipient": target,
            "source_refs": refs, "review_status": "needs_human_review", "central_aev_status": "not_inserted",
            "interpretation_limit": "Candidate from HR-027 return §5.1; verify exact date/role/target before AEV insertion. Event participation does not establish stable alliance or causal effect.",
        }
        for event_id, actor_id, date, name, action, place, target, refs in EVENTS
    ]
    write_csv(OUT / "event_candidates_v1.csv", event_fields, event_rows)

    near_fields = ["warning_id", "verified_actor_id", "near_name", "disposition", "boundary_note", "review_status", "source_document"]
    near_rows = [
        {
            "warning_id": wid, "verified_actor_id": actor_id, "near_name": name,
            "disposition": disposition, "boundary_note": note, "review_status": "human_checked",
            "source_document": "docs/human_review_return_HR027_v1.md §5.1",
        }
        for wid, actor_id, name, disposition, note in NEAR_NAMES
    ]
    write_csv(OUT / "near_name_warnings_v1.csv", near_fields, near_rows)

    summary_fields = ["metric", "value", "note"]
    summary_rows = [
        {"metric": "registry_actors", "value": str(len(actors)), "note": "118 + four HR-027 additions"},
        {"metric": "hr027_human_checked_actors", "value": "4", "note": "A112-A115"},
        {"metric": "candidate_issue_edges_added", "value": str(len(new_issue_rows)), "note": "ai_seeded; not publication-approved"},
        {"metric": "candidate_place_edges_added", "value": str(len(new_place_rows)), "note": "ai_seeded; semantics pending review"},
        {"metric": "event_candidates_not_in_aev", "value": str(len(event_rows)), "note": "dedicated human-review queue"},
        {"metric": "inter_actor_edges_added", "value": "0", "note": "explicit HR-027 boundary"},
    ]
    write_csv(OUT / "integration_summary_v1.csv", summary_fields, summary_rows)

    expected = {"actors": 122, "issues": 241, "places": 135}
    actual = {"actors": len(actors), "issues": len(issue_rows), "places": len(place_rows)}
    if actual != expected:
        raise ValueError(f"HR-027 count mismatch: {actual} != {expected}")
    if any(row["decision"] != "add" for row in review_rows):
        raise ValueError("HR-027 review sheet is not fully decided")
    print(f"HR-027 merged: {actual}; aliases={len(ALIASES)}; event_candidates={len(event_rows)}; relation_edges=0")


if __name__ == "__main__":
    main()
