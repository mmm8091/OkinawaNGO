# 一期方案合同验收审计：基础建设与最终交付

日期：2026-07-12  
验收基准：`source_docs/current/复归后冲绳民间组织 _ NGO 分类与议题网络一期研究方案 (3).docx`（以同目录对应 Markdown 文本逐条定位合同要求）  
审计范围：基础数据包、最终研究解释成果与指定核心图。现有工作台、线上收口计划和各 README 只作为“当前自报状态”，不能修改合同门槛。

## 一、总判断

当前成果**不具备一期合同验收条件**。已经形成一个有分析潜力的 v0 原型，但仍处于“若干模块已有解释性样图和内部报告草稿”的阶段，不能表述为“一期线上工作或一期交付已完成”。

最重要的判断有五项：

1. 合同明确要求 actor registry 为 **120–180 个公开资料可核查 actor**；当前为 103 个，低于下限 17 个。内部文件取消“120+ 机械目标”的决定不能覆盖甲方方案中的明确验收数字。扩表应由模块缺口驱动，但最终仍须达到 120。
2. 基础包缺少独立的 `evidence notes`、`actor–venue edges sample`、`joint action edges sample` 和正式 `coverage audit`；现有侧表只能视为局部替代材料，不能因“有相近文件”直接判定达标。
3. 当前 CSV 底座存在结构错误：`03_issue_taxonomy_v0.csv` 有 8 行未转义逗号导致列错位；actor registry、actor–issue 和 actor–place 各另有 1 行同类问题。标准 CSV reader 会把字段拆错，属于验收前必须修复的 P0 问题。
4. 当前 103 个 actor 中 63 个仍为 `ai_seeded`，23 个为 `needs_second_source`；180 条 actor–issue 边中 129 条、124 条 actor–place 边中 90 条仍为 `ai_seeded`。编码规则要求进入分析结论的 actor/edge 必须有人审，而当前人工参与度也无法从日志计算，因为没有 AI/人工工时字段。
5. 论文、25–35 页报告、15–20 页 PPT 均未形成可验收成品。现有研究报告是 7,102 个汉字左右的 Markdown 内审草稿，仍保留 6 项可视化/检索 TODO，没有排版页数、成稿 DOCX/PDF 或独立论文；仓库中没有一期汇报 PPT。

按合同而非内部“已交工”口径估计：基础底座约完成一半，指定五图约完成两成到四成，最终成品约完成一成。这里的百分比只表示验收成熟度，不表示已投入工时。

## 二、基础建设逐项审计

完成度采用四档：`达标`、`基本达标但需 QA`、`部分完成`、`缺失`。只有内容、结构、证据链和解释用途同时满足才可标为达标。

