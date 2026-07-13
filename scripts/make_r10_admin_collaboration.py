from __future__ import annotations

"""Build the formal R10 administrative/service-ecology package.

This script deliberately separates relation observations, amount observations,
and function observations.  It does not mutate the actor registry, source log,
or the existing funding/support edge sample.
"""

import csv
import re
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "interim"
OUT = ROOT / "outputs" / "R10_administrative_collaboration_v0"

REL_PATH = DATA / "21_admin_collaboration_relations_v0.csv"
AMT_PATH = DATA / "22_admin_amount_observations_v0.csv"
FUN_PATH = DATA / "23_admin_function_observations_v0.csv"

REL_FIELDS = [
    "relation_observation_id", "source_record_ids", "fiscal_year", "period_start",
    "period_end", "source_entity_id", "source_entity_name", "source_entity_kind",
    "target_entity_id", "target_entity_name", "target_entity_kind", "program_name",
    "relation_type", "official_mechanism_code", "mechanism_label", "mechanism_detail",
    "financial_semantics", "relation_scope", "source_refs", "source_locators",
    "evidence_level", "review_status", "merge_disposition", "interpretation_limit",
]

AMT_FIELDS = [
    "amount_observation_id", "relation_observation_id", "fiscal_year", "amount_value",
    "currency", "normalized_unit", "reported_amount", "reported_unit", "amount_basis",
    "amount_scope", "attributed_actor_id", "actor_payment_status", "award_status",
    "line_width_eligible", "source_refs", "source_locators", "evidence_level",
    "review_status", "interpretation_limit",
]

FUN_FIELDS = [
    "function_observation_id", "relation_observation_id", "fiscal_year", "actor_id",
    "actor_name", "function_type", "function_description", "beneficiary_or_audience",
    "place_or_facility", "mechanism_context", "financial_inference_allowed",
    "political_stance_inference_allowed", "source_refs", "source_locators",
    "evidence_level", "review_status", "interpretation_limit",
]

REVIEW_STATUSES = {
    "ai_seeded", "human_checked", "human_revised", "needs_second_source",
    "needs_local_retrieval", "rejected",
}


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def preserve_human_review_rows(
    path: Path,
    rows: list[dict[str, str]],
    business_key: str,
    id_field: str,
    human_fields: tuple[str, ...],
) -> None:
    """Preserve stable IDs and completed human fields across generator reruns."""
    if not path.exists():
        return
    previous_rows = read_csv(path)
    previous = {row.get(business_key, ""): row for row in previous_rows if row.get(business_key, "")}
    if len(previous) != len([row for row in previous_rows if row.get(business_key, "")]):
        raise RuntimeError(f"Duplicate {business_key} in {path}")
    for row in rows:
        old = previous.get(row[business_key])
        if not old:
            continue
        if old.get(id_field):
            row[id_field] = old[id_field]
        for field in human_fields:
            if old.get(field, "").strip():
                row[field] = old[field]


def rel(
    rid: str, records: str, fy: str, start: str, end: str,
    source_id: str, source_name: str, source_kind: str,
    target_id: str, target_name: str, target_kind: str,
    program: str, relation_type: str, code: str, label: str, detail: str,
    semantics: str, scope: str, refs: str, locators: str,
    evidence: str = "E4", review: str = "ai_seeded",
    merge: str = "propose_new_relation", limit: str = "",
) -> dict[str, str]:
    return dict(zip(REL_FIELDS, [
        rid, records, fy, start, end, source_id, source_name, source_kind,
        target_id, target_name, target_kind, program, relation_type, code, label,
        detail, semantics, scope, refs, locators, evidence, review, merge, limit,
    ]))


def amt(
    aid: str, rid: str, fy: str, value: int, currency: str,
    reported_amount: str, reported_unit: str, basis: str, scope: str,
    actor_id: str, payment_status: str, award_status: str, width: str,
    refs: str, locators: str, evidence: str = "E4", review: str = "ai_seeded",
    limit: str = "",
) -> dict[str, object]:
    return dict(zip(AMT_FIELDS, [
        aid, rid, fy, value, currency, currency, reported_amount, reported_unit,
        basis, scope, actor_id, payment_status, award_status, width, refs, locators,
        evidence, review, limit,
    ]))


def fun(
    fid: str, rid: str, fy: str, actor_id: str, actor_name: str,
    function_type: str, description: str, beneficiary: str, place: str,
    mechanism: str, refs: str, locators: str, evidence: str = "E4",
    review: str = "ai_seeded", limit: str = "",
) -> dict[str, str]:
    return dict(zip(FUN_FIELDS, [
        fid, rid, fy, actor_id, actor_name, function_type, description,
        beneficiary, place, mechanism, "no", "no", refs, locators,
        evidence, review, limit,
    ]))


