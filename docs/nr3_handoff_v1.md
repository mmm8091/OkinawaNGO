# NR-03 换手文档 v5：core surface 门禁整改版

日期：2026-07-20（v1–v4 为历史整改记录；v5 为当前架构）
任务编号：NR-03
完成状态：五页探索站、关系层、episode 三语、五条谱系、8个 publication objects 与 core surface 门禁完成
上位依据：`docs/next_round_exploration_system_sessions_v1.md`、`docs/exploration_system_information_architecture_v1.md`（含 §12 修订）、`docs/exploration_system_data_contract_v1.md`

## v5 · 方法门禁整改结论

- 内部 NR-02 adapter 已升至 schema `1.2.0`：121 个可见 actor、141 条已核／142 条研究
  actor–issue 边；LC001–LC005 五条人审生命周期记录进入时间页。LC004／LC005 只显示
  “最后观察到活动”，不写解散；LC006 范围外控制被排除。
- actor class 分组／颜色、region、place→display region 和四个时间分期全部迁入
  `core/presentation/rules.json`。React 不再维护平行研究语义；必需 JSON 缺失会加载失败，不再
  静默替换为空数组。
- 新增唯一发布 seam：`research_publication` 按 `reviewed`／`client_preview`／`internal`
  profile 编译物理隔离、不可变 release。公开 profile 删除本机 archive path/hash 与内部
  复核备注；验证通过后才原子切换 channel。
- `research_publication_core_surfaces_v1.json` 逐文件／逐 JSON pointer 决定所有 core 输出。
  公开站不再复制混合 `demo/relations.json` 或 `research/candidates.json`，未消费旧 views
  也不公开。reviewed profile 物理排除 research、R4 QA-safe 层与 F027。
- Vite 在构建前核对 channel profile、release ID、public flag 和 manifest hash；
  `dist/release.json` 绑定 publication/site release、前端树、base path、Git commit 与 dirty 状态。
- catalog 当前 26 项：8个完整对象、4个有限 core surfaces、5个尚无公开 adapter、5个需继续
  研究、4个永久退役。完整对象为 ARC001/002/003、MR004/005/012/013/014。
- 甲方可见的新增／升格内容包括：五条生命周期、R4 9人审＋10研究观察／5人审＋19研究摘录、
  R5 169条名单观察／21重复身份、R10 616行官方总体、六维覆盖审计和13个六阶段 episode。

当前复现：

```powershell
python scripts\build_publication_snapshot_v1.py --profile client_preview
python scripts\build_publication_snapshot_v1.py --profile client_preview --verify-only
cd prototypes\nr3_explorer
npm test
npm run build
```

权威说明：`docs/research_publication_architecture_v1.md`、`docs/research_publication_asset_audit_v1.md`、
`docs/research_publication_rectification_handoff_v1.md`。

## v3.4 · HR-035 Batch 2 与 episode 三语正式重生

- 当前 build：`4913ff70fa40dfcb`，schema `1.1.0`。中央 294 条 actor–issue 历史边中
  283 条有效，分为 **141 已核／142 研究候选**；四态为 **83 frozen-bounded／
  58 accepted-unfrozen／28 scope-reviewed fact-pending／114 fact-pending**。
- 已核图连接 54/121 个可见 actor，研究图连接 116/121；AI157、AI158 保持
  `needs_second_source` 候选，没有进入已核层。
- strict place–issue 重生为 **306** 条同源三元事实，其中 299 条 E3/E4、81 条双边人审、
  97 条有正式事件附着。
- `data/metadata/episode_display_trilingual_v1.csv` 已成为 NR-02 正式输入：13 个 episode ×
  7 个字段 × 中／日／英＝273 个显示单元，0 缺项、0 空翻译、0 zh 改写、0 运行时回退。
  TE10–TE13 仍是 `analytic_candidate_event_pending`，翻译不改变事实层级。