| 合同项 | 当前证据 | 完成度 | 现有解释价值 | 明显缺口 | 下一步 | done_when |
|---|---|---|---|---|---|---|
| actor registry：120–180 | `01_actor_registry_initial_v0.csv`，103 行；46 个 `okinawa_local`、19 个日本国内、17 个美国来源、13 个国际来源；E4 66、E3 24、E2 13 | **部分完成（约 60%）** | 已能区分冲绳本地行动、国内/国际倡议、军属服务、行政协作等功能层，并支撑功能生态图 | 数量低于合同下限；63 条 `ai_seeded`、23 条待第二来源；46 条仍标 `needs_local_retrieval=yes`；A082 行有未转义逗号；registry 缺活跃时期/成立时间等复归后时间定位字段；12 个 actor 尚未进入 actor–issue 或 actor–place 主边表 | 先修 CSV；按 R1–R11 缺口扩入不少于 17 个有解释价值 actor，优先先岛/与那国、噪音诉讼与法律程序、本土声援层、行政/场域节点；对进入图与正文的节点逐项人工复核 | 有效 actor 数在 120–180；每行可被标准 CSV reader 无错读取；每个 actor 有规范名、类型、来源、议题、地点、证据级别；所有进入正文/图的 actor 均有人工复核记录；层级构成和纳入标准在报告中可解释 |
| actor alias | `02_actor_aliases_initial_v0.csv`，14 行，只覆盖 5 个 actor | **部分完成（约 20%）** | 对 AWWA、MOSCO、Pro Public、Pro Natura 等少数高风险异名已能避免重复节点 | 只覆盖 4.9% registry；日文名、英文名、简称、旧称没有系统完成；Tier A 9 个 actor 的别名/日文正式名仍是已知待办 | 对全部非日文规范名、双语名、旧称/法人化前后名称和 acronym 做规则化核查；优先完成 Tier A 与所有图中节点 | 所有存在公开异名的 actor 均有 alias 行；至少图/正文所用 actor 的日文正式名、英文名/简称、旧称已核对；alias 指向唯一 actor_id、有 source_ref、无重复拆点 |
| issue taxonomy | `03_issue_taxonomy_v0.csv`，名义 19 个一级议题 | **部分完成（约 45%）** | 已覆盖 anti-base、Henoko、dugong、生活安全、自治、公投、法律、国际倡议、先岛前线化等主要分析入口 | 8/19 数据行因未转义逗号列错位，`include_in_phase1` 与 notes 被错误解析；合同明确提到的 `human_rights` 和通用 `environment` 没有独立一级项；定义与父子层级不足以稳定支持多模块比较 | 修复 CSV quoting；补齐/明确环境、人权、反战/和平、先岛安全化等概念边界；建立“一级框架—子议题—地点议题”的层级或映射 | 19+ 条均能按 6 列稳定读取；合同核心概念全部可映射；每项有排他/包含规则、示例和一期范围；actor 标签与 edge 的 issue_id 一致，自动校验通过 |
| place registry | `04_place_registry_v0.csv`，20 个节点，包括边野古、大浦湾、普天间、嘉手纳、与那国、石垣、宫古及外部制度场域 | **基本达标但需 QA（约 75%）** | 可支撑地点—议题矩阵和组织—地点矩阵，并能区分基地 site、municipality、institutional site | 尚未形成地点同义名/层级规则；Futenma 与 MCAS Futenma、Henoko 与 Camp Schwab 等相邻概念可能重复计数；外部法律/国际 venue 未系统进入 place/venue 层 | 加 place alias、父子层级和 site/municipality 去重规则；与 venue 字典明确分工 | 关键地点全部覆盖；同名/嵌套地点有层级与使用规则；所有 actor–place 边能映射且无歧义；先岛三地可独立比较 |
| source log | `05_source_log_initial_v0.csv`，102 条；100 个真实 URL、2 个非 URL；93 archived、2 manual、5 failed；E4 56、E3 37、E2 9 | **部分完成（约 70%）** | 已形成可追溯 source_id 和本地归档机制，来源类型较多元 | 51 条仍为 `ai_seeded`；合同的“覆盖时间”目前基本只有单一 `year`，缺来源所覆盖期间；没有逐条原文证据摘录；5 个归档失败需区分永久不可得与暂态失败 | 对进入结论的 source 做人工核查；增加 `coverage_start/end` 或明确 year 语义；归档失败形成稳定状态；与 evidence notes 一对多连接 | 正文/图所用 source 均 human-checked；URL/非 URL 类型明确；覆盖期、来源类型、可信度/偏差说明齐全；本地归档或可说明的失败状态齐全；所有 source_ref 完整性检查通过 |
| evidence notes | 未找到合同要求的 `06_evidence_notes.csv`；actor/edge 的 `notes` 和 `relation_basis` 多为简短概括，不是原文摘录 | **缺失（约 5%）** | 现有 notes 能提醒解释边界，但不足以让审阅者复核标签与关系 | 缺 `object_id/source_id/evidence_quote_or_summary/location/claim/evidence_level/reviewer` 等独立证据记录；无法从结构化数据追到原文段落/页码；“有 source_ref”不等于“有 evidence note” | 建立独立 evidence notes 表，先覆盖所有核心图、正文结论、E2/E3 边和敏感关系；从已归档网页/PDF回填短摘录或忠实摘要及定位 | 独立表存在；每个正文结论和核心图关键边至少有一条可定位 evidence note；敏感 funding/法律/联盟关系有人工 reviewer；抽样可从 claim 回到 source 原文 |
| actor–issue edges | `07_actor_issue_edges_initial_v0.csv`，180 行，覆盖 91 个 actor；E4 115、E3 60、E2 5 | **部分完成（约 55%）** | 已支撑 bridge shortlist 和地点—议题聚合，可初步回答“如何转译” | 129 条仍 `ai_seeded`；AI018 notes 未转义逗号；12 个 registry actor 不在表；缺独立证据摘录；现图只是桥接节点 shortlist，报告也保留完整网络 TODO | 修复结构；补新 actor 边；对核心边人工复核；构建分层完整网络并与 shortlist 做一致性检查 | CSV 无结构错误；所有纳入分析的 actor 有合理 issue 边；核心边有 evidence note 和人工复核；完整网络图能显示 actor 类型、议题簇、E2–E4/复核状态并有可解释结论 |
| actor–place edges | `08_actor_place_edges_initial_v0.csv`，124 行，覆盖 91 个 actor；E4 76、E3 43、E2 5 | **部分完成（约 55%）** | 已支撑地点—议题聚合和 24 actor 的精选组织—地点矩阵 | 90 条仍 `ai_seeded`；AP012 notes 未转义逗号；12 个 actor 不在表；精选图只展示 36 条关系，不能代表全 registry；地点出现、常设据点、行动现场尚需更明确的 relation_type | 修复结构；把 place relation 分为 headquarters/site presence/event/advocacy target 等；补先岛与新增 actor；人工复核图中边 | 主表无错；关系类型明确；关键地点和合同要求的比较案例有足够节点；所有图中边有 source/evidence note/人工复核；全文不把“声明涉及某地”误写为“现场存在” |
| actor–venue edges sample | 未找到 `09_actor_venue_edges_sample.csv`；`actor_relation_events_v1.csv` 有 action_type/role，国际化路径节点表有局部制度场域信息 | **缺失/仅有代理材料（约 15%）** | 现有事件侧表提示诉讼、公投、要请、共同声明等行动类型，可作为建表种子 | 没有 venue 字典和 actor–venue incidence；无法系统比较媒体、法院、行政、国际机构、街头/现场等场域，也不足以完成 R7“场域与对象转移” | 建 venue taxonomy 和 actor–venue sample；把 9 个现有事件、诉讼角色、国际路径节点统一映射，补噪音诉讼/行政程序 | 独立样本表存在；至少覆盖法律、行政、国际机制、公投/选举、现场抗议/声明等场域；字段含 actor、event、venue、role、date、source、evidence、review；能产出一项跨场域解释 |
| joint action edges sample | `coaction_events_v0.csv` 3 个事件、`coaction_participants_v0.csv` 44 行、2020 MMC 71 团体全名单；`actor_relation_events_v1.csv` 共 9 事件/54 行/5 类行动 | **部分完成（约 45%）** | 已把共同出现重新表述为事件参与而非稳定联盟，这是正确的解释方向 | 合同要求的是共同声明/联署/诉讼/国际提交“样本关系表”；当前没有统一 pair/affiliation edge deliverable；事件仅 9 个，噪音诉讼、protest/行政事件是明确 TODO；跨事件重复性结论样本太薄 | 以 event–actor 二部表作为主结构，并按需派生 pair edge，禁止直接等同联盟；补代表性事件与角色、行动对象和制度场域 | 有统一、验证后的 joint-action 样本表；至少覆盖合同列出的四类行动，并纳入关键地点事件；每条有 role/strength/limit/source/review；派生边可重现且图注明确“事件共现≠稳定联盟” |
| coverage audit | `coverage_gap_summary_v0.csv` 47 行和 `R14_coverage_bias_audit_brief.md`；现有 evidence-gap 图仍基于较早的 93 actor/92 source 状态 | **部分完成（约 35%）** | 已识别公开可见度、来源类型、复核状态和归档缺口 | 不是合同命名的完整 coverage audit；主要是状态计数，缺按时间段、地点、actor 功能层、法律身份、来源语言/类型、议题和缺失字段的交叉覆盖；图已过时；无法检验“复归后”覆盖偏差 | 建 `11_coverage_audit.csv` 或等价可发布表；按时间×地点×actor层×议题×证据/复核状态做缺口矩阵；更新覆盖偏差图 | 审计表和图使用同一冻结版本；明确抽样框、未覆盖范围、线上/当地缺口；至少展示时间、地点、actor 类型、议题、来源和复核六个维度；能直接生成当地任务优先级 |
| coding guide | `data/metadata/coding_schema_v0.md`，含 actor 字段、actor class、origin、issue tags、E0–E4、funding confidence、通用 edge 和保守解释规则 | **部分完成（约 60%）** | 对资金、服务组织、候选边和证据等级的边界较清楚 | 未定义 source/alias/taxonomy/place/evidence-note/actor–issue/actor–place/venue/joint-action 的完整 schema；actor–issue/place 与 funding 通用 edge 结构不一致；缺日期、事件、行动对象、venue controlled vocabulary；“人工参与至少 30%”没有可计算日志字段；taxonomy 实表与 guide 的 issue tags 不完全一致 | 将所有一期表纳入数据字典，增加主外键、必填项、受控词表、日期/事件/venue、证据摘录和自动验证规则；补工时记录方法 | 所有交付 CSV 均有字段定义、受控值、主外键和必填规则；自动 lint 全通过；人工参与度可计算且≥30%；任一图/结论可追溯到规范字段与证据记录 |

