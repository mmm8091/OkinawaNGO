from __future__ import annotations

"""Build the Phase-1 visualization closeout package.

The package complements (and does not overwrite) explanatory_v0 and
module_completion_v0.  It uses only existing project CSVs and keeps candidate
edges and event participation distinct from stable organizational relations.
"""

import csv
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from matplotlib.lines import Line2D


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "interim"
MODULE = ROOT / "outputs" / "module_completion_v0"
OUT = ROOT / "outputs" / "phase1_visuals_v1"

EVIDENCE = {"E2": "#d7b46a", "E3": "#79a486", "E4": "#315f7d"}
FAMILY_COLORS = {
    "本地公民行动": "#2f6f73",
    "环保／国际倡议": "#5f5b99",
    "法律／制度渠道": "#356887",
    "服务／慈善": "#b0823d",
    "行政／国际协作": "#4e8a63",
    "公共外交／资助": "#9b5b4d",
    "其他观察节点": "#7d858d",
}

CLASS_FAMILY = {
    "local_civic_actor": "本地公民行动",
    "citizen_group": "本地公民行动",
    "citizen_network": "本地公民行动",
    "executive_committee": "本地公民行动",
    "domestic_japan_ngo": "环保／国际倡议",
    "international_ngo": "环保／国际倡议",
    "international_advocacy_actor": "环保／国际倡议",
    "media_or_advocacy_actor": "环保／国际倡议",
    "lawyers_network": "法律／制度渠道",
    "base_community_service_actor": "服务／慈善",
    "base_spouse_club": "服务／慈善",
    "base_spouse_charity_network": "服务／慈善",
    "local_international_cooperation_ngo": "行政／国际协作",
    "public_institution_partner": "行政／国际协作",
    "public_diplomacy_or_exchange_actor": "公共外交／资助",
    "public_diplomacy_grant_program": "公共外交／资助",
    "funder_or_intermediary": "公共外交／资助",
    "corporate_sponsor": "公共外交／资助",
    "local_business_sponsor": "公共外交／资助",
}

ORIGIN_ORDER = [
    "okinawa_local", "japan_domestic", "mixed_or_network",
    "international", "us_origin", "public_institution", "corporate",
]
ORIGIN_CN = {
    "okinawa_local": "冲绳本地", "japan_domestic": "日本国内",
    "mixed_or_network": "混合／网络", "international": "国际",
    "us_origin": "美国来源", "public_institution": "公共机构",
    "corporate": "企业",
}


def configure_fonts() -> None:
    candidates = [
        "Microsoft YaHei", "Yu Gothic", "Meiryo", "Noto Sans CJK SC",
        "Noto Sans CJK JP", "SimHei", "Arial Unicode MS", "DejaVu Sans",
    ]
    available = {font.name for font in font_manager.fontManager.ttflist}
    for name in candidates:
        if name in available:
            plt.rcParams["font.family"] = name
            break
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["figure.facecolor"] = "white"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def short(value: str, width: int = 19) -> str:
    return value if len(value) <= width else value[: width - 1] + "…"


