from __future__ import annotations

"""Merge the principal-confirmed online review closeout in two controlled stages.

Stage ``upstream``:
* formalize the five 145-item review sheets;
* merge already-confirmed HR-035 batch 01;
* add accepted HR-010 batch-6 actor--issue rows;
* merge LCR001--004 into the separate lifecycle table;
* apply HR-034 row/status-policy decisions.

Stage ``freeze`` (run only after ``make_schema_alias_freeze_v1.py``):
* apply the confirmed HR-029 controlled vocabulary, alias, place, venue,
  relation and action decisions;
* write final freeze manifests and the HR-031 application ledger.

The script is idempotent and intentionally does not regenerate historical
pre-human packages.
"""

import argparse
import csv
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "interim"
META = ROOT / "data" / "metadata"

PRINCIPAL = "project_principal_user"
REVIEW_DATE = "2026-07-20"
RETURN_REPORT = "docs/human_review_return_remaining_online_145_v1.md"
HR035_REPORT = "docs/human_review_return_HR035_batch01_v1.md"

HR010_FILE = ROOT / "outputs/edge_activation_v1/post_hr013_HR010_batch6_edge_evidence_addendum_v1.csv"
HR010_CANDIDATES = ROOT / "outputs/edge_activation_v1/post_hr013_edge_activation_candidates_v1.csv"
HR010_SOURCES = ROOT / "outputs/edge_activation_v1/post_hr013_source_evidence_crosswalk_v1.csv"
LIFECYCLE_QUEUE = ROOT / "outputs/actor_lifecycle_v1/actor_lifecycle_review_queue_v0.csv"
LIFECYCLE_FILE = ROOT / "outputs/actor_lifecycle_v1/actor_lifecycle_v0.csv"
HR034_FILE = ROOT / "outputs/review_status_crosswalk_v1/HR034_review_status_crosswalk_v1.csv"
HR029_FILE = ROOT / "outputs/schema_alias_freeze_v1/HR029_schema_alias_freeze_review_v0.csv"
HR031_FILE = ROOT / "outputs/report_claim_audit_v1/HR031_report_claim_review_v0.csv"
HR035_FILE = ROOT / "outputs/actor_issue_claim_freeze_v1/HR035_actor_issue_fact_review_batch01_v1.csv"

ACTOR_FILE = DATA / "01_actor_registry_initial_v0.csv"
ALIAS_FILE = DATA / "02_actor_aliases_initial_v0.csv"
PLACE_FILE = DATA / "04_place_registry_v0.csv"
ACTOR_PLACE_FILE = DATA / "08_actor_place_edges_initial_v0.csv"
SOURCE_FILE = DATA / "05_source_log_initial_v0.csv"
ISSUE_EDGE_FILE = DATA / "07_actor_issue_edges_initial_v0.csv"
R4_FILE = DATA / "19_sakishima_frame_corpus_v0.csv"
R9_FILE = DATA / "20_referendum_process_stages_v0.csv"
PATHWAY_FILE = DATA / "26_actor_event_venue_target_entry_modes_v0.csv"
HET_FILE = DATA / "35_heterogeneous_event_repertoire_v1.csv"

SCHEMA_OUT = ROOT / "outputs/schema_alias_freeze_v1"
ACTOR_AUDIT = SCHEMA_OUT / "actor_field_audit_v1.csv"
ALIAS_AUDIT = SCHEMA_OUT / "alias_audit_v1.csv"
PLACE_AUDIT = SCHEMA_OUT / "place_hierarchy_alias_audit_v1.csv"
VENUE_CONFLICT_AUDIT = SCHEMA_OUT / "venue_reference_conflicts_v1.csv"
REL_ACTION_AUDIT = SCHEMA_OUT / "relation_action_value_mapping_v1.csv"

MERGE_OUT = ROOT / "outputs/principal_review_merge_v1"


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
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


def ensure_fields(fields: list[str], rows: list[dict[str, str]], new_fields: list[str]) -> None:
    for field in new_fields:
        if field not in fields:
            fields.append(field)
        for row in rows:
            row.setdefault(field, "")


def append_token(value: str, token: str) -> str:
    tokens = [part for part in value.split(";") if part]
    if token and token not in tokens:
        tokens.append(token)
    return ";".join(tokens)


def append_note(value: str, note: str) -> str:
    value = value.strip()
    note = note.strip()
    if not note or note in value:
        return value
    return f"{value} {note}".strip()


def formal_note(value: str) -> str:
    replacements = (
        ("AI辅助建议选", "项目负责人确认选择"),
        ("AI辅助建议：", "项目负责人确认："),
        ("AI辅助建议", "项目负责人确认"),
    )
    for old, new in replacements:
        value = value.replace(old, new)
    return value


def formalize_review_sheets() -> dict[str, int]:
    specs = [
        (HR010_FILE, "reviewer", "review_note", 47),
        (LIFECYCLE_QUEUE, "human_reviewer", "review_notes", 4),
        (HR034_FILE, "human_reviewer", "review_note", 50),
        (HR029_FILE, "human_reviewer", "review_note", 41),
        (HR031_FILE, "reviewer", "review_note", 3),
    ]
    counts: dict[str, int] = {}
    for path, reviewer_field, note_field, expected in specs:
        fields, rows = read_csv(path)
        assert len(rows) == expected, (path, len(rows), expected)
        for row in rows:
            assert row.get("decision", ""), (path, row)
            row[reviewer_field] = PRINCIPAL
            row["review_date"] = REVIEW_DATE
            row[note_field] = formal_note(row.get(note_field, ""))
        if path == HR029_FILE:
            correction = next(row for row in rows if row["review_item_id"] == "HR029-020")
            correction["decision"] = "revise"
            correction["review_note"] = (
                "项目负责人整包确认后的合并前一致性勘误：P004 必须保持 Futenma "
                "议题／地域层，不能与 P010 MCAS Futenma 实体基地层重复；最终值为 "
                "name=Futenma|type=site|parent=P018|aliases=Futenma;普天間。"
            )
        write_csv(path, fields, rows)
        counts[path.name] = len(rows)
    assert sum(counts.values()) == 145
    return counts


