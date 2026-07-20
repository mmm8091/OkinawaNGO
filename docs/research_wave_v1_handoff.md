# 选题探索波次 v1 换手

日期：2026-07-20
状态：第一轮 H1／H2／H3 pilots 完成；等待负责人选题检查点
范围：独立 `research_only` 输出；中央事实层、现有 exploration builder 和前端均未改动

## 1. 这一轮真正得到什么

### H1 高承载名单与可见层来源依赖

- E3/E4 基线为 234 条 actor–issue 边、101 个可见 actor。
- 去掉 S003／S004／S006 的独占证据支持后为 185／71；只去掉配对的 A001／A004／A005 节点则为 227／98。两种删除单位不同，只能描述性并列，不是匹配反事实。
- 最强单源敏感性来自 S004：234／101 降为 193／76。
- 三源删除损失约 84% 由 S004 单独造成；当前首先是单一 2015 高承载名单的来源集中，不是三类资料宿主反复呈现的机制。
- 234 条 E3/E4 边中有 12 条没有可解析的 `S` 来源，按保守规则在 source-ID 删除中存活。
- 当前只能说明“观测到的跨议题结构依赖少数高承载资料入口”，不能说明真实社会网络因此断裂，也不能把 issue degree 当影响力。
- 已补 E3/E4 actor–issue edge×source 下钻、逐场景删边明细、全来源 leave-one-out 和 6 项后续任务；registry actor×source 表仍不是完整的资料生产／托管关系宇宙。

### H2 基地周围两套功能生态

- 透明规则得到 9 个基地社区服务／军属慈善比较 actor；它们只是 registry 子集，不是服务生态总体。候选锚点规则得到 65 个限制／问责候选 actor，其中 18 个至少有一条人审锚点边、47 个只由候选边选入。
- 14 条已核＋8 条候选 dyadic、4 条 typed-event 与 35 条 R10 目的性记录中，直接跨组组织关系均未编码；27 条 case role 中没有服务侧 actor。这些不同目的性小样本不是独立普查。
- 两组共享全县宽节点 P001 与嘉手纳 P005；只有 P005 是具体共址线索，共址仍不等于接触。
- 人物共享没有系统表，完整 recipient 网络也未取得；两者必须写成 `not_measured`，不能写“没有”。
- “基地生产两套 NGO”仍是因果假设；当前只支持功能并存和公开关系记录稀少。

### H3 前线化／战争记忆共同语言

- 建立 12 条带正文定位的候选语句、6 条事件限定载体、17 条事件参与／赞同记录。
- 当前只支持 A018 与 A100／A108 之间的事件级接触或组织载体候选，以及 A101 活动中的事件性跨议题赞同；传播方向和目标组织独立采用未确认。
- 当前不平衡语料不能检验词汇是否随时间增长；现有证据也不能证明扩散或稳定共同运动。
- 一条原先命中网页 metadata 的观察已改为正文 `S022 raw.html:L347`，并由测试锁定 locator 与 excerpt 同行。
- S119 的 manifest 仍为 failed 但本地 raw 存在；S022／S036／S119 的 source-log 日期或标题也需校正。这三项已单列 source-governance gate，没有静默改中央表。

## 2. 学界接口后的选题排序

1. H3：保留为实证 pilot，不预定主论文。四项直接先行研究已经覆盖 A017、A108、石垣“不让岛成为战场”和军扩—冲绳战类比；可能的新意只剩统一的组织—事件比较、载体／独立采用区分、负案例和重复事件检验。
2. H2：高原创性第二候选，但下一轮必须先找人物、recipient 和反例；不能靠“0 条边”写隔绝论。
3. H1：所有网络结论的强制方法校正；是否独立成文取决于 producer／host／language／lifecycle 字段能否补齐。
4. 其他七个方向已在 `topic_register_v1.csv` 记录为子设计、对照或 outcome，不再把一期既定问题包装成新发现。

## 3. 交付与结构

- 总说明：`docs/research_wave_topic_selection_v1.md`
- 选题与文献：`outputs/research_wave_topic_selection_v1/`
- H1：`outputs/research_wave_h1_documentation_visibility_v1/`
- H2：`outputs/research_wave_h2_two_ecologies_v1/`
- H3：`outputs/research_wave_h3_frontline_memory_v1/`
- 模块目录索引：`outputs/research_wave_topic_selection_v1/frontend_research_modules_v1.json`

索引状态为 `module_index_ready_observation_exports_gated`。它只列模块、指标与可下钻资产，不是行级 frontend contract；三包均为 `not_frontend_ready`。它没有写入 `outputs/exploration_system_data_v1/`，也没有改变现行 reviewed／candidate／relation 契约。

## 4. 人工与当地任务

- 选题强度与预算：`outputs/research_wave_topic_selection_v1/principal_checkpoint_v1.md`
- H1：3 个 source-host 配对仍为 `proposal_not_human_reviewed`。
- H2：`human_review_queue_v1.csv` 7 项；`further_search_queue_v1.csv` 9 项，其中人物表、recipient 与当前 private-organization/service universe 为 P0。线上初查已发现官方 MCIPAC/MCCS 名录及尚未入 registry 的 North Island Okinawa Spouses' Club 线索；这进一步证明现有 9 个 actor 只是比较子集，不是服务生态总体。
- H3：`human_review_queue_v1.csv` 9 项；`local_retrieval_queue_v1.csv` 4 项，其中先岛原始组织文本和与那国早期材料为 P0；新增 source-governance／主语归属与四项直接先行研究的新意门禁。

这些队列尚未回写现有 HR 总账；只有负责人选定第二轮方向后，才编号并并入统一人工任务书，避免同时把三个论文方向都变成大规模人工负担。

## 5. 复现与验证

```powershell
python scripts\make_h1_documentation_visibility_v1.py
python scripts\make_h2_two_ecologies_v1.py
python scripts\make_h3_frontline_memory_v1.py
python scripts\build_research_wave_index_v1.py
python -m unittest discover -s tests -v
```

三个生成器和模块目录构建器都只读现有事实层、写各自独立输出。正式选题前不得把候选观察升级到中央表、已核前端或对外定论。
