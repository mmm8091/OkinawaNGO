# HR-016 先岛框架语义与 locator 复核回交报告 Batch 35A

日期：2026-07-20  
承办人：项目负责人  
辅助调查：Codex  
来源队列：`outputs/R04_sakishima_frame_corpus_v0/hr016_review_items_v0.csv`  
本批范围：HR016-001、006、007、008、009、012，共 6 项  
状态：**负责人已确认——1 项 `accept`、5 项 `revise`**

## 0. 批次边界

- 本批处理可由单一来源独立确认的组织边界、地点层级、speaker 和 locator。
- 训练、预案和说明会是制度事件，不等于实际撤离能力、程序公平或居民同意。
- 新闻中的集会名称／执行委员会不自动成为持续组织或 registry actor。
- 行政机关对陈情的处理方针不能替代陈情者原文，也不能反向赋给某一候选组织。
- 本报告不修改 HR CSV、正式事实表、registry、图或正文，留待主线程统一合并。

## 1. 辅助建议总表

| review_item_id | 辅助建议 | 结论 |
|---|---|---|
| HR016-001 | `revise` | 只保留 2016 年具名集会执行委员会，不 crosswalk 到 A012 |
| HR016-006 | `revise` | R4E024 改为 MOD_JAPAN 的 F_FTE 说明会事件，删除 F_PROC |
| HR016-007 | `revise` | R4E025 改为 place=Sakishima 的县级区域观察，不计为与那国特有事实 |
| HR016-008 | `revise` | p.6 是环境部长宣读的行政处理方针，不是陈情者原文，不回指 A013 |
| HR016-009 | `accept` | Pattern 1 稳定印刷页码已定位为 pp.27–29，可加入 R4S007／R4E007 source_ref |
| HR016-012 | `revise` | R4S024 只保留 F_FTE source scope，拒绝 procedural_fairness |

## 2. HR016-001 · 2016 集会执行委员会不能并入 A012

### 调查结果

琉球新报原文写的是：

> 「宮古島いのちの水を守ろう！　６・１１自衛隊配備を止める市民集会」
> （同実行委員会主催）

并具名执行委员会委员长岸本邦弘。报道所证明的是：

- 2016 年 6 月 11 日存在一次具体市民集会；
- 该集会由与完整集会名称对应的执行委员会主办；
- 集会把反对陆自部署与地下水源保护连接起来；
- 执行委员会次日计划在防卫局说明会会场周边进行无声抗议。

A012 当前 canonical name 仅为 `宮古島いのちの水を守ろう！`，唯一 source_ref 也是 S020，
registry notes 已写明“需要确切全名和连续性”。进一步在线检索只找到同一集会的活动预告和报道，
没有找到该简称作为独立持续组织的章程、自有页面、其他年度活动或明确自称。

因此，活动标题的前半句不能机械截取为持续 actor 名；执行委员会也不能仅凭一次报道与 A012
建立身份同一。

### 辅助建议

**`revise`。**

- R4E001 entity 改为一次性 provisional event committee：
  `PROV_R4_611_EXECUTIVE_COMMITTEE`；
- display name 使用
  `「宮古島いのちの水を守ろう！ 6・11自衛隊配備を止める市民集会」実行委員会`；
- 只保留 2016 集会层级的 F_GW／groundwater-life-safety 观察；
- 不 crosswalk 到 A012，不由本项确认 A012 的持续身份；
- A012 继续保持 `needs_second_source / needs_local_retrieval`，等待独立 registry 处理；
- 不把约 100 名参加者写成委员会成员或宫古全体居民立场。

来源：

- https://ryukyushimpo.jp/news/entry-296563.html
- https://miyakojima.net/event/evcal.cgi?mode=past&year=2016

## 3. HR016-006 · 与那国说明会是 F_FTE 制度事件，不是 F_PROC

### 调查结果

防卫省 2026 年 2 月 20 日公告直接证明：

- 防卫省计划于 2026 年 3 月 2 日在与那国町举办住民说明会；
- 主题是向与那国驻屯地部署中距离地对空导弹部队；
- 防卫省将目的表述为“增进与那国町居民的理解”；
- 参加对象限定为与那国町民，并列出会场行为限制。

公告没有居民发言、问答、参加人数、反对／赞成评价、信息充分性或程序公平评价。“增进理解”是
举办方宣称的目的，不是居民已经理解、同意或认可程序的证据。

### 辅助建议

**`revise`。**

- R4E024 actor 保持 `MOD_JAPAN / 防衛省`；
- event 保持 `中距离地对空导弹部队住民说明会`；
- frame 从 `F_PROC` 修订为 `F_FTE`；
- place 保持 Yonaguni；
- fact text 限定为“防卫省公告举办说明会并自述以增进町民理解为目的”；
- 删除 procedural_fairness，不推断居民同意、程序质量或实际沟通效果。

来源：

- https://www.mod.go.jp/j/press/news/2026/02/20c.html
- https://www.mod.go.jp/j/press/news/2026/02/20c.pdf

## 4. HR016-007 · 先岛五市町村训练只能编码为区域级观察

### 调查结果

冲绳县官方“令和 6 年度国民保护共同图上训练实施结果”明确列出参加市町村：

- 宫古岛市；
- 多良间村；
- 石垣市；
- 竹富町；
- 与那国町。

页面把训练对象概括为先岛诸岛的居民避难，并把“运输能力最大化／具体化”和“要照护者避难”列为
重点课题。它是冲绳县和多机关共同开展的先岛区域训练，不是与那国单独观察。

### 辅助建议

**`revise`。**

