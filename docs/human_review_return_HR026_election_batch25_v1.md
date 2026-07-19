# HR-026 县知事选—市民组织接口回交报告 Batch 25

日期：2026-07-20  
承办人：项目负责人  
辅助调查：Codex  
来源队列：`outputs/R09_election_civic_interface_v1/HR026_election_civic_role_review_v0.csv`  
本批范围：HR026-11–19（2018 年 2 项、2022 年 7 项）  
状态：**负责人已确认——2 项 accept，7 项 accept_with_revision；HR-026 完成**

## 0. 批次边界

- 本批复核公开可见的组织／临时集体—选举事件角色，不判断得票、投票率、选举胜负原因或活动效果。
- `endorsement`、`issue_campaign`、`public_meeting`、`request`、`observation` 继续作为五类粗粒度动作，不为单条记录扩张 taxonomy。
- 组织自报的接入点、参加者、全国行动和宣传范围不等于人数、选民触达、说服或选举效果。
- 国家组织与冲绳县本部是不同 actor 单元；不得把新日本妇人会中央本部的选举行动自动转给 A115。
- 具名个人参加临时委员会，不把委员会角色转给个人所属组织。
- 活动预告与活动已发生必须分开；没有会后材料时不能把“将举行”写成“已经举行”。
- 本轮只做线上调查，不启动当地资料／地方数据库任务。
- 本报告不修改中央 actor registry、候选事件表、HR CSV、source log、图或正文，留待主线程统一合并。

## 0A. 本轮实际调查所得

### PDF 页面核查

S259 与 S260 均完成文字和页面级核查：

- S259 活动表把 2018-09-12 的候选政策比较和 2018-09-19 的政策提言公开列为两次不同报纸发行；
- S260 的署名块明确是 `新日本婦人の会　中央常任委員会`，不是冲绳县本部 A115。

### 7 月 30 日县民大会的分类争议

All Okinawa Council 原始页面和声明全文只出现：

- 支持边野古设计变更不承认；
- 反对遗骨混入土砂开采；
- PFAS、基地事件事故、生活安全；
- 人权、自治权和反新基地诉求；
- 声明对象是日本政府与美国方面。

原始声明没有出现“支持玉城连任”或请求投票。冲绳时报报道的标题／摘要则记录：

- 县政与党评价为“知事选前很好的发信”；
- 在野党评价为“不是县民大会，而是决起集会”。

另有支持方团体事后把大会评价为知事选“事实上的起点”。这些都证明大会存在明显的 election-adjacent political reception，但属于政治主体对事件功能的竞争性解释，不能替代主办方可观察到的公开行动内容。

### 两项线上检索耗尽

1. HR026-18：S267 是 2022-09-07 的会前报道，只说 9 月 8 日、10 日“将举行”两场 talk。本轮用委员会全称、日期、会场 Punga Ponga、登坛者和 YouTube 等组合检索，没有找到录像、会后报道或组织存档。因此只能确认 announced／scheduled role，不能确认两场均实际举行。
2. HR026-19：以活动标题、日期、人物和可能的女性团体名称多轮检索，仍只有赤旗的单篇 E2 报道；没有找到可核实的主办组织名。endorsement event 可以保留，但不能把“女性集会”制造成组织 actor。

两项均记为 `online_exhausted`；本轮不转当地资料任务。

## 1. 辅助建议总表

| item | 记录 | 辅助建议 | 修订重点 | 核心限制 |
|---|---|---|---|---|
| HR026-11 | #みんなごと报纸企划 | `accept_with_revision` | 日期改为 9/12–9/19：先比较候选政策，再公开政策提言 | 不声称阅读量、中立性认证、说服或效果 |
| HR026-12 | 新日本妇人会 2018 选后声明 | `accept_with_revision` | 国家组织；署名中央常任委员会；不 crosswalk A115 | 组织自报全国行动不证明规模或因果 |
| HR026-13 | 女性团体有志请求玉城参选 | `accept` | `request`；具名 ad hoc collective | 玉城当时只说考虑；不推断成员名单或持续性 |
| HR026-14 | 全日本民医连线上支持集会 | `accept` | 国家组织 `endorsement` | 436 个接入点不是人数、选民或效果 |
| HR026-15 | All Okinawa 7.30 县民大会 | `accept_with_revision` | 保留 `issue_campaign`，增加 election-adjacent contested reception | 原始声明无连任号召；政治评价不等于组织目的 |
| HR026-16 | 新日本妇人会 2022 支持号召 | `accept_with_revision` | 国家组织的明确 endorsement；不 crosswalk A115 | 全国声援、扩散与募金号召不证明执行或效果 |
| HR026-17 | 2022 候选人问卷 | `accept_with_revision` | 确认问卷实施和基于结果的活动；删去“完整答卷已公开”暗示 | 原始答卷未找到；个人角色不转移给 A051 等组织 |
| HR026-18 | 基于问卷的两场 talk | `accept_with_revision` | 改成 announced／scheduled public meetings；不写 held | 无会后证据；不进入已举行事件计数 |
| HR026-19 | 8.13 女性支持集会 | `accept_with_revision` | 接受 event-level endorsement；主办方保持 unidentified | 不作为 actor、不进入组织数或稳定妇女联盟 |

