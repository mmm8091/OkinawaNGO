# 探索系统前端数据契约 v1（NR-02）

日期：2026-07-20
状态：implemented / validation PASS  
产品输入：`docs/exploration_system_information_architecture_v1.md`  
构建模块：`scripts/build_exploration_system_data_v1.py`

## 1. 契约目的

本契约在中央研究表与前端之间建立唯一数据 seam。前端不直接读取中央 CSV，不现场判断
哪些边可以显示，也不自行把来源、事件、时间和解释强度拼成结论。

唯一构建 interface：

```python
build_exploration_system_data(project_root: Path, output_dir: Path) -> manifest
```

命令行：

```powershell
python scripts\build_exploration_system_data_v1.py
```

该模块负责读取、归一化、来源 ID 映射、demo/research 分层、五页 view model、展示规则、
验证、哈希与输出。派生数据只写 `outputs/exploration_system_data_v1/`，不反写中央研究表。
它是内部 adapter；公开前还必须经过
`docs/research_publication_architecture_v1.md` 定义的发布编译层。

## 2. 数据流

```text
中央 registry / taxonomy / edge / event / case / evidence / source 表
  + 已核模块派生表（strict triples / translation episodes / coverage）
  + source crosswalk / archive manifest
  → 单一构建模块
  → demo 核心对象与关系
  → research 候选隔离层
  → P1–P5 view model + presentation contract
  → manifest + validation report
  → profile-gated immutable publication snapshot
  → render-only frontend
```

`manifest.json` 记录全部输入哈希和生成文件哈希。构建不写当前时间，输入不变时输出字节
稳定。

## 3. 输出目录

```text
outputs/exploration_system_data_v1/
  manifest.json
  validation_report.md
  demo/
    actors.json
    places.json
    issues.json
    episodes.json
    venues.json
    outcomes.json
    evidence.json
    historical_anchors.json
    relations.json
    dyadic_relations.json
    case_roles.json
    typed_event_participation.json
    administrative_records.json
    aggregate_observations.json
    relation_leads.json
    genealogy_anchors.json
    map_geometry.geojson
  research/
    candidates.json
  views/
    overview.json
    actors.json
    pathways.json
    evidence_coverage.json
    time.json
    presentation.json
    global.json
```

前端应优先读取 `views/*.json` 决定某页使用哪些 ID，再从 `demo/*.json` 取得对象与关系。
研究层只有在用户显式切换后读取。

## 4. 通用字段

可展示对象和关系尽量共享以下字段：

| 字段 | 语义 |
|---|---|
| `id` | 稳定对象或关系 ID |
| `display_label` | 前端短标签；不等于解释结论 |
| `display_summary` | 版本化一行短命题；不存在时不得由前端补写 |
| `display_status` | `demo` / `research` / `infrastructure` |
| `review_status` | 保留中央表或模块表的原始状态 |
| `evidence_level` | E0–E4；与 review_status 分轴 |
| `source_ids` | 已解析到中央 source log 的 ID |
| `unresolved_source_refs` | 只允许留在 research 层的旧引用 |
| `interpretation_limit` | 事实旁必须可见的解释边界 |

数组都按稳定 ID 排序；JSON key 排序；文件以 UTF-8 和 LF 写出。

## 5. 核心对象

### actor

来源：中央 actor registry。

中央 registry 的 122 条 provenance 行及 39 条 alias 全部进入 `demo/actors.json`，但
A072 是已并入 A071 的 duplicate tombstone，`display_status=hidden`；普通界面、搜索和
网络只显示其余 121 个 active actor。这里的准入是“保留在中央 registry／provenance”，
不等于每个分类字段和关系都已经人审。

因此：

- actor 保留原始 `review_status`；
- 关系必须独立通过关系 gate；
- `ai_seeded` actor 不会因此带入 `ai_seeded` actor–issue / actor–place 边；
- event-only、individual、institution 和 provisional procedure node 不进入 actors 集合。

