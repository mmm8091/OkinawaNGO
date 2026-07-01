# 人工复核任务书 v0

日期：2026-06-17

## 1. 目的

本文件用于指挥人工复核。人工复核的目标不是“帮 AI 润色”，而是判断每条 actor、source、edge 是否能进入一期数据底座，是否需要降级、补证或剔除。

原则：

- AI 只负责初筛和结构化，不能做最终审定。
- 敏感关系必须由人审，尤其是资助、委托、公共外交、军属服务、NED / USAID / 外务省 / 美国使领馆相关线索。
- 不确定就降级为 `needs_second_source` 或 `needs_local_retrieval`。

## 0. 当前状态（2026-07-01）

HR-001 至 HR-009 已完成首轮人工复核。详细合并包见：

- `docs/human_review_merge_package_v0.md`
- `data/interim/human_review_log_v0.csv`

首轮结论摘要：

| 任务 | 状态 | 合并结论 |
|---|---|---|
| HR-001 | closed first-pass | A002 保留并确认为 SDCC / 任意団体 / IUCN 国家级 NGO 会员；新增 A076 Save the Dugong Foundation；不得把 A002 写成美国诉讼法律原告。 |
| HR-002 | closed first-pass | A008 保留为全国性国际协力 / 和平 NGO 网络；只写 2019 辺野古县民投票连带声明，不写成本地核心 actor。 |
| HR-003 | closed first-pass | A014 替换为 `住民投票を成功させるための実行委員会` E2；A015 保留为八重山 / 石垣侧声援线索 E2；A016 保留 E3。 |
| HR-004 | closed first-pass | A019 保留 E4，是辺野古现场核心 actor；legal_status 为任意団体；F013 降为 E2。 |
| HR-005 | closed first-pass | AWWA 名称修正为 American Welfare & Works Association；补全 X005/X006/X007/X016/X017 五成员网络。 |
| HR-006 | closed first-pass | X007 OESC 身份、EIN、2025 年 OESC -> USO Okinawa 捐赠可作为 E4 事实。 |
| HR-007 | closed first-pass | X013 只确认 NOFO / grant opportunity 存在；不得写 recipient 或已拨款。 |
| HR-008 | closed first-pass | X014 NED 与 X015 Peace Winds Japan 保持 watchlist_only；不得写 NED/USAID 资助冲绳 NGO。 |
| HR-009 | closed first-pass | A040 / A046 身份确认；A032-A046 只作为 2015 共同署名 / 国际声援节点，不写成稳定联盟。 |

首轮后仍需补的事项不属于 HR 未完成，而是后续补源 / 当地材料收集：

- A014/A015 仍需地方报纸、意见广告实物或议会资料交叉确认。
- A016 仍需成立年月、代表人、法律身份。
- A019 / A076 的 2003 年 dugong 诉讼 plaintiff 映射仍待核实。
- AWWA 网络仍需 charity recipient / Schedule I / 活动手册补证。
- X013 长期观察 Grants.gov / USASpending / 领馆公告是否出现 award 或 recipient。
- X014 NED 跨年度排除需要另查，本轮只覆盖 FY2024 亚洲清单。

## 2. 复核输入材料

主要输入：

- `data/interim/01_actor_registry_initial_v0.csv`
- `data/interim/05_source_log_initial_v0.csv`
- `data/interim/15_funding_or_support_edges_sample_v0.csv`
- `data/metadata/coding_schema_v0.md`

必要时参考：

- `data/actor_registry_seed_v0.csv`
- `data/external_ngo_funding_seed_v0.csv`
- `docs/phase1_external_ngo_funding_adjustment_v0.md`
- 当前方案 md：`source_docs/current/复归后冲绳民间组织 _ NGO 分类与议题网络一期研究方案.md`

## 3. 复核交付物

每轮人工复核后至少交付：

1. 已复核表格：在原表基础上补 `human_reviewer`、`review_date`、`review_note`，或另交 review log。
2. 问题清单：哪些 actor / edge 需要二次来源，哪些需要当地补查，哪些应剔除。
3. 口径修改建议：是否需要新增 actor_class、issue_tags、evidence_level 判定说明。
4. 可进入沟通稿的结论：只写 E3/E4，E2 只能写“线索”。

## 4. 复核判定字段

建议人工复核时补充以下字段：

| 字段 | 说明 |
|---|---|
| human_reviewer | 复核人 |
| review_date | 复核日期 |
| review_status | human_checked / human_revised / needs_second_source / needs_local_retrieval / rejected |
| review_note | 简短说明 |
| evidence_level_final | 人工确认后的 E0-E4 |
| publishable_claim | yes / cautious / no |

## 5. 证据等级复核口径

| 等级 | 可写法 | 人工判断重点 |
|---|---|---|
| E4 | “证据显示”“公开记录确认” | 是否有官方/组织/财报/award/contract/正式报告 |
| E3 | “公开资料显示”“基本确认” | 是否确认关系存在，但金额、年份或链条不全 |
| E2 | “存在相关线索”“仍需核查” | 是否只有新闻、活动页、社媒、二手资料 |
| E1 | 不进结论 | 是否无法复核或政治性指控为主 |
| E0 | 剔除 | 是否误配、同名误认、与冲绳无关 |

## 6. 第一批人工复核任务（原始任务定义，首轮已完成）

### HR-001 Save the Dugong Campaign Center

对象：A002

要查：