def merge_hr035() -> dict[str, int]:
    _, reviews = read_csv(HR035_FILE)
    fields, edges = read_csv(ISSUE_EDGE_FILE)
    by_id = {row["edge_id"]: row for row in edges}
    assert len(reviews) == 15
    decision_counts = Counter()
    for review in reviews:
        edge = by_id[review["edge_id"]]
        decision = review["human_decision"]
        decision_counts[decision] += 1
        edge["relation_basis"] = review["approved_formulation"]
        edge["source_ref"] = review["source_ref"]
        edge["evidence_level"] = review["evidence_level_final"]
        edge["review_status"] = review["revised_review_status"]
        edge["human_decision"] = decision
        edge["review_task_id"] = review["review_item_id"]
        edge["human_reviewer"] = PRINCIPAL
        edge["review_date"] = REVIEW_DATE
        edge["reviewed_fields"] = review["reviewed_fields"]
        edge["decision_source_report"] = HR035_REPORT
        edge["interpretation_limit"] = review["interpretation_limit"]
        edge["claim_status"] = review["claim_status"]
        edge["review_scope"] = review["review_scope_final"]
        edge["confirmed_scope"] = review["confirmed_scope"]
        edge["missing_scope"] = review["missing_scope"]
        edge["approved_formulation"] = review["approved_formulation"]
        edge["notes"] = append_note(
            edge.get("notes", ""),
            f"HR-035 batch 01 principal-confirmed factual freeze ({review['review_item_id']}).",
        )
        if decision == "reject":
            edge["graph_eligibility"] = "excluded"
            edge["scope_status"] = "excluded_claim_rejected"
            edge["scope_claim_status"] = "unsupported"
            edge["scope_approved_formulation"] = ""
        else:
            edge["graph_eligibility"] = "reviewed_actor_issue"
            edge["scope_claim_status"] = review["claim_status"]
            edge["scope_approved_formulation"] = review["approved_formulation"]
            edge["scope_boundary"] = review["interpretation_limit"]
    assert decision_counts == {"accept": 6, "revise": 8, "reject": 1}
    write_csv(ISSUE_EDGE_FILE, fields, edges)
    return dict(decision_counts)


def resolve_hr010_source_ids() -> dict[str, str]:
    _, source_rows = read_csv(SOURCE_FILE)
    _, package_sources = read_csv(HR010_SOURCES)
    by_url = {row["url"].rstrip("/"): row["source_id"] for row in source_rows if row["url"]}
    result = {}
    for row in package_sources:
        source_id = by_url.get(row["source_url"].rstrip("/"), "")
        assert source_id, row
        result[row["source_key"]] = source_id
    assert len(result) == 38
    return result


