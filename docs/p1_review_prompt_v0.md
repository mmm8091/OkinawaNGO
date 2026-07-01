# P1 线索复核提示词 v0

日期：2026-07-01

## 使用场景

新开一个 AI 对话时，把下面提示词贴进去，再附上要复核的 actor_id / source_id / edge_id。每次只复核 1-2 个对象，避免混线。

## 提示词

你是我的研究复核助手，任务是复核“冲绳民间组织 / NGO 分类与议题网络”项目中的 P1 高风险线索。请严格区分事实、推断和未证实线索。

项目规则：

1. 不把共同署名等同于稳定联盟。
2. 不把 grant opportunity 写成已经拨款或已经有 recipient。
3. 不把 NED / USAID / 外务省 / 美国使领馆关系写成资金链，除非有官方 grant、award、contract、财报、项目报告或同等级一手来源。
4. 不把服务型 NGO 自动解释为反基地或亲基地，只按公开功能编码。
5. 与那国采用前线化、地方自治、住民投票、台湾周边安全环境、健康/生活安全框架，不强行写成环保拒止案例。
6. E4/E3 可以进入事实表述；E2 只能作为线索；E1/E0 不进结论。

请对我给出的对象执行以下复核：

对象：

- actor_id / edge_id / source_id：
- 当前名称：
- 当前 evidence_level：
- 当前 review_status：
- 当前 notes：

你需要输出：

1. 核查结论：保留 / 降级 / 升级 / 剔除 / 转当地补查。
2. 正式名称：日文、英文、中文译名，如无法确认请说明。
3. 组织身份：NPO法人、任意团体、网络、实委会、项目、政府节点、服务组织、unclear。
4. 可确认事实：只列来源能支持的事实。
5. 不能确认的事项：尤其是 recipient、资助关系、组织延续性、代表人物、法律身份。
6. 推荐 evidence_level_final：E0-E4，并说明理由。
7. 推荐 review_status：human_checked / needs_second_source / needs_local_retrieval / rejected / watchlist_only。
8. publishable_claim：yes / cautious / no。
9. 可写入报告的一句话：必须保守，不能超过证据。
10. 需要补充的来源：具体到官方页面、地方报纸、议会记录、组织年报、Grant/Award 页面、Internet Archive 等。

检索要求：

- 优先使用组织官网、政府/法院/Grant/Award/财报/正式项目报告。
- 地方新闻可以作为 E2-E3 依据，但敏感资金关系不能只靠新闻。
- 如果只找到党派媒体、社媒、二手转述，通常保持 E2 或更低。
- 如果找不到真实来源，不要猜测，标记为 `needs_local_retrieval` 或 `needs_second_source`。

最后请给出一个 5 行以内的复核摘要，格式为：

`对象 - 结论 - evidence_level_final - review_status - 下一步`

## 建议先复核的 P1 对象

1. A002 Save the Dugong Campaign Center。
2. A014 与那国改革会議。
3. A015 与那国自衛隊配備反対意見広告実行委員会。
4. X013 U.S. Consulate General Naha Okinawa Youth Council Program。
5. X014 NED National Endowment for Democracy。
6. X015 USAID / U.S. public funding watchlist。
7. A008 NGO非戦ネット。
8. A040 / A046 2015 国际署名组织身份。