### 基础底座的解释性结论

现有底座最有价值的不是“103/102/180/124”这组数量，而是已经出现了四个可继续验证的解释方向：

- 冲绳民间组织生态不能被压缩为单一反基地阵营，至少包含本地公民行动、环境/法律/国际倡议、行政/国际协作、军属服务/慈善和制度节点。
- 基地议题的组织化不是一个标签替换，而是经由生态保护、生活安全、地方自治、法律程序与国际机构等不同渠道发生“议题转译”。
- 地点是机制差异的重要来源：边野古/大浦湾偏生态—法律—国际化，嘉手纳/普天间偏基地负担—噪音—生活安全，石垣/宫古偏部署—水源—自治，与那国必须按前线/安全环境—自治—公投—生命安全解释。
- 共同署名、要请和诉讼角色适合用事件二部网络表达，不能直接推断稳定联盟。

但这些方向目前仍依赖大量未人工复核的候选边，且没有 evidence notes 支撑逐条复核。因此它们是“可检验的阶段性解释”，还不是一期最终发现。

## 三、最小资料包其他合同项

| 合同项 | 当前状态 | 验收判断 | done_when |
|---|---|---|---|
| 与那国/先岛 dossier | 没有合同列明的 `12_yonaguni_sakishima_dossier.docx`；报告第 5 节只有约四个短段落，另有地点 brief/CSV | **缺失** | 形成独立小档案，系统比较与那国、石垣、宫古的 actor、事件、议题框架、时间线、证据缺口和当地任务；渲染后页数/版式通过 QA |
| visualization outputs | 已有 `explanatory_v0` 5 图、`phase1_visuals_v1` 3 图、事件图及旧进度图 | **文件数量充足、合同核心图内容未齐** | 见下一节五图逐项验收；每图必须有冻结数据、可运行脚本、中文图注、解释段落和证据边界 |
| public web data | 未见合同列明的 `14_public_web_data/` 成品；`formal_comm_v0/index.html` 是进度同步预览，不是研究成果数据包 | **缺失** | 若该项仍属一期合同，提供经过发布审查、字段脱敏/删减、带数据字典与版本号的网页用数据；若甲方书面取消，应保留变更记录 |
| funding/support sample | `15_funding_or_support_edges_sample_v0.csv` 36 行，并有严格 E3/E4 分层图 | **部分完成、解释边界较好** | 结构 QA 通过；所有进入结论的关系有人审和 evidence note；grant/commission/sponsor/service/non-funding 明确分离；不把 opportunity 写成 award |

