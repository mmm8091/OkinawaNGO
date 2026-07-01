# HR-001 至 HR-009 人工复核合并包 v0

日期：2026-07-01

用途：供主进程同步人工复核结果。本文只汇总已由人类复核者确认的 HR-001 至 HR-009，不启动 LR-001 至 LR-008，也不新增事实判断。

## 0. 合并状态

- 正式人工复核任务：9 个，HR-001 至 HR-009，已完成首轮并写入 `data/interim/human_review_log_v0.csv`。
- 人类决策任务：8 个，HD-001 至 HD-008，均已 closed。
- 当地材料收集任务：8 个，LR-001 至 LR-008，本包不处理。
- 当前数据规模：93 actors、14 aliases、92 sources、180 actor-issue edges、124 actor-place edges、27 support/funding edges。
- source archive 状态：28 archived、1 manual_archived、36 pending_archive、25 skipped_inferred_url、2 skipped_non_url_reference。

## 1. 主进程必须继承的硬边界

1. 共同署名、共同声明、同场出现，只能写成共同署名 / 声援 / 共同在场，不得自动写成稳定联盟。
2. grant opportunity / NOFO 只能写成机会公告，不得写成已拨款、已有 recipient 或资金链。
3. NED / USAID / 外务省 / 美国使领馆关系，除非有官方 grant、award、contract、财报或项目报告，不得写成资助冲绳 NGO。
4. 与那国条目采用前线化、地方自治、住民投票、台湾周边安全环境、健康 / 生活安全框架，不强行环保化。
5. E4/E3 可进入事实表述；E2 只能作为线索；E1/E0 不进结论。

## 2. 可合并为事实的结论

### HR-001 A002 / A076

- A002 `ジュゴン保護キャンペーンセンター（Save the Dugong Campaign Center）` 保留，组织身份 E4。
- A002 是 2001 年成立的日本任意団体、IUCN 国家级 NGO 会员，可写为儒艮保护和国际倡议 actor。
- A002 不应写为边野古儒艮美国诉讼的法律原告。
- 新增 A076 `ジュゴン保護基金委員会（Save the Dugong Foundation）`，作为诉讼原告方向的独立节点，E3，仍需补查。

### HR-002 A008

- A008 `NGO非戦ネット` 保留，重定性为全国性国际协力 / 和平 NGO 网络。
- 可写：其于 2019 年就辺野古县民投票发表尊重结果声明，属于全国网络的连带 / 支援。
- 不可写：冲绳本地核心 actor、稳定联盟成员或现场行动组织。

### HR-003 A014 / A015 / A016

- A014 原 `与那国改革会議` 不保留原名，替换为 `住民投票を成功させるための実行委員会`，E2，线索级。
- A015 `与那国自衛隊配備反対意見広告実行委員会` 保留，E2；定性为八重山 / 石垣侧声援与那国的临时意见广告实委会。
- A016 `与那国島の明るい未来を願うイソバの会` 保留，E3；可写为与那国本地持续活动的市民团体，围绕自卫队部署、弹药库透明性、演习中止和生活安全提出诉求。

### HR-004 A019

- A019 `ヘリ基地反対協議会` 保留，E4，是辺野古现场核心 actor。
- legal_status 改为任意団体；source_refs 使用 S049/S050/S008，剔除占位 S042。
- 可写：1998 年以前身 `名護市民投票推進協議会` 发足，2004 年起在辺野古持续帐篷座り込み与海上行动。

### HR-005 / HR-006 AWWA 网络

- X004 当前名修正为 `American Welfare & Works Association (AWWA / 米国福祉事業協会)`，保留 E4。
- AWWA 五成员网络补全：X005 NOSCO、X006 KOSC、X007 OESC、X016 MOSCO、X017 Army Community Group。
- X016 `Marine Officers' Spouses' Club Okinawa (MOSCO / MOSC)` 新增，E4。
- X017 `Army Community Group of Okinawa` 新增，E3。
- X007 OESC 501(c)(3)、EIN 98-0346507、OESC→USO Okinawa 2025 年捐赠可作为 E4 事实。
- 成员边仅证明 AWWA 伞状结构，不证明任何具体受赠 recipient。

### HR-007 X013

