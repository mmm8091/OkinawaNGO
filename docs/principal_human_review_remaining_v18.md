# 项目负责人人工复核剩余任务盘点 v18

日期：2026-07-20

口径：在 v17 的12项当地／新一手材料任务上，正式加入 HR-035 Batch 2。v17 保留为
“线上任务清零”时点的历史快照，本文件是当前权威总账。

## 当前正式未闭合：35项

| 类别 | 数量 | 状态 |
|---|---:|---|
| 立即可做的线上决定 | 23 | HR-035 Batch 2：18 edge facts＋5 identity companions |
| 有依赖、后做的线上决定 | 0 | 无 |
| 当地／新一手材料决定 | 12 | HR-017：9；HR-018：2；HR-024/A073：1 |
| **合计** | **35** | 23项可立即阅读判断；12项等待新材料 |

## HR-035 Batch 2：23项

正式任务书：

`docs/human_review_task_HR035_batch02_v1.md`

填写文件：

- `outputs/actor_issue_claim_freeze_v1/HR035_actor_issue_fact_review_batch02_v1.csv`
- `outputs/actor_issue_claim_freeze_v1/HR035_actor_identity_companion_batch02_v1.csv`

辅助来源：

- `outputs/actor_issue_claim_freeze_v1/HR035_source_bundle_batch02_v1.csv`
- `outputs/actor_issue_claim_freeze_v1/validation_report_batch02_v1.md`

本批是18条 E4、scope 已人审但 fact 仍为 `ai_seeded` 的完整当前集合；另为5个身份仍为
`ai_seeded` 的 actor 各设一次配套决定。身份与边不得相互替代。

## 当地／新材料12项

- HR-017：9项公投／程序当地材料；
- HR-018：2项已经 defer、等待 Form 990／年报／内部记录；
- HR-024/A073：1项已经 online exhausted、等待独立身份材料。

## 当前顺序

1. 先判断5条 actor identity companions；
2. 再按 actor 成组判断18条 actor–issue facts；
3. 主线程生成回交报告并受控合并；
4. 12条当地任务继续等待材料，不因 Batch 2 强行关闭。

## 不得误读

- 当前正式在线人工任务不再是0，而是23；
- 23项任务是人工决定数，不是23条新事实；
- E4、scope 已审或有官网均不等于自动接受；
- 事实边接受不批准稳定联盟、资助、影响力或因果；
- identity defer／reject 时，相应边不得仅凭 edge 决定进入默认已核图。
