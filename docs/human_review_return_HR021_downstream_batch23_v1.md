# HR-021 R6／R11 下游纳入与 analytical seed 回交报告 Batch 23

日期：2026-07-20  
承办人：项目负责人  
辅助核查：Codex  
来源队列：`outputs/R06_R07_R11_pathways_v1/HR021_review_items_v0.csv`  
本批范围：HR021-001–008  
状态：**负责人已确认——5 项 include，2 项 revise scope，1 项 retain seed；HR-021 完成**

## 0. 批次边界

- HR021-001–007 的 HR-018 前置关系已经由负责人完成 accept／revise。
- 本批只判断这些关系是否及如何进入 R6／R11；不重复复核关系事实，也不改变 HR-018 的判断。
- R11 是“进入方式／角色观察矩阵”，不是金额比较表或稳定关系网。
- 行政委托、指定角色、服务存在和 sponsor tier 必须分层；不能统称为 funding。
- project cost、组织侧事业成本、合同额和点名资金流继续使用 R10 的不同字段，不在 R11 中合并。
- 企业或服务组织参与基地社区服务，不据此推断亲基地或反基地立场。
- HR021-008 只判断四条抽象路径种子能否升级；已有事件事实不等于存在有向传递链。
- 本报告不修改中央 relation 表、AEV 表、R6／R11 数据、HR CSV、图或 brief。

## 0A. 本轮调查所得

### HR021-001–007

逐项回看 HR-018 的负责人判断和 R11 现有 44 条矩阵行后，七项关系都有可说明的下游价值，但需要保持三种结构差异：

1. 行政委托／指定角色：公共机构通过特定事业、合同或年度制度与组织发生有界关系；
2. 服务存在：组织向特定 beneficiary group 提供服务，并在多个 site 出现；
3. 企业赞助：企业被公开列为某个服务组织或区域层级的 sponsor，不代表金额或政治立场。

R11 现有字段没有 amount 栏。因此金额最稳妥的处理不是把多个数塞进 interpretation text，而是：

- R11 只保留关系、项目、时间、角色和解释边界；
- 金额观察继续留在 R10 amount layer；
- R11 通过 relation ID 链回 R10，不复制、相加或重新解释金额。

### HR021-008

本轮检查了 S003、S004、S049，并补查了 WWF Japan、NACS-J 的其他正式活动记录：

- A003 ジュゴンネットワーク沖縄和 A005 WWF Japan 已经分别以 AEV0001、AEV0002 进入 2010 年 67 团体共同声明的正式 `human_checked` 事件层；
- A004 日本自然保護協会已经以 AEV0006 进入 2015 年 31 NGO 紧急共同声明的正式事件层；
- A019 ヘリ基地反対協議会的现场行动可由其官网支持，另有 AEV0060 的诉讼 non-party 边界；
- 2014 年环境评估／埋立手续要请同时点名 A003、A004、A005；
- 2020 年向冲绳县知事提交保护制度要望书同时点名 A019、A003、A004；
- 2007–2008 年 NACS-J／WWF 联合调查支持 A004、A005 的共同调查与环境知识生产。

这些新核查材料证明多次共同要请、调查和事件参与，但仍未证明：

- A019 的现场行动把信息有向传递给 A003；
- A003 再把地方环境知识有向传递给 A004／A005；
- 前一阶段导致后一阶段；
- 四个组织形成稳定联盟或固定分工链。

而且 A003、A004、A005 的可证事件角色已经在正式 AEV 层存在。把 AEV0062–0064 再升级会形成同一来源／同一事件的抽象重复行。

## 1. 辅助建议总表

