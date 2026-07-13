# QA-R10 交叉复核：行政协作／公开资源候选包

日期：2026-07-13
复核者：独立于 R10 原作者的 AI 交叉复核
范围：`annual_relations_v0.csv`、`mechanism_matrix_v0.csv`、`source_candidates_v0.csv`、`visualization_edges_v0.csv`、两份说明文档。
边界：本次未改主数据、控制文档或原始候选；本文件不是人工复核记录，所有敏感关系仍须人审。

## 1. 总判定

R10 包**不能按现状整体合并**。CSV 在语法层面完整，但关系机制层有 5 行误分类，关系、金额观测与功能证据被混在同一张表，且 `20 条关系` 实际包含平行金额观测和重复功能观测。原包对“项目成本不等于支付额／运动资金”的总体警告是正确的，但若直接用于主关系表或作图，会同时出现以下问题：

1. 把县协作表中明确编码为 `委託` 或 `提案型公募による委託` 的关系误写为 `service`、`non_funding_relation` 或泛化的 `administrative_collaboration`。
2. 把同一关系的政府侧金额、组织侧项目成本和功能说明计算成多条关系。
3. 用 `verified_primary` 表示 AI 看过一手材料；这不是项目 schema 允许的人工复核状态。
4. 图中个别金额虽有官方依据，但其口径不是“完整年度支付额”，不能直接控制线宽。

建议把 R10 重构为三层：

- `administrative_relation`：委托、提案型公募委托、补助、指定角色。
- `amount_observation`：合同额、资金流中的交付对象金额、行政表项目费、组织侧事业费分别记录。
- `function_or_role_evidence`：服务内容、会议事务局、受益对象，不另造资金边。

## 2. 结构检查

机器检查结果：

| 文件 | 数据行 | 列数 | 行宽 | ID | 来源外键 |
|---|---:|---:|---|---|---|
| `annual_relations_v0.csv` | 20 | 18 | 全部一致 | 唯一 | 全部指向 R10S01–R10S10 |
| `mechanism_matrix_v0.csv` | 7 | 8 | 全部一致 | 唯一 | 不适用 |
| `source_candidates_v0.csv` | 10 | 11 | 全部一致 | 唯一 | 不适用 |
| `visualization_edges_v0.csv` | 17 | 12 | 全部一致 | 唯一 | 全部指向 R10S01–R10S10 |

但结构可解析不等于可合并：

- 20 行均写 `E4`，其中 13 行仍为 `needs_human_review`；其余 7 行写 `verified_primary`。统一 schema 没有 `verified_primary`，且本包没有人审记录。应全部先回到 `ai_seeded` 或 `needs_human_review`。
- `partner_actor_id` 只有 X010、A066 被使用；冲绳和平协力中心其实已在 registry 为 A088，却留空。多个 JV、财团和服务组织没有 actor crosswalk。
- `public_actor` 只有名称、没有 ID；JICA 冲绳已在 registry 为 X011。当前方向也与主 `funding_or_support_edges` 中 F031–F033 的 ONC→制度节点方向不一致。
- 日期粒度混用完整日期、月份和空值。R10A007 把 ONC 年报中 `6月–3月` 写成 `2024-04-01–2025-03-31`；R10A020 的 `fiscal_year=2025` 无直接来源。
- `amount_jpy` 同时容纳合同／资金流、行政表项目费和组织侧事业费，单一 `evidence_level` 无法表示“关系已确认，但支付语义未确认”。

## 3. 来源回指与去重

### 已在主 source log，禁止重复新增

| R10 source | 主 source | 处置 |
|---|---|---|
| R10S01 | S002 | 同一 URL。R10S01 的 `new_candidate` 错误；直接回指 S002。年份 2025/2026 的差异需按“材料年度／发布日期／访问年”拆字段，不再造来源。 |
| R10S02 | S099 | 同一 URL；ONC FY2024 法定年报，已归档。 |
| R10S03 | S100 | 同一 URL；JICA 2019 报告，已归档。 |
| R10S04 | S101 | 同一 URL；FY2026 MOFA 名单，主归档因 403 失败。 |

R10S09 是 S095 官方站点的**不同子页面 URL**，不能假称同一来源；若项目要求一 URL 一 source，应作为新来源入表，或明确以 S095 作为站点级来源并保存精确页面 locator。

