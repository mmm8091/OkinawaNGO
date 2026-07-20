# NR-05 validation report

Package date: 2026-07-20

## Row counts

- `historical_anchor_candidates.csv`: 15
- `organization_status_candidates.csv`: 11
- `source_candidates.csv`: 32
- `online_exhausted_gaps.csv`: 10
- `human_review_queue.csv`: 20

## Gates

- PASS anchor count: 15 (contract 10-15)
- PASS research-only constants on 88 CSV rows
- PASS source_relationship vocabulary
- PASS separate source/event/activity/claim date semantics
- PASS source crosswalk integrity
- PASS exact locator and interpretation limit on every source
- PASS required domain coverage
- PASS structured relation-type candidates
- PASS sensitive ONC/A015/co-signing/Awase/person-collective gates
- PASS 1998 course-fieldwork/secondary boundary
- PASS NPO-universe-to-base-actor noninference gate
- PASS blank decisions and not-dispatched candidate-pool status
- PASS 1997 A068→A019 correction retained as known exclusion
- PASS archive catalog is locator-only
- PASS literature novelty boundary
- PASS ONC official-certification conflict and G008 online-rich gates
- PASS separated macro-count and carrier/venue/record SVG contract

The 20-row `human_review_queue.csv` is a research candidate pool only. It has not entered the formal HR ledger; the brief reduces the immediate principal checkpoint to seven bundled decisions.

## Known exclusions

- Full-text review corrected a search-snippet trap: the A068→A019 developmental reorganization is a 1997 event, while 2000 refers to later actions. It is excluded from NR-05 anchors and central `LC002` is not rewritten.
- Archive catalog entries are locator-only and never treated as the underlying primary item.
- Spencer (2003) already covers multi-issue anti-base framing; NR-05 does not claim that theme as novel.
- Prefecture-wide NPO counts do not infer incorporation, activity or survival of project actors.
- Smaller RIETI business-report/data-available sample counts are excluded from the cumulative certification series because the denominators differ.

## Deterministic file hashes

- `historical_anchor_candidates.csv`: `68350a37c6f2d42586f0b0851ee497843abb29896d691943e3cece8c09445c44`
- `organization_status_candidates.csv`: `527b2968e83c864a74fddaec6beeb3345b8692caae5c28a9b9a9a6b69d254887`
- `source_candidates.csv`: `cb54a4b5a7cb36e6355018ea34175ae9fae99957d9b267fd81df11a39ae3d927`
- `online_exhausted_gaps.csv`: `ac35dc5b4dfdc5b8a8da3445929b09c7495e6c53e8454fcafb5638aede60f4d1`
- `human_review_queue.csv`: `410bcb7d0bd48e01d49a2bd99c39f9565e26a3dc73d26fac851d9d4af0c2003d`
- `search_log.md`: `76aa89d3a2971ef48654d6dec3cb58e480993938b40050d67ee71d13b9686e96`
- `brief.md`: `e9a967be60341e33047521caa2f0619df66535767f0a1d2f4bb3f1644d4dbc87`
- `README.md`: `4c898fb1bb769cdc8a380d9a7cfdc8aa5bcc9d2d25785c8166f2ac586c86814a`
- `fig1_carrier_venue_trace_timeline_v1.svg`: `01bb2249f07463644802122aa5972b3311d8b2a335ad3b755a581a098f8f3f40`
- `fig1_carrier_venue_trace_timeline_v1_brief.md`: `9bab81acb73f29c8ad53a52e605cc8636948dc059afed6f7735d17f4b9e07aa0`

## Write boundary

The generator wrote only this output directory. It has no central-table, source-archive, frontend or control-document write path.