| item | 对象 | 辅助建议 | 下游处理 | 核心边界 |
|---|---|---|---|---|
| HR021-001 | JICA沖縄→ONC 受托关系 | `include_after_hr018` | 纳入 R6 行政入口与 R11，entry mode=`administrative_commission` | 无公开金额；与普通 event co-participation 分开 |
| HR021-002 | 冲绳市→ONC，FY2024 KIP | `include_after_hr018` | 纳入 R11 的公共设施运营委托 | R11 不复制金额；四个金额口径只留 R10 |
| HR021-003 | 冲绳县→ONC，万国津梁会议支援 | `include_after_hr018` | 纳入 R11 的行政委托／事务局功能 | 两个 project-cost observation 不是付款或运动资金 |
| HR021-004 | 外务省→ONC，FY2024／FY2026 | `revise_scope_after_hr018` | 分成 FY2024 委托和 FY2026 指定角色两个时间观察 | 不把两年合并成无期限关系；不继承金额 |
| HR021-005 | 冲绳县→A066 研讨会合同 | `include_after_hr018` | 纳入 R6／R11 advocacy–administration boundary | 合同可确认；不等于 grant、认可、联盟或运动资金 |
| HR021-006 | USO Okinawa 服务存在 | `include_after_hr018` | 一条 service relation＋8 个 site/function observations | 不生成八条组织关系；不推断政治立场 |
| HR021-007 | MBC／Matson sponsor | `revise_scope_after_hr018` | MBC 纳入本地 direct row；Matson 只进 regional context／外围层 | 无金额；Matson 不是已证实的 Okinawa 定向赞助 |
| HR021-008 | AEV0061–0064 路径种子 | `retain_analytical_seed` | 四条继续与正式事实层分开 | 已有事件角色不构成有向传递或因果链 |

建议分布：

- `include_after_hr018`：5 项；
- `revise_scope_after_hr018`：2 项；
- `retain_analytical_seed`：1 项；
- `exclude`／`promote_with_independent_evidence`：0 项。

## 2. HR021-001 · JICA沖縄→ONC

HR-018-01 已确认：

- ONC 是 FY2019 教师海外研修事业及报告书的受托者；
- 公开材料没有合同金额；
- 事业／报告期间可描述，不能替代精确合同期。

R6 目前的行政路径只有 JICA／ONC 国际协力活动的 `event_collaboration`。受托关系提供另一种不同的行政入口：

> public institution → bounded commissioned role → local NGO service delivery

它有比较价值，但不能把委托和共同参加活动折成同一种关系。

### 辅助建议

**`include_after_hr018`。**

下游字段：

- entry domain：`administrative`；
- entry mode：`administrative_commission`；
- project：FY2019 JICA 教师海外研修；
- role：`commissioned_program_and_report_contractor`；
- amount：不进入 R11；
- boundary：`commission_role_confirmed; public_amount_unavailable`。

## 3. HR021-002 · 冲绳市→ONC，FY2024 KIP

HR-018-04 已经把四个金额口径拆开：

- 18.858m：总事业费；
- 16.662m：点名 ONC 的交付对象部分；
- 2.196m：未在该支路再次点名 recipient；
- 16.040m：ONC 组织侧事业费。

R11 的研究问题是“ONC 通过何种行政关系进入公共国际交流设施运营”，不是四个数之间如何会计对账。因此应纳入委托角色，但不把任何 amount 复制进 R11。

### 辅助建议

**`include_after_hr018`。**

下游只写：

> 冲绳市在 FY2024 KIP 管理运营中点名 ONC 为委托对象；金额口径见 R10，不在 R11 合并或比较。

R11 relation row 链回 R10R004；金额层继续独立保存。

## 4. HR021-003 · 冲绳县→ONC，万国津梁会议运营支援

HR-018-05 已确认：

- 县表的协作形态是 `委託`；
- ONC 人员承担事务局功能；
- 5.140m 与 5.530234m 是来源和口径不同的 project-cost observations；
- 两者都不是已确认的合同付款额。

这条关系适合说明外来／桥梁型组织如何通过行政事务局角色进入县级政策讨论程序，但不能把会议运营写成县政府对 ONC 倡议主张的认可。

### 辅助建议

**`include_after_hr018`。**

建议：

- entry mode：`administrative_commission_and_secretariat`；
- role：`commissioned_support / secretariat`；
- target：万国津梁会议的运营与资料／提言整理程序；
- political boundary：`no_government_endorsement`；
- financial boundary：`project_cost_observations_only; no_confirmed_payment`。

## 5. HR021-004 · 外务省→ONC，FY2024／FY2026

两个年度不是同一种完全相同的证据：

