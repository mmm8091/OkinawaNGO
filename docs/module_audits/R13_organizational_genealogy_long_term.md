# R13 组织谱系与长期演变

## 结论

这个模块价值很高，但不能作为一期的完整承诺。1972 年以来的组织谱系需要档案、旧报纸、组织内部资料、运动史文献和访谈，仅靠公开网页无法做全。当前可行方案是做“谱系线索与历史锚点”，把早期反战地主、1995 后县民大会、1997 名护住民投票、1998 ヘリ基地反対協议会、2004 海上阻止行动、2010s All Okinawa / 県民投票、2020s 先岛反军事化等串成可继续扩展的时间骨架。

## 已主动探查的资料

1. ヘリ基地反対協議会官网：明确说明其正式名称、1997 年名护市民投票相关组织、1998 年结成、现在 12 个加盟团体。这是可以直接用于组织谱系的高质量来源。
   - https://lovehenoko.org/わたしたちの立場/

2. ヘリ基地反対協議会“闘いの主な経緯”：列出 1996 SACO、1997 名护市民投票、2004 边野古 boring 调查阻止行动、2006 沿岸案撤回县民大会等关键节点，可作为边野古运动谱系时间轴。
   - https://lovehenoko.org/闘いの主な経緯/

3. 一坪反战地主相关资料：Kotobank 与琉球新报词条均显示，一坪反战地主会与 1980s 以后反战地主、军用地拒绝出租、草根反战反基地运动重组有关，是复归后长期谱系的重要前史。
   - https://kotobank.jp/word/一坪反戦地主会-154581
   - https://ryukyushimpo.jp/okinawa-dic/prentry-42754.html

4. 冲绳县公文书馆 USCAR 文书说明：虽然 USCAR 到 1972 年为止，但它能提供复归前后治理、治安、大众运动、基地劳动等前史材料。它适合做长期谱系的背景入口，但不能直接替代组织名单。
   - https://www.archives.pref.okinawa.jp/uscar_document/5397

5. 冲绳县立图书馆、地方报刊数据库和公文书馆检索系统：适合追踪 1990s 以后组织名称变化、县民大会、住民投票、市民連絡会、実行委員会等，但很多数据库可能需要馆内使用或付费权限。

## 能抽取的数据关系

- predecessor_successor：某组织是否由前一组织发展、改组、解散后再组织。
- historical_anchor：某组织与某个历史事件的关系，例如 1997 名护市民投票、2004 边野古海上行动、2019 县民投票。
- issue_continuity：同一组织或同一网络是否从“基地负担”转向“环境 / 生活安全 / 地方自治 / 国际倡议”。
- place_continuity：组织是否围绕同一地点长期活动，例如边野古、普天间、嘉手纳、石垣、宫古、与那国。
- actor_generation：老一代反战地主 / 现场抗议组织、2010s 公投组织、2020s 先岛反军事化组织之间的代际关系。

## 推荐字段

- lineage_id
- actor_id
- actor_name
- period_start
- period_end
- predecessor_actor
- successor_actor
- relation_type: formed_from / renamed_from / split_from / coalition_successor / issue_successor / unknown
- key_event
- issue_continuity
- place_continuity
- person_overlap_public
- source_id
- confidence
- evidence_note

## 可交付物

- `organization_lineage_clues.csv`
- `historical_anchor_timeline.csv`
- “边野古组织谱系小图”：1997 名护住民投票 -> 1998 ヘリ基地反対協 -> 2004 海上行动 -> 2019 县民投票 / 后续行动
- “长期演变风险说明”：哪些节点有证据，哪些只是线索，哪些需要档案或访谈

## 难点

最大难点是早期组织资料不在线，且很多团体不是 NPO 法人，而是会、协议会、实委会、原告团、地主会、临时共同斗争组织。名称还可能随事件变化，不能简单按名字去重。

第二个难点是谱系关系通常不是法律继承，而是议题、人物、地点、行动方式上的延续。比如“由 A 发展为 B”和“B 继承了 A 的运动议题”是两种不同关系，必须分开编码。

## 判断

一期可以做“长期演变的骨架”，但不能承诺完整 1972 年以来全量组织谱系。它适合作为大项目的长期主线，当前阶段只需要为后续档案研究和访谈研究留下可扩展的数据结构。
