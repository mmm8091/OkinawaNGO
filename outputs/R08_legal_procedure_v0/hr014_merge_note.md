# HR-014 人工复核落库说明

日期：2026-07-13
人工结论提供者：user
合并脚本：`scripts/merge_hr014.py`

## 落库结果

- `data/interim/17_legal_policy_procedure_cases_v0.csv`：六案均由 `needs_human_review` 更新为 `human_checked`。
- 六案原有 `claim_summary` 和 `outcome_summary` 保持不变；`interpretation_limit` 改为 HR-014 已确认的案件特定边界。
- `outputs/R08_legal_procedure_v0/case_actor_roles_v0.csv`：27/27 角色均更新为 `human_checked`，原始细分角色保留。
- 新增 `data/interim/18_legal_policy_actor_roles_v0.csv`：27/27 角色 `human_decision=accept`，来源回指由 R8S 候选编号规范化为主 source log 的 S 编号。

## 关键角色边界

| 对象 | 案件 | 审定角色 | 限制 |
|---|---|---|---|
| A020 JELF | R8C01 Dugong | plaintiff | 在本案不是 counsel；不得外推到泡濑。 |
| A009 Earthjustice | R8C01 Dugong | counsel | 不是 named plaintiff。 |
| A002 / A019 | R8C01 Dugong | non_party | 组织不得继承相关个人或案外倡议活动的原告身份。 |
| A052 | R8C03 第三次嘉手纳 | plaintiff_group（family=plaintiff） | crosswalk 人审通过；不得推断每位居民的组织成员身份或跨轮次人员恒定。 |
| 第三次嘉手纳弁护团 | R8C03 | counsel | 仅为 provisional procedural collective `P8E004`，不建 actor。 |
| A053 | R8C04 普天间 | plaintiff_group（family=plaintiff） | crosswalk 人审通过；合并案件和其他轮次不得推断人员完全相同。 |
| A011 | R8C05 石垣住民投票 | requester | 不是 named organizational plaintiff。 |
| A055 | R8C06 泡濑 | supporter | 不是组织原告或 counsel。 |
| A020 JELF | R8C06 泡濑 | supporter | 是材料发布／法律网络支援角色，不继承 Dugong 案 plaintiff 身份。 |

## 新角色表结构

`18_legal_policy_actor_roles_v0.csv` 将关系角色与主体登记分开：

- 已登记组织使用 `actor_id`，并通过 actor registry 外键检查。
- 外部机构、个人、匿名居民集合和案件律师集合使用 `provisional_entity_id`（P8E 前缀）及 `entity_kind`。
- 每行必须且只能有一个 `actor_id` 或 `provisional_entity_id`。
- provisional ID 只在案件角色表内稳定引用，不是 actor，不写入 actor registry。
- `role` 保留 plaintiff_group、counsel_secretariat 等原始细分；`role_family` 用于严格区分 plaintiff、counsel、requester、supporter、non_party 及其他制度角色。

角色 family 计数：plaintiff 10、counsel 5、requester 1、supporter 2、non_party 2、defendant 4、commenter 1、proponent 1、institutional_recipient 1。

## 案件结果边界

- Dugong 案保留“程序性标准／信息生产效果”与最终 DoD 胜诉并存的结果，不写成阻止工程。
- 环评程序只确认 NACSJ 的正式意见提交，不把程序存在外推给其他组织，也不推定行政机关接受意见。
- 第三次嘉手纳保留禁止请求／未来损害被驳回与过去损害赔偿维持的分项结果。
- 普天间保留部分赔偿、其余驳回的案件特定结果，不写成运营禁令。
- 石垣住民投票案保留因非行政处分而驳回的程序结果；A011 是 requester，不是组织原告。
- 泡濑第一、第二轮结果分开，不合并为单一胜负。

## 校验

脚本执行以下硬校验：

1. 恰好六案、27 个唯一角色，全部 `human_checked`，27 个决定全部 `accept`。
2. case FK、已登记 actor FK、主 source FK 全部存在。
3. A052/A053、A011、A055、A020、A002、A019、Earthjustice 的角色边界逐项断言。
4. A020 必须且只能是 R8C01 plaintiff、R8C06 supporter。
5. 第三次嘉手纳 counsel 必须保持 `P8E004` provisional 节点，actor_id 为空。
6. 六案解释边界包含必要的非外推／分轮次限制。
7. 连续运行两次后，三张目标 CSV 的 SHA-256 均不变，幂等测试通过。

## 未修改范围

本次未修改 actor registry、source log、控制文档、通用 funding/support 关系表或其他主表；未创建第三次嘉手纳 counsel actor，也未提交 git。
