# USN07 组织官网／正式页面研究支持与决策建议 v1

状态：AI 证据核查完成；项目负责人于 2026-08-21 按本稿建议全部确认。研究日期：2026-08-21。

本文件服务于 `human_review_assignment_USN_actor_directory_v1.md` 的 65 项正式人工任务。下列内容原为**非约束性建议**；负责人已经全部确认，正式决定以 `outputs/actor_directory_v1/HR_USN_actor_directory_decisions_v1.csv` 和 `human_review_return_USN_actor_directory_v1.md` 为准。本轮只审 URL、`url_kind`、页面归属、当前可访问性和 evidence/source 追溯，不修改中央 actor registry、source log、archive manifest、关系表、前端或 publication adapter。

## 一页拍板表

| 分区 | 建议 | 数量 | 项目 |
|---|---:|---:|---|
| 40 项批量区 | `accept` | 36 | B001–B012、B015–B033、B035–B037、B039–B040 |
| 40 项批量区 | `defer` | 3 | B013、B014、B038 |
| 40 项批量区 | `reject` | 1 | B034 |
| 25 项冲突区 | `accept` | 18 | C001–C005、C007–C009、C013、C015–C018、C020–C023、C025 |
| 25 项冲突区 | `revise` | 4 | C006、C010、C011、C024 |
| 25 项冲突区 | `defer` | 2 | C014、C019 |
| 25 项冲突区 | `reject` | 1 | C012 |
| **合计** | **`accept 54 / revise 4 / defer 5 / reject 2`** | **65** | — |

这一结果不是对 40 项批量区的机械否定。36 项仍可一次确认；4 个例外来自 2026-08-21 的当前入口核查：两个诉讼网站返回 403 且无成功归档，一个域名 DNS 失效且无归档，一个历史 NOFO URL 当前只返回错误页。

## A 区：40 项批量区

### 建议一次接受的 36 项

建议将下列项目按候选 URL 和候选 `url_kind` 直接 `accept`：

- B001、B002、B003、B004、B005、B006、B007、B008、B009、B010、B011、B012：A001、A004、A005、A007、A008、A009、A016、A017、A019、A020、A047、A050；
- B015、B016、B017、B018、B019、B020、B021、B022、B023、B024、B025、B026、B027、B028、B029、B030、B031、B032、B033：A057、A062、A063、A066、A074、A075、A087、A089、A090、A091、A092、A093、A097、A098、A099、A101、A102、A105、A106；
- B035、B036、B037：A110、A112、X006；
- B039、B040：X014、X015。

这些行的组织名称、页面归属和页面类型一致，且均可由本包 `source_crosswalk_v1.csv` 回到中央 S-ID 或稳定 `WEB-*` 候选入口。`archive_status=failed` 不单独等于网址失效：例如 B030 与 B035 的页面仍有当前可见内容；B020 的防卫省页面虽然自动请求会触发访问控制，但官方域名、子单位归属与既有归档闭环完整。

B010/A020 与 B016/A062 也建议接受。两行的 `source_id/evidence_ref` 分别是 S061、S127，而首页候选由同一 actor-owned 域名规范化得出；派发包允许用 source ID 回到 crosswalk 的 selected row，校验器也能验证。因此这不是阻断性“证据引用错配”。若后续希望 URL 级追溯更精细，可另补首页专用 source metadata，但不必为此把现有决定降为 `defer`。

上述 36 行可统一采用简短 `review_note`：

> 已核对候选页面的组织名称、页面归属、页面类型与本包 evidence/source crosswalk；按候选 URL 与 url_kind 接受。该决定只批准名录查证入口，不批准组织立场、关系、资金、持续性、活动强度或影响力。

### 四个批量区例外

