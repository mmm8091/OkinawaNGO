from __future__ import annotations

"""Integrate HR-013 and the current online-wave source evidence.

This main-thread pass performs four bounded operations:

1. apply the user's HR-013 scope decisions and the HR-010 correction for A094;
2. add A111 and only its human-approved issue/place/event observations;
3. integrate source metadata from the registry gate and the post-HR013 edge
   activation package without approving any candidate relation;
4. preserve C010/C034 as background references and C029-C033 as explicit
   out-of-scope decisions outside the actor registry.

The pass is idempotent.  It deliberately does not merge the 54 post-HR013
actor-issue candidates; they remain routed to HR-010/HR-024.
"""

import csv
import re
from collections import defaultdict
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "interim"
OUT = ROOT / "outputs" / "hr013_online_wave_integration_v1"

ACTORS = DATA / "01_actor_registry_initial_v0.csv"
ALIASES = DATA / "02_actor_aliases_initial_v0.csv"
SOURCES = DATA / "05_source_log_initial_v0.csv"
ISSUE_EDGES = DATA / "07_actor_issue_edges_initial_v0.csv"
PLACE_EDGES = DATA / "08_actor_place_edges_initial_v0.csv"
EVENT_EDGES = DATA / "09_actor_event_venue_edges_v0.csv"
HUMAN_LOG = DATA / "human_review_log_v0.csv"
SCOPE_DECISIONS = DATA / "31_hr013_scope_decisions_v1.csv"

GATE_SOURCES = ROOT / "outputs" / "registry_expansion_gate_v1" / "source_proposals_v1.csv"
EDGE_SOURCES = (
    ROOT
    / "outputs"
    / "edge_activation_v1"
    / "post_hr013_source_evidence_crosswalk_v1.csv"
)

SOURCE_CROSSWALK = OUT / "source_crosswalk_v1.csv"
DECISION_OVERLAY = OUT / "HR013_human_decision_overlay_v1.csv"
MERGE_NOTE = OUT / "README.md"

TRACKING_QUERY_PREFIXES = ("utm_",)
TRACKING_QUERY_KEYS = {"fbclid", "gclid", "mc_cid", "mc_eid"}


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


def normalize_url(url: str) -> str:
    raw = (url or "").strip()
    parts = urlsplit(raw)
    scheme = parts.scheme.lower()
    hostname = (parts.hostname or "").lower()
    port = parts.port
    if port and not ((scheme == "http" and port == 80) or (scheme == "https" and port == 443)):
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
    return urlunsplit((scheme, netloc, path, urlencode(sorted(query_items)), ""))


def unique(values: list[str]) -> list[str]:
    return list(dict.fromkeys(value.strip() for value in values if value and value.strip()))


def joined(values: list[str], separator: str = ";") -> str:
    return separator.join(unique(values))


def first_year(value: str, title: str = "") -> str:
    for text in (value or "", title or ""):
        match = re.search(r"(?:19|20)\d{2}", text)
        if match:
            return match.group(0)
    if (value or "").lower() in {"current", "current page", "n.d.", "undated"}:
        return "2026"
    return value or "undated"


