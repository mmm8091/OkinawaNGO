# HR-018 行政协作／支持关系回交报告 Batch 21

日期：2026-07-20  
承办人：项目负责人  
辅助核查：Codex  
来源队列：`outputs/R10_administrative_collaboration_v0/HR018_relation_review_v0.csv`  
本批在线范围：HR-018-17–20、23–24  
本批暂不处理：HR-018-21–22  
状态：**负责人已确认——2 项 accept，4 项 revise；HR-018-21、22 暂缓**

## 0. 批次边界

- 本批处理 6 条在线可以完成的服务、赞助、历史成员和实物捐赠关系。
- HR-018-21、22 明确依赖年报、Form 990 或当地补查；按负责人“需要当地资料的不做”的规则，本批不调查、不建议判断。
- 服务对象和军事设施设点不等于亲基地或反基地立场。
- sponsor tier 只证明来源页面列示的赞助层级；没有公开金额时不得生成估计金额、资金边线宽或本地分配额。
- military spouse club 的 umbrella membership 不等于资助，也不能在没有时间证据时写成现行成员。
- 实物捐赠价值不是现金支付；受赠设施与其运营法人必须分层。
- DVIDS／军事公共事务来源可以支持有界事件事实，但证据层级保持 E3，不因正式机构身份 crosswalk 自动升级为 E4。
- 本报告不直接修改中央 relation 表、funding/support 表、source log、HR CSV、图或 brief。

## 0A. 本轮调查结果

