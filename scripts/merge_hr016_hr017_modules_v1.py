from __future__ import annotations

"""Apply the principal's HR-016 and online HR-017 decisions to module layers.

This is a bounded, deterministic merge.  It does not touch the actor registry
or central source log.  HR-016 speaker/source decisions are materialized in
R04's formal fact and safe-source layers.  Only the nine online HR-017 items
enter R09's formal stage/role layers; the nine local-retrieval items remain
open in the review queue.
"""

import csv
import sys
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

R04 = Path("outputs/R04_sakishima_frame_corpus_v0")
R09 = Path("outputs/R09_referendum_process_v0")
OVERLAY = Path("outputs/principal_review_merge_v1/principal_decision_overlay_v1.csv")

R04_FACTS = Path("data/interim/19_sakishima_frame_corpus_v0.csv")
R09_STAGES = Path("data/interim/20_referendum_process_stages_v0.csv")

HR016_FACT_IDS = {
    "R4E001",
    "R4E008",
    "R4E009",
    "R4E009A",
    "R4E009B",
    "R4E016",
    "R4E017",
    "R4E024",
    "R4E025",
}
HR016_SOURCE_IDS = {"R4S002", "R4S007", "R4S008", "R4S015", "R4S024"}
HR017_ONLINE_STAGE_IDS = {
    "R9ST027",
    "R9ST028",
    "R9ST030",
    "R9ST031",
    "R9ST032",
}
HR017_ONLINE_ROLE_IDS = {"R9R001", "R9R030", "R9R031", "R9R034"}
HR017_LOCAL_OPEN_IDS = {
    "R9ST007",
    "R9ST010",
    "R9ST012",
    "R9ST033",
    "R9R006",
    "R9R007",
    "R9R008",
    "R9R020",
    "R9R029",
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
FRAME_CODES = ["F_GW", "F_AUT", "F_FTE", "F_LIFE", "F_ENV"]


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows({field: row.get(field, "") for field in fields} for row in rows)


def ensure_fields(fields: list[str], additions: list[str]) -> list[str]:
    return fields + [field for field in additions if field not in fields]


def split_refs(value: str) -> list[str]:
    return [item.strip() for item in value.split(";") if item.strip()]


def merge_note(existing: str, fixed: str) -> str:
    return fixed if not existing or "HR-017" in existing else f"{existing} | {fixed}"


def load_overlays(root: Path) -> tuple[dict[str, dict[str, str]], dict[str, dict[str, str]]]:
    _, rows = read_csv(root / OVERLAY)
    hr016 = {row["object_id"]: row for row in rows if row["task_family"] == "HR016"}
    hr017 = {
        row["object_id"]: row
        for row in rows
        if row["task_family"] == "HR017_ONLINE"
    }
    if set(hr016) != {f"HR016-{index:03d}" for index in range(1, 13)}:
        raise ValueError("HR-016 overlay must contain the principal's 12 completed decisions")
    if set(hr017) != HR017_ONLINE_STAGE_IDS | HR017_ONLINE_ROLE_IDS:
        raise ValueError("HR-017 overlay must contain exactly the nine online decisions")
    return hr016, hr017


def source_trace(
    source_refs: str, safe_sources: dict[str, dict[str, str]]
) -> tuple[str, str, str]:
    refs = split_refs(source_refs)
    existing: list[str] = []
    urls: list[str] = []
    locators: list[str] = []
    for source_id in refs:
        source = safe_sources[source_id]
        if source.get("existing_source_id") and source["existing_source_id"] not in existing:
            existing.append(source["existing_source_id"])
        if source["url"] not in urls:
            urls.append(source["url"])
        locators.append(f"{source_id}: {source['locator']}")
    return ";".join(existing), ";".join(urls), " | ".join(locators)


def make_r04_fact(
    safe_sources: dict[str, dict[str, str]],
    *,
    fact_id: str,
    place: str,
    entity_id: str,
    entity_name: str,
    entity_status: str,
    event_or_document: str,
    event_year: str,
    frame_code: str,
    frame_label: str,
    relation_basis: str,
    source_ref: str,
    evidence_level: str,
    interpretation_limit: str,
) -> dict[str, str]:
    existing_ids, urls, locator_summary = source_trace(source_ref, safe_sources)
    return {
        "fact_id": fact_id,
        "fact_scope": "human_reviewed_frame_observation",
        "place": place,
        "entity_id_or_provisional": entity_id,
        "entity_name": entity_name,
        "entity_status": entity_status,
        "event_or_document": event_or_document,
        "event_year": event_year,
        "frame_code": frame_code,
        "frame_label": frame_label,
        "relation_basis": relation_basis,
        "source_ref": source_ref,
        "existing_source_ids": existing_ids,
        "source_urls": urls,
        "source_locator_summary": locator_summary,
        "evidence_level": evidence_level,
        "review_status": "human_revised",
        "human_review_required": "no",
        "interpretation_limit": interpretation_limit,
        "relationship_limit": (
            "Frame observation only; not a stable-alliance, support, actor-identity, "
            "resident-consensus, or causal claim."
        ),
    }


def build_r04_matrix(sources: list[dict[str, str]]) -> list[dict[str, str]]:
    grouped: dict[tuple[str, str], list[str]] = defaultdict(list)
    for source in sources:
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
                        "Human-reviewed/QA-safe online excerpts in this R4 package; "
                        "not local prevalence."
                    ),
                }
            )
    return rows


