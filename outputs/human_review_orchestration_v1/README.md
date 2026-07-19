# HR016–HR032 人工复核编排包 v1

日期：2026-07-13

> **历史快照，不再是当前任务单。** 本目录记录合并前的 HR-016–032 编排与依赖，原有计数和空白状态仅供审计。当前剩余任务以 `docs/principal_human_review_remaining_v14.md` 为准：157 项＝现在可做线上 101＋依赖后做线上 44＋当地材料 12。

状态：**只做编排与依赖审计，不做 AI 人审，不修改任何 HR CSV。**

## 1. 当前盘点

- HR 范围：HR016–HR032，共 17 个编号。
- 实际 CSV 行：**397**。
- 真正需要人工决定的行：**389**；当前空白决定：**385**。
- HR018 另有 **8** 个来源前置行；它们不是额外的 accept/revise/reject 决定。
- CSV 中明确标注 `needs_local_retrieval` 的行：**13**（HR017 9、HR018 2、HR019 3）。A073 另为 online-exhausted/E0 条目，但不冒充结构化 local flag。
- HR023 与 HR028 均为有意保留的零任务编号；HR032 已成为 **8 行 P1 live queue**，8 个 `decision` 当前均为空。

两张主表：

- `task_inventory_v1.csv`：逐 HR 记录真实行数、空白决定数、依赖、中央表／图／报告资产、重跑动作和边界。
- `recommended_batches_v1.csv`：按“减少全局重跑次数”而非编号顺序编排。

`dependency_graph_v1.svg/.png` 是同一依赖关系的可视化。实线是硬依赖，虚线是减少重跑的建议顺序；图中没有替任何人填写决定。

## 2. 五条不可改写的主依赖

1. **HR027 已完成并合并 A112–A115；122-actor 的 HR029 中间快照已重生。** 仍须先合并 HR019／024／025 与外部 HR010，再做最后一次 HR029 重生和审查；当前 36 行不能直接作为最终 freeze。
2. **HR018 的 8 个来源前置 → HR018 的 26 条敏感关系 → HR021-001–007。** HR021 只决定下游是否纳入，不重复审核关系事实；HR021-008 可独立复核。
3. **AP123 只由 HR025 决定。** Camp Schwab/P006 与 Camp Foster/P007 的键冲突不能由 HR029 或脚本机械覆盖。
4. **HR031 只管解释强度。** 它可以改变报告／论文措辞，不能批准中央事实、角色、边、金额、资金或因果。
5. **HR032 只约束未来 canonical／JV／registry crosswalk。** 当前两张 R10 source-label 总体图保持 ready，不以 HR032 为 gate，也不因 HR032 自动生成 actor、关系边或成员付款。

## 3. P0、P1、local 与 no-task

### P0：先冻结会造成全局重跑的决定

- 第一优先：HR027。
- 中央 actor／issue／place：HR019、HR024、HR025；外部仍有 HR010 依赖。
- 选举接口：HR026。
- 敏感行政／服务关系：HR018；完成后释放 HR021 前 7 项。
- 来源与发布层：HR022、HR030。
- 重生后的全局 schema／alias freeze：HR029。
- 最终报告解释锁定：HR031。

### P1：不应阻塞安全正文层，但应在最终 alias／模块冻结前处理

- HR016：先岛框架语义与 locator。
- HR017：公投 reviewed-all 扩展层；新的 accepted-only F027/F028 不依赖 HR017。
- HR020：R5 名称／别名／切分。
- HR021：R6/R11 下游纳入；其中 7 项依赖 HR018，1 项独立。
- HR032：S002 合作对象名称、法律前缀、JV 成员与 registry crosswalk；8 行并入 B06。它不阻断当前 R10 source-label 图，只为未来 actor-level 解释和 crosswalk 冻结提供人工决定。

### local：没有材料就保持空白

- HR017：9 行。
- HR018：2 行。
- HR019：3 行。
- HR024 的 A073 是 online-exhausted/E0；需要新的身份闭合证据，不能用旧名单或名称相似激活。

local 队列不应反向阻塞现有 accepted-only 安全图，也不能由 AI 摘要代替原件复核。

### no-task

- HR023：coverage mechanical audit，零人审。
- HR028：异质行动包只重组既有正式事实，零人审。

## 4. 推荐执行法

按 `recommended_batches_v1.csv` 的 B00→B11 执行。每一批内部可以拆成 8–12 行、60–90 分钟的人工作业；批次号只表示依赖与重跑顺序，不表示 AI 已判断重要性或事实真伪。

最重要的“只重跑一次”节点是 B08：主线程汇总 HR027、HR019、HR024、HR025 与外部 HR010 的人工决定，应用 AP123 的 HR025 决定，随后重生 HR029。为避免第二次 alias／relation freeze，建议同时尽量完成 HR018、HR020 与 HR032，再进入 B09。HR032 只进入未来 canonical/JV/registry crosswalk；当前 R10 source-label 图不等它。

## 5. namespace／文档一致性审计

- **没有发现两个同时有效的同号 CSV 人审队列。**
- HR026 有表面命名冲突：R08 目录存在 `HR026_status_v0.md`，但控制文档明确 R8 没有新增 HR026，实际有效 HR026 是 R9 选举的 19 行 CSV。该 R8 文件只能视为状态／墓碑文件，不能当成第二个任务。
- HR019 的任务书仍写 63 条 edge scope；HR-027 合并并重生后，`HR019_edge_scope_review_queue_v0.csv` 实际为 **76**。本包按当前实数计数，不修改原任务书。
- HR020 的任务书“复核包”清单漏列实际 14 行决定队列 `hr020_review_queue_v0.csv`；本包将其作为唯一 live queue 计数，不修改任务书。
- HR018 的 26 条关系使用 `accept`／`revise`／`reject` 三列，而不是统一 `decision` 字段；8 条 source prerequisite 没有决定字段。编排时必须避免把 34 行全部误报为 34 个空白决定。
- HR023／HR028 的状态文件不代表空白人审队列。
- HR032 的唯一 live queue 是 `outputs/R10_official_collaboration_universe_v1/HR032_partner_alias_crosswalk_review_v1.csv`（8 行、单字段 `decision`）。它审 source-label→canonical/JV/member/registry crosswalk，不追认 source-label 为 actor 身份。

## 6. 证据与写作边界

- 候选 edge、共同署名、共同活动与事件重复参与不是稳定联盟。
- source/archive 决定只处理元数据、locator、保存状态和可支持范围，不批准 actor、关系、金额或解释。
- project cost、aggregate、NOFO、sponsor tier、membership、service presence 不得写成 actor payment、funding 或政治立场。
- S002 的 machine display alias、法律前缀差异与 JV/member 字符串不得直接写成同一法人、registry actor 或独立资源边；HR032 也不得把复合体项目费拆给成员。
- 选举观察不支持票数贡献、胜负、政策效果或因果。
- 与那国保持前线／安全环境、地方自治、公投、台湾邻近与生活／健康安全主框架，不强行环境化。

## 7. 重生与复核

生成命令：

```powershell
python scripts/make_human_review_orchestration_v1.py
```

脚本只读取 HR CSV、`figure_manifest_v1.csv` 与 `missing_assets_v1.csv`，只写本目录。当前已完成双跑 SHA-256 零差异与依赖图视觉检查。
