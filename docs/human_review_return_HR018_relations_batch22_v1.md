# HR-018 行政协作／支持关系回交报告 Batch 22

日期：2026-07-20  
承办人：项目负责人  
辅助核查：Codex  
来源队列：`outputs/R10_administrative_collaboration_v0/HR018_relation_review_v0.csv`  
本批范围：HR-018-25–26  
状态：**负责人已确认——2 项 revise；HR-018 线上部分完成**

## 0. 批次边界

- 本批处理 HR-018 最后两条在线可调查的实物支持关系。
- 两条记录都可以确认有界事件事实，但现有字段混入了尚未被来源证明的年份或 recipient identity。
- DVIDS／军方公共事务来源可以支持有界事件事实，证据层级保持 E3。
- 现行组织官网和市政府名单只用于主体名称、服务范围或 locator 候选核查，不能反向补强历史事件细节。
- 实物支持不等于现金资助；共同交付不等于每个参与方分别捐赠全部物品。
- 服务于美军社区的童军组织不据此编码为亲基地或反基地。
- 本报告不直接修改中央 relation 表、funding/support 表、source log、HR CSV、图或 brief。

## 0A. 本轮调查结果

| 项目 | 核查材料 | 本轮调查所得 |
|---|---|---|
| HR-018-25 | S072／DVIDS 2012 AWWA 四十周年报道；Far East Council 和 Scouting America 现行官网 | S072 明确说 AWWA 曾帮助 Boy Scouts of America Far East Council 获得皮划艇，但没有给出事件日期、皮划艇数量、金额或 AWWA 承担份额。2012-04-23 是报道所述纪念宴会／报道日期，不是来源明确写出的皮划艇交付日期。现行正式名称为 `Far East Council, Scouting America`，其 Guiding Compass District 服务范围明确包括 Okinawa。 |
| HR-018-26 | S102／DVIDS 2025 共同捐赠报道；うるま市现行学童クラブ名单 | S102 明确确认四个贡献团体于 2025-08-15 向平敷屋地区一个课后托育中心交付三台工业冷风机。报道没有点名 recipient 的正式名称，也没有金额或四方份额。うるま市现行名单在平敷屋小校区只列 `きむたかこどもセンター学童クラブ`，但现行名单与地理相符仍不足以确认它就是 2025 年受赠机构。 |

## 1. 辅助建议总表

| review item | relation | 辅助建议 | 可批准的最强口径 | 必须保留的边界 |
|---|---|---|---|---|
| HR-018-25 | AWWA→Far East Council | `revise` | AWWA 曾帮助当时的 Boy Scouts of America Far East Council 获得皮划艇 | 事件日期不明；2012 只是报道时点；不补数量、金额、份额或冲绳专属配置 |
| HR-018-26 | NOSCO→平敷屋课后托育中心 | `revise` | NOSCO 是 2025-08-15 三台工业冷风机共同交付事件的四个贡献团体之一 | recipient 正式名称未确认；不把三台设备或全部价值归给 NOSCO |

建议分布：

- `accept`：0 条；
- `revise`：2 条；
- `reject`：0 条。

## 2. HR-018-25 · AWWA→Far East Council

S072 是 2012 年 AWWA 四十周年纪念报道。关于皮划艇，来源只提供三项直接事实：

1. AWWA 曾帮助 `Boy Scouts of America Far East Council` 获得皮划艇；
2. 信息由当时的 Far East Council district executive Dan Richard 提供；
3. 皮划艇使童军有机会完成 Kayak Merit Badge。

来源使用的是回顾性措辞 `In one situation` 和 `helped ... to acquire kayaks`。它没有说明：

- 事件发生在 2012 年；
- AWWA 是否独自购买或直接交付全部皮划艇；
- 皮划艇数量；
- 物品价值或现金金额；
- 是否只供 Okinawa 地区使用；
- 是否存在连续、年度性支持关系。

因此，现有 `fiscal_year=2012` 和“皮划艇捐赠”都比来源更强。最准确的关系语义应从确定的 `donated kayaks` 降为：

> AWWA helped the Boy Scouts of America Far East Council acquire kayaks.

Far East Council 现行官网将自身列为 `Scouting America — Far East Council`，并把 Okinawa 列在 Guiding Compass District 的服务范围。Scouting America 官网也列出 `Far East Council, Scouting America` 作为向亚太地区美国境外成员提供服务的 council。

这可以解决 recipient identity 和组织性质，但不能回填历史事件日期。历史名称与现行名称应同时保留：

- historical event label：`Boy Scouts of America Far East Council`；
- current canonical label：`Far East Council, Scouting America`；
- recipient class：`overseas Scouting council serving U.S.-affiliated communities, including Okinawa`；
- 不归入 `Okinawa-local welfare recipient`。

### 辅助建议

**`revise`。**

建议字段：

- relation type：`in_kind_acquisition_assistance`；
- item：`kayaks`；
- event date／fiscal year：空；
- reported at：`2012-04-23`；
- event label：`AWWA helped Far East Council acquire kayaks; date and quantity unstated`；
- amount semantics：`no_amount_no_quantity_no_share_allocation`；
- evidence：E3；
- recipient identity crosswalk：现行官网可支持 E4 名称／服务范围核查，但不升级事件本身。

不得写成：

- AWWA 在 2012 年捐赠皮划艇；
- AWWA 独自承担全部物品；
- 这是对冲绳本地福利组织的捐赠；
- 单次协助构成稳定资助关系或政治联盟。

