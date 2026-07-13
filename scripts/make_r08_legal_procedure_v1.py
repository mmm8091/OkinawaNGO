"""Build the HR-014 accepted R8 legal/policy/procedure comparison package.

Reads only the six human-checked cases and 27 accepted role observations.
Writes a normalized role-by-case matrix and explanatory SVG/HTML figures without
creating new case facts or changing central registries.
"""

from __future__ import annotations

import csv
import html
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "interim"
OUT = ROOT / "outputs" / "R08_legal_procedure_v1"
LEGACY_ROLES = ROOT / "outputs" / "R08_legal_procedure_v0" / "case_actor_roles_v0.csv"

CASES = DATA / "17_legal_policy_procedure_cases_v0.csv"
ROLES = DATA / "18_legal_policy_actor_roles_v0.csv"
ACTORS = DATA / "01_actor_registry_initial_v0.csv"
SOURCES = DATA / "05_source_log_initial_v0.csv"

MATRIX = DATA / "30_r08_case_channel_matrix_v1.csv"
CASE_COMPARISON = OUT / "case_channel_result_comparison_v1.csv"
ROLE_COUNTS = OUT / "case_role_family_counts_v1.csv"
RESIDUAL = OUT / "residual_gaps_v1.csv"
BRIEF = OUT / "R08_legal_procedure_brief_v1.md"
REPORT_INSERT = OUT / "report_insert_v1.md"
VALIDATION = OUT / "validation_note_v1.md"
HR026 = OUT / "HR026_status_v0.md"

FLOW_SVG = OUT / "fig_r08_procedure_outputs_v1.svg"
FLOW_HTML = OUT / "fig_r08_procedure_outputs_v1.html"
ROLE_SVG = OUT / "fig_r08_role_boundary_matrix_v1.svg"
ROLE_HTML = OUT / "fig_r08_role_boundary_matrix_v1.html"


ROLE_FAMILIES = [
    "plaintiff",
    "counsel",
    "requester",
    "commenter",
    "supporter",
    "non_party",
    "defendant",
    "proponent",
    "institutional_recipient",
]

MATRIX_FIELDS = [
    "matrix_row_id", "case_id", "case_short_label", "case_name", "place",
    "jurisdiction", "channel_type", "procedure_type", "start_date",
    "end_or_decision_date", "target_actor_or_institution", "controversy_translation",
    "procedural_entry", "role_id", "entity_ref", "entity_boundary", "entity_kind",
    "actor_name", "role", "role_family", "side", "target_or_recipient",
    "observed_procedure_output", "relief_or_disposition", "result_component_1",
    "result_component_2", "result_boundary", "case_source_refs", "role_source_refs",
    "case_evidence_level", "role_evidence_level", "case_review_status",
    "role_review_status", "human_decision", "case_interpretation_limit",
    "role_interpretation_limit",
]

LEGACY_ROLE_FIELDS = [
    "role_id", "case_id", "actor_id", "actor_name", "role", "side",
    "target_or_recipient", "role_evidence_summary", "source_refs", "evidence_level",
    "review_status", "interpretation_limit",
]


CASE_FIELDS = [
    "case_id", "case_short_label", "case_name", "place", "jurisdiction",
    "channel_type", "procedure_type", "controversy_translation", "procedural_entry",
    "role_families_observed", "registered_actor_roles", "provisional_node_roles",
    "target_actor_or_institution", "observed_procedure_output", "relief_or_disposition",
    "result_component_1", "result_component_2", "result_boundary", "primary_source_refs",
    "evidence_level", "review_status",
]