- FY2024：ONC 法定年报直接写 `外務省委託`；
- FY2026：外务省官方名单确认 ONC 是该年度 NGO 相談員团体，页面没有金额。

如果在 R11 中折成一条无期限 relation，会遮蔽“委托证据”和“年度指定名单”的差异，也容易让 FY2024 的组织侧成本错误延续到 FY2026。

### 辅助建议

**`revise_scope_after_hr018`。**

拆成两个下游 observation：

1. FY2024：`administrative_commission`，role=`NGO consultant under MOFA commission`；
2. FY2026：`annual_designated_public_service_role`，role=`listed NGO consultant organization`。

共同限制：

- 不写永久指定；
- FY2026 不继承 FY2024 的 2,894,630 円；
- 不推断 ONC 获得的合同金额；
- 不从咨询服务推断 MOFA 对 ONC 其他项目或政治立场的认可；
- 不生成 ONC→其他冲绳 NGO 的资助边。

## 6. HR021-005 · 冲绳县→A066 新外交イニシアティブ

HR-018-08 已确认 2024-05-16 的研讨会业务委托合同和 12,842,500 円合同额。这是本批中唯一可以使用 actual contract amount 的关系。

它对 R6／R11 有独立价值：A066 是日本国内倡议／研究组织，但在这里进入冲绳议题场域的机制是县级 proposal-based commission，而不是共同声明或资助。

### 辅助建议

**`include_after_hr018`。**

建议下游角色：

- entry domain：`advocacy_administration_boundary`；
- entry mode：`proposal_selected_public_contract`；
- role：`commissioned_symposium_contractor`；
- project：在冲美军基地问题研讨会举办业务；
- contract amount：可以通过 R10 linkage 显示 12,842,500 円，但 R11 不以金额决定权重。

不得推断：

- 冲绳县认同 A066 的全部主张；
- 合同是 grant 或 movement funding；
- 双方形成稳定联盟；
- 研讨会造成政策改变。

## 7. HR021-006 · USO Okinawa 服务存在

HR-018-17 已确认：

- 一条 USO Okinawa→eligible military community 的 consolidated service relation；
- 8 个公开地点／服务节点；
- Area Office 与普通 center 需要区分；
- 服务对象不等于成员、资助方或政治支持者。

R11 的 `service` domain 已有 AEC sponsorship、AWWA membership 等关系，但尚缺 service provider→beneficiary 的直接功能观察。加入这条可以让“服务存在”与“赞助／慈善／membership”分层。

### 辅助建议

**`include_after_hr018`。**

结构：

- 一条 R11 service-entry relation；
- 8 个 site/function observations 作为附属地点层；
- 不把 8 个地点计算为 8 个组织；
- 不生成资金方向；
- `political_stance_inference_allowed=no`。

## 8. HR021-007 · MBC／Matson sponsor

HR-018-18、19 的最终差异是：

- MBC：USO Okinawa Platinum Sponsor，主体全名和支持类型可确认，但无 relation amount；
- Matson：USO Indo-Pacific Mission Partner；USO Okinawa 页面是本地展示入口，不证明本地定向赞助或金额分配。

如果两者都直接以 `sponsor→USO Okinawa` 进入同一 R11 层，会抹掉这项范围差异。

### 辅助建议

**`revise_scope_after_hr018`。**

分别处理：

1. MBC：进入 R11 direct Okinawa service-sponsorship row；
2. Matson：不进入“冲绳直接赞助”层；如果 R11 保留区域外围 context，则以 `USO Indo-Pacific regional sponsor, listed on Okinawa page` 进入外围层。

共同限制：

- sponsor tier 不是金额；
- MBC 的现金／实物支持类型不折价；
- Matson 不补本地 allocation；
- sponsor 身份不证明企业的基地政策立场。

## 9. HR021-008 · AEV0061–0064

四条 seed 当前构造的是一个可能的解释序列：

1. A019：local site and action；
2. A003：local environmental translation；
3. A004／A005：domestic environmental translation。

本轮确实查到更多正式活动记录：

