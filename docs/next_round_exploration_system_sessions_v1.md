# 下一轮线上任务总书 v1：研究架构、前端探索系统与早期组织演变

日期：2026-07-18  
状态：待项目负责人按 session 分派  
权威上位文件：`source_docs/current/复归后冲绳民间组织 _ NGO 分类与议题网络一期研究方案 (3).docx`

## 0. 本轮目标

本轮不继续扩充“更多组织、更多来源、更多图”，而是把一期已经形成的材料压缩为一套可导航、可比较、可追溯的研究系统，并对最影响“复归后”长期主张的 1972–2012 时间缺口做两次有界线上补查。

本轮主线：

> 研究架构冻结 → 前端数据契约 → 可点击前端演示 → 1972–1997 补缺 → 1998–2012 补缺 → 证据集成与演示验收

本轮完成后应当能让甲方自行完成以下动作：

1. 找到一个组织，理解其类型、时期、议题、地点、事件和证据；
2. 从实际地图进入一个地点，查看当地问题如何被组织翻译并进入制度场域；
3. 比较两个地点或两类制度路径；
4. 从一个判断下钻到来源、定位、证据等级和人工复核状态；
5. 清楚区分“同期一手材料、后来回顾、二手重建、线索、当地缺口”；
6. 看见 1972–2012 的历史锚点和空白，而不是被一条虚假的连续时间线误导。

## 1. 从一期方案继承的产品结构

一期方案有三个基础问题：

1. 冲绳有哪些相关民间组织？
2. 这些组织如何分类，哪些组织连接多个议题？
3. 在关键地点，环保、生活安全、自治和军事设施争议如何在组织层面连接？

“1972 年复归以来如何形成、重组和扩展”构成第四条纵向问题。

经负责人 2026-07-18 检查点 A 决定，前端固定为四个主展示页，而不是按已有图表建立
十几个页面：

| 主页面 | 主要对应模块 | 要回答的问题 | 主可视化 |
|---|---|---|---|
| 总览 | R3／R4 | 哪里正在发生什么？ | 全域地点—议题研究地图 |
| 组织 | R1／R2（R11 外来 actor 分面） | 谁在参与，以什么功能参与？ | 组织—议题生态图 |
| 路径 | R5–R11 | 行动如何进入事件与制度场域？ | 问题—行动—场域—产出路径图 |
| 证据 | evidence／coverage 基础层 | 当前材料能支持什么、遗漏什么？ | 证据覆盖与偏差图 |

历史演变不另设第五个主页面，而是四页共用的时间层；单条来源核对使用全局证据抽屉。
详情和比较是当前主图的状态、右侧面板或 URL 参数，不增加并列页面。

所有入口最终使用同一数据骨架：

```text
组织 Actor
  ↕
地点 Place — 议题 Issue — 事件 Episode
  ↓
制度场域 Venue
  ↓
中间产出 / 有限结果 / 底层改变 Outcome
  ↓
证据 Evidence
```

原方案列出的“项目介绍、组织分类、组织—议题、地点—议题、法律／国际样本、下载、方法、
更新日志”等页面不再逐项平铺，而是收束进上述四页。前端是中央研究数据经唯一适配层生成
的自动化可视化客户端，不为每个页面或案例另写长文。

## 2. 全局规则

每个 session 开始前必须阅读：

1. `AGENTS.md`
2. `docs/phase1_workbench.md`
3. 本任务总书
4. 自己任务中列出的输入文件

所有 session 共同遵守：

- 不以 registry、source 或 edge 数量增长作为完成标准。
- 不启动无目标的大范围检索。
- 不把候选关系当正式关系，不把共同出现当稳定联盟。
- 不把 `analytical_seed`、事件候选和人工待审项混入默认展示层。
- 不直接重写中央 registry／edge／source 表，除非任务明确授权。
- 新的派生数据写入独立目录，保留来源表、生成脚本和验证报告。
- 必须区分 `source_publication_date`、`event_date`、`actor_active_period` 和 `claim_period`。
- 每个 session 结束时提交一份 handoff：改了什么、生成了什么、未决事项、运行命令、禁止主线程误读的边界。
- 不 commit、不 push，除非主线程另行明确授权。

默认展示分两层：

- **演示层**：只显示正式表、人审事实或来源边界已经冻结的结果。
- **研究层**：可以查看候选、缺口和敏感性，但必须有显式状态标记，不得默认开启。

## 3. 依赖关系

