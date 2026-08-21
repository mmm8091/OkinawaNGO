# 对美问责侧第一轮补强：从“参与过”到“谁在组织、谁在办案、资源如何进入”

日期：2026-08-19

状态：`research_only / 9 principal decisions complete / no central writeback`

## 本轮回答了什么

当前 database 的六个美国来源问责 actor，并不是同一种参与。

- Earthjustice、Center for Biological Diversity、Turtle Island Restoration Network 进入的是同一个可编号诉讼：两家是原告，一家是律师。案件角色已有 R8 人审支持。
- Veterans For Peace Ryukyu/Okinawa Chapter 是本地化的美国退伍军人反军事化节点。新找到的 VFP 官方目录、活动页和会报，已经能给出章节编号、负责人、公开活动和具名协调对象。
- Friends of the Earth U.S. 现有2015、2019两个离散冲绳事件；Pacific Environment 的冲绳材料仍主要停在2015。两者都未达到持续项目门槛。

这使原来的“六个参与反基地行动的美国 NGO”可以拆成三种位置：案件型问责、在地化退伍军人行动、国际声明外围。以后画网络时不能把三类都画成同强度的组织节点。

## 新增的资源事实

Earthjustice 的官方 FY2021 Form 990 在“十大法院判给律师费及成本”中列出 `Okinawa Dugong`，金额 USD 276,345.50；财政部另有 USD 280,000 Judgment Fund 付款记录。两数是不同来源和语义的案件资源观察。

两数相差 USD 3,654.50，现有材料不能解释差额或证明全额直付 Earthjustice。下一步应从案件 docket 和 fee order 追出付款依据；在此之前不合并金额，也不形成 OSD→Earthjustice 简单资金边。

## 新增的人物与组织接口

2003 年 CBD 官方起诉公告可以提取 Peter Galvin、Martin Wagner、土田 Takenobu、籠橋 Takaaki、東恩納 Takuma 五个案件公开角色。2021 年 VFP 官方活动页又明确写出：吉川秀樹同时担任 SDCC 国际事务负责人和 OEJP 负责人；Pete Doktor 是 VFP-ROCK 的共同创办人；Doug Lummis 是协调人。

这类人物记录比“组织共同署名”更接近甲方要求的社会网络分析。人物同一性与点时职务决定已完成，但仍未受控写入中央关系图；共享人物不生成组织联盟边。

## 对下一轮 database 的直接要求

1. 反基地侧要从 actor—issue 图升级为 `person → organization → role → time → source` 与 `organization → case/event → role → time → source`。
2. 资金层必须把 court award、grant、donation、sponsorship、contract、project cost 分表或至少分语义，不能再共用一个“支持关系”。
3. 美国来源 actor 需要一项 `Okinawa-specific continuity` 测量：一次署名、持续项目、本地章节、案件角色必须分开。
4. Friends of the Earth U.S. 只增加2019第二个离散事件，Pacific Environment 仍主要为2015冲绳事件；均不得凭国际知名度赋予持续性或中心性。
5. VFP-ROCK 值得成为第一个社会网络 tracer case：官方材料同时提供人物、章节、活动、跨组织协调和全国组织接口。

## 负责人决定结果

`human_review_queue_v1.csv` 的9项均已决定（`accept 2 / revise 7`）。Earthjustice 两笔金额保持分离；A070按离散日期观察；USAA005 撤回 A019，改为 event-only 十区会或 raw label；吉川秀樹的 A001/A002 点时 person bridge 已确认。正式结果见 `docs/human_review_return_USN_accountability_v1.md`；中央 database 与前端仍未写入。
