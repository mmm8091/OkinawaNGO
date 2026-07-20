# NR-03 Design QA

- source visual truth path: `C:\Users\10857\.codex\generated_images\019f73f3-ca8f-7d51-8fd1-82d5436342e2\call_Up8MiS8BGt83zGMUctd0D2d4.png`
- implementation URL: `http://localhost:4173/`
- implementation screenshot paths (current rewrite): `prototypes/nr3_explorer/qa/final2_overview.png`, `final2_actors.png`, `final2_actors_zoomed.png`, `final2_time.png`
- intended viewport: 1488 × 1024
- state: Overview default; Actors default reviewed-link state; Time default 2015

## Current status (2026-07-19, iteration 3)

The first implementation was treated by the principal as an intention draft; the frontend was
then rewritten (component split under `src/lib`, `src/components`, `src/pages`) with the
following principal decisions applied:

1. 严格证据 map state removed — Overview states are 全域 / 先岛聚焦 only.
2. Time layer is a dedicated fifth page (`#/time`), not a shared bottom sheet; nothing overlays
   any canvas.
3. No evidence-depth marks on the Overview (region labels carry plain region-color dots; the
   depth legend is gone). Per-relation evidence levels remain in the actor detail panel.
4. Type scale established as a design rule: 11 / 12 / 13 / 14 / 19 / 22 / 24 px; no UI text
   below 11px; graph labels render in screen space so zoom never shrinks them.
5. Actors canvas gained wheel zoom-to-cursor (0.6–3.0), drag pan, buttons, and reset — same
   interaction family as the map.
6. Issue/place names stay as taxonomy codes; the planned zh/ja/en mapping is a data-layer
   (NR-02) deliverable, consumed via `labelOf()` when it ships.

## Verified with rendered evidence + scripted interaction (headless Chrome)

- Overview: 2-state segmented; land click selects the polygon's region (冲绳本岛 ✓); hover
  tooltip shows municipality (名護市 ✓); wheel zoom 120% ✓; sakishima aggregation ✓; no
  timeline sheet; no depth legend.
- Actors: wheel zoom 100%→118% ✓; drag pan ✓; reset 100% ✓; selected-actor pill label;
  hover name tooltip; empty-canvas deselect; class/issue/search filters; legend and filter
  counts cover only the 23 reviewed-edge actors.
- Time: 10 year tabs; 2015 shows 2 event cards; 1997 shows 1; participant chip deep-links to
  the actor on the Actors page (与那国自衛隊配備反対意見広告実行委員会 ✓); event-only
  participants counted, never listed; empty historical-anchor boundary stated.
- Pathways (added after principal go-ahead): 9 episodes in 7 route families; six-stage ladder
  renders episode fields + per-tier outcomes; TE01 shows 未观察到 on both result stages,
  TE06 shows 部分/混合 ✓; actor chip deep-links to Actors (泡瀬干潟を守る連絡会 ✓);
  view-level interpretation limits visible. Screenshots: `qa/final3_pathways*.png`.
- Console: 0 errors/warnings across all scripted runs.
- `npm run build` passes.

## Findings fixed in iteration 2 (2026-07-19, earlier same day)

- [P0] Region→place mapping used a regex over `place.region`; P013 Miyako (registry region
  `Sakishima`) vanished from 宫古群岛 and leaked into 八重山群岛 tags.
  Fix: explicit presentation-only `PLACE_DISPLAY_REGION` map.
- [P0] Nearest-centroid map selection could pick the wrong region (本岛 click → 周边岛屿).
  Fix: point-in-polygon hit testing (identity-transform guard for any devicePixelRatio).
- [P0] Region labels were fixed-position overlays and detached from geography on zoom.
  Fix: labels anchored to projected municipality centroids, updated on every draw.
- [P1] React passive wheel listener caused console errors; no drag pan.
  Fix: native non-passive wheel + zoom-to-cursor + clamped drag pan.
- [P1] Actors legend dropped the 7th group; class filter counts covered all 122 actors while
  the canvas shows 23. Fix: counts computed from reviewed-edge actors.
- [P1] Selected-actor label collided with issue labels; nodes unlabeled until clicked.
  Fix: pill label drawn last + hover tooltip + empty-click deselect.
- [P2] Dead controls (compare toggle, filter icon, inert segmented layers, inert issue rows,
  inert source button). Fix: honest disable / removal / real wiring incl. cross-page deep links.
