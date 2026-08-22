# W2-A／W2-D 人物消歧补证侦察 v1

日期：2026-08-22
状态：`research_only / principal_decision_pending / not_frontend_ready / no_central_writeback`

## 1. 本包回答什么

本包只补强 `HR-USN2-01a—01e` 五组人物候选的证据，不替负责人合并姓名、建立 person node 或批准组织桥。侦察以现有官方 IRS XML 为主，另对 exact／near-name 做了有界的政府或组织官网检索；数据经纪、私人社交账号和私人联系方式一律不进入证据链。

五组候选全部位于驻军服务／军属慈善侧：AWWA、KOSC、NOSCO 与 OESC。即使负责人以后认定某组为同一人，也只能形成 **service-side 内部人物桥**，不能据此写成问责侧与服务侧之间的跨生态桥。

## 2. 这次补证改变了什么

- **01a Brooke Epp／Epps：证据明显增强。** AWWA 2022-06—2023-05 申报的 return header 已 exact 写明 `Brooke Epp / AWWA Treasurer`，签署日为 2024-03-01；下一税期 AWWA Part VII 写 `Brooke Epps / Financial Officer`。KOSC 2023-06—2024-05 申报又由 `Brooke Epp / President` 于 2025-03-06 签署，下一税期 Part VII 写 `Brooke Epp / Outgoing President`。美国空军嘉手纳官网另在 2025-03 把 exact-name Brooke Epp 写作 909th ARS key support liaison。它已不再是单一近名碰撞，但仍没有一条记录明说 AWWA 与 KOSC 两项角色属于同一个人。
- **01c Amber N Tracy／Amber Tracy：证据明显增强。** AWWA 同一份 2022-06—2023-05 申报的 filer `InCareOfNm` 和 `BooksInCareOfDetail` 都写 `Amber N Tracy`；OESC 2022-07—2023-06 申报的 header、principal officer 与 Part VII 都写 `AMBER TRACY / President`；下一税期 AWWA Part VII 写 `Amber Tracy / President`。这是一条跨两组织、相邻任期的高收敛链，但 `BooksInCareOf` 只是账簿保管／联系字段，不等于董事或完整任期。
- **01d Trinicia Kloepper：同税期 exact full-name 双组织记录。** AWWA 与 KOSC 在 2022-06—2023-05 同时列出 exact full name，KOSC 下一税期继续列名；官方空军历史报道只补充军属环境背景，不直接证明双组织身份。
- **01e Lesilee Du Fresne／DuFresne：同一 OESC 的相邻税期连续性很强。** 差异只在姓氏空格，角色从 2nd Vice President 转为 Advisor；它是组织内连续性候选，不是跨组织桥。
- **01b Jen Yapsing／Jennifer Yapshing：仍是五组中最弱的一组。** AWWA 连续两税期写 exact `Jen Yapsing`，NOSCO 在重叠税期写 `Jennifer Yapshing`；罕见近名、缩写和一字母倒置使同一人解释可行，但当前组织官网只展示现届 roster，未闭合历史身份。

以上只是证据强度变化；原 HR 决定栏保持未动。

## 3. 关键语义边界

Return header 的 `BusinessOfficerGrp` 通常对应申报签署时点，Part VII 对应所报税期内的 officer／director 等记录，两者不能机械当成同一整段任期。例如 AWWA 2022-06—2023-05 的 Part VII 仍列 Danielle Kessler 为 Treasurer，但该 return 在 2024-03-01 已由 Brooke Epp 以 AWWA Treasurer 身份签署。这更像换届后的申报责任线索，而不是证明 Brooke 在整个税期任 Treasurer。

同理，`InCareOfNm` 与 `BooksInCareOfDetail` 能把 Amber N Tracy 放进 AWWA 的申报／账簿保管语境，但不能单独生成 AWWA officer role。所有时间线都保留 `tax_period_role`、`filing_point_role`、`books_contact` 三种语义。

## 4. 文件

| 文件 | 用途 |
|---|---|
| `evidence_matrix_v1.csv` | 五组逐条官方记录、名称、角色、locator 与语义限制 |
| `candidate_timeline_v1.csv` | 按候选排序的申报期／签署时点时间线 |
| `candidate_assessment_v1.csv` | 补证后的强度、最强可支持判断与竞争解释 |
| `bounded_search_log_v1.csv` | 最多三步的官方／组织网页 exact-name 检索日志 |
| `source_receipts_v1.csv` | 9 份官方 IRS XML 与 4 个政府／组织网页入口 |
| `hash_verification_v1.csv` | 9 份继承 XML 的 SHA-256 复核 |
| `principal_checkpoint_v1.md` | 负责人逐组判断页；不预填决定 |
| `unexpected_findings_register_v1.csv` | 19 列 `lead_only` 方法线索登记 |
| `validation_report_v1.json` | CSV、lead protocol 与哈希验证结果 |
| `manifest_v1.json` | 本包文件清单与 SHA-256 |

## 意外发现登记

本包登记 **1 条** `lead_only` 方法线索：现有 Part VII 长表会漏掉 return header 的当前签署人和 `BooksInCareOfDetail` 的账簿联系人，因此可能低估换届期人物连续性。该线索已经走到“发现遗漏字段 → 对五组补抽 → 确认它会改变两组证据强度”三步边界并停止。它不进入本包结论、中央事实、现有人工决定栏、publication snapshot 或前端；若以后要审计整个服务生态的申报页眉，需另开工作包。

## 6. 不得被误读为

- 不是负责人已经认定任何两条姓名记录为同一人；
- 不是批准 person node、跨组织人物边或组织控制关系；
- 不是两套生态之间发现了共享人物；五组都只在 service-side 内部；
- 不是 return header 角色覆盖整个 tax period；
- 不是 `BooksInCareOf` 等于 officer／board member；
- 不是中央写回、前端发布或 W2-F 放行。

## 7. 复核与验证

```powershell
python scripts/validate_research_work_package_v1.py outputs/us_presence_network_wave2_person_disambiguation_supplement_v1
Import-Csv outputs/us_presence_network_wave2_person_disambiguation_supplement_v1/*.csv | Out-Null
Get-FileHash -Algorithm SHA256 outputs/us_presence_network_wave2_w2_00_spouse_990_v1/raw/*.xml
```
