"""Render current R10/F008 figures without rebuilding any research facts.

This module is deliberately render-only. It reads the post-HR018/HR032
tables and the current typed relation sample, validates their frozen
mechanical counts, and writes only six SVG/HTML files. It never edits a
central CSV, human-review file, report manifest, caption bank, or control
document.
"""

from __future__ import annotations

import csv
import html
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RELATION_SAMPLE_PATH = (
    ROOT / "data" / "interim" / "15_funding_or_support_edges_sample_v0.csv"
)
R10_RELATIONS_PATH = (
    ROOT / "data" / "interim" / "21_admin_collaboration_relations_v0.csv"
)
R10_AMOUNTS_PATH = (
    ROOT / "data" / "interim" / "22_admin_amount_observations_v0.csv"
)
R10_FUNCTIONS_PATH = (
    ROOT / "data" / "interim" / "23_admin_function_observations_v0.csv"
)
HR032_SUMMARY_PATH = (
    ROOT
    / "outputs"
    / "R10_official_collaboration_universe_v1"
    / "HR032_crosswalk_merge_summary_v1.csv"
)

PHASE1_OUTPUT_DIR = ROOT / "outputs" / "phase1_visuals_v1"
R10_OUTPUT_DIR = ROOT / "outputs" / "R10_administrative_collaboration_v0"

OUTPUT_FILENAMES = {
    "fig3_support_service_layers_strict.svg",
    "fig3_support_service_layers_strict.html",
    "fig_r10_mechanism_ecology.svg",
    "fig_r10_mechanism_ecology.html",
    "fig_r10_amount_evidence_boundary.svg",
    "fig_r10_amount_evidence_boundary.html",
}

REVIEWED_STATUSES = {"human_checked", "human_revised"}
SUPPORTED_CLAIMS = {"supported", "supported_bounded"}

