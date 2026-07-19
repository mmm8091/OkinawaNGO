
# HR-019｜R1/R2 分类与解释边界人工复核包

三张任务表均已由负责人完成；本轮重生只保留其历史决定，不重开或覆盖人工字段。

## 三类复核记录

1. `HR019_review_v0.csv`：9 个规则／受控词决定。
2. `HR019_bridge_actor_review_queue_v0.csv`：30 个跨议题 actor 的解释边界决定。
3. `HR019_edge_scope_review_queue_v0.csv`：76 条 actor–issue edge 的时间／案件／事件范围决定；只审核解释层，不把它改写成组织间关系。

## 推荐决策值

- 受控词：`approve_extension` / `map_to_existing` / `needs_more_context`
- bridge：`include_with_scope` / `candidate_only` / `exclude_from_narrative`
- edge scope：`organizational_positioning` / `institutional_or_case_role` / `event_specific` / `remain_unclear`
