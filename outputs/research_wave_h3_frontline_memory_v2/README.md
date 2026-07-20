# research_wave_h3_frontline_memory_v2

独立研究包，检验“反战／防止前线化／台湾有事是否成为跨地区共同语言”，并把问题收紧为两个不同对象：

1. **共同框架（common frame）**：战争记忆、再次成为战场、生活安全、人权、环境、外交／对话如何被压缩在同一叙述中；
2. **共同对象（common object）**：地方组织是否开始把基地、导弹、弹药库、民用港机场与道路、运输／演习、避难视为同一套跨地域“战争准备”体系。

## 当前结论

- 可确认一个**正式跨区域载体**：2025-02-22 成立材料提供治理、共同代表、区域运营、秘书处和信息基础设施；2025-05-06 名册列出 35 个构成团体；2025-06 与 2026-01 出现两次政府交涉。
- 2025 结成宣言与 2026 四岛请愿支持“**共同对象发生上移**”这一强候选解释：文本不再只反对一个设施，而把生产、储存、运输、部署、演习和避难节点连成跨岛／跨西日本体系。
- 这仍**不是扩散证明**。大分、石垣、宫古等地在正式网络成立前已有相近但地方化的语言；“把已有地方运动聚合起来”与“冲绳语言向外扩散”至少同样可行。
- A010 提供“**安装后的尺度转换**”纵向候选：驻屯地启用后改名、成员部分更替，继续本地监视，同时转向九州长射程导弹、正式跨西日本网络与四岛请愿。改名、人员轮换、全国政策变化和少数骨干迁移仍是竞争解释。
- 宫古提供关键边界：2024 有战场化／对话语言且持续进入制度场域，未列入 2025-05 的 35 个正式成员，却进入 2026 四岛共同请愿。**共同语言、共同正式组织、共同事件是三件事。**
- 2026 四岛请愿有 35 个赞同团体，其中 14 个可与现有 registry 做候选 crosswalk；它是事件超边，不是稳定联盟。
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
- `network_membership_candidates_v2.csv`：2025-05-06 的 35 个正式成员主张。
- `four_island_petition_entities_v2.csv`：2026-05-07 的 35 个赞同团体及角色／registry crosswalk。
- `event_roster_overlap_v2.csv`：2023／2025／2026 名单重叠；角色不等价。
- `independent_adoption_panel_v2.csv`：独立采用、媒体归因、名册限定和缺失分开。
- `frame_object_observations_v2.csv`：共同框架与共同对象分离。
- `scale_shift_case_A010_v2.csv`：A010 安装前后尺度转换候选。
- `network_formation_events_v2.csv`：2017–2026 载体／接触／正式行动序列。
- `negative_controls_v2.csv`：负例和竞争解释。
- `academic_connection_v2.csv`：直接案例、历史对照、战争记忆、组织变化和官方反框架的学术连接。
- `human_review_queue_v2.csv`、`local_retrieval_queue_v2.csv`：人工判断与当地材料任务。
- `fig1_carrier_and_object_timeline_v2.svg`、`fig2_roster_overlap_v2.svg`、`fig3_common_frame_vs_common_object_v2.svg`：三张研究图。
- `principal_checkpoint_v2.md`：负责人阅读与选择闸门。
- `validation_report_v2.md`、`manifest.json`：校验与复现信息。

## 硬边界

本包所有行均为 `research_only / candidate / ai_seeded / not_frontend_ready / central_writeback=no`。正式成员主张不生成成员之间的 dyadic 联盟边；共同请愿只生成事件级超边；“契机”是组织方自述；35→38 不写成增长；A010 改名和新别名不自动回写中央。