| 项目 | 核查材料 | 本轮调查所得 |
|---|---|---|
| HR-018-17 | S097 归档页面和[现行 USO Okinawa 页面](https://okinawa.uso.org/sponsors)；[USO admissions policy](https://www.uso.org/admissions)；[USO Okinawa mission page](https://okinawa.uso.org/about/uso-mission-statement) | S097 及现行页面均列 8 个 location：Kinser、Hansen、Kadena、Foster、Kadena AMC Terminal、Okinawa Area Office、Futenma、Schwab。USO 官方政策确认现役、Reserve、Guard 和军属等使用群体。8 个地点可作为一条服务关系下的 8 个 function/site observation。 |
| HR-018-18 | S097；[MBC sponsor detail](https://okinawa.uso.org/sponsors/mbc)；[USO 对 MBC 的感谢页](https://okinawa.uso.org/stories/211) | 现行 USO Okinawa 页面将 MBC 列为 Platinum Sponsor；详情页确认 MBC Okinawa，感谢页确认全名 Mediatti Broadband Communications, Inc. 及现金＋网络／电视等实物支持，但没有可归属于本 relation 的金额。 |
| HR-018-19 | S097；[Matson sponsor detail](https://okinawa.uso.org/sponsors/matson) | sponsor 总页把 Matson 放在 `USO Indo-Pacific Mission Partners`，详情页明确写 `USO Indo-Pacific sponsor`。它出现在 USO Okinawa 页面，但证据不支持把赞助范围缩写成“只给 USO Okinawa 的本地定向赞助”。 |
| HR-018-20 | S041、S072、S081；[NOSCO 现行 AWWA 页面](https://nosco.wildapricot.org/awwa) | 2012 和 2015 材料把 Army Community Group of Okinawa 列为 AWWA 五个成员组织之一，S081 又确认 ACGO 运营 Army on Okinawa Gift Shop；但现行 AWWA 页面只列 NOSCO、KOSC、MOSC、OESC，不含 ACGO。该关系只能冻结为历史成员关系，不能保留为无时间限定的现行 membership。 |
| HR-018-23 | S094；[よみたん救護園官方设施页](https://www.okinawa-j.jp/yomitankyuugoen/pamphlet_yomitankyuugoen) | DVIDS 确认 2015-12-02，AWWA 向 Yomitan Quegoen/Kyugoen 捐赠价值 2,000,000 円的轮椅无障碍车辆。正式日文设施名为 `よみたん救護園`，运营法人为 `社会福祉法人沖縄県社会福祉事業団`；原英文拼写不是 canonical name。 |
| HR-018-24 | S072；[うるま市社会福祉協議会官网](https://www.uruma-shakyo.net/)；[Kadena Air Base 事件照片说明](https://www.kadena.af.mil/News/Photos/igphoto/2000157908/) | “Uruma City Social Welfare Meeting”应校正为 `社会福祉法人うるま市社会福祉協議会`。DVIDS 和 Kadena 官方照片说明支持 2012 年轮椅无障碍车辆捐赠，但未给金额，具体使用该车的下属日间活动设施也未点名。 |

S097 的归档时间为 2026-07-11，本轮于 2026-07-20 对现行页面再次核验。页面时点只证明该时点的公开列示，不外推整个历史期间。

## 1. 辅助建议总表

| review item | relation | 辅助建议 | 可批准的最强口径 | 必须保留的边界 |
|---|---|---|---|---|
| HR-018-17 | USO Okinawa→军事人员及军属的服务存在 | `accept` | 一条服务关系＋8 个 site/function observations | 不生成资金、政治立场或八条组织关系 |
| HR-018-18 | MBC→USO Okinawa | `accept` | MBC 是现行 Platinum Sponsor | 无公开 relation amount；现金与实物支持不估值、不合并 |
| HR-018-19 | Matson→USO | `revise` | Matson 是 USO Indo-Pacific Mission Partner | 不写成本地定向资助；USO Okinawa 页面只是公开展示入口 |
| HR-018-20 | ACGO→AWWA | `revise` | ACGO 在 2012、2015 被列为 AWWA 成员 | 改成历史 membership；当前名单不含 ACGO；不推断精确退出日 |
| HR-018-23 | AWWA→よみたん救護園 | `revise` | 2015-12-02 捐赠一辆价值 2m 円的无障碍车辆 | 校正设施名和运营法人；2m 是实物价值，不是现金 |
| HR-018-24 | AWWA→うるま市社会福祉協議会 | `revise` | 2012 年捐赠无障碍车辆 | 校正法人名；具体下属设施 unresolved；无金额 |

建议分布：

- `accept`：2 条；
- `revise`：4 条；
- `reject`：0 条；
- 本批暂不判断：2 条（HR-018-21、22）。

## 2. HR-018-17 · USO Okinawa 服务关系

S097 归档页面的 location navigation 逐项列出：

1. USO Camp Kinser；
2. USO Camp Hansen；
3. USO Kadena；
4. USO Camp Foster；
5. USO Kadena AMC Terminal；
6. USO Okinawa Area Office；
7. USO Futenma；
8. USO Camp Schwab。

2026-07-20 的现行页面仍列相同 8 个地点。这里的“Okinawa Area Office”是 USO 自己列出的 location，但与其他公开服务 center 的功能不完全相同；所以应保留它的正式类型，而不把八个地点全部写成同质“基地中心”。

USO 官方 admissions policy 表明 center 的主要使用者包括：

- 现役人员；
- Reserve 和 National Guard；
- 持有效证件的 dependents；
- 其他政策列明的退休人员、Gold Star Families 等有限群体。

因此现有 target label“现役人员、预备役／国民警卫队、配偶及家属”是安全的核心概括，但不是完整 admissions policy 枚举。

### 辅助建议

**`accept`。**

数据结构保持：

- 只保留一条 `USO Okinawa → eligible military community` 的 consolidated service relation；
- 8 个地点保留为 8 条 site/function observations；
- Area Office 的 `facility_type` 与普通 center 分开；
- `financial_inference_allowed=no`；
- `political_stance_inference_allowed=no`。

安全措辞：

> USO Okinawa 在其 2026 年公开页面列出 8 个冲绳地点／服务节点，并向符合 USO admissions policy 的现役、Reserve、Guard 人员及军属等提供服务。

不得写：

- USO 因在基地设点而支持某项基地政策；
- 接受服务等于组织成员关系；
- 八个地点代表八个独立组织；
- 服务对象向 USO 提供资金。

## 3. HR-018-18 · MBC→USO Okinawa

S097 和现行 sponsor page 均把 `MBC` 放在 `USO Okinawa Platinum Sponsors` 下。USO 的 MBC 详情页写明：

- `MBC Okinawa is a proud USO Okinawa sponsor`；
- 地点在 Kadena Air Base Building 403；
- 关联官网为 `mbcokinawa.net`。

USO 的感谢页进一步把 MBC 展开为 `Mediatti Broadband Communications, Inc.`，并说明其支持包括：

- cash contributions；
- 向冲绳各 USO center 提供高速网络、Wi-Fi 和 HD 电视；
- 免费技术支持和网络管理。

该页面还称 2025 年是连续第 11 年 Platinum sponsorship。这可以确认主体 crosswalk 和长期赞助性质，但没有逐年金额或现金／实物拆分。

### 辅助建议

**`accept`。**

安全字段：

- source entity canonical display：`Mediatti Broadband Communications, Inc. (MBC Okinawa)`；
- relation type：`sponsorship`；
- tier：`USO Okinawa Platinum Sponsor`；
- public observation time：至少标记 `observed_2026-07-11`，并可记录 2026-07-20 live recheck；
- financial semantics：`sponsor_tier_and_support_types_no_amount`。

限制：

- 不根据 Platinum tier 估算金额；
- 不把免费网络服务折算成市场价值；
- 不把“现金＋实物支持”的概括生成两条带金额 funding edge；
- 不从赞助推断 MBC 对基地政策、军队行动或地方政治的立场。

## 4. HR-018-19 · Matson→USO

S097 与现行 sponsor page 把 Matson 放在：

> USO Indo-Pacific Mission Partners

Matson 的 USO 详情页又明确写：

> Matson is a proud USO Indo-Pacific sponsor.

因此赞助关系成立，但其正式范围是 USO Indo-Pacific，而不是来源明确证明的“Matson 向 USO Okinawa 本地项目定向拨款”。USO Okinawa 页面可以证明该 regional partner 在本地页面展示并与本地区有关联，不能证明本地 amount allocation。

### 辅助建议

**`revise`。**

建议修订：

- relation target 从仅写 `USO Okinawa` 改为 `USO Indo-Pacific`；
- local context 另存 `listed_on_USO_Okinawa_sponsor_page`；
- event/program 改为 `Matson — USO Indo-Pacific Mission Partner`；
- financial semantics 保持 `sponsor_tier_no_amount_or_local_allocation`；
- F035 不删除，但改为 regional sponsor relation；若图只画冲绳直接支持边，应排除或用区域外围样式。

这项 `revise` 是范围校正，不是否定 Matson 的 sponsor 身份。

## 5. HR-018-20 · ACGO→AWWA 历史成员关系

现有三条材料可以确认历史身份和历史 membership：

- S072 的 2012 AWWA 40 周年报道把 ACGO 列为五个 military spouse organizations 之一；
- S094 的 2015 捐赠报道再次列出相同五个 spouse clubs；
- S081 把 Army on Okinawa Gift Shop 写为由 Army Community Group of Okinawa 运营。

这足以证明 ACGO 不是从礼品店名称推出来的虚构主体，并能支持至少 2012、2015 两个历史时点的 AWWA membership。

但是，NOSCO 的现行 AWWA 页面把现有成员列为：

- NOSCO；
- KOSC；
- MOSC；
- OESC。

其中不含 ACGO。公开二手学术材料提出 ACGO 于 2018 年退出，但本批没有找到足以冻结精确退出日期的 primary record，因此不把 2018 直接写成正式 `valid_to`。

### 辅助建议

**`revise`。**

建议修订：

- relation type 仍为 `network_membership`；
- temporal status 改为 `historical_membership`；
- `observed_active_at=2012;2015`；
- `current_status=not_listed_on_current_AWWA_member_page`；
- `valid_to` 暂空，不推定 2018；
- X017 保留为历史／provisional organization node，不因这一 relation 自动进入中央 actor registry；
- 删除 `needs_local_retrieval=yes`：本关系的历史成员判断在线已足够，只有精确退出日仍 unresolved。

限制：

- membership 不是 AWWA→ACGO 或 ACGO→AWWA 的资助；
- ACGO 运营礼品店不等于全部商店收益都进入 AWWA；
- 不把历史成员关系画成当前网络；
- 不因 ACGO 当前不在名单中就判断其已解散；“退出／未列名”与“组织解散”是不同状态。

## 6. HR-018-23 · AWWA→よみたん救護園

S094 是 2015-12-02 的 DVIDS 事件报道。它明确提供：

- donor：American Women’s Welfare Association；
- recipient：文中写作 Yomitan Quegoen／Kyugoen；
- item：wheelchair accessible van；
- item value：2,000,000 円；
- place：Yomitan Village；
- recipient function：为身心障碍成年人提供照护和交通。

日方官方设施页确认正式名称是：

> よみたん救護園

地址为读谷村字都屋 167，运营法人是：

> 社会福祉法人沖縄県社会福祉事業団

因此英文 Quegoen/Kyugoen 是对“救護園”的不稳定罗马字／拼写，不应继续作为 canonical target name。

### 辅助建议

**`revise`。**

建议修订：

- target display 改为 `よみたん救護園`；
- target type=`welfare_facility`；
- operator crosswalk=`社会福祉法人沖縄県社会福祉事業団`；
- event date=`2015-12-02`；
- relation type=`in_kind_donation`；
- amount observation=`2,000,000 JPY item_value_not_cash`；
- event evidence 保持 E3；日方官方页只把 recipient identity crosswalk 提高到 E4，不把捐赠事件整体改成 E4。

这条有界实物捐赠事件可以接受，无须当地资料；但不得写成：

- AWWA 向运营法人支付 2,000,000 円现金；
- 车辆采购价、到账额或会计确认额；
- 对该设施的长期资助关系；
- AWWA 与日方福利机构之间的政治联盟。

## 7. HR-018-24 · AWWA→うるま市社会福祉協議会

S072 的 2012 报道说 AWWA 为 `Uruma City Social Welfare Meeting` 提供一辆 wheelchair accessible van，并说明该设施向老人提供日常活动、约 300 人每日使用。Kadena Air Base 官方照片说明也把这辆车称为 AWWA 捐赠给该老人照护设施的无障碍车辆。

现行日方正式法人名称是：

> 社会福祉法人うるま市社会福祉協議会

英文 `Social Welfare Meeting` 是对 `社会福祉協議会` 的错误直译；标准含义应为 Social Welfare Council。当前材料没有点名具体哪个下属日间活动设施实际保管／使用该车。

### 辅助建议

**`revise`。**

建议修订：

- target display 改为 `社会福祉法人うるま市社会福祉協議会`；
- target ID 可继续使用 provisional `R_uruma_social_welfare`，不自动进入 actor registry；
- `specific_recipient_facility=unresolved`；
- relation type 保持 `in_kind_donation`；
- event time 只写 `2012` 或 `reported_at_2012-04-23`，不把报道日期强行当成交付日；
- amount 继续为空；
- evidence 保持 E3。

限制：

- 不补写车辆价值；
- 不把约 300 人／日解释成受赠人数或网络规模；
- 不把受赠法人误写成“うるま市政府”；
- 不从单次车辆捐赠推断长期资助或稳定联盟。

## 8. HR-018-21 / 22 暂缓记录

本批不对以下两项提出 `accept/revise/reject`：

| item | 暂缓原因 | 当前可保留状态 |
|---|---|---|
| HR-018-21 | 102,000 美元是 scholarships＋AWWA 混合口径；拆分需要 KOSC 年报／Form 990 或等价内部记录 | `deferred_local_or_internal_record`；不得把全额给 AWWA |
| HR-018-22 | 约 8 亿日元／40 年是跨年度、未逐一列 recipient 的累计报道；年度和 recipient 分解需要年报／Form 990 或当地记录 | `deferred_local_or_internal_record`；只可保留不可分配 aggregate history |

这两项不计入本批建议分布，也不因暂缓而否定现有报道。

## 9. 如负责人确认，本批后续动作

1. HR-018-17、18 回填 `accept=X`。
2. HR-018-19、20、23、24 回填 `revise=X`，写入本报告的 scope、time 和 canonical-name 修订。
3. HR-018-21、22 保持空白判断，标记 `deferred_local_or_internal_record`，不进入本轮合并。
4. S097 继续支持 8 个公开地点和 sponsor tier；服务对象的 admissions policy、MBC 全名与支持类型应先走新 source proposal／source-log 流程。
5. F035 改为 Matson→USO Indo-Pacific regional sponsor relation，本地页面展示另存 context。
6. F024 改为 ACGO→AWWA historical membership；不写精确退出日期，也不标组织解散。
7. F028 校正为 `よみたん救護園`，增加运营法人 crosswalk，2m 仅为实物价值。
8. F029 校正为 `社会福祉法人うるま市社会福祉協議会`，具体下属设施 unresolved，不添加金额。
9. 重新生成 R10 图和 brief 前，先完成本批负责人判断；本报告本身不修改中央表。

## 10. 负责人确认记录

负责人于 2026-07-20 确认本批辅助建议：

- HR-018-17 USO Okinawa→军事人员及军属的服务存在：`accept`；
- HR-018-18 MBC→USO Okinawa：`accept`；
- HR-018-19 Matson→USO：`revise`；
- HR-018-20 ACGO→AWWA：`revise`；
- HR-018-23 AWWA→よみたん救護園：`revise`；
- HR-018-24 AWWA→うるま市社会福祉協議会：`revise`。

负责人同时确认：

- Matson 的 relation target／scope 校正为 USO Indo-Pacific，USO Okinawa 页面只作为本地展示 context；
- ACGO→AWWA 改为 2012、2015 可观察的历史成员关系，不填写未经 primary record 确认的退出年份，也不标记组织解散；
- `よみたん救護園` 和 `社会福祉法人うるま市社会福祉協議会` 使用正式日文名称，前者增加运营法人 crosswalk，后者保留具体下属设施 unresolved；
- 2,000,000 円只作为无障碍车辆的实物价值，其他未公开金额不得补写；
- HR-018-21、22 继续暂缓，不在本轮作 `accept/revise/reject` 判断；
- 本批不直接修改中央 relation 表、funding/support 表、source log、HR CSV、图或 brief，留待主线程统一合并。
