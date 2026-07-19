# HR-033 relation-status integration v1

Merged: 2026-07-20  
Human authority: project principal  
Return: `docs/human_review_return_HR033_legacy_relation_status_batch30_v1.md`

## Result

- F006, F007, F022 and F023 are `human_checked` umbrella-to-member relations.
- F021 is `human_revised`: a direct USD 3,250 donation, not sponsorship.
- F025 is `human_revised`: a bounded KOSC→AWWA contribution relation with no
  amount attached.
- R10R029 separately preserves the USD 102,000 scholarships-plus-AWWA
  aggregate. It is not a dyadic organization edge.
- No legacy `verified` value remains in the six-row HR-033 scope.

## Files

- `typed_relation_observations_v1.csv`: seven normalized frontend control
  observations: six dyadic relations and one aggregate observation.
- `integration_summary_v1.csv`: merge counts and boundary checks.

## Frontend boundary

The typed CSV is a controlled handoff for the NR-02 builder, not a browser data
file. The builder must validate endpoints and derive final collections and
display tiers. Membership does not imply funding, control, alliance or policy
position. The aggregate USD 102,000 must never be attached to F025.

## Reproduce

```powershell
python scripts\merge_hr033.py
python -m unittest tests.test_merge_hr033
```
