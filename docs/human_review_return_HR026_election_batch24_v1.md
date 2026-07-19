# HR-026 县知事选—市民组织接口回交报告 Batch 24

日期：2026-07-20  
承办人：项目负责人  
辅助调查：Codex  
来源队列：`outputs/R09_election_civic_interface_v1/HR026_election_civic_role_review_v0.csv`  
本批范围：HR026-01–10（2014 年 5 项、2018 年 5 项）  
状态：**负责人已确认——7 项 accept，3 项 accept_with_revision**

## 0. 批次边界

- 本批判断的是公开可见的 actor–event role，不判断候选人得票、投票率、选举结果原因或组织活动的选举效果。
- `request`、`endorsement`、`issue_campaign`、`public_meeting`、`observation` 是本包的五类粗粒度动作；不能仅因发生在选举窗口内，就把议题集会、观察学习或政策提案起草改写成候选人支持。
- 临时请求团、竞选女性局、学生项目和混合调整会议可以保留为 event node；本批不据此新增 registry actor、成员边或稳定联盟。
- 媒体所报人数、团体数和组织自报活动规模只保留为来源内陈述，不作为独立验证的规模或影响指标。
- 本批不修改中央 actor registry、事件表、HR CSV、source log、图或报告正文；负责人判断只记录在本回交报告，供主线程以后合并。

## 0A. 实际调查与材料核查

本批逐项打开或检查了 S249–S259。S249、S259 为 PDF，除文字抽取外又对关键页做了页面渲染核查。

### S249 的预告缺口

S249 日本 YWCA 2014 年 7 月通讯写的是 7 月 27 日结成大会“将举行”，自身不能单独证明大会后来实际举行。本轮补到 QAB 2014 年 7 月 27 日当日报道：

- 大会当日在宜野湾市举行；
- 结成 appeal 以实现《建白书》、反对边野古新基地为中心；
- 该报道没有把大会写成候选人 endorsement。

补查来源：  
https://www.qab.co.jp/news/2014072756461.html

因此 R9EC001 的“举行结成大会”事实可以保留，但合并时应给这条 QAB 报道建立 source proposal／source-log linkage，不能继续只让会前预告承担事后事实。

### S259 的页面语义

S259 的活动表明确区分：

- 2018-09-05：参加两名候选人的公开讨论会，之后解释术语、核对疑点并分享感受；
- 2018-09-13：公开 workshop，制作“向知事候选人提出的政策提言案”，来源记载 34 名参加者；
- 2018-09-19：在第三期报纸中公开学习、讨论和政策提言。

所以 9 月 13 日能确认的是 **proposal drafting**，不是已向每名候选人交付、被接收或得到回应。为保持本包五类动作不扩张，可以让它留在粗粒度 `request` 类，但最终 role 和句子必须写成“起草政策提言案”，不能写成“向候选人提出了请求”。

## 1. 辅助建议总表

| item | 记录 | 辅助建议 | 保留／修订内容 | 关键限制 |
|---|---|---|---|---|
| HR026-01 | A059 島ぐるみ会議结成大会 | `accept_with_revision` | 确认举行；`issue_campaign`；crosswalk=A059；使用正式全称 | S249 是预告，需补 QAB 当日报道；明确不是直接知事选目的 |
| HR026-02 | 女性要请团请求翁长参选 | `accept` | `request`；临时请求 collective | “52 团体和个人”不是组织名单；不等于稳定联盟 |
| HR026-03 | ひやみかち うまんちゅの会女性局集会 | `accept` | `endorsement`；campaign event node | 单一党派媒体 E2；29 团体不进入 registry |
| HR026-04 | ゆんたくるー现场学习巴士 | `accept` | `observation`；青年现场学习／同辈对话 | 只有 bounded window，没有精确 tour 日期；不推断选票效果 |
| HR026-05 | 新日本妇人会选后谈话 | `accept_with_revision` | 国家级组织的 `observation`／选后解释 | 不 crosswalk 到 A115；冲绳县本部活动只作为国家组织自报 |
| HR026-06 | All Okinawa 撤回支持紧急集会 | `accept` | `issue_campaign`；支持知事行政行为 | 不是候选 endorsement；不推断选举效果 |
| HR026-07 | 8.11 县民大会 | `accept` | `issue_campaign`；反土砂投入／追悼语境 | 临近选举不改变动作类型；排除人数与效果 |
| HR026-08 | 调整会议请求玉城参选 | `accept` | `request`；temporary mixed event node | 8 月 23 日只确认正式请求，当时尚未确认接受 |
| HR026-09 | #みんなごと公开讨论会与回顾 | `accept` | `public_meeting`；civic-learning role | 候选人匿名；不声称中立性已独立审核 |
| HR026-10 | #みんなごと政策提言 workshop | `accept_with_revision` | 粗类保留 `request`，role=`policy_proposal_drafter` | 只确认起草提言案；不写交付、接受、候选 uptake |

