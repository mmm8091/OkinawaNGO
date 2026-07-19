# HR-030 来源元数据与归档复核回交报告 Batch 26

日期：2026-07-20  
承办人：项目负责人  
辅助调查：Codex  
来源队列：`outputs/next_wave_source_integration_v1/HR030_source_metadata_archive_review_v0.csv`  
本批范围：HR030-S253-NW2FS006 至 HR030-S271-NW2FS026，共 11 项  
状态：**负责人已确认——1 项 accept，10 项 accept_with_revision**

## 0. 批次边界

- 本批只复核来源标题、来源类型、年份、定位、支持范围、证据级别和归档处理。
- 来源进入 source log 不等于批准 actor、actor-issue／actor-place edge、联盟、资金、选举作用或因果解释。
- 归档失败不等于页面内容不存在；网页当前可访问时，应先记技术性重试，不降级事实本身。
- 组织自述可支持其公开行动或立场，不独立证明人数、触达、选票、污染、健康影响或行政认同。
- S158、S204 已经是中央 source log 中的 `human_checked` 记录；新提案不得覆盖其既有标题和类型。
- 本轮只做线上调查，不启动当地资料或地方数据库任务。
- 本报告不修改 HR CSV、中央 source log、archive manifest、actor registry、候选边、图或正文，留待主线程统一合并。

## 0A. 本轮实际调查结果

### 三个归档失败项目前均可访问

- S258 琉球新报页面当前可完整打开，2018-08-24 发布；旧失败为 `TimeoutError`。
- S261 沖縄县官方选举页面当前可完整打开，明确列出 2022-08-25 告示、2022-09-11 投票；旧失败为 SSL EOF。
- S263 全日本民医连页面当前可完整打开，2022-08-16 发布，正文确认 7 月 29 日线上集会；旧失败为 SSL EOF。

因此，三项均建议保留来源并执行定向重试，不把失败解释为证据缺失。

### 两份 PDF 已完成文件和页面级核查

1. S259 是真实 PDF，不是伪装 HTML。文件共 14 页，印刷页码为 45–58。当前 locator 把 PDF 页码和印刷页码混在一起，并且活动日期有误：
   - PDF pp.5–6／印刷 pp.49–50：活动表；
   - PDF p.8／印刷 p.52：八名学生组成的非正式小组；
   - 活动表实际包含 9 月 5 日公开讨论、9 月 12 日候选政策比较、9 月 13 日 workshop、9 月 19 日政策提言公开等不同节点。
2. S271 是 20 页扫描 PDF。PDF p.1 的市政府回答书落款为 2023 年 2 月末日，并明确逐项回应研究会 2022-07-18 的意见。PDF p.2 起为附件资料，其中附件 1 本身日期为 2022-11-01；不能把附件日期误作回答书日期。

### 付费墙与快照型页面

- S265 的本地归档 HTML 可核验完整标题、2022-07-31 发布日期和摘要，但元数据明确 `isAccessibleForFree=false`。没有订阅时，支持范围只能到标题／摘要记载的两种相反政治评价，不能声称已核验付费正文。
- S204、S269 是会持续更新的组织网站。`2026` 应解释为访问／快照年份，不是页面首发年份。S269 没有可见发布日期。

## 1. 辅助建议总表