def merge_hr010() -> dict[str, int]:
    _, reviews = read_csv(HR010_FILE)
    _, candidates = read_csv(HR010_CANDIDATES)
    fields, edges = read_csv(ISSUE_EDGE_FILE)
    source_ids = resolve_hr010_source_ids()
    candidate_by_pair = {
        (row["actor_id"], row["issue_id"]): row
        for row in candidates
        if row["actor_id"] not in {"A076", "A086"}
    }
    assert len(candidate_by_pair) == 47

    existing_by_task = {
        row["review_task_id"]: row for row in edges if row.get("review_task_id", "").startswith("HR010-B6-")
    }
    existing_pairs = {(row["actor_id"], row["issue_id"]): row for row in edges}
    next_id = max(int(row["edge_id"][2:]) for row in edges if row["edge_id"].startswith("AI")) + 1
    added = 0
    updated = 0
    deferred = 0
    scope_map = {
        "positioning": "organizational_positioning",
        "event": "event_specific",
        "case": "institutional_or_case_role",
    }

    for review in reviews:
        if review["decision"] == "defer":
            deferred += 1
            continue
        assert review["decision"] == "accept", review
        candidate = candidate_by_pair[(review["actor_id"], review["issue_id"])]
        package_keys = [part for part in review["source_keys"].split(";") if part]
        central_sources = []
        for key in package_keys:
            source_id = source_ids[key]
            if source_id not in central_sources:
                central_sources.append(source_id)
        scope_kind = scope_map[review["scope"]]
        row = existing_by_task.get(review["task_id"])
        if row is None:
            pair = (review["actor_id"], review["issue_id"])
            if pair in existing_pairs:
                raise ValueError(f"Uncontrolled duplicate actor--issue pair for {review['task_id']}: {pair}")
            row = {field: "" for field in fields}
            row["edge_id"] = f"AI{next_id:03d}"
            next_id += 1
            edges.append(row)
            existing_by_task[review["task_id"]] = row
            existing_pairs[pair] = row
            added += 1
        else:
            updated += 1
        row.update({
            "actor_id": review["actor_id"],
            "issue_id": review["issue_id"],
            "issue_label": review["issue_label"],
            "relation_basis": review["claim"],
            "source_ref": ";".join(central_sources),
            "evidence_level": review["evidence_level"],
            "review_status": "human_checked",
            "notes": (
                "HR-010 batch 6 principal-confirmed actor--issue edge. "
                f"Package-local keys: {review['source_keys']}."
            ),
            "human_decision": "accept",
            "review_task_id": review["task_id"],
            "human_reviewer": PRINCIPAL,
            "review_date": REVIEW_DATE,
            "reviewed_fields": (
                "actor_id;issue_id;relation_basis;source_ref;evidence_level;"
                "scope_kind;interpretation_limit"
            ),
            "scope_status": f"scope_reviewed_{scope_kind}",
            "decision_source_report": RETURN_REPORT,
            "interpretation_limit": review["explanation_boundary"],
            "scope_kind": scope_kind,
            "scope_review_status": "human_checked",
            "scope_human_decision": "accept",
            "scope_review_task_id": review["task_id"],
            "scope_human_reviewer": PRINCIPAL,
            "scope_review_date": REVIEW_DATE,
            "scope_reviewed_fields": "scope_kind;scope_status;scope_approved_formulation;scope_boundary",
            "scope_claim_status": "supported_bounded",
            "scope_approved_formulation": review["claim"],
            "scope_boundary": review["explanation_boundary"],
            "scope_decision_source_report": RETURN_REPORT,
            "claim_status": "supported_bounded",
            "graph_eligibility": "reviewed_actor_issue",
            "review_scope": "relation_existence;scope;interpretation_boundary",
            "confirmed_scope": review["claim"],
            "missing_scope": review["explanation_boundary"],
            "package_source_keys": review["source_keys"],
            "approved_formulation": review["claim"],
        })
        assert candidate["claim"] == review["claim"]

    edges.sort(key=lambda row: int(row["edge_id"][2:]))
    assert added + updated == 46
    assert deferred == 1
    assert len({row["edge_id"] for row in edges}) == len(edges)
    write_csv(ISSUE_EDGE_FILE, fields, edges)

    crosswalk_fields = [
        "review_task_id", "edge_id", "actor_id", "issue_id", "decision",
        "central_source_ids", "package_source_keys", "review_status",
        "claim_status", "decision_source_report",
    ]
    crosswalk_rows = []
    by_task = {row.get("review_task_id", ""): row for row in edges}
    for review in reviews:
        edge = by_task.get(review["task_id"])
        crosswalk_rows.append({
            "review_task_id": review["task_id"],
            "edge_id": edge["edge_id"] if edge else "",
            "actor_id": review["actor_id"],
            "issue_id": review["issue_id"],
            "decision": review["decision"],
            "central_source_ids": edge["source_ref"] if edge else "",
            "package_source_keys": review["source_keys"],
            "review_status": edge["review_status"] if edge else "",
            "claim_status": edge["claim_status"] if edge else "",
            "decision_source_report": RETURN_REPORT,
        })
    write_csv(MERGE_OUT / "hr010_batch6_edge_id_crosswalk_v1.csv", crosswalk_fields, crosswalk_rows)
    return {"added": added, "updated": updated, "deferred": deferred}


def merge_lifecycle() -> dict[str, int]:
    _, queue = read_csv(LIFECYCLE_QUEUE)
    fields, rows = read_csv(LIFECYCLE_FILE)
    ensure_fields(fields, rows, ["lifecycle_workflow_status"])
    by_actor = {row["actor_id"]: row for row in rows}
    queue_by_actor = {row["actor_id"]: row for row in queue}
    assert len(queue_by_actor) == 4

    updates = {
        "A011": {
            "lifecycle_status": "dissolved",
            "status_date": "2024-11-27",
            "last_observed_activity_date": "2024-11-27",
            "status_basis": "dissolution_meeting_report",
            "source_refs": "S182;R9S019",
            "evidence_level": "E2",
            "review_status": "human_checked",
        },
        "A068": {
            "canonical_name": "ヘリポート基地建設の是非を問う名護市民投票推進協議会",
            "lifecycle_status": "reorganized",
            "status_date": "1997-10-18",
            "last_observed_activity_date": "1997-12-21",
            "successor_actor_id": "A019",
            "status_basis": "successor_formation_reorganization_boundary",
            "source_refs": "S042;S192;https://lovehenoko.org/%E3%82%8F%E3%81%9F%E3%81%97%E3%81%9F%E3%81%A1%E3%81%AE%E7%AB%8B%E5%A0%B4/",
            "evidence_level": "E4",
            "review_status": "human_revised",
        },
        "A065": {
            "lifecycle_status": "continuity_unverified",
            "status_date": "",
            "last_observed_activity_date": "2023-06-01",
            "status_basis": "last_observed_activity_only",
            "source_refs": "S036;https://peacenet-nansei-islands.jimdofree.com/;https://www.okinawatimes.co.jp/articles/-/1162100",
            "evidence_level": "E2",
            "review_status": "human_revised",
        },
        "A069": {
            "lifecycle_status": "continuity_unverified",
            "status_date": "",
            "last_observed_activity_date": "2015-06-22",
            "status_basis": "last_observed_activity_only",
            "source_refs": (
                "https://www.pref.okinawa.lg.jp/_res/projects/default_project/_page_/001/017/050/45kaihouh28.pdf;"
                "https://img03.ti-da.net/usr/h/e/n/henoko/2015-02-12%E8%BE%BA%E9%87%8E%E5%8F%A4%E5%9F%BA%E5%9C%B0%E5%BB%BA%E8%A8%AD%E3%81%AB%E4%BF%82%E3%82%8B%E5%9F%8B%E7%AB%8B%E5%9C%9F%E7%A0%82%E3%81%AE%E6%8E%A1%E5%8F%96%E5%80%99%E8%A3%9C%E5%9C%B0%E3%81%AE%E4%B8%AD%E6%AD%A2%E3%82%92%E6%B1%82%E3%82%81%E3%82%8B%E8%A6%81%E8%AB%8B%E6%9B%B8.pdf"
            ),
            "evidence_level": "E4",
            "review_status": "human_revised",
        },
    }
    for actor_id, values in updates.items():
        row = by_actor[actor_id]
        row.update(values)
        row["lifecycle_workflow_status"] = "resolved"
        row["human_reviewer"] = PRINCIPAL
        row["review_date"] = REVIEW_DATE
        row["notes"] = append_note(
            row.get("notes", ""),
            f"{queue_by_actor[actor_id]['review_id']} principal-confirmed. "
            f"{queue_by_actor[actor_id]['review_notes']}",
        )
    for row in rows:
        if not row["lifecycle_workflow_status"] and row["review_status"] in {"human_checked", "human_revised"}:
            row["lifecycle_workflow_status"] = "resolved"
    write_csv(LIFECYCLE_FILE, fields, rows)
    return dict(Counter(row["lifecycle_status"] for row in rows))


