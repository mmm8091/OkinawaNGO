# research_wave_h3_frontline_memory_v2

独立研究包，检验“反战／防止前线化／台湾有事是否成为跨地区共同语言”，同时严格区分两个**共同文件层**对象：

1. **共同文件框架（common-text frame）**：战争记忆、再次成为战场、生活安全、人权、环境、外交／对话如何被并置；
2. **共同文件对象（common-text object）**：2025 结成宣言与 2026 请愿如何把基地、导弹、弹药库、民用港机场与道路、运输／演习、避难构造成跨地域“战争准备”体系。

## 当前结论

- 可确认一个**至少持续到 2026 年初的正式跨区域行动载体**：2025-02-22 材料提出治理方案、共同代表、区域运营、秘书处及信息基础设施；2025-05-06 来源列出 35 个“参加／构成团体”；2025-06 与 2026-01 有两次正式行动。它不证明列名团体留存、实际分工或治理方案全部执行。
- 2025 结成宣言与 2026 请愿在**共同文件层**清楚并置生产、储存、运输、部署、演习和避难等节点。现阶段不能把这一文本构造转写成“组织／地方运动已经对象上移”。
- 这仍**不是扩散证明**。大分、石垣、宫古等地在正式网络成立前已有相近但地方化的语言；“把已有地方运动聚合起来”与“冲绳语言向外扩散”至少同样可行。
- 两家地方报纸在来源层明确报道旧名称 A010 于 2023-04-15 总会改为新名称；这一报道与 HR-012 的中央生命周期记录冲突，因此中央 canonical／alias／生命周期仍待人工裁决。旧名称 A010 在驻屯地启用前已经使用台湾有事、避难与外交框架，本包明确不写“安装造成尺度上移”。
- 宫古的 A013 战场化／对话框架来自对其共同代表的媒体归因，不是组织自写文本；同篇报道中撤离／生活安全说法来自其他发言者，不能转嫁给 A013。官方会议记录只证明一个相似名称主体提交意见／请求并获得答复，不证明到场或与 A013 完全同一。
- 2026-05-07 是提交／行动日，页面发布于 2026-05-16。正文只有与那国、石垣、宫古三个地方请求段；“四地”指外部报道中的发言／行动超边。35 个赞同团体中有 14 个 registry 候选 crosswalk；“首次”仅作发布方／党媒归因。
- 2010／2015／2020 三份完整环境文本没有目标词，只能作为**文体／议题负例**，不能证明社会总体词汇增长。

## 复现

```powershell
python scripts\make_research_wave_h3_frontline_memory_v2.py
python -m unittest tests.test_make_research_wave_h3_frontline_memory_v2
```

## 文件

- `frontline_memory_brief_v2.md`：解释性研究简报。
- `hypothesis_tests_v2.csv`：七个可证伪命题及当前判定。
- `comparable_corpus_v2.csv`：28 条分层语料观察；组织自写、转载、媒体归因、官方与学术反框架分开。
- `source_log_v2.csv`、`search_log_v2.csv`：来源与检索边界。
- `network_participating_group_candidates_v2.csv`：截至 2025-05-06 的 35 个参加／构成团体主张。
- `three_island_request_four_place_event_entities_v2.csv`：5 月 7 日事件／提交、5 月 16 日发布的 35 个赞同团体及分层角色。
- `three_island_request_sections_v2.csv`：三个地方请求段；起草者与代表组织均保持 unknown，不把段落归给列名赞同团体。
- `event_speaker_attributions_v2.csv`：3 条逐发言者媒体归因，防止个人发言转嫁给组织。
- `event_endorser_issue_family_candidates_v2.csv`：分析者提出的事件赞同团体功能分类候选，不是来源原分类。
- `event_roster_overlap_v2.csv`：2023／2025／2026 名单重叠；角色不等价。
- `independent_adoption_panel_v2.csv`：独立采用、媒体归因、名册限定和缺失分开。
- `frame_object_observations_v2.csv`：共同框架与共同对象分离。
- `ishigaki_name_lifecycle_candidate_v2.csv`：保存来源层明确报道的改名，同时将与 HR-012 冲突的中央生命周期写回保持 human-pending。
- `network_formation_events_v2.csv`：2017–2026 载体／接触／正式行动序列。
- `negative_controls_v2.csv`：负例和竞争解释。
- `academic_connection_v2.csv`：直接案例、历史对照、战争记忆、组织变化和官方反框架的学术连接。
- `human_review_queue_v2.csv`、`local_retrieval_queue_v2.csv`：人工判断与当地材料任务。
- `fig1_carrier_and_object_timeline_v2.svg`、`fig2_roster_overlap_v2.svg`、`fig3_common_frame_vs_common_object_v2.svg`：三张研究图。
- `principal_checkpoint_v2.md`：负责人阅读与选择闸门。
- `validation_report_v2.md`、`manifest.json`：校验与复现信息。

## 硬边界

本包所有行均为 `research_only / candidate / ai_seeded / not_frontend_ready / central_writeback=no`。参加／构成团体主张不生成团体之间的 dyadic 联盟边；共同请愿只生成事件级超边；“契机／首次”均保留为来源归因；35→38 不写成增长或留存；A010 的来源层改名报道不直接写入中央生命周期；共同文件对象不外推为各组织独立采用或前后变化。
