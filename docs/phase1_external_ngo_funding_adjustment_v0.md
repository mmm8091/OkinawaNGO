# 一期方案补充调整：外来 NGO、军属服务网络与资助关系 v0

日期：2026-06-17

## 1. 本轮新增约束

根据最新沟通，一期方案需要在原有“冲绳本土 NGO / 市民团体 / 反基地与环保网络”基础上，补入以下方向：

1. 外来或跨国 NGO：包括美国、日本本土、国际环保 / 法律 / 人权 / 公共外交 / 国际合作组织。
2. 与美军基地社区直接相关的服务型 NGO 或福利组织：例如 USO Okinawa、American Red Cross Okinawa、Navy-Marine Corps Relief Society Okinawa、军属配偶慈善组织等。
3. 资助与委托关系：包括美国政府体系、NED、USAID、美国驻日使领馆、外务省、JICA、地方政府、企业赞助、基金会、休眠预金等。
4. 证据分级：不能把“可能有资助”写成事实，要区分“证据确凿、基本确认、疑似线索、未确认”。
5. 人工参与度：AI 可以辅助资料发现、初筛和结构化，但所有敏感判断必须由熟悉项目的人审；不能做成“AI 写、AI 审”的闭环。

这会让项目从单纯的“反基地 NGO 网络”扩展为：

> 冲绳基地与安全议题相关的民间组织生态，包括反基地 / 环保 / 自治倡议网络、外来服务型 NGO、军属福利网络、公共外交项目、国际合作 NGO 和资助 / 委托关系。

## 2. 对研究对象边界的调整

原方案已经强调“不只做 NPO 法人”。现在还需要进一步明确：一期 actor registry 不只收录冲绳本土运动组织，也应收录与冲绳基地和安全议题发生实质连接的外来组织、服务组织、资助机构和项目型网络。

建议把 actor 分成六类：

| 类别 | 说明 | 一期处理 |
|---|---|---|
| local_civic_actor | 冲绳本地市民团体、住民の会、連絡会、実行委員会 | 核心 |
| domestic_japan_ngo | 日本本土 NGO、法律团体、环保团体、和平团体 | 核心或桥接 |
| international_advocacy_actor | Earthjustice、Center for Biological Diversity、国际环保 / 人权组织等 | 核心或样本核心 |
| base_community_service_actor | USO、American Red Cross、NMCRS、军属配偶慈善组织等 | 新增观察层 |
| public_diplomacy_or_exchange_actor | 美国使领馆项目、TOMODACHI、青年交流、奖学金、公共外交项目 | 新增观察层 |
| funder_or_intermediary | NED、USAID、外务省、JICA、企业赞助方、基金会等 | 作为 actor 或 edge source 节点 |

关键处理原则：

- 不把所有组织都解释成反基地或亲基地。
- 服务型 NGO 主要用于解释“基地社会如何被日常服务、福利、慈善、公共外交和资金网络支撑”。
- 资助机构不等于操控者。只有在官方资助记录、财报、项目报告或合同中可确认时，才写成资助关系。
- 若只有二手说法或政治性指控，只能作为线索，不进入结论。

## 3. 轻量探索后的可用线索

### 3.1 美军基地社区服务与福利网络

USO Okinawa 是一个很合适的新增样本。USO Okinawa 官网明确说明 USO 是 not-for-profit organization，且不是 DoD 的一部分；USO Okinawa 页面列出 Camp Kinser、Camp Hansen、Kadena、Camp Foster、Futenma、Camp Schwab 等地点。USO Pacific 文章称 Okinawa team 支持约 47,000 名 service members and families，拥有 6 个中心和 780 多名 volunteers。

可抽取关系：

- USO Okinawa -> service_members_and_families
- USO Okinawa -> bases / camps
- corporate_sponsor -> USO Okinawa
- local_business_donation -> USO Okinawa

初步证据：

- USO Okinawa sponsors page: https://okinawa.uso.org/sponsors
- USO Pacific volunteer spotlight: https://pacific.uso.org/stories/800
- Phoenix Park Hotel donation to USO Okinawa: https://okinawa.uso.org/stories/172

American Women's Welfare Association / American Welfare & Works Association 也应进入样本。DVIDS 资料称 AWWA 为 Okinawa 上军属配偶组织提供资源协调，包含五个 military spouse organizations，并支持 American and Okinawan charities。NOSCO 页面称 AWWA 由 Okinawa 上 U.S. Forces spouses clubs 代表组成。

