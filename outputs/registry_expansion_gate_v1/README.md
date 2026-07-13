# Registry expansion gate v1

日期：2026-07-13

这个包只回答一个机器侧问题：R1/R2 提出的 9 个候选，是否已经具备送交人工作组织级入表决定的证据闭环。它不修改 registry、source log、actor–issue、actor–place 或 event 表，也不把机器 gate 当作人工决定。

## 结果

- `ready_for_human_decision`：8 个（C010、C011、C015、C029、C031–C034）。
- `not_ready_online`：0 个。
- `out_of_scope_candidate`：1 个（C030）。
- 至少两个值得人工决定：是，而且不是为了补足 120 而放宽标准。

`ready_for_human_decision` 只表示身份、持续性／法人状态、一期直接连接和“非一次署名”四道机器门已闭合；最终 `add / defer / reject / historical-only` 必须由人作出。

## 人工任务路由

- C010、C011、C029–C034 是尚未完成的 HR-013 对象，因此使用 `HR013_evidence_addendum_v1.csv`，不新建重复 HR。
- C015 是 HR-011 已暂缓对象，本轮新二源触发 `HR011_C015_reopen_addendum_v1.csv`。
- 两张表的 `decision / reviewer / review_date / review_note` 全部留空。本包不代表 HR-013 或 HR-011 已完成。

## 文件

- `registry_expansion_gate_v1.csv`：9/9 机器 gate 总表。
- `evidence_closure_matrix_v1.csv`：逐候选的身份、持续性和一期连接闭环。
- `source_proposals_v1.csv`：26 条可回溯来源提案；仅 S113 已在主 source log，其他未分配 S 编号。
- `merge_field_candidates_v1.csv`：canonical／alias／issue／place／event 等候选字段，全部待人审。
- `HR013_evidence_addendum_v1.csv`：8 个 HR-013 补证条目。
- `HR011_C015_reopen_addendum_v1.csv`：C015 重开补证条目。
- `registry_expansion_gate_brief_v1.md`：门槛、解释和使用边界。
- `validation_report_v1.md`：由校验脚本生成。

中央可消费副本由 `scripts/validate_registry_expansion_gate_v1.py` 生成到 `data/interim/29_registry_expansion_gate_v1.csv`。生成动作仍不修改任何主表。
