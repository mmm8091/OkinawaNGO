from __future__ import annotations

"""Build the findings-led v2 figures for the third progress sync.

Unlike the audit-oriented v1 package, this package foregrounds comparative
mechanisms.  It only reuses reviewed/formal outputs or labels an inference as a
working hypothesis with a local-retrieval gate.
"""

import csv
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, Rectangle
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "formal_comm_v2"
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
BLUE_LIGHT = "#DCE8EE"
ORANGE = "#D48632"
ORANGE_LIGHT = "#F0D6AE"
GREEN = "#408C6A"
GREEN_LIGHT = "#DCEADF"
GRAY = "#A7ADB2"
LIGHT_GRAY = "#E8E7E2"
RUST = "#9A513C"
RUST_LIGHT = "#F2E4DF"
PURPLE = "#75629A"
PURPLE_LIGHT = "#E7E1EE"


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
    for name in ("Microsoft YaHei", "Noto Sans CJK SC", "SimHei", "DejaVu Sans"):
        if name in available:
            plt.rcParams["font.family"] = name
            break
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["figure.facecolor"] = BG
    plt.rcParams["axes.facecolor"] = BG
    FIG.mkdir(parents=True, exist_ok=True)
    DATA.mkdir(parents=True, exist_ok=True)


def rounded_box(
    fig: plt.Figure,
    x: float,
    y: float,
    w: float,
    h: float,
    face: str,
    edge: str = "none",
    radius: float = 0.014,
    linewidth: float = 1.0,
) -> FancyBboxPatch:
    box = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle=f"round,pad=0.008,rounding_size={radius}",
        transform=fig.transFigure,
        facecolor=face,
        edgecolor=edge,
        linewidth=linewidth,
    )
    fig.add_artist(box)
    return box


def title_block(fig: plt.Figure, title: str, subtitle: str) -> None:
    fig.text(0.055, 0.945, title, ha="left", va="top", fontsize=22.5, weight="bold", color=INK)
    fig.text(0.055, 0.893, subtitle, ha="left", va="top", fontsize=11.2, color=MUTED)


def save(fig: plt.Figure, filename: str) -> None:
    fig.savefig(FIG / filename, dpi=180, facecolor=BG, bbox_inches="tight", pad_inches=0.12)
    plt.close(fig)


def arrow(fig: plt.Figure, x1: float, x2: float, y: float, color: str = GRAY) -> None:
    ax = fig.add_axes([0, 0, 1, 1], frameon=False)
    ax.set_axis_off()
    ax.annotate(
        "",
        xy=(x2, y),
        xytext=(x1, y),
        xycoords=fig.transFigure,
        textcoords=fig.transFigure,
        arrowprops={"arrowstyle": "->", "color": color, "lw": 1.6},
    )


