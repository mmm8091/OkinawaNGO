# R6 / R7 / R11 线上解释层 brief v1

日期：2026-07-20
状态：HR-021 八项决定已合并。

## 共享底盘

- 正式 actor–event–venue–target/entry-mode 事实：**80** 条。
- `analytical_seed`：**4** 条，继续与正式事实分离。
- HR-021：5 项 `include_after_hr018`、2 项 `revise_scope_after_hr018`、1 项 `retain_analytical_seed`；未决 0。

HR-018 已审并不自动等于进入路径分析。只有 HR-021 明确放行的九条 R10 关系新增到正式底盘；其余已审关系留在 R10 的本模块事实层。

## R6：行政入口的三种不同事实

R6 的行政比较现在同时保留：ONC／JICA 的事件共同参与、JICA→ONC 的有界受托角色、冲绳县→A066 的提案选定合同。三者不能折成“共同合作”或“资金网络”；具体金额仍只在 R10 amount layer。

## R11：53 条进入观察

R11 共有 **53** 条：administrative 7, advocacy 30, charity 2, legal 5, public_diplomacy 1, service 8。

- FY2024 外务省委托与 FY2026 年度指定分成两个观察，后者不继承前者金额。
- USO Okinawa 服务存在只形成一条 service relation；八个 site/function 继续留在 R10 功能层。
- MBC 是本地 direct sponsor observation；Matson 只作为 USO Indo-Pacific 区域 sponsor perimeter，不写成本地定向资助。
- 委托、指定、服务和 sponsor tier 都不自动产生政治立场、稳定联盟或因果路径。

## analytical seed 边界

AEV0061–0064 继续作为分析性路径假说。已有的共同要请、调查和事件事实不证明 A019→A003→A004/A005 的有向传递；四条 seed 不进入正式计数、默认事实层或稳定关系网。

## 图状态

本轮没有重绘 R6／R7／R11 SVG/HTML；这些图是 pre-HR021 快照。当前事实计数与下游范围以 CSV、本 brief 与 validation note 为准。
