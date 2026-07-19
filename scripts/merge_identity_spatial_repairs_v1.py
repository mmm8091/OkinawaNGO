from __future__ import annotations

"""Apply principal-approved identity, scope and blocking place-key repairs.

This merge is intentionally narrower than the later HR-016--032 fact merge.
It applies only decisions that must be stable before downstream regeneration:

* actor-class and selected identity normalization from HR-019/HR-025;
* the A072 -> A071 duplicate tombstone and core-edge provenance;
* X014/X015 review-workflow versus analytical-scope separation;
* P021 Sakishima Islands and the AP048/AP049/AP117/AP118/AP123 decisions.

It does not decide lifecycle candidates, add unreviewed actor--actor relations,
or treat new URLs named in review reports as centrally integrated sources.
"""

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = Path("data/interim")
OUT = Path("outputs/identity_spatial_repairs_v1")

REVIEWER = "project_principal_user"

ACTOR_EXTRA_FIELDS = [
    "scope_status",
    "merged_duplicate_of",
    "human_decision",
    "review_task_id",
    "human_reviewer",
    "review_date",
    "reviewed_fields",
    "identity_review_ref",
]

EDGE_EXTRA_FIELDS = [
    "original_actor_id",
    "human_decision",
    "review_task_id",
    "human_reviewer",
    "review_date",
    "reviewed_fields",
    "scope_status",
    "place_semantic",
    "superseded_by_edge_id",
    "decision_source_report",
    "interpretation_limit",
]

ISSUE_EDGE_EXTRA_FIELDS = [
    "original_actor_id",
    "human_decision",
    "review_task_id",
    "human_reviewer",
    "review_date",
    "reviewed_fields",
    "scope_status",
    "superseded_by_edge_id",
    "decision_source_report",
    "interpretation_limit",
]

ACTOR_CLASS_UPDATES = {
    "A026": "citizen_group",
    "A089": "labor_union",
    "A090": "labor_union",
    "A091": "labor_union",
    "A092": "labor_union",
    "A093": "labor_union",
    "A114": "labor_union",
    "A105": "womens_organization",
    "A107": "womens_organization",
    "A111": "womens_organization",
    "A115": "womens_organization",
}

ACTOR_NAME_UPDATES = {
    "A058": "安保廃棄・くらしと民主主義を守る沖縄県統一行動連絡会議",
    "A059": "沖縄「建白書」を実現し未来を拓く島ぐるみ会議",
    "A067": "辺野古土砂搬出反対全国連絡協議会",
    "A068": "ヘリポート基地建設の是非を問う名護市民投票推進協議会",
    "A070": "Veterans For Peace Ryukyu/Okinawa Chapter Kokusai (VFP-ROCK)",
    "A071": "沖縄から基地をなくし世界の平和を求める市民連絡会",
}

IDENTITY_REPORTS = {
    "A023": "docs/human_review_return_HR025_batch07_v1.md",
    "A026": "docs/human_review_return_HR019_batch01_v1.md",
    "A054": "docs/human_review_return_HR025_batch07_v1.md",
    "A057": "docs/human_review_return_HR025_batch07_v1.md",
    "A058": "docs/human_review_return_HR025_batch07_v1.md",
    "A059": "docs/human_review_return_HR025_batch05_v1.md",
    "A067": "docs/human_review_return_HR019_edge_scope_batch17_v1.md",
    "A068": "docs/human_review_return_HR019_edge_scope_batch17_v1.md",
    "A070": "docs/human_review_return_HR025_batch05_v1.md",
    "A071": "docs/human_review_return_HR025_batch05_v1.md",
    "A072": "docs/human_review_return_HR025_batch05_v1.md",
    "X014": "docs/human_review_return_HR019_batch01_v1.md",
    "X015": "docs/human_review_return_HR019_batch01_v1.md",
}