def figure_translation_mechanisms() -> None:
    episodes = {
        row["episode_id"]: row
        for row in read_csv(
            ROOT / "outputs" / "translation_episode_comparison_v1" / "translation_episode_candidates_v1.csv"
        )
    }
    for episode_id in ("TE01", "TE02", "TE03", "TE04", "TE05", "TE07", "TE09"):
        assert episode_id in episodes
    assert episodes["TE03"]["bounded_gain"] == "yes"
    assert episodes["TE04"]["bounded_gain"] == "yes"
    assert all(episodes[item]["underlying_change"] == "no" for item in ("TE01", "TE02", "TE03", "TE04", "TE05", "TE07", "TE09"))

    rows = [
        {
            "comparison_family": "海洋新建工程",
            "places": "边野古／大浦湾",
            "material_problem": "基地填海、儒艮与海洋生态",
            "translated_claim": "文化财义务／科学评价／县民意思",
            "venue": "美国法律、EIA、县民投票",
            "observable_output": "审查标准、正式意见、投票与通知",
            "hard_limit": "没有自动停止工程",
            "evidence_status": "正式证据",
            "episode_ids": "TE01;TE02;TE09",
        },
        {
            "comparison_family": "既有基地慢性损害",
            "places": "嘉手纳／普天间",
            "material_problem": "噪音、睡眠与日常生活损害",
            "translated_claim": "人格／期间损害与差止请求",
            "venue": "损害赔偿与差止诉讼",
            "observable_output": "违法／损害认定与部分赔偿",
            "hard_limit": "没有形成运营禁令",
            "evidence_status": "正式证据",
            "episode_ids": "TE03;TE04",
        },
        {
            "comparison_family": "新部署与前线化",
            "places": "石垣；宫古／与那国待地方补强",
            "material_problem": "部署、自治、地下水与撤离",
            "translated_claim": "谁来决定／生活条件／避难可行性",
            "venue": "议会、条例、公投、行政与司法",
            "observable_output": "签名、议程、投票、答复或诉讼记录",
            "hard_limit": "可能被阻断、改写或再解释",
            "evidence_status": "石垣正式；宫古／与那国为待检验比较",
            "episode_ids": "TE05;R4_SAKISHIMA",
        },
    ]
    write_csv(
        DATA / "fig1_translation_mechanisms_v2.csv",
        rows,
        list(rows[0].keys()),
    )

    fig = plt.figure(figsize=(13.33, 7.5))
    title_block(
        fig,
        "不同争议不是换一套口号，而是进入不同的制度语法",
        "同样围绕基地／部署，物质损害不同，可被组织转译和制度接收的方式也不同。",
    )

    headers = ["争议对象", "被转译为", "进入场域", "制度可见产出", "硬边界"]
    x_positions = [0.055, 0.24, 0.43, 0.62, 0.81]
    widths = [0.155, 0.16, 0.16, 0.16, 0.145]
    for x, w, header in zip(x_positions, widths, headers):
        rounded_box(fig, x, 0.79, w, 0.06, "#E9ECEE", edge="#B9C2C8")
        fig.text(x + w / 2, 0.82, header, ha="center", va="center", fontsize=10.5, weight="bold", color=INK)

    lane_specs = [
        (0.58, BLUE, BLUE_LIGHT),
        (0.365, TEAL, TEAL_LIGHT),
        (0.15, ORANGE, ORANGE_LIGHT),
    ]
    cell_fields = ["material_problem", "translated_claim", "venue", "observable_output", "hard_limit"]
    for row, (y, accent, light) in zip(rows, lane_specs):
        fig.text(0.035, y + 0.078, row["comparison_family"], ha="right", va="center", fontsize=11, weight="bold", color=accent)
        fig.text(0.035, y + 0.045, row["places"], ha="right", va="center", fontsize=8.2, color=MUTED)
        for index, (x, w, field) in enumerate(zip(x_positions, widths, cell_fields)):
            face = light if index < 4 else RUST_LIGHT
            edge = accent if index < 4 else "#D9B3A8"
            rounded_box(fig, x, y, w, 0.155, face, edge=edge, linewidth=1.1)
            fig.text(
                x + w / 2,
                y + 0.078,
                row[field].replace("／", "／\n") if field in {"material_problem", "translated_claim"} else row[field],
                ha="center",
                va="center",
                fontsize=9.2,
                color=TEXT if index < 4 else RUST,
                weight="bold" if index in {0, 4} else "normal",
            )
            if index < 4:
                arrow(fig, x + w + 0.006, x_positions[index + 1] - 0.006, y + 0.078, accent)

    rounded_box(fig, 0.055, 0.055, 0.89, 0.062, "#EFEEE9")
    fig.text(
        0.075,
        0.086,
        "解释：组织的作用不只是“反对”，而是把地方损害改写为某个制度能够受理的科学、损害、自治或程序主张。",
        fontsize=10.2,
        color=INK,
        weight="bold",
        va="center",
    )
    fig.text(
        0.055,
        0.025,
        "边界：这是跨案例机制比较；第三行中的宫古／与那国差异仍需当地组织原始材料检验，不是已完成的因果规律。",
        fontsize=8.9,
        color=RUST,
    )
    save(fig, "fig1_translation_mechanisms_v2.png")


