# R2 组织—议题网络

## 结论

可做，价值高，一期核心模块。它能把“反基地如何转化为环保、生活安全、地方自治、国际倡议”可视化出来。

## 已探查资料

1. WWF Japan 2010 年 67 团体边野古 / 儒艮声明，可抽取 actor、issue、place、international_signature 等关系。
   - https://www.wwf.or.jp/activities/statement/3436.html

2. 日本自然保护协会 2015 年 31 NGO 边野古紧急声明，可抽取环保 NGO、和平 NGO、边野古 / 大浦湾议题连接。
   - https://www.nacsj.or.jp/statement/50827/

3. Peace Boat 2015 年页面可验证和平运动组织如何接入边野古环保声明。
   - https://peaceboat.org/3620.html

4. OEJP 2020 年 71 团体向美国 Marine Mammal Commission 提交请求书和 civil society report，可抽取地方组织、国内 NGO、国际机构之间的议题连接。
   - https://okinawaejp.blogspot.com/2020/07/

5. 石垣、宫古、与那国地方新闻中的市民团体与议题连接，可支持先岛专题。

## 可抽取关系

- actor -> issue
- actor -> place
- actor -> action_type
- actor -> target_institution
- actor -> event

## 核心议题标签初稿

- Henoko / Oura Bay
- dugong
- coral
- environmental impact assessment
- Futenma
- Kadena
- Yonaguni
- Ishigaki
- Miyako
- missile deployment
- referendum
- groundwater
- electromagnetic / health concern
- frontline risk
- UN / U.S. institution / international advocacy

## 推荐字段

- edge_id
- actor_id
- actor_name
- issue_id
- issue_label
- issue_category
- place_tags
- event_id
- action_type
- source_id
- evidence_note
- confidence
- review_status

## 可交付物

- `actor_issue_edges.csv`
- 组织—议题二部网络图
- 议题聚类图
- “跨议题桥梁组织”列表
- “议题转译说明”：反基地如何变成环保、生活安全、自治、国际倡议

## 难点

来源材料中的议题词不统一，需要标准化。例如“生活安全”“標的化”“避難”“健康被害”“騒音”“地下水”可能都属于生活安全/风险框架，但不能过度合并。

另一个难点是组织—议题关系有强弱。共同声明署名只说明该组织在该事件中公开连接某议题，不一定说明该组织长期主打该议题。建议区分 primary_issue、secondary_issue 和 event_issue。

## 判断

标准一期完全可以做。建议先以共同声明和重点新闻为样本，不做全量媒体抽取。
