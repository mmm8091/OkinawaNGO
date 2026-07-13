# HR-016：R4 先岛框架人工复核包

范围：7 条 actor/frame semantic-human 项与 5 条 source locator/speaker 项。

## 复核方法

1. 打开 CSV 中的 URL，并按 source locator 回到原页。
2. 在 `review_decision` 填 `accept`、`revise` 或 `reject`；同时填写 reviewer、日期与理由。
3. `revise` 必须写明修订后的 actor/speaker、place、frame 或 locator。
4. 人审完成前，12 项均不进入正式事实或图；人物不等于机构、匿名样本不等于总体、会议不等于同意。

## Actor / frame（7）

### HR016-001 · R4E001

- 问题：R4S003 具名的是“6・11自衛隊配備を止める市民集会”実行委員会。请判定它是否与 A012 为同一持续组织；若不能确认，是否 revise 为一次性 provisional event committee，只保留 2016 集会层级？
- 打开：https://ryukyushimpo.jp/news/entry-296563.html；定位：R4S003: 正文第140-147行／集会主办者与地下水诉求
- 影响：R4E001（若通过则新增/修订正式事实）；entity-frame 图与 R4 brief；三地 source 图当前已计 R4S003
- 默认边界：默认不 crosswalk 到 A012；保留一次性事件委员会候选，不证明组织持续性。

### HR016-002 · R4E008

- 问题：请把久貝美奈子议员的提问与総務部長答复分开，判定 local_autonomy_referendum 是否只能归给具名议员个人，而不能归给整个宫古岛市议会。
- 打开：https://www.city.miyakojima.lg.jp/gyosei/gikai/files/kaigiroku0706.pdf；定位：R4S008: 印刷 p.139-140／久貝美奈子提问与総務部長上地俊暢答复分段
- 影响：候选 R4E008；entity-frame 图、三地 source 图与 R4 brief
- 默认边界：个人议员不等于市议会；待 speaker 人审前不进正式事实。

### HR016-003 · R4E009

- 问题：请核 R4S008 中台湾有事／全岛撤离陈述的具体 speaker，判定 F_FTE 应归给久貝美奈子个人、行政答复方，还是因归属不清而拒绝。
- 打开：https://www.city.miyakojima.lg.jp/gyosei/gikai/files/kaigiroku0706.pdf；定位：R4S008: 印刷 p.139-140／久貝美奈子提问与総務部長上地俊暢答复分段
- 影响：候选 R4E009；entity-frame 图、三地 source 图与 R4 brief
- 默认边界：个人提问、行政答复和议会机构必须分开；预案讨论不等于实际撤离。

### HR016-004 · R4E016

- 问题：请逐条核 R4S015 的匿名居民发言与箭头后的行政答复，判定是否可将 F_FTE 仅编码为“该场 23 人意见交换会中的匿名发言”，而不建立 RESIDENTS_ISHIGAKI 稳定 actor。
- 打开：https://www.city.ishigaki.okinawa.jp/material/files/group/3/ikenkoukankai_ibaruma.pdf；定位：R4S015: p.1 起；逐条保留“意见”和箭头后的行政答复
- 影响：候选 R4E016；entity-frame 图、三地 source 图与 R4 brief
- 默认边界：匿名 23 人会议样本不等于全市居民，也不形成稳定 actor。

### HR016-005 · R4E017

- 问题：请逐条核 R4S015 中关于撤离义务与决策的匿名问题，判定 F_AUT 是否可保留为会议样本中的匿名程序疑问；不得概括为石垣全体居民立场。
- 打开：https://www.city.ishigaki.okinawa.jp/material/files/group/3/ikenkoukankai_ibaruma.pdf；定位：R4S015: p.1 起；逐条保留“意见”和箭头后的行政答复
- 影响：候选 R4E017；entity-frame 图、三地 source 图与 R4 brief
- 默认边界：匿名程序疑问不等于统一自治立场；待逐条 speaker 复核。

### HR016-006 · R4E024

