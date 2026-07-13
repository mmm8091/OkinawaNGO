from __future__ import annotations

import csv
import math
import textwrap
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch, Rectangle


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "interim"
ARCHIVE_MANIFEST = ROOT / "source_docs" / "source_archive" / "source_archive_manifest.csv"
OUT = ROOT / "outputs" / "explanatory_v0"

GOOD_EVIDENCE = {"E3", "E4"}
LINE_EVIDENCE = {"E2", "E3", "E4"}


def configure_fonts() -> None:
    candidates = [
        "Microsoft YaHei",
        "Yu Gothic",
        "Meiryo",
        "Noto Sans CJK JP",
        "Noto Sans CJK SC",
        "SimHei",
        "Arial Unicode MS",
        "DejaVu Sans",
    ]
    available = {f.name for f in font_manager.fontManager.ttflist}
    for name in candidates:
        if name in available:
            plt.rcParams["font.family"] = name
            break
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["figure.facecolor"] = "white"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def split_refs(value: str) -> set[str]:
    return {part.strip() for part in value.replace(",", ";").split(";") if part.strip()}


def short_label(name: str, limit: int = 18) -> str:
    name = name.replace("（", "\n（", 1)
    if len(name) <= limit:
        return name
    return name[: limit - 1] + "…"


def wrap_label(value: str, width: int = 16) -> str:
    return "\n".join(textwrap.wrap(value, width=width, break_long_words=False)) or value


