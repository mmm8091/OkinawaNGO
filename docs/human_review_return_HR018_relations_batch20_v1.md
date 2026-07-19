# HR-018 行政协作关系回交报告 Batch 20

日期：2026-07-20  
承办人：项目负责人  
辅助核查：Codex  
来源队列：`outputs/R10_administrative_collaboration_v0/HR018_relation_review_v0.csv`  
本批范围：HR-018-09–16  
状态：**负责人已确认——6 项 accept，HR-018-11、13 revise**

## 0. 批次边界

- 本批逐项复核 8 条冲绳县→组织／项目联合体的委托或补助关系。
- `accept` 只表示接受 relation observation 的方向、对象、项目范围、来源和解释边界；`revise` 表示关系可以保留，但至少一个字段需要按新证据修订。
- 官方协作表中的 `事業費`、企划征集上限、初始预算、合同金额、补助决定额和实际支付额必须分开。
- 共同企业体只作为项目期复合主体；成员说明不等于稳定组织联盟，也不能把联合体总金额分配给成员。
- 本批组织或成员的 wider registry crosswalk 仍由 HR-032 决定；接受本批 relation 不自动新增中央 actor。
- S002 的协作形态代码是该调查表的官方分类。若合同公开表另记 proposal 选定程序，应把两种来源特定字段并存，不静默改写 S002。
- 行政协作、国际交流或和平教育项目不等于反基地政治立场、稳定联盟或运动资金。
- 本批不需要当地资料。
- 本报告不直接修改中央 relation 表、funding/support 表、source log、HR CSV、图或 brief。

## 0A. 本轮调查与视觉核查

