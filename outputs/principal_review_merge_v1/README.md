# Principal-review source metadata overlay v1

This directory contains a non-mutating, machine-readable overlay for the
principal's completed HR-022 and HR-030 source reviews.

## Contents

- `source_metadata_overlay_v1.csv`
  - 71 rows total.
  - HR-022: 49 `accept_with_revision`.
  - HR-030: 1 `accept` and 21 `accept_with_revision`.
  - One row per authoritative review-queue item.
- `build_source_metadata_overlay.py`
  - Rebuilds the overlay from the two authoritative blank queues plus the
    principal-confirmed return-report decisions encoded in this directory.
  - Validates queue coverage, row count, uniqueness and required fields.

Authoritative queues:

- `outputs/phase1_source_integration_v1/HR022_source_metadata_review_v0.csv`
- `outputs/next_wave_source_integration_v1/HR030_source_metadata_archive_review_v0.csv`

Authoritative return reports are named in each overlay row's `source_report`
field.

## Merge boundary

This overlay does **not** modify the central source log, archive manifest,
actor registry, relation tables, candidate edges, figures or report prose.
It records source metadata, locator, support-scope, evidence-level and archive
handling decisions only.

Accepting a source does not approve:

- an actor identity or organizational continuity claim;
- an actor-to-actor edge, alliance or member relation;
- funding, payment, award or contract-payment semantics;
- election effects, policy causality or substantive project change.

Archive resolutions describe the approved handling of the source artifact.
Technical archive failure does not by itself invalidate accessible content.
Conversely, a successful archive does not expand the approved support scope.

## Important preservation rules

- S158 and S204 retain their existing `human_checked` source status.
- S279 uses its current archived state; the older failed state in the HR-030
  queue is stale.
- S137 must use the migrated court URL before archive retry.
- S197 must use the corrected 2018-10-19 meeting URL; S198 keeps the
  speaker/administrative-response split. SSL failure may remain a technical
  status.
- S294 is an academic presentation, not an academic article; archive retry
  requires normal browser headers and the researchmap parent-page referer.
- Source acceptance never converts co-appearance into alliance or project
  cost into actor payment.

## Validation

Run:

```powershell
python outputs\principal_review_merge_v1\build_source_metadata_overlay.py
```

Expected result:

```text
Wrote 71 rows ...\source_metadata_overlay_v1.csv
```
