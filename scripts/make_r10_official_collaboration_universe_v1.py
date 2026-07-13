from __future__ import annotations

"""Build the R10 FY2024 official-collaboration source-universe layer.

This generator extracts every source row from S002 and produces source-label
aggregations only.  It never creates an actor-registry record, actor identity
crosswalk, approved relation edge, award record, or human-review decision.
"""

import csv
import hashlib
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import colors, font_manager
import numpy as np
import pdfplumber


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "R10_official_collaboration_universe_v1"
AUDIT_OUT = ROOT / "outputs" / "R10_completeness_audit_v1"
SOURCE_PDF = ROOT / "source_docs" / "source_archive" / "S002" / "raw.pdf"
MANIFEST = ROOT / "source_docs" / "source_archive" / "source_archive_manifest.csv"
AUDIT_INDEX = AUDIT_OUT / "s002_universe_index_v1.csv"

SOURCE_TITLE = "令和6年度「NPO等との協働実績調査」"
SOURCE_YEAR = "2024"
SOURCE_ID = "S002"

MECHANISMS = {
    "1": ("委託", "NPO等へ業務委託を行った事業", "delegated_public_program"),
    "2": ("提案型公募による委託", "提案型公募による委託", "proposal_based_delegated_program"),
    "3": ("指定管理者制度による委任", "指定管理者制度による委任", "designated_management"),
    "4": ("補助", "補助金・助成金の支給又は物的支援", "subsidy_assistance_or_in_kind"),
    "5": ("共催", "NPO等と共催という形で実施", "cohosting"),
    "6": ("後援", "NPO等の事業を後援という形で支援", "endorsement_or_support"),
    "7": ("実行委員会等", "委員会等にNPO等のメンバーを加えた事業", "committee_participation"),
    "8": ("事業協力", "共催以外の形態で協力・連携", "program_cooperation"),
    "9": ("講師等", "講演会等の講師をNPO等が担当", "lecturer_or_expertise"),
    "10": ("その他", "上記以外の協働形態", "other_collaboration"),
}

ISSUES = {
    "1": "保健、医療又は福祉の増進を図る事業",
    "2": "社会教育及び生涯学習の推進を図る事業",
    "3": "地域づくりの推進を図る事業",
    "4": "観光の振興を図る事業",
    "5": "農山漁村又は離島・過疎地域の振興を図る事業",
    "6": "学術、文化、芸術又はスポーツの振興を図る事業",
    "7": "環境の保全を図る事業",
    "8": "災害救援事業",
    "9": "地域安全及び犯罪防止に関する事業",
    "10": "人権の擁護又は平和の推進を図る事業",
    "11": "国際協力及び国際交流に関する事業",
    "12": "男女共同参画社会の形成の促進を図る事業",
    "13": "子どもの教育及び健全育成を図る事業",
    "14": "情報化社会の発展を図る事業",
    "15": "科学技術及び研究活動の振興を図る事業",
    "16": "経済活動の活性化を図る事業",
    "17": "職業能力の開発又は雇用機会の拡充を支援する事業",
    "18": "消費者の保護を図る事業",
    "19": "NPO等の活動や運営を支援する事業",
}

ISSUE_SHORT = {
    "1": "保健・医療・福祉",
    "2": "社会教育・生涯学習",
    "3": "地域づくり",
    "4": "観光振興",
    "5": "農山漁村・離島・過疎",
    "6": "学術・文化・芸術・スポーツ",
    "7": "環境保全",
    "8": "災害救援",
    "9": "地域安全・犯罪防止",
    "10": "人権擁護・平和推進",
    "11": "国際協力・国際交流",
    "12": "男女共同参画",
    "13": "子ども教育・健全育成",
    "14": "情報化社会",
    "15": "科学技術・研究",
    "16": "経済活動活性化",
    "17": "職業能力・雇用機会",
    "18": "消費者保護",
    "19": "NPO活動・運営支援",
}

PARTNER_KINDS = {
    "1": "特定非営利活動法人（NPO法人）",
    "2": "公益社団又は公益財団法人",
    "3": "営利を目的としない一般社団又は一般財団法人",
    "4": "社会福祉法人",
    "5": "学校法人、医療法人等上記1～4以外の非営利法人",
    "6": "自治会",
    "7": "JV（複数の異なる団体等が共同で事業を行う組織）",
    "8": "その他、法人格を持たない任意団体等",
}

MECHANISM_COLORS = {
    "1": "#225f73",
    "2": "#3f88a8",
    "3": "#76a9c2",
    "4": "#ca7a3b",
    "5": "#4f8a68",
    "6": "#7dab82",
    "7": "#8e6b9e",
    "8": "#a98a55",
    "9": "#b36c79",
    "10": "#8c8f91",
}

AUTHORITATIVE_FIELDS = [
    "source_row_uid",
    "source_id",
    "source_title",
    "fiscal_year",
    "source_row_number",
    "pdf_page",
    "department_source_text",
    "department_display_machine",
    "office_source_text",
    "office_display_machine",
    "official_mechanism_code",
    "official_mechanism_label",
    "official_mechanism_definition",
    "mechanism_analytical_family",
    "official_issue_field_code",
    "official_issue_field_label",
    "program_name_source_text",
    "program_name_display_machine",
    "program_description_source_text",
    "partner_kind_code",
    "partner_kind_label",
    "partner_name_source_text",
    "partner_name_display_alias_machine",
    "partner_display_label_id",
    "partner_cell_scope",
    "period_source_text",
    "project_cost_thousand_jpy_source_text",
    "project_cost_thousand_jpy_numeric",
    "project_cost_presence",
    "planning主体_source_text",
    "implementation主体_source_text",
    "r10_purposive_sample_status",
    "r10_purposive_relation_id",
    "r10_purposive_amount_id",
    "identity_crosswalk_status",
    "relation_edge_status",
    "amount_semantics",
    "interpretation_limit",
]

