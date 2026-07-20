import { ArrowRight, WarningCircle } from "@phosphor-icons/react";
import { labelOf } from "../lib/data.js";
import { tr, useLang } from "../lib/labels.js";
import { tu } from "../lib/ui_strings.js";
import { PendingBadge, SourceChips } from "./ui.jsx";

const FAMILY_COLORS = {
  resources_funding: "#b07a28",
  commission_service: "#6b7fa3",
  legal_collaboration: "#55756b",
  structural_affiliation: "#2b7f80",
  coordination: "#8a6c98",
};

// candidates.json may carry the typed collections under `relations` or at top
// level depending on the builder version; accept both.
const pick = (obj, key) => obj?.relations?.[key] || obj?.[key] || [];

function RelationRow({ row, actor, actorById, onSelectActor, lang }) {
  const outgoing = row.source_endpoint === actor.id;
  const otherId = outgoing ? row.target_endpoint : row.source_endpoint;
  const other = actorById.get(otherId);
  const otherName = other ? labelOf(other) : otherId;
  const OtherLink = (
    <button
      className="org-link"
      type="button"
      title={otherName}
      onClick={() => other && onSelectActor(otherId)}
      disabled={!other}
    >
      {otherName}
    </button>
  );

  return (
    <article className={`relation-row ${row.claim_status}`}>
      <header>
        <span
          className="family-chip"
          style={{ background: FAMILY_COLORS[row.relation_family] || "#9aa6a8" }}
        >
          {tr(row.relation_family, lang)}
        </span>
        <em className={`claim-chip ${row.claim_status}`}>{tr(row.claim_status, lang)}</em>
      </header>
      <strong className="relation-dir">
        {outgoing ? (
          <>
            {labelOf(actor)} <ArrowRight size={13} /> {OtherLink}
          </>
        ) : (
          <>
            {OtherLink} <ArrowRight size={13} /> {labelOf(actor)}
          </>
        )}
      </strong>
      <small className="relation-type">
        {tr(row.relation_type, lang)}
        {row.source_role && row.target_role
          ? ` · ${tr(row.source_role, lang)} → ${tr(row.target_role, lang)}`
          : ""}
      </small>
      {row.claim_status === "supported_bounded" && (
        <div className="scope-lines">
          {row.confirmed_scope && (
            <p>
              <small>{tu("relation.confirmed", lang)}</small>
              {row.confirmed_scope}
            </p>
          )}
          {row.missing_scope && (
            <p className="missing">
              <small>{tu("relation.missing", lang)}</small>
              {row.missing_scope}
            </p>
          )}
        </div>
      )}
      {(row.amount || row.amount_semantics || row.date_or_period) && (
        <small className="relation-amount">
          {row.amount ? `${row.amount} ${row.currency || ""} · ` : ""}
          {tr(row.amount_semantics, lang)}
          {row.date_or_period ? ` · ${row.date_or_period}` : ""}
        </small>
      )}
      <div className="relation-meta">
        <span>{row.evidence_level}</span>
        <span>{tr(row.review_status, lang)}</span>
        <SourceChips ids={row.source_ids || []} />
      </div>
      {row.interpretation_limit && <p className="limit-line">{row.interpretation_limit}</p>}
    </article>
  );
}

function RecordRow({ row, badge, lang }) {
  return (
    <article className="relation-row record">
      <header>
        <span className="record-type">{tr(row.relation_type, lang)}</span>
        <PendingBadge>{badge}</PendingBadge>
      </header>
      {row.case_id && (
        <p className="record-scope">
          <strong>{row.case_id}</strong> · {tr(row.role, lang)}
        </p>
      )}
      {row.event_or_program && (
        <p className="record-scope">{row.event_or_program}</p>
      )}
      {row.confirmed_scope && <p className="record-scope">{row.confirmed_scope}</p>}
      {row.missing_scope && (
        <p className="record-scope missing">
          <small>{tu("relation.missing", lang)}</small>
          {row.missing_scope}
        </p>
      )}
      {(row.amount || row.amount_semantics || row.date_or_period) && (
        <small className="relation-amount">
          {row.amount ? `${row.amount} ${row.currency || ""} · ` : ""}
          {row.amount_semantics ? tr(row.amount_semantics, lang) : ""}
          {row.amount_semantics && row.date_or_period ? " · " : ""}
          {row.date_or_period || ""}
        </small>
      )}
      <div className="relation-meta">
        <span>{row.evidence_level}</span>
        <span>{tr(row.review_status, lang)}</span>
        <SourceChips ids={row.source_ids || []} />
      </div>
      {row.interpretation_limit && <p className="limit-line">{row.interpretation_limit}</p>}
    </article>
  );
}

