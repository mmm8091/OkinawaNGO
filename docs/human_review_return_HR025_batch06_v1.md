# HR-025 外部服务／国际倡议组织地点语义回交报告 Batch 06

日期：2026-07-19  
承办人：项目负责人  
辅助核查：Codex  
状态：**已完成——11/11 条**

## 0. 批次边界

- 本批复核 HR-025 中 11 条外部服务、企业、国际合作、公共外交和跨国倡议 actor–place 候选边。
- 核心任务是区分：组织总部、持续／有界在场、事件场地和倡议对象。
- 特别遵守两条边界：
  - 军人家庭／基地社区服务组织按公开功能编码，不自动归为反基地或亲基地 actor；
  - 冲绳活动、冲绳议题或冲绳代表参与跨国网络，不自动证明在冲绳设有正式分支。
- 本批不批准资助边、联盟、成员关系、政治效果或组织立场；也不直接修改中央 registry、actor–place、source log、archive manifest 或 HR CSV。

## 1. 建议结论总表

| 项目 | 当前候选 | 辅助建议 | 核心理由 |
|---|---|---|---|
| AP022 | A017 沖縄対話プロジェクト→P001 `site_presence` | `accept` | 组织规约明确在名护设主事务所，并记录冲绳内连续对话活动；P001 只保留县域在场 |
| AP035 | X002 Phoenix Corporation / Phoenix Park Hotel→P001 `unclear` | `accept_with_revision`：`site_presence` | USO Okinawa 报道直接定位 Phoenix Park Hotel 在名护，并确认其属于 Phoenix Corporation；不得由捐赠反推企业总部 |
| AP036 | X003 AEC→P001 `unclear` | `accept_with_revision`：改键 P018 Ginowan、`headquarters` | AEC 官方公司页明确“沖縄本社”位于宜野湾市大山 |
| AP037 | X004 AWWA→P001 `site_presence` | `accept` | 多个来源确认其由冲绳美军配偶组织组成、在冲绳定期协调及开展慈善活动 |
| AP038 | X005 NOSCO→P001 `site_presence` | `accept` | 组织名、AWWA 成员身份及冲绳配偶会功能共同支持县域在场 |
| AP040 | X007 OESC→P001 `site_presence` | `accept` | 捐赠报道、非营利记录及 AWWA 材料共同支持冲绳持续服务组织身份 |
| AP044 | X010 沖縄NGOセンター→P001 `site_presence` | `accept_with_revision`：改键 P018 Ginowan、`headquarters` | 政府法人资料明确本店位于宜野湾市宜野湾 3-23-52 |
| AP046 | X012 TOMODACHI Initiative→P001 `unclear` | `accept_with_revision`：`site_presence` | TOMODACHI 官方设有“冲绳区域”校友框架及冲绳联系人，并有冲绳特定项目；不是冲绳总部 |
| AP105 | A064 No Bases Network→P001 `unclear` | `accept_with_revision`：`advocacy_target` | 可证冲绳代表参与及网络公开声援冲绳斗争，但不能证明正式“冲绳节点” |
| AP110 | A066 新外交イニシアティブ→P020 Naha `unclear` | `accept_with_revision`：`event_site` | ND 官方记录多次在那霸举办／运营活动；其机构总部仍在东京 |
| AP124 | X017 ACGO→P001 `unclear` | `accept_with_revision`：有时间边界的 `site_presence` | 2006 新闻、2012 AWWA 材料及免税组织索引支持冲绳组织身份；不据此声称当前连续运作或 Torii Station 总部 |

## 2. AP022 · 沖縄対話プロジェクト—Okinawa Prefecture

S022 官方规约明确：

- 正式名称为 `「台湾有事」を起こさせない・沖縄対話プロジェクト`；
- 主事务所置于冲绳县名护市田井等 415；
- 目的为通过冲绳—台湾对话避免双方成为战场；
- 组织开展连续对话研讨会、总结会、小型集会和传播活动。

来源：

- `https://okinawataiwa.net/index.php/about-us/about_terms/`
- `https://okinawataiwa.net/`

### 辅助建议

**AP022=`accept`，保留 P001 `site_presence`。**

P001 表示组织及其公开活动在冲绳县内存在。规约还足以另建 A017→P004 Nago `headquarters` 候选，但不必把现有县域边改成总部边。

时间边界：规约最初把它写成一年期项目；当前材料可证明项目后续活动，但地点边不应被表述为永久性机构。

## 3. AP035 · Phoenix Corporation / Phoenix Park Hotel—Okinawa Prefecture