| review_item_id | 来源 | 辅助建议 | 元数据／定位处理 | 归档处理 |
|---|---|---|---|---|
| HR030-S253-NW2FS006 | S253 | `accept_with_revision` | 类型保留 `community_site`；标题改为页面完整标题；注明第一人称参与者回顾 | `archived_verified` |
| HR030-S254-NW2FS007 | S254 | `accept_with_revision` | 使用页面原题；publisher 为新日本妇人会中央本部；区分网页发布日期和谈话日期 | `archived_verified` |
| HR030-S258-NW2FS011 | S258 | `accept_with_revision` | 保留原题但 locator 区分 8/23 请求与 8/26 预计受诺 | `retry_transient_failure` |
| HR030-S259-NW2FS012 | S259 | `accept_with_revision` | 修正 PDF／印刷页码和活动日期 | `archived_pdf_verified` |
| HR030-S261-NW2FS014 | S261 | `accept_with_revision` | 使用官方完整页面标题；2022 为选举年份，另记 2024 页面更新日 | `retry_transient_failure` |
| HR030-S263-NW2FS016 | S263 | `accept_with_revision` | 使用页面原题；区分 7/29 活动与 8/16 报道日 | `retry_transient_failure` |
| HR030-S265-NW2FS018 | S265 | `accept_with_revision` | 补完整标题并把 locator 限于标题／摘要可见内容 | `archived_paywall_limited` |
| HR030-S158-NW2FS022 | S158 | `accept` | 原 `human_checked` 标题、类型、年份全部保留 | `reuse_existing_preserve_human_checked` |
| HR030-S204-NW2FS023 | S204 | `accept_with_revision` | 原标题／类型保留；2026 标为访问年；缩窄 locator | `reuse_existing_preserve_human_checked` |
| HR030-S269-NW2FS024 | S269 | `accept_with_revision` | 2026 标为访问年；精确到两个相关小节 | `archived_snapshot_verified` |
| HR030-S271-NW2FS026 | S271 | `accept_with_revision` | 精确到 PDF p.1；保留简明题名和 2023 年 | `archived_scanned_pdf_verified` |

建议分布：

- `accept`：1 项；
- `accept_with_revision`：10 项；
- `reject`／当地资料 defer：0 项。

所有 11 项证据级别建议保持不变。

## 2. HR030-S253-NW2FS006 · S253

### 调查结果

本地归档页面显示：

- 发布日期为 2015-04-29；
- 页面完整标题是 `第1回「ゆんたく」から始まった、沖縄・若者の抵抗（元山 仁士郎）`；
- 作者以第一人称回顾 2014-08-12 的学生 cross-talk 如何促成联系，并说明知事选前组织边野古、高江 field-learning bus tour。

它既不是机构正式报告，也不是独立新闻，而是刊载于社区／评论网站的具名参与者叙述。中央受控类型中没有必要新增 `participant_account`。

### 辅助建议

**`accept_with_revision`。**

- `source_type=community_site` 保持；
- `title` 改用上述页面完整题名；
- `year=2015`、`evidence_level=E3` 保持；
- locator 改为：

> 2015-04-29；“知られていない基地”小节中关于 2014-08-12 cross-talk、知事选前讨论和边野古／高江 bus tour 的第一人称记述。

- 支持范围保持“2014 youth observation/dialogue intervention”；
- bias note 必须保留“retrospective first-person participant account”；
- 文中自报约 50 人、首次到访比例和媒体扩散，不作为独立人数、触达或选举效果事实。

来源：  
https://www.magazine9.jp/article/yuntacrew/18975

## 3. HR030-S254-NW2FS007 · S254

### 调查结果

页面显示：

- 站点／publisher 为 `新日本婦人の会中央本部`；
- 页面题名为 `【談話】 沖縄県知事選で圧勝の民意に応え ただちに新基地建設中止を`；
- 网页发布日期为 2014-11-21；
- 谈话正文日期为 2014-11-19；
- 署名为副会长西川香子；
- 正文明确把连续行动归于“沖縄県本部の会員”，同时也自报全国会员行动。

### 辅助建议

**`accept_with_revision`。**

- `source_type=organization_statement`、`year=2014`、`E4` 保持；
- 标题按页面原题统一；
- publisher 明确为中央本部，不把来源本身改写为 A115 冲绳县本部文件；
- locator 改为：

> 2014-11-21 网页；正文落款 2014-11-19；第二段明确归因“沖縄県本部の会員”行动。

- 可支持国家组织的公开选后解释和其对县本部会员行动的具名自报；
- 不能由此证明行动规模、选票作用，也不能把国家组织的全部行动自动转给 A115。

来源：  
https://www.shinfujin.gr.jp/2943/

## 4. HR030-S258-NW2FS011 · S258

### 调查结果

页面当前可完整打开。精确标题为：

