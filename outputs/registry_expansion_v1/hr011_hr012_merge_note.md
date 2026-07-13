# HR-011 / HR-012 合并说明

合并日期：2026-07-13
依据：用户人工结论；由 `scripts/merge_hr011_hr012.py` 幂等落库。

## 结果

- 新增 A107 `沖縄YWCA`。它与 A105 `日本YWCA` 保持独立 actor，并以 A105 → A107 的 `organizational_affiliation` 表示总组织到地域组织关系。该边不是资金关系，也不表示运动联盟；A105 的每项声明不能自动归给 A107。
- 新增 A108 `沖縄を再び戦場にさせない県民の会`。它进入冲绳本地的前线化／反战动员层；公开活动只证明事件期动员，不证明参与组织之间存在稳定联盟。
- C015 `宮古島・命の水・自衛隊配備について考える会` 不入 registry。当前材料不足以安全闭合名称、组织身份与议题行动归属，保留在 HR-011 拒绝记录中。
- 新增 A109 `第4次嘉手納基地爆音差止訴訟弁護団`，并添加 A109 → A052 的 `legal_counsel`。律师团与原告团是不同 actor；不从现有材料推断完整个人律师名册。
- 新增 A110 `辺野古に基地を絶対つくらせない大阪行動`，作为本土声援层而非冲绳本地核心层。其公开行动不表示稳定联盟或资金关系。

## 沿革与规范名

- A052 规范名调整为 `嘉手納基地爆音差止訴訟原告団`；原名 `嘉手納爆音訴訟原告団` 保留为 `former_canonical`。
- C026 `第4次嘉手納基地爆音差止訴訟原告団` 作为 A052 的 `round_of` 记录，不建新 actor；不假定各轮原告成员完全相同。
- A053 规范名调整为 `普天間基地爆音訴訟原告団`；原名 `普天間爆音訴訟団` 保留为 `former_canonical`。
- C027 `普天間基地第2次爆音訴訟原告団` 作为 A053 的 `round_of` 记录，不建新 actor；不假定各轮原告成员完全相同。
- C028 `石垣島への自衛隊配備を止める住民の会` 作为 A010 的 `predecessor_of` 谱系记录，不建新 actor。材料记载其于 2015-08-20 成立；A010 于 2016 年 9 月作为包含该会、公民馆、工会、和平／市民团体、市议员与个人的较广联盟形成。两者不能当作完全同名同体。

## 数据改动

- actor registry：新增 4 行，更新 A010、A052、A053。
- actor aliases：新增 2 个旧规范名、2 个诉讼轮次名、1 个前身谱系名。
- actor-issue edges：新增 15 条已人审议题边；没有为 C015 建边。
- funding/support sample：新增 2 条非资金关系边：A109 → A052 `legal_counsel`、A105 → A107 `organizational_affiliation`。
- human review log：新增／更新 HR-011 五项和 HR-012 三项结论。
- issue taxonomy：本轮未新增类别，全部使用现有 I001–I024。

## 来源与限制

本轮没有自行占用新 S 编号。尚未统一进入 source log 的依据暂保留为 `SC010`、`SC013`、`SC026`、`SC029`–`SC032`、`SC041`–`SC042`；主线程后续统一分配或映射 S 编号。

所有新增关系均明确为 `not_funding_relation`，并在 notes 中写明非联盟限制。人员桥接没有进入 organization actor registry；具名代表、召集人或律师只保留在来源说明中，等待未来独立 person table 决策。

## 自校验

脚本检查：

- actor、alias、issue edge、relation 与 human-review log 主键唯一；
- actor-issue 与 actor-actor 外键完整；
- A107–A110 存在，C015 及 C026–C028 未生成 actor；
- `round_of`／`predecessor_of` 谱系行齐全；
- F042/F043 均为 `not_funding_relation`，且 notes 明确不是稳定联盟；
- 所有 S／SC 引用均能在现有 source log 或 source candidate 表找到。
