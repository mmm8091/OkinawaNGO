from __future__ import annotations

"""Apply the principal's completed HR-020 and HR-026 decisions.

This is a deterministic post-generation merge.  It intentionally does not
touch the actor registry or source log:

* HR-020 resolves source-list identity only.  Human-confirmed event-only
  identities may bridge sampled events, but they do not become registry
  actors and repeated co-signing does not become an alliance.
* HR-026 resolves election-window actor-event roles only.  It does not infer
  votes, turnout, persuasion, electoral causality, stable coalitions, or
  registry membership.

Run this after regenerating R05 or R09 candidate packages.
"""

import csv
from collections import Counter, defaultdict
from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parents[1]

OVERLAY_PATH = Path(
    "outputs/principal_review_merge_v1/principal_decision_overlay_v1.csv"
)
REGISTRY_PATH = Path("data/interim/01_actor_registry_initial_v0.csv")
R5_PARTICIPATION_PATH = Path(
    "data/interim/25_coaction_event_participation_v0.csv"
)
R5_DIR = Path("outputs/R05_coaction_v1")
R5_QUEUE_PATH = R5_DIR / "hr020_review_queue_v0.csv"
R9_EVENT_PATH = Path("data/interim/33_r09_election_civic_events_v1.csv")
R9_DIR = Path("outputs/R09_election_civic_interface_v1")
R9_QUEUE_PATH = R9_DIR / "HR026_election_civic_role_review_v0.csv"
R9_SOURCE_PATH = R9_DIR / "source_proposals_v1.csv"
R9_GAP_PATH = R9_DIR / "online_gap_register_v1.csv"
REPORT_PATH = Path(
    "outputs/principal_review_merge_v1/HR020_HR026_merge_report_v1.md"
)


R5_EVENT_META = {
    "EV2010_WWF_67": {
        "event_name": "2010 WWF Japan 67-group Henoko / dugong joint statement",
        "event_date": "2010-05-14",
        "event_year": "2010",
        "action_type": "joint_statement",
        "role_vocabulary": "listed_endorser",
        "target_institution": "Prime Minister; Minister of Defense; Minister for Foreign Affairs",
        "issue_tags": "Henoko;dugong;biodiversity;anti_base;democracy;life_safety",
        "place_tags": "Henoko;Oura Bay;Kayo;Okinawa",
        "source_refs": "S003",
        "source_locator": "archived raw.html lines 437-439; h3 賛同団体 and following paragraph",
        "declared_participant_count": "67",
    },
    "EV2015_NACSJ_31": {
        "event_name": "2015 NACSJ / Peace Boat 31-NGO Henoko emergency joint statement",
        "event_date": "2015-03-25",
        "event_year": "2015",
        "action_type": "joint_statement",
        "role_vocabulary": "listed_joint_statement_signatory",
        "target_institution": "Government of Japan; Government of the United States",
        "issue_tags": "Henoko;Oura Bay;biodiversity;human_rights;peace;anti_base",
        "place_tags": "Henoko;Oura Bay;Okinawa",
        "source_refs": "S004;S005",
        "source_locator": "S004 archived raw.html lines 346-412; 31 consecutive organization divs",
        "declared_participant_count": "31",
    },
    "EV2020_OEJP_MMC_71": {
        "event_name": "2020 OEJP-led 71-group request and civil-society report to MMC",
        "event_date": "2020-07-10",
        "event_year": "2020",
        "action_type": "request_letter_and_civil_society_report",
        "role_vocabulary": "initiator_and_undersigned_participant;undersigned_request_participant",
        "target_institution": "U.S. Marine Mammal Commission",
        "issue_tags": "Henoko;Oura Bay;dugong;environment;international_advocacy;administrative_oversight",
        "place_tags": "Henoko;Oura Bay;Okinawa;United States",
        "source_refs": "S006",
        "source_locator": "Letter of Request to the U.S. Marine Mammal Commission, 2020-07-10, pp. 5-7",
        "declared_participant_count": "71",
    },
}

R5_REPORT_A = "docs/human_review_return_HR020_names_batch34A_v1.md"
R5_REPORT_B = "docs/human_review_return_HR020_names_batch34B_v1.md"


def event_only_patch(
    canonical_name: str,
    identity_group_id: str,
    decision_id: str,
    note: str,
    *,
    actor_class: str = "",
) -> dict[str, str]:
    result = {
        "canonical_name": canonical_name,
        "actor_id": "",
        "candidate_actor_id": "",
        "identity_group_id": identity_group_id,
        "identity_status": "event_only_identity_human_checked",
        "identity_review_status": "human_checked",
        "identity_decision_id": decision_id,
        "identity_note": note,
        "decision_source_report": R5_REPORT_A
        if int(decision_id.split("-")[-1]) <= 8
        else R5_REPORT_B,
    }
    if actor_class:
        result["actor_class"] = actor_class
    return result