USER_SOURCES = [
    {
        "origin_key": "UHR013-C011-FOUNDATION-HOME",
        "origin_type": "HR-013 supplied URL, attribution corrected",
        "subject_id": "C011",
        "title": "公益財団法人おきなわ女性財団 公式サイト",
        "url": "https://www.okinawajosei.org/",
        "source_type": "foundation_site",
        "year": "2026",
        "supports": "Third-party program context for C011; not C011 organizational identity",
        "evidence_level": "E4",
        "review_status": "ai_seeded",
        "boundary": "The site belongs to おきなわ女性財団, not 沖縄県女性団体連絡協議会; do not label it C011's official site.",
        "priority": 0,
    },
    {
        "origin_key": "UHR013-C011-OT",
        "origin_type": "HR-013 human-reviewed source",
        "subject_id": "C011",
        "title": "沖縄タイムス―女団協、米軍性暴力を受け県民大会開催へ",
        "url": "https://www.okinawatimes.co.jp/articles/-/1474162",
        "source_type": "local_news",
        "year": "2024",
        "supports": "HR-013 A111: named chair and 2024 prefectural rally concerning U.S. military sexual violence",
        "evidence_level": "E4",
        "review_status": "human_checked",
        "boundary": "Event-level mobilization; does not create stable alliance edges among participating groups.",
        "priority": 0,
    },
    {
        "origin_key": "UHR013-C011-RS",
        "origin_type": "HR-013 human-reviewed source",
        "subject_id": "C011",
        "title": "琉球新報―女団協、米軍性暴力を巡る県民大会を呼び掛け",
        "url": "https://ryukyushimpo.jp/national/entry-3299439.html",
        "source_type": "local_news",
        "year": "2024",
        "supports": "HR-013 A111: organizational history, named leadership and 2024 anti-sexual-violence mobilization",
        "evidence_level": "E4",
        "review_status": "human_checked",
        "boundary": "Use the historical base-removal action as a dated event, not proof of an unchanged alliance structure.",
        "priority": 0,
    },
    {
        "origin_key": "UHR013-C010",
        "origin_type": "HR-013 human-reviewed source",
        "subject_id": "C010",
        "title": "ひめゆり平和祈念財団について",
        "url": "https://www.himeyuri.or.jp/establish/foundation/",
        "source_type": "organization_site",
        "year": "2026",
        "supports": "HR-013 C010: public-interest foundation identity and war-memory/peace-education function",
        "evidence_level": "E4",
        "review_status": "human_checked",
        "boundary": "Background war-memory node only; do not infer an anti-base position or relation.",
        "priority": 0,
    },
    {
        "origin_key": "UHR013-C034",
        "origin_type": "HR-013 human-reviewed source",
        "subject_id": "C034",
        "title": "沖縄県サンゴ礁保全推進協議会 公式サイト",
        "url": "https://ocrcc.sakura.ne.jp/",
        "source_type": "organization_site",
        "year": "2026",
        "supports": "HR-013 C034: continuing mixed-sector coral-conservation platform",
        "evidence_level": "E4",
        "review_status": "human_checked",
        "boundary": "Background administrative/coral platform; membership or public collaboration does not imply an anti-base stance.",
        "priority": 0,
    },
    {
        "origin_key": "UHR013-MIYAKO-GW",
        "origin_type": "HR-013 human-reviewed candidate lead",
        "subject_id": "MGR-candidate",
        "title": "宮古島地下水研究会 公式サイト",
        "url": "https://miyakojima-tikasui.com/",
        "source_type": "organization_site",
        "year": "2026",
        "supports": "HR-013 follow-up lead: distinct Miyako groundwater organization for later direct phase-one assessment",
        "evidence_level": "E4",
        "review_status": "human_checked",
        "boundary": "Candidate lead only; does not resolve C015 identity and does not authorize registry entry.",
        "priority": 0,
    },
]


def collect_source_records() -> list[dict[str, str | int]]:
    records: list[dict[str, str | int]] = [row.copy() for row in USER_SOURCES]

    _, gate_rows = read_csv(GATE_SOURCES)
    for row in gate_rows:
        records.append(
            {
                "origin_key": row["proposal_id"],
                "origin_type": "registry_expansion_gate_v1",
                "subject_id": row["candidate_id"],
                "title": row["title"],
                "url": row["url"],
                "source_type": row["source_type"],
                "year": first_year(row["publication_or_record_date"], row["title"]),
                "supports": f"{row['candidate_id']}: {row['support_scope']}",
                "evidence_level": row["suggested_evidence_level"],
                "review_status": "ai_seeded",
                "boundary": row["caveat"],
                "priority": 1,
            }
        )

    _, edge_rows = read_csv(EDGE_SOURCES)
    for row in edge_rows:
        records.append(
            {
                "origin_key": row["source_key"],
                "origin_type": "edge_activation_post_HR013_v1",
                "subject_id": row["actor_id"],
                "title": row["source_title"],
                "url": row["source_url"],
                "source_type": row["source_type"],
                "year": first_year(row["source_date"], row["source_title"]),
                "supports": joined(
                    [
                        f"{row['actor_id']} identity: {row['identity_support']}",
                        f"direct issue support: {row['direct_issue_support']}",
                    ],
                    " | ",
                ),
                "evidence_level": row["evidence_level"],
                "review_status": "ai_seeded",
                "boundary": row["explanation_limit"],
                "priority": 2,
            }
        )
    return records