## 四、五个指定核心图验收

合同要求“至少 5 个核心可视化”，且指定了五种内容。不能用其他统计图的数量替代指定图。

| 指定核心图 | 当前对应物 | 完成度 | 当前能解释什么 | 缺口与 done_when |
|---|---|---|---|---|
| 组织—议题网络 | `fig_actor_issue_bridge_network.png` | **部分完成** | 哪些已录入 actor 连接两个以上重点议题 | 当前只是 bridge shortlist，不是完整组织—议题网络；报告仍有 `TODO-VIS-02`。完成条件：基于修复后的全量表，显示主要议题簇、actor 功能/来源层与 E2–E4/复核状态，并给出至少 2–3 个经 evidence notes 支撑的桥接机制解释 |
| 地点—议题图 | `fig_place_issue_matrix_explanatory.png` | **基本成形、需更新 QA** | 不同地点承接的议题框架差异 | 图包 README 仍记录 93 actor/92 source 的旧快照，需确认图是否与冻结数据一致。完成条件：用最终数据重生，明确分母/计数逻辑、候选边边界，并在报告解释本岛与先岛的差异 |
| 国际倡议/法律程序路径图 | `fig_henoko_internationalization_pathway.png` + lawsuit role table | **部分完成** | 边野古/大浦湾个案如何经儒艮、环境程序、美国法院/机构形成外部路径 | 目前是单案例手工节点路径，不能代表一般网络，且缺多案件/程序统一事件表。完成条件：节点角色、每一步 source/evidence note、法律当事人与倡议者严格区分；报告明确这是案例机制图，并至少用另一法律/程序事件作边界比较 |
| 与那国/先岛专题图 | 没有专门图；地点—议题矩阵和精选 actor–place 图只含局部先岛信息 | **缺失** | 现图只能提示与那国数据稀疏以及石垣/宫古的生活安全框架 | 完成条件：专图比较与那国/石垣/宫古的 actor—事件—框架—证据密度或时间线；与那国使用前线/安全环境、自治、公投、台湾邻近和生命安全主框架；图中显式呈现缺证据而不以低密度冒充“组织弱” |
| 覆盖偏差图 | `fig_evidence_gap_map.png` + 功能生态图透明度提示 | **部分完成且过时** | 当前 review/source archive 状态与 E2 可见度提醒 | 原图基于旧状态，且偏工作进度计数，不足以解释抽样偏差。完成条件：基于最终 coverage audit，交叉展示时间、地点、actor 层、议题、来源和证据/复核状态，明确哪些结论可能由线上可见度造成 |