建议分布：

- `accept`：7 项；
- `accept_with_revision`：3 项；
- `reject`／`defer`：0 项。

## 2. HR026-01 · 島ぐるみ会議结成大会

### 调查结果

S249 的关键价值不是事后事件确认，而是由共同代表撰写的组织目的说明：

- 建立由冲绳市民主体参与的长期平台；
- 围绕土地、海空和基地支配问题组织行动；
- 明确写明该组织“并非直接以知事选举为目的”。

QAB 当日报道补足了 S249 的时态缺口，确认 2014 年 7 月 27 日结成大会实际在宜野湾市举行。组织全称与前面 HR-019、HR-025 已确认的 A059 正式单元一致：

> `沖縄「建白書」を実現し未来を拓く島ぐるみ会議`

`島ぐるみ会議` 只作 alias；不得把各市町村的同名／近名组织自动并入 A059。

### 辅助建议

**`accept_with_revision`。**

- `action_type=issue_campaign`；
- `registry_crosswalk=A059`；
- `entity_boundary=Okinawa-wide civic network`；
- publishable wording 可写：

> 2014 年 7 月 27 日，A059 举行结成大会，以实现《建白书》和长期反基地议题为公开平台；组织材料明确说它并非直接以知事选举为目的。

- 给 QAB 2014-07-27 报道建立新增 source linkage；
- 不编为 endorsement、vote mobilization 或翁长后援组织。

## 3. HR026-02 · 女性团体请求翁长雄志参选

### 调查结果

QAB 2014 年 8 月 21 日报道直接点名：

- `てぃんさぐの会`；
- `翁長雄志さんを沖縄県知事に送る女性要請団`；
- 两个团体分别公开请求翁长雄志参加县知事选。

赤旗次日报道称后一个请求团由新日本妇人会、女性 9 条会等“52 个团体和个人”构成，并报道约 150 人到场。这里的“团体和个人”是混合口径，且没有完整 roster，不能拆成 52 个组织 actor。

### 辅助建议

**`accept`。**

- 保留 `action_type=request` 和 2014-08-21 的 day precision；
- actor 保留为 `ad_hoc_event_collective`，不自动进入 registry；
- observable action 只写“公开请求翁长参选”；
- 不把请求等同于翁长接受、正式候选资格、稳定联盟或 52 个组织共同背书。

来源：

- https://www.qab.co.jp/news/2014082157456.html
- https://www.jcp.or.jp/akahata/aik14/2014-08-22/2014082204_01_1.html

## 4. HR026-03 · 女性大集会

### 调查结果

S252 报道 2014 年 10 月 9 日在那霸举行女性大集会，由 `ひやみかち うまんちゅの会 女性局` 主办，公开呼吁翁长胜选，并称 29 个女性团体支持活动。这里有明确的候选胜选诉求，足以与一般 issue campaign 区分。

局限是：

- 只有一条党派媒体来源，证据维持 E2；
- 29 个团体的完整名单未获得；
- `女性局` 是竞选组织内的活动单元，不据此推断为长期独立妇女 NGO。

### 辅助建议

**`accept`。**

- `action_type=endorsement`；
- actor boundary 保持 `candidate_campaign_body`；
- 只接受这一场 2014-10-09 endorsement event；
- 不新增 29 个 actor、不生成成员边或稳定妇女联盟。

来源：  
https://www.jcp.or.jp/akahata/aik14/2014-10-11/2014101104_01_1.html