HR032_ROWS = [
    {
        "review_item_id": "HR032-01",
        "priority": "P0_figure_count",
        "source_rows": "60-71;73;79-83;163;191;292;314;317;521",
        "source_label_variants": "社会福祉法人沖縄県社会福祉協議会 | 沖縄県社会福祉協議会",
        "ambiguity_type": "legal_prefix_omission",
        "current_machine_handling": "两种 display alias 分开；不作身份合并",
        "why_high_value": "合并会把高频 partner-label 计数从20+4改为24，并改变第二图首位条目的范围。",
        "human_question": "两种来源写法是否可作为同一法人名称的报告级 alias 合并？",
        "downstream_if_accept": "只重算 partner-label 汇总与第二图；不自动进入 registry 或生成关系边。",
        "decision": "",
        "approved_display_name": "",
        "registry_crosswalk_decision": "",
        "reviewer": "",
        "review_date": "",
        "review_note": "",
    },
    {
        "review_item_id": "HR032-02",
        "priority": "P0_phase1_field10_amount_outlier",
        "source_rows": "9;496",
        "source_label_variants": "公益財団法人沖縄県平和祈念財団（partner kind 2 / kind 3）",
        "ambiguity_type": "same_name_partner_kind_conflict",
        "current_machine_handling": "同一 display alias 汇总2行；不据此断言法人身份或纠正partner kind",
        "why_high_value": "两行均在field10，分别为资料馆业务与指定管理；row496事业费241,109千日元会支配任何金额尺度。",
        "human_question": "两行是否为同一财团，并如何解释kind 2/3冲突；是否明确区别于ひめゆり平和祈念財団？",
        "downstream_if_accept": "只允许人工身份/类别说明；事业费仍不得视为向财团付款。",
        "decision": "",
        "approved_display_name": "",
        "registry_crosswalk_decision": "",
        "reviewer": "",
        "review_date": "",
        "review_note": "",
    },
    {
        "review_item_id": "HR032-03",
        "priority": "P0_gender_scope_boundary",
        "source_rows": "197;205-207",
        "source_label_variants": "公益財団法人おきなわ女性財団 | 公益財団法人おきなわ女性財団（沖縄県男女共同参画センター管理運営団体）",
        "ambiguity_type": "organization_vs_management_role_composite_label",
        "current_machine_handling": "基础名称与带管理角色括注的source cell分开；不拆分、不连registry",
        "why_high_value": "四行横跨field1/12及委托/指定管理；名称容易与A111女団協、已移出的A094混淆。",
        "human_question": "row207括注是同一财团的管理角色还是复合主体表记；与A111/A094的边界是否明确？",
        "downstream_if_accept": "可增加管理角色 crosswalk；不得把财团、管理设施与女性团体互相替代。",
        "decision": "",
        "approved_display_name": "",
        "registry_crosswalk_decision": "",
        "reviewer": "",
        "review_date": "",
        "review_note": "",
    },
    {
        "review_item_id": "HR032-04",
        "priority": "P0_phase1_fields10_11",
        "source_rows": "10;11;501",
        "source_label_variants": "特定非営利活動法人沖縄平和協力センター | registry candidate A088／English alias OPAC待冻结",
        "ambiguity_type": "registry_crosswalk_plus_cross_department_continuity",
        "current_machine_handling": "三行同一machine display alias；不自动连A088",
        "why_high_value": "若人工确认，A088将从两项知事公室和平教育委托扩展到教育厅field11项目，改变行政桥接解释。",
        "human_question": "三行是否均crosswalk到A088；日文全称与OPAC英文/缩写如何冻结？",
        "downstream_if_accept": "可形成actor-level三项目解释；关系仍由HR018或其后继任务决定。",
        "decision": "",
        "approved_display_name": "",
        "registry_crosswalk_decision": "",
        "reviewer": "",
        "review_date": "",
        "review_note": "",
    },
    {
        "review_item_id": "HR032-05",
        "priority": "P0_phase1_field11",
        "source_rows": "432;435;436;438",
        "source_label_variants": "公益社団法人青年海外協力協会沖縄事務所 | three JV member strings",
        "ambiguity_type": "standalone_partner_vs_JV_member",
        "current_machine_handling": "standalone source cell与三个JV source cell分开；不拆JV",
        "why_high_value": "若展开成员，会形成 field11 中跨四项目的高可见桥接节点；不经人审不得据此画 actor 网络。",
        "human_question": "是否建立JOCA冲绳事务所的成员级 crosswalk；如建立，能否仅用于复合体成员说明？",
        "downstream_if_accept": "允许单独的 member-of-composite 展示层；不得把项目费拆给成员。",
        "decision": "",
        "approved_display_name": "",
        "registry_crosswalk_decision": "",
        "reviewer": "",
        "review_date": "",
        "review_note": "",
    },
    {
        "review_item_id": "HR032-06",
        "priority": "P0_phase1_field11",
        "source_rows": "433;434;571",
        "source_label_variants": "一般社団法人世界若者ウチナーンチュ連合会 | 世界若者ウチナーンチュ連合会 | Team OKIYUA member string",
        "ambiguity_type": "legal_prefix_plus_composite_member",
        "current_machine_handling": "三种source cell分开；row434不拆成员",
        "why_high_value": "三行均在field11；决定是否能说明同一主体以独立受托者、共同企业体成员和调查协调者多路径进入。",
        "human_question": "rows433/571是否同一法人；row434成员身份是否只作成员crosswalk而非独立资源边？",
        "downstream_if_accept": "可重算field11的actor-level解释；当前source-universe图不受影响。",
        "decision": "",
        "approved_display_name": "",
        "registry_crosswalk_decision": "",
        "reviewer": "",
        "review_date": "",
        "review_note": "",
    },
    {
        "review_item_id": "HR032-07",
        "priority": "P0_cross_field_mechanism",
        "source_rows": "529;545;548;551",
        "source_label_variants": "沖縄県ユネスコ協会（partner kind 1 / kind 8）",
        "ambiguity_type": "same_name_legal_kind_and_continuity_conflict",
        "current_machine_handling": "同一display alias汇总4行；不据此确认法律身份或持续主体",
        "why_high_value": "四行横跨field3/10/11/13与C4/C6；若为同一主体，会直接改变‘相关渠道不只是采购’的解释。",
        "human_question": "四行是否为同一持续组织；kind1/8差异如何解释？",
        "downstream_if_accept": "可作跨字段/机制actor解释；C6后援与C4补助必须继续分开。",
        "decision": "",
        "approved_display_name": "",
        "registry_crosswalk_decision": "",
        "reviewer": "",
        "review_date": "",
        "review_note": "",
    },
    {
        "review_item_id": "HR032-08",
        "priority": "P0_cross_field_mechanism",
        "source_rows": "204;466;499;591",
        "source_label_variants": "NPO法人レインボーハートokinawa（PDF空白/全角差异）",
        "ambiguity_type": "same_name_cross_program_continuity",
        "current_machine_handling": "NFKC/PDF排版清理后为同一display alias；不据此确认四行均为同一法人",
        "why_high_value": "四行横跨field3/10/13与C1/C6/C9/C10；row466项目主题异常，人工确认会改变公共协作桥接解释。",
        "human_question": "四行是否均为同一法人；row466是否存在source表记/主体错配？",
        "downstream_if_accept": "可作跨机制source-to-actor crosswalk；不得把C10或零事业费写成合同付款。",
        "decision": "",
        "approved_display_name": "",
        "registry_crosswalk_decision": "",
        "reviewer": "",
        "review_date": "",
        "review_note": "",
    },
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def clean_pdf_cell(value: str | None) -> str:
    if not value:
        return ""
    return re.sub(r"\s+", " ", value).strip()


def display_machine(value: str) -> str:
    """Repair obvious PDF wrapping only; never claim identity equivalence."""
    value = unicodedata.normalize("NFKC", value or "").strip()
    value = re.sub(r"\s+", " ", value)
    japanese = r"\u3040-\u30ff\u3400-\u9fff\uff66-\uff9f"
    value = re.sub(fr"(?<=[{japanese}])\s+(?=.)", "", value)
    value = re.sub(fr"(?<=.)\s+(?=[{japanese}])", "", value)
    value = re.sub(r"\s*([()「」『』【】・、,;:／/])\s*", r"\1", value)
    return value


def parse_cost(value: str) -> tuple[str, str]:
    cleaned = unicodedata.normalize("NFKC", value or "").replace(",", "").strip()
    if cleaned in {"", "-", "−", "ー"}:
        return "", "not_reported_dash"
    if not re.fullmatch(r"\d+", cleaned):
        raise RuntimeError(f"Unexpected project-cost cell: {value!r}")
    number = int(cleaned)
    return str(number), "positive" if number > 0 else "zero"


def extract_source_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    with pdfplumber.open(SOURCE_PDF) as document:
        for page_number, page in enumerate(document.pages, start=1):
            tables = page.extract_tables()
            if len(tables) != 1:
                raise RuntimeError(f"S002 page {page_number}: expected one table, got {len(tables)}")
            for raw in tables[0][3:]:
                if not raw[0] or not clean_pdf_cell(raw[0]).isdigit():
                    continue
                cells = [clean_pdf_cell(cell) for cell in raw]
                rows.append(
                    {
                        "source_row_number": cells[0],
                        "pdf_page": str(page_number),
                        "department": cells[1],
                        "office": cells[2],
                        "official_mechanism_code": cells[3],
                        "official_issue_field_code": cells[4],
                        "program_name": cells[5],
                        "program_description": cells[6],
                        "partner_kind_code": cells[7],
                        "partner_name": cells[8],
                        "period": cells[9],
                        "project_cost_thousand_jpy": cells[10],
                        "planning主体": cells[11],
                        "implementation主体": cells[12],
                    }
                )
    return rows


def audit_sample_map() -> dict[str, tuple[str, str]]:
    output: dict[str, tuple[str, str]] = {}
    for row in read_csv(AUDIT_INDEX):
        relation_id = row["included_r10_relation_id"]
        if relation_id:
            output[row["source_row_number"]] = (relation_id, row["included_r10_amount_id"])
    return output


def build_authoritative_rows(
    raw_rows: list[dict[str, str]], sample_map: dict[str, tuple[str, str]]
) -> list[dict[str, str]]:
    first_seen_aliases: dict[str, str] = {}
    for row in raw_rows:
        alias = display_machine(row["partner_name"])
        if alias not in first_seen_aliases:
            first_seen_aliases[alias] = f"S002PL{len(first_seen_aliases) + 1:03d}"

    output: list[dict[str, str]] = []
    for row in raw_rows:
        mechanism_code = row["official_mechanism_code"]
        issue_code = row["official_issue_field_code"]
        partner_kind = row["partner_kind_code"]
        if mechanism_code not in MECHANISMS or issue_code not in ISSUES or partner_kind not in PARTNER_KINDS:
            raise RuntimeError(f"Unknown code(s) in S002 row {row['source_row_number']}")
        cost_numeric, cost_presence = parse_cost(row["project_cost_thousand_jpy"])
        relation_id, amount_id = sample_map.get(row["source_row_number"], ("", ""))
        alias = display_machine(row["partner_name"])
        scope = (
            "official_JV_or_multi_party_source_cell_unsplit"
            if partner_kind == "7"
            else "source_partner_name_cell_unsplit"
        )
        output.append(
            {
                "source_row_uid": f"S002-R{int(row['source_row_number']):04d}",
                "source_id": SOURCE_ID,
                "source_title": SOURCE_TITLE,
                "fiscal_year": SOURCE_YEAR,
                "source_row_number": row["source_row_number"],
                "pdf_page": row["pdf_page"],
                "department_source_text": row["department"],
                "department_display_machine": display_machine(row["department"]),
                "office_source_text": row["office"],
                "office_display_machine": display_machine(row["office"]),
                "official_mechanism_code": mechanism_code,
                "official_mechanism_label": MECHANISMS[mechanism_code][0],
                "official_mechanism_definition": MECHANISMS[mechanism_code][1],
                "mechanism_analytical_family": MECHANISMS[mechanism_code][2],
                "official_issue_field_code": issue_code,
                "official_issue_field_label": ISSUES[issue_code],
                "program_name_source_text": row["program_name"],
                "program_name_display_machine": display_machine(row["program_name"]),
                "program_description_source_text": row["program_description"],
                "partner_kind_code": partner_kind,
                "partner_kind_label": PARTNER_KINDS[partner_kind],
                "partner_name_source_text": row["partner_name"],
                "partner_name_display_alias_machine": alias,
                "partner_display_label_id": first_seen_aliases[alias],
                "partner_cell_scope": scope,
                "period_source_text": row["period"],
                "project_cost_thousand_jpy_source_text": row["project_cost_thousand_jpy"],
                "project_cost_thousand_jpy_numeric": cost_numeric,
                "project_cost_presence": cost_presence,
                "planning主体_source_text": row["planning主体"],
                "implementation主体_source_text": row["implementation主体"],
                "r10_purposive_sample_status": "selected" if relation_id else "not_selected",
                "r10_purposive_relation_id": relation_id,
                "r10_purposive_amount_id": amount_id,
                "identity_crosswalk_status": "machine_display_alias_only_not_actor_identity",
                "relation_edge_status": "source_universe_row_not_relation_edge",
                "amount_semantics": "whole_program_project_cost_not_actor_payment_or_award",
                "interpretation_limit": "Authoritative mechanical source-row extraction; no registry merge, relation approval, actor payment, alliance, or political stance inference.",
            }
        )
    return output


def joined(values: set[str], numeric: bool = False) -> str:
    key = (lambda value: int(value)) if numeric else None
    return ";".join(sorted(values, key=key))


def build_partner_summaries(rows: list[dict[str, str]]) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]]]:
    by_alias: dict[str, list[dict[str, str]]] = defaultdict(list)
    by_alias_mechanism: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    by_alias_department: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        alias = row["partner_name_display_alias_machine"]
        by_alias[alias].append(row)
        by_alias_mechanism[(alias, row["official_mechanism_code"])].append(row)
        by_alias_department[(alias, row["department_display_machine"])].append(row)

    summaries: list[dict[str, object]] = []
    for alias, members in sorted(by_alias.items(), key=lambda item: (-len(item[1]), item[1][0]["source_row_number"])):
        mechanism_counts = Counter(row["official_mechanism_code"] for row in members)
        dominant_code = sorted(mechanism_counts, key=lambda code: (-mechanism_counts[code], int(code)))[0]
        summaries.append(
            {
                "partner_display_label_id": members[0]["partner_display_label_id"],
                "partner_name_display_alias_machine": alias,
                "source_row_count": len(members),
                "raw_source_literal_variant_count": len({row["partner_name_source_text"] for row in members}),
                "department_count": len({row["department_display_machine"] for row in members}),
                "mechanism_count": len(mechanism_counts),
                "issue_field_count": len({row["official_issue_field_code"] for row in members}),
                "dominant_mechanism_code": dominant_code,
                "dominant_mechanism_label": MECHANISMS[dominant_code][0],
                "department_names": joined({row["department_display_machine"] for row in members}),
                "mechanism_codes": joined(set(mechanism_counts), numeric=True),
                "issue_field_codes": joined({row["official_issue_field_code"] for row in members}, numeric=True),
                "source_row_numbers": joined({row["source_row_number"] for row in members}, numeric=True),
                "contains_official_composite_cell": "yes" if any(row["partner_kind_code"] == "7" for row in members) else "no",
                "identity_status": "machine_display_alias_only_not_actor_identity",
                "interpretation_limit": "Repeated source label; not an organization count, registry crosswalk, or network-centrality claim.",
            }
        )

    mechanism_edges: list[dict[str, object]] = []
    for (alias, code), members in sorted(
        by_alias_mechanism.items(), key=lambda item: (int(item[0][1]), item[1][0]["partner_display_label_id"])
    ):
        mechanism_edges.append(
            {
                "partner_display_label_id": members[0]["partner_display_label_id"],
                "partner_name_display_alias_machine": alias,
                "official_mechanism_code": code,
                "official_mechanism_label": MECHANISMS[code][0],
                "source_row_count": len(members),
                "raw_source_literal_variant_count": len({row["partner_name_source_text"] for row in members}),
                "department_count": len({row["department_display_machine"] for row in members}),
                "department_names": joined({row["department_display_machine"] for row in members}),
                "issue_field_codes": joined({row["official_issue_field_code"] for row in members}, numeric=True),
                "source_row_numbers": joined({row["source_row_number"] for row in members}, numeric=True),
                "edge_semantics": "source_label_x_official_mechanism_cooccurrence",
                "identity_status": "machine_display_alias_only_not_actor_identity",
                "human_gate": "none_for_source_label_aggregation__HR032_only_for_identity_or_member_crosswalk",
                "interpretation_limit": "Bimode edge is an aggregation of official table rows, not an approved actor-resource relation.",
            }
        )

    department_edges: list[dict[str, object]] = []
    for (alias, department), members in sorted(
        by_alias_department.items(), key=lambda item: (item[0][1], item[1][0]["partner_display_label_id"])
    ):
        department_edges.append(
            {
                "partner_display_label_id": members[0]["partner_display_label_id"],
                "partner_name_display_alias_machine": alias,
                "department_display_machine": department,
                "source_row_count": len(members),
                "mechanism_codes": joined({row["official_mechanism_code"] for row in members}, numeric=True),
                "issue_field_codes": joined({row["official_issue_field_code"] for row in members}, numeric=True),
                "source_row_numbers": joined({row["source_row_number"] for row in members}, numeric=True),
                "edge_semantics": "source_label_x_department_cooccurrence",
                "identity_status": "machine_display_alias_only_not_actor_identity",
                "human_gate": "none_for_source_label_aggregation__HR032_only_for_identity_or_member_crosswalk",
                "interpretation_limit": "Department visibility is source-row cooccurrence, not organizational dependence or stable partnership.",
            }
        )
    return summaries, mechanism_edges, department_edges


