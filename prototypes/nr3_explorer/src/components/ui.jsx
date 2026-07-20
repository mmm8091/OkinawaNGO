import { Circle, CircleHalf } from "@phosphor-icons/react";
import { useEvidence } from "../lib/data.js";
import { useLang } from "../lib/labels.js";
import { tu } from "../lib/ui_strings.js";

export function SegmentedControl({ value, onChange, items, label }) {
  return (
    <div className="segmented" aria-label={label}>
      {items.map((item) => (
        <button
          key={item.id}
          className={value === item.id ? "active" : ""}
          onClick={() => onChange(item.id)}
          type="button"
        >
          {item.icon && <item.icon size={17} />}
          {item.label}
        </button>
      ))}
    </div>
  );
}

export function EvidenceMark({ level = "E4", size = "md" }) {
  const pixels = size === "sm" ? 13 : 18;
  const Icon = level === "E3" ? CircleHalf : Circle;
  return (
    <span className={`evidence-mark ${size}`} aria-label={`证据 ${level}`}>
      <Icon
        size={pixels}
        weight={level === "E4" || level === "E3" ? "fill" : "regular"}
      />
    </span>
  );
}

// "?" affordance next to each chart title: how-to-read and interpretation
// boundaries live here, not as persistent on-canvas copy.
export function ChartHelp({ title, children }) {
  const lang = useLang();
  const ariaLabel = tu("chartHelp.aria", lang).replace("{title}", title);
  return (
    <span className="chart-help" tabIndex={0} aria-label={ariaLabel}>
      <svg viewBox="0 0 22 22" width="22" height="22" aria-hidden="true">
        <circle cx="11" cy="11" r="10.5" fill="currentColor" />
        <text
          x="11"
          y="15.2"
          textAnchor="middle"
          fontSize="12.5"
          fontWeight="700"
          fill="#f6f4ec"
          fontFamily="'Noto Sans SC', sans-serif"
        >
          ?
        </text>
      </svg>
      <span className="chart-help-pop">
        <strong>{title}</strong>
        {children}
      </span>
    </span>
  );
}

export function PendingBadge({ children }) {
  return <em className="pending-badge">{children || "待审"}</em>;
}

export function SourceChips({ ids }) {
  const { openEvidence } = useEvidence();
  return (
    <div className="source-chips">
      {ids.map((id) => (
        <button key={id} type="button" onClick={() => openEvidence(ids)}>
          {id}
        </button>
      ))}
    </div>
  );
}