ALIASES = [
    {
        "actor_id": "A058",
        "alias": "沖縄県統一連",
        "alias_type": "short_name",
        "source_ref": "",
        "notes": "HR-025 normalized short name; direct URL awaits central source-ID integration.",
    },
    {
        "actor_id": "A058",
        "alias": "安保廃棄沖縄県統一連",
        "alias_type": "short_name",
        "source_ref": "",
        "notes": "HR-025 documented newsletter form; direct URL awaits central source-ID integration.",
    },
    {
        "actor_id": "A059",
        "alias": "島ぐるみ会議",
        "alias_type": "short_name",
        "source_ref": "S029",
        "notes": "Do not collapse municipal 島ぐるみ会議 units into the prefectural umbrella actor.",
    },
    {
        "actor_id": "A067",
        "alias": "辺野古土砂全協",
        "alias_type": "short_name",
        "source_ref": "S040",
        "notes": "Short form for the normalized national liaison council name.",
    },
    {
        "actor_id": "A068",
        "alias": "名護市民投票推進協議会",
        "alias_type": "short_name",
        "source_ref": "S042",
        "notes": "1997 referendum-process actor; lifecycle/genealogy remains separately undecided.",
    },
    {
        "actor_id": "A068",
        "alias": "名護市民投票の会",
        "alias_type": "deprecated_working_name",
        "source_ref": "",
        "notes": "Legacy project label not supported as the formal name; retained only for provenance/search.",
    },
    {
        "actor_id": "A070",
        "alias": "Veterans for Peace Okinawa",
        "alias_type": "short_name",
        "source_ref": "S048",
        "notes": "Legacy concise English form; do not transfer all parent-organization activity.",
    },
    {
        "actor_id": "A070",
        "alias": "VFP-ROCK",
        "alias_type": "acronym",
        "source_ref": "S048",
        "notes": "Ryukyu/Okinawa Chapter Kokusai acronym.",
    },
    {
        "actor_id": "A070",
        "alias": "Veterans for Peace, Ryukyu/Okinawa (VFP ROC)",
        "alias_type": "name_variant",
        "source_ref": "S048",
        "notes": "Documented chapter-name variant.",
    },
    {
        "actor_id": "A070",
        "alias": "Chapter 1003 - Ryukyu Okinawa",
        "alias_type": "chapter_listing_variant",
        "source_ref": "S048",
        "notes": "Documented chapter-listing form.",
    },
    {
        "actor_id": "A070",
        "alias": "平和を求める元軍人の会・琉球沖縄国際支部",
        "alias_type": "japanese_name",
        "source_ref": "S048",
        "notes": "Japanese chapter name confirmed in HR-025.",
    },
    {
        "actor_id": "A071",
        "alias": "沖縄平和市民連絡会",
        "alias_type": "short_name",
        "source_ref": "",
        "notes": "Officially documented abbreviation; direct URL awaits central source-ID integration.",
    },
]


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


def ensure_fields(fields: list[str], additions: list[str]) -> list[str]:
    return fields + [field for field in additions if field not in fields]


def index_unique(rows: list[dict[str, str]], field: str) -> dict[str, dict[str, str]]:
    result = {row[field]: row for row in rows}
    if len(result) != len(rows):
        raise ValueError(f"duplicate {field}")
    return result


def remove_ref(value: str, unwanted: str) -> str:
    return ";".join(
        token.strip()
        for token in value.split(";")
        if token.strip() and token.strip() != unwanted
    )


def add_note(row: dict[str, str], text: str) -> None:
    current = row.get("notes", "").strip()
    if text not in current:
        row["notes"] = f"{current} {text}".strip()


def mark_actor_revision(
    row: dict[str, str],
    fields: str,
    task: str,
    report: str,
    date: str,
) -> None:
    row.update(
        {
            "human_decision": "revise",
            "review_task_id": task,
            "human_reviewer": REVIEWER,
            "review_date": date,
            "reviewed_fields": fields,
            "identity_review_ref": report,
        }
    )


def upsert_alias(rows: list[dict[str, str]], addition: dict[str, str]) -> None:
    matches = [
        row
        for row in rows
        if row.get("actor_id") == addition["actor_id"]
        and row.get("alias") == addition["alias"]
    ]
    if len(matches) > 1:
        raise ValueError(f"duplicate alias key: {addition['actor_id']} {addition['alias']}")
    if matches:
        matches[0].update(addition)
    else:
        rows.append(dict(addition))