def integrate_sources() -> tuple[dict[str, str], dict[str, str], int]:
    fields, source_rows = read_csv(SOURCES)
    existing_by_norm: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in source_rows:
        if row.get("url"):
            existing_by_norm[normalize_url(row["url"])].append(row)

    records = collect_source_records()
    grouped: dict[str, list[dict[str, str | int]]] = defaultdict(list)
    order: list[str] = []
    for record in records:
        normalized = normalize_url(str(record["url"]))
        if normalized not in grouped:
            order.append(normalized)
        grouped[normalized].append(record)

    max_source_number = max(int(row["source_id"][1:]) for row in source_rows)
    origin_to_source: dict[str, str] = {}
    normalized_to_source: dict[str, str] = {}
    added = 0

    for normalized in order:
        group = sorted(grouped[normalized], key=lambda row: (int(row["priority"]), str(row["origin_key"])))
        matches = existing_by_norm.get(normalized, [])
        if matches:
            chosen_id = sorted(matches, key=lambda row: int(row["source_id"][1:]))[0]["source_id"]
        else:
            primary = group[0]
            max_source_number += 1
            chosen_id = f"S{max_source_number:03d}"
            review_status = str(primary["review_status"])
            source_rows.append(
                {
                    "source_id": chosen_id,
                    "source_type": str(primary["source_type"]),
                    "title": str(primary["title"]),
                    "year": str(primary["year"]),
                    "url": str(primary["url"]),
                    "what_it_supports": joined([str(row["supports"]) for row in group], " | "),
                    "evidence_level": str(primary["evidence_level"]),
                    "bias_note": joined([str(row["boundary"]) for row in group], " | "),
                    "review_status": review_status,
                    "notes": (
                        "HR-013/online-wave source integration 2026-07-13. Source inclusion does not approve "
                        "candidate actor-issue edges, actor entry, alliance, funding, or political-position inference."
                    ),
                }
            )
            existing_by_norm[normalized].append(source_rows[-1])
            added += 1
        normalized_to_source[normalized] = chosen_id
        for record in group:
            origin_to_source[str(record["origin_key"])] = chosen_id

    source_rows.sort(key=lambda row: int(row["source_id"][1:]))
    write_csv(SOURCES, fields, source_rows)

    crosswalk_fields = [
        "origin_type",
        "origin_key",
        "subject_id",
        "source_id",
        "normalized_url",
        "source_log_state",
        "source_review_status",
        "relation_or_claim_approved",
        "evidence_boundary",
    ]
    crosswalk_rows: list[dict[str, str]] = []
    current_ids = {row["source_id"] for row in source_rows}
    for record in records:
        normalized = normalize_url(str(record["url"]))
        source_id = origin_to_source[str(record["origin_key"])]
        crosswalk_rows.append(
            {
                "origin_type": str(record["origin_type"]),
                "origin_key": str(record["origin_key"]),
                "subject_id": str(record["subject_id"]),
                "source_id": source_id,
                "normalized_url": normalized,
                "source_log_state": "integrated_or_existing" if source_id in current_ids else "error",
                "source_review_status": str(record["review_status"]),
                "relation_or_claim_approved": "no",
                "evidence_boundary": str(record["boundary"]),
            }
        )
    if any(row["relation_or_claim_approved"] != "no" for row in crosswalk_rows):
        raise ValueError("Source integration must not approve candidate relations or claims")
    write_csv(SOURCE_CROSSWALK, crosswalk_fields, crosswalk_rows)
    return origin_to_source, normalized_to_source, added


def source_refs(origin_to_source: dict[str, str], keys: list[str]) -> str:
    return joined([origin_to_source[key] for key in keys])


