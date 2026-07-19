# HR-030 来源元数据与归档复核回交报告 Batch 27

日期：2026-07-20  
承办人：项目负责人  
辅助调查：Codex  
来源队列：`outputs/next_wave_source_integration_v1/HR030_source_metadata_archive_review_v0.csv`  
本批范围：HR030-S273-NW2FS028 至 HR030-S294-NW2FS049，共 11 项  
状态：**负责人已确认——11 项 accept_with_revision；HR-030 完成**

## 0. 批次边界

- 本批只复核来源标题、类型、年份、locator、支持范围、证据级别和归档处理。
- 来源纳入和元数据确认不批准 actor、edge、联盟、合作、污染／健康因果、罢工合法性或组织连续性。
- 官方记录中的请求、发言、争议行为和行政知悉只按可观察程序记录，不推断结果或法律评价。
- S290、S291、S294 的既有失败状态不等于来源不存在；本轮重新测试其当前可访问性。
- 本轮只做线上调查，不启动当地资料；八重山大地会更长期的连续性仍不在本批解决。
- 本报告不修改 HR CSV、中央 source log、archive manifest、actor registry、候选边、图或正文。

## 0A. 本轮实际调查结果

### 归档状态发生了一项实质更新

HR-030 队列生成时把 S279 记作 SSL 失败，但当前 archive manifest 已显示：

- `archive_status=archived`；
- HTTP 200；
- 本地文件为 `source_docs/source_archive/S279/raw.html`。

因此 S279 不再需要重试。HR 队列是历史状态，合并时应以当前 manifest 为准。

### 三份 PDF 均完成页面级核验

1. **S273**：83 页 PDF。PDF p.1 的委员会报告日期为 2023-08-31；相关听证发生于 2022-12-09。PDF p.7 明确出现町田直美、仲松典子两名共同代表以及自 2016 年 PFOS 公布后开展水问题活动的证言。
2. **S282**：官方行政记录。目标条目在**印刷页 4／PDF p.5**，不是含义不清的单独 `p.4`。该条目确认 2008-02-14 新日本妇人会冲绳县本部向县知事公室提出请求。
3. **S294**：原 archive manifest 为 HTTP 403，但本轮以普通浏览器 User-Agent 和 parent-page Referer 成功取得 1,790,863 字节的 23 页 PDF。PDF 与 researchmap parent page共同确认：
   - 作者：鈴木鉄忠；
   - 发表日期：2019-03-08；
   - 场合：East Asian Sociological Association Inaugural Congress；
   - PDF p.22 把 `やいま大地会` 列为 A17，并把 A17 列入 A22 的 13 团体构成式。

S294 因而是有日期的会议发表幻灯片，不是 2026 年的 academic article。

### 两个失败网页目前可正常访问

- S290 当前 HTTP 200，最终 URL 自动补 `/`；页面标题显示荒谬的 `2302年12月23日`，但正文是“12 月 23 日八重山历史事件”跨年表，其中 2015 年条目记载八重山大地会结成。这说明 URL 年份段是页面／日历异常，不能当作史实年份。
- S291 琉球新报当前可完整访问；2016-01-24 发布，正文明确点名八重山大地会和八重洋一郎代表。旧 `TimeoutError` 可重试。

## 1. 辅助建议总表