def figure_institutional_conversion() -> None:
    episodes = {
        row["episode_id"]: row
        for row in read_csv(
            ROOT / "outputs" / "translation_episode_comparison_v1" / "translation_episode_candidates_v1.csv"
        )
    }
    selected_ids = ["TE01", "TE02", "TE03", "TE04", "TE05", "TE06", "TE07", "TE09"]
    selected = [episodes[item] for item in selected_ids]
    assert sum(row["venue_entry"] == "yes" for row in selected) == 8
    assert sum(row["intermediate_output"] == "yes" for row in selected) == 8
    assert sum(row["bounded_gain"] == "yes" for row in selected) == 4
    assert sum(row["bounded_gain"] == "mixed" for row in selected) == 1
    assert sum(row["underlying_change"] == "yes" for row in selected) == 0

    rows = [
        {
            "channel": "生态／国际程序",
            "case_count": 2,
            "input_claim": "儒艮、文化财与环境评价",
            "institutional_conversion": "可审查标准、科学意见与公开记录",
            "bounded_result": "程序信息增加",
            "unresolved": "工程未因此停止",
            "episode_ids": "TE01;TE02",
        },
        {
            "channel": "噪音民事诉讼",
            "case_count": 2,
            "input_claim": "睡眠、健康与生活损害",
            "institutional_conversion": "期间损害认定与赔偿",
            "bounded_result": "部分原告／期间获赔",
            "unresolved": "没有运营禁令",
            "episode_ids": "TE03;TE04",
        },
        {
            "channel": "公投／地方自治",
            "case_count": 3,
            "input_claim": "居民决定权与直接请求",
            "institutional_conversion": "条例、投票、通知或可诉性判断",
            "bounded_result": "民意或门槛被正式记录",
            "unresolved": "不自动拘束行政决定",
            "episode_ids": "TE05;TE07;TE09",
        },
        {
            "channel": "公金支出诉讼",
            "case_count": 1,
            "input_claim": "生态、经济与支出合理性",
            "institutional_conversion": "公共支出合法性审查",
            "bounded_result": "第一波限制支出",
            "unresolved": "第二波居民败诉，结果混合",
            "episode_ids": "TE06",
        },
    ]
    write_csv(DATA / "fig2_institutional_conversion_v2.csv", rows, list(rows[0].keys()))

    fig = plt.figure(figsize=(13.33, 7.5))
    title_block(
        fig,
        "制度不是简单回答“同意／不同意”，而是把诉求转换成有限结果",
        "八个正式证据案例显示，不同渠道会留下不同类型的收益与边界；“进入制度”不能用一个胜负概括。",
    )

    x_positions = [0.055, 0.25, 0.48, 0.705]
    widths = [0.165, 0.20, 0.195, 0.24]
    headers = ["制度渠道", "地方诉求如何进入", "制度把它转换成什么", "获得了什么／没有什么"]
    for x, w, header in zip(x_positions, widths, headers):
        rounded_box(fig, x, 0.79, w, 0.06, "#E9ECEE", edge="#B9C2C8")
        fig.text(x + w / 2, 0.82, header, ha="center", va="center", fontsize=10.2, weight="bold", color=INK)

    lane_y = [0.625, 0.465, 0.305, 0.145]
    lane_colors = [BLUE, TEAL, PURPLE, ORANGE]
    lane_lights = [BLUE_LIGHT, TEAL_LIGHT, PURPLE_LIGHT, ORANGE_LIGHT]
    for row, y, accent, light in zip(rows, lane_y, lane_colors, lane_lights):
        contents = [
            f"{row['channel']}\n（{row['case_count']}案）",
            row["input_claim"],
            row["institutional_conversion"],
            f"获得：{row['bounded_result']}\n未获：{row['unresolved']}",
        ]
        for index, (x, w, content) in enumerate(zip(x_positions, widths, contents)):
            face = light if index < 3 else "#EFEEE9"
            rounded_box(fig, x, y, w, 0.115, face, edge=accent if index < 3 else "#C7C7C3")
            fig.text(
                x + w / 2,
                y + 0.058,
                content,
                ha="center",
                va="center",
                fontsize=8.9 if index else 9.5,
                color=TEXT,
                weight="bold" if index in {0, 3} else "normal",
            )
            if index < 3:
                arrow(fig, x + w + 0.006, x_positions[index + 1] - 0.006, y + 0.058, accent)

    rounded_box(fig, 0.055, 0.052, 0.89, 0.064, RUST_LIGHT, edge="#D9B3A8")
    fig.text(
        0.075,
        0.084,
        "共同机制：制度承认、记录或补偿某一部分诉求，同时把运行停止、工程否决或行政拘束留在门外。",
        fontsize=10.2,
        weight="bold",
        color=RUST,
        va="center",
    )
    fig.text(0.055, 0.022, "边界：8案是已进入场域的目的性案例，不是所有行动的总体成功率，也不是因果估计。", fontsize=8.9, color=MUTED)
    save(fig, "fig2_institutional_conversion_v2.png")


