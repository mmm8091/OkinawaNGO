# 基地内私人组织公开规则层 v1

日期：2026-08-22

状态：research_only / formal_rule_layer / ai_seeded / not_frontend_ready / central_writeback=no

## 1. 问题与范围

本包回答一个严格有界的问题：MCIPAC-MCB Camp Butler 与 Kadena Air Base 的公开规则，怎样规定基地内 private organization 的运作准入、合规、暂停或撤销、场地许可与成本偿还、持续零售例外以及行政档案义务？

选择框只包括两份现行公开规则：2022 年 MCIPAC-MCBBO 5760.2 与 2024 年 18 FSS OI 34-223-1。观察单位是“一个规则条款所规定的一项制度位置、权限或义务”，不是组织的政治立场，也不是现实中的资金或控制关系。

本包由既有 lead 包中获负责人批准的“公开规则层”重新按正式研究 schema 提取。原 lead 行只作 provenance；本包的事实均重新回到官方原文和 locator。未取得的 actor-specific authorization、license、room、费用单据、章程、季度账、银行流水和捐赠收据没有被升格。

## 2. 最短结果

公开规则支持的是一种“私人主体＋基地运作许可”的制度结构：组织本身保持 non-federal／私人责任地位；installation command 掌握能否在基地内运作以及实施规则制裁的权限；MCCS 或 FSS 负责申请流转、合规监测和规定材料的接收或保管。Kadena 规则明确把 18 MSG 的 supervision 限定在准入与撤销，不延伸为对组织内部活动或结构的控制；但同一规则又将第四次文档违规原文写为 “Dissolution of the PO”。本包忠实保留这个措辞，尚未确认它是否实际执行，也不据此断言基地外法人已经或必然消灭。

场地与后勤不能直接写成补贴。MCIPAC 对持续使用 DoD 场地要求 real-estate license，并要求偿还水电、材料、服务及其他成本；Kadena 规定使用 18 FSS 设备、服务或支持时按正常费用收费。两份规则都没有证明任何具名组织获得免费房间、免水电或政府日常供养。

持续零售是另一种制度位置。MCIPAC 规则为 thrift shop 和 authorized gift shop 保留一般禁售规则的例外；Kadena 规则具名允许 Kadena Officers' Spouses Club Gift Corner 与 Kadena Enlisted Spouses Club Thrift Store 持续零售。它证明被允许的创收渠道，不是政府拨款、独占权、组织隶属或政治背书。

## 3. 交付计数

- 1 个冻结选择框；
- 2 份官方规则来源收据，其中 Kadena PDF 有包内原件与 SHA-256；
- 25 条规则事实：MCIPAC 14 条、Kadena 11 条；
- 9 类关系／属性语法；
- 10 个同维度比较单元；
- 6 条可用于内部报告草稿的有界命题；
- 5 项明确排除范围；
- 0 条本包新增意外发现。

所有事实仍为 ai_seeded，未获得逐行人审；“可用于报告”是指命题已具官方来源、locator 与限定语，可以进入负责人审稿，不等于 publication 或前端资格。

## 4. 关系语法的核心边界

本包将制度位置拆成：

1. installation_authorization：允许在基地内运作；
2. administrative_monitoring：申请流转、合规监测或审计；
3. compliance_reporting：组织须提交的治理／财务材料；
4. sanction_authority：probation、suspension、revocation，以及 Kadena 第四次违规原文所称 “Dissolution of the PO”；
5. facility_license_requirement：持续场地使用所需的许可；
6. reimbursable_support_terms：可提供服务的费用与条件；
7. continuous_resale_exception：持续零售禁令中的具名或类别例外；
8. legal_status_boundary：non-federal／私人地位；
9. private_liability_boundary：组织或成员承担债务与风险。

这些语法的 graph_eligibility 全部是合法值 administrative_record；其中纯属性边界另在 layer_kind 标为 attribute_only。它们不生成组织—组织边，不进入网络中心性，也不能转写为 affiliation、governance_control、funding 或 sponsorship。Kadena 的 dissolution 原文也不能被降格改写为单纯的 operating-status revocation；与此同时，在没有执行记录和基地外法律机制材料时，它也不能升格为已证实的法人消灭。

## 5. 明确留在原 lead 包的部分

installation records office 可能保存的 actor-specific 章程、预算、季度账、银行流水、捐赠收据、授权书和 license 仍是 lead_only 取件方向。本正式包只确认“规则要求形成或提交哪些材料”，不把取得这些材料写成交付预期，也不以其缺失阻断本包。

本包没有发送信息公开请求，没有新增当地任务，没有修改中央表、HR、publication adapter 或前端，也没有改变 W2-F 状态。

## 6. 文件

| 文件 | 用途 |
|---|---|
| selection_frame_v1.csv | 问题、来源、纳入与排除边界 |
| public_rule_facts_v1.csv | 25 条带 locator 的正式规则事实 |
| governance_relation_grammar_v1.csv | 九类制度关系／属性的方向、证据门和禁推规则 |
| regime_comparison_matrix_v1.csv | MCIPAC 与 Kadena 的同维度比较 |
| bounded_report_claims_v1.csv | 六条有界报告命题、证据和反证条件 |
| lead_promotion_crosswalk_v1.csv | 原 lead 与正式规则层的 provenance；未升格部分仍留 lead_only |
| scope_exclusions_v1.csv | 未纳入本包的 actor-specific、Navy／Army、资金和取件事项 |
| source_receipts_v1.csv | 官方来源、locator、归档状态与解释边界 |
| local_artifact_manifest_v1.csv | 包内 Kadena 原始 PDF 的哈希收据 |
| unexpected_findings_register_v1.csv | 本轮 0 条，保留标准表头 |
| validate_package_v1.py | 包内语义、状态、引用、哈希和格式门禁 |
| manifest_v1.json | 文件哈希和包状态 |
| validation_report_v1.json | 验证结果 |

## 意外发现登记

本轮没有在获批问题之外继续侦察，登记 0 条。unexpected_findings_register_v1.csv 保留标准 19 列表头。原 lead 包中的行政档案取件方向没有被复制到本表，也没有自动升级。

## 7. 复现与验证

    python outputs\us_presence_network_wave2_base_private_org_governance_rules_v1\validate_package_v1.py
    python scripts\validate_research_work_package_v1.py outputs\us_presence_network_wave2_base_private_org_governance_rules_v1

两项 PASS 只证明本包结构、来源引用、隔离状态和本地哈希一致；不授予中央写回、publication 或前端资格。