按严格合同口径，当前没有一张可以在不更新数据/证据说明的情况下直接作为最终图验收；地点—议题图最接近，组织—议题、国际路径和覆盖偏差为半成品，与那国/先岛专题图缺失。

## 五、最终研究解释成果验收

| 合同交付 | 当前证据 | 完成度 | 明显缺口 | 下一步与 done_when |
|---|---|---|---|---|
| 8,000–12,000 字论文 | 未找到独立一期论文；`phase1_research_report_v0.md` 是报告草稿，不是把前期选举研究与本研究结合的课程论文 | **缺失（0%）** | 缺前期知事选举发现的实质接合、文献对话、理论框架、方法、论证、讨论、参考文献；当前报告约 7,102 汉字，也未达到合同字数下限 | 数据/五图冻结后另写论文。完成条件：8,000–12,000 字；明确把 1990–2022 选举发现与组织动员/议题转译相连；有研究问题、文献、方法、发现、讨论、局限、结论和规范引文；人工学术审阅完成 |
| 25–35 页研究报告 | `docs/phase1_research_report_v0.md`，13,366 字符、约 7,102 汉字、193 行；状态明示“可审阅草稿”；含 `TODO-VIS-02/04/06` 和 `TODO-SEARCH-01` 等 | **部分完成（约 25%）** | 没有最终 DOCX/PDF与可验证页数；篇幅明显不足以支撑 25–35 页；多节只有结论性短段；没有嵌图版式、完整引用和附录；数据与部分图不同步 | 先完成底座/图，再扩成正式报告。完成条件：最终渲染为 25–35 页；五图和必要表格嵌入；每个基础问题与所选模块均有“证据—模式—解释—限制”；无 TODO；引文/数据版本一致；逐页视觉 QA 通过 |
| 15–20 页汇报 PPT | 仓库没有 `.pptx`；第二次进度同步 PDF 不是一期最终汇报 PPT | **缺失（0%）** | 无最终叙事、页数、speaker-facing 图文、验收版文件 | 报告定稿后制作。完成条件：15–20 页；覆盖问题、方法、组织生态、议题转译、地点差异、国际/法律路径、先岛专题、覆盖偏差、结论与下一步；五图可读；渲染逐页 QA 通过 |
| 至少 5 个指定核心图 | 已有多张 PNG，但指定内容只有 1 张接近完成、3 张部分完成、1 张缺失 | **部分完成（约 30%）** | “PNG 数量≥5”不等于合同指定五图达标；证据版本、解释 brief 和图文一致性尚未封版 | 按上一节逐图 done_when 完成，生成冻结版图包、配套 CSV、脚本、图注、可发布边界和报告对应段落 |

### 当前报告对三个基础问题的回答强度