def apply_registry_decisions(origin_to_source: dict[str, str]) -> None:
    actor_fields, actors = read_csv(ACTORS)
    actors = [row for row in actors if row["actor_id"] not in {"A094", "A111"}]
    c011_refs = source_refs(
        origin_to_source,
        ["GSP003", "GSP004", "GSP005", "GSP006", "UHR013-C011-OT", "UHR013-C011-RS"],
    )
    actors.append(
        {
            "actor_id": "A111",
            "canonical_name": "沖縄県女性団体連絡協議会",
            "actor_class": "womens_or_community_organization",
            "origin_type": "okinawa_local",
            "legal_status_guess": "informal_network",
            "primary_places": "Okinawa",
            "issue_tags": "women;peace;anti_base;human_rights",
            "source_refs": c011_refs,
            "evidence_level": "E4",
            "review_status": "human_checked",
            "needs_local_retrieval": "no",
            "review_priority": "P1",
            "notes": (
                "HR-013: women-focused prefectural network formed in 1967; dated base-related mobilization is documented for 1995 and 2024. "
                "Keep distinct from former A094 and A049. okinawajosei.org belongs to おきなわ女性財団 and is used only as a third-party program record. "
                "Public-event co-participation does not create stable alliance edges."
            ),
        }
    )
    actors.sort(key=lambda row: int(row["actor_id"][1:]))
    if len(actors) != 118:
        raise ValueError(f"HR-013 replacement should keep registry at 118, got {len(actors)}")
    if any(row["actor_id"] == "A094" for row in actors):
        raise ValueError("A094 must be absent after the HR-010 scope correction")
    if sum(row["actor_id"] == "A111" for row in actors) != 1:
        raise ValueError("A111 must occur exactly once")
    write_csv(ACTORS, actor_fields, actors)

    alias_fields, aliases = read_csv(ALIASES)
    aliases = [row for row in aliases if row["actor_id"] not in {"A094", "A111"}]
    aliases.extend(
        [
            {
                "actor_id": "A111",
                "alias": "県婦人団体連絡協議会",
                "alias_type": "former_name",
                "source_ref": origin_to_source["UHR013-C011-RS"],
                "notes": "HR-013: historical name used in the 1995 base-removal mobilization context.",
            },
            {
                "actor_id": "A111",
                "alias": "女団協",
                "alias_type": "acronym",
                "source_ref": origin_to_source["GSP005"],
                "notes": "HR-013: documented abbreviation. Do not transfer 沖女連, which is associated with former A094.",
            },
        ]
    )
    write_csv(ALIASES, alias_fields, aliases)


def next_numeric_id(rows: list[dict[str, str]], field: str, prefix: str) -> int:
    values = [int(row[field][len(prefix) :]) for row in rows if row[field].startswith(prefix)]
    return max(values, default=0) + 1