建议分布：

- `accept`：2 项；
- `accept_with_revision`：7 项；
- `reject`／当地资料 defer：0 项。

## 2. HR026-11 · #みんなごと报纸企划

### 调查结果

S259 活动表明确列出：

- 2018-09-12：报纸企划第二期，总结两名候选人的政策差异和青年关注议题上的意见差异；
- 2018-09-19：报纸企划第三期，总结此前学习／讨论过程并发表项目政策提言。

当前 R9EC011 只使用 9 月 19 日，却把“候选政策比较”和“政策提言公开”合成同一天，时序不准确。

### 辅助建议

**`accept_with_revision`。**

- 保留一个 row 时，改为：
  - `event_date_start=2018-09-12`；
  - `event_date_end=2018-09-19`；
  - `date_precision=day_range`；
- `action_type=observation`；
- observable wording：

> 9 月 12 日公开候选政策比较，9 月 19 日公开此前学习过程和项目政策提言。

- 不把论文作者关于“中立性”的自我评价写成独立审核结论；
- 不推断读者数量、SNS reach、候选吸收或投票效果。

来源：  
https://www.jstage.jst.go.jp/article/isvsjapan/19/0/19_45/_pdf/-char/en

## 3. HR026-12 · 新日本妇人会 2018 年选后声明

### 调查结果

S260 是一页正式声明，标题为冲绳县知事选历史性胜利与立即停止新基地建设，日期 2018-10-03。页面署名明确是：

> `新日本婦人の会　中央常任委員会`

声明由国家组织解释选举结果，并自报“县内以及全国”围绕玉城胜选开展了行动。它没有把该声明署名给冲绳县本部，也没有独立证明行动规模或对票数的作用。

### 辅助建议

**`accept_with_revision`。**

- actor 保持国家级 `新日本婦人の会`；
- issuer unit 记录为 `中央常任委員会`；
- `registry_crosswalk=none`，不 crosswalk 到 A115；
- `action_type=observation`，role=`post_result_interpreter`；
- 组织自报的县内／全国行动只放在 notes，不作为规模或效果结论；
- 不复述声明中的得票、群体投票比例等数字，正式选举数字如需使用应回官方选举记录。

来源：  
https://www.shinfujin.gr.jp/wp-content/uploads/2018/11/20181003_seimei_okinawatidisen.pdf

## 4. HR026-13 · 女性团体有志请求玉城参选

### 调查结果

琉球新报 2022-04-09 当日报道：

- `沖縄の輝く未来をつくる女性たちの会` 由支持玉城县政的女性团体有志等组成；
- 代表为狩俣信子；
- 当日在那霸市教育福祉会馆举行集会并请求玉城参加连任选举；
- 玉城当时回应为会认真考虑，并非当场接受。

另有参加者个人记录使用同一全称，说明宫古岛的 `市民ネット結` 人员以个人／所属团体背景参加。该记录可交叉确认名称和活动，但不能据此生成成员边。除本次请求外，没有找到可确认组织连续性的后续材料。

### 辅助建议

**`accept`。**

- `action_type=request`；
- actor boundary 保持 `ad_hoc_event_collective`；
- observable action 写“举行集会并请求玉城参加连任”；
- 不写玉城当场接受；
- 不新增 registry actor、不重建成员 roster，也不把参与者个人角色转给其所属组织。

来源：

- https://ryukyushimpo.jp/news/entry-1499534.html
- https://mjaku-note.hatenablog.com/entry/allokinawa001

## 5. HR026-14 · 全日本民医连线上支持集会