```text
NR-01 研究信息架构冻结
  └─ NR-02 前端数据契约与适配层
       └─ NR-03 可点击前端最小演示

NR-03 通过负责人检查后
  ├─ NR-04 1972–1997 线上历史补缺
  └─ NR-05 1998–2012 线上历史补缺

NR-03 + NR-04 + NR-05
  └─ NR-06 证据集成、红队 QA 与演示验收
```

NR-04／NR-05 可以技术上与 NR-02／NR-03 并行，但不得直接写入前端默认层；必须等 NR-06 和负责人检查后再集成。

| 任务 | 依赖 | 可否并行 | 当前状态 |
|---|---|---|---|
| NR-01 信息架构 | 无 | 必须最先完成 | checkpoint_A_approved |
| NR-02 数据契约 | NR-01＋检查点 A | 不与 NR-01 并行 | complete |
| NR-03 前端演示 | NR-02 | 不与 NR-02 并行 | ready_to_assign |
| NR-04 1972–1997 | 原则上等 NR-03；技术上只依赖 NR-01 | 可与 NR-05 并行 | hold_until_demo |
| NR-05 1998–2012 | 原则上等 NR-03；技术上只依赖 NR-01 | 可与 NR-04 并行 | hold_until_demo |
| NR-06 集成验收 | NR-03／04／05＋检查点 B | 最后执行 | blocked |

---

## NR-01：研究信息架构冻结

### 任务目的

从一期方案、三个基础问题和 R1–R11／R14 模块出发，确定前端如何组织研究，而不是从第三次同步的六项发现或已有图表反推网站栏目。

### 必读输入

- 原始一期方案 DOCX
- `docs/phase1_scheme_acceptance_audit_v1.md`
- `docs/phase1_academic_client_redteam_audit_v1.md`
- `docs/phase1_workbench.md`
- `data/metadata/coding_schema_v0.md`
- `outputs/report_assembly_v1/`
- `outputs/learning_v1/okinawa_regions_research_map_v1.png`

### 工作内容

1. 把一期三个基础问题、纵向历史问题和各模块映射到四个主展示页。
2. 设计以下用户路径：
   - 组织 → 议题 → 事件 → 证据；
   - 地图 → 地点 → 地方问题 → 制度路径 → 结果；
   - 事件 → 参与者 → 场域 → 结果；
   - 时间段 → 历史锚点 → 组织连续性／缺口。
3. 规定四个主可视化引擎、右侧面板、全局证据抽屉与时间层的数据边界。
4. 规定“演示层／研究层”的切换边界。
5. 明确前端是后端数据的自动化可视化客户端，固定文案、数据字段、版本化短命题和解释边界
   分层管理。
6. 使用视觉意向稿确认构图方向；本轮不以低保真 wireframe 数量作为完成条件。

### 交付物

- `docs/exploration_system_information_architecture_v1.md`
- `outputs/exploration_system_ia_v1/module_to_view_crosswalk.csv`
- `outputs/exploration_system_ia_v1/view_visual_inventory_v1.csv`
- `outputs/exploration_system_ia_v1/checkpoint_A_decision_sheet_v1.md`
- `outputs/exploration_system_ia_v1/README.md`

旧 `route_map.svg` 与 `wireframe.html` 如保留，只能标记为 superseded exploration。

### 完成条件

- 固定四个主页面、四个主可视化引擎、一个全局时间层与一个全局证据抽屉；
- 三个基础问题和长期问题均能从任一主图进入对应证据；
- R1–R11 每个模块都有明确前端归宿，不另建孤立页面；
- 首页从全域地图进入具体对象，但组织、路径和证据保持直接导航；
- 候选关系不会在默认层伪装成事实；
- 时间覆盖不足被设计为系统信息，而不是藏在方法附录；
- 前端不需要为单个地区、组织或 episode 另写页面文案；
- 不新增任何研究事实。

### 负责人检查点 A

负责人已确认：

- 四个主页面为总览、组织、路径、证据；
- 首页采用第二张意向稿的中央主图、右侧详情和底部时间层；
- 前端是数据驱动的自动化可视化，不是报告目录或长文网站；
- 一期五张核心图收束进四个可视化引擎；
- 历史与证据下钻使用全局层，不增加页面。

### 可直接交给 session 的开场任务

> NR-01 检查点 A 已通过。后续若修订，只维护四页、四主图、全局时间层、全局证据抽屉和数据
> 驱动边界；不得从旧 wireframe 恢复六页面族，也不得新增研究内容。