def build_r04_entity_matrix(facts: list[dict[str, str]]) -> list[dict[str, str]]:
    grouped: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    order: list[tuple[str, str]] = []
    for fact in facts:
        key = (fact["entity_id_or_provisional"], fact["entity_name"])
        if key not in grouped:
            order.append(key)
        grouped[key].append(fact)
    rows: list[dict[str, str]] = []
    for entity_id, entity_name in order:
        entity_facts = grouped[(entity_id, entity_name)]
        statuses = {row["entity_status"] for row in entity_facts}
        if statuses == {"existing_actor"}:
            category = "registry_actor"
        elif statuses == {"external_institution"}:
            category = "external_institution"
        else:
            category = "provisional_entity"
        counts = Counter(row["frame_code"] for row in entity_facts)
        rows.append(
            {
                "entity_id_or_provisional": entity_id,
                "entity_name": entity_name,
                "entity_category": category,
                "places": ";".join(dict.fromkeys(row["place"] for row in entity_facts)),
                **{f"{code}_count": str(counts[code]) for code in FRAME_CODES},
                "safe_fact_count": str(len(entity_facts)),
                "fact_ids": ";".join(row["fact_id"] for row in entity_facts),
                "interpretation_limit": (
                    "Cells count bounded frame observations; they do not encode "
                    "co-occurrence, inter-entity ties, stable alliances, resident "
                    "consensus, or political agreement."
                ),
            }
        )
    return rows


def render_r04_brief(
    facts: list[dict[str, str]],
    sources: list[dict[str, str]],
    matrix: list[dict[str, str]],
) -> str:
    fact_counts = Counter(row["place"] for row in facts)
    source_counts = Counter(row["place"] for row in sources)
    matrix_counts = {
        (row["place"], row["frame_label"]): row["safe_source_count"] for row in matrix
    }
    categories = Counter(
        "registry_actor"
        if row["entity_status"] == "existing_actor"
        else "external_institution"
        if row["entity_status"] == "external_institution"
        else "bounded_non_registry"
        for row in facts
    )
    return f"""# R4 先岛三地框架：HR-016 合并后的线上证据安全层

日期：2026-07-20
状态：HR-016 **12/12 已合并**；speaker、地点层级、frame 与 locator 均按负责人决定冻结。

## 合并结果

- 正式 frame observations：**{len(facts)}** 条（宫古 {fact_counts['Miyako']}、石垣 {fact_counts['Ishigaki']}、与那国 {fact_counts['Yonaguni']}、先岛区域 {fact_counts['Sakishima']}）。
- 安全来源摘录：**{len(sources)}** 条（宫古 {source_counts['Miyako']}、石垣 {source_counts['Ishigaki']}、与那国 {source_counts['Yonaguni']}、先岛区域 {source_counts['Sakishima']}）。
- 事实主体构成：registry actor {categories['registry_actor']} 条、external institution {categories['external_institution']} 条、具名个人／一次性委员会／匿名事件话语 {categories['bounded_non_registry']} 条。
- HR-016 模块内待审事实与 locator：**0**；组织持续性与当地材料缺口仍由 registry／local-retrieval 任务管理。

## 三项关键修订

1. 宫古材料严格分开久貝美奈子的个人质询与宫古岛市行政答复；不再制造“市议会整体立场”。2016 年 6・11 集会只归一次性执行委员会，不 crosswalk 到 A012。
2. 石垣意见交换会只编码匿名意见主题块及相应行政答复；23 名参加者不是 23 名发言者，更不代表全市居民。F_AUT 只表示意见 1、4、7 中的程序／地方意见疑问，不表示提出住民投票。
3. 与那国导弹部队说明会只支持防卫省的 F_FTE 制度事件，不支持程序公平或居民同意；县级五市町村训练按 `Sakishima` 区域编码，不扇出为与那国特有事实。

## 可见度读法

- 宫古：地下水／饮用水 {matrix_counts[('Miyako', 'groundwater_life_safety')]}；前线／撤离 {matrix_counts[('Miyako', 'frontline_taiwan_evacuation')]}。
- 石垣：自治／公投 {matrix_counts[('Ishigaki', 'local_autonomy_referendum')]}；前线／撤离 {matrix_counts[('Ishigaki', 'frontline_taiwan_evacuation')]}；生活安全 {matrix_counts[('Ishigaki', 'life_safety')]}。
- 与那国：前线／撤离 {matrix_counts[('Yonaguni', 'frontline_taiwan_evacuation')]}；自治／公投 {matrix_counts[('Yonaguni', 'local_autonomy_referendum')]}；环境—部署直接连接 {matrix_counts[('Yonaguni', 'environment_deployment')]}。

数字只衡量本包线上材料的公开可见度，不代表现实动员规模或居民态度分布。预案、训练、质询和说明会不等于实际撤离能力、政策落实、程序公平或居民同意；个人、匿名发言与行政答复也不得升级为组织／地区总体立场。
"""


def render_hr016_completed_packet(rows: list[dict[str, str]]) -> str:
    lines = [
        "# HR-016：R4 先岛框架人工复核包（已完成）",
        "",
        "日期：2026-07-20",
        "",
        "状态：**12/12 已由项目负责人决定并合并正式层**。本文件保留为审计索引；逐项依据见两份回交报告。",
        "",
        "| review item | object | decision | approved formulation |",
        "|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row['review_item_id']} | {row['original_id']} | "
            f"{row['review_decision']} | {row['approved_formulation']} |"
        )
    lines.extend(
        [
            "",
            "## 回交报告",
            "",
            "- `docs/human_review_return_HR016_sakishima_batch35A_v1.md`",
            "- `docs/human_review_return_HR016_sakishima_batch35B_v1.md`",
            "",
            "## 合并边界",
            "",
            "- 一次性委员会不 crosswalk 到 A012；具名议员不等于市议会；匿名会议话语不形成居民 actor。",
            "- 行政答复不回指 A013；先岛区域材料不扇出为与那国特有事实。",
            "- 预案、训练和说明会不等于实际撤离能力、程序公平或居民同意。",
            "",
        ]
    )
    return "\n".join(lines)