- [P2] favicon 404. Fix: inline SVG icon.

## Open items for the principal

- Time page event cards show action-type codes (`co_signing`, …) and the data's English
  `interpretation_limit` lines verbatim; these belong to the same future zh/ja/en mapping work.
- The map's visual salience is still bounded by real archipelago geography (long NE–SW chain);
  default fit shows all 42 municipalities.
- The IA document was amended (`docs/exploration_system_information_architecture_v1.md` §12)
  to record the five-page revision; principal confirmation requested.

## Comparison history

- Iteration 1: dense copy, slow/inaccessible map zoom, false unclassified labels → fixed.
- Iteration 2: rendered evidence captured; P0 region-mapping/hit-test/label-anchor bugs,
  P1 passive-wheel/pan/legend-count/label-collision bugs, P2 dead controls fixed.
- Iteration 3: principal redesign decisions (5th time page, no strict state, no depth marks,
  type scale, codes-not-English) implemented in a full rewrite; regression green.
- Iteration 4 (2026-07-19): principal round-3 decisions — copy discipline (no non-permanent
  text), chart-name titles with "?" help popovers, research view (演示/研究) showing reviewed +
  pending with dashed/待审 marks on all four pages, time-page period anchors from the DOCX and
  an honest genealogy gap band. Pathways page added earlier the same day. One real bug found by
  rendered QA: a legacy `.page-intro span` rule silently overrode the popover's `display:none`
  (kept it always visible); fixed by deleting the dead rule. Screenshots: `qa/clean_*.png`,
  `qa/final4_*_research.png`.
- Iteration 5 (2026-07-19): Evidence page (V4) shipped — 6 dimensions, per-facet bars with
  count/share/unit/denominator, D5 source-type × archive matrix, implication panel
  (mechanism / impact / online+local gap actions / affected modules / interpretation limit).
  All five IA pages are now live; the evidence nav item is enabled. "?" icon redrawn as inline
  SVG after principal feedback. Screenshots: `qa/final5_*.png`.
- Iteration 6 (2026-07-19): principal approved the zh/ja/en label mapping
  (`data/metadata/display_label_mapping_draft_v0.csv`, now 229 codes incl. 73 source types and
  facet names). Frontend consumes it through a generated `src/lib/labels.js` + topbar 中/日/EN
  switch (default zh); ChartHelp copy rewritten in positive, instructive phrasing per principal
  feedback (no stacked negations). Global evidence drawer shipped: any source chip opens the
  drawer with source title/URL, type, level, review status, publication year, supports,
  archive status, bias note and interpretation limit; `can_support_claim=false` is flagged.
  Screenshots: `qa/final6_*.png`, `qa/final7_*.png`.
- Iteration 7 (2026-07-19): full-UI i18n — fixed interface copy (nav, page titles, metrics,
  section headers, stage names, status chips, period labels, drawer, loading, help popovers)
  moved into `src/lib/ui_strings.js` (zh/ja/en), so the 中/日/EN switch now covers both data
  codes and UI chrome. Brand mark filled to match the "?" affordance. Screenshots:
  `qa/final8_*.png`.
- Iteration 8 (2026-07-19, rectification after main-thread acceptance): all ten findings
  fixed and re-verified — region panel episode entries (map→place→episode→evidence chain),
  full 122-actor search incl. IDs and aliases (A073 reachable), actor event lists with
  year deep-links (actor→issue→event→evidence chain), region compare and episode six-stage
  compare, drawer locator, ≤820px mobile breakpoint (390×844 no horizontal overflow),
  research-summary wording (已核 9 ＋ 待审 4), English dimension names, aria-hidden removed
  from interactive map labels, handoff screenshots retaken with forced state reset and
  md5-distinct pairs, workbench staleness corrected. Handoff updated to `docs/nr3_handoff_v1.md` v2.
- Iteration 9 (2026-07-20, recheck wrap-up per `nr3_recheck_and_relation_frontend_brief_v1.md`):
  EN-mode Chinese residuals swept (brand name, nav/lang/layer aria-labels, canvas aria-labels,
  control titles, map-state aria, evidence title/help, period range — remaining CJK is data
  fields or the 中/日 switcher labels by design); 演示视图 renamed 已核视图 per principal
  decision; handoff doc separates the A073 search test from the A002 event chain; evidence
  drawer closes on route change. Verified at 1280×900 and 390×844; build + console PASS/0.