| 项目 | actor | 建议 | 证据、风险与可回填说明 |
|---|---|---|---|
| B013 | A052 嘉手納基地爆音差止訴訟原告団 | `defer` | `kadena-bakuon.jp` 的页面归属有外部正式材料支持，但 2026-08-21 自动访问返回普通 403，S151 归档也为 failed；本轮用户可见浏览器复判因浏览器连接自身超时而无效，不能据此升格或否定。建议 note：`页面归属有正式交叉材料支持，但当前入口返回403且S151无成功归档；暂不能确认可公开使用的现行入口。若负责人在普通浏览器可正常打开，可在拍板时改为accept。` |
| B014 | A053 普天間基地爆音訴訟団 | `defer` | `futenma-bakuon.jp` 当前返回 403，S156 归档失败；[沖縄合同法律事務所](https://okinawagodo.org/blog/1230/)明确称其为该诉讼团官网，故身份归属较清楚，缺口是当前可访问性。建议 note：`正式外部页面明确将该域名称为普天间基地爆音诉讼团官网，但当前入口返回403且S156无成功归档；暂缓至普通浏览器确认可访问。` |
| B034 | A108 沖縄を再び戦場にさせない県民の会 | `reject` | `kenminnokai.okinawa` 于 2026-08-21 DNS 不存在，HTTPS 无法建立连接，S146 也无成功归档。建议 note：`当前域名DNS不存在，HTTPS无法建立连接，S146归档亦失败；候选URL不满足当前可访问性或历史可恢复性。reject只否定这一名录入口，不否定actor本身。` |
| B038 | X013 Okinawa Youth Council Program | `defer` | S056 本地归档可证明该 URL 曾是美国驻日使领馆正式 NOFO PDF，但当前入口返回 `Technical Difficulties` HTML，而非 PDF。建议 note：`S056归档证明该URL曾是正式NOFO；当前入口仅返回Technical Difficulties错误页，暂不作为可访问的目录入口。NOFO只证明项目机会，不表示授奖或recipient关系。` |

## B 区：25 项冲突区

| 项目 | actor | 建议 | URL／类型与理由 |
|---|---|---|---|
| C001 | A002 SDCC | `accept` | 保留 `http://www.sdcc.jp/` / `official_site`。页面明确显示组织日英名称，当前 HTTP 入口可访问，S057 已归档；HTTPS 兼容性与页面较旧不等于组织终止。 |
| C002 | A033 Friends of the Earth U.S. | `accept` | 保留 [foe.org](https://foe.org/) / `official_site`。About 与页脚明确属于 FoE U.S.；`WEB-A033-20260819` 可回溯，后续补中央 source/archive。 |
| C003 | A040 Pro Public | `accept` | 保留 [propublic.org](https://propublic.org/) / `official_site`。官网名称、1991 年成立信息与 Kathmandu 地址一致；[FoEI Nepal 成员页](https://www.foei.org/member-groups/nepal/)将 Friends of the Earth Nepal 指向 Pro Public，排除近名错配。 |
| C004 | A042 Pacific Environment | `accept` | 保留 [pacificenvironment.org](https://www.pacificenvironment.org/) / `official_site`。组织名称、About 与当前联系方式一致；后续补中央 source/archive。 |
| C005 | A045 Center for Biological Diversity | `accept` | 保留 [biologicaldiversity.org](https://www.biologicaldiversity.org/) / `official_site`。About、页脚法人名与主体一致；后续补中央 source/archive。 |
| C006 | A046 Pro Natura | `revise` | 改为 [https://www.pronatura.ch/en](https://www.pronatura.ch/en) / `official_site`。原 [IUCN 成员页](https://iucn.org/our-union/members/iucn-members/pro-natura-friends-earth-switzerland)已确认 `Pro Natura / Friends of the Earth Switzerland` 并直接链接该自有站点；按本包排序规则，组织自有站点优先于 `official_registry`。 |
| C007 | A070 VFP-ROCK | `accept` | 保留 VFP 总部决议页 / `parent_org_page`。正文明确识别并列出 Veterans For Peace Ryukyu/Okinawa Chapter Kokusai；不显示为分会独立官网，也不由此延长组织持续期。 |
| C008 | A086 Turtle Island Restoration Network | `accept` | 保留 [seaturtles.org](https://seaturtles.org/) / `official_site`。首页组织名与 S228 同域正式 Form 990 闭环；后续补 actor-source crosswalk。 |
| C009 | A103 全国基地爆音訴訟原告団連絡会議 | `accept` | 保留 [成员站托管专页](https://bakuon.org/yonjitop/zenkoku.html) / `parent_org_page`。页面以全国连络会议本身为对象，列成立、宗旨、成员与总会；不推断成员间稳定联盟。 |
| C010 | A104 普天間基地爆音訴訟弁護団 | `revise` | 改为 [全国公害弁護団連絡会議的现行律师团名录](https://www.kogai-net.com/top/counsel/counsel_al/) / `parent_org_page`。原 S124 是案件报告；新页明确列团队名称、地址、联系人和电话。 |
| C011 | A107 沖縄YWCA | `revise` | 改为 [日本 YWCA 现行地域名录](https://www.ywca.or.jp/aboutus/japan/) / `parent_org_page`。原 S144 是专题文章；新页明确列 Okinawa YWCA、邮箱与正式社交入口。 |
| C012 | A109 第4次嘉手納基地爆音差止訴訟弁護団 | `reject` | `kadena-bakuon.jp` 是第4次原告团／案件入口，S151 与当前材料均未把它明确归属于律师团。reject 只表示未确认该团队的合格正式页面，不否定团队存在或诉讼角色。 |
| C013 | A114 全港湾沖縄地方本部 | `accept` | 保留 S289 PDF / `parent_org_page`。全国全港湾官网托管的正式报告页首明确署名该地方本部，URL 当前返回 PDF；它只作正式托管身份入口，不显示为分部独立官网，也不据此推断持续活动。 |
| C014 | A115 新日本婦人の会沖縄県本部 | `defer` | S280 当前页及归档内容均未出现“沖縄”“県本部”或地方组织名录，不能支持本 actor 的页面归属。全国官网另有具名联署材料可证身份，但不是合格目录入口；等待明确介绍冲绳县本部的正式名录／托管页。 |
| C015 | X001 USO Okinawa | `accept` | 保留 [USO Okinawa](https://okinawa.uso.org/) / `official_subunit`。地方站明确列 Okinawa Area Office、冲绳地点与 `@uso.org` 联系方式；不视为独立法人。 |
| C016 | X003 AEC | `accept` | 保留 [AEC 官网](https://www.aec-japan.co.jp/) / `official_site`。公司日英文名与宜野湾市冲绳总部一致；只核页面，不连带批准赞助或合同关系。 |
| C017 | X004 AWWA | `accept` | 保留 [NOSCO 托管的 AWWA 专页](https://nosco.wildapricot.org/awwa) / `parent_org_page`。页面明确命名 AWWA、相关俱乐部与联系邮箱；`parent_org_page` 在这里仅表示正式托管入口，不编码 NOSCO 对 AWWA 的治理／控制。 |
| C018 | X005 NOSCO | `accept` | 保留 [NOSCO About](https://nosco.wildapricot.org/About-Us) / `official_site`。页面明确完整组织名与用途；使用 `WEB-X005-20260819`，不能用 AWWA 页面 S055 冒充该 URL 的来源。 |
| C019 | X007 OESC | `defer` | `okinawaesc.com` 当前返回 404/Wix `ConnectYourDomain Error`；搜索缓存只能证明旧官网曾存在，尚未确认替代正式社交账号或现行正式页面。S041 是第三方报道，不能替代。 |
| C020 | X008 American Red Cross Okinawa | `accept` | 保留 [U.S. Naval Hospital Okinawa 托管页](https://okinawa.tricare.mil/About-Us/Employment-Opportunities/Volunteer-Red-Cross) / `official_subunit`。页面明确院内卫星办公室与 Camp Foster 主办公室；403 属站点访问策略，不标作红十字会独立官网。 |
| C021 | X009 NMCRS Okinawa | `accept` | 保留 [NMCRS Okinawa location](https://www.nmcrs.org/locations/okinawa-japan) / `official_subunit`。全国官网列 Camp Foster 地址、联系方式、开放时间与服务。 |
| C022 | X010 沖縄NGOセンター | `accept` | 保留 [oki-ngo.org](https://www.oki-ngo.org/) / `official_site`。组织名、地址、联系方式明确，S095 已归档；后续只修 actor-source crosswalk。 |
| C023 | X011 JICA沖縄 | `accept` | 保留 [JICA 沖縄](https://www.jica.go.jp/domestic/okinawa/index.html) / `official_subunit`。标题、面包屑与事务所栏目均明确地方据点。 |
| C024 | X012 TOMODACHI Initiative | `revise` | 改为 [https://usjapantomodachi.org/](https://usjapantomodachi.org/) / `official_site`。原 [U.S.-Japan Council 项目页](https://www.usjapancouncil.org/tomodachi/)正式链接该专属站点；新站含 Staff、Reports、Current Programs 和 2026 更新。项目仍非独立法人。 |
| C025 | X016 MOSCO | `accept` | 保留 [moscoki.com](https://www.moscoki.com/) / `official_site`。页面明确完整组织名、Board、Membership、Philanthropy 与组织邮箱；排除 NOSCO/AWWA 页面作为本 actor 入口。 |

## 四项 `revise` 的建议回填文字

### C006 / A046

`revised_url=https://www.pronatura.ch/en`；`revised_url_kind=official_site`

> 原 IUCN 成员页确认 Pro Natura 与 Friends of the Earth Switzerland 为同一成员实体并链接其自有站点。按官网优先规则改用 Pro Natura 自有英文站，类型改为 official_site；新 URL 后续补 WEB evidence ref、source metadata 与归档。本决定不连带批准 IUCN/FoEI 关系或持续性。

### C010 / A104

`revised_url=https://www.kogai-net.com/top/counsel/counsel_al/`；`revised_url_kind=parent_org_page`

> 原 S124 为案件报告，不宜作为律师团目录入口。改用全国公害弁護団連絡会議“活動中の弁護団”现行正式名录；该页明确列普天間基地爆音訴訟弁護団及联系信息。新 URL 后续补 WEB evidence ref、source metadata 与归档。

### C011 / A107

`revised_url=https://www.ywca.or.jp/aboutus/japan/`；`revised_url_kind=parent_org_page`

> 原 S144 是日本 YWCA 专题文章。改用日本 YWCA 现行地域名录；页面明确列 Okinawa YWCA、联系邮箱与正式社交入口，作为 parent_org_page 更稳定。新 URL 后续补 WEB evidence ref、source metadata 与归档，不标作独立官网。

### C024 / X012

`revised_url=https://usjapantomodachi.org/`；`revised_url_kind=official_site`

> U.S.-Japan Council 正式项目页明确把 usjapantomodachi.org 链接为 TOMODACHI website；该专属站有 Staff、Reports、Current Programs 与 2026 更新，故改用该 URL 并标 official_site。项目不是独立法人；新 URL 后续补 WEB evidence ref、source metadata 与归档。

## 拍板后的受控动作

若负责人按本稿确认，下一步只做本任务书允许的回填与回传：

1. 填写 65 行最后六列；`accept` 行不改 URL，4 个 `revise` 行写入上述新 URL 与类型；5 个 `defer`、2 个 `reject` 保留清楚的限制理由。
2. 生成独立 `human_review_return_USN_actor_directory_v1.md` 和 post-return validator；不为通过 pre-human validator 而清空决定。
3. 新 URL 与未归档 `WEB-*` 只形成待整合的 source/archive 动作清单。现阶段不修改中央 source log 或 archive manifest，也不静默覆盖失败／历史快照。
4. 本任务通过只意味着“可作为组织名录查证入口”。不得据此新增 actor、关系、资金、活动连续性、立场或现实影响结论。
5. 第3份回传完成并暂停后，再进入第4份“43条旧关系归位”的 6 项分组研究。