EXPECTED_R10_REVIEW_COUNTS = Counter(
    {"human_checked": 24, "human_revised": 10, "needs_local_retrieval": 1}
)
EXPECTED_AMOUNT_REVIEW_COUNTS = Counter(
    {"human_checked": 21, "human_revised": 6, "needs_local_retrieval": 1}
)
EXPECTED_FUNCTION_REVIEW_COUNTS = Counter(
    {"human_checked": 29, "human_revised": 13, "needs_local_retrieval": 1}
)
EXPECTED_STRICT_PANEL_COUNTS = Counter(
    {
        "dyadic_relation": 7,
        "administrative_record": 6,
        "event_participation": 1,
        "research_lead": 2,
    }
)
EXPECTED_MECHANISM_COUNTS = Counter(
    {
        "行政委托／指定": 15,
        "补助／grant 关系": 2,
        "企业赞助": 3,
        "直接捐赠": 1,
        "实物支持": 4,
        "成员关系": 5,
        "服务存在": 1,
        "活动协作": 1,
        "汇总观察": 2,
        "NOFO／机会": 1,
    }
)
EXPECTED_AMOUNT_BOUNDARY_COUNTS = Counter(
    {
        "实际合同额": 5,
        "点名委托资金流": 3,
        "点名现金捐赠": 2,
        "项目／事业成本": 14,
        "recipient 未解析": 1,
        "跨期／混合汇总": 2,
        "实物价值（非现金）": 1,
    }
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def load_current() -> dict[str, list[dict[str, str]]]:
    """Read only the current typed and post-review tables."""
    return {
        "sample": read_csv(RELATION_SAMPLE_PATH),
        "relations": read_csv(R10_RELATIONS_PATH),
        "amounts": read_csv(R10_AMOUNTS_PATH),
        "functions": read_csv(R10_FUNCTIONS_PATH),
        "hr032": read_csv(HR032_SUMMARY_PATH),
    }


def strict_sample_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    """Return the reviewed E3/E4 typed records eligible for the F008 panel.

    This is not the retired pre-HR018 38-row evidence-only filter. It requires
    an explicit accepted/bounded claim and an explicit graph/display semantic.
    Research leads remain panel-only and cannot become organization edges.
    """
    return [
        row
        for row in rows
        if row["evidence_level"] in {"E3", "E4"}
        and row["review_status"] in REVIEWED_STATUSES
        and row["claim_status"] in SUPPORTED_CLAIMS
        and row["graph_eligibility"] in EXPECTED_STRICT_PANEL_COUNTS
    ]


def classify_mechanism(row: dict[str, str]) -> str:
    relation_type = row["relation_type"]
    mapping = {
        "commission": "行政委托／指定",
        "designated_role": "行政委托／指定",
        "grant": "补助／grant 关系",
        "sponsorship": "企业赞助",
        "donation": "直接捐赠",
        "in_kind_donation": "实物支持",
        "in_kind_acquisition_assistance": "实物支持",
        "joint_in_kind_contribution": "实物支持",
        "network_membership": "成员关系",
        "service_presence": "服务存在",
        "event_collaboration": "活动协作",
        "aggregate_financial_contribution": "汇总观察",
        "aggregate_history": "汇总观察",
        "grant_opportunity": "NOFO／机会",
    }
    try:
        return mapping[relation_type]
    except KeyError as error:
        raise ValueError(f"unmapped R10 relation_type: {relation_type!r}") from error


def classify_amount(row: dict[str, str]) -> str:
    amount_basis = row["amount_basis"]
    mapping = {
        "actual_contract_amount": "实际合同额",
        "municipal_named_recipient_commission_flow": "点名委托资金流",
        "documented_donation": "点名现金捐赠",
        "municipal_total_project_cost": "项目／事业成本",
        "organization_reported_project_cost": "项目／事业成本",
        "prefecture_collaboration_table_project_cost": "项目／事业成本",
        "municipal_noneligible_commission_observation": "recipient 未解析",
        "aggregate_mixed_recipient_report": "跨期／混合汇总",
        "aggregate_long_term_history": "跨期／混合汇总",
        "reported_in_kind_item_value": "实物价值（非现金）",
    }
    try:
        return mapping[amount_basis]
    except KeyError as error:
        raise ValueError(f"unmapped R10 amount_basis: {amount_basis!r}") from error


def hr032_metrics(rows: list[dict[str, str]]) -> dict[str, int]:
    return {row["metric"]: int(row["value"]) for row in rows}


def validate_current(tables: dict[str, list[dict[str, str]]]) -> None:
    sample = tables["sample"]
    relations = tables["relations"]
    amounts = tables["amounts"]
    functions = tables["functions"]
    hr032 = hr032_metrics(tables["hr032"])

    if len(sample) != 43:
        raise ValueError(f"current relation sample must retain 43 rows, got {len(sample)}")

    strict = strict_sample_rows(sample)
    strict_counts = Counter(row["graph_eligibility"] for row in strict)
    if len(strict) != 16 or strict_counts != EXPECTED_STRICT_PANEL_COUNTS:
        raise ValueError(
            f"unexpected F008 strict layer: rows={len(strict)}, counts={strict_counts}"
        )
    if Counter(row["review_status"] for row in strict) != Counter(
        {"human_checked": 8, "human_revised": 8}
    ):
        raise ValueError("F008 strict layer must remain 8 checked + 8 revised")
    if any(row["relation_type"] == "grant_opportunity" for row in strict):
        raise ValueError("grant opportunity entered the F008 reviewed relation layer")

    if len(relations) != 35:
        raise ValueError(f"R10 relations must contain 35 rows, got {len(relations)}")
    relation_reviews = Counter(row["review_status"] for row in relations)
    if relation_reviews != EXPECTED_R10_REVIEW_COUNTS:
        raise ValueError(f"unexpected R10 relation review counts: {relation_reviews}")
    mechanism_counts = Counter(classify_mechanism(row) for row in relations)
    if mechanism_counts != EXPECTED_MECHANISM_COUNTS:
        raise ValueError(f"unexpected R10 mechanism counts: {mechanism_counts}")
    opportunities = [
        row for row in relations if row["relation_type"] == "grant_opportunity"
    ]
    if len(opportunities) != 1 or "opportunity_only_no_award" not in {
        row["financial_semantics"] for row in opportunities
    }:
        raise ValueError("NOFO must remain a single opportunity-only, no-award record")

    if len(amounts) != 28:
        raise ValueError(f"R10 amounts must contain 28 rows, got {len(amounts)}")
    amount_reviews = Counter(row["review_status"] for row in amounts)
    if amount_reviews != EXPECTED_AMOUNT_REVIEW_COUNTS:
        raise ValueError(f"unexpected R10 amount review counts: {amount_reviews}")
    amount_counts = Counter(classify_amount(row) for row in amounts)
    if amount_counts != EXPECTED_AMOUNT_BOUNDARY_COUNTS:
        raise ValueError(f"unexpected R10 amount boundary counts: {amount_counts}")
    actual_contracts = [
        row for row in amounts if row["amount_basis"] == "actual_contract_amount"
    ]
    if len(actual_contracts) != 5:
        raise ValueError("current R10 layer must contain exactly five actual contracts")
    project_costs = [
        row for row in amounts if classify_amount(row) == "项目／事业成本"
    ]
    if len(project_costs) != 14 or any(
        row["actor_payment_status"] != "not_actor_payment" for row in project_costs
    ):
        raise ValueError("all 14 project-cost observations must remain non-payments")
    grant_cost = next(row for row in amounts if row["amount_observation_id"] == "R10AM021")
    if grant_cost["award_status"] != "relation_confirmed_amount_not_award":
        raise ValueError("grant-related project cost was misread as an award amount")

    if len(functions) != 43:
        raise ValueError(f"R10 functions must contain 43 rows, got {len(functions)}")
    function_reviews = Counter(row["review_status"] for row in functions)
    if function_reviews != EXPECTED_FUNCTION_REVIEW_COUNTS:
        raise ValueError(f"unexpected R10 function review counts: {function_reviews}")
    if any(
        row["financial_inference_allowed"] != "no"
        or row["political_stance_inference_allowed"] != "no"
        for row in functions
    ):
        raise ValueError("R10 function rows must not authorize funding or stance inference")

    expected_hr032 = {
        "source_universe_rows_unchanged": 616,
        "identity_crosswalk_rows": 48,
        "member_crosswalk_rows": 5,
        "registry_crosswalk_rows": 3,
        "administrative_relation_edges_approved": 0,
        "amount_allocations_approved": 0,
    }
    if hr032 != expected_hr032:
        raise ValueError(f"unexpected HR032 merge summary: {hr032}")


def escape(value: str) -> str:
    return html.escape(value, quote=True)


def multiline(
    lines: list[str],
    x: int | float,
    y: int | float,
    css_class: str,
    *,
    line_height: int = 21,
    anchor: str = "start",
) -> str:
    spans = "".join(
        f'<tspan x="{x}" dy="{0 if index == 0 else line_height}">'
        f"{escape(line)}</tspan>"
        for index, line in enumerate(lines)
    )
    return (
        f'<text x="{x}" y="{y}" text-anchor="{anchor}" '
        f'class="{css_class}">{spans}</text>'
    )


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
        '<rect width="100%" height="100%" fill="#FAF9F5"/>'
        '<style>'
        'text{font-family:"Noto Sans CJK SC","Microsoft YaHei",Arial,sans-serif;'
        'fill:#17231F}.title{font-size:32px;font-weight:700}.sub{font-size:15px;'
        'fill:#52605A}.head{font-size:18px;font-weight:700}.label{font-size:15px}'
        '.small{font-size:13px;fill:#52605A}.tiny{font-size:12px;fill:#65716C}'
        '.num{font-size:30px;font-weight:700}.count{font-size:19px;font-weight:700}'
        "</style>"
        f'<text x="58" y="55" class="title">{escape(title)}</text>'
        f'<text x="58" y="84" class="sub">{escape(subtitle)}</text>'
        f"{body}</svg>"
    )


