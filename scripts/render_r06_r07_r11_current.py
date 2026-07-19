"""Render the current R6/R7/R11 figures from their reviewed module CSVs.

This is deliberately a renderer, not a data builder.  It reads exactly three
current module tables and writes exactly six SVG/HTML figure files.  It never
touches central CSVs, HR-021, the explanatory brief, or the validation note.
"""

from __future__ import annotations

import csv
import html
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT_DIR = ROOT / "outputs" / "R06_R07_R11_pathways_v1"
DEFAULT_OUTPUT_DIR = DEFAULT_INPUT_DIR

INPUT_FILENAMES = {
    "r6": "r06_pathway_comparison_v0.csv",
    "r7": "r07_venue_shift_stages_v0.csv",
    "r11": "r11_external_entry_matrix_v0.csv",
}
OUTPUT_FILENAMES = {
    "fig_r06_target_pathways_v0.svg",
    "fig_r06_target_pathways_v0.html",
    "fig_r07_venue_shift_small_multiples_v0.svg",
    "fig_r07_venue_shift_small_multiples_v0.html",
    "fig_r11_external_entry_matrix_v0.svg",
    "fig_r11_external_entry_matrix_v0.html",
}

R11_DOMAINS = [
    "advocacy",
    "legal",
    "administrative",
    "service",
    "charity",
    "public_diplomacy",
]
R11_OBJECTS = [
    "Henoko/Oura",
    "ONC/JICA",
    "Prefecture/base-policy",
    "USO/service",
    "spouse network",
    "unknown recipient",
]
EXPECTED_DOMAIN_COUNTS = Counter(
    {
        "advocacy": 30,
        "legal": 5,
        "administrative": 7,
        "service": 8,
        "charity": 2,
        "public_diplomacy": 1,
    }
)
EXPECTED_OBJECT_COUNTS = Counter(
    {
        ("advocacy", "Henoko/Oura"): 30,
        ("legal", "Henoko/Oura"): 5,
        ("administrative", "ONC/JICA"): 6,
        ("administrative", "Prefecture/base-policy"): 1,
        ("service", "USO/service"): 4,
        ("service", "spouse network"): 4,
        ("charity", "USO/service"): 2,
        ("public_diplomacy", "unknown recipient"): 1,
    }
)

R6_SHORT = {
    "R6P01": {
        "family": "国际法律",
        "roles": "原告／律师／non-party 边界",
        "venue": "美国联邦法院",
        "target": "美国国防部",
    },
    "R6P02": {
        "family": "国际机构请求",
        "roles": "请求发起者与事件参与者",
        "venue": "美国海洋哺乳动物委员会",
        "target": "美国海洋哺乳动物委员会",
    },
    "R6P03": {
        "family": "日本国内环保声援",
        "roles": "主办方与日本国内署名者",
        "venue": "公开声明",
        "target": "边野古基地建设计划",
    },
    "R6P04": {
        "family": "海外事件声援",
        "roles": "海外署名者",
        "venue": "跨国公开声明",
        "target": "边野古基地建设计划",
    },
    "R6P05": {
        "family": "行政协作／受托",
        "roles": "活动协作／受托／提案选定",
        "venue": "JICA 活动／委托；县基地政策合同",
        "target": "ONC／JICA；冲绳县基地政策研讨会",
    },
    "R6P06": {
        "family": "公共外交机会",
        "roles": "机会发布者；recipient 未知",
        "venue": "美国公共外交机会",
        "target": "recipient 未公开的青年项目",
    },
}