def build_relations() -> list[dict[str, str]]:
    rows = [
        rel("R10R001", "R10A001", "2019", "2019-06", "2020-03", "X011", "JICA沖縄", "public_institution_partner", "X010", "沖縄NGOセンター", "registered_actor", "JICA教師海外研修（九州・沖縄）", "commission", "", "委託", "官方项目报告将 ONC 列为本事业及报告书受托者", "commission_role_amount_not_public", "public_to_actor", "S100", "PDF p.103", merge="propose_new_relation", limit="受托角色可确认；没有公开合同金额，不推定资金规模。"),
        rel("R10R002", "R10A002", "2019", "2019-04-01", "2020-03-31", "PUB_OKINAWA_CITY", "冲绳市", "public_authority_provisional", "X010", "沖縄NGOセンター", "registered_actor", "Koza International Plaza 运营", "commission", "", "委託", "市级交付金检证表点名 ONC 为委托费接收者", "named_recipient_commission_flow", "public_to_actor", "R10S05", "PDF pp.9-10, 国际交流事業资金流", merge="propose_new_relation", limit="公共国际交流设施运营委托，不属于运动资金。"),
        rel("R10R003", "R10A003", "2020", "2020-04-01", "2021-03-31", "PUB_OKINAWA_CITY", "冲绳市", "public_authority_provisional", "X010", "沖縄NGOセンター", "registered_actor", "Koza International Plaza 运营", "commission", "", "委託", "市级交付金检证表点名 ONC 为委托费接收者", "named_recipient_commission_flow", "public_to_actor", "R10S06", "PDF pp.9-10, 国际交流事業资金流", merge="propose_new_relation", limit="公共国际交流设施运营委托，不属于运动资金。"),
        rel("R10R004", "R10A004;R10A005;R10A020;F033", "2024", "2024-04-01", "2025-03-31", "PUB_OKINAWA_CITY", "冲绳市", "public_authority_provisional", "X010", "沖縄NGOセンター", "registered_actor", "Koza International Plaza 管理运营", "commission", "", "委託", "同一 FY2024 关系折叠市侧资金流、ONC 事业费与服务说明", "named_recipient_flow_plus_parallel_costs", "public_to_actor", "R10S07;S099;R10S09;R10S10", "R10S07 PDF pp.5-6; S099 PDF pp.1-2", merge="update_existing_F033", limit="16.662m 只是交付对象部分；2.196m 与 ONC 16.040m 必须作为不同金额口径保留。"),
        rel("R10R005", "R10A006;R10A007;R10A019;F032", "2024", "2024-07-04", "2025-03-31", "PUB_OKINAWA_PREF", "冲绳县", "public_authority_provisional", "X010", "沖縄NGOセンター", "registered_actor", "多文化共生社会の構築に関する万国津梁会議运营支援", "commission", "C1", "委託", "官方 C=1；会议事务局功能附着于同一关系", "commission_relation_project_costs_only", "public_to_actor", "S002;S099;R10S08;R10S12", "S002 PDF p.59 row 431; S099 PDF pp.3,8; R10S12 PDF p.2", merge="update_existing_F032", limit="5.140m 与 5,530,234 都是项目成本观察，不是确认合同支付额。"),
        rel("R10R006", "R10A008;F031", "2024", "2024-04", "2025-03", "PUB_MOFA", "外务省", "public_authority_provisional", "X010", "沖縄NGOセンター", "registered_actor", "NGO相談員（外務省委託）", "commission", "", "委託", "ONC 法定报告明确写外务省委托", "commission_relation_organization_cost_only", "public_to_actor", "S099", "PDF pp.2,8", merge="update_existing_F031", limit="2,894,630 日元是 ONC 事业分类成本，不是 MOFA 支付额或合同额。"),
        rel("R10R007", "R10A009;F031", "2026", "2026-04-01", "2027-03-31", "PUB_MOFA", "外务省", "public_authority_provisional", "X010", "沖縄NGOセンター", "registered_actor", "令和8年度 NGO相談員", "designated_role", "", "指定角色", "官方名单确认年度指定延续", "designation_no_amount", "public_to_actor", "S101", "official list, FY2026", merge="update_existing_F031_time_extension", limit="指定延续不提供金额，也不证明对其他冲绳 NGO 的资助。"),
        rel("R10R008", "R10A010;R10V008", "2024", "2024-05-16", "2025-03-31", "PUB_OKINAWA_PREF", "冲绳县", "public_authority_provisional", "A066", "新外交イニシアティブ（ND）", "registered_actor", "在冲美军基地问题研讨会举办业务", "commission", "C2", "提案型公募委託", "修正原 generic administrative collaboration 错分", "confirmed_contract", "public_to_actor", "S002;R10S11;R10S12", "S002 PDF p.1 row 1; R10S11 PDF p.1 row 2; R10S12 PDF p.2", merge="propose_new_relation_after_human_review", limit="实际合同可确认；不等于 grant、政治支持或运动资金。"),
        rel("R10R009", "R10A011;R10V009", "2024", "2024-06-12", "2025-03-14", "PUB_OKINAWA_PREF", "冲绳县", "public_authority_provisional", "A088", "特定非营利活动法人冲绳和平协力中心", "registered_actor", "“和平之思”传播·交流·传承事业", "commission", "C2", "提案型公募委託", "修正原 non-funding relation 错分", "confirmed_contract", "public_to_actor", "S002;R10S11;R10S12", "S002 PDF p.2 row 10; R10S11 PDF p.2 row 11; R10S12 PDF p.2", merge="propose_new_relation_after_human_review", limit="合同机制确认；项目主题不能替代组织整体立场判断。"),
        rel("R10R010", "R10A012;R10V010", "2024", "2024-06-12", "2025-03-14", "PUB_OKINAWA_PREF", "冲绳县", "public_authority_provisional", "A088", "特定非营利活动法人冲绳和平协力中心", "registered_actor", "冲绳战讲述者培养事业", "commission", "C2", "提案型公募委託", "修正原 non-funding relation 错分", "confirmed_contract", "public_to_actor", "S002;R10S11;R10S12", "S002 PDF p.2 row 11; R10S11 PDF p.2 row 12; R10S12 PDF p.2", merge="propose_new_relation_after_human_review", limit="合同机制确认；不得与另一合同合并为一笔。"),
        rel("R10R011", "R10A013", "2024", "2024-05-15", "2025-02-28", "PUB_OKINAWA_PREF", "冲绳县", "public_authority_provisional", "P_R10_IC_HRD_JV", "国际协力人才培养事业共同企业体", "provisional_composite_actor", "冲绳国际协力人才培养事业", "commission", "C2", "提案型公募委託", "JV 由青年海外协力协会冲绳事务所与 JTB 冲绳组成", "commission_relation_project_cost_only", "public_to_composite", "S002;R10S12", "S002 PDF p.59 row 432; R10S12 PDF p.2", merge="module_only_pending_actor_crosswalk", limit="项目总成本不能拆分给 JV 成员。"),
        rel("R10R012", "R10A014;R10V012", "2024", "2024-04-01", "2025-03-31", "PUB_OKINAWA_PREF", "冲绳县", "public_authority_provisional", "P_R10_WYUR", "世界若者ウチナーンチュ连合会", "provisional_actor", "次世代ウチナーネットワーク继承基础建设（UNC 运营）", "commission", "C1", "委託", "修正原 service 关系错分；service 只保留为功能", "commission_relation_project_cost_only", "public_to_actor", "S002;R10S12", "S002 PDF pp.59-60 row 433; R10S12 PDF p.2", merge="module_only_pending_actor_crosswalk", limit="10.329m 是协作表项目费，不是确认合同额。"),
        rel("R10R013", "R10A015", "2024", "2024-04-01", "2025-03-31", "PUB_OKINAWA_PREF", "冲绳县", "public_authority_provisional", "P_R10_TEAM_OKIYUA", "Team OKIYUA", "provisional_composite_actor", "次世代ウチナーネットワーク继承基础建设（留学生接收）", "commission", "C1", "委託", "共同企业体含冲绳映像中心与世界若者ウチナーンチュ连合会", "commission_relation_project_cost_only", "public_to_composite", "S002;R10S12", "S002 PDF p.60 row 434; R10S12 PDF p.2", merge="module_only_pending_actor_crosswalk", limit="39.739m 不能拆给成员组织。"),
        rel("R10R014", "R10A016;R10V014", "2024", "2024-05-24", "2025-02-28", "PUB_OKINAWA_PREF", "冲绳县", "public_authority_provisional", "P_R10_JOCA_OKINAWA", "青年海外协力协会冲绳事务所", "provisional_actor", "Let's Study! Uchina Network", "commission", "C2", "提案型公募委託", "修正原 service 关系错分；教育服务保留为功能", "commission_relation_project_cost_only", "public_to_actor", "S002;R10S12", "S002 PDF p.60 row 435; R10S12 PDF p.2", merge="module_only_pending_actor_crosswalk", limit="7.171m 是协作表项目费，不是确认支付额。"),
        rel("R10R015", "R10A017", "2024", "2024-04-30", "2025-02-28", "PUB_OKINAWA_PREF", "冲绳县", "public_authority_provisional", "P_R10_JUNIOR_STUDY_JV", "Uchina Junior Study 共同企业体", "provisional_composite_actor", "Uchina Junior Study 事业", "commission", "C2", "提案型公募委託", "JV 由青年海外协力协会冲绳事务所与东武 Top Tours 冲绳支店组成", "commission_relation_project_cost_only", "public_to_composite", "S002;R10S12", "S002 PDF p.60 row 436; R10S12 PDF p.2", merge="module_only_pending_actor_crosswalk", limit="15.442m 不能拆给 JV 成员。"),
        rel("R10R016", "R10A018", "2024", "2024-04-01", "2025-03-31", "PUB_OKINAWA_PREF", "冲绳县", "public_authority_provisional", "P_R10_OIHF", "冲绳县国际交流·人才育成财团", "provisional_actor", "国际交流·协力推进事业", "grant", "C4", "補助", "官方 C=4 且叙述说明支付补助金", "grant_relation_project_cost_not_award", "public_to_actor", "S002;R10S12", "S002 PDF p.60 row 437; R10S12 PDF p.2", merge="module_only_pending_award_record", limit="17.932m 是项目费字段，不自动等于补助决定额。"),
        rel("R10R017", "F011", "", "", "", "X010", "沖縄NGOセンター", "registered_actor", "X011", "JICA沖縄", "registered_actor", "国际协力 festival 协作", "event_collaboration", "", "活动协作", "官方页面公开列名", "non_funding_collaboration", "actor_to_actor", "S095", "ONC/JICA official program pages", review="human_checked", merge="already_in_main_F011", limit="共同参与活动不是资金关系或稳定联盟。"),
        rel("R10R018", "F003;F004;F005", "", "", "", "X001", "USO Okinawa", "registered_actor", "BENEF_US_MIL_FAMILIES", "美军现役人员、预备役/国民警卫队、配偶及家属", "beneficiary_group", "USO Okinawa 基地社区服务", "service_presence", "", "服务存在", "8 个公开服务点；不含金额语义", "service_presence_no_funding", "actor_to_beneficiary_group", "S097", "USO Okinawa centers and audience page", evidence="E4", merge="module_only_consolidated_service_relation", limit="按服务功能编码，不推断亲基地或反基地立场。"),
        rel("R10R019", "F002", "2026", "", "", "X003", "American Engineering Corporation (AEC)", "registered_actor", "X001", "USO Okinawa", "registered_actor", "USO Okinawa 长期企业伙伴", "sponsorship", "", "企业赞助", "Silver sponsor；另有一笔公开 16,000 美元捐赠", "sponsor_tier_plus_named_donation", "actor_to_actor", "S097;S098", "S097 sponsors page; S098 named donation report", review="human_checked", merge="already_in_main_F002", limit="赞助与捐赠可确认；不据此推断企业或 USO 的基地政策立场。"),
        rel("R10R020", "F034", "", "", "", "P_R10_MBC", "Mediatti Broadband (MBC)", "provisional_corporate_actor", "X001", "USO Okinawa", "registered_actor", "USO Okinawa sponsor tier", "sponsorship", "", "企业赞助", "Platinum sponsor；页面未给金额或年度", "sponsor_tier_no_amount", "actor_to_actor", "S097", "USO Okinawa sponsors page", evidence="E3", merge="already_in_main_F034", limit="赞助层级不是金额。"),
        rel("R10R021", "F035", "", "", "", "P_R10_MATSON", "Matson", "provisional_corporate_actor", "X001", "USO Okinawa", "registered_actor", "USO Okinawa sponsor tier", "sponsorship", "", "企业赞助", "Mission Partner；页面未给金额或年度", "sponsor_tier_no_amount", "actor_to_actor", "S097", "USO Okinawa sponsors page", evidence="E3", merge="already_in_main_F035", limit="赞助层级不是金额。"),
        rel("R10R022", "F021", "2025", "2025-12", "2025-12", "X007", "Okinawa Enlisted Spouses' Club (OESC)", "registered_actor", "X001", "USO Okinawa", "registered_actor", "OESC 向 USO Okinawa 捐赠", "donation", "", "直接捐赠", "公开报道给出日期与 3,250 美元", "named_donation", "actor_to_actor", "S053", "Stripes Okinawa, Dec. 2025 report", review="human_checked", merge="already_in_main_F021", limit="直接慈善捐赠，不代表政治立场或运动关系。"),
        rel("R10R023", "F026", "", "", "", "X004", "American Welfare & Works Association (AWWA)", "registered_actor", "X001", "USO Okinawa", "registered_actor", "USO Kinser kitchen refresh", "grant", "", "慈善 grant", "USO 官方故事确认 grant；金额未公开", "named_grant_no_amount", "actor_to_actor", "S077", "USO official story", evidence="E3", review="human_checked", merge="already_in_main_F026", limit="只确认这项 grant，不外推完整年度 recipient 网络。"),
        rel("R10R024", "F006", "", "", "", "X004", "AWWA", "registered_actor", "X005", "NOSCO", "registered_actor", "AWWA umbrella membership", "network_membership", "", "成员关系", "军属配偶俱乐部伞状成员", "membership_no_funding", "actor_to_actor", "S041;S055;S072", "AWWA/NOSCO membership pages", review="human_revised", merge="already_in_main_F006", limit="成员关系不构成资助。"),
        rel("R10R025", "F007", "", "", "", "X004", "AWWA", "registered_actor", "X006", "KOSC", "registered_actor", "AWWA umbrella membership", "network_membership", "", "成员关系", "军属配偶俱乐部伞状成员", "membership_no_funding", "actor_to_actor", "S041;S055;S072;S075", "AWWA/KOSC membership pages", review="human_revised", merge="already_in_main_F007", limit="成员关系不构成资助。"),
        rel("R10R026", "F022", "", "", "", "X004", "AWWA", "registered_actor", "X007", "OESC", "registered_actor", "AWWA umbrella membership", "network_membership", "", "成员关系", "军属配偶俱乐部伞状成员", "membership_no_funding", "actor_to_actor", "S041;S055", "AWWA/OESC membership pages", review="human_revised", merge="already_in_main_F022", limit="成员关系不构成资助。"),
        rel("R10R027", "F023", "", "", "", "X004", "AWWA", "registered_actor", "X016", "MOSCO", "registered_actor", "AWWA umbrella membership", "network_membership", "", "成员关系", "军属配偶俱乐部伞状成员", "membership_no_funding", "actor_to_actor", "S041;S055;S079", "AWWA/MOSCO membership pages", review="human_revised", merge="already_in_main_F023", limit="成员关系不构成资助。"),
        rel("R10R028", "F024", "", "", "", "X004", "AWWA", "registered_actor", "X017", "Army Community Group of Okinawa", "registered_actor_identity_pending", "AWWA umbrella membership", "network_membership", "", "成员关系", "伞状成员线索；独立身份仍需二手来源", "membership_no_funding", "actor_to_actor", "S041;S072;S081", "AWWA/community sources", evidence="E3", review="needs_second_source", merge="already_in_main_F024", limit="成员关系不构成资助；组织身份仍待核。"),
        rel("R10R029", "F025", "", "", "", "X006", "KOSC", "registered_actor", "P_R10_KOSC_MIXED_RECIPIENTS", "scholarships 与 AWWA 混合口径", "composite_recipient_scope", "KOSC prior-year contribution report", "aggregate_history", "", "合并口径", "102,000 美元未拆分到 scholarships 与 AWWA", "aggregate_mixed_recipient_no_allocation", "actor_to_composite", "S075", "KOSC charity page", review="needs_local_retrieval", merge="replace_F025_with_aggregate_observation_proposal", limit="不得把全部 102,000 美元写成付给 AWWA。"),
        rel("R10R030", "F027", "", "", "", "X004", "AWWA", "registered_actor", "UNKNOWN_OKINAWA_WELFARE", "冲绳福利设施（未逐一列名）", "aggregate_recipient_scope", "AWWA long-term donation history", "aggregate_history", "", "长期累计口径", "40 年约 8 亿日元；不是年度 recipient 表", "aggregate_history_no_allocation", "actor_to_aggregate", "S078", "Ryukyu Shimpo English long-term aggregate", evidence="E3", review="needs_local_retrieval", merge="already_in_main_F027", limit="累计口径不能拆给任何具体 recipient 或年度。"),
        rel("R10R031", "F028", "2015", "2015-12-02", "2015-12-02", "X004", "AWWA", "registered_actor", "R_YOMITAN_QUEGOEN", "Yomitan Quegoen disability facility", "named_recipient", "轮椅无障碍车辆捐赠", "in_kind_donation", "", "实物捐赠", "报道给出 200 万日元车辆价值", "named_in_kind_item_value", "actor_to_recipient", "S094", "DVIDS, 2015-12-02", evidence="E3", review="needs_second_source", merge="already_in_main_F028", limit="金额是实物价值，不是现金支付；军方 PA 来源需保持 E3。"),
        rel("R10R032", "F029", "2012", "", "", "X004", "AWWA", "registered_actor", "R_URUMA_SOCIAL_WELFARE", "Uruma City Social Welfare Meeting", "named_recipient", "无障碍车辆捐赠", "in_kind_donation", "", "实物捐赠", "点名冲绳福利 recipient；未公开金额", "named_in_kind_no_amount", "actor_to_recipient", "S072", "DVIDS 40-year AWWA article", evidence="E3", review="needs_second_source", merge="already_in_main_F029", limit="只确认点名实物 recipient。"),
        rel("R10R033", "F030", "2012", "", "", "X004", "AWWA", "registered_actor", "R_BSA_FAR_EAST", "Boy Scouts of America Far East Council", "named_recipient", "皮划艇捐赠", "in_kind_donation", "", "实物捐赠", "点名美军社区 recipient；未公开金额", "named_in_kind_no_amount", "actor_to_recipient", "S072", "DVIDS 40-year AWWA article", evidence="E3", review="needs_second_source", merge="already_in_main_F030", limit="recipient 属美军社区，不能写成对冲绳本地福利组织的捐赠。"),
        rel("R10R034", "F036", "2025", "", "", "X005", "NOSCO", "registered_actor", "R_HESHIKIYA_CHILDCARE", "Heshikiya after-school childcare center", "named_recipient_identity_pending", "三台工业冷风机共同捐赠", "joint_in_kind_contribution", "", "共同实物贡献", "NOSCO 是四个贡献团体之一；份额与物品价值未拆", "joint_contribution_no_share_allocation", "actor_to_recipient", "S102", "DVIDS joint donation report", evidence="E3", review="needs_second_source", merge="already_in_main_F036", limit="不能把全部三台设备或全部价值归给 NOSCO。"),
        rel("R10R035", "F012", "2024", "", "2024-04-15", "X013", "U.S. Consulate General Naha Okinawa Youth Council Program", "registered_program_actor", "UNKNOWN_RECIPIENT", "未公开 recipient", "unknown_recipient", "Okinawa Youth Council Program NOFO", "grant_opportunity", "", "NOFO／机会公告", "机会存在且已截止；未发现 award 或 recipient", "opportunity_only_no_award", "program_to_unknown", "S056;S082;S083;S084", "NOFO and award-search records", review="human_checked", merge="do_not_merge_as_award_or_recipient", limit="不得写成已拨款、已有 recipient 或与 TOFU 项目相同。"),
    ]
    return rows