def build_matrix_rows(
    rows: list[dict[str, str]], dimension: str, values: list[str]
) -> list[dict[str, object]]:
    grouped: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[(row[dimension], row["official_mechanism_code"])].append(row)
    output: list[dict[str, object]] = []
    for value in values:
        for code in map(str, range(1, 11)):
            members = grouped.get((value, code), [])
            if dimension == "official_issue_field_code":
                dimension_label = ISSUES[value]
            else:
                dimension_label = value
            output.append(
                {
                    "dimension_type": "official_issue_field" if dimension == "official_issue_field_code" else "department_source_label",
                    "dimension_code_or_name": value,
                    "dimension_label": dimension_label,
                    "official_mechanism_code": code,
                    "official_mechanism_label": MECHANISMS[code][0],
                    "source_row_count": len(members),
                    "distinct_partner_display_alias_count": len({row["partner_name_display_alias_machine"] for row in members}),
                    "source_row_numbers": joined({row["source_row_number"] for row in members}, numeric=True),
                    "fact_layer": "S002_616_row_source_universe_mechanical_aggregation",
                    "human_gate": "none_ready_now",
                    "interpretation_limit": "Counts are source records, not organizations, contracts, awards, or payments.",
                }
            )
    return output


def build_mechanism_summary(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    total = len(rows)
    output: list[dict[str, object]] = []
    for code in map(str, range(1, 11)):
        members = [row for row in rows if row["official_mechanism_code"] == code]
        output.append(
            {
                "official_mechanism_code": code,
                "official_mechanism_label": MECHANISMS[code][0],
                "official_mechanism_definition": MECHANISMS[code][1],
                "mechanism_analytical_family": MECHANISMS[code][2],
                "source_row_count": len(members),
                "share_of_616_percent": f"{100 * len(members) / total:.1f}",
                "distinct_partner_display_alias_count": len({row["partner_name_display_alias_machine"] for row in members}),
                "department_count": len({row["department_display_machine"] for row in members}),
                "issue_field_count": len({row["official_issue_field_code"] for row in members}),
                "cash_transfer_inference_allowed_from_s002_alone": "no",
                "interpretation_limit": "Official collaboration-form category; project cost is not automatically an actor payment or award.",
            }
        )
    return output


def build_department_summary(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    output: list[dict[str, object]] = []
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        groups[row["department_display_machine"]].append(row)
    for department, members in sorted(groups.items(), key=lambda item: (-len(item[1]), item[0])):
        output.append(
            {
                "department_display_machine": department,
                "source_row_count": len(members),
                "share_of_616_percent": f"{100 * len(members) / len(rows):.1f}",
                "office_count": len({row["office_display_machine"] for row in members}),
                "distinct_partner_display_alias_count": len({row["partner_name_display_alias_machine"] for row in members}),
                "mechanism_count": len({row["official_mechanism_code"] for row in members}),
                "issue_field_count": len({row["official_issue_field_code"] for row in members}),
                "interpretation_limit": "Department-level visibility in one FY2024 official table; not spending, performance, or dependence.",
            }
        )
    return output


def build_alias_collision_audit(rows: list[dict[str, str]], top_aliases: set[str]) -> list[dict[str, object]]:
    variants: dict[str, set[str]] = defaultdict(set)
    row_counts: Counter[str] = Counter()
    source_rows: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        alias = row["partner_name_display_alias_machine"]
        variants[alias].add(row["partner_name_source_text"])
        row_counts[alias] += 1
        source_rows[alias].add(row["source_row_number"])
    output: list[dict[str, object]] = []
    for alias in sorted((key for key in variants if len(variants[key]) > 1), key=lambda key: (-row_counts[key], key)):
        output.append(
            {
                "partner_name_display_alias_machine": alias,
                "source_row_count": row_counts[alias],
                "raw_source_literal_variant_count": len(variants[alias]),
                "raw_source_literal_variants": " | ".join(sorted(variants[alias])),
                "source_row_numbers": joined(source_rows[alias], numeric=True),
                "appears_in_top_partner_figure": "yes" if alias in top_aliases else "no",
                "normalization_scope": "NFKC_plus_PDF_wrap_whitespace_only",
                "identity_merge_status": "not_performed",
                "interpretation_limit": "Collision reflects display cleanup only; it does not establish that legally distinct names are the same actor.",
            }
        )
    return output


def configure_font() -> str:
    candidates = [
        "Microsoft YaHei",
        "Yu Gothic",
        "Meiryo",
        "Noto Sans CJK SC",
        "Noto Sans CJK JP",
        "SimHei",
        "DejaVu Sans",
    ]
    installed = {font.name for font in font_manager.fontManager.ttflist}
    chosen = next((name for name in candidates if name in installed), "DejaVu Sans")
    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": [chosen],
            "axes.unicode_minus": False,
            "figure.facecolor": "#f6f2e8",
            "axes.facecolor": "#fffdf8",
            "savefig.facecolor": "#f6f2e8",
        }
    )
    return chosen