def apply_a111_observations(origin_to_source: dict[str, str]) -> None:
    issue_fields, issue_rows = read_csv(ISSUE_EDGES)
    issue_rows = [row for row in issue_rows if row["actor_id"] not in {"A094", "A111"}]
    next_issue = next_numeric_id(issue_rows, "edge_id", "AI")
    issue_specs = [
        ("I022", "women", "Prefectural women's-network identity and women-focused public action", ["UHR013-C011-OT", "UHR013-C011-RS"]),
        ("I019", "peace", "Long-running women-led peace mobilization, including dated 1995 and 2024 actions", ["UHR013-C011-RS"]),
        ("I001", "anti_base", "Dated base-removal and U.S.-military accountability mobilization", ["UHR013-C011-OT", "UHR013-C011-RS"]),
        ("I023", "human_rights", "2024 mobilization framed U.S.-military sexual violence as a rights and accountability issue", ["UHR013-C011-OT", "UHR013-C011-RS"]),
    ]
    for offset, (issue_id, label, basis, keys) in enumerate(issue_specs):
        issue_rows.append(
            {
                "edge_id": f"AI{next_issue + offset:03d}",
                "actor_id": "A111",
                "issue_id": issue_id,
                "issue_label": label,
                "relation_basis": basis,
                "source_ref": source_refs(origin_to_source, keys),
                "evidence_level": "E4",
                "review_status": "human_checked",
                "notes": "HR-013 human-approved actor-issue observation; dated mobilization does not imply a stable inter-organizational alliance.",
            }
        )
    write_csv(ISSUE_EDGES, issue_fields, issue_rows)

    place_fields, place_rows = read_csv(PLACE_EDGES)
    place_rows = [row for row in place_rows if row["actor_id"] not in {"A094", "A111"}]
    next_place = next_numeric_id(place_rows, "edge_id", "AP")
    place_rows.append(
        {
            "edge_id": f"AP{next_place:03d}",
            "actor_id": "A111",
            "place_id": "P001",
            "place_name": "Okinawa Prefecture",
            "relation_basis": "Prefecture-wide women's network and prefectural public mobilization",
            "source_ref": source_refs(origin_to_source, ["UHR013-C011-OT", "UHR013-C011-RS"]),
            "evidence_level": "E4",
            "review_status": "human_checked",
            "notes": "HR-013: broad prefectural field only; no municipality-level location is inferred.",
        }
    )
    write_csv(PLACE_EDGES, place_fields, place_rows)

    event_fields, event_rows = read_csv(EVENT_EDGES)
    event_rows = [
        row
        for row in event_rows
        if row["actor_or_counterpart_id"] not in {"A094", "A111"}
        and row["record_id"] != "AEV0065"
    ]
    event_rows.append(
        {
            "record_id": "AEV0065",
            "record_scope": "event",
            "event_id": "EV2024_WOMEN_ANTI_VIOLENCE_RALLY",
            "event_name": "2024 prefectural rally against U.S. military sexual violence",
            "event_year": "2024",
            "actor_or_counterpart_id": "A111",
            "legacy_candidate_id": "C011",
            "actor_or_counterpart_name": "沖縄県女性団体連絡協議会",
            "entity_type": "registry_actor",
            "action_type": "public_rally",
            "venue_id": "V015",
            "target_type": "government_accountability",
            "target_id_or_name": "Japan and U.S. governments / prevention and accountability policy",
            "role": "organizer_or_convener",
            "pathway_stage": "women_human_rights_public_mobilization",
            "evidence_level": "E4",
            "source_id": origin_to_source["UHR013-C011-OT"],
            "reviewer_status": "human_checked",
            "interpretation_limit": "Event-level organizing only; co-participation does not establish stable alliance ties.",
            "notes": "HR-013 human-reviewed event observation; attendance and co-organizers are not expanded beyond the cited source.",
            "review_decision": "accept",
            "human_reviewer": "project_principal_user",
            "review_date": "2026-07-13",
            "review_task_id": "HR-013",
        }
    )
    write_csv(EVENT_EDGES, event_fields, event_rows)


SCOPE_ROWS = [
    ("HR-013", "C010", "", "公益財団法人ひめゆり平和祈念財団", "background_actor", "war_memory_and_peace_education_background", "E4", "War-memory institution; no anti-base relation or political stance inferred."),
    ("HR-013", "C011", "A111", "沖縄県女性団体連絡協議会", "add_core_support", "women_peace_human_rights_mobilization", "E4", "Added as A111; event participation is not a stable alliance."),
    ("HR-013", "C029", "", "NPO法人ピースメーカーズネットワーク", "out_of_scope_reject", "general_public_interest", "identity_E4;phase1_scope_rejected", "A single documented 2014 Henoko symposium is retained in the evidence lineage but is insufficient for continuing phase-one inclusion."),
    ("HR-013", "C030", "", "特定非営利活動法人環境の未来を考える会", "out_of_scope_reject", "general_public_interest", "identity_E4;phase1_scope_rejected", "General resource-circulation activity without a retained continuing phase-one connection."),
    ("HR-013", "C031", "", "特定非営利活動法人宮古島自然緑化協会", "out_of_scope_reject", "general_public_interest", "identity_E4;phase1_scope_rejected", "General greening/coastal conservation without a retained military-facility controversy connection."),
    ("HR-013", "C032", "", "NPO法人美ぎ島MIYAKO", "out_of_scope_reject", "general_public_interest", "identity_E4;phase1_scope_rejected", "General environment/culture work; groundwater-deployment participation not established."),
    ("HR-013", "C033", "", "特定非営利活動法人おきなわ環境クラブ", "out_of_scope_reject", "general_public_interest", "identity_E4;phase1_scope_rejected", "General environmental education/wetland work without a retained direct phase-one connection."),
    ("HR-013", "C034", "", "沖縄県サンゴ礁保全推進協議会", "background_actor", "coral_conservation_administrative_background", "E4", "Mixed administrative/civic/scientific platform; no anti-base stance inferred."),
    ("HR-010", "A094", "", "一般社団法人沖縄県女性連合会", "remove_from_registry_scope", "general_womens_association", "identity_E4;phase1_scope_rejected", "Historical base-related events remain in the evidence lineage, but the human scope decision excludes this general women's association from the phase-one actor registry."),
]


