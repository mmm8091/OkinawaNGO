"""Merge principal-confirmed HR-018 and HR-021 decisions.

This is a deterministic overlay, not a new research pass.  It keeps the three
R10 fact layers separate, preserves the HR-033 F025/R10R029 split, and admits
only the nine HR-021-approved relations to the shared R6/R11 fact layer.

The script intentionally does not mutate the actor registry, source log,
funding/support main table, frontend, or figures.
"""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def split_refs(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def join_refs(*values: str) -> str:
    result: list[str] = []
    for value in values:
        for part in split_refs(value):
            if part not in result:
                result.append(part)
    return ";".join(result)


def index_unique(rows: list[dict[str, str]], key: str) -> dict[str, dict[str, str]]:
    indexed: dict[str, dict[str, str]] = {}
    for row in rows:
        value = row[key]
        if not value or value in indexed:
            raise ValueError(f"non-unique {key}={value!r}")
        indexed[value] = row
    return indexed


def overlay_index(root: Path) -> dict[str, dict[str, dict[str, str]]]:
    rows = read_csv(
        root / "outputs/principal_review_merge_v1/principal_decision_overlay_v1.csv"
    )
    grouped: dict[str, dict[str, dict[str, str]]] = {}
    for row in rows:
        grouped.setdefault(row["task_family"], {})[row["object_id"]] = row
    expected = {
        "HR018_PREREQUISITE": 8,
        "HR018_RELATION": 26,
        "HR021": 8,
    }
    for family, count in expected.items():
        actual = len(grouped.get(family, {}))
        if actual != count:
            raise ValueError(f"{family}: expected {count} decisions, got {actual}")
    return grouped


def review_metadata(
    row: dict[str, str],
    overlay: dict[str, str],
    decision: str,
    review_status: str,
    scope: str,
) -> None:
    row["review_status"] = review_status
    row["human_decision"] = decision
    row["human_reviewer"] = overlay["human_reviewer"]
    row["review_date"] = overlay["review_date"]
    row["decision_source_report"] = overlay["source_report"]
    row["review_scope"] = scope


def apply_hr018(
    root: Path,
    overlays: dict[str, dict[str, dict[str, str]]],
) -> tuple[
    list[dict[str, str]],
    list[dict[str, str]],
    list[dict[str, str]],
    list[dict[str, str]],
]:
    r10 = root / "outputs/R10_administrative_collaboration_v0"
    data = root / "data/interim"
    queue_path = r10 / "HR018_relation_review_v0.csv"
    prereq_path = r10 / "HR018_source_prerequisites_v0.csv"
    relation_path = data / "21_admin_collaboration_relations_v0.csv"
    amount_path = data / "22_admin_amount_observations_v0.csv"
    function_path = data / "23_admin_function_observations_v0.csv"

    queue = read_csv(queue_path)
    prereqs = read_csv(prereq_path)
    relations = read_csv(relation_path)
    amounts = read_csv(amount_path)
    functions = read_csv(function_path)
    relation_by_id = index_unique(relations, "relation_observation_id")
    amount_by_id = index_unique(amounts, "amount_observation_id")
    function_by_id = index_unique(functions, "function_observation_id")

    for row in prereqs:
        overlay = overlays["HR018_PREREQUISITE"][row["source_prerequisite_id"]]
        row["current_status"] = overlay["decision"]
        row["archive_verified"] = "yes"
        row["decision"] = overlay["decision"]
        row["human_reviewer"] = overlay["human_reviewer"]
        row["review_date"] = overlay["review_date"]
        row["review_note"] = (
            f"{overlay['approved_formulation']} | 边界：{overlay['scope_boundary']}"
        )
        row["approved_formulation"] = overlay["approved_formulation"]
        row["scope_boundary"] = overlay["scope_boundary"]
        row["decision_source_report"] = overlay["source_report"]

    decision_to_status = {
        "accept": "human_checked",
        "revise": "human_revised",
    }
    for queue_row in queue:
        item_id = queue_row["review_item_id"]
        overlay = overlays["HR018_RELATION"][item_id]
        decision = overlay["decision"]
        queue_row["decision"] = decision
        queue_row["human_reviewer"] = overlay["human_reviewer"]
        queue_row["review_date"] = overlay["review_date"]
        queue_row["review_note"] = (
            f"{overlay['approved_formulation']} | 边界：{overlay['scope_boundary']}"
        )
        queue_row["approved_formulation"] = overlay["approved_formulation"]
        queue_row["scope_boundary"] = overlay["scope_boundary"]
        queue_row["decision_source_report"] = overlay["source_report"]

        relation_id = queue_row["relation_observation_id"]
        relation = relation_by_id[relation_id]

        # HR-018-21 was superseded at the fact-layer merge by HR-033.  The
        # queue remains deferred for itemization, while the bounded amountless
        # F025 dyad and separate R10R029 aggregate observation stay intact.
        if item_id == "HR-018-21":
            continue
        if item_id == "HR-018-22":
            relation["review_status"] = "needs_local_retrieval"
            for amount_id in split_refs(queue_row["linked_amount_ids"]):
                amount_by_id[amount_id]["review_status"] = "needs_local_retrieval"
            for function_id in split_refs(queue_row["linked_function_ids"]):
                function_by_id[function_id]["review_status"] = "needs_local_retrieval"
            continue

        status = decision_to_status[decision]
        scope = (
            f"{overlay['approved_formulation']}；边界：{overlay['scope_boundary']}"
        )
        review_metadata(relation, overlay, decision, status, scope)
        if overlay["scope_boundary"] != "同上":
            relation["interpretation_limit"] = overlay["scope_boundary"]

        for amount_id in split_refs(queue_row["linked_amount_ids"]):
            amount = amount_by_id[amount_id]
            review_metadata(amount, overlay, decision, status, scope)
            if overlay["scope_boundary"] != "同上":
                amount["interpretation_limit"] = overlay["scope_boundary"]

        for function_id in split_refs(queue_row["linked_function_ids"]):
            function = function_by_id[function_id]
            review_metadata(function, overlay, decision, status, scope)
            if overlay["scope_boundary"] != "同上":
                function["interpretation_limit"] = overlay["scope_boundary"]

    apply_hr018_revisions(relations, amounts, functions)
    amount_by_id = index_unique(amounts, "amount_observation_id")
    queue_by_id = index_unique(queue, "review_item_id")
    for item_id, amount_id in (
        ("HR-018-11", "R10AM027"),
        ("HR-018-13", "R10AM028"),
    ):
        row = queue_by_id[item_id]
        row["linked_amount_ids"] = join_refs(row["linked_amount_ids"], amount_id)
        row["linked_source_refs"] = join_refs(row["linked_source_refs"], "R10S13")
        locator = "R10S13 PDF No.91" if item_id.endswith("-11") else "R10S13 PDF No.90"
        row["linked_source_locators"] = (
            f"{row['linked_source_locators']} | {amount_id}={locator}"
        )

    write_csv(prereq_path, prereqs)
    write_csv(queue_path, queue)
    write_csv(relation_path, relations)
    write_csv(amount_path, amounts)
    write_csv(function_path, functions)
    return relations, amounts, functions, queue


def apply_hr018_revisions(
    relations: list[dict[str, str]],
    amounts: list[dict[str, str]],
    functions: list[dict[str, str]],
) -> None:
    relation = index_unique(relations, "relation_observation_id")
    amount = index_unique(amounts, "amount_observation_id")
    function = index_unique(functions, "function_observation_id")

    relation["R10R011"].update(
        {
            "financial_semantics": "confirmed_contract_plus_project_cost",
            "source_refs": join_refs(relation["R10R011"]["source_refs"], "R10S13"),
            "source_locators": (
                "S002 PDF p.59 row 432; R10S12 PDF p.2; "
                "R10S13 PDF No.91"
            ),
            "interpretation_limit": (
                "21.799m 是事业费；27.199m 是该 JV 的实际合同额；"
                "合同额不得拆给成员。"
            ),
        }
    )
    relation["R10R013"].update(
        {
            "financial_semantics": "confirmed_contract_plus_project_cost",
            "source_refs": join_refs(relation["R10R013"]["source_refs"], "R10S13"),
            "source_locators": (
                "S002 PDF p.60 row 434; R10S12 PDF p.2; "
                "R10S13 PDF No.90"
            ),
            "interpretation_limit": (
                "39.739m 是事业费；37,220,999 円是该复合主体的实际合同额；"
                "不得拆给成员。"
            ),
        }
    )
    relation["R10R020"].update(
        {
            "source_entity_name": "Mediatti Broadband Communications, Inc. (MBC Okinawa)",
            "mechanism_detail": (
                "USO Okinawa Platinum Sponsor；公开材料概括现金与实物支持，"
                "但没有金额或估值。"
            ),
            "financial_semantics": "sponsor_tier_and_support_types_no_amount",
            "relation_scope": "direct_okinawa_service_sponsorship",
            "interpretation_limit": (
                "Platinum 层级和支持类型不能换算金额；赞助不证明基地政策立场。"
            ),
        }
    )
    relation["R10R021"].update(
        {
            "target_entity_id": "P_R10_USO_INDO_PACIFIC",
            "target_entity_name": "USO Indo-Pacific",
            "target_entity_kind": "regional_service_network",
            "program_name": "Matson — USO Indo-Pacific Mission Partner",
            "mechanism_detail": (
                "USO Indo-Pacific Mission Partner；USO Okinawa 页面只构成"
                "本地展示 context。"
            ),
            "financial_semantics": "sponsor_tier_no_amount_or_local_allocation",
            "relation_scope": "regional_context_not_okinawa_direct",
            "interpretation_limit": (
                "不写成 Matson 对 USO Okinawa 的本地定向资助；无金额、"
                "无本地 allocation、无政治立场推断。"
            ),
        }
    )
    relation["R10R028"].update(
        {
            "fiscal_year": "2012;2015",
            "period_start": "2012",
            "period_end": "2015",
            "source_entity_id": "X017",
            "source_entity_name": "Army Community Group of Okinawa",
            "source_entity_kind": "historical_provisional_organization",
            "target_entity_id": "X004",
            "target_entity_name": "AWWA",
            "target_entity_kind": "registered_actor",
            "program_name": "ACGO 的 AWWA 历史成员关系",
            "mechanism_detail": (
                "2012 与 2015 两个时点可观察为成员；当前名单未列 ACGO；"
                "精确退出日未知。"
            ),
            "relation_scope": "historical_actor_to_umbrella",
            "source_refs": "S072;S094;S081",
            "source_locators": "2012/2015 membership mentions; ACGO-operated gift-shop identity",
            "interpretation_limit": (
                "历史 membership 不是资助；不写精确退出年份，也不因当前未列名"
                "推定组织解散。"
            ),
        }
    )
    relation["R10R031"].update(
        {
            "target_entity_name": "よみたん救護園",
            "target_entity_kind": "welfare_facility",
            "program_name": "无障碍车辆实物捐赠",
            "mechanism_detail": (
                "2015-12-02 向よみたん救護園捐赠无障碍车辆；"
                "运营法人=社会福祉法人沖縄県社会福祉事業団。"
            ),
            "interpretation_limit": (
                "2,000,000 円是实物价值，不是现金、付款或长期资助。"
            ),
        }
    )
    relation["R10R032"].update(
        {
            "target_entity_name": "社会福祉法人うるま市社会福祉協議会",
            "target_entity_kind": "welfare_operator_specific_facility_unresolved",
            "program_name": "无障碍车辆实物捐赠",
            "mechanism_detail": (
                "2012 年报道点名社会福祉法人；具体下属设施 unresolved。"
            ),
            "interpretation_limit": (
                "只确认 2012 年报道中的法人 recipient 与实物支持；"
                "不补金额或具体下属设施。"
            ),
        }
    )
    relation["R10R033"].update(
        {
            "fiscal_year": "",
            "period_start": "",
            "period_end": "",
            "target_entity_name": "Boy Scouts of America Far East Council",
            "target_entity_kind": "overseas_scouting_council",
            "program_name": "AWWA 帮助 Far East Council 获得皮划艇",
            "relation_type": "in_kind_acquisition_assistance",
            "mechanism_label": "实物取得协助",
            "mechanism_detail": (
                "历史名称=Boy Scouts of America Far East Council；"
                "现行 crosswalk=Far East Council, Scouting America；报道日 2012-04-23。"
            ),
            "financial_semantics": "no_amount_no_quantity_no_share_allocation",
            "interpretation_limit": (
                "事件日期、数量、金额与 AWWA 份额均未知；不得改写成"
                "“2012 年 AWWA 独自捐赠皮划艇”。"
            ),
        }
    )
    relation["R10R034"].update(
        {
            "period_start": "2025-08-15",
            "period_end": "2025-08-15",
            "target_entity_name": "平敷屋地区の放課後児童クラブ（正式名称未確認）",
            "target_entity_kind": "provisional_descriptive_recipient",
            "program_name": "三台工业冷风机共同交付（事件级）",
            "mechanism_detail": (
                "NOSCO 是四个点名贡献团体之一；きむたかこどもセンター"
                "学童クラブ仅为未批准 locator candidate。"
            ),
            "financial_semantics": "no_amount_no_contributor_share_allocation",
            "interpretation_limit": (
                "recipient 正式名称未确认；不把三台设备或全部价值归给 NOSCO，"
                "也不从共同交付推定联盟。"
            ),
        }
    )

    # Two new contract observations.  They use a module-local source candidate
    # because this bounded merge is not authorized to mutate the central source log.
    new_amounts = [
        {
            "amount_observation_id": "R10AM027",
            "relation_observation_id": "R10R011",
            "fiscal_year": "2024",
            "amount_value": "27199000",
            "currency": "JPY",
            "normalized_unit": "JPY",
            "reported_amount": "27199000",
            "reported_unit": "JPY",
            "amount_basis": "actual_contract_amount",
            "amount_scope": "named project-composite counterparty contract",
            "attributed_actor_id": "P_R10_IC_HRD_JV",
            "actor_payment_status": "confirmed_contract_not_member_allocation",
            "award_status": "not_applicable",
            "line_width_eligible": "yes_same_currency_scope",
            "source_refs": "R10S13",
            "source_locators": "PDF No.91",
            "evidence_level": "E4",
            "review_status": "human_revised",
            "interpretation_limit": (
                "实际合同额属于 JV 复合相手方；不得拆给 JOCA 冲绳事务所或 JTB 成员。"
            ),
            "human_decision": "revise",
            "human_reviewer": "项目负责人",
            "review_date": "2026-07-20",
            "decision_source_report": (
                "docs/human_review_return_HR018_relations_batch20_v1.md"
            ),
            "review_scope": (
                "HR-018-11：新增实际合同额；保留 21.799m 项目费为不同口径。"
            ),
        },
        {
            "amount_observation_id": "R10AM028",
            "relation_observation_id": "R10R013",
            "fiscal_year": "2024",
            "amount_value": "37220999",
            "currency": "JPY",
            "normalized_unit": "JPY",
            "reported_amount": "37220999",
            "reported_unit": "JPY",
            "amount_basis": "actual_contract_amount",
            "amount_scope": "named project-composite counterparty contract",
            "attributed_actor_id": "P_R10_TEAM_OKIYUA",
            "actor_payment_status": "confirmed_contract_not_member_allocation",
            "award_status": "not_applicable",
            "line_width_eligible": "yes_same_currency_scope",
            "source_refs": "R10S13",
            "source_locators": "PDF No.90",
            "evidence_level": "E4",
            "review_status": "human_revised",
            "interpretation_limit": (
                "实际合同额属于 Team OKIYUA 复合相手方；不得拆给成员。"
            ),
            "human_decision": "revise",
            "human_reviewer": "项目负责人",
            "review_date": "2026-07-20",
            "decision_source_report": (
                "docs/human_review_return_HR018_relations_batch20_v1.md"
            ),
            "review_scope": (
                "HR-018-13：新增实际合同额；保留 39.739m 项目费为不同口径。"
            ),
        },
    ]
    existing_amount_ids = {row["amount_observation_id"] for row in amounts}
    for row in new_amounts:
        if row["amount_observation_id"] not in existing_amount_ids:
            amounts.append(row)
        else:
            amount[row["amount_observation_id"]].update(row)

    function["R10FN028"].update(
        {
            "actor_name": "Mediatti Broadband Communications, Inc. (MBC Okinawa)",
            "mechanism_context": "direct USO Okinawa sponsor tier; no amount",
            "interpretation_limit": (
                "Platinum 层级与现金／实物支持概括不生成估值或政治立场。"
            ),
        }
    )
    function["R10FN029"].update(
        {
            "function_description": "以 Mission Partner 身份支持 USO Indo-Pacific",
            "beneficiary_or_audience": "USO Indo-Pacific 服务对象",
            "place_or_facility": "USO Indo-Pacific；USO Okinawa 页面为本地展示 context",
            "mechanism_context": "regional sponsor; no local allocation",
            "interpretation_limit": (
                "不写成对 USO Okinawa 的本地定向赞助；无金额或政治立场推断。"
            ),
        }
    )
    function["R10FN036"].update(
        {
            "actor_id": "X017",
            "actor_name": "Army Community Group of Okinawa",
            "function_type": "historical_umbrella_membership",
            "function_description": "2012、2015 两个时点被列为 AWWA 成员",
            "beneficiary_or_audience": "AWWA 军属配偶组织网络",
            "place_or_facility": "Okinawa bases（历史）",
            "mechanism_context": "historical membership; no funding inference",
            "interpretation_limit": (
                "当前未列名不等于精确退出或组织解散；membership 不是资助。"
            ),
        }
    )
    function["R10FN039"].update(
        {
            "function_description": "向よみたん救護園捐赠无障碍车辆",
            "beneficiary_or_audience": "よみたん救護園使用者",
            "place_or_facility": "読谷村・よみたん救護園",
            "interpretation_limit": "2m 円仅为实物价值，不是现金或长期资助。",
        }
    )
    function["R10FN040"].update(
        {
            "function_description": "向社会福祉法人うるま市社会福祉協議会提供无障碍车辆",
            "beneficiary_or_audience": "法人服务对象；具体下属设施 unresolved",
            "place_or_facility": "うるま市",
            "interpretation_limit": "2012 年报道可确认法人 recipient；无金额、具体设施未决。",
        }
    )
    function["R10FN041"].update(
        {
            "fiscal_year": "",
            "function_type": "military_community_youth_acquisition_assistance",
            "function_description": "帮助 Far East Council 获得皮划艇",
            "beneficiary_or_audience": "Far East Council 童军（含 Okinawa 服务范围）",
            "place_or_facility": "亚太／Okinawa 服务范围；事件地点未明",
            "mechanism_context": "in-kind acquisition assistance; date/quantity/amount unknown",
            "interpretation_limit": (
                "2012 是报道时点；不能写成 AWWA 在 2012 年独自捐赠全部皮划艇。"
            ),
        }
    )
    function["R10FN042"].update(
        {
            "function_description": (
                "作为四个点名贡献团体之一参与 2025-08-15 三台工业冷风机共同交付"
            ),
            "beneficiary_or_audience": "平敷屋地区课后托育儿童与工作人员",
            "place_or_facility": "平敷屋地区／White Beach 附近；正式 recipient 未确认",
            "mechanism_context": "one_of_four_named_contributors; no share allocation",
            "interpretation_limit": (
                "不把三台设备、全部价值或きむたか locator 归给 NOSCO。"
            ),
        }
    )

    # Explicitly preserve the HR-033 split: the dyadic F025 has no amount,
    # while R10R029/R10AM024 is an off-graph mixed-recipient aggregate.
    relation["R10R029"].update(
        {
            "review_status": "human_revised",
            "merge_disposition": "hr033_accepted_aggregate_observation",
            "financial_semantics": "aggregate_mixed_recipient_no_allocation",
            "interpretation_limit": (
                "The aggregate cannot be allocated to AWWA, any scholarship recipient, "
                "or any single actor; it does not enter the organization relation graph."
            ),
        }
    )
    amount["R10AM024"].update(
        {
            "review_status": "human_revised",
            "amount_value": "102000",
            "actor_payment_status": "not_allocable_to_named_actor",
            "interpretation_limit": (
                "合计 102,000 美元不能分配给 AWWA、任一 scholarship recipient "
                "或任何单一 actor；明确财年与分项金额仍缺失。"
            ),
        }
    )
    function["R10FN037"].update(
        {
            "review_status": "human_revised",
            "interpretation_limit": (
                "这是 scholarships 与 AWWA 的混合 recipient 汇总披露，"
                "不是 AWWA 或任一 recipient 获得 102,000 美元的记录，"
                "也不上组织关系图。"
            ),
        }
    )


def update_r10_package(
    root: Path,
    relations: list[dict[str, str]],
    amounts: list[dict[str, str]],
    functions: list[dict[str, str]],
) -> None:
    out = root / "outputs/R10_administrative_collaboration_v0"
    relation_by_id = index_unique(relations, "relation_observation_id")

    candidates_path = out / "source_candidates_v0.csv"
    candidates = read_csv(candidates_path)
    candidates = [row for row in candidates if row["source_candidate_id"] != "R10S13"]
    candidates.append(
        {
            "source_candidate_id": "R10S13",
            "title": "令和6年度 文化観光スポーツ部 随意契約実績",
            "year": "2024",
            "owner": "Okinawa Prefecture",
            "source_type": "official_contract_record",
            "url": (
                "https://www.pref.okinawa.lg.jp/_res/projects/default_project/"
                "_page_/001/011/879/r6_1zuiikei2.pdf"
            ),
            "used_for": "R10R011 No.91; R10R013 No.90 actual contract amounts",
            "evidence_level": "E4",
            "archive_or_access_status": "web_verified_pending_main_source_log_and_archive",
            "review_status": "human_revised_fact_scope_only",
            "notes": (
                "Module-local source candidate created by the bounded HR-018 merge; "
                "central source-log mutation remains out of scope."
            ),
        }
    )
    write_csv(candidates_path, candidates)

    crosswalk_path = out / "source_crosswalk_v1.csv"
    crosswalk = read_csv(crosswalk_path)
    crosswalk = [row for row in crosswalk if row["source_ref"] != "R10S13"]
    crosswalk.append(
        {
            "source_ref": "R10S13",
            "title": "冲绳县 FY2024 文化观光体育部随意合同实绩",
            "url": (
                "https://www.pref.okinawa.lg.jp/_res/projects/default_project/"
                "_page_/001/011/879/r6_1zuiikei2.pdf"
            ),
            "status": "module_candidate_not_in_main_log",
            "locator_coverage": "PDF No.91 R10R011; No.90 R10R013",
            "merge_note": "add/archive in central source workflow; do not replace with bare URL",
        }
    )
    write_csv(crosswalk_path, crosswalk)

    annual_path = out / "annual_relations_v0.csv"
    annual = read_csv(annual_path)
    annual_to_relation: dict[str, dict[str, str]] = {}
    for relation in relations:
        for source_record_id in split_refs(relation["source_record_ids"]):
            if source_record_id.startswith("R10A"):
                annual_to_relation[source_record_id] = relation
    for row in annual:
        normalized = annual_to_relation[row["relation_id"]]
        row["review_status"] = normalized["review_status"]
        row["human_decision"] = normalized.get("human_decision", "")
        row["human_reviewer"] = normalized.get("human_reviewer", "")
        row["review_date"] = normalized.get("review_date", "")
        row["decision_source_report"] = normalized.get("decision_source_report", "")
    annual_corrections = {
        "R10A010": ("commission", "A066", "R10S11"),
        "R10A011": ("commission", "A088", "R10S11"),
        "R10A012": ("commission", "A088", "R10S11"),
        "R10A013": ("commission", "", "R10S13"),
        "R10A014": ("commission", "", ""),
        "R10A015": ("commission", "", "R10S13"),
        "R10A016": ("commission", "", ""),
    }
    for row in annual:
        if row["relation_id"] not in annual_corrections:
            continue
        relation_type, actor_id, source_ref = annual_corrections[row["relation_id"]]
        row["relation_type"] = relation_type
        if actor_id:
            row["partner_actor_id"] = actor_id
        if source_ref:
            row["source_refs"] = join_refs(row["source_refs"], source_ref)
        if row["relation_id"] in {"R10A010", "R10A011", "R10A012", "R10A013", "R10A015"}:
            row["financial_status"] = "project_cost_with_separate_confirmed_contract"
            row["interpretation_limit"] = (
                "Flat annual row retains the project-cost observation; exact contract "
                "amount is stored separately in data/interim/22 and must not be summed."
            )
    write_csv(annual_path, annual)

    visual_path = out / "visualization_edges_v0.csv"
    visual = read_csv(visual_path)
    visual_map = {
        "R10V001": "R10R001",
        "R10V002": "R10R002",
        "R10V003": "R10R003",
        "R10V004": "R10R004",
        "R10V005": "R10R005",
        "R10V006": "R10R006",
        "R10V007": "R10R007",
        "R10V008": "R10R008",
        "R10V009": "R10R009",
        "R10V010": "R10R010",
        "R10V011": "R10R011",
        "R10V012": "R10R012",
        "R10V013": "R10R013",
        "R10V014": "R10R014",
        "R10V015": "R10R015",
        "R10V016": "R10R016",
        "R10V017": "R10R005",
    }
    for row in visual:
        normalized = relation_by_id[visual_map[row["edge_id"]]]
        row["review_status"] = normalized["review_status"]
        row["human_decision"] = normalized.get("human_decision", "")
        row["decision_source_report"] = normalized.get("decision_source_report", "")
    visual_updates = {
        "R10V008": ("12842500", "R10S11", "actual_contract_amount"),
        "R10V009": ("26439000", "R10S11", "actual_contract_amount"),
        "R10V010": ("8479000", "R10S11", "actual_contract_amount"),
        "R10V011": ("27199000", "R10S13", "actual_contract_amount"),
        "R10V013": ("37220999", "R10S13", "actual_contract_amount"),
    }
    for row in visual:
        if row["edge_id"] in {"R10V008", "R10V009", "R10V010", "R10V012", "R10V014"}:
            row["mechanism"] = "commission"
            row["visual_group"] = "commission"
        if row["edge_id"] in visual_updates:
            value, source_ref, visual_status = visual_updates[row["edge_id"]]
            row["amount_jpy"] = value
            row["source_refs"] = join_refs(row["source_refs"], source_ref)
            row["amount_visual_status"] = visual_status
            row["tooltip_limit"] = (
                "Exact contract amount for the named project counterparty; "
                "not a grant, payment-to-members, or movement funding."
            )
    write_csv(visual_path, visual)

    mechanism_path = out / "mechanism_matrix_v0.csv"
    mechanisms = read_csv(mechanism_path)
    counts = {
        "commission": "16",
        "designated_role": "1",
        "grant": "1",
        "service": "1",
        "non_funding_relation": "1",
        "parallel_amount_observation": "2",
        "administrative_collaboration": "0",
    }
    for row in mechanisms:
        row["rows_in_annual_table"] = counts[row["mechanism"]]
    write_csv(mechanism_path, mechanisms)

    proposal_path = out / "main_merge_proposal_v1.csv"
    proposals = read_csv(proposal_path)
    proposal_by_id = index_unique(proposals, "relation_observation_id")
    for relation_id, relation in relation_by_id.items():
        proposal = proposal_by_id[relation_id]
        proposal["merge_disposition"] = relation["merge_disposition"]
        proposal["proposal_scope"] = relation["review_status"]
        proposal["human_gate"] = (
            "needs_local_retrieval"
            if relation["review_status"] == "needs_local_retrieval"
            else "completed_hr018_or_prior_human_review"
        )
    write_csv(proposal_path, proposals)

    metrics: list[dict[str, str]] = [
        {
            "metric": "relation_observations",
            "value": str(len(relations)),
            "definition": "unique normalized relations in the current purposive R10 sample",
        },
        {
            "metric": "mechanism_figure_admin_layer",
            "value": "16",
            "definition": "pre-HR018 figure-layer count; PNG not redrawn in this merge",
        },
        {
            "metric": "mechanism_figure_lower_layer",
            "value": "19",
            "definition": "pre-HR018 figure-layer count; PNG not redrawn in this merge",
        },
        {
            "metric": "amount_observations",
            "value": str(len(amounts)),
            "definition": "separate monetary observations; not additive by default",
        },
        {
            "metric": "function_observations",
            "value": str(len(functions)),
            "definition": "service/role/site observations with no independent funding inference",
        },
        {
            "metric": "actual_contract_amounts",
            "value": str(sum(row["amount_basis"] == "actual_contract_amount" for row in amounts)),
            "definition": "exact official named-counterparty contract observations",
        },
        {
            "metric": "project_cost_observations",
            "value": str(sum("project_cost" in row["amount_basis"] for row in amounts)),
            "definition": "context only; not actor payment",
        },
        {
            "metric": "aggregate_amount_observations",
            "value": str(sum(row["amount_basis"].startswith("aggregate_") for row in amounts)),
            "definition": "not allocable to actor/year",
        },
    ]
    for status, count in sorted(Counter(row["review_status"] for row in relations).items()):
        metrics.append(
            {
                "metric": f"relation_review_status_{status}",
                "value": str(count),
                "definition": "current post-HR018 relation status count",
            }
        )
    for status, count in sorted(Counter(row["review_status"] for row in amounts).items()):
        metrics.append(
            {
                "metric": f"amount_review_status_{status}",
                "value": str(count),
                "definition": "current post-HR018 amount-observation status count",
            }
        )
    for status, count in sorted(Counter(row["review_status"] for row in functions).items()):
        metrics.append(
            {
                "metric": f"function_review_status_{status}",
                "value": str(count),
                "definition": "current post-HR018 function-observation status count",
            }
        )
    for relation_type, count in sorted(Counter(row["relation_type"] for row in relations).items()):
        metrics.append(
            {
                "metric": f"relation_type_{relation_type}",
                "value": str(count),
                "definition": "within-package relation_type count; sums to 35",
            }
        )
    write_csv(out / "figure_metrics_v1.csv", metrics)
    (out / "R10_explanatory_brief_v1.md").write_text(
        r10_brief(relations, amounts, functions),
        encoding="utf-8",
    )


def make_r10_fact(
    relation: dict[str, str],
    *,
    entry_mode: str,
    venue_label: str,
    place: str,
    origin_type: str,
    local_object: str | None = None,
) -> dict[str, str]:
    return {
        "observation_id": f"OBS_{relation['relation_observation_id']}",
        "source_layer": "R10_human_reviewed_relation",
        "source_record_ids": relation["relation_observation_id"],
        "event_or_project_id": relation["relation_observation_id"],
        "event_or_project_name": relation["program_name"],
        "date_or_period": relation["fiscal_year"] or relation["period_start"],
        "actor_id": relation["source_entity_id"],
        "legacy_candidate_id": "",
        "actor_name": relation["source_entity_name"],
        "actor_category": relation["source_entity_kind"],
        "origin_type": origin_type,
        "role": relation["relation_type"],
        "entry_mode": entry_mode,
        "venue_id": "R10_VENUE",
        "venue_label": venue_label,
        "target_type": relation["target_entity_kind"],
        "target_id_or_name": relation["target_entity_name"],
        "local_object": local_object or relation["target_entity_name"],
        "place": place,
        "observation_type": "human_reviewed_function_or_resource_relation",
        "evidence_level": relation["evidence_level"],
        "source_refs": relation["source_refs"],
        "review_status": relation["review_status"],
        "interpretation_limit": relation["interpretation_limit"],
    }


def apply_hr021(
    root: Path,
    overlays: dict[str, dict[str, dict[str, str]]],
    relations: list[dict[str, str]],
) -> None:
    out = root / "outputs/R06_R07_R11_pathways_v1"
    data = root / "data/interim"
    relation_by_id = index_unique(relations, "relation_observation_id")

    queue_path = out / "HR021_review_items_v0.csv"
    queue = read_csv(queue_path)
    for row in queue:
        overlay = overlays["HR021"][row["review_item_id"]]
        row["review_decision"] = overlay["decision"]
        row["human_reviewer"] = overlay["human_reviewer"]
        row["review_date"] = overlay["review_date"]
        row["review_note"] = (
            f"{overlay['approved_formulation']} | 边界：{overlay['scope_boundary']}"
        )
        row["approved_formulation"] = overlay["approved_formulation"]
        row["scope_boundary"] = overlay["scope_boundary"]
        row["decision_source_report"] = overlay["source_report"]
        row["prerequisite_status"] = (
            "not_applicable_seed_review"
            if row["review_item_id"] == "HR021-008"
            else "hr018_completed"
        )
    write_csv(queue_path, queue)

    seeds_path = out / "analytical_seeds_v0.csv"
    seeds = read_csv(seeds_path)
    seed_overlay = overlays["HR021"]["HR021-008"]
    for row in seeds:
        row["hr021_disposition"] = "retain_analytical_seed"
        row["human_reviewer"] = seed_overlay["human_reviewer"]
        row["review_date"] = seed_overlay["review_date"]
        row["decision_source_report"] = seed_overlay["source_report"]
        row["hr021_scope_boundary"] = seed_overlay["scope_boundary"]
    write_csv(seeds_path, seeds)

    specs = {
        "R10R001": (
            "administrative_commission",
            "JICA commissioned-program venue",
            "Okinawa international-cooperation field",
            "public_institution",
            "Okinawa NGO Center (ONC)",
        ),
        "R10R004": (
            "administrative_commission",
            "Okinawa City public-facility commission",
            "Koza/Okinawa City",
            "public_institution",
            "Koza International Plaza / ONC",
        ),
        "R10R005": (
            "administrative_commission_and_secretariat",
            "Okinawa Prefecture multicultural-policy venue",
            "Okinawa Prefecture",
            "public_institution",
            "multicultural meeting support / ONC",
        ),
        "R10R006": (
            "administrative_commission",
            "MOFA NGO consultation commission",
            "Okinawa/Japan",
            "public_institution",
            "ONC FY2024 NGO consultation",
        ),
        "R10R007": (
            "annual_designated_public_service_role",
            "MOFA annual designation list",
            "Okinawa/Japan",
            "public_institution",
            "ONC FY2026 annual designated role",
        ),
        "R10R008": (
            "proposal_selected_public_contract",
            "Okinawa Prefecture advocacy-administration boundary",
            "Okinawa Prefecture",
            "public_institution",
            "base-policy symposium commission / A066",
        ),
        "R10R018": (
            "service_presence",
            "USO/base-community service venue",
            "Okinawa bases",
            "us_origin",
            "eligible U.S. military community",
        ),
        "R10R020": (
            "service_sponsorship",
            "USO Okinawa direct sponsor layer",
            "Okinawa",
            "corporate",
            "USO Okinawa",
        ),
        "R10R021": (
            "regional_service_sponsorship_context",
            "USO Indo-Pacific regional sponsor perimeter",
            "Indo-Pacific; Okinawa page context",
            "corporate",
            "USO Indo-Pacific regional perimeter",
        ),
    }
    new_fact_ids = {f"OBS_{relation_id}" for relation_id in specs}
    facts_path = data / "26_actor_event_venue_target_entry_modes_v0.csv"
    facts = [
        row for row in read_csv(facts_path) if row["observation_id"] not in new_fact_ids
    ]
    for relation_id, (entry_mode, venue, place, origin, local_object) in specs.items():
        facts.append(
            make_r10_fact(
                relation_by_id[relation_id],
                entry_mode=entry_mode,
                venue_label=venue,
                place=place,
                origin_type=origin,
                local_object=local_object,
            )
        )
    write_csv(facts_path, facts)

    r11_path = out / "r11_external_entry_matrix_v0.csv"
    r11 = [
        row
        for row in read_csv(r11_path)
        if row["fact_observation_id"] not in new_fact_ids
    ]
    fact_by_id = index_unique(facts, "observation_id")
    r11_specs = [
        ("R10R001", "administrative", None),
        ("R10R004", "administrative", None),
        ("R10R005", "administrative", None),
        ("R10R006", "administrative", None),
        ("R10R007", "administrative", None),
        ("R10R008", "administrative", "A066"),
        ("R10R018", "service", None),
        ("R10R020", "service", None),
        ("R10R021", "service", None),
    ]
    stances = {
        "R10R001": "commission role only; no public amount or event-co-participation collapse",
        "R10R004": "amounts remain in R10 only; no government endorsement",
        "R10R005": "project costs are not payments or movement funding",
        "R10R006": "FY2024 commission only; no disclosed contract amount",
        "R10R007": "FY2026 annual designation only; no inherited FY2024 amount",
        "R10R008": "specific contract only; no grant, alliance, or government endorsement",
        "R10R018": "service presence does not establish a base-policy stance",
        "R10R020": "direct sponsor tier has no amount or political-stance inference",
        "R10R021": "regional sponsor context; no Okinawa-directed allocation",
    }
    for relation_id, domain, entry_override in r11_specs:
        fact = fact_by_id[f"OBS_{relation_id}"]
        entry_actor_id = fact["actor_id"]
        entry_actor_name = fact["actor_name"]
        origin = fact["origin_type"]
        target = fact["target_id_or_name"]
        if entry_override == "A066":
            entry_actor_id = "A066"
            entry_actor_name = "新外交イニシアティブ（ND）"
            origin = "japan_domestic"
            target = "冲绳县"
        r11.append(
            {
                "matrix_row_id": "",
                "fact_observation_id": fact["observation_id"],
                "entry_domain": domain,
                "entry_mode": fact["entry_mode"],
                "entry_actor_id": entry_actor_id,
                "entry_actor_name": entry_actor_name,
                "origin_type": origin,
                "local_object": fact["local_object"],
                "event_or_project": fact["event_or_project_name"],
                "venue_or_entry_point": fact["venue_label"],
                "target": target,
                "place": fact["place"],
                "role": fact["role"],
                "evidence_level": fact["evidence_level"],
                "source_refs": fact["source_refs"],
                "review_status": fact["review_status"],
                "directionality": "observed role/relation only; no causal direction beyond source",
                "political_stance_boundary": stances[relation_id],
                "interpretation_limit": fact["interpretation_limit"],
            }
        )
    for index, row in enumerate(r11, start=1):
        row["matrix_row_id"] = f"R11M{index:03d}"
    write_csv(r11_path, r11)

    r6_path = out / "r06_pathway_comparison_v0.csv"
    r6 = read_csv(r6_path)
    r6_by_id = index_unique(r6, "pathway_id")
    r6_by_id["R6P05"].update(
        {
            "observed_actor_roles": (
                "event collaborator; commissioned program/report contractor; "
                "proposal-selected public contractor"
            ),
            "venue_or_entry_point": (
                "JICA/international-cooperation event and commission; "
                "Okinawa Prefecture policy-program contract"
            ),
            "target": "ONC/JICA cooperation and Okinawa base-policy symposium",
            "fact_observation_ids": "OBS_R10R017;OBS_R10R001;OBS_R10R008",
            "fact_count": "3",
            "verified_actor_or_entity_count": "3",
            "unverified_event_participant_count": "0",
            "source_refs": "S095;S100;S002;R10S11",
            "observed_result": (
                "The sample distinguishes event co-participation, a bounded "
                "commissioned training/report role, and a proposal-selected "
                "base-policy symposium contract."
            ),
            "interpretation_limit": (
                "These are specific administrative entry modes, not grants, "
                "stable alliances, government endorsement, or movement funding. "
                "Amounts remain in the separate R10 amount layer."
            ),
        }
    )
    write_csv(r6_path, r6)

    (out / "R06_R07_R11_explanatory_brief_v1.md").write_text(
        pathways_brief(facts, seeds, r11),
        encoding="utf-8",
    )
    (out / "validation_note_v0.md").write_text(
        pathways_validation(facts, seeds, r11),
        encoding="utf-8",
    )


def r10_brief(
    relations: list[dict[str, str]],
    amounts: list[dict[str, str]],
    functions: list[dict[str, str]],
) -> str:
    relation_status = Counter(row["review_status"] for row in relations)
    amount_status = Counter(row["review_status"] for row in amounts)
    function_status = Counter(row["review_status"] for row in functions)
    actual_contracts = sum(row["amount_basis"] == "actual_contract_amount" for row in amounts)
    project_costs = sum("project_cost" in row["amount_basis"] for row in amounts)
    aggregates = sum(row["amount_basis"].startswith("aggregate_") for row in amounts)
    return f"""# R10 解释 brief v1：行政协作、资金证据与服务生态

日期：2026-07-20
状态：HR-018 已合并；关系、金额与功能仍是三张独立事实表。

## 1. 当前样本与人审状态

当前目的性跨来源样本共有 **{len(relations)} 条关系观察、{len(amounts)} 条金额观察、{len(functions)} 条功能观察**。这不是冲绳县 616 行官方总体的年度／部门全量，也不是“运动资金网”。

- 关系：24 `human_checked`、10 `human_revised`、1 `needs_local_retrieval`。
- 金额：21 `human_checked`、6 `human_revised`、1 `needs_local_retrieval`。
- 功能：29 `human_checked`、13 `human_revised`、1 `needs_local_retrieval`。

机器校验对应值：relations={dict(relation_status)}；amounts={dict(amount_status)}；functions={dict(function_status)}。

## 2. 现在可以说什么

1. JICA、冲绳市、冲绳县和外务省公开材料确认了若干有界的委托、指定角色与补助关系。它们只适用于具名项目和期间，不证明稳定联盟、政府对组织全部主张的认可或反基地运动资金。
2. KIP 的 18.858m 总事业费、16.662m 点名交付对象部分、2.196m 独立运营观察和 ONC 16.040m 组织侧事业费继续分栏；不相加、不相减、不当成同一付款口径。
3. 县多文化项目的 5.140m 与 ONC 5.530234m 是两种 project-cost observation；外务省 2.894630m 也是组织侧事业分类成本，均不是已确认合同付款。
4. 精确合同额现在有 **{actual_contracts} 条**：A066、A088 两项、国际协力人才培养 JV 与 Team OKIYUA。合同额属于具名项目相手方，不拆给 JV 成员，也不改写成 grant。
5. USO、AWWA 与军属配偶组织只按公开的服务、赞助、成员、慈善与实物支持功能编码，不由此推断亲基地／反基地立场。

## 3. 金额边界

- `actual_contract_amount`：{actual_contracts} 条，可按具名合同表达，但不是成员分配或运动资金。
- project-cost observations：{project_costs} 条，只作会计／项目背景。
- aggregate observations：{aggregates} 条，不按 recipient、成员或年度拆分。
- KOSC 的 102,000 美元仍是 scholarships＋AWWA 混合汇总；HR-033 已确认的 KOSC→AWWA dyad 金额为空，混合总额只留在 R10R029／R10AM024，永不上组织关系图。
- JPY 与 USD 不跨币种求和；实物价值不写成现金支付；sponsor tier 不换算金额。

## 4. 唯一未收口项

R10R030 的约 8 亿日元／40 年仍为 `needs_local_retrieval`：来源没有逐年、逐 recipient 分解。它只能作为不可分配 aggregate history，不阻断其余线上 HR-018 收口。

## 5. 下游与图

HR-021 只允许九条有解释价值的已审关系进入 R6／R11；R11 不复制 R10 金额。`fig_r10_mechanism_ecology.png` 与 `fig_r10_amount_evidence_boundary.png` 本轮没有重绘，视为 pre-HR018 快照；当前正式计数和语义以三张中央 CSV 与本 brief 为准。
"""


def pathways_brief(
    facts: list[dict[str, str]],
    seeds: list[dict[str, str]],
    r11: list[dict[str, str]],
) -> str:
    counts = Counter(row["entry_domain"] for row in r11)
    return f"""# R6 / R7 / R11 线上解释层 brief v1

日期：2026-07-20
状态：HR-021 八项决定已合并。

## 共享底盘

- 正式 actor–event–venue–target/entry-mode 事实：**{len(facts)}** 条。
- `analytical_seed`：**{len(seeds)}** 条，继续与正式事实分离。
- HR-021：5 项 `include_after_hr018`、2 项 `revise_scope_after_hr018`、1 项 `retain_analytical_seed`；未决 0。

HR-018 已审并不自动等于进入路径分析。只有 HR-021 明确放行的九条 R10 关系新增到正式底盘；其余已审关系留在 R10 的本模块事实层。

## R6：行政入口的三种不同事实

R6 的行政比较现在同时保留：ONC／JICA 的事件共同参与、JICA→ONC 的有界受托角色、冲绳县→A066 的提案选定合同。三者不能折成“共同合作”或“资金网络”；具体金额仍只在 R10 amount layer。

## R11：53 条进入观察

R11 共有 **{len(r11)}** 条：{", ".join(f"{key} {value}" for key, value in sorted(counts.items()))}。

- FY2024 外务省委托与 FY2026 年度指定分成两个观察，后者不继承前者金额。
- USO Okinawa 服务存在只形成一条 service relation；八个 site/function 继续留在 R10 功能层。
- MBC 是本地 direct sponsor observation；Matson 只作为 USO Indo-Pacific 区域 sponsor perimeter，不写成本地定向资助。
- 委托、指定、服务和 sponsor tier 都不自动产生政治立场、稳定联盟或因果路径。

## analytical seed 边界

AEV0061–0064 继续作为分析性路径假说。已有的共同要请、调查和事件事实不证明 A019→A003→A004/A005 的有向传递；四条 seed 不进入正式计数、默认事实层或稳定关系网。

## 图状态

R6／R7／R11 的三张 SVG 与三张 HTML 由独立的 `scripts/render_r06_r07_r11_current.py` 从当前 6／9／{len(r11)} 行模块 CSV 重绘。本合并脚本不写这六个图件；每次合并后必须再次运行该 renderer，且不得把旧 pre-HR021 图当作当前输出。
"""


def pathways_validation(
    facts: list[dict[str, str]],
    seeds: list[dict[str, str]],
    r11: list[dict[str, str]],
) -> str:
    return f"""# Validation note

- Formal observations: {len(facts)}
- Analytical seeds: {len(seeds)}
- R6 pathway families: 6
- R7 cases/stages: 3 / 9
- R11 external-entry observations: {len(r11)}
- HR-021 unresolved items: 0
- HR-021 decisions: 5 include_after_hr018; 2 revise_scope_after_hr018; 1 retain_analytical_seed
- HR-021 downstream additions: 9 R10 observations only

HR-018 human review is necessary but not sufficient for pathway admission.  The
formal shared table adds only the nine relations explicitly approved by HR-021.
R11 carries no amount field and does not duplicate, sum, or reinterpret R10
amount observations.  AEV0061–0064 remain analytical seeds outside facts and
counts.  The six SVG/HTML assets are rendered separately from the current
6/9/{len(r11)}-row module CSVs by `scripts/render_r06_r07_r11_current.py`.
This merge does not write those figures, so the renderer must be rerun after
every merge; pre-HR021 assets are never valid current outputs.
"""


def validate(
    relations: list[dict[str, str]],
    amounts: list[dict[str, str]],
    functions: list[dict[str, str]],
    root: Path,
) -> None:
    expected = {
        "relations": Counter(
            {"human_checked": 24, "human_revised": 10, "needs_local_retrieval": 1}
        ),
        "amounts": Counter(
            {"human_checked": 21, "human_revised": 6, "needs_local_retrieval": 1}
        ),
        "functions": Counter(
            {"human_checked": 29, "human_revised": 13, "needs_local_retrieval": 1}
        ),
    }
    actual = {
        "relations": Counter(row["review_status"] for row in relations),
        "amounts": Counter(row["review_status"] for row in amounts),
        "functions": Counter(row["review_status"] for row in functions),
    }
    if actual != expected:
        raise ValueError(f"post-HR018 status mismatch: {actual}")
    if len(relations) != 35 or len(amounts) != 28 or len(functions) != 43:
        raise ValueError(
            f"post-HR018 counts mismatch: {len(relations)}/{len(amounts)}/{len(functions)}"
        )
    facts = read_csv(
        root / "data/interim/26_actor_event_venue_target_entry_modes_v0.csv"
    )
    r11 = read_csv(
        root / "outputs/R06_R07_R11_pathways_v1/r11_external_entry_matrix_v0.csv"
    )
    if len(facts) != 80 or len(r11) != 53:
        raise ValueError(f"post-HR021 counts mismatch: facts={len(facts)} r11={len(r11)}")
    new_ids = {
        "OBS_R10R001",
        "OBS_R10R004",
        "OBS_R10R005",
        "OBS_R10R006",
        "OBS_R10R007",
        "OBS_R10R008",
        "OBS_R10R018",
        "OBS_R10R020",
        "OBS_R10R021",
    }
    fact_ids = {row["observation_id"] for row in facts}
    if not new_ids <= fact_ids or "OBS_R10R029" in fact_ids:
        raise ValueError("HR021 downstream gate was not preserved")


def merge(root: Path = ROOT) -> None:
    overlays = overlay_index(root)
    relations, amounts, functions, _ = apply_hr018(root, overlays)
    update_r10_package(root, relations, amounts, functions)
    apply_hr021(root, overlays, relations)
    validate(relations, amounts, functions, root)


if __name__ == "__main__":
    merge()
    print(
        "Merged HR-018/HR-021: "
        "R10=35 relations/28 amounts/43 functions; R11=53 observations."
    )
