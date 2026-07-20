# H2 service universe v1 validation

日期：2026-07-20

## 结构检查

- 10 张 CSV 均可由标准 CSV parser 读取；
- 行数分别为 82、12、6、55、10、9、9、18、6、11；
- 各表 ID 字段在表内无重复；
- 所有带 `package_scope` 的行均为 `research_only`；
- 所有带 `frontend_eligibility` 的行均为 `excluded_research_only`；
- 人物与官方目录候选未获得中央 actor ID；
- 未生成组织—组织关系边、人物节点、funding edge 或政治立场字段。

## 在线来源复核

- MCIPAC/MCCS 页面说明 PO 是经书面许可活动的 self-sustaining non-federal entities，
  不隶属 MCCS；页面同时覆盖 Okinawa、Camp Fuji 与 MCAS Iwakuni。
- 页面可见表在 2026-07-07 更新，当前抽取为 82 行：81 active、1 inactive；页面正文的
  “more than 90” 与显示表计数分别保留。
- Marine Thrift Shop 自有页面明确记载独立董事会、grant 申请、AWWA member/contributor
  表述及具名 recipient 示例；均保持候选关系语义。
- AWWA 成员结构存在五个配偶组织与七个 member organizations 两种公开口径；本包保留冲突，
  不冻结成员总数，也不自动把商店／子实体 actor 化。
- 人物角色来自组织官网、政府／军方公开报道或 IRS filing 的公开接口；年度与事件日期没有
  被改写为完整任期。

## 解释门禁

本包通过的是数据结构和检索覆盖检查，不是事实／关系／身份人工复核。四个新增 actor
建议、两项 defer、10 组人物 crosswalk、6 条福利接口及 11 条机制种子均需负责人决定后，
才能进入任何中央或报告确定性层。
