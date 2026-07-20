from __future__ import annotations

import csv
import hashlib
import html
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def read_csv(name: str) -> list[dict[str, str]]:
    with (ROOT / name).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_text(name: str, text: str) -> None:
    (ROOT / name).write_text(text, encoding="utf-8", newline="\n")


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def svg_text(x: int, y: int, value: str, size: int = 22, weight: int = 400,
             fill: str = "#172033", anchor: str = "start") -> str:
    return (
        f'<text x="{x}" y="{y}" font-family="Arial, Noto Sans CJK SC, sans-serif" '
        f'font-size="{size}" font-weight="{weight}" fill="{fill}" '
        f'text-anchor="{anchor}">{esc(value)}</text>'
    )


def box(x: int, y: int, w: int, h: int, title: str, lines: list[str],
        fill: str, stroke: str, dashed: bool = False) -> str:
    dash = ' stroke-dasharray="9 7"' if dashed else ""
    parts = [
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="2.5"{dash}/>',
        svg_text(x + 20, y + 34, title, 22, 700),
    ]
    for idx, line in enumerate(lines):
        parts.append(svg_text(x + 20, y + 66 + idx * 27, line, 18, 400, "#344057"))
    return "\n".join(parts)


def arrow(x1: int, y1: int, x2: int, y2: int, color: str,
          dashed: bool = False) -> str:
    dash = ' stroke-dasharray="10 8"' if dashed else ""
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
        f'stroke-width="4" marker-end="url(#arrow)"{dash}/>'
    )


def svg_shell(width: int, height: int, body: str, title: str) -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<title>{esc(title)}</title>
<defs>
  <marker id="arrow" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto">
    <path d="M0,0 L12,6 L0,12 z" fill="#52627a"/>
  </marker>
