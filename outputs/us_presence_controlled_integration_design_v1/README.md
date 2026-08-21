# USN controlled integration design v1

This package is a machine-checkable design contract. It does not modify central data and does not authorize a publication adapter or frontend release.

Files:

- `expected_central_actions_v1.csv`: object- and field-level future actions, including explicit holds.
- `expected_table_deltas_v1.csv`: known, bounded and unresolved table deltas.
- `id_namespace_plan_v1.csv`: identifier ownership and collision rules.
- `source_admission_plan_v1.csv`: source deduplication and archive sequencing.
- `test_matrix_v1.csv`: mandatory plan/apply/idempotence/failure-injection gates.
- `manifest.json`: package hashes and baseline receipts.

Authoritative narrative: `docs/us_presence_controlled_integration_design_v1.md`.

Validation:

```powershell
python scripts\validate_us_presence_controlled_integration_design_v1.py
```

Expected status: `PASS_DESIGN_ONLY`. No `data/interim/usn_v1/` tables or merger are created by this package.