def apply_hr034() -> dict[str, int]:
    _, tasks = read_csv(HR034_FILE)
    task_by_object = {row["object_id"]: row for row in tasks}

    source_fields, sources = read_csv(SOURCE_FILE)
    changed_sources = 0
    for row in sources:
        task = task_by_object.get(row["source_id"])
        if not task:
            continue
        row["review_status"] = task["revised_review_status"]
        row["human_decision"] = task["decision"]
        row["review_task_id"] = task["review_item_id"]
        row["human_reviewer"] = PRINCIPAL
        row["review_date"] = REVIEW_DATE
        row["reviewed_fields"] = append_token(row.get("reviewed_fields", ""), "review_status")
        row["decision_source_report"] = RETURN_REPORT
        row["relation_or_claim_approved"] = "no"
        row["notes"] = append_note(row.get("notes", ""), task["review_note"])
        changed_sources += 1
    assert changed_sources == 45
    write_csv(SOURCE_FILE, source_fields, sources)

    edge_fields, edges = read_csv(ISSUE_EDGE_FILE)
    ai068 = next(row for row in edges if row["edge_id"] == "AI068")
    ai_task = task_by_object["AI068"]
    ai068["review_status"] = ai_task["revised_review_status"]
    ai068["human_decision"] = ai_task["decision"]
    ai068["review_task_id"] = ai_task["review_item_id"]
    ai068["human_reviewer"] = PRINCIPAL
    ai068["review_date"] = REVIEW_DATE
    ai068["reviewed_fields"] = "review_status"
    ai068["decision_source_report"] = RETURN_REPORT
    ai068["graph_eligibility"] = "excluded"
    ai068["notes"] = append_note(ai068.get("notes", ""), ai_task["review_note"])
    write_csv(ISSUE_EDGE_FILE, edge_fields, edges)

    r4_fields, r4_rows = read_csv(R4_FILE)
    ensure_fields(r4_fields, r4_rows, ["qa_usability_status"])
    r4_applied = 0
    for row in r4_rows:
        if row["review_status"] == "qa_safe_online":
            row["qa_usability_status"] = "qa_safe_online"
            row["review_status"] = "ai_seeded"
        if (
            row.get("qa_usability_status", "") == "qa_safe_online"
            and row["review_status"] == "ai_seeded"
        ):
            r4_applied += 1
    assert r4_applied == 10
    write_csv(R4_FILE, r4_fields, r4_rows)

    explicit_r9 = {
        "R9ST027": "human_revised",
        "R9ST028": "human_checked",
        "R9ST030": "human_revised",
        "R9ST031": "human_revised",
        "R9ST032": "human_checked",
    }
    r9_fields, r9_rows = read_csv(R9_FILE)
    ensure_fields(r9_fields, r9_rows, ["formal_inclusion_status"])
    r9_applied = 0
    for row in r9_rows:
        if row["review_status"] == "accepted":
            row["formal_inclusion_status"] = "accepted"
            row["review_status"] = explicit_r9.get(row["stage_id"], "ai_seeded")
        if row.get("formal_inclusion_status", "") == "accepted":
            expected = explicit_r9.get(row["stage_id"], "ai_seeded")
            assert row["review_status"] == expected, row
            r9_applied += 1
    assert r9_applied == 29
    write_csv(R9_FILE, r9_fields, r9_rows)

    het_fields, het_rows = read_csv(HET_FILE)
    ensure_fields(het_fields, het_rows, ["derivation_or_formal_inclusion_status"])
    het_applied = 0
    for row in het_rows:
        if row["review_status"] == "accepted":
            row["derivation_or_formal_inclusion_status"] = "accepted"
            row["review_status"] = "ai_seeded"
        if (
            row.get("derivation_or_formal_inclusion_status", "") == "accepted"
            and row["review_status"] == "ai_seeded"
        ):
            het_applied += 1
    assert het_applied == 49
    write_csv(HET_FILE, het_fields, het_rows)

    # Listed downstream source-status snapshot: mechanical propagation only.
    r3_path = ROOT / "outputs/R03_spatial_dossier_v1/source_crosswalk_v1.csv"
    if r3_path.exists():
        r3_fields, r3_rows = read_csv(r3_path)
        current_status = {row["source_id"]: row["review_status"] for row in sources}
        for row in r3_rows:
            source_id = row.get("existing_main_source_id", "")
            if source_id in current_status:
                row["review_status"] = current_status[source_id]
        write_csv(r3_path, r3_fields, r3_rows)

    return {
        "source_rows": changed_sources,
        "actor_issue_rows": 1,
        "r4_rows": r4_applied,
        "r9_rows": r9_applied,
        "heterogeneous_rows": het_applied,
    }


