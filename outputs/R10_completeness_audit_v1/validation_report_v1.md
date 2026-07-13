# R10 completeness audit validation v1

Date: 2026-07-13

## Structural checks

- PASS: 35 unique relation observations
- PASS: 26 unique amount observations
- PASS: 43 unique function observations
- PASS: all amount foreign keys resolve
- PASS: all function foreign keys resolve
- PASS: S002 extracts sequential rows 1-616 with no gaps or duplicates
- PASS: exactly 10 S002 source rows crosswalk to R10
- PASS: S002 selected-row set is stable
- PASS: S002 field 10 contains 8 rows
- PASS: S002 field 11 contains 11 rows
- PASS: S002 Exchange Promotion Division contains 8 rows
- PASS: R10 crosswalks 24 of 43 central relation-sample rows
- PASS: S099 represented amount IDs match the three public-commission rows
- PASS: S002 archive SHA matches manifest
- PASS: S099 archive SHA matches manifest
- PASS: audit preserves 9 inherited human-reviewed relations and does not upgrade others

## Boundary checks

- PASS: S002 whole-table coverage is 10/616; classification is purposive sample.
- PASS: S002 field 10+11 coverage is 10/19; no full-field claim is allowed.
- PASS: S099's three explicitly public-commissioned rows are represented, while only 3/6 non-zero program-cost rows are selected.
- PASS: No central actor, relation, amount, function, source-log, or human-review table is mutated by this audit.
- PASS: Every generated table states that source-universe crosswalk status does not approve a sensitive relation.
