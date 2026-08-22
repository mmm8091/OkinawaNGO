# W2-C bounded matched non-entry arm audit v1

Date: 2026-08-22

Status: **research_only / arm_not_established / not_frontend_ready**

## 1. Outcome

This bounded pass did **not** establish a defensible matched non-entry arm for the 13 W2-C accountability episodes.

The admission rule was deliberately strict: a candidate had to match one selected episode on project/place, issue, action family and time, and a primary or official record had to show that the submission was not accepted, was returned, was not registered, or was not docketed **before** any hearing or substantive processing. The same submission also had to be traced for later entry or an alternative venue.

No candidate cleared all gates. This is a bounded failure result, not evidence that non-entry never occurs.

## 2. What changed during the pass

The 2004 Henoko pollution-mediation case was initially considered because it matches TE02 closely. The Okinawa Pollution Review Board record shows, however, that the application was received on 2004-02-03 and three committee meetings were held before dismissal under Article 50. It is therefore a **post-entry/pre-substantive gate-control case**, not a true non-entry arm.

A 2018 request to Ryukyu Cement is the clearest positive delivery refusal found. Two local newspapers report that the company did not accept the request letter and only agreed to designate a contact person. It was excluded because it does not match any W2-C episode on all four frozen dimensions, its target is a private company rather than the institutional venue of the nearest comparison episode, and no target-issued or official non-receipt record was located.

## 3. Frozen rules

- Match all four: same named project/place, same substantive issue, same action family, and overlapping period or no more than three years apart.
- Require affirmative non-entry evidence: `not_accepted`, `returned`, `not_registered`, or `not_docketed` before hearings or substantive processing.
- Exclude received applications, docketed petitions, threshold-qualified platform petitions, cases heard and dismissed, and requests whose response is merely not found.
- Trace later entry of the same submission and any alternative venue; an alternative action does not retroactively convert the original attempt into entry.
- Do not actorize anonymous applicants or upgrade an actor's central review status inside this package.

## 4. Files

- `selection_rules_v1.csv`: rules fixed before final candidate disposition.
- `candidate_screen_v1.csv`: candidate-by-candidate admission decisions.
- `selection_matching_table_v1.csv`: four matching dimensions plus the strict non-entry and source gates.
- `outcome_table_v1.csv`: header-only because no arm was admitted.
- `arm_status_v1.csv`: the explicit `arm_not_established` result.
- `gate_control_comparison_v1.csv`: the 2004 case, preserved only as post-entry gate control.
- `negative_search_log_v1.csv`: route-family search audit and bounded stopping reasons.
- `source_receipts_v1.csv`: frozen/reused evidence receipts; admission here does not approve a central fact.
- `change_notes_v1.csv`: records the rejected initial interpretation and its effect.
- `principal_checkpoint_v1.md`: decisions required before any future synthesis.
- `unexpected_findings_register_v1.csv`: package-local lead protocol; header only.
- `validation_report_v1.json` and `manifest.json`: generated verification receipts.

## 5. Interpretation boundary

Allowed now:

> The bounded search found several post-entry procedural gates and one reported delivery refusal, but no case met the predeclared matching, non-entry, primary-source and later-route requirements simultaneously.

Not allowed:

- “Accountability attempts always enter institutions.”
- “Institutions never refuse Okinawa civic organizations.”
- Treating the 2004 mediation dismissal as no entry.
- Treating the 2018 corporate refusal as an institutional match for TE02 or TE09.
- Adding any row in this package to W2-C outcomes, central facts, publication adapters or frontend views without a separate principal decision.

## 6. Reproduction and validation

```powershell
python scripts\validate_us_presence_network_wave2_w2_c_nonentry_v1.py
python scripts\validate_research_work_package_v1.py outputs\us_presence_network_wave2_w2_c_nonentry_v1
python -m unittest tests.test_validate_us_presence_network_wave2_w2_c_nonentry_v1
```

## 意外发现登记

本轮登记 **0 条**。`unexpected_findings_register_v1.csv` 仅保留现行 19 列表头。题外线索若以后出现，只能以 `lead_only` 留在本包，最多沿单条线索追查三步、全包最多十条观察；不得进入结论、中央事实、人工复核队列、publication snapshot 或前端。