### 可作为新 source candidate，但先归档

- R10S05、R10S06、R10S07：冲绳市 FY2019、FY2020、FY2024 交付金检证表，均为官方资金流资料。
- R10S08：冲绳县多文化共生会议纪要，支持 ONC 人员作为事务局。
- R10S09：ONC 项目页，支持 KIP 市委托和服务内容；组织自述，不代替支付记录。
- R10S10：冲绳市 KIP 设施页，只支持设施／服务功能；不支持指定年度金额。

还应新增而原包漏掉的关键官方来源：

- 冲绳县 FY2024 第一季度随意合同实绩：`https://www.pref.okinawa.jp/_res/projects/default_project/_page_/001/015/127/koushitsu1.pdf`。PDF 第 1 页确认 A066 合同额 12,842,500 日元；第 2 页确认冲绳和平协力中心两份合同分别为 26,439,000 和 8,479,000 日元。
- 冲绳县 FY2024 NPO 协作调查汇总：`https://www.pref.okinawa.jp/_res/projects/default_project/_page_/001/004/917/2r6kekka.pdf`。PDF 第 2 页给出代码定义：C=1 为 `委託`，C=2 为 `提案型公募による委託`，C=4 为 `補助`。

所有来源在合并前应增加精确 locator（PDF 页码、表号／行号）。当前 `used_for` 只写用途，回指粒度不足。

## 4. 四组重点金额的语义边界

### 4.1 KIP：16.662m vs 16.04m

两数不是同一会计对象，不能称为简单的“行政侧与组织侧差异”：

- 冲绳市 FY2024 检证表（R10S07，PDF 第 5–6 页）列示总事业费 18.858m、交付对象事业费 16.662m、交付对象外经费 2.196m；资金流把 16.662m 标为给 ONC 的 `委託料`，另列 2.196m 的 3 月运营委托费为交付对象外经费。
- ONC 年报（S099，PDF 第 1–2 页）把 KIP `コザインターナショナルプラザ委託管理業務（沖縄市委託）` 的 `事業費` 列为 16.040m。它是组织侧项目成本，不是合同收入或现金到账。

因此：

- 16.662m 可作为 `municipal_eligible_commission_flow`，但**不能标成完整年度委托支付额**。
- 2.196m 必须作为同一市级项目的独立 `non_eligible_commission_observation` 保留；若不展示它，就不能用 16.662m 作为整条边的金额线宽。
- 16.040m 只能作为 `organization_reported_project_cost`；不与 16.662m 或 18.858m 相减来推断利润、漏报或未付款。
- R10A004 的期间是全年，但金额只是交付对象部分，`period` 与 `amount_scope` 必须拆开。

### 4.2 县多文化项目：5.14m vs 5.53m

- S002（PDF 第 59 页）把该行 C 编为 1=`委託`，项目费 J 列为 5.140m，期间为 2024-07-04 至 2025-03-31。
- S099（PDF 第 3 页）明确写 `沖縄県委託`，组织侧 `事業費` 为 5.530m，实施期写 `6月–3月`；财务报表注记（PDF 第 8 页）给出该事业分类成本 5,530,234 日元。

关系本身可确认是 commission，但两数都是不同文件中的项目成本观察，不是已确认合同额。R10A006/R10A007 应合并为**一条关系、两条 amount observations**。R10A007 的 4 月 1 日开始日期应拒绝，等待按年报改为月粒度 `2024-06`，或人审获得合同日期。

### 4.3 MOFA NGO 相談員：2.894m

S099 的事业表（PDF 第 2 页）写明 `NGO相談員（外務省委託）`、期间 `4月–3月`、事业费 `2,894千円`；财务注记（PDF 第 8 页）给出对应事业分类成本 2,894,630 日元。由此可确认：

- FY2024 委托角色：可确认。
- 组织侧项目成本：可确认，若存整数日元应优先保存 2,894,630，并记录业务表为千元显示。
- “MOFA 支付 ONC 2.894m”“合同额 2.894m”或“外务省资助”：均不可确认。

R10A008 不应同时用 FY2026 名单 S101 支持 FY2024 金额。FY2024 关系／成本用 S099；FY2026 指定延续用 S101，二者分开。

