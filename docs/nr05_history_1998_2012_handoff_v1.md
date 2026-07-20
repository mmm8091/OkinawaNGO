# NR-05 1998–2012 线上历史补缺换手

状态：**完成，待主线程复验／负责人检查点；未进入正式 HR、中央表或前端。**
日期：2026-07-20

## 1. 本 session 做了什么

按 `docs/next_round_exploration_system_sessions_v1.md` 的 NR-05 契约，完成 1998–2012 线上历史补缺：

- 15 个带日期语义的历史锚点；
- 11 个组织状态候选；
- 32 个来源候选，全部有 exact locator、来源关系和解释边界；
- 10 个缺口／后续机会，其中 G008 明确为 `online_followup_material_rich`；
- 20 个逐行研究复核候选；
- brief、search log、README、validation；
- 一张可复现 SVG“载体—制度场域—材料留存”时间图及 figure brief；
- 可重复生成器和 4 项专用测试。

所有 CSV 行均固定为：

`research_only / candidate / ai_seeded / not_frontend_ready / central_writeback=no`

本 session **没有**修改中央 actor/source/edge、source archive、前端、workbench 或其他控制文档，也没有 commit。

## 2. 交付文件

- `outputs/history_1998_2012_online_v1/historical_anchor_candidates.csv`
- `outputs/history_1998_2012_online_v1/organization_status_candidates.csv`
- `outputs/history_1998_2012_online_v1/source_candidates.csv`
- `outputs/history_1998_2012_online_v1/search_log.md`
- `outputs/history_1998_2012_online_v1/online_exhausted_gaps.csv`
- `outputs/history_1998_2012_online_v1/human_review_queue.csv`
- `outputs/history_1998_2012_online_v1/brief.md`
- `outputs/history_1998_2012_online_v1/README.md`
- `outputs/history_1998_2012_online_v1/validation_report.md`
- `outputs/history_1998_2012_online_v1/fig1_carrier_venue_trace_timeline_v1.svg`
- `outputs/history_1998_2012_online_v1/fig1_carrier_venue_trace_timeline_v1_brief.md`
- `scripts/make_history_1998_2012_online_v1.py`
- `tests/test_make_history_1998_2012_online_v1.py`
- 本换手文件

## 3. 15 个锚点的覆盖

1. 1998 琉大课程田野的同期二手 baseline；
2. 1999–2004／2012 全县认证 NPO 累计数；
3. ONC 1999-06 设立、二手沿革所称 2008 转换阶段与官方 2009-05-14 认证日；
4. 普天间第一次噪音诉讼 2002–2003 日期差异；
5. 2003-09-25 冲绳儒艮美国诉讼进入；
6. 2004-02-03 至 03-30 公害调停受理后因管辖设计被排除；
7. 2004-04-19 边野古现场行动；
8. 2004-06-10 NACS-J 环评方法书正式意见；
9. 2005-05-20 泡濑第一波公金诉讼；
10. 2008-02-14 女性／人权请求；
11. 2010-05-14 WWF 67 团体事件级联署；
12. 2011-04-28 嘉手纳第三次诉讼；
13. 2011-06-23 宫古／下地岛反部署集会；
14. 普天间第二次诉讼 2012 标签与 2012–2013 并行案件；
15. 2012-08-25 与那国意见广告实行委员会线索。

另在组织状态表中保留 A076、A055、A088、A069、珊瑚平台等形成／法人／最低活动日期，不为凑锚点而把 status 自动写成事件或连续组织。

## 4. 最有价值的实证判断

“1998 年后较易追踪”只能被保守确认：

- 法人认证、法院案件轮次、正式环评意见、行政日志留下结构化日期；
- 非正式组织、实行委员会、地方集会载体仍大量依赖后来回顾、地方／政党媒体和档案目录；
- 因而可见性增量主要来自制度留档，不能等同于活动增加、寿命变长或网络中心性。

更值得继续检验的假设不是一般“议题多元化”，而是：

> 1998 后全行业 NPO 法人化快速增长，但基地问责的地方载体可能主要保持非正式／事件型／案件型，并通过律师、外部法人 NGO 和程序场域取得专业能力。

这仍只是比较假设。当前 51 actor 的选择性基地问责子集里仅 1 行明确标为 specified NPO，只能视为 audit signal；purposive registry、标签筛选和 `legal_status_guess` 都不支持总体比例推断。

同时，2012 冲绳县 NPO Plaza 资料说明法人制度带来年度报告、登记、地方税等维护义务，也提到无活动／资源不足的法人可能解散或回到任意团体。它说明法人制度既生产可见记录，也生产维护与退出成本，不能把“法人化”直接等同“长寿化”；该材料不支持发生率推断。

## 5. 文献新颖性边界

- Spencer 2003 已研究冲绳反基地市民团体中的环境、女性和反军国主义框架，所以“议题多元化”不能包装成本项目新发现。
- 1998 琉大文章只可作同期课程田野／解释性 baseline，不是全县普查。
- 2001 一般环境志愿活动调查提供竞争解释：NPO 法前已有不同于反基地运动的环境团体和行政协作，不可写成所有环境行动由反基地运动线性派生。
- 本项目可争取的新贡献，是比较不同制度场域如何差异化地制造历史可见性，并检验法律 NPO 生态与基地问责载体为何没有简单重合。

