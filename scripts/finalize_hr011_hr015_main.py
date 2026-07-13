from __future__ import annotations

"""Main-thread finalization for HR-011/012/014/015.

This pass owns the cross-task work that the bounded merge agents deliberately
left alone: permanent source IDs, source-reference crosswalks, exact user-given
evidence levels/names, and the S051 archive-mismatch correction.  Run the
individual HR merge scripts first, then this script.  The pass is idempotent.
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


NEW_SOURCES = [
    {
        "source_id": "S144",
        "source_type": "parent_organization_profile",
        "title": "日本YWCA『沖縄YWCAのご紹介』",
        "year": "2022",
        "url": "https://www.ywca.or.jp/kaze/0214news-2/",
        "what_it_supports": "HR-011 A107: 2002 founding, regional-YWCA identity, named officers, youth activity, and direct Henoko activity",
        "evidence_level": "E4",
        "bias_note": "Parent-body profile; strong for organizational affiliation and reported activity, not independent evaluation",
        "review_status": "human_checked",
        "notes": "User-reviewed 2026-07-13; specific article dated 2022-02-14.",
    },
    {
        "source_id": "S145",
        "source_type": "parent_organization_topic_page",
        "title": "日本YWCA 沖縄专题页",
        "year": "2026",
        "url": "https://www.ywca.or.jp/tag/%E6%B2%96%E7%B8%84/",
        "what_it_supports": "HR-011 A107: continuing parent-body coverage of Okinawa YWCA and Okinawa-related activity",
        "evidence_level": "E3",
        "bias_note": "Parent-body topic index; use with the specific organization profile S144",
        "review_status": "human_checked",
        "notes": "Merged from SC010; accessed and human-reviewed 2026-07-13.",
    },
    {
        "source_id": "S146",
        "source_type": "organization_site",
        "title": "沖縄を再び戦場にさせない県民の会 公式サイト",
        "year": "2023",
        "url": "https://kenminnokai.okinawa/",
        "what_it_supports": "HR-011 A108: official name, representatives, purpose, structure, and activities",
        "evidence_level": "E4",
        "bias_note": "Primary movement source; use news sources for attendance and external corroboration",
        "review_status": "human_checked",
        "notes": "User-reviewed 2026-07-13.",
    },
    {
        "source_id": "S147",
        "source_type": "local_news",
        "title": "QAB『沖縄を再び戦場にさせない「県民平和大集会」』",
        "year": "2023",
        "url": "https://www.qab.co.jp/news/20231123193623.html",
        "what_it_supports": "HR-011 A108: 2023-11-23 prefectural peace rally and organizer-reported attendance",
        "evidence_level": "E4",
        "bias_note": "Attendance is organizer-reported and must be attributed as such",
        "review_status": "human_checked",
        "notes": "User-reviewed 2026-07-13; event participation does not establish stable alliances.",
    },
    {
        "source_id": "S148",
        "source_type": "local_news",
        "title": "沖縄を再び戦場にさせない県民の会 发足报道",
        "year": "2023",
        "url": "https://ryukyushimpo.jp/news/entry-1754082.html",
        "what_it_supports": "HR-011 A108: formation, purpose, and prefecture-wide network positioning",
        "evidence_level": "E4",
        "bias_note": "News account; umbrella formation does not make every participant a stable member edge",
        "review_status": "human_checked",
        "notes": "Merged from SC013; user-reviewed 2026-07-13.",
    },
    {
        "source_id": "S149",
        "source_type": "local_news",
        "title": "嘉手納爆音、第4次訴訟を提起―原告3万5566人",
        "year": "2022",
        "url": "https://ryukyushimpo.jp/news/entry-1461735.html",
        "what_it_supports": "HR-011/012 A052/A109: fourth Kadena round, filing, plaintiff scale, households, municipalities, and counsel-team existence",
        "evidence_level": "E4",
        "bias_note": "News account; does not establish a complete individual-lawyer roster",
        "review_status": "human_checked",
        "notes": "User-reviewed 2026-07-13; published 2022-01-28.",
    },
    {
        "source_id": "S150",
        "source_type": "local_news",
        "title": "QAB 第4次嘉手納基地爆音差止訴訟 第1回口頭弁論前夜集会",
        "year": "2023",
        "url": "https://www.qab.co.jp/news/20230119159860.html",
        "what_it_supports": "HR-011 A109: fourth-round plaintiffs and lawyers preparing the first oral hearing",
        "evidence_level": "E3",
        "bias_note": "Event report; confirms case-specific role, not the full counsel roster",
        "review_status": "human_checked",
        "notes": "Exact QAB page located during main-thread integration; user had identified the 2023-01-19 report.",
    },
    {
        "source_id": "S151",
        "source_type": "organization_site",
        "title": "嘉手納基地爆音差止訴訟原告団 公式サイト",
        "year": "2026",
        "url": "https://kadena-bakuon.jp/",
        "what_it_supports": "HR-011/012 A052/A109: official plaintiff-group identity and fourth-round litigation context",
        "evidence_level": "E4",
        "bias_note": "Plaintiff-group source; strong for self-identity and case chronology",
        "review_status": "human_checked",
        "notes": "User-reviewed 2026-07-13.",
    },
    {
        "source_id": "S152",
        "source_type": "participating_law_firm_record",
        "title": "第4次嘉手納基地爆音差止訴訟 提訴说明",
        "year": "2022",
        "url": "https://ameblo.jp/hibikilaw-staff/entry-12727218527.html",
        "what_it_supports": "HR-011 A109: participating-law-firm confirmation of a case-specific counsel team",
        "evidence_level": "E3",
        "bias_note": "Participating firm account; do not infer a complete roster or representation scope",
        "review_status": "human_checked",
        "notes": "Merged from SC026; bounded by the user's no-roster-inference decision.",
    },
    {
        "source_id": "S153",
        "source_type": "organization_site",
        "title": "辺野古に基地を絶対つくらせない大阪行動 公式博客",
        "year": "2026",
        "url": "https://blog.livedoor.jp/henoko_osaka/",
        "what_it_supports": "HR-011 A110: sustained Osaka/Kansai Henoko solidarity action",
        "evidence_level": "E3",
        "bias_note": "Self-published action record; use only as mainland solidarity layer",
        "review_status": "human_checked",
        "notes": "Merged from SC041; public action does not establish a stable alliance.",
    },
    {
        "source_id": "S154",
        "source_type": "media_record",
        "title": "IWJ 大阪・辺野古声援行动记录",
        "year": "2014",
        "url": "https://iwj.co.jp/wj/open/archives/146582",
        "what_it_supports": "HR-011 A110: externally reported Osaka action concerning Henoko",
        "evidence_level": "E3",
        "bias_note": "Single event report; cannot by itself establish full organizational continuity",
        "review_status": "human_checked",
        "notes": "Merged from SC042; user-reviewed 2026-07-13.",
    },
    {
        "source_id": "S155",
        "source_type": "organization_history",
        "title": "嘉手納基地爆音差止訴訟原告団 訴訟の歴史",
        "year": "2026",
        "url": "https://kadena-bakuon.jp/trial/history/",
        "what_it_supports": "HR-012 A052: continuity from the first through fourth Kadena litigation rounds",
        "evidence_level": "E4",
        "bias_note": "Plaintiff-group history; strong for self-described organizational continuity",
        "review_status": "human_checked",
        "notes": "User-reviewed 2026-07-13; rounds are not separate registry actors.",
    },
    {
        "source_id": "S156",
        "source_type": "organization_site",
        "title": "普天間基地爆音訴訟団 公式サイト",
        "year": "2026",
        "url": "https://futenma-bakuon.jp/",
        "what_it_supports": "HR-012 A053: official canonical name and continuity across Futenma litigation rounds",
        "evidence_level": "E4",
        "bias_note": "Plaintiff-group source; strong for self-identity and chronology",
        "review_status": "human_checked",
        "notes": "User-reviewed 2026-07-13; use with official judgment S135.",
    },
    {
        "source_id": "S157",
        "source_type": "union_research_report",
        "title": "島の未来は市民が決める―石垣島の自衛隊配備問題―",
        "year": "2018",
        "url": "https://www.jichiro.gr.jp/jichiken_kako/report/rep_tosa37/08/0802_yre/index.htm",
        "what_it_supports": "HR-012 A010: predecessor formed 2015-08-20 and wider citizens liaison group formed 2016-09",
        "evidence_level": "E4",
        "bias_note": "Movement-side local-government research report; detailed first-hand chronology",
        "review_status": "human_checked",
        "notes": "Merged from SC032; user-reviewed 2026-07-13.",
    },
    {
        "source_id": "S158",
        "source_type": "organization_profile",
        "title": "宮古島地下水研究会 団体概要",
        "year": "2026",
        "url": "https://miyakojima-tikasui.com/about_us.html",
        "what_it_supports": "HR-011 C015 defer: comparison organization has a distinct confirmed name and named co-representatives",
        "evidence_level": "E4",
        "bias_note": "Comparison source only; does not establish identity of C015",
        "review_status": "human_checked",
        "notes": "Use to prevent mistaken merger; C015 remains needs_second_source and outside the registry.",
    },
    {
        "source_id": "S159",
        "source_type": "news_magazine",
        "title": "週刊金曜日 石垣島に軍事基地をつくらせない市民連絡会 2023年行动报道",
        "year": "2023",
        "url": "https://www.kinyobi.co.jp/kinyobinews/2023/04/04/antena-1238/",
        "what_it_supports": "HR-012 A010: the established canonical name remained in documented use in 2023",
        "evidence_level": "E3",
        "bias_note": "Movement-oriented magazine; useful for name-in-use cross-check",
        "review_status": "human_checked",
        "notes": "Supports rejecting the unverified 2023 rename claim; not proof of every organizational detail.",
    },
]


ACTOR_UPDATES = {
    "A010": {
        "source_refs": "S016;S017;S157;S159",
        "review_status": "human_revised",
        "notes": (
            "HR-012: 石垣島への自衛隊配備を止める住民の会 formed 2015-08-20 and was a predecessor/founding core; "
            "A010 formed in 2016-09 as a wider coalition. Office/secretariat: 藤井幸子. This was expansion, not a simple rename. "
            "The unverified claim of a 2023 rename to 石垣島の平和と自然を守る市民連絡会 is not adopted."
        ),
    },
    "A011": {
        "source_refs": "S018;S019;S137;S138",
        "review_status": "human_checked",
        "notes": (
            "HR-014: source-backed referendum-request movement actor. In the 2020 litigation, the named plaintiffs were individuals; "
            "A011 is coded requester/support movement, not organizational plaintiff. S051 was removed after its archived domain proved unrelated."
        ),
    },
    "A052": {
        "canonical_name": "嘉手納基地爆音差止訴訟原告団",
        "source_refs": "S026;S149;S151;S155",
        "evidence_level": "E4",
        "review_status": "human_checked",
        "notes": (
            "HR-012: continuous plaintiff-group actor from 1982 through the fourth round; 第4次嘉手納基地爆音差止訴訟原告団 "
            "is a round_of A052, not a new actor. 新川秀清 led the third and fourth rounds. Round participants must not be assumed identical across time."
        ),
    },
    "A053": {
        "canonical_name": "普天間基地爆音訴訟団",
        "source_refs": "S027;S135;S136;S156",
        "evidence_level": "E4",
        "review_status": "human_checked",
        "notes": (
            "HR-012: continuous plaintiff-group actor across the first (2002), second (2012), and third (2020) Futenma noise-litigation rounds. "
            "普天間基地第2次爆音訴訟原告団 is a round_of A053, not a new actor; participants must not be assumed identical across rounds."
        ),
    },
    "A107": {
        "legal_status_guess": "association_or_regional_ywca",
        "issue_tags": "women;human_rights;peace;anti_base",
        "source_refs": "S144;S295",
        "evidence_level": "E3",
        "review_status": "human_checked",
        "notes": (
            "HR-011: local/regional YWCA founded in 2002, distinct from A105 Japan YWCA; direct Henoko photo-exhibit activity is documented. "
            "S295 is an externally hosted YWCA contribution, not independent reporting or standalone identity proof. "
            "The A105-to-A107 affiliation is organizational, not funding or a movement alliance; parent-body actions do not automatically transfer to A107."
        ),
    },
    "A108": {
        "issue_tags": "anti_war;frontline_prevention;Taiwan_contingency;peace",
        "source_refs": "S146;S147;S148",
        "evidence_level": "E4",
        "review_status": "human_checked",
        "notes": (
            "HR-011: prefecture-wide anti-war/frontline-prevention network formed in 2023 by 63 groups/individuals; representatives and secretariat are named. "
            "The umbrella count and mass-rally participation are event/structure evidence, not automatic stable-alliance edges."
        ),
    },
    "A109": {
        "issue_tags": "noise;life_safety;legal;anti_base",
        "source_refs": "S149;S150;S151;S152",
        "evidence_level": "E4",
        "review_status": "human_checked",
        "notes": (
            "HR-011/012: case-specific fourth Kadena counsel team, distinct from A052 plaintiff group. Its existence and role are E4; "
            "the complete individual-lawyer roster and representation scope remain unasserted absent the complaint/formal roster."
        ),
    },
    "A110": {
        "issue_tags": "Henoko;anti_base;solidarity;mobilization",
        "source_refs": "S153;S154",
        "evidence_level": "E3",
        "review_status": "human_checked",
        "notes": (
            "HR-011: sustained Osaka/Kansai mainland-solidarity action actor. Keep in the R11 background/solidarity layer, not the Okinawa-local core; "
            "public actions do not establish a stable alliance or funding relation."
        ),
    },
}


NEW_ISSUES = [
    {
        "issue_id": "I025",
        "issue_label": "anti_war",
        "issue_group": "peace_human_rights",
        "definition": "Opposition to war, military escalation, or the conversion of Okinawa into a battlefield",
        "include_in_phase1": "yes",
        "notes": "Added through HR-011; distinct from a narrower anti-base or anti-deployment code.",
    },
    {
        "issue_id": "I026",
        "issue_label": "mobilization",
        "issue_group": "collective_action",
        "definition": "Sustained public organizing, street action, or campaign mobilization",
        "include_in_phase1": "yes",
        "notes": "Added through HR-011; mobilization does not itself establish stable alliance ties.",
    },
]


ACTOR_ISSUE_SPECS = {
    "A107": {
        "women": ("I022", "Okinawa YWCA regional identity and women-focused mission"),
        "human_rights": ("I023", "Okinawa YWCA human-rights mission and activities"),
        "peace": ("I019", "Okinawa YWCA peace mission and activities"),
        "anti_base": ("I001", "Direct Henoko new-base opposition photo-exhibit activity"),
    },
    "A108": {
        "anti_war": ("I025", "Prefecture-wide anti-war network formed to prevent Okinawa becoming a battlefield"),
        "frontline_prevention": ("I017", "Network purpose explicitly centers preventing Okinawa becoming a battlefield"),
        "Taiwan_contingency": ("I018", "Public framing connects Okinawa frontline risk to regional contingency planning"),
        "peace": ("I019", "Prefectural anti-war and peace mobilization"),
    },
    "A109": {
        "noise": ("I021", "Fourth Kadena base-noise injunction litigation counsel role"),
        "life_safety": ("I007", "Fourth Kadena litigation addresses residents' daily noise harm"),
        "legal": ("I011", "Case-specific legal representation in fourth Kadena litigation"),
        "anti_base": ("I001", "Flight-injunction claim concerning Kadena base-noise burden"),
    },
    "A110": {
        "Henoko": ("I003", "Sustained Osaka public actions opposing Henoko base construction"),
        "anti_base": ("I001", "Sustained Osaka public actions opposing Henoko base construction"),
        "solidarity": ("I024", "Mainland public solidarity actions concerning Henoko"),
        "mobilization": ("I026", "Long-running fixed Osaka/Kansai action repertoire"),
    },
}


ACTOR_ISSUE_SOURCE = {
    "A107": "S144;S295",
    "A108": "S146;S147;S148",
    "A109": "S149;S150;S151;S152",
    "A110": "S153;S154",
}


def merge_sources() -> None:
    path = DATA / "05_source_log_initial_v0.csv"
    fields, rows = read_csv(path)
    by_id = {row["source_id"]: row for row in rows}
    by_url = {row["url"]: row["source_id"] for row in rows if row.get("url")}
    for source in NEW_SOURCES:
        collision = by_url.get(source["url"])
        if collision and collision != source["source_id"]:
            raise ValueError(f"URL already assigned to {collision}: {source['url']}")
        if source["source_id"] in by_id:
            by_id[source["source_id"]].update(source)
        else:
            rows.append(source.copy())
            by_id[source["source_id"]] = rows[-1]
            by_url[source["url"]] = source["source_id"]

    s051 = by_id["S051"]
    s051.update(
        {
            "what_it_supports": "No current claim: archived capture resolves to unrelated Ishigaki tourism/food site",
            "evidence_level": "E0",
            "bias_note": "Archive/domain mismatch; cannot support the referendum organization",
            "review_status": "rejected_archive_mismatch",
            "notes": (
                "Main-thread QA after R4/R9 cross-review: archived title is 石垣島ヘイヨー and content is unrelated tourism/food material. "
                "Do not use for A011 identity, signatures, continuity, or dissolution; historical-domain recovery remains a retrieval task."
            ),
        }
    )
    write_csv(path, fields, rows)


def update_actors() -> None:
    path = DATA / "01_actor_registry_initial_v0.csv"
    fields, rows = read_csv(path)
    by_id = {row["actor_id"]: row for row in rows}
    missing = set(ACTOR_UPDATES) - set(by_id)
    if missing:
        raise ValueError(f"Missing actors required by HR finalization: {sorted(missing)}")
    for actor_id, updates in ACTOR_UPDATES.items():
        by_id[actor_id].update(updates)
    write_csv(path, fields, rows)


def update_issues_and_edges() -> None:
    issue_path = DATA / "03_issue_taxonomy_v0.csv"
    issue_fields, issues = read_csv(issue_path)
    issue_by_id = {row["issue_id"]: row for row in issues}
    for issue in NEW_ISSUES:
        if issue["issue_id"] in issue_by_id:
            issue_by_id[issue["issue_id"]].update(issue)
        else:
            issues.append(issue.copy())
    write_csv(issue_path, issue_fields, issues)

    edge_path = DATA / "07_actor_issue_edges_initial_v0.csv"
    edge_fields, edges = read_csv(edge_path)
    pairs = {(row["actor_id"], row["issue_id"]): row for row in edges}
    used_ids = {row["edge_id"] for row in edges}
    next_id = 1
    while f"AI{next_id:03d}" in used_ids:
        next_id += 1
    for actor_id, label_specs in ACTOR_ISSUE_SPECS.items():
        actor_level = ACTOR_UPDATES[actor_id]["evidence_level"]
        for label, (issue_id, basis) in label_specs.items():
            key = (actor_id, issue_id)
            updates = {
                "actor_id": actor_id,
                "issue_id": issue_id,
                "issue_label": label,
                "relation_basis": basis,
                "source_ref": ACTOR_ISSUE_SOURCE[actor_id],
                "evidence_level": actor_level,
                "review_status": "human_checked",
                "notes": "HR-011 main-thread finalization; issue relation is source-bounded and does not imply a stable inter-organizational alliance.",
            }
            if key in pairs:
                pairs[key].update(updates)
            else:
                while f"AI{next_id:03d}" in used_ids:
                    next_id += 1
                row = {"edge_id": f"AI{next_id:03d}", **updates}
                edges.append(row)
                pairs[key] = row
                used_ids.add(row["edge_id"])
                next_id += 1
    write_csv(edge_path, edge_fields, edges)


def update_aliases() -> None:
    path = DATA / "02_actor_aliases_initial_v0.csv"
    fields, rows = read_csv(path)
    source_crosswalk = {
        ("A010", "石垣島への自衛隊配備を止める住民の会"): "S157",
        ("A052", "第4次嘉手納基地爆音差止訴訟原告団"): "S149;S151;S155",
        ("A053", "普天間基地第2次爆音訴訟原告団"): "S135;S156",
    }
    for row in rows:
        key = (row["actor_id"], row["alias"])
        if key in source_crosswalk:
            row["source_ref"] = source_crosswalk[key]

    required = {
        ("A053", "普天間基地爆音訴訟原告団"): {
            "actor_id": "A053",
            "alias": "普天間基地爆音訴訟原告団",
            "alias_type": "descriptive_variant",
            "source_ref": "S135;S136",
            "notes": "HR-012: descriptive plaintiff-group variant; canonical follows the official site name 普天間基地爆音訴訟団.",
        }
    }
    existing = {(row["actor_id"], row["alias"]) for row in rows}
    rows.extend(value for key, value in required.items() if key not in existing)
    write_csv(path, fields, rows)


def update_relations() -> None:
    path = DATA / "15_funding_or_support_edges_sample_v0.csv"
    fields, rows = read_csv(path)
    by_id = {row["edge_id"]: row for row in rows}
    by_id["F042"].update(
        {
            "evidence_level": "E4",
            "source_ref": "S149;S151;S152",
            "review_status": "human_checked",
            "notes": "HR-011/012: case-specific counsel-team to plaintiff-group role for the fourth round; neither funding nor a stable alliance.",
        }
    )
    by_id["F043"].update(
        {
            "evidence_level": "E3",
            "source_ref": "S144;S145",
            "review_status": "human_checked",
            "notes": "HR-011: parent/regional organizational affiliation only; not funding, not a movement alliance, and no automatic transfer of A105 actions to A107.",
        }
    )
    write_csv(path, fields, rows)


def update_review_log() -> None:
    path = DATA / "human_review_log_v0.csv"
    fields, rows = read_csv(path)
    by_key = {(row["task_id"], row["object_id"]): row for row in rows}
    corrections = {
        ("HR-011", "A107"): {
            "review_status": "human_checked",
            "evidence_level_final": "E3",
            "decision": "add_core_support",
            "next_steps": "No blocking identity work; keep A105 affiliation separate from action/issue attribution.",
        },
        ("HR-011", "A108"): {
            "review_status": "human_checked",
            "evidence_level_final": "E4",
            "decision": "add_core",
            "next_steps": "Do not turn the 63-group umbrella description into unverified stable member edges.",
        },
        ("HR-011", "C015"): {
            "review_status": "needs_second_source",
            "evidence_level_final": "E3",
            "publishable_claim": "Single-source candidate may be confused with 宮古島地下水研究会; identity unresolved",
            "decision": "defer_no_actor",
            "review_note": "HR-011: exact formal name, representative, continuity, and relation to 宮古島地下水研究会 remain unresolved; do not enter the actor registry.",
            "next_steps": "Open SC015 original, obtain an independent second source, and crosswalk the similarly named groundwater organization.",
        },
        ("HR-011", "A109"): {
            "review_status": "human_checked",
            "evidence_level_final": "E4",
            "decision": "add_core_support",
            "next_steps": "Complete lawyer roster only from the complaint or formal plaintiff/counsel material; do not infer from a law-firm blog.",
        },
        ("HR-011", "A110"): {
            "review_status": "human_checked",
            "evidence_level_final": "E3",
            "decision": "add_background_mainland_solidarity",
            "next_steps": "Use in R11 solidarity layer only; do not count as Okinawa-local core.",
        },
    }
    missing = set(corrections) - set(by_key)
    if missing:
        raise ValueError(f"Missing HR review-log rows: {sorted(missing)}")
    for key, updates in corrections.items():
        by_key[key].update(updates)

    new_rows = [
        {
            "task_id": "HR-014",
            "object_id": case_id,
            "review_date": "2026-07-13",
            "human_reviewer": "user",
            "review_status": "human_checked",
            "evidence_level_final": "E4",
            "publishable_claim": claim,
            "decision": "accept_case_fact_with_boundaries",
            "review_note": note,
            "next_steps": next_steps,
        }
        for case_id, claim, note, next_steps in [
            (
                "R8C01",
                "Dugong litigation established a procedural review route but did not stop construction",
                "DoD prevailed on the 2020 appeal; plaintiff, counsel, individual and non-party roles remain case-specific.",
                "Keep A002/A019 as non-parties and do not transfer personal roles to organizations.",
            ),
            (
                "R8C02",
                "Henoko EIA existed and NACSJ made dated formal submissions; the procedure did not stop construction",
                "Procedure existence does not prove that every civic actor used the EIA channel.",
                "Code only named, dated formal participants.",
            ),
            (
                "R8C03",
                "Third Kadena claims for injunction/future harm failed while compensation for past noise harm remained",
                "A052 is the organizational plaintiff-group crosswalk; individuals and litigation rounds remain distinct.",
                "Do not create the third-round counsel group as a registry actor.",
            ),
            (
                "R8C04",
                "Futenma noise litigation awarded bounded compensation and rejected remaining claims",
                "A053 is the organizational plaintiff group; joined docket-number mapping remains bounded by the judgment.",
                "Retain exact case-number follow-up as non-blocking legal metadata work.",
            ),
            (
                "R8C05",
                "Ishigaki mandatory-order referendum suit was dismissed at the threshold",
                "Named plaintiffs were anonymized individuals; A011 is requester/campaign body, not organizational plaintiff.",
                "Keep requester and plaintiff roles separate.",
            ),
            (
                "R8C06",
                "Awase first- and second-wave public-funds litigation had opposite results and cannot be collapsed",
                "A055 and A020 are case-specific supporters/material hosts rather than organizational plaintiffs.",
                "Preserve first-wave/second-wave outcomes separately in all reporting.",
            ),
        ]
    ]
    new_rows.extend(
        [
            {
                "task_id": "HR-014",
                "object_id": "R8R001-R8R027",
                "review_date": "2026-07-13",
                "human_reviewer": "user",
                "review_status": "human_checked",
                "evidence_level_final": "role_specific_E3-E4",
                "publishable_claim": "All 27 legal/procedural role rows accepted with case-specific role boundaries",
                "decision": "accept_27_roles",
                "review_note": "Plaintiff, counsel, requester, supporter, defendant, government-node and non-party roles remain distinct; no person-to-organization transfer.",
                "next_steps": "Use data/interim/18_legal_policy_actor_roles_v0.csv; do not promote provisional procedural collectives into the actor registry.",
            },
            {
                "task_id": "HR-015",
                "object_id": "EN0001-EN0049",
                "review_date": "2026-07-13",
                "human_reviewer": "user",
                "review_status": "human_checked",
                "evidence_level_final": "row_specific_E2-E4",
                "publishable_claim": "49 evidence notes accepted or revised with conservative evidence boundaries",
                "decision": "accept_with_locator_and_wording_revisions",
                "review_note": "No reject rows; Dugong legal notes use S129; unresolved locators remain explicit rather than guessed.",
                "next_steps": "Resolve the five remaining locator-level follow-ups without changing claim scope.",
            },
            {
                "task_id": "HR-015",
                "object_id": "AEV0001-AEV0064",
                "review_date": "2026-07-13",
                "human_reviewer": "user",
                "review_status": "human_checked",
                "evidence_level_final": "row_specific_E2-E4; four analytical_seed",
                "publishable_claim": "64 event-venue rows retained with action-type and interpretation boundaries",
                "decision": "accept_with_event_only_and_analytical_seed_limits",
                "review_note": "Co-signing is not alliance; nine MMC small groups remain unverified event participants outside the registry; four pathway rows are analytical seeds, not factual relations.",
                "next_steps": "Regenerate derived figures after the A077-A085 main-registry removal.",
            },
        ]
    )
    for row in new_rows:
        key = (row["task_id"], row["object_id"])
        if key in by_key:
            by_key[key].update(row)
        else:
            rows.append(row)
            by_key[key] = rows[-1]
    write_csv(path, fields, rows)


def update_candidate_decisions() -> None:
    path = ROOT / "outputs" / "registry_expansion_v1" / "candidate_actors_v1.csv"
    fields, rows = read_csv(path)
    by_id = {row["candidate_id"]: row for row in rows}
    changes = {
        "C008": ("", "rejected", "removed_hr010_scope", "Removed from the registry by the HR-010 scope correction; evidence remains historical only."),
        "C009": ("A107", "human_checked", "added_hr011", "Added as core-support; permanent sources S144/S295. S295 is YWCA-authored rather than independent reporting."),
        "C010": ("", "human_checked", "background_only_hr013", "HR-013 retained this foundation only as a war-memory background node, not a base-dispute actor."),
        "C011": ("A111", "human_checked", "added_hr013", "HR-013 added A111 as a core-support women/peace/human-rights actor; do not confuse it with A094 or おきなわ女性財団."),
        "C012": ("A108", "human_checked", "added_hr011", "Added as core at E4; permanent sources S146-S148."),
        "C013": ("A095", "ai_seeded", "merged_identity_only", "Merged as A095 at the E4 identity layer; classification and relations still require the applicable human gate."),
        "C014": ("A096", "ai_seeded", "merged_identity_only", "Merged as A096 at the E4 identity layer; classification and relations still require the applicable human gate."),
        "C015": ("", "needs_second_source", "defer", "Exact identity remains unresolved; do not merge with 宮古島地下水研究会."),
        "C016": ("A097", "ai_seeded", "merged_identity_only", "Merged as A097 at the E4 identity layer; classification and relations still require the applicable human gate."),
        "C017": ("A098", "ai_seeded", "merged_identity_only", "Merged as A098 at the E4 identity layer; classification and relations still require the applicable human gate."),
        "C018": ("A099", "ai_seeded", "merged_identity_only", "Merged as A099 at the E4 identity layer; classification and relations still require the applicable human gate."),
        "C019": ("A100", "ai_seeded", "merged_identity_only", "Merged as A100 at the E4 identity layer; classification and relations still require the applicable human gate."),
        "C020": ("A101", "ai_seeded", "merged_identity_only", "Merged as A101 at the E4 identity layer; classification and relations still require the applicable human gate."),
        "C021": ("A102", "human_checked", "added_hr010", "HR-010 added the national pollution-lawyers network as a background/support legal actor."),
        "C022": ("A103", "human_checked", "added_hr010", "HR-010 added the national base-noise plaintiff liaison as a background/support legal actor."),
        "C023": ("A109", "human_checked", "added_hr011", "Added as fourth-round counsel team at E4 existence; roster remains bounded."),
        "C024": ("A104", "human_checked", "added_hr010", "HR-010 added the Futenma noise-litigation counsel team; it is distinct from the plaintiff group A053."),
        "C025": ("A105", "human_checked", "added_hr010_background", "HR-010 added Japan YWCA only as a mainland statement/solidarity actor; no stable-alliance edge."),
        "C026": ("A052", "human_checked", "merged_round_of", "Fourth-round designation of continuous A052; no new actor."),
        "C027": ("A053", "human_checked", "merged_round_of", "Second-round designation of continuous A053; no new actor."),
        "C028": ("A010", "human_revised", "merged_predecessor_of", "2015 predecessor/founding core of wider A010 formed 2016-09; not a rename."),
        "C029": ("", "rejected", "out_of_scope_hr013", "HR-013 rejected this general public-interest organization because no direct Phase-1 issue connection was verified."),
        "C030": ("", "rejected", "out_of_scope_hr013", "HR-013 rejected this general public-interest organization because no direct Phase-1 issue connection was verified."),
        "C031": ("", "rejected", "out_of_scope_hr013", "HR-013 rejected this general public-interest organization because no direct Phase-1 issue connection was verified."),
        "C032": ("", "rejected", "out_of_scope_hr013", "HR-013 rejected this general public-interest organization because no direct Phase-1 issue connection was verified."),
        "C033": ("", "rejected", "out_of_scope_hr013", "HR-013 rejected this general public-interest organization because no direct Phase-1 issue connection was verified."),
        "C034": ("", "human_checked", "background_only_hr013", "HR-013 retained this administrative coral-conservation platform only as a background node; no political stance or anti-base edge."),
        "C035": ("A106", "human_checked", "added_hr010_background", "HR-010 added this mainland solidarity actor as A106; canonical キャンペーン／連絡会 alias remains a bounded check."),
        "C036": ("A110", "human_checked", "added_hr011_background", "Added only to mainland-solidarity/R11 background layer."),
    }
    for candidate_id, (final_id, status, recommendation, reason) in changes.items():
        row = by_id[candidate_id]
        row["proposed_id"] = final_id
        row["review_status"] = status
        row["triage_recommendation"] = recommendation
        row["add_or_defer_reason"] = reason
    by_id["C011"]["issue_tags"] = "women;peace;anti_base;human_rights"
    by_id["C011"]["evidence_level"] = "E4"
    by_id["C012"]["evidence_level"] = "E4"
    by_id["C023"]["evidence_level"] = "E4"
    write_csv(path, fields, rows)


def update_hr014_source_metadata() -> None:
    """Keep source-level metadata distinct from the completed HR-014 case review."""
    path = DATA / "05_source_log_initial_v0.csv"
    fields, rows = read_csv(path)
    by_id = {row["source_id"]: row for row in rows}
    year_corrections = {"S128": "2017", "S132": "2004", "S143": "2007"}
    for source_id in (f"S{number:03d}" for number in range(128, 144)):
        row = by_id[source_id]
        if source_id in year_corrections:
            row["year"] = year_corrections[source_id]
        prefix = row["notes"].split("; legal outcome", 1)[0]
        row["notes"] = (
            f"{prefix}; case outcome and actor-role semantics were accepted by the user in HR-014; "
            "source metadata remains ai_seeded unless separately reviewed."
        )
    write_csv(path, fields, rows)


def validate() -> None:
    _, sources = read_csv(DATA / "05_source_log_initial_v0.csv")
    source_ids = {row["source_id"] for row in sources}
    assert all(f"S{number:03d}" in source_ids for number in range(144, 160))
    s051 = next(row for row in sources if row["source_id"] == "S051")
    assert s051["evidence_level"] == "E0" and s051["review_status"] == "rejected_archive_mismatch"
    assert next(row for row in sources if row["source_id"] == "S128")["year"] == "2017"
    assert next(row for row in sources if row["source_id"] == "S132")["year"] == "2004"
    assert next(row for row in sources if row["source_id"] == "S143")["year"] == "2007"

    _, actors = read_csv(DATA / "01_actor_registry_initial_v0.csv")
    actor_by_id = {row["actor_id"]: row for row in actors}
    assert actor_by_id["A053"]["canonical_name"] == "普天間基地爆音訴訟団"
    assert actor_by_id["A108"]["evidence_level"] == "E4"
    assert actor_by_id["A109"]["evidence_level"] == "E4"
    assert "S051" not in actor_by_id["A011"]["source_refs"]
    for actor_id in ("A010", "A052", "A053", "A107", "A108", "A109", "A110"):
        refs = actor_by_id[actor_id]["source_refs"].split(";")
        assert all(ref in source_ids for ref in refs), (actor_id, refs)

    _, edges = read_csv(DATA / "07_actor_issue_edges_initial_v0.csv")
    pairs = {(row["actor_id"], row["issue_id"]) for row in edges}
    assert ("A107", "I001") in pairs
    assert ("A108", "I025") in pairs
    assert ("A110", "I026") in pairs

    _, relations = read_csv(DATA / "15_funding_or_support_edges_sample_v0.csv")
    by_relation_id = {row["edge_id"]: row for row in relations}
    assert by_relation_id["F042"]["evidence_level"] == "E4"
    assert by_relation_id["F042"]["funding_relation_confidence"] == "not_funding_relation"
    assert by_relation_id["F043"]["funding_relation_confidence"] == "not_funding_relation"


def main() -> None:
    merge_sources()
    update_actors()
    update_issues_and_edges()
    update_aliases()
    update_relations()
    update_review_log()
    update_candidate_decisions()
    update_hr014_source_metadata()
    validate()
    print(
        "Finalized HR-011/012/014/015 cross-task state: S144-S159, S051 rejection, "
        "actor/source crosswalks, exact evidence levels/names, issues, relations, and candidate dispositions."
    )


if __name__ == "__main__":
    main()