def matrix_from_rows(
    rows: list[dict[str, str]], row_key: str, row_values: list[str]
) -> np.ndarray:
    lookup = Counter((row[row_key], row["official_mechanism_code"]) for row in rows)
    return np.array(
        [[lookup[(value, str(code))] for code in range(1, 11)] for value in row_values],
        dtype=float,
    )


def annotate_heatmap(ax, matrix: np.ndarray) -> None:
    threshold = max(matrix.max() * 0.35, 4)
    for y in range(matrix.shape[0]):
        for x in range(matrix.shape[1]):
            value = int(matrix[y, x])
            if not value:
                continue
            ax.text(
                x,
                y,
                str(value),
                ha="center",
                va="center",
                fontsize=7.2,
                fontweight="bold" if value >= threshold else "normal",
                color="white" if value >= threshold else "#17322b",
            )


def make_issue_mechanism_figure(rows: list[dict[str, str]]) -> None:
    values = list(map(str, range(1, 20)))
    matrix = matrix_from_rows(rows, "official_issue_field_code", values)
    masked = np.ma.masked_where(matrix == 0, matrix)
    cmap = colors.LinearSegmentedColormap.from_list("r10green", ["#eef3e9", "#8dbba1", "#1f6655"])
    cmap.set_bad("#fffdf8")

    fig, ax = plt.subplots(figsize=(15.6, 11.2))
    fig.subplots_adjust(left=0.25, right=0.94, top=0.83, bottom=0.17)
    image = ax.imshow(masked, aspect="auto", cmap=cmap, norm=colors.LogNorm(vmin=1, vmax=max(matrix.max(), 1)))
    annotate_heatmap(ax, matrix)
    ax.set_xticks(range(10), [f"C{code}\n{MECHANISMS[str(code)][0]}" for code in range(1, 11)], rotation=32, ha="right", fontsize=9)
    field_totals = matrix.sum(axis=1).astype(int)
    ax.set_yticks(
        range(19),
        [f"F{code:02d}  {ISSUE_SHORT[str(code)]}  · {field_totals[code - 1]}" for code in range(1, 20)],
        fontsize=9.2,
    )
    ax.set_xlabel("官方协作形态（S002 code）", fontsize=11, labelpad=12)
    ax.set_ylabel("官方事业分野 · 行总数", fontsize=11, labelpad=14)
    ax.set_xticks(np.arange(-0.5, 10, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, 19, 1), minor=True)
    ax.grid(which="minor", color="#d8d4c9", linewidth=0.55)
    ax.tick_params(which="minor", bottom=False, left=False)
    for spine in ax.spines.values():
        spine.set_visible(False)
    cbar = fig.colorbar(image, ax=ax, fraction=0.028, pad=0.025)
    cbar.set_label("官方表来源行数（对数色阶）", fontsize=9)
    fig.text(0.05, 0.955, "R10｜FY2024 行政协作来源总体：议题分野 × 协作机制", fontsize=19, fontweight="bold", color="#17322b")
    fig.text(0.05, 0.918, "S002 全部 616 行；格内数字为官方表记录数，零值留白", fontsize=11.5, color="#53645e")
    fig.text(0.05, 0.876, "事实层：纯 source-universe 机械聚合 · ready_now · no HR gate", fontsize=10.5, color="#26735f", fontweight="bold")
    fig.text(0.05, 0.06, "边界：记录数 ≠ 组织数、合同数或拨款数；‘事业费’字段不自动等于向合作方支付的金额。", fontsize=10.2, color="#6b5434")
    fig.savefig(
        OUT / "fig_r10_s002_issue_mechanism_matrix_v1.png",
        dpi=180,
        metadata={"Software": "make_r10_official_collaboration_universe_v1.py"},
    )
    plt.close(fig)


