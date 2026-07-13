# R10 解释 brief v1：行政协作、资金证据与服务生态

日期：2026-07-13
口径：本包描述**行政委托／补助、慈善支持、成员与服务功能**，不是“运动资金网”。共同出现在行政表、共同活动、赞助或服务对象均不自动构成政治联盟。

## 1. 本模块回答什么

R10 回答的是：冲绳的民间／非营利组织如何通过公开委托、补助、指定角色、慈善、成员网络和服务据点进入公共与基地社区生态；同时说明公开材料能够确认的金额语义上限。它不回答“谁资助反基地运动”，也不把服务美军人员与军属家庭的组织默认为亲基地或反基地 actor。

当前**目的性、跨来源 R10 样本**内共有 **35 条关系观察、26 条金额观察、43 条功能观察**。机制生态图在样本内分为上层行政机制 **16 条**与下层服务／慈善／非资金边界 **19 条**，内部加总为 16+19=35。该计数不代表任何官方表、部门、年度或机制的全量抽取。

样本内关系类型计数为：commission 14、designated_role 1、grant 2、sponsorship 3、donation 1、network_membership 5、in_kind_donation 3、joint_in_kind_contribution 1、service_presence 1、aggregate_history 2、grant_opportunity 1、event_collaboration 1；以上对当前 35 条内部加总完备，没有把活动协作或慈善 grant 隐入其他类型。

## 2. 解释性候选与已审边界

1. **ONC 的组织功能位于国际合作／多文化共生层；具体行政关系仍待 HR-018。** 公开材料为 JICA 教师海外研修、冲绳市 KIP 管理运营、冲绳县多文化共生会议运营支援与外务省 NGO 相談員形成官方来源候选。KIP 的多语咨询、语言课程与交流活动可解释其公共功能；但这些敏感行政关系须经 HR-018 接受／修订后才能作为事实关系发布，也没有证据把它们连到反基地运动网络。
2. **官方机制码把“服务内容”和“资金机制”分开。** 本包采用 C1=委託、C2=提案型公募による委託、C4=補助，并修正原候选五个错分：R10A010/A011/A012/A014/A016 全部是 commission，服务／教育留在功能表。
3. **官方记录形成 A066 与 A088 三份采购合同候选。** 记录金额分别为 12,842,500、26,439,000、8,479,000 日元；HR-018 接受前不得作为已冻结受托关系发布。即使接受，它们也只证明具体项目／年度的采购关系，不证明 grant、无条件行政支持、稳定政治联盟或“运动资金”。
4. **USO／AWWA／OESC／NOSCO 构成服务与慈善观察层。** USO 的公开对象是美军人员及军属家庭，AWWA 是军属配偶俱乐部伞状网络；赞助、成员、直接捐赠、实物支持和服务设点使用不同边型。OESC→USO 的直接捐赠与 NOSCO 共同交付冷风机均只能按具体事件表述。
5. **NOFO、aggregate 和 sponsor tier 必须留在证据边界外侧。** Okinawa Youth Council 只有机会公告，没有公开 award／recipient；AWWA 40 年累计口径与 KOSC 102,000 美元混合口径不能拆给具体 recipient；USO sponsor tier 不产生金额。

## 3. 金额为什么不能放进一条“资金边”

- `actual_contract_amount` 3 条：可以按合同写，但仅限具体项目、年度和相对方。
- `municipal_named_recipient_commission_flow` 3 条：2019/2020 KIP 是点名资金流；FY2024 的 16.662m 只是交付对象部分，必须同时保留 2.196m 交付对象外 3 月运营委托观察。
- project cost 共 14 条：包括行政表项目费与组织侧事业费，只能用于会计／项目背景，不能写成付款。
- aggregate 2 条：不按 recipient、年度或成员拆分。
- JPY 与 USD 保持原币种，不做跨币种求和；实物价值不写成现金支付。

## 4. 可确认与待人审

当前 9 条关系沿用既有 human_checked／human_revised 决策，26 条仍为 AI 整理或待第二来源／当地材料，不能由 AI 自行升级为 human_checked。

`HR018_relation_review_v0.csv` 将这 26 条关系作为 26 个主复核项；金额与功能仅以关联 ID 附着，不拆成额外数十条人工任务。`HR018_source_prerequisites_v0.csv` 另列 R10S05–R10S12 八项来源归档／source-log 前置条件，这些前置项尚未预作人审。

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
