# HR-033：legacy `verified` 关系状态归一化

日期：2026-07-20  
任务性质：敏感关系人工决定；不要求重新做大范围检索  
依据：`data/metadata/coding_schema_v1.md`  
输入：`data/interim/15_funding_or_support_edges_sample_v0.csv`
状态：**已完成并由主线程合并**

回交：`docs/human_review_return_HR033_legacy_relation_status_batch30_v1.md`  
合并：`scripts/merge_hr033.py`、`outputs/hr033_integration_v1/`

## 任务目的

早期关系表使用了不在正式 schema 中的 `verified`。本任务不把它自动解释为
`human_checked`，而是逐行确认：

1. 哪个事实已经核实；
2. 哪些字段仍不完整；
3. 该记录是否为真正 actor—actor 关系；
4. 应迁移为 `human_checked`、`human_revised`、`needs_*` 或 `rejected`。

## 回填格式

每行填写：

- `decision`：accept / revise / defer / reject
- `new_review_status`
- `review_scope`
- `reviewed_fields`
- `claim_status`
- `confirmed_scope`
- `missing_scope`
- `graph_eligibility`
- `interpretation_limit`

## 待复核六行

### F006 AWWA → NOSCO

- 原关系：`network_membership`
- 原证据：S041；S055；S072，E4
- 当前可见边界：伞状组织／成员关系，不是资助
- 待决定：方向与端点角色是否准确；是否迁移为 `human_checked`
- decision：

### F007 AWWA → KOSC

- 原关系：`network_membership`
- 原证据：S041；S055；S072；S075，E4
- 当前可见边界：伞状组织／成员关系，不是资助
- 待决定：方向与端点角色是否准确；是否迁移为 `human_checked`
- decision：

### F021 OESC → USO Okinawa

- 原关系：`donation`
- 原证据：S053，E4
- 当前命题：2025-12 OESC 向 USO Okinawa 捐赠 3,250 美元
- 待决定：关系、方向、金额和日期是否均接受
- decision：

### F022 AWWA → OESC

- 原关系：`network_membership`
- 原证据：S041；S055，E4
- 当前可见边界：伞状组织／成员关系，不是资助；F008 为本行重复项并已 rejected
- 待决定：方向与端点角色是否准确；是否迁移为 `human_checked`
- decision：

### F023 AWWA → MOSCO

- 原关系：`network_membership`
- 原证据：S041；S055；S079，E4
- 当前可见边界：伞状组织／成员关系，不是资助
- 待决定：方向与端点角色是否准确；是否迁移为 `human_checked`
- decision：

### F025 KOSC → AWWA／奖学金项目

- 原关系：`funding_contribution`
- 原证据：S075，E4
- 当前命题：KOSC页面报告上一年度向奖学金和AWWA等提供合计10.2万美元
- 已知缺口：无法把总额拆给AWWA或任一recipient；完整年度明细仍需报告
- 待决定：应作为 `supported_bounded` 的 actor—actor关系、aggregate observation，
  还是继续 defer
- decision：

## 强制边界

- 不因 E4 自动接受整行；
- 不因 `verified` 自动进入已核视图；
- membership 不写成 funding；
- 合计金额不拆给单一recipient；
- 负责人只需复核现有来源和边界，不需要替AI扩展新关系。

## 合并结果（2026-07-20）

- F006／F007／F022／F023：`human_checked`；
- F021／F025：`human_revised`；
- legacy `verified`：0；
- F025 保留无金额 KOSC→AWWA `supported_bounded` 关系；
- USD 102,000 仅保存在 `R10R029` composite-recipient aggregate observation，不上组织关系图。