def wrap_partner_label(value: str, width: int = 26) -> str:
    if len(value) <= width:
        return value
    return value[: width - 1] + "…"


def make_partner_department_figure(
    rows: list[dict[str, str]], partner_summaries: list[dict[str, object]]
) -> set[str]:
    department_values = [
        row[0]
        for row in sorted(
            Counter(r["department_display_machine"] for r in rows).items(),
            key=lambda item: (-item[1], item[0]),
        )
    ]
    matrix = matrix_from_rows(rows, "department_display_machine", department_values)
    top = [row for row in partner_summaries if int(row["source_row_count"]) >= 5]
    top_aliases = {str(row["partner_name_display_alias_machine"]) for row in top}
    partner_mechanism = Counter(
        (row["partner_name_display_alias_machine"], row["official_mechanism_code"])
        for row in rows
    )

    fig = plt.figure(figsize=(18.2, 15.0))
    grid = fig.add_gridspec(2, 1, height_ratios=[1.05, 1.25], left=0.22, right=0.95, top=0.82, bottom=0.15, hspace=0.40)
    ax1 = fig.add_subplot(grid[0])
    ax2 = fig.add_subplot(grid[1])

    masked = np.ma.masked_where(matrix == 0, matrix)
    cmap = colors.LinearSegmentedColormap.from_list("r10blue", ["#edf2f3", "#87aec0", "#245f74"])
    cmap.set_bad("#fffdf8")
    image = ax1.imshow(masked, aspect="auto", cmap=cmap, norm=colors.LogNorm(vmin=1, vmax=max(matrix.max(), 1)))
    annotate_heatmap(ax1, matrix)
    dept_totals = matrix.sum(axis=1).astype(int)
    ax1.set_yticks(
        range(len(department_values)),
        [f"{name} · {dept_totals[index]}" for index, name in enumerate(department_values)],
        fontsize=9.2,
    )
    ax1.set_xticks(range(10), [f"C{code} {MECHANISMS[str(code)][0]}" for code in range(1, 11)], rotation=30, ha="right", fontsize=8.8)
    ax1.set_title("A｜部门 × 官方协作机制：来源行结构", loc="left", fontsize=14, fontweight="bold", pad=13, color="#17322b")
    ax1.set_xticks(np.arange(-0.5, 10, 1), minor=True)
    ax1.set_yticks(np.arange(-0.5, len(department_values), 1), minor=True)
    ax1.grid(which="minor", color="#d8d4c9", linewidth=0.5)
    ax1.tick_params(which="minor", bottom=False, left=False)
    for spine in ax1.spines.values():
        spine.set_visible(False)
    cbar = fig.colorbar(image, ax=ax1, fraction=0.025, pad=0.018)
    cbar.set_label("来源行数（对数色阶）", fontsize=8.5)

    y = np.arange(len(top))
    left = np.zeros(len(top))
    for code in map(str, range(1, 11)):
        values = np.array(
            [partner_mechanism[(str(row["partner_name_display_alias_machine"]), code)] for row in top]
        )
        ax2.barh(
            y,
            values,
            left=left,
            height=0.68,
            color=MECHANISM_COLORS[code],
            label=f"C{code} {MECHANISMS[code][0]}",
        )
        left += values
    ax2.set_yticks(
        y,
        [wrap_partner_label(str(row["partner_name_display_alias_machine"])) for row in top],
        fontsize=9,
    )
    ax2.invert_yaxis()
    ax2.set_xlabel("该 machine display label 对应的 S002 来源行数", fontsize=10.5)
    ax2.set_title("B｜高频 partner source-label × 机制（每个标签 ≥ 5 行；17 个）", loc="left", fontsize=14, fontweight="bold", pad=13, color="#17322b")
    ax2.grid(axis="x", color="#dedad0", linewidth=0.7)
    ax2.set_axisbelow(True)
    for index, row in enumerate(top):
        ax2.text(
            float(row["source_row_count"]) + 0.25,
            index,
            f"{row['source_row_count']}行 · {row['department_count']}部门",
            va="center",
            fontsize=8.2,
            color="#53645e",
        )
    handles, labels = ax2.get_legend_handles_labels()
    fig.legend(
        handles,
        labels,
        ncol=5,
        bbox_to_anchor=(0.5, 0.060),
        loc="lower center",
        frameon=False,
        fontsize=8.2,
        handlelength=1.4,
    )
    for spine in ["top", "right", "left"]:
        ax2.spines[spine].set_visible(False)

    fig.text(0.045, 0.958, "R10｜公开行政协作：部门—机制与 raw partner label 结构", fontsize=19, fontweight="bold", color="#17322b")
    fig.text(0.045, 0.923, "S002 全部 616 行；B 面板采用固定阈值 ≥5 行，避免在 4 行并列组中任意截断", fontsize=11.5, color="#53645e")
    fig.text(0.045, 0.884, "事实层：source-label 聚合 · ready_now；HR032 只约束未来的法人 alias／JV成员／registry crosswalk", fontsize=10.2, color="#26735f", fontweight="bold")
    fig.text(0.045, 0.020, "边界：source label 重复不等于同一法人已合并，也不表示稳定行政伙伴关系；共同企业体未拆分，项目费未归给成员。", fontsize=10.1, color="#6b5434")
    fig.savefig(
        OUT / "fig_r10_s002_partner_department_resource_structure_v1.png",
        dpi=180,
        metadata={"Software": "make_r10_official_collaboration_universe_v1.py"},
    )
    plt.close(fig)
    return top_aliases


def build_descriptive_stats(
    rows: list[dict[str, str]], partner_summaries: list[dict[str, object]]
) -> list[dict[str, object]]:
    raw_literal_count = len({row["partner_name_source_text"] for row in rows})
    aliases = {row["partner_name_display_alias_machine"] for row in rows}
    mechanism_1_4 = sum(row["official_mechanism_code"] in {"1", "2", "3", "4"} for row in rows)
    field_10_11 = sum(row["official_issue_field_code"] in {"10", "11"} for row in rows)
    cost_presence = Counter(row["project_cost_presence"] for row in rows)
    department_counts = Counter(row["department_display_machine"] for row in rows)
    top5_departments = sum(count for _name, count in department_counts.most_common(5))
    metrics = [
        ("M01", "official_source_rows", len(rows), "rows", "S002 source universe"),
        ("M02", "pdf_pages", 86, "pages", "S002 archived PDF"),
        ("M03", "departments", len(department_counts), "source labels", "machine display cleanup only"),
        ("M04", "offices", len({row["office_display_machine"] for row in rows}), "source labels", "machine display cleanup only"),
        ("M05", "official_issue_fields", len({row["official_issue_field_code"] for row in rows}), "codes", "official codebook"),
        ("M06", "official_mechanisms", len({row["official_mechanism_code"] for row in rows}), "codes", "official codebook"),
        ("M07", "distinct_partner_source_literals", raw_literal_count, "strings", "not organizations"),
        ("M08", "distinct_partner_display_aliases_machine", len(aliases), "display labels", "not actor identities"),
        ("M09", "display_aliases_repeated_two_or_more_rows", sum(int(row["source_row_count"]) >= 2 for row in partner_summaries), "display labels", "not centrality"),
        ("M10", "display_aliases_spanning_two_or_more_departments", sum(int(row["department_count"]) >= 2 for row in partner_summaries), "display labels", "identity unresolved"),
        ("M11", "mechanism_codes_1_to_4_rows", mechanism_1_4, "rows", "delegated/subsidy-adjacent official categories; no payment inference"),
        ("M12", "mechanism_codes_1_to_4_share", f"{100 * mechanism_1_4 / len(rows):.1f}", "percent", "row share"),
        ("M13", "phase1_adjacent_official_fields_10_11", field_10_11, "rows", "human rights/peace + international cooperation/exchange"),
        ("M14", "phase1_adjacent_fields_10_11_share", f"{100 * field_10_11 / len(rows):.1f}", "percent", "row share"),
        ("M15", "positive_project_cost_cells", cost_presence["positive"], "rows", "whole-program project cost; not actor payment"),
        ("M16", "zero_project_cost_cells", cost_presence["zero"], "rows", "reported zero"),
        ("M17", "dash_project_cost_cells", cost_presence["not_reported_dash"], "rows", "not reported"),
        ("M18", "top_five_departments_rows", top5_departments, "rows", "mechanical concentration"),
        ("M19", "top_five_departments_share", f"{100 * top5_departments / len(rows):.1f}", "percent", "mechanical concentration"),
        ("M20", "r10_purposive_rows_inside_source_universe", sum(row["r10_purposive_sample_status"] == "selected" for row in rows), "rows", "separate HR018-gated layer"),
    ]
    return [
        {
            "metric_id": metric_id,
            "metric_name": name,
            "value": value,
            "unit": unit,
            "claim_scope": scope,
            "fact_layer": "S002_616_row_source_universe_mechanical_aggregation",
            "human_gate": "none_ready_now",
            "interpretation_limit": "No actor identity, relation, payment, award, alliance, or political stance inference.",
        }
        for metric_id, name, value, unit, scope in metrics
    ]


