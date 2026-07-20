"""Render F035/F036 from the current, already-formalized S002 universe tables.

This module is deliberately render-only.  It reads the authoritative 616-row
source-universe table and its current mechanical aggregate tables, validates
their parity, and writes four new SVG/HTML assets.  It does not parse the
original PDF, rebuild identity crosswalks, touch the R10 relation/amount/
function layers, or overwrite the historical PNGs.
"""

from __future__ import annotations

import csv
import html
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UNIVERSE_DIR = ROOT / "outputs" / "R10_official_collaboration_universe_v1"
UNIVERSE_PATH = UNIVERSE_DIR / "official_collaboration_source_universe_v1.csv"
ISSUE_MATRIX_PATH = UNIVERSE_DIR / "issue_mechanism_matrix_v1.csv"
DEPARTMENT_MATRIX_PATH = UNIVERSE_DIR / "department_mechanism_matrix_v1.csv"
PARTNER_SUMMARY_PATH = UNIVERSE_DIR / "partner_display_alias_summary_v1.csv"
HR032_SUMMARY_PATH = UNIVERSE_DIR / "HR032_crosswalk_merge_summary_v1.csv"

INPUT_PATHS = (
    UNIVERSE_PATH,
    ISSUE_MATRIX_PATH,
    DEPARTMENT_MATRIX_PATH,
    PARTNER_SUMMARY_PATH,
    HR032_SUMMARY_PATH,
)
LEGACY_PNG_PATHS = (
    UNIVERSE_DIR / "fig_r10_s002_issue_mechanism_matrix_v1.png",
    UNIVERSE_DIR / "fig_r10_s002_partner_department_resource_structure_v1.png",
)
OUTPUT_FILENAMES = {
    "fig_r10_s002_issue_mechanism_matrix_current.svg",
    "fig_r10_s002_issue_mechanism_matrix_current.html",
    "fig_r10_s002_partner_department_resource_structure_current.svg",
    "fig_r10_s002_partner_department_resource_structure_current.html",
}