def review_counts(rows: list[dict[str, str]]) -> Counter[str]:
    return Counter(row["review_status"] for row in rows)


def render_f008(sample: list[dict[str, str]]) -> str:
    rows = strict_sample_rows(sample)
    panel_order = [
        ("dyadic_relation", "组织—组织关系", "仅此层可进入关系图"),
        ("administrative_record", "行政／recipient 记录", "端点含 program／机构，不是组织边"),
        ("event_participation", "事件级记录", "共同交付不等于稳定联盟"),
        ("research_lead", "面板限定线索", "可查阅，不进入组织关系图"),
    ]
    panel_details = {
        "dyadic_relation": [
            ("成员关系", 5),
            ("直接捐赠", 1),
            ("点名贡献（金额未知）", 1),
        ],
        "administrative_record": [
            ("委托／咨询员记录", 3),
            ("点名实物支持记录", 3),
        ],
        "event_participation": [("共同实物交付事件", 1)],
        "research_lead": [("赞助层级／区域范围有界", 2)],
    }
    fills = ["#D8E9E2", "#DEE6F1", "#F2E1CA", "#E8DCEB"]
    body: list[str] = []
    body.append('<text x="58" y="125" class="num">16</text>')
    body.append(
        '<text x="115" y="122" class="head">条 current E3/E4 reviewed + supported/bounded 记录</text>'
    )
    body.append(
        '<text x="115" y="147" class="small">8 human_checked ＋ 8 human_revised；不沿用旧 38 行 evidence-only 快照</text>'
    )

    for index, (panel, label, boundary) in enumerate(panel_order):
        panel_rows = [row for row in rows if row["graph_eligibility"] == panel]
        reviews = review_counts(panel_rows)
        x = 58 + index * 380
        y = 190
        body.append(
            f'<rect x="{x}" y="{y}" width="350" height="430" rx="16" '
            f'fill="{fills[index]}" stroke="#C9D1CD"/>'
        )
        body.append(f'<text x="{x + 22}" y="{y + 42}" class="head">{escape(label)}</text>')
        body.append(
            f'<text x="{x + 305}" y="{y + 46}" text-anchor="end" '
            f'class="num">{len(panel_rows)}</text>'
        )
        body.append(multiline([boundary], x + 22, y + 76, "small"))
        item_y = y + 128
        for item_label, count in panel_details[panel]:
            body.append(
                f'<circle cx="{x + 30}" cy="{item_y - 5}" r="7" fill="#17624F"/>'
            )
            body.append(
                f'<text x="{x + 49}" y="{item_y}" class="label">'
                f"{escape(item_label)}</text>"
            )
            body.append(
                f'<text x="{x + 315}" y="{item_y}" text-anchor="end" '
                f'class="count">{count}</text>'
            )
            item_y += 52
        body.append(
            f'<line x1="{x + 22}" y1="{y + 327}" x2="{x + 328}" y2="{y + 327}" '
            'stroke="#AEB8B3"/>'
        )
        body.append(
            f'<text x="{x + 22}" y="{y + 360}" class="small">'
            f"checked {reviews['human_checked']} · revised {reviews['human_revised']}</text>"
        )
        e4 = sum(row["evidence_level"] == "E4" for row in panel_rows)
        e3 = sum(row["evidence_level"] == "E3" for row in panel_rows)
        body.append(
            f'<text x="{x + 22}" y="{y + 389}" class="small">E4 {e4} · E3 {e3}</text>'
        )

    body.append(
        '<rect x="58" y="660" width="1482" height="190" rx="14" fill="#FFFFFF" '
        'stroke="#D0D6D2"/>'
    )
    boundary_lines = [
        "NOFO／grant opportunity 只证明机会存在：不等于 award，也不等于已有 recipient；不进入本图关系层。",
        "成员关系不是 funding；service／recipient 记录不产生亲基地或反基地政治立场。",
        "事件参与、共同交付与 co-presence 只保留事件语义；候选或 legacy event-action 不提升为稳定联盟。",
        "图中数量是目的性样本的展示资格，不是影响力、资金规模或总体组织关系数量。",
    ]
    body.append(multiline(boundary_lines, 85, 699, "label", line_height=37))
    return svg_page(
        "F008：严格支持／委托／服务分层（当前层）",
        "关系、行政记录、事件记录与面板线索分开；只有 dyadic_relation 可成为组织—组织边",
        "".join(body),
        width=1600,
        height=900,
        description=(
            "Sixteen reviewed E3/E4 supported or bounded records: seven dyadic "
            "relations, six administrative records, one event record, and two "
            "panel-only research leads."
        ),
    )


