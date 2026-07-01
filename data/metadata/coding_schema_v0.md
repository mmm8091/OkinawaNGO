# Phase 1 编码字段与复核规则 v0

日期：2026-06-17

## 1. 基本原则

本期数据只记录公开可复核信息。AI 可以初搜、摘录和结构化，但不能作为最终复核者。所有进入分析结论的 actor、edge、funding/support relation 都必须有人审。

人工参与度最低 30%。计算方式：

`human_review_minutes / (ai_work_minutes + human_review_minutes)`

## 2. actor_registry 字段

| 字段 | 说明 |
|---|---|
| actor_id | 稳定编号，例如 A001、X001 |
| canonical_name | 规范名称 |
| actor_class | local_civic_actor / international_advocacy_actor / base_community_service_actor 等 |
| origin_type | okinawa_local / japan_domestic / us_origin / international / public_institution / corporate |
| legal_status_guess | NPO 法人、公益法人、任意団体、project、unclear 等 |
| primary_places | 主要地点，多个用分号 |
| issue_tags | 议题标签，多个用分号 |
| source_refs | source_id、seed_id 或 URL |
| evidence_level | E0-E4 |
| review_status | ai_seeded / human_checked / human_revised / needs_second_source / needs_local_retrieval / rejected |
| needs_local_retrieval | yes / no |
| notes | 复核说明 |

## 3. actor_class 建议值

- local_civic_actor
- local_npo
- citizen_group
- citizen_network
- executive_committee
- lawyers_network
- domestic_japan_ngo
- international_advocacy_actor
- international_ngo
- base_community_service_actor
- base_spouse_club
- base_spouse_charity_network
- public_diplomacy_or_exchange_actor
- public_diplomacy_grant_program
- local_international_cooperation_ngo
- public_institution_partner
- corporate_sponsor
- local_business_sponsor
- funder_or_intermediary

## 4. origin_type 建议值

- okinawa_local
- japan_domestic
- us_origin
- international
- mixed_or_network
- public_institution
- corporate
- unclear

## 5. issue_tags 初版

- anti_base
- anti_military
- Henoko
- dugong
- environment
- biodiversity
- groundwater
- life_safety
- health_risk
- local_autonomy
- referendum
- legal
- human_rights
- peace
- anti_war
- international_advocacy
- public_diplomacy
- international_cooperation
- military_family_service
- base_community_welfare
- frontline_prevention
- Taiwan_contingency
- administrative_collaboration

## 6. evidence_level

| 等级 | 名称 | 判定 |
|---|---|---|
| E4 | 证据确凿 | 官方 grant / award / contract、组织财报、政府名单、组织官网、正式项目报告明确支持 |
| E3 | 基本确认 | 官方或组织页面确认合作 / 赞助 / 委托 / 项目关系，但缺金额、年份或完整链条 |
| E2 | 可信线索 / 疑似 | 地方新闻、DVIDS / Stripes、活动页、二手资料、公开社媒，有具体名称但缺正式记录 |
| E1 | 未确认说法 | 单一政治性指控、论坛、博客、无法复核截图、转述 |
| E0 | 排除 | 查证后不相关、误配、同名误认、资料矛盾无法解决 |

## 7. funding_relation_confidence

- confirmed_grant
- confirmed_sponsorship
- confirmed_commission
- confirmed_service_role
- probable_funding
- suspected_lead
- no_public_evidence
- not_funding_relation

## 8. edge 表通用字段

| 字段 | 说明 |
|---|---|
| edge_id | 稳定编号 |
| source_actor_id | 起点 actor |
| target_actor_id | 终点 actor |
| relation_type | sponsorship / donation / service / partnership / grant_opportunity / consultant / member_of / site_presence 等 |
| event_or_program | 具体项目、活动或事件 |
| place | 地点 |
| evidence_level | E0-E4 |
| funding_relation_confidence | 资助关系置信度 |
| source_ref | source_id、seed_id 或 URL |
| review_status | 复核状态 |
| needs_local_retrieval | 是否需要当地补查 |
| notes | 解释边界 |

## 9. 解释规则

- `E4` 可以写入结论。
- `E3` 可以写入结论，但用“基本确认”“公开资料显示”等保守措辞。
- `E2` 只能写入线索或待查清单。
- `E1` 不进入正文结论。
- `grant opportunity` 只证明有项目机会，不证明有 recipient 或实际拨款。
- sponsor page 可以证明赞助关系存在，但不一定证明金额和年份。
- 服务型 NGO 只按服务 / 福利 / 慈善 / 公共外交功能编码，不自动赋予政治立场。

## 10. 当地补查标记

`needs_local_retrieval=yes` 的典型情况：

- NPO 财报、事業報告書、年度报告线上不可得。
- 组织旧称、解散、合并、分裂需要地方资料确认。
- 军属俱乐部捐赠去向只在活动手册、基地报纸或本地记录中出现。
- 报刊数据库、馆内数据库或纸质档案才可能确认。
- 公开资料只说明 grant opportunity，缺 award / recipient。