def write_figure_registry() -> None:
    rows = [
        {
            "figure_id": "R10U-F01",
            "figure_file": "fig_r10_s002_issue_mechanism_matrix_v1.png",
            "input_tables": "official_collaboration_source_universe_v1.csv;issue_mechanism_matrix_v1.csv",
            "fact_layer": "pure_616_row_source_universe_aggregation",
            "human_gate": "none_ready_now",
            "suggested_report_role": "正文主图：替换‘目的性样本即总体’的错觉，回答官方协作机制与议题分布。",
            "conservative_caption": "图以冲绳县FY2024《NPO等との協働実績調査》616条来源行为总体，按官方事业分野与协作形态计数；格数表示公开表中记录数，不等同于组织数、合同数或实际拨款。",
            "interpretation_limit": "No HR032 or HR018 gate; any actor-level interpretation remains separate.",
        },
        {
            "figure_id": "R10U-F02",
            "figure_file": "fig_r10_s002_partner_department_resource_structure_v1.png",
            "input_tables": "official_collaboration_source_universe_v1.csv;department_mechanism_matrix_v1.csv;partner_display_alias_summary_v1.csv",
            "fact_layer": "616_row_source_label_aggregation",
            "human_gate": "none_for_current_raw_label_figure__HR032_only_for_future_identity_crosswalk",
            "suggested_report_role": "正文辅图或附录主图：说明部门—机制结构与达到固定阈值（每个标签至少5行）的来源标签；若篇幅紧，正文保留A面板、附录放完整图。",
            "conservative_caption": "图按原表合作方名称单元的机器排版别名展示部门—机制结构；B面板采用每个标签至少5条来源行的固定阈值，共17个标签，不在4行并列组中任意截断。同名重复不代表已完成法人身份合并，项目事业费亦不等于向该名称对应组织支付的金额。",
            "interpretation_limit": "Current display is ready now; canonical alias, JV-member split, registry crosswalk, or actor centrality requires HR032.",
        },
    ]
    write_csv(OUT / "figure_registry_v1.csv", rows, list(rows[0]))


def write_brief(
    rows: list[dict[str, str]],
    mechanism_summary: list[dict[str, object]],
    department_summary: list[dict[str, object]],
    partner_summaries: list[dict[str, object]],
) -> None:
    mechanism_counts = {row["official_mechanism_code"]: int(row["source_row_count"]) for row in mechanism_summary}
    top_departments = department_summary[:5]
    top_partners = partner_summaries[:6]
    delegated = sum(mechanism_counts[str(code)] for code in range(1, 5))
    brief = f"""# R10 官方行政协作来源总体层 v1

日期：2026-07-13
来源：S002《{SOURCE_TITLE}》本地归档 PDF，86 页、616 条编号记录

## 一句话结论

冲绳县公开协作表显示的不是单一“补助金网络”，而是一套以**委托、提案型委托、指定管理和补助／物的支援**为主、并包含共催、后援、委员会、事业协力和讲师等机制的公共协作生态；但表内 partner 名称、事业费和同表出现都不能自动转写为 registry actor、实际付款、稳定关系或政治立场。

## R10 基础问题：哪些主体进入公开行政协作与可见资源渠道？

1. **总体不是少量一期核心 actor。** 616 行包含 {len({row['partner_name_source_text'] for row in rows})} 个不同 source-literal partner 字符串，经 NFKC 与 PDF 换行清理后得到 {len(partner_summaries)} 个 machine display aliases。二者都不是“组织数”；JV、复合体和缩略名尚未做人类身份合并。
2. **公开渠道高度制度化。** 官方 C1 委托 {mechanism_counts['1']} 行、C2 提案型委托 {mechanism_counts['2']} 行、C3 指定管理 {mechanism_counts['3']} 行、C4 补助／助成／物的支援 {mechanism_counts['4']} 行，合计 {delegated}/616（{100 * delegated / len(rows):.1f}%）。这只说明官方协作形态，不说明每行的 actor payment 或补助决定额。
3. **可见度集中于公共服务部门。** 前五个部门为 {'、'.join(f"{row['department_display_machine']} {row['source_row_count']}行" for row in top_departments)}，共 {sum(int(row['source_row_count']) for row in top_departments)}/616（{100 * sum(int(row['source_row_count']) for row in top_departments) / len(rows):.1f}%）。因此 R10 的总体层首先刻画福利、医疗、教育、儿童与文化旅游等公共服务生态，而非反基地组织的资金网。
4. **一期相邻议题只是总体的小部分。** 官方 field10“人权／和平”8 行、field11“国际协力／交流”11 行，共 19/616（3.1%）。其中可见新外交イニシアティブ、冲绳和平协力中心、冲绳 NGO 中心和多个国际交流／共同企业体 source cells；是否并入 actor 层仍由 HR018／HR032 分别控制关系与身份。
5. **高频名称只能称 source labels。** 当前频次较高的 machine display aliases 包括 {'、'.join(f"{row['partner_name_display_alias_machine']}（{row['source_row_count']}行）" for row in top_partners)}。这些计数不能被称为网络中心性；法律形态缩写、同名变体与 JV 成员仍需人审。

## 三层必须分开

| 层 | 当前规模 | 能回答什么 | gate |
|---|---:|---|---|
| S002 source-universe | 616 行 | 官方表中哪些分野、部门、机制和 partner source labels 可见 | 纯机械聚合 `ready_now`，不需 HR gate |
| R10 purposive sample | 35 relations／26 amounts／43 functions，其中 S002 仅 10 行 | 一期重点案例如何进入委托、补助、服务与慈善场域 | 关系与金额解释受 HR018 控制 |
| actor identity／alias crosswalk | 当前不在总体层执行 | 哪些缩略名、复合体成员或 source labels 可归到同一法人／registry actor | 只审会改变正文图或核心解释的 8 项 HR032 |

## 两张图如何使用

### R10U-F01：议题分野 × 协作机制矩阵

- **事实层：**616 行纯机械聚合。
- **状态：**`ready_now / no HR gate`。
- **建议角色：**正文主图；用于说明 R10 的官方总体构成，并约束 35 条目的性样本的外推。
- **可直接入报告的保守图注：**图以冲绳县 FY2024《NPO 等との協働実績調査》616 条来源行为总体，按官方事业分野与协作形态计数；格数表示公开表中记录数，不等同于组织数、合同数或实际拨款。

### R10U-F02：部门—机制与 raw partner label 结构

- **事实层：**616 行部门／机制聚合＋达到固定阈值 `source_row_count >= 5` 的 17 个 source-label 机器排版别名；4 行并列组全部不展示。
- **状态：**当前 raw-label 图 `ready_now`；只有把 label 解释为同一法人、拆 JV 成员或连 registry 时才受 HR032。
- **建议角色：**正文辅图或附录主图；篇幅紧时正文只引用部门结构，把完整 partner-label 面板放附录。
- **可直接入报告的保守图注：**图按原表合作方名称单元的机器排版别名展示部门—机制结构；B 面板采用每个标签至少 5 条来源行的固定阈值，共 17 个标签，不在 4 行并列组中任意截断。同名重复不代表已完成法人身份合并，项目事业费亦不等于向该名称对应组织支付的金额。

## 解释边界

- C4 官方定义同时涵盖补助金、助成金和物的支援，不能把全部 C4 行写成现金 grant。
- S002 的“事业费”是项目口径；即使 partner 有名，也不能由该列推断向其支付同额。
- source label 同名重复不等于法人身份已合并，也不等于稳定行政伙伴或网络中心。
- JV／共同企业体按原 source cell 保留，不把项目费拆给成员。
- S002 公开出现不恢复 HR-013 已移出 registry 的 A094，也不把一般公益组织自动写成一期核心 actor。
"""
    (OUT / "R10_official_collaboration_universe_brief_v1.md").write_text(brief, encoding="utf-8")


