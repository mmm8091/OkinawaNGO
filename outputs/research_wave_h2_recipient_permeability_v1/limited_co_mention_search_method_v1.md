# H2 有限组织名共现检索方法

日期：2026-07-20
状态：`research_only / ai_search_log / not a symmetric or closure test`

## 设计

- 锚点是 18 个已经具有人审 actor–issue 基础的基地问责组织，属于非随机、非总体样本。
- 每个锚点只执行一条完全记录的组织名共现查询。
- 查询右侧固定覆盖：
  - `Marine Thrift Shop`
  - `Okinawa International Women's Club`
  - `American Welfare and Works Association`
  - `American Women's Welfare Association`
  - `米国福祉事業協会`
  - `米国婦人福祉協会`
- 检索接口为 `web.search_query`。每条实际查询式、返回数和返回 URL 都保存在
  `accountability_limited_co_mention_search_v2.csv`。

## 本次执行结果

18 条查询均由检索接口返回 `0` 个结果，因此没有可记录的结果 URL。CSV 没有把 URL
空白当作遗漏，而是同时记录：

- `query_execution_status=completed_no_results_returned`
- `returned_result_count=0`
- `returned_result_urls` 为空

## 能说与不能说

最强可用表述只有：

> 现有 AI 日志在 18 个非随机问责锚点的一组有限组织名共现查询中，没有记录到可归属
> 的直接组织关系。

这不是对称检验，也不是闭合检验。它没有：

- 对服务侧建立可比的随机或完整锚点；
- 分别穷尽每个组织的全部历史别名；
- 测量人员名册、最终受赠者或非公开接触；
- 覆盖地方报刊馆藏、内部档案、纸本会报或社交平台全部历史内容；
- 估计关系不存在的概率。

因此它不能支持“没有共享人员”“两个生态闭合”或“当前两侧完全没有接口”。后续若要
检验当代组织／人员交叉，必须另建双侧可比样本、人员名册与来源覆盖设计。
