# 研究发布架构 v1

日期：2026-07-20  
状态：架构整改完成；生产部署待授权  
上位依据：一期研究方案、中央 coding schema、人工复核规则与
`docs/adr/0001-compiled-research-publication-snapshot.md`

## 1. 结论

静态站不是研究效率瓶颈。过去真正的缺口，是中央事实、模块分析和页面之间没有唯一的研究
发布 seam：旧核心数据包能绕过资产 catalog，React 也可能直接读取混合关系或候选包。

当前唯一合法路径为：

```text
研究方法与编码规则
  → 中央事实／模块观察
  → 可重复分析
  → 人工解释门禁
  → publication catalog + core surface registry
  → profile 专属投影与 adapter
  → 不可变 publication snapshot
  → render-only React/Vite
```

前端不扫描 `outputs/`，不直接读取中央 CSV，不根据文件存在决定展示资格，也不在浏览器内
生成研究分类、分母或主张。需要新增展示时，只改发布模块和受控 metadata；页面调用
interface 不变。

## 2. 分层模型

| 层 | 对象 | 不能自动升级成 |
|---|---|---|
| L0 | 方法、编码、证据和复核规则 | 页面配置 |
| L1 | 中央事实／有界研究观察 | 解释性结论 |
| L2 | 带单位、分母和版本的分析结果 | 因果机制 |
| L3 | 带竞争解释和强度的研究主张 | 总体规律 |
| L4 | 问题导向的模块与展品 | 独立“漂亮图” |
| L5 | profile 专属不可变快照 | 新事实源 |
| L6 | render-only 前端 | 方法裁判 |

`evidence_level`、`review_status`、`human_decision`、`method_status`、
`claim_status`、`surface_eligibility` 和 `frontend_status` 分轴保存，不压成一个
`verified` 或 `ready` 字段。

## 3. 深模块与 interface

研究发布模块位于 `research_publication/`。外部只需学习三个操作：

```python
compile_publication_snapshot(project_root, output_dir, profile, channel_file)
verify_publication_snapshot(snapshot_dir)
verify_publication_channel(project_root, channel_file, expected_profile)
```

复杂实现——源文件读取、JSON pointer 投影、profile 行过滤、catalog 门禁、三语覆盖、内部
字段裁剪、对象 envelope、追溯、哈希、不可变保存和 channel 原子切换——全部留在该模块内。

## 4. 两道互补准入门

### 4.1 研究资产 catalog

`data/metadata/research_publication_catalog_v1.json` 登记研究问题、分析单位、选择边界、方法
状态、主张强度、允许措辞、解释限制、目标页面和 release profile。

完整模块只有 `frontend_status=integrated` 才进入公开 publication object index。
`adapter_needed_partial_existing` 只允许登记过的有限事实子层继续作为导航或查询面，不能被称为
完整模块。

### 4.2 Core surface registry

`data/metadata/research_publication_core_surfaces_v1.json` 对核心 builder 的每一个输出作出显式
处置。每个公开 surface 都有：

- `source_path` 与可选 `json_pointer`；
- 独立 `output_path`；
- `surface_status`；
- catalog owner；
- release profiles；
- 前端消费者与解释限制；
- 必要时的 profile 行过滤。

编译器要求 registry 的 source-path 并集与 builder manifest 完全相等。未登记输出、登记了
不存在的输出、owner 未过方法门禁、公开 profile 超过 owner 权限，都会整体失败。

旧 `demo/relations.json` 与 `research/candidates.json` 不再进入公开快照。编译器把其各关系族
投影为独立物理文件，例如：

```text
core/relations/actor_issue.json
core/relations/strict_place_issue.json
core/events/participation.json
core/legal/roles.json
research/actor_issue.json
research/episodes.json
research/dyadic_relations.json
```

因此，开放某一候选族不会顺带公开其他候选族。前端未消费的 `views/global.json`、
`views/overview.json`、`views/actors.json`、重复 lifecycle 文件等也不进入公开站。

## 5. Core surface 四态

| 状态 | 含义 |
|---|---|
| `architecture_required` | 地图几何、控制词表、证据抽屉等无独立研究主张的基础表面 |
| `module_integrated` | 已通过方法门禁并属于完整发布对象 |
| `partial_bounded` | 方法安全的有限事实子层；完整模块仍缺 adapter 或下钻 |
| `internal_only` | 旧投影、诊断或重复文件，仅供内部审计 |

当前四个有限 core surface owner 为：

- `PUB-MR-001`：组织身份、组织—议题已核／候选导航；尚缺行级来源下钻；
- `PUB-MR-003`：同源地点—议题计数；尚缺 actor→source→event 下钻；
- `PUB-MR-008`：actor 面板中的案件角色事实；尚缺六案 case＋role 完整比较；
- `PUB-MR-011`：关系面板中的行政／金额边界子层；不等于 R10 正式模块全部接入。

它们可以展示安全事实，但不能被同步稿写成“该模块已经完成前端集成”。

