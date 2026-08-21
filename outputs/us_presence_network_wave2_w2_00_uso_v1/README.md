# W2-00 USO / USAspending anchor package v1

Date: 2026-08-22
Status: `research_only`; official-primary extraction pending principal review
Scope: USO 2024 national finance and impact anchors, DoD award `HQ00342310002`, and the Indo-Pacific–Japan/Okinawa site hierarchy

This package does not write any central table, create an S-ID, add a funding edge, update a publication adapter, or change the frontend.

## What is now established

1. **USO has two different 2024 financial perimeters.** The audited consolidated statement reports USD 265.050 million in support and revenue, USD 204.912 million in gross program-services expense, and USD 258.883 million in operating expense. USO, Inc.'s IRS Form 990 separately reports USD 168.028 million in total revenue, USD 111.074 million in program-service expense, and USD 163.487 million in total expense. These figures are retained side by side and are neither added nor substituted.
2. **The three public impact counts measure different things.** USO reports more than 11.3 million program/service uses, more than 7.2 million center visits, and more than 950,000 people reached or provided programs. Uses, visits and people are not interchangeable.
3. **The Okinawa “6 versus 8” count is a type problem, not evidence of two incompatible organizations.** The official April 2025 narrative names six operating centers: Foster, Hansen, Kinser, Schwab, Futenma and Kadena. The current Okinawa directory lists eight presences because it also includes the Kadena AMC Terminal and the Okinawa Area Office. The site ledger therefore uses six centers and eight typed presences.
4. **The DoD award is national and the local allocation layer is missing.** USAspending identifies United Service Organizations, Inc. as the prime recipient of grant `HQ00342310002`; the award-level cumulative obligation is USD 72 million over a stated 2023-09-30 to 2028-09-29 performance period. The inspected public award, transaction and subaward fields do not disclose a Japan, Indo-Pacific, Okinawa or center allocation.
5. **A zero subaward count is bounded.** The award overview reports zero subawards, and the saved FAIN search returned no subaward rows. That does not resolve internal regional allocations, interoffice transfers, procurement or reimbursements.

## The interrupted chain

The official records close these segments:

`DoD / WHS → USO, Inc. national award`
`USO, Inc. → Indo-Pacific region → USO Japan / USO Okinawa → Okinawa presences`

They do not close the monetary segment between the national prime award and the operating hierarchy. This package therefore does not estimate an Okinawa budget and does not create a DoD-to-USO Okinawa money relation.

## Files

- `anchor_candidates_v1.csv` — 32 typed anchor observations with allowed and prohibited claims.
- `source_receipts_v1.csv` — 11 frozen official-source receipts with local paths and SHA-256 hashes.
- `site_hierarchy_probe_v1.csv` — regional, area and Okinawa-presence typing, including the six-center/eight-presence resolution.
- `change_notes_v1.csv` — eight recorded changes to initial assumptions and calculation semantics.
- `artifacts/` — downloaded official PDFs, HTML snapshots, USAspending API responses, and the two POST request bodies used for reproducibility.

## Reading order

1. Read `change_notes_v1.csv`, especially `W2B-CN001`, `W2B-CN004`, `W2B-CN005` and `W2B-CN006`.
2. Use `anchor_candidates_v1.csv` for exact figures and claim boundaries.
3. Use `site_hierarchy_probe_v1.csv` for the center/presence distinction.
4. Open the artifact named by each source receipt and follow its `exact_locator`.

## Method and remaining decisions

- All facts here were extracted from USO or USAspending primary records. They have not received principal human review and remain outside the central fact layer.
- Every row-level `review_status` in the anchor, hierarchy and change-note tables is therefore `ai_seeded`. Research-package semantics remain in `anchor_status`, `classification`, `decision_status`, source receipts and notes; `ai_seeded` is not human approval.
- `W2B-A030` preserves a USAspending field-semantic issue: the retrieved overview exposes USD 41.212 million in account-obligation/transaction-obligated fields alongside the USD 72 million award-level total. The package does not rename either as cash paid or expenditure.
- The global ratio `USD 204.912m / at least 11.3m uses` is only a scale diagnostic. It is at most about USD 18.13 per reported use and is not a unit cost.
- The approximately 47,000 people supported by USO Okinawa is an organization-reported 2025 scale statement, not a same-year official population denominator for the 2024 financial data.

## Reproduction and validation

The API request bodies are frozen as:

- `artifacts/usaspending_transactions_request.json`
- `artifacts/usaspending_subawards_request.json`

Recheck file hashes in PowerShell:

```powershell
Get-ChildItem outputs/us_presence_network_wave2_w2_00_uso_v1/artifacts -File |
  Get-FileHash -Algorithm SHA256
```

The package was validated for CSV rectangularity, unique IDs, referenced receipt IDs, artifact existence, SHA-256 agreement, JSON parsing, PDF readability and legal row-level `review_status` values (`ai_seeded` throughout). No central data or frontend build is part of this validation.