- R4E025 actor 保持 `GOV_OKINAWA_PREF / 沖縄県`；
- place 从 Yonaguni 修订为 `Sakishima`；
- frame 保持 `F_LIFE / life_safety`，并可在说明中附带区域撤离制度背景；
- fact text 限定为县级训练把运输能力与要照护者避难列为先岛区域重点课题；
- 不增加与那国专属事实、专属计数或地方立场；
- 五市町村参加训练不等于五地对方案内容形成政治同意。

来源：

- https://www.pref.okinawa.lg.jp/bosaianzen/kokuminhogo/1023175/1026163/1032696/1032939.html
- https://www.pref.okinawa.lg.jp/_res/projects/default_project/_page_/001/032/695/r6kunrengaiyou.pdf

## 5. HR016-008 · 地下水段落是县环境部行政处理方针

### 调查结果

该 PDF 是 2019 年 3 月 19 日冲绳县议会土木环境委员会记录。文书结构明确：

1. 委员长要求环境部长说明环境部所管陈情；
2. 环境部长大浜浩志说明将依据“请愿・陈情案件资料”宣读处理方针；
3. 在“陳情平成29年第32号の2 陸自ミサイル部隊の配備に関する陳情”处，环境部长说明：
   - 县和宫古岛市正在进行地下水调查；
   - 当时未检出异常值；
   - 县将继续与市协作关注地下水环境保护；
   - 千代田陆自基地已开工，不属于县环境影响评价条例对象；
   - 县认为冲绳防卫局有必要兼顾环境并争取当地理解。

这些文字是环境部长代表县环境部宣读的行政处理方针。当前 PDF 没有展示陈情者原文，也没有在该段
具名 A013。

### 辅助建议

**`revise`。**

- R4S002 speaker／source role 改为
  `Okinawa Prefecture Environment Department government response`；
- locator 使用 PDF 印刷 p.6，委员会记录第 165–175 行对应段；
- 只作为部署相关地下水监测与县行政回应的背景来源；
- 不恢复 R4E002，不回指 A013，不把行政措辞写成陈情者或民间组织立场；
- 若要确认 A013，仍需独立取得具名陈情原文或组织自有声明。

来源：

- https://www.pref.okinawa.jp/_res/projects/default_project/_page_/001/016/966/doboku310319.pdf

## 6. HR016-009 · Pattern 1 的稳定印刷页码已补齐

### 调查结果

宫古岛市《避難実施要領のパターン》PDF 共 96 个文件页，正文具有稳定印刷页码。Pattern 1 的关键
定位为：

- 印刷 p.27：八种 pattern 总表；Pattern 1 摘要明确写明因全岛可能被控制，设想疏散全市居民及
  游客等；
- 印刷 p.28：Pattern 1 正文再次写明
  `市全域の住民及び観光客等を市外の避難施設に避難させる事案`；
- 印刷 p.29：实施要领记载例把要避难地区写为全市域，并写明以巴士、飞机等疏散居民和游客。

该材料同时明确这是架空国民保护事案的 pattern／预案例示，不能写成已经发生或已验证的撤离。

### 辅助建议

**`accept`。**

- R4S007 可进入安全来源 register；
- source locator 冻结为
  `印刷 pp.27–29；Pattern 1 摘要 p.27，正文 p.28，实施要领记载例 p.29`；
- R4E007 的 source_ref 可补入 R4S007；
- 支持 GOV_MIYAKO_CITY 的 F_FTE／life-safety 预案观察；
- fact text 必须包含 `scenario / pattern / plan example` 边界，不称为实际撤离或能力验证。

来源：

- https://www.city.miyakojima.lg.jp/kurashi/bousai/bousaijyouhou/files/hinanjissi.pdf

## 7. HR016-012 · R4S024 只支持 F_FTE source scope

### 调查结果

本项与 HR016-006 使用同一防卫省公告，但审的是 source scope。公告只包含举办机关、部队部署主题、
防卫省宣称的说明会目的、日期地点和参加限制。没有居民回应或独立程序评价。

### 辅助建议

**`revise`。**

- R4S024 source scope 改为 `frontline_taiwan_evacuation / F_FTE-only`；
- safe excerpt 使用防卫省公告首段“增进理解”目的，但明确标注为 `official stated purpose`；
- 删除 `procedural_fairness / F_PROC`；
- 不编码居民同意、程序充分性、代表性或说明会效果；
- 后续如取得问答记录或居民评价，应作为新 source／新 observation 单独复核，不能倒填到本公告。

来源：

- https://www.mod.go.jp/j/press/news/2026/02/20c.html

## 8. 建议负责人本批判断

建议一次确认：

- HR016-001 `revise`
- HR016-006 `revise`
- HR016-007 `revise`
- HR016-008 `revise`
- HR016-009 `accept`
- HR016-012 `revise`

## 9. 负责人确认

负责人于 2026-07-20 确认采用本报告全部建议：

- HR016-009 为 `accept`；
- HR016-001、006、007、008、012 为 `revise`；
- 2016 集会执行委员会不 crosswalk 到 A012；
- 防卫省与那国说明会及其公告只进入 F_FTE，不进入 procedural_fairness；
- 先岛五市町村训练按 Sakishima 区域级编码；
- 县环境部行政回应不回指 A013；
- 宫古 Pattern 1 以印刷 pp.27–29 进入安全来源层，但保持架空预案边界。

HR-016 已完成 **6/12**，剩余 6 项。全部人工复核剩余量从 80 降至 **74**；
可立即处理的线上非依赖项从 29 降至 **23**；排除当地材料后的线上剩余量从
68 降至 **62**。
