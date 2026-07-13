# Registry value gate v2

日期：2026-07-13

这个包执行 NW2-C，只做组织级候选的机器证据门控。它没有修改 actor registry、source log、issue/place/event/relation 中央表，没有分配 A 号，也没有把候选关系写成事实边。

## 结果

- 完整评估 5 个组织级候选；首要对象 `宮古島地下水研究会` 已完成四门核查。
- 4 个达到 `ready_for_human_decision`：宮古島地下水研究会、宜野湾ちゅら水会、全日本港湾労働組合沖縄地方本部、新日本婦人の会沖縄県本部。
- 1 个 `defer_online_continuity_gap`：八重山大地会。它有 2015–2017 组织级证据，但缺 2018–2026 的持续／解散／承继记录，不送 HR-027。
- `ready_for_human_decision` 不是 add 决定。四个候选仍须由 HR-027 人工选择 add/defer/reject，并冻结 alias、actor class、issue scope 和边界措辞。

## 文件

- `registry_value_gate_v2.csv`：五候选四门、排序、机器建议与边界。
- `four_gate_evidence_matrix_v2.csv`：5 × 4 = 20 条逐门证据矩阵。
- `alias_duplicate_crosswalk_v2.csv`：12 条别名／近名／既有 actor 去重记录。
- `source_proposals_v2.csv`：29 条历史 source proposal；原始 `source_log_match` 只标 S158/S204，29/29 `relation_or_claim_approved=no`。
- `source_log_provenance_v2.csv`：建包时的候选来源整合快照（S001–S294）中的 29/29 URL 交叉表；其中 27 条为 NW2-H provisional source index。S295 属于该批完成后的补充来源，明确不纳入本候选来源批快照；快照索引存在不批准 actor、edge 或 claim。
- `HR027_registry_value_review_v0.csv`：4 条真正达到人工决定门槛的任务；按稳定候选任务号保留人审字段，当前已填写 decision 0 条。
- `registry_value_gate_brief_v2.md`：排序、解释增量与强制边界。
- `validation_report_v2.md`：脚本内机械校验结果。

中央可消费的候选副本为 `data/interim/34_registry_value_candidates_v2.csv`，内容与本包 gate 表逐字节一致。

## 明确排除

- A073 的退出／保留继续由 HR-024 控制；本包不重复创建任务。
- C015 继续属于 HR-011；宮古島地下水研究会的证据不能替代 C015 身份复核。
- 一次署名、一般公益使命、共同参与或单场活动均未被当作持续组织证据。
- 来源提案不批准 actor 入表、alias、edge、联盟、资金或因果解释。
