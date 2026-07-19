from __future__ import annotations

"""Build client-facing figures for the third progress sync.

The figures are deliberately simpler than the internal audit charts.  Every
number is read from an existing research output, asserted against the current
snapshot, and exported with a compact supporting CSV.
"""

import csv
from pathlib import Path
from textwrap import fill

import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.colors import BoundaryNorm, ListedColormap
from matplotlib.patches import FancyBboxPatch, Rectangle
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "formal_comm_v1"
FIG = OUT / "fig"
DATA = OUT / "data"

BG = "#F7F5F1"
INK = "#18364B"
TEXT = "#27333B"
MUTED = "#68747C"
GRID = "#D8D6D0"
TEAL = "#2F7F79"
TEAL_MID = "#78AEA7"
TEAL_LIGHT = "#DCEBE8"
BLUE = "#397596"
ORANGE = "#D48632"
ORANGE_LIGHT = "#F0D6AE"
GREEN = "#408C6A"
GRAY = "#A7ADB2"
LIGHT_GRAY = "#E4E5E4"
RUST = "#9A513C"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def configure() -> None:
    available = {font.name for font in font_manager.fontManager.ttflist}
    for name in (
        "Microsoft YaHei",
        "Noto Sans CJK SC",
        "Source Han Sans SC",
        "SimHei",
        "Arial Unicode MS",
        "DejaVu Sans",
    ):
        if name in available:
            plt.rcParams["font.family"] = name
            break
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["figure.facecolor"] = BG
    plt.rcParams["axes.facecolor"] = BG
    FIG.mkdir(parents=True, exist_ok=True)
    DATA.mkdir(parents=True, exist_ok=True)


def save(fig: plt.Figure, name: str) -> None:
    fig.savefig(FIG / name, dpi=180, facecolor=BG, bbox_inches="tight", pad_inches=0.12)
    plt.close(fig)


def title_block(fig: plt.Figure, title: str, subtitle: str) -> None:
    fig.text(0.055, 0.945, title, ha="left", va="top", fontsize=23, weight="bold", color=INK)
    fig.text(0.055, 0.892, subtitle, ha="left", va="top", fontsize=11.5, color=MUTED)


def rounded_box(
    fig: plt.Figure,
    x: float,
    y: float,
    w: float,
    h: float,
    face: str,
    edge: str = "none",
    radius: float = 0.015,
) -> FancyBboxPatch:
    box = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle=f"round,pad=0.008,rounding_size={radius}",
        transform=fig.transFigure,
        facecolor=face,
        edgecolor=edge,
        linewidth=1.0,
    )
    fig.add_artist(box)
    return box


def draw_metric_card(
    fig: plt.Figure,
    x: float,
    y: float,
    w: float,
    h: float,
    value: str,
    label: str,
    note: str,
    accent: str,
) -> None:
    rounded_box(fig, x, y, w, h, "#EFEEE9")
    fig.add_artist(
        Rectangle((x, y), 0.008, h, transform=fig.transFigure, facecolor=accent, edgecolor="none")
    )
    fig.text(x + 0.026, y + h * 0.62, value, fontsize=25, weight="bold", color=accent, va="center")
    fig.text(x + 0.026, y + h * 0.35, label, fontsize=11.5, weight="bold", color=TEXT, va="center")
    fig.text(x + 0.026, y + h * 0.15, note, fontsize=8.8, color=MUTED, va="center")