可抽取关系：

- AWWA -> spouse_clubs
- spouse_club -> charity_donation
- AWWA / spouse_club -> Okinawan charity
- AWWA / spouse_club -> American charity

初步证据：

- DVIDS AWWA 40 years: https://www.dvidshub.net/news/87854/american-womens-welfare-association-celebrates-40-years
- NOSCO AWWA page: https://nosco.wildapricot.org/awwa

American Red Cross Okinawa 和 Navy-Marine Corps Relief Society Okinawa 也可以作为美军基地社区服务网络节点。它们不应被写成政治组织，但可以作为“基地日常治理 / 福利服务 / 军属支持”的 NGO 或准 NGO 节点。

初步证据：

- U.S. Naval Hospital Okinawa Red Cross volunteer page: https://okinawa.tricare.mil/About-Us/Employment-Opportunities/Volunteer-Red-Cross
- Military OneSource emergency assistance page, including NMCRS Okinawa: https://installations.militaryonesource.mil/military-installation/camp-s-d-butler-camp-foster-kinser-courtney-hansen-schwab-and-mcas-futenma/base-essentials/emergency-assistance

### 3.2 外务省 / JICA / 国际合作型 NGO

沖縄NGOセンター应从普通“冲绳 NPO”升级为重点样本。外务省令和7年度 NGO 相談員名单列出沖縄NGOセンター；JICA Okinawa 页面也将 ONC 与国际理解教育、多文化共生、国际协力连接起来。这类组织未必直接参与反基地运动，但能说明“冲绳本地 NGO 与外务省 / JICA / 国际合作体系之间的制度连接”。

可抽取关系：

- 沖縄NGOセンター -> 外务省 NGO 相談員
- 沖縄NGOセンター -> JICA Okinawa / international cooperation events
- 沖縄NGOセンター -> development education / multicultural coexistence

初步证据：

- 外务省 NGO 相談員リスト令和7年度: https://www.mofa.go.jp/mofaj/gaiko/oda/about/shimin/pagew_000001_00002.html
- JICA Okinawa ONC page: https://www.jica.go.jp/domestic/okinawa/activities/kaihatsu/festival/syutten/31.html
- MOFA International Cooperation and NGOs PDF: https://www.mofa.go.jp/files/000024755.pdf

### 3.3 美国公共外交、青年项目与资助项目

TOMODACHI Initiative 可作为“公共外交 / 青年交流 / 美日关系网络”样本。U.S.-Japan Council 页面说明 TOMODACHI 是 U.S.-Japan Council 与 U.S. Embassy Tokyo 的 public-private partnership，并得到日本政府支持。它和基地议题未必直接相关，但如果在冲绳地区有项目或参与者，应作为 public_diplomacy_or_exchange_actor 进入观察层。

初步证据：

- U.S.-Japan Council TOMODACHI page: https://www.usjapancouncil.org/tomodachi/
- TOMODACHI official page: https://usjapantomodachi.org/

美国驻日使领馆项目需要作为“资金 / 项目机会”观察。快速检索显示 U.S. Consulate General Naha 曾有 Okinawa Youth Council Program 和 U.S. Ambassador's Scholarship Program for Okinawa High School Students 等 grant / public diplomacy 项目。这个方向需要继续确认具体 recipient organization，不能只凭 grant opportunity 推断某个冲绳 NGO 已经拿钱。

初步证据：

- Grants.gov Okinawa Youth Council Program: https://grants.gov/search-results-detail/351830
- FY2024 U.S. Consulate General Naha NOFO PDF: https://jp.usembassy.gov/wp-content/uploads/sites/7/2024/05/nofo-2024-naha-pas-02-okinawa-youth-council-e.pdf

### 3.4 NED / USAID / 外国资助关系

NED、USAID 方向可以纳入，但必须更谨慎：

- NED 官网说明其每年向 100 多个国家的非政府团体提供 grant。FY2024 Asia public grant listing 中可以看到 Asia-Pacific regional 项目，也有涉及 Japanese and Korean legislators 的区域性项目，但快速探索中尚未确认与冲绳本地 NGO 的直接资助关系。
- USAID 方向可用 Peace Winds Japan 做方法样本。Peace Winds Japan 有公开 USAID 资助线索，但这不等于它与冲绳基地议题存在直接关系。若只证明“日本国际 NGO 获得 USAID 资助”，容易偏题；只有当该组织在冲绳、先岛、基地、灾害治理或安全网络中出现时，才进入主表。