> 沖縄県知事選 出遅れ危機感「結束優先」 玉城氏、出馬要請受諾

正文确认：

- 由县议会与党会派、反边野古政党、劳组、企业构成的临时“调整会议”正式决定拥立；
- 8 月 23 日向玉城提出参选请求；
- 正文当时写的是预计玉城将在 8 月 26 日受诺。

标题使用“受诺”，但当日正文仍将实际受诺写为未来预期，因此本来源最稳妥支持的是 8 月 23 日的决定和请求，不能单凭标题把实际受诺日期提前。

### 辅助建议

**`accept_with_revision`。**

- `source_type=local_news`、`year=2018`、`E3` 保持；
- 使用页面精确标题；
- locator 改为：

> 2018-08-24 发布，正文首段及 8 月 23 日调整会议段落：确认正式拥立和提出参选请求；正文把 8 月 26 日受诺写作预计事项。

- support scope 保持“2018 candidate-selection request by a temporary mixed coalition”；
- 调整会议只作临时事件节点，不编码成 NGO 或稳定联盟；
- archive resolution=`retry_transient_failure`。当前页面可访问，旧 `TimeoutError` 不构成证据否定。

来源：  
https://ryukyushimpo.jp/news/entry-789039.html

## 5. HR030-S259-NW2FS012 · S259

### 调查结果

J-STAGE endpoint 返回的本地文件为可正常解析和渲染的 14 页 PDF，MIME 为 `application/pdf;charset=UTF-8`。现有 locator 的 `pp.4-5`、`p.7` 没说明使用 PDF 页码还是印刷页码，且列出的 9/13、9/19 日期没有覆盖实际活动表结构。

### 辅助建议

**`accept_with_revision`。**

- `source_type=academic_article`、`year=2019`、`E4` 保持；
- archive resolution=`archived_pdf_verified`；
- locator 改为：

> PDF pp.5–6／印刷 pp.49–50：2018 年活动表，含 9/5 公开讨论、9/12 候选政策比较、9/13 workshop、9/19 政策提言公开；PDF p.8／印刷 p.52：八名学生组成的非正式小组，论文未给成员 roster。

- 可支持该项目的 civic-learning、公共讨论、政策比较和提言公开窗口；
- 论文为实践者学术记录，不能把被遮蔽候选人或未列名学生制造成 actor，也不证明选举效果。

来源：  
https://www.jstage.jst.go.jp/article/isvsjapan/19/0/19_45/_pdf/-char/en

## 6. HR030-S261-NW2FS014 · S261

### 调查结果

冲绳县官方页面当前可正常访问。页面精确标题为：

> 【特設ページ】令和4年沖縄県知事選挙及び沖縄県議会議員補欠選挙

页面显示：

- 知事选告示日为 2022-08-25；
- 选举期日为 2022-09-11；
- 页面更新日为 2024-02-22；
- 另链接候选人、投票和开票官方数据。

### 辅助建议

**`accept_with_revision`。**

- 使用官方完整题名；
- `source_type=official_data`、`year=2022`、`E4` 保持；
- 在 note 中另记 `page updated 2024-02-22`，不把更新年误作选举年；
- locator 改为“选举日程第 1 节及选举数据第 5 节”；
- 只支持选举窗口和制度背景，不支持任何市民 actor 的角色或因果效果；
- archive resolution=`retry_transient_failure`。当前访问成功，旧 SSL EOF 应定向重试。

来源：  
https://www.pref.okinawa.jp/kensei/senkyo/1005009/1023802/1025046/index.html

## 7. HR030-S263-NW2FS016 · S263

### 调查结果

全日本民医连官方页面当前可正常访问：

- 网页发布日期为 2022-08-16；
- 页面原题为 `全国の連帯で平和な沖縄 沖縄県知事選集会ひらく`；
- 正文确认全日本民医连于 7 月 29 日举行全国线上集会；
- 页面自报全国 436 个接入点，并明确出现要求玉城胜选／连任的号召。

### 辅助建议

**`accept_with_revision`。**