## 5. HR026-04 · ゆんたくるー青年学习活动

### 调查结果

S253 是参与者／组织方回顾：

- 2014 年 8 月 12 日一次青年 cross-talk 后形成小组；
- 参与者讨论在选举前能做什么；
- 随后以边野古、高江现场学习巴士和同辈对话作为活动方式；
- 页面没有给出 tour 的精确日期。

材料支持“青年观察／学习介入”，但没有支持候选 endorsement、组织中立性审计、参与规模的独立核验或活动对投票的影响。

### 辅助建议

**`accept`。**

- `action_type=observation`；
- `entity_boundary=informal_youth_group`；
- 保留 2014-08-12 至投票前的 bounded window，不造出精确 tour day；
- publishable wording 保持“在知事选前组织现场学习和同辈对话”，不写动员选票或改变投票。

来源：  
https://www.magazine9.jp/article/yuntacrew/18975/

## 6. HR026-05 · 新日本妇人会 2014 年选后谈话

### 调查结果

S254 页面由 **新日本婦人の会中央本部** 发布，正文署名为副会长，网页发布日为 2014-11-21，谈话落款日为 2014-11-19。它可以确认：

- 国家级组织发布了对冲绳县知事选结果的解释；
- 该组织自报冲绳县本部会员和全国会员开展了支持活动。

但 actor registry 的 A115 是 **新日本婦人の会沖縄県本部**，HR-027 已明确国家组织行动不能自动转给县本部。当前 R9EC005 以国家级 `新日本婦人の会` 为 actor 是合理的；不能仅因正文提到冲绳县本部，就把整条谈话 crosswalk 到 A115。

### 辅助建议

**`accept_with_revision`。**

- actor 保持国家级 `新日本婦人の会`，`registry_crosswalk=none`；
- `entity_boundary=organization_outside_registry / national body`；
- `event_date=2014-11-19` 表示谈话落款日；另保留 `web_publication_date=2014-11-21`；
- `action_type=observation`，role 为选后公开解释；
- 对 A115 的活动只写成“国家组织谈话中的自报”，不升级为独立核实的 A115 event role；
- 不使用自报活动证明规模、选举贡献或因果效果。

来源：  
https://www.shinfujin.gr.jp/2943/

## 7. HR026-06 · 埋立承认撤回支持紧急集会

### 调查结果

S256 报道 All Okinawa Council 在翁长知事宣布启动撤回埋立承认程序后，于 2018 年 7 月 27 日在县民广场举行紧急集会，并通过支持撤回的 appeal。

它支持的是对一项现任知事行政行为和边野古政策的公开支持。报道中的参加人数不需要进入正式结论；该事件也不能因为靠近知事选窗口而变成候选人 endorsement。

### 辅助建议

**`accept`。**

- `action_type=issue_campaign`；
- observable action 保持“举行集会并通过支持撤回表明的 appeal”；
- 不编 endorsement，不推断对选举的动员或效果。

来源：  
https://ryukyushimpo.jp/news/entry-770040.html

## 8. HR026-07 · 8.11 县民大会

### 调查结果

S257 是 All Okinawa Council 的活动页，明确给出：

- 2018 年 8 月 11 日；
- 奥武山公园陆上竞技场；
- 反对边野古土砂投入、要求放弃新基地建设；
- 翁长知事逝世后的追悼语境。

组织目的仍然是公开的基地议题活动，页面没有出现对某位后继候选人的支持。

### 辅助建议

**`accept`。**

- `action_type=issue_campaign`；
- role 保持 organizer；
- 可保留“集会兼具追悼语境”，但核心 observable action 是反土砂投入／反新基地议题集会；
- 不写候选 endorsement、参加人数或政治效果。

来源：  
https://all-okinawa.jp/492/

## 9. HR026-08 · 调整会议请求玉城 Denny 参选

### 调查结果

S258 直接说明：

- 该调整会议由县议会执政会派、反对边野古新基地的政党、工会和企业组成；
- 2018 年 8 月 23 日正式决定推举玉城 Denny，并前往其事务所提出参选请求；
- 报道当时写的是玉城预计 8 月 26 日接受请求。

