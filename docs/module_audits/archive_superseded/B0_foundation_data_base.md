# B0 基础建设模块：actor registry / source log / taxonomy / evidence notes

## 核查结论

可做，且必须做。这个模块不是研究问题本身，而是所有后续模块的底座。若没有统一 actor registry、source log、issue taxonomy 和 evidence notes，后续网络图会很快变成不可复核的“漂亮图”。

## 已探查资料

- 内阁府 NPO 法人ポータルサイト：可用于确认 NPO 法人格、所在地、活动领域等。
- 冲绳县 NPO プラザ：可用于冲绳县 NPO 法人、NPO 行政协作和制度资料。
- 冲绳县公文书馆：可用于早期组织、行政文件和历史背景。
- 冲绳县立图书馆数据库说明：可确认 1997/1998 年以后地方报刊数据库的馆内可用性。
- 共同声明、请求书、新闻报道：可用于纳入非法人、市民団体、実行委員会、連絡会、弁護団、原告団等。

## 可抽取字段

- actor_id
- canonical_name_jp / aliases / name_en / name_zh
- actor_type
- legal_status
- primary_places
- issue_tags
- action_tags
- period_active
- source_ids
- evidence_quote
- confidence
- review_status

## 可交付物

- `actor_registry.csv`
- `actor_alias.csv`
- `issue_taxonomy.csv`
- `place_registry.csv`
- `source_log.csv`
- `evidence_notes.csv`
- `actor_issue_edges.csv`
- `actor_place_edges.csv`

## 难点

最大难点是“actor”定义。NPO 法人只是一个法律身份，不能等同于研究对象。关键政治行动主体常常是任意团体、共同声明网络、实委会、支援会、律师团、原告团。

## 判断

一期必须先建 30-50 个 seed actor，再扩到 150-200 个。不要先全量抓 NPO 法人名册，否则会引入大量与基地、环保、和平、地方自治无关的公共服务型 NPO。

