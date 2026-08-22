# 对美主线第二轮《意外发现登记》与有限侦察 retrofit 审计 v1

日期：2026-08-22
范围：W2-A、W2-B、W2-C、W2-D、W2-E 的现有输出包、builder 与测试
状态：`retrofit_completed`

## 1. 审计结论

审计开始时，五个包都没有 README 的《意外发现登记》栏目，也没有
`unexpected_findings_register_v1.csv`。本轮现已完成 retrofit：W2-A—E 的 builder、README 与定向测试
均接入正式 19 列契约，五张登记表均为 0 行、保留表头；W2-A/B/D/E 的既有 manifest 已纳入新文件，
W2-C 按原架构继续不设 manifest。

实施保持在最小范围：五个 builder 增加同一字段契约、一条 CSV 写出、README 固定栏目和定向验证；
没有新增图、中央表、publication adapter、前端输出或 HR 队列。通用验证器由
`scripts/validate_research_work_package_v1.py` 提供，五包已通过。

本轮不应把任何现有实质发现追溯倒灌进登记表。它们已经进入正式分析表、来源收据、负检索、
负责人队列、端点 handoff、claim table 或历史 spine。把这些内容再复制成 `lead_only` 会制造两套
状态和两个后续入口。五包本次 retrofit 均已生成 **0 行、保留表头** 的登记表。

当前材料中只有 W2-C 的 `W2C2-SR029` 接近纯 locator 线索：它是未被分析采用的名护市 PDF
快照，`supports_ids` 为空，原始直链未闭合。但它已作为 provenance receipt 被保存；不建议回填。
若 W2-C 日后因新的研究授权实质重开，并决定追查原始直链，则从那一刻起可把“原始 PDF locator
闭合”记作新的 `lead_only` 根线索。

## 2. 适用触发与非触发

“新建研究包”是新建输出目录及其 builder。“实质重开”是获授权后新增外部检索、新观察，或重新
解释并改写分析行／claim 的研究工作。发生任一情况时，包必须同时具备 README 栏目与登记 CSV。

确定性重建、`--check`、测试、manifest/hash 刷新、render-only、纯拼写或标签修正不构成新的侦察
授权；但一旦 builder 完成 retrofit，这些机械运行仍必须稳定保留登记文件和 README 栏目。
“最多三步”是上限，不是把关闭的包重新打开或扩大研究问题的授权。

## 3. 正式 CSV 契约

审计时曾考虑更细的 21 列方案；负责人随后批准了更轻量的正式契约，避免把偶发线索登记变成另一套
事实表。权威列序只取自 `data/metadata/unexpected_findings_register_template_v1.csv`，语义和
升级边界只取自 `docs/research_work_package_protocol_v1.md`，本审计不再维护第二份字段表。

计数单位是新观察行：每包累计最多 10 行，根发现为 step 0 并计入总额；每个子行的 step 必须等于
父行加一，任何路径不得超过 step 3。登记行不是 source receipt、fact、claim、negative result 或
HR task，也不能因留有 URL／locator 而分配中央 S-ID。

## 4. README 最小栏目

每个包加入同名栏目 `## 意外发现登记`，只需包含：

- `unexpected_findings_register_v1.csv` 的路径和当前行数；
- 固定边界：全部 `lead_only`，不进入本包结论、中央层或前端，不触发 HR；
- 每条根线索最多向外追查 3 步，每包最多 10 条新观察；
- 空表解释：“本次构建没有登记新的偶发线索”，不表示现实中不存在其他关系或材料。

README 不应逐条复述线索，也不应把登记行计入“发现”“证据”“候选关系”“负责人判断”或图表计数。

## 5. 五包现有内容的去向判定

| 包 | 已进入正式分析，禁止倒灌 | 当前仅登记候选 | 初始登记建议 |
|---|---|---|---|
| W2-A | OESC/MTS→AWWA 的重复输入、AWWA 分配与 recipient coverage、MTS→Lions USD 10,000、三项 LEG2 候选均已进入 ledger／mediation／recipient 表；人物消歧、exact transaction、Lions 下游、MOSCO/KOSC 已进入正式 queue、negative log 或 W2-D handoff。 | 无。Lions 最终端点虽未闭合，但已是正式复核项，不是偶发旁线。 | 0 行表头。 |
| W2-B | USO 年份／站点口径、同一 federal award 的两种金额视图、全国→地区→冲绳分配缺口、本地 sponsor/service observations、NMCRS→ARC 接口均已进入正式表或 queue。`W2B2-DE012` Okinawa Nurses Association 已是 W2-D event-only endpoint candidate。 | 无。DE012 若在新规则下首次发现会适合登记，但现已正式 handoff，不再复制。 | 0 行表头。 |
| W2-C | 13 个 selected comparison episodes、六行 gate/control frame、真正 matched non-entry arm 缺口、TE10–13 人审边界、泡濑一审候选、Earthjustice/Treasury 差额、JPY 930bn／648.3bn 边界均已进入分析表、README 或 queue。 | `W2C2-SR029` 只适合未来重开时登记“原始 PDF 直链闭合”这一 locator 追查；它当前已是无支持对象的 provenance receipt，不回填。 | 0 行表头。 |
| W2-D | 4,482 行 pair-family matrix、36 个有界 public-record zero、DoD `system_interface`、人物／recipient／funder 缺口、NMCRS→ARC、X018 admission 与 A070 alias 均已进入 matrix、graph、claim 或 queue。 | 无。未解析 pair 是正式审计结果或覆盖缺口，不能批量改名为意外发现。 | 0 行表头。 |
| W2-E | 30 行历史 spine、记录制度差异、care→proposal→行政／省厅／国会路径、NPO 法可见性锚点、AWWA genealogy conflict、1997 statement、NARA 403 均已进入 source receipt、claim、search log 或 local task。H018 虽写作 identity lead，H030 虽写作 material-support lead，也已经是正式 spine 行。 | 无。H018、H030 和 NARA locator 都不能因名称含 `lead` 而倒灌。 | 0 行表头。 |