def save_function_ecology(actors: list[dict[str, str]]) -> None:
    family_order = list(FAMILY_COLORS)
    cells: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for actor in actors:
        family = CLASS_FAMILY.get(actor["actor_class"], "其他观察节点")
        cells[(family, actor["origin_type"])].append(actor)

    rows: list[dict[str, object]] = []
    for family in family_order:
        for origin in ORIGIN_ORDER:
            items = cells[(family, origin)]
            ev = Counter(a["evidence_level"] for a in items)
            rows.append({
                "functional_family": family,
                "origin_type": origin,
                "actor_count": len(items),
                "E2": ev["E2"], "E3": ev["E3"], "E4": ev["E4"],
                "actor_ids": ";".join(a["actor_id"] for a in items),
                "actor_names": ";".join(a["canonical_name"] for a in items),
            })
    write_csv(
        OUT / "functional_ecology_matrix.csv", rows,
        ["functional_family", "origin_type", "actor_count", "E2", "E3", "E4", "actor_ids", "actor_names"],
    )

    fig, ax = plt.subplots(figsize=(13.8, 7.8))
    for yi, family in enumerate(family_order):
        for xi, origin in enumerate(ORIGIN_ORDER):
            items = cells[(family, origin)]
            if not items:
                continue
            ev = Counter(a["evidence_level"] for a in items)
            strong_share = (ev["E3"] + ev["E4"]) / len(items)
            size = 80 + 72 * len(items)
            ax.scatter(
                xi, yi, s=size, color=FAMILY_COLORS[family],
                alpha=0.35 + 0.55 * strong_share, edgecolor="#26343c", linewidth=0.7,
            )
            ax.text(xi, yi, str(len(items)), ha="center", va="center", fontsize=9,
                    color="white" if strong_share > 0.55 else "#1d2a31", fontweight="bold")

    ax.set_xticks(range(len(ORIGIN_ORDER)), [ORIGIN_CN[x] for x in ORIGIN_ORDER], fontsize=10)
    ax.set_yticks(range(len(family_order)), family_order, fontsize=10)
    ax.invert_yaxis()
    ax.set_xlim(-0.65, len(ORIGIN_ORDER) - 0.35)
    ax.set_ylim(len(family_order) - 0.35, -0.65)
    ax.grid(color="#dfe5e8", linewidth=0.8)
    ax.set_axisbelow(True)
    ax.set_title("一期组织功能生态：功能层 × 来源层", fontsize=17, loc="left", pad=22, fontweight="bold")
    ax.text(
        0, 1.035,
        "气泡面积＝registry 中 actor 数；透明度越低表示 E2 占比越高。分类按观察到的功能，不代表政治立场。",
        transform=ax.transAxes, fontsize=10, color="#52616b",
    )
    ax.text(
        0, -0.12,
        "证据边界：这是当前公开资料驱动样本的构成，不是复归后冲绳全部 NGO 的总体分布；军属服务／慈善节点按功能单列。",
        transform=ax.transAxes, fontsize=9.5, color="#66747d",
    )
    for spine in ax.spines.values():
        spine.set_visible(False)
    fig.subplots_adjust(left=0.18, right=0.98, top=0.84, bottom=0.16)
    fig.savefig(OUT / "fig1_functional_ecology.png", dpi=220)
    plt.close(fig)


def select_actor_place_rows(
    actors: list[dict[str, str]], place_edges: list[dict[str, str]], places: list[str], limit: int = 24,
) -> tuple[list[str], dict[tuple[str, str], str]]:
    actors_by_id = {a["actor_id"]: a for a in actors}
    edge_ev: dict[tuple[str, str], str] = {}
    rank = {"E2": 2, "E3": 3, "E4": 4}
    for edge in place_edges:
        if edge["place_name"] not in places or edge["evidence_level"] not in rank:
            continue
        key = (edge["actor_id"], edge["place_name"])
        if rank[edge["evidence_level"]] > rank.get(edge_ev.get(key, ""), 0):
            edge_ev[key] = edge["evidence_level"]

    by_actor: dict[str, set[str]] = defaultdict(set)
    for actor_id, place in edge_ev:
        if actor_id in actors_by_id:
            by_actor[actor_id].add(place)

    selected: list[str] = []
    # First guarantee that each place with data has a visible representative.
    for place in places:
        candidates = [aid for aid, ps in by_actor.items() if place in ps]
        candidates.sort(key=lambda aid: (-len(by_actor[aid]), -rank[edge_ev[(aid, place)]], aid))
        if candidates and candidates[0] not in selected:
            selected.append(candidates[0])
    ranked = sorted(
        by_actor,
        key=lambda aid: (-len(by_actor[aid]), -sum(rank[edge_ev[(aid, p)]] for p in by_actor[aid]), aid),
    )
    for aid in ranked:
        if aid not in selected:
            selected.append(aid)
        if len(selected) >= limit:
            break
    selected.sort(key=lambda aid: (-len(by_actor[aid]), actors_by_id[aid]["origin_type"], aid))
    return selected, edge_ev