### 4.4 A066：12.843m

原包把 A066 编为泛化行政协作、项目费 12.843m，过于保守且机制错误：

- S002（PDF 第 1 页）该行 C=2，按官方代码是 `提案型公募による委託`；J 列 12,843（千日元）是协作调查中的项目费。
- 公募页面的 12,843,000 日元是**提案限度额**，页面明确说与实际合同额不同，不能当 award／contract。
- FY2024 随意合同实绩（上述 `koushitsu1.pdf` 第 1 页）确认实际合同对象为新外交イニシアティブ，合同额 12,842,500 日元。S002 的 12,843 千日元与之只是千元显示上的对应，不应当作精确值。

安全替代是：`relation_type=commission`、`funding_relation_confidence=confirmed_commission`、`contract_amount_jpy=12842500`、合同来源回指 `koushitsu1.pdf`。不得写成 grant、运动资金或无条件行政支持。

## 5. 关系分类错误与替代候选

S002 的 C 列是关系机制，服务内容应放在 `function_layer`。以下 5 行／5 条可视化边应拒绝现状并替换：

| annual row | visual row | 当前分类 | 官方 C 码 | 替代候选 | 金额处置 |
|---|---|---|---:|---|---|
| R10A010 | R10V008 | administrative_collaboration / non_funding visual group | 2 | commission（提案型公募委托） | 12,842,500 为另份官方合同确认额；12.843m 留作千元项目费观察 |
| R10A011 | R10V009 | non_funding_relation | 2 | commission；partner_actor_id=A088 | 25.547m 是协作表项目费；官方合同额 26,439,000，二者分栏 |
| R10A012 | R10V010 | non_funding_relation | 2 | commission；partner_actor_id=A088 | 6.496m 是协作表项目费；官方合同额 8,479,000，二者分栏 |
| R10A014 | R10V012 | service | 1 | commission；function_layer 保留 service | 10.329m 仅项目费，合同／支付待核 |
| R10A016 | R10V014 | service | 2 | commission；function_layer 保留 service/education | 7.171m 仅项目费，合同／支付待核 |

相应地，`mechanism_matrix_v0.csv` 当前计数 11 commission、3 service、3 non-funding、1 generic collaboration 是错误的。按 C 码纠正后，20 条原记录的表面类型应为：16 commission、1 designated role、1 grant、1 non-funding role observation、1 service/function observation。但后两类仍不应都算独立行政关系。

## 6. 重复、冲突与解释越界

### 必须折叠的重复／平行观测

- R10A004 + R10A005：同一 FY2024 KIP 委托；一条 relation、至少三条金额观测（16.662m、2.196m、16.040m）。
- R10A006 + R10A007：同一县多文化委托；一条 relation、两条金额观测（5.140m、5.530m/5,530,234）。
- R10A019：同一多文化项目中 ONC 人员担任事务局的角色证据，宜附着于上述 relation，不再造一条网络边。
- R10A020：KIP 服务功能说明，应附着于 KIP program/function；来源不支持 `fiscal_year=2025`，不能作为独立年度边。
- R10A005、R10A007、R10A008、R10A009 与主表 F033、F032、F031 已有明显重叠；只能补充证据／金额观测，不新增平行主边。

因此，说明文档中的“20 条年度／项目关系”应改为“20 条关系、金额与功能观测”；在折叠前不能声称有 20 条独立关系。

### 目前没有越界、可保留的解释

- 委托不是 grant，更不是反基地运动资金。
- 服务组织不因服务对象或行政角色被推断政治立场。
- 共同出现于县协作表不构成组织间联盟。
- whole project cost、organization project cost 和合同／支付额不可相加或平均。

### 应拒绝的解释／展示

- 把 16.662m 作为 FY2024 KIP 完整支付额控制线宽，而不同时处理 2.196m。
- 把 5.14m、5.53m、2.894m、17.932m 或县协作表其他 J 列金额称为已支付给组织的款项。
- 把 A066 12.843m 写成 grant、补助或“运动资金”；也不能把公募上限冒充合同额。
- 把 R10A011/R10A012 继续画成 non-funding 共同实施；官方材料已经确认委托机制和合同。
- 用 `verified_primary` 冒充人审，或让 E4 同时替关系强度和金额支付语义背书。

