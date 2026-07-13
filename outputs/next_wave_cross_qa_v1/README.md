# Next-wave cross-package reproducibility QA v1

日期：2026-07-14

## 结论

本包对 NW2 的八个生成／审计流程做过隔离双跑、人工字段注入、CSV／ID／图件校验和中央写入失败测试。2026-07-14 又按当前工作树做了只读基线刷新：118 actors／295 sources／222 actor–issue／129 actor–place／67 AEV。S248–S294 仍是可复核的 NW2-H 历史波次，S295 是波次之后的 HR-011 补充来源，不改写该波次边界。

此前发现的五类实质性阻断已经关闭：

- HR025／026／027／029／030／031 的声明人工字段均可按稳定 ID 跨重跑保留；
- R3、R9、R5/R7、schema 的九个 SVG 均已消除行尾空格；
- source-log integration 已改为完整验证后原子替换，并通过两种失败注入；
- AP123 仅由 HR025 决定，schema 不再机械越权或复制任务；
- schema 使用动态 `N × 3` 校验，并明确执行顺序为 HR027 后再重生／完成 HR029。

I013／I014 已关闭：当前报告与 validation 的 SHA 完全一致，审计脚本／输出行尾洁净，claim SVG 有末尾换行。当前 QA 问题中只剩 I010 这一项非阻断的快照 provenance 遗留；HR031 的 3 项空白决定仍是研究者判断门槛，不是生成质量缺陷。

## QA 范围

- R3 空间语义与先岛 dossier；
- R9 选举—市民组织接口；
- R9 公投程序 accepted-only 正文图的跨包发布边界；
- registry value gate v2；
- R5/R7 异质行动 repertoire；
- schema／alias freeze；
- next-wave source proposal audit；
- next-wave source integration；
- report claim-evidence audit；
- 对应 `data/interim/32_*`–`38_*` 与 HR-025–031。

本轮动态破坏性测试全部在 `%TEMP%` 的完整仓库副本中进行，没有用测试值污染共享工作树。除已授权的各 package owner 修复外，本 QA 包本身只维护 `outputs/next_wave_cross_qa_v1/`。

## 双跑结果

| 脚本 | 第一次 rc／变化 | 第二次 rc／变化 | 结论 |
|---|---:|---:|---|
| `make_r03_spatial_dossier_v1.py` | 0／0 | 0／0 | 129 rows；41 HR025 |
| `make_r09_election_civic_interface_v1.py` | 0／0 | 0／0 | 19 records；21 sources；19 HR026 |
| `make_registry_value_gate_v2.py` | 0／0 | 0／0 | 5 candidates；4 HR027 |
| `make_r05_r07_heterogeneous_repertoire_v1.py` | 0／0 | 0／0 | 148 observations；HR028=0 |
| `make_schema_alias_freeze_v1.py` | 0／0 | 0／0 | 467 candidates；34 HR029 |
| `audit_next_wave_source_proposals_v1.py` | 0／0 | 0／0 | 49 URLs；中央只读 |
| `integrate_next_wave_sources_v1.py` | 0／0 | 0／0 | 历史波次 S248–S294；当前中央表 295；22 HR030 |
| `audit_report_claims_v1.py` | 0／最终 trace 刷新 | 0／0 | 正文与 validation SHA 一致；78 claims；32 numeric groups |

最终报告审计为 `safe 71 / revise 6 / block 1`，32 组定量检查没有数值不一致，source ID 与 formal path 均无缺失。`block 1` 是既有人工任务控制的发布边界；HR031 另保留 3 项空白解释性决定，没有被自动填写。

## 当前基线与历史波次

- 中央基线：118 actors／295 sources／222 actor–issue／129 actor–place／67 AEV。
- R3 当前派生层：129 条空间语义，17 条 human-reviewed／112 条 candidate or evidence-gap，41 项 HR025。
- R5/R7 当前派生层：148 条正式观察，拆分为 63／27／24／25／9，去重为 39 个行动单元。
- NW2-H 的 47 个新 URL 仍固定映射到 S248–S294；S295 只进入当前 source log，不重编号、不扩张该批 HR030 的历史对象范围。

## 人工任务 round-trip

| 任务 | 当前行数 | 稳定键 | 注入后两次重跑 |
|---|---:|---|---|
| HR025 | 41 | `object_id` | 五个声明人工字段全部保留；第二次 0 diff |
| HR026 | 19 | `review_item_id` | 声明字段及附加人工字段保留；第二次 0 diff |
| HR027 | 4 | 业务稳定 `task_id`，如 `HR027-RV2C001` | 声明的 decision/reviewer/date/note 保留；第二次 0 diff |
| HR028 | 0 | 无任务表 | 按设计保持 0，不新增事实任务 |
| HR029 | 34 | `review_item_id` | 声明字段及附加人工字段保留；第二次 0 diff |
| HR030 | 22 | source/audit 复合 `review_item_id` | decision、metadata 修订与 reviewer 字段保留；第二次 0 diff |
| HR031 | 3 | `review_item_id` | decision/reviewer/date/note 保留；第二次 0 diff |

当前真实 task book 的人工字段仍全空。以上结论来自临时副本注入，不代表替用户作出任何研究判断。

## 中央 source-log 原子性

`integrate_next_wave_sources_v1.py` 是本范围唯一获准写 `data/processed/05_source_log_initial_v0.csv` 的流程。修复后，完整 prospective state 会先校验，再通过同目录临时文件和 `os.replace` 提交。