---

## NR-02：前端数据契约与适配层

### 任务目的

在中央研究表与前端之间建立唯一数据接口，防止前端直接读取几十个 CSV 后混淆正式事实、候选关系、分析种子和人审状态。

### 依赖

- NR-01 已通过负责人检查点 A。

### 必读输入

- NR-01 全部交付物
- `data/interim/01_actor_registry_initial_v0.csv`
- `data/interim/02_actor_aliases_initial_v0.csv`
- `data/interim/03_issue_taxonomy_v0.csv`
- `data/interim/04_place_registry_v0.csv`
- `data/interim/05_source_log_initial_v0.csv`
- `data/interim/06_evidence_notes_v0.csv`
- `data/interim/07_actor_issue_edges_initial_v0.csv`
- `data/interim/08_actor_place_edges_initial_v0.csv`
- `data/interim/09_actor_event_venue_edges_v0.csv`
- `data/interim/17_legal_policy_procedure_cases_v0.csv`
- `data/interim/18_legal_policy_actor_roles_v0.csv`
- `outputs/translation_episode_comparison_v1/`
- `outputs/coverage_audit_v1/`

### 工作内容

1. 定义前端只认识的核心对象：
   - actor
   - place
   - issue
   - episode
   - venue
   - outcome
   - evidence
   - historical_anchor
2. 为所有对象统一以下字段：
   - `display_status`
   - `review_status`
   - `evidence_level`
   - `source_ids`
   - `interpretation_limit`
   - `source_publication_date`
   - `event_date`
   - `claim_period`
   - `actor_active_from/to`
3. 建立确定性分层：
   - `accepted`
   - `human_checked`
   - `source_backed_bounded`
   - `candidate`
   - `analytical_seed`
   - `local_retrieval_gap`
4. 默认 public/demo 数据只吸收允许展示的层；候选层单独输出。
5. 建立确定性、引用完整性、孤儿 ID、重复 ID、日期语义和状态越权验证。
6. 派生数据不得反写中央研究表。

### 建议交付物

- `docs/exploration_system_data_contract_v1.md`
- `scripts/build_exploration_system_data_v1.py`
- `outputs/exploration_system_data_v1/manifest.json`
- `outputs/exploration_system_data_v1/demo/actors.json`
- `outputs/exploration_system_data_v1/demo/places.json`
- `outputs/exploration_system_data_v1/demo/issues.json`
- `outputs/exploration_system_data_v1/demo/episodes.json`
- `outputs/exploration_system_data_v1/demo/venues.json`
- `outputs/exploration_system_data_v1/demo/outcomes.json`
- `outputs/exploration_system_data_v1/demo/evidence.json`
- `outputs/exploration_system_data_v1/demo/historical_anchors.json`
- `outputs/exploration_system_data_v1/demo/relations.json`
- `outputs/exploration_system_data_v1/research/candidates.json`
- `outputs/exploration_system_data_v1/views/overview.json`
- `outputs/exploration_system_data_v1/views/actors.json`
- `outputs/exploration_system_data_v1/views/pathways.json`
- `outputs/exploration_system_data_v1/views/evidence_coverage.json`
- `outputs/exploration_system_data_v1/views/global.json`
- `outputs/exploration_system_data_v1/validation_report.md`
- `tests/test_build_exploration_system_data_v1.py`

### 完成条件

- 一条前端结论可以机械追到来源 ID 和中央正式表；
- 默认层没有 `needs_human_review`、`analytical_seed` 或 event-only 名称冒充正式 actor；
- source year 与 event year 不再混用；
- 生成脚本重复运行结果稳定；
- 中央表无改动；
- 数据接口足够支持 NR-03，不要求前端再次自行解释研究语义。

### 可直接交给 session 的开场任务

> 执行任务总书 NR-02。建立中央研究数据到前端之间的唯一数据契约与派生层。禁止直接修改中央 registry、edge、source 表；禁止把候选、分析种子或共同出现关系放入默认演示数据。

完成记录（2026-07-18）：构建与 8 个端到端测试通过；manifest validation 为 PASS／0 errors。
AP123 因 place key/name 冲突在适配层隔离到 research，中央表未改。NR-03 只消费本包的
`views/`、`demo/` 和显式 `research/` 层。

---

## NR-03：可点击前端最小演示

### 任务目的

用现有材料做一条完整、可点击、可追溯的纵向切片，证明前端能够降低理解成本；不追求一次完成全部页面和全部图。

