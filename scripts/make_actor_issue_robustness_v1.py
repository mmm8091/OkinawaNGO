from __future__ import annotations

"""Sensitivity analysis for the actor-issue bridge results.

The analysis asks whether cross-frame actors and the ecology-to-international
route survive removal of the three large-list / pathway sources S003, S004 and
S006, and how much remains when only human-reviewed edges are retained.
"""

import csv
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "interim"
OUT = ROOT / "outputs" / "R02_actor_issue_robustness_v1"
E3PLUS = {"E3", "E4"}
REVIEWED = {"human_checked", "human_revised"}

FRAME_MAP = {
    "F1 基地／反军事": {"anti_base", "anti_military", "Henoko"},
    "F2 生态／环境": {"environment", "biodiversity", "dugong", "groundwater"},
    "F3 生命／健康": {"life_safety", "health_risk", "noise", "base_community_welfare", "military_family_service"},
    "F4 自治／公投": {"local_autonomy", "referendum"},
    "F5 法律／程序": {"legal"},
    "F6 国际路径": {"international_advocacy", "public_diplomacy", "international_cooperation"},
    "F7 前线／台海": {"frontline_prevention", "Taiwan_contingency", "anti_war"},
    "F8 女性／人权／和平": {"women", "human_rights", "peace", "solidarity", "mobilization"},
}

