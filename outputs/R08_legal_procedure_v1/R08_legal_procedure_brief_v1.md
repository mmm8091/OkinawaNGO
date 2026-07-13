# R8 法律／政策／环境程序比较包 v1

日期：2026-07-13

## 验收结论

本包只读取 HR-014 已完成的 **6 个 human_checked 案例／程序**和 **27 个 human_checked、accept 角色**。它回答的不是“哪一案胜率更高”，而是：不同争议如何被转译进不同制度渠道，谁以何种案件特定角色进入，以及程序实际留下了什么产出与未提供什么救济。

27 个角色中，13 条使用 registry actor 外键，14 条使用案件内 provisional procedural node。角色 family 为：plaintiff 10; counsel 5; requester 1; commenter 1; supporter 2; non_party 2; defendant 4; proponent 1; institutional_recipient 1。

## 六案比较

1. **Dugong／美国法律**：生态与文化财主张进入 NHPA §402／APA 审查。程序形成可审查标准和公开记录，但 2020 年最终维持 DoD 胜诉，没有停止工程。
2. **边野古 EIA**：NACSJ 以 commenter 身份把珊瑚礁、儒艮、调查与预测充分性写入正式意见；提交不等于采纳，程序完成也不等于工程停止。
3. **第三次嘉手纳**：居民把噪音转译为差止与损害请求；过去损害赔偿获维持，运营／噪音差止和未来损害请求未获支持。
4. **普天间周边噪音**：两个并合行动确认部分原告、部分期间的损害赔偿并驳回其余请求；本案不产生运营禁令。
5. **石垣住民投票**：部署争议经条例请求进入义务付诉讼，法院因住民投票实施不属可义务付的行政处分而驳回；这是程序门槛，不是对地方自治政治价值的总体判断。
6. **泡濑公金支出**：第一波在无合理修订计划时限制未来支出，第二波居民在上诉与最高法院阶段未获支持。两波结果相反，必须分列。

## 强制角色边界

- A002、A019 在 R8C01 均为 `non_party`，不继承相关个人或外围倡议的原告身份。
- A020 在 R8C01 是 `plaintiff`，在 R8C06 是 `supporter`／正式材料承载者；不得跨案泛化为 plaintiff 或 counsel。
- A009 在 R8C01 是 `counsel`，不是 named plaintiff。
- A011 在 R8C05 是 `requester`，不是 named organizational plaintiff。
- A055 在 R8C06 是 `supporter`，不是组织原告或 counsel。
- A052／A053 是各自案件特定的 `plaintiff_group` crosswalk；不得推断个体成员或轮次人员恒定。
- P8E004 第三次嘉手纳 counsel 继续是 provisional procedural collective，不进入 actor registry。

## 图表读法

`fig_r08_procedure_outputs_v1` 按“争议／地点—程序入口—已审角色—制度对象—程序产出／边界”并列六案。横向排列是解释框架，不是因果箭头。`fig_r08_role_boundary_matrix_v1` 只显示 27 条 accepted role observation 的 family 计数，并同时标出 registered/provisional 数量；零表示当前没有 accepted role row，不表示该角色在现实中绝对不存在。

## Residual gaps 与 HR-026

当前 3 项 residual gap 都是非阻断的案号、phase locator 或泡濑 subcase 细化问题，不改变六案、27 角色或已审结果边界。本轮不创建 HR-026：没有需要新增人类判断的事实或角色；如未来要求审级级时间线，再按 `residual_gaps_v1.csv` 补精确 locator。

## 可直接写入报告

> 冲绳的基地与开发争议并非进入同一种法律渠道，而是依争议对象和可用制度被转译为不同程序问题。边野古／大浦湾的儒艮与生态知识分别进入美国 NHPA Section 402／APA 审查和日本环境影响评价意见程序；嘉手纳与普天间的航空器噪音则被表达为人格、生活与期间损害；石垣的陆自部署争议进入住民投票条例请求和义务付诉讼；泡濑的填海生态、经济与灾害风险进入公共支出合法性与合理性审查。六案的程序产出不能用统一胜败概括：Dugong 案形成可审查标准与公开记录但最终维持 DoD 胜诉，EIA 意见进入记录却不等于被采纳，噪音案确认部分既往损害但没有形成运营禁令，石垣案因行政处分门槛被程序性驳回，泡濑第一波限制未来支出而第二波在上诉与最高法院阶段未获支持。相应地，原告、律师、请求者、评论者、非当事支持者和制度节点必须分开编码；A002／A019 在 Dugong 案是 non-party，A011 在石垣案是 requester，A020 仅在 Dugong 案是 plaintiff、在泡濑案则是 supporter。
