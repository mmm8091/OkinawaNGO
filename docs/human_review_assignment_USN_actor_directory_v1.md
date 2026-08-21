# USN07 人工复核任务：组织官网／正式页面

任务编号：`USN07-DIR-v1`

日期：2026-08-19

回填表：`outputs/actor_directory_v1/HR_USN_actor_directory_decisions_v1.csv`

状态：项目负责人已于 2026-08-21 按研究支持稿确认全部建议；65 项决定已回填。研究支持见 `docs/human_review_research_USN_actor_directory_v1.md`，正式回传见 `docs/human_review_return_USN_actor_directory_v1.md`。

## 这次只审什么

本任务只决定五个页面字段：

1. `official_url` 是否确实属于该 actor，或属于明确托管该 actor 的正式上级机构／登记机构；
2. `url_kind` 是否正确；
3. 页面归属能否从页面标题、页脚、About、机构域名或正式名录确认；
4. 页面当前是否可以访问；
5. `source_id` 或 `WEB-*` evidence ref 是否能回到本包的 source crosswalk。

这次不审组织的亲美／反美立场，不审组织关系、资金、持续性、活动强度、影响力，也不连带批准其他 registry 字段。一个网址通过，只表示它可以作为名录里的正式查证入口。

## 填写方法

只填写回填表最后六列；AI 没有预填任何决定：

- `decision=accept`：候选 URL、页面类型、页面归属和证据入口均可接受。
- `decision=revise`：需要改 URL 或页面类型；同时填写 `revised_url`、`revised_url_kind` 和 `review_note`。若网址是新发现的，在 note 中写清证据入口。
- `decision=defer`：现有材料不足，暂不发布。
- `decision=reject`：该页面不属于这个 actor，或只是新闻／案件／活动页面；该 actor 返回“暂未确认正式页面”，不会从 registry 删除。

允许的 `revised_url_kind` 只有：

- `official_site`：组织自有网站、长期自有博客或经确认的正式组织社交页面；
- `official_subunit`：上级机构官网内的冲绳分支、地方办公室或正式项目页面；
- `official_registry`：政府或正式成员登记系统的组织页面；
- `parent_org_page`：母组织或上级机构官网中明确介绍该地方组织、分会、团队或项目的页面。

新闻报道、活动日历、法院材料和第三方介绍不能改成 `official_site`。页面打不开时先看 `archive_status`：只有历史归档能证明身份但当前入口已经失效，可填 `defer` 或 `reject` 并在 note 说明。

## A 区：40 项可批量确认

这 40 行没有进入当前冲突队列，都已有唯一的候选页面和证据入口。建议在浏览器中批量打开链接，确认页面名称和归属后，将整区 `decision` 一次填为 `accept`；任何例外仍逐行改为 `revise`、`defer` 或 `reject`。

范围为回填表中的 `USN07-DIR-B001`—`USN07-DIR-B040`：

| 项目 | actor | 页面类型 | 证据 |
|---|---|---|---|
| B001–B010 | A001, A004, A005, A007, A008, A009, A016, A017, A019, A020 | 组织官网 | S006, S004, S003, S005, S065, S009, S052, S022, S049, S061 |
| B011–B020 | A047, A050, A052, A053, A057, A062, A063, A066, A074, A075 | 官网／官方子页面 | S031, S037, S151, S156, S034, S127, S038, S032, S043, S047 |
| B021–B030 | A087, A089, A090, A091, A092, A093, A097, A098, A099, A101 | 组织官网 | S230, S105, S106, S107, S109, S110, S114, S115, S116, S120 |
| B031–B040 | A102, A105, A106, A108, A110, A112, X006, X013, X014, X015 | 官网／官方子页面 | S121, S125, S126, S146, S153, S158, S075, S056, S086, S087 |

每一行仍单独保留 `decision`、`revised_url`、`revised_url_kind` 和 `review_note`，因此批量确认不会阻止负责人修正个别页面。

## B 区：25 项必须逐行决定

回填表的每一行还保留候选网址、source title、source URL、archive status、原始冲突入口和完整说明。下面的“建议”只是复核路径，不是决定。

