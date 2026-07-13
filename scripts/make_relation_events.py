from __future__ import annotations

"""MT-008: build an event-aware relation table.

Consolidates the co-action samples, the dugong lawsuit, and the referendum
events into one table that carries event_id / action_type / relation_strength,
so static issue tags become event-aware network data.

Output: outputs/module_completion_v0/actor_relation_events_v1.csv

Conservative: co-signing is one-off event participation, not stable alliance;
only actors with a registry actor_id become network rows (individual plaintiffs
are noted in the lawsuit role table, not here).
"""

import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "outputs" / "module_completion_v0"

FIELDS = [
    "event_id", "event_name", "event_year", "action_type",
    "actor_id", "canonical_name", "role", "relation_strength",
    "evidence_level", "source_ref", "interpretation_limit",
]

# event relation_type -> action_type
ACTION_BY_RELATION = {
    "joint_statement": "co_signing",
    "request_letter_report": "request_letter",
}
# participant relation_strength -> normalized relation_strength
STRENGTH_BY_EVENT = {
    "co_signatory_event": "one_off_co_signatory",
    "request_participant_event": "request_participant",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def from_coaction() -> list[dict[str, str]]:
    events = {e["event_id"]: e for e in read_csv(MODULE / "coaction_events_v0.csv")}
    rows: list[dict[str, str]] = []
    for p in read_csv(MODULE / "coaction_participants_v0.csv"):
        ev = events.get(p["event_id"], {})
        rows.append({
            "event_id": p["event_id"],
            "event_name": ev.get("event_name", ""),
            "event_year": ev.get("event_year", ""),
            "action_type": ACTION_BY_RELATION.get(ev.get("relation_type", ""), "co_signing"),
            "actor_id": p["actor_id"],
            "canonical_name": p["canonical_name"],
            "role": p["role"],
            "relation_strength": STRENGTH_BY_EVENT.get(p["relation_strength"], p["relation_strength"]),
            "evidence_level": p["evidence_level"],
            "source_ref": p["source_id"],
            "interpretation_limit": "co-signing is one-off event participation, not stable alliance",
        })
    return rows


def from_lawsuit() -> list[dict[str, str]]:
    strength = {
        "named_plaintiff": "named_plaintiff",
        "legal_counsel": "plaintiff_counsel",
    }
    rows: list[dict[str, str]] = []
    for r in read_csv(MODULE / "lawsuit_actor_role_table_v0.csv"):
        if r["role"] not in strength:
            continue  # skip individuals, non-parties, defendant
        if not r["actor_id"]:
            continue
        rows.append({
            "event_id": "EV2003_DUGONG_LAWSUIT",
            "event_name": "Okinawa Dugong v. Rumsfeld NHPA lawsuit (C 03-4350 MHP)",
            "event_year": "2003",
            "action_type": "litigation",
            "actor_id": r["actor_id"],
            "canonical_name": r["party_name"],
            "role": r["role"],
            "relation_strength": strength[r["role"]],
            "evidence_level": r["evidence_level"],
            "source_ref": r["source_refs"],
            "interpretation_limit": "US NHPA suit party role; not a stable alliance",
        })
    return rows


# referendum / opinion-ad events (manual spec; initiator actors from registry)
REFERENDUM_ROWS = [
    ("EV2019_PREF_REFERENDUM", "2019 Henoko prefectural referendum", "2019", "referendum",
     "A051", "「辺野古」県民投票の会", "referendum_initiator", "E4", "S025"),
    ("EV1997_NAGO_REFERENDUM", "1997 Nago city referendum", "1997", "referendum",
     "A068", "名護市民投票の会", "referendum_initiator", "E3", "S042"),
    ("EV_ISHIGAKI_REFERENDUM", "Ishigaki referendum drive (2018-2019)", "2019", "referendum",
     "A011", "石垣市住民投票を求める会", "referendum_initiator", "E4", "S018;S019;S137;S138"),
    ("EV2015_YONAGUNI_REFERENDUM", "2015 Yonaguni SDF-deployment referendum", "2015", "referendum",
     "A014", "住民投票を成功させるための実行委員会", "referendum_committee", "E2", "S069;S010"),
    ("EV2012_YONAGUNI_OPINION_AD", "2012 Yonaguni anti-deployment opinion ad", "2012", "opinion_ad",
     "A015", "与那国自衛隊配備反対意見広告実行委員会", "opinion_ad_committee", "E2", "S015"),
]


def from_referendums() -> list[dict[str, str]]:
    rows = []
    for eid, name, year, action, aid, aname, role, ev, src in REFERENDUM_ROWS:
        rows.append({
            "event_id": eid, "event_name": name, "event_year": year, "action_type": action,
            "actor_id": aid, "canonical_name": aname, "role": role,
            "relation_strength": role, "evidence_level": ev, "source_ref": src,
            "interpretation_limit": "referendum/opinion-ad participation; E2 rows are leads",
        })
    return rows


def write_note(rows: list[dict[str, str]]) -> None:
    """Keep the explanatory note synchronized with both event tables."""
    counts = Counter(row["action_type"] for row in rows)
    formal_path = ROOT / "data" / "interim" / "09_actor_event_venue_edges_v0.csv"
    formal_rows = read_csv(formal_path)
    formal_counts = Counter(row["action_type"] for row in formal_rows)
    formal_review = Counter(row["reviewer_status"] for row in formal_rows)
    note = f"""# MT-008 关系边事件化 note v0

日期：2026-07-13（HR-015 同步）

**目标**：把静态 actor–issue / actor–place 边升级为事件感知数据，用 `event_id`、`action_type` 与 `relation_strength` 区分长期组织定位、事件性署名、法律程序角色、公投参与和分析种子。

## 两层数据，不混用

- `actor_relation_events_v1.csv` 是 **registry-only 派生表**：{len(rows)} 行、{len({row['event_id'] for row in rows})} 个事件、{len(counts)} 类 action。它只保留已有 `actor_id` 的组织级角色，用于当前网络图。
- `data/interim/09_actor_event_venue_edges_v0.csv` 是 HR-015 正式事实／分析表：{len(formal_rows)} 行；其中 {formal_review.get('human_checked', 0)} 行 `human_checked`、{formal_review.get('analytical_seed', 0)} 行 `analytical_seed`。它保留九个 E2 `unverified_event_participant`，这些名称不在 actor registry。

| action_type | registry-only 行数 | 正式 AEV 行数 |
|---|---:|---:|
| co_signing | {counts.get('co_signing', 0)} | {formal_counts.get('co_signing', 0)} |
| request_letter | {counts.get('request_letter', 0)} | {formal_counts.get('request_letter', 0)} |
| litigation | {counts.get('litigation', 0)} | {formal_counts.get('litigation', 0)} |
| referendum | {counts.get('referendum', 0)} | {formal_counts.get('referendum', 0)} |
| opinion_ad | {counts.get('opinion_ad', 0)} | {formal_counts.get('opinion_ad', 0)} |
| pathway_role | {counts.get('pathway_role', 0)} | {formal_counts.get('pathway_role', 0)} |

## 解释边界

- 共同署名、共同要请、同场参与只证明一次事件角色，不构成稳定联盟。
- 四条 `pathway_role` 是解释性分析种子，不是事实关系。
- E2 event-only 名称在取得独立身份与持续性证据前不得回填 registry。
- 诉讼中的个人、组织、律师、请求者、支援者与 non-party 必须分开；个人角色不得转嫁给其所属组织。

## 可视化

`fig/fig_event_repertoire.html` 读取 registry-only 表生成当前 repertoire 时间线，气泡面积只表示当前 registry 中可核组织角色数。HR-015 前的旧截图已改名 `fig_event_repertoire_pre_hr015.png`，只作历史快照；正式全量事件参与以 AEV 表为准。

## 下一步

- 从正式 AEV 重做事实事件图，并把四条 analytical seed 分层显示。
- 将嘉手纳、普天间与泡瀬案件按案件／轮次补入 event 层。
- 在不破坏现有 07/08 图脚本前提下，评估把 `event_id`、`action_type`、`relation_strength` 作为可空字段并入下一版边表。
"""
    (MODULE / "MT008_edge_enrichment_note.md").write_text(note, encoding="utf-8")


def main() -> None:
    rows = from_coaction() + from_lawsuit() + from_referendums()
    out = MODULE / "actor_relation_events_v1.csv"
    with out.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)
    write_note(rows)
    n_events = len({r["event_id"] for r in rows})
    n_actions = len({r["action_type"] for r in rows})
    print(f"Wrote {out.relative_to(ROOT)}: {len(rows)} rows, "
          f"{n_events} events, {n_actions} action types")


if __name__ == "__main__":
    main()