- Iteration 10 (2026-07-20, relation layer): NR-02 builder extended with typed relation
  collections (historical pre-merge snapshot; counts superseded by iteration 11). L0 panel relation area +
  other-records/leads area; L1 relation graph state on the Actors page (family colors,
  direction arrows, reviewed solid/candidate dashed, per-family toggles, edge detail card,
  layered counts). Control cases verified: F021 supported USD 3,250 direct donation;
  F025 supported_bounded with empty amount and visible missing scope; R10R029 only in the
  aggregate records area, never on the graph. Screenshots: `qa/rel_*.png`.
- Iteration 11 (2026-07-20, post-merge repair): rebuilt from the merged central
  field-level decisions instead of re-inferring all non-HR033 rows. Current typed split:
  14 reviewed/8 candidate dyadic relations, 6 reviewed/5 candidate administrative
  records, 2 aggregate observations, 4 reviewed event-participation records, 4 research
  leads and 27 case roles; F036 remains event participation. A072 is hidden from ordinary
  search and display; AI068 and other deactivated actor-issue rows are absent from the
  default graph (238 active inputs). Relation-class filtering changes the visible family
  counts; AWWA panel renders bounded amount semantics; NOSCO panel labels F036 as event
  participation and explicitly rejects alliance inference. `npm run build` and the full
  Python suite pass; page console has no app-origin warning/error (only unrelated browser
  extension warnings).

final result: pass (agent-verified with rendered evidence; awaiting principal confirmation)

- Iteration 14 (2026-07-20, actor–issue gate states per `frontend_actor_issue_state_handoff_v1.md`):
  builder derives fact/scope/schema-freeze gates plus `display_state` and passes through 10
  central fields; counts verified exactly 7/58/59/114 with research fact-gate 143/25/5
  (22/22 builder tests, validation PASS). Frontend consumes `display_state` without deriving:
  edge rows carry state chips (frozen_bounded / accepted_unfrozen / scope_reviewed_fact_pending /
  fact_pending) and needs_* overlays; canvas note reads 65 accepted (7 field-frozen) and
  research 65+173 with "其中 59 条已完成范围复核"; pending-section sublabel no longer says
  未人审; help text clarifies reviewed = displayed fact edges, not actor identity. Verified on
  A002 (accepted_unfrozen chips) and A059 (scope_reviewed_fact_pending / fact_pending chips).
  Screenshots: `qa/states_*.png`.

- Iteration 13 (2026-07-20, data-version visibility rework per main-thread recheck): topbar
  version stamp (as_of_date · short build id · 121 active / 122 provenance from manifest);
  class filter reads 当前图中组织（25/121）and research shows 103/121 with an explicit
  "18 个无边组织只可搜索" note; actor card shows evidence_level / review_status / scope_status;
  X014 visibly marked watchlist_only in search and panel; A072 (merged_duplicate) hidden from
  search and graphs; build-id watch polls manifest (20s + window focus) and offers a reload
  banner; handoff counts unified (14 reviewed = 10 supported + 4 supported_bounded, admin
  6+5, aggregate 2, event 4, lead 4, case roles 27). Verified at 1488×1024; console clean.
  Screenshots: `qa/version_*.png`.

- Iteration 12 (2026-07-20, header unification): page headers normalized to one spec —
  row 1 = chart title + "?" left and the page's primary control right; row 2 (when needed) =
  `.toolbar-row` with search and inline filters. The Actors header no longer wraps three
  control groups into dead space; time/pathways/evidence summaries merged into one
  `.page-summary` component. Parallel main-thread additions (case-role and event-participation
  records in the panel, iteration 11 post-merge repair) verified intact. Screenshots:
  `qa/unified_*.png`.

- Iteration 14b (2026-07-20): page title now follows graph state — 议题生态 mode shows
  组织—议题生态图, 组织关系 mode shows 组织关系图, each with its own "?" reading text
  (relation help: family colors, direction arrows, solid/dashed semantics, dyadic-only scope).