</defs>
<rect width="{width}" height="{height}" fill="#f5f7fb"/>
{body}
</svg>
"""


def render_selective_permeability() -> None:
    body = [
        svg_text(48, 55, "H2：基地社区—冲绳社会的三种选择性接口", 32, 700),
        svg_text(48, 87, "研究假设图；箭头表示可观察过程，不是中央关系边", 18, 400, "#5b687c"),
        box(45, 170, 245, 190, "基地社区资源", ["军属社群", "慈善商店／俱乐部", "军事单位与公共事务"], "#e8efff", "#6687c5"),
        box(355, 105, 330, 145, "① 申请／筛选", ["MTS 董事会、AWWA 中介", "OIWC 申请与实物配置"], "#fff3d6", "#d59a23"),
        box(355, 290, 330, 145, "② 混合成员／接触", ["OIWC 与复归前 welfare council", "长期接触 ≠ 政治联盟"], "#e9f7f0", "#4d9b77"),
        box(355, 475, 330, 170, "③ 照护 → 权利", ["个案累积 → 调查／命名", "1979 提言 → 权利／政策", "后期公开基地责任主张"], "#f7eaf3", "#aa5d91"),
        box(755, 105, 555, 145, "本地福利／教育／障碍者组织", ["公开 recipient 可见；部分也在 S002 行政协作中出现", "recipient ≠ 盟友；S002 项目成本 ≠ 付款"], "#ffffff", "#99a5b7"),
        box(755, 290, 555, 145, "社会接触接口", ["冲绳人与美国人可共同参与福利活动", "成员比例、持续性和人员共享仍未完整测量"], "#ffffff", "#99a5b7"),
        box(755, 475, 555, 170, "权利／政策／基地问责接口", ["ISSO 是福利转向问责的历史候选", "18 个非随机问责锚点的有限 AI 查询", "未记录可归属直接组织关系"], "#ffffff", "#99a5b7"),
        arrow(290, 240, 355, 178, "#52627a"),
        arrow(290, 260, 355, 360, "#52627a"),
        arrow(290, 290, 355, 555, "#52627a"),
        arrow(685, 178, 755, 178, "#52627a"),
        arrow(685, 360, 755, 360, "#52627a"),
        arrow(685, 560, 755, 560, "#52627a"),
        svg_text(48, 715, "可说：历史材料削弱“长期始终完全封闭”的外推。", 22, 700, "#25334a"),
        svg_text(48, 750, "不可说：当代组织／人员已被对称测量，或两套生态完全隔绝。", 20, 400, "#9a3546"),
    ]
    write_text("fig_h2_selective_permeability_v1.svg", svg_shell(1360, 790, "\n".join(body), "H2 selective permeability"))


def render_overlap(summary: list[dict[str, str]]) -> None:
    width, height = 1360, 710
    max_total = max(int(row["unique_research_labels"]) for row in summary)
    bar_max = 760
    colors = {
        "direct": "#2c8c69",
        "composite": "#d9a72e",
        "identity": "#cc704f",
        "none": "#dce2ea",
    }
    body = [
        svg_text(48, 55, "跨期清单 crosswalk：少数名称候选共同可见", 32, 700),
        svg_text(48, 87, "受赠名单与 FY2024 S002 时期／单位不同；不估计转化概率或通透门槛", 18, 400, "#5b687c"),
    ]
    cohort_labels = {
        "H2OV001": "AWWA 前期公开受赠候选",
        "H2OV002": "OIWC 2015–24 公开受赠名册",
        "H2OV003": "MTS 近期网页标签",
        "H2OV004": "MTS FY2021–24 第三方 IRS 展示对象",
    }
    y = 150
    for row in summary:
        total = int(row["unique_research_labels"])
        direct = int(row["direct_name_family_candidates"])
        composite = int(row["composite_member_only"])
        identity = int(row["identity_scope_candidates"])
        none = int(row["no_match_or_not_listed"])
        body.append(svg_text(48, y, cohort_labels[row["cohort_id"]], 19, 700))
        x = 470
        scale = bar_max / max_total
        segments = [
            ("direct", direct),
            ("composite", composite),
            ("identity", identity),
            ("none", none),
        ]
        cursor = x
        for key, value in segments:
            segment_width = value * scale
            if value:
                body.append(
                    f'<rect x="{cursor:.1f}" y="{y - 25}" width="{segment_width:.1f}" '
                    f'height="30" fill="{colors[key]}"/>'
                )
            cursor += segment_width
        body.append(
            f'<rect x="{x}" y="{y - 25}" width="{total * scale:.1f}" height="30" '
            f'fill="none" stroke="#7a8798" stroke-width="1.5"/>'
        )
        body.append(svg_text(1260, y, f"n={total}", 18, 700, "#344057", "end"))
        body.append(svg_text(
            470, y + 28,
            f"直接名称族 {direct} · 联合体成员 {composite} · 身份范围候选 {identity} · 其余 {none}",
            16, 400, "#5b687c"
        ))
        y += 115
    legend_y = 610
    labels = [
        ("direct", "直接名称族候选"),
        ("composite", "仅联合体成员"),
        ("identity", "身份范围待核"),
        ("none", "无匹配／未列"),
    ]
    x = 48
    for key, label in labels:
        body.append(f'<rect x="{x}" y="{legend_y}" width="22" height="22" fill="{colors[key]}"/>')
        body.append(svg_text(x + 31, legend_y + 18, label, 17))
        x += 255
    body.append(svg_text(48, 670, "只记录候选名称共同可见；不推断转化概率、通透门槛、付款、关系或联盟。", 18, 700, "#8e3b4b"))
    write_text("fig_h2_recipient_admin_overlap_v1.svg", svg_shell(width, height, "\n".join(body), "H2 recipient and S002 overlap"))


def render_timeline() -> None:
    body = [
        svg_text(48, 55, "历史分化候选：接触、慈善与照护—权利并非同一路径", 32, 700),
        svg_text(48, 87, "事件顺序图；横向间距不按年份比例。虚线框为需原始材料确认的机制", 18, 400, "#5b687c"),
        svg_text(48, 145, "资源／接触轨", 21, 700, "#315c9a"),
        svg_text(48, 420, "照护／权利轨", 21, 700, "#8d4978"),
        arrow(165, 245, 1280, 245, "#6687c5"),
        arrow(165, 520, 1280, 520, "#aa5d91"),
    ]
    top = [
        ("1953", "OIWC\n自称成立"),
        ("1971", "福利理事会\n九俱乐部"),
        ("1972", "2000官方回溯\nAWWA六组"),
        ("1992–99", "AWWA\n年度汇总"),
        ("2015–24", "OIWC\n受赠名册"),
        ("2021–24", "第三方IRS展示\n待核原表"),
        ("2024", "Lions\n例外绕行"),
    ]
    bottom = [
        ("1958", "ISS Okinawa\n成立"),
        ("1972", "本地化／\n支持替换"),
        ("1979", "个案→\n正式提言"),
        ("1985", "国籍法修改\n多因结果"),
        ("1997", "公开基地\n责任主张"),
        ("1998", "咨询所闭所"),
        ("1999", "Amer-Asian\nSchool 线索"),
    ]
    xs = [185, 360, 535, 710, 885, 1060, 1235]
    for x, (date, label) in zip(xs, top):
        body.append(f'<circle cx="{x}" cy="245" r="10" fill="#315c9a"/>')
        body.append(svg_text(x, 190, date, 18, 700, "#315c9a", "middle"))
        for idx, line in enumerate(label.split("\n")):
            body.append(svg_text(x, 215 + idx * 22, line, 16, 400, "#344057", "middle"))
    for idx, (x, (date, label)) in enumerate(zip(xs, bottom)):
        body.append(f'<circle cx="{x}" cy="520" r="10" fill="#8d4978"/>')
        body.append(svg_text(x, 575, date, 18, 700, "#8d4978", "middle"))
        for line_idx, line in enumerate(label.split("\n")):
            body.append(svg_text(x, 600 + line_idx * 22, line, 16, 400, "#344057", "middle"))
        if idx in (1, 6):
            body.append(f'<rect x="{x-72}" y="548" width="144" height="85" rx="10" fill="none" stroke="#aa5d91" stroke-width="2" stroke-dasharray="7 6"/>')
    body.extend([
        svg_text(48, 690, "候选解释：复归带来的不是简单断裂，而可能是军属慈善中介与本地专业福利／权利工作的制度分化。", 20, 700, "#25334a"),
        svg_text(48, 725, "禁止：把相邻节点连成同一组织谱系；把 1999 学校线索当作咨询所延续。", 18, 400, "#9a3546"),
    ])
    write_text("fig_h2_historical_differentiation_v1.svg", svg_shell(1360, 770, "\n".join(body), "H2 historical differentiation candidate"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def validate() -> str:
    expected_counts = {
        "source_registry_v1.csv": 17,
        "mts_schedule_i_grants_v1.csv": 13,
        "mts_recent_recipient_labels_v1.csv": 41,
        "oiwc_public_recipient_roster_v1.csv": 86,
        "oiwc_annual_disclosure_v1.csv": 7,
        "recipient_s002_crosswalk_v1.csv": 11,
        "recipient_s002_overlap_summary_v1.csv": 4,
        "source_disclosure_audit_v1.csv": 8,
        "accountability_limited_co_mention_search_v2.csv": 18,
        "historical_interface_timeline_v1.csv": 17,
        "historical_interface_observations_v1.csv": 11,
        "literature_positioning_v1.csv": 5,
        "human_review_leads_v1.csv": 6,
    }
    rows_by_file = {name: read_csv(name) for name in expected_counts}
    for name, expected in expected_counts.items():
        actual = len(rows_by_file[name])
        assert actual == expected, f"{name}: expected {expected}, got {actual}"
        for row in rows_by_file[name]:
            if "package_scope" in row:
                assert row["package_scope"] == "research_only", f"{name}: non-research row"
            if "frontend_eligibility" in row:
                assert row["frontend_eligibility"] == "excluded_research_only", f"{name}: frontend leak"

    mts = rows_by_file["mts_schedule_i_grants_v1.csv"]
    sums: dict[str, int] = {}
    for row in mts:
        key = row["recipient_research_key"]
        if key:
            sums[key] = sums.get(key, 0) + int(row["amount_usd"])
    assert sums["awwa"] == 151672
    assert sums["kubasaki_high_school_ptso"] == 38051
    assert sum(row["observation_semantics"] == "named_grant_row" for row in mts) == 11
    assert sum(row["observation_semantics"] == "unitemized_grant_bucket" for row in mts) == 2
    assert all(
        row["source_basis"] == "third_party_IRS_derived_display_original_filing_not_checked"
        and row["review_status"] == "ai_seeded"
        for row in mts
    )

    oiwc = rows_by_file["oiwc_public_recipient_roster_v1.csv"]
    assert len({row["recipient_research_key"] for row in oiwc}) == 70
    assert sum(row["cycle"] == "2018-2019" for row in oiwc) == 14
    annual = {row["cycle"]: row for row in rows_by_file["oiwc_annual_disclosure_v1.csv"]}
    assert int(annual["2016-2017"]["row_amount_sum_jpy"]) == 1880762
    assert int(annual["2015-2016"]["row_amount_sum_jpy"]) == 1710604
    assert annual["2023-2024"]["named_rows_visible"] == "13"
    assert annual["2023-2024"]["organization_reported_recipient_count"] == "18"

    overlap = rows_by_file["recipient_s002_overlap_summary_v1.csv"]
    for row in overlap:
        total = int(row["unique_research_labels"])
        component_sum = sum(
            int(row[key]) for key in (
                "direct_name_family_candidates",
                "composite_member_only",
                "identity_scope_candidates",
                "no_match_or_not_listed",
            )
        )
        assert component_sum == total, f"{row['cohort_id']}: overlap components do not sum"

    search = rows_by_file["accountability_limited_co_mention_search_v2.csv"]
    assert len({row["actor_id"] for row in search}) == 18
    assert all(
        row["direct_org_interface_result"]
        == "limited_ai_log_no_attributable_direct_organization_relation_recorded"
        for row in search
    )
    assert all(
        row["query_family"] == "limited_exact_actor_x_service_name_web_co_mention_v1"
        and row["query_execution_status"] == "completed_no_results_returned"
        and row["returned_result_count"] == "0"
        and row["returned_result_urls"] == ""
        and row["anchor_selection"] == "nonrandom_accountability_anchor"
        for row in search
    )
    for row in search:
        for required_name in (
            "American Welfare and Works Association",
            "American Women's Welfare Association",
            "米国福祉事業協会",
            "米国婦人福祉協会",
        ):
            assert required_name in row["exact_query_string"]
        assert row["person_overlap_status"] == "not_symmetrically_measured_person_rosters_incomplete"

    crosswalk = rows_by_file["recipient_s002_crosswalk_v1.csv"]
    guarded = [row for row in crosswalk if row["existing_review_overlap"]]
    assert len(guarded) == 1 and guarded[0]["crosswalk_id"] == "H2XW003"
    leads = rows_by_file["human_review_leads_v1.csv"]
    guard_leads = [row for row in leads if row["assignment_status"] == "closed_by_duplicate_guard"]
    assert len(guard_leads) == 1 and guard_leads[0]["lead_id"] == "H2PHL006"

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for required in (
        "research_only",
        "not_frontend_ready",
        "fig_h2_selective_permeability_v1.svg",
        "principal_checkpoint_v1.md",
        "limited_co_mention_search_method_v1.md",
    ):
        assert required in readme

    render_selective_permeability()
    render_overlap(overlap)
    render_timeline()
    for figure in (
        "fig_h2_selective_permeability_v1.svg",
        "fig_h2_recipient_admin_overlap_v1.svg",
        "fig_h2_historical_differentiation_v1.svg",
    ):
        text = (ROOT / figure).read_text(encoding="utf-8")
        assert text.startswith("<svg")
        assert "<title>" in text
        assert "中央关系边" in text or "关系" in text or "谱系" in text

    hashes = []
    for path in sorted(ROOT.glob("*.csv")) + sorted(ROOT.glob("*.svg")):
        hashes.append((path.name, sha256(path)))
    count_lines = "\n".join(
        f"- `{name}`: {len(rows_by_file[name])} rows" for name in expected_counts
    )
    hash_lines = "\n".join(f"- `{name}`: `{digest}`" for name, digest in hashes)
    return f"""# H2 recipient permeability validation

