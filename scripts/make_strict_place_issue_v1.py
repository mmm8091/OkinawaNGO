from __future__ import annotations

"""Build a source-constrained actor × place × issue evidence layer.

The previous place × issue matrix crossed every place and issue attached to an
actor.  That is useful only as an upper-bound sensitivity projection.  This
script requires the place and issue edges to share at least one source ID and
separates human-reviewed triples from E3/E4 candidate triples.  Formal AEV
records are attached when the same actor and source also identify an event.
"""

import csv
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.colors import PowerNorm
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "interim"
OUT = ROOT / "outputs" / "R03_strict_place_issue_v1"

REVIEWED = {"human_checked", "human_revised"}
E3PLUS = {"E3", "E4"}

PLACE_FOCUS = [
    ("P002", "边野古"), ("P003", "大浦湾"), ("P012", "石垣"),
    ("P013", "宫古"), ("P011", "与那国"), ("P005", "嘉手纳"),
    ("P004", "普天间"), ("P018", "宜野湾"), ("P020", "那霸"),
    ("P001", "冲绳全县"),
]

FRAME_MAP = [
    ("F1", "基地／反军事", {"anti_base", "anti_military", "Henoko"}),
    ("F2", "生态／环境", {"environment", "biodiversity", "dugong", "groundwater"}),
    ("F3", "生命／健康", {"life_safety", "health_risk", "base_community_welfare", "military_family_service", "noise"}),
    ("F4", "自治／公投", {"local_autonomy", "referendum"}),
    ("F5", "法律／程序", {"legal"}),
    ("F6", "国际路径", {"international_advocacy", "public_diplomacy", "international_cooperation"}),
    ("F7", "前线／台海", {"frontline_prevention", "Taiwan_contingency", "anti_war"}),
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def refs(value: str) -> set[str]:
    return {item.strip() for item in value.split(";") if item.strip().startswith("S")}


def configure_fonts() -> None:
    available = {font.name for font in font_manager.fontManager.ttflist}
    for name in ("Microsoft YaHei", "Yu Gothic", "Meiryo", "Noto Sans CJK SC", "SimHei", "DejaVu Sans"):
        if name in available:
            plt.rcParams["font.family"] = name
            break
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["figure.facecolor"] = "white"


def frame_for(issue_label: str) -> tuple[str, str] | None:
    for frame_id, frame_name, labels in FRAME_MAP:
        if issue_label in labels:
            return frame_id, frame_name
    return None


def active_edge(row: dict[str, str]) -> bool:
    status = row.get("scope_status", "")
    return not (
        row.get("review_status") == "rejected"
        or row.get("claim_status") == "unsupported"
        or row.get("graph_eligibility") == "excluded"
        or status.startswith("retired_")
        or status.startswith("deactivated_")
    )


def main() -> None:
    configure_fonts()
    OUT.mkdir(parents=True, exist_ok=True)
    actors = {row["actor_id"]: row for row in read_csv(DATA / "01_actor_registry_initial_v0.csv")}
    sources = {row["source_id"]: row for row in read_csv(DATA / "05_source_log_initial_v0.csv")}
    issue_history = read_csv(DATA / "07_actor_issue_edges_initial_v0.csv")
    place_history = read_csv(DATA / "08_actor_place_edges_initial_v0.csv")
    issues = [row for row in issue_history if active_edge(row)]
    places = [row for row in place_history if active_edge(row)]
    observations = read_csv(DATA / "26_actor_event_venue_target_entry_modes_v0.csv")

    event_index: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in observations:
        actor_id = row.get("actor_id", "")
        for source_id in refs(row.get("source_refs", "")):
            if actor_id:
                event_index[(actor_id, source_id)].append(row)

    issue_by_actor: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in issues:
        issue_by_actor[row["actor_id"]].append(row)

    triples: list[dict[str, object]] = []
    seen: set[tuple[str, str, str, str]] = set()
    for place in places:
        actor_id = place["actor_id"]
        place_refs = refs(place["source_ref"])
        for issue in issue_by_actor.get(actor_id, []):
            frame = frame_for(issue["issue_label"])
            if not frame:
                continue
            for source_id in sorted(place_refs & refs(issue["source_ref"])):
                key = (actor_id, place["place_id"], issue["issue_id"], source_id)
                if key in seen:
                    continue
                seen.add(key)
                attached = event_index.get((actor_id, source_id), [])
                event_ids = sorted({row["event_or_project_id"] for row in attached if row.get("event_or_project_id")})
                event_names = sorted({row["event_or_project_name"] for row in attached if row.get("event_or_project_name")})
                event_dates = sorted({row["date_or_period"] for row in attached if row.get("date_or_period")})
                reviewed = place["review_status"] in REVIEWED and issue["review_status"] in REVIEWED
                e3plus = place["evidence_level"] in E3PLUS and issue["evidence_level"] in E3PLUS
                triples.append(
                    {
                        "triple_id": f"SPI{len(triples)+1:04d}",
                        "actor_id": actor_id,
                        "actor_name": actors.get(actor_id, {}).get("canonical_name", actor_id),
                        "place_edge_id": place["edge_id"],
                        "place_id": place["place_id"],
                        "place_name": place["place_name"],
                        "issue_edge_id": issue["edge_id"],
                        "issue_id": issue["issue_id"],
                        "issue_label": issue["issue_label"],
                        "frame_id": frame[0],
                        "frame_name": frame[1],
                        "shared_source_id": source_id,
                        "document_year": sources.get(source_id, {}).get("year", ""),
                        "document_title": sources.get(source_id, {}).get("title", ""),
                        "event_ids": ";".join(event_ids),
                        "event_names": ";".join(event_names),
                        "event_dates": ";".join(event_dates),
                        "place_review_status": place["review_status"],
                        "issue_review_status": issue["review_status"],
                        "place_evidence_level": place["evidence_level"],
                        "issue_evidence_level": issue["evidence_level"],
                        "triple_layer": "human_reviewed_same_source" if reviewed else ("e3plus_same_source_candidate" if e3plus else "lower_evidence_same_source_candidate"),
                        "interpretation_limit": "Same-source coincidence supports a bounded actor-place-issue evidence triple; it does not by itself establish causality, duration, alliance, or substantive policy effect.",
                    }
                )

    triple_fields = [
        "triple_id", "actor_id", "actor_name", "place_edge_id", "place_id", "place_name",
        "issue_edge_id", "issue_id", "issue_label", "frame_id", "frame_name", "shared_source_id",
        "document_year", "document_title", "event_ids", "event_names", "event_dates",
        "place_review_status", "issue_review_status", "place_evidence_level", "issue_evidence_level",
        "triple_layer", "interpretation_limit",
    ]
    write_csv(OUT / "same_source_actor_place_issue_triples_v1.csv", triples, triple_fields)

    place_ids = [item[0] for item in PLACE_FOCUS]
    place_labels = [item[1] for item in PLACE_FOCUS]
    frames = [item[0] for item in FRAME_MAP]

    def actor_cells(layer: str) -> dict[tuple[str, str], set[str]]:
        cells: dict[tuple[str, str], set[str]] = defaultdict(set)
        for row in triples:
            if row["place_id"] not in place_ids:
                continue
            if layer == "reviewed" and row["triple_layer"] != "human_reviewed_same_source":
                continue
            if layer == "e3plus" and row["triple_layer"] not in {"human_reviewed_same_source", "e3plus_same_source_candidate"}:
                continue
            cells[(str(row["place_id"]), str(row["frame_id"]))].add(str(row["actor_id"]))
        return cells

    strict_all = actor_cells("e3plus")
    strict_reviewed = actor_cells("reviewed")

    # Reproduce the retired actor-level Cartesian projection only as an explicit
    # method upper bound for retention/sensitivity comparison.
    actor_issue_frames: dict[str, set[str]] = defaultdict(set)
    for row in issues:
        if row["evidence_level"] not in E3PLUS:
            continue
        frame = frame_for(row["issue_label"])
        if frame:
            actor_issue_frames[row["actor_id"]].add(frame[0])
    wide: dict[tuple[str, str], set[str]] = defaultdict(set)
    for row in places:
        if row["evidence_level"] not in E3PLUS or row["place_id"] not in place_ids:
            continue
        for frame_id in actor_issue_frames.get(row["actor_id"], set()):
            wide[(row["place_id"], frame_id)].add(row["actor_id"])

    matrix_rows: list[dict[str, object]] = []
    for place_id, place_label in PLACE_FOCUS:
        for frame_id, frame_name, _ in FRAME_MAP:
            upper = len(wide[(place_id, frame_id)])
            strict = len(strict_all[(place_id, frame_id)])
            reviewed = len(strict_reviewed[(place_id, frame_id)])
            matrix_rows.append(
                {
                    "place_id": place_id, "place_label": place_label, "frame_id": frame_id,
                    "frame_name": frame_name, "wide_upper_bound_actor_count": upper,
                    "same_source_e3plus_actor_count": strict,
                    "human_reviewed_same_source_actor_count": reviewed,
                    "strict_retention_ratio": round(strict / upper, 3) if upper else "",
                    "same_source_actor_ids": ";".join(sorted(strict_all[(place_id, frame_id)])),
                    "reviewed_actor_ids": ";".join(sorted(strict_reviewed[(place_id, frame_id)])),
                }
            )
    write_csv(
        OUT / "place_issue_strict_sensitivity_matrix_v1.csv",
        matrix_rows,
        ["place_id", "place_label", "frame_id", "frame_name", "wide_upper_bound_actor_count",
         "same_source_e3plus_actor_count", "human_reviewed_same_source_actor_count",
         "strict_retention_ratio", "same_source_actor_ids", "reviewed_actor_ids"],
    )

    arrays = []
    for cells in (wide, strict_all, strict_reviewed):
        arrays.append(np.array([[len(cells[(pid, fid)]) for fid in frames] for pid in place_ids], dtype=int))
    vmax = max(1, int(max(array.max() for array in arrays)))
    fig, axes = plt.subplots(1, 3, figsize=(18, 7.7), sharey=True)
    titles = ["A 旧宽投影上界\n（不可作发现）", "B 同源约束 E3+\n（严格候选）", "C 同源＋双边人审\n（最稳健子集）"]
    cmaps = ["Greys", "YlGnBu", "PuBuGn"]
    for idx, (ax, array, title, cmap) in enumerate(zip(axes, arrays, titles, cmaps)):
        im = ax.imshow(array, cmap=cmap, norm=PowerNorm(gamma=0.5, vmin=0, vmax=vmax), aspect="auto")
        ax.set_title(title, fontsize=13, fontweight="bold", pad=12)
        ax.set_xticks(range(len(frames)), labels=frames, fontsize=9)
        if idx == 0:
            ax.set_yticks(range(len(place_labels)), labels=place_labels, fontsize=10)
        ax.tick_params(length=0)
        for i in range(array.shape[0]):
            for j in range(array.shape[1]):
                if array[i, j]:
                    ax.text(j, i, str(array[i, j]), ha="center", va="center", fontsize=8.5,
                            color="white" if array[i, j] > vmax * 0.55 else "#17232c")
        for spine in ax.spines.values():
            spine.set_visible(False)
    fig.colorbar(im, ax=axes, fraction=0.018, pad=0.02, label="不同 actor 数")
    frame_key = "  ".join(f"{fid} {name}" for fid, name, _ in FRAME_MAP)
    fig.suptitle("R3 地点 × 议题：从 actor 宽投影收紧到同一来源三元事实", fontsize=18, fontweight="bold", x=0.06, ha="left")
    fig.text(0.06, 0.925, "每格计不同 actor；B/C 要求 place edge 与 issue edge 至少共享一个 source_id。C 还要求两条边均已经人工复核。", fontsize=10.5, color="#45525c")
    fig.text(0.06, 0.045, frame_key, fontsize=9, color="#34424b")
    fig.text(0.06, 0.018, "解释边界：同源证明文档级三元共现，不自动证明同一事件、因果效果、长期在场或稳定联盟。", fontsize=9, color="#7a3e2e")
    fig.subplots_adjust(left=0.08, right=0.94, top=0.82, bottom=0.1, wspace=0.12)
    fig.savefig(OUT / "fig_strict_place_issue_sensitivity_v1.png", dpi=220, bbox_inches="tight")
    plt.close(fig)

    strict_rows = [row for row in triples if row["triple_layer"] in {"human_reviewed_same_source", "e3plus_same_source_candidate"}]
    reviewed_rows = [row for row in triples if row["triple_layer"] == "human_reviewed_same_source"]
    event_rows = [row for row in strict_rows if row["event_ids"]]
    summary = [
        {"metric": "actor_issue_history_rows", "value": len(issue_history), "note": "includes retained rejected/deactivated audit rows"},
        {"metric": "actor_issue_active_rows", "value": len(issues), "note": "used by this strict layer"},
        {"metric": "actor_place_history_rows", "value": len(place_history), "note": "includes retained rejected audit rows"},
        {"metric": "actor_place_active_rows", "value": len(places), "note": "used by this strict layer"},
        {"metric": "all_same_source_triples", "value": len(triples), "note": "all evidence levels"},
        {"metric": "e3plus_same_source_triples", "value": len(strict_rows), "note": "strict candidate layer"},
        {"metric": "human_reviewed_same_source_triples", "value": len(reviewed_rows), "note": "both underlying edges human-reviewed"},
        {"metric": "strict_triples_with_formal_event_attachment", "value": len(event_rows), "note": "same actor/source found in formal AEV-derived observation table"},
        {"metric": "wide_nonzero_cells", "value": sum(bool(v) for v in wide.values()), "note": "retired upper-bound method"},
        {"metric": "strict_e3plus_nonzero_cells", "value": sum(bool(v) for v in strict_all.values()), "note": "source-constrained"},
        {"metric": "reviewed_nonzero_cells", "value": sum(bool(v) for v in strict_reviewed.values()), "note": "source-constrained and dual reviewed"},
    ]
    write_csv(OUT / "validation_metrics_v1.csv", summary, ["metric", "value", "note"])

    readme = f"""# R3 strict place × issue evidence v1

This package replaces the interpretive use of the retired actor-level Cartesian projection.

- The input gate retains `{len(issue_history)}` actor–issue and `{len(place_history)}` actor–place history rows, but excludes rejected/deactivated records; `{len(issues)}` and `{len(places)}` active rows enter the strict join.
- `{len(triples)}` document-level same-source triples were found.
- `{len(strict_rows)}` are E3/E4 strict candidates.
- `{len(reviewed_rows)}` have both underlying edges human-reviewed.
- `{len(event_rows)}` strict triples can also be attached to a formal event observation through the same actor/source pair.

The three-panel figure is a sensitivity result, not three competing findings: panel A is an explicit upper bound, panel B is the usable research-candidate layer, and panel C is the conservative reviewed subset.  A shared source still does not prove causal effect, persistent presence or alliance.
"""
    (OUT / "README.md").write_text(readme, encoding="utf-8", newline="\n")
    print(f"Strict place-issue package: {len(triples)} triples / {len(strict_rows)} E3+ / {len(reviewed_rows)} dual-reviewed / {len(event_rows)} event-attached")


if __name__ == "__main__":
    main()