- 主线程语义审查同时修正 TE01／05／06／07／11 的既有精度问题，包括 caption 当事人边界、
  石垣义务付诉讼门槛、泡濑未来支出、A068→A019 改组边界、PFAS 土壤采样及完整事件号。
- 26 项 adapter tests、2 项前端语言测试与 production build 通过；路径页中／日／英及
  已核／研究切换经实际浏览器复验，控制台 0 error / 0 warning。

## v2.1 收尾整改（对应复验三项）

1. **英文界面中文 UI 残留**：品牌名（中／日／EN）、导航与语言组 aria-label、画布控制 title、
   地图与组织画布 aria-label、地图状态 aria-label 全部进入 `ui_strings.js`；同时按负责人
   批准把界面"演示视图"统一改名为"已核视图"（layer.demo、layer.hint、帮助文案、图例注记）。
2. **A073 与 A002 两条测试拆开**：A073 仅证明"全量 registry 搜索可达"（该 actor 当前
   0 议题／0 事件）；组织→议题→事件→时间链由 A002 等有事件 actor 证明，见下方验证节。
3. **跨路由关闭证据抽屉**：路由改变时清空 drawer selection，旧抽屉不再覆盖新页面。

## v3 组织关系层（2026-07-20，按 `nr3_recheck_and_relation_frontend_brief_v1.md` 实现）

**数据（NR-02 构建模块扩展，`scripts/build_exploration_system_data_v1.py`）**：
类型化集合 `demo/dyadic_relations.json`（14 条 reviewed＝10 supported＋4 supported_bounded，
两端均解析到 registry actor）、
`demo/aggregate_observations.json`（F027＋R10R029）、`demo/case_roles.json`（27 行）、
`demo/administrative_records.json`（6）、`demo/typed_event_participation.json`（4）、
`demo/relation_leads.json`（恒空）、
`demo/genealogy_anchors.json`（恒空）；`research/candidates.json` 新增
`dyadic_relations`（8 条候选）、`administrative_records`（5）、`relation_leads`
（F012/F013/F034/F035）。F008（rejected duplicate）被排除；构建确定性字节一致；
中央表零改动。claim 分层：supported 13、supported_bounded 15、candidate 13、lead 2、
excluded 1。

**呈现（L0＋L1）**：组织面板新增"与其他组织的关系"区（族色芯片、方向箭头、claim 芯片、
supported_bounded 的已确认／缺口两行、金额语义、来源下钻抽屉）与"其他记录与研究线索"区
（行政记录／汇总观察标"非组织关系边"、线索标"非资助事实"）；组织页新增"议题生态／组织
关系"图形状态，关系画布按族着色、箭头表方向、实线已核／虚线候选、族独立开关、边详情卡，
计数按"已确认 · 有限确认 · 待审"分层，无混合总数。

**控制案例实测**：F021 以 supported＋USD 3,250 直接捐赠进入面板与关系图；F025 以
supported_bounded 进入（金额为空，缺口显示"AWWA allocation、奖学金 recipient 待年报"）；
R10R029 只进 X006 面板的汇总观察区（非组织关系边），不上关系图。

截图：`rel_x001_panel.png`、`rel_x004_panel.png`、`rel_graph_demo.png`、`rel_graph_research.png`。

### v3.1 数据版本可见性返工（冻结前历史快照）
- 顶栏新增版本戳：`as_of_date · build_id（短）· 121 组织（122 谱系）`，取自 manifest。
- 组织页类型筛选从"全部类型（N）"改为"当前图中组织（25/121）"；研究视图显示 103/121，
  画布注记追加"18 个无边组织只可搜索"。
- 组织卡显示 evidence_level、review_status、scope_status 状态芯片；X014 明示
  watchlist_only（搜索下拉与面板均标"仅观察名单"）；A072（merged_duplicate）从搜索与
  普通图隐藏。