def update_hr016_ledger(
    root: Path, overlays: dict[str, dict[str, str]]
) -> list[dict[str, str]]:
    path = root / R04 / "hr016_review_items_v0.csv"
    fields, rows = read_csv(path)
    fields = ensure_fields(
        fields,
        [
            "review_decision",
            "human_reviewer",
            "review_date",
            "review_note",
            "approved_formulation",
            "scope_boundary",
            "decision_source_report",
        ],
    )
    by_id = {row["review_item_id"]: row for row in rows}
    for item_id, overlay in overlays.items():
        row = by_id[item_id]
        row["review_decision"] = overlay["decision"]
        row["human_reviewer"] = overlay["human_reviewer"]
        row["review_date"] = overlay["review_date"]
        row["review_note"] = (
            f"{overlay['approved_formulation']} | 边界：{overlay['scope_boundary']}"
        )
        row["approved_formulation"] = overlay["approved_formulation"]
        row["scope_boundary"] = overlay["scope_boundary"]
        row["decision_source_report"] = overlay["source_report"]
    write_csv(path, fields, rows)
    return rows


def merge_r04(
    root: Path,
    overlays: dict[str, dict[str, str]],
    render_figures: bool,
) -> dict[str, int]:
    module = root / R04
    fact_path = root / R04_FACTS
    fact_fields, current_facts = read_csv(fact_path)
    source_fields, current_sources = read_csv(module / "online_evidence_safe_sources_v0.csv")
    _, source_candidates = read_csv(module / "source_excerpt_locators_v0.csv")
    source_candidates_by_id = {row["corpus_source_id"]: row for row in source_candidates}

    safe_sources = {
        row["corpus_source_id"]: row
        for row in current_sources
        if row["corpus_source_id"] not in HR016_SOURCE_IDS
    }
    source_updates = {
        "R4S002": {
            "speaker_or_owner": "Okinawa Prefecture Environment Department government response",
            "locator": "印刷 p.6／委员会记录第165–175行；环境部长宣读陈情处理方针",
            "paraphrase_zh": "县环境部对陆自部署陈情宣读地下水监测与环境保护处理方针",
            "frame_candidates": "groundwater_life_safety;environment_deployment",
            "qa_reason": "行政处理方针；不是陈情者原文，不回指 A013。",
            "interpretation_limit": "Government response only; does not establish A013 wording or identity.",
        },
        "R4S007": {
            "locator": "印刷 pp.27–29；Pattern 1 摘要 p.27，正文 p.28，实施要领记载例 p.29",
            "frame_candidates": "frontline_taiwan_evacuation;life_safety",
            "qa_reason": "稳定印刷页码已人工确认。",
            "interpretation_limit": "Scenario/pattern/plan example; not an actual evacuation or capacity test.",
        },
        "R4S008": {
            "speaker_or_owner": "久貝美奈子（一般質問）／総務部長 上地俊暢（行政答弁）",
            "locator": "印刷 pp.139–140／久貝美奈子一般質問与総務部長上地俊暢答弁",
            "excerpt_short": "久貝美奈子一般質問／総務部長上地俊暢答弁（逐段）",
            "paraphrase_zh": "具名议员的问题化与市行政的制度答复分别支持自治参与、撤离和生活安全框架",
            "frame_candidates": "frontline_taiwan_evacuation;life_safety;local_autonomy_referendum",
            "qa_reason": "个人质询与市行政答复逐段分离；不生成市议会机构立场。",
            "interpretation_limit": "Named councillor question and municipal response remain separate observations.",
        },
        "R4S015": {
            "speaker_or_owner": "anonymous meeting utterances / Ishigaki City administrative responses",
            "locator": "pp.1–4／意見1–9；无箭头为匿名意见，箭头后为行政答复；括号职务按原文保留",
            "frame_candidates": "frontline_taiwan_evacuation;life_safety;local_autonomy_referendum",
            "qa_reason": "匿名意见主题块与行政答复拆分；23 名参加者不等于发言者或全市居民。",
            "interpretation_limit": "Event-level anonymous utterances only; not a resident actor or citywide stance.",
        },
        "R4S024": {
            "speaker_or_owner": "Ministry of Defense (official stated purpose)",
            "locator": "正文第16行／说明会主题及防卫省自述的“增进理解”目的",
            "frame_candidates": "frontline_taiwan_evacuation",
            "qa_reason": "只支持说明会制度事件；删除 procedural_fairness。",
            "interpretation_limit": "Official stated purpose only; no resident response, consent, or process-quality finding.",
        },
    }
    for source_id, updates in source_updates.items():
        row = dict(source_candidates_by_id[source_id])
        row.update(updates)
        row["qa_disposition"] = "human_checked" if source_id == "R4S007" else "human_revised"
        row["review_status"] = row["qa_disposition"]
        row["coding_status"] = "human_reviewed"
        row["human_review_note"] = updates["interpretation_limit"]
        safe_sources[source_id] = row

    safe_source_rows = sorted(
        safe_sources.values(), key=lambda row: int(row["corpus_source_id"][3:])
    )
    if len(safe_source_rows) != 24:
        raise ValueError(f"HR-016 merge expected 24 safe sources, got {len(safe_source_rows)}")
    safe_source_map = {row["corpus_source_id"]: row for row in safe_source_rows}

    facts = [
        row for row in current_facts if row["fact_id"] not in HR016_FACT_IDS
    ]
    r4e007 = next(row for row in facts if row["fact_id"] == "R4E007")
    r4e007["source_ref"] = "R4S006;R4S007;R4S009"
    (
        r4e007["existing_source_ids"],
        r4e007["source_urls"],
        r4e007["source_locator_summary"],
    ) = source_trace(r4e007["source_ref"], safe_source_map)
    r4e007["review_status"] = "human_checked"
    r4e007["interpretation_limit"] = (
        "The statutory plan, Pattern 1 (printed pp.27–29), and public Q&A support "
        "a scenario/plan observation only; not an actual evacuation or capacity test."
    )

    additions = [
        make_r04_fact(
            safe_source_map,
            fact_id="R4E001",
            place="Miyako",
            entity_id="PROV_R4_611_EXECUTIVE_COMMITTEE",
            entity_name="「宮古島いのちの水を守ろう！ 6・11自衛隊配備を止める市民集会」実行委員会",
            entity_status="provisional_event_committee",
            event_or_document="陸自配備阻止集会",
            event_year="2016",
            frame_code="F_GW",
            frame_label="groundwater_life_safety",
            relation_basis="2016 集会主办者把反部署与地下水源保护连接",
            source_ref="R4S003",
            evidence_level="E3",
            interpretation_limit=(
                "One-time 2016 event committee only; not crosswalked to A012 and "
                "not evidence of organizational continuity or participant membership."
            ),
        ),
        make_r04_fact(
            safe_source_map,
            fact_id="R4E008",
            place="Miyako",
            entity_id="PROV_COUNCILOR_KUGAI_MINAKO",
            entity_name="宮古島市議会議員 久貝美奈子",
            entity_status="named_individual_non_registry",
            event_or_document="先島有事避難計画に関する一般質問",
            event_year="2025",
            frame_code="F_AUT",
            frame_label="local_autonomy_referendum",
            relation_basis="具名议员追问居民意见进入计划的机制与时点",
            source_ref="R4S008",
            evidence_level="E4",
            interpretation_limit=(
                "Individual legislative question, not a council position and not a referendum proposal."
            ),
        ),
        make_r04_fact(
            safe_source_map,
            fact_id="R4E009A",
            place="Miyako",
            entity_id="PROV_COUNCILOR_KUGAI_MINAKO",
            entity_name="宮古島市議会議員 久貝美奈子",
            entity_status="named_individual_non_registry",
            event_or_document="先島有事避難計画に関する一般質問",
            event_year="2025",
            frame_code="F_FTE",
            frame_label="frontline_taiwan_evacuation",
            relation_basis="具名议员将台湾有事设想、全岛撤离、要照护者、返岛与生活恢复问题化",
            source_ref="R4S008",
            evidence_level="E4",
            interpretation_limit=(
                "Councillor's risk questions only; not a council consensus or confirmation "
                "that evacuation, return, or recovery capacity exists."
            ),
        ),
        make_r04_fact(
            safe_source_map,
            fact_id="R4E009B",
            place="Miyako",
            entity_id="GOV_MIYAKO_CITY_ADMIN",
            entity_name="宮古島市行政（総務部長 上地俊暢答弁）",
            entity_status="external_institution",
            event_or_document="先島有事避難計画に関する行政答弁",
            event_year="2025",
            frame_code="F_FTE",
            frame_label="frontline_taiwan_evacuation",
            relation_basis="市行政说明机关间检讨，并将返岛与避难后生活列为仍待讨论课题",
            source_ref="R4S008",
            evidence_level="E4",
            interpretation_limit=(
                "Municipal response only; planning under discussion is not verified "
                "transport, return, or livelihood-restoration capacity."
            ),
        ),
        make_r04_fact(
            safe_source_map,
            fact_id="R4E016",
            place="Ishigaki",
            entity_id="EVENT_R4S015_ANONYMOUS_COMMENT_UNITS",
            entity_name="2024-08-02 伊原間意见交换会匿名意见主题块",
            entity_status="non_actor_event_evidence",
            event_or_document="避难意见交换会",
            event_year="2024",
            frame_code="F_FTE",
            frame_label="frontline_taiwan_evacuation",
            relation_basis="匿名意见 1–6、8–9 提出撤离可行性与生活安全问题",
            source_ref="R4S015",
            evidence_level="E4",
            interpretation_limit=(
                "Anonymous event-level utterance units; nine blocks are not nine people, "
                "23 attendees are not 23 speakers, and no citywide stance is inferred."
            ),
        ),
        make_r04_fact(
            safe_source_map,
            fact_id="R4E017",
            place="Ishigaki",
            entity_id="EVENT_R4S015_ANONYMOUS_COMMENT_UNITS",
            entity_name="2024-08-02 伊原間意见交换会匿名意见主题块",
            entity_status="non_actor_event_evidence",
            event_or_document="避难意见交换会",
            event_year="2024",
            frame_code="F_AUT",
            frame_label="local_autonomy_referendum",
            relation_basis="匿名意见 1、4、7 提出义务、判断标准与地方意见进入决策的疑问",
            source_ref="R4S015",
            evidence_level="E4",
            interpretation_limit=(
                "Opinion blocks 1, 4 and 7 are separate anonymous utterance units; "
                "not a coherent person, resident actor, citywide stance, or referendum claim."
            ),
        ),
        make_r04_fact(
            safe_source_map,
            fact_id="R4E024",
            place="Yonaguni",
            entity_id="MOD_JAPAN",
            entity_name="防衛省",
            entity_status="external_institution",
            event_or_document="中距离地对空导弹部队住民说明会",
            event_year="2026",
            frame_code="F_FTE",
            frame_label="frontline_taiwan_evacuation",
            relation_basis="防卫省公告举办说明会并自述以增进町民理解为目的",
            source_ref="R4S024",
            evidence_level="E4",
            interpretation_limit=(
                "Meeting announcement and official stated purpose only; no resident consent, "
                "procedural-fairness, representativeness, or communication-effect finding."
            ),
        ),
        make_r04_fact(
            safe_source_map,
            fact_id="R4E025",
            place="Sakishima",
            entity_id="GOV_OKINAWA_PREF",
            entity_name="沖縄県",
            entity_status="external_institution",
            event_or_document="国民保护联合图上训练",
            event_year="2025",
            frame_code="F_LIFE",
            frame_label="life_safety",
            relation_basis="县级训练把运输能力与要照护者避难列为先岛区域重点课题",
            source_ref="R4S021",
            evidence_level="E4",
            interpretation_limit=(
                "Sakishima regional observation covering five municipalities; not a "
                "Yonaguni-only fact and not evidence of political agreement by each locality."
            ),
        ),
    ]
    facts.extend(additions)
    facts.sort(
        key=lambda row: (
            int("".join(char for char in row["fact_id"] if char.isdigit())),
            row["fact_id"],
        )
    )
    if len(facts) != 19:
        raise ValueError(f"HR-016 merge expected 19 formal facts, got {len(facts)}")

    human_fields, human_rows = read_csv(module / "human_review_queue_v0.csv")
    human_rows = [
        row for row in human_rows if row["candidate_edge_id"] not in HR016_FACT_IDS
    ]
    source_human_fields, source_human_rows = read_csv(module / "source_review_queue_v0.csv")
    source_human_rows = [
        row
        for row in source_human_rows
        if row["corpus_source_id"] not in HR016_SOURCE_IDS
    ]
    if human_rows or source_human_rows:
        raise ValueError("All 12 HR-016 fact/source items should be closed after merge")

    matrix = build_r04_matrix(safe_source_rows)
    entity_matrix = build_r04_entity_matrix(facts)
    matrix_fields = list(matrix[0])
    entity_fields = list(entity_matrix[0])

    write_csv(fact_path, fact_fields, facts)
    write_csv(module / "online_evidence_safe_sources_v0.csv", source_fields, safe_source_rows)
    write_csv(module / "human_review_queue_v0.csv", human_fields, human_rows)
    write_csv(module / "source_review_queue_v0.csv", source_human_fields, source_human_rows)
    write_csv(module / "three_place_safe_source_matrix_v0.csv", matrix_fields, matrix)
    write_csv(module / "entity_frame_safe_matrix_v0.csv", entity_fields, entity_matrix)

    brief = render_r04_brief(facts, safe_source_rows, matrix)
    (module / "R04_online_evidence_brief_v1.md").write_text(brief, encoding="utf-8")
    category_counts = Counter(row["entity_category"] for row in entity_matrix)
    note = f"""# R4 formalization note

Generated by `python scripts/merge_hr016_hr017_modules_v1.py` on 2026-07-20.

- HR-016 decisions merged: 12/12
- Formal human-reviewed/QA-safe facts: {len(facts)}
- Open semantic-human queue: {len(human_rows)}
- Rejected actor candidates retained: {len(read_csv(module / 'reject_log_v0.csv')[1])}
- Safe source excerpts: {len(safe_source_rows)}
- Open source locator/speaker queue: {len(source_human_rows)}
- Entity/frame matrix: {len(entity_matrix)} entities ({category_counts['registry_actor']} registry actors; {category_counts['external_institution']} external institutions; {category_counts['provisional_entity']} bounded non-registry entities)

The formal table contains bounded frame observations, not stable alliances,
organizational identities, resident consensus, actual evacuation capacity or
causal effects.  A one-time committee, named individual and anonymous meeting
utterances remain outside the actor registry.
"""
    (module / "formalization_note_v0.md").write_text(note, encoding="utf-8")
    hr016_items = update_hr016_ledger(root, overlays)
    if len(hr016_items) != 12 or any(
        not row.get("review_decision") for row in hr016_items
    ):
        raise ValueError("HR-016 review ledger must retain 12 completed decisions")
    (module / "HR016_human_review_packet.md").write_text(
        render_hr016_completed_packet(hr016_items), encoding="utf-8"
    )

    if render_figures:
        from scripts import make_r04_sakishima_formal as r04

        svg = r04.render_svg(matrix, facts)
        entity_svg = r04.render_entity_svg(entity_matrix, facts)
        (module / "fig_r4_three_place_frames_v0.svg").write_text(svg, encoding="utf-8")
        (module / "fig_r4_three_place_frames_v0.html").write_text(
            "<!doctype html><html lang='zh-CN'><head><meta charset='utf-8'>"
            "<meta name='viewport' content='width=device-width,initial-scale=1'>"
            "<title>R4 先岛三地框架比较</title><style>body{margin:0;background:#eceae4}"
            "main{max-width:1420px;margin:24px auto;background:white;box-shadow:0 8px 28px #0002}"
            "svg{display:block;width:100%;height:auto}</style></head><body><main>"
            + svg
            + "</main></body></html>",
            encoding="utf-8",
        )
        (module / "fig_r4_entity_frame_matrix_v0.svg").write_text(
            entity_svg, encoding="utf-8"
        )
        (module / "fig_r4_entity_frame_matrix_v0.html").write_text(
            "<!doctype html><html lang='zh-CN'><head><meta charset='utf-8'>"
            "<meta name='viewport' content='width=device-width,initial-scale=1'>"
            "<title>R4 主体／制度节点 × 框架</title><style>body{margin:0;background:#eceae4}"
            "main{max-width:1500px;margin:24px auto;background:white;box-shadow:0 8px 28px #0002}"
            "svg{display:block;width:100%;height:auto}</style></head><body><main>"
            + entity_svg
            + "</main></body></html>",
            encoding="utf-8",
        )

    return {
        "r04_formal_facts": len(facts),
        "r04_safe_sources": len(safe_source_rows),
        "r04_open_fact_items": len(human_rows),
        "r04_open_source_items": len(source_human_rows),
    }