def render_f031(
    relations: list[dict[str, str]],
    functions: list[dict[str, str]],
    hr032: list[dict[str, str]],
) -> str:
    order = [
        "行政委托／指定",
        "补助／grant 关系",
        "企业赞助",
        "直接捐赠",
        "实物支持",
        "成员关系",
        "服务存在",
        "活动协作",
        "汇总观察",
        "NOFO／机会",
    ]
    grouped = {
        label: [row for row in relations if classify_mechanism(row) == label]
        for label in order
    }
    status_colors = {
        "human_checked": "#17624F",
        "human_revised": "#C97926",
        "needs_local_retrieval": "#7E8984",
    }
    body: list[str] = []
    legend_x = 980
    for status, label in [
        ("human_checked", "human_checked"),
        ("human_revised", "human_revised"),
        ("needs_local_retrieval", "needs_local"),
    ]:
        body.append(
            f'<rect x="{legend_x}" y="107" width="17" height="17" rx="3" '
            f'fill="{status_colors[status]}"/>'
        )
        body.append(
            f'<text x="{legend_x + 25}" y="121" class="small">{label}</text>'
        )
        legend_x += 185

    left, top, bar_w, bar_h = 350, 160, 1040, 38
    scale = bar_w / 15
    for index, label in enumerate(order):
        y = top + index * 68
        rows = grouped[label]
        body.append(
            f'<text x="58" y="{y + 25}" class="label">{escape(label)}</text>'
        )
        body.append(
            f'<rect x="{left}" y="{y}" width="{bar_w}" height="{bar_h}" rx="7" '
            'fill="#EBEEE9"/>'
        )
        x = left
        counts = review_counts(rows)
        for status in (
            "human_checked",
            "human_revised",
            "needs_local_retrieval",
        ):
            value = counts[status]
            if not value:
                continue
            width = value * scale
            body.append(
                f'<rect x="{x}" y="{y}" width="{width}" height="{bar_h}" rx="7" '
                f'fill="{status_colors[status]}"/>'
            )
            if width >= 40:
                body.append(
                    f'<text x="{x + width / 2}" y="{y + 26}" text-anchor="middle" '
                    'class="label" style="fill:#FFFFFF">'
                    f"{value}</text>"
                )
            x += width
        body.append(
            f'<text x="{left + bar_w + 32}" y="{y + 27}" class="count">{len(rows)}</text>'
        )
        if label == "NOFO／机会":
            body.append(
                f'<text x="{left + 85}" y="{y + 27}" class="small" '
                'style="fill:#17231F">线索；不是 award／recipient</text>'
            )

    metrics = hr032_metrics(hr032)
    body.append(
        '<rect x="58" y="850" width="1482" height="178" rx="14" fill="#FFFFFF" '
        'stroke="#D0D6D2"/>'
    )
    notes = [
        "35 条关系观察＝24 checked＋10 revised＋1 local；横条是机制构成，不是资金流或联盟强度。",
        "43 条功能观察全部标记 financial inference=no、political stance inference=no：service 不产生政治立场。",
        (
            f"HR032 保持 {metrics['source_universe_rows_unchanged']} 条来源总体不变；"
            f"批准新增关系 {metrics['administrative_relation_edges_approved']}、"
            f"金额分配 {metrics['amount_allocations_approved']}。"
        ),
        "活动协作／co-presence 不生成稳定联盟；grant opportunity 不等于 grant award。",
    ]
    body.append(multiline(notes, 85, 887, "label", line_height=34))
    return svg_page(
        "F031：行政与服务生态机制（post-HR018／HR032）",
        "三类人审状态叠加在十类机制上；名称 crosswalk 不生成关系或金额分配",
        "".join(body),
        width=1600,
        height=1080,
        description=(
            "Thirty-five current R10 relation observations grouped into ten "
            "mechanism families and split by human review status."
        ),
    )


