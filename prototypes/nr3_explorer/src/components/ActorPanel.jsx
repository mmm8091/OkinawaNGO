import { useEffect, useState } from "react";
import {
  CaretRight,
  FileText,
  MapPin,
  Network,
} from "@phosphor-icons/react";
import { actorClassGroup, actorClassMeta, labelOf } from "../lib/data.js";
import { tr, useLang } from "../lib/labels.js";
import { tu } from "../lib/ui_strings.js";
import { EvidenceMark, PendingBadge, SourceChips } from "./ui.jsx";

export function ActorPanel({
  actor,
  issues,
  relations,
  issueFilter,
  onPickIssue,
  onPickYear,
  layer,
  candidates,
}) {
  const [sourcesOpen, setSourcesOpen] = useState(false);
  const research = layer === "research" && candidates;
  const lang = useLang();

  useEffect(() => {
    setSourcesOpen(false);
  }, [actor?.id]);

  const actorEdges = relations.actor_issue.filter(
    (edge) => edge.actor_id === actor?.id,
  );
  const actorPlaces = relations.actor_place.filter(
    (edge) => edge.actor_id === actor?.id,
  );
  const eventRows = relations.event_participation.filter(
    (edge) => edge.actor_id === actor?.id,
  );
  const candEdges = research
    ? candidates.relations.actor_issue.filter((edge) => edge.actor_id === actor?.id)
    : [];
  const candPlaces = research
    ? candidates.relations.actor_place.filter((edge) => edge.actor_id === actor?.id)
    : [];
  const issueById = new Map(issues.map((issue) => [issue.id, issue]));
  const groupId = actorClassGroup(actor?.actor_class);

  if (!actor) {
    return (
      <aside className="detail-panel actor-panel empty">
        <Network size={36} />
        <h2>{tu("actors.panelEmptyTitle", lang)}</h2>
        <p>{tu("actors.panelEmptyHint", lang)}</p>
      </aside>
    );
  }

  return (
    <aside className="detail-panel actor-panel">
      <div className="detail-eyebrow">
        <span
          className="region-swatch"
          style={{ background: actorClassMeta(actor.actor_class).color }}
        />
        {tu(`classGroup.${groupId}`, lang)}
      </div>
      <div className="actor-title">
        <EvidenceMark level={actor.evidence_level} />
        <div>
          <h2>{labelOf(actor)}</h2>
          <p>
            {actor.id} · {actor.legal_status}
          </p>
        </div>
      </div>
      <div className="metric-strip">
        <div>
          <strong>{actorEdges.length}</strong>
          <span>{tu("metric.issues", lang)}</span>
        </div>
        <div>
          <strong>{actorPlaces.length}</strong>
          <span>{tu("metric.places", lang)}</span>
        </div>
        <div>
          <strong>{eventRows.length}</strong>
          <span>{tu("metric.events", lang)}</span>
        </div>
      </div>
      <section className="detail-section">
        <header>
          <span>{tu("section.issues", lang)}</span>
          <small>{tu("section.issuesReviewed", lang)}</small>
        </header>
        <div className="issue-list">
          {actorEdges.map((edge) => {
            const issue = issueById.get(edge.issue_id);
            return (
              <button
                key={edge.id}
                type="button"
                className={`with-mark ${
                  issueFilter === edge.issue_id ? "active" : ""
                }`}
                title={tu("overview.pickIssue", lang)}
                onClick={() =>
                  onPickIssue(issueFilter === edge.issue_id ? "all" : edge.issue_id)
                }
              >
                <EvidenceMark level={edge.evidence_level} size="sm" />
                <span>
                  <strong>{issue ? tr(issue.display_label, lang) : edge.issue_id}</strong>
                </span>
                <CaretRight size={15} />
              </button>
            );
          })}
          {!actorEdges.length && (
            <div className="empty-note">{tu("empty.actorIssues", lang)}</div>
          )}
        </div>
      </section>
      {research && (
        <section className="detail-section">
          <header>
            <span>{tu("section.pendingIssues", lang)}</span>
            <small>{tu("section.pendingSub", lang)}</small>
          </header>
          <div className="issue-list">
            {candEdges.map((edge) => {
              const issue = issueById.get(edge.issue_id);
              return (
                <button
                  key={edge.id}
                  type="button"
                  className={`pending ${
                    issueFilter === edge.issue_id ? "active" : ""
                  }`}
                  title={tu("overview.pickIssue", lang)}
                  onClick={() =>
                    onPickIssue(issueFilter === edge.issue_id ? "all" : edge.issue_id)
                  }
                >
                  <span>
                    <strong>{issue ? tr(issue.display_label, lang) : edge.issue_id}</strong>
                  </span>
                  <PendingBadge>{tu("common.pending", lang)}</PendingBadge>
                  <CaretRight size={15} />
                </button>
              );
            })}
            {!candEdges.length && (
              <div className="empty-note">{tu("empty.actorPending", lang)}</div>
            )}
          </div>
        </section>
      )}
      <section className="detail-section compact">
        <header>
          <span>{tu("section.places", lang)}</span>
          <small>
            {actorPlaces.length}
            {research && candPlaces.length > 0
              ? ` +${candPlaces.length} ${tu("common.pending", lang)}`
              : ""}
          </small>
        </header>
        <div className="place-tags">
          {actorPlaces.map((edge) => (
            <span key={edge.id}>
              <MapPin size={13} />
              {tr(edge.canonical_place_label, lang)}
            </span>
          ))}
          {research &&
            candPlaces.map((edge) => (
              <span key={edge.id} className="pending">
                <MapPin size={13} />
                {tr(edge.canonical_place_label, lang)}
                <PendingBadge>{tu("common.pending", lang)}</PendingBadge>
              </span>
            ))}
          {!actorPlaces.length && !(research && candPlaces.length) && (
            <span className="muted-tag">{tu("empty.actorPlaces", lang)}</span>
          )}
        </div>
      </section>
      <section className="detail-section">
        <header>
          <span>{tu("section.events", lang)}</span>
          <small>{eventRows.length}</small>
        </header>
        <div className="issue-list">
          {eventRows.slice(0, 6).map((row) => (
            <button
              key={row.id}
              type="button"
              title={tu("overview.pickEvent", lang)}
              onClick={() =>
                onPickYear(String(row.event_date || "").match(/\d{4}/)?.[0])
              }
            >
              <span>
                <strong>{row.event_label}</strong>
              </span>
              <em>
                {row.event_date} · {tr(row.action_type, lang)}
              </em>
              <CaretRight size={15} />
            </button>
          ))}
          {!eventRows.length && (
            <div className="empty-note">{tu("empty.actorEvents", lang)}</div>
          )}
        </div>
      </section>
      <button
        className="evidence-button"
        type="button"
        onClick={() => setSourcesOpen(!sourcesOpen)}
      >
        <FileText size={18} />
        {sourcesOpen
          ? tu("sources.hide", lang)
          : tu("sources.show", lang).replace("{n}", actor.source_ids.length)}
        <CaretRight size={16} />
      </button>
      {sourcesOpen && (
        <>
          <SourceChips ids={actor.source_ids} />
          {!!actor.unresolved_source_refs?.length && (
            <div className="source-chips">
              <em>
                {tu("sources.unresolved", lang).replace(
                  "{n}",
                  actor.unresolved_source_refs.length,
                )}
              </em>
            </div>
          )}
        </>
      )}
    </aside>
  );
}