def build_amounts() -> list[dict[str, object]]:
    return [
        amt("R10AM001", "R10R002", "2019", 17_157_000, "JPY", "17157", "JPY_thousand", "municipal_named_recipient_commission_flow", "full recorded KIP commission flow", "X010", "confirmed_named_recipient_flow", "not_applicable", "yes_same_currency_scope", "R10S05", "PDF pp.9-10", limit="公开资金流点名 ONC；公共设施运营委托，非运动资金。"),
        amt("R10AM002", "R10R003", "2020", 16_970_000, "JPY", "16970", "JPY_thousand", "municipal_named_recipient_commission_flow", "full recorded KIP commission flow", "X010", "confirmed_named_recipient_flow", "not_applicable", "yes_same_currency_scope", "R10S06", "PDF pp.9-10", limit="公开资金流点名 ONC；公共设施运营委托，非运动资金。"),
        amt("R10AM003", "R10R004", "2024", 18_858_000, "JPY", "18858", "JPY_thousand", "municipal_total_project_cost", "KIP total project cost", "", "not_actor_payment", "not_applicable", "no", "R10S07", "PDF pp.5-6", limit="总事业费不能写成付给 ONC 的金额。"),
        amt("R10AM004", "R10R004", "2024", 16_662_000, "JPY", "16662", "JPY_thousand", "municipal_named_recipient_commission_flow", "eligible-project portion paid as commission to ONC", "X010", "confirmed_partial_scope_named_recipient_flow", "not_applicable", "conditional_partial_scope", "R10S07", "PDF pp.5-6", limit="只覆盖交付对象部分；不能单独代表完整年度委托支付。"),
        amt("R10AM005", "R10R004", "2024", 2_196_000, "JPY", "2196", "JPY_thousand", "municipal_noneligible_commission_observation", "March operating commission outside eligible-project costs", "", "recipient_scope_unresolved", "not_applicable", "no", "R10S07", "PDF pp.5-6", limit="保留为同一项目的独立口径；来源图未在本模型中将其归给 ONC。"),
        amt("R10AM006", "R10R004", "2024", 16_040_000, "JPY", "16040", "JPY_thousand", "organization_reported_project_cost", "ONC KIP project cost", "X010", "not_actor_payment", "not_applicable", "no", "S099", "PDF pp.1-2", limit="组织侧事业费不是合同收入或现金到账。"),
        amt("R10AM007", "R10R005", "2024", 5_140_000, "JPY", "5140", "JPY_thousand", "prefecture_collaboration_table_project_cost", "prefecture table project cost", "", "not_actor_payment", "not_applicable", "no", "S002", "PDF p.59 row 431", limit="项目费字段不等于支付给 ONC 的金额。"),
        amt("R10AM008", "R10R005", "2024", 5_530_234, "JPY", "5530234", "JPY", "organization_reported_project_cost", "ONC exact project-category cost; narrative rounds to 5,530 thousand", "X010", "not_actor_payment", "not_applicable", "no", "S099", "PDF p.8; narrative p.3", limit="组织侧成本不是县合同额或支付额。"),
        amt("R10AM009", "R10R006", "2024", 2_894_630, "JPY", "2894630", "JPY", "organization_reported_project_cost", "ONC MOFA consultant project-category cost; narrative rounds to 2,894 thousand", "X010", "not_actor_payment", "not_applicable", "no", "S099", "PDF p.8; narrative p.2", limit="不得写成 MOFA 支付 ONC 2.894m。"),
        amt("R10AM010", "R10R008", "2024", 12_843_000, "JPY", "12843", "JPY_thousand", "prefecture_collaboration_table_project_cost", "collaboration survey project cost", "", "not_actor_payment", "not_applicable", "no", "S002", "PDF p.1 row 1", limit="千元项目费不是精确合同额，也不是公募上限的替代标签。"),
        amt("R10AM011", "R10R008", "2024", 12_842_500, "JPY", "12842500", "JPY", "actual_contract_amount", "named counterparty contract", "A066", "confirmed_contract", "not_applicable", "yes_same_currency_scope", "R10S11", "PDF p.1 row 2", limit="实际合同额；委托不是 grant 或运动资金。"),
        amt("R10AM012", "R10R009", "2024", 25_547_000, "JPY", "25547", "JPY_thousand", "prefecture_collaboration_table_project_cost", "collaboration survey project cost", "", "not_actor_payment", "not_applicable", "no", "S002", "PDF p.2 row 10", limit="项目费与实际合同额分栏。"),
        amt("R10AM013", "R10R009", "2024", 26_439_000, "JPY", "26439000", "JPY", "actual_contract_amount", "named counterparty contract", "A088", "confirmed_contract", "not_applicable", "yes_same_currency_scope", "R10S11", "PDF p.2 row 11", limit="实际合同额；不得与另一合同相加后归为单一关系。"),
        amt("R10AM014", "R10R010", "2024", 6_496_000, "JPY", "6496", "JPY_thousand", "prefecture_collaboration_table_project_cost", "collaboration survey project cost", "", "not_actor_payment", "not_applicable", "no", "S002", "PDF p.2 row 11", limit="项目费与实际合同额分栏。"),
        amt("R10AM015", "R10R010", "2024", 8_479_000, "JPY", "8479000", "JPY", "actual_contract_amount", "named counterparty contract", "A088", "confirmed_contract", "not_applicable", "yes_same_currency_scope", "R10S11", "PDF p.2 row 12", limit="实际合同额；不得与另一合同相加后归为单一关系。"),
        amt("R10AM016", "R10R011", "2024", 21_799_000, "JPY", "21799", "JPY_thousand", "prefecture_collaboration_table_project_cost", "JV project cost", "", "not_actor_payment", "not_applicable", "no", "S002", "PDF p.59 row 432", limit="不得拆分给 JV 成员。"),
        amt("R10AM017", "R10R012", "2024", 10_329_000, "JPY", "10329", "JPY_thousand", "prefecture_collaboration_table_project_cost", "program project cost", "", "not_actor_payment", "not_applicable", "no", "S002", "PDF pp.59-60 row 433", limit="不是确认合同支付额。"),
        amt("R10AM018", "R10R013", "2024", 39_739_000, "JPY", "39739", "JPY_thousand", "prefecture_collaboration_table_project_cost", "JV project cost", "", "not_actor_payment", "not_applicable", "no", "S002", "PDF p.60 row 434", limit="不得拆分给共同企业体成员。"),
        amt("R10AM019", "R10R014", "2024", 7_171_000, "JPY", "7171", "JPY_thousand", "prefecture_collaboration_table_project_cost", "program project cost", "", "not_actor_payment", "not_applicable", "no", "S002", "PDF p.60 row 435", limit="不是确认合同支付额。"),
        amt("R10AM020", "R10R015", "2024", 15_442_000, "JPY", "15442", "JPY_thousand", "prefecture_collaboration_table_project_cost", "JV project cost", "", "not_actor_payment", "not_applicable", "no", "S002", "PDF p.60 row 436", limit="不得拆分给共同企业体成员。"),
        amt("R10AM021", "R10R016", "2024", 17_932_000, "JPY", "17932", "JPY_thousand", "prefecture_collaboration_table_project_cost", "grant-related program project cost", "", "not_actor_payment", "relation_confirmed_amount_not_award", "no", "S002", "PDF p.60 row 437", limit="补助关系可确认；项目费不是补助决定额。"),
        amt("R10AM022", "R10R019", "2026", 16_000, "USD", "16000", "USD", "documented_donation", "named donation to USO Okinawa", "X001", "confirmed_donation", "not_applicable", "yes_same_currency_scope", "S098", "named donation report", review="human_checked", limit="捐赠不是 sponsor tier 的金额换算，也不代表政治立场。"),
        amt("R10AM023", "R10R022", "2025", 3_250, "USD", "3250", "USD", "documented_donation", "named donation to USO Okinawa", "X001", "confirmed_donation", "not_applicable", "yes_same_currency_scope", "S053", "Dec. 2025 report", review="human_checked", limit="直接慈善捐赠。"),
        amt("R10AM024", "R10R029", "", 102_000, "USD", "102000", "USD", "aggregate_mixed_recipient_report", "scholarships plus AWWA combined", "", "not_allocable_to_named_actor", "not_applicable", "no", "S075", "KOSC charity page", review="needs_local_retrieval", limit="不得把全额分配给 AWWA 或任一 scholarship recipient。"),
        amt("R10AM025", "R10R030", "", 800_000_000, "JPY", "800000000", "JPY", "aggregate_long_term_history", "approximately 40-year network total", "", "not_allocable_to_named_actor_or_year", "not_applicable", "no", "S078", "long-term aggregate report", evidence="E3", review="needs_local_retrieval", limit="不能拆分到年度或具体 recipient。"),
        amt("R10AM026", "R10R031", "2015", 2_000_000, "JPY", "2000000", "JPY", "reported_in_kind_item_value", "wheelchair-accessible vehicle value", "R_YOMITAN_QUEGOEN", "confirmed_in_kind_value_not_cash", "not_applicable", "no", "S094", "DVIDS 2015-12-02", evidence="E3", review="needs_second_source", limit="实物价值不是现金支付。"),
    ]