| 项目 | actor | 冲突说明 | 建议判断 | 证据入口 |
|---|---|---|---|---|
| USN07-DIR-C001 | A002 | 同一 actor 有组织自有域名、IUCN 成员页和 GEOC 名录页；三者的页面归属和类型不同。 | 先核对 sdcc.jp 是否仍由该组织持有且可访问。若属实，建议 accept + official_site；否则在 IUCN／GEOC 页面中选择并相应改为 official_registry。 | [S057](http://www.sdcc.jp/) |
| USN07-DIR-C002 | A033 | foe.org 是本轮定向找到的官网候选，但尚无中央 source ID，也未进入本地归档。 | 核对页面页脚或组织介绍是否明确属于 Friends of the Earth U.S.；属实可 accept，后续另行登记来源与归档。 | [WEB-A033-20260819](https://foe.org/) |
| USN07-DIR-C003 | A040 | propublic.org 与 FoE Nepal 成员页同时进入候选，但可能对应不同实体，存在名称近似或历史来源错配风险。 | 逐项核对 Forum for Protection of Public Interest (Pro Public) 的正式英文名与所属国；仅在实体一致时 accept，否则 revise 或 defer。 | [S089](https://propublic.org/) |
| USN07-DIR-C004 | A042 | pacificenvironment.org 是本轮定向找到的官网候选，但尚无中央 source ID，也未进入本地归档。 | 核对页面组织名与主体归属；属实可 accept，后续另行登记来源与归档。 | [WEB-A042-20260819](https://www.pacificenvironment.org/) |
| USN07-DIR-C005 | A045 | biologicaldiversity.org 是本轮定向找到的官网候选，但尚无中央 source ID，也未进入本地归档。 | 核对页面组织名与主体归属；属实可 accept，后续另行登记来源与归档。 | [WEB-A045-20260819](https://www.biologicaldiversity.org/) |
| USN07-DIR-C006 | A046 | IUCN 成员页和 Friends of the Earth International 瑞士成员页都能指向 Pro Natura，但都不是独立官网。 | 确认两页是否指向同一法律实体；保留 IUCN 时建议 accept + official_registry，改用 FoEI 页面时建议 revise + parent_org_page。 | [S091](https://iucn.org/our-union/members/iucn-members/pro-natura-friends-earth-switzerland) |
| USN07-DIR-C007 | A070 | 页面由 Veterans For Peace 总部托管并提到 VFP-ROCK，不是分会独立网站。 | 若正文明确识别该冲绳分会，建议 accept + parent_org_page；不能确认分会身份则 reject 或 defer。 | [S048](https://www.veteransforpeace.org/who-we-are/2025-online-business-meeting/resolution-2025-1-us-military-expansion-and-environmental-destruction-okinawa) |
| USN07-DIR-C008 | A086 | seaturtles.org 是 TIRN 直接官网，但依据来自 source log 其他位置的 S228，不在 actor 原 source_refs 中。 | 核对官网归属与可访问性；属实可 accept + official_site，并在后续受控合并时补 actor-source 追溯。 | [S228](https://seaturtles.org/) |
| USN07-DIR-C009 | A103 | 全国连络会议页面托管在成员原告团网站 bakuon.org 内，不是独立域名。 | 若页面明确以全国连络会议自身为对象，建议 accept + parent_org_page；若只是成员团体叙述，则 defer 或 reject。 | [S122](https://bakuon.org/yonjitop/zenkoku.html) |
| USN07-DIR-C010 | A104 | 律师团资料由全国公害律师网络托管，不是该诉讼律师团独立网站。 | 核对页面是否明确识别普天间律师团；属实可 accept + parent_org_page，否则 reject。 | [S124](https://www.kogai-net.com/sokai-document/document38/38-200/38-223/) |
| USN07-DIR-C011 | A107 | 页面是日本 YWCA 对冲绳 YWCA 的正式介绍，不是冲绳 YWCA 独立官网。 | 若名称和地域组织身份一致，建议 accept + parent_org_page；不要改成 official_site。 | [S144](https://www.ywca.or.jp/kaze/0214news-2/) |
| USN07-DIR-C012 | A109 | 所选页面属于第4次嘉手纳原告团，未必是律师团自己的正式页面。 | 只有页面明确识别第4次律师团时才 accept + parent_org_page；若只能证明案件或原告团，应 reject。 | [S151](https://kadena-bakuon.jp/) |
| USN07-DIR-C013 | A114 | 所选入口是全国港湾官网托管的冲绳地方本部报告 PDF，不是分部主页。 | 若 PDF 明确识别该地方本部，可 accept + parent_org_page；若希望正式页面必须可持续导航，可 defer 寻找分部页。 | [S289](https://www.zenkowan.org/wp-content/uploads/2025/06/%E6%B2%96%E7%B8%84%E5%9C%B0%E6%96%B9%E3%80%80%E6%AF%94%E5%98%89%E5%8B%81%E5%B8%8C.pdf) |
| USN07-DIR-C014 | A115 | 页面是新日本妇人之会全国组织的地方组织名录，不是冲绳县本部独立主页。 | 若名录明确列出冲绳县本部，建议 accept + parent_org_page；不要改成 official_site。 | [S280](https://www.shinfujin.gr.jp/about/organization) |
| USN07-DIR-C015 | X001 | USO Okinawa 官方地方站点已定位，但 registry 仍保留未解析的旧 X001 来源引用，当前网址没有中央 source ID。 | 核对页面归属和可访问性；属实可 accept + official_subunit，来源登记留给后续受控合并。 | [WEB-X001-20260819](https://okinawa.uso.org/) |
| USN07-DIR-C016 | X003 | AEC 官网已定位，但 registry 仍保留未解析的旧 X003 来源引用，当前网址没有中央 source ID。 | 核对公司名称和冲绳主体；属实可 accept + official_site，来源登记留给后续受控合并。 | [WEB-X003-20260819](https://www.aec-japan.co.jp/) |
| USN07-DIR-C017 | X004 | NOSCO 官网内的 AWWA 页面与 AWWA 官方 Facebook 均可作为入口；前者是母组织托管页，后者是组织社交页面。S041 为第三方报道，不能采用。 | 优先判断希望展示的入口：NOSCO 页面应 accept + parent_org_page；若改用经核实的官方 Facebook，应 revise + official_site。 | [S055](https://nosco.wildapricot.org/awwa) |
| USN07-DIR-C018 | X005 | 现有 S055 指向 NOSCO 的 AWWA 页面，不是 NOSCO About 页；当前官网候选尚无中央 source ID。 | 核对 NOSCO About 页归属；属实可 accept + official_site，后续新增正确 source 行，不能沿用 S055 充当该网址来源。 | [WEB-X005-20260819](https://nosco.wildapricot.org/About-Us) |
| USN07-DIR-C019 | X007 | 历史 S041 被标成 organization_site，但实际是 Okinawa Hai 第三方报道；当前 OESC 官网是新发现候选。 | 核对 okinawaesc.com 的组织归属；属实可 accept + official_site，且明确不以 S041 支持该网址。 | [WEB-X007-20260819](https://www.okinawaesc.com/) |
| USN07-DIR-C020 | X008 | 红十字会冲绳入口位于美军医疗系统官网的地方志愿服务页，且无中央 source ID。 | 若页面明确对应 American Red Cross Okinawa，建议 accept + official_subunit；不要标成独立官网。 | [WEB-X008-20260819](https://okinawa.tricare.mil/About-Us/Employment-Opportunities/Volunteer-Red-Cross) |
| USN07-DIR-C021 | X009 | NMCRS Okinawa 是全国机构官网内的地方 location 页，且无中央 source ID。 | 若地点和机构名称一致，建议 accept + official_subunit。 | [WEB-X009-20260819](https://www.nmcrs.org/locations/okinawa-japan) |
| USN07-DIR-C022 | X010 | 官网 S095 已在 source log 中，但 actor registry 仍保留未解析的旧 X010 来源引用。 | 核对 oki-ngo.org 归属；属实可 accept + official_site，后续仅修复 actor-source crosswalk。 | [S095](https://www.oki-ngo.org/) |
| USN07-DIR-C023 | X011 | JICA 冲绳页面位于 JICA 全国官网内，且当前网址无中央 source ID。 | 若页面明确是 JICA Okinawa，建议 accept + official_subunit；不要标成独立官网。 | [WEB-X011-20260819](https://www.jica.go.jp/domestic/okinawa/index.html) |
| USN07-DIR-C024 | X012 | TOMODACHI 页面由 U.S.-Japan Council 托管，且当前网址无中央 source ID。 | 核对页面是否为该项目当前正式入口；属实可 accept + parent_org_page。 | [WEB-X012-20260819](https://www.usjapancouncil.org/tomodachi/) |
| USN07-DIR-C025 | X016 | MOSCO 官网与 NOSCO/AWWA 页面同时出现在候选来源链中，后者属于不同组织。 | 核对 moscoki.com 的 MOSCO 身份；属实可 accept + official_site，并排除 NOSCO/AWWA 页面作为本 actor 入口。 | [S079](https://www.moscoki.com/) |

## 回交要求

1. 65 行 `decision` 全部填写；没有修改 URL 时保持 `revised_url` 和 `revised_url_kind` 为空。
2. `revise` 必须填写新 URL、新类型和简短理由；`defer`／`reject` 必须在 `review_note` 写明缺口或排除原因。
3. 不改 actor registry、source log、archive manifest 或前端。负责人只回交本 CSV。
4. 回交后先运行：

```powershell
python scripts\validate_hr_usn_actor_directory_v1.py
```

当前校验器要求所有决定字段为空，用于验证派发包。负责人回交后，合并线程应另建 return validator，不能为通过本检查而清空决定。

## 派发包验收

- 决定表恰好 65 行，与 `actor_directory_candidate_v1.csv` 中全部非 `not_found` actor 一一对应。
- A 区 40 行、B 区 25 行；actor ID 唯一，A072 不出现。
- 25 个冲突行均有冲突说明、建议判断和证据入口。
- 所有 65 个候选都能通过 `source_crosswalk_v1.csv` 回溯；没有中央 S-ID 的新网址使用稳定 `WEB-*` evidence ref。
- `decision`、`revised_url`、`revised_url_kind`、`review_note`、`reviewer`、`review_date` 在派发时全部为空。
