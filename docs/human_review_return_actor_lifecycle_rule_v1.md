# Actor 生命周期标记规则确认记录 v1

日期：2026-07-19  
承办人：项目负责人  
辅助整理：Codex  
状态：**规则已确认；首批种子表已建立**

## 1. 发现的问题

中央 actor registry 当前没有 `active_status`、`dissolution_date`、`active_period` 或等价字段。`review_status` 只描述证据／人工复核状态，不能表示组织当前是否活动。

组织解散、休止、改组和持续性缺口此前散落在：

- actor `notes`；
- 事件／程序时间线；
- registry expansion 候选包；
- 单项人工复核报告。

这会导致历史组织在当前网络图、组织数量和桥梁名单中被误读为仍在活动。

## 2. 负责人确认的处理

负责人于 2026-07-19 确认：

1. 先建立独立生命周期表和人工复核队列；
2. HR-019 进行期间不直接扩展中央 actor registry；
3. 待 HR-029 schema freeze 时再决定如何并入最终 codebook／registry；
4. 不以“近期没有检索到活动”推定组织已经解散或停止活动。

## 3. 受控状态

首版 `lifecycle_status` 使用以下少量值：

- `active_confirmed`：在明确截止日期仍有可核组织级活动；
- `dissolved`：有组织决议、官方法人记录或等价来源确认解散；
- `reorganized`：组织明确发展性解散、改组或转入后继组织；
- `dormant_reported`：组织／官方年度材料明确报告休止或无主要活动；
- `continuity_unverified`：只知道最后可观察活动，之后持续、休止、解散或承继状态不明。

边界：

- `continuity_unverified` 不等于 `dissolved`；
- `last_observed_activity_date` 不等于 `activity_end_date`；
- 法律实体仍存在不等于有实质活动；
- 改组／前身—后继关系不等于同一 actor 无缝延续；
- 新闻报道的解散必须保留证据等级和人工复核状态。

## 4. 已建立文件

- `outputs/actor_lifecycle_v1/actor_lifecycle_v0.csv`
- `outputs/actor_lifecycle_v1/actor_lifecycle_review_queue_v0.csv`

首批只纳入本轮已经暴露的六个案例：

- A051：已人工确认 2019-03-26 解散；
- A068：身份修复前保持 `continuity_unverified`；
- A011：2024-11-27 解散为待审候选；
- A065：2018 年后持续性未确认；
- A069：2012 年后持续性未确认；
- C030：已确认解散的 registry 外控制案例。

本轮没有对其余 actor 批量推断生命周期。

## 5. 后续合并门槛

HR-029 前需要：

1. 决定生命周期是并入 actor registry 还是保留一对多历史表；
2. 对明确解散、改组、休止的组织完成人工决定；
3. 为 `status_date`、`last_observed_activity_date` 和 `successor_actor_id` 建立 lint；
4. 所有当前网络图明确选择“全历史 actor”或“指定日期仍活动 actor”口径；
5. 不因 lifecycle source inclusion 自动批准 actor–issue edge、联盟、资金或因果关系。