def save_actor_place_matrix(actors: list[dict[str, str]], place_edges: list[dict[str, str]]) -> None:
    places = [
        "Henoko", "Oura Bay", "Nago", "Takae", "Kadena", "Futenma", "Ginowan",
        "Ishigaki", "Miyako", "Yonaguni", "Camp Foster", "JICA Okinawa",
    ]
    selected, edge_ev = select_actor_place_rows(actors, place_edges, places)
    amap = {a["actor_id"]: a for a in actors}
    values = np.zeros((len(selected), len(places)), dtype=int)
    output_rows: list[dict[str, object]] = []
    for yi, aid in enumerate(selected):
        for xi, place in enumerate(places):
            ev = edge_ev.get((aid, place), "")
            values[yi, xi] = {"": 0, "E2": 2, "E3": 3, "E4": 4}[ev]
            if ev:
                output_rows.append({
                    "actor_id": aid, "canonical_name": amap[aid]["canonical_name"],
                    "functional_family": CLASS_FAMILY.get(amap[aid]["actor_class"], "其他观察节点"),
                    "origin_type": amap[aid]["origin_type"], "place": place,
                    "evidence_level": ev, "candidate_edge": "yes",
                })
    write_csv(
        OUT / "actor_place_matrix_selected.csv", output_rows,
        ["actor_id", "canonical_name", "functional_family", "origin_type", "place", "evidence_level", "candidate_edge"],
    )

    fig_h = max(8.5, 0.37 * len(selected) + 2.1)
    fig, ax = plt.subplots(figsize=(14.5, fig_h))
    for yi, aid in enumerate(selected):
        for xi, place in enumerate(places):
            ev = edge_ev.get((aid, place), "")
            if ev:
                ax.scatter(xi, yi, s={"E2": 58, "E3": 82, "E4": 108}[ev],
                           color=EVIDENCE[ev], edgecolor="white", linewidth=0.8)
    labels = [f"{aid}  {short(amap[aid]['canonical_name'])}" for aid in selected]
    ax.set_xticks(range(len(places)), places, rotation=35, ha="right", fontsize=9.5)
    ax.set_yticks(range(len(selected)), labels, fontsize=8.5)
    ax.invert_yaxis()
    ax.set_xlim(-0.55, len(places) - 0.45)
    ax.set_ylim(len(selected) - 0.4, -0.6)
    ax.grid(color="#e2e7ea", linewidth=0.8)
    ax.set_axisbelow(True)
    ax.set_title("组织—地点矩阵：哪些组织在多个关键场域公开出现", fontsize=17, loc="left", pad=22, fontweight="bold")
    ax.text(
        0, 1.015,
        "展示关键地点至少一个代表 actor，并优先保留跨地点 actor；圆点颜色／大小＝候选地点边证据等级。",
        transform=ax.transAxes, fontsize=10, color="#52616b",
    )
    legend = [Line2D([0], [0], marker="o", linestyle="", markersize=8 + 2 * i,
                     markerfacecolor=EVIDENCE[ev], markeredgecolor="white", label=ev)
              for i, ev in enumerate(["E2", "E3", "E4"])]
    ax.legend(handles=legend, title="证据等级", loc="lower right", frameon=False)
    ax.text(
        0, -0.105,
        "证据边界：圆点表示公开材料支持的 actor–place 候选关系，不代表组织常设驻点、行动强度或稳定联盟。与那国按前线／自治／生命安全语境解释。",
        transform=ax.transAxes, fontsize=9.3, color="#66747d",
    )
    for spine in ax.spines.values():
        spine.set_visible(False)
    fig.subplots_adjust(left=0.31, right=0.98, top=0.88, bottom=0.16)
    fig.savefig(OUT / "fig2_actor_place_matrix.png", dpi=220)
    plt.close(fig)