因此 8 月 23 日 event 可以确认“选择并正式请求”，不能在同一 event row 中写成已接受。这个混合会议是特定选举程序的临时协调节点，不是 NGO，也不能仅由这次共同选择推断稳定联盟。

### 辅助建议

**`accept`。**

- `action_type=request`；
- `entity_boundary=temporary_mixed_selection_coalition`；
- publishable wording 保持“选定玉城并正式请求其参选”；
- 8 月 23 日这条不写“玉城已接受”；
- 不进入 NGO registry，不生成政党—工会—企业稳定联盟边。

来源：  
https://ryukyushimpo.jp/news/entry-789039.html

## 10. HR026-09 · #みんなごと公开讨论会与回顾

### 调查结果

S259 活动表记载 2018 年 9 月 5 日：

- 项目成员参加两名候选人的公开讨论会；
- 观察候选政策和人物；
- 会后解释现场术语、核对未理解之处并交流感受。

论文是参与者的学术活动记录，候选人姓名被匿名化，也没有提供对该项目政治中立性的独立审核。

### 辅助建议

**`accept`。**

- `action_type=public_meeting`；
- `entity_boundary=informal_student_civic_project`；
- generic target nodes 保持 `候補者1／候補者2`；
- 只写“观察公开讨论会并开展结构化回顾／澄清”；
- 不写独立中立认证、说服效果、候选 uptake 或投票影响。

来源：  
https://www.jstage.jst.go.jp/article/isvsjapan/19/0/19_45/_pdf/-char/en

## 11. HR026-10 · #みんなごと政策提言案 workshop

### 调查结果

S259 活动表把 2018 年 9 月 13 日写成公开 workshop，并明确使用“知事候选人へ政策提言の案の作成”。它支持：

- 面向公众招募；
- 34 名参加者这一来源内 event count；
- 起草面向候选人的政策提言案。

该页不支持在 9 月 13 日已分别向候选人交付、候选人接受或产生回应。9 月 19 日的报纸公开是下一条 R9EC011 的事件，不应提前并入本条。

### 辅助建议

**`accept_with_revision`。**

- 为保持既有五类粗动作，`action_type` 可继续放在 `request`；
- 必须保留 `role_label=policy_proposal_drafter`；
- 最终句子写“举行公开 workshop，起草面向候选人的政策提言案”；
- interpretation limit 增加：

> `request is a coarse aggregation class only; drafting confirmed; delivery, receipt, response and candidate uptake not established`

- 34 人只作 source-reported event count，不用于 reach／effect；
- 不与 R9EC011 的 9 月 19 日公开活动合并。

## 12. 建议负责人本批判断

建议一次确认以下 10 项：

1. HR026-01：`accept_with_revision`；
2. HR026-02：`accept`；
3. HR026-03：`accept`；
4. HR026-04：`accept`；
5. HR026-05：`accept_with_revision`；
6. HR026-06：`accept`；
7. HR026-07：`accept`；
8. HR026-08：`accept`；
9. HR026-09：`accept`；
10. HR026-10：`accept_with_revision`。

如负责人确认，主线程后续合并时：

- 把判断回填 HR-026，但不把选举接口改写成选举效果；
- R9EC001 补入 QAB 当日报道的 source proposal／linkage；
- R9EC001 crosswalk 到 A059，并使用此前人工确认的正式全称；
- R9EC005 保持国家级组织，不 crosswalk 到 A115；
- R9EC010 保留五类动作中的粗粒度 `request`，但以 proposal drafting 作为正式 role 和可发表措辞；
- 临时 collective、campaign body、学生项目与混合调整会议仍为 event node，不自动进入 actor registry。

## 13. 负责人确认

负责人于 2026-07-20 确认本批判断：

- `accept`：HR026-02、HR026-03、HR026-04、HR026-06、HR026-07、HR026-08、HR026-09；
- `accept_with_revision`：HR026-01、HR026-05、HR026-10；
- `reject`／`defer`：0 项。

本报告作为 10 项人工决定的回交记录。中央 actor registry、事件表、HR CSV、source log、图与报告正文仍不在本批修改，留待主线程统一合并。
