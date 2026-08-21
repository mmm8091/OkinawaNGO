# USN-SERVICE-01 人工复核任务：驻军社会服务／慈善生态

状态：负责人已于 2026-08-20 按研究支持稿确认全部建议；正式 queue 已回填。任务范围仅限 `outputs/us_presence_service_recon_v1/` 的 13 项候选，不代表中央表已修改。

AI 研究支持（2026-08-19）：[`human_review_research_USN_service_ecology_v1.md`](human_review_research_USN_service_ecology_v1.md) 已完成逐项证据、反证、建议决定和可粘贴 `principal_note` 草稿。该支持稿原本不构成负责人决定；现已按负责人确认写入正式 queue。

负责人回传（2026-08-20）：[`human_review_return_USN_service_ecology_v1.md`](human_review_return_USN_service_ecology_v1.md)。正式决定以回填后的 queue 和该回传记录为准；尚未授权中央合并或前端发布。

下列正文保留派发时问题与建议作为 provenance。SR-HR-008 的“新 flow”初始建议已被正式 `defer` 覆盖；SR-HR-012 的三级方案已被正式 LEG0–LEG3 四级决定覆盖，不得再将派发文本当作现行规则。

## 回填办法

逐项阅读下列证据后，在 `outputs/us_presence_service_recon_v1/human_review_queue_v1.csv` 填写：

- `principal_decision`：只使用该项列出的允许决定；
- `principal_note`：写明判断理由、采用的名称/类型/边界；
- 在单独回传文档中记录复核人和复核日期。

不要直接改中央 actor、relation、source、person 或前端数据。完成后交主线程生成专用、幂等的受控合并器。金额关系必须保留年份、用途、金额语义和来源；人物职务必须保留适用年份；组织宣传不得直接判为实际合法化效果。

## 先确认共同口径

- L0：可核的服务、资源流、受益对象或项目事实。
- L1：组织、军方或发言人使用的 `goodwill`、`friendship`、`bond`、`bridge`、`unity`、`community relationship` 等叙事。
- L2：服务实际提高当地公众或受益者对美国军事存在的接受度。

本包目前只有 L0、L1 证据。L2 必须有受益者一侧、地方社会一侧或独立效果材料，不能由慈善行为或宣传文本直接推定。

---

## SR-HR-001 — Marine Thrift Shop Okinawa 是否入表

**对象：** SA010

**证据：** 独立组织网站公开 mission、board、grants、outreach；MCIPAC 当前 roster 列为 active；IRS-derived 记录显示 EIN 38-3924106、501(c)(3) 与 FY2024 申报；2024 年军方报道有具名、具额捐赠。

**建议：** 作为服务／慈善侧 actor 审定，不赋亲基地立场。需同时确定 `actor_class`、`origin_type` 和 Marine Gift Shop/MOSCO/AWWA 的实体边界。

**允许决定：** `add_background_service_actor` / `defer_identity_or_scope` / `reject_duplicate_or_out_of_scope`

**回填要点：** 若 add，写 canonical name、actor class、origin type；是否接受其官网为身份来源；不得自动批准任何资金边。

## SR-HR-002 — Marine Gift Shop 是否入表

**对象：** SA011

**证据：** MCIPAC roster 记 active；FY2025 IRS-derived filing 有收入、库存销售与 officer；但公开界面同时提示其未出现在最新 exempt list，自有网站只有占位页。

**建议：** 优先解决 IRS/MCIPAC 状态冲突，再决定是否作为独立 gift-shop actor。

**允许决定：** `add_with_status_note` / `defer_status_conflict` / `reject_duplicate_or_inactive`

**回填要点：** 若 add，说明当前状态如何编码；不得与 MOSCO、AWWA 或 Marine Thrift Shop 合并，除非另有结构证据。

## SR-HR-003 — Neighborhood Pantry 是 actor 还是 program

**对象：** SA012

**证据：** 有独立项目页、MCIPAC active roster 条目、Foster/Kinser 两个点位、具名负责人和持续服务记录；尚未找到独立法人、财务或治理资料。

**建议：** 在“组织 actor”和“项目节点”之间明确选一，避免把项目名称直接 actor 化。

**允许决定：** `add_actor` / `program_node_only` / `defer_autonomy` / `reject_duplicate`

**回填要点：** 若 program，写明承载组织及可用关系类型；若 actor，说明独立性证据。

## SR-HR-004 — NIOSC 是否入表

**对象：** SA013

**证据：** 官方网站说明多军种配偶成员、军事家庭与冲绳地方公益；MCIPAC 当前 roster 列 active；只找到 2025 年 president 线索，税务/完整 board 未确认。

**建议：** 可按服务侧 background spouse club 审定，人物边仍单独保留候选。

**允许决定：** `add_background_service_actor` / `defer_second_source` / `reject_out_of_scope`

**回填要点：** 若 add，写 actor class、origin type、证据等级；不要把官网“positive contribution”写成社会效果。

## SR-HR-005 — AER、AFAS 的范围口径

**对象：** SA014、SA015

**证据：** Military OneSource 当前页面分别确认 Torii Station 的 Army Emergency Relief、Kadena 的 Air & Space Forces Aid Society 服务点及贷款/补助功能。

**建议：** 与 Red Cross/NMCRS 使用一致模型：全国组织与冲绳服务 presence 分开，不伪装成冲绳本地 NGO。

**允许决定：** `national_actor_with_local_presence` / `service_presence_node_only` / `defer_scope_rule` / `out_of_scope`

**回填要点：** 对 AER、AFAS 可分别决定；写明总部 actor 与地方 presence 是否共用 ID。

## SR-HR-006 — 两个 roster 线索是否继续入表