def update_hr017_queue(
    root: Path, overlays: dict[str, dict[str, str]]
) -> list[dict[str, str]]:
    path = root / R09 / "hr017_review_queue_v0.csv"
    fields, rows = read_csv(path)
    fields = ensure_fields(
        fields,
        ["approved_formulation", "scope_boundary", "decision_source_report"],
    )
    by_id = {row["object_id"]: row for row in rows}
    for object_id, overlay in overlays.items():
        row = by_id[object_id]
        row["decision"] = overlay["decision"]
        row["human_reviewer"] = overlay["human_reviewer"]
        row["review_date"] = overlay["review_date"]
        row["decision_note"] = (
            f"{overlay['approved_formulation']} | 边界：{overlay['scope_boundary']}"
        )
        row["approved_formulation"] = overlay["approved_formulation"]
        row["scope_boundary"] = overlay["scope_boundary"]
        row["decision_source_report"] = overlay["source_report"]
    write_csv(path, fields, rows)
    return rows


def r09_source_rows() -> list[dict[str, str]]:
    return [
        {
            "source_id": "R9S035",
            "existing_source_id": "",
            "case_id": "R9C_ISHIGAKI_2018_2024",
            "source_tier": "primary_litigation_archive",
            "source_type": "court_judgment_copy",
            "title": "那覇地方裁判所令和3年（行ウ）第5号判決",
            "year": "2023",
            "url": "https://www.call4.jp/file/pdf/202407/654c30e79b09c673e0855664f9069578.pdf",
            "evidence_level": "E3",
            "review_status": "human_checked",
            "disposition": "usable_with_limit",
            "supports": "2023-05-23一审判决、三名自然人原告、全部却下及诉讼费用",
            "interpretation_limit": "CALL4托管的裁判书影印，不升为法院官网E4。",
            "notes": "HR-017 online review, 2026-07-20.",
        },
        {
            "source_id": "R9S036",
            "existing_source_id": "",
            "case_id": "R9C_ISHIGAKI_2018_2024",
            "source_tier": "primary_litigation_archive",
            "source_type": "case_material_index",
            "title": "石垣市住民投票を求める裁判 CALL4訴訟資料一覧",
            "year": "2021-2024",
            "url": "https://www.call4.jp/search.php?items_id=I0000141&items_id_PAL%5B%5D=match+comp&run=true&type=material",
            "evidence_level": "E3",
            "review_status": "human_checked",
            "disposition": "usable_with_limit",
            "supports": "诉状材料所载2021-04-26第二诉讼起诉日",
            "interpretation_limit": "案件材料索引不是法院官网；不据此把A011写成组织原告。",
            "notes": "HR-017 online review, 2026-07-20.",
        },
        {
            "source_id": "R9S037",
            "existing_source_id": "",
            "case_id": "R9C_ISHIGAKI_2018_2024",
            "source_tier": "secondary_academic",
            "source_type": "research_article",
            "title": "自治総研 47巻515号 pp.40–（J-STAGE PDF）",
            "year": "2021",
            "url": "https://www.jstage.jst.go.jp/article/jichisoken/47/515/47_40/_pdf",
            "evidence_level": "E3",
            "review_status": "human_checked",
            "disposition": "usable_with_limit",
            "supports": "2021-04-26第二诉讼起诉日与程序背景交叉确认",
            "interpretation_limit": "研究文献用于日期交叉确认，不替代法院裁判书。",
            "notes": "HR-017 online review, 2026-07-20.",
        },
    ]