### place / issue / venue

来自受控 taxonomy。它们是导航与编码对象，不是事实主张。`why_relevant` / `definition`
进入 `display_summary`，不由前端另写地区文章。

总览地图几何来自既有简化 municipal GeoJSON，共 42 个 Polygon/MultiPolygon feature，
随构建复制为 `demo/map_geometry.geojson` 并进入输入/输出哈希。当前 place registry 有
21 个 place／field 节点，但没有
逐地点经纬度或已核 municipality crosswalk，因此 NR-03 只能先做区域级地图选择，不得
自行猜测基地、湾区或组织的精确点位。

### episode

来源：translation episode comparison。

- demo：6 个 `human_checked` R8 episode、2 个 `accepted_process` R9 episode、1 个
  `accepted_process_with_local_gap` episode，共 9 个；
- research：4 个 `analytic_candidate_event_pending` HR-027 episode。

module-specific `R9Sxxx` 来源引用通过 source crosswalk 映射回中央 `Sxxx`，同时保留
`module_source_refs` 供审计。

### outcome

每个 episode 派生三类 outcome：

1. `intermediate_output`
2. `bounded_gain`
3. `underlying_change`

状态只使用 `yes / mixed / no / unknown`。前端不得把中间产出自动升级为有限结果或底层改变。

### evidence

`evidence.json` 包含：

- `sources`：295 条中央 source log 记录，并附 archive status/path/hash；
- `notes`：49 条正式 evidence notes。

所有 source 都可用于覆盖审计，但 `E0` 或 rejected source 的 `can_support_claim=false`。
S051 因 archive/domain mismatch 不能支持任何可见 claim。

### historical_anchor / genealogy_anchor

当前默认层包含 LC001–LC005 五条 `resolved` 且 `human_checked`／`human_revised` 的中央
生命周期记录：两条解散、一条有界重组、两条“最后观察到活动／连续性未闭合”。LC006 是
范围外控制，不进入展示。最后观察日期不是解散日期；重组也不等于简单改名、合并或不间断
同一性。新增 NR-04／NR-05 候选仍须经过相同人工门禁。

## 6. 关系集合与分层规则

`demo/relations.json` 当前包含：

| 关系 | demo gate | 当前数 |
|---|---|---:|
| `actor_issue` | `human_checked` / `human_revised` | 141 |
| `actor_place` | 人审且 place key/label 一致 | 53 |
| `strict_place_issue` | 两侧均人审且同一来源 | 81 |
| `actor_episode` | 由 9 个 demo episode 派生 | 15 |
| `event_participation` | `human_checked` | 63 |
| `legal_roles` | 六案 27 条人审角色 | 27 |

AP123 的旧快照曾出现 `place_id=P006`／`place_name=Camp Foster` 冲突并被隔离；HR-025
已把它修订为 P007 Camp Foster。当前构建使用 53 条已核 actor—place 边，旧的 16／17 条
计数只属于 pre-HR-025 历史快照。

`research/candidates.json` 当前隔离：

- 142 条 actor–issue；
- 77 条 actor–place；
- 225 条 strict same-source 候选；
- 4 条 analytical event participation；
- 4 个候选 episode 及其 4 条 actor–episode、12 个 outcome。

8 个 registry actor 仍带非中央 `Xxxx` 身份引用；research 关系层当前涉及 9 个不同旧
代码。它们保留为 `unresolved_source_refs`，但不会伪装成中央 `source_ids` 或进入 demo
关系的证据链。

## 7. event-only 与 provisional 节点

63 条 human-checked event participation 中有 13 条不是 registry actor：

- 9 个 unverified event participant；
- 3 个 individual；
- 1 个 institution。

它们只作为带 `entity_type`、`is_registry_actor=false` 的参与记录出现，不进入
`actors.json`，不能在组织页计数、搜索结果或网络节点中冒充组织。