**对象：** SA016 Helping Japan International；SA017 Okinawa Area Office Civilian Welfare Council

**证据：** 当前只有 MCIPAC active roster 行。其 function、逐行 geography、负责人、独立网站与财务均未确认。

**建议：** 维持 defer，除非负责人认为 roster 身份已足以创建最低限度背景节点。

**允许决定：** 每个对象分别填写 `add_roster_only_background` / `defer_second_source` / `reject_out_of_scope`

**回填要点：** 不得凭名称中的 `Helping` 或 `Welfare` 推定实际服务关系。

## SR-HR-007 — ACGO 生命周期

**对象：** SA009 / X017

**证据：** IRS-derived filing 截至 FY2018；当前 MCIPAC roster 未见；尚无一手 dissolution、withdrawal、rename 或 successor 记录。

**建议：** 作为历史 actor 保留，当前状态未知，不写解散日。

**允许决定：** `retain_historical_status_unknown` / `defer_lifecycle` / `set_end_or_successor_with_new_primary_source`

**回填要点：** 只有选择第三项时才能填写结束日期或 successor，并必须补 URL 与 locator。

## SR-HR-008 — KOSC → AWWA 2,580 美元

**对象：** RF001

**证据：** KOSC FY ending 2025-05 的 IRS-derived Schedule I 报告 `American Womens Welfare Association` 2,580 美元。

**建议：** 经底层 Form 990/XML 和名称 crosswalk 确认后，作为一条**新的、有年度的 flow**加入。历史 F025 继续保留为有界关系，不被 RF001 覆盖或替换。

**允许决定：** `accept_new_dated_flow` / `defer_underlying_filing_or_crosswalk` / `reject_endpoint_or_semantics`

**回填要点：** 若 accept，保留 `currency=USD`、`amount_semantics=exact_reported`、FY、用途和来源；不得把它扩写为 AWWA 全年总额。

## SR-HR-009 — OESC → AWWA 8,479 美元

**对象：** RF002

**证据：** OESC FY ending 2025-06 的 IRS-derived Schedule I 报告 AWWA 8,479 美元，用途说明为支持冲绳美军社区相关免税组织。

**建议：** 核底层 filing 后审定为年度 grant flow。

**允许决定：** `accept_new_dated_flow` / `defer_underlying_filing` / `reject_endpoint_or_semantics`

**回填要点：** 若 accept，保留 `currency=USD`、`amount_semantics=exact_reported`、FY、用途与来源；不推断政治影响。

## SR-HR-010 — Marine Thrift Shop 与 AWWA 的结构关系

**对象：** SA010 / X004

**证据：** Shop 自有 grants 页面称其为 AWWA member/contributor；2024 军方报道描述 AWWA 通常参与日本侧 recipient 选择。

**建议：** 将结构 membership、年度 contribution、recipient-channel 分开复核，不合成一条“合作关系”。

**允许决定：** `accept_membership_only` / `accept_membership_and_separate_channel_role` / `defer_relation_type` / `reject_relation`

**回填要点：** 明确方向、有效年份、关系类型；金额必须另立 flow，不能写进 affiliation。

## SR-HR-011 — USO 当前 sponsor roster

**对象：** SA001 及 USO 页面当前 partner tiers

**证据：** USO Okinawa Area Office 页面当前列 Mission Partner、Community Partner、Platinum、Silver、Bronze 等层级；页面为动态现状，没有统一起始日期和金额。

**建议：** 若采用，只建带 `observed_at=2026-08-19` 的 tier snapshot；无金额不写 funding amount，无治理证据不写 affiliation。

**允许决定：** `accept_dated_sponsor_snapshot` / `defer_archive_or_identity_crosswalk` / `reject_current_page_as_too_volatile`

**回填要点：** 对每个 sponsor 分别 crosswalk；tier 与 amount 分开；AEC 的具额 2025 flow 仍是另一条事实。

## SR-HR-012 — L0/L1/L2 解释门禁

**对象：** LC001–LC012

**证据：** 本包有服务与转移事实，也有 USO/AWWA 等使用 goodwill、friendship、bond、bridge、unity 的可定位文本；没有受益者调查、地方舆情或独立效果评估。

**建议：** 正式采用三级：L0 可作为事实候选，L1 可作为来源话语，L2 保持未证。

**允许决定：** `adopt_L0_L1_L2_gate` / `revise_gate_with_explicit_rule` / `defer_interpretive_schema`

**回填要点：** 若 revise，必须写出 L2 所需证据门槛；不得批准任何现有 LC 行为 L2 效果结论。

## SR-HR-013 — 日本侧 recipient 名称 crosswalk

**对象：** SR006、SR007、SR009、SR010

**证据：** Marine Thrift Shop 页面列出 NPO/ARU、Tinsaku no Kai、Far East Council、Oki Hands Oki Hearts 等英文或转写名称；尚未全部对应到日文正式名称和独立身份来源。

**建议：** 逐个 crosswalk，未确认者留 event/recipient-only，不进 actor registry。

**允许决定：** 每个名称分别填写 `accept_crosswalk_with_canonical_name` / `defer_identity` / `reject_mismatch_or_non_actor`

**回填要点：** 若 accept，补日文 canonical name、alias、组织 URL、legal/identity source；recipient 事实和 actor 身份仍是两次不同批准。

---

## 交回主线程时

请同时交付：

1. 已填 `human_review_queue_v1.csv`；
2. 一份简短回传记录，列出 13 项决定、复核人、日期和新增来源；
3. 若补了新 URL，注明是否需要进入 source proposal 和本地归档。

主线程复核后才能决定是否生成中央合并器；本任务本身不授权自动合并或前端发布。
