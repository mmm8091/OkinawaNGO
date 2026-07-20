# 前端同步说明：actor–issue 人审状态不是数据未同步

日期：2026-07-20  
对象：探索系统前端／NR-02 构建 session  
状态：可立即实施；不等待 HR-035 回交

## 一句话结论

前端已经读到当前中央数据，`65 已核／173 研究／238 有效` 的切分本身正确。此前的误判是
把“解释范围已审”“事实边已审”和“schema v1 字段已冻结”混成了一个人审状态。

当前 manifest 的 actor–issue 输入哈希为
`954233c440a988d067a83090344578a93f6eba910a1757eb3dc59c3837a04628`，
与中央 `data/interim/07_actor_issue_edges_initial_v0.csv` 一致；不是旧数据或漏跑构建。

## 当前四种真实状态

| 前端状态 | 数量 | 准确含义 |
|---|---:|---|
| 字段已冻结·有限确认 | 7 | HR-024 已填完 v1 字段；均为案件限定的 `supported_bounded` |
| 人工接受·字段待冻结 | 58 | 旧批次已接受事实边，但缺 `claim_status/reviewed_fields` 等 v1 字段 |
| 范围已审·事实待审 | 59 | HR-019 已决定长期定位／案件角色／事件标签，但没有批准事实边 |
| 事实待审 | 114 | 尚未完成上述 scope 人审，也未完成事实边人审 |

合计关系：

- 人工接受层：`7 + 58 = 65`；
- 研究层：`59 + 114 = 173`；
- 当前有效：`65 + 173 = 238`。

59 条“范围已审·事实待审”进一步分为：

- `ai_seeded` 44；
- `needs_second_source` 13；
- `needs_local_retrieval` 2。

整个 173 条研究层中仍有 25 条待二源、5 条待当地材料。不要把“143 条
`ai_seeded`”写成“143 条从未被人看过”。

## 已完成任务的正确解释

- HR-019 已完成 115/115：9 条规则、30 个 bridge 解释、76 条 edge scope；它不批准事实边。
- HR-024 线上边 7/7 已合并；唯一 A073 项已 `online_exhausted`，不应生成边。
- HR-025 已完成 actor–place 复核；它不会增加 actor–issue 或组织关系边。
- 不得要求负责人重做 HR-019 bridge／scope，也不得称 HR-024／025 “未填完”。

## 构建端立即改动

在 `normalize_actor_issue` 中从中央行输出并明确派生三个互不替代的状态：

1. `fact_gate_status`
   - `human_accepted`
   - `fact_pending`
   - `needs_second_source`
   - `needs_local_retrieval`
2. `scope_gate_status`
   - `scope_reviewed`
   - `scope_pending`
3. `schema_freeze_status`
   - `field_frozen`
   - `legacy_field_freeze_pending`

同时透传：

- `claim_status`
- `review_scope`
- `reviewed_fields`
- `scope_kind`
- `scope_claim_status`
- `scope_approved_formulation`
- `scope_boundary`
- `confirmed_scope`
- `missing_scope`
- `approved_formulation`

上述状态由构建端按中央字段生成；React 前端只消费，不自行从一个 `review_status` 猜出其余
状态。当前 58 条 legacy 行不得被脚本自动补成 `supported`。

## UI 文案

研究视图总说明使用：

> 人工接受记录 65 条，事实待审记录 173 条；事实待审中有 59 条已经完成解释范围复核，
> 但尚未完成关系事实复核。

建议给每条 actor–issue 记录显示主状态：

- `字段已冻结·有限确认`
- `人工接受·字段待冻结`
- `范围已审·事实待审`
- `事实待审`

并按需叠加：

- `待二源`
- `待当地材料`

“已核视图”帮助文案继续明确：已核的是当前显示的事实边，不是所有可搜索 actor 的身份。

## HR-035 与刷新顺序

HR-035 专门补此前缺失的 actor–issue 事实／字段冻结，不重开 HR-019。当前先派
15 条案件、公投和程序边的事实复核：

`outputs/actor_issue_claim_freeze_v1/HR035_actor_issue_fact_review_batch01_v1.csv`

前端现在即可实现上述三门状态；不必等待决定。HR-035 每批合并后再运行：

```powershell
python scripts\make_r01_r02_actor_issue.py
python scripts\make_strict_place_issue_v1.py
python scripts\make_coverage_audit_v1.py
python scripts\build_exploration_system_data_v1.py
```

计数必须从新 manifest 读取，不得把 65／173 硬编码为永久值。

## 禁止事项

- 不把 59 条 scope 已审记录升入已核事实层；
- 不自动由 `human_checked` 推导 `claim_status=supported`；
- 不自动替 58 条 legacy 行填 v1 字段；
- 不从 registry `issue_tags` 生成 actor–issue 边；
- 不让 A073 生成边；
- 不把 HR-019 bridge 解释画成组织—组织关系；
- 不把 HR-025 地点记录计入 actor–issue；
- 不用节点面积、度数或边宽暗示影响力。

## 验收

- 当前基线仍为 `65／173／238`，且构建 hash 与中央输入一致；
- 精确显示 `7／58／59／114` 四种状态；
- 25 条显示待二源，5 条显示待当地材料；
- A073 无边，HR-019 bridge 不生成边，HR-025 不改变 actor–issue 计数；
- 页面不再出现“173 条均未人审”或“HR-019/024/025 尚未完成”的笼统表述；
- HR-035 合并后四类计数自动随 manifest 更新。
