# HR-024 与 HR-010 batch 6 复核说明

当前状态（2026-07-20）：HR-024 线上项与 HR-010 batch 6 已完成并合并。HR-010 的47项中
46项接受并生成 AI249–AI294，HR010-B6-019 暂缓且没有生成中央 edge；A073 仍为1项当地
材料任务。以下保留为历史复核说明，不能重新作为空白任务表使用。

## HR-024（8项）

- HR024-001：A073 身份与 registry 去留；线上未找到可核实体，不能从 issue_tags 反推 edge。
- 其余项目：A076/A086 已经 HR-014 确认的 Dugong 案件角色，是否映射为相应 issue edge，以及 scope 是否保持 `case`。
- A076 的持续性、法律身份仍沿用 HR-001/当地补查，不在本包伪闭合。

## HR-010 edge-evidence addendum / batch 6

- `HR010_batch6_edge_evidence_addendum_v0.csv` 是 HR-013 前 51 项取证快照；其中 A094 的 4 项已被 HR-013 排除，不再送审。
- 权威回交表为 `post_hr013_HR010_batch6_edge_evidence_addendum_v1.csv`（47项）。A087–A093、
  A095–A101 属于原 HR-010 范围；本表只是 edge-level evidence，不另建 HR-024。
- 为保持取证谱系，post-HR013 表保留原 task ID，A094 对应 ID 空缺不重排。
- `decision/reviewer/review_date/review_note` 已按负责人确认回填；不得再次清空或让历史 builder
  覆盖。

## 复核顺序

1. 先核 actor 归属：总会、分支、人员或临时活动是否被混同。
2. 再核 issue 映射：来源是否直接支持该 issue，而非来自 registry 标签。
3. 再核 scope：`positioning`、`case`、`event` 三选一。
4. 最后核解释边界：事件参与不升为联盟；组织主张不升为事实因果；服务/行政机构不推断政治立场。
