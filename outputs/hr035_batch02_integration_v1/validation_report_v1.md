# HR-035 Batch 2 controlled merge validation v1

Date: 2026-07-20

Status: **PASS**

Validated boundaries:

- PASS — 23 principal decisions applied.
- PASS — five identity companions are human-reviewed.
- PASS — sixteen facts entered the reviewed layer.
- PASS — AI157 and AI158 remain second-source candidates.
- PASS — AI044 uses S023 and records S024 as invalidated.
- PASS — AI016 and AI233 are explicitly event-scoped.
- Central actor registry remains 122 history rows; no actor was added or removed.
- Central actor–issue table remains 294 history rows; the current analytical gate yields 283 active rows (141 human-reviewed / 142 candidate) before downstream regeneration.
- The merge changes only five reviewed actor rows and eighteen reviewed actor–issue rows; all other central rows are protected by the merge.
- AI157 and AI158 are completed human defer decisions and online second-source leads, not blank review tasks or accepted facts.
- No actor–actor relation, funding relation, event, place, alliance, continuity or causal claim is approved.

Errors: none.