### 依赖

- NR-01、NR-02 完成。

### 最小功能

1. 总览页直接呈现 V1 全域地点—议题研究地图，并可进入组织、路径和证据三页；历史由底部时间层展开。
2. 组织生态：
   - 搜索／筛选 122 个 actor；
   - 打开 actor 详情；
   - 查看类型、议题、地点、事件和证据。
3. 实际地图：
   - 冲绳本岛、宫古、八重山／与那国真实地理；
   - 至少覆盖边野古、嘉手纳／普天间、宫古、石垣、与那国；
   - 点击地点进入地点详情。
4. 制度路径：
   - 至少使用 8 个已核 episode；
   - 统一显示“地方问题 → 组织翻译 → 场域 → 中间产出 → 有限结果 → 底层改变”。
5. 比较：
   - 至少可以比较两个地点或两个 episode；
   - 使用同一字段，不靠两段散文并排。
6. 证据抽屉：
   - 来源、日期、locator、证据等级、人工状态和解释边界。
7. 证据覆盖：
   - 证据页使用 V4 显示时间、地域、actor 类型、议题、来源类型和证据等级的不对称；
   - 四页共用时间层显示方案时期与已核历史锚点；
   - 不能把来源稀疏误画为组织活动低。

### 明确不做

- 不做复杂全屏网络“毛线球”；
- 不做十几个独立 dashboard；
- 不引入新研究结论；
- 不把第三次同步稿改造成网页长文；
- 不为单个地区、组织或 episode 维护手写页面文章；
- 不部署生产版本，先完成本地演示和负责人检查。

### 建议交付物

- `explorer/` 或经 NR-01 指定的单一前端目录
- `docs/exploration_system_demo_v1.md`
- `outputs/exploration_system_demo_qa_v1/`
- 本地启动命令
- 5 分钟演示路径

### 完成条件

- 用户可以完成“地图 → 地点 → episode → 证据”的完整点击链；
- 用户可以完成“组织 → 议题 → 事件 → 证据”的完整点击链；
- 至少一个比较视图真正减少阅读，而非把两段文字并排；
- 所有可见结论都有证据入口；
- 390px 与 1280px 宽度均可使用；
- 首屏没有统计卡片堆砌；
- 不需要阅读项目内部文档才能理解导航。

### 负责人检查点 B

项目负责人用 60–90 分钟自由探索，记录：

- 最先点击了什么；
- 哪一步不知道该点哪里；
- 哪个页面仍然信息过载；
- 哪个比较最有研究启发；
- 哪些解释自己不认可；
- 是否继续把历史材料整合进这个产品结构。

### 可直接交给 session 的开场任务

> 执行任务总书 NR-03。只使用 NR-02 的前端数据契约构建本地可点击最小演示。重点验证两条完整探索链和证据下钻，不扩研究、不做网络毛线球、不部署生产版本。

---

## NR-04：1972–1997 线上历史补缺

### 任务目的

建立早期社会运动组织与 1990 年代关键重组的“历史锚点候选层”，判断线上公开资料能够把长期主张推进到什么程度。

### 当前基线

- 当前 coverage audit 的 1972–1997 来源年份记录仅 4／295；
- 已知线索包括反战地主、一坪反战地主、1995 女性反基地动员、1997 名护住民投票、1998 ヘリ基地反対協成立前史；
- 后来回顾材料不得冒充同期一手材料。

### 检索边界

仅围绕以下对象和关系做定向检索：

1. 反战地主／一坪反战地主组织线；
2. 劳工、和平、女性和人权组织的复归后延续；
3. 嘉手纳／普天间噪音原告团早期轮次；
4. 1995 县民大会及相关组织重组；
5. 1997 名护公投和 1998 ヘリ基地反対協前史；
6. 当前 registry 中明确声称成立于 1972–1997 的组织。

优先路径：

- 组织沿革、旧官网和 Web Archive；
- 冲绳县公文书馆、国会图书馆、自治体数字记录；
- 法院、议会和政府公开资料；
- 可定位的运动史／学术文献及其一手文献线索；
- 已数字化的地方报刊索引。

### 必须记录

- 查询对象、日文关键词、数据库／域名、检索日期、结果；
- source publication date 与 historical event date；
- 当时名称与今天名称；
- relation type：
  - `formed`
  - `renamed`
  - `split`
  - `merged`
  - `coalition_successor`
  - `issue_continuity`
  - `place_continuity`
  - `person_overlap_public`
  - `unknown`
