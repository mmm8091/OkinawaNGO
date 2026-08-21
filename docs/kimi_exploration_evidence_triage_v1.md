# Kimi 探索材料审计 v1

日期：2026-08-21

对象：负责人转交的 Kimi 对话记录及 `tmp/service_recon_990/` 缓存

结论：可作检索线索，不是可直接合并的正式研究包

## 1. 先说结果

Kimi 找到的方向是对的：下一轮要从普通网页扩展到 IRS 申报、USAspending、DoD／NAFI 制度文件和日方预算记录。但对话里混入了几处超出材料的结论，不能直接进入 database、报告或前端。

仓库中没有一份独立的 Kimi 正式包、manifest、source crosswalk 或人工回传。现有 `tmp/service_recon_990/` 是 ignored 缓存，共 24 个文本／HTML 文件，约 3.33 MB；其内容已经被 USN 服务生态普查部分吸收。缓存本身不能替代正式 source admission 和 archive receipt。

## 2. 可以保留的内容

### 线上渠道确实存在

- IRS 提供 Form 990 系列的年度 XML 下载与 TEOS 查证入口，可用于组织身份、年度财务总量、Part VII 人物职务和部分 Schedule I recipient。官方入口：<https://www.irs.gov/charities-non-profits/form-990-series-downloads>。
- USAspending 可查询联邦 award。官方 API 已核到 United Service Organizations, Inc. 的 DoD award `HQ00342310002`，总额 USD 72,000,000，期间 2023-09-30—2028-09-29（[award record](https://www.usaspending.gov/award/ASST_NON_HQ00342310002_097)）。它是 USO 全国组织的 award，不能分配成 USO Okinawa 收到 7,200 万美元。
- DoD FMR Volume 13 和 DoDI 1015.15 规定 NAFI 的预算、会计和年度财务管理框架，可用于建立“应当存在什么记录”的制度清单。它们不能替代某一冲绳据点的实际支出表。
- 日本侧的驻留军经费、基地交付金与相关预算存在公开渠道，但必须把国家财政、军方机构、地方财政与 NGO 资金分开，不能画成一条资金链。

### 当前缓存实际有什么

| 组织 | 缓存申报 | Schedule I 状态 | 可安全提取 |
|---|---|---|---|
| AWWA | TY2023 Form 990-EZ | 无完整 Schedule I | 年度总量、负责人等有限字段；不能恢复完整 recipient 年表 |
| KOSC | TY2024 Form 990 | 有 | 年度财务、Part VII、部分 recipient／项目条目 |
| MOSCO | TY2024 Form 990-EZ | 无完整 Schedule I | 有限年度与负责人字段 |
| NOSCO | TY2024 Form 990 | 有 | 年度财务、Part VII、部分 Schedule I 条目 |
| OESC | TY2024 Form 990 | 有 | 年度财务、Part VII、Schedule I；已支持 OESC→AWWA USD 8,479 有期 flow |

所以“已经拿到五家完整 990＋Schedule I”不成立；只有 KOSC、NOSCO、OESC 属于本轮可见的完整 990＋Schedule I 组。

## 3. 必须撤回或改写的说法

| 对话中的说法 | 问题 | 可用写法 |
|---|---|---|
| “两套网络互不来往” | 当前只对有界输入核过组织—组织边，人物、recipient 与历史关系没有对称测量 | “冻结的 9／6 比较框中尚未编码直接跨组组织关系；人物、recipient 和历史接口仍待查” |
| “六起诉讼和公投全部失效” | 法律案件、公投、请愿的制度和结果不同；部分留下赔偿、程序记录或标准 | “所选制度进入案例产生记录、赔偿或程序输出，但尚未观察到底层军事项目按诉求改变” |
| “慈善 NGO 替基地生产合法性” | 当前只有 LEG0 服务事实与 LEG1 行动方叙事，LEG3 为零 | “服务组织参与驻军社会再生产；这些活动是否形成地方接受或合法化效果，仍需 LEG2／LEG3 证据” |
| “148→39 证明运动没有稳定联盟” | 去重只说明观察粒度，不证明组织关系不存在 | “现有正式观察可归并为 39 个行动单元；稳定关系须另用组织证据验证” |
| “删除一个主要地方媒体后桥梁 8→4” | S004 不是媒体，而是 NACS-J／Peace Boat 的 2015 年 31 团体声明 | “可见网络对少数高密度联合声明来源敏感；这是 source-deletion sensitivity，不是社会网络消失” |
| “13 个跨语言传播案例” | 13 个 episode 包括法律和公投，不是 13 个国际传播案例 | “13 个制度转译 episode 用于比较进入场域、输出与项目变化；国际传播只是其中一部分” |
| “政府资源集中流向少数组织” | S002 的 616 行是官方合作记录行，不是 616 个组织或支付；365 个机器标签不是 actor | “616 行可描述部门、机制和议题字段分布；组织集中度须先做实体解析和支付语义复核” |
| “三个互不重合的网络” | 当前只是候选解释；R10、服务、问责的采样和端点并不对称 | “三类资源／行动层可并列比较，是否相交要用统一端点和人物／recipient 设计验证” |
| “依法应公开却查不到就是发现” | 缺失也可能来自披露例外、名字变化、申报类型或检索口径 | “只有预先声明记录义务、版本、字段、检索式和披露例外后，才能报告有界的 missing expected record” |

另一个重要限制：普通 990／990-EZ 的 Schedule B 捐赠者姓名和地址通常不对公众披露。Form 990 可以帮助找“组织怎么花、谁任职、部分给了谁”，但不能承诺穿透所有“谁给的钱”。IRS 官方 Schedule B 说明见 <https://www.irs.gov/instructions/i990sb>。

## 4. 方法更新：不是先猜金额，而是先列“预期记录”

“先推理它理应花多少钱、用多少人”容易把模型假设写成事实。更稳、也更有效的做法是建立 expected-record matrix：

| 对象类型 | 理应形成的记录 | 主要渠道 | 能回答什么 | 查不到时能说什么 |
|---|---|---|---|---|
| 美国免税组织 | 990／990-EZ、Part VII、适用附表 | IRS XML／TEOS | 年度总量、负责人、部分 recipient | 在指定税期与名称／EIN 下未定位；不能推出无活动 |
| 联邦 award recipient | award、agency、period、amount、assistance type | USAspending | 全国组织得到何种联邦资源 | 在既定筛选框内未定位；不能推出无间接资源 |
| NAFI／MCCS | 制度、预算、审计与内部财务记录 | DoD 文件、记录申请 | 机构职责与理论记录链 | 公开网页未披露；是否可取得需另核 |
| 军属俱乐部／慈善 | 990、Schedule I、官网年度报告 | IRS＋组织档案 | 谁任职、给谁、金额／用途的已披露部分 | 只报告具体缺失字段 |
| 日本 recipient | 法人登记、年报、受赠公告、地方报道 | 法人番号、组织官网、地方档案 | 端点身份、收到什么、如何回应 | 进入 LEG2 或当地补查清单 |

模型只用于决定先查哪里，不能填补缺失金额。真正的结论仍来自文件所记录的交易、职务、服务和反应。

## 5. 值得进入下一轮的 tracer

### P0

1. **USO national award → Okinawa presence**：保存 DoD→USO 全国 award；另查 USO Okinawa 的组织层级、据点、人员与 allocation。没有 allocation 证据前，两者不能相连成冲绳金额。
2. **KOSC／OESC／NOSCO → AWWA → recipient**：逐税期读取 IRS XML／Schedule I，再向日方 recipient 公告和年报反向核。先做 OESC USD 8,479 这条完整可核链。
3. **人物年度网络**：用 Part VII／Schedule O 建 person–actor–role–observed_at，不把申报年自动当任期。

### P1

4. **Marine Thrift Shop → AWWA／Lions／地方 recipient**：资金、membership、分配渠道和服务事实分层；补 recipient 一侧材料形成 LEG2 候选。
5. **Earthjustice／Dugong case 资源**：court-award accounting 与 Treasury payment mechanism 分开，定向寻找 fee order／settlement 正文。
6. **9／6／2 冻结框的对称 USAspending 检索**：按 EIN／法人名／别名记录 query 与零结果，避免只查服务侧。

### P2

7. **MCCS／NAFI 制度和公开记录可得性**：先做 record map，再判断是否发 FOIA／记录申请。
8. **日方 host-nation fiscal context**：只作制度背景，除非出现具名 NGO recipient，否则不生成 NGO 资金边。
9. **R10 合作资源生态**：完成 616 行 entity resolution 与机制／支付语义后，才比较它与服务侧、问责侧是否相交。

## 6. 与 USN wave 1 的关系

这些 tracer 不需要推翻现有架构。USN 已把 money、accounting、person–actor–time、service–recipient、affiliation、action–institution、official-site 和 LEG 证据分开。Kimi 材料的价值是补充检索渠道和下一轮顺序，不是提供新结论。

本审计不修改中央 actor、source、relation、publication 或前端数据。若负责人批准 P0，下一步应先做一条 tracer 的完整 source→fact→HR→typed-table 切片，再决定是否铺开。