def figure_referendum_gates() -> None:
    cases = {
        row["case_id"]: row
        for row in read_csv(ROOT / "outputs" / "R09_referendum_process_v0" / "case_summary_v0.csv")
    }
    expected_ids = {
        "R9C_NAGO_1997",
        "R9C_YONAGUNI_2015",
        "R9C_PREF_2019",
        "R9C_ISHIGAKI_2018_2024",
    }
    assert set(cases) == expected_ids
    assert "17,539" in cases["R9C_NAGO_1997"]["institutional_entry"]
    assert "92,848" in cases["R9C_PREF_2019"]["institutional_entry"]
    assert "14,263" in cases["R9C_ISHIGAKI_2018_2024"]["institutional_entry"]

    rows = [
        {
            "case": "名护 1997",
            "entry": "17,539 份\n有效签名",
            "ordinance": "议会改为\n四选项条例",
            "vote_or_court": "举行投票",
            "formal_result": "反对 16,639\n赞成 14,267",
            "after": "市长接受基地\n并辞职",
            "status_pattern": "pass;redesign;pass;pass;reinterpret",
        },
        {
            "case": "与那国 2015",
            "entry": "自治体\n个别条例路径",
            "ordinance": "条例修正",
            "vote_or_court": "举行投票",
            "formal_result": "正式结果表\n待当地取得",
            "after": "町长解释为\n推进依据",
            "status_pattern": "pass;redesign;pass;local_gap;reinterpret",
        },
        {
            "case": "县民投票 2019",
            "entry": "92,848 份\n有效签名",
            "ordinance": "条例加入\n第三选项",
            "vote_or_court": "全 41 市町村\n举行投票",
            "formal_result": "反对 434,273\n（71.7%）",
            "after": "知事通知日美\n工程未自动停止",
            "status_pattern": "pass;redesign;pass;pass;reinterpret",
        },
        {
            "case": "石垣 2018–2024",
            "entry": "14,263 份\n有效签名",
            "ordinance": "条例案\n两次被否决",
            "vote_or_court": "未投票；\n转入两条诉讼",
            "formal_result": "义务付诉讼\n程序性却下",
            "after": "公投条款删除；\n后续败诉",
            "status_pattern": "pass;blocked;blocked;blocked;blocked",
        },
    ]
    write_csv(DATA / "fig3_referendum_gates_v2.csv", rows, list(rows[0].keys()))

    fig = plt.figure(figsize=(13.33, 7.5))
    title_block(
        fig,
        "签名达标不保证投票，投票结果也不自动约束行政",
        "四个案例显示，自治诉求会被条例设计、议会否决、司法可诉性和行政解释逐层转换。",
    )

    headers = ["请求／入口", "条例／议会", "投票／司法", "正式结果", "后续行政／解释"]
    x_positions = [0.19, 0.35, 0.51, 0.67, 0.83]
    cell_w = 0.13
    for x, header in zip(x_positions, headers):
        rounded_box(fig, x, 0.79, cell_w, 0.06, "#E9ECEE", edge="#B9C2C8")
        fig.text(x + cell_w / 2, 0.82, header, ha="center", va="center", fontsize=9.6, weight="bold", color=INK)

    colors = {
        "pass": (GREEN_LIGHT, GREEN),
        "redesign": (ORANGE_LIGHT, ORANGE),
        "blocked": (RUST_LIGHT, RUST),
        "reinterpret": (PURPLE_LIGHT, PURPLE),
        "local_gap": (LIGHT_GRAY, GRAY),
    }
    y_positions = [0.635, 0.48, 0.325, 0.17]
    fields = ["entry", "ordinance", "vote_or_court", "formal_result", "after"]
    for row, y in zip(rows, y_positions):
        fig.text(0.165, y + 0.057, row["case"], ha="right", va="center", fontsize=10.5, weight="bold", color=INK)
        statuses = row["status_pattern"].split(";")
        for index, (x, field, status) in enumerate(zip(x_positions, fields, statuses)):
            face, accent = colors[status]
            rounded_box(fig, x, y, cell_w, 0.112, face, edge=accent, linewidth=1.1)
            fig.text(x + cell_w / 2, y + 0.056, row[field], ha="center", va="center", fontsize=8.4, color=TEXT, weight="bold" if status in {"blocked", "local_gap"} else "normal")
            if index < 4:
                arrow(fig, x + cell_w + 0.006, x_positions[index + 1] - 0.006, y + 0.056, accent)

    legend = [("放行", "pass"), ("重新设计", "redesign"), ("阻断", "blocked"), ("结果转化／再解释", "reinterpret"), ("当地材料缺口", "local_gap")]
    lx = 0.19
    for label, status in legend:
        face, accent = colors[status]
        fig.add_artist(Rectangle((lx, 0.09), 0.015, 0.015, transform=fig.transFigure, facecolor=face, edgecolor=accent, linewidth=1))
        fig.text(lx + 0.021, 0.098, label, fontsize=8.2, color=MUTED, va="center")
        lx += 0.135
    fig.text(
        0.055,
        0.035,
        "解释：公投不是一个“民意输入→政策输出”的单点，而是一条可能被改写、阻断或再解释的制度门槛链。",
        fontsize=10.1,
        color=INK,
        weight="bold",
    )
    save(fig, "fig3_referendum_gates_v2.png")