| review_item_id | 来源 | 辅助建议 | 关键修订 | 归档处理 |
|---|---|---|---|---|
| HR030-S273-NW2FS028 | S273 | `accept_with_revision` | 2023 为报告年；另记 2022-12-09 听证；locator 精确至 PDF pp.5–7 | `archived_pdf_verified` |
| HR030-S275-NW2FS030 | S275 | `accept_with_revision` | 补全朝日标题；locator 限于付费墙前可见段落 | `archived_paywall_visible_lead` |
| HR030-S278-NW2FS033 | S278 | `accept_with_revision` | 补全标题；确认 query URL；精确到组织、照屋和专家限制语 | `archived_dynamic_url_verified` |
| HR030-S279-NW2FS034 | S279 | `accept_with_revision` | 补全标题；队列失败状态改用当前已归档状态 | `archive_status_stale_now_archived` |
| HR030-S280-NW2FS035 | S280 | `accept_with_revision` | 2026 仅作快照年；全国结构来自页面图示 | `archived_snapshot_verified` |
| HR030-S282-NW2FS037 | S282 | `accept_with_revision` | locator 改为印刷 p.4／PDF p.5 | `archived_pdf_verified` |
| HR030-S285-NW2FS040 | S285 | `accept_with_revision` | 2026 作为快照年；写明 2020–2026 可见通知范围 | `archived_rolling_page_snapshot` |
| HR030-S288-NW2FS043 | S288 | `accept_with_revision` | 使用完整会议信息；发言 133–134；不采纳合法性断言 | `archived_dynamic_url_verified` |
| HR030-S290-NW2FS045 | S290 | `accept_with_revision` | 重写标题和 year；2302 是异常页面路径，不是事件年 | `retry_currently_accessible` |
| HR030-S291-NW2FS046 | S291 | `accept_with_revision` | 精确标题／日期／段落；限制为多主办方活动中的 organizer-side role | `retry_transient_failure` |
| HR030-S294-NW2FS049 | S294 | `accept_with_revision` | 改为 2019 conference presentation；真实标题；PDF p.22 | `retry_with_browser_headers` |

建议分布：

- `accept`：0 项；
- `accept_with_revision`：11 项；
- `reject`／当地资料 defer：0 项。

11 项 evidence level 建议均保持不变。

## 2. HR030-S273-NW2FS028 · S273

### 调查结果

PDF 并非只包含一次请愿，而是第 448 回宜野湾市议会定例会福祉教育常任委员会的审查结果和会议录：

- PDF p.1：2023-08-31 委员会审查结果报告；
- PDF p.5：2022-12-09 “请愿第 1 号”听证开始，照屋正史以宜野湾ちゅら水会身份出席；
- PDF p.7：明确町田直美、仲松典子为两名共同代表，并回顾自 2016 年 PFOS 水问题公开后开展的活动；
- PDF pp.5–15：围绕血中浓度检查、健康调查和行政请求的质询。

证言只能证明组织自述的活动史和请求内容，不能给出精确法律成立日，也不能证明 PFAS 健康因果。

### 辅助建议

**`accept_with_revision`。**

- `source_type=official_legislative_record`、`year=2023`、`E4` 保持；
- 2023 明确为报告日期，note 另记听证日 2022-12-09；
- 标题可保留现有描述性题名；
- locator 改为：

> PDF p.1（2023-08-31 委员会报告）；PDF pp.5–7（2022-12-09 请愿听证）；尤其 PDF p.7 的町田直美、仲松典子共同代表及 2016 年以来活动史证言。

- 可支持组织身份、当时共同代表、PFAS 活动自述和健康调查请求；
- 不把 2016 写成精确成立日期，也不把请求／共同参加写成合作关系。

来源：  
https://www.city.ginowan.lg.jp/material/files/group/61/hukusi_202212.pdf

## 3. HR030-S275-NW2FS030 · S275

### 调查结果

朝日页面当前公开可见：

- 完整标题为 `学校敷地から化学物質PFOS 沖縄米軍基地に隣接 米基準の29倍`；
- 发布日期为 2022-09-25；
- 可见正文明确写宜野湾ちゅら水会募捐并委托专业机构调查；
- 可见正文也写明 2022-08-15 采样和 9 月 5 日公布结果；
- 随后进入付费墙。

当前 locator 所需的组织直接角色确实在付费墙前，不必声称核验了剩余 833 字。

### 辅助建议

**`accept_with_revision`。**

- `source_type=news`、`year=2022`、`E3` 保持；
- 补全标题；
- locator 改为：

> 2022-09-25 页面付费墙前可见第 2–3 段：宜野湾ちゅら水会募捐、委托专业机构、8 月 15 日三点采样、9 月 5 日公布结果。

- archive resolution=`archived_paywall_visible_lead`；
- 可支持 resident-funded commissioned sampling 的直接角色；
- 新闻及受访专家的污染来源判断不能自动升级为已裁定的基地来源或健康因果。

来源：  
https://www.asahi.com/articles/ASQ9S5J0LQ96TPOB004.html

## 4. HR030-S278-NW2FS033 · S278

### 调查结果

动态 query 页面当前最终 URL 保持 `?display=1`，可完整读取：