def apply_actor_repairs(data: Path) -> tuple[int, int, int]:
    path = data / "01_actor_registry_initial_v0.csv"
    fields, rows = read_csv(path)
    fields = ensure_fields(fields, ACTOR_EXTRA_FIELDS)
    actors = index_unique(rows, "actor_id")

    required = set(ACTOR_CLASS_UPDATES) | set(ACTOR_NAME_UPDATES) | {
        "A023",
        "A054",
        "A057",
        "A072",
        "X014",
        "X015",
    }
    missing = required - set(actors)
    if missing:
        raise ValueError(f"missing actors for identity repair: {sorted(missing)}")

    for actor_id, actor_class in ACTOR_CLASS_UPDATES.items():
        actors[actor_id]["actor_class"] = actor_class
        mark_actor_revision(
            actors[actor_id],
            "actor_class",
            "HR-019",
            "docs/human_review_return_HR019_batch01_v1.md",
            "2026-07-19",
        )

    for actor_id, canonical_name in ACTOR_NAME_UPDATES.items():
        actors[actor_id]["canonical_name"] = canonical_name
        mark_actor_revision(
            actors[actor_id],
            "canonical_name",
            "HR-019/HR-025",
            IDENTITY_REPORTS[actor_id],
            "2026-07-19",
        )

    actors["A023"]["origin_type"] = "japan_domestic"
    mark_actor_revision(
        actors["A023"],
        "origin_type",
        "HR-025",
        IDENTITY_REPORTS["A023"],
        "2026-07-19",
    )
    actors["A054"]["legal_status_guess"] = "association_or_unclear"
    mark_actor_revision(
        actors["A054"],
        "legal_status_guess",
        "HR-025",
        IDENTITY_REPORTS["A054"],
        "2026-07-19",
    )
    actors["A057"]["origin_type"] = "japan_domestic"
    mark_actor_revision(
        actors["A057"],
        "origin_type",
        "HR-025",
        IDENTITY_REPORTS["A057"],
        "2026-07-19",
    )

    # Remove sources that the principal explicitly identified as belonging to
    # a different actor. New direct URLs stay in the review report/source-
    # proposal flow until they receive central source IDs.
    for actor_id in ("A048", "A058", "A071", "A072"):
        actors[actor_id]["source_refs"] = remove_ref(actors[actor_id]["source_refs"], "S031")
    actors["A048"]["source_refs"] = remove_ref(actors["A048"]["source_refs"], "S038")
    add_note(
        actors["A048"],
        "HR-025: S038 is the Kanto-block source, not direct A048 identity evidence.",
    )
    add_note(
        actors["A058"],
        "HR-025 normalized the full name; direct supporting URLs await central source-ID integration.",
    )
    add_note(
        actors["A071"],
        "HR-025 merged A072 as a duplicate; S031 belongs to A047 and was removed.",
    )

    actors["A072"].update(
        {
            "scope_status": "merged_duplicate",
            "merged_duplicate_of": "A071",
            "review_status": "rejected",
            "human_decision": "reject",
            "review_task_id": "HR-025",
            "human_reviewer": REVIEWER,
            "review_date": "2026-07-19",
            "reviewed_fields": "actor_identity;canonical_name;duplicate_crosswalk",
            "identity_review_ref": IDENTITY_REPORTS["A072"],
        }
    )
    add_note(
        actors["A072"],
        "Tombstone only: duplicate of A071; retain row for provenance and do not count as an active actor.",
    )

    actors["X014"].update(
        {
            "review_status": "human_checked",
            "scope_status": "watchlist_only",
            "human_decision": "accept",
            "review_task_id": "HR-019",
            "human_reviewer": REVIEWER,
            "review_date": "2026-07-19",
            "reviewed_fields": "review_status;scope_status",
            "identity_review_ref": IDENTITY_REPORTS["X014"],
        }
    )
    actors["X015"].update(
        {
            "review_status": "human_checked",
            "scope_status": "in_scope_limited",
            "human_decision": "revise",
            "review_task_id": "HR-019",
            "human_reviewer": REVIEWER,
            "review_date": "2026-07-19",
            "reviewed_fields": "review_status;scope_status",
            "identity_review_ref": IDENTITY_REPORTS["X015"],
        }
    )
    add_note(
        actors["X014"],
        "Scope is external funding-system watchlist only; no Okinawa recipient/project relation is confirmed.",
    )
    add_note(
        actors["X015"],
        "Limited scope: Sakishima community disaster-prevention/evacuation interface; no military stance, contract, or executed deployment inferred.",
    )

    write_csv(path, fields, rows)

    alias_path = data / "02_actor_aliases_initial_v0.csv"
    alias_fields, aliases = read_csv(alias_path)
    for alias in ALIASES:
        upsert_alias(aliases, alias)
    write_csv(alias_path, alias_fields, aliases)

    active = sum(row.get("scope_status") != "merged_duplicate" for row in rows)
    return len(rows), active, len(aliases)