R5_PATCHES = {
    "EV2020_OEJP_MMC_71:P012": event_only_patch(
        "沖縄国際人権法研究会",
        "EO_R5_AOCHR",
        "HR020-01",
        "AOCHR resolved to this event-only organization, not A054.",
    ),
    "EV2020_OEJP_MMC_71:P044": event_only_patch(
        "不戦へのネットワーク",
        "EO_R5_ANTI_WAR_NETWORK_AICHI",
        "HR020-02",
        "Anti-war Network resolved to the Aichi/Nagoya group, not A008.",
    ),
    "EV2010_WWF_67:P018": event_only_patch(
        "基地のない平和で豊かな沖縄をめざす会・大阪",
        "EO_R5_BASE_FREE_OKINAWA_OSAKA",
        "HR020-03",
        "2010 source form and 2020 English source form are the same event-only organization.",
    ),
    "EV2020_OEJP_MMC_71:P068": event_only_patch(
        "基地のない平和で豊かな沖縄をめざす会・大阪",
        "EO_R5_BASE_FREE_OKINAWA_OSAKA",
        "HR020-03",
        "Source omitted Osaka; identity is the Osaka organization, not A071/A072.",
    ),
    "EV2020_OEJP_MMC_71:P051": {
        "actor_id": "A110",
        "candidate_actor_id": "",
        "identity_group_id": "",
        "identity_status": "registry_actor",
        "identity_review_status": "human_checked",
        "identity_decision_id": "HR020-04",
        "identity_note": "Source-attested transliteration of A110; event participation only.",
        "decision_source_report": R5_REPORT_A,
    },
    "EV2020_OEJP_MMC_71:P065": event_only_patch(
        "Stop!辺野古埋め立てキャンペーン",
        "EO_R5_STOP_HENOKO_RECLAMATION",
        "HR020-05",
        "Resolved as a distinct event-only organization, not A106.",
    ),
    "EV2010_WWF_67:P060": event_only_patch(
        "憲法ひろば・杉並",
        "EO_R5_KENPO_HIROBA_SUGINAMI",
        "HR020-06",
        "Human-confirmed first organization in the source's missing-delimiter string.",
    ),
    "EV2010_WWF_67:P061": event_only_patch(
        "福岡地区合同労働組合",
        "EO_R5_FUKUOKA_GENERAL_UNION",
        "HR020-06",
        "Human-confirmed second organization in the source's missing-delimiter string.",
        actor_class="labor_union",
    ),
    "EV2010_WWF_67:P010": event_only_patch(
        "ヘリ基地いらない二見以北十区の会",
        "EO_R5_FUTAMI_TEN_DISTRICTS",
        "HR020-07",
        "Human-confirmed Japanese/English event-only identity.",
    ),
    "EV2020_OEJP_MMC_71:P019": event_only_patch(
        "ヘリ基地いらない二見以北十区の会",
        "EO_R5_FUTAMI_TEN_DISTRICTS",
        "HR020-07",
        "Futamai is the source spelling for Futami/二見.",
    ),
    "EV2010_WWF_67:P013": event_only_patch(
        "北限のジュゴンを見守る会",
        "EO_R5_NORTHERN_DUGONG_WATCH",
        "HR020-08",
        "Parent/office organization; related to but not identical with Team Zan.",
    ),
    "EV2020_OEJP_MMC_71:P009": event_only_patch(
        "北限のジュゴン調査チーム・ザン",
        "EO_R5_NORTHERN_DUGONG_TEAM_ZAN",
        "HR020-08",
        "Field survey team related to the parent body; not a strict alias.",
    ),
    "EV2010_WWF_67:P022": event_only_patch(
        "環瀬戸内海会議",
        "EO_R5_PAN_SETO",
        "HR020-09",
        "Human-confirmed self-used Japanese/English identity.",
    ),
    "EV2020_OEJP_MMC_71:P035": event_only_patch(
        "環瀬戸内海会議",
        "EO_R5_PAN_SETO",
        "HR020-09",
        "Pan-Seto Inland Sea Congress is the organization's self-used English name.",
    ),
    "EV2010_WWF_67:P032": event_only_patch(
        "海の生き物を守る会",
        "EO_R5_AMCO",
        "HR020-10",
        "Human-confirmed Japanese/English event-only identity.",
    ),
    "EV2020_OEJP_MMC_71:P029": event_only_patch(
        "海の生き物を守る会",
        "EO_R5_AMCO",
        "HR020-10",
        "Source translation variant uses Conservation; official English uses Protection (AMCo).",
    ),
    "EV2010_WWF_67:P042": event_only_patch(
        "みん宿ヤポネシア",
        "EO_R5_YAPONESIA",
        "HR020-11",
        "Family-run small lodging/civic venue; participation does not make it an NGO.",
        actor_class="small_lodging_civic_venue",
    ),
    "EV2020_OEJP_MMC_71:P016": event_only_patch(
        "みん宿ヤポネシア",
        "EO_R5_YAPONESIA",
        "HR020-11",
        "Minshuku Yaponesia is a source alias for the same lodging/civic entity.",
        actor_class="small_lodging_civic_venue",
    ),
    "EV2010_WWF_67:P066": event_only_patch(
        "じゅごんの里",
        "EO_R5_DUGONG_NO_SATO",
        "HR020-12",
        "Human-confirmed Japanese/romanized event-only identity.",
    ),
    "EV2020_OEJP_MMC_71:P003": event_only_patch(
        "じゅごんの里",
        "EO_R5_DUGONG_NO_SATO",
        "HR020-12",
        "Dugong no Sato is the source romanization.",
    ),
    "EV2010_WWF_67:P055": event_only_patch(
        "沖縄について考え連帯する「命どぅ宝」の会（「命どぅ宝」あいち）",
        "EO_R5_NUCHIDUTAKARA_AICHI",
        "HR020-13",
        "Aichi organization; distinct from the 2020 Okinawa organization and A018.",
    ),
    "EV2020_OEJP_MMC_71:P020": event_only_patch(
        "命どぅ宝を継承する会",
        "EO_R5_NUCHIDUTAKARA_OKINAWA",
        "HR020-13",
        "Okinawa peace-memory organization; distinct from the 2010 Aichi organization and A018.",
    ),
    "EV2010_WWF_67:P017": event_only_patch(
        "「自然の権利」基金",
        "EO_R5_FUND_FOR_RIGHTS_OF_NATURE",
        "HR020-14",
        "Independent event-only organization, not an alias/unit/project of A020 JELF.",
    ),
}