- 问题：R4S024 只直接证明防卫省举办新导弹部队说明会及其“增进理解”目的。请判定本行是否 revise 为 MOD_JAPAN 的 F_FTE 制度事件；没有居民程序评价时不得保留 F_PROC。
- 打开：https://www.mod.go.jp/j/press/news/2026/02/20c.html；定位：R4S024: 正文第16行说明会目的
- 影响：候选 R4E024；entity-frame 图、三地 source 图与与那国解释
- 默认边界：说明会存在不等于程序公平或居民同意；默认只保留候选 F_FTE。

### HR016-007 · R4E025

- 问题：R4S021 覆盖先岛五市町村。请判定是否 revise 为 place=Sakishima 的区域级 GOV_OKINAWA_PREF life_safety 观察；不得作为与那国特有事实。
- 打开：https://www.pref.okinawa.lg.jp/bosaianzen/kokuminhogo/1023175/1026163/1032696/1032939.html；定位：R4S021: 页面训练项目第203-214行
- 影响：候选 R4E025（只能区域级）；entity-frame 图与区域背景；不得增加与那国专属计数
- 默认边界：先岛区域材料不得落为与那国特有事实。

## Source locator / speaker（5）

### HR016-008 · R4S002

- 问题：请确认 p.6 地下水文字的 speaker 是县环境部行政回应还是陈情者原文。若只确认行政回应，是否 revise 为 government_response 的地下水背景来源，并继续禁止回指 A013？
- 打开：https://www.pref.okinawa.jp/_res/projects/default_project/_page_/001/016/966/doboku310319.pdf；定位：p.6／“陸自ミサイル部隊”陈情处理段落
- 影响：不自动恢复 R4E002；若要归给 A013 必须另有具名陈情原文；三地 source 图的宫古地下水计数及 brief
- 默认边界：行政答复不能替代 A013 的自有措辞；默认留在 source 人审队列。

### HR016-009 · R4S007

- 问题：请在 PDF 中补出 Pattern 1 的稳定印刷页码，并确认“市全域の住民及び観光客”所在页；页码可复核后才可 accept 到安全来源及 R4E007 source_ref。
- 打开：https://www.city.miyakojima.lg.jp/kurashi/bousai/bousaijyouhou/files/hinanjissi.pdf；定位：PDF Pattern 1 的具体印刷页码待补
- 影响：正式 R4E007 的 source_ref 可补入 R4S007；三地 source 图的宫古 F_FTE/life_safety 计数
- 默认边界：没有稳定页码前不进入安全 source register。

### HR016-010 · R4S008

- 问题：请按印刷 p.139–140 分段标出久貝美奈子提问与総務部長上地俊暢答复，分别判定 F_AUT、F_FTE 与 life_safety 的 speaker 归属。
- 打开：https://www.city.miyakojima.lg.jp/gyosei/gikai/files/kaigiroku0706.pdf；定位：印刷 p.139-140／久貝美奈子提问与総務部長上地俊暢答复分段
- 影响：候选 R4E008、R4E009；entity-frame 图、三地 source 图与 brief
- 默认边界：个人议员、行政官员与议会机构不得合并。

### HR016-011 · R4S015

- 问题：请逐条拆分 p.1 起的匿名居民意见与箭头后的防灾危机管理课答复，并判断哪些短句可进入 F_FTE 或 F_AUT；23 名参加者不得代表全市。
- 打开：https://www.city.ishigaki.okinawa.jp/material/files/group/3/ikenkoukankai_ibaruma.pdf；定位：p.1 起；逐条保留“意见”和箭头后的行政答复
- 影响：候选 R4E016、R4E017；entity-frame 图、三地 source 图与 brief
- 默认边界：匿名居民、行政答复与全市居民不得合并。

### HR016-012 · R4S024

- 问题：请确认正文第16行只支持说明会事件及防卫省宣称的“增进理解”目的。若无居民回应或程序评价，是否 revise 为 F_FTE-only source，并拒绝 procedural_fairness？
- 打开：https://www.mod.go.jp/j/press/news/2026/02/20c.html；定位：正文第16行说明会目的
- 影响：候选 R4E024；entity-frame 图、三地 source 图与与那国解释
- 默认边界：举办说明会不证明 procedural fairness 或居民同意。

## 完成条件

CSV 12 条均有决定、复核者、日期和理由；所有 revise 项写明新编码。完成前不得更新正式事实或图。