- contemporaneous／retrospective／secondary／lead-only；
- 是否需要当地报刊、会报、传单或访谈。

### 交付物

- `outputs/history_1972_1997_online_v1/historical_anchor_candidates.csv`
- `outputs/history_1972_1997_online_v1/source_candidates.csv`
- `outputs/history_1972_1997_online_v1/search_log.md`
- `outputs/history_1972_1997_online_v1/online_exhausted_gaps.csv`
- `outputs/history_1972_1997_online_v1/human_review_queue.csv`
- `outputs/history_1972_1997_online_v1/brief.md`

### 完成条件

- 不要求凑来源数量；
- 每个目标组织都有“找到／部分找到／线上耗尽”状态；
- 同名不自动判同一实体；
- 形成至少一条可复核的小谱系，但不伪造全时期连续网络；
- 明确哪些事实只能由 T2-F 当地任务完成；
- 不直接合并中央 registry 或前端默认层。

### 可直接交给 session 的开场任务

> 执行任务总书 NR-04。只做 1972–1997 的定向线上历史补缺，建立候选和检索日志，不追求数量、不自动认定组织连续性、不修改中央表。重点区分同期一手资料与后来回顾。

---

## NR-05：1998–2012 线上历史补缺

### 任务目的

落实一期方案原定的“1998–2012 优先采集”，研究 NPO 法施行后组织法律身份、组织形式和行动路径如何变化，并补足这一时期明显偏薄的来源和事件层。

### 当前基线

- 当前 coverage audit 的 1998–2012 来源年份记录为 21／295；
- 已知节点包括 2003 儒艮诉讼、2004 环评意见／海上行动、嘉手纳／普天间噪音诉讼、泡濑公金诉讼、2007 珊瑚平台、2010 联署／意见广告、2011 宫古反部署、2012 环评／与那国意见广告；
- 当前 NPO portal 页面可能包含早期成立事实，但来源年份往往是当前年份，必须拆分日期语义。

### 检索边界

按“组织形式变化＋关键行动”两条线推进：

1. 1998 NPO 法后法人化、解散、改名和持续性；
2. 边野古／大浦湾环境程序和现场组织；
3. 嘉手纳／普天间原告团与律师团轮次；
4. 泡濑湿地与公金诉讼组织；
5. 2000 年代女性、人权、和平和劳工网络；
6. 2010–2012 意见广告、联署、先岛反部署早期组织。

### 重点问题

- 法人化是否改变公开资料可见性，而不是假定改变运动本身；
- 短期实委会如何与持续组织区分；
- 组织名称、诉讼轮次和行动联盟如何编码；
- 环境／法律／国际路径是否在这一时期形成；
- 哪些当前“桥梁组织”只是因为旧资料保存较好而显得中心。

### 交付物

- `outputs/history_1998_2012_online_v1/historical_anchor_candidates.csv`
- `outputs/history_1998_2012_online_v1/organization_status_candidates.csv`
- `outputs/history_1998_2012_online_v1/source_candidates.csv`
- `outputs/history_1998_2012_online_v1/search_log.md`
- `outputs/history_1998_2012_online_v1/online_exhausted_gaps.csv`
- `outputs/history_1998_2012_online_v1/human_review_queue.csv`
- `outputs/history_1998_2012_online_v1/brief.md`

### 完成条件

- 对方案所说的“1998 年后较易追踪”给出实证判断，而不是继续当假设；
- 至少形成法人状态、历史事件和关系类型三种结构化候选；
- 当前网页中的历史事实不被错误记为当前年份事件；
- 不把诉讼轮次、前身、同名组织或共同活动自动合并；
- 不直接改中央表或前端默认层。

### 可直接交给 session 的开场任务

> 执行任务总书 NR-05。只补 1998–2012 的组织法律状态、关键行动和组织重组线上证据。严格分离来源年份、事件年份和组织活动期；所有结果先进入候选与人工队列，不直接写中央表。

---

## NR-06：证据集成、红队 QA 与演示验收

### 任务目的

将 NR-03 的前端演示和 NR-04／NR-05 的历史候选放在同一证据框架下审核，决定哪些历史信息可以进入演示层，并形成下一次甲方自主探索的稳定版本。

### 依赖

- NR-03、NR-04、NR-05 完成；
- 负责人完成检查点 B。

### 工作内容