## 6. Publication object envelope

每个完整发布对象都由编译器附加同一 envelope：

```text
catalog_id
release_profile
method_status
claim_status
analysis_unit
selection_boundary
allowed_wording
interpretation_limit
```

adapter 不能自行改写这些字段。验证器逐对象核对 envelope、公开 catalog 和 object index。
核心完整模块使用 `views/core_surfaces/<PUB-ID>.json` 描述其物理 surfaces；专用 adapter
使用 `exhibits/<PUB-ID>.json`。

## 7. Release profiles 与物理隔离

| profile | 用途 | 物理规则 |
|---|---|---|
| `reviewed` | 对外已核包 | 不存在 `research/`；R4 QA-safe 层、F027 等未完成人审记录均不存在 |
| `client_preview` | 甲方探索站 | 已核＋显式标记研究层；内部 locator／复核备注不存在 |
| `internal` | 团队审计 | 可含内部诊断和完整 catalog；不得部署 |

输出固定为：

```text
outputs/publication_releases_v1/<profile>/<release_id>/
outputs/publication_channels_v1/<profile>.json
```

profile 默认 channel 已按 profile 派生。编译先进入 staging，验证通过后保存不可变 release，
最后原子切换相应 channel；失败保留上一个有效 release。

`--verify-only` 不只验 snapshot，还核对 channel 的 profile、release ID、snapshot 路径和
manifest SHA-256。Vite 构建时再次验证活动 `client_preview` channel，不能直接相信指针。

## 8. 失败行为

| 失败 | 行为 |
|---|---|
| 必需输入、翻译或引用缺失 | 构建失败，不生成空数组替代 |
| builder 多出／少出文件 | 构建失败 |
| core output 未被 surface registry 决定 | 构建失败 |
| owner 未 integrated／explicit partial | 构建失败 |
| retired 或 candidate hypothesis 进入公开层 | 构建失败 |
| publication envelope 与 catalog 不一致 | 构建失败 |
| snapshot 多出未校验文件 | 验证失败 |
| research payload 与 profile 不一致 | 验证失败 |
| 前端必需 JSON 加载失败 | 显示发布错误，不解释成零记录 |
| 证据抽屉读取失败 | 显示明确错误，不永久停在“加载中” |

## 9. 当前已进入架构的内容

当前 catalog 为 26 项：

- 3 个 architecture objects 已集成；
- 5 个方法模块完整集成；
- 4 个模块只有 `partial_bounded` core surface；
- 5 个方法模块尚无公开 surface；
- 5 个候选研究仍在方法／负责人门禁；
- 4 个 retired 家族永久禁止发布。

完整 object index 共 8 项：

| ID | 内容 | 类型 |
|---|---|---|
| PUB-ARC-001 | 五条生命周期锚点 | core |
| PUB-ARC-002 | 类型化关系／非关系分层 | core |
| PUB-ARC-003 | 经核事件参与事实层 | core |
| PUB-MR-004 | 先岛三地框架语料 | exhibit |
| PUB-MR-005 | 三次名单与重复参与 | exhibit |
| PUB-MR-012 | 官方 616 行协作来源总体 | exhibit |
| PUB-MR-013 | 六维覆盖与可见性审计 | core |
| PUB-MR-014 | 13 个制度转译 episode | core |

这不等于一期报告、论文、PPT 或 26 项 catalog 全部完成。

## 10. 部署边界

可部署边界只有：

```text
prototypes/nr3_explorer/dist/
```

生产 stamp 写入：

- publication release ID 与 manifest hash；
- site release ID 与前端 tree hash；
- base path；
- Git commit；
- dirty 状态与脏路径数；
-内部泄漏检查和 payload 文件数。

外部 Google Fonts 依赖已经移除，避免中国网络可用性和第三方请求问题。Hash routing 不要求
OSS 为每个页面配置服务端重写。根域使用 `VITE_BASE_PATH=/`；子路径必须以真实 base path
重新构建。

静态架构在当前规模下是合适的。只有出现多人实时写入、动态权限、服务端秘密、超大查询或
用户写回时，才需要重新评估后端。

## 11. 复现

```powershell
python -m unittest `
  tests.test_build_exploration_system_data_v1 `
  tests.test_research_publication_compiler_v1 `
  tests.test_publication_adapter_r4 `
  tests.test_publication_adapter_r5 `
  tests.test_publication_adapter_r10

python scripts\build_publication_snapshot_v1.py --profile reviewed
python scripts\build_publication_snapshot_v1.py --profile reviewed --verify-only
python scripts\build_publication_snapshot_v1.py --profile client_preview
python scripts\build_publication_snapshot_v1.py --profile client_preview --verify-only

Push-Location prototypes\nr3_explorer
npm test
$env:VITE_BASE_PATH = "/"
npm run build
Pop-Location
```

全仓历史测试仍含冻结前断言，不能用本轮发布门测试通过来宣称全仓全部绿色。
