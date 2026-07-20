import { ArrowSquareOut, X } from "@phosphor-icons/react";
import { tr, useLang } from "../lib/labels.js";
import { tu } from "../lib/ui_strings.js";

export function EvidenceDrawer({ state, sourceIds, onClose }) {
  const lang = useLang();
  const ready = state.status === "ready";
  const sourceById = new Map(
    (ready ? state.evidence.sources : []).map((source) => [source.id, source]),
  );
  const rows = sourceIds
    .map((id) => sourceById.get(id))
    .filter(Boolean);
  const missing = sourceIds.filter((id) => !sourceById.has(id));

  return (
    <aside className="evidence-drawer" aria-label={tu("drawer.title", lang)}>
      <header className="drawer-header">
        <div>
          <strong>{tu("drawer.title", lang)}</strong>
          <small>{sourceIds.length}</small>
        </div>
        <button onClick={onClose} title={tu("common.close", lang)} type="button">
          <X size={18} />
        </button>
      </header>
      <div className="drawer-body">
        {state.status === "loading" && (
          <p className="drawer-note">{tu("drawer.loading", lang)}</p>
        )}
        {state.status === "error" && (
          <p className="drawer-note drawer-error" role="alert">
            {tu("drawer.error", lang)}
          </p>
        )}
        {ready &&
          rows.map((source) => (
            <article className="source-card" key={source.id}>
              <header>
                <span className="source-id">{source.id}</span>
                {!source.can_support_claim && (
                  <em className="no-claim">{tu("drawer.noClaim", lang)}</em>
                )}
              </header>
              <a
                className="source-title"
                href={source.url}
                target="_blank"
                rel="noreferrer"
              >
                {source.display_label}
                <ArrowSquareOut size={14} />
              </a>
              <div className="source-meta">
                <span>{tr(source.source_type, lang)}</span>
                <span>{source.evidence_level}</span>
                <span>{tr(source.review_status, lang)}</span>
              </div>
              {source.source_publication_date && (
                <p className="source-line">
                  <small>{tu("drawer.year", lang)}</small>
                  {source.source_publication_date}
                </p>
              )}
              {source.supports && (
                <p className="source-line">
                  <small>{tu("drawer.supports", lang)}</small>
                  {source.supports}
                </p>
              )}
              <p className="source-line">
                <small>{tu("drawer.archive", lang)}</small>
                {tr(source.archive_status, lang)}
                {source.archive_status === "failed" && tu("drawer.archiveFailed", lang)}
              </p>
              {source.archive_path && (
                <p className="source-line">
                  <small>locator</small>
                  <code className="source-locator">{source.archive_path}</code>
                </p>
              )}
              {source.bias_note && (
                <p className="source-line">
                  <small>{tu("drawer.bias", lang)}</small>
                  {source.bias_note}
                </p>
              )}
              {source.interpretation_limit && (
                <p className="source-limit">{source.interpretation_limit}</p>
              )}
            </article>
          ))}
        {ready &&
          missing.map((id) => (
            <p className="drawer-note" key={id}>
              {tu("drawer.missing", lang).replace("{id}", id)}
            </p>
          ))}
      </div>
    </aside>
  );
}