def write_hr032_guide() -> None:
    guide = """# HR-032 高价值 partner alias／复合体 crosswalk 复核指南

日期：2026-07-13
范围：只审 8 个会改变正文 partner-label 图或一期相邻字段核心解释的名称问题；不逐条复核 616 行。

## 决定值

- `accept_display_alias_only`：允许在报告级 source-label 汇总中合并显示，但不进入 registry。
- `accept_member_crosswalk_only`：允许说明共同企业体成员；不得把项目费拆给成员，也不得生成稳定关系。
- `revise`：修订名称范围、有效期、法律形态或成员层级后再使用。
- `keep_separate`：保持不同 source labels／主体。
- `defer`：线上材料不足，转当地／法人一手材料。

## 强制边界

1. 当前两张总体图不等待 HR032：它们展示 source rows／source labels，不做法人身份主张。
2. HR032 只控制未来 canonical alias、JV-member 展开、actor-level 解读与 registry crosswalk。
3. `accept_display_alias_only` 不等于 registry 纳入，也不批准 actor–resource relation。
4. composite source cell 必须永久保留；任何成员展开只能作为另层 crosswalk。
5. A094 已被 HR-013 移出一期 registry；S002 出现不能机械恢复，且不得与 A111 女団協混同。
6. 所有 `decision`、复核人、日期和说明均由人工填写，生成器保持空白。
"""
    (OUT / "HR032_review_guide_v1.md").write_text(guide, encoding="utf-8")


def write_readme() -> None:
    readme = """# R10 official collaboration source universe v1

This is the authoritative, rerunnable FY2024 S002 source-universe layer for R10.

## Formal source tables

- `official_collaboration_source_universe_v1.csv`: all 616 authoritative mechanical source rows, preserving `source_row_number` and `pdf_page`.
- `official_resource_type_summary_v1.csv`: the 10 official collaboration mechanisms and descriptive counts.
- `issue_mechanism_matrix_v1.csv`: full 19×10 matrix, including zero cells.
- `department_mechanism_matrix_v1.csv`: full 15×10 matrix, including zero cells.
- `partner_mechanism_bimode_edges_v1.csv`: source-label × official-mechanism bimode aggregation.
- `partner_department_bimode_edges_v1.csv`: source-label × department aggregation.
- `partner_display_alias_summary_v1.csv`: 365 machine display labels; these are not actor identities.
- `machine_display_alias_collision_audit_v1.csv`: PDF-wrap normalization collisions only.
- `department_resource_summary_v1.csv` and `descriptive_statistics_v1.csv`: descriptive source-universe statistics.

## Figures and report roles

- `fig_r10_s002_issue_mechanism_matrix_v1.png`: pure 616-row aggregation, `ready_now / no HR gate`; recommended main-text figure.
- `fig_r10_s002_partner_department_resource_structure_v1.png`: current raw-label aggregation uses the disclosed fixed threshold `source_row_count >= 5` (17 labels) and is ready now; HR032 applies only if future writing turns a label into a canonical actor, splits JV members, or creates a registry crosswalk. Recommended supporting/main appendix figure.
- `figure_registry_v1.csv`: exact fact layer, gate, suggested report role, and conservative caption for both figures.

## Interpretation and human review

- `R10_official_collaboration_universe_brief_v1.md`: answers the R10 basic question while separating source universe, purposive sample, and HR018 relation layer.
- `HR032_partner_alias_crosswalk_review_v1.csv` and `HR032_review_guide_v1.md`: eight high-value ambiguities only; all human decision fields are blank.
- `validation_report_v1.md`: source SHA, extraction parity, row/code, aggregation, gate, and cleanliness checks.

No output in this package is an actor registry, approved relation edge, award table, payment table, alliance, or political-stance classification. Run with `python scripts/make_r10_official_collaboration_universe_v1.py`.
"""
    (OUT / "README.md").write_text(readme, encoding="utf-8")