def build_functions() -> list[dict[str, str]]:
    rows = [
        fun("R10FN001", "R10R001", "2019", "X010", "沖縄NGOセンター", "international_cooperation_training", "承担教师海外研修与报告制作", "九州/冲绳教师与国际理解教育参与者", "JICA 九州・冲绳项目", "commission", "S100", "PDF p.103"),
        fun("R10FN002", "R10R004", "2024", "X010", "沖縄NGOセンター", "multilingual_consultation", "每周六日提供多语言生活咨询并转介专业机构", "外国居民及多语种服务使用者", "Koza International Plaza", "commission", "R10S07;R10S09;R10S10", "R10S07 PDF pp.5-6"),
        fun("R10FN003", "R10R004", "2024", "X010", "沖縄NGOセンター", "language_education", "开设英语、西班牙语、中文、日语与越南语课程", "冲绳市居民与外国居民", "Koza International Plaza", "commission", "R10S07;R10S09;R10S10", "R10S07 PDF pp.5-6"),
        fun("R10FN004", "R10R004", "2024", "X010", "沖縄NGOセンター", "international_exchange_service", "举办多国籍居民交流会与文化活动", "多国籍居民与本地居民", "Koza International Plaza", "commission", "R10S07;R10S09;R10S10", "R10S07 PDF pp.5-6"),
        fun("R10FN005", "R10R005", "2024", "X010", "沖縄NGOセンター", "multicultural_policy_support", "运营多文化共生政策会议并整理建议", "冲绳县政策部门、会议委员与在住外国人相关议题", "冲绳县", "C1 commission", "S002;S099", "S002 PDF p.59; S099 PDF p.3"),
        fun("R10FN006", "R10R005", "2024", "X010", "沖縄NGOセンター", "meeting_secretariat", "ONC 人员在会议纪要中以事务局角色出现", "政策会议参与者", "万国津梁会议", "role evidence attached to commission", "R10S08", "official meeting minutes", limit="事务局功能不另造资金边。"),
        fun("R10FN007", "R10R006", "2024", "X010", "沖縄NGOセンター", "ngo_consultation", "提供国际协力与 ODA 市民参与相关咨询", "NGO、市民与国际协力参与者", "冲绳/日本", "commission", "S099", "PDF p.2"),
        fun("R10FN008", "R10R007", "2026", "X010", "沖縄NGOセンター", "ngo_consultation", "作为外务省指定 NGO 相談員持续提供咨询", "NGO 与市民", "冲绳/日本", "designated role", "S101", "official FY2026 list"),
        fun("R10FN009", "R10R008", "2024", "A066", "新外交イニシアティブ（ND）", "base_policy_public_information", "举办在冲美军基地问题研讨会并对外传播信息", "县内外公众", "冲绳县项目", "C2 commission", "S002;R10S11", "S002 PDF p.1; R10S11 PDF p.1"),
        fun("R10FN010", "R10R009", "2024", "A088", "冲绳和平协力中心", "peace_education_exchange", "组织冲绳、广岛、长崎及亚洲青年共同学习和平教育", "青年参与者与公众", "冲绳和平祈念资料馆项目", "C2 commission", "S002;R10S11", "S002 PDF p.2; R10S11 PDF p.2"),
        fun("R10FN011", "R10R010", "2024", "A088", "冲绳和平协力中心", "oral_history_training", "培养冲绳战讲述者与传承人才", "讲述者候选与公众", "冲绳和平祈念资料馆项目", "C2 commission", "S002;R10S11", "S002 PDF p.2; R10S11 PDF p.2"),
        fun("R10FN012", "R10R011", "2024", "P_R10_IC_HRD_JV", "国际协力人才培养事业共同企业体", "international_cooperation_training", "派遣高中生观察 ODA 现场并开展出前讲座", "冲绳县内高中生", "冲绳/开发中国家", "C2 commission", "S002", "PDF p.59 row 432"),
        fun("R10FN013", "R10R012", "2024", "P_R10_WYUR", "世界若者ウチナーンチュ连合会", "diaspora_network_service", "运营 Uchina Network Concierge 平台", "世界冲绳人网络与下一代参与者", "线上/冲绳", "C1 commission", "S002", "PDF pp.59-60 row 433"),
        fun("R10FN014", "R10R013", "2024", "P_R10_TEAM_OKIYUA", "Team OKIYUA", "diaspora_student_exchange", "接收海外冲绳人子弟及亚洲地区留学生", "留学生与县内大学/企业", "冲绳", "C1 commission", "S002", "PDF p.60 row 434"),
        fun("R10FN015", "R10R014", "2024", "P_R10_JOCA_OKINAWA", "青年海外协力协会冲绳事务所", "migration_history_education", "面向学校开展移民史与 Uchina Network 出前讲座", "县内小中高校学生", "冲绳县内学校", "C2 commission", "S002", "PDF p.60 row 435"),
        fun("R10FN016", "R10R015", "2024", "P_R10_JUNIOR_STUDY_JV", "Uchina Junior Study 共同企业体", "diaspora_youth_exchange", "让海外县系人子弟与县内学生共同学习历史文化与自然", "海外县系人子弟与县内学生", "冲绳", "C2 commission", "S002", "PDF p.60 row 436"),
        fun("R10FN017", "R10R016", "2024", "P_R10_OIHF", "冲绳县国际交流·人才育成财团", "international_exchange_grant_program", "开展国际交流与协力事业", "国际交流参与者", "冲绳/国际", "C4 grant", "S002", "PDF p.60 row 437", limit="功能与补助关系可确认；项目费不等于 award amount。"),
        fun("R10FN018", "R10R017", "", "X010", "沖縄NGOセンター", "event_collaboration", "参与 JICA 国际协力 festival", "国际协力活动参与者", "冲绳", "non-funding collaboration", "S095", "official program page", review="human_checked", limit="公开共同参与不证明资金或稳定联盟。"),
    ]

    uso_sites = [
        "Camp Kinser", "Camp Hansen", "Kadena", "Camp Foster",
        "Kadena AMC Terminal", "Okinawa Area Office", "Futenma", "Camp Schwab",
    ]
    for index, site in enumerate(uso_sites, start=19):
        rows.append(fun(
            f"R10FN{index:03d}", "R10R018", "", "X001", "USO Okinawa",
            "base_community_service_site", "提供休息、联络与军人家庭支持服务",
            "美军现役人员、预备役/国民警卫队、配偶及家属", site,
            "service presence; no funding inference", "S097", "USO Okinawa centers page",
            limit="服务对象与设点不推导亲基地或反基地立场。",
        ))

    rows.extend([
        fun("R10FN027", "R10R019", "2026", "X003", "AEC", "corporate_sponsorship", "长期支持 USO Okinawa 并参与中心建设/翻新", "USO Okinawa 服务对象", "Camp Schwab 等", "sponsorship plus named donation", "S097;S098", "sponsors page and donation report", review="human_checked"),
        fun("R10FN028", "R10R020", "", "P_R10_MBC", "Mediatti Broadband", "corporate_sponsorship", "以 Platinum sponsor 身份支持 USO Okinawa", "USO Okinawa 服务对象", "冲绳", "sponsor tier; no amount", "S097", "sponsors page", evidence="E3"),
        fun("R10FN029", "R10R021", "", "P_R10_MATSON", "Matson", "corporate_sponsorship", "以 Mission Partner 身份支持 USO Okinawa", "USO Okinawa 服务对象", "冲绳", "sponsor tier; no amount", "S097", "sponsors page", evidence="E3"),
        fun("R10FN030", "R10R022", "2025", "X007", "OESC", "charitable_donation", "向 USO Okinawa 捐赠 3,250 美元", "USO Okinawa 服务对象", "冲绳", "named donation", "S053", "Dec. 2025 report", review="human_checked"),
        fun("R10FN031", "R10R023", "", "X004", "AWWA", "charitable_grant", "支持 USO Kinser 厨房翻新", "USO Kinser 使用者", "Camp Kinser", "named grant; amount unknown", "S077", "USO official story", evidence="E3", review="human_checked"),
        fun("R10FN032", "R10R024", "", "X004", "AWWA", "umbrella_coordination", "连接 NOSCO 等军属配偶俱乐部", "成员俱乐部", "冲绳美军基地社区", "membership; no funding inference", "S041;S055;S072", "membership pages", review="human_revised"),
        fun("R10FN033", "R10R025", "", "X004", "AWWA", "umbrella_coordination", "连接 KOSC 等军属配偶俱乐部", "成员俱乐部", "Kadena/冲绳", "membership; no funding inference", "S041;S055;S072;S075", "membership pages", review="human_revised"),
        fun("R10FN034", "R10R026", "", "X004", "AWWA", "umbrella_coordination", "连接 OESC 等军属配偶俱乐部", "成员俱乐部", "冲绳美军基地社区", "membership; no funding inference", "S041;S055", "membership pages", review="human_revised"),
        fun("R10FN035", "R10R027", "", "X004", "AWWA", "umbrella_coordination", "连接 MOSCO 等军属配偶俱乐部", "成员俱乐部", "Camp Foster/冲绳", "membership; no funding inference", "S041;S055;S079", "membership pages", review="human_revised"),
        fun("R10FN036", "R10R028", "", "X004", "AWWA", "umbrella_coordination", "Army Community Group 成员线索", "成员俱乐部", "冲绳美军基地社区", "membership; identity pending", "S041;S072;S081", "community sources", evidence="E3", review="needs_second_source"),
        fun("R10FN037", "R10R029", "", "X006", "KOSC", "aggregate_charity_reporting", "报告 scholarships 与 AWWA 合计捐赠", "混合 recipient 范围", "Kadena/冲绳", "aggregate; no allocation", "S075", "KOSC charity page", review="needs_local_retrieval"),
        fun("R10FN038", "R10R030", "", "X004", "AWWA", "aggregate_charity_reporting", "长期支持冲绳福利设施的累计口径", "未逐一列名福利设施", "冲绳", "aggregate; no annual allocation", "S078", "long-term aggregate report", evidence="E3", review="needs_local_retrieval"),
        fun("R10FN039", "R10R031", "2015", "X004", "AWWA", "local_welfare_in_kind_support", "向读谷残障成人设施捐赠无障碍车辆", "残障成人与设施使用者", "读谷", "named in-kind donation", "S094", "DVIDS 2015-12-02", evidence="E3", review="needs_second_source"),
        fun("R10FN040", "R10R032", "2012", "X004", "AWWA", "local_welfare_in_kind_support", "向宇流麻社会福利机构捐赠无障碍车辆", "老年人与福利服务使用者", "宇流麻", "named in-kind donation", "S072", "DVIDS 40-year article", evidence="E3", review="needs_second_source"),
        fun("R10FN041", "R10R033", "2012", "X004", "AWWA", "military_community_youth_support", "向 Boy Scouts Far East Council 捐赠皮划艇", "美军社区童军", "冲绳", "named in-kind donation", "S072", "DVIDS 40-year article", evidence="E3", review="needs_second_source"),
        fun("R10FN042", "R10R034", "2025", "X005", "NOSCO", "joint_local_childcare_support", "参与向平敷屋课后托育中心交付三台工业冷风机", "课后托育儿童与工作人员", "平敷屋/宇流麻", "joint in-kind contribution", "S102", "DVIDS joint donation report", evidence="E3", review="needs_second_source", limit="只确认参与共同交付，不能归属全部物品或价值。"),
        fun("R10FN043", "R10R035", "2024", "X013", "Okinawa Youth Council Program", "public_diplomacy_opportunity", "发布青年项目 NOFO", "潜在申请者；recipient 未公开", "冲绳", "opportunity only; no award", "S056;S082;S083;S084", "NOFO and award-search records", review="human_checked", limit="机会公告不是拨款、award 或 recipient 关系。"),
    ])
    return rows