27 条 legal role 同样区分 registry actor 与 provisional procedure node。前端必须显示
`entity_kind`，不得把 counsel、plaintiff、requester、supporter 合并成一种“参与者”。

## 8. 五页 view model

### P1 `overview.json`

提供：

- 21 个 place ID 与 region 分组；
- 42 个 municipality polygon 的正式前端几何文件；
- 26 个 issue ID；
- 53 条无键名冲突的 demo actor–place；
- 81 条双人审同源 strict place–issue；
- `all_regions / sakishima_focus / compare` 三种状态。

地图本身只做地理导航；严格地点—议题三元组在地区详情中显示并可回到来源。

### P2 `actors.json`

提供：

- 122 条 registry provenance，其中 A072 隐藏、121 个 actor 可见；
- 141 条 demo actor–issue；
- 15 条 demo actor–episode；
- actor class、origin、legal status、place、issue 与 review status 筛选字段。

节点面积、度数或重复出现不能命名为影响力。

### P3 `pathways.json`

提供：

- 9 个 demo episode；
- 16 类 venue；
- 63 条 event participation；
- 27 条 legal role；
- route family 与固定 stage order。

固定阶段是读图语法，不是因果证明。

### P4 `evidence_coverage.json`

提供 coverage audit 的 D1–D6 六个维度 category cells 与 6 条 implication。2026-07-20
当前层重生后的 cell 数只是一项生成结果，不是前端契约；精确分类或 workflow 状态变化时可
增减。契约只固定六个 dimension、字段语义和解释边界。计数单位按 cell 保留，前端不得跨
dimension 相加，也不得把覆盖率解释为冲绳民间组织总体分布。当前默认统计使用 121 个有效
actor、283 条 `analysis_inclusion=active` actor–issue 边和 130 条
`graph_eligibility!=excluded` actor–place 边；122／294／135 的中央历史行仅作为审计边界。

### P5 `time.json`

提供一期方案的四个时间分期、正式事件锚点和 LC001–LC005 五条有界生命周期锚点。事件年份
不能推断组织成立或持续；`last_observed_activity` 只能视为下界。

### `presentation.json`

提供 actor class 分组和颜色、地区颜色、place→display region 映射及四个时间分期。以上均
是受控展示语义，React 不再自行维护平行常量。

### G1/G2 `global.json`

提供：

- event anchor；
- coverage period；
- 五条有界 historical anchor；
- evidence drawer 必需字段；
- 跨页选择状态键。

## 9. 日期契约

日期语义禁止混用：

| 字段 | 用途 |
|---|---|
| `source_publication_date` | 来源发布或页面年份 |
| `event_date` | 事件或程序发生时间 |
| `claim_period` | 主张适用时期 |
| `actor_active_from/to` | 组织活动期；当前数据缺失时保持空 |

前端不得用 source publication date 填补 event date，也不得用事件年份推断组织成立或持续。

## 10. 验证门禁

构建失败条件包括：

- 核心对象重复 ID；
- demo/research episode 重叠；
- actor / place / issue / venue / episode 孤儿引用；
- legal role case orphan；
- demo source ref 无法解析；
- candidate 或 analytical episode 泄漏 demo；
- event-only 名称进入 actor 集合；
- E0 source 可支持 claim；
- archive manifest 缺 source；
- coverage 六维不完整；
- demo actor-place 的 place ID/name 冲突。
- lifecycle actor/successor 孤儿、非法状态或 LC006 泄漏；
- presentation actor class 未覆盖、地点映射无效或时间分期重叠。

当前验证：PASS，0 errors。warnings 是显式研究边界，不自动改写中央表。

## 11. NR-03 消费规则

NR-03 只允许：

1. 从活动 publication snapshot 的 `views/exhibits.json` 和 `views/core_surfaces.json` 取得合法对象；
2. 从编译器生成的 `core/**` 精确投影取得默认对象与关系；
3. 在显式研究层按族读取 `research/*.json`，不得读取混合 `research/candidates.json`；
4. 使用 `interpretation_limit` 和证据抽屉显示边界；
5. 使用全局选择状态跨页传递 actor/place/issue/episode/time；
6. 从 `core/presentation/rules.json` 读取分类、地区与时间展示语义。