R9_PATCHES = {
    "R9EC001": {
        "actor_name": "沖縄「建白書」を実現し未来を拓く島ぐるみ会議",
        "registry_crosswalk": "A059",
        "entity_boundary": "okinawa_wide_civic_network",
        "source_proposal_ids": "R9EC_S002;R9EC_S022",
        "observable_action": (
            "Held a founding assembly on 2014-07-27 to establish a long-term "
            "platform for the Kenpakusho and anti-base issues."
        ),
        "interpretation_limit": (
            "Organization material explicitly says it was not directly created "
            "for the gubernatorial election; do not code endorsement or vote mobilization."
        ),
        "notes": "島ぐるみ会議 is an alias; similarly named municipal bodies are not merged into A059.",
    },
    "R9EC005": {
        "entity_boundary": "organization_outside_registry / national_body",
        "registry_crosswalk": "none",
        "notes": (
            "Issuer is 新日本婦人の会中央本部; statement date 2014-11-19 and "
            "web publication date 2014-11-21. Okinawa-branch activity is only "
            "the national body's self-report, not an A115 event role."
        ),
    },
    "R9EC010": {
        "role_label": "policy_proposal_drafter",
        "observable_action": (
            "Held a public workshop to draft policy proposals for gubernatorial candidates."
        ),
        "interpretation_limit": (
            "Request is a coarse aggregation class only; drafting is confirmed, "
            "but delivery, receipt, response and candidate uptake are not established."
        ),
        "notes": "The source reports 34 participants; this is not a reach or effect metric.",
    },
    "R9EC011": {
        "event_date_start": "2018-09-12",
        "event_date_end": "2018-09-19",
        "date_precision": "day_range",
        "observable_action": (
            "Published a candidate-policy comparison on 9/12 and the project's "
            "learning process and policy proposals on 9/19."
        ),
        "interpretation_limit": (
            "Information production is confirmed; readership, independent neutrality "
            "certification, persuasion, turnout and vote effects are not."
        ),
    },
    "R9EC012": {
        "entity_boundary": "organization_outside_registry / national_body",
        "registry_crosswalk": "none",
        "notes": (
            "Issuer unit is 新日本婦人の会中央常任委員会; do not crosswalk to A115. "
            "Organization-wide activity remains a self-report without scale or causal proof."
        ),
    },
    "R9EC015": {
        "observable_action": (
            "Convened an online issue assembly supporting non-approval of the "
            "Henoko design change and connecting remains-in-fill, PFAS, base "
            "life-safety, human-rights and autonomy issues."
        ),
        "interpretation_limit": (
            "Organizer-framed issue campaign in an election-adjacent context; "
            "political actors disputed whether it functioned as an election rally; "
            "the official statement contains no explicit candidate endorsement."
        ),
    },
    "R9EC016": {
        "entity_boundary": "organization_outside_registry / national_body",
        "registry_crosswalk": "none",
        "notes": (
            "National-body action; do not crosswalk to A115. Fundraising appears "
            "only as a campaign call and creates no amount or recipient relation."
        ),
    },
    "R9EC017": {
        "observable_action": (
            "Administered an August 2022 questionnaire of 26 themes and 74 questions "
            "to all three candidates and announced discussion based on the results."
        ),
        "interpretation_limit": (
            "The original answer sheets were not located; do not compare candidate "
            "answers or transfer named individuals' roles to A051 or other organizations."
        ),
    },
    "R9EC018": {
        "event_status": "announced_not_occurrence_verified",
        "observable_action": (
            "Announced two public talks for 9/8 and 9/10 based on the candidate questionnaire."
        ),
        "interpretation_limit": (
            "The available source is a pre-event announcement and no post-event "
            "record was found; exclude this row from confirmed-held event counts."
        ),
        "notes": "online_exhausted; retain as an announced public-meeting record only.",
    },
    "R9EC019": {
        "actor_name": "主催者未確認",
        "entity_boundary": "unidentified_organizer_event_record",
        "registry_crosswalk": "none",
        "interpretation_limit": (
            "The endorsement event is reported, but the organizer is unidentified; "
            "do not actorize the event label, infer membership, or construct a stable women's alliance."
        ),
        "notes": "online_exhausted; E2 single party-media event record.",
    },
}


R9_SOURCE_022 = {
    "proposal_id": "R9EC_S022",
    "title": "島ぐるみ会議が結成大会",
    "url": "https://www.qab.co.jp/news/2014072756461.html",
    "publisher": "琉球朝日放送",
    "source_type": "local_broadcast_news",
    "publication_or_record_date": "2014-07-27",
    "locator": "Same-day report confirming the founding assembly was held in Ginowan",
    "support_scope": "R9EC001 occurrence/date and issue-campaign framing only",
    "suggested_evidence_level": "E3",
    "source_log_state": "module_proposal_only",
    "relation_or_claim_approved": "no",
    "caveat": (
        "Module-local linkage only; source indexing does not approve election "
        "causality, endorsement, alliance, or a new actor."
    ),
}


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=fields, extrasaction="ignore", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)


def ensure_fields(fields: list[str], additions: list[str]) -> list[str]:
    return fields + [field for field in additions if field not in fields]


def overlay_by_family(root: Path, family: str) -> dict[str, dict[str, str]]:
    _, rows = read_csv(root / OVERLAY_PATH)
    result = {
        row["object_id"]: row for row in rows if row["task_family"] == family
    }
    expected = 14 if family == "HR020" else 19
    if len(result) != expected:
        raise ValueError(f"{family} overlay must contain {expected} decisions")
    return result


def apply_queue_overlay(
    path: Path,
    overlay: dict[str, dict[str, str]],
    *,
    key_field: str,
    note_field: str,
) -> None:
    fields, rows = read_csv(path)
    fields = ensure_fields(
        fields,
        [
            "decision",
            "human_reviewer",
            "review_date",
            note_field,
            "approved_formulation",
            "scope_boundary",
            "decision_source_report",
        ],
    )
    seen: set[str] = set()
    for row in rows:
        key = row[key_field]
        if key not in overlay:
            continue
        item = overlay[key]
        row["decision"] = item["decision"]
        row["human_reviewer"] = item["human_reviewer"]
        row["review_date"] = item["review_date"]
        row[note_field] = (
            f"{item['approved_formulation']} | 边界：{item['scope_boundary']}"
        )
        row["approved_formulation"] = item["approved_formulation"]
        row["scope_boundary"] = item["scope_boundary"]
        row["decision_source_report"] = item["source_report"]
        seen.add(key)
    if seen != set(overlay):
        raise ValueError(f"Overlay keys missing from {path}: {sorted(set(overlay) - seen)}")
    write_csv(path, fields, rows)


def r5_entity_key(row: dict[str, str]) -> str:
    if row["actor_id"]:
        return f"ACTOR:{row['actor_id']}"
    if row.get("identity_group_id"):
        return f"EVENT_ONLY:{row['identity_group_id']}"
    return f"NAME:{row['participant_key']}"