- build ID 变更检测：每 20 秒及窗口聚焦时核对 manifest，发现新 build 弹横幅提示重新加载。
- 换手计数统一为当前口径：14 条已核关系＝10 supported＋4 supported_bounded；行政记录
  已核 6＋候选 5；另有 aggregate 2、event 4、lead 4、case role 27，不混入组织关系数。

### v3.2 actor–issue 三门状态（冻结前历史快照）

- 构建端派生 `fact_gate_status`／`scope_gate_status`／`schema_freeze_status` 与直接可消费的
  `display_state`，并透传 claim_status、review_scope、reviewed_fields、scope_kind 等 10 个
  中央字段；四态计数精确为 **7（字段已冻结·有限确认）／58（人工接受·字段待冻结）／
  59（范围已审·事实待审）／114（事实待审）**，研究层 fact gate 为 143＋25 待二源＋5 待当地。
- 前端只消费 `display_state` 不重算：议题边行显示四态芯片与待二源／待当地叠加；画布注记
  为"已核 65（7 条字段已冻结）／研究 人工接受 65＋事实待审 173（其中 59 条已完成范围
  复核）"；待审区不再笼统称"未人审"；帮助文案明确"已核＝当前显示的事实边，不是组织身份"。
- HR-019／024／025 均已完成，不重开；HR-035 批次合并后计数随 manifest 自动更新。
- 构建 22/22 测试通过，validation PASS，页面回归零控制台错误。

### v3.3 · 145 项线上决定合并后的正式重生与浏览器复验（历史基线）

- 当前 build 为 `5ed5528a649de4d1`，前端数据已经从正式中央层重生，不再是临时构建。
- 283 条有效 actor–issue 边分为 **125 人审／158 候选**；四态为
  **67 `frozen_bounded`／58 `accepted_unfrozen`／44
  `scope_reviewed_fact_pending`／114 `fact_pending`**。研究事实门为 128 普通待审、
  25 待二源、5 待当地材料。
- 已核图连接 47/121 个可见 actor；研究图连接 116/121，另有 5 个无议题边 actor
  仍可检索。组织身份状态与关系状态继续分开显示。
- strict place–issue 为 **305** 条同源三元事实，其中 71 双边人审、234 候选、
  298 条 E3/E4、97 条有正式事件附着。
- 390×844 下逐页实测总览／组织／时间／路径／证据，五页文档宽度均为 375px，
  无横向溢出；1280×900 桌面端无溢出；页面控制台 0 error / 0 warning。
- 中央已有 5 条可导出的 lifecycle 记录（其中 4 条为本轮 LCR001–004 新决定），但 adapter 仍输出
  `genealogy_anchors=0`。因此时间页的“谱系锚点 0 条”是当前真实的**导出缺口**，
  不是“没有生命周期材料”；L2 必须先把 LC001–LC005 映射成有界记录后再验收。

### v3.3 Post-freeze delta（历史基线，已由 v3.4 取代）

- **中央权威字段**：构建器以
  `15_funding_or_support_edges_sample_v0.csv` 已填的 `claim_status`、
  `confirmed_scope`、`missing_scope`、`graph_eligibility`、`amount_semantics`、
  `reviewed_fields` 等为第一优先；已完成的 HR-033 补充表只补中央空字段，最后才按受控规则
  派生。被负责人
  明确复核为空的字段（如 F025 amount）不得被补充包覆盖。
- **最新数据口径**：registry 保留 122 行历史记录，普通界面只显示 121 active actor；
  A072 为 merged duplicate、`display_status=hidden`，搜索与普通图均不可见。默认 actor—issue
  图为 125 条已核边＋158 条候选边；actor—place 为 53 条已核边＋77 条候选边。AI068 属
  事件限定且明确排除出默认冲绳叙事，不进入已核或研究关系图。strict place—issue 为
  305 条总三元组（71 条双人审＋234 条候选；其中 298 条为 E3/E4，97 条有正式事件附着）。