def support_layer(row: dict[str, str]) -> str | None:
    confidence = row["funding_relation_confidence"]
    relation = row["relation_type"]
    if row["evidence_level"] not in {"E3", "E4"}:
        return None
    if confidence in {"no_public_evidence", "probable_funding", "suspected_lead", "not_supported"}:
        return None
    if confidence in {"confirmed_grant", "confirmed_in_kind_donation"}:
        return "grant／donation"
    if confidence == "confirmed_sponsorship" or relation in {"sponsorship", "funding_contribution"}:
        return "sponsorship"
    if confidence in {"confirmed_commission", "confirmed_designated_role"}:
        return "commission／designated role"
    if confidence == "confirmed_service_role":
        return "service／site presence"
    if confidence in {"confirmed_collaboration", "not_funding_relation"}:
        return "non-funding relation"
    return None


def save_support_layers(
    actors: list[dict[str, str]], places_rows: list[dict[str, str]], funding: list[dict[str, str]],
) -> None:
    labels = {a["actor_id"]: a["canonical_name"] for a in actors}
    labels.update({p["place_id"]: p["place_name"] for p in places_rows})
    manual = {
        "MOFA_ngo_consultant_program": "外务省 NGO 相談員制度",
        "Okinawa_Pref_multicultural_project": "冲绳县多文化共生项目",
        "Okinawa_City": "冲绳市",
        "R_yomitan_quegoen": "读谷 Quegoen",
        "R_uruma_social_welfare": "宇流麻社会福祉",
        "R_boy_scouts_far_east": "Boy Scouts Far East",
        "unknown_recipient": "recipient 未确认",
        "unknown_okinawa_welfare_facilities": "冲绳福利设施（未列名）",
        "Mediatti_Broadband_MBC": "Mediatti Broadband",
        "Matson": "Matson",
    }
    labels.update(manual)
    layer_order = [
        "grant／donation", "sponsorship", "commission／designated role",
        "service／site presence", "non-funding relation",
    ]
    kept: list[dict[str, object]] = []
    for row in funding:
        layer = support_layer(row)
        if not layer:
            continue
        kept.append({
            **row, "analytic_layer": layer,
            "source_label": labels.get(row["source_actor_id"], row["source_actor_id"]),
            "target_label": labels.get(row["target_actor_id"], row["target_actor_id"]),
        })
    kept.sort(key=lambda r: (layer_order.index(str(r["analytic_layer"])), str(r["edge_id"])))
    write_csv(
        OUT / "support_relations_strict_e3e4.csv", kept,
        ["edge_id", "analytic_layer", "source_actor_id", "source_label", "target_actor_id", "target_label",
         "relation_type", "event_or_program", "place", "evidence_level", "funding_relation_confidence",
         "source_ref", "review_status", "needs_local_retrieval", "notes"],
    )

    counts = Counter((str(r["analytic_layer"]), str(r["evidence_level"])) for r in kept)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15.5, 9.2), gridspec_kw={"width_ratios": [0.75, 1.65]})
    y = np.arange(len(layer_order))
    left = np.zeros(len(layer_order))
    for ev in ["E4", "E3"]:
        vals = np.array([counts[(layer, ev)] for layer in layer_order])
        ax1.barh(y, vals, left=left, color=EVIDENCE[ev], label=ev, height=0.58)
        for yi, (start, val) in enumerate(zip(left, vals)):
            if val:
                ax1.text(start + val / 2, yi, str(int(val)), ha="center", va="center", color="white", fontsize=9, fontweight="bold")
        left += vals
    ax1.set_yticks(y, layer_order, fontsize=9.5)
    ax1.invert_yaxis()
    ax1.set_xlabel("严格纳入的样本关系数")
    ax1.grid(axis="x", color="#e1e6e9")
    ax1.legend(frameon=False, loc="lower right")
    ax1.set_title("关系层构成", fontsize=13, loc="left", fontweight="bold")

    ax2.set_xlim(0, 1)
    ax2.set_ylim(len(kept) + 0.8, -1.2)
    current_layer = None
    row_y = 0
    for row in kept:
        layer = str(row["analytic_layer"])
        if layer != current_layer:
            ax2.text(0.01, row_y, layer, fontsize=9.5, fontweight="bold", color="#33434c", va="center")
            current_layer = layer
            row_y += 0.75
        source = short(str(row["source_label"]), 20)
        target = short(str(row["target_label"]), 22)
        ev = str(row["evidence_level"])
        ax2.text(0.02, row_y, str(row["edge_id"]), fontsize=7.8, color="#73808a", va="center")
        ax2.text(0.105, row_y, source, fontsize=8.2, va="center")
        ax2.annotate("", xy=(0.73, row_y), xytext=(0.43, row_y),
                     arrowprops={"arrowstyle": "-|>", "lw": 1.1, "color": EVIDENCE[ev], "alpha": 0.85})
        ax2.text(0.77, row_y, target, fontsize=8.2, va="center")
        ax2.text(0.99, row_y, ev, fontsize=7.8, color=EVIDENCE[ev], va="center", ha="right", fontweight="bold")
        row_y += 0.72
    ax2.set_ylim(row_y + 0.2, -1.0)
    ax2.axis("off")
    ax2.set_title("逐条可复核关系（来源 → 对象）", fontsize=13, loc="left", fontweight="bold")

    fig.suptitle("支持、委托与服务关系：严格 E3／E4 分层", fontsize=17, x=0.035, ha="left", fontweight="bold")
    fig.text(
        0.035, 0.935,
        "仅纳入 confirmed 类或明确 not_funding_relation；排除 probable funding、NOFO／grant opportunity 与 E2 线索。",
        fontsize=10, color="#52616b",
    )
    fig.text(
        0.035, 0.035,
        f"证据边界：这是 {len(funding)} 条 support/funding 样本边中的严格子集，不是完整资金流。non-funding 单列，不能把协作、成员关系或服务在场写成资助。金额与年度不完整时不作金额比较。",
        fontsize=9.3, color="#66747d",
    )
    for ax in (ax1, ax2):
        for spine in ax.spines.values():
            spine.set_visible(False)
    fig.subplots_adjust(left=0.15, right=0.985, top=0.87, bottom=0.1, wspace=0.22)
    fig.savefig(OUT / "fig3_support_service_layers_strict.png", dpi=220)
    plt.close(fig)