原候选只能从向 USO Okinawa 捐赠推测地点，理由不足。补查的 USO Okinawa 署名报道直接写明：

- Phoenix Park Hotel 是 Phoenix Corporation 的酒店；
- 酒店位于名护；
- Phoenix Corporation owner 向 USO Okinawa 交付 1,000,000 日元捐赠。

来源：

- `https://okinawa.stripes.com/community-news/phoenix-park-hotel-proud-supporter-of-uso-okinawa.html`

### 辅助建议

**AP035=`accept_with_revision`，`unclear→site_presence`。**

关系文本改为：

> Phoenix Corporation 旗下 Phoenix Park Hotel 被直接定位于名护，支持其在冲绳县的实体经营在场。

限制：

- 地点成立依赖酒店的直接定位，不依赖“向冲绳组织捐赠”的反向推断；
- 现有 `Phoenix Corporation / Phoenix Park Hotel` 是公司＋设施的复合标签，后续 registry freeze 应决定以 Phoenix Corporation 为 actor、酒店为经营设施，还是保留复合 actor；
- 在实体层级未冻结前，不改写为企业 `headquarters`，也不把捐赠转成政治立场。

## 4. AP036 · American Engineering Corporation—Ginowan

旧关系文本只是 USO Okinawa sponsor listing，不能定位公司。AEC 官方公司资料已经直接给出：

- 公司正式名称；
- `沖縄本社`；
- 地址 `沖縄県宜野湾市大山7-11-47`；
- 1964 年开设冲绳本社及后续办公地点历史。

清水建设收购公告也独立称 AEC head office 位于 Ginowan-shi, Okinawa。

来源：

- `https://www.aec-japan.co.jp/company/`
- `https://www.shimz.co.jp/en/company/about/news-release/2026/2025058.html`

### 辅助建议

**AP036=`accept_with_revision`：P001→P018 Ginowan，`unclear→headquarters`。**

关系文本改为：

> American Engineering Corporation 的冲绳本社位于宜野湾市大山 7-11-47。

USO sponsor listing 不再作为总部定位依据。公司承包或赞助活动不自动表示对军事设施争议的政治立场。

## 5. AP037 · AWWA—Okinawa Prefecture

DVIDS 2012 报道明确：

- `American Women’s Welfare Association` 在冲绳举行 40 周年活动；
- AWWA 由五个冲绳美军配偶组织构成；
- 组织按月聚会，协调冲绳及周边岛屿的社区参与和慈善活动。

Okinawa Hai 与 NOSCO 材料也记录其冲绳配偶组织网络及岛内礼品／旧货店筹资机制。

来源：

- `https://www.dvidshub.net/news/87854/american-womens-welfare-association-celebrates-40-years`
- `https://okinawahai.com/american-womens-welfare-association/amp/`
- `https://nosco.wildapricot.org/awwa`

### 辅助建议

**AP037=`accept`，`site_presence`。**

本边只表示 AWWA 在冲绳的组织协调和服务活动。名称 freeze 时应把 `American Women’s Welfare Association` 作为有直接材料支持的名称，谨慎处理 NOSCO 页面出现的 `American Welfare & Works Association` 变体；本批不决定两种展开形式的历史／法定关系。

## 6. AP038 · NOSCO—Okinawa Prefecture

NOSCO 自身名称是 `Naval Officers' Spouses' Club of Okinawa`。其页面及 AWWA 资料把 NOSCO 列为冲绳五个配偶组织之一，并记录其参与岛内慈善／礼品店机制。

来源：

- `https://nosco.wildapricot.org/awwa`
- `https://www.dvidshub.net/news/87854/american-womens-welfare-association-celebrates-40-years`

### 辅助建议

**AP038=`accept`，`site_presence`。**

地点边不具体化为某一基地总部，因为本批来源支持的是冲绳县域组织在场。AWWA 成员关系属于单独的 actor–actor relation 审查，不由本地点决定自动批准。

## 7. AP040 · OESC—Okinawa Prefecture

现有材料分别支持：

- `Okinawa Enlisted Spouses' Club` 的明确冲绳身份；
- 组织向 USO Okinawa 的具名捐赠；
- 非营利记录；
- AWWA 材料中的冲绳配偶组织身份和岛内服务／筹资功能。

来源：

- `https://okinawa.stripes.com/community-news/okinawa-enlisted-spouses-club-uso-okinawa.html`
- `https://projects.propublica.org/nonprofits/organizations/980346507`
- `https://nosco.wildapricot.org/awwa`

### 辅助建议

**AP040=`accept`，`site_presence`。**