def apply_place_registry(data: Path) -> int:
    path = data / "04_place_registry_v0.csv"
    fields, rows = read_csv(path)
    places = index_unique(rows, "place_id")
    addition = {
        "place_id": "P021",
        "place_name": "Sakishima Islands",
        "place_type": "region",
        "region": "Okinawa",
        "why_relevant": "Regional scale for sources that explicitly name Sakishima as a whole.",
        "phase1_priority": "high",
        "notes": (
            "只用于来源明确指称先岛整体、但不能下沉到与那国／石垣／宫古的观察；"
            "不得自动向 P011/P012/P013 扇出。 HR-025 approved 2026-07-19."
        ),
    }
    if "P021" in places:
        places["P021"].update(addition)
    else:
        rows.append(addition)
    write_csv(path, fields, rows)
    return len(rows)


def edge_decision(
    row: dict[str, str],
    *,
    decision: str,
    status: str,
    task: str,
    date: str,
    fields: str,
    scope_status: str,
    report: str,
    interpretation_limit: str,
) -> None:
    row.update(
        {
            "human_decision": decision,
            "review_status": status,
            "review_task_id": task,
            "human_reviewer": REVIEWER,
            "review_date": date,
            "reviewed_fields": fields,
            "scope_status": scope_status,
            "decision_source_report": report,
            "interpretation_limit": interpretation_limit,
        }
    )