def figure_sakishima_hypothesis() -> None:
    safe = read_csv(
        ROOT / "outputs" / "R04_sakishima_frame_corpus_v0" / "three_place_safe_source_matrix_v0.csv"
    )
    lookup = {(row["place"], row["frame_label"]): int(row["safe_source_count"]) for row in safe}
    assert lookup[("Miyako", "groundwater_life_safety")] == 2
    assert lookup[("Ishigaki", "local_autonomy_referendum")] == 3
    assert lookup[("Yonaguni", "frontline_taiwan_evacuation")] == 6

    rows = [
        {
            "place": "宫古",
            "dominant_frame": "地下水／饮用水",
            "safe_excerpt_count": 2,
            "mechanism_hypothesis": "地下水依赖使部署争议\n落到水源与生活条件",
            "current_bias": "官方／议会材料多；\n组织原始陈情不足",
            "local_need": "A012／A013／A112 的\n陈情、会报、集会资料",
        },
        {
            "place": "石垣",
            "dominant_frame": "自治／公投",
            "safe_excerpt_count": 3,
            "mechanism_hypothesis": "部署争议被组织成\n“谁有权决定”的自治问题",
            "current_bias": "制度链强；\n运动方沿革与刊物不足",
            "local_need": "A010／A011 的传单、会报、\n请求书与历次公投材料",
        },
        {
            "place": "与那国",
            "dominant_frame": "前线／台湾邻近／撤离",
            "safe_excerpt_count": 6,
            "mechanism_hypothesis": "台湾邻近使争议进入\n监视、撤离与生活恢复",
            "current_bias": "政府／防卫叙事占主导；\n民间组织材料最薄",
            "local_need": "A014／A015／A016 的\n广告、请求书、会议记录",
        },
    ]
    write_csv(DATA / "fig4_sakishima_hypothesis_v2.csv", rows, list(rows[0].keys()))

    fig = plt.figure(figsize=(13.33, 7.5))
    title_block(
        fig,
        "先岛三地不是同一种“环保反部署”模式——但这个比较需要当地材料检验",
        "当前线上安全层提示三种地方问题化方式；数字只是本包可核摘录数，不代表现实动员强度。",
    )

    card_x = [0.055, 0.365, 0.675]
    accents = [BLUE, TEAL, ORANGE]
    lights = [BLUE_LIGHT, TEAL_LIGHT, ORANGE_LIGHT]
    for row, x, accent, light in zip(rows, card_x, accents, lights):
        rounded_box(fig, x, 0.18, 0.27, 0.61, "#EFEEE9", edge="#D2D1CC")
        rounded_box(fig, x + 0.018, 0.69, 0.234, 0.072, light, edge=accent)
        fig.text(x + 0.04, 0.726, row["place"], fontsize=18, weight="bold", color=accent, va="center")
        fig.text(x + 0.125, 0.726, row["dominant_frame"], fontsize=10.2, weight="bold", color=TEXT, va="center")
        fig.text(x + 0.235, 0.726, f"{row['safe_excerpt_count']}条", fontsize=8.5, color=MUTED, va="center", ha="right")

        fig.text(x + 0.03, 0.63, "当前解释假设", fontsize=9, color=MUTED, weight="bold")
        fig.text(x + 0.03, 0.555, row["mechanism_hypothesis"], fontsize=12, color=INK, weight="bold", va="center")
        fig.add_artist(Rectangle((x + 0.03, 0.48), 0.21, 0.003, transform=fig.transFigure, facecolor=GRID, edgecolor="none"))
        fig.text(x + 0.03, 0.44, "当前证据偏差", fontsize=9, color=MUTED, weight="bold")
        fig.text(x + 0.03, 0.375, row["current_bias"], fontsize=9.6, color=TEXT, va="center")
        fig.add_artist(Rectangle((x + 0.03, 0.31), 0.21, 0.003, transform=fig.transFigure, facecolor=GRID, edgecolor="none"))
        fig.text(x + 0.03, 0.275, "当地协作者要找", fontsize=9, color=RUST, weight="bold")
        fig.text(x + 0.03, 0.22, row["local_need"], fontsize=9.3, color=TEXT, va="center")

    rounded_box(fig, 0.055, 0.075, 0.89, 0.062, RUST_LIGHT, edge="#D9B3A8")
    fig.text(
        0.075,
        0.106,
        "当地核查的价值：不是再找几篇新闻，而是检验“地下水—自治—前线化”差异究竟来自民间组织，还是来自线上行政材料偏差。",
        fontsize=10.1,
        color=RUST,
        weight="bold",
        va="center",
    )
    fig.text(0.055, 0.03, "边界：语料未出现不等于当地不存在相关议题；与那国尤其不能强行套用宫古的地下水框架。", fontsize=8.9, color=MUTED)
    save(fig, "fig4_sakishima_hypothesis_v2.png")