- `source_type=organization_action_record`、`year=2022`、`E4` 保持；
- 标题按页面原题，避免自行加入破折号；
- locator 改为：

> 2022-08-16 报道；首段与后续发言段确认 2022-07-29 集会、组织自报 436 个接入点和明确连任号召。

- 436 是 access points，不是人数、独立组织数、选民数或效果；
- archive resolution=`retry_transient_failure`。当前访问成功，旧 SSL EOF 应重试。

来源：  
https://www.min-iren.gr.jp/news-press/shinbun/20220816_46093.html

## 8. HR030-S265-NW2FS018 · S265

### 调查结果

冲绳时报网页受 robots／付费限制，但已归档 HTML 的公开元数据可核验：

- 发布日期为 2022-07-31；
- `isAccessibleForFree=false`；
- 完整标题为：

> 「知事選を前にいい発信ができた」と玉城デニー氏の与党 野党は一蹴「県民大会ではなく決起集会」

- description 只支持与党把 7 月 30 日活动评价为知事选前的良好发信、在野党把它评价为决起集会。

### 辅助建议

**`accept_with_revision`。**

- `source_type=local_news`、`year=2022`、`E3` 保持；
- 使用完整标题；
- locator 限为：

> archived HTML title／description／datePublished；付费正文未核验。

- support scope 保持“classification dispute for 2022 All Okinawa issue event”；
- 两方评价只能作为竞争性政治解释，不能据此裁定主办目的，也不能把议题活动自动升级为 endorsement；
- archive resolution=`archived_paywall_limited`。

来源：  
https://www.okinawatimes.co.jp/articles/-/1000372

## 9. HR030-S158-NW2FS022 · S158

### 调查结果

中央 source log 中 S158 已为 `human_checked`。当前页面“研究会について”可见：

- 2018-03-31 的设立宗旨；
- 三名共同代表；
- 研究会规约链接；
- 事务局信息；
- 后续更新的签名活动内容。

三名共同代表属于 2018 年有日期的领导层观察，不是永久 roster。新提案的元数据差异不足以推翻既有人工决定。

### 辅助建议

**`accept`。**

- 完整保留既有 `title=宮古島地下水研究会 団体概要`；
- 完整保留 `source_type=organization_profile`、`year=2026`、`E4`；
- locator 可继续写“設立趣旨；2018-03-31 共同代表；規約；事務局”；
- archive resolution=`reuse_existing_preserve_human_checked`；
- 不以此来源解决 C015 身份，也不把 2018 代表名单当作当前名单。

来源：  
https://miyakojima-tikasui.com/about_us.html

## 10. HR030-S204-NW2FS023 · S204

### 调查结果

中央 source log 中 S204 已为 `human_checked`。当前首页提供活动报告、研究报告、媒体报道和通知入口，并显示 2024–2025 年的具日期内容。它适合支持组织网站持续存在和公开活动索引，但首页不是所有具体科学主张的统一证据。

### 辅助建议

**`accept_with_revision`。**

- 既有 `title=宮古島地下水研究会 公式サイト`、`source_type=organization_site`、`E4` 保持；
- `year=2026` 保持，但 note 明确这是访问／快照年，不是组织成立年或页面首发年；
- locator 缩窄为：

> 首页“活動報告／研究レポート／メディア報道／お知らせ”索引及可见 2024–2025 日期条目。

- archive resolution=`reuse_existing_preserve_human_checked`；
- 可支持网站连续性和进一步检索入口；单项污染、健康或行政关系主张仍需相应页面和 claim-level review。

来源：  
https://miyakojima-tikasui.com/

## 11. HR030-S269-NW2FS024 · S269

### 调查结果

页面没有可见发布日期，当前正文明确把军事设施连接到两类水安全问题：

- “2017 年以后消费量急增”小节：把自卫队设施建设和驻屯地人口列入用水、生活排水增加的组织方解释；
- “自衛隊施設の排水”小节：明确把重金属、化学物质和地下水污染风险联系起来。

这些是研究会自己的风险框架，不是独立检测结果。

### 辅助建议

**`accept_with_revision`。**

