# Figure brief — 载体—制度场域—材料留存时间图

Asset: `fig1_carrier_venue_trace_timeline_v1.svg`
Status: `research_only / candidate / ai_seeded / not_frontend_ready`

## Purpose

This figure visualizes the NR-05 empirical judgment: post-1998 traceability grows selectively through legal,
administrative and organization-hosted document regimes. It is not an actor-network graph and not an event
frequency chart.

## Panel design

- **Panel A** uses its own count axis for all-field Okinawa certified NPO corporations: 1999=6, 2004=163,
  2012=550. It is a macro institutional background and has a different denominator from every item below.
- **Panel B** is a qualitative three-lane timeline: carrier/organizational form → institutional venue →
  surviving record. Vertical or diagonal connectors join fields within one historical anchor only.
- The two panels share calendar position for orientation but **do not share a numeric y-axis**. No ratio,
  subtraction or trend comparison between the panels is valid.

## Source-relationship encoding

- Blue: `contemporaneous_primary`
- Orange: `retrospective`
- Green: `secondary`
- Gray: `lead`

Color applies to the surviving-record node, not to actor ideology, evidence certainty or organizational type.
All items still require the candidate/human-review gate.

## Reading route

1. Read Panel A only as the expansion of a legal/documentary environment.
2. In Panel B compare the materials left by a U.S. complaint, EIA opinion, court judgment, administrative
   diary, organization history, local newspaper and single party-news lead.
3. Notice that ONC's carrier starts in 1999 while the official certification field is 2009-05-14; the later
   interview's 2008 transition claim remains a separate unresolved stage.
4. Notice the explicit negative cases: 913 applicants are not actorized; A055 is support/movement, not the
   organizational plaintiff; co-signing is an event hyperedge, not an alliance.

## Data sources

- Panel A: NR05S002 and NR05S003/NR05S004.
- Panel B: selected H98_001, H98_003–H98_015 anchors. It is selective by design; omitted anchors are not
  absent events.

## Must not be read as

- the number or proportion of base-accountability actors that incorporated;
- a causal effect of the NPO Law;
- a network or alliance structure;
- organizational longevity;
- a complete 1998–2012 event census;
- evidence that actors with better archives were socially more central.

## Reproduce

```powershell
python scripts\make_history_1998_2012_online_v1.py
```
