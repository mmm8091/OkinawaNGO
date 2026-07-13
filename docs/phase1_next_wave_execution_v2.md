# 一期下一轮线上执行简报 v2

日期：2026-07-13

验收权威：`source_docs/current/复归后冲绳民间组织 _ NGO 分类与议题网络一期研究方案 (3).docx`
起点底盘：118 actor、247 source、222 actor–issue、125 actor–place、65 AEV

## 总目标

在派当地协作者前，补齐原方案中仍最薄的线上解释闭环：R3 空间关系与先岛 dossier、R9 选举侧、R5/R7 异质行动比较，并用价值驱动方式找回 registry 至少 120 的组织级下限。所有新事实先进入候选／人工任务层，不直接改中央 registry、source log 或正式关系表。

## NW2-A：R3 空间语义与先岛 dossier（P0）

输入：125 条 actor–place edge、place/venue taxonomy、R4 先岛语料、R9 公投链、现有来源和归档。

输出：

- `data/interim/32_actor_place_semantic_candidates_v1.csv`
- `outputs/R03_spatial_dossier_v1/`：全量空间关系图、关系类型构成图、与那国／石垣／宫古三地 dossier、来源交叉表、brief
- `HR025_actor_place_semantics_review_v0.csv`：只收无法机械冻结的 HQ/site/event/target/institutional-venue 语义项，人工字段全空
- 幂等生成脚本

done_when：125/125 条边都有候选语义与解释边界；三地 dossier 分开写“已证事实／候选解释／当地缺口”；与那国继续使用前线／自治／公投／台湾邻近／生命安全框架，不强行环境化；图中候选边与人审边视觉分层。

## NW2-B：R9 选举—市民组织接口（P0）

范围：2014、2018、2022 冲绳县知事选的组织公开声明、议题活动、集会／请求或制度介入窗口。个人候选人与政党只作事件／制度对照节点，不进入 NGO registry。

输出：

- `data/interim/33_r09_election_civic_events_v1.csv`
- `outputs/R09_election_civic_interface_v1/`：三届事件窗口表、组织介入方式图、非因果机制图、来源提案、brief
- `HR026_election_civic_role_review_v0.csv`：敏感 actor–event role 与措辞项，人工字段全空
- 幂等生成脚本

done_when：三届都有公开可核的事件窗口或明确 `online_exhausted`；严格区分 endorsement、issue campaign、public meeting、request、observation；不声称组织导致票数、胜负或民意变化。

## NW2-C：Registry 价值驱动补样（P1）

首要对象：`宮古島地下水研究会`。继续从 PFAS／健康、先岛地方组织、女性／劳工薄层找至少三个组织级候选；A073 的退出／保留继续由 HR-024 控制，不重复建任务。

输出：

- `data/interim/34_registry_value_candidates_v2.csv`
- `outputs/registry_value_gate_v2/`：身份／持续性／一期直接连接／模块修复价值四门 gate、别名去重、source proposal、brief
- `HR027_registry_value_review_v0.csv`：只把真正达到人工决定门槛者送审，决定栏全空
- 幂等验证脚本

done_when：宮古島地下水研究会有明确 add/defer/reject 的机器建议与边界；至少三个其他候选完成在线 gate；不得把一般公益使命、一次活动名称或共同署名当组织持续性；不得自动分配 A 编号或写中央边。

## NW2-D：R5/R7 异质行动与场域比较（P1，前三线回收后启动）

输入优先使用已人审 AEV、R8、R9、R10 正式事实；补入噪音诉讼、公投、现场行动、公共集会、行政协作，与三次环保联署比较。

输出：统一 actor–event–venue–target 表、行动 repertoire 图、跨案例场域小倍图、brief；若必须新增事实，则创建 `HR028_heterogeneous_event_review_v0.csv`，不得让 AI 自审。

done_when：至少五类行动和四类场域可比；共同出现不升级为稳定联盟；流程顺序不画成因果效果。

## 后续冻结与正式交付

前三线回收后，主线程依次：

1. 将 HR-019、HR-024–027 与既有 HR-016–022 汇总为不重复的人工作业；
2. 冻结 actor class、legal status、alias、place hierarchy、venue 和 relation type；
3. 重生五类核心图与报告图注；
4. 先制作 25–35 页 DOCX/PDF 研究报告，再从同一冻结底盘派生论文和 PPT；
5. 只有报告明确指出“该字段会改变图或解释且线上已耗尽”时，才从 Tier 2 派当地协作者。

## 子线程写入边界

- 每条线只写自己的 `data/interim/32–35`、`outputs/<package>/` 与生成／验证脚本。
- 不改中央 actor/source/issue/place/event/relation 表，不改 workbench、验收审计或研究报告。
- 新 URL 只做 source proposal；主线程统一去重、编号、归档。
- 人工任务的 decision、reviewer、review_date、review_note 一律留空。