两项隔离失败测试均通过：

1. `NW2H_FAIL_AFTER_SOURCE_VALIDATION=1`：命令按预期返回 1，source log SHA 不变；
2. 从 247 行 premerge 状态运行并设置 `NW2H_FAIL_BEFORE_ATOMIC_REPLACE=1`：命令按预期返回 1，source log 仍为 247 行，且没有残留临时文件。

因此，I003 的“失败但中央表已被部分写入”风险已经关闭。

## 数据、ID 与图件

- 58 个范围内 CSV 均可解析且行列矩形；关键主键唯一，跨表引用通过。
- `data/interim/32_*`–`38_*` 与各输出包当前计数一致；`interim/38_*` 已与当前报告 SHA 对齐。NW2-H 整合包已显示当前 295 条／S001–S295，同时仍将 S248–S294 作为历史波次、将 S295 作为批外补充。
- 当前 HR025／026／027／029／030／031 分别为 41／19／4／34／22／3 行，稳定键均唯一。
- 10 个范围内 SVG 均可由 XML parser 解析，且行尾空格计数为 0；所有 HTML 相对图件引用可解析。
- 九个模块 SVG 与报告审计的 `fig_claim_publish_status_v1.svg` 均已洁净；claim SVG 末尾字节为 LF。
- 本次另行复核的两张 R9 accepted-only SVG 也均可解析且行尾空格为 0；PNG 实际尺寸分别为 3260×2096 与 2547×1505。
- audit script 与 `outputs/report_claim_audit_v1/` 全部文件的 scoped 行尾检查为 0；主线程最终第二次审计运行全包 diff=0。

## R9 accepted-only 正文图补充复核

R9 公投程序的两张正文图已把正式层与 HR-017 扩展层分开：

- `referendum_process_timeline_accepted_v1.png/.svg` 只读取中央正式表的 24 条 `accepted` stages；
- `institutional_gate_flow_accepted_v1.png/.svg` 同时受 25 条 `accepted` role observations 约束；
- 生成器 `accepted_figure_inputs()` 明确只读正式表，拒绝行中出现 `needs_human_review`、`HR-017`／`HR017` 或 `pending`；
- reviewed-all 表中的 9 条待审阶段与 9 条待审角色仍留在 HR-017，但未进入 accepted-only 图；
- `figure_manifest_v1.csv` 的 F027／F028 均为 `ready_now`、`hr_gate=none`；
- `missing_assets_v1.csv` 的 MA005 已为 `online_completed`、`status=completed_v1`、`blocks_boss_facing_final=no`、`human_gate=none`。

因此，MA005 已消除，HR-017 只控制未来扩展层，不再阻断这两张 accepted-only 正文图。旧 `*_v0.png` reviewed-all 图仍仅作为历史审计附录，不得替代正文版；图中顺序／箭头也不表示因果。

## 本轮补充闭环与仍开放问题

- I008 已解决：R9 README 将 21 行 proposal 文件标为 historical snapshot 并链接 NW2-H integration crosswalk；registry README 同样区分 29 行历史 proposal、S001–S294 波次 provenance 与波次后 S295。
- I009 已解决：R9、registry、R5/R7 与 integration 的 21／29／29／189／50／49 行相关表均使用 `relation_or_claim_approved=no`；`no_new_approval` 只保留在独立的 provenance-scope 字段中。
- I011 已解决：R8 的 `HR026_status_v0.md` 标题和正文均明确它是 module-local historical note，并指向 R9 的 19 项权威 HR026 task book 与总导航。
- I013 已解决：报告与 validation 共用 SHA `aa7509bc582f7d73192df694b217b1939ef4d3f8fd5f1d1c37cd76fc3e163887`，78 claims／32 numeric groups／0 mismatch／0 missing paths。
- I014 已解决：当前 SHA `aa7509bc582f7d73192df694b217b1939ef4d3f8fd5f1d1c37cd76fc3e163887` 对应的 audit script 与输出无行尾空格，claim SVG 有末尾换行。
- I010 仍开放：八个流程保留固定日期／快照守卫，未来数据增长需显式版本与重生顺序。

当前 QA 包的唯一 open issue 是 I010。

## 报告审计最终核对

正文与 validation 的共同 SHA-256：

`aa7509bc582f7d73192df694b217b1939ef4d3f8fd5f1d1c37cd76fc3e163887`

最终核对结果：

- claim 单元：78；
- publish status：safe 71／revise 6／block 1；
- numeric groups：32，mismatch 0；
- missing source IDs：0；missing formal paths：0；
- mechanical fix：0；
- HR031：3 行，decision／reviewer／date／note 全空；
- 当前只读复核：report SHA 与 validation SHA 一致；
- audit script／output trailing whitespace：0；claim SVG 以 LF 结尾。

审计技术门禁已经闭合；任何未来正文修改仍必须重新运行审计并再次要求 SHA 对齐与第二次 0 diff。HR031 与既有人工 gate 的实质判断仍需研究者完成，不能因 QA 通过而视为自动接受。

## 研究边界

- 本 QA 不判断候选 actor、空间语义、选举角色、alias、资金、污染／健康因果或选举效果是否应被接受。
- 没有发现任何 `relation_or_claim_approved=yes` 或同义正向批准。
- source inclusion 仍不批准 actor、关系、联盟、资金、因果或政治立场。
- R5/R7 的观察单元不是频率估计，路径箭头不是因果关系。
