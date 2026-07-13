"""Build the auditable online-evidence-safe layer for R4 Sakishima framing.

Inputs are the candidate package and its independent QA dispositions.  Only
QA-safe actor/frame observations enter the formal fact table.  Semantic-human
and rejected candidates are emitted to separate queues/logs.
"""

from __future__ import annotations

import csv
import html
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "outputs" / "R04_sakishima_frame_corpus_v0"
DATA = ROOT / "data" / "interim"

CANDIDATES = MODULE / "actor_frame_event_candidates_v0.csv"
ACTOR_DISPOSITIONS = MODULE / "corrected_actor_frame_event_dispositions_v0.csv"
SOURCES = MODULE / "source_excerpt_locators_v0.csv"
SOURCE_DISPOSITIONS = MODULE / "corrected_source_excerpt_dispositions_v0.csv"

FORMAL_FACTS = DATA / "19_sakishima_frame_corpus_v0.csv"
SAFE_SOURCES = MODULE / "online_evidence_safe_sources_v0.csv"
HUMAN_QUEUE = MODULE / "human_review_queue_v0.csv"
REJECT_LOG = MODULE / "reject_log_v0.csv"
SOURCE_HUMAN_QUEUE = MODULE / "source_review_queue_v0.csv"
SOURCE_REJECT_LOG = MODULE / "source_reject_log_v0.csv"
MATRIX = MODULE / "three_place_safe_source_matrix_v0.csv"
SVG = MODULE / "fig_r4_three_place_frames_v0.svg"
HTML = MODULE / "fig_r4_three_place_frames_v0.html"
ENTITY_MATRIX = MODULE / "entity_frame_safe_matrix_v0.csv"
ENTITY_SVG = MODULE / "fig_r4_entity_frame_matrix_v0.svg"
ENTITY_HTML = MODULE / "fig_r4_entity_frame_matrix_v0.html"
BRIEF = MODULE / "R04_online_evidence_brief_v1.md"
NOTE = MODULE / "formalization_note_v0.md"

SAFE_ACTOR_STATUS = {"safe_merge"}
HUMAN_ACTOR_STATUS = {"human_semantic_review"}
REJECT_ACTOR_STATUS = {"reject", "reject_current_evidence"}
SAFE_SOURCE_STATUS = {"safe_merge", "safe_with_correction"}
HUMAN_SOURCE_STATUS = {"human_semantic_review", "human_locator_review"}
REJECT_SOURCE_STATUS = {"reject_current_locator"}

PLACE_OVERRIDE = {"R4S021": "Sakishima"}
FACT_SOURCE_EXCLUDE = {
    # Locator remains human-pending; R4E007 remains supported by R4S006/R4S009.
    "R4E007": {"R4S007"},
}
FACT_LIMIT_OVERRIDE = {
    "R4E007": (
        "Only the statutory plan and verified public Q&A are used here; the R4S007 "
        "pattern-page locator remains outside the formal fact. Planning scenarios are not events."
    ),
    "R4E018": (
        "The report names the referendum committee and chair for the 2015 vote only; "
        "it does not establish long-term organizational continuity or authorize later expansion."
    ),
}

FRAME_ORDER = [
    ("groundwater_life_safety", "地下水／饮用水"),
    ("local_autonomy_referendum", "自治／公投"),
    ("frontline_taiwan_evacuation", "前线／台湾邻近／撤离"),
    ("life_safety", "健康／生活安全"),
    ("environment_deployment", "环境—部署连接"),
]
PLACE_ORDER = ["Miyako", "Ishigaki", "Yonaguni"]
PLACE_ZH = {"Miyako": "宫古", "Ishigaki": "石垣", "Yonaguni": "与那国"}
FRAME_CODE_ORDER = ["F_GW", "F_AUT", "F_FTE", "F_LIFE", "F_ENV"]
FRAME_CODE_ZH = {
    "F_GW": "地下水／饮用水",
    "F_AUT": "自治／公投",
    "F_FTE": "前线／台湾／撤离",
    "F_LIFE": "健康／生活安全",
    "F_ENV": "环境—部署",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows({field: row.get(field, "") for field in fields} for row in rows)


def split_refs(value: str) -> list[str]:
    return [item.strip() for item in value.split(";") if item.strip()]


def corrected(base: dict[str, str], disposition: dict[str, str]) -> dict[str, str]:
    row = dict(base)
    for field in ("date_or_period", "locator", "excerpt_short", "frame_candidates"):
        value = disposition.get(f"corrected_{field}", "").strip()
        if value:
            row[field] = value
    row["place"] = PLACE_OVERRIDE.get(row["corpus_source_id"], row["place"])
    row["qa_disposition"] = disposition["qa_disposition"]
    row["qa_reason"] = disposition["qa_reason"]
    return row


def build_safe_sources(
    sources: list[dict[str, str]], dispositions: dict[str, dict[str, str]]
) -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]]:
    safe: list[dict[str, str]] = []
    human: list[dict[str, str]] = []
    rejected: list[dict[str, str]] = []
    for source in sources:
        source_id = source["corpus_source_id"]
        row = corrected(source, dispositions[source_id])
        row["review_status"] = (
            "qa_safe_online_source"
            if row["qa_disposition"] in SAFE_SOURCE_STATUS
            else "needs_human_review"
            if row["qa_disposition"] in HUMAN_SOURCE_STATUS
            else "rejected_current_evidence"
        )
        row["interpretation_limit"] = row["human_review_note"]
        if row["qa_disposition"] in SAFE_SOURCE_STATUS:
            safe.append(row)
        elif row["qa_disposition"] in HUMAN_SOURCE_STATUS:
            human.append(row)
        elif row["qa_disposition"] in REJECT_SOURCE_STATUS:
            rejected.append(row)
        else:
            raise ValueError(f"unknown source disposition on {source_id}")
    return safe, human, rejected