## 7. 合并分级

### 可安全合并项（仅候选／来源层，不等于可发布人审结论）

1. R10S01–R10S04 按 S002/S099/S100/S101 去重回指。
2. R10S05–R10S10 作为官方／组织来源候选入 source log，状态保持 `ai_seeded`，先归档并加 locator。
3. R10A001 的 JICA→ONC 受托角色（无金额）；公共节点应 crosswalk 到 X011。
4. R10A002、R10A003 的 KIP 2019/2020 官方资金流委托费；金额分别为 17,157,000、16,970,000，需保持“公共设施运营委托、非运动资金”。
5. R10A004 的 FY2024 KIP 委托关系本身；16.662m 只能以 `eligible commission flow` 金额观测合并。
6. R10A005、R10A007、R10A008、R10A009 作为 F033/F032/F031 的证据或时间延续补充，不新增边。
7. A066、A088 两组官方合同记录可进入“确认委托”候选；先由人工核对来源、actor crosswalk 和方向。

项目硬规则要求进入分析结论的敏感关系有人审，所以本包当前**没有任何一行可直接改成 `human_checked` 并发布**。

### 必须人工复核项

1. KIP 18.858m 总事业费、16.662m 交付对象委托费、2.196m 交付对象外 3 月委托费与 ONC 16.040m 项目成本的合同期／交付金范围／会计口径。
2. 县多文化项目 5.140m 与 5.530m/5,530,234 的期间差异（7 月 4 日 vs 6 月）及合同额。
3. MOFA FY2024 合同／支付记录；在取得前只保留委托角色和组织侧项目成本。
4. R10A013–R10A018 的 JV、财团、协会 actor 身份与 ID；复合受托体不能把总额拆给成员。
5. 主关系表的方向政策：公共机构→受托者，还是 actor→制度／项目节点；不得并存两套方向制造重复。
6. R10A019、R10A020 是否只进入 function/venue 层；R10A020 的时间字段应删除或补源。
7. 所有 `verified_primary` 改为 schema 状态并纳入正式 human review log。

### 应拒绝项（按现状）

- R10A010–R10A012、R10A014、R10A016 及对应 V008–V010、V012、V014 的关系分类。
- R10A007 的 `period_start=2024-04-01`。
- R10A020 的 `fiscal_year=2025` 和作为独立关系边的用法。
- R10S01 的 `new_candidate` 状态。
- 说明文档的“20 条独立关系”口径和未纠正的五类机制计数。
- R10M04 把 UNC／教育项目的 service 当成资金机制，R10M05 以和平协力中心两行作为 non-funding 示例，R10M07 以 A066 作为非委托的泛化协作示例。

本轮没有生成 `corrected_*` CSV：错误涉及关系实体、金额观测和功能证据的拆表及与主表去重，未完成人审前直接复制一份“修正版”会制造第二套伪最终数据。上面的替代候选足以供主线程重建。

## 8. done_when

R10 只有同时满足以下条件才可标记完成：

1. R10S01–R10S04 完成主 source ID 去重；R10S05–R10S10 和两份新增县官方材料完成归档与页码 locator。
2. 数据拆成 relation、amount observation、function/role evidence 三层，或等效地增加稳定主键与 `observation_type`，确保同一项目只计一条关系。
3. 按官方 C 码纠正 5 行关系类型；A088、X011 与其他 actor/JV 完成 crosswalk。
4. KIP FY2024 图不再把 16.662m 当完整年度支付；A066 与和平协力中心使用合同额时明确 contract basis。
5. MOFA 2.894m、县 5.14m/5.53m 均只作项目成本观察，除非补到合同／付款记录。
6. 复算机制计数和唯一关系数，重写 brief 与 visualization sketch；图的金额线宽只使用 `confirmed_contract_amount` 或定义清楚的 `documented_recipient_flow`。
7. 与 F031–F033 去重，确定统一边方向；R10A019/R10A020 不再制造重复金融边。
8. 人工复核写入正式 log；最终表只使用项目 schema 允许的 review status。

在此之前，R10 的安全结论只能是：公开材料确认多种行政委托、指定和补助角色；不同文件的项目费、组织侧成本、合同额和资金流金额必须分层，不能投影成统一“资助网络”。