def render_r09_brief(
    stages: list[dict[str, str]], roles: list[dict[str, str]]
) -> str:
    formal_stages = [row for row in stages if row["review_status"] == "accepted"]
    formal_roles = [row for row in roles if row["review_status"] == "accepted"]
    open_stages = [row for row in stages if row["review_status"] == "needs_human_review"]
    open_roles = [row for row in roles if row["review_status"] == "needs_human_review"]
    return f"""# R9 住民投票／意见广告／诉讼程序 brief v1

日期：2026-07-20
状态：HR-017 在线 **9/9 已合并**；另 9 项当地资料任务保持开放。

## 正式层

- 正式程序阶段：**{len(formal_stages)}**；reviewed-all 共 {len(stages)}，其中当地待审 {len(open_stages)}。
- 正式角色：**{len(formal_roles)}**；reviewed-all 共 {len(roles)}，其中当地待审 {len(open_roles)}。
- 正式层仍按 `公众动员 → 代表/签名资格 → 条例议程与设计 → 投票或司法门槛 → 结果再解释` 拆分，不把同场参与或程序相邻写成联盟或因果。

## 本轮闭合的石垣诉讼链

第二条地位确认等当事者诉讼现以 2021-04-26 为起诉日；三名自然人原告不得转写为 A011 组织原告。2023-05-23 那霸地裁判决将三名原告之诉全部却下；2024-03-12 福冈高裁那霸支部将各控诉全部棄却。2024-09-26 最高裁阶段只冻结中性结论“决定后败诉确定”，在没有最高裁官方决定书和案号前，不选定单一处分类型。

R9R030 只保留三名个人原告的程序性 collective；R9R031 只保留代理律师的 counsel 功能；R9R034 只表示最高裁司法场域。个人、律师和法院均不因此进入 civic actor registry。

## 名护与当地任务边界

R9R001 映射 A068，仅限 1997 年条例直接请求和签名组织角色；不据此推断组织持续至今。A068 的规范名与谱系由 registry／lifecycle 任务另行维护。

仍开放的 9 项全部需要当地或组织档案：与那国 2012 意见广告、2015 反对侧运动与正式选管结果、A011 的组织角色及解散材料。它们继续留在 HR-017 队列，不进入正式表。A011 requester/supporter 与个人 plaintiff 必须保持区分。

## 解释边界

公投、条例、诉讼和行政回应可用于分析自治诉求如何经过制度门槛被转换；不能据此识别组织动员造成政策结果。法院的程序处理也不是对部署政策实体是非的判断。图中箭头只表示程序顺序。
"""


