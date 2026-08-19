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
- `HR_USN_relation_retype_rules_v1.csv`: six blank group decisions covering all 43 rows.
- `validation_report_v1.json`: row, key, mapping and decision-blank checks.
- `manifest.json`: hashes and package status.

All row and rule decision cells are blank. Approval of a destination table only
approves the semantic crosswalk; it does not approve an unreviewed fact, fill an
amount, resolve an endpoint, or make the row graph-eligible.

## Rebuild

```powershell
python scripts\make_us_presence_relation_retype_v1.py
python -m unittest tests.test_make_us_presence_relation_retype_v1
```