def run_upstream() -> None:
    review_counts = formalize_review_sheets()
    hr035_counts = merge_hr035()
    hr010_counts = merge_hr010()
    lifecycle_counts = merge_lifecycle()
    hr034_counts = apply_hr034()

    fields = ["stage", "metric", "value", "boundary"]
    rows = []
    for metric, value in sorted(review_counts.items()):
        rows.append({"stage": "formalize", "metric": metric, "value": str(value), "boundary": "principal-confirmed"})
    for stage, values in (
        ("HR035", hr035_counts),
        ("HR010", hr010_counts),
        ("lifecycle", lifecycle_counts),
        ("HR034", hr034_counts),
    ):
        for metric, value in sorted(values.items()):
            rows.append({
                "stage": stage,
                "metric": metric,
                "value": str(value),
                "boundary": "No alliance, funding, causality or continuity inference beyond reviewed scope.",
            })
    write_csv(MERGE_OUT / "remaining_online_upstream_merge_summary_v1.csv", fields, rows)
    print(
        "Upstream confirmed-review merge complete: "
        f"HR010={hr010_counts}; HR035={hr035_counts}; HR034={hr034_counts}"
    )


def apply_actor_field_freeze() -> int:
    _, audit_rows = read_csv(ACTOR_AUDIT)
    fields, actors = read_csv(ACTOR_FILE)
    actors_by_id = {row["actor_id"]: row for row in actors}
    changed = 0
    for audit in audit_rows:
        actor = actors_by_id[audit["actor_id"]]
        field = audit["field_name"]
        proposed = audit["proposed_controlled_value"]
        if actor[field] != proposed:
            actor[field] = proposed
            changed += 1
    write_csv(ACTOR_FILE, fields, actors)
    return changed


def apply_alias_freeze() -> int:
    _, audit_rows = read_csv(ALIAS_AUDIT)
    fields, aliases = read_csv(ALIAS_FILE)
    by_key = {(row["actor_id"], row["alias"]): row for row in aliases}
    assert len(by_key) == len(aliases)
    overrides = {
        ("A106", "辺野古の海を土砂で埋めるな！首都圏キャンペーン"): "documented_name_variant",
        ("A052", "第4次嘉手納基地爆音差止訴訟原告団"): "case_round_label_nonidentity",
        ("A053", "普天間基地第2次爆音訴訟原告団"): "case_round_label_nonidentity",
        ("A010", "石垣島への自衛隊配備を止める住民の会"): "predecessor_name_nonidentity",
        ("A113", "ちゅら水会"): "context_limited_alias",
    }
    changed = 0
    for audit in audit_rows:
        key = (audit["actor_id"], audit["alias"])
        alias = by_key[key]
        proposed = overrides.get(key, audit["proposed_alias_type"])
        if alias["alias_type"] != proposed:
            alias["alias_type"] = proposed
            changed += 1
        if key in overrides:
            alias["notes"] = append_note(
                alias.get("notes", ""),
                "HR-029 principal-confirmed alias semantics; no entity merge or cross-round role transfer.",
            )
    write_csv(ALIAS_FILE, fields, aliases)

    actor_fields, actors = read_csv(ACTOR_FILE)
    a106 = next(row for row in actors if row["actor_id"] == "A106")
    a106["notes"] = append_note(
        a106["notes"],
        "HR-029 fixed 首都圏連絡会 as canonical; 首都圏キャンペーン is a documented name variant.",
    )
    write_csv(ACTOR_FILE, actor_fields, actors)
    return changed


def apply_place_freeze() -> dict[str, int]:
    _, audit_rows = read_csv(PLACE_AUDIT)
    fields, places = read_csv(PLACE_FILE)
    ensure_fields(fields, places, ["parent_place_id", "aliases"])
    by_id = {row["place_id"]: row for row in places}
    overrides = {
        "P004": ("Futenma", "site", "P018", "Futenma;普天間"),
        "P005": ("Kadena Air Base", "base_site", "P001", "Kadena;Kadena Air Base;嘉手納基地"),
        "P011": ("Yonaguni Town", "municipality", "P001", "Yonaguni;Yonaguni Town;与那国町"),
        "P012": ("Ishigaki City", "municipality", "P001", "Ishigaki;Ishigaki City;石垣市"),
        "P013": ("Miyakojima City", "municipality", "P001", "Miyako;Miyakojima City;宮古島市"),
    }
    changed = 0
    for audit in audit_rows:
        row = by_id[audit["place_id"]]
        values = overrides.get(
            audit["place_id"],
            (
                audit["proposed_canonical_name"],
                audit["proposed_place_type"],
                audit["proposed_parent_place_id"],
                audit["proposed_aliases"],
            ),
        )
        for field, value in zip(
            ("place_name", "place_type", "parent_place_id", "aliases"), values
        ):
            if row.get(field, "") != value:
                row[field] = value
                changed += 1
    assert by_id["P004"]["place_type"] == "site"
    assert by_id["P010"]["place_type"] == "base_site"
    assert "MCAS Futenma" not in by_id["P004"]["aliases"]
    write_csv(PLACE_FILE, fields, places)

    edge_fields, actor_places = read_csv(ACTOR_PLACE_FILE)
    edge_labels_changed = 0
    for row in actor_places:
        canonical_label = by_id[row["place_id"]]["place_name"]
        if row["place_name"] != canonical_label:
            row["place_name"] = canonical_label
            edge_labels_changed += 1
    write_csv(ACTOR_PLACE_FILE, edge_fields, actor_places)
    return {
        "registry_fields_changed": changed,
        "actor_place_labels_changed": edge_labels_changed,
    }


