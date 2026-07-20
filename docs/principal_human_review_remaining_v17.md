# 项目负责人人工复核剩余任务盘点 v17

日期：2026-07-20

口径：HR-035 Batch 1、HR-010 batch 6、LCR001–004、HR-034、HR-029、HR-031
均已由负责人确认并完成受控合并。

## 当前正式未闭合：12项

| 类别 | 数量 | 状态 |
|---|---:|---|
| 立即可做的线上决定 | 0 | 本轮正式线上任务已清零 |
| 有依赖、后做的线上决定 | 0 | HR-029／031 已闭合 |
| 当地／新一手材料决定 | 12 | HR-017：9；HR-018：2；HR-024/A073：1 |
| **合计** | **12** | 10项等待材料后决定；HR-018两项已有 defer 决定并等待新材料 |

## 已闭合在线任务

- HR-035 Batch 1：15条，accept 6／revise 8／reject 1；
- HR-010 batch 6：47条，accept 46／defer 1；
- LCR001–004：4条，accept_status 1／revise_status 3；
- HR-034：50条，revise 49／reject 1；
- HR-029：41条，accept 28／revise 13；
- HR-031：3条，全部选择 B。

正式记录：

- `docs/human_review_return_HR035_batch01_v1.md`
- `docs/human_review_return_remaining_online_145_v1.md`
- `docs/principal_human_review_master_return_2026-07-20_v1.md`

## 当地／新材料12项

### HR-017：9项

需要公投程序、诉讼或制度流程的当地报刊、判决／决定原件、馆藏或等价一手材料。在线资料
不足时不得虚构精确日期、主体或程序结果。

### HR-018：2项

两项已有 `deferred_local_or_internal_record` 决定，等待 Form 990、组织年报、内部财务记录或
等价材料。不得把长期累计金额拆给具体 recipient 或年度。

### HR-024/A073：1项

A073 已 `online_exhausted`。需要当地资料确认独立组织身份；不得从 issue tag、近似名称或一次
事件出现反推 actor 身份。

## 尚未正式派发的事实债务

HR-035 审计另识别出旧人审字段补全和其余 actor–issue 候选事实债务。它们仍在前端／审计层
显示为未冻结，但尚未形成新的正式 HR batch，因此不计入当前12项。若要继续，应另行生成
HR-035 Batch 2，并再次保持“AI调查、负责人判断、逐批留报告”的节奏。

## 下一步

1. 线上正式人工任务暂时清零；
2. 不在缺少当地材料时强行关闭12项；
3. 先完成冻结后图件／前端重生和最终 codebook lint；
4. 是否派发 HR-035 Batch 2，由负责人另行决定。
