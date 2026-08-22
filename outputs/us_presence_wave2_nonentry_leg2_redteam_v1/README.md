# W2-F 前置研究方法红队包 v1

日期：2026-08-22

状态：`research_only / design_audit_only / principal_review_pending / central_writeback=no / not_frontend_ready`

本包是 `docs/us_presence_wave2_nonentry_leg2_redteam_v1.md` 的配套协议包。它只冻结 ONE matched non-entry arm 与 ONE key recipient／LEG2 microcase 的定义、最小表结构、覆盖指标、证伪条件和负责人决定，不新增案例事实，不解除 W2-F 阻断。

当前结论：W2-C 的六行仍是 gate/control，不构成 matched non-entry；W2-A 的 Ambitious 等原件可以形成 LEG2 微型案例，但 action、transaction 与 narrative uptake 必须分开闭合。

## 意外发现登记

本轮 0 条。`unexpected_findings_register_v1.csv` 仅保留统一 19 列表头。方法风险、反例与验收条件属于本包正式审计内容，不放入 `lead_only`。

## 边界

- 不修改中央事实、现有 W2-A／C 数据或负责人决定；
- 不把“未查到”编码为 non-entry；
- 不把礼节性致谢、行动方转载或媒体复述编码为合法性效果；
- 不授权 W2-F、W2-G、publication adapter 或前端。

## 验证

```powershell
python scripts\validate_research_work_package_v1.py outputs\us_presence_wave2_nonentry_leg2_redteam_v1
```
