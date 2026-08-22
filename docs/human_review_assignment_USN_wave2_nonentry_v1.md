# HR-USN2-NE — W2-C matched non-entry arm decision

Date issued: 2026-08-22

Status: **principal decisions complete / named local task registered**
Source package: `outputs/us_presence_network_wave2_w2_c_nonentry_v1/`

This task does not authorize central writeback, W2-C revision, W2-F synthesis, publication or frontend release.

## Decision table

| decision_id | Question | Options | Principal decision | Decision note |
|---|---|---|---|---|
| HR-USN2-NE-001 | Accept the frozen true-nonentry gate and the bounded result `arm_not_established`? | `accept` / `revise` / `reject` | `accept` | 接受严格入口门槛与本轮有界失败结果。 |
| HR-USN2-NE-002 | Retain the 2004 Henoko pollution-mediation case only as a post-entry/pre-substantive gate-control comparator? | `accept` / `revise` / `reject` | `accept` | 只作进入后的法定排除控制案，不生成 non-entry outcome。 |
| HR-USN2-NE-003 | Does this bounded failure complete the W2-F prerequisite, or should a new-primary/local retrieval task continue? | `accept_bounded_failure` / `continue_primary_retrieval` | `accept_bounded_failure_with_named_local_task` | 接受本轮前置完成；具名取件已登记为 `docs/local_retrieval_tasks_v1.md` T2-H／`USN-NE-001`，目标为 2018-12-19 琉球セメント对岛ぐるみ会議名護请求书的受付／退件原件。 |

## What each choice means

- `accept` for NE-001 preserves the rule that receipt, registration, docketing or a hearing counts as entry even if the claim is later dismissed.
- `revise` for NE-001 must name the stage being studied—for example “no merits hearing” or “no target response.” It cannot continue to call a post-entry gate “non-entry.”
- `accept` for NE-002 leaves the 2004 case outside `outcome_table_v1.csv` and outside the central actor/event layer.
- `accept_bounded_failure` for NE-003 allows later synthesis to state only that no matched arm was established; it does not create a negative-case estimate.
- `continue_primary_retrieval` for NE-003 should produce a separate task naming the target institution, attempted submission, date, expected intake/return record and alternative-route evidence.

## Mandatory boundaries

- Do not assign the 913 applicants collectively to A069.
- Do not promote the 2018 corporate refusal into an institutional match.
- Do not interpret a header-only outcome table as zero real-world non-entry.
- Do not apply any decision until it is signed and a separate controlled merge/synthesis instruction is issued.
