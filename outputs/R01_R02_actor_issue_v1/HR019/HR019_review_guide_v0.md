
# HR-019｜R1/R2 分类与解释边界人工复核包

本包不包含 AI 代替人审的决定。所有 `review_decision`、`human_reviewer`、`review_date` 均留空。

## 需要决定的三类问题

1. `HR019_review_v0.csv`：9 个规则／受控词决定。重点是 6 个超出当前 schema 的 `actor_class` 术语，以及 `watchlist_only` 是否应继续作为 review status。
2. `HR019_bridge_actor_review_queue_v0.csv`：30 个“跨议题但尚未形成双侧人审证据”的 actor。复核时必须区分长期组织定位、案件角色和事件性参加。
3. `HR019_edge_scope_review_queue_v0.csv`：65 条当前文字无法可靠判断时间范围的 actor–issue edge。这里只审核 edge 的解释层，不把它改写成组织间关系。

## 推荐决策值

- 受控词：`approve_extension` / `map_to_existing` / `needs_more_context`
- bridge：`include_with_scope` / `candidate_only` / `exclude_from_narrative`
- edge scope：`organizational_positioning` / `institutional_or_case_role` / `event_specific` / `remain_unclear`
