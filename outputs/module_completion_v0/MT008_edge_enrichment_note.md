# MT-008 关系边事件化 note v0

日期：2026-07-13（HR-015 同步）

**目标**：把静态 actor–issue / actor–place 边升级为事件感知数据，用 `event_id`、`action_type` 与 `relation_strength` 区分长期组织定位、事件性署名、法律程序角色、公投参与和分析种子。

## 两层数据，不混用

- `actor_relation_events_v1.csv` 是 **registry-only 派生表**：45 行、9 个事件、5 类 action。它只保留已有 `actor_id` 的组织级角色，用于当前网络图。
- `data/interim/09_actor_event_venue_edges_v0.csv` 是 HR-015 正式事实／分析表：67 行；其中 63 行 `human_checked`、4 行 `analytical_seed`。它保留九个 E2 `unverified_event_participant`，这些名称不在 actor registry。

| action_type | registry-only 行数 | 正式 AEV 行数 |
|---|---:|---:|
| co_signing | 33 | 33 |
| request_letter | 2 | 11 |
| litigation | 5 | 12 |
| referendum | 4 | 4 |
| opinion_ad | 1 | 1 |
| pathway_role | 0 | 4 |

## 解释边界

- 共同署名、共同要请、同场参与只证明一次事件角色，不构成稳定联盟。
- 四条 `pathway_role` 是解释性分析种子，不是事实关系。
- E2 event-only 名称在取得独立身份与持续性证据前不得回填 registry。
- 诉讼中的个人、组织、律师、请求者、支援者与 non-party 必须分开；个人角色不得转嫁给其所属组织。

## 可视化

`fig/fig_event_repertoire.html` 读取 registry-only 表生成当前 repertoire 时间线，气泡面积只表示当前 registry 中可核组织角色数。HR-015 前的旧截图已改名 `fig_event_repertoire_pre_hr015.png`，只作历史快照；正式全量事件参与以 AEV 表为准。

## 下一步

- 从正式 AEV 重做事实事件图，并把四条 analytical seed 分层显示。
- 将嘉手纳、普天间与泡瀬案件按案件／轮次补入 event 层。
- 在不破坏现有 07/08 图脚本前提下，评估把 `event_id`、`action_type`、`relation_strength` 作为可空字段并入下一版边表。