| 项目 | 核查材料 | 本轮调查所得 |
|---|---|---|
| HR-018-09 / 10 | S002 PDF p.2 rows 10–11；S184 PDF p.2 rows 11–12；S104、S231、S232 | 视觉核查确认两个项目均点名 A088 正式法人名，均为 C2；S002 的 25,547 千円和 6,496 千円是 `事業費`。S184 分别记录两份独立合同，合同额为 26,439,000 円和 8,479,000 円。 |
| HR-018-11 | S002 PDF p.59 row 432；[冲绳县 FY2024 文化观光体育部随意合同公开表](https://www.pref.okinawa.lg.jp/_res/projects/default_project/_page_/001/011/879/r6_1zuiikei2.pdf) No.91；[企划征集要领](https://www.pref.okinawa.jp/_res/projects/default_project/_page_/001/028/661/r6_boshu.pdf) | S002 确认 C2、项目期、21,799 千円事业费及两名 JV 成员。新增官方合同表确认 2024-05-15、合同额 27,199,000 円、同名 JV 及相同成员；因此 current `project_cost_only` 已不完整。 |
| HR-018-12 | S002 PDF p.59 row 433；[官方企划提案要领](https://www.pref.okinawa.jp/_res/projects/default_project/_page_/001/027/902/01youryou.pdf)；[WYUA 组织页](https://wyua.okinawa/organization/) | 正式法人名、项目实施、期间和 C1 均可确认。10,329,000 円在征集文件中明确是提案用上限且“与实际合同金额不同”；S002 同额字段仍是事业费，不能升级为实际合同额。 |
| HR-018-13 | S002 PDF p.60 row 434；[冲绳县 FY2024 文化观光体育部随意合同公开表](https://www.pref.okinawa.lg.jp/_res/projects/default_project/_page_/001/011/879/r6_1zuiikei2.pdf) No.90 | S002 确认 Team OKIYUA、两名成员、C1、项目期和 39,739 千円事业费。新增合同表确认 2024-04-01 实际合同 37,220,999 円，并说明经两家应募的 proposal 审查选定；因此需要新增合同金额，同时保留 S002 的 C1 来源分类。 |
| HR-018-14 | S002 PDF p.60 row 435；[JICA 对 JOCA 冲绳事务所的官方介绍](https://www.jica.go.jp/domestic/okinawa/activities/kaihatsu/festival/2021/organization_02/02.html) | S002 确认 C2、项目期、7,171 千円事业费和受托单位。官方介绍确认“青年海外协力协会冲绳事务所”是 JOCA 的冲绳事务所，而不是另一个独立法人。本轮未找到实际合同额。 |
| HR-018-15 | S002 PDF p.60 row 436 | 视觉核查确认 C2、项目期、15,442 千円事业费、JV 名称以及 JOCA 冲绳事务所、东武トップツアーズ冲绳支店两名成员。本轮未找到实际合同额。 |
| HR-018-16 | S002 PDF p.60 row 437；[冲绳县 FY2024 施策检证表](https://www.pref.okinawa.jp/_res/projects/default_project/_page_/001/034/310/r5_4-2omonatorikumibunsupo.pdf)；[财团官网](https://www.oihf.or.jp/) | S002 的项目叙述明确说向 OIHF 的国际交流・协力事业经费“交付补助金”，足以确认 grant relation；17,932 千円仍只是 S002 事业费。另一官方表给出同名项目 FY2024 初始预算 21,127 千円，但这也不是补助决定额或实际支付额。 |

视觉核查文件保存在 `tmp/pdfs/hr018_batch20/`，仅作工作底稿，不是正式来源。

## 1. 辅助建议总表

| review item | relation | 辅助建议 | 可批准的最强口径 | 必须保留的边界 |
|---|---|---|---|---|
| HR-018-09 | 冲绳县→A088，“和平之思”传播・交流・传承 | `accept` | C2 委托；实际合同 26,439,000 円 | 25.547m 是事业费；与 HR-018-10 是两份独立合同 |
| HR-018-10 | 冲绳县→A088，冲绳战讲述者培养 | `accept` | C2 委托；实际合同 8,479,000 円 | 6.496m 是事业费；与 HR-018-09 是两份独立合同 |
| HR-018-11 | 冲绳县→国际协力人才培养事业 JV | `revise` | C2 委托；实际合同 27,199,000 円 | 21.799m 是事业费；JV 为项目复合主体；合同额不得拆给成员 |
| HR-018-12 | 冲绳县→WYUA，UNC 运营 | `accept` | 委托关系、对象、期间和 S002 C1 成立 | 10.329m 是事业费／提案上限，不是实际合同额；registry crosswalk 留给 HR-032 |
| HR-018-13 | 冲绳县→Team OKIYUA，留学生接收 | `revise` | 委托关系；实际合同 37,220,999 円 | 39.739m 是事业费；C1 是 S002 分类，proposal 是合同采购程序；不得拆额 |
| HR-018-14 | 冲绳县→JOCA 冲绳事务所，Let's Study! | `accept` | C2 委托关系、期间和教育功能成立 | 7.171m 只是事业费；事务所不是独立法人；registry crosswalk 留给 HR-032 |
| HR-018-15 | 冲绳县→Uchina Junior Study JV | `accept` | C2 委托关系、期间、JV 和成员构成成立 | 15.442m 只是事业费；JV 为项目复合主体；不得拆额 |
| HR-018-16 | 冲绳县→OIHF，国际交流・协力推进 | `accept` | C4 补助关系成立 | 17.932m 是事业费；21.127m 是初始预算；均不是 award 或 paid amount |

建议分布：

- `accept`：6 条；
- `revise`：2 条；
- `reject`：0 条。

## 2. HR-018-09 / 10 · 冲绳县→A088，两项和平教育委托

### 身份与 relation crosswalk

S002 和 S184 都使用“特定非营利活動法人沖縄平和協力センター”。这与 A088 的 canonical name 一致；S104 的官方 NPO 门户记录，以及 S231、S232 的 JICA 官方伙伴／项目页进一步支持该法人身份。因此本批的 relation target 可以交叉映射到 A088，不需要另建相似名称 actor。

这只确认行政项目相手方身份。A088 仍应按已观察到的和平教育、human security 和国际协力功能编码，不能因组织名称或两项县委托推断反基地或亲基地立场。

### 两份合同必须分开

S002 p.2 分别记录：

- row 10：“平和への思い”発信・交流・継承事業，C2，2024-06-12–2025-03-14，事业费 25,547 千円；
- row 11：沖縄戦の語り継ぎ手養成事業，C2，同一期间，事业费 6,496 千円。

S184 p.2 又分别记录：

- No.11，合同日 2024-06-12，合同额 26,439,000 円；
- No.12，合同日 2024-06-12，合同额 8,479,000 円。

两行拥有不同合同名称、编号和金额。相同相手方、合同日与履行期不能成为合并理由。

### 辅助建议

**HR-018-09=`accept`；HR-018-10=`accept`。**

安全措辞：

> 冲绳县在 FY2024 分别与 A088 冲绳和平协力中心签订“和平之思”传播・交流・传承事业和冲绳战讲述者培养事业委托合同，合同额分别为 26,439,000 円和 8,479,000 円。

合并边界：

- 25,547,000 円和 6,496,000 円保留为 S002 `whole_program_project_cost`；
- 26,439,000 円和 8,479,000 円保留为 S184 `confirmed_contract_amount`；
- 不相加、不替代、不解释差额；
- 两条 relation 不合并，也不从两个同年度合同推断长期独家合作。

## 3. HR-018-11 · 冲绳县→国际协力人才培养事业共同企业体

S002 row 432 确认：

- 正式项目展示名为 `令和６年度おきなわ国際協力人材育成事業共同企業体`；
- 成员为公益社团法人青年海外协力协会冲绳事务所和冲绳 JTB 株式会社；
- 协作形态为 C2；
- 期间为 2024-05-15–2025-02-28；
- 事业费为 21,799 千円。

新增官方随意合同公开表 No.91 又确认：

- 合同名称为 FY2024 冲绳国际协力人才培养事业委托业务；
- 合同日为 2024-05-15；
- 合同相手方为同名共同企业体；
- 两名成员与 S002 一致；
- 合同额为 27,199,000 円；
- 经 proposal 公募，一家应募者通过审查被选定。

企划征集文件允许由多个法人组成共同企业体，并要求设管理法人，但公开合同表未把合同金额拆给成员。因此 JV 是本合同的相手方，应保留为项目复合主体。

### 辅助建议

**`revise`。**

建议修订：

1. relation 本身保留；
2. `current_financial_semantics` 从 `commission_relation_project_cost_only` 改为能同时表达项目费与实际合同额的语义，例如 `confirmed_contract_plus_project_cost`;
3. 新增 27,199,000 円 `confirmed_contract_amount`；
4. 原 21,799,000 円继续标记 `whole_program_project_cost_not_actor_payment`；
5. source refs 增加 FY2024 文化观光体育部随意合同表；该 URL 须先走 source-log proposal／归档流程，不能在合并脚本中临时使用裸 URL；
6. JV 只进入 project-composite 层；JOCA 冲绳事务所和冲绳 JTB 只进入 `member_of_composite` 说明层；
7. 两个金额都不得拆分或复制到成员节点。

这里的 `revise` 不是否定关系，而是新官方合同证据使原来的“只有项目费”语义不再完整。

## 4. HR-018-12 · 冲绳县→世界若者ウチナーンチュ连合会

WYUA 官方组织页确认：

- 法人正式名称为 `一般社団法人世界若者ウチナーンチュ連合会`；
- 英文名为 `World Youth Uchinanchu Association`；
- 法人设立于 2015-07-17，前身任意团体成立于 2011-10-14；
- 组织具有持续性，不是为 FY2024 单一项目临时组成的 JV。

S002 row 433 点名该一般社团法人运营 UNC 平台，协作形态为 C1，期间为 2024-04-01–2025-03-31，事业费为 10,329 千円。官方企划提案要领进一步说明：

- 通过企划竞赛选择受托者后签订随意合同；
- 10,329,000 円只是提案估价上限；
- 文件明确说明该金额与实际合同金额不同。

所以 C1 是 S002 调查表的来源特定分类；proposal selection 是采购程序的补充信息。二者可以并存，不能因为后者而静默把 S002 原始代码改成 C2。

### 辅助建议

**`accept`。**

限制：

- relation type 保持 `commission`，平台运营留在功能层；
- 10,329,000 円只保留为 S002 事业费；征集文件中的同额上限不创建第二个金额；
- 不写 actual contract amount、award、payment 或 organization income；
- 本批可以接受 source label 对应同一正式法人，但是否进入中央 actor registry、以及 row 433/434/571 的 wider crosswalk，继续由 HR-032 决定；
- 不从 Uchinanchu 网络服务推断政治立场或运动关系。

## 5. HR-018-13 · 冲绳县→Team OKIYUA

S002 row 434 把 Team OKIYUA 明确列为 JV，并在同一 source cell 中列出：

- 株式会社沖縄映像センター；
- 一般社団法人世界若者ウチナーンチュ連合会。

S002 的协作形态为 C1，期间为 2024-04-01–2025-03-31，事业费为 39,739 千円。

新增官方随意合同公开表 No.90 确认：

- 合同相手方为 Team OKIYUA；
- 两名成员与 S002 一致；
- 合同日为 2024-04-01；
- 实际合同额为 37,220,999 円；
- 两家应募者经 proposal 审查后选定该合同相手方。

S002 C1 与合同公开表的 proposal 程序看似不一致，但它们回答不同问题：前者是 NPO 协作调查的机制代码，后者是合同采购／选定程序。除非项目以后决定统一重编码所有 S002 机制，否则应保留两个来源特定字段。

### 辅助建议

**`revise`。**

建议修订：

1. relation 本身保留；
2. `current_financial_semantics` 从 `commission_relation_project_cost_only` 改为 `confirmed_contract_plus_project_cost` 或等价受控值；
3. 新增 37,220,999 円 `confirmed_contract_amount`；
4. 39,739,000 円继续作为 S002 `whole_program_project_cost_not_actor_payment`；
5. source refs 增加官方随意合同表，并先走 source-log proposal／归档流程；
6. `official_collaboration_mechanism_code=C1` 与 `procurement_method=proposal_based_discretionary_contract` 分字段并存；
7. Team OKIYUA 只作为项目期复合主体，不进入稳定 actor 层；
8. 合同额和事业费都不得拆给沖縄映像センター或 WYUA，也不得据共同投标／履约推断长期联盟。

## 6. HR-018-14 / 15 · JOCA 冲绳事务所及相关 JV

### HR-018-14

S002 row 435 确认：

- target 为 `公益社団法人青年海外協力協会沖縄事務所`；
- 项目为 Let's Study! Uchina Network；
- 协作形态 C2；
- 期间为 2024-05-24–2025-02-28；
- 事业费为 7,171 千円。

JICA 官方介绍把它写作公益社团法人青年海外协力协会（JOCA）的冲绳事务所，并介绍其国际理解、研修、和平与 SDGs 教育功能。它是真实、持续的地区办事机构，但不是与 JOCA 母法人平行的另一个法人。

### HR-018-15

S002 row 436 确认：

- target 为 FY2024 Uchina Junior Study 事业共同企业体；
- 成员为 JOCA 冲绳事务所和东武トップツアーズ株式会社冲绳支店；
- 协作形态 C2；
- 期间为 2024-04-30–2025-02-28；
- 事业费为 15,442 千円。

本轮对官方合同公开表和精确名称／金额进行了在线检索，但没有找到足以把 7,171,000 円或 15,442,000 円升级为实际合同额的记录。没有找到不等于合同不存在，只表示当前证据边界仍是 S002 事业费。

### 辅助建议

**HR-018-14=`accept`；HR-018-15=`accept`。**

边界：

- HR-018-14 target 在 module 内可以显示为 JOCA 冲绳事务所，但法人层归属于 JOCA；wider member crosswalk 留给 HR-032；
- HR-018-15 target 是项目 JV，成员只进入 `member_of_composite` 层；
- 7,171,000 円和 15,442,000 円都标 `whole_program_project_cost_not_actor_payment`；
- 不创建合同金额、付款额或成员收入；
- 教育、国际理解和交流活动只进入功能层，不推断稳定组织联盟或政治立场。

## 7. HR-018-16 · 冲绳县→OIHF 国际交流・协力推进事业

S002 row 437 同时提供：

- target 为公益财团法人冲绳县国际交流・人才育成财团；
- 协作形态 C4；
- 期间为 2024-04-01–2025-03-31；
- 事业费为 17,932 千円；
- 叙述明确说明对该财团实施国际交流・协力事业所需经费“交付补助金”。

因此补助关系本身不是从数字或组织名称推出来的，而是由官方机制代码和点名叙述直接支持。

补充官方施策检证表把同名 `沖縄県国際交流・協力推進事業費補助金` 的 FY2024 初始预算列为 21,127 千円。该表还说明 FY2023 决算见込为 18,856 千円，并把财团列为实施主体。它能加强项目连续性和预算背景，但 FY2024 的 21,127,000 円仍是初始预算，不是对财团的最终交付决定、结算或到账证明。

### 辅助建议

**`accept`。**

安全措辞：

> 冲绳县 FY2024 官方协作表确认向 OIHF 的国际交流・协力推进事业经费提供补助；公开材料中的 17,932,000 円是协作表事业费，21,127,000 円是同名项目初始预算，当前均不作为 award amount 或 paid amount。

合并边界：

- relation type=`grant`、mechanism=`C4;補助` 可以批准；
- 17,932,000 円继续标 `whole_program_project_cost_not_award`；
- 21,127,000 円如以后进入 amount observation，只能标 `initial_budget_not_award_or_payment`，且须先完成新 source 入表；
- 在获得补助决定通知、交付额清单、决算或财团财务记录前，不建立 award-sized funding edge；
- 财团身份可确认，但是否作为中央 actor 及其跨项目 alias 处理仍留给 HR-032。

## 8. 复合主体与 crosswalk 的统一处理

本批建议冻结以下三层，不混用：

| 层 | 对象 | 允许表达 | 禁止表达 |
|---|---|---|---|
| persistent organization / office | A088、WYUA、JOCA／冲绳事务所、OIHF | 正式身份、办事机构归属、单独受托／受补助关系 | 未经 HR-032 自动新增 actor 或扩展所有别名 |
| project composite | 国际协力人才培养 JV、Team OKIYUA、Uchina Junior Study JV | 某项目期的合同相手方、正式成员构成 | 永久 actor、稳定联盟、跨项目自动延续 |
| member-of-composite | 各 JV 成员 | “成员参与该项目复合体” | 把 JV 的合同额、事业费、政策立场或全部功能复制给成员 |

这一处理允许后续解释“同一组织以独立受托者或 JV 成员进入行政项目”的现象，但不会把项目联合体误画成长期组织网络。

## 9. 如负责人确认，本批后续动作

1. HR-018-09、10、12、14、15、16 回填 `accept=X`。
2. HR-018-11、13 回填 `revise=X`，并写入上述 revision instructions。
3. HR-018-11 新增实际合同金额 27,199,000 円；HR-018-13 新增实际合同金额 37,220,999 円。
4. 两条新增合同来源先进入 source proposal、source log 和 archive，再供中央 relation／amount 表引用；来源入表不扩大 claim approval。
5. 保留所有 S002 `事業費` 为 project-cost 观察，不覆盖、不相加，也不解释与合同额之间的差额。
6. HR-018-12、13 的 C1 调查代码与 proposal procurement 信息分字段保存，不做静默机制覆盖。
7. 三个 JV 进入 project-composite 层，成员进入 member-of-composite 层；不新增成员资金边。
8. A088 crosswalk 可在本批 relation 层确认；JOCA、WYUA、OIHF 的 wider actor／alias crosswalk 仍交 HR-032。
9. 重新生成 R10 关系表、金额边界图和 brief 前，先完成本批负责人判断；本报告本身不执行合并。

## 10. 负责人确认记录

负责人于 2026-07-20 确认本批辅助建议：

- HR-018-09 冲绳县→A088，“和平之思”传播・交流・传承：`accept`；
- HR-018-10 冲绳县→A088，冲绳战讲述者培养：`accept`；
- HR-018-11 冲绳县→国际协力人才培养事业 JV：`revise`；
- HR-018-12 冲绳县→WYUA，UNC 运营：`accept`；
- HR-018-13 冲绳县→Team OKIYUA，留学生接收：`revise`；
- HR-018-14 冲绳县→JOCA 冲绳事务所，Let's Study!：`accept`；
- HR-018-15 冲绳县→Uchina Junior Study JV：`accept`；
- HR-018-16 冲绳县→OIHF，国际交流・协力推进：`accept`。

负责人同时确认：

- HR-018-11 新增 27,199,000 円实际合同额，HR-018-13 新增 37,220,999 円实际合同额；
- 两条原有 S002 事业费继续作为独立 project-cost 观察，不覆盖、不相加，也不解释与合同额之间的差额；
- 三个 JV 仅作为项目复合主体，成员关系仅进入 `member_of_composite` 层，任何金额均不得拆给成员；
- S002 的 C1/C2 调查代码与合同采购程序分字段保留；
- 本批不直接修改中央 relation 表、funding/support 表、source log、HR CSV、图或 brief，留待主线程统一合并。