def render_hr017_audit_packet(rows: list[dict[str, str]]) -> str:
    decided = [row for row in rows if row["decision"]]
    open_rows = [row for row in rows if not row["decision"]]
    lines = [
        "# HR-017 R9 程序与角色复核包（部分完成）",
        "",
        "日期：2026-07-20",
        "",
        f"状态：在线可闭合 **{len(decided)}/9 已决定并合并**；当地资料 **{len(open_rows)}/9 保持空白**。",
        "",
        "## 已合并的在线项目",
        "",
        "| object | type | decision | approved formulation |",
        "|---|---|---|---|",
    ]
    for row in decided:
        lines.append(
            f"| {row['object_id']} | {row['object_type']} | {row['decision']} | "
            f"{row.get('approved_formulation', '')} |"
        )
    lines.extend(
        [
            "",
            "## 仍需当地资料的项目",
            "",
            "| object | subject | evidence | source refs |",
            "|---|---|---|---|",
        ]
    )
    for row in open_rows:
        lines.append(
            f"| {row['object_id']} | {row['subject']} | {row['evidence_level']} | "
            f"{row['source_refs']} |"
        )
    lines.extend(
        [
            "",
            "这些空白项不得凭在线相邻材料补决定。A011 组织角色、个人原告、请求代表与签名居民必须分开；与那国意见广告、反对侧委员会和正式选管结果继续等待当地材料。",
            "",
            "在线决定依据：`docs/human_review_return_HR017_online_batch36_v1.md`。",
            "",
        ]
    )
    return "\n".join(lines)