### 调查结果

全日本民医连官方活动报道确认：

- 2022-07-29 由全日本民医连举办全国线上集会；
- 标题和发言明确要求玉城胜选／连任；
- 冲绳民医连负责人、全日本民医连负责人及多地参加者发言；
- 页面自报“全国 436 个接入点”。

这是明确 endorsement，不只是健康议题说明或一般冲绳 solidarity。主办 actor 是国家级全日本民医连，不是由参加者名单推导出的临时联盟。

### 辅助建议

**`accept`。**

- actor=`全日本民主医療機関連合会`；
- `entity_boundary=organization_outside_registry / national federation`；
- `action_type=endorsement`；
- event date 使用 2022-07-29，网页 2022-08-16 是报道日期；
- “436”只能写作组织自报 access points，不等于 436 人、436 名选民或 436 个独立组织；
- 不推断触达、说服、投票或因果效果。

来源：  
https://www.min-iren.gr.jp/news-press/shinbun/20220816_46093.html

## 6. HR026-15 · All Okinawa 7 月 30 日县民大会

### 调查结果

主办方原始页面的标题、声明和对象均是基地议题：

- 设计变更不承认；
- 遗骨混入土砂；
- PFAS 污染；
- 基地事件事故、噪音、生活安全；
- 人权、自治权和反新基地；
- 声明送交日本政府、美国总统和驻日美国大使等。

玉城以现任知事身份登坛，并处在连任选举前。冲绳时报记录县政与党和在野党对大会选举功能的相反评价；其他支持团体也把它评价为选举启动节点。但是，主办方正式声明没有连任、投票或候选支持号召。

### 辅助建议

**`accept_with_revision`。**

- 保留 `action_type=issue_campaign`；
- channel=`online_prefectural_assembly`；
- observable wording：

> All Okinawa Council 举行线上议题大会，支持边野古设计变更不承认，并公开连接遗骨土砂、PFAS、基地生活安全、人权与自治问题。

- interpretation limit 增加：

> `organizer-framed issue campaign in an election-adjacent context; political actors disputed whether it functioned as an election rally; no explicit candidate endorsement in the official statement`

- 不写“完全与选举无关”，也不升级为 endorsement；
- 不把玉城登坛等同于组织对其连任的正式背书。

来源：

- https://all-okinawa.jp/2005/
- https://www.okinawatimes.co.jp/articles/-/1000372

## 7. HR026-16 · 新日本妇人会 2022 年支持号召

### 调查结果

来源页面标题和站点抬头明确属于 `新日本婦人の会中央本部`。正文直接写：

- 玉城 Denny 连任；
- 全国声援；
- 向冲绳亲友呼吁；
- SNS 扩散；
- 以“冲绳支援”名义募金。

因此 endorsement 事实非常明确，但 actor 仍是国家组织，不能转给 A115。募金号召也不能在没有收款／用途记录时变成资金流边。

### 辅助建议

**`accept_with_revision`。**

- actor 保持国家级 `新日本婦人の会`；
- `registry_crosswalk=none`，不 crosswalk A115；
- `action_type=endorsement`；
- observable wording 保留“公开要求玉城连任并号召全国声援／扩散”；
- 募金只记作公开 campaign call，不生成金额、recipient relation 或运动资金事实；
- 不推断受众触达、响应、选票或效果。

来源：  
https://www.shinfujin.gr.jp/up/newspaper/12908/

## 8. HR026-17 · 三名候选人问卷

### 调查结果

琉球新报 2022-09-07 报道以既成事实写明：

- 实行委员会在 8 月对佐喜真淳、下地幹郎、玉城 Denny 三名候选人实施问卷；
- 问卷包含气候变化／能源、PFAS、性少数等 26 个主题、74 问；
- 委员会计划以问卷结果为基础讨论知事选争点和领导者资质。

报道点名具志堅隆松、元山仁士郎等个人参加委员会。元山的历史身份涉及 A051，但这不表示 A051 作为组织实施了本次问卷。原始问题／完整答卷页面仍未找到。

### 辅助建议

**`accept_with_revision`。**

- `action_type=observation`；
- actor 保持具名 `ad_hoc_event_collective`；
- observable wording修为：

> 委员会在 2022 年 8 月对三名候选人实施 26 主题、74 问的问卷，并宣布将以结果为基础开展争点讨论。

