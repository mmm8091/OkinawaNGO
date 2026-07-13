# report_claim_audit_v1

Reproducible paragraph/claim audit of `docs/phase1_research_report_v0.md`.

- Main audit: `data/interim/38_report_claim_evidence_audit_v1.csv`
- Mechanical repair queue: `mechanical_fix_queue_v1.csv`
- Existing human-gate blockers: `publication_blockers_v1.csv`
- New interpretive decisions only: `HR031_report_claim_review_v0.csv`
- Numeric comparisons: `numeric_check_results_v1.csv`
- Claim/source validation: `claim_source_crosswalk_v1.csv`
- Claim/formal-table validation: `claim_formal_table_crosswalk_v1.csv`
- Red-line scan: `red_line_scan_v1.csv`

Run from the repository root with `python scripts/audit_report_claims_v1.py`. The script does not modify the report or central research tables.