## 6. 日期与分母纠错

- 已完全分开 `source_publication_date / event_date / actor_active_period / claim_period`。
- 专修大 PDF 正文写的是 1997 年 6 月组成推進協、同年 10 月发展性解散／重组；搜索摘要容易把后续 2000 行动黏到重组年份。本包明确排除“2000 lifecycle”锚点，不重复修改中央 `LC002`。
- RIETI 认证累计表的冲绳值为 1999=6、2000=20、2001=37、2002=84、2003=127、2004=163；2012-10-31 冲绳官方 newsletter 为 550。
- RIETI 另一张表的 1999=5、2000=15 是资料／事业报告可用样本口径，不与累计认证表连接，也不当作矛盾。
- 全县所有领域的认证 NPO 数与本项目选择性运动样本不是同一分母，不能画成一条同质序列或作法人化比例推断。
- ONC 的 2022 二手访谈写 2008 取得 NPO 法人格／改现名，但内阁府所辖厅正式记录的 `設立認証年月日` 是 2009-05-14；本包将内部决议／申请／名称使用与正式认证分开，未把两者强行择一。
- G008 不是线上穷尽：县 NPO Plaza 当前页仍公开“现存法人（认证日／20领域）”和“解散・取消・移管（退出日）”两张表，可先在线构建 surviving cohort 与 exit-event 下界，再按实体补退出法人认证日。

## 7. 复核队列不是正式 HR

`human_review_queue.csv` 的 20 行是研究候选池，字段明确：

- `queue_role=research_candidate_pool`
- `formal_hr_dispatch_status=not_dispatched`
- 负责人决定栏全部留空

负责人本轮**不需要逐条处理 20 行**。建议只开一个 7 项高杠杆检查点：

1. 1998 baseline 是进入报告 context box，还是只留文献层；
2. 是否推进“制度化路径分化／组织分工”假设；
3. 是否公开展示普天间轮次标签压缩与并行案件；
4. 是否把 2004 管辖排除纳入正式负例比较；
5. 是否研究法律／程序托管造成的留档优势；
6. 宫古／与那国是否优先派当地材料；
7. A076／A055／A069 身份与连续性是否值得当地／档案投入。

负责人选完后，再由下一 session 把被选中的行生成正式 HR；当前 20 行不得自动并入正式总账。

## 8. 强制解释边界

- litigation round 不是新 actor，不推定跨轮次成员相同；
- 共同原告／同案、联署、参会、共同提出请求都不是稳定联盟；
- A055 是泡濑运动／supporter，不是组织性具名原告；
- H98_009 的 `actor_ids` 已留空：提诉主体写为个人住民，A055 只在后续报道中保留 movement/support 角色；
- H98_011 的 `actor_ids` 只有 `A005`，其余名单只在事件参与描述中出现；
- 2004 公害调停 913 名申请人是个人集合，不 actor 化；
- A015 仍是 E2 单一政党媒体线索；
- archive catalog 只作 locator，未读底层材料不作事实来源；
- 当前网页里的历史日期不写成网页访问年的事件；
- 来源保存能力不等于社会影响力；
- 不从 NPO 总量推出基地 actor 法人化或 NPO 法因果。

## 9. 验证与复现

执行：

```powershell
python scripts\make_history_1998_2012_online_v1.py
python -m unittest discover -s tests -p "test_make_history_1998_2012_online_v1.py" -v
python -m py_compile scripts\make_history_1998_2012_online_v1.py
```

结果：

- 生成器成功；
- 4 tests passed；
- `py_compile` 通过；
- 两次生成字节级一致；
- 1800×1060 目视复验通过；2010–2012 密集区已在各自泳道内错层，H98_011–015 的节点与框内文字无覆盖，未跨泳道或删除边界语义；
- validation 内含文件 hash、门禁和 known exclusions。

## 10. 主线程复验建议

1. 先读 `brief.md` 与 `validation_report.md`；
2. 抽查 H98_001、H98_002、H98_006、H98_009、H98_014、H98_015 六行；
3. 检查 `human_review_queue.csv` 的 20 行均为 `not_dispatched`；
4. 确认 7 项负责人检查点后，再决定是否生成正式 HR；
5. NR-06 之前不要把任何历史候选送入前端已核层。
6. 目视复核 SVG：宏观 NPO 背景有独立 count axis；下方三泳道不以节点数和 550 相除；颜色只表示 source relationship。

## 11. 不得被主线程误读为

- NR-05 已完成中央历史补录；
- 20 个正式人工任务已派发；
- 1998 baseline 是全县统计事实；
- 550 个 NPO 与本项目 actor registry 可直接比较；
- 基地问责载体“已证明”不法人化；
- ONC 是对 1998 文章的直接制度回应；
- 环境／女性框架是本项目首次发现；
- 诉讼、环评或调停进入已经改变工程／基地运行；
- A068→A019 生命周期需要再次修改。
