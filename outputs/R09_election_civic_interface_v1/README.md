# R09 election-civic interface v1

HR-026 is merged: all 19 actor-event roles are `human_checked`.
R9EC018 is announcement-only and excluded from confirmed-held counts;
R9EC019 retains an unidentified organizer and is not actorized.

The five action classes describe public interfaces, not electoral
effects. No row licenses claims about votes, turnout, persuasion,
victory causality, policy uptake, registry membership, or stable alliance.

Regeneration order:

```powershell
python scripts\make_r09_election_civic_interface_v1.py
python scripts\merge_hr020_hr026_v1.py
```