- 删除“完整答卷已作为公共信息公开”的暗示；
- 原始答卷未取得时，不比较候选回答、不做立场编码；
- 个人参加不向 A051、ガマフヤー或其他所属组织转移角色；
- 问卷覆盖所有三名候选人不自动证明委员会政治中立性经过独立审核。

来源：  
https://ryukyushimpo.jp/news/entry-1579341.html

## 9. HR026-18 · 基于问卷的两场 talk

### 调查结果

同一篇 2022-09-07 报道只写：

- 9 月 8 日和 10 日“将举行”线上 talk；
- 10 日另在 Punga Ponga 设置先到 10 人的线下席位；
- 活动计划以三名候选人的问卷结果为基础讨论争点和领导者资质。

它是活动预告，不是会后报道。本轮没有找到能确认两场均实际举行的录像、会后文章或组织记录。

### 辅助建议

**`accept_with_revision`。**

- 保留为 `announced_public_meeting_series`，不作为 confirmed-held event；
- 粗粒度 `action_type=public_meeting` 可以保留，但必须增加 `event_status=announced_not_occurrence_verified`；
- observable wording 改为：

> 委员会宣布将在 9 月 8 日和 10 日举行两场基于候选问卷结果的公共 talk。

- 从“已举行 public meeting”数量、正式 AEV 和事件参与计数中排除；
- 以后若取得录像／会后记录，可由新证据升级为 held；
- `online_exhausted`，不转本轮当地资料任务。

来源：  
https://ryukyushimpo.jp/news/entry-1579341.html

## 10. HR026-19 · 8 月 13 日女性支持集会

### 调查结果

赤旗 2022-08-14 报道明确确认：

- 8 月 13 日那霸市内举行女性集会并在线配信；
- 活动明确号召玉城连任；
- 议题包括边野古、生活、福利、儿童贫困与 LGBTQ；
- 报道点名若干发言者和政治人物。

但页面没有主办方名称。多轮搜索仍未找到 flyer、活动页、录像说明或其他报道来识别 organizer。`女性集会` 是事件描述，不是组织名称。

### 辅助建议

**`accept_with_revision`。**

- 接受 2022-08-13 的 event-level endorsement；
- actor 字段改成 `主催者未確認` 或等价缺失值，不把 `女性集会` 当 canonical actor；
- `entity_boundary=unidentified_organizer_event_record`；
- 不进入 actor registry、组织数量、组织网络或稳定妇女联盟；
- 不把到场发言者自动认定为主办者／成员；
- 证据维持 E2 single party-media；
- `online_exhausted`，不转本轮当地资料任务。

来源：  
https://www.jcp.or.jp/akahata/aik22/2022-08-14/2022081403_01_0.html

## 11. 建议负责人本批判断

建议一次确认：

1. HR026-11：`accept_with_revision`；
2. HR026-12：`accept_with_revision`；
3. HR026-13：`accept`；
4. HR026-14：`accept`；
5. HR026-15：`accept_with_revision`；
6. HR026-16：`accept_with_revision`；
7. HR026-17：`accept_with_revision`；
8. HR026-18：`accept_with_revision`；
9. HR026-19：`accept_with_revision`。

如负责人确认，主线程后续合并时：

- R9EC011 使用 9 月 12–19 日的 day range，保留政策比较与提言公开的先后顺序；
- R9EC012、R9EC016 作为国家级新日本妇人会行动，不 crosswalk A115；
- R9EC015 保留 `issue_campaign` 并显式记录争议性选举语境；
- R9EC017 只确认问卷实施及基于结果的活动计划，不暗示完整答卷已经取得；
- R9EC018 改为 announced event，排除出已举行事件计数；
- R9EC019 只保留 endorsement event，主办方保持 unidentified，不计算为组织 actor。

## 12. 负责人确认

负责人于 2026-07-20 确认本批判断：

- `accept`：HR026-13、HR026-14；
- `accept_with_revision`：HR026-11、HR026-12、HR026-15、HR026-16、HR026-17、HR026-18、HR026-19；
- `reject`／当地资料 defer：0 项。

连同 Batch 24，HR-026 共 19 项已经全部由负责人判断：

- `accept`：9 项；
- `accept_with_revision`：10 项；
- `reject`／`defer`：0 项。

本报告作为后 9 项人工决定及 HR-026 完成状态的回交记录。中央 actor registry、候选事件表、HR CSV、source log、图与正文仍留待主线程统一合并。