def join_source_field(
    source_ids: list[str], sources: dict[str, dict[str, str]], field: str
) -> str:
    values: list[str] = []
    for source_id in source_ids:
        value = sources[source_id].get(field, "").strip()
        if value and value not in values:
            values.append(value)
    return ";".join(values)


def build_actor_outputs(
    candidates: list[dict[str, str]],
    dispositions: dict[str, dict[str, str]],
    safe_sources: dict[str, dict[str, str]],
) -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]]:
    facts: list[dict[str, str]] = []
    human: list[dict[str, str]] = []
    rejected: list[dict[str, str]] = []

    for candidate in candidates:
        fact_id = candidate["candidate_edge_id"]
        disposition = dispositions[fact_id]
        status = disposition["qa_disposition"]
        merged = dict(candidate)
        for target, correction in (
            ("actor_id_or_provisional", "corrected_actor_id_or_provisional"),
            ("place", "corrected_place"),
            ("frame_code", "corrected_frame_code"),
            ("corpus_source_ids", "corrected_corpus_source_ids"),
        ):
            if disposition.get(correction, "").strip():
                merged[target] = disposition[correction].strip()
        merged["qa_disposition"] = status
        merged["qa_reason"] = disposition["qa_reason"]

        if status in SAFE_ACTOR_STATUS:
            refs = [
                ref
                for ref in split_refs(merged["corpus_source_ids"])
                if ref not in FACT_SOURCE_EXCLUDE.get(fact_id, set())
            ]
            if not refs:
                raise ValueError(f"safe fact {fact_id} has no safe source")
            if any(ref not in safe_sources for ref in refs):
                bad = [ref for ref in refs if ref not in safe_sources]
                raise ValueError(f"safe fact {fact_id} cites non-safe sources: {bad}")

            facts.append(
                {
                    "fact_id": fact_id,
                    "fact_scope": "online_frame_observation",
                    "place": merged["place"],
                    "entity_id_or_provisional": merged["actor_id_or_provisional"],
                    "entity_name": merged["actor_name"],
                    "entity_status": merged["actor_status"],
                    "event_or_document": merged["event_or_document"],
                    "event_year": merged["event_year"],
                    "frame_code": merged["frame_code"],
                    "frame_label": merged["frame_label"],
                    "relation_basis": merged["relation_basis"],
                    "source_ref": ";".join(refs),
                    "existing_source_ids": join_source_field(refs, safe_sources, "existing_source_id"),
                    "source_urls": join_source_field(refs, safe_sources, "url"),
                    "source_locator_summary": " | ".join(
                        f"{ref}: {safe_sources[ref]['locator']}" for ref in refs
                    ),
                    "evidence_level": merged["evidence_level"],
                    "review_status": "qa_safe_online",
                    "human_review_required": "no",
                    "interpretation_limit": FACT_LIMIT_OVERRIDE.get(
                        fact_id, merged["interpretation_limit"]
                    ),
                    "relationship_limit": (
                        "Frame observation only; not a stable-alliance, support, or causal claim."
                    ),
                }
            )
        elif status in HUMAN_ACTOR_STATUS:
            merged["required_decision"] = "accept/revise/reject"
            merged["queue_status"] = "needs_human_semantic_review"
            human.append(merged)
        elif status in REJECT_ACTOR_STATUS:
            merged["reject_status"] = "excluded_from_formal_fact_table"
            rejected.append(merged)
        else:
            raise ValueError(f"unknown actor disposition on {fact_id}")
    return facts, human, rejected


