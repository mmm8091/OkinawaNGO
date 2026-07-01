# R9 选举 / 县民投票与市民组织连接

## 结论

能做，但要谨慎。可以研究组织如何参与县民投票、住民投票、公开声明和地方自治动员；不宜在一期承诺“组织动员导致选票变化”的因果分析。

这个模块可以作为前一个知事选研究和当前 NGO 项目的桥梁，但它的重点应从选票模型转为“市民组织如何把基地争议制度化为投票、直接请求、公开立场和地方自治议题”。

## 已主动探查的资料

1. 2019 年边野古县民投票及相关运动：可追踪“辺野古”県民投票の会、署名、投票执行争议、县民投票结果和后续声明。

2. 石垣自卫队配备住民投票运动：可追踪“石垣市住民投票を求める会”、署名、条例 / 诉讼、地方自治与基地争议。

3. 与那国 2015 年自卫队配备住民投票：可追踪自卫队配备争议、住民投票、反对派团体和健康 / 电磁波 / 前线化担忧。

4. 前一阶段已有 2014 / 2018 / 2022 市町村层面反边野古候选人得票数据，可作为背景连接，但不应直接用来推断组织动员因果。

## 能抽取的数据关系

- actor -> referendum_event
- actor -> signature_campaign
- actor -> public_position
- actor -> election_related_statement
- actor -> local_autonomy_claim
- actor -> voting_result_context

## 推荐字段

- election_or_referendum_id
- event_type
- event_date
- place
- actor_id
- actor_name
- action_type
- public_position
- issue_tags
- result_summary
- source_id
- evidence_note
- confidence

## 可交付物

- `referendum_actor_events.csv`
- `election_statement_events.csv`
- 组织参与投票 / 公投事件表
- 住民投票运动小档案
- 组织公开立场与投票结果背景图

## 难点

投票结果与组织动员之间存在因果识别问题。组织活跃的地方可能本来就更反基地，不能简单说组织导致投票结果。

另一个难点是选举支持关系可能较敏感。除非有公开声明或组织官网材料，否则不要推断某组织支持某候选人。

## 判断

一期可做“组织—投票事件连接”，不要做因果模型。该模块适合作为背景桥梁：展示 NGO / 市民组织如何把基地问题推进到县民投票、住民投票和地方自治程序中。