1. 审核所有前端可见 claim：
   - 是否有来源；
   - 是否使用正确的时间字段；
   - 是否超出人工复核状态；
   - 是否把事件参与写成联盟；
   - 是否把程序产出写成底层改变；
   - 是否把材料可见性写成组织活动强度。
2. 对 NR-04／NR-05 结果生成正式人工复核任务；未经负责人决定的历史连续性不进入演示层。
3. 建立统一历史证据视觉语言：
   - 同期一手；
   - 后来组织回顾；
   - 二手重建；
   - 线索；
   - 当地材料缺口。
4. 检查四个主页面与全局时间层能否回答一期基础问题和纵向问题。
5. 检查 R1–R11 和长期问题是否均有前端归宿。
6. 形成 5 分钟引导路线与 20 分钟自由探索测试。
7. 如负责人批准，再准备可部署版本；部署本身另行授权。

### 交付物

- `outputs/exploration_system_release_gate_v1/frontend_claim_manifest.csv`
- `outputs/exploration_system_release_gate_v1/history_integration_decisions.csv`
- `outputs/exploration_system_release_gate_v1/validation_report.md`
- `outputs/exploration_system_release_gate_v1/redteam_findings.md`
- `outputs/exploration_system_release_gate_v1/demo_script_5min.md`
- `outputs/exploration_system_release_gate_v1/exploration_test_20min.md`
- 更新后的本地演示版本

### 完成条件

- 所有默认可见 claim 都可追到证据和状态；
- 所有历史连续性都有负责人决定或保持为缺口；
- 甲方不看文档也能完成至少两条自主探索路径；
- 系统可以明确回答一期三个基础问题；
- 系统明确显示而不掩盖 1972–2012 的资料不对称；
- 无候选关系、分析种子、错误日期或过强因果措辞泄漏进演示层；
- 下一次展示以系统为主体，文档只作简短导览和方法说明。

### 负责人检查点 C

项目负责人最终决定：

- 是否保留“复归后”作为报告和系统主标题；
- 历史层目前可写成“完整演变”“历史骨架”还是“背景锚点”；
- 哪些缺口正式派给当地协作者 T2-F；
- 是否批准生产部署。

### 可直接交给 session 的开场任务

> 执行任务总书 NR-06。对前端和两批历史候选做统一证据 QA，生成可追溯 claim manifest、红队报告和演示测试。未经负责人决定的历史连续性不得进入默认层；本任务不自动部署。

## 4. 项目负责人参与安排

为保持约 50% 的解释性参与，本轮不把负责人放在最终验收末端，而设置三个实质检查点：

| 检查点 | 时间投入建议 | 负责人实际判断 |
|---|---:|---|
| A 信息架构 | 30–45 分钟 | 系统应该如何组织研究问题 |
| B 前端自由探索 | 60–90 分钟 | 哪些交互真正降低理解成本，哪些解释不成立 |
| C 历史与发布 | 45–60 分钟 | 是否保留长期标题、哪些历史连续性可写、是否派当地任务 |

AI／session 负责机械整理、适配、实现、验证和候选检索；负责人负责导航取舍、解释强度、历史连续性和发布决定。

## 5. 本轮不做

- 不继续无目标扩 actor registry；
- 不继续为第三次同步加图；
- 不立即写完整报告或论文；
- 不把所有现有图搬进前端；
- 不以图表数量衡量系统完成；
- 不把前端做成报告页面滚动版；
- 不承诺线上完成 1972 年以来全量谱系；
- 不在历史补查完成前用当前网络反推长期组织增长；
- 不在负责人检查前部署生产版本。

## 6. 本轮最终成功标准

本轮成功不是“上线了一个网站”，而是同时满足：

1. 研究方案、数据结构、前端导航和证据状态使用同一套对象；
2. 甲方能够自主探索，而不需要主线程逐图讲解；
3. 前端减少理解成本，不增加新栏目和新图表负担；
4. 1972–2012 缺口被分解为可验证的线上上限和当地任务；
5. 长期主张的强度由证据决定，而不是由项目标题决定；
6. 每个 session 都有独立边界、独立目录和明确 handoff，可由主线程稳定集成。

## 7. 每个 session 的统一 handoff 模板

```text
任务编号：
完成状态：complete / partial / blocked

完成了：
- 

新增或修改文件：
- 

关键计数与验证：
- 

运行／复现命令：
- 

未决人工判断：
- 

不得被主线程误读为：
- 

建议下一 session：
- 
```