- **关系层计数**：43 条中央观察＋R10R029 独立汇总观察＝44 输入；已核层为 14 条组织关系、
  6 条行政记录、2 条汇总观察、4 条事件参与记录、27 条案件角色；研究层为 8 条候选组织
  关系、5 条行政候选、4 条研究线索。F036 只显示为事件参与，F011/F040/F041 同样不派生
  稳定组织关系边。
- **中央关系状态**：43 条中央观察分别为 `human_checked` 18、`human_revised` 8、
  `ai_seeded` 12、`needs_second_source` 2、`needs_local_retrieval` 2、`rejected` 1。
  这些中央状态计数不能替代上述 endpoint／claim／graph gate 后的前端集合计数。
- **组织身份状态**：121 个普通界面可见 actor 中，32 个身份行为
  `human_checked`／`human_revised`，其余 89 个仍为 `ai_seeded`、二源不足或待当地材料。
  “已核视图”只表示当前显示的关系／主张经过 gate，不表示 121 个组织身份全部完成人审。
- **前端回归**：组织类别筛选同时作用于议题生态图与组织关系图；`RecordRow` 显示
  amount semantics；女性组织类与 P021 先岛节点有中／日／英标签；案件角色明确标注
  “非协作边”。
- **复现与测试**：

```powershell
python scripts\build_exploration_system_data_v1.py
python -m unittest tests.test_build_exploration_system_data_v1
python -m unittest discover -s tests
cd prototypes\nr3_explorer
npm run build
```

不得把行政记录、汇总金额、事件参与或同案角色计入组织关系；不得把
`supported_bounded` 的金额／期间缺口补成事实；不得让 rejected、duplicate、E0、AI068
或 A072 回到默认展示。

## v2 整改清单（历史验收快照；当前计数以 Post-merge delta 为准）

| 验收意见 | 整改 |
|---|---|
| 地区面板无 episode 入口 | 地区面板新增"相关 episode"区（按地点匹配，含研究层待审），点击直达路径页对应 episode；地图→地点→episode→证据链闭合 |
| 演示层当时只能搜 23 个 actor，17 个 edge-isolated 不可搜 | v2 当时改为全量 122 条 registry 记录可搜；合并 A072 后，当前普通界面为 121 个可见 actor（名称／别名／ID 匹配），A073 仍实测可达 |
| 组织详情无事件列表 | 组织面板新增"事件记录"区（事件名、年份、动作类型），点击跳时间页对应年份；组织→议题→事件→证据链闭合 |
| 比较功能缺失 | 新增两处同字段比较：地区对比（总览面板双列指标与议题）、episode 对比（路径页六阶段并排，TE01↔TE03 实测） |
| 证据抽屉无 locator | 抽屉卡片新增 locator（archive_path，等宽字体） |
| 390px 不可用 | 新增 ≤820px 移动断点：顶栏换行、页面单列、画布定高、路径轨横滚、抽屉全宽；390×844 实测无横向溢出 |
| "13 个已核 episode（含待审）"措辞错误 | 改为"已核 9 ＋ 待审 4 · 11 类路径" |
| 英文证据页残留中文标题／维度名 | D1–D6 维度名进入 `ui_strings.js` 三语表 |
| 地图区域按钮在 aria-hidden 容器内 | 已移除该属性；搜索下拉提供键盘可达的组织选择路径 |
| 换手截图 9 张仅 7 张不同 | 截图流程修正（每次截图前强制刷新重置 SPA 状态）并逐对校验 md5 不同，见下方"页面截图" |
| workbench 把已完成项列为待办、保留已取消的检查点 B | `docs/phase1_workbench.md` 下一步 4–7 条已更新 |

## v2／v2.1 完成项（交付沿革；下列计数已按当前构建口径校正）