def actor_lookup(actors: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {row["actor_id"]: row for row in actors}


def save_actor_issue_bridge_network(
    actors: list[dict[str, str]],
    issue_edges: list[dict[str, str]],
) -> None:
    actors_by_id = actor_lookup(actors)
    focus_issues = [
        "anti_base",
        "biodiversity",
        "international_advocacy",
        "local_autonomy",
        "legal",
        "life_safety",
        "frontline_prevention",
        "military_family_service",
    ]
    issue_set = set(focus_issues)

    actor_to_issues: dict[str, set[str]] = defaultdict(set)
    edge_evidence: dict[tuple[str, str], str] = {}
    for edge in issue_edges:
        if edge["issue_label"] not in issue_set:
            continue
        if edge["evidence_level"] not in LINE_EVIDENCE:
            continue
        actor_to_issues[edge["actor_id"]].add(edge["issue_label"])
        edge_evidence[(edge["actor_id"], edge["issue_label"])] = edge["evidence_level"]

    selected_actor_ids = {
        actor_id
        for actor_id, issues in actor_to_issues.items()
        if len(issues) >= 2 and actor_id in actors_by_id
    }

    rows: list[dict[str, object]] = []
    full_actor_order = sorted(selected_actor_ids, key=lambda aid: (-len(actor_to_issues[aid]), actors_by_id[aid]["origin_type"], aid))
    display_actor_ids = set(full_actor_order[:18])
    graph = nx.Graph()
    for issue in focus_issues:
        graph.add_node(issue, kind="issue", label=issue)
    for actor_id in full_actor_order:
        actor = actors_by_id[actor_id]
        issues = sorted(actor_to_issues[actor_id])
        rows.append(
            {
                "actor_id": actor_id,
                "canonical_name": actor["canonical_name"],
                "origin_type": actor["origin_type"],
                "actor_class": actor["actor_class"],
                "issue_count": len(issues),
                "issues": ";".join(issues),
                "evidence_level": actor["evidence_level"],
                "review_status": actor["review_status"],
            }
        )
        if actor_id not in display_actor_ids:
            continue
        graph.add_node(
            actor_id,
            kind="actor",
            label=f"{actor_id}\n{short_label(actor['canonical_name'], 18)}",
            origin=actor["origin_type"],
        )
        for issue in issues:
            graph.add_edge(actor_id, issue, evidence=edge_evidence[(actor_id, issue)])

    issue_y = {issue: i * 1.25 for i, issue in enumerate(reversed(focus_issues))}
    actor_order = [aid for aid in full_actor_order if aid in display_actor_ids]
    actor_y = {aid: idx * (len(focus_issues) - 1) / max(1, len(actor_order) - 1) for idx, aid in enumerate(reversed(actor_order))}
    pos = {issue: (1.0, issue_y[issue]) for issue in focus_issues}
    pos.update({aid: (0.0, actor_y[aid] * 1.25) for aid in actor_order})

    fig, ax = plt.subplots(figsize=(14, 8.2))
    ax.set_title("Top bridge actors：组织如何把基地问题连接到环保、自治、法律、国际倡议等议题", fontsize=15, pad=18)
    ax.text(
        0,
        len(focus_issues) * 1.25 + 0.55,
        "图上显示跨议题连接数最高的 18 个 actor；完整清单见 actor_issue_bridge_nodes.csv；E2 边仅作线索。",
        fontsize=9,
        color="#555",
    )

    edge_colors = {"E4": "#355c7d", "E3": "#6c8f70", "E2": "#c9a44c"}
    for source, target, data in graph.edges(data=True):
        x1, y1 = pos[source]
        x2, y2 = pos[target]
        ax.plot([x1, x2], [y1, y2], color=edge_colors.get(data["evidence"], "#999"), alpha=0.42, linewidth=1.4)

    origin_colors = {
        "okinawa_local": "#2f6f73",
        "japan_domestic": "#9b5b4d",
        "international": "#5f5b99",
        "us_origin": "#7a6a3a",
        "mixed_or_network": "#4b7f52",
        "public_institution": "#68707a",
        "corporate": "#8a6f8f",
    }

    for issue in focus_issues:
        x, y = pos[issue]
        ax.scatter(x, y, s=520, marker="s", color="#f0f3f5", edgecolor="#445", linewidth=1.2, zorder=3)
        ax.text(x + 0.035, y, issue, va="center", fontsize=10)

    for actor_id in actor_order:
        actor = actors_by_id[actor_id]
        x, y = pos[actor_id]
        color = origin_colors.get(actor["origin_type"], "#777")
        size = 80 + 35 * len(actor_to_issues[actor_id])
        ax.scatter(x, y, s=size, color=color, edgecolor="white", linewidth=0.8, zorder=4)
        ax.text(x - 0.03, y, graph.nodes[actor_id]["label"], va="center", ha="right", fontsize=7.4)

    legend_items = [
        ("E4", edge_colors["E4"]),
        ("E3", edge_colors["E3"]),
        ("E2 lead", edge_colors["E2"]),
    ]
    for idx, (label, color) in enumerate(legend_items):
        ax.plot([0.42 + idx * 0.13, 0.49 + idx * 0.13], [-0.8, -0.8], color=color, linewidth=2)
        ax.text(0.5 + idx * 0.13, -0.8, label, va="center", fontsize=8)

    ax.set_xlim(-0.52, 1.35)
    ax.set_ylim(-1.15, len(focus_issues) * 1.25 + 1.05)
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(OUT / "fig_actor_issue_bridge_network.png", dpi=220)
    plt.close(fig)

    write_csv(
        OUT / "actor_issue_bridge_nodes.csv",
        rows,
        ["actor_id", "canonical_name", "origin_type", "actor_class", "issue_count", "issues", "evidence_level", "review_status"],
    )


def save_place_issue_matrix(issue_edges: list[dict[str, str]], place_edges: list[dict[str, str]]) -> None:
    place_focus = [
        "Henoko",
        "Oura Bay",
        "Ishigaki",
        "Miyako",
        "Yonaguni",
        "Kadena",
        "Futenma",
        "Camp Foster",
        "U.S. Consulate General Naha",
        "JICA Okinawa",
    ]
    frame_map = {
        "base / anti-military": {"anti_base", "anti_military", "Henoko"},
        "ecology / environment": {"environment", "biodiversity", "dugong", "groundwater"},
        "life / health safety": {"life_safety", "health_risk", "base_community_welfare", "military_family_service"},
        "autonomy / referendum": {"local_autonomy", "referendum"},
        "legal / procedure": {"legal"},
        "international route": {"international_advocacy", "public_diplomacy", "international_cooperation"},
        "frontline / Taiwan": {"frontline_prevention", "Taiwan_contingency"},
    }

    actor_issues: dict[str, set[str]] = defaultdict(set)
    for edge in issue_edges:
        if edge["evidence_level"] in LINE_EVIDENCE:
            actor_issues[edge["actor_id"]].add(edge["issue_label"])

    actor_places: dict[str, set[str]] = defaultdict(set)
    for edge in place_edges:
        if edge["evidence_level"] in LINE_EVIDENCE:
            actor_places[edge["actor_id"]].add(edge["place_name"])

    counts: dict[tuple[str, str], int] = defaultdict(int)
    actor_sets: dict[tuple[str, str], set[str]] = defaultdict(set)
    for actor_id, places in actor_places.items():
        issues = actor_issues.get(actor_id, set())
        for place in places:
            if place not in place_focus:
                continue
            for frame, frame_issues in frame_map.items():
                if issues & frame_issues:
                    counts[(place, frame)] += 1
                    actor_sets[(place, frame)].add(actor_id)

    frames = list(frame_map)
    data = [[counts[(place, frame)] for frame in frames] for place in place_focus]

    fig, ax = plt.subplots(figsize=(13.5, 6.4))
    im = ax.imshow(data, cmap="YlGnBu")
    ax.set_title("地点 × 议题框架矩阵：不同场域承接的组织议题组合", fontsize=15, pad=18)
    frame_labels = [f"F{i}" for i in range(1, len(frames) + 1)]
    ax.set_xticks(range(len(frames)), labels=frame_labels, rotation=0, ha="center", fontsize=8.2)
    ax.set_yticks(range(len(place_focus)), labels=place_focus, fontsize=10)
    for i, row in enumerate(data):
        for j, value in enumerate(row):
            if value:
                ax.text(j, i, str(value), ha="center", va="center", fontsize=9, color="#1b2a32")
    key_lines = [
        "Frame key",
        "F1 base / anti-military",
        "F2 ecology / environment",
        "F3 life / health safety",
        "F4 autonomy / referendum",
        "F5 legal / procedure",
        "F6 international route",
        "F7 frontline / Taiwan",
    ]
    fig.text(0.07, 0.47, "\n".join(key_lines), fontsize=9.2, va="top", color="#2d3740")
    fig.text(
        0.29,
        0.055,
        "数字表示同时连接该地点与该议题框架的 actor 数；与那国不强行环保化，按前线化 / 自治 / 健康风险读取。",
        fontsize=9,
        color="#555",
    )
    fig.colorbar(im, ax=ax, fraction=0.025, pad=0.02)
    fig.subplots_adjust(left=0.31, bottom=0.17, right=0.9, top=0.86)
    fig.savefig(OUT / "fig_place_issue_matrix_explanatory.png", dpi=220)
    plt.close(fig)

    rows = []
    for place in place_focus:
        for frame in frames:
            rows.append(
                {
                    "place": place,
                    "frame": frame,
                    "actor_count": counts[(place, frame)],
                    "actor_ids": ";".join(sorted(actor_sets[(place, frame)])),
                }
            )
    write_csv(OUT / "place_issue_matrix.csv", rows, ["place", "frame", "actor_count", "actor_ids"])


def save_henoko_pathway() -> None:
    layers = [
        ("Local site", [("Henoko / Oura Bay", "P002/P003")]),
        ("Local actors", [("A019\nヘリ基地反対協", "E4"), ("A003\nジュゴンネットワーク沖縄", "E3"), ("A076\nSave the Dugong Foundation", "E3")]),
        ("Domestic NGO / legal", [("A004\nNACSJ", "E4"), ("A005\nWWF Japan", "E4"), ("A020\nJELF", "E4")]),
        ("Translation frames", [("dugong / biodiversity", "E4"), ("EIA / legal procedure", "E3/E4"), ("local autonomy", "E3")]),
        ("International route", [("A001\nOEJP -> MMC", "E4"), ("A009\nEarthjustice", "E4"), ("2015 / 2020\nsignatory networks", "signatory-only")]),
    ]

    fig, ax = plt.subplots(figsize=(14, 6.4))
    ax.set_title("边野古 / 大浦湾：地方基地争议如何转译为环保、法律程序与国际倡议", fontsize=15, pad=18)
    ax.text(
        0.02,
        0.02,
        "读法：这是路径图，不是资金链，也不是稳定联盟图；共同署名只表示共同发声。",
        transform=ax.transAxes,
        fontsize=9,
        color="#555",
    )

    colors = ["#e8f1f2", "#eaf4ea", "#f6eee9", "#f5f1da", "#eceaf4"]
    xs = [i * 2.35 for i in range(len(layers))]
    node_positions = []
    for layer_idx, ((title, nodes), x) in enumerate(zip(layers, xs)):
        ax.text(x, 4.85, title, ha="center", fontsize=11, fontweight="bold", color="#28343a")
        y_start = 3.85
        for idx, (label, tag) in enumerate(nodes):
            y = y_start - idx * 1.18
            rect = Rectangle((x - 0.75, y - 0.36), 1.5, 0.72, facecolor=colors[layer_idx], edgecolor="#6b7680", linewidth=1)
            ax.add_patch(rect)
            ax.text(x, y + 0.08, label, ha="center", va="center", fontsize=8.2)
            ax.text(x, y - 0.22, tag, ha="center", va="center", fontsize=7, color="#666")
            node_positions.append((layer_idx, idx, x, y))

    for layer_idx in range(len(layers) - 1):
        left_nodes = [p for p in node_positions if p[0] == layer_idx]
        right_nodes = [p for p in node_positions if p[0] == layer_idx + 1]
        for _, _, x1, y1 in left_nodes:
            for _, _, x2, y2 in right_nodes:
                if len(left_nodes) > 2 and len(right_nodes) > 2 and abs(y1 - y2) > 1.4:
                    continue
                arrow = FancyArrowPatch(
                    (x1 + 0.78, y1),
                    (x2 - 0.78, y2),
                    arrowstyle="-|>",
                    mutation_scale=9,
                    linewidth=1.05,
                    color="#77838c",
                    alpha=0.55,
                )
                ax.add_patch(arrow)

    ax.set_xlim(-1, xs[-1] + 1)
    ax.set_ylim(-0.2, 5.25)
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(OUT / "fig_henoko_internationalization_pathway.png", dpi=220)
    plt.close(fig)


def save_coaction_event_composition(actors: list[dict[str, str]]) -> None:
    events = [
        ("2010 WWF\n67 groups", "S003"),
        ("2015 NACSJ\n31 NGOs", "S004"),
        ("2020 OEJP/MMC\n71 groups", "S006"),
    ]
    origin_order = ["okinawa_local", "japan_domestic", "international", "us_origin", "mixed_or_network", "unclear"]
    colors = {
        "okinawa_local": "#2f6f73",
        "japan_domestic": "#9b5b4d",
        "international": "#5f5b99",
        "us_origin": "#7a6a3a",
        "mixed_or_network": "#4b7f52",
        "unclear": "#9aa0a6",
    }
    rows = []
    counts_by_event: dict[str, Counter[str]] = {}
    for label, source_id in events:
        counter: Counter[str] = Counter()
        actor_ids = []
        for actor in actors:
            if source_id in split_refs(actor["source_refs"]):
                origin = actor["origin_type"] if actor["origin_type"] in origin_order else "unclear"
                counter[origin] += 1
                actor_ids.append(actor["actor_id"])
        counts_by_event[label] = counter
        for origin in origin_order:
            rows.append({"event": label.replace("\n", " "), "source_id": source_id, "origin_type": origin, "count": counter[origin]})
        rows.append({"event": label.replace("\n", " "), "source_id": source_id, "origin_type": "actor_ids", "count": ";".join(sorted(actor_ids))})

    fig, ax = plt.subplots(figsize=(10.8, 5.9))
    bottoms = [0] * len(events)
    x = list(range(len(events)))
    for origin in origin_order:
        values = [counts_by_event[label][origin] for label, _ in events]
        ax.bar(x, values, bottom=bottoms, label=origin, color=colors[origin], width=0.55)
        bottoms = [b + v for b, v in zip(bottoms, values)]
    for idx, total in enumerate(bottoms):
        ax.text(idx, total + 0.35, str(total), ha="center", fontsize=10)
    ax.set_title("共同行动样本：署名来源构成，而非稳定联盟强度", fontsize=15, pad=15)
    ax.set_xticks(x, labels=[label for label, _ in events], fontsize=10)
    ax.set_ylabel("Actors currently entered in registry")
    ax.grid(axis="y", alpha=0.25)
    ax.legend(loc="upper left", bbox_to_anchor=(1.01, 1), frameon=False, fontsize=8)
    ax.text(
        -0.45,
        -4.2,
        "注意：这里统计的是当前 registry 中带有对应 source_id 的 actor，不是声明原文全量签名数。",
        fontsize=9,
        color="#555",
    )
    fig.tight_layout()
    fig.savefig(OUT / "fig_coaction_sample_composition.png", dpi=220)
    plt.close(fig)
    write_csv(OUT / "coaction_sample_composition.csv", rows, ["event", "source_id", "origin_type", "count"])


def save_evidence_gap_map(actors: list[dict[str, str]], sources: list[dict[str, str]], manifest: list[dict[str, str]]) -> None:
    actor_status = Counter(row["review_status"] for row in actors)
    source_archive = Counter(row["archive_status"] for row in manifest)

    fig, axes = plt.subplots(1, 2, figsize=(13.5, 5.4))
    status_colors = ["#607d8b", "#8d6e63", "#6b8e62", "#c9a44c", "#9e6a6a", "#7e6ca8", "#9099a1"]

    items = actor_status.most_common()
    axes[0].barh([k for k, _ in items][::-1], [v for _, v in items][::-1], color=status_colors[: len(items)][::-1])
    axes[0].set_title("Actor review status after HR merge", fontsize=12)
    axes[0].grid(axis="x", alpha=0.25)
    for i, (_, value) in enumerate(items[::-1]):
        axes[0].text(value + 0.25, i, str(value), va="center", fontsize=9)

    archive_items = source_archive.most_common()
    axes[1].barh([k for k, _ in archive_items][::-1], [v for _, v in archive_items][::-1], color=status_colors[: len(archive_items)][::-1])
    axes[1].set_title("Source archive status", fontsize=12)
    axes[1].grid(axis="x", alpha=0.25)
    for i, (_, value) in enumerate(archive_items[::-1]):
        axes[1].text(value + 0.25, i, str(value), va="center", fontsize=9)

    fig.suptitle("下一轮调查缺口：复核状态与来源归档状态", fontsize=15)
    fig.tight_layout()
    fig.savefig(OUT / "fig_evidence_gap_map.png", dpi=220)
    plt.close(fig)

    rows = []
    source_by_id = {row["source_id"]: row for row in sources}
    for row in actors:
        if row["review_status"] in {"needs_second_source", "needs_local_retrieval", "watchlist_only"} or row["evidence_level"] == "E2":
            rows.append(
                {
                    "item_type": "actor",
                    "item_id": row["actor_id"],
                    "name": row["canonical_name"],
                    "priority": row["review_priority"],
                    "status": row["review_status"],
                    "evidence_level": row["evidence_level"],
                    "next_action": "second_source_or_local_retrieval",
                    "notes": row["notes"],
                }
            )
    for row in manifest:
        if row["archive_status"] in {"pending_archive", "skipped_inferred_url", "skipped_non_url_reference"}:
            source = source_by_id.get(row["source_id"], {})
            rows.append(
                {
                    "item_type": "source",
                    "item_id": row["source_id"],
                    "name": row["title"],
                    "priority": "",
                    "status": row["archive_status"],
                    "evidence_level": source.get("evidence_level", ""),
                    "next_action": "archive_or_verify_url",
                    "notes": row["note"],
                }
            )
    write_csv(
        OUT / "next_investigation_candidates.csv",
        rows,
        ["item_type", "item_id", "name", "priority", "status", "evidence_level", "next_action", "notes"],
    )


def write_readme(
    actors: list[dict[str, str]],
    sources: list[dict[str, str]],
    manifest: list[dict[str, str]],
) -> None:
    archive_status = Counter(row["archive_status"] for row in manifest)
    content = f"""# 解释性图表包 v0

日期：2026-07-12（数据刷新）

目的：把当前 {len(actors)} 个 actor、{len(sources)} 条 source 和人工复核状态转成可沟通、可继续探索的图件。此包不是最终报告；它用于下一次沟通前验证叙事，并暴露下一轮补源方向。HR-011/012/014/015 已回写；HR-013 尚未收到；A087-A101 仍只完成 E4 身份级合并，A077-A085 依 HR-015 仅保留为 E2 事件参与者、不进入 registry。

## 图件

1. `fig_actor_issue_bridge_network.png`
   - 显示连接两个及以上重点议题的 actor。
   - 读法：哪些组织在反基地、环保、国际倡议、地方自治、法律、生活安全之间起桥接作用。
   - 注意：E2 边只作线索。

2. `fig_place_issue_matrix_explanatory.png`
   - 显示地点和议题框架的交叉强度。
   - 读法：边野古/大浦湾承接环保和国际倡议，石垣/宫古承接生活安全，与那国按前线化/自治/健康风险读取。

3. `fig_henoko_internationalization_pathway.png`
   - 显示边野古/大浦湾如何从地方基地争议转译为儒艮、生物多样性、法律程序和国际倡议。
   - 注意：这是路径图，不是资金链，也不是稳定联盟图。

4. `fig_coaction_sample_composition.png`
   - 显示 2010、2015、2020 三个共同行动样本在当前 registry 中的 actor 来源构成。
   - 注意：统计的是当前录入 actor，不是声明原文全量签名数。

5. `fig_evidence_gap_map.png`
   - 显示 HR 合并后的 actor 复核状态和 source archive 状态。
   - 用于决定下一轮调查优先级。

## 配套 CSV

- `actor_issue_bridge_nodes.csv`
- `place_issue_matrix.csv`
- `coaction_sample_composition.csv`
- `next_investigation_candidates.csv`

## 当前最适合继续调查的方向

1. 手工处理 {archive_status.get('failed', 0)} 条自动归档失败来源；失败状态不等于证据不存在。
2. 执行已收到的 HR-010、011、012、014、015：新增主体定性、E3 补源、沿革/范围、R8 角色及 evidence/venue seed；HR-013 仍待提交。
3. 与那国 A014/A015 的地方报纸、意见广告实物、议会资料。
4. AWWA / spouse club charity recipients 和 Schedule I / 活动手册。
5. 继续把共同行动保持为 event table，不因重复同场直接生成联盟网络。

## 禁止误读

- 共同署名不等于稳定联盟。
- grant opportunity 不等于已拨款。
- 服务型 NGO 不自动代表政治立场。
- 与那国不强行写成环保拒止案例。
"""
    (OUT / "README.md").write_text(content, encoding="utf-8")


def main() -> None:
    configure_fonts()
    OUT.mkdir(parents=True, exist_ok=True)
    actors = read_csv(DATA / "01_actor_registry_initial_v0.csv")
    sources = read_csv(DATA / "05_source_log_initial_v0.csv")
    issue_edges = read_csv(DATA / "07_actor_issue_edges_initial_v0.csv")
    place_edges = read_csv(DATA / "08_actor_place_edges_initial_v0.csv")
    manifest = read_csv(ARCHIVE_MANIFEST)

    save_actor_issue_bridge_network(actors, issue_edges)
    save_place_issue_matrix(issue_edges, place_edges)
    save_henoko_pathway()
    save_coaction_event_composition(actors)
    save_evidence_gap_map(actors, sources, manifest)
    write_readme(actors, sources, manifest)
    print(f"Wrote explanatory graph package to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
