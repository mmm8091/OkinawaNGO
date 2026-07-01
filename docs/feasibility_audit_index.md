# 可行性审计文件索引

本轮任务目标：不是全面推进 NGO 网络项目，而是核查原方案第 5 节“研究模块菜单”中的每个模块是否能做、靠什么资料做、难度和价值判断是否正确；随后回头核查第 1 节项目定位和核心问题是否可实现。

## 1. 总表

- `module_audit_matrix_v0.md`  
  所有模块的横向核查表，按可行性、价值、难度、一期建议排序。

- `module_feasibility_audit_v0.md`  
  第一轮综合核查说明，比总表更详细，包含数据入口、模块判断、报价和工期初步建议。

- `feasibility_audit_work_summary_v0.md`  
  本轮可行性审计工作的汇总说明，说明做了什么、得出什么结论、如何调整第5/6/7节。

- `section7_module_review_mechanism_v0.md`  
  可替换原方案第7节的模块核查机制说明。

- `section5_6_reordering_pricing_audit_v0.md`  
  专门说明第5节模块排序和第6节工期/报价是否需要调整。

## 2. 单模块核查文档

目录：`docs/module_audits/`

- `B0_foundation_data_base.md`：基础 actor registry / source log / taxonomy
- `R01_organization_classification_ecology.md`：组织分类与组织生态
- `R02_actor_issue_network.md`：组织—议题网络
- `R03_place_spatial_yonaguni_sakishima.md`：地点与空间分布、与那国/先岛专题
- `R04_environment_life_safety_frame.md`：环保/生活安全框架与军事设施争议
- `R05_coalition_joint_action_network.md`：联盟/共同行动网络
- `R06_media_visibility_who_speaks.md`：媒体可见度与“谁在发声”
- `R07_field_target_shift.md`：场域与对象转移
- `R08_public_resources_admin_collaboration.md`：公开资源/行政协作渠道
- `R09_election_referendum_civil_society.md`：选举/县民投票与市民组织连接
- `R10_legal_policy_environmental_procedure.md`：法律/政策/环境程序渠道
- `R11_transnational_international_advocacy_network.md`：跨国/国际倡议网络
- `R12_people_organization_interlock.md`：人物—组织互锁与关键经纪人
- `R13_organizational_genealogy_long_term.md`：组织谱系与长期演变
- `R14_coverage_bias_audit.md`：资料覆盖与偏差审计

## 3. 数据样本

目录：`data/`

- `pilot_source_log_v0.csv`  
  24 条小样本 source log，覆盖 NPO 官方入口、边野古环保联署、OEJP/MMC、与那国、石垣、宫古、近期反前线化组织等。

- `actor_registry_seed_v0.csv`  
  20 个 actor seed，用于验证 actor registry 结构是否可用。

- `module_audit_matrix_v0.csv`  
  模块核查总表的 CSV 版本。

- `section7_module_review_table_v0.csv`  
  第7节模块核查机制的正式核查表。

- `revised_section5_6_recommendations_v0.csv`  
  第5、6节排序、工期和报价调整建议表。

## 4. 项目定位审计

- `project_positioning_audit_v0.md`  
  回头审第 1 节“项目定位”和三个核心问题：哪些能搞定，哪些需要收边界。

## 5. 需要用户/甲方判断

- `decisions_needed_from_user.md`  
  专门记录超出当前要求、需要你或甲方判断的问题。

## 6. 当前结论一句话

项目可以做，而且有价值；但标准一期应定位为：

> 冲绳民间组织分类底库与重点议题网络原型

而不是：

> 1972 年以来冲绳 NGO 全量历史网络

一期最稳的核心是：组织分类、组织—议题网络、地点—议题网络、环保/生活安全框架、与那国/先岛专题、小样本共同行动网络、跨国倡议样本、资料偏差审计。
