# report_claim_audit_v1

Reproducible paragraph/claim audit of `docs/phase1_research_report_v0.md`.

- Main audit: `data/interim/38_report_claim_evidence_audit_v1.csv`
- Mechanical repair queue: `mechanical_fix_queue_v1.csv`
- Existing human-gate blockers: `publication_blockers_v1.csv`
- Principal-confirmed interpretive decisions: `HR031_report_claim_review_v0.csv`
- Applied decision ledger: `hr031_principal_application_v1.csv`
- Numeric comparisons: `numeric_check_results_v1.csv`
- Claim/source validation: `claim_source_crosswalk_v1.csv`
- Claim/formal-table validation: `claim_formal_table_crosswalk_v1.csv`
- Red-line scan: `red_line_scan_v1.csv`

HR-031 selected B for all three groups, and the corresponding report passages were revised on
2026-07-20. The summary SHA below describes the pre-HR031 report snapshot and is no longer the current
report hash. The original full audit builder remains historical until its frozen counts and claim text are
updated; do not rerun it unchanged against the current merged layer.