## 3. HR-018-26 · NOSCO→平敷屋地区课后托育中心

S102 明确给出事件日期 `2025-08-15`、物品 `three industrial cooling fans`，并点名四个贡献团体：

1. Commander, Fleet Activities Okinawa personnel；
2. Patrol Squadron (VP) 9 “Golden Eagles”；
3. CFAO Chief Petty Officers’ Association；
4. Naval Officers’ Spouses’ Club of Okinawa。

报道把事件写为 CFAO community relations activity，并说明 recipient 是 White Beach Naval Facility 附近、平敷屋地区的一所 after-school childcare center。它没有提供：

- recipient 的日文正式名称；
- recipient 的法人／运营主体；
- 设备金额；
- 四个贡献团体各自的现金、采购或实物份额；
- NOSCO 是否交付了其中某一台特定设备。

报道后文另称一名参与者代表 `VP-9 First Class Petty Officer Association` 作出贡献。这是 VP-9 内部贡献说明；在没有更完整账目时，不应擅自把报道开头的“四个贡献团体”改写成五个同层级 donor。

うるま市 2026-07-13 更新的学童クラブ页面，在 `平敷屋小` 校区只列一所公设机构：

> きむたかこどもセンター学童クラブ

这使它成为合理的 locator candidate，但仍有时间与身份链缺口：

- 市名单是 2026 年现行名单；
- 捐赠事件发生于 2025 年；
- S102 只说“平敷屋地区、White Beach 附近”，没有写 `平敷屋小` 校区；
- 没有直接来源把 S102 的 recipient 与该正式名称连起来。

因此不能把当前地理候选直接冻结为事件 recipient。

### 辅助建议

**`revise`。**

建议字段：

- target display：`平敷屋地区の放課後児童クラブ（正式名称未確認）`；
- target identity status：`provisional_descriptive_recipient`；
- possible locator candidate：`きむたかこどもセンター学童クラブ`；
- locator approval：`no`；
- event date：`2025-08-15`；
- relation type：`joint_in_kind_contribution`；
- NOSCO role：`one_of_four_named_contributing_groups`；
- item：`three industrial cooling fans at event level`；
- amount／share：`no_amount_no_contributor_share_allocation`；
- evidence：E3。

安全措辞：

> NOSCO 是 2025 年 8 月 15 日向平敷屋地区一所正式名称未确认的课后托育中心共同交付三台工业冷风机的四个点名贡献团体之一。

不得写成：

- NOSCO 单独捐赠三台设备；
- 四个团体各捐赠一台或平均承担费用；
- recipient 已确认是 `きむたかこどもセンター学童クラブ`；
- 此次 COMREL 事件证明稳定组织联盟或政治立场。

## 4. HR-018 在线部分总账

在负责人确认本批建议后，HR-018 的 26 个 review item 可形成以下总账：

| 状态 | 数量 | item |
|---|---:|---|
| `accept` | 16 | HR-018-01–10，以及 12、14–18 |
| `revise` | 8 | HR-018-11、13、19、20、23、24，以及本批建议的 25、26 |
| `deferred_local_or_internal_record` | 2 | HR-018-21、22 |
| `reject` | 0 | 无 |

按具体编号展开：

- `accept`：01–10、12、14–18；
- `revise`：11、13、19、20、23–26；
- `deferred`：21、22。

上述统计中的 25、26 目前仍是 AI 辅助建议，必须在负责人确认后才成立。其余 24 项沿用 Batch 19–21 的负责人判断。

如果本批确认：

- HR-018 的全部在线可处理项即告完成；
- 21、22 继续留在当地／内部记录队列，不阻塞线上 review 收口；
- 总账只作为人工复核回交记录，不代表中央数据已经合并；
- 后续主线程可按各批确认记录统一回填 HR CSV、中央 relation/support 表，再重生 R10 图和 brief。

## 5. 本批证据入口

- S072／DVIDS：<https://www.dvidshub.net/news/87854/american-womens-welfare-association-celebrates-40-years>
- Far East Council 官方简介：<https://www.fareastcouncil.org/far-east-council-home/about-the-far-east-council>
- Scouting America 海外 council 页面：<https://www.scouting.org/international/resources/22-333/>
- S102／DVIDS：<https://www.dvidshub.net/news/546868/us-navy-sailors-help-okinawan-childcare-center-beat-heat>
- うるま市学童クラブ名单：<https://www.city.uruma.lg.jp/1005002000/contents/11212.html>

## 6. 负责人确认记录

负责人于 2026-07-20 确认本批两项辅助建议：

1. HR-018-25：`revise`。保留“AWWA 帮助 Far East Council 获得皮划艇”，删除确定的 2012 事件年份，使用历史名＋现行名 crosswalk；数量、金额、份额和冲绳专属配置均不补写。
2. HR-018-26：`revise`。确认 NOSCO 是四个点名贡献团体之一，但 recipient 继续保留正式名称未确认；`きむたかこどもセンター学童クラブ` 只作未批准 locator candidate，不把三台设备或全部价值归给 NOSCO。

HR-018 最终回交总账：

- `accept`：16 项；
- `revise`：8 项；
- `deferred_local_or_internal_record`：2 项（HR-018-21、22）；
- `reject`：0 项。

至此，HR-018 全部在线可处理项完成。上述结果仅写入人工复核回交报告；本批未修改中央 relation 表、funding/support 表、source log、HR CSV、图或 brief，留待主线程统一合并。
