# HR-USN2-01 人物消歧正式回传 v1

日期：2026-08-22

状态：`principal_confirmed / research_overlay_only / no_central_writeback / not_frontend_ready / W2-F_not_released`

## 回传决定

| 子项 | 负责人决定 | 研究层处理 |
|---|---|---|
| 01a Brooke Epp／Epps（AWWA／KOSC） | `accept — same_person` | 合并为同一 research-overlay person；保留 filing-point 与 tax-period 两种时间语义 |
| 01b Jen Yapsing／Jennifer Yapshing（AWWA／NOSCO） | `remain_unresolved — no merge` | 保留两条人物字符串；`Yapsing`／`Yapshing` 可能是不同姓氏，且没有 bio／历史 roster 闭合 |
| 01c Amber N Tracy／Amber Tracy（AWWA／OESC） | `accept — same_person` | 合并为同一 research-overlay person；AWWA `InCareOfNm`／`BooksInCareOfDetail` 仍只记联系／账簿语境 |
| 01d Trinicia Kloepper（AWWA／KOSC） | `accept — same_person` | 合并为同一 research-overlay person；申报期相同不等于精确任期相同 |
| 01e Lesilee Du Fresne／DuFresne（OESC） | `accept — spelling_variant / same_person` | 合并 OESC 内部相邻申报期时间线，不生成跨组织边 |

判断依据见 `outputs/us_presence_network_wave2_person_disambiguation_supplement_v1/` 的 evidence matrix、timeline 与负责人判断页。负责人判断改变身份解析状态，不改变原 IRS 申报记录本身。

## 网络结构影响

决定在服务侧形成 4 个统一人物身份，其中 3 人跨组织：

- AWWA—KOSC：Brooke Epp／Epps、Trinicia Kloepper，共 2 名共享人物；
- AWWA—OESC：Amber Tracy，共 1 名共享人物；
- OESC 内部：Lesilee DuFresne 的两期角色连续；
- AWWA—NOSCO：Jen／Jennifer 未解决，不新增人物桥。

资金层不随人物决定自动改变。OESC→AWWA 的三个已确认税期流为 USD 16,308、14,371、8,479，合计 USD 39,158；AWWA—OESC 因而成为当前 research overlay 中同时具有人物层和资金层记录的 service-side pair。AWWA—KOSC 只有确认人物桥和既有隶属观察，没有确认资金流；KOSC 申报中的 USD 2,580 名称行仍属于个人援助组语义，不能改写成 KOSC→AWWA 组织付款。

重建后的分层网络位于 `outputs/us_presence_network_wave2_service_person_confirmed_overlay_v1/`。人物角色观察、人物投影与资金流分别存表，未把多层关系压成一种边或一个总权重。

## 边界

- 五组人物都在驻军服务／军属慈善侧；本回传没有审计问责侧 roster，因此只说明这些决定未创建跨侧边，不能报告跨生态零；
- `same_person` 不等于控制、联盟、资金授权或政治立场；
- return header 是申报时点观察，Part VII 是所报税期角色，`BooksInCareOf` 是联系／账簿字段；
- 本回传不改中央事实表、W2-A 原始长表、publication adapter 或前端；
- 本回传不放行 W2-F，其他 HR-USN2 判断和实际信息公开请求仍按主线程总账处理。
