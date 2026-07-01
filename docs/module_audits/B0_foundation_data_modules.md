# B0 基础建设模块：actor registry / source log / taxonomy / evidence notes

## 结论

可做，而且必须做。这个模块不是研究问题本身，而是所有后续模块的底座。若没有统一的 actor registry、source log、issue taxonomy、place registry 和 evidence notes，后续网络图会很快变成不可复核的“漂亮图”。

一期建议先建 30-50 个 seed actor 做试跑，再扩到 150-200 个。这里的 actor 不能等同于 NPO 法人，而应包括 NPO 法人、任意团体、市民連絡会、住民の会、実行委員会、弁護団、原告団、共同声明网络、项目型组织和国际 NGO。

## 已主动探查的资料

1. 内阁府 NPO 法人ポータルサイト：适合确认 NPO 法人格、所在地、活动领域等，但不能覆盖非正式市民团体。
   - https://www.npo-homepage.go.jp/npoportal/

2. 冲绳县 NPO Plaza / NPO 页面：适合做冲绳县法人层、制度层和行政协作层资料入口。
   - https://www.pref.okinawa.jp/kurashikankyo/katsudo/1004889/1004890.html

3. 冲绳县 NPO 等协作实绩调查：适合 R8 行政协作模块，但不适合作为反基地 / 环保运动主体的唯一来源。
   - https://www.pref.okinawa.lg.jp/_res/projects/default_project/_page_/001/004/917/2r6hp.pdf

4. 共同声明、请求书、诉讼、新闻报道：适合纳入非法人、市民团体、实委会、连络会、律师团和原告团。

5. 冲绳县公文书馆、县立图书馆、地方报刊数据库说明：适合后续补历史资料和媒体资料，但一期不应依赖它们完成全量谱系。

## 推荐数据表

- `actor_registry.csv`
- `actor_alias.csv`
- `issue_taxonomy.csv`
- `place_registry.csv`
- `source_log.csv`
- `evidence_notes.csv`
- `actor_issue_edges.csv`
- `actor_place_edges.csv`
- `event_actor_edges.csv`

## 推荐字段

- actor_id
- canonical_name_jp
- aliases
- name_en
- name_zh
- actor_type
- legal_status
- primary_places
- issue_tags
- action_tags
- period_active
- source_ids
- evidence_quote_or_summary
- confidence
- review_status
- notes

## 难点

最大难点是 actor 定义。NPO 法人只是法律身份，不能等同于研究对象。关键政治行动主体常常是任意团体、共同声明网络、实委会、支援会、律师团、原告团、地方住民组织或临时组织。

第二个难点是异名。日本资料中同一组织可能使用正式名、简称、英文名、旧名、活动名。必须建立 alias 表，否则网络图会把同一组织拆成多个节点。

## 判断

B0 是一期必做。项目能不能长期推进，主要取决于这个底座是否干净。建议先不要全量抓 NPO 法人名册，而是采用“议题入口 + 法人入口”的双入口采样。