def write_audit() -> None:
    rows = [
        ("R1", "组织分类与组织生态", "仅有早期 actor class 计数图", "缺功能层与来源层的交叉解释", "fig1_functional_ecology.png", "已补", "报告第3节"),
        ("R2", "组织—议题网络", "bridge network + shortlist", "只显示桥接 actor，非完整网络；E2 需保留边界", "保留现图；完整网络待报告按需", "基本覆盖", "报告第4节"),
        ("R3", "地点与空间分布", "地点—议题矩阵", "缺 actor 直接对应关键地点", "fig2_actor_place_matrix.png", "已补", "报告第5节"),
        ("R4", "环保／生活安全与军事设施", "地点—议题矩阵", "现图已能显示场域差异；与那国需避免环保化", "保留现图", "基本覆盖", "报告第5节"),
        ("R5", "共同行动网络", "样本构成 + event repertoire 时间线", "尚不足以证明稳定联盟；重复参与很少", "保留事件感知时间线，不补静态联盟图", "基本覆盖", "报告第6节"),
        ("R6", "跨国／国际倡议", "Henoko internationalization pathway", "当前集中边野古／大浦湾，其他国际路径较薄", "保留现图；当地或后续源补足后再扩", "基本覆盖", "报告第4/6节"),
        ("R7", "场域与对象转移", "路径图提供单案例", "缺跨事件、跨制度场域的可比时间数据", "暂不作图，先补 event/venue 字段", "数据不足", "二期／报告局限"),
        ("R8", "法律／政策／环境程序", "路径图 + lawsuit role table", "缺多案件／程序的统一事件表", "暂不重复作图；先扩法律事件", "部分覆盖", "报告第6节"),
        ("R9", "选举／公投连接", "event repertoire 含公投", "只有发起组织，非完整参与网络", "保留时间线，避免把单节点当全体", "部分覆盖", "报告第5/6节"),
        ("R10", "公开资源／行政协作", "support/funding 样本早期计数", "资金、委托、服务、非资金关系曾混在一起", "fig3_support_service_layers_strict.png", "已补", "报告第7节"),
        ("R11", "外来 NGO 与国际倡议", "Henoko pathway + event layer", "军属服务与倡议层需明确分开", "fig1 + fig3 共同呈现功能分层", "已补边界", "报告第6/7节"),
        ("R12", "媒体可见度", "无", "一期已排除，且需要报刊数据库", "不作图", "扩展模块", "报告局限"),
        ("R13", "人物—组织互锁", "无", "人物字段与人工复核不足", "不作图", "扩展模块", "报告局限"),
        ("R14", "覆盖／证据偏差", "evidence gap map + coverage brief", "现有图偏状态计数，未比较功能层可见度", "fig1 透明度补充功能层证据差异", "基本覆盖", "报告第8节"),
    ]
    write_csv(
        OUT / "visualization_audit.csv",
        [dict(zip(["module", "research_question", "existing_figure", "gap", "recommendation_or_new_figure", "status", "report_section"], row)) for row in rows],
        ["module", "research_question", "existing_figure", "gap", "recommendation_or_new_figure", "status", "report_section"],
    )