MECHANISM_SHORT = {
    "1": "委托",
    "2": "提案委托",
    "3": "指定管理",
    "4": "补助等",
    "5": "共催",
    "6": "后援",
    "7": "委员会",
    "8": "事业协力",
    "9": "讲师等",
    "10": "其他",
}
MECHANISM_COLORS = {
    "1": "#17624F",
    "2": "#3C806D",
    "3": "#70A391",
    "4": "#C97926",
    "5": "#587E9A",
    "6": "#7899AE",
    "7": "#8B6F93",
    "8": "#A58C5D",
    "9": "#B36C79",
    "10": "#7E8984",
}
ISSUE_SHORT = {
    "1": "保健・医疗・福祉",
    "2": "社会教育・终身学习",
    "3": "地域营造",
    "4": "观光振兴",
    "5": "农山渔村・离岛",
    "6": "学术・文化・体育",
    "7": "环境保全",
    "8": "灾害救援",
    "9": "地域安全・防罪",
    "10": "人权・和平",
    "11": "国际合作・交流",
    "12": "男女共同参画",
    "13": "儿童教育・健全育成",
    "14": "信息化社会",
    "15": "科学技术・研究",
    "16": "经济活动",
    "17": "职业能力・就业",
    "18": "消费者保护",
    "19": "NPO 活动支援",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def load_current() -> dict[str, list[dict[str, str]]]:
    """Read only current source-universe and mechanical aggregate tables."""
    return {
        "universe": read_csv(UNIVERSE_PATH),
        "issues": read_csv(ISSUE_MATRIX_PATH),
        "departments": read_csv(DEPARTMENT_MATRIX_PATH),
        "partners": read_csv(PARTNER_SUMMARY_PATH),
        "hr032": read_csv(HR032_SUMMARY_PATH),
    }


def _aggregate(
    rows: list[dict[str, str]], first: str, second: str
) -> Counter[tuple[str, str]]:
    return Counter((row[first], row[second]) for row in rows)


def _matrix_counts(
    rows: list[dict[str, str]], first: str
) -> dict[tuple[str, str], int]:
    return {
        (row[first], row["official_mechanism_code"]): int(row["source_row_count"])
        for row in rows
    }


def hr032_metrics(rows: list[dict[str, str]]) -> dict[str, int]:
    return {row["metric"]: int(row["value"]) for row in rows}


def validate_current(tables: dict[str, list[dict[str, str]]]) -> None:
    """Fail closed if any current aggregate drifts from the 616 source rows."""
    universe = tables["universe"]
    issues = tables["issues"]
    departments = tables["departments"]
    partners = tables["partners"]

    if len(universe) != 616:
        raise ValueError(f"S002 current universe must contain 616 rows, got {len(universe)}")
    row_numbers = sorted(int(row["source_row_number"]) for row in universe)
    if row_numbers != list(range(1, 617)):
        raise ValueError("S002 source_row_number must remain the complete 1..616 sequence")
    if len({row["source_row_uid"] for row in universe}) != 616:
        raise ValueError("S002 source_row_uid values are not unique")
    if {row["source_id"] for row in universe} != {"S002"}:
        raise ValueError("current official universe contains a non-S002 source")
    if {row["official_issue_field_code"] for row in universe} != {
        str(code) for code in range(1, 20)
    }:
        raise ValueError("official issue-code universe drifted from 1..19")
    if {row["official_mechanism_code"] for row in universe} != {
        str(code) for code in range(1, 11)
    }:
        raise ValueError("official mechanism-code universe drifted from 1..10")

    expected_issue_cells = {
        (str(issue), str(mechanism))
        for issue in range(1, 20)
        for mechanism in range(1, 11)
    }
    issue_counts = _matrix_counts(issues, "dimension_code_or_name")
    if len(issues) != 190 or set(issue_counts) != expected_issue_cells:
        raise ValueError("issue×mechanism table must retain all 19×10 cells")
    issue_source_counts = _aggregate(
        universe, "official_issue_field_code", "official_mechanism_code"
    )
    if issue_counts != {
        key: issue_source_counts[key] for key in expected_issue_cells
    }:
        raise ValueError("issue×mechanism table no longer matches the 616 source rows")

    department_names = {
        row["department_display_machine"] for row in universe
    }
    expected_department_cells = {
        (department, str(mechanism))
        for department in department_names
        for mechanism in range(1, 11)
    }
    department_counts = _matrix_counts(departments, "dimension_code_or_name")
    if len(department_names) != 15 or len(departments) != 150:
        raise ValueError("department×mechanism table must retain 15×10 cells")
    if set(department_counts) != expected_department_cells:
        raise ValueError("department×mechanism cell keys drifted")
    department_source_counts = _aggregate(
        universe, "department_display_machine", "official_mechanism_code"
    )
    if department_counts != {
        key: department_source_counts[key] for key in expected_department_cells
    }:
        raise ValueError("department×mechanism table no longer matches the source rows")

    partner_counts = Counter(
        row["partner_name_display_alias_machine"] for row in universe
    )
    summary_counts = {
        row["partner_name_display_alias_machine"]: int(row["source_row_count"])
        for row in partners
    }
    if len(partners) != 365 or summary_counts != partner_counts:
        raise ValueError("365-label partner summary no longer matches the source rows")
    if sum(summary_counts.values()) != 616:
        raise ValueError("partner source-label counts no longer sum to 616")
    if sum(count >= 5 for count in summary_counts.values()) != 17:
        raise ValueError("fixed ≥5-row partner-label threshold must retain 17 labels")
    if any(
        row["identity_status"] != "machine_display_alias_only_not_actor_identity"
        for row in partners
    ):
        raise ValueError("a machine display label was promoted to actor identity")

    expected_hr032 = {
        "source_universe_rows_unchanged": 616,
        "administrative_relation_edges_approved": 0,
        "amount_allocations_approved": 0,
    }
    metrics = hr032_metrics(tables["hr032"])
    if any(metrics.get(key) != value for key, value in expected_hr032.items()):
        raise ValueError(f"HR032 source-universe boundary drifted: {metrics}")


def escape(value: object) -> str:
    return html.escape(str(value), quote=True)


def svg_page(
    title: str,
    subtitle: str,
    body: str,
    *,
    width: int,
    height: int,
    description: str,
) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">'
        f'<title id="title">{escape(title)}</title>'
        f'<desc id="desc">{escape(description)}</desc>'
        '<rect width="100%" height="100%" fill="#FAF8F1"/>'
        "<style>"
        'text{font-family:"Noto Sans CJK SC","Microsoft YaHei",Arial,sans-serif;'
        "fill:#17231F}.title{font-size:32px;font-weight:700}"
        ".sub{font-size:15px;fill:#52605A}.head{font-size:17px;font-weight:700}"
        ".label{font-size:14px}.small{font-size:12px;fill:#52605A}"
        ".tiny{font-size:10px;fill:#65716C}.cell{font-size:11px;font-weight:700}"
        "</style>"
        f'<text x="54" y="52" class="title">{escape(title)}</text>'
        f'<text x="54" y="80" class="sub">{escape(subtitle)}</text>'
        f"{body}</svg>"
    )


