# Research wave v2 synthesis

日期：2026-07-20  
状态：`research_only / principal_interpretive_decision_required / not_frontend_ready`

本目录不是第四个经验模块，而是 H1／H2／H3 三个独立研究包的负责人判断索引。

## 入口

- 负责人解释性判断：`docs/research_wave_v2_principal_checkpoint.md`
- 三假设状态：`hypothesis_status_v2.csv`
- 负责人决定栏：`principal_decision_queue_v2.csv`
- 自动边界检查：`validation_report_v2.md`

## 上游包

- H1：`outputs/research_wave_h1_documentation_visibility_v2/`
- H2：`outputs/research_wave_h2_recipient_permeability_v1/`
- H3：`outputs/research_wave_h3_frontline_memory_v2/`

三个包的结论不是同一强度：H1 的原命题未获当前 proxy 支持；H2 只把“长期完全封闭”
降为不可维持的过强外推；H3 仅在共同文件层支持一个重新表述后的命题。不得把三者统一
写成“已验证”。

本轮最终证据边界提交：H1 `42efe92`（在 `10991db` 基础上的最终图件修订）、H2
`0f05255`、H3 `3ac119c`。这些提交均为附加型研究包，没有修改中央表或前端。

## 边界

- 本目录不批准 actor、关系、案件角色、事件角色、资助或组织谱系。
- “未找到”只描述有界公开语料，不等于现实中不存在。
- 名单重叠只表示重复公开出现，不生成成员间关系。
- 三个假设都保持 `research_only`；负责人判断和相应人审完成前不得接入前端。
- 本目录的决定栏不自动并入 live HR ledger，避免在选题前制造大规模人工负担。

复验：

```powershell
python scripts\validate_research_wave_v2_synthesis.py
python -m unittest tests.test_validate_research_wave_v2_synthesis -v
```