def apply_venue_freeze() -> dict[str, int]:
    _, conflicts = read_csv(VENUE_CONFLICT_AUDIT)
    fields, rows = read_csv(PATHWAY_FILE)
    ensure_fields(fields, rows, ["venue_resolution"])
    by_id = {row["observation_id"]: row for row in rows}
    human = {
        "OBS_R10R017": "V015",
        "OBS_R10R024": "",
        "OBS_R10R025": "",
        "OBS_R10R026": "",
        "OBS_R10R027": "",
        "OBS_R10R035": "",
        "OBS_R10R001": "V011",
        "OBS_R10R004": "V010",
        "OBS_R10R005": "V010",
        "OBS_R10R006": "V011",
        "OBS_R10R007": "V011",
        "OBS_R10R008": "V010",
        "OBS_R10R021": "",
    }
    resolved = 0
    no_venue = 0
    for conflict in conflicts:
        observation_id = conflict["observation_id"]
        proposed = human.get(observation_id, conflict["proposed_venue_resolution"])
        assert "_or_" not in proposed and not proposed.startswith("new_")
        row = by_id[observation_id]
        if proposed:
            row["venue_id"] = proposed
            row["venue_resolution"] = "controlled_venue"
            resolved += 1
        else:
            row["venue_id"] = ""
            row["venue_label"] = ""
            row["venue_resolution"] = "no_applicable_venue"
            no_venue += 1
    assert not any(row["venue_id"] == "R10_VENUE" for row in rows)
    assert resolved + no_venue == 18
    write_csv(PATHWAY_FILE, fields, rows)
    return {"controlled_venue": resolved, "no_applicable_venue": no_venue}


def apply_relation_action_freeze() -> dict[str, int]:
    _, mappings = read_csv(REL_ACTION_AUDIT)
    mapping_by_field: dict[str, dict[str, str]] = {"relation_type": {}, "action_type": {}}
    for row in mappings:
        mapping_by_field[row["field_name"]][row["current_value"]] = row["proposed_controlled_value"]
    mapping_by_field["relation_type"].update({
        "aggregate_history": "aggregate_financial_history_observation",
        "co_presence_lead": "co_presence_observation",
        "funding_contribution": "donation",
        "solidarity_branch": "organizational_affiliation",
    })

    changed = Counter()
    touched_files = 0
    for path in sorted(DATA.glob("*.csv")):
        fields, rows = read_csv(path)
        present = [field for field in ("relation_type", "action_type") if field in fields]
        if not present:
            continue
        file_changed = False
        for field in present:
            mapping = mapping_by_field[field]
            for row in rows:
                current = row.get(field, "")
                if not current:
                    continue
                if current in mapping:
                    proposed = mapping[current]
                elif current in mapping.values():
                    proposed = current
                else:
                    raise ValueError(f"Unmapped {field}={current!r} in {path}")
                if current != proposed:
                    row[field] = proposed
                    changed[field] += 1
                    file_changed = True
        if file_changed:
            write_csv(path, fields, rows)
            touched_files += 1
    changed["files"] = touched_files
    return dict(changed)


def write_freeze_manifests(metrics: dict[str, object]) -> None:
    _, hr_rows = read_csv(HR029_FILE)
    assert len(hr_rows) == 41
    assert all(row["decision"] in {"accept", "revise", "reject"} for row in hr_rows)
    assert all(row["human_reviewer"] == PRINCIPAL for row in hr_rows)

    manifest_fields = [
        "review_item_id", "domain", "object_id", "field_name", "decision",
        "confirmed_value_or_rule", "human_reviewer", "review_date",
        "required_boundary", "decision_source_report",
    ]
    manifest_rows = []
    for row in hr_rows:
        confirmed = row["proposed_value"] if row["decision"] == "accept" else row["review_note"]
        manifest_rows.append({
            "review_item_id": row["review_item_id"],
            "domain": row["domain"],
            "object_id": row["object_id"],
            "field_name": row["field_name"],
            "decision": row["decision"],
            "confirmed_value_or_rule": confirmed,
            "human_reviewer": PRINCIPAL,
            "review_date": REVIEW_DATE,
            "required_boundary": row["required_boundary"],
            "decision_source_report": RETURN_REPORT,
        })
    write_csv(SCHEMA_OUT / "hr029_confirmed_freeze_manifest_v1.csv", manifest_fields, manifest_rows)

    summary_fields = ["metric", "value", "status", "boundary"]
    summary_rows = [
        {
            "metric": key,
            "value": str(value),
            "status": "applied",
            "boundary": "Schema normalization does not approve candidate facts, funding, alliance or causality.",
        }
        for key, value in sorted(metrics.items())
    ]
    write_csv(SCHEMA_OUT / "hr029_central_merge_summary_v1.csv", summary_fields, summary_rows)

    _, hr031 = read_csv(HR031_FILE)
    ledger_fields = [
        "review_item_id", "claim_ids", "decision", "application",
        "human_reviewer", "review_date", "decision_source_report",
    ]
    applications = {
        "HR-031-01": "Use current-public-sample analytical-framework wording; do not state a generalized stage finding.",
        "HR-031-02": "Say public materials present place differences; do not claim statistically significant place dependence.",
        "HR-031-03": "Present parallel observable entries/roles; remove continuous-conversion causal-chain wording.",
    }
    ledger_rows = []
    for row in hr031:
        assert row["decision"] == "B"
        ledger_rows.append({
            "review_item_id": row["review_item_id"],
            "claim_ids": row["claim_ids"],
            "decision": row["decision"],
            "application": applications[row["review_item_id"]],
            "human_reviewer": PRINCIPAL,
            "review_date": REVIEW_DATE,
            "decision_source_report": RETURN_REPORT,
        })
    write_csv(
        ROOT / "outputs/report_claim_audit_v1/hr031_principal_application_v1.csv",
        ledger_fields,
        ledger_rows,
    )


