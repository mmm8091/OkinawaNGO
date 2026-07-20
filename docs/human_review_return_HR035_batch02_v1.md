# HR-035 Batch 2 人工复核回传（负责人已确认）

日期：2026-07-20

任务：E4 actor–issue 事实与组织身份配套冻结

状态：**项目负责人已确认全部 23 项，中央受控合并与下游重生均已完成**

## 1. 权威回传文件

- 18 条事实决定：
  `outputs/actor_issue_claim_freeze_v1/HR035_actor_issue_fact_review_batch02_v1.csv`
- 5 条身份决定：
  `outputs/actor_issue_claim_freeze_v1/HR035_actor_identity_companion_batch02_v1.csv`
- 逐来源包：
  `outputs/actor_issue_claim_freeze_v1/HR035_source_bundle_batch02_v1.csv`
- 证据判断说明：
  `docs/human_review_ai_assist_HR035_batch02_v1.md`
- 可重放确认脚本：
  `scripts/apply_hr035_batch02_ai_assist.ps1`

两张权威 CSV 均已写入：

- `human_reviewer=project_principal_user`
- `review_date=2026-07-20`
- 实际 `reviewed_fields`

## 2. 负责人确认的决定

身份配套：

- `accept_identity`：1
- `revise_identity`：4

actor–issue 事实：

- `accept`：7
- `revise`：9
- `defer_second_source`：2
- `reject`：0
- `defer_local`：0

## 3. 关键修订

1. A007、A018、A049、A066 的身份均保留，但未获来源证明的精确法律形态被改为
   `nonprofit_form_unresolved` 或 `legal_form_unresolved_citizen_group`；A049 的身份
   证据同步降至 E3。
2. AI044 删除错位的 S024，改用直接点名 A018 及其台湾有事框架的 S023。
3. AI119、AI121、AI232、AI234 按直接来源上限由 E4 降至 E3。
4. AI016 只保留 2015 年共同声明事件参与，AI233 只保留 2024 年民用港军事利用争议；
   两项均填写 `scope_revision_required=yes`，不得静默维持一般组织定位。
5. AI157 ND—legal 与 AI158 ND—local_autonomy 确认为
   `defer_second_source / needs_second_source / candidate`。当前 S032 只闭合政策倡议、
   外交智库及沖縄／基地研究主题，不足以冻结精确法律或地方自治边。

## 4. 合并结果与边界

主线程已新增专用、可重复运行的 `scripts/merge_hr035_batch02_v1.py`；没有复用
`scripts/merge_confirmed_remaining_online_reviews_v1.py` 中只支持 Batch 1 的函数。合并器
已完成：

- 5 条 identity 对 actor registry 的字段级回填；
- 16 条 accept／revise edge 对中央 actor–issue 表的回填并进入人审层；
- AI157、AI158 保持 candidate／needs_second_source，不进入默认已核图；
- AI016、AI233 的 HR-019 scope 冲突显式迁移；
- AI044 的 S024→S023 来源替换。

合并后中央 actor–issue 表为 294 条历史行、283 条当前有效边，其中 141 条人审、142 条
候选；R1/R2、strict place–issue、coverage 与探索系统已经重生。strict place–issue 当前有
306 条同源三元组，其中 81 条两端均人审。专用验证与逐行 manifest 位于
`outputs/hr035_batch02_integration_v1/`。

后续仍不得通过旧 pre-human builder 覆盖已完成的人审字段；AI157、AI158 只有在补入独立
二源并形成新的人审任务后才可升级。

## 5. 强制解释边界

- 身份接受与议题边接受是不同决定；
- 共同声明、共同行动与共同署名不生成稳定联盟；
- 分支与母体的行动不得互相转嫁；
- 风险主张不升级为污染、健康、冲突或政策效果事实；
- 本批不批准组织关系、资金关系、人物节点、地点边、事件边或因果结论。