def merge_r5(
    root: Path, overlay: dict[str, dict[str, str]], *, render_figures: bool
) -> dict[str, int]:
    registry = {
        row["actor_id"]: row for row in read_csv(root / REGISTRY_PATH)[1]
    }
    fields, rows = read_csv(root / R5_PARTICIPATION_PATH)
    source_names = {row["participant_key"]: row["source_name"] for row in rows}
    fields = ensure_fields(
        fields,
        [
            "identity_group_id",
            "identity_decision_id",
            "identity_note",
            "decision_source_report",
        ],
    )
    by_key = {row["participant_key"]: row for row in rows}
    if len(by_key) != 169:
        raise ValueError("R5 participation table must contain 169 unique rows")
    if set(R5_PATCHES) - set(by_key):
        raise ValueError(f"Missing R5 participant keys: {sorted(set(R5_PATCHES) - set(by_key))}")

    for key, patch in R5_PATCHES.items():
        by_key[key].update(patch)
        if by_key[key]["actor_id"]:
            actor = registry[by_key[key]["actor_id"]]
            by_key[key]["canonical_name"] = actor["canonical_name"]
            by_key[key]["origin_type"] = actor["origin_type"]
            by_key[key]["actor_class"] = actor["actor_class"]
        if by_key[key]["identity_decision_id"] == "HR020-06":
            by_key[key]["event_observation_status"] = (
                "human_checked_source_segmentation"
            )

    if any(row["identity_status"] == "alias_pending" for row in rows):
        pending = [
            row["participant_key"]
            for row in rows
            if row["identity_status"] == "alias_pending"
        ]
        raise ValueError(f"HR-020 left alias-pending rows: {pending}")
    if source_names != {row["participant_key"]: row["source_name"] for row in rows}:
        raise AssertionError("HR-020 must not rewrite source_name")

    events_by_entity: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        events_by_entity[r5_entity_key(row)].add(row["event_id"])
    for row in rows:
        count = len(events_by_entity[r5_entity_key(row)])
        if count > 1:
            row["relation_strength"] = f"repeated_public_participation_{count}_events"
        elif row["identity_status"] == "registry_actor":
            row["relation_strength"] = "single_event_registry_participation"
        elif row["identity_status"] == "event_only_identity_human_checked":
            row["relation_strength"] = "single_event_human_reviewed_identity"
        else:
            row["relation_strength"] = "single_event_observation"

    write_csv(root / R5_PARTICIPATION_PATH, fields, rows)

    event_fields = [
        "event_id",
        "event_name",
        "event_date",
        "event_year",
        "action_type",
        "role_vocabulary",
        "target_institution",
        "issue_tags",
        "place_tags",
        "source_refs",
        "source_locator",
        "declared_participant_count",
        "structured_participant_count",
        "registry_actor_rows",
        "human_reviewed_event_only_rows",
        "event_only_name_rows",
        "alias_pending_rows",
        "interpretation_limit",
    ]
    event_rows: list[dict[str, str]] = []
    for event_id, meta in R5_EVENT_META.items():
        items = [row for row in rows if row["event_id"] == event_id]
        counts = Counter(row["identity_status"] for row in items)
        event_rows.append(
            {
                "event_id": event_id,
                **meta,
                "structured_participant_count": str(len(items)),
                "registry_actor_rows": str(counts["registry_actor"]),
                "human_reviewed_event_only_rows": str(
                    counts["event_only_identity_human_checked"]
                ),
                "event_only_name_rows": str(counts["event_only_name"]),
                "alias_pending_rows": "0",
                "interpretation_limit": (
                    "Source-list participation is event-level only; counts are not "
                    "membership, alliance, funding or influence measures."
                ),
            }
        )
    write_csv(root / R5_DIR / "event_catalog_v0.csv", event_fields, event_rows)

    edge_fields = [
        "edge_id",
        "event_id",
        "participant_key",
        "entity_key",
        "actor_id",
        "identity_group_id",
        "canonical_name",
        "source_name",
        "identity_status",
        "identity_decision_id",
        "action_type",
        "role",
        "relation_strength",
        "source_refs",
        "review_status",
        "interpretation_limit",
    ]
    edges = []
    for index, row in enumerate(rows, 1):
        edges.append(
            {
                "edge_id": f"R5BE{index:03d}",
                "event_id": row["event_id"],
                "participant_key": row["participant_key"],
                "entity_key": r5_entity_key(row),
                "actor_id": row["actor_id"],
                "identity_group_id": row.get("identity_group_id", ""),
                "canonical_name": row["canonical_name"],
                "source_name": row["source_name"],
                "identity_status": row["identity_status"],
                "identity_decision_id": row.get("identity_decision_id", ""),
                "action_type": row["action_type"],
                "role": row["role"],
                "relation_strength": row["relation_strength"],
                "source_refs": row["source_refs"],
                "review_status": row["identity_review_status"],
                "interpretation_limit": row["interpretation_limit"],
            }
        )
    write_csv(
        root / R5_DIR / "actor_event_bipartite_edges_v0.csv", edge_fields, edges
    )

    entity_rows: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        entity_rows[r5_entity_key(row)].append(row)
    bridge_fields = [
        "bridge_id",
        "entity_key",
        "identity_scope",
        "actor_id",
        "identity_group_id",
        "canonical_name",
        "origin_type",
        "actor_class",
        "event_count",
        "event_ids",
        "action_types",
        "roles",
        "first_year",
        "last_year",
        "relation_strength",
        "evidence_basis",
        "interpretation_limit",
    ]
    bridges: list[dict[str, str]] = []
    for entity_key, items in entity_rows.items():
        event_ids = sorted(
            {item["event_id"] for item in items},
            key=lambda event_id: int(R5_EVENT_META[event_id]["event_year"]),
        )
        if len(event_ids) < 2:
            continue
        first = items[0]
        identity_scope = (
            "registry_actor"
            if entity_key.startswith("ACTOR:")
            else "human_reviewed_event_only"
        )
        if identity_scope == "human_reviewed_event_only" and not all(
            item["identity_status"] == "event_only_identity_human_checked"
            for item in items
        ):
            raise AssertionError("Only human-reviewed event-only identities may bridge")
        years = [int(R5_EVENT_META[event_id]["event_year"]) for event_id in event_ids]
        bridges.append(
            {
                "bridge_id": "",
                "entity_key": entity_key,
                "identity_scope": identity_scope,
                "actor_id": first["actor_id"],
                "identity_group_id": first.get("identity_group_id", ""),
                "canonical_name": first["canonical_name"],
                "origin_type": first["origin_type"],
                "actor_class": first["actor_class"],
                "event_count": str(len(event_ids)),
                "event_ids": ";".join(event_ids),
                "action_types": ";".join(
                    sorted({item["action_type"] for item in items})
                ),
                "roles": ";".join(sorted({item["role"] for item in items})),
                "first_year": str(min(years)),
                "last_year": str(max(years)),
                "relation_strength": (
                    f"repeated_public_participation_{len(event_ids)}_events"
                ),
                "evidence_basis": ";".join(
                    sorted({item["source_refs"] for item in items})
                ),
                "interpretation_limit": (
                    "Strict repeated identity across sampled public actions only; "
                    "not proof of stable alliance, membership or continuous coordination."
                ),
            }
        )
    bridges.sort(
        key=lambda row: (
            -int(row["event_count"]),
            row["identity_scope"] != "registry_actor",
            row["canonical_name"].casefold(),
        )
    )
    for index, row in enumerate(bridges, 1):
        row["bridge_id"] = f"R5BR{index:02d}"
    write_csv(
        root / R5_DIR / "repeat_participation_bridges_v0.csv",
        bridge_fields,
        bridges,
    )

    overlap_fields = [
        "event_a",
        "event_b",
        "confirmed_registry_actors_a",
        "confirmed_registry_actors_b",
        "shared_confirmed_registry_actors",
        "jaccard_confirmed_registry",
        "shared_actor_ids",
        "strict_identities_a",
        "strict_identities_b",
        "shared_strict_identities",
        "jaccard_strict_identity",
        "shared_entity_keys",
        "interpretation_limit",
    ]
    registry_sets: dict[str, set[str]] = defaultdict(set)
    strict_sets: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        key = r5_entity_key(row)
        if row["actor_id"]:
            registry_sets[row["event_id"]].add(row["actor_id"])
        if row["actor_id"] or row["identity_status"] == "event_only_identity_human_checked":
            strict_sets[row["event_id"]].add(key)
    overlaps = []
    event_ids = list(R5_EVENT_META)
    for index, event_a in enumerate(event_ids):
        for event_b in event_ids[index + 1 :]:
            shared_registry = sorted(
                registry_sets[event_a] & registry_sets[event_b]
            )
            registry_union = registry_sets[event_a] | registry_sets[event_b]
            shared_strict = sorted(strict_sets[event_a] & strict_sets[event_b])
            strict_union = strict_sets[event_a] | strict_sets[event_b]
            overlaps.append(
                {
                    "event_a": event_a,
                    "event_b": event_b,
                    "confirmed_registry_actors_a": str(len(registry_sets[event_a])),
                    "confirmed_registry_actors_b": str(len(registry_sets[event_b])),
                    "shared_confirmed_registry_actors": str(len(shared_registry)),
                    "jaccard_confirmed_registry": (
                        f"{len(shared_registry) / len(registry_union):.4f}"
                        if registry_union
                        else "0.0000"
                    ),
                    "shared_actor_ids": ";".join(shared_registry),
                    "strict_identities_a": str(len(strict_sets[event_a])),
                    "strict_identities_b": str(len(strict_sets[event_b])),
                    "shared_strict_identities": str(len(shared_strict)),
                    "jaccard_strict_identity": (
                        f"{len(shared_strict) / len(strict_union):.4f}"
                        if strict_union
                        else "0.0000"
                    ),
                    "shared_entity_keys": ";".join(shared_strict),
                    "interpretation_limit": (
                        "Strict overlap includes registry actors plus HR-020-confirmed "
                        "event-only identities; it is not a stable-alliance measure."
                    ),
                }
            )
    write_csv(root / R5_DIR / "event_overlap_v0.csv", overlap_fields, overlaps)

    identity_counts = Counter(row["identity_status"] for row in rows)
    event_only_bridges = sum(
        row["identity_scope"] == "human_reviewed_event_only" for row in bridges
    )
    readme = dedent(
        f"""
        # R05 co-action network v1

        HR-020 is merged: all 14 identity/segmentation decisions are
        `human_checked`. The package contains 169 source-list observations,
        {len(bridges)} strict repeated identities ({len(bridges) - event_only_bridges}
        registry actors and {event_only_bridges} human-reviewed event-only
        identities).

        `source_name` remains literal. Event-only identities remain outside the
        actor registry. Repeated participation and co-signing are event-level
        observations, not stable alliances, membership, funding, hierarchy or
        continuous coordination.

        Regeneration order:

        ```powershell
        python scripts\\make_r05_coaction_v1.py
        python scripts\\merge_hr020_hr026_v1.py
        ```
        """
    ).strip() + "\n"
    (root / R5_DIR / "README.md").write_text(readme, encoding="utf-8")
    brief = dedent(
        f"""
        # R5 共同行动网络解释性简报 v1

        三张一手名单仍是 **169 条组织／名称—事件观察**，不是组织间联盟网。
        HR-020 已完成 14/14：错误的 A054、A008、A072、A106 映射已移除，
        A110 获得 2020 事件参与；2010 缺分隔符继续保留为两个组织。

        严格身份重算后共有 **{len(bridges)} 个重复参与实体**：
        {len(bridges) - event_only_bridges} 个 registry actor，加上
        {event_only_bridges} 个经人工确认但仍不入 registry 的 event-only
        身份。后者是大阪基地撤去会、二见以北十区、環瀬戸内海会議、
        海の生き物を守る会、みん宿ヤポネシア、じゅごんの里。

        北限のジュゴンを見守る会与調査チーム・ザン保留母体／现场队
        的区别；两个“命どぅ宝”组织保持分离；“自然の権利”基金不再
        被当作 JELF 别名。任何重复出现都只说明跨样本公开参与，不能
        推定稳定联盟、组织成员关系、长期连续性或政策影响。
        """
    ).strip() + "\n"
    (root / R5_DIR / "R05_explanatory_brief_v0.md").write_text(
        brief, encoding="utf-8"
    )
    validation = dedent(
        f"""
        # R05 validation report v1

        - PASS — participation rows: 169 (67 / 31 / 71).
        - PASS — HR-020 decisions merged: 14/14.
        - PASS — literal `source_name` values preserved.
        - PASS — alias pending rows: 0.
        - PASS — registry/event-only-human/event-only-unreviewed:
          {identity_counts['registry_actor']} /
          {identity_counts['event_only_identity_human_checked']} /
          {identity_counts['event_only_name']}.
        - PASS — strict repeat bridges: {len(bridges)}, including
          {event_only_bridges} human-reviewed event-only identities.
        - PASS — event-only identities have no actor ID and do not enter registry.
        - PASS — co-signing/repeat participation is not encoded as stable alliance.
        """
    ).strip() + "\n"
    (root / R5_DIR / "validation_report_v0.md").write_text(
        validation, encoding="utf-8"
    )
    if render_figures:
        render_r5_figures(root, event_rows, bridges)
    return {
        "r5_participation_rows": len(rows),
        "r5_strict_repeat_bridges": len(bridges),
        "r5_event_only_repeat_bridges": event_only_bridges,
    }


