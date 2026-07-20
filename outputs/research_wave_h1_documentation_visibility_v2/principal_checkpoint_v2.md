# H1 v2 负责人检查点

状态：`principal_interpretive_decision_required`。本包维持 `not_frontend_ready`。

## 建议负责人先读的 8 个反例

- X016 Marine Officers' Spouses' Club Okinawa (MOSCO / MOSC)：dense_registry_trace_low_actor_issue_degree；registry 4 源／全部 linked 4 源，1 个 issue edges。
- X004 American Welfare & Works Association (AWWA / 米国福祉事業協会)：dense_registry_trace_low_actor_issue_degree；registry 6 源／全部 linked 10 源，2 个 issue edges。
- A002 ジュゴン保護キャンペーンセンター（Save the Dugong Campaign Center）：dense_registry_trace_low_actor_issue_degree；registry 4 源／全部 linked 7 源，2 个 issue edges。
- A008 NGO非戦ネット：dense_registry_trace_low_actor_issue_degree；registry 4 源／全部 linked 4 源，2 个 issue edges。
- A047 沖縄平和運動センター：thin_registry_trace_high_actor_issue_visibility；registry 1 源／全部 linked 1 源，4 个 issue edges。
- A102 全国公害弁護団連絡会議：thin_registry_trace_high_actor_issue_visibility；registry 1 源／全部 linked 1 源，4 个 issue edges。
- A104 普天間基地爆音訴訟弁護団：thin_registry_trace_high_actor_issue_visibility；registry 1 源／全部 linked 1 源，4 个 issue edges。
- A105 日本YWCA：thin_registry_trace_high_actor_issue_visibility；registry 1 源／全部 linked 3 源，4 个 issue edges。

四个 dense-low 与四个 thin-high 已平衡抽取。请逐个判断：是 issue 标签过宽／过窄、组织范围不同，还是确有“registry 来源痕迹与编码可见度不一致”。

## 先处理的来源 crosswalk

`unresolved_reference_audit_v2.csv` 有 9 个 legacy-token actor。它们未进入主要 proxy sensitivity 或 matched pairs；不要把 0 个已解析 S-source 写成“没有材料”。

## 建议抽读的 matched pairs

- A008 ↔ A027（冲绳本地公民行动 | nonlocal_or_institutional | formal_or_incorporated_guess）
- A076 ↔ A087（冲绳本地公民行动 | okinawa_local | formal_or_incorporated_guess）
- A113 ↔ A013（冲绳本地公民行动 | okinawa_local | informal_unclear_or_program）
- A112 ↔ A017（冲绳本地公民行动 | okinawa_local | informal_unclear_or_program）
- A010 ↔ A024（冲绳本地公民行动 | okinawa_local | informal_unclear_or_program）
- A011 ↔ A025（冲绳本地公民行动 | okinawa_local | informal_unclear_or_program）
- A014 ↔ A015（冲绳本地公民行动 | okinawa_local | informal_unclear_or_program）
- A052 ↔ A029（冲绳本地公民行动 | okinawa_local | informal_unclear_or_program）
- A053 ↔ A047（冲绳本地公民行动 | okinawa_local | informal_unclear_or_program）
- A114 ↔ A089（劳工／教育组织 | okinawa_local | informal_unclear_or_program）

完整 12 对见 `matched_actor_pairs_v2.csv`。dense/thin 只按 registry_source_count 定义；匹配只是缩小功能／来源差异，不是因果设计。

## 需要负责人拍板

1. H1 在一期报告中的位置：
   - 建议：方法／偏差章节的核心敏感性；
   - 可选：独立方法短文候选；
   - 暂不建议：主论文的实质性中心命题。
2. 是否接受当前最强措辞：
   - “移除 S004 的证据支持，会使当前 234 条 E3/E4 编码边中的 41 条失去全部已列支持”；
   - “总来源相关是 construction diagnostic；registry-only 与 outcome-excluded proxy、reviewed 与 candidate 层给出不同结果，现阶段不能确认 H1”。
3. 是否批准一轮 **36 actor 以内** 的人工 capacity crosswalk：
   - 先补 9 个 legacy X-token 的 source crosswalk；
   - 自有官网／第三方 host；
   - 日英双语原文，而非标题；
   - staff／律师／秘书处／Web team；
   - 成立、重组、终止与右删失；
   - 固定时间窗的外部报道。
4. 是否将 H3 的“秘书处＋Web team 与真实协调同组织共存”仅列为跨包机制候选，不合并为本包事实。

## 停止条件

若负责人不批准第 3 项，本包在这里停止，作为 H1 方法附录即可；不得继续把 proxy 强化成 actor capacity 或 causal effect。