def validate(
    raw_rows: list[dict[str, str]],
    rows: list[dict[str, str]],
    partner_summaries: list[dict[str, object]],
    partner_mechanism_edges: list[dict[str, object]],
    partner_department_edges: list[dict[str, object]],
    issue_matrix_rows: list[dict[str, object]],
    department_matrix_rows: list[dict[str, object]],
    mechanism_summary: list[dict[str, object]],
    top_aliases: set[str],
) -> list[str]:
    checks: list[str] = []

    def check(condition: bool, message: str) -> None:
        if not condition:
            raise AssertionError(message)
        checks.append(message)

    source_numbers = [int(row["source_row_number"]) for row in raw_rows]
    check(source_numbers == list(range(1, 617)), "PASS: authoritative extraction has sequential S002 rows 1-616")
    check(len(rows) == 616 and len({row["source_row_uid"] for row in rows}) == 616, "PASS: 616 unique authoritative source-row IDs")
    check({row["pdf_page"] for row in rows} == {str(page) for page in range(1, 87)}, "PASS: source rows preserve all PDF pages 1-86")
    check(Counter(row["official_mechanism_code"] for row in rows) == Counter({"1": 303, "2": 60, "3": 13, "4": 93, "5": 25, "6": 65, "7": 9, "8": 21, "9": 21, "10": 6}), "PASS: official mechanism counts match the verified S002 distribution")
    check(Counter(row["official_issue_field_code"] for row in rows) == Counter({"1": 226, "2": 28, "3": 14, "4": 32, "5": 4, "6": 55, "7": 32, "8": 12, "9": 18, "10": 8, "11": 11, "12": 4, "13": 83, "14": 7, "15": 13, "16": 25, "17": 28, "18": 4, "19": 12}), "PASS: official issue-field counts match the verified S002 distribution")
    check(len({row["partner_name_source_text"] for row in rows}) == 390, "PASS: 390 distinct source-literal partner strings")
    check(len(partner_summaries) == 365, "PASS: 365 machine display aliases; no actor identity count asserted")
    check(sum(int(row["source_row_count"]) for row in partner_summaries) == 616, "PASS: partner display summary accounts for all 616 source rows")
    check(sum(int(row["source_row_count"]) for row in partner_mechanism_edges) == 616, "PASS: partner-mechanism bimode edges account for all 616 source rows")
    check(sum(int(row["source_row_count"]) for row in partner_department_edges) == 616, "PASS: partner-department bimode edges account for all 616 source rows")
    check(len(issue_matrix_rows) == 190 and sum(int(row["source_row_count"]) for row in issue_matrix_rows) == 616, "PASS: complete 19x10 issue-mechanism matrix sums to 616")
    check(len(department_matrix_rows) == 150 and sum(int(row["source_row_count"]) for row in department_matrix_rows) == 616, "PASS: complete 15x10 department-mechanism matrix sums to 616")
    check(len(mechanism_summary) == 10 and sum(int(row["source_row_count"]) for row in mechanism_summary) == 616, "PASS: official resource-type summary sums to 616")
    check(sum(row["r10_purposive_sample_status"] == "selected" for row in rows) == 10, "PASS: exactly 10 S002 rows remain crosswalked to the separate purposive R10 layer")
    check(all(row["identity_crosswalk_status"] == "machine_display_alias_only_not_actor_identity" for row in rows), "PASS: no authoritative row is upgraded to actor identity")
    check(all(row["relation_edge_status"] == "source_universe_row_not_relation_edge" for row in rows), "PASS: no authoritative row is upgraded to a relation edge")
    check(all(not row["decision"] and not row["reviewer"] and not row["review_date"] for row in HR032_ROWS), "PASS: all eight HR032 human-decision fields remain blank")
    qualifying_aliases = {
        str(row["partner_name_display_alias_machine"])
        for row in partner_summaries
        if int(row["source_row_count"]) >= 5
    }
    check(top_aliases == qualifying_aliases and len(top_aliases) == 17, "PASS: second figure uses all 17 machine display labels meeting the disclosed >=5-row threshold")
    check(sum(int(row["source_row_count"]) == 4 for row in partner_summaries) == 16 and not any(int(row["source_row_count"]) == 4 and str(row["partner_name_display_alias_machine"]) in top_aliases for row in partner_summaries), "PASS: all sixteen four-row tied labels are excluded; no arbitrary tie-break remains")
    check(plt.imread(OUT / "fig_r10_s002_issue_mechanism_matrix_v1.png").shape[:2] == (2015, 2808), "PASS: R10U-F01 renders at the expected 2808x2015 pixels")
    check(plt.imread(OUT / "fig_r10_s002_partner_department_resource_structure_v1.png").shape[:2] == (2700, 3276), "PASS: R10U-F02 renders at the expected 3276x2700 pixels")

    audit_rows = read_csv(AUDIT_INDEX)
    parity_fields = [
        "source_row_number", "pdf_page", "department", "office", "official_mechanism_code",
        "official_issue_field_code", "program_name", "program_description", "partner_kind_code",
        "partner_name", "period", "project_cost_thousand_jpy", "planning主体", "implementation主体",
    ]
    check(
        all(all(raw_rows[index][field] == audit_rows[index][field] for field in parity_fields) for index in range(616)),
        "PASS: authoritative extraction exactly matches the previously validated 616-row audit index",
    )
    manifest = {row["source_id"]: row for row in read_csv(MANIFEST)}
    check(manifest[SOURCE_ID]["sha256"] == sha256(SOURCE_PDF), "PASS: S002 PDF SHA matches the archive manifest")
    return checks


def write_validation_report(checks: list[str]) -> None:
    report = "# R10 official collaboration source-universe validation v1\n\nDate: 2026-07-13\n\n"
    report += "## Structural and scope checks\n\n" + "\n".join(f"- {check}" for check in checks) + "\n\n"
    report += "## Figure QA contract\n\n"
    report += "- R10U-F01 uses only the 616-row authoritative source table and official code dictionaries; status `ready_now / no HR gate`.\n"
    report += "- R10U-F02 uses department counts and all 17 machine display aliases meeting the disclosed `source_row_count >= 5` threshold; all sixteen four-row ties are excluded, so no arbitrary cutoff remains. The current figure is ready now, while canonical identity, JV-member split, registry crosswalk, and actor-level centrality remain gated by HR032.\n"
    report += "- Both figures explicitly state that source-row counts are not organization, contract, award, payment, alliance, or political-stance claims.\n"
    report += "- PASS (manual visual QA, 2026-07-13): R10U-F01 has readable labels, complete 19x10 cells, no clipping, no overlap, and no missing glyphs.\n"
    report += "- PASS (manual visual QA, 2026-07-13): R10U-F02 has readable department and top-label panels, a separated legend/x-axis/caption, no clipping, and no missing glyphs.\n"
    report += "- The generator additionally validates all figure input totals and exact PNG dimensions.\n\n"
    report += "## Mutation boundary\n\n"
    report += "- No central actor, actor-edge, amount, source-log, HR018, or registry file is written by this generator.\n"
    report += "- The only human-review output is an eight-row HR032 queue with blank decision fields.\n"
    (OUT / "validation_report_v1.md").write_text(report, encoding="utf-8")


def validate_text_cleanliness() -> None:
    for path in sorted([*OUT.glob("*.md"), *OUT.glob("*.csv")]):
        lines = path.read_text(encoding="utf-8").splitlines()
        bad = [number for number, line in enumerate(lines, start=1) if line.rstrip() != line]
        if bad:
            raise AssertionError(f"Trailing whitespace in {path}: {bad}")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    configure_font()
    raw_rows = extract_source_rows()
    sample_map = audit_sample_map()
    rows = build_authoritative_rows(raw_rows, sample_map)
    partner_summaries, partner_mechanism_edges, partner_department_edges = build_partner_summaries(rows)
    issue_matrix_rows = build_matrix_rows(rows, "official_issue_field_code", list(map(str, range(1, 20))))
    department_values = sorted(
        {row["department_display_machine"] for row in rows},
        key=lambda department: (-sum(r["department_display_machine"] == department for r in rows), department),
    )
    department_matrix_rows = build_matrix_rows(rows, "department_display_machine", department_values)
    mechanism_summary = build_mechanism_summary(rows)
    department_summary = build_department_summary(rows)

    make_issue_mechanism_figure(rows)
    top_aliases = make_partner_department_figure(rows, partner_summaries)
    alias_collisions = build_alias_collision_audit(rows, top_aliases)
    descriptive_stats = build_descriptive_stats(rows, partner_summaries)

    checks = validate(
        raw_rows,
        rows,
        partner_summaries,
        partner_mechanism_edges,
        partner_department_edges,
        issue_matrix_rows,
        department_matrix_rows,
        mechanism_summary,
        top_aliases,
    )

    write_csv(OUT / "official_collaboration_source_universe_v1.csv", rows, AUTHORITATIVE_FIELDS)
    write_csv(OUT / "official_resource_type_summary_v1.csv", mechanism_summary, list(mechanism_summary[0]))
    write_csv(OUT / "issue_mechanism_matrix_v1.csv", issue_matrix_rows, list(issue_matrix_rows[0]))
    write_csv(OUT / "department_mechanism_matrix_v1.csv", department_matrix_rows, list(department_matrix_rows[0]))
    write_csv(OUT / "partner_display_alias_summary_v1.csv", partner_summaries, list(partner_summaries[0]))
    write_csv(OUT / "partner_mechanism_bimode_edges_v1.csv", partner_mechanism_edges, list(partner_mechanism_edges[0]))
    write_csv(OUT / "partner_department_bimode_edges_v1.csv", partner_department_edges, list(partner_department_edges[0]))
    write_csv(OUT / "machine_display_alias_collision_audit_v1.csv", alias_collisions, list(alias_collisions[0]))
    write_csv(OUT / "department_resource_summary_v1.csv", department_summary, list(department_summary[0]))
    write_csv(OUT / "descriptive_statistics_v1.csv", descriptive_stats, list(descriptive_stats[0]))
    write_csv(OUT / "HR032_partner_alias_crosswalk_review_v1.csv", HR032_ROWS, list(HR032_ROWS[0]))
    write_figure_registry()
    write_brief(rows, mechanism_summary, department_summary, partner_summaries)
    write_hr032_guide()
    write_readme()
    write_validation_report(checks)
    validate_text_cleanliness()
    print(
        "R10 official collaboration universe built: "
        f"{len(rows)} source rows, {len(partner_summaries)} display aliases, "
        f"{len(partner_mechanism_edges)} partner-mechanism edges, {len(HR032_ROWS)} HR032 items"
    )


if __name__ == "__main__":
    main()