def merge_r9(
    root: Path, overlay: dict[str, dict[str, str]], *, render_figures: bool
) -> dict[str, int]:
    fields, rows = read_csv(root / R9_EVENT_PATH)
    fields = ensure_fields(
        fields,
        [
            "event_status",
            "review_status",
            "human_review_decision",
            "human_reviewer",
            "review_date",
            "approved_formulation",
            "scope_boundary",
            "decision_source_report",
        ],
    )
    by_id = {row["record_id"]: row for row in rows}
    if len(by_id) != 19:
        raise ValueError("R9 election interface must contain 19 unique records")
    for record_id, row in by_id.items():
        review_id = f"HR026-{int(record_id[-3:]):02d}"
        item = overlay[review_id]
        row["event_status"] = "confirmed_observed_action"
        row["review_status"] = "human_checked"
        row["human_review_decision"] = item["decision"]
        row["human_reviewer"] = item["human_reviewer"]
        row["review_date"] = item["review_date"]
        row["approved_formulation"] = item["approved_formulation"]
        row["scope_boundary"] = item["scope_boundary"]
        row["decision_source_report"] = item["source_report"]
        row["machine_status"] = "human_review_merged"
        row.update(R9_PATCHES.get(record_id, {}))
    write_csv(root / R9_EVENT_PATH, fields, rows)

    source_fields, sources = read_csv(root / R9_SOURCE_PATH)
    source_by_id = {row["proposal_id"]: row for row in sources}
    source_by_id["R9EC_S022"] = dict(R9_SOURCE_022)
    sources = sorted(source_by_id.values(), key=lambda row: int(row["proposal_id"][-3:]))
    write_csv(root / R9_SOURCE_PATH, source_fields, sources)

    gap_fields, gaps = read_csv(root / R9_GAP_PATH)
    for row in gaps:
        if row["gap_id"] == "R9EC_G04":
            row["safe_current_use"] = (
                "Use the reported 26 themes/74 questions; the two talks are "
                "announcement-only and excluded from confirmed-held counts."
            )
    write_csv(root / R9_GAP_PATH, gap_fields, gaps)

    window_fields = [
        "election_id",
        "election_year",
        "election_name",
        "official_vote_date",
        "official_context_source",
        "candidate_event_rows",
        "confirmed_observed_action_rows",
        "announced_not_occurrence_verified_rows",
        "action_types_observed",
        "pre_campaign_rows",
        "campaign_rows",
        "post_result_rows",
        "online_status",
        "online_limit",
    ]
    official = {
        "2014": ("2014-11-16", "R9EC_S001"),
        "2018": ("2018-09-30", "R9EC_S008"),
        "2022": ("2022-09-11", "R9EC_S014"),
    }
    limits: dict[str, list[str]] = defaultdict(list)
    for gap in gaps:
        limits[gap["election_year"]].append(gap["missing_detail"])
    windows = []
    for year in ("2014", "2018", "2022"):
        items = [row for row in rows if row["election_year"] == year]
        phase = Counter(row["window_phase"] for row in items)
        windows.append(
            {
                "election_id": f"R9GE{year}",
                "election_year": year,
                "election_name": f"{year} Okinawa gubernatorial election",
                "official_vote_date": official[year][0],
                "official_context_source": official[year][1],
                "candidate_event_rows": str(len(items)),
                "confirmed_observed_action_rows": str(
                    sum(
                        row["event_status"] == "confirmed_observed_action"
                        for row in items
                    )
                ),
                "announced_not_occurrence_verified_rows": str(
                    sum(
                        row["event_status"]
                        == "announced_not_occurrence_verified"
                        for row in items
                    )
                ),
                "action_types_observed": ";".join(
                    sorted({row["action_type"] for row in items})
                ),
                "pre_campaign_rows": str(phase["pre_campaign"]),
                "campaign_rows": str(phase["campaign"]),
                "post_result_rows": str(phase["post_result"]),
                "online_status": "minimum_public_window_found",
                "online_limit": "; ".join(limits[year]),
            }
        )
    write_csv(root / R9_DIR / "three_election_windows_v1.csv", window_fields, windows)

    mode_fields = [
        "election_year",
        "action_type",
        "candidate_row_count",
        "confirmed_observed_action_count",
        "announced_not_occurrence_verified_count",
        "status_boundary",
    ]
    actions = [
        "endorsement",
        "issue_campaign",
        "public_meeting",
        "request",
        "observation",
    ]
    modes = []
    for year in ("2014", "2018", "2022"):
        for action in actions:
            items = [
                row
                for row in rows
                if row["election_year"] == year and row["action_type"] == action
            ]
            modes.append(
                {
                    "election_year": year,
                    "action_type": action,
                    "candidate_row_count": str(len(items)),
                    "confirmed_observed_action_count": str(
                        sum(
                            row["event_status"] == "confirmed_observed_action"
                            for row in items
                        )
                    ),
                    "announced_not_occurrence_verified_count": str(
                        sum(
                            row["event_status"]
                            == "announced_not_occurrence_verified"
                            for row in items
                        )
                    ),
                    "status_boundary": (
                        "human_checked actor-event role; row count is not reach, "
                        "votes, effect or stable alliance"
                    ),
                }
            )
    write_csv(root / R9_DIR / "intervention_mode_counts_v1.csv", mode_fields, modes)

    action_counts = Counter(row["action_type"] for row in rows)
    confirmed = sum(
        row["event_status"] == "confirmed_observed_action" for row in rows
    )
    announced = sum(
        row["event_status"] == "announced_not_occurrence_verified" for row in rows
    )
    brief = dedent(
        f"""
        # R9 选举—市民组织接口 brief v2

        HR-026 已完成 19/19。五类动作保持为：`endorsement`
        {action_counts['endorsement']}、`issue_campaign`
        {action_counts['issue_campaign']}、`observation`
        {action_counts['observation']}、`public_meeting`
        {action_counts['public_meeting']}、`request`
        {action_counts['request']}。

        其中 **{confirmed} 条**确认了已发生或已发布的可观察行动；
        R9EC018 仅确认两场 talk 的预告，状态为
        `announced_not_occurrence_verified`，不计入已举行事件。R9EC019
        只保留一条 E2 支持活动记录，主办方未确认，不能把“女性集会”
        actor 化。

        A059 的 2014 结成大会已用同日报道补足发生事实；新日本妇人会
        2014、2018、2022 三条均是国家组织，不转给 A115。政策提言
        workshop 只确认起草；候选问卷只确认实施与后续活动计划；
        All Okinawa 7.30 大会保持议题行动及其有争议的选举邻接语境。

        本包能说明组织如何以支持、议题行动、公共讨论、请求和信息生产
        进入选举公共空间；不能说明得票、投票率、胜负原因、说服效果、
        候选吸收或稳定联盟。
        """
    ).strip() + "\n"
    (root / R9_DIR / "R09_election_civic_interface_brief_v1.md").write_text(
        brief, encoding="utf-8"
    )
    readme = dedent(
        """
        # R09 election-civic interface v1

        HR-026 is merged: all 19 actor-event roles are `human_checked`.
        R9EC018 is announcement-only and excluded from confirmed-held counts;
        R9EC019 retains an unidentified organizer and is not actorized.

        The five action classes describe public interfaces, not electoral
        effects. No row licenses claims about votes, turnout, persuasion,
        victory causality, policy uptake, registry membership, or stable alliance.

        Regeneration order:

        ```powershell
        python scripts\\make_r09_election_civic_interface_v1.py
        python scripts\\merge_hr020_hr026_v1.py
        ```
        """
    ).strip() + "\n"
    (root / R9_DIR / "README.md").write_text(readme, encoding="utf-8")
    validation = dedent(
        f"""
        # R09 election-civic interface validation v2

        - PASS — HR-026 decisions merged: 19/19.
        - PASS — action counts: endorsement=4; issue_campaign=4;
          observation=5; public_meeting=2; request=4.
        - PASS — confirmed observed actions: {confirmed}.
        - PASS — announced but occurrence not verified: {announced} (R9EC018).
        - PASS — R9EC019 organizer remains unidentified and is not actorized.
        - PASS — no registry crosswalk to A115.
        - PASS — temporary bodies, candidates and parties remain event/institutional nodes.
        - PASS — no vote, turnout, persuasion, victory, policy-effect or stable-alliance inference.
        """
    ).strip() + "\n"
    (root / R9_DIR / "validation_report_v1.md").write_text(
        validation, encoding="utf-8"
    )
    if render_figures:
        render_r9_mode_figure(root, modes)
    return {
        "r9_event_rows": len(rows),
        "r9_confirmed_observed_actions": confirmed,
        "r9_announced_not_occurrence_verified": announced,
    }