- 2010 年 67 团体向政府提交共同声明，A003、A005 在名单中；
- 2014 年环境评估／埋立手续要请同时列 A003、A004、A005；
- 2015 年 31 NGO 紧急共同声明记录 A004 的参与；
- 2020 年县级保护制度要望书同时列 A019、A003、A004；
- NACS-J／WWF 的 2007–2008 年联合调查记录共同环境知识生产。

但是这些证据的方向都是：

> actor → specific statement/request/investigation

它们不提供：

> A019 → A003 → A004/A005

的观察性传递边。多个 actor 出现在同一要请或调查，也只证明 event-specific co-action。

此外：

- A003、A005 的 2010 事件角色已经分别存在于 AEV0001、AEV0002；
- A004 的 2015 事件角色已经存在于 AEV0006；
- A019 的现场组织身份和诉讼 non-party 边界已有其他正式记录。

因此不能用已有事实重复制造四条泛化 pathway fact。

### 辅助建议

**`retain_analytical_seed`。**

保留方式：

- AEV0061–0064 继续放在 `analytical_seeds_v0.csv`；
- 不进入默认事实层、事实计数或稳定网络；
- 图中使用虚线／独立图例；
- caption 明写“分析性路径假说；各阶段有事件事实，但阶段间传递未被观察”；
- 已查到的新事件如果未来需要纳入，应各自建立有日期、对象、动作和 source 的 event row，而不是升级泛化 seed。

不建议 `exclude_seed`，因为该解释序列对提出“现场行动如何可能被环境／制度语言转译”仍有研究价值；只是目前不能当作事实链。

## 10. 如负责人确认，本批后续动作

1. HR021-001、002、003、005、006 记录 `include_after_hr018`。
2. HR021-004、007 记录 `revise_scope_after_hr018`，分别执行年度拆分和本地／区域 sponsor 范围拆分。
3. HR021-008 记录 `retain_analytical_seed`。
4. R11 新增／修订的行只继承 HR-018 已确认事实；不重新生成关系判断。
5. R11 不复制金额，使用 relation ID 链回 R10 amount layer。
6. R6 行政入口至少区分 `event_collaboration`、`administrative_commission` 和 `advocacy_administration_boundary`。
7. analytical seed 仍从正式 facts、默认图层和事实计数中排除。
8. 本报告只留人工复核记录；中央 CSV、图和 brief 留待主线程统一合并／重生。

## 11. 本批证据入口

- S003／WWF Japan 2010 共同声明：<https://www.wwf.or.jp/activities/statement/3436.html>
- S004／NACS-J 2015 紧急共同声明：<https://www.nacsj.or.jp/statement/50827/>
- S049／ヘリ基地反対協議会：<https://lovehenoko.org/>
- WWF Japan 2014 环境评估／埋立手续要请：<https://www.wwf.or.jp/activities/statement/1620.html>
- NACS-J 2020 冲绳县保护制度要望书：<https://www.nacsj.or.jp/statement/50673/>
- NACS-J／WWF 大浦湾联合调查：<https://what-we-do.nacsj.or.jp/2008/07/350/>

## 12. 负责人确认记录

负责人于 2026-07-20 确认本批全部辅助建议：

- HR021-001、002、003、005、006：`include_after_hr018`；
- HR021-004、007：`revise_scope_after_hr018`；
- HR021-008：`retain_analytical_seed`。

负责人同时确认：

- FY2024 外务省委托和 FY2026 NGO 相談員年度指定拆成两个下游时间／角色观察，FY2026 不继承 FY2024 金额；
- MBC 可进入 USO Okinawa 直接赞助层，Matson 只作为 USO Indo-Pacific 区域 sponsor context，不写成本地定向赞助；
- R11 不复制或合并 R10 金额，只通过 relation ID 保持链回；
- AEV0061–0064 继续作为独立 analytical seed，不进入默认事实层、事实计数或稳定关系网；
- 多次共同要请、调查和事件参与不构成 A019→A003→A004/A005 的有向传递或因果链。

至此 HR-021 的 8 项决定全部完成。本批只更新人工复核回交报告；未修改中央 relation 表、AEV 表、R6／R11 数据、HR CSV、图或 brief，留待主线程统一合并／重生。