这里按观察到的军人家庭／社区服务功能编码，不推断反基地或亲基地立场。具体基地设施位置如需编码，应使用独立地址／运营来源另建候选边。

## 8. AP044 · 沖縄NGOセンター—Ginowan

经济产业省 Gビズインフォ 的法人资料明确：

- 法人名称 `特定非営利活動法人沖縄ＮＧＯセンター`；
- 法人番号 `7360005003047`；
- 本店所在地 `沖縄県宜野湾市宜野湾3丁目23番52号`；
- 同址还有适用事业所记录。

来源：

- `https://info.gbiz.go.jp/hojin/ichiran?hojinBango=7360005003047`
- `https://www.oki-ngo.org/about`

### 辅助建议

**AP044=`accept_with_revision`：P001→P018 Ginowan，`site_presence→headquarters`。**

关系文本改为：

> 特定非营利活动法人冲绳 NGO Center 的法定本店位于宜野湾市宜野湾 3-23-52。

其与 JICA、外务省或地方政府的服务／委托关系继续在 R10 等关系表单独编码；总部地点不证明资助链或运动联盟。

## 9. AP046 · TOMODACHI Initiative—Okinawa Prefecture

原 X012 只写“可能与冲绳有关”。补查官方材料确认：

- TOMODACHI 校友区域框架正式列有 `沖縄地域［沖縄］`；
- 有独立 Okinawa regional contact；
- 官方历史项目包括面向冲绳学生的 TOMODACHI-Frogs Jr.；
- 官方后续活动继续记录冲绳区域活动。

来源：

- `https://usjapantomodachi.org/ja/tomodachi-alumni-regional-framework/`
- `https://usjapantomodachi.org/ja/entrepreneurship-leadership/tomodachi-frogs-jr/`
- `https://usjapantomodachi.org/ja/2013/09/8772/`

### 辅助建议

**AP046=`accept_with_revision`，`unclear→site_presence`。**

关系文本改为：

> TOMODACHI 设有正式列名的冲绳校友区域框架，并实施过冲绳特定青年项目。

限制：

- `site_presence` 指区域网络和项目在场，不是法定总部或独立冲绳法人；
- 不把美国驻那霸总领事馆的支持写成 TOMODACHI 的那霸总部；
- 公共外交／交流项目按观察功能编码，不推断基地立场。

## 10. AP105 · No Bases Network—Okinawa Prefecture

S033 的“International network Okinawa node”说法过强。补查学术和运动会议材料只能安全确认：

- 2007 年全球反基地会议及 No Bases 网络有日本／冲绳代表参加；
- 研究者把这些代表描述为仍主要认同本地运动、并倾向保持松散网络；
- 代表该网络发言的会议文本明确声援冲绳当地社区的反基地斗争；
- 未找到正式章程、分支名录或组织页面证明存在制度化的 `Okinawa node`。

来源：

- `https://academic.oup.com/isq/article/53/3/571/1799701`
- `https://www.antiatom.org/GSKY/en/WC/e07wc/11-Naga-Close.pdf`

### 辅助建议

**AP105=`accept_with_revision`，`unclear→advocacy_target`。**

关系文本改为：

> No Bases Network 的公开跨国倡议与会议发言把冲绳反基地斗争作为声援和国际传播对象；冲绳代表参与网络，但未证实正式冲绳分支。

必须删除 `International network Okinawa node` 表述。共同参会、声援或跨国身份不构成稳定联盟或正式组织隶属。

## 11. AP110 · 新外交イニシアティブ—Naha

ND 官方资料明确显示其机构地址在东京，不支持那霸办公室。但其官方活动档案支持 P020 作为事件场地：

- 2014 年在那霸举办设立一周年／出版纪念研讨会；
- 2018 年列有 `トランプ政権下の東アジア外交と沖縄（那覇）`；
- 2022 年在那霸琉球新报 Hall 举行冲绳地域外交研讨会；
- 2025 年在那霸举行日美安保与冲绳和平构建研讨会；
- 多项活动由 ND 受冲绳县委托负责企划／运营。

来源：

- `https://www.nd-initiative.org/topics/1125/`
- `https://www.nd-initiative.org/event/`
- `https://www.nd-initiative.org/event/11326/`
- `https://www.nd-initiative.org/event/13026/`

### 辅助建议

**AP110=`accept_with_revision`，保留 P020 Naha，`unclear→event_site`。**

关系文本改为：

> 新外交イニシアティブ多次在那霸举办或受托运营冲绳基地、地域外交及国际和平相关活动；其组织总部仍在东京。

