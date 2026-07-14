# 解释性图表包 v0

日期：2026-07-14（方法状态修订）

目的：保留早期解释性探索图及其方法轨迹。此包不是最终报告，也不是当前正式图源。HR-011–015 已回写；A087–A093、A095–A101 仍只完成 E4 身份级合并，A077–A085 依 HR-015 仅保留为 E2 事件参与者、不进入 registry。

## 图件

1. `fig_actor_issue_bridge_network.png`
   - 显示连接两个及以上重点议题的 actor。
   - 读法：哪些组织在反基地、环保、国际倡议、地方自治、法律、生活安全之间起桥接作用。
   - 注意：E2 边只作线索。

2. `fig_place_issue_matrix_explanatory.png`
   - **已退役，不得作为合同地点×议题图或正文证据。**
   - 旧算法把同一 actor 的全部 actor–place 边与全部 actor–issue 边作宽投影，不要求地点和议题来自同一来源、同一事件或同一时期；因此只能用于暴露待核组合，不能证明某议题在某地点由同一公开行动连接。
   - 正式替代物 MA002 必须使用 `actor × place × issue × event/document × date × source` 三元事实，正文只允许同一来源或同一事件口径。

3. `fig_henoko_internationalization_pathway.png`
   - 显示边野古/大浦湾如何从地方基地争议转译为儒艮、生物多样性、法律程序和国际倡议。
   - 注意：这是路径图，不是资金链，也不是稳定联盟图。

4. `fig_coaction_sample_composition.png`
   - 显示 2010、2015、2020 三个共同行动样本在当前 registry 中的 actor 来源构成。
   - 注意：统计的是当前录入 actor，不是声明原文全量签名数。

5. `fig_evidence_gap_map.png`
   - 显示 HR 合并后的 actor 复核状态和 source archive 状态。
   - 用于决定下一轮调查优先级。

## 配套 CSV

- `actor_issue_bridge_nodes.csv`
- `place_issue_matrix.csv`
  - 与旧图同为宽投影历史产物，不得进入最终报告。
- `coaction_sample_composition.csv`
- `next_investigation_candidates.csv`

## 当前最适合继续调查的方向

1. 手工处理 26 条自动归档失败来源；失败状态不等于证据不存在。
2. 执行已收到的 HR-010、011、012、014、015：新增主体定性、E3 补源、沿革/范围、R8 角色及 evidence/venue seed；HR-013 仍待提交。
3. 与那国 A014/A015 的地方报纸、意见广告实物、议会资料。
4. AWWA / spouse club charity recipients 和 Schedule I / 活动手册。
5. 继续把共同行动保持为 event table，不因重复同场直接生成联盟网络。

## 禁止误读

- 共同署名不等于稳定联盟。
- grant opportunity 不等于已拨款。
- 服务型 NGO 不自动代表政治立场。
- 与那国不强行写成环保拒止案例。
