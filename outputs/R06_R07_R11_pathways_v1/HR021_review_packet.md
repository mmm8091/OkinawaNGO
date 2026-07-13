# HR-021：R6/R7/R11 下游纳入与 analytical seed 复核包

前 7 项均为 `dependent_on_hr018`：HR-018 负责关系事实判断，HR-021 只在对应 HR-018 项 accept/revise 后决定是否及以何种边界进入 R6/R11。前置复核未完成时不得填写决定。

前 7 项决定选项为 include_after_hr018 / revise_scope_after_hr018 / exclude。第 8 项只审 analytical seed 是否有独立事实边证据。所有决定栏保持空白。

## HR021-001 · R10R001

- 依赖类型：dependent_on_hr018
- HR-018 前置项：HR-018-01；状态：pending_hr018_completion
- 问题：After HR-018 accepts or revises R10R001, should the resulting relation enter the R6 administrative comparison and R11 matrix, and with what no-public-amount boundary?
- 来源：S100；定位：PDF p.103
- 影响：R6 administrative comparison; R11 administrative entry matrix
- 默认边界：受托角色可确认；没有公开合同金额，不推定资金规模。
- 决定选项：include_after_hr018|revise_scope_after_hr018|exclude

## HR021-002 · R10R004

- 依赖类型：dependent_on_hr018
- HR-018 前置项：HR-018-04；状态：pending_hr018_completion
- 问题：After HR-018 accepts or revises R10R004, should the resulting relation enter R11, and how must the 16.662m flow, 2.196m observation and 16.040m project cost remain separated in that downstream scope?
- 来源：R10S07;S099;R10S09;R10S10；定位：R10S07 PDF pp.5-6; S099 PDF pp.1-2
- 影响：R11 administrative/service entry
- 默认边界：16.662m 只是交付对象部分；2.196m 与 ONC 16.040m 必须作为不同金额口径保留。
- 决定选项：include_after_hr018|revise_scope_after_hr018|exclude

## HR021-003 · R10R005

- 依赖类型：dependent_on_hr018
- HR-018 前置项：HR-018-05；状态：pending_hr018_completion
- 问题：After HR-018 accepts or revises R10R005, should the resulting relation enter R11, and should its downstream scope remain administrative support without movement-funding inference?
- 来源：S002;S099;R10S08;R10S12；定位：S002 PDF p.59 row 431; S099 PDF pp.3,8; R10S12 PDF p.2
- 影响：R11 administrative entry
- 默认边界：5.140m 与 5,530,234 都是项目成本观察，不是确认合同支付额。
- 决定选项：include_after_hr018|revise_scope_after_hr018|exclude

## HR021-004 · R10R006;R10R007

- 依赖类型：dependent_on_hr018
- HR-018 前置项：HR-018-06;HR-018-07；状态：pending_hr018_completion
- 问题：After HR-018 accepts or revises R10R006/R10R007, which accepted period and role observations should enter R11, with what no-disclosed-contract-amount and no-base-movement-relation boundaries?
- 来源：S099;S101；定位：PDF pp.2,8 | official list, FY2026
- 影响：R11 administrative/public-service entry
- 默认边界：2,894,630 日元是 ONC 事业分类成本，不是 MOFA 支付额或合同额。 | 指定延续不提供金额，也不证明对其他冲绳 NGO 的资助。
- 决定选项：include_after_hr018|revise_scope_after_hr018|exclude

## HR021-005 · R10R008

- 依赖类型：dependent_on_hr018
- HR-018 前置项：HR-018-08；状态：pending_hr018_completion
- 问题：After HR-018 accepts or revises R10R008, should the resulting relation enter the R6/R11 advocacy-administration boundary, and with what limits on payment, stable-alliance and government-endorsement claims?
- 来源：S002;R10S11;R10S12；定位：S002 PDF p.1 row 1; R10S11 PDF p.1 row 2; R10S12 PDF p.2
- 影响：R6/R11 advocacy-administration boundary
- 默认边界：实际合同可确认；不等于 grant、政治支持或运动资金。
- 决定选项：include_after_hr018|revise_scope_after_hr018|exclude

## HR021-006 · R10R018

- 依赖类型：dependent_on_hr018
- HR-018 前置项：HR-018-17；状态：pending_hr018_completion
- 问题：After HR-018 accepts or revises R10R018, should the resulting service-presence relation enter R11, and with what explicit prohibition on anti-base/pro-base stance inference?
- 来源：S097；定位：USO Okinawa centers and audience page
- 影响：R11 service entry
- 默认边界：按服务功能编码，不推断亲基地或反基地立场。
- 决定选项：include_after_hr018|revise_scope_after_hr018|exclude

## HR021-007 · R10R020;R10R021

- 依赖类型：dependent_on_hr018
- HR-018 前置项：HR-018-18;HR-018-19；状态：pending_hr018_completion
- 问题：After HR-018 accepts or revises R10R020/R10R021, should either sponsor-tier observation enter R11, and with what no-amount, no-year and no-political-stance boundaries?
- 来源：S097；定位：USO Okinawa sponsors page
- 影响：R11 service sponsorship
- 默认边界：赞助层级不是金额。
- 决定选项：include_after_hr018|revise_scope_after_hr018|exclude

## HR021-008 · AEV0061;AEV0062;AEV0063;AEV0064

- 依赖类型：independent_evidence_review
- HR-018 前置项：不适用；状态：not_applicable
- 问题：Does independent factual directed-edge evidence exist for any of the four analytical pathway seeds? Cite that evidence before promotion; otherwise retain analytical_seed.
- 来源：S049;S003;S004；定位：formal AEV analytical_seed rows
- 影响：R6/R7 pathway diagrams and R11 entry interpretation
- 默认边界：Retain as analytical_seed; no observed stable chain or causal arrow.
- 决定选项：promote_with_independent_evidence|retain_analytical_seed|exclude_seed
