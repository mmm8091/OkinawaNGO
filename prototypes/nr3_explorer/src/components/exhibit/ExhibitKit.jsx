import { Quotes, WarningCircle } from "@phosphor-icons/react";
import "./exhibit.css";

// Shared exhibit kit: one anatomy for all published research exhibits.
// Data values, status labels, denominators and interpretation limits are
// always rendered from the payload; only chrome layout and copy length
// are unified here.

export function ExhibitHeader({ kicker, title, subtitle, metrics = [] }) {
  return (
    <header className="xh-header">
      <div className="xh-header-main">
        {kicker && <span className="xh-kicker">{kicker}</span>}
        <h2>{title}</h2>
        {subtitle && <p>{subtitle}</p>}
      </div>
      {metrics.length > 0 && (
        <div className="xh-metrics">
          {metrics.map((metric) => (
            <div className="xh-metric" key={metric.label}>
              <strong>{metric.value}</strong>
              <span>{metric.label}</span>
              {metric.note && <small>{metric.note}</small>}
            </div>
          ))}
        </div>
      )}
    </header>
  );
}

export function BoundaryNote({ title, children }) {
  return (
    <aside className="xh-boundary">
      <WarningCircle size={15} aria-hidden="true" />
      <p>
        {title && <b>{title} </b>}
        {children}
      </p>
    </aside>
  );
}

export function TierBadge({ tier, labels }) {
  return <em className={`xh-tier ${tier}`}>{labels[tier] || tier}</em>;
}

export function ExhibitTabs({ items, value, onChange, ariaLabel }) {
  return (
    <div className="xh-tabs" role="tablist" aria-label={ariaLabel}>
      {items.map((item) => (
        <button
          key={item.id}
          type="button"
          role="tab"
          aria-selected={value === item.id}
          className={value === item.id ? "active" : ""}
          onClick={() => onChange(item.id)}
        >
          <strong>{item.label}</strong>
          {item.note && <small>{item.note}</small>}
        </button>
      ))}
    </div>
  );
}

export function EmptyNote({ children }) {
  return <p className="xh-empty">{children}</p>;
}

export function Unavailable({ text }) {
  return (
    <section className="xh-unavailable" role="alert">
      <Quotes size={20} aria-hidden="true" />
      <strong>{text}</strong>
    </section>
  );
}

export function RecordCard({ id, title, badges = [], children }) {
  return (
    <details className="xh-record">
      <summary>
        <span className="xh-record-id">{id}</span>
        <span className="xh-record-title">{title}</span>
        {badges.length > 0 && <span className="xh-record-badges">{badges}</span>}
      </summary>
      <div className="xh-record-body">{children}</div>
    </details>
  );
}

export function MetaGrid({ items, cols = 4 }) {
  return (
    <dl className={`xh-meta-grid cols-${cols}`}>
      {items
        .filter((item) => item.value !== undefined && item.value !== null && item.value !== "")
        .map((item) => (
          <div key={item.label}>
            <dt>{item.label}</dt>
            <dd>{item.value}</dd>
          </div>
        ))}
    </dl>
  );
}

export function LimitLine({ label, text }) {
  if (!text) return null;
  return (
    <p className="xh-limit">
      {label && <b>{label} </b>}
      {text}
    </p>
  );
}