def render_f032(amounts: list[dict[str, str]]) -> str:
    current = [
        ("实际合同额", "可写作具名合同；不得拆给 JV 成员"),
        ("点名委托资金流", "点名委托流；其中 1 条仅为部分范围"),
        ("点名现金捐赠", "可写作具名慈善捐赠；不是政治支持"),
        ("项目／事业成本", "不是 actor payment，也不是 contract／award"),
        ("recipient 未解析", "2.196m 的 recipient scope 未解析"),
        ("跨期／混合汇总", "不能拆到单一 recipient／年度"),
        ("实物价值（非现金）", "物品估值，不是现金支付"),
    ]
    counts = Counter(classify_amount(row) for row in amounts)
    strong = {"实际合同额", "点名委托资金流", "点名现金捐赠"}
    colors = {
        "实际合同额": "#17624F",
        "点名委托资金流": "#3D7C6C",
        "点名现金捐赠": "#6F9F92",
        "项目／事业成本": "#C97926",
        "recipient 未解析": "#9D8E78",
        "跨期／混合汇总": "#7E8984",
        "实物价值（非现金）": "#8B6F93",
    }
    body: list[str] = []
    body.append('<text x="58" y="130" class="num">28</text>')
    body.append(
        '<text x="115" y="127" class="head">条金额观察：21 checked＋6 revised＋1 local</text>'
    )
    body.append(
        '<text x="115" y="152" class="small">仅 5 条 amount_basis=actual_contract_amount；币种与口径不跨项求和</text>'
    )
    body.append(
        '<line x1="800" y1="188" x2="800" y2="698" stroke="#B6C0BB" '
        'stroke-width="2" stroke-dasharray="8 7"/>'
    )
    body.append(
        '<text x="58" y="207" class="head">可作具名金额表达</text>'
    )
    body.append(
        '<text x="842" y="207" class="head">只能作背景／边界金额</text>'
    )

    left_index = 0
    right_index = 0
    for label, boundary in current:
        if label in strong:
            x = 58
            y = 240 + left_index * 145
            left_index += 1
        else:
            x = 842
            y = 240 + right_index * 112
            right_index += 1
        count = counts[label]
        card_w = 700
        body.append(
            f'<rect x="{x}" y="{y}" width="{card_w}" height="94" rx="13" '
            f'fill="{colors[label]}" opacity="0.16" stroke="{colors[label]}"/>'
        )
        body.append(
            f'<rect x="{x}" y="{y}" width="10" height="94" rx="5" '
            f'fill="{colors[label]}"/>'
        )
        body.append(
            f'<text x="{x + 28}" y="{y + 37}" class="head">{escape(label)}</text>'
        )
        body.append(
            f'<text x="{x + card_w - 28}" y="{y + 43}" text-anchor="end" '
            f'class="num">{count}</text>'
        )
        body.append(
            f'<text x="{x + 28}" y="{y + 70}" class="small">{escape(boundary)}</text>'
        )

    body.append(
        '<rect x="58" y="735" width="1482" height="185" rx="14" fill="#FFFFFF" '
        'stroke="#D0D6D2"/>'
    )
    notes = [
        "14 条 project／program cost 均为 not_actor_payment；其中 grant 关系相关金额也不是 award 或 paid amount。",
        "NOFO／grant opportunity 没有进入 28 条金额观察：机会公告不证明 award、recipient 或付款。",
        "sponsor tier、service presence、membership 与 co-presence 没有金额时保持空值，不补 0、不估值。",
        "JPY 与 USD 不相加；实物价值不等于现金；事件参与不等于联盟。",
    ]
    body.append(multiline(notes, 85, 772, "label", line_height=36))
    return svg_page(
        "F032：金额证据边界（当前 28 条）",
        "把合同、点名资金流、捐赠与 project cost／aggregate／实物价值分开",
        "".join(body),
        width=1600,
        height=960,
        description=(
            "Twenty-eight reviewed amount observations split into ten named "
            "money observations and eighteen contextual or bounded amounts. "
            "Only five are actual contract amounts."
        ),
    )


