# HR-USN2：对美主线第二轮人工复核任务书 v1

日期：2026-08-22

状态：`assigned_to_principal / decisions_blank`。本任务只处理会改变人物桥、recipient 端点、资金／服务关系语义、问责结果或跨生态表述的判断。原始逐行队列仍保存在 W2-A／B／C／D 各包的 `principal_review_queue_v1.csv`；本任务按阅读包合并展示，不删除任何原决定。

## 回传规则

每项填写：`accept / revise / defer_new_primary / reject`，并给一到三句理由。子项不能用一个总决定覆盖。找不到决定性原件时，`defer_new_primary` 是完整决定，不要求猜测。

人工确认只改变相应研究层判断；中央写回、publication adapter 和前端仍需 W2-G 另行授权。

## HR-USN2-01：军属组织人物同一性

原队列：W2A-HR001、002、003、004、016；W2D-PR002。

先读：`outputs/us_presence_network_wave2_w2_a_v1/person_actor_role_time_v1.csv`、`w2d_endpoint_handoff_v1.csv` 和对应 IRS XML Part VII。

| 子项 | 候选 | 需要决定 | 负责人决定 |
|---|---|---|---|
| 01a | Brooke Epps（AWWA）／Brooke Epp（KOSC） | same person／different／unresolved |  |
| 01b | Jen Yapsing（AWWA）／Jennifer Yapshing（NOSCO） | same person／different／unresolved |  |
| 01c | Amber Tracy（AWWA／OESC） | 是否为同一人且任期重叠 |  |
| 01d | Trinicia Kloepper（AWWA／KOSC） | 是否为同一人且任期重叠 |  |
| 01e | Lesilee Du Fresne／DuFresne（OESC） | spelling variant／different／unresolved |  |

边界：这些最多形成服务侧人物桥；即使确认，也不是问责侧—服务侧的跨生态人物桥。

## HR-USN2-02：VFP-ROCK chapter 身份连续性

原队列：W2D-PR003。

对象：`VFP-ROCK`、`VFP ROC`、`Ryukyu/Okinawa Chapter Kokusai`、`Ryukyu-Okinawa Chapter`、`Chapter 1003`。

先读：W2-D `person_disambiguation_queue_v1.csv`；A070 的 2023／2025 官方 resolution 和 2024 peace-tour 页面。

决定：`one_continuous_chapter / partial_alias_with_dates / distinct_or_unresolved / defer_charter_or_roster`。

负责人决定：

## HR-USN2-03：AWWA recipient 身份 crosswalk

原队列：W2A-HR005—007。

先读：`awwa_recipient_identity_leg2_v1.csv` 中 W2A-A071、A072、A075 及其 source receipts。

| 子项 | 英文申报描述 | 候选实体 | 决定 |
|---|---|---|---|
| 03a | NPO ARU | 一般社団法人ある |  |
| 03b | Okinawa Nanbu Rehabilitation and Medical Center | 沖縄南部療育医療センター |  |
| 03c | Okinawa Southern Medical Center | 沖縄県立南部医療センター・こども医療センター |  |

可选：`accept_crosswalk / revise_entity / reject / defer_new_primary`。注意 03b 与 03c 不得因英文近名合并。

## HR-USN2-04：三笔 recipient 交易是否闭合

原队列：W2A-HR008—010。

| 子项 | 申报行／地方材料 | 当前问题 | 决定 |
|---|---|---|---|
| 04a | Himawari USD 13,378／地方通讯 JPY 2m | 是否同一事件；现有地方记录时间似晚于申报期 |  |
| 04b | Ambitious USD 13,423／2024-06 JPY 2m | 是否应继续视为不同事件 |  |
| 04c | Kana-san USD 15,287／2023 无金额传单 | 是否只能确认 recipient 回应，不能闭合金额 |  |

可选：`same_transaction / separate_events / acknowledgment_only / defer_ledger_or_accounts`。

## HR-USN2-05：LEG2 地方回应分类

原队列：W2A-HR011。

分别阅读 Kana-san、Ambitious、Himawari 的 recipient／地方原文。每条可多选但须说明：`practical_use / gratitude / partner_or_bridge_narration / rights_or_compensation_reframing / distance_or_rejection / insufficient`。

负责人决定：

边界：任何 LEG2 决定都不能生成 LEG3“合法性提升”。

## HR-USN2-06：Marine Thrift Shop／MOSCO 新一手材料门

原队列：W2A-HR012、013、015；W2A-HR014 为既有 standing defer，不重审。

| 子项 | 当前缺口 | 建议 | 决定 |
|---|---|---|---|
| 06a | MTS `>110k`／DVIDS `>126k`／IRS `125,218` 三口径 | 保持并列，不任选或相加 |  |
| 06b | MTS→Lions USD 10k 的最终儿童医疗 recipient | 未闭合 Lions→最终端点 |  |
| 06c | MOSCO FY2025 grants 元素缺失、USD 7,500 program expense | blank 不是 0，不能写成付给 AWWA |  |