- 完整标题为 `泡が消えた後に残った白い粉からPFAS検出 宜野湾市のマンホール`；
- 发布主体为琉球放送，日期为 2026-05-05；
- 正文点名宜野湾ちゅら水会成员采样并委托专家检测；
- 点名照屋正史事务局长；
- 专家明确说不能换算成泡沫体积或当时下水浓度。

### 辅助建议

**`accept_with_revision`。**

- `source_type=news`、`year=2026`、`E3` 保持；
- 使用完整标题；
- locator 改为：

> 第 3–6 段：宜野湾ちゅら水会采样和委托、专家检测、不能换算的限制语；第 8 段：照屋正史事务局长。

- archive resolution=`archived_dynamic_url_verified`；
- 可支持 2026 年组织连续可见性、照屋职位和一次有界采样角色；
- 不将检测结果换算成污染规模、排水浓度、来源归责或健康影响。

来源：  
https://newsdig.tbs.co.jp/articles/-/2642471?display=1

## 5. HR030-S279-NW2FS034 · S279

### 调查结果

当前页面和本地归档均可用。完整标题结构为：

> 沖縄の米軍基地PFAS汚染／周辺住民の健康放置 地位協定などを議論／全国交流集会

2026-02-16 报道把：

- `PFAS汚染から市民の生命を守る連絡会`；
- `宜野湾ちゅら水会`

作为两个分别加引号列出的市民团体，并记录两个团体成员在同一线上交流集会报告。它适合用于 identity separation 和 attributed participation，不适合生成联盟边。

### 辅助建议

**`accept_with_revision`。**

- `source_type=party_news`、`year=2026`、`E3` 保持；
- 使用完整标题；
- locator 改为“2026-02-16 正文第 2 段，分别列名两个团体”；
- archive resolution=`archive_status_stale_now_archived`；
- 不把同场报告写成稳定联盟、合作机构或成员关系；
- 党报的单篇报道不独立证明污染／健康因果。

来源：  
https://www.jcp.or.jp/akahata/aik25/2026-02-16/2026021611_01_0.php

## 6. HR030-S280-NW2FS035 · S280

### 调查结果

新日本妇人会中央本部“新妇人介绍”页面明确提供：

- 正式名称和英文名；
- 五项目的；
- 1962-10-19 创立；
- 中央本部信息；
- 页面“全国”结构图写有 8,600 个班、900 个支部、47 都道府县本部和中央本部。

页面没有可见发布日期，2026 只能是访问／归档快照年。

### 辅助建议

**`accept_with_revision`。**

- `source_type=organization_website`、`E4` 保持；
- `year=2026` 保持，但 note 写“access/snapshot year; page has no publication date”；
- locator 改为：

> “会の名称／会の目的／会の創立／中央本部／全国”各栏及全国组织结构图。

- support scope 可保持“国家协会身份和都道府县本部结构”；
- 该结构支持冲绳县本部作为分支层级的组织边界，但不把中央本部的每次行动转给 A115，也不推断党派隶属。

来源：  
https://www.shinfujin.gr.jp/about/organization/

## 7. HR030-S282-NW2FS037 · S282

### 调查结果

《沖縄県行政記録 平成20年》目标条目在：

- PDF p.5；
- 该页底部印刷页码为 4；
- 2008 年 2 月 14 日栏。

条目明确写新日本妇人会冲绳县本部就美国海军陆战队员对女中学生暴行事件等向县知事公室提出请求。

### 辅助建议

**`accept_with_revision`。**

- `source_type=prefectural_official`、`year=2008`、`E4` 保持；
- locator 改为：

> 2008-02-14 entry，印刷 p.4／PDF p.5。

- archive resolution=`archived_pdf_verified`；
- 可独立支持 A115 在该日期提出请求；
- 行政日志不提供请求全文、回应或结果，不转移中央组织行动，也不推断党派隶属。

来源：  
https://www.pref.okinawa.lg.jp/_res/projects/default_project/_page_/001/014/905/h20gyouseikiroku.pdf

## 8. HR030-S285-NW2FS040 · S285

### 调查结果

冲绳县滚动页面当前显示：

- 页面标题 `争議行為の届出と予告`；
- 更新日 2026-03-25；
- 2020 年度至 2025 年度范围内，多次列出 `全日本港湾労働組合沖縄地方本部`；
- 可见开始日从 2020-11-30 延伸到 2026-04-06。