def heat_fill(value: int) -> tuple[str, str]:
    if value == 0:
        return "#FFFDF8", "#A7AEA9"
    if value <= 2:
        return "#E6F0EA", "#17322B"
    if value <= 7:
        return "#B9D6C7", "#17322B"
    if value <= 19:
        return "#78AA92", "#FFFFFF"
    if value <= 49:
        return "#3D806B", "#FFFFFF"
    return "#17624F", "#FFFFFF"


def render_f035(tables: dict[str, list[dict[str, str]]]) -> str:
    counts = _matrix_counts(tables["issues"], "dimension_code_or_name")
    mechanism_totals = Counter(
        row["official_mechanism_code"] for row in tables["universe"]
    )
    c1_c4_rows = sum(mechanism_totals[str(code)] for code in range(1, 5))
    c1_c4_share = c1_c4_rows / len(tables["universe"]) * 100
    left, top, cell_w, cell_h = 465, 170, 103, 43
    body: list[str] = [
        '<text x="54" y="112" class="head">19 个官方事业分野 × 10 种官方协作机制</text>',
        '<text x="54" y="137" class="small">格内数字为来源记录数；零值留白。颜色只编码记录数，不编码金额或影响力。</text>',
    ]
    for mechanism in range(1, 11):
        x = left + (mechanism - 1) * cell_w + cell_w / 2
        body.append(
            f'<text x="{x}" y="{top - 29}" text-anchor="middle" class="small">'
            f"C{mechanism}</text>"
        )
        body.append(
            f'<text x="{x}" y="{top - 11}" text-anchor="middle" class="tiny">'
            f"{escape(MECHANISM_SHORT[str(mechanism)])}</text>"
        )

    for issue in range(1, 20):
        code = str(issue)
        y = top + (issue - 1) * cell_h
        row_total = sum(counts[(code, str(mechanism))] for mechanism in range(1, 11))
        body.append(
            f'<text x="{left - 18}" y="{y + 27}" text-anchor="end" class="label">'
            f"F{issue:02d}　{escape(ISSUE_SHORT[code])}　· {row_total}</text>"
        )
        for mechanism in range(1, 11):
            value = counts[(code, str(mechanism))]
            x = left + (mechanism - 1) * cell_w
            fill, text_fill = heat_fill(value)
            body.append(
                f'<rect x="{x}" y="{y}" width="{cell_w - 3}" height="{cell_h - 3}" '
                f'rx="4" fill="{fill}" stroke="#D8DDD8"/>'
            )
            if value:
                body.append(
                    f'<text x="{x + (cell_w - 3) / 2}" y="{y + 27}" '
                    f'text-anchor="middle" class="cell" style="fill:{text_fill}">'
                    f"{value}</text>"
                )

    boundary_y = top + 19 * cell_h + 42
    body.append(
        f'<rect x="54" y="{boundary_y}" width="1492" height="142" rx="13" '
        'fill="#FFFFFF" stroke="#D0D6D2"/>'
    )
    notes = [
        "616 条来源行构成 S002 FY2024 官方来源总体；来源行数 ≠ 组织数、合同数、拨款数。",
        (
            f"C1–C4 合计 {c1_c4_rows}/616（{c1_c4_share:.1f}%），"
            "只表示官方机制分类；C4 不等于现金 grant。"
        ),
        "“事业费”是项目／事业层字段，不自动等于向合作方支付的金额。",
    ]
    for index, note in enumerate(notes):
        body.append(
            f'<text x="82" y="{boundary_y + 38 + index * 34}" class="label">'
            f"{escape(note)}</text>"
        )
    return svg_page(
        "F035｜FY2024 行政协作来源总体：议题分野 × 协作机制",
        "只读 current 规范表的机械重绘 · S002 全量来源行 · no actor／relation inference",
        "".join(body),
        width=1600,
        height=boundary_y + 185,
        description=(
            "A 19 by 10 matrix of all 616 S002 source records, grouped by "
            "official issue field and official collaboration mechanism."
        ),
    )


