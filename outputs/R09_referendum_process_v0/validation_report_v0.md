# R09 validation report v0

Generated: 2026-07-13

- Formal stage rows: 24; every row `review_status=accepted`.
- Reviewed-all stage rows: 33 (`accepted=24`, `needs_human_review=9`).
- Formal role rows: 25; every row `review_status=accepted`.
- Reviewed-all role rows: 34 (`accepted=25`, `needs_human_review=9`).
- Source rows: 32 ({"accepted": 20, "rejected": 2, "usable_with_limit": 10}).
- Rejected claims: 6.
- HR-017 queue: 18 pending stage/role records; all decision/reviewer/date/note fields blank.
- Case/stage/role/source/actor/existing-source foreign keys: passed.
- Per-case stage order and provisional-entity consistency: passed.
- Rejected sources unused by formal stages and roles: passed.
- Nago official vote-number assertions: passed.
- Ishigaki 2019-06-17 councillor-proposal wording assertion: passed.
- Ishigaki two-chain and neutral Supreme Court wording assertions: passed.
- A014 E2 / needs-human-review / local-retrieval boundary: passed.
- Individual plaintiff roles not transferred to A011: passed.
- Formal-report figures generated only from 24 accepted stages and 25 accepted roles: passed.
- HR-017 pending nodes absent from accepted-only PNG/SVG figures; reviewed-all figures retained as historical audit appendix: passed.
- Figure note preserves sequence-not-causality and A011 requester ≠ individual plaintiff boundaries: passed.
- Two consecutive executions on 2026-07-13: all generated outputs byte-stable by SHA-256.