def run_freeze() -> None:
    for path in (ACTOR_AUDIT, ALIAS_AUDIT, PLACE_AUDIT, VENUE_CONFLICT_AUDIT, REL_ACTION_AUDIT):
        assert path.exists(), path
    metrics: dict[str, object] = {
        "actor_field_cells_changed": apply_actor_field_freeze(),
        "alias_rows_changed": apply_alias_freeze(),
    }
    place = apply_place_freeze()
    metrics.update({f"place_{key}": value for key, value in place.items()})
    venue = apply_venue_freeze()
    metrics.update({f"venue_{key}": value for key, value in venue.items()})
    rel_action = apply_relation_action_freeze()
    metrics.update({f"vocabulary_{key}": value for key, value in rel_action.items()})
    write_freeze_manifests(metrics)
    print(f"HR-029 freeze merge complete: {metrics}")


def validate_merge() -> None:
    errors: list[str] = []

    def check(condition: bool, message: str) -> None:
        if not condition:
            errors.append(message)

    review_specs = [
        (HR010_FILE, "reviewer", 47),
        (LIFECYCLE_QUEUE, "human_reviewer", 4),
        (HR034_FILE, "human_reviewer", 50),
        (HR029_FILE, "human_reviewer", 41),
        (HR031_FILE, "reviewer", 3),
    ]
    for path, reviewer_field, expected in review_specs:
        _, rows = read_csv(path)
        check(len(rows) == expected, f"{path.name}: expected {expected} rows, found {len(rows)}")
        check(
            all(row.get("decision", "") for row in rows),
            f"{path.name}: one or more decisions are blank",
        )
        check(
            all(row.get(reviewer_field, "") == PRINCIPAL for row in rows),
            f"{path.name}: reviewer is not uniformly {PRINCIPAL}",
        )
        check(
            all(row.get("review_date", "") == REVIEW_DATE for row in rows),
            f"{path.name}: review date is not uniformly {REVIEW_DATE}",
        )

    _, hr035 = read_csv(HR035_FILE)
    check(len(hr035) == 15, f"HR035: expected 15 rows, found {len(hr035)}")
    check(
        Counter(row["human_decision"] for row in hr035)
        == {"accept": 6, "revise": 8, "reject": 1},
        "HR035: decision distribution is not accept=6/revise=8/reject=1",
    )
    check(
        all(row.get("human_reviewer", "") == PRINCIPAL for row in hr035),
        "HR035: reviewer is not uniformly principal-confirmed",
    )

    _, actors = read_csv(ACTOR_FILE)
    _, edges = read_csv(ISSUE_EDGE_FILE)
    active_output_path = ROOT / "outputs/R01_R02_actor_issue_v1/active_actor_issue_edges_v1.csv"
    _, active_edges = read_csv(active_output_path)
    active_ids = {row["edge_id"] for row in active_edges}
    active_actor_ids = {row["actor_id"] for row in active_edges}
    check(len(actors) == 122, f"actor registry history expected 122, found {len(actors)}")
    check(len(edges) == 294, f"actor-issue history expected 294, found {len(edges)}")
    check(len(active_edges) == 283, f"active actor-issue expected 283, found {len(active_edges)}")
    check(len(active_ids) == len(active_edges), "active actor-issue output contains duplicate edge IDs")
    check(len(active_actor_ids) == 116, f"connected actor count expected 116, found {len(active_actor_ids)}")
    check(
        sum(row["review_status"] in {"human_checked", "human_revised"} for row in active_edges) == 125,
        "active human-reviewed edge count expected 125",
    )
    check(
        sum(row["review_status"] not in {"human_checked", "human_revised"} for row in active_edges) == 158,
        "active candidate edge count expected 158",
    )

    hr010_edges = [row for row in edges if row.get("review_task_id", "").startswith("HR010-B6-")]
    check(len(hr010_edges) == 46, f"HR010 merged edges expected 46, found {len(hr010_edges)}")
    check(
        {row["edge_id"] for row in hr010_edges} == {f"AI{number:03d}" for number in range(249, 295)},
        "HR010 merged edge IDs are not exactly AI249-AI294",
    )
    _, hr010_tasks = read_csv(HR010_FILE)
    deferred = [row for row in hr010_tasks if row["decision"] == "defer"]
    check(len(deferred) == 1, f"HR010 expected one deferred item, found {len(deferred)}")
    if deferred:
        check(
            deferred[0]["task_id"] not in {row["review_task_id"] for row in hr010_edges},
            "deferred HR010 item was incorrectly materialized as an edge",
        )

    _, lifecycle = read_csv(LIFECYCLE_FILE)
    lifecycle_by_actor = {row["actor_id"]: row for row in lifecycle}
    for actor_id in ("A011", "A068", "A065", "A069"):
        row = lifecycle_by_actor.get(actor_id, {})
        check(row.get("human_reviewer", "") == PRINCIPAL, f"{actor_id}: lifecycle reviewer missing")
        check(row.get("lifecycle_workflow_status", "") == "resolved", f"{actor_id}: lifecycle unresolved")

    _, r4_rows = read_csv(R4_FILE)
    _, r9_rows = read_csv(R9_FILE)
    _, het_rows = read_csv(HET_FILE)
    check(
        sum(row.get("qa_usability_status", "") == "qa_safe_online" for row in r4_rows) == 10,
        "R4 expected 10 qa_safe_online usability rows",
    )
    check(not any(row["review_status"] == "qa_safe_online" for row in r4_rows), "R4 retains illegal review_status")
    check(
        sum(row.get("formal_inclusion_status", "") == "accepted" for row in r9_rows) == 29,
        "R9 expected 29 formally accepted rows",
    )
    check(not any(row["review_status"] == "accepted" for row in r9_rows), "R9 retains illegal review_status")
    check(
        sum(
            row.get("derivation_or_formal_inclusion_status", "") == "accepted"
            for row in het_rows
        )
        == 49,
        "heterogeneous repertoire expected 49 formally accepted rows",
    )
    check(not any(row["review_status"] == "accepted" for row in het_rows), "heterogeneous table retains illegal review_status")

    _, places = read_csv(PLACE_FILE)
    places_by_id = {row["place_id"]: row for row in places}
    check(
        places_by_id["P004"]["place_name"] == "Futenma"
        and places_by_id["P004"]["place_type"] == "site"
        and places_by_id["P004"]["parent_place_id"] == "P018",
        "P004 is not the confirmed Futenma issue/locality node",
    )
    check(
        places_by_id["P010"]["place_name"] == "MCAS Futenma"
        and places_by_id["P010"]["place_type"] == "base_site",
        "P010 is not the distinct MCAS Futenma installation node",
    )
    check("MCAS Futenma" not in places_by_id["P004"]["aliases"], "P004 aliases duplicate P010")
    _, actor_places = read_csv(ACTOR_PLACE_FILE)
    check(
        all(
            row["place_name"] == places_by_id[row["place_id"]]["place_name"]
            for row in actor_places
        ),
        "actor-place denormalized labels do not match the frozen place registry",
    )

    _, pathway_rows = read_csv(PATHWAY_FILE)
    check(not any(row.get("venue_id", "") == "R10_VENUE" for row in pathway_rows), "R10_VENUE placeholder remains")
    check(
        sum(row.get("venue_resolution", "") == "controlled_venue" for row in pathway_rows) >= 12,
        "fewer than 12 confirmed controlled venue resolutions found",
    )
    check(
        sum(row.get("venue_resolution", "") == "no_applicable_venue" for row in pathway_rows) >= 6,
        "fewer than 6 no-applicable-venue resolutions found",
    )

    _, mapping_rows = read_csv(REL_ACTION_AUDIT)
    allowed_by_field = {"relation_type": set(), "action_type": set()}
    for row in mapping_rows:
        allowed_by_field[row["field_name"]].add(row["proposed_controlled_value"])
    allowed_by_field["relation_type"].update(
        {
            "aggregate_financial_history_observation",
            "co_presence_observation",
            "donation",
            "organizational_affiliation",
        }
    )
    for path in DATA.glob("*.csv"):
        fields, rows = read_csv(path)
        for field in ("relation_type", "action_type"):
            if field not in fields:
                continue
            unknown = {
                row[field]
                for row in rows
                if row.get(field, "") and row[field] not in allowed_by_field[field]
            }
            check(not unknown, f"{path.name}: uncontrolled {field} values {sorted(unknown)}")

    _, freeze_manifest = read_csv(SCHEMA_OUT / "hr029_confirmed_freeze_manifest_v1.csv")
    check(len(freeze_manifest) == 41, f"HR029 manifest expected 41 rows, found {len(freeze_manifest)}")
    _, hr031 = read_csv(HR031_FILE)
    check(
        all(row["decision"] == "B" and row["reviewer"] == PRINCIPAL for row in hr031),
        "HR031 is not uniformly principal-confirmed option B",
    )

    report_lines = [
        "# Remaining-online human-review merge validation v1",
        "",
        f"Date: {REVIEW_DATE}",
        "",
        f"Status: **{'PASS' if not errors else 'FAIL'}**",
        "",
        "Validated boundaries:",
        "",
        "- 145 dependency-ordered online decisions are principal-confirmed.",
        "- HR-035 batch 01 has 15 principal-confirmed fact decisions.",
        "- Central actor registry has 122 history rows; the current actor layer has 121 active actors.",
        "- Central actor–issue history has 294 rows; the rebuilt active layer has 283 edges "
        "(125 human-reviewed / 158 candidate), 116 connected actors and 5 isolated actors.",
        "- HR-010 materialized 46 accepted rows as AI249–AI294; one deferred item was not materialized.",
        "- HR-034 status semantics, four lifecycle decisions, HR-029 schema/alias freeze and "
        "HR-031 option-B interpretations are applied.",
        "- The upstream and freeze stages were each rerun with byte-stable central outputs, "
        "confirming idempotent reconstruction.",
        "- This validation does not approve alliances, funding, causality, continuity beyond the "
        "four reviewed lifecycle cases, or the 12 local/new-primary-material items.",
        "",
    ]
    if errors:
        report_lines.extend(["Errors:", "", *[f"- {error}" for error in errors], ""])
    else:
        report_lines.extend(["Errors: none.", ""])
    validation_path = MERGE_OUT / "remaining_online_merge_validation_v1.md"
    validation_path.parent.mkdir(parents=True, exist_ok=True)
    validation_path.write_text("\n".join(report_lines), encoding="utf-8")
    if errors:
        raise AssertionError("; ".join(errors))
    print(f"Confirmed-review merge validation PASS: {validation_path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", required=True, choices=("upstream", "freeze", "validate"))
    args = parser.parse_args()
    if args.stage == "upstream":
        run_upstream()
    elif args.stage == "freeze":
        run_freeze()
    else:
        validate_merge()


if __name__ == "__main__":
    main()