R7_SHORT = {
    ("R7C01", "1"): ("边野古／大浦湾", "儒艮／基地工程转译为 NHPA §402 主张"),
    ("R7C01", "2"): ("美国联邦地方法院", "具名原告与律师进入美国联邦法院"),
    ("R7C01", "3"): ("第九巡回法院", "确认 §402 审查标准；判决支持 DoD"),
    ("R7C02", "1"): ("边野古／大浦湾议题", "请求以儒艮与施工问题为对象"),
    ("R7C02", "2"): ("市民社会请求", "OEJP、JELF 与事件参与者公开列名"),
    ("R7C02", "3"): ("美国海洋哺乳动物委员会", "请求提交美国联邦机构"),
    ("R7C03", "1"): ("边野古／大浦湾", "边野古／大浦湾是声明对象"),
    ("R7C03", "2"): ("NACSJ／Peace Boat 声明", "主办方组织公开倡议场域"),
    ("R7C03", "3"): ("日本本土与海外署名场", "本土与海外组织在同一声明中列名"),
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def load_current(input_dir: Path = DEFAULT_INPUT_DIR) -> dict[str, list[dict[str, str]]]:
    """Read only the three reviewed current tables."""
    input_dir = Path(input_dir)
    return {
        key: read_csv(input_dir / filename)
        for key, filename in INPUT_FILENAMES.items()
    }


def classify_r11_object(row: dict[str, str]) -> str:
    """Assign a local-object column without permissive string fallbacks."""
    domain = row["entry_domain"]
    if domain in {"advocacy", "legal"}:
        return "Henoko/Oura"
    if domain == "administrative":
        if (
            row["entry_actor_id"] == "A066"
            and row["entry_mode"] == "proposal_selected_public_contract"
        ):
            return "Prefecture/base-policy"
        return "ONC/JICA"
    if domain == "service":
        if row["entry_mode"] == "service_network_coordination":
            return "spouse network"
        return "USO/service"
    if domain == "charity":
        return "USO/service"
    if domain == "public_diplomacy":
        return "unknown recipient"
    raise ValueError(f"unmapped R11 entry domain: {domain!r}")


def validate_current(tables: dict[str, list[dict[str, str]]]) -> None:
    r6, r7, r11 = tables["r6"], tables["r7"], tables["r11"]
    if len(r6) != 6 or {row["pathway_id"] for row in r6} != set(R6_SHORT):
        raise ValueError("current R6 table must contain R6P01–R6P06 exactly once")
    if any(int(row["fact_count"]) <= 0 for row in r6):
        raise ValueError("every R6 pathway must retain at least one fact observation")

    case_counts = Counter(row["case_id"] for row in r7)
    if len(r7) != 9 or case_counts != Counter({"R7C01": 3, "R7C02": 3, "R7C03": 3}):
        raise ValueError("current R7 table must contain three three-stage cases")
    if any("no causal inference" not in row["arrow_semantics"] for row in r7):
        raise ValueError("R7 ordered arrows must retain the no-causal-inference boundary")

    domain_counts = Counter(row["entry_domain"] for row in r11)
    if len(r11) != 53 or domain_counts != EXPECTED_DOMAIN_COUNTS:
        raise ValueError(
            f"unexpected R11 domain counts: rows={len(r11)}, counts={domain_counts}"
        )
    object_counts = Counter(
        (row["entry_domain"], classify_r11_object(row)) for row in r11
    )
    if object_counts != EXPECTED_OBJECT_COUNTS:
        raise ValueError(f"unexpected R11 object classification: {object_counts}")

    a066 = [row for row in r11 if row["entry_actor_id"] == "A066"]
    if len(a066) != 1 or classify_r11_object(a066[0]) != "Prefecture/base-policy":
        raise ValueError("A066 prefectural base-policy contract was misclassified")


def svg_page(title: str, subtitle: str, body: str, width: int, height: int) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">'
        '<rect width="100%" height="100%" fill="#FAF9F5"/>'
        '<style>'
        'text{font-family:"Noto Sans CJK SC","Microsoft YaHei",Arial,sans-serif;'
        'fill:#17231F}.title{font-size:30px;font-weight:700}.sub{font-size:14px;'
        'fill:#53615B}.head{font-size:16px;font-weight:700}.label{font-size:14px}'
        '.small{font-size:12px;fill:#53615B}.num{font-size:24px;font-weight:700}'
        "</style>"
        f'<text x="55" y="52" class="title">{html.escape(title)}</text>'
        f'<text x="55" y="80" class="sub">{html.escape(subtitle)}</text>'
        f"{body}</svg>"
    )


def multiline(
    lines: list[str],
    x: int | float,
    y: int | float,
    css_class: str,
    *,
    line_height: int = 19,
    anchor: str = "start",
) -> str:
    content = "".join(
        f'<tspan x="{x}" dy="{0 if index == 0 else line_height}">'
        f"{html.escape(line)}</tspan>"
        for index, line in enumerate(lines)
    )
    return (
        f'<text x="{x}" y="{y}" text-anchor="{anchor}" '
        f'class="{css_class}">{content}</text>'
    )