MODULE_SOURCES = [
    {"source_ref": "R10S05", "title": "冲绳市 FY2019 交付金事业检证表", "url": "https://www.city.okinawa.okinawa.jp/documents/1858/1kanryou.pdf", "status": "module_candidate_not_in_main_log", "locator_coverage": "KIP PDF pp.9-10", "merge_note": "archive and add to source log before main-table merge"},
    {"source_ref": "R10S06", "title": "冲绳市 FY2020 交付金事业检证表", "url": "https://www.city.okinawa.okinawa.jp/documents/1858/2kannryou.pdf", "status": "module_candidate_not_in_main_log", "locator_coverage": "KIP PDF pp.9-10", "merge_note": "archive and add to source log before main-table merge"},
    {"source_ref": "R10S07", "title": "冲绳市 FY2024 交付金事业检证表", "url": "https://www.city.okinawa.okinawa.jp/documents/1858/r0607okinawashi.pdf", "status": "module_candidate_not_in_main_log", "locator_coverage": "KIP PDF pp.5-6", "merge_note": "archive and add to source log before main-table merge"},
    {"source_ref": "R10S08", "title": "FY2024 第3回多文化共生万国津梁会议纪要", "url": "https://www.pref.okinawa.jp/_res/projects/default_project/_page_/001/034/046/3gaiyo.pdf", "status": "module_candidate_not_in_main_log", "locator_coverage": "secretariat role", "merge_note": "archive and add to source log before main-table merge"},
    {"source_ref": "R10S09", "title": "ONC 的活动", "url": "https://www.oki-ngo.org/project", "status": "module_candidate_not_in_main_log", "locator_coverage": "KIP/NGO consultant function", "merge_note": "distinct subpage; do not collapse into S095 without a page-level policy"},
    {"source_ref": "R10S10", "title": "Koza International Plaza 设施页", "url": "https://www.city.okinawa.okinawa.jp/k034/sportsbunka/bunkarekishi/bunkageijutsu/3938939394.html", "status": "module_candidate_not_in_main_log", "locator_coverage": "facility/service scope", "merge_note": "function evidence only"},
    {"source_ref": "R10S11", "title": "冲绳县 FY2024 第一季度随意合同实绩（知事公室）", "url": "https://www.pref.okinawa.jp/_res/projects/default_project/_page_/001/015/127/koushitsu1.pdf", "status": "module_candidate_not_in_main_log", "locator_coverage": "PDF p.1 A066; p.2 A088", "merge_note": "key official contract source; archive and add before merge"},
    {"source_ref": "R10S12", "title": "冲绳县 FY2024 NPO 协作调查结果汇总", "url": "https://www.pref.okinawa.jp/_res/projects/default_project/_page_/001/004/917/2r6kekka.pdf", "status": "module_candidate_not_in_main_log", "locator_coverage": "PDF p.2 mechanism-code dictionary", "merge_note": "code-definition source; archive and add before merge"},
]


def build_source_crosswalk(relations: list[dict[str, str]], amounts: list[dict[str, object]], functions: list[dict[str, str]]) -> list[dict[str, str]]:
    used: set[str] = set()
    for row in [*relations, *amounts, *functions]:
        used.update(ref for ref in str(row["source_refs"]).split(";") if ref)
    main_rows = {r["source_id"]: r for r in read_csv(DATA / "05_source_log_initial_v0.csv")}
    module = {r["source_ref"]: r for r in MODULE_SOURCES}
    output: list[dict[str, str]] = []
    for ref in sorted(used):
        if ref in main_rows:
            row = main_rows[ref]
            output.append({
                "source_ref": ref, "title": row["title"], "url": row["url"],
                "status": "existing_main_source", "locator_coverage": "see observation rows",
                "merge_note": "reuse; do not duplicate",
            })
        elif ref in module:
            output.append(module[ref])
        else:
            raise ValueError(f"Unresolved source ref: {ref}")
    return output


def build_mechanism_dictionary() -> list[dict[str, str]]:
    return [
        {"mechanism_code": "C1", "mechanism_label": "委託", "relation_semantics": "public body commissions a named organization", "amount_rule": "project-cost field is not payment unless a contract/funds-flow record says so", "visual_rule": "solid administrative relation; no amount width from project cost"},
        {"mechanism_code": "C2", "mechanism_label": "提案型公募による委託", "relation_semantics": "proposal-based public commission", "amount_rule": "proposal ceiling, project cost, and actual contract must remain separate", "visual_rule": "solid administrative relation; width only for exact contract or named flow"},
        {"mechanism_code": "C4", "mechanism_label": "補助", "relation_semantics": "subsidy/grant relation", "amount_rule": "collaboration-table project cost is not automatically the award amount", "visual_rule": "grant line without amount width until award decision is sourced"},
        {"mechanism_code": "", "mechanism_label": "指定角色", "relation_semantics": "official designation or service role", "amount_rule": "designation alone carries no amount", "visual_rule": "dashed role line"},
        {"mechanism_code": "", "mechanism_label": "赞助／捐赠", "relation_semantics": "corporate or charitable support", "amount_rule": "sponsor tier is non-numeric; named donation may carry its stated currency", "visual_rule": "separate from administrative commissions"},
        {"mechanism_code": "", "mechanism_label": "成员／服务存在", "relation_semantics": "umbrella membership, beneficiary service, or site presence", "amount_rule": "no funding inference", "visual_rule": "dotted non-financial line"},
        {"mechanism_code": "", "mechanism_label": "NOFO／机会", "relation_semantics": "opportunity exists", "amount_rule": "no award, recipient, or payment unless separately sourced", "visual_rule": "open outline; never a funding edge"},
    ]


def validate(relations: list[dict[str, str]], amounts: list[dict[str, object]], functions: list[dict[str, str]], sources: list[dict[str, str]]) -> None:
    def unique(rows: list[dict[str, object]], field: str) -> None:
        values = [str(r[field]) for r in rows]
        assert len(values) == len(set(values)), f"Duplicate {field}"

    unique(relations, "relation_observation_id")
    unique(amounts, "amount_observation_id")
    unique(functions, "function_observation_id")
    unique(sources, "source_ref")
    relation_ids = {r["relation_observation_id"] for r in relations}
    relation_by_id = {r["relation_observation_id"]: r for r in relations}
    assert all(str(r["relation_observation_id"]) in relation_ids for r in amounts)
    assert all(r["relation_observation_id"] in relation_ids for r in functions)

    for rows in (relations, amounts, functions):
        for row in rows:
            assert row["review_status"] in REVIEW_STATUSES, row
            fy = str(row["fiscal_year"])
            assert not fy or re.fullmatch(r"\d{4}", fy), row
            assert str(row["source_refs"]).strip(), row
            assert str(row["source_locators"]).strip(), row

    for row in amounts:
        assert isinstance(row["amount_value"], int) and row["amount_value"] > 0
        assert row["currency"] in {"JPY", "USD"}
        assert row["normalized_unit"] == row["currency"]
        assert row["reported_unit"] in {"JPY", "JPY_thousand", "USD"}
        relation_fy = relation_by_id[str(row["relation_observation_id"])]["fiscal_year"]
        assert not row["fiscal_year"] or not relation_fy or row["fiscal_year"] == relation_fy
        if "project_cost" in str(row["amount_basis"]):
            assert row["actor_payment_status"] == "not_actor_payment"
            assert row["line_width_eligible"] == "no"
        if "aggregate" in str(row["amount_basis"]):
            assert str(row["actor_payment_status"]).startswith("not_allocable")
            assert row["line_width_eligible"] == "no"
        if row["award_status"] == "relation_confirmed_amount_not_award":
            assert row["actor_payment_status"] == "not_actor_payment"

    for row in functions:
        relation_fy = relation_by_id[row["relation_observation_id"]]["fiscal_year"]
        assert not row["fiscal_year"] or not relation_fy or row["fiscal_year"] == relation_fy
        assert row["financial_inference_allowed"] == "no"
        assert row["political_stance_inference_allowed"] == "no"

    by_record: dict[str, dict[str, str]] = {}
    for row in relations:
        for record in row["source_record_ids"].split(";"):
            by_record[record] = row
    expected = {
        "R10A010": ("commission", "C2"),
        "R10A011": ("commission", "C2"),
        "R10A012": ("commission", "C2"),
        "R10A014": ("commission", "C1"),
        "R10A016": ("commission", "C2"),
    }
    for record, pair in expected.items():
        row = by_record[record]
        assert (row["relation_type"], row["official_mechanism_code"]) == pair

    exact_contracts = {
        (r["relation_observation_id"], r["amount_value"])
        for r in amounts if r["amount_basis"] == "actual_contract_amount"
    }
    assert exact_contracts == {
        ("R10R008", 12_842_500), ("R10R009", 26_439_000), ("R10R010", 8_479_000)
    }

    source_ids = {r["source_ref"] for r in sources}
    for row in [*relations, *amounts, *functions]:
        assert set(str(row["source_refs"]).split(";")) <= source_ids

    admin = [r for r in relations if r["relation_scope"].startswith("public_to")]
    lower = [r for r in relations if r not in admin]
    assert len(admin) == 16 and len(lower) == 19 and len(relations) == 35
    expected_type_counts = {
        "aggregate_history": 2, "commission": 14, "designated_role": 1,
        "donation": 1, "event_collaboration": 1, "grant": 2,
        "grant_opportunity": 1, "in_kind_donation": 3,
        "joint_in_kind_contribution": 1, "network_membership": 5,
        "service_presence": 1, "sponsorship": 3,
    }
    assert Counter(r["relation_type"] for r in relations) == expected_type_counts