def build_matrix(safe_sources: list[dict[str, str]]) -> list[dict[str, str]]:
    grouped: dict[tuple[str, str], list[str]] = defaultdict(list)
    for source in safe_sources:
        if source["place"] not in PLACE_ORDER:
            continue
        for frame in split_refs(source["frame_candidates"]):
            grouped[(source["place"], frame)].append(source["corpus_source_id"])

    rows: list[dict[str, str]] = []
    for place in PLACE_ORDER:
        for frame, label in FRAME_ORDER:
            source_ids = sorted(grouped[(place, frame)])
            rows.append(
                {
                    "place": place,
                    "place_zh": PLACE_ZH[place],
                    "frame_label": frame,
                    "frame_label_zh": label,
                    "safe_source_count": str(len(source_ids)),
                    "corpus_source_ids": ";".join(source_ids),
                    "measurement_scope": (
                        "QA-safe online source excerpts in this R4 package; not local prevalence."
                    ),
                }
            )
    return rows


def build_entity_matrix(facts: list[dict[str, str]]) -> list[dict[str, str]]:
    grouped: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    entity_order: list[tuple[str, str]] = []
    for fact in facts:
        key = (fact["entity_id_or_provisional"], fact["entity_name"])
        if key not in entity_order:
            entity_order.append(key)
        grouped[key].append(fact)

    rows: list[dict[str, str]] = []
    for entity_id, entity_name in entity_order:
        entity_facts = grouped[(entity_id, entity_name)]
        statuses = {fact["entity_status"] for fact in entity_facts}
        if statuses == {"existing_actor"}:
            category = "registry_actor"
        elif statuses == {"external_institution"}:
            category = "external_institution"
        else:
            category = "provisional_entity"
        counts = Counter(fact["frame_code"] for fact in entity_facts)
        rows.append(
            {
                "entity_id_or_provisional": entity_id,
                "entity_name": entity_name,
                "entity_category": category,
                "places": ";".join(dict.fromkeys(fact["place"] for fact in entity_facts)),
                **{f"{code}_count": str(counts[code]) for code in FRAME_CODE_ORDER},
                "safe_fact_count": str(len(entity_facts)),
                "fact_ids": ";".join(fact["fact_id"] for fact in entity_facts),
                "interpretation_limit": (
                    "Cells count QA-safe frame observations for this entity; they do not encode "
                    "co-occurrence, inter-entity ties, stable alliances, or political agreement."
                ),
            }
        )
    return rows


