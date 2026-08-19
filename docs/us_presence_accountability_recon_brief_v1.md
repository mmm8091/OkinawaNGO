# 对美问责侧第一轮补强：从“参与过”到“谁在组织、谁在办案、资源如何进入”

日期：2026-08-19

状态：`research_only / principal review required`

## 本轮回答了什么

当前 database 的六个美国来源问责 actor，并不是同一种参与。

- Earthjustice、Center for Biological Diversity、Turtle Island Restoration Network 进入的是同一个可编号诉讼：两家是原告，一家是律师。案件角色已有 R8 人审支持。
- Veterans For Peace Ryukyu/Okinawa Chapter 是本地化的美国退伍军人反军事化节点。新找到的 VFP 官方目录、活动页和会报，已经能给出章节编号、负责人、公开活动和具名协调对象。
- Friends of the Earth U.S. 与 Pacific Environment 在当前冲绳语料中仍主要是 2015 年一次共同声明的参与者；第一轮官方域名检索没有把它们推进为可证明持续性的冲绳项目。

这使原来的“六个参与反基地行动的美国 NGO”可以拆成三种位置：案件型问责、在地化退伍军人行动、国际声明外围。以后画网络时不能把三类都画成同强度的组织节点。

## 新增的资源事实

Earthjustice 的官方 FY2021 Form 990 在“十大法院判给律师费及成本”中列出 `Okinawa Dugong`，金额 276,345.50 美元。这个数值说明诉讼不仅留下案件与判决，也留下了案件级资源记录。

但当前表故意不填资金提供者：990 本身没有在该行说明付款人，也没有把它写成捐赠、grant 或项目预算。下一步应从案件 docket 和 fee order 追出付款依据，再决定能否形成“付款方 → Earthjustice → 案件”的资金边。

## 新增的人物与组织接口

2003 年 CBD 官方起诉公告可以提取 Peter Galvin、Martin Wagner、土田 Takenobu、籠橋 Takaaki、東恩納 Takuma 五个案件公开角色。2021 年 VFP 官方活动页又明确写出：吉川秀樹同时担任 SDCC 国际事务负责人和 OEJP 负责人；Pete Doktor 是 VFP-ROCK 的共同创办人；Doug Lummis 是协调人。

这类人物记录比“组织共同署名”更接近甲方要求的社会网络分析，因为它能解释谁把美国法律组织、冲绳环保组织和退伍军人网络接在一起。现阶段它们仍是待人审人物—职务—时间观察，不直接进中央关系图。

## 对下一轮 database 的直接要求

1. 反基地侧要从 actor—issue 图升级为 `person → organization → role → time → source` 与 `organization → case/event → role → time → source`。
2. 资金层必须把 court award、grant、donation、sponsorship、contract、project cost 分表或至少分语义，不能再共用一个“支持关系”。
3. 美国来源 actor 需要一项 `Okinawa-specific continuity` 测量：一次署名、持续项目、本地章节、案件角色必须分开。
4. 对 Friends of the Earth U.S.、Pacific Environment 的当前定位应降为“事件参与可证，持续冲绳项目待证”，而不是仅凭国际知名度赋予中心性。
5. VFP-ROCK 值得成为第一个社会网络 tracer case：官方材料同时提供人物、章节、活动、跨组织协调和全国组织接口。

## 交负责人判断

`human_review_queue_v1.csv` 有 9 项。优先判断四项：Earthjustice 金额语义；A070 身份与连续性；A070→A019 协调边；吉川秀樹 A001/A002 双重职务。只有这四项通过，才值得把问责侧第一张“人物—组织—案件”图接入 database 与前端。