def _truncate(value: str, limit: int = 26) -> str:
    return value if len(value) <= limit else value[: limit - 1] + "…"


def render_f036(tables: dict[str, list[dict[str, str]]]) -> str:
    universe = tables["universe"]
    department_counts = _matrix_counts(
        tables["departments"], "dimension_code_or_name"
    )
    department_totals = Counter(
        row["department_display_machine"] for row in universe
    )
    departments = [
        name
        for name, _count in sorted(
            department_totals.items(), key=lambda item: (-item[1], item[0])
        )
    ]
    partners = sorted(
        (
            row
            for row in tables["partners"]
            if int(row["source_row_count"]) >= 5
        ),
        key=lambda row: (
            -int(row["source_row_count"]),
            row["partner_name_display_alias_machine"],
        ),
    )
    partner_mechanisms = _aggregate(
        universe,
        "partner_name_display_alias_machine",
        "official_mechanism_code",
    )

    left, top, cell_w, cell_h = 400, 170, 108, 38
    body: list[str] = [
        '<text x="54" y="112" class="head">A｜15 个部门 × 10 种机制：来源行结构</text>',
        '<text x="54" y="137" class="small">部门按来源行总数排序；格内数字是记录数。</text>',
    ]
    for mechanism in range(1, 11):
        x = left + (mechanism - 1) * cell_w + cell_w / 2
        body.append(
            f'<text x="{x}" y="{top - 16}" text-anchor="middle" class="tiny">'
            f"C{mechanism} {escape(MECHANISM_SHORT[str(mechanism)])}</text>"
        )
    for index, department in enumerate(departments):
        y = top + index * cell_h
        body.append(
            f'<text x="{left - 18}" y="{y + 25}" text-anchor="end" class="label">'
            f"{escape(department)}　· {department_totals[department]}</text>"
        )
        for mechanism in range(1, 11):
            value = department_counts[(department, str(mechanism))]
            x = left + (mechanism - 1) * cell_w
            fill, text_fill = heat_fill(value)
            body.append(
                f'<rect x="{x}" y="{y}" width="{cell_w - 3}" height="{cell_h - 3}" '
                f'rx="4" fill="{fill}" stroke="#D8DDD8"/>'
            )
            if value:
                body.append(
                    f'<text x="{x + (cell_w - 3) / 2}" y="{y + 24}" '
                    f'text-anchor="middle" class="cell" style="fill:{text_fill}">'
                    f"{value}</text>"
                )

    chart_top = top + len(departments) * cell_h + 72
    body.append(
        f'<text x="54" y="{chart_top}" class="head">'
        "B｜高频 partner source-label × 机制（固定阈值：每个标签 ≥ 5 行；17 个）"
        "</text>"
    )
    body.append(
        f'<text x="54" y="{chart_top + 25}" class="small">'
        "标签保持机器排版层；不应用法人合并、JV 拆分或 registry actor 化。"
        "</text>"
    )
    bar_left, bar_top, bar_width, bar_h, row_gap = 430, chart_top + 53, 870, 18, 31
    max_total = max(int(row["source_row_count"]) for row in partners)
    for index, partner in enumerate(partners):
        label = partner["partner_name_display_alias_machine"]
        total = int(partner["source_row_count"])
        y = bar_top + index * row_gap
        body.append(
            f'<text x="{bar_left - 18}" y="{y + 14}" text-anchor="end" class="small">'
            f"{escape(_truncate(label))}</text>"
        )
        x = bar_left
        for mechanism in range(1, 11):
            value = partner_mechanisms[(label, str(mechanism))]
            if not value:
                continue
            width = bar_width * value / max_total
            body.append(
                f'<rect x="{x}" y="{y}" width="{width}" height="{bar_h}" '
                f'fill="{MECHANISM_COLORS[str(mechanism)]}"/>'
            )
            x += width
        body.append(
            f'<text x="{bar_left + bar_width + 20}" y="{y + 14}" class="small">'
            f"{total} 行 · {partner['department_count']} 部门</text>"
        )

    legend_y = bar_top + len(partners) * row_gap + 18
    for mechanism in range(1, 11):
        column = (mechanism - 1) % 5
        row = (mechanism - 1) // 5
        x = 430 + column * 205
        y = legend_y + row * 27
        body.append(
            f'<rect x="{x}" y="{y - 12}" width="16" height="16" rx="3" '
            f'fill="{MECHANISM_COLORS[str(mechanism)]}"/>'
        )
        body.append(
            f'<text x="{x + 23}" y="{y + 1}" class="tiny">'
            f"C{mechanism} {escape(MECHANISM_SHORT[str(mechanism)])}</text>"
        )

    boundary_y = legend_y + 76
    body.append(
        f'<rect x="54" y="{boundary_y}" width="1492" height="142" rx="13" '
        'fill="#FFFFFF" stroke="#D0D6D2"/>'
    )
    notes = [
        "365 个机器排版标签不是 actor；同名重复不等于同一法人已完成合并。",
        "共同企业体未拆分；HR-032 名称 crosswalk 不生成 actor、付款或关系边。",
        "项目事业费不等于向标签对应主体付款；高频标签也不表示网络中心性或政治影响力。",
    ]
    for index, note in enumerate(notes):
        body.append(
            f'<text x="82" y="{boundary_y + 38 + index * 34}" class="label">'
            f"{escape(note)}</text>"
        )
    return svg_page(
        "F036｜FY2024 行政协作：部门—机制与 partner source-label",
        "只读 current 规范表的机械重绘 · 616 条来源行 · raw-label layer",
        "".join(body),
        width=1600,
        height=boundary_y + 185,
        description=(
            "All 616 S002 source rows shown as a department by mechanism "
            "matrix and a fixed-threshold chart of 17 machine display labels."
        ),
    )