export function RelationArea({
  actor,
  actors,
  dyadicRelations,
  administrativeRecords,
  aggregateObservations,
  eventParticipation,
  caseRoles,
  layer,
  candidates,
  onSelectActor,
}) {
  const lang = useLang();
  const research = layer === "research" && candidates;
  const actorById = new Map(actors.map((item) => [item.id, item]));
  const involves = (row) =>
    row.source_endpoint === actor.id || row.target_endpoint === actor.id;

  const demoRelations = (dyadicRelations || []).filter(involves);
  const candRelations = research
    ? pick(candidates, "dyadic_relations").filter(involves)
    : [];
  const demoAdmin = (administrativeRecords || []).filter(involves);
  const candAdmin = research
    ? pick(candidates, "administrative_records").filter(involves)
    : [];
  const demoAgg = (aggregateObservations || []).filter(involves);
  const candAgg = research
    ? pick(candidates, "aggregate_observations").filter(involves)
    : [];
  const leads = research ? pick(candidates, "relation_leads").filter(involves) : [];
  const demoEventRecords = (eventParticipation || []).filter(involves);
  const candEventRecords = research
    ? pick(candidates, "event_participation").filter(involves)
    : [];
  const actorCaseRoles = (caseRoles || []).filter((row) => row.actor_id === actor.id);

  const countOf = (rows, status) => rows.filter((row) => row.claim_status === status).length;
  const counts = {
    s: countOf(demoRelations, "supported"),
    b: countOf(demoRelations, "supported_bounded"),
    c: candRelations.length,
    l: leads.length,
  };
  const countText = research
    ? tu("relation.counts", lang)
        .replace("{s}", counts.s)
        .replace("{b}", counts.b)
        .replace("{c}", counts.c)
        .replace("{l}", counts.l)
    : `${counts.s + counts.b}`;

  return (
    <>
      <section className="detail-section">
        <header>
          <span>{tu("section.relations", lang)}</span>
          <small>{countText}</small>
        </header>
        <div className="relation-list">
          {demoRelations.map((row) => (
            <RelationRow
              key={row.id}
              row={row}
              actor={actor}
              actorById={actorById}
              onSelectActor={onSelectActor}
              lang={lang}
            />
          ))}
          {candRelations.map((row) => (
            <RelationRow
              key={row.id}
              row={{ ...row, claim_status: row.claim_status || "candidate" }}
              actor={actor}
              actorById={actorById}
              onSelectActor={onSelectActor}
              lang={lang}
            />
          ))}
          {!demoRelations.length && !candRelations.length && (
            <div className="empty-note">
              <WarningCircle size={18} />
              {tu("empty.relations", lang)}
            </div>
          )}
        </div>
      </section>
      {research && (demoAdmin.length > 0 ||
        candAdmin.length > 0 ||
        demoAgg.length > 0 ||
        candAgg.length > 0 ||
        demoEventRecords.length > 0 ||
        candEventRecords.length > 0 ||
        actorCaseRoles.length > 0 ||
        leads.length > 0) && (
        <details className="detail-section research-records">
          <summary>
            <span>{tu("section.otherRecords", lang)}</span>
            <small>{tu("section.otherRecordsSub", lang)}</small>
          </summary>
          <div className="relation-list research-record-list">
            {[...demoAdmin, ...candAdmin, ...demoAgg, ...candAgg].map((row) => (
              <RecordRow
                key={row.id}
                row={row}
                badge={tu("relation.notDyadic", lang)}
                lang={lang}
              />
            ))}
            {[...demoEventRecords, ...candEventRecords].map((row) => (
              <RecordRow
                key={row.id}
                row={row}
                badge={tu("relation.eventRecord", lang)}
                lang={lang}
              />
            ))}
            {actorCaseRoles.map((row) => (
              <RecordRow
                key={row.id}
                row={row}
                badge={tu("relation.caseRole", lang)}
                lang={lang}
              />
            ))}
            {leads.map((row) => (
              <RecordRow
                key={row.id}
                row={row}
                badge={tu("relation.isLead", lang)}
                lang={lang}
              />
            ))}
          </div>
        </details>
      )}
    </>
  );
}