def render_svg(matrix: list[dict[str, str]], facts: list[dict[str, str]]) -> str:
    counts = {(row["place"], row["frame_label"]): int(row["safe_source_count"]) for row in matrix}
    fact_counts = Counter(row["place"] for row in facts)
    width, height = 1420, 830
    left, top, cell_w, cell_h = 300, 185, 205, 118
    colors = ["#F5F2EA", "#DCEBE4", "#B8D8C9", "#7DB9A2", "#3D8D74", "#17624F", "#0B473A"]

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#FAF9F5"/>',
        '<style>text{font-family:"Noto Sans CJK SC","Microsoft YaHei",Arial,sans-serif;fill:#17231F}.title{font-size:30px;font-weight:700}.sub{font-size:15px;fill:#52605A}.head{font-size:16px;font-weight:700}.place{font-size:24px;font-weight:700}.num{font-size:30px;font-weight:700}.small{font-size:13px;fill:#52605A}.call{font-size:15px}</style>',
        '<text x="60" y="58" class="title">先岛三地：线上安全语料中的框架可见度</text>',
        '<text x="60" y="88" class="sub">数值 = 本包 QA-safe source excerpt 数；不是当地真实动员规模，也不证明未出现议题不存在</text>',
    ]

    for index, (_, label) in enumerate(FRAME_ORDER):
        x = left + index * cell_w + cell_w / 2
        label_lines = label.split("／")
        parts.append(f'<text x="{x}" y="130" text-anchor="middle" class="head">')
        for line_no, line in enumerate(label_lines[:3]):
            parts.append(f'<tspan x="{x}" dy="{0 if line_no == 0 else 21}">{html.escape(line)}</tspan>')
        parts.append("</text>")

    for row_index, place in enumerate(PLACE_ORDER):
        y = top + row_index * cell_h
        parts.append(
            f'<text x="60" y="{y + 45}" class="place">{PLACE_ZH[place]}</text>'
            f'<text x="60" y="{y + 72}" class="small">正式安全事实 {fact_counts[place]} 条</text>'
        )
        for col_index, (frame, _) in enumerate(FRAME_ORDER):
            value = counts[(place, frame)]
            x = left + col_index * cell_w
            color = colors[min(value, len(colors) - 1)]
            parts.extend(
                [
                    f'<rect x="{x + 5}" y="{y}" width="{cell_w - 12}" height="{cell_h - 12}" rx="12" fill="{color}" stroke="#FFFFFF" stroke-width="3"/>',
                    f'<text x="{x + cell_w / 2}" y="{y + 63}" text-anchor="middle" class="num" style="fill:{("#FFFFFF" if value >= 4 else "#17231F")}">{value}</text>',
                ]
            )

    callouts = [
        ("宫古", "水源／饮用水最具地方物质性；部署—地下水的组织 crosswalk 仍在人审队列。"),
        ("石垣", "自治／公投呈现最完整的制度事实链，同时出现撤离中的医疗、运输与补偿问题。"),
        ("与那国", "主轴是台湾邻近、前线监视、自治／公投与岛外撤离；生活安全嵌入救援和安置。"),
    ]
    base_y = 585
    for index, (place, text_value) in enumerate(callouts):
        y = base_y + index * 55
        parts.append(f'<circle cx="76" cy="{y - 5}" r="7" fill="#C46A45"/>')
        parts.append(f'<text x="96" y="{y}" class="call"><tspan font-weight="700">{place}：</tspan>{html.escape(text_value)}</text>')
    parts.append(
        '<text x="60" y="790" class="small">与那国“环境—部署连接”计数为 0，仅表示本包安全语料尚未出现具名直接连接，不得写成环境关切不存在。</text>'
    )
    parts.append("</svg>")
    return "".join(parts)


def render_entity_svg(rows: list[dict[str, str]], facts: list[dict[str, str]]) -> str:
    width, height = 1500, 1120
    left, top, cell_w, row_h = 485, 190, 182, 93
    registry_color = "#DCEBE4"
    institution_color = "#F2E2C8"
    provisional_color = "#E4E5E4"
    category_colors = {
        "registry_actor": registry_color,
        "external_institution": institution_color,
        "provisional_entity": provisional_color,
    }
    category_labels = {
        "registry_actor": "registry actor",
        "external_institution": "external institution",
        "provisional_entity": "provisional entity",
    }
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#FAF9F5"/>',
        '<style>text{font-family:"Noto Sans CJK SC","Microsoft YaHei",Arial,sans-serif;fill:#17231F}.title{font-size:30px;font-weight:700}.sub{font-size:15px;fill:#52605A}.head{font-size:16px;font-weight:700}.name{font-size:16px;font-weight:700}.meta{font-size:12px;fill:#59655F}.num{font-size:24px;font-weight:700}.note{font-size:14px;fill:#394740}</style>',
        '<text x="55" y="55" class="title">R4 组织／制度节点 × 议题框架（线上安全事实）</text>',
        '<text x="55" y="85" class="sub">单元格 = 该实体的 QA-safe 框架观察数；不表示实体之间的共现、合作或稳定联盟</text>',
    ]
    for index, code in enumerate(FRAME_CODE_ORDER):
        x = left + index * cell_w + cell_w / 2
        lines = FRAME_CODE_ZH[code].split("／")
        parts.append(f'<text x="{x}" y="135" text-anchor="middle" class="head">')
        for line_no, line in enumerate(lines):
            parts.append(f'<tspan x="{x}" dy="{0 if line_no == 0 else 20}">{html.escape(line)}</tspan>')
        parts.append("</text>")

    for row_index, row in enumerate(rows):
        y = top + row_index * row_h
        color = category_colors[row["entity_category"]]
        parts.append(f'<rect x="45" y="{y - 16}" width="1400" height="{row_h - 8}" rx="10" fill="{color}" opacity="0.68"/>')
        parts.append(f'<text x="65" y="{y + 13}" class="name">{html.escape(row["entity_name"])}</text>')
        parts.append(
            f'<text x="65" y="{y + 38}" class="meta">{html.escape(row["entity_id_or_provisional"])} · '
            f'{category_labels[row["entity_category"]]} · {html.escape(row["places"])}</text>'
        )
        for col_index, code in enumerate(FRAME_CODE_ORDER):
            value = int(row[f"{code}_count"])
            x = left + col_index * cell_w
            fill = "#17624F" if value else "#FFFFFF"
            text_color = "#FFFFFF" if value else "#A5ADA9"
            parts.append(f'<rect x="{x + 13}" y="{y - 6}" width="{cell_w - 26}" height="56" rx="9" fill="{fill}" stroke="#D2D6D3"/>')
            parts.append(
                f'<text x="{x + cell_w / 2}" y="{y + 31}" text-anchor="middle" class="num" style="fill:{text_color}">{value}</text>'
            )

    legend_y = top + len(rows) * row_h + 22
    legends = [
        (registry_color, "registry actor：2 个；仅 A014 的 2015 公投事件与 A016 的 2024 停训请求"),
        (institution_color, "external institution：6 个；当前安全事实明显由制度节点主导"),
        (provisional_color, "provisional entity：正式表 0 个；相关候选仅保留在人审队列"),
    ]
    for index, (color, label) in enumerate(legends):
        y = legend_y + index * 38
        parts.append(f'<rect x="65" y="{y - 17}" width="25" height="25" rx="5" fill="{color}" stroke="#C5CAC7"/>')
        parts.append(f'<text x="105" y="{y + 2}" class="note">{html.escape(label)}</text>')
    registry_facts = sum(1 for fact in facts if fact["entity_status"] == "existing_actor")
    institutional_facts = len(facts) - registry_facts
    parts.append(
        f'<text x="65" y="{height - 40}" class="sub">事实构成：registry actor {registry_facts}/{len(facts)}；external institution {institutional_facts}/{len(facts)}。制度节点主导是当前线上证据边界，不是民间组织不活跃的结论。</text>'
    )
    parts.append("</svg>")
    return "".join(parts)