def merge_r09(
    root: Path,
    overlays: dict[str, dict[str, str]],
    render_figures: bool,
) -> dict[str, int]:
    module = root / R09
    stage_fields, stages = read_csv(module / "process_stages_reviewed_all_v0.csv")
    role_fields, roles = read_csv(module / "actor_process_roles_reviewed_all_v0.csv")
    stage_by_id = {row["stage_id"]: row for row in stages}
    role_by_id = {row["role_id"]: row for row in roles}

    stage_changes = {
        "R9ST027": {
            "date_start": "2021-04-26",
            "date_end": "2021-04-26",
            "date_precision": "day",
            "process_action": "三名石垣市民提起地位确认等当事者诉讼",
            "outcome": "那覇地方裁判所令和3年（行ウ）第5号进入第二条诉讼链",
            "source_refs": "R9S036;R9S037",
            "interpretation_limit": "三名自然人原告不等于A011；不得与第一条实施义务付け诉讼合并。",
        },
        "R9ST028": {
            "interpretation_limit": "只确认2021-03-23终结与案号；上诉起日和具体主文未取得。",
        },
        "R9ST030": {
            "outcome": "三名原告之诉全部却下；诉讼费用由原告承担",
            "source_refs": "R9S035",
            "interpretation_limit": "却下是程序处理，不是对自卫队部署政策实体是非的判断。",
        },
        "R9ST031": {
            "outcome": "本件各控诉均被棄却；控诉费用由控诉人承担",
            "source_refs": "R9S026;R9S027",
            "interpretation_limit": "CALL4托管裁判书正本影印为E3；官方保存表只交叉确认案号。",
        },
        "R9ST032": {
            "process_action": "2024-09-26最高裁决定后第二诉讼链败诉确定",
            "outcome": "最高裁程序结束，第二诉讼链败诉确定；官方决定书与案号未取得",
            "interpretation_limit": "保持中性终结措辞；不得确定写成上告棄却或上告不受理。",
        },
    }
    for stage_id, changes in stage_changes.items():
        row = stage_by_id[stage_id]
        row.update(changes)
        row["review_status"] = "accepted"
        row["needs_local_retrieval"] = "no"
        row["notes"] = merge_note(
            row.get("notes", ""),
            "HR-017 online human review accepted/revised by project principal on 2026-07-20.",
        )

    role_changes = {
        "R9R001": {
            "actor_id": "A068",
            "entity_id": "",
            "entity_name": "ヘリポート基地建設の是非を問う名護市民投票推進協議会",
            "entity_kind": "registry_actor",
            "role_scope": "1997 direct request and statutory signature process only",
            "interpretation_limit": "只限1997直接请求与签名组织角色；不推断长期连续活动。",
        },
        "R9R030": {
            "entity_kind": "individual_plaintiff_collective",
            "role_scope": "status-confirmation chain; three named natural-person plaintiffs",
            "source_refs": "R9S035;R9S027",
            "interpretation_limit": "程序性个人原告集合；不映射A011，不新建actor。",
        },
        "R9R031": {
            "entity_kind": "counsel_collective",
            "role_scope": "counsel for the three individual plaintiffs in the status-confirmation chain",
            "source_refs": "R9S035;R9S027",
            "interpretation_limit": "只记录诉讼代理功能；不新建律师个人或组织actor。",
        },
        "R9R034": {
            "role_scope": "status-confirmation finalization; judicial forum only",
            "interpretation_limit": "E2司法场域；无官方决定书与案号，不冻结单一处分类型。",
        },
    }
    for role_id, changes in role_changes.items():
        row = role_by_id[role_id]
        row.update(changes)
        row["review_status"] = "accepted"
        row["needs_local_retrieval"] = "no"
        row["notes"] = merge_note(
            row.get("notes", ""),
            "HR-017 online human review accepted/revised by project principal on 2026-07-20.",
        )

    queue = update_hr017_queue(root, overlays)
    if {row["object_id"] for row in queue if not row["decision"]} != HR017_LOCAL_OPEN_IDS:
        raise ValueError("HR-017 must preserve exactly nine blank local-retrieval items")

    formal_stages = [row for row in stages if row["review_status"] == "accepted"]
    formal_roles = [row for row in roles if row["review_status"] == "accepted"]
    if (len(formal_stages), len(formal_roles)) != (29, 29):
        raise ValueError(
            f"HR-017 merge expected 29 stages/29 roles, got "
            f"{len(formal_stages)}/{len(formal_roles)}"
        )
    if Counter(row["review_status"] for row in stages) != Counter(
        {"accepted": 29, "needs_human_review": 4}
    ):
        raise ValueError("R09 stage status distribution drift")
    if Counter(row["review_status"] for row in roles) != Counter(
        {"accepted": 29, "needs_human_review": 5}
    ):
        raise ValueError("R09 role status distribution drift")

    source_fields, sources = read_csv(module / "source_register_v0.csv")
    sources = [row for row in sources if row["source_id"] not in {"R9S035", "R9S036", "R9S037"}]
    for row in sources:
        if row["source_id"] in {"R9S027", "R9S028", "R9S029"}:
            row["review_status"] = "human_checked"
    sources.extend(r09_source_rows())
    sources.sort(key=lambda row: int(row["source_id"][3:]))

    case_fields, case_rows = read_csv(module / "case_summary_v0.csv")
    for case in case_rows:
        case_stages = [row for row in stages if row["case_id"] == case["case_id"]]
        case["accepted_stage_count"] = str(
            sum(row["review_status"] == "accepted" for row in case_stages)
        )
        case["pending_stage_count"] = str(
            sum(row["review_status"] == "needs_human_review" for row in case_stages)
        )

    write_csv(module / "process_stages_reviewed_all_v0.csv", stage_fields, stages)
    write_csv(root / R09_STAGES, stage_fields, formal_stages)
    write_csv(module / "actor_process_roles_reviewed_all_v0.csv", role_fields, roles)
    write_csv(module / "actor_process_roles_v0.csv", role_fields, formal_roles)
    write_csv(module / "source_register_v0.csv", source_fields, sources)
    write_csv(module / "case_summary_v0.csv", case_fields, case_rows)

    (module / "R09_process_brief_v1.md").write_text(
        render_r09_brief(stages, roles), encoding="utf-8"
    )
    (module / "HR017_review_packet_v0.md").write_text(
        render_hr017_audit_packet(queue), encoding="utf-8"
    )
    readme = f"""# R09 referendum process formal package

Generated by `python scripts/merge_hr016_hr017_modules_v1.py`.

- `../../data/interim/20_referendum_process_stages_v0.csv`: 29 accepted stages.
- `process_stages_reviewed_all_v0.csv`: 33 reviewed stages (29 accepted; 4 local-retrieval open).
- `actor_process_roles_v0.csv`: 29 accepted roles.
- `actor_process_roles_reviewed_all_v0.csv`: 34 reviewed roles (29 accepted; 5 local-retrieval open).
- `hr017_review_queue_v0.csv`: 18 audit rows; 9 online decisions recorded and 9 local items blank.
- accepted-v1 figures read only the 29-stage/29-role formal layers.

The online merge does not close the nine local-retrieval items. Sequence and
arrows are procedural, not causal. A011 requester/supporter remains distinct
from the three individual plaintiffs; no person, court or counsel collective
is added to the civic actor registry.
"""
    (module / "README.md").write_text(readme, encoding="utf-8")
    validation = f"""# R09 validation report v0

Generated: 2026-07-20

- Formal stage rows: 29; all accepted.
- Reviewed-all stage rows: 33 (`accepted=29`, `needs_human_review=4`).
- Formal role rows: 29; all accepted.
- Reviewed-all role rows: 34 (`accepted=29`, `needs_human_review=5`).
- HR-017 queue: 18 rows; 9 online decisions complete, 9 local-retrieval items blank.
- R9ST027 exact date: 2021-04-26.
- R9ST030: three plaintiffs' actions all procedurally dismissed.
- R9ST031: all appeals dismissed; E3 CALL4-hosted judgment copy boundary retained.
- R9ST032: neutral Supreme Court finalization wording retained.
- A011 not coded as an individual plaintiff; R9R030 has no actor_id.
- A068 role limited to the 1997 direct-request/signature process.
- Figure sequence does not encode causal effects.
"""
    (module / "validation_report_v0.md").write_text(validation, encoding="utf-8")

    if render_figures:
        from scripts import make_r09_referendum_process as r09

        r09.STAGES[:] = stages
        r09.ROLES[:] = roles
        r09.make_timeline()
        r09.make_gate_flow()
        r09.make_accepted_timeline(formal_stages, formal_roles)
        r09.make_accepted_gate_flow(formal_stages, formal_roles)

    return {
        "r09_formal_stages": len(formal_stages),
        "r09_formal_roles": len(formal_roles),
        "r09_open_local_items": sum(not row["decision"] for row in queue),
    }


def merge_hr016_hr017_modules(
    root: Path = ROOT, *, render_figures: bool = True
) -> dict[str, int]:
    hr016, hr017 = load_overlays(root)
    summary = {
        **merge_r04(root, hr016, render_figures),
        **merge_r09(root, hr017, render_figures),
    }
    return summary


if __name__ == "__main__":
    result = merge_hr016_hr017_modules()
    print(
        "HR-016/017 module merge complete: "
        f"R04 {result['r04_formal_facts']} facts / {result['r04_safe_sources']} sources; "
        f"R09 {result['r09_formal_stages']} stages / {result['r09_formal_roles']} roles; "
        f"{result['r09_open_local_items']} local HR-017 items remain open."
    )
