# W2-C 问责结果、闸门／控制与项目改变归因 v1

日期：2026-08-22

状态：`research_only` / `not_frontend_ready` / `central_writeback=no` / `review_status=ai_seeded`。

## 结论先行

本包不能把“制度只能记录、认定、补偿，不能进一步改变项目”的笼统结果上限判断写成已被确认推翻。泡濑第一波公金诉讼提供的是一个**待负责人确认的有界候选**：官方一审判决主文支持在判决层编码财政／权限限制，但当前 W2-C 研究层尚未完成人工解释确认。

`PROJECT_BUDGET=yes_bounded` 与 `PROJECT_AUTHORITY=yes_bounded` 只表示官方一审判决主文所支持的 judgment-level outcome candidate。它们不表示项目被持久取消、不表示权限限制后来持续有效，也不表示实际预算、财政支出或决算已经改变。后续项目过程与约 185ha→95ha 的范围变化必须另行解释。

目前只能保留更窄的描述：13 个既有 episode 被选择用于九轴并列比较，入口状态必须逐行读取。TE12（工作场所／港口行动）和 TE13（参与／动员记录）不满足独立制度入口；TE10–TE13 的事件事实仍待人审。其余若干案例有正式入口、记录、赔偿或程序产出，但这组选择性材料不能估计入口率、成功率或总体结果上限。

六行补充材料只构成 gate/control frame。它们包含已入场后遇到的闸门、回应追踪控制和一手材料未闭合案例；真正可与已入场案例比较的 matched non-entry arm 尚未建立。

## 三组样本

- 被选 episode 比较框：13 个 source episode；泡濑拆为两波，共 14 个分析单元。它不是正向入口分母。
- 闸门／控制框：6 行；所有行均标记 `true_matched_nonentry_arm_status=not_established`。
- 项目改变／归因比较框：6 行，逐项分开事实改变、决定主体与 civic attribution。
- 并列结果账本：126 行（14 分析单元 × 9 轴）。
- 来源收据：49 条；每个在表中使用的 receipt 均有本地文件、SHA-256 和双向 row↔receipt crosswalk。

## 这轮最重要的校正

1. `selection_condition` 现在只编码 `selected_comparison_axis`；实际入口状态另存 `entry_status_at_selection`，不能拿 13/13 算入口率或成功率。
2. TE05 不是简单的“进入”：请求进入议会、诉讼进入法院，但目标公投被正式闸门挡住。
3. TE06 必须分 `TE06-W1` 与 `TE06-W2`；两波结果相反。
4. TE10–TE13 全部待事件级人审；TE12/TE13 只能按各自行动／参与状态进入比较，不能称为独立制度入口。
5. 泡濑一审的两个 `yes_bounded` 是待负责人确认的判决层候选，不是持久取消、持续权限限制或实际预算改变。
6. TE12 的罢工真实发生并影响民用物流，但美国海军官方记录确认军舰访问仍完成；不能把物流扰动写成军事访问被阻止。
7. 泡濑面积由约 185ha 缩为约 95ha 是项目改变，但市方审查／修订在判决前已启动；不能从前后顺序推断诉讼造成缩减。
8. Henoko 约 JPY 930bn 是 2019 年官方粗略总成本估计；JPY 648.3bn 仍只是 2025 记者提问中的累计支出前提，未由底层官方支出表闭合。
9. Earthjustice 申报 USD 276,345.50，Treasury 付款记录 USD 280,000；差额 USD 3,654.50 保留为 `unreconciled difference`，不猜解释。

## 文件

- `selected_episode_comparison_frame_v1.csv`：13 个被选 episode、逐行入口状态与 14 个分析单元。
- `gate_control_frame_v1.csv`：六行闸门／控制观察；不构成 matched non-entry arm。
- `project_change_attribution_frame_v1.csv`：项目改变与独立 attribution。
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