def html_page(title: str, svg: str, *, max_width: int = 1600) -> str:
    return (
        "<!doctype html><html lang='zh-CN'><head><meta charset='utf-8'>"
        f"<title>{escape(title)}</title>"
        "<meta name='viewport' content='width=device-width,initial-scale=1'>"
        "<style>body{margin:0;background:#ECEAE4}"
        f"main{{max-width:{max_width}px;margin:24px auto;background:white;"
        "box-shadow:0 8px 28px #0002}svg{display:block;width:100%;height:auto}"
        "@media(max-width:700px){main{margin:0;box-shadow:none}}</style>"
        "</head><body><main>"
        f"{svg}</main></body></html>"
    )


def render_current(output_dir: Path = UNIVERSE_DIR) -> set[Path]:
    """Validate current inputs and write only four new F035/F036 assets."""
    tables = load_current()
    validate_current(tables)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    figures = [
        (
            output_dir / "fig_r10_s002_issue_mechanism_matrix_current",
            "F035 current S002 issue-mechanism universe",
            render_f035(tables),
        ),
        (
            output_dir / "fig_r10_s002_partner_department_resource_structure_current",
            "F036 current S002 department-mechanism and source-label structure",
            render_f036(tables),
        ),
    ]
    written: set[Path] = set()
    for stem, title, svg in figures:
        svg_path = stem.with_suffix(".svg")
        html_path = stem.with_suffix(".html")
        svg_path.write_text(svg, encoding="utf-8")
        html_path.write_text(html_page(title, svg), encoding="utf-8")
        written.update({svg_path, html_path})

    if {path.name for path in written} != OUTPUT_FILENAMES:
        raise ValueError("renderer output set drifted beyond the four declared assets")
    return written


def main() -> None:
    written = render_current()
    print(
        "Current F035/F036 render OK: "
        f"{len(written)} files from S002 616-row source universe."
    )


if __name__ == "__main__":
    main()