def figure_official_civic_ecology() -> None:
    stats = {
        row["metric_id"]: float(row["value"])
        for row in read_csv(
            ROOT / "outputs" / "R10_official_collaboration_universe_v1" / "descriptive_statistics_v1.csv"
        )
    }
    assert stats["M01"] == 616
    assert stats["M11"] == 469
    assert stats["M12"] == 76.1
    assert stats["M18"] == 443
    assert stats["M19"] == 71.9
    assert stats["M13"] == 19
    assert stats["M14"] == 3.1

    mechanisms = read_csv(
        ROOT / "outputs" / "R10_official_collaboration_universe_v1" / "official_resource_type_summary_v1.csv"
    )
    mechanism_lookup = {row["official_mechanism_label"]: int(row["source_row_count"]) for row in mechanisms}
    departments = read_csv(
        ROOT / "outputs" / "R10_official_collaboration_universe_v1" / "department_resource_summary_v1.csv"
    )
    top = departments[:5]
    assert sum(int(row["source_row_count"]) for row in top) == 443

    export = [
        {"metric": "official_source_rows", "value": 616, "unit": "rows"},
        {"metric": "institutionalized_mechanism_rows", "value": 469, "unit": "rows"},
        {"metric": "institutionalized_mechanism_share", "value": 76.1, "unit": "percent"},
        {"metric": "top_five_service_department_rows", "value": 443, "unit": "rows"},
        {"metric": "top_five_service_department_share", "value": 71.9, "unit": "percent"},
        {"metric": "human_rights_peace_international_rows", "value": 19, "unit": "rows"},
        {"metric": "human_rights_peace_international_share", "value": 3.1, "unit": "percent"},
    ]
    write_csv(DATA / "fig5_official_civic_ecology_metrics_v2.csv", export, ["metric", "value", "unit"])

    fig = plt.figure(figsize=(13.33, 7.5))
    title_block(
        fig,
        "公开行政协作首先呈现公共服务体系，而不是一张统一的抗争网络",
        "FY2024 冲绳县《NPO等との協働実績調査》616条来源行提供了一个与一期争议样本不同的官方协作基线。",
    )

    ax1 = fig.add_axes([0.07, 0.22, 0.42, 0.55])
    mech_labels = ["委托", "提案型委托", "指定管理", "补助／物的支援", "其他协作"]
    mech_values = [
        mechanism_lookup["委託"],
        mechanism_lookup["提案型公募による委託"],
        mechanism_lookup["指定管理者制度による委任"],
        mechanism_lookup["補助"],
        616 - 469,
    ]
    mech_colors = [TEAL, TEAL_MID, BLUE, ORANGE, GRAY]
    y = np.arange(len(mech_labels))
    bars = ax1.barh(y, mech_values, color=mech_colors, height=0.58)
    ax1.set_yticks(y, labels=mech_labels, fontsize=9.8)
    ax1.invert_yaxis()
    ax1.set_xlim(0, 330)
    ax1.set_xticks([0, 100, 200, 300])
    ax1.grid(axis="x", color=GRID, linewidth=0.8)
    ax1.set_axisbelow(True)
    ax1.spines[["top", "right", "left"]].set_visible(False)
    ax1.tick_params(axis="y", length=0, colors=TEXT)
    ax1.tick_params(axis="x", colors=MUTED)
    ax1.set_title("官方协作机制构成", loc="left", fontsize=12.5, color=INK, weight="bold")
    for bar, value in zip(bars, mech_values):
        ax1.text(value + 5, bar.get_y() + bar.get_height() / 2, str(value), va="center", fontsize=10, weight="bold", color=TEXT)

    ax2 = fig.add_axes([0.57, 0.30, 0.36, 0.47])
    dept_labels = [row["department_display_machine"] for row in top][::-1]
    dept_values = [int(row["source_row_count"]) for row in top][::-1]
    y2 = np.arange(len(dept_labels))
    bars2 = ax2.barh(y2, dept_values, color=BLUE, height=0.58)
    ax2.set_yticks(y2, labels=dept_labels, fontsize=8.8)
    ax2.set_xlim(0, 130)
    ax2.set_xticks([0, 40, 80, 120])
    ax2.grid(axis="x", color=GRID, linewidth=0.8)
    ax2.set_axisbelow(True)
    ax2.spines[["top", "right", "left"]].set_visible(False)
    ax2.tick_params(axis="y", length=0, colors=TEXT)
    ax2.tick_params(axis="x", colors=MUTED)
    ax2.set_title("来源行最多的五个公共服务部门", loc="left", fontsize=12.5, color=INK, weight="bold")
    for bar, value in zip(bars2, dept_values):
        ax2.text(value + 2, bar.get_y() + bar.get_height() / 2, str(value), va="center", fontsize=9.5, weight="bold", color=TEXT)

    rounded_box(fig, 0.56, 0.17, 0.37, 0.075, "#E4ECEF")
    fig.text(0.585, 0.207, "前五部门 443 / 616（71.9%）", fontsize=13.2, color=BLUE, weight="bold", va="center")
    rounded_box(fig, 0.56, 0.07, 0.37, 0.075, RUST_LIGHT, edge="#D9B3A8")
    fig.text(0.585, 0.107, "人权／和平＋国际协作 19 / 616（3.1%）", fontsize=11.5, color=RUST, weight="bold", va="center")

    fig.text(0.07, 0.145, "委托／提案型委托／指定管理／补助或物的支援：469 / 616（76.1%）", fontsize=10.3, color=TEAL, weight="bold")
    fig.text(
        0.055,
        0.025,
        "边界：616是官方表的来源行，不是616个组织、合同或拨款；事业费也不等于向合作方支付的金额。",
        fontsize=8.9,
        color=MUTED,
    )
    save(fig, "fig5_official_civic_ecology_v2.png")