def apply_scope_and_review_logs(origin_to_source: dict[str, str]) -> None:
    refs_by_object = {
        "C010": source_refs(origin_to_source, ["UHR013-C010", "GSP001", "GSP002"]),
        "C011": source_refs(origin_to_source, ["GSP003", "GSP004", "GSP005", "GSP006", "UHR013-C011-OT", "UHR013-C011-RS"]),
        "C029": source_refs(origin_to_source, ["GSP011", "GSP012", "GSP013"]),
        "C030": source_refs(origin_to_source, ["GSP014", "GSP015"]),
        "C031": source_refs(origin_to_source, ["GSP016", "GSP017"]),
        "C032": source_refs(origin_to_source, ["GSP018", "GSP019", "GSP020"]),
        "C033": source_refs(origin_to_source, ["GSP021", "GSP022"]),
        "C034": source_refs(origin_to_source, ["GSP023", "GSP024", "UHR013-C034", "GSP026"]),
        "A094": "S111",
    }
    scope_fields = [
        "task_id",
        "object_id",
        "registry_actor_id",
        "canonical_name",
        "decision",
        "analytical_layer",
        "source_refs",
        "evidence_level_final",
        "review_status",
        "interpretation_boundary",
    ]
    scope_rows = [
        {
            "task_id": task_id,
            "object_id": object_id,
            "registry_actor_id": registry_actor_id,
            "canonical_name": name,
            "decision": decision,
            "analytical_layer": layer,
            "source_refs": refs_by_object[object_id],
            "evidence_level_final": evidence,
            "review_status": (
                "rejected"
                if decision in {"out_of_scope_reject", "remove_from_registry_scope"}
                else "human_checked"
            ),
            "interpretation_boundary": boundary,
        }
        for task_id, object_id, registry_actor_id, name, decision, layer, evidence, boundary in SCOPE_ROWS
    ]
    write_csv(SCOPE_DECISIONS, scope_fields, scope_rows)
    write_csv(DECISION_OVERLAY, scope_fields, scope_rows)

    log_fields, log_rows = read_csv(HUMAN_LOG)
    keys_to_replace = {(row["task_id"], row["object_id"]) for row in scope_rows}
    log_rows = [row for row in log_rows if (row["task_id"], row["object_id"]) not in keys_to_replace]
    for row in scope_rows:
        decision = row["decision"]
        if decision == "add_core_support":
            claim = "Prefectural women's network with dated base-related and anti-sexual-violence mobilization"
            next_steps = "Use A111 in R1/R2 and event-level analysis; do not create alliance edges from umbrella participation."
        elif decision == "background_actor":
            claim = "Stable background institution/platform retained outside the phase-one movement actor registry"
            next_steps = "Use only as an explicitly labelled background node in the relevant explanatory module."
        elif decision == "remove_from_registry_scope":
            claim = "Organization identity exists, but the human scope decision removes it from the phase-one actor registry"
            next_steps = "Retain historical evidence lineage; do not reactivate A094 or transfer its alias to A111."
        else:
            claim = "Organization identity may be valid, but the human scope decision rejects phase-one registry inclusion"
            next_steps = "Keep outside the registry unless future direct, dated phase-one participation is human-reviewed."
        log_rows.append(
            {
                "task_id": row["task_id"],
                "object_id": row["object_id"],
                "review_date": "2026-07-13",
                "human_reviewer": "user",
                "review_status": row["review_status"],
                "evidence_level_final": row["evidence_level_final"],
                "publishable_claim": claim,
                "decision": decision,
                "review_note": row["interpretation_boundary"],
                "next_steps": next_steps,
            }
        )
    write_csv(HUMAN_LOG, log_fields, log_rows)