def configure_fonts() -> None:
    candidates = ["Microsoft YaHei", "Yu Gothic", "Meiryo", "Noto Sans CJK SC", "SimHei", "DejaVu Sans"]
    available = {f.name for f in font_manager.fontManager.ttflist}
    for name in candidates:
        if name in available:
            plt.rcParams["font.family"] = name
            break
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["figure.facecolor"] = "white"


def card(ax, x: float, y: float, w: float, h: float, title: str, body: str, color: str, edge: str = "#334650") -> None:
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.015,rounding_size=0.025", facecolor=color, edgecolor=edge, linewidth=1.0)
    ax.add_patch(box)
    if h <= 0.14:
        title_offset, body_offset, body_size = 0.035, 0.082, 8.2
    else:
        title_offset, body_offset, body_size = 0.05, 0.12, 8.8
    ax.text(x + 0.025, y + h - title_offset, title, fontsize=11, fontweight="bold", va="top", color="#1f3038")
    ax.text(x + 0.025, y + h - body_offset, body, fontsize=body_size, va="top", color="#42545d", linespacing=1.28)


def save_mechanism_figure(relations: list[dict[str, str]]) -> None:
    admin = [r for r in relations if r["relation_scope"].startswith("public_to")]
    lower = [r for r in relations if r not in admin]
    lower_counts = Counter(r["relation_type"] for r in lower)
    c1 = sum(r["official_mechanism_code"] == "C1" for r in admin)
    c2 = sum(r["official_mechanism_code"] == "C2" for r in admin)
    c4 = sum(r["official_mechanism_code"] == "C4" for r in admin)
    other_admin = len(admin) - c1 - c2 - c4
    assert len(admin) == 16 and len(lower) == 19
    assert sum(lower_counts.values()) == 19

    fig, ax = plt.subplots(figsize=(15.5, 9.2))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.text(0.03, 0.95, "R10 行政与服务生态：机制不同，不构成同一“运动资金网”", fontsize=19, fontweight="bold", color="#20343d")
    ax.text(0.03, 0.905, f"当前目的性跨来源样本：{len(relations)} 条规范化关系观察＝上层行政机制 {len(admin)} 条＋下层服务／慈善／非资金边界 {len(lower)} 条；非官方表全量。", fontsize=10.5, color="#5b6d76")

    card(ax, 0.03, 0.64, 0.18, 0.18, "公共部门", "冲绳县／冲绳市\n外务省／JICA", "#dbeaf0")
    card(ax, 0.28, 0.60, 0.28, 0.26, "行政机制", f"C1 委託：{c1} 条\nC2 提案型公募委託：{c2} 条\nC4 補助：{c4} 条\n其他委托／指定角色：{other_admin} 条", "#e7f0dc")
    card(ax, 0.63, 0.60, 0.33, 0.26, "可观察公共功能", "多文化共生／国际交流设施运营\n和平教育／基地议题公共信息\n国际协力与移民史教育\nNGO 咨询与 diaspora network", "#f3ead7")
    for x1, x2 in [(0.21, 0.28), (0.56, 0.63)]:
        ax.add_patch(FancyArrowPatch((x1, 0.73), (x2, 0.73), arrowstyle="-|>", mutation_scale=14, color="#55717d", linewidth=1.8))

    card(ax, 0.03, 0.27, 0.18, 0.20, "服务／慈善／边界 actor", "USO／AWWA／军属配偶俱乐部\n企业 sponsor／NOFO 项目\nONC–JICA 活动协作", "#eadff0")
    card(ax, 0.28, 0.23, 0.28, 0.28, "服务、支持与非资金边界", f"赞助 {lower_counts['sponsorship']}；直接捐赠 {lower_counts['donation']}；慈善 grant {lower_counts['grant']}\n成员 {lower_counts['network_membership']}；实物捐赠 {lower_counts['in_kind_donation']}；共同实物贡献 {lower_counts['joint_in_kind_contribution']}\n服务存在 {lower_counts['service_presence']}；aggregate {lower_counts['aggregate_history']}\nNOFO {lower_counts['grant_opportunity']}；活动协作 {lower_counts['event_collaboration']}", "#f0e7d5")
    card(ax, 0.63, 0.23, 0.33, 0.28, "可观察服务对象／功能", "美军人员与军属家庭服务\n冲绳福利机构及军属社区 recipient\n伞状成员协调、慈善与实物支持\n机会公告与非资金活动协作", "#dfece8")
    for x1, x2 in [(0.21, 0.28), (0.56, 0.63)]:
        ax.add_patch(FancyArrowPatch((x1, 0.37), (x2, 0.37), arrowstyle="-|>", mutation_scale=14, color="#6d6272", linewidth=1.8))

    ax.plot([0.03, 0.96], [0.555, 0.555], color="#a5b1b6", linewidth=1.2, linestyle="--")
    ax.text(0.03, 0.12, "解释边界", fontsize=11, fontweight="bold", color="#8b4f42")
    ax.text(0.13, 0.12, "委托 ≠ grant ≠ 运动资金；赞助层级／成员／服务存在不产生金额；服务对象不产生政治立场；共同出现不产生稳定联盟。", fontsize=10, color="#5d514d")
    fig.subplots_adjust(left=0.02, right=0.98, top=0.98, bottom=0.04)
    fig.savefig(OUT / "fig_r10_mechanism_ecology.png", dpi=220)
    plt.close(fig)


def save_amount_boundary_figure(relations: list[dict[str, str]], amounts: list[dict[str, object]]) -> None:
    contracts = [r for r in amounts if r["amount_basis"] == "actual_contract_amount"]
    named_flows = [r for r in amounts if r["amount_basis"] in {"municipal_named_recipient_commission_flow", "documented_donation", "reported_in_kind_item_value"}]
    project_costs = [r for r in amounts if "project_cost" in str(r["amount_basis"])]
    aggregates = [r for r in amounts if "aggregate" in str(r["amount_basis"])]
    unresolved = [r for r in amounts if r["actor_payment_status"] == "recipient_scope_unresolved"]
    non_amount = [r for r in relations if r["financial_semantics"] in {"sponsor_tier_no_amount", "membership_no_funding", "designation_no_amount", "opportunity_only_no_award", "named_grant_no_amount"}]

    fig, ax = plt.subplots(figsize=(15.5, 9.5))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.text(0.04, 0.95, "R10 资金证据边界：能说到哪一步", fontsize=19, fontweight="bold", color="#20343d")
    ax.text(0.04, 0.91, f"当前目的性样本内 {len(amounts)} 条金额观察；币种保留 JPY／USD，不跨币种求和，不把项目成本画成付款线宽。", fontsize=10.5, color="#5b6d76")

    rows = [
        (0.75, "A  实际合同／点名资金流", f"实际合同 {len(contracts)} 条；点名委托流／捐赠／实物价值 {len(named_flows)} 条", "可写：合同额、点名资金流或原币种捐赠。\n仍须说明机制与范围；不自动成为“运动资金”。", "#dceee3"),
        (0.57, "B  项目成本", f"{len(project_costs)} 条：行政表 whole-project cost 或组织侧 project cost", "只写会计／项目背景。不得改写为合同、award、现金到账或对 actor 的付款。", "#f5e7c8"),
        (0.39, "C  Aggregate／范围未拆", f"aggregate {len(aggregates)} 条；recipient scope 未解 {len(unresolved)} 条", "不能拆到具体 recipient、年度、JV 成员或贡献者份额；不能相减推断利润／缺口。", "#f1dcd4"),
        (0.21, "D  Sponsor tier／成员／服务／指定", f"{len(non_amount)} 条非金额关系", "层级、成员、服务点、指定角色只证明关系或功能，不生成金额。", "#e5e2f1"),
        (0.03, "E  NOFO／机会公告", "1 条机会关系；0 条公开 award／recipient", "只能写机会存在且已截止；不得写成已拨款或 recipient 关系。", "#e4e9ed"),
    ]
    for y, title, metric, rule, color in rows:
        card(ax, 0.04, y, 0.24, 0.13, title, metric, color)
        card(ax, 0.34, y, 0.62, 0.13, "表达规则", rule, "#fafafa")
        ax.add_patch(FancyArrowPatch((0.285, y + 0.065), (0.335, y + 0.065), arrowstyle="-|>", mutation_scale=13, color="#6b7b82", linewidth=1.4))
    fig.subplots_adjust(left=0.02, right=0.98, top=0.98, bottom=0.03)
    fig.savefig(OUT / "fig_r10_amount_evidence_boundary.png", dpi=220)
    plt.close(fig)


def write_merge_proposal(relations: list[dict[str, str]]) -> None:
    fields = ["relation_observation_id", "source_record_ids", "merge_disposition", "proposal_scope", "human_gate"]
    rows = []
    for row in relations:
        disposition = row["merge_disposition"]
        if disposition.startswith("already_in_main"):
            scope = "no new edge; preserve as formal R10 crosswalk"
        elif disposition.startswith("update_existing"):
            scope = "evidence/time/amount observation update only; no duplicate edge"
        elif disposition.startswith("do_not_merge"):
            scope = "retain opportunity-only relation; never merge as award/recipient"
        elif "module_only" in disposition:
            scope = "module-only until actor/source/award crosswalk is resolved"
        else:
            scope = "candidate new relation after source archive and human review"
        rows.append({
            "relation_observation_id": row["relation_observation_id"],
            "source_record_ids": row["source_record_ids"],
            "merge_disposition": disposition,
            "proposal_scope": scope,
            "human_gate": "required_before_main_table_mutation",
        })
    write_csv(OUT / "main_merge_proposal_v1.csv", rows, fields)


HR018_FIELDS = [
    "review_item_id", "relation_observation_id", "source_record_ids", "fiscal_year",
    "source_entity", "target_entity", "program_name", "current_relation_type",
    "current_mechanism", "current_financial_semantics", "linked_amount_ids",
    "linked_function_ids", "linked_source_refs", "linked_source_locators",
    "current_evidence_level", "current_review_status", "precise_review_question",
    "accept", "revise", "reject", "revision_instructions", "human_notes",
    "affected_main_table_proposal", "affected_figures", "affected_brief_sections",
]