def setup_plotting() -> None:
    import matplotlib.pyplot as plt
    from matplotlib import font_manager

    candidates = [
        "Microsoft YaHei",
        "Noto Sans CJK SC",
        "Noto Sans CJK JP",
        "SimHei",
        "DejaVu Sans",
    ]
    installed = {font.name for font in font_manager.fontManager.ttflist}
    font = next((name for name in candidates if name in installed), "DejaVu Sans")
    plt.rcParams.update(
        {
            "font.family": font,
            "axes.unicode_minus": False,
            "figure.facecolor": "#F7F4EE",
            "axes.facecolor": "#F7F4EE",
            "savefig.facecolor": "#F7F4EE",
            "svg.hashsalt": "hr020-hr026-v1",
        }
    )


def render_r5_figures(
    root: Path,
    event_rows: list[dict[str, str]],
    bridges: list[dict[str, str]],
) -> None:
    import matplotlib.pyplot as plt

    setup_plotting()
    labels = ["2010 WWF 67", "2015 NACSJ 31", "2020 MMC 71"]
    categories = [
        ("registry_actor_rows", "registry actor", "#236B8E"),
        (
            "human_reviewed_event_only_rows",
            "人审 event-only",
            "#D8842F",
        ),
        ("event_only_name_rows", "其他 event-only", "#9AA0A6"),
    ]
    fig, ax = plt.subplots(figsize=(11.5, 6.8))
    left = [0, 0, 0]
    for field, label, color in categories:
        values = [int(row[field]) for row in event_rows]
        ax.barh(labels, values, left=left, label=label, color=color)
        left = [a + b for a, b in zip(left, values)]
    ax.set_title("R5 三次公开行动：身份层构成（HR-020 已合并）", loc="left")
    ax.set_xlabel("来源名单行；不是联盟成员数")
    ax.legend(frameon=False, ncol=3, loc="lower center", bbox_to_anchor=(0.5, -0.28))
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.grid(axis="x", alpha=0.25)
    fig.text(
        0.02,
        0.02,
        "共同署名只证明事件参与；event-only 身份未进入 registry。",
        color="#5A4D3F",
    )
    fig.tight_layout(rect=[0, 0.09, 1, 1])
    fig.savefig(
        root / R5_DIR / "fig_r05_event_bipartite_v0.png",
        dpi=180,
        metadata={"Software": "merge_hr020_hr026_v1.py"},
    )
    plt.close(fig)

    event_ids = list(R5_EVENT_META)
    fig, ax = plt.subplots(figsize=(12.5, max(7.5, len(bridges) * 0.38)))
    for index, row in enumerate(bridges):
        xs = [event_ids.index(event_id) for event_id in row["event_ids"].split(";")]
        color = "#236B8E" if row["identity_scope"] == "registry_actor" else "#D8842F"
        ax.plot([min(xs), max(xs)], [index, index], color=color, linewidth=1.8)
        ax.scatter(xs, [index] * len(xs), color=color, s=45, zorder=3)
    ax.set_xticks(range(3), labels)
    ax.set_yticks(
        range(len(bridges)),
        [
            ("[R] " if row["identity_scope"] == "registry_actor" else "[E] ")
            + row["canonical_name"]
            for row in bridges
        ],
        fontsize=8.5,
    )
    ax.invert_yaxis()
    ax.xaxis.tick_top()
    ax.set_title(
        f"严格身份口径下的重复公开参与（{len(bridges)} 个实体）",
        loc="left",
        pad=20,
    )
    ax.grid(axis="x", alpha=0.3)
    ax.spines[:].set_visible(False)
    fig.text(
        0.02,
        0.01,
        "[R] registry actor；[E] 人审 event-only。重复出现不等于稳定联盟或持续协调。",
        color="#5A4D3F",
    )
    fig.tight_layout(rect=[0, 0.035, 1, 1])
    fig.savefig(
        root / R5_DIR / "fig_r05_repeat_bridges_v0.png",
        dpi=180,
        metadata={"Software": "merge_hr020_hr026_v1.py"},
    )
    plt.close(fig)