CASE_SPECS = {
    "R8C01": {
        "short": "边野古／大浦湾儒艮",
        "translation": "基地建设与儒艮影响 → 海外文化财程序义务",
        "entry": "美国 NHPA §402／APA 联邦司法审查",
        "output": "形成 Section 402 可审查程序标准与公开记录",
        "disposition": "2020 年维持 DoD 胜诉；没有停止工程",
        "component_1": "程序产出：确认 Section 402 适用并形成可审查标准",
        "component_2": "最终处分：DoD 的 take-into-account 合规判断获维持",
        "boundary": "程序标准／信息生产与最终救济结果必须并列；不是阻止工程的政策效果。",
    },
    "R8C02": {
        "short": "边野古／大浦湾 EIA",
        "translation": "基地建设与生态影响 → 调查、预测、减缓充分性",
        "entry": "日本 EIA 方法书／补正评价书正式意见",
        "output": "NACSJ 的科学批评进入正式行政记录",
        "disposition": "补正 EIA 完成；不证明意见被采纳或工程停止",
        "component_1": "程序产出：2004／2013 正式意见进入 EIA 阶段",
        "component_2": "程序边界：行政机关完成并公布补正评价书",
        "boundary": "commenter、事业者和审查／收件机关不可合并；提交意见不等于采纳。",
    },
    "R8C03": {
        "short": "第三次嘉手纳噪音",
        "translation": "航空器噪音与日常负担 → 人格／生活损害",
        "entry": "日本民事差止与过去／未来损害赔偿诉讼",
        "output": "符合条件的过去噪音损害赔偿获维持",
        "disposition": "运营／噪音差止及未来损害请求被驳回",
        "component_1": "获得：部分过去损害赔偿",
        "component_2": "未获得：差止与未来损害救济",
        "boundary": "赔偿不表示噪音停止；A052 不代表所有个体或其他轮次成员恒定。",
    },
    "R8C04": {
        "short": "普天间周边噪音",
        "translation": "航空器噪音与睡眠／健康负担 → 期间损害",
        "entry": "2018／2020 并合损害赔偿诉讼",
        "output": "法院命令日本向列名原告赔偿指定期间损害",
        "disposition": "其余请求被驳回；没有形成运营禁令",
        "component_1": "获得：部分原告、部分期间的损害赔偿",
        "component_2": "未获得：其余请求；本案不处理运营差止",
        "boundary": "A053 是案件特定 plaintiff group；并合案与其他轮次不等于人员完全相同。",
    },
    "R8C05": {
        "short": "石垣部署住民投票",
        "translation": "陆自部署争议 → 地方自治与住民投票实施义务",
        "entry": "条例请求后进入不作为违法确认／义务付诉讼",
        "output": "法院明确了义务付诉讼的行政处分门槛",
        "disposition": "因住民投票实施不属可义务付处分而全部驳回",
        "component_1": "前置步骤：条例请求与议会否决",
        "component_2": "司法处分：mandatory-order actions 程序性驳回",
        "boundary": "A011 是 requester／campaign body，不是具名组织原告；议会与市长步骤分开。",
    },
    "R8C06": {
        "short": "泡濑公金支出",
        "translation": "填海生态／经济／灾害风险 → 公共支出合法性与合理性",
        "entry": "住民监查与地方自治法公金支出差止诉讼",
        "output": "两波诉讼把生态争议转化为支出与裁量审查",
        "disposition": "第一波限制支出；第二波居民在上诉／最高裁阶段未获支持",
        "component_1": "第一波：无合理修订计划时限制未来支出",
        "component_2": "第二波：居民上诉败诉，2017 年上告／申请被驳回",
        "boundary": "两波相反结果必须分列；A055、A020 均为 supporter，不是本案组织原告／counsel。",
    },
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def split_refs(value: str) -> list[str]:
    return [item.strip() for item in value.replace("|", ";").split(";") if item.strip()]


def unique_join(values: list[str]) -> str:
    return ";".join(dict.fromkeys(value for value in values if value))


def canonicalize_registered_actor_names(
    roles: list[dict[str, str]], actors_by_id: dict[str, dict[str, str]],
) -> list[dict[str, str]]:
    """Use the central registry canonical name for every registered-actor role.

    Role facts remain case-specific.  This only prevents an older alias captured
    during HR-014 seeding from leaking into current R8 display products.
    """
    normalized: list[dict[str, str]] = []
    for source_row in roles:
        row = dict(source_row)
        if row["actor_id"]:
            actor = actors_by_id.get(row["actor_id"])
            if actor is None:
                raise ValueError(f"actor FK missing: {row['role_id']}")
            row["actor_name"] = actor["canonical_name"]
        normalized.append(row)
    return normalized


def sync_legacy_role_actor_names(actors_by_id: dict[str, dict[str, str]]) -> None:
    """Keep the accepted HR-014 v0 role table aligned with registry canonicals."""
    legacy_rows = read_csv(LEGACY_ROLES)
    for row in legacy_rows:
        if row["actor_id"]:
            actor = actors_by_id.get(row["actor_id"])
            if actor is None:
                raise ValueError(f"legacy actor FK missing: {row['role_id']}")
            row["actor_name"] = actor["canonical_name"]
    write_csv(LEGACY_ROLES, legacy_rows, LEGACY_ROLE_FIELDS)
    if read_csv(LEGACY_ROLES) != legacy_rows:
        raise ValueError("legacy R8 role CSV roundtrip mismatch")


def build_case_comparison(
    cases: list[dict[str, str]], roles: list[dict[str, str]]
) -> list[dict[str, str]]:
    roles_by_case: dict[str, list[dict[str, str]]] = defaultdict(list)
    for role in roles:
        roles_by_case[role["case_id"]].append(role)
    rows: list[dict[str, str]] = []
    for case in cases:
        spec = CASE_SPECS[case["case_id"]]
        case_roles = roles_by_case[case["case_id"]]
        family_counts = Counter(row["role_family"] for row in case_roles)
        family_summary = ";".join(
            f"{family}:{family_counts[family]}" for family in ROLE_FAMILIES if family_counts[family]
        )
        rows.append(
            {
                "case_id": case["case_id"],
                "case_short_label": spec["short"],
                "case_name": case["case_name"],
                "place": case["place"],
                "jurisdiction": case["jurisdiction"],
                "channel_type": case["channel_type"],
                "procedure_type": case["procedure_type"],
                "controversy_translation": spec["translation"],
                "procedural_entry": spec["entry"],
                "role_families_observed": family_summary,
                "registered_actor_roles": str(sum(bool(row["actor_id"]) for row in case_roles)),
                "provisional_node_roles": str(sum(bool(row["provisional_entity_id"]) for row in case_roles)),
                "target_actor_or_institution": case["target_actor_or_institution"],
                "observed_procedure_output": spec["output"],
                "relief_or_disposition": spec["disposition"],
                "result_component_1": spec["component_1"],
                "result_component_2": spec["component_2"],
                "result_boundary": spec["boundary"],
                "primary_source_refs": case["primary_source_refs"],
                "evidence_level": case["evidence_level"],
                "review_status": case["review_status"],
            }
        )
    return rows


def build_matrix(
    cases: list[dict[str, str]], roles: list[dict[str, str]]
) -> list[dict[str, str]]:
    case_by_id = {row["case_id"]: row for row in cases}
    rows: list[dict[str, str]] = []
    for index, role in enumerate(roles, start=1):
        case = case_by_id[role["case_id"]]
        spec = CASE_SPECS[role["case_id"]]
        entity_ref = role["actor_id"] or role["provisional_entity_id"]
        rows.append(
            {
                "matrix_row_id": f"R8M{index:03d}",
                "case_id": case["case_id"],
                "case_short_label": spec["short"],
                "case_name": case["case_name"],
                "place": case["place"],
                "jurisdiction": case["jurisdiction"],
                "channel_type": case["channel_type"],
                "procedure_type": case["procedure_type"],
                "start_date": case["start_date"],
                "end_or_decision_date": case["end_or_decision_date"],
                "target_actor_or_institution": case["target_actor_or_institution"],
                "controversy_translation": spec["translation"],
                "procedural_entry": spec["entry"],
                "role_id": role["role_id"],
                "entity_ref": entity_ref,
                "entity_boundary": "registered_actor" if role["actor_id"] else "provisional_procedural_node",
                "entity_kind": role["entity_kind"],
                "actor_name": role["actor_name"],
                "role": role["role"],
                "role_family": role["role_family"],
                "side": role["side"],
                "target_or_recipient": role["target_or_recipient"],
                "observed_procedure_output": spec["output"],
                "relief_or_disposition": spec["disposition"],
                "result_component_1": spec["component_1"],
                "result_component_2": spec["component_2"],
                "result_boundary": spec["boundary"],
                "case_source_refs": case["primary_source_refs"],
                "role_source_refs": role["source_refs"],
                "case_evidence_level": case["evidence_level"],
                "role_evidence_level": role["evidence_level"],
                "case_review_status": case["review_status"],
                "role_review_status": role["review_status"],
                "human_decision": role["human_decision"],
                "case_interpretation_limit": case["interpretation_limit"],
                "role_interpretation_limit": role["interpretation_limit"],
            }
        )
    return rows


def build_role_counts(roles: list[dict[str, str]]) -> list[dict[str, str]]:
    counts = Counter((row["case_id"], row["role_family"]) for row in roles)
    rows: list[dict[str, str]] = []
    for case_id in CASE_SPECS:
        for family in ROLE_FAMILIES:
            rows.append(
                {
                    "case_id": case_id,
                    "case_short_label": CASE_SPECS[case_id]["short"],
                    "role_family": family,
                    "accepted_role_count": str(counts[(case_id, family)]),
                    "cell_semantics": "accepted HR-014 role observations; zero means no accepted role row in this case",
                }
            )
    return rows


def residual_rows() -> list[dict[str, str]]:
    return [
        {
            "gap_id": "R8G01", "case_id": "R8C03", "gap_type": "case_number_locator_detail",
            "detail": "The accepted Third Kadena comparison does not normalize every district/appellate case number into the central case row.",
            "blocking": "no", "safe_current_boundary": "Use the accepted case family, claims, roles and appellate result; do not infer cross-round person identity.",
            "next_route": "Online: refine the official judgment title/case-number locator if a publication table later requires it."
        },
        {
            "gap_id": "R8G02", "case_id": "R8C05", "gap_type": "phase_locator_detail",
            "detail": "R8R021 counsel evidence is limited to the related later status-confirmation phase, not every claim in the 2020 mandatory-order judgment.",
            "blocking": "no", "safe_current_boundary": "Keep the accepted phase-specific counsel limit and never generalize it to all Ishigaki claims.",
            "next_route": "Online: add pleading/phase locators only if a finer procedural chronology is commissioned."
        },
        {
            "gap_id": "R8G03", "case_id": "R8C06", "gap_type": "subcase_locator_detail",
            "detail": "The accepted case registry keeps the first and second Awase waves in one case family rather than separate subcase IDs.",
            "blocking": "no", "safe_current_boundary": "Keep the two accepted outcome components separate; do not collapse them into one win/loss label.",
            "next_route": "Online: split subcase IDs and normalize each case number/date only for later court-level chronology."
        },
    ]


def esc(value: object) -> str:
    return html.escape(str(value))


def multiline(x: int, y: int, lines: list[str], css: str = "body", gap: int = 21) -> str:
    spans = "".join(
        f'<tspan x="{x}" dy="{0 if index == 0 else gap}">{esc(line)}</tspan>'
        for index, line in enumerate(lines)
    )
    return f'<text x="{x}" y="{y}" class="{css}">{spans}</text>'


def render_flow(case_rows: list[dict[str, str]]) -> str:
    y0, row_h = 165, 180
    body = []
    columns = [(35, 250, "争议／地点"), (300, 300, "程序入口"), (615, 300, "已审角色"), (930, 250, "制度对象"), (1195, 455, "可观察程序产出／边界")]
    for x, width, label in columns:
        body.append(f'<text x="{x + 10}" y="128" class="col">{esc(label)}</text>')
        body.append(f'<line x1="{x}" y1="140" x2="{x + width}" y2="140" class="rule"/>')
    for index, row in enumerate(case_rows):
        y = y0 + index * row_h
        body.append(f'<rect x="25" y="{y - 18}" width="1640" height="162" rx="12" class="lane"/>')
        body.append(multiline(45, y + 10, [row["case_short_label"], row["place"]], "case", 25))
        entry_parts = row["procedural_entry"].replace("／", "／|").split("|")
        body.append(multiline(310, y + 8, entry_parts[:3], "body", 21))
        role_lines = [item.replace(":", " × ") for item in row["role_families_observed"].split(";")]
        body.append(multiline(625, y + 5, role_lines[:5], "body", 20))
        target = row["target_actor_or_institution"].replace("; ", "| ").split("|")
        body.append(multiline(940, y + 8, target[:4], "body", 20))
        if row["case_id"] == "R8C06":
            body.append('<rect x="1205" y="%d" width="435" height="48" rx="8" class="out-a"/>' % (y - 3))
            body.append(multiline(1220, y + 16, [row["result_component_1"]], "small", 18))
            body.append('<rect x="1205" y="%d" width="435" height="48" rx="8" class="out-b"/>' % (y + 55))
            body.append(multiline(1220, y + 74, [row["result_component_2"]], "small", 18))
        else:
            body.append(multiline(1210, y + 4, [row["observed_procedure_output"], row["relief_or_disposition"]], "body", 22))
        body.append(multiline(310, y + 105, ["制度转译：" + row["controversy_translation"]], "limit", 18))
        body.append(multiline(1210, y + 105, [row["result_boundary"]], "limit", 18))
    height = y0 + len(case_rows) * row_h + 40
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1690" height="{height}" viewBox="0 0 1690 {height}" role="img" aria-labelledby="flow-title flow-desc">
<title id="flow-title">R8 六案如何进入不同程序并产生不同程序产出</title>
<desc id="flow-desc">Six horizontal case lanes compare controversy and place, procedural entry, accepted roles, institutional target, and observed procedural output. The ordering is explanatory, not causal.</desc>
<rect width="1690" height="{height}" fill="#f3f0e8"/>
<style>text{{font-family:"Noto Sans CJK SC","Microsoft YaHei",Arial,sans-serif;fill:#17312b}}.title{{font-size:31px;font-weight:700}}.sub{{font-size:14px;fill:#5d6a65}}.col{{font-size:16px;font-weight:700}}.rule{{stroke:#8d9b96;stroke-width:1}}.lane{{fill:#fffdf8;stroke:#d4d0c5}}.case{{font-size:15px;font-weight:700}}.body{{font-size:13px}}.small{{font-size:12px}}.limit{{font-size:11px;fill:#6b5a3c}}.out-a{{fill:#d8e8df}}.out-b{{fill:#eadccb}}</style>
<text x="35" y="48" class="title">R8：争议如何进入程序，程序产出是什么</text>
<text x="35" y="77" class="sub">六案均为 HR-014 human_checked；横向顺序表示制度转译的比较框架，不是因果链，也不是胜败排行榜。</text>
<rect x="35" y="91" width="1625" height="27" rx="7" fill="#efe2c6"/><text x="48" y="110" class="limit">角色必须按案件读取：plaintiff / counsel / requester / commenter / supporter / non_party / institutional node 不可互换。</text>
{''.join(body)}</svg>'''


def render_role_matrix(role_rows: list[dict[str, str]]) -> str:
    counts = Counter((row["case_id"], row["role_family"]) for row in role_rows)
    registered = Counter(row["case_id"] for row in role_rows if row["actor_id"])
    provisional = Counter(row["case_id"] for row in role_rows if row["provisional_entity_id"])
    short = {case_id: spec["short"] for case_id, spec in CASE_SPECS.items()}
    x0, y0, cell_w, cell_h = 330, 165, 125, 92
    labels = {
        "plaintiff": "plaintiff", "counsel": "counsel", "requester": "requester",
        "commenter": "commenter", "supporter": "supporter", "non_party": "non_party",
        "defendant": "defendant", "proponent": "proponent", "institutional_recipient": "recipient",
    }
    body = []
    for col, family in enumerate(ROLE_FAMILIES):
        x = x0 + col * cell_w
        body.append(f'<text x="{x + cell_w/2}" y="138" text-anchor="middle" class="head">{labels[family]}</text>')
    for row_index, case_id in enumerate(CASE_SPECS):
        y = y0 + row_index * cell_h
        body.append(f'<text x="35" y="{y + 30}" class="case">{esc(case_id)} · {esc(short[case_id])}</text>')
        body.append(f'<text x="35" y="{y + 55}" class="mini">registered {registered[case_id]} / provisional {provisional[case_id]}</text>')
        for col, family in enumerate(ROLE_FAMILIES):
            x = x0 + col * cell_w
            value = counts[(case_id, family)]
            css = "active" if value else "empty"
            body.append(f'<rect x="{x + 10}" y="{y}" width="105" height="64" rx="9" class="{css}"/>')
            body.append(f'<text x="{x + 62.5}" y="{y + 41}" text-anchor="middle" class="num {css}-text">{value}</text>')
    notes_y = y0 + len(CASE_SPECS) * cell_h + 25
    notes = [
        "Dugong：A002／A019 = non_party；A020 = plaintiff；A009 = counsel。",
        "石垣：A011 = requester，匿名居民／署名者为 plaintiff；不得把组织升级为原告。",
        "泡濑：A055／A020 = supporter；A020 的 Dugong plaintiff 身份不跨案继承。",
        "provisional procedural node 用于个人、匿名居民集合、律师集合和公机构；它们不是 registry actor。",
    ]
    for index, note in enumerate(notes):
        body.append(f'<text x="35" y="{notes_y + index * 25}" class="note">{esc(note)}</text>')
    height = notes_y + len(notes) * 25 + 35
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1510" height="{height}" viewBox="0 0 1510 {height}" role="img" aria-labelledby="role-title role-desc">
<title id="role-title">R8 accepted case-role family matrix</title><desc id="role-desc">Counts of 27 HR-014 accepted roles across six cases and nine strict role families, with registered and provisional entity boundaries.</desc>
<rect width="1510" height="{height}" fill="#f3f0e8"/>
<style>text{{font-family:"Noto Sans CJK SC","Microsoft YaHei",Arial,sans-serif;fill:#17312b}}.title{{font-size:30px;font-weight:700}}.sub{{font-size:14px;fill:#5d6a65}}.head{{font-size:12px;font-weight:700}}.case{{font-size:14px;font-weight:700}}.mini{{font-size:12px;fill:#64716c}}.active{{fill:#2b7764}}.empty{{fill:#fffdf8;stroke:#d5d1c6}}.num{{font-size:21px;font-weight:700}}.active-text{{fill:#fff}}.empty-text{{fill:#a7aca9}}.note{{font-size:13px;fill:#5d4c2e}}</style>
<text x="35" y="48" class="title">R8：六案角色 family 与主体边界</text>
<text x="35" y="76" class="sub">单元格是 accepted role observation 数，不是组织影响力；同一 actor 的角色必须按 case_id 读取。</text>
{''.join(body)}</svg>'''


def html_page(title: str, svg: str) -> str:
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)}</title><style>body{{margin:0;background:#e8e5dd}}main{{max-width:1700px;margin:20px auto;box-shadow:0 8px 28px #0002}}svg{{display:block;width:100%;height:auto}}@media(max-width:700px){{main{{margin:0;box-shadow:none}}}}</style></head><body><main>{svg}</main></body></html>'''


def report_paragraph() -> str:
    return """冲绳的基地与开发争议并非进入同一种法律渠道，而是依争议对象和可用制度被转译为不同程序问题。边野古／大浦湾的儒艮与生态知识分别进入美国 NHPA Section 402／APA 审查和日本环境影响评价意见程序；嘉手纳与普天间的航空器噪音则被表达为人格、生活与期间损害；石垣的陆自部署争议进入住民投票条例请求和义务付诉讼；泡濑的填海生态、经济与灾害风险进入公共支出合法性与合理性审查。六案的程序产出不能用统一胜败概括：Dugong 案形成可审查标准与公开记录但最终维持 DoD 胜诉，EIA 意见进入记录却不等于被采纳，噪音案确认部分既往损害但没有形成运营禁令，石垣案因行政处分门槛被程序性驳回，泡濑第一波限制未来支出而第二波在上诉与最高法院阶段未获支持。相应地，原告、律师、请求者、评论者、非当事支持者和制度节点必须分开编码；A002／A019 在 Dugong 案是 non-party，A011 在石垣案是 requester，A020 仅在 Dugong 案是 plaintiff、在泡濑案则是 supporter。"""


def render_brief(
    case_rows: list[dict[str, str]], role_rows: list[dict[str, str]], residual: list[dict[str, str]]
) -> str:
    family_counts = Counter(row["role_family"] for row in role_rows)
    entity_counts = Counter("registered actor" if row["actor_id"] else "provisional procedural node" for row in role_rows)
    return f"""# R8 法律／政策／环境程序比较包 v1

日期：2026-07-13

## 验收结论

本包只读取 HR-014 已完成的 **6 个 human_checked 案例／程序**和 **27 个 human_checked、accept 角色**。它回答的不是“哪一案胜率更高”，而是：不同争议如何被转译进不同制度渠道，谁以何种案件特定角色进入，以及程序实际留下了什么产出与未提供什么救济。

27 个角色中，{entity_counts['registered actor']} 条使用 registry actor 外键，{entity_counts['provisional procedural node']} 条使用案件内 provisional procedural node。角色 family 为：{'; '.join(f'{family} {family_counts[family]}' for family in ROLE_FAMILIES if family_counts[family])}。

## 六案比较

1. **Dugong／美国法律**：生态与文化财主张进入 NHPA §402／APA 审查。程序形成可审查标准和公开记录，但 2020 年最终维持 DoD 胜诉，没有停止工程。
2. **边野古 EIA**：NACSJ 以 commenter 身份把珊瑚礁、儒艮、调查与预测充分性写入正式意见；提交不等于采纳，程序完成也不等于工程停止。
3. **第三次嘉手纳**：居民把噪音转译为差止与损害请求；过去损害赔偿获维持，运营／噪音差止和未来损害请求未获支持。
4. **普天间周边噪音**：两个并合行动确认部分原告、部分期间的损害赔偿并驳回其余请求；本案不产生运营禁令。
5. **石垣住民投票**：部署争议经条例请求进入义务付诉讼，法院因住民投票实施不属可义务付的行政处分而驳回；这是程序门槛，不是对地方自治政治价值的总体判断。
6. **泡濑公金支出**：第一波在无合理修订计划时限制未来支出，第二波居民在上诉与最高法院阶段未获支持。两波结果相反，必须分列。

## 强制角色边界

- A002、A019 在 R8C01 均为 `non_party`，不继承相关个人或外围倡议的原告身份。
- A020 在 R8C01 是 `plaintiff`，在 R8C06 是 `supporter`／正式材料承载者；不得跨案泛化为 plaintiff 或 counsel。
- A009 在 R8C01 是 `counsel`，不是 named plaintiff。
- A011 在 R8C05 是 `requester`，不是 named organizational plaintiff。
- A055 在 R8C06 是 `supporter`，不是组织原告或 counsel。
- A052／A053 是各自案件特定的 `plaintiff_group` crosswalk；不得推断个体成员或轮次人员恒定。
- P8E004 第三次嘉手纳 counsel 继续是 provisional procedural collective，不进入 actor registry。

## 图表读法

`fig_r08_procedure_outputs_v1` 按“争议／地点—程序入口—已审角色—制度对象—程序产出／边界”并列六案。横向排列是解释框架，不是因果箭头。`fig_r08_role_boundary_matrix_v1` 只显示 27 条 accepted role observation 的 family 计数，并同时标出 registered/provisional 数量；零表示当前没有 accepted role row，不表示该角色在现实中绝对不存在。

## Residual gaps 与 HR-026

当前 {len(residual)} 项 residual gap 都是非阻断的案号、phase locator 或泡濑 subcase 细化问题，不改变六案、27 角色或已审结果边界。本轮不创建 HR-026：没有需要新增人类判断的事实或角色；如未来要求审级级时间线，再按 `residual_gaps_v1.csv` 补精确 locator。

## 可直接写入报告

> {report_paragraph()}
"""


def validate(
    cases: list[dict[str, str]], roles: list[dict[str, str]], matrix: list[dict[str, str]],
    comparison: list[dict[str, str]], counts: list[dict[str, str]], source_ids: set[str],
    actors_by_id: dict[str, dict[str, str]],
) -> None:
    if len(cases) != 6 or {row["case_id"] for row in cases} != set(CASE_SPECS):
        raise ValueError("R8 v1 requires exactly the six HR-014 cases")
    if any(row["review_status"] != "human_checked" for row in cases):
        raise ValueError("non-human-checked case entered R8 v1")
    if len(roles) != 27 or len({row["role_id"] for row in roles}) != 27:
        raise ValueError("R8 v1 requires 27 unique roles")
    if any(row["review_status"] != "human_checked" or row["human_decision"] != "accept" for row in roles):
        raise ValueError("non-accepted role entered R8 v1")
    if any(row["case_id"] not in CASE_SPECS for row in roles):
        raise ValueError("role has invalid case FK")
    for row in roles:
        if bool(row["actor_id"]) == bool(row["provisional_entity_id"]):
            raise ValueError(f"role must have exactly one entity reference: {row['role_id']}")
        if row["actor_id"] and row["actor_id"] not in actors_by_id:
            raise ValueError(f"actor FK missing: {row['role_id']}")
        if row["actor_id"] and row["actor_name"] != actors_by_id[row["actor_id"]]["canonical_name"]:
            raise ValueError(f"stale actor display name: {row['role_id']}")
        if not set(split_refs(row["source_refs"])).issubset(source_ids):
            raise ValueError(f"role source FK missing: {row['role_id']}")
    for row in cases:
        if not set(split_refs(row["primary_source_refs"])).issubset(source_ids):
            raise ValueError(f"case source FK missing: {row['case_id']}")
    if len(matrix) != 27 or len(comparison) != 6 or len(counts) != 54:
        raise ValueError("R8 output row counts are incomplete")

    role_lookup = {(row["case_id"], row["actor_id"]): row for row in roles if row["actor_id"]}
    for actor_id in ("A002", "A019"):
        if role_lookup[("R8C01", actor_id)]["role_family"] != "non_party":
            raise ValueError(f"{actor_id} must remain non-party in Dugong case")
    if role_lookup[("R8C01", "A020")]["role_family"] != "plaintiff":
        raise ValueError("A020 must be plaintiff in R8C01")
    if role_lookup[("R8C06", "A020")]["role_family"] != "supporter":
        raise ValueError("A020 must be supporter in R8C06")
    if role_lookup[("R8C01", "A009")]["role_family"] != "counsel":
        raise ValueError("A009 must be counsel in R8C01")
    if role_lookup[("R8C05", "A011")]["role_family"] != "requester":
        raise ValueError("A011 must be requester in R8C05")
    if role_lookup[("R8C06", "A055")]["role_family"] != "supporter":
        raise ValueError("A055 must be supporter in R8C06")
    p8e004 = next(row for row in roles if row["provisional_entity_id"] == "P8E004")
    if p8e004["role_family"] != "counsel" or p8e004["actor_id"]:
        raise ValueError("P8E004 must remain provisional counsel")
    awase = next(row for row in comparison if row["case_id"] == "R8C06")
    if not ("第一波" in awase["result_component_1"] and "第二波" in awase["result_component_2"]):
        raise ValueError("Awase wave outcomes were collapsed")
    if awase["result_component_1"] == awase["result_component_2"]:
        raise ValueError("Awase wave outcomes must remain distinct")


def main() -> None:
    cases = read_csv(CASES)
    actors_by_id = {row["actor_id"]: row for row in read_csv(ACTORS)}
    roles = canonicalize_registered_actor_names(read_csv(ROLES), actors_by_id)
    source_ids = {row["source_id"] for row in read_csv(SOURCES)}

    comparison = build_case_comparison(cases, roles)
    matrix = build_matrix(cases, roles)
    counts = build_role_counts(roles)
    residual = residual_rows()
    validate(cases, roles, matrix, comparison, counts, source_ids, actors_by_id)
    sync_legacy_role_actor_names(actors_by_id)

    OUT.mkdir(parents=True, exist_ok=True)
    write_csv(MATRIX, matrix, MATRIX_FIELDS)
    write_csv(CASE_COMPARISON, comparison, CASE_FIELDS)
    write_csv(ROLE_COUNTS, counts, ["case_id", "case_short_label", "role_family", "accepted_role_count", "cell_semantics"])
    write_csv(RESIDUAL, residual, ["gap_id", "case_id", "gap_type", "detail", "blocking", "safe_current_boundary", "next_route"])

    flow_svg = render_flow(comparison)
    role_svg = render_role_matrix(roles)
    FLOW_SVG.write_text(flow_svg, encoding="utf-8")
    FLOW_HTML.write_text(html_page("R8 procedure outputs", flow_svg), encoding="utf-8")
    ROLE_SVG.write_text(role_svg, encoding="utf-8")
    ROLE_HTML.write_text(html_page("R8 role boundary matrix", role_svg), encoding="utf-8")
    BRIEF.write_text(render_brief(comparison, roles, residual), encoding="utf-8")
    REPORT_INSERT.write_text("# R8 报告插入段落\n\n" + report_paragraph() + "\n", encoding="utf-8")
    HR026.write_text(
        "# R8 module-local historical status note — not the global HR-026 task\n\n"
        "R8 本轮当时未创建新的人工任务：六案与 27 个角色全部来自已完成的 HR-014；"
        "三项 residual gap 仅涉及非阻断的案号、phase locator 或 subcase 粒度，不需要新的关系／角色判断。\n\n"
        "此文件只记录 **R8 模块当时的局部状态**，不能解释为全项目‘没有 HR-026’。"
        "全局 HR-026 后续已分配给 R9 三届县知事选—市民组织接口，共 19 项；权威任务文件为 "
        "`outputs/R09_election_civic_interface_v1/HR026_election_civic_role_review_v0.csv`，"
        "总导航见 `docs/human_review_tasks_v0.md`。\n",
        encoding="utf-8",
    )

    family_counts = Counter(row["role_family"] for row in roles)
    entity_counts = Counter("registered_actor" if row["actor_id"] else "provisional_node" for row in roles)
    VALIDATION.write_text(
        "# Validation note v1\n\n"
        f"- Cases: {len(cases)}; all human_checked.\n"
        f"- Roles: {len(roles)}; all human_checked + accept.\n"
        f"- Entity boundary: {entity_counts['registered_actor']} registered actor roles; {entity_counts['provisional_node']} provisional procedural-node roles.\n"
        f"- Role families: {unique_join([f'{family}={family_counts[family]}' for family in ROLE_FAMILIES if family_counts[family]])}.\n"
        f"- Normalized matrix: {len(matrix)} rows; case comparison: {len(comparison)} rows; role-family grid: {len(counts)} cells.\n"
        "- Hard boundaries checked: A002/A019 non_party; A020 cross-case role split; A009 counsel; A011 requester; A055 supporter; P8E004 provisional counsel.\n"
        "- Awase first/second waves remain separate; no win-rate or causal-effect encoding.\n"
        f"- Residual gaps: {len(residual)}, all non-blocking; no HR-026 created.\n",
        encoding="utf-8",
    )

    if read_csv(MATRIX) != matrix or read_csv(CASE_COMPARISON) != comparison or read_csv(ROLE_COUNTS) != counts:
        raise ValueError("R8 v1 CSV roundtrip mismatch")
    print(
        f"R8 v1 OK: {len(cases)} cases; {len(roles)} accepted roles; "
        f"{len(matrix)} matrix rows; {len(counts)} role-family cells"
    )


if __name__ == "__main__":
    main()