def validate() -> dict[str, int]:
    _, actors = read_csv(ACTORS)
    _, aliases = read_csv(ALIASES)
    _, sources = read_csv(SOURCES)
    _, issue_rows = read_csv(ISSUE_EDGES)
    _, place_rows = read_csv(PLACE_EDGES)
    _, event_rows = read_csv(EVENT_EDGES)
    _, scope_rows = read_csv(SCOPE_DECISIONS)
    _, crosswalk_rows = read_csv(SOURCE_CROSSWALK)
    if len(actors) != 118 or any(row["actor_id"] == "A094" for row in actors):
        raise ValueError("Registry replacement validation failed")
    if sum(row["actor_id"] == "A111" for row in actors) != 1:
        raise ValueError("A111 registry validation failed")
    if {row["alias"] for row in aliases if row["actor_id"] == "A111"} != {"県婦人団体連絡協議会", "女団協"}:
        raise ValueError("A111 alias boundary validation failed")
    if any(row["actor_id"] == "A094" for row in issue_rows + place_rows):
        raise ValueError("A094 remains in a current central edge table")
    if len([row for row in issue_rows if row["actor_id"] == "A111"]) != 4:
        raise ValueError("A111 must have four human-approved issue observations")
    if len([row for row in place_rows if row["actor_id"] == "A111"]) != 1:
        raise ValueError("A111 must have one broad-place observation")
    if len([row for row in event_rows if row["actor_or_counterpart_id"] == "A111"]) != 1:
        raise ValueError("A111 must have one bounded event observation")
    if len(scope_rows) != 9:
        raise ValueError("Expected eight HR-013 decisions plus one HR-010 correction")
    if any(row["relation_or_claim_approved"] != "no" for row in crosswalk_rows):
        raise ValueError("Source crosswalk incorrectly approves a claim")
    source_ids = [row["source_id"] for row in sources]
    if len(source_ids) != len(set(source_ids)):
        raise ValueError("Duplicate source IDs")
    return {
        "actors": len(actors),
        "sources": len(sources),
        "issue_edges": len(issue_rows),
        "place_edges": len(place_rows),
        "event_rows": len(event_rows),
        "source_crosswalk": len(crosswalk_rows),
        "wave_unique_sources": len({row["source_id"] for row in crosswalk_rows}),
        "wave_new_source_ids": len(
            {row["source_id"] for row in crosswalk_rows if int(row["source_id"][1:]) > 198}
        ),
    }


def write_note(counts: dict[str, int]) -> None:
    MERGE_NOTE.write_text(
        "\n".join(
            [
                "# HR-013 与下一轮线上来源主线程合并 v1",
                "",
                f"- Registry：{counts['actors']}；A094 按 HR-010 范围勘误移出，A111 按 HR-013 加入，净数不变。",
                f"- Source log：{counts['sources']}；本波 70 条来源引用归并为 {counts['wave_unique_sources']} 个 URL，其中 {counts['wave_new_source_ids']} 个为 S199 以后新增来源。",
                f"- Actor–issue：{counts['issue_edges']}，其中 A111 仅有 4 条 HR-013 人工批准观察。",
                f"- Actor–place：{counts['place_edges']}；A111 仅落 P001 全县场域。",
                f"- Event/venue：{counts['event_rows']}；新增 AEV0065 为 2024 县民大会组织角色。",
                f"- 来源交叉表：{counts['source_crosswalk']} 条，全部 `relation_or_claim_approved=no`。",
                "- 54 条 post-HR013 edge-activation 候选仍在人工任务队列，未写入 actor–issue 主表。",
                "- C010/C034 仅作背景节点，C029–C033 明确 out_of_scope；均不占 actor registry 计数。",
                "- `okinawajosei.org` 归属おきなわ女性財団，只作第三方项目记录；A111 不接收 `沖女連` 别名。",
                "- A094 的历史基地行动证据保留在取证谱系中；移出是本期范围决定，不是宣称其从无相关行动。",
                "",
                "运行 `python scripts/integrate_hr013_online_wave.py` 可幂等复现。",
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    origin_to_source, _, added_sources = integrate_sources()
    apply_registry_decisions(origin_to_source)
    apply_a111_observations(origin_to_source)
    apply_scope_and_review_logs(origin_to_source)
    counts = validate()
    write_note(counts)
    print(
        "HR-013 online-wave integration OK: "
        + " ".join(f"{key}={value}" for key, value in counts.items())
        + f" added_sources={added_sources}"
    )


if __name__ == "__main__":
    main()