def figure_place_issue() -> None:
    metrics = {
        row["metric"]: int(row["value"])
        for row in read_csv(ROOT / "outputs" / "R03_strict_place_issue_v1" / "validation_metrics_v1.csv")
    }
    expected = {
        "all_same_source_triples": 330,
        "e3plus_same_source_triples": 323,
        "human_reviewed_same_source_triples": 67,
        "strict_e3plus_nonzero_cells": 42,
        "reviewed_nonzero_cells": 13,
    }
    for key, value in expected.items():
        assert metrics[key] == value, (key, metrics[key], value)

    rows = read_csv(
        ROOT / "outputs" / "R03_strict_place_issue_v1" / "place_issue_strict_sensitivity_matrix_v1.csv"
    )
    place_order = []
    frame_order = []
    for row in rows:
        if row["place_label"] not in place_order:
            place_order.append(row["place_label"])
        if row["frame_name"] not in frame_order:
            frame_order.append(row["frame_name"])

    def matrix(field: str) -> np.ndarray:
        lookup = {(r["place_label"], r["frame_name"]): int(r[field]) for r in rows}
        return np.array([[lookup[(p, f)] for f in frame_order] for p in place_order], dtype=int)

    strict = matrix("same_source_e3plus_actor_count")
    reviewed = matrix("human_reviewed_same_source_actor_count")

    fig = plt.figure(figsize=(13.33, 7.5))
    title_block(
        fig,
        "方法更新：地点 × 议题图改用同一来源证据",
        "旧图把一个组织的全部地点与全部议题相互组合，已停止使用；新图只保留文献中可追溯的同源关系。",
    )

    rounded_box(fig, 0.055, 0.785, 0.89, 0.058, "#F2E4DF", edge="#D9B3A8")
    fig.text(
        0.073,
        0.814,
        "主动修正：旧宽口径矩阵仅保留作方法上界，不再作为各地议题分布的正式结论。",
        fontsize=10.5,
        color=RUST,
        va="center",
        weight="bold",
    )

    cards = [
        ("330", "同源证据记录", "组织 × 地点 × 议题 × 来源", BLUE),
        ("323", "E3 / E4 严格候选", "排除低证据同源记录", TEAL),
        ("67", "双边均已人工复核", "地点边与议题边均经复核", ORANGE),
    ]
    for i, item in enumerate(cards):
        draw_metric_card(fig, 0.055 + i * 0.302, 0.635, 0.282, 0.115, *item)

    cmap = ListedColormap(["#F2F1ED", TEAL_LIGHT, "#9ECAC2", TEAL])
    norm = BoundaryNorm([-0.5, 0.5, 2.5, 5.5, 100], cmap.N)
    axes = [
        fig.add_axes([0.075, 0.135, 0.41, 0.405]),
        fig.add_axes([0.545, 0.135, 0.41, 0.405]),
    ]
    arrays = [strict, reviewed]
    panel_titles = [
        "同源 E3 / E4 候选层 · 42 个非空格",
        "双边人工复核层 · 13 个非空格",
    ]
    for idx, (ax, array, panel_title) in enumerate(zip(axes, arrays, panel_titles)):
        ax.imshow(array, cmap=cmap, norm=norm, aspect="auto")
        ax.set_title(panel_title, loc="left", fontsize=12.5, weight="bold", color=INK, pad=10)
        ax.set_xticks(range(len(frame_order)), labels=[name.replace("／", "\n") for name in frame_order], fontsize=7.8)
        ax.set_yticks(range(len(place_order)), labels=place_order if idx == 0 else [], fontsize=8.8)
        ax.tick_params(length=0, colors=TEXT)
        for i in range(array.shape[0]):
            for j in range(array.shape[1]):
                value = int(array[i, j])
                if value:
                    ax.text(
                        j,
                        i,
                        str(value),
                        ha="center",
                        va="center",
                        fontsize=7.5,
                        weight="bold",
                        color="white" if value >= 6 else TEXT,
                    )
        for spine in ax.spines.values():
            spine.set_visible(False)

    legend = [("1–2", TEAL_LIGHT), ("3–5", "#9ECAC2"), ("6+", TEAL)]
    lx = 0.075
    for label, color in legend:
        fig.add_artist(Rectangle((lx, 0.076), 0.018, 0.018, transform=fig.transFigure, facecolor=color, edgecolor="none"))
        fig.text(lx + 0.024, 0.085, f"每格不同组织数：{label}" if lx == 0.075 else label, fontsize=8.4, color=MUTED, va="center")
        lx += 0.135 if lx == 0.075 else 0.075
    fig.text(
        0.055,
        0.03,
        "读法：同源证明文献级共现；它仍不自动证明同一事件、因果关系、长期在场或稳定联盟。",
        fontsize=9.2,
        color=RUST,
    )
    save(fig, "fig1_place_issue_evidence_v1.png")

    export = []
    for row in rows:
        export.append(
            {
                "place": row["place_label"],
                "issue_frame": row["frame_name"],
                "same_source_e3plus_actor_count": row["same_source_e3plus_actor_count"],
                "dual_human_reviewed_actor_count": row["human_reviewed_same_source_actor_count"],
            }
        )
    write_csv(
        DATA / "fig1_place_issue_evidence_v1.csv",
        export,
        ["place", "issue_frame", "same_source_e3plus_actor_count", "dual_human_reviewed_actor_count"],
    )


