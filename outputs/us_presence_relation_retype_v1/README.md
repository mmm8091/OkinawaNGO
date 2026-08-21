# Existing relation retype v1

This package maps the existing 43-row funding/support/relation sample to the
proposed U.S.-presence multilayer contracts. It adds no factual observation and
does not change any central review or claim status.

## Result

- 8 rows → `USN02 money_flows`
- 4 rows → `USN04 service_recipient`
- 9 rows → `USN05 affiliation_control`
- 20 rows → `USN06 action_institution`
- 1 grant opportunity → research lead only
- 1 rejected duplicate → history only

The split shows why the legacy 43 rows cannot be analysed as one funding or
organization network. Public commissions remain action/institution records
unless payment is separately evidenced; base service presence remains attached
to a place/institution node; in-kind transfers remain service-recipient facts;
membership remains structural affiliation.

## Files

- `relation_retype_crosswalk_v1.csv`: one proposal for each F001–F043 row.
- `mapping_summary_v1.csv`: counts by destination and original relation type.
- `HR_USN_relation_retype_rules_v1.csv`: six principal-confirmed group decisions covering all 43 rows (`accept` 5 / `revise` 1).
- `docs/human_review_research_USN_relation_retype_v1.md`: 2026-08-21 row-by-row semantic audit; its recommendations are now principal-confirmed.
- `docs/human_review_return_USN_relation_retype_v1.md`: formal return, decision boundaries and QA record.
- `scripts/validate_hr_usn_relation_retype_return_v1.py`: post-return rule and coverage validator.
- `validation_report_v1.json`: immutable pre-human row, key, mapping and decision-blank snapshot.
- `manifest.json`: immutable pre-human generation receipt; its README/rules hashes refer to the dispatched bytes, not the returned files.
- `post_return_validation_report_v1.json`: 2026-08-21 completed-rule, 43-row coverage and non-expansion checks.
- `post_return_manifest_v1.json`: hashes for the returned rules, return record, validator, README and post-return validation report.

The six rule decision cells and five-item principal architecture checkpoint are
complete. The 43-row crosswalk remains intentionally unexpanded until a
controlled integration design is reviewed. Approval of a destination table
only approves the semantic crosswalk; it does not approve an unreviewed fact,
fill an amount, resolve an endpoint, or make the row graph-eligible.

## Rebuild

```powershell
python scripts\make_us_presence_relation_retype_v1.py
python -m unittest tests.test_make_us_presence_relation_retype_v1
```
