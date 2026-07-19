# R10 解释 brief v1：行政协作、资金证据与服务生态

日期：2026-07-20
状态：HR-018 已合并；关系、金额与功能仍是三张独立事实表。

## 1. 当前样本与人审状态

当前目的性跨来源样本共有 **35 条关系观察、28 条金额观察、43 条功能观察**。这不是冲绳县 616 行官方总体的年度／部门全量，也不是“运动资金网”。

- 关系：24 `human_checked`、10 `human_revised`、1 `needs_local_retrieval`。
- 金额：21 `human_checked`、6 `human_revised`、1 `needs_local_retrieval`。
- 功能：29 `human_checked`、13 `human_revised`、1 `needs_local_retrieval`。

机器校验对应值：relations={'human_checked': 24, 'human_revised': 10, 'needs_local_retrieval': 1}；amounts={'human_checked': 21, 'human_revised': 6, 'needs_local_retrieval': 1}；functions={'human_checked': 29, 'human_revised': 13, 'needs_local_retrieval': 1}。

## 2. 现在可以说什么

1. JICA、冲绳市、冲绳县和外务省公开材料确认了若干有界的委托、指定角色与补助关系。它们只适用于具名项目和期间，不证明稳定联盟、政府对组织全部主张的认可或反基地运动资金。
2. KIP 的 18.858m 总事业费、16.662m 点名交付对象部分、2.196m 独立运营观察和 ONC 16.040m 组织侧事业费继续分栏；不相加、不相减、不当成同一付款口径。
3. 县多文化项目的 5.140m 与 ONC 5.530234m 是两种 project-cost observation；外务省 2.894630m 也是组织侧事业分类成本，均不是已确认合同付款。
4. 精确合同额现在有 **5 条**：A066、A088 两项、国际协力人才培养 JV 与 Team OKIYUA。合同额属于具名项目相手方，不拆给 JV 成员，也不改写成 grant。
5. USO、AWWA 与军属配偶组织只按公开的服务、赞助、成员、慈善与实物支持功能编码，不由此推断亲基地／反基地立场。

## 3. 金额边界

- `actual_contract_amount`：5 条，可按具名合同表达，但不是成员分配或运动资金。
- project-cost observations：14 条，只作会计／项目背景。
- aggregate observations：2 条，不按 recipient、成员或年度拆分。
- KOSC 的 102,000 美元仍是 scholarships＋AWWA 混合汇总；HR-033 已确认的 KOSC→AWWA dyad 金额为空，混合总额只留在 R10R029／R10AM024，永不上组织关系图。
- JPY 与 USD 不跨币种求和；实物价值不写成现金支付；sponsor tier 不换算金额。

## 4. 唯一未收口项

R10R030 的约 8 亿日元／40 年仍为 `needs_local_retrieval`：来源没有逐年、逐 recipient 分解。它只能作为不可分配 aggregate history，不阻断其余线上 HR-018 收口。

## 5. 下游与图

HR-021 只允许九条有解释价值的已审关系进入 R6／R11；R11 不复制 R10 金额。`fig_r10_mechanism_ecology.png` 与 `fig_r10_amount_evidence_boundary.png` 本轮没有重绘，视为 pre-HR018 快照；当前正式计数和语义以三张中央 CSV 与本 brief 为准。