- 日文正式名是否为 `ジュゴン保護キャンペーンセンター` 或其他写法。
- 是否有独立官网、组织说明、法律身份或代表信息。
- 与 Earthjustice / OEJP / Henoko dugong litigation 的关系是否只是共同倡议，还是更稳定组织关系。

材料：

- `S007` APJJF 文章
- `S009` Earthjustice 页面
- `S004` NACSJ 2015 声明

交付物：

- 确认 canonical_name。
- 给出 legal_status_guess。
- 给出 evidence_level_final。
- 若找不到正式资料，标 `needs_second_source`。

### HR-002 NGO非戦ネット

对象：A008

要查：

- 组织结构：网络、任意团体、实委会还是项目名。
- 成员名单或参与声明。
- 是否与冲绳议题有直接关系，还是全国和平网络支援。

材料：

- `S005` Peace Boat 页面
- 组织官网 / Web Archive / 声明页

交付物：

- actor_class 判定。
- issue_tags 修正。
- 是否进入核心 actor 或只作为背景 actor。

### HR-003 与那国早期反部署组织

对象：A014、A015、A016

要查：

- `与那国改革会議`
- `与那国自衛隊配備反対意見広告実行委員会`
- `与那国島の明るい未来を願うイソバの会`

重点：

- 是否有地方新闻、议会记录、活动传单、住民投票资料支持。
- 不能只依赖党派媒体。
- 如果只有赤旗或单一报道，维持 E2。

材料：

- `S010` QAB 住民投票报道
- `S011` 琉球新报报道
- `S015` 赤旗报道

交付物：

- 每个组织是否保留。
- 是否需要当地补查。
- 与那国专题中可写到什么程度。

### HR-004 ヘリ基地反対協議会

对象：A019

要查：

- 直接官网或组织声明。
- 成立时间、活动地点、是否为边野古现场核心组织。
- 与边野古现场行动、共同声明、县民投票或国际倡议是否有公开关系。

材料：

- `S008`
- 组织官网 / Web Archive
- 地方新闻

交付物：

- 组织时间线简表。
- 可作为核心 actor 的依据。
- 缺口说明。

### HR-005 AWWA 正式名称与网络

对象：X004、X005、X006、X007

要查：

- AWWA 的正式名称到底是 American Women's Welfare Association 还是 American Welfare & Works Association，或是否历史上有改名。
- AWWA 与 NOSCO / KOSC / OESC 的成员或协调关系。
- 是否有 charity recipients / grant recipients。

材料：

- `X004` DVIDS
- NOSCO / KOSC / OESC 官网
- base newspaper / event booklet

交付物：

- actor alias 表建议。
- AWWA network edge 是否保留。
- 哪些内容需要当地补查。

### HR-006 OESC 线索复核

对象：X007

要查：

- OESC 是否有独立官网或公开社媒。
- Stripes 报道中的 501(c)(3)、USO donation、local/military community support 是否可由组织资料确认。

材料：

- Okinawa Stripes 报道
- OESC 官网 / 社媒 / 活动材料

交付物：

- evidence_level_final。
- 是否从 E2 升为 E3/E4。
- 不能确认时保持 `needs_second_source`。

### HR-007 美国领馆 Okinawa Youth Council

对象：X013、F012

要查：

- Grants.gov 或美国使领馆页面是否有 award notice。
- 实际 recipient organization 是谁。
- 执行机构是否为冲绳本地组织、学校、外部承包机构或美国机构。

材料：

- Grants.gov 页面
- U.S. Embassy / Consulate NOFO PDF
- 领馆活动新闻 / 社媒 / local news

交付物：

- recipient 是否确认。
- 若只是 grant opportunity，必须保留 `no_public_evidence`。
- 不得写成“美国领馆资助了某冲绳 NGO”，除非找到 award / recipient。

### HR-008 NED / USAID watchlist

对象：X014、X015

要查：

- NED FY2024 Asia grant listing 中是否有日本 / 冲绳 / 琉球 / Okinawa 直接 recipient。
- Peace Winds Japan 是否与冲绳基地、先岛、灾害治理或安全网络有一期相关连接。
- USAID 资助是否只作为“方法样本”，而不是冲绳关系。

材料：

- NED grant listing
- USAspending
- Peace Winds Japan 项目页

交付物：

- 是否进入 actor registry 主表。
- 是否仅保留 watchlist。
- 可写入沟通稿的保守措辞。

### HR-009 2015 国际署名组织身份确认

对象：A040、A046，必要时包括 A032-A045

要查：

- Pro Public 是哪个国家 / 哪个组织，是否与 NACSJ 英文署名一致。
- Pro Natura / FoE Switzerland 的正式组织名称。
- 其他海外组织是否只作为 2015 署名 seed，而不进入核心网络解释。

材料：

- `S004` NACSJ 2015 声明
- 各组织官网

交付物：

- 正式英文名。
- origin_type。
- 是否需要 actor_alias。

## 7. 人工复核节奏

建议每轮 60-90 分钟，先处理 8-12 个高风险条目。

优先级：

1. E2 但可能进入结论的条目。
2. 资助 / 赞助 / 公共外交 / 军属服务关系。
3. 与那国 / 先岛专题核心组织。
4. 组织名、别名、法律身份不稳定的条目。

## 8. 不合格复核示例

以下不算合格人工复核：

- 只说“看起来重要”。
- 只把 AI 输出重读一遍。
- 没有打开来源。
- 没有说明为什么升/降 evidence_level。
- 把“出现于署名名单”写成“稳定联盟成员”。
- 把“grant opportunity”写成“已获资助”。