README = r"""# 一期核心可视化补图包 v1

日期：2026-07-12

本包补足一期现有 `explanatory_v0` / `module_completion_v0` 尚未充分回答的三个问题。它不是对既有图的替换，也不把候选关系升级为最终发现。

## 图件

1. `fig1_functional_ecology.png` — 组织功能生态（功能层 × 来源层）。回答 registry 中不同功能 actor 如何构成，并把军属服务、行政协作和公共外交观察层与倡议网络分开。配套 `functional_ecology_matrix.csv`。
2. `fig2_actor_place_matrix.png` — 组织—地点矩阵。直接显示哪些组织在关键地点的公开资料中出现，证据等级由圆点颜色与大小标注。配套 `actor_place_matrix_selected.csv`。
3. `fig3_support_service_layers_strict.png` — 严格 E3/E4 的支持、委托与服务分层图。仅保留 confirmed 类或明确的 `not_funding_relation`，排除 probable funding、NOFO/grant opportunity、E2 线索。配套 `support_relations_strict_e3e4.csv`。

## 审计表

- `visualization_audit.csv`：研究模块 → 现有图 → 缺口 → 建议／补图 → 报告段落。

审计结论：现有地点—议题矩阵、边野古国际化路径、桥接 actor 图与事件 repertoire 时间线应保留；不应为了数量再画一张静态“联盟网络”。R7/R8/R9 的进一步网络图需要更多跨事件、法律程序和参与者数据后再做。

## 共同证据边界

- actor–place 与 actor–issue 均为候选边，不是最终关系。
- 共同署名、共同要请、共同在场不等于稳定联盟。
- 服务组织按观察到的服务／慈善功能编码，不推断亲基地或反基地立场。
- grant opportunity／NOFO 不等于 award；`probable_funding` 不进入严格图。
- 与那国按前线／安全环境、地方自治、公投、台湾邻近和生命安全解释，不强行环保化。
- 所有图描述当前公开资料驱动样本，不代表复归后冲绳全部 NGO 的总体分布。

## 复现

```powershell
python scripts\make_phase1_visuals.py
```
"""


def main() -> None:
    configure_fonts()
    OUT.mkdir(parents=True, exist_ok=True)
    actors = read_csv(DATA / "01_actor_registry_initial_v0.csv")
    place_edges = read_csv(DATA / "08_actor_place_edges_initial_v0.csv")
    places = read_csv(DATA / "04_place_registry_v0.csv")
    funding = read_csv(DATA / "15_funding_or_support_edges_sample_v0.csv")
    save_function_ecology(actors)
    save_actor_place_matrix(actors, place_edges)
    save_support_layers(actors, places, funding)
    write_audit()
    (OUT / "README.md").write_text(README, encoding="utf-8")
    print(f"Wrote Phase-1 visualization package to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