核心判定标准不是一行是否带有 `candidate`、`lead` 或 `unresolved` 字样，而是它是否已经参与正式
选择框、分析、claim、来源支持、负检索、任务或 handoff。已经参与者留在原有生命周期中；登记表
只接住以后研究过程中偶发、尚未进入这些正式通道的旁线。

## 6. 各 builder 的最小落点

### W2-A

在 `scripts/build_us_presence_network_wave2_w2_a_v1.py` 增加字段常量和返回空列表的
`build_unexpected_findings()`；在 `build()` 的 CSV 写出区写固定表头，并把行数加入 `counts`、README
和 validation。现有 `manifest.json` 使用 `rglob`，重建后会自动纳入新文件，不改 manifest 架构。

### W2-B

在 `scripts/build_us_presence_wave2_w2_b_v1.py` 的 `tables` 与 `fieldsets` 各加一项，并在
`validate_package()` 与 README 中加入契约检查和计数。当前 deliverables 从 `tables` 生成，因此
`manifest_v1.json` 会自动收录，无需另写 manifest 分支。

### W2-C

在 `scripts/make_us_presence_network_wave2_w2_c_v1.py` 的 `build_tables()` 增加空表及固定字段；在
`validate()`、`readme()`、`validation_report()` 加计数和边界检查。`payloads()` 与 `--check` 会自动
覆盖新 CSV。不要为这一个 retrofit 新增 manifest 或图。

### W2-D

在 `scripts/build_us_presence_network_wave2_w2_d_v1.py` 的 `main()` 增加空表写出，把 rows 传入
`validate()` 并加入 README count。现有 `manifest_v1.json` 使用 `rglob`，会自动收录。

### W2-E

在 `scripts/build_us_presence_network_wave2_w2_e_v1.py` 的 `build()` 增加空表写出、count、README
栏目和 `validate()` 参数。现有 `manifest.json` 使用 `rglob`，会自动收录。不要把
`historical_spine_v1.csv` 中名称带 `lead` 的既有行搬入新表。

五个 builder 从正式模板取得同一列序；不得从本审计早期草案另造字段契约。将来建立新的 wave
builder 模板时，再把写出逻辑提升为模板级规则。

## 7. 验收与测试清单

五个现有测试文件各增加相同的包级断言，并保留原有业务断言：

1. CSV 存在；空表也具有正式模板的精确表头，README 存在固定栏目且计数一致。
2. 行数 `<= 10`，`lead_id` 唯一。
3. 所有行固定为 `workflow_status=lead_only`、`claim_eligibility=no`、
   `human_review_trigger=no`、`central_writeback=no`、`publication_eligibility=no`。
4. step 只允许 0–3；根行 parent 为空；子行的 chain、parent 和 step 链完整。
5. locator 不自动进入 source receipt。
6. 登记 ID 不出现在 claim table、主分析表、principal review queue、端点 handoff、图、publication
   或 frontend payload；README 只显示文件路径、计数和边界，不显示逐行内容。
7. 每个 builder 连续运行两次结果一致；W2-C `--check` 通过；各包原有 validation 状态仍为 PASS。
8. 受保护中央文件哈希保持不变，现有业务表行数与语义不因空登记表改变。

对应测试文件为：

- `tests/test_build_us_presence_network_wave2_w2_a_v1.py`
- `tests/test_build_us_presence_wave2_w2_b_v1.py`
- `tests/test_make_us_presence_network_wave2_w2_c_v1.py`
- `tests/test_build_us_presence_network_wave2_w2_d_v1.py`
- `tests/test_build_us_presence_network_wave2_w2_e_v1.py`

## 8. 推荐实施顺序与停止条件

先在五个 builder 中加入空表契约并重建对应包，再运行五组定向测试和现有 package validation。
只有未来实质研究中真的出现旁线时才新增非空行。达到任一条件即停止侦察：已回答预写的单一检查、
下一步会进入原包主问题、需要新增研究授权、达到 step 3，或全包达到 10 行。

此次 retrofit 不做历史线索迁移，不新建 HR，不改变现有 claim 强度，不新增来源到中央层，不改
publication/frontend，也不生成任何新图。

## 9. 实施验证

2026-08-22 主线程完成以下复验：

- W2-A—E 五张登记表均精确符合 19 列模板，数据行为 0；
- 五包 README 均含精确栏目 `## 意外发现登记`；
- 通用协议验证器对五包返回 `PASS`；
- 通用验证与五包定向单元测试合计 54 项通过；
- W2-A—E 原研究表计数和结论没有因空登记表改变；
- W2-B 的 47,000 口径修正另行完成，不属于意外发现登记，也没有进入该图或发布层。
