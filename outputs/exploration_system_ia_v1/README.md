# exploration_system_ia_v1 — NR-01 研究信息架构

日期：2026-07-18  
状态：checkpoint A direction approved；已按负责人决定重写

## 当前冻结结论

前端是中央研究数据经唯一适配层生成的自动化可视化客户端，不是另写文案的内容网站。

主展示固定为四页：

1. 总览：V1 全域地点—议题研究地图
2. 组织：V2 组织—议题生态图
3. 路径：V3 问题—行动—场域—产出路径图
4. 证据：V4 证据覆盖与偏差图

共用组件：

- G1 全局时间层；
- G2 全局证据抽屉；
- 比较是主图状态，不是第五页；
- 地点、组织、episode、议题和来源详情使用右侧面板、抽屉或 URL 参数，不增加并列主页面。

## 有效输入

| 文件 | 角色 |
|---|---|
| `../../docs/exploration_system_information_architecture_v1.md` | NR-02 的产品与信息架构输入 |
| `view_visual_inventory_v1.csv` | 四页、四主图、两全局组件及禁用图清单 |
| `module_to_view_crosswalk.csv` | 后端模块到四个可视化引擎的归宿 |
| `checkpoint_A_decision_sheet_v1.md` | 负责人已确认的方向与 NR-02 边界 |

## 退出冻结交付的探索物

| 文件 | 当前角色 |
|---|---|
| `wireframe.html` | superseded exploration；记录旧六页面族思路，不作为页面需求 |
| `route_map.svg` | superseded exploration；记录旧路由思路，不作为路由需求 |

保留这些文件是为了让设计决策可追溯，不代表需要继续修补旧线框。

## 与一期合同的对应

一期五张核心图保留在四个视觉引擎中：

- 组织—议题网络 → V2；
- 地点—议题图 → V1 严格证据状态；
- 国际倡议／法律程序路径 → V3；
- 与那国／先岛专题 → V1 先岛聚焦状态；
- 覆盖偏差图 → V4。

R1–R11 是后端研究生产结构，不出现在用户导航中。R14 历史演变进入全局时间层；完整谱系仍是扩展研究。

## NR-02 handoff

NR-02 应输出一个版本化前端 view model，统一 actor、place、issue、episode、venue、outcome、
evidence 与 historical_anchor，并为 V1–V4 预先构造合法节点、边、状态和短标签。

不得让浏览器现场推断联盟、因果、影响力或历史连续性；不得为单个地区或案例另写页面文章。