def render_brief(
    facts: list[dict[str, str]],
    safe_sources: list[dict[str, str]],
    matrix: list[dict[str, str]],
    human_count: int,
    reject_count: int,
) -> str:
    matrix_counts = {(r["place"], r["frame_label"]): int(r["safe_source_count"]) for r in matrix}
    fact_counts = Counter(row["place"] for row in facts)
    source_counts = Counter(row["place"] for row in safe_sources)
    registry_facts = [row for row in facts if row["entity_status"] == "existing_actor"]
    institution_facts = [row for row in facts if row["entity_status"] == "external_institution"]
    registry_entities = {row["entity_id_or_provisional"] for row in registry_facts}
    institution_entities = {row["entity_id_or_provisional"] for row in institution_facts}
    return f"""# R4 先岛三地框架：线上证据安全层 brief

日期：2026-07-13
口径：仅使用 QA-safe 或已按源文完成机械性纠正、无需新增人工语义判断的记录。

## 结论

三地不是同一种“环保反部署”模式。

- **宫古**：安全语料首先显示地下水／饮用水作为地方生活条件，以及国民保护／撤离制度。部署反对与地下水的直接新闻连接存在于 R4S003，但其 6・11 执委会是否等同 A012 尚待人工 crosswalk，因此没有写成正式 actor 事实。
- **石垣**：最强的是住民投票、条例审议和市民意思确认所形成的自治制度链；同时，撤离决议把医疗、交通、补偿和残留人员问题带入生活安全。失效的 R4S012 没有用于组织归属。
- **与那国**：主框架是台湾邻近／前线监视、安全环境、自治与 2015 公投，以及撤离、救援、接收安置所体现的健康／生活安全。防卫省材料仅代表防卫机构自我框架，不代表居民共识；本模块不把与那国强塞进环境阻工框架。

## 可审核规模

- 正式安全事实：**{len(facts)}** 条（宫古 {fact_counts['Miyako']}、石垣 {fact_counts['Ishigaki']}、与那国 {fact_counts['Yonaguni']}）。
- QA-safe source excerpts：**{len(safe_sources)}** 条（宫古 {source_counts['Miyako']}、石垣 {source_counts['Ishigaki']}、与那国 {source_counts['Yonaguni']}；另有先岛区域级 {source_counts['Sakishima']} 条）。
- semantic-human queue：**{human_count}** 条，不进入正式事实表。
- reject log：**{reject_count}** 条，不进入正式事实表。

## 三地差异的证据读法

图中数字是安全 source excerpt 的框架标签计数：

- 宫古：地下水／饮用水 {matrix_counts[('Miyako', 'groundwater_life_safety')]}；前线／撤离 {matrix_counts[('Miyako', 'frontline_taiwan_evacuation')]}。
- 石垣：自治／公投 {matrix_counts[('Ishigaki', 'local_autonomy_referendum')]}；前线／撤离 {matrix_counts[('Ishigaki', 'frontline_taiwan_evacuation')]}；生活安全 {matrix_counts[('Ishigaki', 'life_safety')]}。
- 与那国：前线／台湾邻近／撤离 {matrix_counts[('Yonaguni', 'frontline_taiwan_evacuation')]}；自治／公投 {matrix_counts[('Yonaguni', 'local_autonomy_referendum')]}；生活安全 {matrix_counts[('Yonaguni', 'life_safety')]}；环境—部署直接连接 {matrix_counts[('Yonaguni', 'environment_deployment')]}。

这些数字衡量的是**本包限定线上语料的公开可见度**，不是现实中的组织数量、动员强度或居民态度分布。**语料未出现不等于议题不存在。**

## 组织／制度节点 × 框架图的解释

1. 11 条正式事实中，registry actor 只有 **{len(registry_facts)}** 条、涉及 **{len(registry_entities)}** 个主体；external institution 有 **{len(institution_facts)}** 条、涉及 **{len(institution_entities)}** 个制度节点。当前安全层明显由政府、议会和防卫机构材料主导，这是线上可核证据的结构边界，不是民间组织不活跃的结论。
2. registry actor 的安全行只覆盖 A014 的 2015 公投事件和 A016 的 2024 停止联合训练请求。它们证明特定事件中的公开角色，不证明两者彼此合作、形成联盟或代表当地全部意见。
3. provisional entity 在正式矩阵中为 0；6・11 集会执行委员会、具名议员和匿名居民等仍留在 semantic-human queue。第二张图因此展示的是“谁的框架能安全归属”，而不是把待审主体补齐后的完整组织生态。

## 可以讲的结论

1. 宫古的地方差异来自地下水依赖如何把安全问题落到饮用水和生活条件，但组织归属仍要区分政策背景、新闻事件与持续组织。
2. 石垣的解释力主要来自自治程序本身：签名、条例审议、两次否决和市议会要求形成制度链；这不等于法院匿名原告可回指 A011。
3. 与那国的证据集中于台湾邻近和前线位置如何转化为监视、扩编说明、岛外撤离、救援与接收训练；2015 公投只支持当时事件，不能授权后续全部扩编。
4. 本包没有找到与那国“具名主体＋部署事件＋明确环境对象”的安全直接证据。只能写“尚未证实”，不能写“没有环境问题”。

## 不可以讲的结论

- 不把共同出现、同一会议或同一议题写成稳定联盟。
- 不把政府计划、说明会或训练写成居民同意、实际能力已验证或政策已落实。
- 不把具名议员、匿名居民或行政答复聚合成整个议会／全体居民立场。
- 不把一般环境组织的生态功能自动编码成反部署。
- 不把与那国归入单一环境阻工叙事。

## 文件关系

- 正式事实表：`data/interim/19_sakishima_frame_corpus_v0.csv`
- 安全来源表：`online_evidence_safe_sources_v0.csv`
- 待人审：`human_review_queue_v0.csv`
- 拒绝记录：`reject_log_v0.csv`
- 三地比较图：`fig_r4_three_place_frames_v0.svg` / `.html`
- 组织／制度节点 × 框架矩阵：`entity_frame_safe_matrix_v0.csv`
- 组织／制度节点 × 框架图：`fig_r4_entity_frame_matrix_v0.svg` / `.html`
"""