def figure_event_reassembly() -> None:
    events = {
        row["event_id"]: row
        for row in read_csv(ROOT / "outputs" / "R05_coaction_v1" / "event_catalog_v0.csv")
    }
    overlaps = read_csv(ROOT / "outputs" / "R05_coaction_v1" / "event_overlap_v0.csv")
    repeats = read_csv(ROOT / "outputs" / "R05_coaction_v1" / "repeat_participation_bridges_v0.csv")

    event_ids = ["EV2010_WWF_67", "EV2015_NACSJ_31", "EV2020_OEJP_MMC_71"]
    assert set(event_ids).issubset(events)
    assert sum(int(events[item]["structured_participant_count"]) for item in event_ids) == 169
    assert len(repeats) == 15
    assert sum(int(row["event_count"]) == 3 for row in repeats) == 3

    overlap_lookup = {
        (row["event_a"], row["event_b"]): int(row["shared_confirmed_registry_actors"])
        for row in overlaps
    }
    assert overlap_lookup[("EV2010_WWF_67", "EV2015_NACSJ_31")] == 10
    assert overlap_lookup[("EV2010_WWF_67", "EV2020_OEJP_MMC_71")] == 8
    assert overlap_lookup[("EV2015_NACSJ_31", "EV2020_OEJP_MMC_71")] == 3

    rows = [
        {
            "event": "2010 WWF 声明",
            "source_list_rows": 67,
            "confirmed_registry_rows": 16,
            "target_or_venue": "日本政府",
            "action": "共同声明",
        },
        {
            "event": "2015 NACSJ／Peace Boat 声明",
            "source_list_rows": 31,
            "confirmed_registry_rows": 31,
            "target_or_venue": "日本国内＋跨国 NGO",
            "action": "共同声明",
        },
        {
            "event": "2020 OEJP／MMC 请求",
            "source_list_rows": 71,
            "confirmed_registry_rows": 16,
            "target_or_venue": "美国海洋哺乳动物委员会",
            "action": "请求信／公民社会报告",
        },
    ]
    export = rows + [
        {"event": "2010↔2015", "source_list_rows": "", "confirmed_registry_rows": 10, "target_or_venue": "两事件重叠", "action": ""},
        {"event": "2010↔2020", "source_list_rows": "", "confirmed_registry_rows": 8, "target_or_venue": "两事件重叠", "action": ""},
        {"event": "2015↔2020", "source_list_rows": "", "confirmed_registry_rows": 3, "target_or_venue": "两事件重叠", "action": ""},
        {"event": "贯穿三次", "source_list_rows": "", "confirmed_registry_rows": 3, "target_or_venue": "重复骨架", "action": ""},
    ]
    write_csv(
        DATA / "fig6_event_reassembly_v2.csv",
        export,
        ["event", "source_list_rows", "confirmed_registry_rows", "target_or_venue", "action"],
    )

    fig = plt.figure(figsize=(13.33, 7.5))
    title_block(
        fig,
        "公开行动更像按议题重新组队，而不是固定联盟反复出场",
        "三次边野古／儒艮行动共169条名单观察；当前确认身份层有15个组织至少重复一次，只有3个贯穿三次。",
    )

    card_x = [0.055, 0.365, 0.675]
    accents = [BLUE, TEAL, ORANGE]
    lights = [BLUE_LIGHT, TEAL_LIGHT, ORANGE_LIGHT]
    for row, x, accent, light in zip(rows, card_x, accents, lights):
        rounded_box(fig, x, 0.48, 0.27, 0.29, "#EFEEE9", edge="#D2D1CC")
        rounded_box(fig, x + 0.018, 0.675, 0.234, 0.065, light, edge=accent)
        fig.text(x + 0.135, 0.708, row["event"], ha="center", va="center", fontsize=10.5, weight="bold", color=accent)
        fig.text(x + 0.055, 0.61, str(row["source_list_rows"]), ha="center", va="center", fontsize=26, weight="bold", color=INK)
        fig.text(x + 0.055, 0.565, "来源名单行", ha="center", va="center", fontsize=8.5, color=MUTED)
        fig.text(x + 0.195, 0.61, str(row["confirmed_registry_rows"]), ha="center", va="center", fontsize=26, weight="bold", color=accent)
        fig.text(x + 0.195, 0.565, "已确认 registry 行", ha="center", va="center", fontsize=8.5, color=MUTED)
        fig.text(x + 0.135, 0.515, f"{row['action']} → {row['target_or_venue']}", ha="center", va="center", fontsize=8.7, color=TEXT)

    overlap_specs = [
        (0.28, "2010 与 2015", 10, BLUE),
        (0.47, "2010 与 2020", 8, TEAL),
        (0.66, "2015 与 2020", 3, ORANGE),
    ]
    for x, label, value, accent in overlap_specs:
        rounded_box(fig, x, 0.355, 0.15, 0.075, "#E9ECEE", edge=accent)
        fig.text(x + 0.075, 0.404, label, ha="center", va="center", fontsize=8.4, color=MUTED)
        fig.text(x + 0.075, 0.374, f"重叠 {value} 个", ha="center", va="center", fontsize=11, color=accent, weight="bold")

    rounded_box(fig, 0.055, 0.155, 0.89, 0.145, "#EFEEE9", edge="#C7C7C3")
    rounded_box(fig, 0.075, 0.185, 0.17, 0.085, TEAL_LIGHT, edge=TEAL)
    fig.text(0.16, 0.239, "15 个", ha="center", va="center", fontsize=20, color=TEAL, weight="bold")
    fig.text(0.16, 0.207, "至少出现两次", ha="center", va="center", fontsize=8.7, color=MUTED)
    rounded_box(fig, 0.27, 0.185, 0.17, 0.085, PURPLE_LIGHT, edge=PURPLE)
    fig.text(0.355, 0.239, "3 个", ha="center", va="center", fontsize=20, color=PURPLE, weight="bold")
    fig.text(0.355, 0.207, "贯穿三次", ha="center", va="center", fontsize=8.7, color=MUTED)
    fig.text(
        0.49,
        0.228,
        "小型重复骨架在不同对象与场域之间持续接入，\n更大的参与外围则随具体行动重新组合。",
        ha="left",
        va="center",
        fontsize=11.2,
        color=INK,
        weight="bold",
    )
    fig.text(
        0.055,
        0.065,
        "边界：这是三个目的性公开行动的身份冻结层；重复署名不等于稳定联盟，event-only／alias pending 未被强行跨事件合并。",
        fontsize=8.9,
        color=RUST,
    )
    save(fig, "fig6_event_reassembly_v2.png")


def main() -> None:
    configure()
    figure_translation_mechanisms()
    figure_institutional_conversion()
    figure_referendum_gates()
    figure_sakishima_hypothesis()
    figure_official_civic_ecology()
    figure_event_reassembly()
    print(f"Findings-led third sync v2 figures written to {FIG}")


if __name__ == "__main__":
    main()