1. **“有哪些组织？”——回答不足。** 已能展示 103 actor 的功能构成，但未达到 120 下限，历史时段和离岛小型组织的覆盖无法量化，且大部分条目未完成分析级人工复核。
2. **“如何分类、谁是跨议题桥梁？”——有可用雏形。** 功能生态图与 bridge shortlist 已提出“本地行动—环保/法律/国际倡议—行政协作—军属服务”的分层，但 taxonomy 结构错误、alias 稀薄、完整组织—议题网络和证据摘录缺失，使分类与桥梁判断尚不能封版。
3. **“关键地点如何连接环保、生活安全、自治与军事设施争议？”——边野古较强，先岛不平衡。** 边野古/大浦湾已有生态—法律—国际化机制；石垣/宫古有自治/水源/生活安全线索；与那国组织级证据和专图明显不足；嘉手纳/普天间噪音诉讼尚未进入事件层。

因此，下一轮不能只“补交文件”，而应围绕这三个问题补足能改变解释的材料：补 actor 是为了修复组织生态与地点/功能层缺口，补事件是为了比较行动机制，补 evidence notes 是为了让解释可复核，补图则是为了检验而不是装饰已有结论。

## 六、建议的线上收口顺序

### P0：先修底座，暂停把现图称作最终图

1. 修复 11 行 CSV quoting/列错位问题，并给所有交付 CSV 增加自动 schema lint。
2. 建立 `evidence_notes`、venue taxonomy/edges、统一 event–actor/joint-action 表和正式 coverage audit。
3. 把 human review log 扩展到可计算人工参与度，并确保所有进入图/正文的节点和边有人审。

### P1：按合同与研究问题扩充 registry，而不是机械灌名

1. 至少补到 120；新增 actor 必须填补一个明确分析缺口。
2. 优先池：先岛/与那国持续性组织与住民团体；嘉手纳/普天间噪音诉讼原告团/律师团；环境/法律程序主体；能形成独立“日本本土声援层”的 Tier B；必要的行动对象/制度节点。
3. Tier C 一次性署名者仍可留在 event participant 表，不必为凑数全部升级为 registry actor。
4. 每扩一组 actor，同步补 alias、issue/place/venue 边、evidence note 和人工复核，不留“孤立节点”。

### P2：完成五个合同图并让每图产生解释

1. 全量组织—议题网络：识别桥接类型，而非只报 degree。
2. 更新地点—议题图：比较本岛基地场域与先岛部署场域的框架差异。
3. 国际/法律路径：解释“地方知识—国内法律/环保语言—外部制度渠道”的转换条件与边界。
4. 新做与那国/先岛专题图：把三岛差异和证据稀疏同时可视化。
5. 新做覆盖审计图：解释哪些发现可能是来源可见度造成的。

每图必须回答一个问题、给出至少一个非显然模式、说明不能推出什么，并以 evidence notes 支撑关键节点/关系。

### P3：数据与图冻结后制作成品

1. 先写 25–35 页研究报告；每个基础问题和实际选做模块均有解释段落。
2. 再独立写 8,000–12,000 字论文，把前期选举研究与本期组织机制真正接合，不能把报告改标题后当论文。
3. 最后制作 15–20 页 PPT，将五图组织成一条可讲述的论证链。
4. 成品统一做数据版本、数字、引用、图注和视觉 QA；然后再根据明确 evidence gaps 派当地协作者。

## 七、一期基础与最终交付的总 done_when

一期只有同时满足以下条件，才可以对甲方表述为“达到方案验收”：

- actor registry 有 120–180 个可核查条目，关键分析节点完成人工复核，alias 与主边表同步；
- taxonomy、place、source、evidence notes、actor–issue、actor–place、actor–venue、joint action、coverage audit、coding guide 均有可机读且通过 lint 的正式表/文档；
- 所有正文结论和核心图关键边都能从 object/edge 追溯到 source 与 evidence note；敏感关系有人审；
- 五个指定核心图全部基于同一冻结数据版本，可复现、有中文图注、解释段落和限制；
- 与那国/先岛有独立 dossier 和专题图，而不是散落在地点矩阵中的少量格子；
- 8,000–12,000 字论文、25–35 页报告、15–20 页 PPT 均为独立成品且通过内容/版式 QA；
- 三个基础问题得到明确回答，每个回答都包含证据、机制解释、地点/组织差异和不可推断边界；
- 当地协作者任务由最终 coverage/evidence gap 反推，字段明确，不再是宽泛“继续找资料”。