def apply_actor_place_repairs(data: Path) -> tuple[int, int]:
    path = data / "08_actor_place_edges_initial_v0.csv"
    fields, rows = read_csv(path)
    fields = ensure_fields(fields, EDGE_EXTRA_FIELDS)
    edges = index_unique(rows, "edge_id")
    required = {"AP048", "AP049", "AP117", "AP118", "AP123"}
    missing = required - set(edges)
    if missing:
        raise ValueError(f"missing actor-place edges: {sorted(missing)}")

    edge_decision(
        edges["AP048"],
        decision="reject",
        status="rejected",
        task="HR-025",
        date="2026-07-19",
        fields="relation_existence;place_id;place_semantic",
        scope_status="retired_candidate",
        report="docs/human_review_return_HR024_HR025_batch03_v1.md",
        interpretation_limit=(
            "No public evidence supports an Okinawa recipient, project or place relation; "
            "this does not assert that no historical relation ever existed."
        ),
    )
    edges["AP048"]["place_semantic"] = ""

    edges["AP049"].update(
        {
            "place_id": "P021",
            "place_name": "Sakishima Islands",
            "relation_basis": (
                "PWJ reports FY2024 expansion of a community disaster-prevention contact network "
                "to the Sakishima Islands."
            ),
            "place_semantic": "site_presence",
            "evidence_level": "E4",
            "source_ref": "",
            "needs_local_retrieval": "no",
        }
    )
    edge_decision(
        edges["AP049"],
        decision="revise",
        status="needs_second_source",
        task="HR-025",
        date="2026-07-19",
        fields="place_id;place_name;relation_basis;place_semantic;evidence_level",
        scope_status="source_id_integration_pending",
        report="docs/human_review_return_HR024_HR025_batch03_v1.md",
        interpretation_limit=(
            "The source supports Sakishima as a whole only; do not fan out to Yonaguni, Ishigaki or "
            "Miyako, and do not infer headquarters, branch, permanent presence, contract or military stance. "
            "The direct annual-report URL still needs a central source ID."
        ),
    )

    edge_decision(
        edges["AP117"],
        decision="revise",
        status="human_revised",
        task="HR-025",
        date="2026-07-19",
        fields="actor_identity;place_semantic;source_boundary",
        scope_status="in_scope",
        report="docs/human_review_return_HR025_batch05_v1.md",
        interpretation_limit=(
            "Countywide public activity does not imply a precise headquarters, representation of all "
            "Okinawa residents, or stable alliance with co-participants."
        ),
    )
    edges["AP117"]["place_semantic"] = "site_presence"
    edges["AP117"]["source_ref"] = remove_ref(edges["AP117"]["source_ref"], "S031")

    edges["AP118"]["original_actor_id"] = "A072"
    edges["AP118"]["superseded_by_edge_id"] = "AP117"
    edge_decision(
        edges["AP118"],
        decision="reject",
        status="rejected",
        task="HR-025",
        date="2026-07-19",
        fields="actor_identity;duplicate_crosswalk;place_semantic",
        scope_status="retired_duplicate",
        report="docs/human_review_return_HR025_batch05_v1.md",
        interpretation_limit="A072 is a duplicate tombstone of A071; AP118 must not be counted or drawn.",
    )
    edges["AP118"]["source_ref"] = remove_ref(edges["AP118"]["source_ref"], "S031")

    edges["AP123"].update(
        {
            "place_id": "P007",
            "place_name": "Camp Foster",
            "place_semantic": "site_presence",
        }
    )
    edge_decision(
        edges["AP123"],
        decision="revise",
        status="human_revised",
        task="HR-025",
        date="2026-07-19",
        fields="place_id;place_name;place_semantic;interpretation_boundary",
        scope_status="in_scope",
        report="docs/human_review_return_HR018_preflight_HR025_AP123_batch02_v1.md",
        interpretation_limit=(
            "Bounded scholarship/Marine Gift Shop charity and fundraising venue; not headquarters, "
            "MCCS affiliation, political stance or alliance."
        ),
    )

    write_csv(path, fields, rows)
    retired = sum(row.get("scope_status", "").startswith("retired") for row in rows)
    return len(rows), retired


def apply_duplicate_issue_edge_provenance(data: Path) -> int:
    path = data / "07_actor_issue_edges_initial_v0.csv"
    fields, rows = read_csv(path)
    fields = ensure_fields(fields, ISSUE_EDGE_EXTRA_FIELDS)
    edges = index_unique(rows, "edge_id")
    pairs = {"AI174": "AI173", "AI175": "AI172"}
    for edge_id, retained_edge_id in pairs.items():
        row = edges[edge_id]
        row.update(
            {
                "original_actor_id": "A072",
                "actor_id": "A071",
                "review_status": "rejected",
                "human_decision": "reject",
                "review_task_id": "HR-025",
                "human_reviewer": REVIEWER,
                "review_date": "2026-07-19",
                "reviewed_fields": "actor_identity;duplicate_crosswalk",
                "scope_status": "retired_duplicate",
                "superseded_by_edge_id": retained_edge_id,
                "decision_source_report": "docs/human_review_return_HR025_batch05_v1.md",
                "interpretation_limit": (
                    "Retired only because A072 is a duplicate actor key; use the retained A071 edge "
                    "after its separate HR-019 scope decision."
                ),
                "source_ref": remove_ref(row.get("source_ref", ""), "S031"),
            }
        )
    for edge_id in ("AI172", "AI173"):
        edges[edge_id]["source_ref"] = remove_ref(edges[edge_id].get("source_ref", ""), "S031")
        add_note(
            edges[edge_id],
            "S031 removed because it belongs to A047; direct A071 sources await source-ID integration.",
        )
    write_csv(path, fields, rows)
    return len(pairs)