def render_r9_mode_figure(root: Path, modes: list[dict[str, str]]) -> None:
    import matplotlib.pyplot as plt

    setup_plotting()
    actions = [
        "endorsement",
        "issue_campaign",
        "public_meeting",
        "request",
        "observation",
    ]
    labels = ["公开支持", "议题行动", "公共讨论", "请求/提案", "观察/信息"]
    colors = ["#C45850", "#2A6F6B", "#D69E2E", "#6B5B95", "#457B9D"]
    years = ["2014", "2018", "2022"]
    lookup = {
        (row["election_year"], row["action_type"]): int(row["candidate_row_count"])
        for row in modes
    }
    fig, ax = plt.subplots(figsize=(10.8, 6.6))
    bottoms = [0, 0, 0]
    for action, label, color in zip(actions, labels, colors):
        values = [lookup[(year, action)] for year in years]
        ax.bar(range(3), values, bottom=bottoms, label=label, color=color)
        bottoms = [a + b for a, b in zip(bottoms, values)]
    ax.set_xticks(range(3), years)
    ax.set_ylabel("人工已核 actor-event 记录")
    ax.set_title("三届县知事选：市民组织进入公共接口的方式", loc="left")
    ax.legend(frameon=False, ncol=3, loc="lower center", bbox_to_anchor=(0.5, -0.25))
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.grid(axis="y", alpha=0.25)
    fig.text(
        0.02,
        0.02,
        "19 条均经 HR-026；R9EC018 仅为活动预告，不计入已举行事件。条数不代表票数或效果。",
        color="#5A4D3F",
    )
    fig.tight_layout(rect=[0, 0.08, 1, 1])
    png = root / R9_DIR / "fig_r09_intervention_modes_v1.png"
    svg = root / R9_DIR / "fig_r09_intervention_modes_v1.svg"
    fig.savefig(
        png, dpi=180, metadata={"Software": "merge_hr020_hr026_v1.py"}
    )
    fig.savefig(svg, metadata={"Date": "2026-07-20"})
    plt.close(fig)
    svg.write_text(
        "\n".join(line.rstrip() for line in svg.read_text(encoding="utf-8").splitlines())
        + "\n",
        encoding="utf-8",
    )