NR-03 不允许：

- 重新读取中央 CSV；
- 在浏览器内按 review status 自行决定 demo gate；
- 根据 source 数、degree 或共同出现生成影响力、联盟或成功率；
- 为具体地区、组织、episode 另建手写内容文章；
- 根据事件年份或来源年份补写组织生命周期。

## 12. 已实现的关系状态扩展（2026-07-20）

本节原为下一版构建契约。HR-033 合并、NR-02 构建扩展和 L0／L1 前端现已实现；当前
`outputs/exploration_system_data_v1/` 已生成并验证以下类型化集合。L2 已接入五条中央
已核生命周期锚点；NR-04／NR-05 新候选仍不得自动进入。

- 用户界面的 `demo` 改称“已核视图”；内部目录名可为兼容暂时保留；
- evidence level、review status、human decision、claim status、graph eligibility 和
  display tier 分轴；
- 已核视图包括 `supported` 与 `supported_bounded`；
- `supported_bounded` 必须输出 `confirmed_scope`、`missing_scope` 和
  `interpretation_limit`；
- 关系输出拆为 `dyadic_relations`、`case_roles`、`event_participation`、
  `administrative_records`、`aggregate_observations`、`relation_leads` 和
  `genealogy_anchors`；
- 六条 legacy `verified` 关系已由 HR-033 逐条决定，中央旧值已清零；不得按旧
  `verified` 字符串自动进入已核层；
- 前端继续只消费构建结果，不自行根据中央 `review_status` 计算展示资格。

当前输入与验证依据：

- `data/metadata/coding_schema_v1.md`
- `docs/actor_relation_architecture_v1.md`
- `docs/nr3_recheck_and_relation_frontend_brief_v1.md`

当前关系构建计数：

- 44 条输入观察＝43 条中央关系／支持记录＋R10R029 独立汇总观察；
- 已核层：14 条 dyadic relation、6 条 administrative record、2 条 aggregate
  observation、4 条 typed event participation、27 条 case role；
- 研究层：8 条 candidate dyadic relation、5 条 administrative candidate、4 条
  relation lead；
- 生命周期层：5 条 reviewed genealogy anchor，LC006 排除；
- 中央 43 条状态：`human_checked` 18、`human_revised` 8、`ai_seeded` 12、
  `needs_second_source` 2、`needs_local_retrieval` 2、`rejected` 1。

中央状态计数与前端集合计数不可相加或互相替代；后者还经过 endpoint、claim 和 graph
eligibility gate。

## 13. 发布层与前端边界（2026-07-20）

Vite 不再把本内部 adapter 目录整体复制进站点。`research_publication` 编译器先按
`reviewed`／`client_preview`／`internal` profile 生成物理隔离、不可变的发布快照；公开
profile 删除本机 archive path/hash 和内部复核备注。校验通过后只原子更新 channel 指针。
前端缺必需 JSON 时直接报错，不再把缺文件静默当作空数据。

内部 builder manifest 只证明输出的 provenance，不授予公开资格。每个 builder output 必须由
core surface registry 明确决定；混合 `demo/relations.json` 和 `research/candidates.json`
按 JSON pointer 投影后才可发布，未消费旧 views 不进入 public profile。

`npm run build` 会依次重建发布快照、核对 channel profile/release/manifest hash、构建站点，
并写入绑定数据 release、前端源码、Git commit 和 base path 的 `dist/release.json`。准入
catalog 与完整规则见：

- `data/metadata/research_publication_catalog_v1.json`
- `data/metadata/research_publication_core_surfaces_v1.json`
- `data/metadata/publication_release_profiles_v1.json`
- `docs/research_publication_architecture_v1.md`
