# Actor directory candidate v1

本包为 121 个当前有效 actor 建立“官网／正式组织页面”候选目录。它解决的是名录展示与查证入口问题，不是对组织立场、关系、资金来源或影响力的新增判断。

## 当前结果

- 中央 registry 有 122 条历史记录；本包排除已并入 A071 的 A072，恰好输出 121 个当前有效 actor。
- 65 个 actor 有合格页面候选：48 个组织官网、7 个官方子页面、1 个官方登记页、9 个母组织页面。
- 56 个 actor 暂未在其已关联来源中确认合格页面，统一标记为 `not_found`。
- 17 个 `us_origin` actor 已逐个重点核对，其中 16 个有页面候选；X017 Army Community Group of Okinawa 暂未找到可确认的组织自有页面。
- 65 个页面候选中，48 个所选来源已有本地归档，6 个来源归档抓取失败，11 个是尚未进入中央归档的新网址候选。

`not_found` 只表示本轮有边界的来源检查没有找到合格页面，不表示组织没有网络活动、已经停止运作或不重要。

## 文件

- `actor_directory_candidate_v1.csv`：每个有效 actor 一行的目录候选层。
- `coverage_summary_v1.csv`：总体、来源地与 actor class 分组的页面覆盖情况。
- `official_url_conflicts_v1.csv`：多域名、母组织页面、来源类型误标和无官网等需要人工判断的冲突。
- `source_crosswalk_v1.csv`：actor 来源引用、中央 source log、归档状态、候选网址与取舍理由的逐行追溯。
- `manifest.json`：输入、输出、哈希、计数与硬性校验结果。
- `docs/actor_directory_frontend_slice_v1.md`：人工审定后进入前端第一张组织名录表的字段、交互和验收要求。

## USN07 人工复核包

- `HR_USN_actor_directory_decisions_v1.csv`：65 个非 `not_found` 页面候选的空白负责人决定表；前 40 行为可批量确认区，后 25 行为逐行冲突区。
- `docs/human_review_assignment_USN_actor_directory_v1.md`：复核范围、决定语义、25 项冲突说明与回交要求。
- `scripts/validate_hr_usn_actor_directory_v1.py`：验证 65 行、40＋25 分区、actor 唯一、证据回溯和决定字段为空。

该复核只批准页面 URL、页面类型、页面归属、可访问性和来源追溯，不批准组织立场、关系、资金、持续性或影响力。

## 页面类型

- `official_site`：组织自有网站、长期自有博客或组织正式社交页面。
- `official_subunit`：上级机构官网内的冲绳分支、地方办公室或正式项目页面。
- `official_registry`：政府或正式行业／成员登记系统内的组织页面。
- `parent_org_page`：母组织官网中能够明确确认该地方组织、分会、诉讼团队或项目的页面；不能显示成独立官网。
- `not_found`：没有确认到以上四类页面。

新闻报道、活动日历、第三方介绍、共同声明、法院材料和一般证据页都不会仅因提到组织就成为 `official_url`。例如 S041 的 Okinawa Hai 页面虽曾被标成 `organization_site`，实际是第三方报道，本包明确排除；S051 是已知归档错配，也不得支持 A011。

## 生成方法

1. 从 `01_actor_registry_initial_v0.csv` 取得当前 actor 和 `source_refs`，排除 A072。
2. 将 actor 的直接来源引用与 source log 中明确带该 actor ID 的支持说明展开到 `source_crosswalk_v1.csv`。
3. 只让能够证明页面归属的 source type 进入候选排序；组织官网优先于官方子页面、正式登记页和母组织页面。
4. 对 17 个 `us_origin` actor 逐个检查当前官方页面；新发现的网址保留为空 `source_id`，因为本包无权改中央 source log。
5. 对已知错配、多个可信域名、母组织代管页和无法确认的情况写入冲突表，等待字段级人工复核。

名称字段保留 registry 原名，并在可用时提供日文和英文展示名。项目目前没有一套经人工复核的 121 组织中文译名，因此 `name_zh` 暂留空；前端不可用机器临时翻译覆盖原名。英文名沿用项目既有英文展示 crosswalk，仍属于本候选包的一部分。

## 使用边界

本包状态为 `candidate_only_not_central_not_frontend_ready`：

- 未修改 actor registry、source log、archive manifest 或前端数据包。
- 所有页面候选的 `review_status_candidate` 仍是候选状态，不应出现在“已核视图”。
- 官方页面只证明一个可供查证的组织入口；不能由此推断组织亲美／反美、资金来源、组织关系、政治立场、持续性或现实影响力。
- 页面覆盖率反映资料发现能力，也会受组织保存网站、使用英文和拥有专业传播资源等条件影响，不能作为网络中心性或组织重要性的替代指标。

人工复核应逐项确认页面归属、页面类型、当前可访问性和 source 追溯。通过后，再由受控合并器写入正式目录 overlay，并经 publication compiler 生成前端数据；前端不得直接读取本目录中的 CSV。

## 已执行校验

- 输出恰好 121 行，actor ID 唯一。
- A072 不在输出中，17 个 `us_origin` actor 全数在表。
- `url_kind` 只使用五个允许值。
- 非 `not_found` 行均为 HTTP(S) URL；`not_found` 行 URL 为空。
- 任何非空 `source_id` 都能回溯中央 source log，并在 crosswalk 中有选中记录。
- S051 和 Okinawa Hai 第三方页面均未被选为官网。
