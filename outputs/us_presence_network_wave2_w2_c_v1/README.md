# W2-C 问责结果、负案例与项目改变反例 v1

日期：2026-08-22

状态：`research_only` / `not_frontend_ready` / `central_writeback=no` / `review_status=ai_seeded`。

## 结论先行

原先“制度只能记录、认定、补偿，不能进一步改变项目”的**笼统结果上限判断被削弱**。

原因不是出现了基地取消或迁移，而是泡濑第一波公金诉讼提供了一个明确、可执行、可归因的反例：那霸地裁禁止县与市继续作未来公金支出、签订合同或负担新义务（已经发生的支付义务除外）。因此它同时落在 `PROJECT_BUDGET=yes_bounded` 与 `PROJECT_AUTHORITY=yes_bounded`。

目前仍可保留的窄结论是：在这组选择性案例中，民间行动较稳定地留下制度入口与正式记录，部分案件获得过去损害赔偿或程序性产出；除泡濑第一波的有界财政／权限限制外，尚无经负责人复核的案例证明民间行动造成了军事设施／部署的持久取消、迁移或核心运行改变。观察到的其他项目变化，多数有技术、行政审查、地方政府协商或政府间争议等竞争解释。

这不是成功率，也不是冲绳全部民间行动的总体结论。13 个正向 episode 本来就是按可观察入口／记录选出的。

## 三组样本

- 正向入口框：13 个 source episode；泡濑拆为两波，共 14 个分析单元。
- 匹配闸门框：6 行；其中包含严格匹配闸门、有界未决、回应追踪控制，以及 1 个明确排除出严格“未入场”框但保留作司法救济控制的案件。
- 项目改变／反例框：6 行，逐项分开事实改变与 civic attribution。
- 并列结果账本：126 行（14 分析单元 × 9 轴）。
- 来源收据：49 条；每个在表中使用的 receipt 均有本地文件、SHA-256 和双向 row↔receipt crosswalk。

## 这轮最重要的校正

1. `ENTRY` 与 `RECORD` 是正向框的入选条件，不是发现，不能拿 13/13 算成功率。
2. TE05 不是简单的“进入”：请求进入议会、诉讼进入法院，但目标公投被正式闸门挡住。
3. TE06 必须分 `TE06-W1` 与 `TE06-W2`；两波结果相反。
4. TE12 的罢工真实发生并影响民用物流，但美国海军官方记录确认军舰访问仍完成；不能把物流扰动写成军事访问被阻止。
5. 泡濑面积由约 185ha 缩为约 95ha 是项目改变，但市方审查／修订在判决前已启动；不能从前后顺序推断诉讼造成缩减。
6. Henoko 约 JPY 930bn 是 2019 年官方粗略总成本估计；JPY 648.3bn 仍只是 2025 记者提问中的累计支出前提，未由底层官方支出表闭合。
7. Earthjustice 申报 USD 276,345.50，Treasury 付款记录 USD 280,000；差额 USD 3,654.50 保留为 `unreconciled difference`，不猜解释。

## 文件

- `positive_entry_sample_v1.csv`：固定 13 episode 与 14 分析单元。
- `nonentry_negative_sample_v1.csv`：按闸门位置重分的负／控制案例。
- `project_change_counterexample_sample_v1.csv`：项目改变与独立 attribution。
- `accountability_outcome_ledger_v1.csv`：9 个并列结果轴。
- `source_receipts_v1.csv`：来源、locator、本地路径、哈希与反向支持行。
- `negative_search_log_v1.csv`：每条 route family 的有界检索结果。
- `project_change_causal_evidence_v1.csv`：行动、决定、时间顺序、因果陈述四项证据。
- `competing_explanations_v1.csv`：竞争解释。
- `principal_review_queue_v1.csv`：负责人需要判断的高影响项目，决定栏全部留白。
- `inclusion_exclusion_log_v1.csv`：三组样本的冻结纳入／排除记录。
- `resource_anchor_crosswalk_v1.csv`：W2-00 金额与预算口径原样保留。
- `artifacts/`：本轮新增或重新冻结的官方原件。

## 复现与验证

```powershell
python scripts\make_us_presence_network_wave2_w2_c_v1.py
python scripts\make_us_presence_network_wave2_w2_c_v1.py --check
python -m unittest tests.test_make_us_presence_network_wave2_w2_c_v1
```

本包不修改中央事实、publication adapter、前端或控制文档。负责人复核前，任何结论都不得提升为正式 publication claim。