- `title=地下水の危機とは？`、`source_type=organization_site`、`E3` 保持；
- `year=2026` 保持，但必须标明“访问／快照年；页面无发布日期”；
- locator 改为：

> “2017年以降、消費量が一気に増加”及“自衛隊施設の排水”两节；2026 年访问快照。

- support scope 可写“研究会公开把自卫队设施用水、生活排水及设施排水表述为地下水风险类别”；
- 不写成已证实的污染、因果健康影响或行政认定；
- archive resolution=`archived_snapshot_verified`。

来源：  
https://miyakojima-tikasui.com/crisis.html

## 12. HR030-S271-NW2FS026 · S271

### 调查结果

扫描 PDF p.1 的回答书标题较长，核心对象是研究会 2022-07-18 对市长回答所提出的意见。页面显示：

- 回答主体为宫古岛市；
- 回答书日期为 2023 年 2 月末日；
- 明确逐项回应研究会提出的五项提案／意见；
- PDF pp.2–20 是附件和检验资料，不应把附件日期当作回答书日期。

它可以独立支持市政府把研究会作为行政回应对象，但不能证明市政府同意研究会的科学解释。

### 辅助建议

**`accept_with_revision`。**

- 简明 `title=宮古島地下水研究会の見解に対する回答書` 可保留；
- `source_type=local_official`、`year=2023`、`E4` 保持；
- locator 改为：

> PDF p.1：完整标题、宫古岛市署名、2023 年 2 月末日及对研究会提案 1–5 的回应结构；pp.2–20 为附件。

- support scope 保持“independent municipal recognition of the group as an administrative interlocutor”；
- 将“repeated”限定为该文件呈现了“研究会提案—市长回答—研究会意见—市政府再回答”的往返程序，而不是概括所有年份的持续协作；
- 不推断行政同意、正式合作、污染事实或健康因果；
- archive resolution=`archived_scanned_pdf_verified`。

来源：  
https://www.city.miyakojima.lg.jp/kurashi/seikatsu/kankyohozen/files/tikasui.pdf

## 13. 建议负责人本批判断

建议一次确认：

1. HR030-S253-NW2FS006：`accept_with_revision`；
2. HR030-S254-NW2FS007：`accept_with_revision`；
3. HR030-S258-NW2FS011：`accept_with_revision`；
4. HR030-S259-NW2FS012：`accept_with_revision`；
5. HR030-S261-NW2FS014：`accept_with_revision`；
6. HR030-S263-NW2FS016：`accept_with_revision`；
7. HR030-S265-NW2FS018：`accept_with_revision`；
8. HR030-S158-NW2FS022：`accept`；
9. HR030-S204-NW2FS023：`accept_with_revision`；
10. HR030-S269-NW2FS024：`accept_with_revision`；
11. HR030-S271-NW2FS026：`accept_with_revision`。

如负责人确认，主线程后续合并时：

- 不改 S158、S204 的既有人工确认标题和来源类型；
- 为 S258、S261、S263 重试归档，并在重试前保留“当前网页可访问”的人工记录；
- 对 S265 明示 `paywall-limited metadata/lead only`；
- 按本报告修正 S259、S271 的 PDF 页码 locator；
- 对 S204、S269 把 2026 解释为访问／快照年；
- 不借任何一项批准 actor、edge、联盟、资金、污染事实、健康影响或选举因果。

## 14. 负责人确认

负责人于 2026-07-20 确认本批判断：

- `accept`：HR030-S158-NW2FS022；
- `accept_with_revision`：HR030-S253-NW2FS006、HR030-S254-NW2FS007、HR030-S258-NW2FS011、HR030-S259-NW2FS012、HR030-S261-NW2FS014、HR030-S263-NW2FS016、HR030-S265-NW2FS018、HR030-S204-NW2FS023、HR030-S269-NW2FS024、HR030-S271-NW2FS026；
- `reject`／当地资料 defer：0 项。

本报告作为 HR-030 前 11 项人工决定的回交记录。中央 source log、HR CSV、archive manifest、actor registry、候选边、图与正文仍留待主线程统一合并。
