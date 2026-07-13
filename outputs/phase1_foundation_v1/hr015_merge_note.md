# HR-015 human-review merge note

Review date: 2026-07-13
Human reviewer: project principal (user)
Merge script: `scripts/merge_hr015.py`

## Result

- Evidence notes: 49 reviewed rows, comprising 19 `accept` and 30 `revise`; 0 `reject`.
- Actor-event-venue (AEV): 64 reviewed rows, comprising 38 `accept` and 26 `revise`; 0 `reject`.
- Formal outputs:
  - `data/interim/06_evidence_notes_v0.csv`
  - `data/interim/09_actor_event_venue_edges_v0.csv`
- The formal tables retain evidence level, review decision/status, reviewer/date/task, and interpretation limits.
- No rejected-row file was created because the reviewed batch contains no rejection.

`revise` records an explicit wording, role, evidence, or locator boundary. It does not upgrade the row's evidence level.

## Human-review boundaries applied

1. `EN0025`–`EN0032` and every row from `AEV0045` through `AEV0060` are `human_checked`. Within that AEV span, the legal-role rows are `AEV0045`–`AEV0049` and `AEV0055`–`AEV0060`; named organizational plaintiffs, named individual plaintiffs, counsel, defendant, and non-party organizations remain separate. Person-level participation is not transferred to an organization. The intervening referendum rows retain referendum-specific interpretation limits rather than legal-case wording.
2. `AEV0036`–`AEV0044` remain E2 signatory-only observations. They record one-off publicly visible participation, not organizational continuity or a stable alliance.
3. `EN0017`, `AEV0053`, and `AEV0054` remain E2 Yonaguni event-context evidence. Organization identity and continuity remain unresolved pending local retrieval; these rows are not definite findings.
4. `AEV0061`–`AEV0064` are explicitly `analytical_seed`. They may support a hypothesis/figure scaffold, but are not an observed causal chain, stable alliance, or deterministic result.
5. Co-signing, joint statements, and event co-occurrence remain event participation only unless separately evidenced.
6. Funding/support wording is unchanged in substance: a NOFO/opportunity is not an award; project cost is not a contract payment; membership, sponsorship, service, and in-kind support are not movement funding unless a primary record establishes that relation.
7. Service-location or service-function evidence does not establish an anti-base or pro-base stance.

## MMC signatory-only withdrawal from the actor main table

The user review requires `AEV0036`–`AEV0044` to remain event participants whose identities are unconfirmed, not registry actors. Accordingly:

- A077–A085 were removed from `data/interim/01_actor_registry_initial_v0.csv`.
- The primary aliases, actor–issue, actor–place, and funding/support tables were checked for the same IDs; no related rows were present to remove.
- The nine AEV records remain in both the reviewed seed and formal AEV table.
- Their `actor_or_counterpart_id` is blank, their former candidate number is retained in `legacy_candidate_id`, and `entity_type=unverified_event_participant`.
- These rows are excluded from actor foreign-key requirements and must not be counted as main-registry actors.

## Locator revisions retained

The following five rows identify the correct source but lack a verified exact page or HTML section and therefore carry `locator_status=needs_locator_revision`:

`EN0021`, `EN0033`, `EN0038`, `EN0039`, `EN0040`.

No page/section was guessed. Each row records the user's request to leave the exact locator pending until it can be verified.

`EN0025`–`EN0030` now uniformly cite official Ninth Circuit opinion No. 18-16836 (`S129`). The organizational-plaintiff and defendant roles cite opinion p. 1 / PDF index 0 (caption); the Earthjustice counsel role cites opinion p. 4 / PDF index 3 (counsel section). These six locators are `verified_exact_page`. `EN0031`–`EN0032` retain the HR-014 human-confirmed negative organizational-role boundary.

## Validation

Running `python scripts/merge_hr015.py` checks:

- exact row and ID sets: `EN0001`–`EN0049` (49) and `AEV0001`–`AEV0064` (64);
- source, evidence-object, actor, event, and venue foreign keys;
- zero rejected rows;
- Dugong human-review status;
- unchanged E2 status for MMC small groups and Yonaguni rows;
- exactly four blank-event `analytical_seed` pathway rows;
- exactly five `needs_locator_revision` rows and exact S129 opinion locators for `EN0025`–`EN0030`;
- absence of A077–A085 from all actor primary tables while preserving their nine legacy AEV event records;
- byte-stable formal/seed outputs on repeated execution.

The source log and control documents were not modified. The actor registry was modified only to withdraw A077–A085 under the user's explicit HR-015 boundary; all unrelated registry rows were preserved.
