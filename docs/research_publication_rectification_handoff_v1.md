# 研究发布架构整改换手 v1

日期：2026-07-20  
范围：研究方法到静态展示站的唯一发布 seam，以及既有成果重新准入  
状态：整改完成；部署待负责人提供阿里云／域名配置

## 1. 本轮完成

本轮完成了两件不同的事：

1. 先修架构，使任何展示都不能绕过研究方法；
2. 再审计已有成果，把方法合格但旧架构未正式接入的内容纳入，把方法不足的内容继续挡在
   `internal`。

当前路径：

```text
中央事实／模块观察
  → core surface registry 或专用 adapter
  → publication catalog 方法与主张门禁
  → profile 专属投影
  → envelope／追溯／哈希验证
  → 不可变 release
  → channel 完整性验证
  → Vite 静态站
```

## 2. 核心旁路已经封闭

旧版 compiler 会把核心 builder 的全部输出复制进公开站。即使 catalog 说某模块
`adapter_needed`，React 仍可能直接读取 `relations.json`、coverage 或 episode，形成事实上的
绕行。

当前修复：

- 新增 `data/metadata/research_publication_core_surfaces_v1.json`；
- builder 的每个输出都必须在 registry 中有明确处置；
- `demo/relations.json` 和 `research/candidates.json` 按 JSON pointer 拆为独立发布文件；
- public profile 只包含被允许的投影；
- 未消费旧 views、重复生命周期文件和空 leads 不进入 public；
- reviewed profile 对 aggregate 行作人审过滤，F027 不存在；
- client preview 可保留 F027，但仍标 `needs_local_retrieval`／非 dyadic。

公开站已经不含：

```text
demo/relations.json
research/candidates.json
views/global.json
views/overview.json
views/actors.json
demo/historical_anchors.json
```

## 3. 已有内容的真实处置

catalog 现为 26 项：

| 类别 | 数量 |
|---|---:|
| 完整 architecture objects | 3 |
| 完整方法模块 | 5 |
| 有限 core surfaces | 4 |
| 方法就绪、尚无公开模块表面 | 5 |
| 需继续研究 | 5 |
| retired | 4 |

完整 object index 共 8 项：

- `PUB-ARC-001` lifecycle；
- `PUB-ARC-002` typed relation/non-relation；
- `PUB-ARC-003` event participation；
- `PUB-MR-004` Sakishima frames；
- `PUB-MR-005` repeated participation；
- `PUB-MR-012` official 616-row universe；
- `PUB-MR-013` coverage audit；
- `PUB-MR-014` translation episodes。

四项 `partial_bounded` 为 `PUB-MR-001/003/008/011`。它们只代表安全事实子层可查，不代表
完整研究模块已经接入。

## 4. 第一批新增／正式升格的可演示内容

### 生命周期

LC001–LC005 五条进入时间页。LC006 排除。最后活动日期只作为公开记录下限，重组不作简单
actor 合并。

### 先岛框架语料

- reviewed：9 条观察、5 条摘录；
- research：追加10条 QA-safe 观察、19条 QA-safe 摘录；
- 三地 tab 内合计少1条的原因，是另有1条 Sakishima regional context。

个人、行政、匿名发言和组织不互相转嫁。

### 重复公开参与

2010／2015／2020 三份目的性名单共169条观察、21个严格重复身份。它只展示 event-level
重复参与，不生成组织关系边。

### 官方协作来源总体

完整 86 页／616 行、15部门、19事業分野和10机制。明确显示“616行不是616组织”。

### 六维覆盖审计

时间、地点、组织功能、议题、来源和复核层的单位、分母、机制与线上／当地缺口均已三语化。
这是全站读图护栏，不是组织总体估计。

### 13个制度转译 episode

reviewed profile 只有 TE01–09；client preview 的研究视图追加 TE10–13。六阶段严格拆开
场域进入、中间产出、有限结果和底层变化，不能计算成功率。

## 5. 仍然不准进入甲方发现层

- H1 资料留存＝中心性；
- H2 两套生态没有共享人员；
- H3 前线化已成为全日本共同语言；
- 1998–2012制度化与载体史候选；
- 制度转译负案例。

这些方向仍值得研究，但当前只能作为 `internal` hypothesis。四个退役图家族继续永久禁止
回流。

## 6. 代码与数据

主要新增／修改：

- `research_publication/compiler.py`
- `research_publication/adapters/`
- `data/metadata/research_publication_catalog_v1.json`
- `data/metadata/research_publication_core_surfaces_v1.json`
- `data/metadata/publication_release_profiles_v1.json`
- `data/metadata/frontend_presentation_rules_v1.json`
- `data/metadata/coverage_implication_display_trilingual_v1.json`
- `scripts/build_publication_snapshot_v1.py`
- `scripts/stamp_frontend_release_v1.py`
- `prototypes/nr3_explorer/src/lib/data.js`
- `prototypes/nr3_explorer/src/pages/`
- `prototypes/nr3_explorer/src/components/*Exhibit*`

## 7. 安全与失败行为

- profile 默认 channel 已按 profile 派生；
- `--verify-only` 同时验 channel 与 snapshot；
- Vite 构建时核对 channel profile、release ID、public flag 和 manifest hash；
- Vite 每一代开发服务器固定一个 release；channel 推进后整体重启并绑定新快照；
- snapshot 多出任何未校验文件会失败；
- adapter 和 core publication object 都必须带统一 envelope；
- 必需 JSON 缺失或 research 分片读取失败会显示全页发布错误；
- 证据抽屉失败显示错误，不再永久显示“加载中”；
- 外部 Google Fonts 请求已移除；
- `dist/release.json` 记录 Git commit、dirty 状态、publication/site release 和 base path。

## 8. 复现与验收

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
npm run build
Pop-Location
```

验收必须同时确认：

- reviewed 不含 `research/`、R4 QA-safe 层和 F027；
- client preview 研究候选仍有显式状态；
- legacy bundle 和未消费 views 不在 `dist/`；
- object index 与公开 catalog ID 一致；
- 桌面／移动端无横向溢出；
- 浏览器 console 无 error；
- `release.json` 的 source commit 与部署 commit 一致且 `source_dirty=false`。

全仓历史测试仍有冻结前断言，不能宣称全仓全部通过。本轮只对当前发布 seam、adapter、核心
builder 和生产前端作验收。

## 9. 阿里云／公司域名下一步

可上传的唯一目录：

```text
prototypes/nr3_explorer/dist/
```

需要负责人下一轮提供：

1. 公司域名或子域名；
2. OSS bucket、地域及是否已有静态网站／CDN；
3. 备案、DNS、HTTPS 证书状态；
4. 公网开放、密码保护或其他访问策略；
5. 根域还是子路径部署。

建议使用版本前缀上传，先以临时域名验收，再原子切换。`index.html`、`release.json` 短缓存
或不缓存；内容哈希 JS/CSS 长缓存。保留上一 site release 以便回滚。

## 10. 不得误读为

- 8个完整对象不等于一期全部验收完成；
- partial core surface 不等于完整模块；
- client preview 候选层不等于已核层；
- 没有编码关系不等于现实不存在；
- 纯静态可部署不等于已经取得阿里云修改授权；
- 本轮没有替负责人做 H1/H2/H3 的解释性结论决定。
