# USN07 组织官网／正式页面负责人回传 v1

状态：项目负责人于 2026-08-21 按 `human_review_research_USN_actor_directory_v1.md` 的全部建议拍板；65 项决定已写入 `outputs/actor_directory_v1/HR_USN_actor_directory_decisions_v1.csv`。

本回传只批准目录 URL、`url_kind`、页面归属、当前可访问性和证据追溯。它不批准组织立场、关系、资金、持续性、活动强度、影响力或其他 registry 字段，也不执行中央合并或前端发布。

## 决定汇总

| 决定 | 数量 | 项目 |
|---|---:|---|
| `accept` | 54 | 批量区 B001–B012、B015–B033、B035–B037、B039–B040；冲突区 C001–C005、C007–C009、C013、C015–C018、C020–C023、C025 |
| `revise` | 4 | C006、C010、C011、C024 |
| `defer` | 5 | B013、B014、B038、C014、C019 |
| `reject` | 2 | B034、C012 |

所有行均记录 `reviewer=project_principal_user`、`review_date=2026-08-21` 和非空 `review_note`。

## 四项 URL／类型修订

| 项目 | actor | 批准 URL | 批准类型 | 修订原因 |
|---|---|---|---|---|
| C006 | A046 Pro Natura | `https://www.pronatura.ch/en` | `official_site` | IUCN 成员页确认身份并链接组织自有站点；按官网优先规则替换 registry 页面 |
| C010 | A104 普天間基地爆音訴訟弁護団 | `https://www.kogai-net.com/top/counsel/counsel_al/` | `parent_org_page` | 原 S124 是案件报告；现行正式名录明确列律师团及联系方式 |
| C011 | A107 沖縄YWCA | `https://www.ywca.or.jp/aboutus/japan/` | `parent_org_page` | 原 S144 是专题文章；现行地域名录明确列地方组织和联系入口 |
| C024 | X012 TOMODACHI Initiative | `https://usjapantomodachi.org/` | `official_site` | U.S.-Japan Council 正式项目页链接该专属站点，且站点有现行项目、人员与报告栏目 |

这些新 URL 后续需要稳定 `WEB-*` evidence ref、中央 source metadata 和独立归档；本回传不直接写 source log 或 archive manifest。

## 暂缓与拒绝边界

- B013/A052 与 B014/A053：域名归属有正式交叉材料，但当前返回 403，且 S151/S156 均无成功归档；保持 `defer`。日后若负责人能在普通浏览器稳定打开，可重新提交。
- B038/X013：S056 证明历史 NOFO，但当前 URL 返回错误页；保持 `defer`。NOFO 不因此变成 award 或资金边。
- C014/A115：S280 当前页和归档均未明确列沖縄県本部；保持 `defer`，等待正式地方名录／托管页。
- C019/X007：旧域名当前返回 404/Wix 域名未连接，替代官方入口未核实；保持 `defer`，且 S041 第三方报道不得替代。
- B034/A108：域名 DNS 不存在且无成功归档；`reject` 只否定该 URL，不否定 actor。
- C012/A109：候选页属于第4次嘉手纳原告团／案件，不是已确认的律师团页面；`reject` 不否定律师团存在或诉讼角色。

## 接受项的共同边界

- B010/A020 与 B016/A062 的中央 S-ID 是同一 actor-owned 域名内的原始材料，crosswalk 可追到规范化首页；后续可补首页专用 source metadata，但不构成阻断。
- 防卫省、TRICARE 等页面的自动请求限制不否定已有官方域名、页面归属和归档闭环；接受只表示目录入口可用。
- `parent_org_page`／正式托管页不表示治理、控制、membership、联盟或独立法人资格。
- 活动报告 PDF、历史博客或仍可访问的旧页面只承担本回传明确限定的页面身份，不据此推断组织当前活跃或持续性。

## QA 与下一步

- 回填表仍为 65 行、65 个唯一 actor，40＋25 分区不变。
- 决定分布为 `accept 54 / revise 4 / defer 5 / reject 2`；决定、note、reviewer 和日期无空值。
- 4 个 `revise` 均有合法 HTTP(S) URL 与允许的 `url_kind`；其余 61 行修订字段为空。
- 与原派发版相比，前 25 个非负责人字段零漂移。
- `python scripts/validate_hr_usn_actor_directory_return_v1.py` 已通过；本任务保持已回传、未中央合并状态。第4份关系归位和五项 USN 架构检查点也已完成，下一步进入受控集成设计。