这能支持组织精确名称和跨年公开运作，但只涉及公益事业争议预告，不能直接证明其基地／和平议题立场。

### 辅助建议

**`accept_with_revision`。**

- `source_type=prefectural_official`、`E4` 保持；
- `year=2026` 作为本次滚动页面快照年；
- locator 改为：

> 页面更新 2026-03-25；“争議予告の公表—沖縄県公表”中 2020–2025 年度、开始日 2020-11-30 至 2026-04-06 的全港湾冲绳地方本部条目。

- archive resolution=`archived_rolling_page_snapshot`；
- 可支持身份和连续运作，不裁定具体罢工合法性、效果或 Phase-1 政治立场。

来源：  
https://www.pref.okinawa.lg.jp/shigoto/koyorodo/1012030/1012056.html

## 9. HR030-S288-NW2FS043 · S288

### 调查结果

国会记录的完整标题为：

> 第213回国会 参議院 政府開発援助等及び沖縄・北方問題に関する特別委員会 第5号 令和6年5月24日

发言 133 中，议员描述全港湾冲绳地方本部于 2024-03-11 至 13 日在石垣港实施罢工，并提出强烈合法性评价。发言 134 中，冲绳担当大臣：

- 明确认知该组织在石垣港实施罢工；
- 把理由概括为米军舰艇使用港口带来的地域安心／安全担忧；
- 明确拒绝对劳动法定位作答。

因此可接受的官方确认来自发言 134；发言 133 的“违法”“恐怖行为”等是提问者意见，不能作为本项目裁定。

### 辅助建议

**`accept_with_revision`。**

- `source_type=official_legislative_record`、`year=2024`、`E4` 保持；
- 使用完整会议信息作为 title；
- locator=`statements 133–134, especially ministerial acknowledgment in 134`；
- archive resolution=`archived_dynamic_url_verified`；
- 可支持事件发生、组织归属和官方转述的罢工理由；
- 不裁定合法性、预告义务、物流损害强度或行动效果。

来源：  
https://kokkai.ndl.go.jp/simple/detail?minId=121315359X00520240524

## 10. HR030-S290-NW2FS045 · S290

### 调查结果

当前页面 HTTP 200，但存在明显的日历／URL 异常：

- URL 和页面 h1 显示 `2302年12月23日`；
- 页面实际栏目是“今日の日の八重山の過去の主なできごと”；
- 其 2015 年历史条目写“从文化活动视角阻止石垣岛自卫队部署，八重山大地会结成”。

因此，`2302` 不是史实年份；2015 是页面历史条目的事件年，不是网页发布日期。当前题名“地域年表 2015 年 12 月 23 日”把二者混合了。

### 辅助建议

**`accept_with_revision`。**

- `source_type=community_site`、`E2` 保持；
- title 改为：

> やいまタイム「今日の日の八重山の過去の主なできごと」（12月23日）

- year 改为：

> `n.d. / accessed 2026; historical entry dated 2015-12-23`

- locator 精确到 2015 年条目；
- archive resolution=`retry_currently_accessible`，重试时使用补尾斜杠后的最终 URL；
- 只能作为成立日期和议题目的的 E2 lead；冻结 2015-12-23 前仍需原始地方报纸或其他独立来源；
- 不据此推断 2015 至今连续活动。

来源：  
https://yaimatime.com/schedule/archive/2302/12/23/

## 11. HR030-S291-NW2FS046 · S291

### 调查结果

琉球新报页面当前可完整访问：

- 题名 `陸自配備反対を決議 石垣、住民180人が緊急集会`；
- 发布于 2016-01-24；
- 正文写住民会等主办 1 月 23 日紧急集会；
- “主办者致辞”段点名市民团体八重山大地会的八重洋一郎代表。

它支持名称、代表和 organizer-side greeting，但没有给出全部主办 roster，也不能证明稳定联盟。

### 辅助建议

**`accept_with_revision`。**

- `source_type=local_news`、`year=2016`、`E3` 保持；
- locator 改为“2026 页面中的 2016-01-24 原始报道，第 1–3 段；尤其主办者致辞段”；
- support scope 改为：

> Exact identity, representative, and organizer-side public role in a multi-organizer anti-deployment rally.