def make_report(summary: dict[str, int]) -> str:
    return dedent(
        f"""
        # HR-020 / HR-026 principal-decision merge report v1

        Generated by `python scripts/merge_hr020_hr026_v1.py`.

        ## HR-020

        - Decisions applied: {summary['hr020_decisions']}/14.
        - R5 participation rows: {summary['r5_participation_rows']}.
        - Strict repeat identities: {summary['r5_strict_repeat_bridges']};
          {summary['r5_event_only_repeat_bridges']} are human-reviewed
          event-only identities and remain outside the registry.
        - Wrong A054/A008/A072/A106 mappings are removed; A110 receives only
          its source-backed 2020 event participation.
        - Literal source names are unchanged. Co-signing and repeat
          participation are not stable-alliance evidence.

        ## HR-026

        - Decisions applied: {summary['hr026_decisions']}/19.
        - Human-checked election-interface rows: {summary['r9_event_rows']}.
        - Confirmed observed actions: {summary['r9_confirmed_observed_actions']}.
        - Announcement with occurrence unverified:
          {summary['r9_announced_not_occurrence_verified']} (R9EC018).
        - R9EC019 organizer remains unidentified and is not actorized.
        - No vote, turnout, persuasion, victory-causality, policy-uptake or
          stable-alliance inference is introduced.

        ## Rebuild order

        This is an idempotent post-generation merge. If either candidate
        package is regenerated, rerun:

        ```powershell
        python scripts\\merge_principal_review_overlays_v1.py
        python scripts\\merge_hr020_hr026_v1.py
        ```
        """
    ).strip() + "\n"


def merge_hr020_hr026(
    root: Path = ROOT, *, render_figures: bool = True
) -> dict[str, int]:
    hr020 = overlay_by_family(root, "HR020")
    hr026 = overlay_by_family(root, "HR026")
    apply_queue_overlay(
        root / R5_QUEUE_PATH,
        hr020,
        key_field="queue_id",
        note_field="decision_note",
    )
    apply_queue_overlay(
        root / R9_QUEUE_PATH,
        hr026,
        key_field="review_item_id",
        note_field="review_note",
    )
    summary = {
        "hr020_decisions": len(hr020),
        "hr026_decisions": len(hr026),
    }
    summary.update(merge_r5(root, hr020, render_figures=render_figures))
    summary.update(merge_r9(root, hr026, render_figures=render_figures))
    report_path = root / REPORT_PATH
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(make_report(summary), encoding="utf-8")
    return summary


def main() -> None:
    summary = merge_hr020_hr026()
    print(
        "HR020/HR026 merged: "
        f"R5={summary['r5_participation_rows']} rows/"
        f"{summary['r5_strict_repeat_bridges']} strict repeat identities; "
        f"R9={summary['r9_event_rows']} reviewed rows/"
        f"{summary['r9_confirmed_observed_actions']} confirmed observed actions/"
        f"{summary['r9_announced_not_occurrence_verified']} announcement-only."
    )


if __name__ == "__main__":
    main()