- 五个页面全部上线：总览 `#/`、组织 `#/actors`、时间 `#/time`、路径 `#/pathways`、证据 `#/evidence`。
- 总览（V1）：42 市町村 GeoJSON、点选陆地选区、滚轮缩放（以光标为中心）、拖拽平移、区域标签随地理锚定；全域／先岛聚焦两状态；面板含指标、议题入口（跳组织页）、相关 episode（跳路径页）、地点标签；地区对比模式。
- 组织（V2）：141 条已核 actor—issue 边为默认层；普通界面搜索 121 个可见 actor（中央
  provenance 仍保留 122 行，A072 隐藏；搜索含别名与 ID）；类型／议题筛选；节点详情
  （议题、地点、事件记录、身份来源）；画布缩放平移。
- 时间（第五页，历史 v2 状态）：一期方案四个时段节点、12 个已核事件按年组织、参与者跳组织页；
  当时尚为0个谱系锚点；当前 v5 已导出 LC001–LC005 五条。
- 路径（V3）：9 个已核 episode 六阶段阶梯，状态直读数据；episode 六阶段对比；参与组织、来源、关联案件。
- 证据（V4）：六维度 120 个当前生成单元，facet 条形与来源类型×归档矩阵，机制解释面板；
  单元数是生成结果，不是稳定契约。
- 研究视图：已核／研究全局开关，142 条候选议题边（虚线）＋225 条候选 strict
  place—issue 三元组＋77 条候选地点边＋4 个候选 episode＋4 条分析种子，全部带待审标记；
  措辞经专项修正。
- 三语：数据代码经 `data/metadata/display_label_mapping_draft_v0.csv`（229 码，负责人审定）生成的 `labels.js`；UI 文案在 `ui_strings.js`；中／日／EN 切换默认 zh，数据与界面文案均整页切换。
- 证据抽屉：来源标题外链、类型、等级、复核状态、来源年份、支持内容、归档状态、locator、偏向提示、解释边界；`can_support_claim=false` 单独标记。
- 390px 与 1280px 双宽度可用；设计规范：图名即标题、读法收"?"弹层、七档字阶、无临时文案、无死按钮。

## 新增或修改文件

- `prototypes/nr3_explorer/src/`（全部前端实现与样式）。
- `prototypes/nr3_explorer/AGENTS.md`：仅保留持久设计规则。
- `data/metadata/display_label_mapping_draft_v0.csv`：229 码三语映射（建议 NR-02 重建时纳入构建输入）。
- `docs/exploration_system_information_architecture_v1.md` §12、`docs/phase1_workbench.md`、`design-qa.md`。
- 未改动：中央研究表、NR-02 构建脚本与数据包、其他 outputs。

## 关键计数与验证

- 构建 `npm run build` 通过；浏览器控制台 0 error / 0 warning。
- 数据隔离：122 条 actor provenance／121 个普通界面可见 actor；9 个已核 episode；
  TE10–TE13 仅在 research；A094 未进入；S051 保持 E0、不可支持主张。
- 探索链 A（地图）：地图→地点（选区）→episode（面板入口）→来源（路径页芯片→抽屉）实测通过。
- 探索链 B（组织）：A073 实测证明 121 个普通界面可见 registry actor 可搜索（该 actor
  当前 0 议题／0 事件，不承担事件链）；A072 仅作隐藏 provenance tombstone；A002 实测
  证明组织→议题→事件记录→时间页 2003 链通过。
- 比较：地区双列（全部区域 vs 八重山群岛）与 episode 六阶段对比（儒艮海外诉讼 vs 嘉手纳第三次噪音诉讼，12 格）实测通过。
- 研究措辞："已核 9 ＋ 待审 4"；英文证据页维度名全部英文；抽屉含 locator。
- 390×844：五页文档宽度均为 375px，无横向溢出、无页面错误；1280×900 桌面布局不变。
- 截图证据：本文件下方 12 张，demo/research 成对文件 md5 均已校验不同。

## 运行／复现命令

```powershell
cd D:\冲绳研究\ngo_network_project\prototypes\nr3_explorer
npm install
npm run dev -- --port 4173   # http://localhost:4173/
npm run build
```

前端数据来自活动 `client_preview` publication channel；`npm run dev`／`npm run build`
会自动重建并验证。`outputs/exploration_system_data_v1/` 只是内部 adapter，不得直接部署。