初步证据：

- NED grant program: https://www.ned.org/apply-for-grant/en/
- NED FY2024 Asia grant listing: https://www.ned.org/wp-content/uploads/2025/04/Asia-Grant-Listing-FY24.pdf
- Peace Winds Japan USAID funding example: https://en.peace-winds.org/1790/
- USAspending Peace Winds Japan award example: https://www.usaspending.gov/award/ASST_NON_720BHA23GR00038_7200

## 4. 关系证据分级

建议在所有 actor 和 edge 表中新增 `evidence_level`、`relation_type`、`funding_evidence_type`、`review_status` 字段。

| 等级 | 名称 | 判定标准 | 能否进结论 |
|---|---|---|---|
| E4 | 证据确凿 | 官方 grant / award / contract、组织财报、审计报告、政府名单、组织官网明确金额或关系 | 可以 |
| E3 | 基本确认 | 官方或组织页面确认合作 / 赞助 / 委托 / 项目关系，但缺金额、年份或完整链条 | 可以，但措辞保守 |
| E2 | 可信线索 / 疑似 | 地方新闻、DVIDS / Stripes、活动页、二手资料、社媒公开帖，有具体名称但缺正式记录 | 只能作为线索 |
| E1 | 未确认说法 | 单一政治性指控、论坛、博客、无法复核截图、转述 | 不进结论，只进待查 |
| E0 | 排除 | 查证后发现不相关、误配、同名误认、资料矛盾无法解决 | 不采用 |

资助关系还要单独记录 `funding_relation_confidence`：

- confirmed_grant：有官方 grant / award / 财报。
- confirmed_sponsorship：官方 sponsor page 或公开捐赠记录。
- confirmed_commission：政府 / 机构委托或咨询名单。
- probable_funding：基本确认有资助或委托，但金额 / 年份 / 合同缺失。
- suspected_lead：疑似，需要当地资料或进一步查证。
- no_public_evidence：查不到公开证据，不能写成事实。

建议措辞：

- “证据显示 X 获得 Y 资助”只用于 E4。
- “基本确认 X 与 Y 存在项目 / 委托 / 赞助关系”用于 E3。
- “存在 X 与 Y 可能有关的线索，仍需核查”用于 E2。
- 不使用“背后资助”“资金链确定”等强判断，除非有公开财务文件或合同支撑。

## 5. 人工参与与反幻觉机制

用户提出“人工至少 30% 参与度”是必要的，建议直接写入 coding guide。

可操作规则：

1. AI 可负责初搜、摘录、表格初填、异名提示和图表草稿。
2. 每条 actor、edge、funding relation 必须有人审，不能 AI 自审。
3. 敏感关系，如 NED / USAID / 外务省 / 美国使领馆 / 企业赞助，至少需要二次人工复核。
4. 若 AI 用 1 小时生成初稿，人审 1 小时，则人工参与度记为 50%。计算方式为：`human_review_minutes / (ai_work_minutes + human_review_minutes)`。
5. 每个表新增 `human_reviewer`、`review_date`、`review_status`、`review_note`、`needs_local_check`。
6. 所有“好像很重要”的判断都要降级为待查，不进入发现部分。

建议 `review_status`：

- ai_seeded
- human_checked
- human_revised
- needs_second_source
- needs_local_retrieval
- rejected

## 6. 需要实地 / 当地协作者确认的方向

### 方向一：冲绳本地 NPO 的财报、事業報告書和行政资料

确定需要当地人或有权限的人协助。原因是部分 NPO 资料虽理论公开，但网上检索不稳定，旧年度材料、附属明细、纸质报告、地方行政协作记录可能需要到冲绳县 NPO 相关窗口、图书馆、资料室或组织本身确认。

要查的问题：

- 组织是否真实存在、是否解散、是否改名。
- 是否有外务省、JICA、县、市町村、基金会、休眠预金、企业赞助等收入。
- 事業報告書里如何描述项目目标、对象、合作方和经费来源。
- 与反基地、国际合作、多文化共生、公共外交、军属服务是否有实际交叉。

### 方向二：美军基地社区服务组织和军属慈善网络

确定需要当地资料。USO、AWWA、KOSC、NOSCO、OESC、American Red Cross、NMCRS 等在线资料能确认存在和部分活动，但要搞清楚“谁给谁钱、钱用于谁、是否服务本地冲绳机构、是否只服务美军军属”，需要查更多地方材料。