HR018_QUESTIONS = {
    "R10R001": "请核对 S100 p.103 是否足以确认 ONC 是该事业及报告受托者、FY2019 期间与公共机构→actor 方向；若接受，仍须确认不附加金额。",
    "R10R002": "请核对 R10S05 pp.9-10 的 FY2019 KIP 资金流、ONC 名称与 17,157,000 日元是否为点名委托费，并确认来源已归档后才提议并表。",
    "R10R003": "请核对 R10S06 pp.9-10 的 FY2020 KIP 资金流、ONC 名称与 16,970,000 日元是否为点名委托费，并确认来源已归档后才提议并表。",
    "R10R004": "请逐项核对 FY2024 KIP 的 18.858m 总事业费、16.662m 交付对象委托流、2.196m 交付对象外 3 月运营费与 ONC 16.040m 事业费；确认仅保留一条关系且不把后两类成本写成付款。",
    "R10R005": "请核对 S002 row 431 的 C1、2024-07-04 起始日、5.140m 项目费，以及 S099 的 6月–3月/5,530,234 成本和 R10S08 事务局角色；决定期间写法并确认两金额都不是合同额。",
    "R10R006": "请核对 S099 是否足以确认 FY2024 NGO相談員为外务省委托，并确认 2,894,630 日元只作为 ONC 组织侧项目成本，不写成 MOFA 支付。",
    "R10R007": "请核对 S101 FY2026 名单是否只确认 ONC 指定角色延续、期间与服务定义；不得从名单推定金额或 recipient 网络。",
    "R10R008": "请核对 A066 actor crosswalk、S002 C2、12.843m 项目费与 R10S11 12,842,500 日元实际合同额；确认不是 grant、机会限额或运动资金。",
    "R10R009": "请核对 A088 crosswalk、S002 C2、25.547m 项目费与 R10S11 26,439,000 日元合同额，并确认此项目独立于另一份 A088 合同。",
    "R10R010": "请核对 A088 crosswalk、S002 C2、6.496m 项目费与 R10S11 8,479,000 日元合同额，并确认此项目独立于另一份 A088 合同。",
    "R10R011": "请核对国际协力人才培养 JV 的法定/项目名称、两名成员、C2 与 21.799m 项目费；决定是否建复合 actor，且不得把总额拆给成员。",
    "R10R012": "请核对世界若者ウチナーンチュ连合会的组织身份/crosswalk、S002 C1、项目期间与 10.329m 项目费；service 只能保留为功能。",
    "R10R013": "请核对 Team OKIYUA 的复合主体与成员、S002 C1、项目期间及 39.739m 项目费；不得将总额分配给任一成员。",
    "R10R014": "请核对青年海外协力协会冲绳事务所的 actor identity、S002 C2、期间及 7.171m 项目费；教育服务只留在功能层。",
    "R10R015": "请核对 Uchina Junior Study JV 名称/成员、S002 C2、期间及 15.442m 项目费；决定复合 actor 处理且不得拆额。",
    "R10R016": "请核对冲绳县国际交流·人才育成财团 actor identity、S002 C4 与补助叙述；确认 17.932m 只是项目费，若要 award amount 必须另取补助决定。",
    "R10R018": "请核对 S097 所列服务对象与 8 个 USO Okinawa 服务点是否完整、是否应合并为一条服务关系；确认不由对象/据点推定政治立场或资金。",
    "R10R020": "请核对 S097 截图/归档是否明确 MBC 为 Platinum sponsor、页面时点与主体名称；确认 sponsor tier 不生成金额。",
    "R10R021": "请核对 S097 截图/归档是否明确 Matson 为 Mission Partner、页面时点与主体名称；确认 sponsor tier 不生成金额。",
    "R10R028": "请核对 Army Community Group of Okinawa 的独立身份、现名与 AWWA 成员证据；若身份不足则 revise/reject，且成员关系不得改写为资助。",
    "R10R029": "请核对 S075 的 102,000 美元是否明确为 scholarships+AWWA 合并口径、报告年度与措辞；确认不能把全额分配给 AWWA，并决定是否继续要求年报。",
    "R10R030": "请核对 S078 的约 8 亿日元/40 年累计口径、组织名称与 recipient 范围；确认不得拆到具体年度/recipient，并决定 Form 990/年报补查要求。",
    "R10R031": "请核对 Yomitan Quegoen 的正式名称/recipient 身份、2015-12-02 事件与 200 万日元车辆价值；确认是实物价值而非现金，并决定 E3 单源是否接受。",
    "R10R032": "请核对 Uruma City Social Welfare Meeting 的正式名称、2012 点名 recipient 与无障碍车辆事实；来源未给金额，不得补写金额。",
    "R10R033": "请核对 Boy Scouts Far East Council 的正式 recipient 名称、2012 皮划艇事实及美军社区属性；不得归为冲绳本地福利 recipient。",
    "R10R034": "请核对 S102 所列四个贡献团体、平敷屋课后托育 recipient 的法定名称及三台冷风机事实；只能确认 NOSCO 参与，不得归属全部物品/价值。",
}


def build_hr018_review_rows(
    relations: list[dict[str, str]],
    amounts: list[dict[str, object]],
    functions: list[dict[str, str]],
) -> list[dict[str, str]]:
    amount_by_relation: dict[str, list[dict[str, object]]] = {}
    function_by_relation: dict[str, list[dict[str, str]]] = {}
    for row in amounts:
        amount_by_relation.setdefault(str(row["relation_observation_id"]), []).append(row)
    for row in functions:
        function_by_relation.setdefault(row["relation_observation_id"], []).append(row)

    pending = [
        row for row in relations
        if row["review_status"] not in {"human_checked", "human_revised"}
    ]
    pending.sort(key=lambda row: row["relation_observation_id"])
    assert len(pending) == 26
    assert {row["relation_observation_id"] for row in pending} == set(HR018_QUESTIONS)

    output: list[dict[str, str]] = []
    for index, relation in enumerate(pending, start=1):
        rid = relation["relation_observation_id"]
        linked_amounts = amount_by_relation.get(rid, [])
        linked_functions = function_by_relation.get(rid, [])
        refs: list[str] = []
        locator_parts = [f"REL={relation['source_locators']}"]
        for ref in relation["source_refs"].split(";"):
            if ref and ref not in refs:
                refs.append(ref)
        for row in linked_amounts:
            for ref in str(row["source_refs"]).split(";"):
                if ref and ref not in refs:
                    refs.append(ref)
            locator_parts.append(f"{row['amount_observation_id']}={row['source_locators']}")
        for row in linked_functions:
            for ref in row["source_refs"].split(";"):
                if ref and ref not in refs:
                    refs.append(ref)
            locator_parts.append(f"{row['function_observation_id']}={row['source_locators']}")
        affected_brief = "§2;§3;§4;§6" if linked_amounts else "§2;§4;§6"
        output.append(dict(zip(HR018_FIELDS, [
            f"HR-018-{index:02d}", rid, relation["source_record_ids"],
            relation["fiscal_year"], relation["source_entity_name"],
            relation["target_entity_name"], relation["program_name"],
            relation["relation_type"],
            ";".join(filter(None, [relation["official_mechanism_code"], relation["mechanism_label"]])),
            relation["financial_semantics"],
            ";".join(str(row["amount_observation_id"]) for row in linked_amounts),
            ";".join(row["function_observation_id"] for row in linked_functions),
            ";".join(refs), " | ".join(locator_parts), relation["evidence_level"],
            relation["review_status"], HR018_QUESTIONS[rid], "", "", "", "", "",
            relation["merge_disposition"],
            "fig_r10_mechanism_ecology.png;fig_r10_amount_evidence_boundary.png",
            affected_brief,
        ])))
    return output