def validate(
    candidates: list[dict[str, str]],
    actor_dispositions: dict[str, dict[str, str]],
    sources: list[dict[str, str]],
    source_dispositions: dict[str, dict[str, str]],
    facts: list[dict[str, str]],
    safe_sources: list[dict[str, str]],
    human: list[dict[str, str]],
    rejected: list[dict[str, str]],
    source_human: list[dict[str, str]],
    source_rejected: list[dict[str, str]],
    matrix: list[dict[str, str]],
    entity_matrix: list[dict[str, str]],
) -> None:
    def require(condition: bool, message: str) -> None:
        if not condition:
            raise ValueError(message)

    require(len(candidates) == 26, f"expected 26 actor candidates, found {len(candidates)}")
    require(len(actor_dispositions) == 26, "actor disposition coverage must be complete")
    require(len(sources) == 25, f"expected 25 source candidates, found {len(sources)}")
    require(len(source_dispositions) == 25, "source disposition coverage must be complete")
    require((len(facts), len(human), len(rejected)) == (11, 7, 8), "actor 11/7/8 split failed")
    require(
        (len(safe_sources), len(source_human), len(source_rejected)) == (19, 5, 1),
        "source 19/5/1 split failed",
    )
    fact_ids = {row["fact_id"] for row in facts}
    require(len(fact_ids) == len(facts), "duplicate formal fact ID")
    require(
        fact_ids.isdisjoint({row["candidate_edge_id"] for row in human + rejected}),
        "human/rejected candidate leaked into formal facts",
    )
    safe_source_ids = {row["corpus_source_id"] for row in safe_sources}
    for fact in facts:
        refs = split_refs(fact["source_ref"])
        require(bool(refs), f"fact {fact['fact_id']} lacks source_ref")
        require(set(refs).issubset(safe_source_ids), f"fact {fact['fact_id']} has unsafe source")
        require(bool(fact["source_urls"]), f"fact {fact['fact_id']} lacks traceable URL")
        require(
            fact["relationship_limit"].startswith("Frame observation only"),
            f"fact {fact['fact_id']} lacks relation boundary",
        )
    source_log_ids = {
        row["source_id"] for row in read_csv(DATA / "05_source_log_initial_v0.csv")
    }
    for source in safe_sources:
        require(bool(source["url"]), f"source {source['corpus_source_id']} lacks URL")
        if source["existing_source_id"]:
            require(
                source["existing_source_id"] in source_log_ids,
                f"unknown existing source ID {source['existing_source_id']}",
            )
    require(len(matrix) == 15, "three-place matrix must have 15 cells")
    counts = {(row["place"], row["frame_label"]): int(row["safe_source_count"]) for row in matrix}
    require(
        counts[("Yonaguni", "frontline_taiwan_evacuation")]
        > counts[("Yonaguni", "local_autonomy_referendum")]
        > counts[("Yonaguni", "environment_deployment")],
        "Yonaguni framing hierarchy is not preserved",
    )
    require(counts[("Yonaguni", "life_safety")] > 0, "Yonaguni life-safety evidence missing")
    require(counts[("Yonaguni", "environment_deployment")] == 0, "Yonaguni forced into environment frame")
    require(
        next(row for row in safe_sources if row["corpus_source_id"] == "R4S021")["place"]
        == "Sakishima",
        "regional R4S021 must not be counted as Yonaguni-only",
    )
    require(len(entity_matrix) == 8, "entity/frame matrix must contain eight safe entities")
    category_counts = Counter(row["entity_category"] for row in entity_matrix)
    require(category_counts["registry_actor"] == 2, "expected two registry actors")
    require(category_counts["external_institution"] == 6, "expected six external institutions")
    require(category_counts["provisional_entity"] == 0, "provisional entity leaked into formal matrix")
    represented_facts: list[str] = []
    matrix_cell_sum = 0
    for row in entity_matrix:
        represented_facts.extend(split_refs(row["fact_ids"]))
        matrix_cell_sum += sum(int(row[f"{code}_count"]) for code in FRAME_CODE_ORDER)
        require(
            "not encode co-occurrence" in row["interpretation_limit"],
            "entity matrix lacks non-alliance boundary",
        )
    require(sorted(represented_facts) == sorted(row["fact_id"] for row in facts), "entity matrix fact coverage mismatch")
    require(matrix_cell_sum == len(facts), "entity matrix cell total must equal formal fact count")