要查的问题：

- 军属配偶俱乐部的年度 charity recipients / grant recipients。
- thrift shop、bazaar、gala、sponsorship 的公开账目或活动手册。
- 接收捐助的冲绳本地福利机构名单。
- USO Okinawa 的本地 sponsor 变动、金额、in-kind support。
- 这些组织与地方政府、学校、福利机构、基地管理部门之间的实际合作。

### 方向三：美国领馆 / 公共外交 / 青年交流项目的 recipient 与执行链条

确定需要进一步查。Grant opportunity 只能说明有项目机会，不能说明哪个组织实际拿到钱或执行项目。需要查 award notice、活动报告、参与者招募页、承办机构、地方新闻和领馆社媒归档。

要查的问题：

- Okinawa Youth Council Program、U.S. Ambassador's Scholarship 等项目的实际 recipient organization。
- 项目目标是否涉及 U.S.-Japan Alliance、基地理解、Indo-Pacific security、青年领导力。
- 执行方是否为冲绳本地 NPO、学校、国际交流组织、外部承包机构。
- 是否与 TOMODACHI、JICA、ONC、美国领馆、地方教育机构形成重复网络。

## 7. 对第1周和第2周安排的调整

原规划：

- 第1周：收束论文问题，确定资料边界、样本口径和编码规则。
- 第2周：收集 NPO / NGO / 市民团体资料，建立组织样本初版。

建议调整后：

### 第1周增加内容

1. 明确 actor universe 不只包括本土市民团体，也包括外来服务型 NGO、军属福利组织、公共外交项目、资助机构和国际合作 NGO。
2. 确定证据分级和资助关系字段。
3. 建立人工复核规则，明确最低 30% 人工参与度。
4. 新增 `needs_local_retrieval` 标记，用来给当地协作者派任务。
5. 对外沟通时把“资金链”改写为“资助 / 委托 / 赞助关系的证据分级核查”。

### 第2周增加内容

1. 在原本 60-80 个 actor seed 之外，加入 15-25 个外来 / 服务 / 资助 / 公共外交节点。
2. 建立 `funding_or_support_edges_sample.csv` 初版。
3. 为 USO、AWWA、Red Cross、NMCRS、ONC、JICA、TOMODACHI、美国领馆项目、NED、USAID 建立 source log。
4. 区分“组织存在证据”“项目关系证据”“资助证据”“解释性判断”四层。
5. 列出第一批需要当地人查的资料清单。

## 8. 对方案文本的建议替换句

可加入项目定位：

> 本项目的一期样本不仅包括冲绳本土市民团体和 NGO，也将纳入与冲绳基地和安全议题发生实质连接的外来 NGO、国际倡议组织、军属服务组织、公共外交项目和资助 / 委托机构。研究不会预设所有组织均属于反基地阵营，而是区分倡议型、服务型、公共外交型、国际合作型和资助型 actor，分析不同组织如何共同构成冲绳基地社会的民间组织生态。

可加入方法说明：

> 对于资助、委托、赞助和项目合作关系，本项目采用证据分级。只有官方 grant / award / contract、组织财报、政府名单、组织官网或正式项目报告能够支持的关系，才写入结论；地方新闻、活动页和社媒线索仅作为待核查资料。涉及 NED、USAID、外务省、美国使领馆和企业赞助的敏感关系，必须经过人工复核，不采用 AI 自审结果。

可加入实地调查说明：

> 如果公开线上资料显示某些组织、人物或资助关系高度相关但无法确认，本项目将列入“当地协作者补查清单”，优先查阅冲绳县 NPO 资料、图书馆 / 报刊数据库、组织年报、活动手册、基地社区公开资料和地方机构记录。

## 9. 本轮结论

新增方向是必要的，而且能显著增强 proposal。它会让研究从“反基地运动组织网络”升级为“冲绳基地社会中的民间组织生态与外部资源网络”。

但它也增加了风险：

- 资金链不能轻易下判断。
- 美国或外务省相关项目要区分 grant opportunity、award、recipient、implementation。
- 美军军属服务组织要单独分类，不要混入反基地或环保网络。
- 没有公开证据的内容要明确交给当地人补查。

因此，一期最稳做法是：

> 标准一期继续以本土市民团体、反基地 / 环保 / 自治 / 国际倡议网络为核心，同时新增“外来 NGO 与资助关系样本层”。这一层先做 seed、source log、证据分级和实地调查清单，不承诺完整资金链。