def html_page(title: str, svg: str, *, max_width: int = 1600) -> str:
    return (
        "<!doctype html><html lang='zh-CN'><head><meta charset='utf-8'>"
        f"<title>{escape(title)}</title>"
        "<meta name='viewport' content='width=device-width,initial-scale=1'>"
        "<style>body{margin:0;background:#eceae4}"
        f"main{{max-width:{max_width}px;margin:24px auto;background:white;"
        "box-shadow:0 8px 28px #0002}svg{display:block;width:100%;height:auto}"
        "@media(max-width:700px){main{margin:0;box-shadow:none}}</style>"
        "</head><body><main>"
        f"{svg}</main></body></html>"
    )


def render_current(
    phase1_output_dir: Path = PHASE1_OUTPUT_DIR,
    r10_output_dir: Path = R10_OUTPUT_DIR,
) -> set[Path]:
    """Validate current inputs and write only the six declared figure files."""
    tables = load_current()
    validate_current(tables)

    phase1_output_dir = Path(phase1_output_dir)
    r10_output_dir = Path(r10_output_dir)
    phase1_output_dir.mkdir(parents=True, exist_ok=True)
    r10_output_dir.mkdir(parents=True, exist_ok=True)

    figures = [
        (
            phase1_output_dir / "fig3_support_service_layers_strict",
            "F008 current strict relation layers",
            render_f008(tables["sample"]),
        ),
        (
            r10_output_dir / "fig_r10_mechanism_ecology",
            "F031 current R10 mechanism ecology",
            render_f031(
                tables["relations"],
                tables["functions"],
                tables["hr032"],
            ),
        ),
        (
            r10_output_dir / "fig_r10_amount_evidence_boundary",
            "F032 current R10 amount evidence boundary",
            render_f032(tables["amounts"]),
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
        raise ValueError("renderer output set drifted beyond the six declared assets")
    return written


def main() -> None:
    written = render_current()
    print(
        "Current F008/R10 render OK: "
        f"{len(written)} files from strict16 / relations35 / amounts28 / functions43."
    )


if __name__ == "__main__":
    main()
