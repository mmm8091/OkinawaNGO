# HR-034 review_status crosswalk v1

日期：2026-07-20  
状态：**50项已由负责人确认并完成中央受控迁移**

## 交付

- `HR034_review_status_crosswalk_v1.csv`：50 个已确认任务。
  - 45 个中央 source-log 逐行任务；
  - 1 个中央 actor–issue 逐行任务（当前实际为 AI068；AI067 已是 `rejected`）；
  - 4 个表级政策任务。
- `downstream_mechanical_impacts_v1.csv`：9 个派生影响点，只在上游决定后机械重生，不重复人审。
- `validation_report_v1.md`：计数与空白字段门禁。

## 为什么不能自动迁移

`verified`、`human_verified`、`accepted`、`qa_safe_online`、`watchlist_only`
以及 lifecycle 的 queue/workflow 名称分别混合了“资料可用”“模块纳入”“人工流程”
和“展示边界”。它们不能仅凭字符串自动视为 `human_checked`。

中央逐行旧值分布：{'human_verified': 35, 'rejected_archive_mismatch': 1, 'verified': 9, 'watchlist_only': 1}。

## 表级政策范围

- R4：10 行 `qa_safe_online`；
- R9：29 行 `accepted`；
- heterogeneous repertoire：49 行 `accepted`，是上游 R9 记录的派生投影；
- lifecycle：4 行把 identity/continuity queue 状态写进了 `review_status`。

## 强制边界

- 所有 `decision`、`revised_review_status`、`human_reviewer`、`review_date`、
  `review_note` 均已填写；reviewer 为 `project_principal_user`。
- 来源状态迁移不批准 actor、edge、资金关系或解释性结论。
- AI067 已被 HR-019 拒绝；本包只处理当前仍为 `watchlist_only` 的 AI068，
  且不据此恢复冲绳连接。
- table policy 只决定字段语义与迁移规则；不能把 10/29/49 行批量推定为人审通过。
- lifecycle 的工作流状态已与 `review_status` 分栏；线上未见活动不等于解散。
  LCR001–LCR004 已由独立生命周期决定合并。

`make_review_status_crosswalk_v1.py` 现为 pre-review provenance builder，不得在当前迁移后中央层
重新运行。