- X013 `Okinawa Youth Council Program` 保留，E4 仅限于 NOFO / grant opportunity 存在。
- 可写：美国驻那霸总领事馆 PAS 发布过该项目资助机会，机会已于 2024-04-15 截止。
- 不可写：存在公开 recipient、某冲绳组织获得该资助。

### HR-008 X014 / X015

- X014 NED 保持 watchlist_only。FY2024 亚洲拨款清单未见日本、冲绳或琉球 direct recipient。
- X015 Peace Winds Japan 保持 watchlist_only。其 USAID 关系仅为 2018 年西日本水灾 / 北海道地震灾害救援方法样本，未见冲绳基地或先岛安全议题连接。

### HR-009 A040 / A046

- A040 改名为 `Forum for Protection of Public Interest (Pro Public)`，alias 保留 Pro Public / Friends of the Earth Nepal，E4 身份确认。
- A046 改名为 `Pro Natura`，alias 为 Friends of the Earth Switzerland / Pro Natura / FoE Switzerland，不拆分，E4 身份确认。
- A032-A046 只作为 2015 年共同署名 / 国际声援节点保留，不进入核心网络解释，不写成稳定联盟。

## 3. 只能作为线索或待补的事项

- A014 `住民投票を成功させるための実行委員会`：组织规范名称、代表人、与 2012 签名运动的延续性待当地资料确认。
- A015：仅赤旗单一来源支撑，需八重山日报 / 八重山毎日 / 意见广告实物交叉确认。
- A016：存在与持续活动已确认，但成立年月、代表人、法律身份仍需补。
- A019 dugong 诉讼原告映射：2003 年 plaintiff 名称究竟对应 A019、命を守る会或其他组织，仍待核实。
- F013 A047→A019：降为 E2 `co_presence_lead`，不得写成正式 coordination。
- X017 Army Community Group：需独立官网、税号、基地社区页或其他二次来源确认法律身份。
- F012 X013：维持 `grant_opportunity` + `no_public_evidence`，长期观察 USASpending / grants.gov award tab。
- X014 NED：本轮只覆盖 FY2024 亚洲清单，跨年度排除需另查。

## 4. 禁写清单

- 禁写 A002 SDCC 是边野古儒艮诉讼法律原告。
- 禁写 A008 是冲绳本地核心 actor 或稳定联盟成员。
- 禁写原 `与那国改革会議` 为已确认 actor。
- 禁写 A015 是与那国本地组织；它目前应写成八重山跨岛声援线索。
- 禁写共同署名自动构成稳定联盟，包括 2015 NACSJ 31 团体和 2020 MMC 71 团体。
- 禁写 AWWA 成员边等于某笔具体 donation recipient。
- 禁写 Okinawa Youth Council NOFO 已经拨款或已有公开 recipient。
- 禁写 TOFU 是 Okinawa Youth Council recipient；TOFU 是那霸市 / JICE 派遣项目，不能混同。
- 禁写 NED / USAID 已资助冲绳 NGO。
- 禁写 Peace Winds Japan 与冲绳基地 / 先岛安全网络存在已确认连接。

## 5. 数据表同步动作

主进程合并时应确认以下文件已纳入：

- `data/interim/01_actor_registry_initial_v0.csv`
- `data/interim/02_actor_aliases_initial_v0.csv`
- `data/interim/05_source_log_initial_v0.csv`
- `data/interim/07_actor_issue_edges_initial_v0.csv`
- `data/interim/08_actor_place_edges_initial_v0.csv`
- `data/interim/15_funding_or_support_edges_sample_v0.csv`
- `data/interim/human_review_log_v0.csv`
- `source_docs/source_archive/source_archive_manifest.csv`
- `source_docs/source_archive/S057` 至 `S092`
- `source_docs/source_archive/S007/raw.pdf`

## 6. 合并后推荐状态

- HR 阶段：closed for first-pass human review。
- LR 阶段：not started，本包不触发。
- 下一步优先级：
  1. 归档 36 条 pending URL。
  2. 处理 25 条 `inferred_url` 占位来源。
  3. 生成解释性图表包前，先按本包过滤禁写关系。
  4. 后续若启动 LR，优先与那国、军属慈善 recipient、外务省 / JICA / ONC。