def main() -> None:
    candidates = read_csv(CANDIDATES)
    actor_dispositions = {
        row["candidate_edge_id"]: row for row in read_csv(ACTOR_DISPOSITIONS)
    }
    sources = read_csv(SOURCES)
    source_dispositions = {
        row["corpus_source_id"]: row for row in read_csv(SOURCE_DISPOSITIONS)
    }

    safe_sources, source_human, source_rejected = build_safe_sources(
        sources, source_dispositions
    )
    safe_source_map = {row["corpus_source_id"]: row for row in safe_sources}
    facts, human, rejected = build_actor_outputs(
        candidates, actor_dispositions, safe_source_map
    )
    matrix = build_matrix(safe_sources)
    entity_matrix = build_entity_matrix(facts)
    validate(
        candidates,
        actor_dispositions,
        sources,
        source_dispositions,
        facts,
        safe_sources,
        human,
        rejected,
        source_human,
        source_rejected,
        matrix,
        entity_matrix,
    )

    fact_fields = [
        "fact_id", "fact_scope", "place", "entity_id_or_provisional", "entity_name",
        "entity_status", "event_or_document", "event_year", "frame_code", "frame_label",
        "relation_basis", "source_ref", "existing_source_ids", "source_urls",
        "source_locator_summary", "evidence_level", "review_status",
        "human_review_required", "interpretation_limit", "relationship_limit",
    ]
    source_fields = list(safe_sources[0].keys())
    candidate_queue_fields = list(human[0].keys())
    reject_fields = list(rejected[0].keys())
    source_queue_fields = list(source_human[0].keys())
    source_reject_fields = list(source_rejected[0].keys())
    matrix_fields = list(matrix[0].keys())
    entity_matrix_fields = list(entity_matrix[0].keys())

    write_csv(FORMAL_FACTS, fact_fields, facts)
    write_csv(SAFE_SOURCES, source_fields, safe_sources)
    write_csv(HUMAN_QUEUE, candidate_queue_fields, human)
    write_csv(REJECT_LOG, reject_fields, rejected)
    write_csv(SOURCE_HUMAN_QUEUE, source_queue_fields, source_human)
    write_csv(SOURCE_REJECT_LOG, source_reject_fields, source_rejected)
    write_csv(MATRIX, matrix_fields, matrix)
    write_csv(ENTITY_MATRIX, entity_matrix_fields, entity_matrix)

    svg = render_svg(matrix, facts)
    SVG.write_text(svg, encoding="utf-8")
    HTML.write_text(
        "<!doctype html><html lang='zh-CN'><head><meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width,initial-scale=1'>"
        "<title>R4 先岛三地框架比较</title><style>body{margin:0;background:#eceae4}"
        "main{max-width:1420px;margin:24px auto;background:white;box-shadow:0 8px 28px #0002}"
        "svg{display:block;width:100%;height:auto}</style></head><body><main>"
        + svg
        + "</main></body></html>",
        encoding="utf-8",
    )
    entity_svg = render_entity_svg(entity_matrix, facts)
    ENTITY_SVG.write_text(entity_svg, encoding="utf-8")
    ENTITY_HTML.write_text(
        "<!doctype html><html lang='zh-CN'><head><meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width,initial-scale=1'>"
        "<title>R4 组织／制度节点 × 框架</title><style>body{margin:0;background:#eceae4}"
        "main{max-width:1500px;margin:24px auto;background:white;box-shadow:0 8px 28px #0002}"
        "svg{display:block;width:100%;height:auto}</style></head><body><main>"
        + entity_svg
        + "</main></body></html>",
        encoding="utf-8",
    )
    BRIEF.write_text(
        render_brief(facts, safe_sources, matrix, len(human), len(rejected)),
        encoding="utf-8",
    )
    NOTE.write_text(
        f"""# R4 formalization note

Generated by `python scripts/make_r04_sakishima_formal.py` on 2026-07-13.

- Formal QA-safe facts: {len(facts)}
- Semantic-human queue: {len(human)}
- Rejected actor candidates: {len(rejected)}
- QA-safe source excerpts: {len(safe_sources)}
- Source locator/speaker review queue: {len(source_human)}
- Rejected source locators: {len(source_rejected)}
- Entity/frame matrix: 8 entities (2 registry actors; 6 external institutions; 0 provisional)

The formal table contains frame observations, not stable alliances. Source-level
counts measure visibility in this bounded online corpus; absence is not proof
that a frame or issue does not exist locally. No actor registry, source log, or
control document is modified by the generator.
""",
        encoding="utf-8",
    )

    # Re-read the formal CSVs to catch malformed columns or row loss.
    formal_roundtrip = read_csv(FORMAL_FACTS)
    source_roundtrip = read_csv(SAFE_SOURCES)
    entity_matrix_roundtrip = read_csv(ENTITY_MATRIX)
    require = lambda condition, message: condition or (_ for _ in ()).throw(ValueError(message))
    require(formal_roundtrip == facts, "formal fact CSV roundtrip mismatch")
    require(source_roundtrip == safe_sources, "safe source CSV roundtrip mismatch")
    require(entity_matrix_roundtrip == entity_matrix, "entity matrix CSV roundtrip mismatch")
    require(str(len(facts)) in BRIEF.read_text(encoding="utf-8"), "brief count mismatch")
    require(str(len(facts)) in svg, "SVG fact count missing")
    require("2/11" in entity_svg and "9/11" in entity_svg, "entity SVG composition mismatch")
    print(
        "R4 formalization OK: 11 formal facts; 7 human-review; 8 rejected; "
        "19 safe sources; 5 source-review; 1 rejected locator."
    )


if __name__ == "__main__":
    main()