本边不把一次或多次活动参加转换成在地分支，也不从受托运营自动推出金额、政策效果或运动联盟。

## 12. AP124 · Army Community Group of Okinawa—Okinawa Prefecture

现有 S041/S072/S081 之外，补查到第二条独立公开报道和免税组织索引：

- Stars and Stripes 2006 报道把 ACGO 写为非营利组织，记录其由 `Army Women’s Group` 更名、秘书及为军人家庭提供 quality-of-life community programs；
- DVIDS 2012 把 ACGO 列为 AWWA 五个冲绳成员组织之一；
- AWWA 社区资料记录 Army on Okinawa Gift Shop；
- 公共免税组织索引以 EIN `26-1170858` 列出 `ARMY COMMUNITY GROUP OF OKINAWA ACGO`，地址层级为 APO, AP。

来源：

- `https://www.stripes.com/news/2006-07-26/okinawa-business-donates-to-military-support-group-1926638.html1`
- `https://www.dvidshub.net/news/87854/american-womens-welfare-association-celebrates-40-years`
- `https://okinawahai.com/american-womens-welfare-association/amp/`
- `https://501c3lookup.org/state/AP`

### 辅助建议

**AP124=`accept_with_revision`，`unclear→site_presence`，并加时间边界。**

关系文本改为：

> 2006–2012 公开材料确认 Army Community Group of Okinawa 作为冲绳军人家庭／社区服务组织在场，并被列为 AWWA 成员组织。

限制：

- 现有证据不充分证明 2026 年仍连续运作、当前法定状态或现名；
- 不把 P001 县域边精确化为 Torii Station `headquarters`；
- AWWA membership 仍需在 HR-018 按时期和身份边界单独决定；
- 服务组织不自动归为反基地或亲基地 actor。

## 13. 如负责人确认，本批主线程动作

1. AP022、AP037、AP038、AP040 按现有 `site_presence` 接受。
2. AP035 改为 `site_presence`，重写关系依据；在 registry freeze 处理 Phoenix Corporation／Phoenix Park Hotel 复合标签。
3. AP036 改键至 P018 Ginowan 并标为 `headquarters`；移除 sponsor listing 的定位功能。
4. AP044 改键至 P018 Ginowan 并标为 `headquarters`；补入政府法人资料。
5. AP046 改为 `site_presence`，补 TOMODACHI 冲绳区域框架和冲绳特定项目来源。
6. AP105 改为 `advocacy_target`，删除 `Okinawa node`；来源改为跨国网络研究及公开声援材料。
7. AP110 保留 P020 Naha，改为 `event_site`；明确总部在东京。
8. AP124 改为有时间边界的 `site_presence`；不生成 Torii Station 总部边，不在本批批准 AWWA membership。
9. 将本批新增网页先作为 source proposal 进入来源整合，所有 `relation_or_claim_approved` 仍为 `no`，再由主线程分配 S 编号与归档。
10. 合并后重跑 R03 spatial dossier、strict place–issue、source crosswalk、schema alias freeze、claim audit 和 HR-029 输入。

本报告本身未修改中央 CSV、source log、archive manifest 或 HR 队列。

## 14. 负责人决定

负责人于 2026-07-19 确认本批全部辅助建议：

- AP022、AP037、AP038、AP040：`accept`，保留 `site_presence`；
- AP035：`accept_with_revision`，`unclear→site_presence`，但不由酒店地点推断 Phoenix Corporation 总部；
- AP036：`accept_with_revision`，改键至 P018 Ginowan，语义为 `headquarters`；
- AP044：`accept_with_revision`，改键至 P018 Ginowan，语义为 `headquarters`；
- AP046：`accept_with_revision`，语义为 `site_presence`，仅表示 TOMODACHI 冲绳区域网络／项目在场；
- AP105：`accept_with_revision`，语义为 `advocacy_target`，删除未经证实的 `Okinawa node`；
- AP110：`accept_with_revision`，保留 P020 Naha，语义为 `event_site`，不得写成那霸办公室；
- AP124：`accept_with_revision`，保留有时间边界的 `site_presence`，不推断当前连续运作或 Torii Station 总部。

负责人同时确认本批所有来源与解释边界：

- 军人家庭／基地社区服务组织按观察功能编码，不自动归为反基地或亲基地 actor；
- 共同参会、跨国声援、受托运营或公共外交项目不生成联盟、隶属、资助效果或政治立场；
- AWWA membership、ACGO 当前身份及 Phoenix 复合实体规范继续由相应关系／schema gate 单独处理；
- 本报告作为人工决定回交记录，中央表仍留待主线程统一合并。