def figure_robustness() -> None:
    rows = read_csv(ROOT / "outputs" / "R02_actor_issue_robustness_v1" / "scenario_metrics_v1.csv")
    by_id = {row["scenario_id"]: row for row in rows}
    scenario_ids = ["FULL", "NO_S003", "NO_S004", "NO_S006", "NO_BIG3", "REVIEWED"]
    labels = ["全量 E3/E4", "移除 2010 名单", "移除 2015 名单", "移除 2020 名单", "移除三组名单", "仅人工复核"]
    values = [int(by_id[item]["ecology_international_bridge_count"]) for item in scenario_ids]
    assert values == [8, 8, 4, 8, 4, 2], values

    survival = read_csv(
        ROOT / "outputs" / "R02_actor_issue_robustness_v1" / "ecology_international_bridge_survival_v1.csv"
    )
    survivors = [row for row in survival if row["NO_BIG3"] == "survives"]
    assert [row["actor_id"] for row in survivors] == ["A001", "A002", "A009", "A046"]

    fig = plt.figure(figsize=(13.33, 7.5))
    title_block(
        fig,
        "名单来源影响外围结构，但不能解释全部跨议题连接",
        "检验的是同一组织是否同时出现在“生态／环境”和“国际路径”议题中；不是稳定联盟或影响力排名。",
    )

    ax = fig.add_axes([0.075, 0.19, 0.50, 0.61])
    y = np.arange(len(labels))
    colors = [TEAL, TEAL_MID, ORANGE, TEAL_MID, ORANGE, BLUE]
    bars = ax.barh(y, values, color=colors, height=0.58)
    ax.set_yticks(y, labels=labels, fontsize=10)
    ax.invert_yaxis()
    ax.set_xlim(0, 9)
    ax.set_xticks(range(0, 10, 2))
    ax.set_xlabel("候选跨议题组织数", fontsize=9.5, color=MUTED)
    ax.grid(axis="x", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", length=0, colors=TEXT)
    ax.tick_params(axis="x", colors=MUTED)
    for bar, value in zip(bars, values):
        ax.text(value + 0.14, bar.get_y() + bar.get_height() / 2, str(value), va="center", fontsize=12, weight="bold", color=TEXT)
    ax.annotate(
        "8 → 4",
        xy=(4, 4),
        xytext=(6.3, 3.45),
        fontsize=18,
        weight="bold",
        color=ORANGE,
        arrowprops={"arrowstyle": "->", "color": ORANGE, "lw": 1.8},
    )

    rounded_box(fig, 0.625, 0.215, 0.32, 0.55, "#EFEEE9")
    fig.text(0.65, 0.72, "移除三组名单后仍存在的\n候选跨议题组织", fontsize=13, weight="bold", color=INK, va="top")
    display_names = {
        "A001": "Okinawa Environmental Justice Project",
        "A002": "ジュゴン保護キャンペーンセンター（SDCC）",
        "A009": "Earthjustice",
        "A046": "Pro Natura",
    }
    for index, actor_id in enumerate(["A001", "A002", "A009", "A046"]):
        yy = 0.61 - index * 0.092
        fig.add_artist(Rectangle((0.651, yy - 0.012), 0.014, 0.014, transform=fig.transFigure, facecolor=TEAL, edgecolor="none"))
        fig.text(0.675, yy, actor_id, fontsize=9.8, weight="bold", color=TEXT, va="center")
        fig.text(0.718, yy, fill(display_names[actor_id], 30), fontsize=9.5, color=TEXT, va="center")
    rounded_box(fig, 0.65, 0.245, 0.27, 0.072, "#E4ECEF")
    fig.text(0.668, 0.281, "仅人工复核层目前保留 2 个：A002、A046", fontsize=9.5, color=BLUE, va="center", weight="bold")

    fig.text(
        0.055,
        0.085,
        "发现：2015 年大名单对外围结构影响明显，但移除三组名单后仍保留 4 个候选跨议题组织。",
        fontsize=11.5,
        weight="bold",
        color=INK,
    )
    fig.text(
        0.055,
        0.04,
        "边界：来源删除只移除失去全部支持来源的议题边；跨议题共现不等于网络中介、稳定联盟或政策影响。",
        fontsize=9.2,
        color=RUST,
    )
    save(fig, "fig2_actor_issue_robustness_v1.png")

    export = []
    for sid, label, value in zip(scenario_ids, labels, values):
        export.append({"scenario_id": sid, "scenario_label": label, "candidate_actor_count": value})
    write_csv(DATA / "fig2_actor_issue_robustness_v1.csv", export, ["scenario_id", "scenario_label", "candidate_actor_count"])
    write_csv(
        DATA / "fig2_surviving_candidate_actors_v1.csv",
        [{"actor_id": actor_id, "actor_name": display_names[actor_id]} for actor_id in display_names],
        ["actor_id", "actor_name"],
    )


def figure_repeat_participation() -> None:
    participation = read_csv(
        ROOT / "outputs" / "R05_coaction_v1" / "actor_event_bipartite_edges_v0.csv"
    )
    event_ids_ordered = ["EV2010_WWF_67", "EV2015_NACSJ_31", "EV2020_OEJP_MMC_71"]
    event_counts = {
        event_id: sum(row["event_id"] == event_id for row in participation)
        for event_id in event_ids_ordered
    }
    assert event_counts == {
        "EV2010_WWF_67": 67,
        "EV2015_NACSJ_31": 31,
        "EV2020_OEJP_MMC_71": 71,
    }, event_counts
    total_participation = sum(event_counts.values())
    assert total_participation == len(participation) == 169

    rows = read_csv(ROOT / "outputs" / "R05_coaction_v1" / "repeat_participation_bridges_v0.csv")
    assert len(rows) == 15
    counts = {row["actor_id"]: int(row["event_count"]) for row in rows}
    assert sum(value == 3 for value in counts.values()) == 3
    assert sum(value == 2 for value in counts.values()) == 12

    event_sets = {row["actor_id"]: set(row["event_ids"].split(";")) for row in rows}
    event_2010 = "EV2010_WWF_67"
    event_2015 = "EV2015_NACSJ_31"
    event_2020 = "EV2020_OEJP_MMC_71"
    pattern_counts = {
        "贯穿三次": sum(len(events) == 3 for events in event_sets.values()),
        "仅 2010 + 2015": sum(events == {event_2010, event_2015} for events in event_sets.values()),
        "仅 2010 + 2020": sum(events == {event_2010, event_2020} for events in event_sets.values()),
        "仅 2015 + 2020": sum(events == {event_2015, event_2020} for events in event_sets.values()),
    }
    assert list(pattern_counts.values()) == [3, 7, 5, 0], pattern_counts

    fig = plt.figure(figsize=(13.33, 7.5))
    title_block(
        fig,
        "三次公开行动的可见连续性，集中在少数重复参与组织",
        "2010、2015、2020 三张边野古／大浦湾完整名单已结构化；重复计算只使用身份已确认的组织。",
    )

    cards = [
        (
            str(total_participation),
            "参与记录",
            " + ".join(str(event_counts[event_id]) for event_id in event_ids_ordered),
            BLUE,
        ),
        ("15", "至少重复出现两次", "按已确认身份严格合并", TEAL),
        ("3", "贯穿三次行动", "少数节点形成可见连续性", ORANGE),
    ]
    for i, item in enumerate(cards):
        draw_metric_card(fig, 0.055 + i * 0.302, 0.695, 0.282, 0.125, *item)

    ax = fig.add_axes([0.095, 0.225, 0.50, 0.38])
    labels = list(pattern_counts.keys())
    values = list(pattern_counts.values())
    colors = [ORANGE, TEAL, TEAL_MID, LIGHT_GRAY]
    y = np.arange(len(labels))
    bars = ax.barh(y, values, color=colors, height=0.55)
    ax.set_yticks(y, labels=labels, fontsize=10.5)
    ax.invert_yaxis()
    ax.set_xlim(0, 8)
    ax.set_xticks(range(0, 9, 2))
    ax.set_xlabel("重复参与组织数", fontsize=9.5, color=MUTED)
    ax.grid(axis="x", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", length=0, colors=TEXT)
    ax.tick_params(axis="x", colors=MUTED)
    for bar, value in zip(bars, values):
        ax.text(max(value, 0) + 0.12, bar.get_y() + bar.get_height() / 2, str(value), va="center", fontsize=12, weight="bold", color=TEXT)

    rounded_box(fig, 0.64, 0.255, 0.305, 0.33, "#EFEEE9")
    fig.text(0.668, 0.545, "贯穿三次的 3 个组织", fontsize=13, weight="bold", color=INK, va="top")
    three = [row for row in rows if int(row["event_count"]) == 3]
    names = [
        "ジュゴン保護キャンペーンセンター（SDCC）",
        "日本自然保護協会（NACSJ）",
        "ラムサール・ネットワーク日本",
    ]
    assert {row["actor_id"] for row in three} == {"A002", "A004", "A022"}
    for index, name in enumerate(names):
        yy = 0.47 - index * 0.082
        fig.add_artist(Rectangle((0.67, yy - 0.012), 0.014, 0.014, transform=fig.transFigure, facecolor=ORANGE, edgecolor="none"))
        fig.text(0.695, yy, name, fontsize=10, color=TEXT, va="center")

    fig.text(
        0.055,
        0.105,
        "发现：连续性不是由名单规模自动产生；严格合并后，15 个组织重复出现，其中只有 3 个贯穿三次。",
        fontsize=11.5,
        weight="bold",
        color=INK,
    )
    fig.text(
        0.055,
        0.055,
        "边界：三次都是目的性选取的公开行动；重复署名／要请只证明公开参与，不证明成员关系、稳定联盟或持续协调。",
        fontsize=9.2,
        color=RUST,
    )
    save(fig, "fig3_repeat_participation_v1.png")

    export = [
        {"record_type": "event_participation", "label": event_id, "count": event_counts[event_id]}
        for event_id in event_ids_ordered
    ]
    export.append({"record_type": "event_participation_total", "label": "three_event_total", "count": total_participation})
    export.extend(
        {"record_type": "repeat_pattern", "label": key, "count": value}
        for key, value in pattern_counts.items()
    )
    write_csv(DATA / "fig3_repeat_participation_v1.csv", export, ["record_type", "label", "count"])


def figure_translation_results() -> None:
    rows = read_csv(
        ROOT / "outputs" / "translation_episode_comparison_v1" / "translation_episode_candidates_v1.csv"
    )
    selected_ids = ["TE01", "TE02", "TE03", "TE04", "TE05", "TE06", "TE07", "TE09"]
    selected = [row for row in rows if row["episode_id"] in selected_ids]
    selected.sort(key=lambda row: selected_ids.index(row["episode_id"]))
    assert [row["episode_id"] for row in selected] == selected_ids

    stages = [
        ("进入制度／策略场域", "venue_entry"),
        ("产生可观察中间产出", "intermediate_output"),
        ("有限救济／参与性决定", "bounded_gain"),
        ("底层项目／政策按诉求改变", "underlying_change"),
    ]
    summary = []
    for label, field in stages:
        counts = {status: sum(row[field] == status for row in selected) for status in ("yes", "mixed", "no", "unknown")}
        summary.append({"stage": label, **counts})
    assert [(r["yes"], r["mixed"], r["no"]) for r in summary] == [(8, 0, 0), (8, 0, 0), (4, 1, 3), (0, 1, 7)]

    fig = plt.figure(figsize=(13.33, 7.5))
    title_block(
        fig,
        "程序产出与政策改变，是两个不同层次的结果",
        "比较 8 个已有正式证据支持、且无明确当地证据缺口的法律／行政／公投案例；不是总体成功率。",
    )

    ax = fig.add_axes([0.085, 0.22, 0.58, 0.58])
    y = np.arange(len(stages))
    left = np.zeros(len(stages))
    status_specs = [("yes", "是", GREEN), ("mixed", "混合", ORANGE), ("no", "否", GRAY)]
    for status, label, color in status_specs:
        values = np.array([row[status] for row in summary])
        bars = ax.barh(y, values, left=left, color=color, height=0.58, label=label)
        for bar, value in zip(bars, values):
            if value:
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_y() + bar.get_height() / 2,
                    f"{label} {int(value)}",
                    ha="center",
                    va="center",
                    fontsize=10,
                    weight="bold",
                    color="white" if status in {"yes", "mixed"} else TEXT,
                )
        left += values
    ax.set_yticks(y, labels=[item[0] for item in stages], fontsize=11)
    ax.invert_yaxis()
    ax.set_xlim(0, 8)
    ax.set_xticks(range(0, 9))
    ax.set_xlabel("案例数（n=8）", fontsize=9.5, color=MUTED)
    ax.grid(axis="x", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", length=0, colors=TEXT)
    ax.tick_params(axis="x", colors=MUTED)
    ax.legend(frameon=False, loc="lower left", bbox_to_anchor=(0, 1.01), ncol=3, fontsize=9.5)

    rounded_box(fig, 0.71, 0.255, 0.235, 0.49, "#EFEEE9")
    fig.text(0.733, 0.708, "纳入比较的 8 个案例", fontsize=13, weight="bold", color=INK, va="top")
    case_names = [
        "儒艮海外诉讼",
        "边野古 EIA 意见",
        "嘉手纳第三次噪音诉讼",
        "普天间周边噪音诉讼",
        "石垣部署公投诉讼",
        "泡濑公金诉讼",
        "名护 1997 公投",
        "2019 边野古县民投票",
    ]
    for index, name in enumerate(case_names):
        yy = 0.65 - index * 0.0365
        fig.text(0.735, yy, f"{index + 1}. {name}", fontsize=8.25, color=TEXT, va="center")

    rounded_box(fig, 0.73, 0.275, 0.195, 0.085, "#F2E4DF", edge="#D9B3A8")
    fig.text(0.748, 0.331, "明确按诉求改变", fontsize=9.1, color=RUST, va="center")
    fig.text(0.748, 0.298, "0 / 8（另 1 个混合）", fontsize=13.5, weight="bold", color=RUST, va="center")

    fig.text(
        0.055,
        0.105,
        "发现：8 个案例都留下判决、行政记录或投票结果；4 个有有限收益、1 个结果混合，但没有明确的底层项目改变。",
        fontsize=11.2,
        weight="bold",
        color=INK,
    )
    fig.text(
        0.055,
        0.052,
        "边界：案例本来就是“已进入场域”的目的性样本；赔偿、程序记录、投票或行政答复不能自动写成政策成功。",
        fontsize=9.2,
        color=RUST,
    )
    save(fig, "fig4_translation_results_v1.png")

    write_csv(
        DATA / "fig4_translation_results_summary_v1.csv",
        summary,
        ["stage", "yes", "mixed", "no", "unknown"],
    )
    write_csv(
        DATA / "fig4_translation_formal_cases_v1.csv",
        selected,
        list(selected[0].keys()),
    )


def main() -> None:
    configure()
    figure_place_issue()
    figure_robustness()
    figure_repeat_participation()
    figure_translation_results()
    print(f"Third progress sync figures written to {FIG}")


if __name__ == "__main__":
    main()
