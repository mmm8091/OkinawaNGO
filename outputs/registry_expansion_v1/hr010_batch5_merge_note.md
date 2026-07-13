# HR-010 批5合并记录：A102-A106

日期：2026-07-13

## 人工结论

- A102 全国公害弁護団連絡会議：`background_support`，全国法律协调网络；R8 使用，不写成冲绳本地核心。
- A103 全国基地爆音訴訟原告団連絡会議：`background_support`；A052、A053 为其具名成员原告团。
- A104 普天間基地爆音訴訟弁護団：`core_support`；律师团与 A053 原告团为不同 actor，记录法律代理关系。
- A105 日本YWCA：`background_solidarity`；只记录 2020 辺野古声明层，不生成联盟边，并与 C009 沖縄YWCA 区分。
- A106 首都圈声援组织：`background_solidarity`；与 A025/A062 只记录事件/伙伴行动。`首都圏キャンペーン` 进入 alias 表，canonical name 仍待定。

## 数据合并

- A102-A106 的 `review_status` 改为 `human_checked`。
- 新增 I020-I024：environment、noise、women、human_rights、solidarity。
- 新增 AI181-AI200 共 20 条人审 actor-issue 边。
- 新增 F037-F041 共 5 条 `not_funding_relation`：2 条 network membership、1 条 legal counsel、2 条事件/伙伴行动。
- `human_review_log_v0.csv` 新增 5 行 HR-010 记录。

## 解释边界

- A102/A103 是全国支持/协调层，不改变冲绳本地核心 actor 的统计口径。
- A104 与 A053 不得因名称接近而合并；诉讼代际继续在 HR-011/HR-012 统一处理。
- A105 的正式声明不等于稳定联盟。
- A106 的两条关系只证明公开行动连接，不证明长期组织联盟。
- 所有 F037-F041 均为非资金关系。