- Iteration 15 (2026-07-20, post-freeze regeneration and browser QA): rebuilt the explorer
  from the merged 145-item online-review layer. Current actor–issue split is 125 reviewed /
  158 research, with display states 67 frozen_bounded / 58 accepted_unfrozen /
  44 scope_reviewed_fact_pending / 114 fact_pending; strict place–issue is 71 reviewed /
  234 research. In-app browser checks passed on all five routes at 1280×900 and 390×844.
  A real mobile overflow was found in the topbar and Actors header controls; the ≤820px
  grid, segmented controls, search and filters now shrink or wrap, leaving all five pages at
  375px document width in the 390px viewport. App console: 0 warning / 0 error. Time-page
  genealogy remains an explicit open defect: five reviewed central LC records exist, but
  `genealogy_anchors` still exports 0.

- Iteration 14c (2026-07-20): issue nodes in the ecology canvas are clickable — hover shows
  issue name + edge count, click focuses that issue (same selection state as the toolbar
  select and panel issue rows), second click resets. Hit testing now picks the nearer of
  actor vs issue node, so issue nodes stay clickable inside dense actor clusters. Verified
  full focus/reset cycle (儒艮保护 I004 → all).

- Iteration 15 (2026-07-21, exhibit refactor): three published exhibits rebuilt on a shared
  kit (`src/components/exhibit/`): ExhibitHeader, BoundaryNote, TierBadge, ExhibitTabs,
  RecordCard, MetaGrid, LimitLine, Unavailable — replacing ~2,000 lines of duplicated
  per-exhibit CSS with one anatomy. Sakishima frame exhibit: compact observation/excerpt
  cards with expandable meta+sources+limits, place tabs, frame filter, data-driven scope
  note. Repeat participation: three event cards with tier stacks and one merged boundary
  line. Official collaboration: header metric cards, boundary line, mode tabs, summary
  rows with bars, and collapsed compact trace references. Lifecycle anchors on the Time
  page became compact expandable cards. Relation graph: coordination family now defaults
  on in research view. Fixed a state-destroying gate where switching layers unmounted the
  whole page (research overlay now merges asynchronously; overlay failure shows a
  non-blocking banner instead). Verified: 7/7 npm tests, build PASS with release stamp,
  sakishima demo/research (8→15 records) without remount, OCE 15 rows + collapsed traces,
  lifecycle 5 cards, repeat 3 cards, EN pass, 390px no overflow. Screenshots:
  `qa/refactor_*.png`.

- Iteration 16 (2026-07-21, sakishima v2 redesign after principal critique): the frame
  corpus moved from a text list with cryptic dual numbers to stacked obs/exc frame bars
  (click-to-filter); observation and excerpt columns merged into one record list with
  type tabs (all/observations/excerpts) and type badges; the long research boundary
  collapsed to one line plus an expander; scope note is data-driven; period labels on the
  time axis no longer orphan-wrap. Commits 0e89ef0e (shared kit + layer-state fix) and
  b10fadeb (v2 redesign); dist rebuilt, release.json source_commit == HEAD,
  source_dirty == false, validation pass. Screenshots: `qa/v2_*.png`.

- Iteration 17 (2026-07-21, principal screenshot review fixes): full interpretation text
  moved behind a "?" popover (one visible boundary line — the inline expander and footer
  methodology lines are gone); time page axis/genealogy/pending bands made flex-shrink:0 so
  the year selector is never covered and no inner horizontal scrollbars remain; R5 event
  cards normalized to the type scale (no oversized numbers), redundant hints removed; OCE
  hardcoded metric fallbacks replaced by data-or-"—" (real values 616/86/15/76.1%/3.1% now
  provably from payload). Commit 18c1bf7; dist rebuilt, release.json aligned. Screenshots:
  `qa/fix_*.png`.

- Iteration 18 (2026-07-21, public-presentation taste pass): removed the visible build stamp,
  made each selected subview own its title, replaced defensive blocks with compact help,
  compressed time-event records into expandable rows, and kept research queues out of the
  reviewed actor panel. Reviewed and research actor panels now share the same visual anatomy:
  both retain evidence marks, actor metadata and issue-status chips; only the research layer
  adds pending records. Exhibit boundary help now reuses the site-wide `ChartHelp` component
  instead of maintaining a second question-mark control. R5 and R10 exhibits now lead with a question or
  finding; time-event labels/actions are trilingual. Browser route QA caught and repaired a
  MapPin runtime regression on Evidence; all five routes are required to render with zero
  console errors. A final copy pass rewrote defensive “not / does not mean” disclaimers as
  reading instructions: each surface now states its unit, the comparison it supports and the
  evidence layer to open for adjacent questions. Frozen English audit text remains verbatim
  where the publication validator requires exact source equality.