def build_hr018_source_prerequisites(review_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    fields = [
        "source_prerequisite_id", "source_ref", "title", "url", "required_locator",
        "current_status", "affected_review_item_ids", "archive_verified",
        "main_source_id", "human_notes",
    ]
    rows: list[dict[str, str]] = []
    for index, source in enumerate(MODULE_SOURCES, start=1):
        affected = [
            row["review_item_id"] for row in review_rows
            if source["source_ref"] in row["linked_source_refs"].split(";")
        ]
        rows.append(dict(zip(fields, [
            f"HR-018-S{index:02d}", source["source_ref"], source["title"], source["url"],
            source["locator_coverage"], "pending_archive_and_source_log_prerequisite",
            ";".join(affected), "", "", "",
        ])))
    assert len(rows) == 8
    return rows


def write_hr018_package(
    relations: list[dict[str, str]],
    amounts: list[dict[str, object]],
    functions: list[dict[str, str]],
) -> None:
    review_rows = build_hr018_review_rows(relations, amounts, functions)
    prerequisite_rows = build_hr018_source_prerequisites(review_rows)
    prerequisite_fields = [
        "source_prerequisite_id", "source_ref", "title", "url", "required_locator",
        "current_status", "affected_review_item_ids", "archive_verified",
        "main_source_id", "human_notes",
    ]
    review_path = OUT / "HR018_relation_review_v0.csv"
    prerequisite_path = OUT / "HR018_source_prerequisites_v0.csv"
    preserve_human_review_rows(
        review_path, review_rows, "relation_observation_id", "review_item_id",
        ("accept", "revise", "reject", "revision_instructions", "human_notes"),
    )
    preserve_human_review_rows(
        prerequisite_path, prerequisite_rows, "source_ref", "source_prerequisite_id",
        ("archive_verified", "main_source_id", "human_notes"),
    )
    write_csv(review_path, review_rows, HR018_FIELDS)
    write_csv(prerequisite_path, prerequisite_rows, prerequisite_fields)

    guide = f"""# HR-018 R10 关系级人工复核指南

日期：2026-07-13

## 复核范围

本包只将尚非 `human_checked`／`human_revised` 的 **{len(review_rows)} 条 relation observation** 作为主复核项。关联的金额和功能通过 `linked_amount_ids`、`linked_function_ids` 回指，不拆成额外人工任务。已有 9 条 human_checked／human_revised 关系不重复进入本包。

## 填写规则

1. 每个主条目只在 `accept`、`revise`、`reject` 三栏之一填 `X`。
2. 选择 `revise` 时，在 `revision_instructions` 写明应修改的字段与安全措辞；`human_notes` 可记录来源页码、actor crosswalk 或方向判断。
3. `accept` 表示接受该条关系的机制、范围、来源与解释边界，不表示把所有关联 project cost 接受为付款。
4. `reject` 后仍保留原始来源追溯，不从本包直接删除中央数据。
5. 本包不自动修改 actor registry、source log、funding 主表或中央任务簿；完成签审后另行执行 merge proposal。

## 来源前置条件

`HR018_source_prerequisites_v0.csv` 单列 R10S05–R10S12 共 {len(prerequisite_rows)} 项归档／source-log 前置条件。`archive_verified`、`main_source_id` 和 `human_notes` 当前留空，不能把 `pending_archive_and_source_log_prerequisite` 当成人审通过。

## 影响范围

每条主复核项列出会影响的 main-table proposal、两张 R10 图与 brief 章节。任何 project cost、aggregate、sponsor tier、membership、service presence 或 NOFO 的 revise，都应同步检查资金证据边界图；任何 relation_type 的 revise，都应同步检查当前目的性样本内 16+19=35 的加总计数。
"""
    (OUT / "HR018_review_guide_v0.md").write_text(guide, encoding="utf-8")


def write_brief(relations: list[dict[str, str]], amounts: list[dict[str, object]], functions: list[dict[str, str]]) -> None:
    rel_types = Counter(r["relation_type"] for r in relations)
    amount_bases = Counter(str(r["amount_basis"]) for r in amounts)
    confirmed_contracts = [r for r in amounts if r["amount_basis"] == "actual_contract_amount"]
    human = sum(r["review_status"] in {"human_checked", "human_revised"} for r in relations)
    pending = len(relations) - human
    admin = [r for r in relations if r["relation_scope"].startswith("public_to")]
    lower = [r for r in relations if r not in admin]
    brief = f"""# R10 解释 brief v1：行政协作、资金证据与服务生态

日期：2026-07-13
口径：本包描述**行政委托／补助、慈善支持、成员与服务功能**，不是“运动资金网”。共同出现在行政表、共同活动、赞助或服务对象均不自动构成政治联盟。

## 1. 本模块回答什么

R10 回答的是：冲绳的民间／非营利组织如何通过公开委托、补助、指定角色、慈善、成员网络和服务据点进入公共与基地社区生态；同时说明公开材料能够确认的金额语义上限。它不回答“谁资助反基地运动”，也不把服务美军人员与军属家庭的组织默认为亲基地或反基地 actor。

当前**目的性、跨来源 R10 样本**内共有 **{len(relations)} 条关系观察、{len(amounts)} 条金额观察、{len(functions)} 条功能观察**。机制生态图在样本内分为上层行政机制 **{len(admin)} 条**与下层服务／慈善／非资金边界 **{len(lower)} 条**，内部加总为 {len(admin)}+{len(lower)}={len(relations)}。该计数不代表任何官方表、部门、年度或机制的全量抽取。

样本内关系类型计数为：commission {rel_types['commission']}、designated_role {rel_types['designated_role']}、grant {rel_types['grant']}、sponsorship {rel_types['sponsorship']}、donation {rel_types['donation']}、network_membership {rel_types['network_membership']}、in_kind_donation {rel_types['in_kind_donation']}、joint_in_kind_contribution {rel_types['joint_in_kind_contribution']}、service_presence {rel_types['service_presence']}、aggregate_history {rel_types['aggregate_history']}、grant_opportunity {rel_types['grant_opportunity']}、event_collaboration {rel_types['event_collaboration']}；以上对当前 {len(relations)} 条内部加总完备，没有把活动协作或慈善 grant 隐入其他类型。

## 2. 解释性候选与已审边界

1. **ONC 的组织功能位于国际合作／多文化共生层；具体行政关系仍待 HR-018。** 公开材料为 JICA 教师海外研修、冲绳市 KIP 管理运营、冲绳县多文化共生会议运营支援与外务省 NGO 相談員形成官方来源候选。KIP 的多语咨询、语言课程与交流活动可解释其公共功能；但这些敏感行政关系须经 HR-018 接受／修订后才能作为事实关系发布，也没有证据把它们连到反基地运动网络。
2. **官方机制码把“服务内容”和“资金机制”分开。** 本包采用 C1=委託、C2=提案型公募による委託、C4=補助，并修正原候选五个错分：R10A010/A011/A012/A014/A016 全部是 commission，服务／教育留在功能表。
3. **官方记录形成 A066 与 A088 三份采购合同候选。** 记录金额分别为 {confirmed_contracts[0]['amount_value']:,}、{confirmed_contracts[1]['amount_value']:,}、{confirmed_contracts[2]['amount_value']:,} 日元；HR-018 接受前不得作为已冻结受托关系发布。即使接受，它们也只证明具体项目／年度的采购关系，不证明 grant、无条件行政支持、稳定政治联盟或“运动资金”。
4. **USO／AWWA／OESC／NOSCO 构成服务与慈善观察层。** USO 的公开对象是美军人员及军属家庭，AWWA 是军属配偶俱乐部伞状网络；赞助、成员、直接捐赠、实物支持和服务设点使用不同边型。OESC→USO 的直接捐赠与 NOSCO 共同交付冷风机均只能按具体事件表述。
5. **NOFO、aggregate 和 sponsor tier 必须留在证据边界外侧。** Okinawa Youth Council 只有机会公告，没有公开 award／recipient；AWWA 40 年累计口径与 KOSC 102,000 美元混合口径不能拆给具体 recipient；USO sponsor tier 不产生金额。

## 3. 金额为什么不能放进一条“资金边”

- `actual_contract_amount` {amount_bases['actual_contract_amount']} 条：可以按合同写，但仅限具体项目、年度和相对方。
- `municipal_named_recipient_commission_flow` {amount_bases['municipal_named_recipient_commission_flow']} 条：2019/2020 KIP 是点名资金流；FY2024 的 16.662m 只是交付对象部分，必须同时保留 2.196m 交付对象外 3 月运营委托观察。
- project cost 共 {sum(v for k, v in amount_bases.items() if 'project_cost' in k)} 条：包括行政表项目费与组织侧事业费，只能用于会计／项目背景，不能写成付款。
- aggregate {sum(v for k, v in amount_bases.items() if 'aggregate' in k)} 条：不按 recipient、年度或成员拆分。
- JPY 与 USD 保持原币种，不做跨币种求和；实物价值不写成现金支付。

## 4. 可确认与待人审

当前 {human} 条关系沿用既有 human_checked／human_revised 决策，{pending} 条仍为 AI 整理或待第二来源／当地材料，不能由 AI 自行升级为 human_checked。

`HR018_relation_review_v0.csv` 将这 {pending} 条关系作为 {pending} 个主复核项；金额与功能仅以关联 ID 附着，不拆成额外数十条人工任务。`HR018_source_prerequisites_v0.csv` 另列 R10S05–R10S12 八项来源归档／source-log 前置条件，这些前置项尚未预作人审。

可作为来源支持充分的候选：C1/C2/C4 机制映射、JICA→ONC 受托角色、2019/2020 KIP 点名委托流、FY2024 KIP 关系本身、A066/A088 三份官方合同、USO 公开服务对象与八个服务点。

仍需人审／归档：

- 把 R10S05–R10S12 归档并纳入 source log，保持精确页码；
- 决定主表统一方向（公共机构→受托者），避免 F031–F033 的反向／项目节点重复；
- 核对 KIP 18.858m／16.662m／2.196m／ONC 16.040m 的会计范围；
- 取得 ONC 县多文化项目与 MOFA NGO 相談員的合同／支付记录；
- 核对 R10R011–R10R016 的 JV／财团 actor crosswalk；
- AWWA 完整 recipient 年表仍需 Form 990 Schedule I／年报，当地协作者任务由报告缺口明确触发。

## 5. 可视化怎么读

- `fig_r10_mechanism_ecology.png`：上半部是公共委托／补助，下半部是基地社区服务／慈善；两层并置用于比较组织生态，**不是把它们连成一个阵营**。
- `fig_r10_amount_evidence_boundary.png`：只有实际合同与点名资金流能进入强金额表达；project cost、aggregate、sponsor tier、membership、service presence 和 NOFO 使用非金额视觉语法。

## 6. 主表合并边界

`main_merge_proposal_v1.csv` 只是 proposal，不改 actor registry、source log 或现有 funding 主表。F031–F033 只做证据／时间／金额观察更新，不新增平行边；已有 F002/F006 等只做 R10 crosswalk；NOFO 永远不按 award／recipient 合并。
"""
    (OUT / "R10_explanatory_brief_v1.md").write_text(brief, encoding="utf-8")


def write_metrics(relations: list[dict[str, str]], amounts: list[dict[str, object]], functions: list[dict[str, str]]) -> None:
    fields = ["metric", "value", "definition"]
    admin = [r for r in relations if r["relation_scope"].startswith("public_to")]
    lower = [r for r in relations if r not in admin]
    relation_types = Counter(r["relation_type"] for r in relations)
    rows = [
        {"metric": "relation_observations", "value": len(relations), "definition": "unique normalized relations in the current purposive cross-source R10 sample"},
        {"metric": "mechanism_figure_admin_layer", "value": len(admin), "definition": "public_to* relations in the current sample's upper administrative layer"},
        {"metric": "mechanism_figure_lower_layer", "value": len(lower), "definition": "service/charity/non-funding-boundary relations in the current sample's lower layer"},
        {"metric": "amount_observations", "value": len(amounts), "definition": "selected monetary observations in the current sample; not additive by default"},
        {"metric": "function_observations", "value": len(functions), "definition": "selected service/role/site observations with no independent funding inference"},
        {"metric": "actual_contract_amounts", "value": sum(r["amount_basis"] == "actual_contract_amount" for r in amounts), "definition": "exact official named-counterparty contracts"},
        {"metric": "project_cost_observations", "value": sum("project_cost" in str(r["amount_basis"]) for r in amounts), "definition": "context only; not actor payment"},
        {"metric": "aggregate_amount_observations", "value": sum("aggregate" in str(r["amount_basis"]) for r in amounts), "definition": "not allocable to actor/year"},
        {"metric": "human_checked_or_revised_relations", "value": sum(r["review_status"] in {"human_checked", "human_revised"} for r in relations), "definition": "inherits existing human decisions only"},
    ]
    for relation_type in sorted(relation_types):
        rows.append({
            "metric": f"relation_type_{relation_type}",
            "value": relation_types[relation_type],
            "definition": "within-package relation_type count; sums to the current purposive relation sample only",
        })
    write_csv(OUT / "figure_metrics_v1.csv", rows, fields)


def validate_generated_markdown() -> None:
    for path in [OUT / "R10_explanatory_brief_v1.md", OUT / "HR018_review_guide_v0.md"]:
        lines = path.read_text(encoding="utf-8").splitlines()
        bad = [index for index, line in enumerate(lines, start=1) if line.rstrip() != line]
        assert not bad, f"Trailing whitespace in {path}: {bad}"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    relations = build_relations()
    amounts = build_amounts()
    functions = build_functions()
    sources = build_source_crosswalk(relations, amounts, functions)
    validate(relations, amounts, functions, sources)

    write_csv(REL_PATH, relations, REL_FIELDS)
    write_csv(AMT_PATH, amounts, AMT_FIELDS)
    write_csv(FUN_PATH, functions, FUN_FIELDS)
    write_csv(OUT / "source_crosswalk_v1.csv", sources, ["source_ref", "title", "url", "status", "locator_coverage", "merge_note"])
    write_csv(OUT / "mechanism_dictionary_v1.csv", build_mechanism_dictionary(), ["mechanism_code", "mechanism_label", "relation_semantics", "amount_rule", "visual_rule"])
    write_merge_proposal(relations)
    write_metrics(relations, amounts, functions)
    write_hr018_package(relations, amounts, functions)
    write_brief(relations, amounts, functions)
    validate_generated_markdown()
    configure_fonts()
    save_mechanism_figure(relations)
    save_amount_boundary_figure(relations, amounts)
    print(f"R10 built: {len(relations)} relations, {len(amounts)} amounts, {len(functions)} functions")


if __name__ == "__main__":
    main()