- archive resolution=`retry_transient_failure`；
- 不把“住民会等”还原成未列出的固定联盟，也不据一场活动证明长期连续性。

来源：  
https://ryukyushimpo.jp/news/entry-209354.html

## 12. HR030-S294-NW2FS049 · S294

### 调查结果

researchmap parent page 和成功取得的 PDF 共同推翻了当前两项元数据：

- 不是 2026 年无日期附件；发表日期是 2019-03-08；
- 不是 academic article；是 EASA 国际会议一般口头发表的幻灯片。

真实题名是：

> Militarizing a Border Island: Local Struggles Supporting and Opposing a Military Base Installation in Ishigaki Island, Okinawa

PDF p.22：

- A17=`やいま大地会`；
- A22=`石垣島に軍事基地をつくらせない市民連絡会`；
- 作者用括号把 A17 列为 A22 的 13 个组成团体之一。

这仍是作者的分析图，不是 A22 官方名册；它可以作为 alias／component lead，但不能单独冻结成员关系。

### 辅助建议

**`accept_with_revision`。**

- title 改为上述真实英文发表题名；
- `source_type` 改为 `academic_presentation`，不要保留会暗示论文／同行评议的 `academic_article`；
- `year=2019`；
- `evidence_level=E2` 保持；
- locator 改为：

> researchmap parent record: 2019-03-08, EASA Inaugural Congress；PDF p.1 title/date/author；PDF p.22 A17 and A22 component notation.

- support scope 保持“alias lead and possible component relation to A010”；
- archive resolution=`retry_with_browser_headers`：本轮以 browser User-Agent + parent Referer 已成功取得 PDF，中央 archive manifest 仍应通过正式归档流程更新；
- `やいま大地会` 与 `八重山大地会` 的 alias 关系可作为强线索，但正式冻结仍需 S291、其他独立来源和人工决定共同处理；
- 作者分析式不等于官方 roster、稳定联盟或持续成员关系。

来源：

- https://researchmap.jp/teppy/presentations/10378736
- https://researchmap.jp/teppy/presentations/10378736/attachment_file.pdf

## 13. 建议负责人本批判断

建议 11 项全部确认为 `accept_with_revision`：

1. HR030-S273-NW2FS028；
2. HR030-S275-NW2FS030；
3. HR030-S278-NW2FS033；
4. HR030-S279-NW2FS034；
5. HR030-S280-NW2FS035；
6. HR030-S282-NW2FS037；
7. HR030-S285-NW2FS040；
8. HR030-S288-NW2FS043；
9. HR030-S290-NW2FS045；
10. HR030-S291-NW2FS046；
11. HR030-S294-NW2FS049。

如负责人确认，主线程后续合并时：

- HR-030 共 22 项结清：Batch 26 的 1 accept／10 accept_with_revision，加本批 11 accept_with_revision；
- S279 使用当前已成功归档状态，不再重试；
- S290、S291 定向重试；
- S294 改为 2019 `academic_presentation`，按浏览器请求头重新正式归档；
- S282 locator 改为印刷 p.4／PDF p.5；
- S273 同时保留 2023 报告年与 2022-12-09 听证日；
- S275 明示付费墙前 visible lead；
- S285 明示滚动页面快照日期和可见通知范围；
- 不借上述元数据决定批准任何 actor、edge、联盟、合作、污染／健康因果、合法性或历史连续性。

## 14. 负责人确认

负责人于 2026-07-20 确认本批判断：

- `accept_with_revision`：HR030-S273-NW2FS028、HR030-S275-NW2FS030、HR030-S278-NW2FS033、HR030-S279-NW2FS034、HR030-S280-NW2FS035、HR030-S282-NW2FS037、HR030-S285-NW2FS040、HR030-S288-NW2FS043、HR030-S290-NW2FS045、HR030-S291-NW2FS046、HR030-S294-NW2FS049；
- `accept`／`reject`／当地资料 defer：0 项。

连同 Batch 26，HR-030 共 22 项已经全部由负责人判断：

- `accept`：1 项；
- `accept_with_revision`：21 项；
- `reject`／当地资料 defer：0 项。

本报告作为后 11 项人工决定及 HR-030 完成状态的回交记录。中央 source log、HR CSV、archive manifest、actor registry、候选边、图与正文仍留待主线程统一合并。