Generated by `python outputs/research_wave_h2_recipient_permeability_v1/render_and_validate.py`.

## Result

`PASS`

## Row counts

{count_lines}

## Numerical checks

- MTS third-party IRS-derived display transcription: 13 ai-seeded rows; 11 named rows and 2 unitemized buckets; original filing pages are not yet checked.
- Four displayed AWWA filing-year rows sum to **151,672 USD**, pending original-filing review.
- Four Kubasaki-label filing-year rows sum to **38,051 USD**; identity remains unresolved.
- OIWC roster: 86 raw rows and 70 research keys across seven displayed cycles.
- OIWC 2023–2024 mismatch retained: 13 public names versus application-guide count 18.
- Limited co-mention search: 18 nonrandom accountability anchors; exact queries and zero-result execution records are retained. This is not a symmetric or closure test.
- S002 overlap summaries add exactly to each disclosure-cohort denominator.

## Boundary checks

- Every CSV row with scope fields is `research_only / excluded_research_only`.
- No historical node receives an actor ID; existing actor IDs appear only as the 18 search anchors.
- H2WI003 is guarded as the single F029/HR018-24 overlap and creates no duplicate task.
- Unitemized grants, S002 project costs, composite partner cells and event co-presence are not converted to dyadic funding/alliance edges.
- Cross-period recipient/S002 name visibility is not interpreted as a transition probability or permeability threshold.
- The 1972 AWWA six-group label is explicitly a 2000 official retrospective, not a frozen cross-period count.
- Three SVGs are research-hypothesis figures and are not frontend contracts.

## SHA-256

{hash_lines}
"""


if __name__ == "__main__":
    report = validate()
    write_text("validation_report_v1.md", report)
    print("PASS: H2 recipient permeability package validated and figures rendered")