可选：`accept_current_boundary / revise / defer_new_primary`。

## HR-USN2-07：USO 财务、站点与地区分配缺口

原队列：W2B2-PR001、002、006。

先读：W2-B 图、README §3.1—3.2、USO 2024 审计财报 p.8 和 `federal_award_allocation_audit_v1.csv`。

请分别决定：

1. 接受 2021 `7 listed locations`／2025 `6 physical centers`／当前 `8 directory entries`，不作生命周期推断；
2. 接受 USD 72m 与 USD 41.21246329m 为同一 award 的并列报送视图；
3. 接受 gross USD 204.912m（含 in-kind USD 105.538m）／net USD 99.374m；
4. 接受“地区金额分配层未公开闭合”的最强结论。

负责人决定：

## HR-USN2-08：USO 本地资源、sponsor scope 与 LEG 边界

原队列：W2B2-PR003、004、007。

先读：`sponsor_and_local_flow_observations_v1.csv` 与相关 official source receipts。

决定：哪些具日具额现金／具名实物行可进入未来共享 ledger；regional sponsor tier 与 Okinawa local tier 是否按网页层级分开；USO 自有故事中的参与者话语是否继续停在 LEG0／行动方 LEG1。

负责人决定：

## HR-USN2-09：NMCRS→American Red Cross 服务接口

原队列：W2B2-PR005、W2D-PR009。

先读：W2B2-SR022—024 和 W2B2-DE028。

拟定编码：`NMCRS → American Red Cross / directed_after_hours_intake_disbursement_delegation / uses_NMCRS_funds / current_snapshot`。

可选：`accept_service_interface / revise_direction_or_type / defer / reject`。

负责人决定：

边界：不是 Red Cross 获得 grant，不是联盟、合并或共同政治立场。

## HR-USN2-10：泡濑一审的判决层结果

原队列：W2C-HR002、003、011。

先读：`source_docs/source_archive/S140/raw.pdf` p.1、197–198；W2-C `project_change_attribution_frame_v1.csv` 的 W2C-PC001／002。

请分别决定：

1. 是否接受一审主文支持 `PROJECT_BUDGET=yes_bounded`、`PROJECT_AUTHORITY=yes_bounded` 的 judgment-level outcome；
2. 是否同意它只构成有界反例候选，不代表持续限制、实际预算改变或项目取消；
3. 是否维持 185ha→95ha 范围变化不能归因给诉讼。

负责人决定：

## HR-USN2-11：问责比较框、事件与归因

原队列：W2C-HR001、004—010。

建议分两步：

1. 先判方法：13 episode 是异质比较框；六行是 gate／control；true matched non-entry arm `not_established`；TE12／TE13 不计独立制度入口。
2. 再逐行判 TE10—TE13、TE12 军舰访问是否完成、Nago／FRF 与 1997 公投的归因、PFAS mediation／EIA redo／十问信的 gate semantics。

逐行决定仍填写 W2-C `principal_review_queue_v1.csv`，本处只填是否接受上述两步复核结构：

负责人决定：

## HR-USN2-12：Bridge audit 的有界负面表述

原队列：W2D-PR001。

证据：S0×A0 54 对中 48 对两端同期可观察，36 对完成声明来源范围内的 direct-relation 对称检索，18 对未决；跨侧确认桥为 0。

拟定表述：**在声明的 2023–2025 公开资料窗口中，尚未确认两侧 actor 的直接组织关系。**

可选：`accept_bounded_wording / narrow_to_current_typed_inputs / defer / reject`。

负责人决定：

边界：人物、recipient、funder、event 均不能据此写零。

## HR-USN2-13：DoD 共同制度接口与人物网络范围

原队列：W2D-PR004—007。

请分别决定：

1. DoD 是否单列 `system_interface`：对 USO 全国组织是 prime-award institution，对问责侧是被告／诉求对象；不计 NGO bridge；
2. 人物层是否只做 tracer egonet，不做覆盖不足的全网中心性；
3. Marine Thrift Shop（X018）是否继续留在 tracer，待 actor admission 和 S1 版本化；
4. ARC Okinawa、NMCRS Okinawa、ACGO 的当前 roster／财务是否进入下一批当地／新一手材料任务。

负责人决定：

## 正式回传格式

建议新建：`docs/human_review_return_USN_wave2_ABCD_v1.md`。

逐项写：

```text
HR-USN2-xx / 子项：
决定：accept | revise | defer_new_primary | reject
理由：
证据：文件／页码／locator
允许写法：
禁止外推：
```

W2-A／B／C／D 原始 queue 的 `principal_decision`／`human_decision` 字段在受控合并前保持空白；不要直接手改生成 CSV。