def split_short(text: str, limit: int = 22) -> list[str]:
    """Split a short label into at most two SVG lines."""
    if len(text) <= limit:
        return [text]
    break_at = max(
        text.rfind(separator, 0, limit + 1)
        for separator in ("／", "；", " ", "、", "，")
    )
    if break_at < max(6, limit // 2):
        break_at = limit
    first = text[: break_at + (1 if text[break_at : break_at + 1] in "／；、，" else 0)]
    second = text[len(first) :].lstrip()
    if len(second) > limit + 4:
        second = second[: limit + 3].rstrip() + "…"
    return [first.rstrip(), second]


def render_r6(rows: list[dict[str, str]]) -> str:
    body: list[str] = []
    colors = ["#D7E8E1", "#DDE5F0", "#F0DFC9", "#E8D8E8", "#DDE8CF", "#F2D9D2"]
    for index, row in enumerate(sorted(rows, key=lambda item: item["pathway_id"])):
        labels = R6_SHORT[row["pathway_id"]]
        y = 126 + index * 110
        body.append(
            f'<rect x="55" y="{y}" width="1390" height="92" rx="12" '
            f'fill="{colors[index]}"/>'
        )
        body.append(multiline([labels["family"]], 75, y + 27, "head"))
        body.append(multiline(split_short(labels["roles"], 19), 75, y + 53, "small", line_height=17))
        body.append(multiline(["入口"] + split_short(labels["venue"], 20), 420, y + 24, "label", line_height=20))
        body.append(multiline(["目标"] + split_short(labels["target"], 20), 850, y + 24, "label", line_height=20))
        body.append(
            f'<text x="1330" y="{y + 48}" text-anchor="middle" '
            f'class="num">{int(row["fact_count"])}</text>'
        )
        body.append(
            f'<text x="1330" y="{y + 70}" text-anchor="middle" '
            'class="small">事实观察</text>'
        )
    body.append(
        '<text x="55" y="820" class="small">'
        "六类入口不是一张统一国际网络；法律、请求、署名、行政与机会角色不可互换。"
        "</text>"
    )
    return svg_page(
        "R6：目标路径比较",
        "六类公开入口的事实观察数；数字不是影响力，也不表示政策效果",
        "".join(body),
        1500,
        860,
    )


def render_r7(rows: list[dict[str, str]]) -> str:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row["case_id"]].append(row)
    case_titles = {
        "R7C01": "儒艮国际诉讼",
        "R7C02": "2020 MMC 请求",
        "R7C03": "2015 跨国声明",
    }
    colors = ["#D7E8E1", "#DDE5F0", "#F0DFC9"]
    body: list[str] = []
    for case_index, case_id in enumerate(("R7C01", "R7C02", "R7C03")):
        stages = sorted(grouped[case_id], key=lambda row: int(row["stage_order"]))
        y = 142 + case_index * 235
        body.append(f'<text x="55" y="{y}" class="head">{case_titles[case_id]}</text>')
        for stage_index, stage in enumerate(stages):
            x = 80 + stage_index * 465
            venue, observation = R7_SHORT[(case_id, stage["stage_order"])]
            body.append(
                f'<rect x="{x}" y="{y + 25}" width="380" height="125" rx="13" '
                f'fill="{colors[case_index]}"/>'
            )
            body.append(
                f'<text x="{x + 18}" y="{y + 50}" class="small">'
                f'{html.escape(stage["date_or_period"])} · 阶段 {stage["stage_order"]}</text>'
            )
            body.append(multiline(split_short(venue, 20), x + 18, y + 76, "head", line_height=19))
            body.append(multiline(split_short(observation, 23), x + 18, y + 112, "small", line_height=17))
            if stage_index < 2:
                body.append(
                    f'<line x1="{x + 390}" y1="{y + 88}" x2="{x + 450}" '
                    'y2="{}" stroke="#7C8983" stroke-width="2" '
                    'stroke-dasharray="6 5"/>'.format(y + 88)
                )
                body.append(
                    f'<text x="{x + 420}" y="{y + 75}" text-anchor="middle" '
                    'class="small">顺序</text>'
                )
    body.append(
        '<text x="55" y="855" class="small">'
        "虚线只表示程序时间或同一事件中的展示顺序；不表示因果，也不证明政策效果。"
        "</text>"
    )
    return svg_page(
        "R7：三案例场域序列",
        "法律程序按时间排序；请求与声明按同一事件中的角色／入口构成排序",
        "".join(body),
        1500,
        900,
    )