## 页面截图

### 总览（演示视图）

![总览·演示](nr3_handoff_assets/handoff_overview_demo.png)

### 总览（研究视图）

![总览·研究](nr3_handoff_assets/handoff_overview_research.png)

### 总览（地区对比）

![地区对比](nr3_handoff_assets/handoff_region_compare.png)

### 组织（演示视图）

![组织·演示](nr3_handoff_assets/handoff_actors_demo.png)

### 组织（研究视图）

![组织·研究](nr3_handoff_assets/handoff_actors_research.png)

### 时间

![时间](nr3_handoff_assets/handoff_time_demo.png)

### 路径（演示视图）

![路径·演示](nr3_handoff_assets/handoff_pathways_demo.png)

### 路径（研究视图）

![路径·研究](nr3_handoff_assets/handoff_pathways_research.png)

### 路径（episode 对比）

![episode 对比](nr3_handoff_assets/handoff_episode_compare.png)

### 证据（演示视图）

![证据](nr3_handoff_assets/handoff_evidence_demo.png)

### 证据（英文界面）

![证据·EN](nr3_handoff_assets/handoff_evidence_en.png)

### 证据抽屉（含 locator）

![证据抽屉](nr3_handoff_assets/handoff_evidence_drawer.png)

## 未决人工判断

- episode 三语映射已完成语义审查并纳入 NR-02 构建输入及 input hash；其他非 episode
  数据字段的翻译仍按各自数据层任务处理。
- LC001–LC005 已完成有界导出；NR-04／NR-05 的新增历史候选仍不得直接进入已核层。
- 部分来源 supports／bias_note／interpretation_limit 仍为数据层原文字段；episode 的
  7 类内容已全部由正式三语 overlay 提供。
- 画布节点本身不可键盘聚焦（canvas 技术限制）；键盘与读屏路径由搜索下拉、区域按钮和各页 DOM 面板提供。
- 部署未授权。

## 已完成的前端语义整改（v3.1 历史记录）

- 保留负责人已经批准的“已核视图”名称，但帮助文案须明确：**已核的是当前显示的
  关系／主张，不是所有可搜索组织的身份**。
- 组织卡／详情面板显式显示 actor 自身的 `review_status`、`evidence_level` 与
  `scope_status`；不得用关系 gate 替代身份状态。
- `X014` 当前为 `watchlist_only`。依据负责人已批准的“不完全证据也可展示”规则，
  可以在检索／研究语境中保留，但必须显示 watchlist 标签，且没有已核关系边时不得
  因可搜索而被读成当前网络成员。

## 不得被主线程误读为

- 已核层≠全量数据：普通界面有 121 个可见 actor，但已核议题网络只使用 141 条已核边；
  它是“可公开辩护”的关系子集，不能用 actor provenance 行数替代关系 gate。
- 研究视图的虚线与待审项是候选，不是事实；共同联署与同场参与不是稳定联盟。
- 时间页时段节点是一期方案的采集策略，不是数据断言；事件年份不代表组织成立或持续。
- 地图只有市町村几何，没有基地／组织点位；区域颜色不表示组织密度或活动强度。
- 证据页计数是工作样本的文献可见度，不是冲绳民间组织总体分布。
- 前端不读中央 CSV，不改中央表；`PLACE_DISPLAY_REGION` 与七组分类映射为展示层，不反写。

## 建议下一 session

- 仍有9个方法模块缺完整 adapter：其中 MR001/003/008/011 已有有限 core surface，MR002/006/007/009/010
  尚无公开模块表面；按解释价值逐项推进，不得批量搬图。
- episode 三语任务已经完成，不再重开；后续如扩展 episode，必须同步扩展 13×7 精确网格门禁。
- 完成上节“组织身份状态≠关系已核”的面板提示与 X014 watchlist 标签。
- 5 分钟演示路径文档可在 NR-06 验收前补齐。