def apply_event_label_repairs(data: Path) -> int:
    path = data / "09_actor_event_venue_edges_v0.csv"
    fields, rows = read_csv(path)
    changed = 0
    for row in rows:
        if row.get("actor_or_counterpart_id") == "A068":
            row["actor_or_counterpart_name"] = ACTOR_NAME_UPDATES["A068"]
            changed += 1
        elif row.get("actor_or_counterpart_id") == "A070":
            row["actor_or_counterpart_name"] = ACTOR_NAME_UPDATES["A070"]
            changed += 1
        elif row.get("actor_or_counterpart_id") == "A071":
            row["actor_or_counterpart_name"] = ACTOR_NAME_UPDATES["A071"]
            changed += 1
        elif row.get("actor_or_counterpart_id") == "A072":
            row["actor_or_counterpart_id"] = "A071"
            row["actor_or_counterpart_name"] = ACTOR_NAME_UPDATES["A071"]
            changed += 1
    write_csv(path, fields, rows)
    return changed


def upsert_review_log(data: Path) -> None:
    path = data / "human_review_log_v0.csv"
    fields, rows = read_csv(path)
    key = "HR-019-HR-025-IDENTITY-SPATIAL"
    addition = {
        "task_id": key,
        "object_id": "identity_scope_AP048_AP049_AP117_AP118_AP123",
        "review_date": "2026-07-19",
        "human_reviewer": REVIEWER,
        "review_status": "human_revised",
        "evidence_level_final": "field-specific; see decision source reports",
        "publishable_claim": "bounded",
        "decision": "Apply identity/scope repair and place-key corrections",
        "review_note": (
            "A072 retained as duplicate tombstone; X014/X015 workflow and scope split; "
            "P021 added without geographic fan-out; AP049 awaits central source-ID integration."
        ),
        "next_steps": (
            "Apply remaining HR overlays, integrate review-report source proposals, regenerate "
            "derived modules, then rebuild HR-029 without filling its decisions."
        ),
    }
    existing = [row for row in rows if row.get("task_id") == key]
    if len(existing) > 1:
        raise ValueError(f"duplicate review-log task {key}")
    if existing:
        existing[0].update(addition)
    else:
        rows.append(addition)
    write_csv(path, fields, rows)


def write_summary(root: Path, summary: dict[str, int]) -> None:
    out = root / OUT
    out.mkdir(parents=True, exist_ok=True)
    rows = [{"metric": key, "value": str(value)} for key, value in summary.items()]
    write_csv(out / "merge_summary_v1.csv", ["metric", "value"], rows)
    (out / "README.md").write_text(
        "# Identity and spatial blocking repairs v1\n\n"
        "Principal-approved HR-019/HR-025 identity, scope and place-key decisions were applied "
        "to the central tables by `scripts/merge_identity_spatial_repairs_v1.py`.\n\n"
        "Important boundaries:\n\n"
        "- A072 is a provenance tombstone (`merged_duplicate_of=A071`), not an active actor.\n"
        "- A068 was renamed, but lifecycle/genealogy candidates remain undecided.\n"
        "- AP049 uses P021 Sakishima as a whole and remains source-ID-integration pending; it "
        "must not fan out to three island municipalities.\n"
        "- AP048/AP118 and duplicate A072 issue edges remain in the tables as rejected/retired "
        "provenance rows and must not enter figures.\n"
        "- New review-report URLs were not silently inserted into the central source log.\n",
        encoding="utf-8",
    )


def apply_identity_spatial_repairs(root: Path = ROOT) -> dict[str, int]:
    data = root / DATA
    registry_rows, active_rows, alias_rows = apply_actor_repairs(data)
    place_rows = apply_place_registry(data)
    actor_place_rows, retired_place_edges = apply_actor_place_repairs(data)
    retired_issue_edges = apply_duplicate_issue_edge_provenance(data)
    event_label_repairs = apply_event_label_repairs(data)
    upsert_review_log(data)
    summary = {
        "registry_rows": registry_rows,
        "active_actor_rows": active_rows,
        "alias_rows": alias_rows,
        "place_rows": place_rows,
        "actor_place_rows": actor_place_rows,
        "retired_place_edges": retired_place_edges,
        "retired_duplicate_issue_edges": retired_issue_edges,
        "event_label_repairs": event_label_repairs,
    }
    write_summary(root, summary)
    return summary


if __name__ == "__main__":
    result = apply_identity_spatial_repairs()
    print(
        "Identity/spatial repair complete: "
        + ", ".join(f"{key}={value}" for key, value in result.items())
    )
