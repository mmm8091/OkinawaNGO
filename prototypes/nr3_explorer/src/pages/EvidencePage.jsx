import { useMemo, useState } from "react";
import { Books, MapPin, WarningCircle } from "@phosphor-icons/react";
import { tr, useLang } from "../lib/labels.js";
import { tu } from "../lib/ui_strings.js";
import { ChartHelp } from "../components/ui.jsx";

const ARCHIVE_ORDER = ["archived", "manual_archived", "failed", "skipped_non_url_reference"];

export function EvidencePage({ data }) {
  const view = data.coverageView;
  const cells = view?.cells || [];
  const implications = view?.implications || [];
  const lang = useLang();

  const dimensions = useMemo(() => {
    const order = view?.dimensions || [];
    return order.map((id) => {
      const dimCells = cells.filter((cell) => cell.dimension_id === id);
      const facets = [...new Set(dimCells.map((cell) => cell.facet))];
      const implication = implications.find((item) => item.dimension_id === id);
      return { id, cells: dimCells, facets, implication };
    });
  }, [cells, implications, view]);

  const [selectedId, setSelectedId] = useState(dimensions[0]?.id || null);
  const dimension = dimensions.find((item) => item.id === selectedId) || dimensions[0];

  return (
    <main className="workspace evidence-workspace">
      <div className="workspace-top">
        <div className="page-intro">
          <h1>
            {tu("evidence.title", lang)}
            <ChartHelp title={tu("evidence.title", lang)}>
              <p>{tu("help.evidence.p1", lang)}</p>
              <p>{tu("help.evidence.p2", lang)}</p>
            </ChartHelp>
          </h1>
        </div>
        <div className="path-summary">
          <Books size={18} />
          {tu("evidence.summary", lang)
            .replace("{c}", cells.length)
            .replace("{d}", dimensions.length)}
        </div>
      </div>
      <div className="evidence-grid">
        <aside className="episode-rail">
          {dimensions.map((item) => (
            <button
              key={item.id}
              className={`coverage-dim ${item.id === dimension?.id ? "active" : ""}`}
              onClick={() => setSelectedId(item.id)}
              type="button"
            >
              <strong>{tu(`dim.${item.id}`, lang)}</strong>
              <small>
                {item.id} · {item.cells.length}
                {tu("evidence.cellUnit", lang)}
              </small>
            </button>
          ))}
        </aside>
        <section className="coverage-body">
          {dimension?.facets.map((facet) => {
            const facetCells = dimension.cells.filter((cell) => cell.facet === facet);
            const max = Math.max(...facetCells.map((cell) => cell.count), 1);
            const denominator = facetCells[0]?.denominator;
            const unit = facetCells[0]?.unit;
            const isMatrix = facet === "source_type_x_archive";
            return (
              <section className="coverage-facet" key={facet}>
                <header>
                  <span>{tr(facet, lang)}</span>
                  <small>
                    {unit}
                    {denominator
                      ? ` · ${tu("evidence.denominator", lang).replace("{n}", denominator)}`
                      : ""}
                  </small>
                </header>
                {isMatrix ? (
                  <CoverageMatrix cells={facetCells} lang={lang} />
                ) : (
                  <div className="coverage-rows">
                    {facetCells.map((cell) => (
                      <div className="coverage-row" key={`${cell.category}-${cell.subcategory}`}>
                        <span className="coverage-cat" title={cell.category}>
                          {tr(cell.category, lang)}
                        </span>
                        <span className="coverage-track">
                          <i style={{ width: `${Math.max((cell.count / max) * 100, cell.count ? 1.5 : 0)}%` }} />
                        </span>
                        <span className="coverage-num">{cell.count}</span>
                        <span className="coverage-share">{cell.share_pct}%</span>
                      </div>
                    ))}
                  </div>
                )}
              </section>
            );
          })}
        </section>
        <aside className="detail-panel coverage-panel">
          {dimension?.implication ? (
            <>
              <div className="detail-eyebrow">
                <WarningCircle size={13} />
                {dimension.implication.dimension_id} · {tu(`dim.${dimension.id}`, lang)}
              </div>
              <div className="detail-heading">
                <div>
                  <h2>{tu(`dim.${dimension.id}`, lang)}</h2>
                  <p>{dimension.implication.observed_skew}</p>
                </div>
              </div>
              <section className="detail-section">
                <header>
                  <span>{tu("evidence.mechanism", lang)}</span>
                </header>
                <p className="coverage-text">{dimension.implication.visibility_mechanism}</p>
              </section>
              <section className="detail-section">
                <header>
                  <span>{tu("evidence.impact", lang)}</span>
                </header>
                <p className="coverage-text">{dimension.implication.impact_on_q1_q3}</p>
              </section>
              <section className="detail-section">
                <header>
                  <span>{tu("evidence.online", lang)}</span>
                </header>
                <p className="coverage-text">{dimension.implication.online_gap_action}</p>
              </section>
              <section className="detail-section">
                <header>
                  <span>{tu("evidence.local", lang)}</span>
                </header>
                <p className="coverage-text">{dimension.implication.local_gap_action}</p>
              </section>
              <section className="detail-section compact">
                <header>
                  <span>{tu("evidence.modules", lang)}</span>
                </header>
                <div className="place-tags">
                  {dimension.implication.affected_modules.map((module) => (
                    <span key={module}>
                      <MapPin size={13} />
                      {module}
                    </span>
                  ))}
                </div>
              </section>
              <div className="interpretation-note">
                <WarningCircle size={18} />
                <p>{dimension.implication.interpretation_limit}</p>
              </div>
            </>
          ) : (
            <div className="empty-note">{tu("evidence.noImplication", lang)}</div>
          )}
        </aside>
      </div>
    </main>
  );
}

function CoverageMatrix({ cells, lang }) {
  const types = [...new Set(cells.map((cell) => cell.category))];
  const byKey = new Map(
    cells.map((cell) => [`${cell.category}|${cell.subcategory}`, cell]),
  );
  const max = Math.max(...cells.map((cell) => cell.count), 1);
  return (
    <div className="coverage-matrix">
      <div className="matrix-head">
        <span />
        {ARCHIVE_ORDER.map((status) => (
          <span key={status}>{tr(status, lang)}</span>
        ))}
      </div>
      {types.map((type) => (
        <div className="matrix-row" key={type}>
          <span className="coverage-cat" title={type}>
            {tr(type, lang)}
          </span>
          {ARCHIVE_ORDER.map((status) => {
            const cell = byKey.get(`${type}|${status}`);
            const count = cell?.count ?? 0;
            return (
              <span
                key={status}
                className={`matrix-cell ${count ? "" : "zero"}`}
                title={cell ? `${count} 条 · ${cell.share_pct}%` : "0"}
              >
                <i style={{ opacity: count ? 0.25 + (count / max) * 0.75 : 0.06 }} />
                {count}
              </span>
            );
          })}
        </div>
      ))}
    </div>
  );
}