SCENARIOS = [
    ("FULL", "全量 E3+", set(), False),
    ("NO_S003", "去 S003", {"S003"}, False),
    ("NO_S004", "去 S004", {"S004"}, False),
    ("NO_S006", "去 S006", {"S006"}, False),
    ("NO_BIG3", "去 S003/4/6", {"S003", "S004", "S006"}, False),
    ("REVIEWED", "仅人审边", set(), True),
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
    return {item.strip() for item in value.split(";") if item.strip()}


def issue_frame(label: str) -> str | None:
    for frame, labels in FRAME_MAP.items():
        if label in labels:
            return frame
    return None


def configure_fonts() -> None:
    available = {font.name for font in font_manager.fontManager.ttflist}
    for name in ("Microsoft YaHei", "Yu Gothic", "Meiryo", "Noto Sans CJK SC", "SimHei", "DejaVu Sans"):
        if name in available:
            plt.rcParams["font.family"] = name
            break
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["figure.facecolor"] = "white"


def scenario_edges(edges: list[dict[str, str]], dropped: set[str], reviewed_only: bool) -> list[dict[str, str]]:
    selected = []
    for edge in edges:
        if edge["evidence_level"] not in E3PLUS:
            continue
        if reviewed_only and edge["review_status"] not in REVIEWED:
            continue
        edge_refs = refs(edge["source_ref"])
        # A leave-source-out scenario removes only edges whose complete stated
        # support is exhausted.  Multi-sourced edges survive on remaining refs.
        if dropped and edge_refs and not (edge_refs - dropped):
            continue
        selected.append(edge)
    return selected


def metrics_for(edges: list[dict[str, str]]) -> tuple[dict[str, object], dict[str, set[str]]]:
    actor_frames: dict[str, set[str]] = defaultdict(set)
    actors: set[str] = set()
    for edge in edges:
        frame = issue_frame(edge["issue_label"])
        if not frame:
            continue
        actors.add(edge["actor_id"])
        actor_frames[edge["actor_id"]].add(frame)
    cross = {actor for actor, frames in actor_frames.items() if len(frames) >= 2}
    eco_int = {actor for actor, frames in actor_frames.items() if "F2 生态／环境" in frames and "F6 国际路径" in frames}
    eco_base = {actor for actor, frames in actor_frames.items() if "F2 生态／环境" in frames and "F1 基地／反军事" in frames}
    legal_base = {actor for actor, frames in actor_frames.items() if "F5 法律／程序" in frames and "F1 基地／反军事" in frames}
    return (
        {
            "edge_count": len(edges), "actor_count": len(actors), "cross_frame_actor_count": len(cross),
            "ecology_international_bridge_count": len(eco_int), "ecology_base_bridge_count": len(eco_base),
            "legal_base_bridge_count": len(legal_base),
        },
        {"cross": cross, "eco_int": eco_int, "eco_base": eco_base, "legal_base": legal_base, **actor_frames},
    )


def main() -> None:
    configure_fonts()
    OUT.mkdir(parents=True, exist_ok=True)
    actors = {row["actor_id"]: row for row in read_csv(DATA / "01_actor_registry_initial_v0.csv")}
    edges = read_csv(DATA / "07_actor_issue_edges_initial_v0.csv")

    scenario_metrics: list[dict[str, object]] = []
    scenario_sets: dict[str, dict[str, set[str]]] = {}
    for scenario_id, label, dropped, reviewed_only in SCENARIOS:
        selected = scenario_edges(edges, dropped, reviewed_only)
        metrics, sets = metrics_for(selected)
        scenario_sets[scenario_id] = sets
        scenario_metrics.append(
            {
                "scenario_id": scenario_id, "scenario_label": label,
                "dropped_sources": ";".join(sorted(dropped)), "reviewed_only": "yes" if reviewed_only else "no",
                **metrics,
                "interpretation": "Edges with independent remaining source refs survive source removal; REVIEWED is a different evidence-layer restriction.",
            }
        )

    full = next(row for row in scenario_metrics if row["scenario_id"] == "FULL")
    for row in scenario_metrics:
        for metric in ("edge_count", "actor_count", "cross_frame_actor_count", "ecology_international_bridge_count"):
            denominator = int(full[metric])
            row[f"{metric}_retention"] = round(int(row[metric]) / denominator, 3) if denominator else ""

    metric_fields = [
        "scenario_id", "scenario_label", "dropped_sources", "reviewed_only", "edge_count", "actor_count",
        "cross_frame_actor_count", "ecology_international_bridge_count", "ecology_base_bridge_count",
        "legal_base_bridge_count", "edge_count_retention", "actor_count_retention",
        "cross_frame_actor_count_retention", "ecology_international_bridge_count_retention", "interpretation",
    ]
    write_csv(OUT / "scenario_metrics_v1.csv", scenario_metrics, metric_fields)

    full_eco_int = scenario_sets["FULL"]["eco_int"]
    actor_rows: list[dict[str, object]] = []
    for actor_id in sorted(full_eco_int):
        row: dict[str, object] = {
            "actor_id": actor_id, "actor_name": actors.get(actor_id, {}).get("canonical_name", actor_id),
            "actor_class": actors.get(actor_id, {}).get("actor_class", ""),
            "origin_type": actors.get(actor_id, {}).get("origin_type", ""),
        }
        for scenario_id, _, _, _ in SCENARIOS:
            row[scenario_id] = "survives" if actor_id in scenario_sets[scenario_id]["eco_int"] else "drops"
        actor_rows.append(row)
    write_csv(
        OUT / "ecology_international_bridge_survival_v1.csv", actor_rows,
        ["actor_id", "actor_name", "actor_class", "origin_type"] + [item[0] for item in SCENARIOS],
    )

    # Dependency audit: an edge is exclusive to a listed source if removing
    # that source exhausts all stated support references.
    dependency_rows: list[dict[str, object]] = []
    for edge in edges:
        edge_refs = refs(edge["source_ref"])
        if edge["evidence_level"] not in E3PLUS:
            continue
        dependency_rows.append(
            {
                "edge_id": edge["edge_id"], "actor_id": edge["actor_id"], "issue_label": edge["issue_label"],
                "source_refs": edge["source_ref"],
                "exclusive_S003": "yes" if edge_refs and not (edge_refs - {"S003"}) else "no",
                "exclusive_S004": "yes" if edge_refs and not (edge_refs - {"S004"}) else "no",
                "exclusive_S006": "yes" if edge_refs and not (edge_refs - {"S006"}) else "no",
                "exclusive_big3": "yes" if edge_refs and not (edge_refs - {"S003", "S004", "S006"}) else "no",
                "review_status": edge["review_status"],
            }
        )
    write_csv(
        OUT / "edge_source_dependency_audit_v1.csv", dependency_rows,
        ["edge_id", "actor_id", "issue_label", "source_refs", "exclusive_S003", "exclusive_S004", "exclusive_S006", "exclusive_big3", "review_status"],
    )

    labels = [row["scenario_label"] for row in scenario_metrics]
    scenario_ids = [row["scenario_id"] for row in scenario_metrics]
    metric_specs = [
        ("actor_count_retention", "有边 actor", "#3a6f8f"),
        ("cross_frame_actor_count_retention", "跨 frame actor", "#d2863b"),
        ("ecology_international_bridge_count_retention", "生态→国际桥", "#4b8c6b"),
    ]
    fig = plt.figure(figsize=(16.5, 9.2))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.08, 1.45], wspace=0.28)
    ax1 = fig.add_subplot(gs[0, 0])
    x = np.arange(len(labels))
    width = 0.23
    for offset, (field, name, color) in enumerate(metric_specs):
        values = [float(row[field]) * 100 for row in scenario_metrics]
        bars = ax1.bar(x + (offset - 1) * width, values, width=width, label=name, color=color)
        for bar, value in zip(bars, values):
            ax1.text(bar.get_x() + bar.get_width() / 2, value + 1.0 + offset * 1.3, f"{value:.0f}%", ha="center", va="bottom", fontsize=7.5)
    ax1.set_xticks(x, labels=labels, rotation=28, ha="right")
    ax1.set_ylim(0, 112)
    ax1.set_ylabel("相对全量 E3+ 的保留率")
    ax1.set_title("A 结果对来源删除与人审收紧的敏感性", loc="left", fontsize=13, fontweight="bold")
    ax1.grid(axis="y", color="#d9dfdf", linewidth=0.7)
    ax1.spines[["top", "right"]].set_visible(False)
    ax1.legend(frameon=False, loc="upper right")

    ax2 = fig.add_subplot(gs[0, 1])
    ranked = sorted(
        full_eco_int,
        key=lambda actor: (-sum(actor in scenario_sets[sid]["eco_int"] for sid in scenario_ids), actor),
    )
    matrix = np.array([[1 if actor in scenario_sets[sid]["eco_int"] else 0 for sid in scenario_ids] for actor in ranked], dtype=int)
    if matrix.size:
        ax2.imshow(matrix, cmap="Greens", vmin=0, vmax=1, aspect="auto")
        ax2.set_yticks(range(len(ranked)), labels=[f"{actor}  {actors.get(actor, {}).get('canonical_name', actor)[:12]}" for actor in ranked], fontsize=8.5)
        ax2.set_xticks(range(len(labels)), labels=labels, rotation=28, ha="right")
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                ax2.text(j, i, "●" if matrix[i, j] else "×", ha="center", va="center", fontsize=9,
                         color="white" if matrix[i, j] else "#9a4a3c")
    else:
        ax2.text(0.5, 0.5, "全量层没有生态→国际桥 actor", ha="center", va="center")
        ax2.set_axis_off()
    ax2.set_title("B ‘生态→国际路径’ actor 的逐场景存活", loc="left", fontsize=13, fontweight="bold")
    ax2.tick_params(length=0)
    for spine in ax2.spines.values():
        spine.set_visible(False)

    fig.suptitle("R2 网络稳健性：关键桥接是否由少数大名单来源制造？", x=0.05, ha="left", fontsize=18, fontweight="bold")
    fig.text(0.05, 0.925, "删除来源时，只有在剩余 source_ref 为空的边才被移除；‘仅人审边’是更严格、但尚未完成全部人工复核的下界。", fontsize=10.5, color="#485761")
    fig.text(0.05, 0.025, "解释边界：跨议题共现表示组织在公开材料中连接多个 frame，不等于网络中介、稳定联盟或政策影响。", fontsize=9.2, color="#7a3e2e")
    fig.subplots_adjust(left=0.08, right=0.98, top=0.84, bottom=0.16)
    fig.savefig(OUT / "fig_actor_issue_robustness_v1.png", dpi=220, bbox_inches="tight")
    plt.close(fig)

    full_m = next(row for row in scenario_metrics if row["scenario_id"] == "FULL")
    no_big3 = next(row for row in scenario_metrics if row["scenario_id"] == "NO_BIG3")
    reviewed = next(row for row in scenario_metrics if row["scenario_id"] == "REVIEWED")
    readme = f"""# R2 actor-issue robustness v1

The leave-source-out result is not uniform. S003 and S006 have little effect under the independent-support rule, while removing S004 cuts the ecology-to-international bridge set from {full_m['ecology_international_bridge_count']} to {next(row for row in scenario_metrics if row['scenario_id'] == 'NO_S004')['ecology_international_bridge_count']}. Removing S003/S004/S006 together still leaves {no_big3['ecology_international_bridge_count']} such actors and retains {no_big3['cross_frame_actor_count_retention']:.1%} of all cross-frame actors. The international perimeter is therefore partly list-dependent, but a smaller core survives.

The largest overall contraction occurs in the human-reviewed-only layer ({reviewed['edge_count']} edges versus {full_m['edge_count']} full E3+ edges). This is currently an audit of review completeness as much as a substantive robustness test. Both qualifications matter: S004 materially shapes the outer bridge layer, while incomplete edge-level human review limits how much of the remaining core can be presented as final.
"""
    (OUT / "README.md").write_text(readme, encoding="utf-8", newline="\n")
    print(f"Actor-issue robustness: full eco-int={full_m['ecology_international_bridge_count']} / no-big3={no_big3['ecology_international_bridge_count']} / reviewed={reviewed['ecology_international_bridge_count']}")


if __name__ == "__main__":
    main()
