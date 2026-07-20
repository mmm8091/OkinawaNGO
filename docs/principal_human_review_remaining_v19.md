# 项目负责人人工复核剩余任务盘点 v19

日期：2026-07-20

口径：继承 v18。HR-035 Batch 2 的 23 项人工决定已由项目负责人全部确认并完成中央受控
合并；本文件是当前人工决定总账。人工决定、中央合并与最终合同产物仍分开记录。

## 当前正式未闭合人工决定：12 项

| 类别 | 数量 | 状态 |
|---|---:|---|
| 立即可做的线上决定 | 0 | HR-035 Batch 2 已确认并合并 |
| 有依赖、后做的线上决定 | 0 | 当前无已派发空白决定 |
| 当地／新一手材料决定 | 12 | HR-017：9；HR-018：2；HR-024/A073：1 |
| **合计** | **12** | 均等待当地或新一手材料 |

## HR-035 Batch 2：23 项已闭合

正式回传：

`docs/human_review_return_HR035_batch02_v1.md`

确认计数：

- identity：1 accept、4 revise；
- actor–issue：7 accept、9 revise、2 defer_second_source。

两条 `defer_second_source` 是已经完成的人工决定，不是空白人审项：

- AI157：新外交イニシアティブ（ND）—legal；
- AI158：新外交イニシアティブ（ND）—local_autonomy。

它们形成后续在线补源线索；只有新材料登记、归档并形成新任务时，才重新进入人工决定
计数。

## 当地／新材料 12 项

- HR-017：9 项公投／程序当地材料；
- HR-018：2 项已有 `deferred_local_or_internal_record` 决定，等待 Form 990／年报／
  内部记录；
- HR-024/A073：1 项已经 online exhausted，等待独立身份材料。

## 集成状态

HR-035 Batch 2 已由专用、可重复运行的
`scripts/merge_hr035_batch02_v1.py` 合并到中央 actor registry 与 actor–issue 表；旧的
Batch 1 合并函数未被复用。R1/R2、strict place–issue、coverage 与探索系统均已重生。

合并后 actor–issue 中央表为 294 条历史行、283 条当前有效边，其中 141 条人审、142 条候选；
strict place–issue 为 306 条当前同源三元组，其中 81 条两端均人审。验证报告见
`outputs/hr035_batch02_integration_v1/validation_report_v1.md`。

## 不得误读

- “当前线上人工决定为 0”不表示所有研究缺口已消失；
- AI157、AI158 是确认后的补源需求，不是已接受事实边；
- 12 项当地任务不因 Batch 2 完成而关闭；
- 本轮人工回传与中央合并均已完成，但这不等于 12 项当地任务、最终图版或合同产物完成。