def render_r11(rows: list[dict[str, str]]) -> str:
    counts = Counter(
        (row["entry_domain"], classify_r11_object(row)) for row in rows
    )
    column_labels = {
        "Henoko/Oura": ["Henoko/", "Oura"],
        "ONC/JICA": ["ONC/", "JICA"],
        "Prefecture/base-policy": ["Prefecture/", "base-policy"],
        "USO/service": ["USO/", "service"],
        "spouse network": ["spouse", "network"],
        "unknown recipient": ["unknown", "recipient"],
    }
    row_labels = {
        "advocacy": "advocacy",
        "legal": "legal",
        "administrative": "administrative",
        "service": "service",
        "charity": "charity",
        "public_diplomacy": "public diplomacy",
    }
    left, top, cell_w, cell_h = 270, 160, 190, 92
    body: list[str] = []
    for index, obj in enumerate(R11_OBJECTS):
        x = left + index * cell_w + cell_w / 2
        body.append(multiline(column_labels[obj], x, 118, "head", line_height=18, anchor="middle"))
    for row_index, domain in enumerate(R11_DOMAINS):
        y = top + row_index * cell_h
        body.append(f'<text x="55" y="{y + 48}" class="head">{row_labels[domain]}</text>')
        for column_index, obj in enumerate(R11_OBJECTS):
            value = counts[(domain, obj)]
            x = left + column_index * cell_w
            fill = "#17624F" if value else "#FFFFFF"
            text_color = "#FFFFFF" if value else "#A4ACA8"
            body.append(
                f'<rect x="{x + 8}" y="{y + 8}" width="{cell_w - 16}" height="70" '
                f'rx="10" fill="{fill}" stroke="#D0D6D2"/>'
            )
            body.append(
                f'<text x="{x + cell_w / 2}" y="{y + 53}" text-anchor="middle" '
                f'class="num" style="fill:{text_color}">{value}</text>'
            )
    body.append(
        '<text x="55" y="748" class="small">'
        "53 条已核进入观察；A066 的县基地政策合同单列，不进入 USO/service。"
        "</text>"
    )
    body.append(
        '<text x="55" y="769" class="small">'
        "事件／案件角色不得外推为联盟；服务、慈善与行政记录不得外推基地政治立场；NOFO 不是 award。"
        "</text>"
    )
    return svg_page(
        "R11：外来 actor 进入方式 × 本地对象",
        "按明确的对象分类呈现 53 条观察；单元格不是联盟强度或政治阵营",
        "".join(body),
        1500,
        800,
    )


def html_page(title: str, svg: str, max_width: int = 1500) -> str:
    return (
        "<!doctype html><html lang='zh-CN'><head><meta charset='utf-8'>"
        f"<title>{html.escape(title)}</title>"
        "<style>body{margin:0;background:#eceae4}"
        f"main{{max-width:{max_width}px;margin:24px auto;background:white;"
        "box-shadow:0 8px 28px #0002}svg{display:block;width:100%;height:auto}"
        "</style></head><body><main>"
        f"{svg}</main></body></html>"
    )


def render_current(
    input_dir: Path = DEFAULT_INPUT_DIR,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> set[Path]:
    """Render and write only the six declared figure assets."""
    tables = load_current(Path(input_dir))
    validate_current(tables)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    figures = {
        "fig_r06_target_pathways_v0": (
            "R6 target pathways",
            render_r6(tables["r6"]),
        ),
        "fig_r07_venue_shift_small_multiples_v0": (
            "R7 venue sequences",
            render_r7(tables["r7"]),
        ),
        "fig_r11_external_entry_matrix_v0": (
            "R11 external entry matrix",
            render_r11(tables["r11"]),
        ),
    }
    written: set[Path] = set()
    for stem, (title, svg) in figures.items():
        svg_path = output_dir / f"{stem}.svg"
        html_path = output_dir / f"{stem}.html"
        svg_path.write_text(svg, encoding="utf-8")
        html_path.write_text(html_page(title, svg), encoding="utf-8")
        written.update({svg_path, html_path})
    if {path.name for path in written} != OUTPUT_FILENAMES:
        raise ValueError("renderer output set drifted beyond the six declared assets")
    return written


def main() -> None:
    written = render_current()
    print(
        "Current R6/R7/R11 render OK: "
        f"{len(written)} figure files from 6/9/53 reviewed rows."
    )


if __name__ == "__main__":
    main()
