import { useMemo, useState } from "react";
import { ClockCounterClockwise } from "@phosphor-icons/react";
import { labelOf } from "../lib/data.js";
import { tr, useLang } from "../lib/labels.js";
import { tu } from "../lib/ui_strings.js";
import { ChartHelp, PendingBadge } from "../components/ui.jsx";

const yearOf = (value) => String(value || "").match(/\d{4}/)?.[0] || null;

// Period anchors from the original Phase-1 plan (DOCX §3.2): plan-defined
// scopes, not data claims.
const PERIODS = [
  { id: "p1", from: 1972, to: 1997, range: "1972–1997" },
  { id: "p2", from: 1998, to: 2012, range: "1998–2012" },
  { id: "p3", from: 2013, to: 2019, range: "2013–2019" },
  { id: "p4", from: 2020, to: 2099, range: "2020–现在" },
];

const periodOf = (year) =>
  PERIODS.find((period) => {
    const value = Number(year);
    return value >= period.from && value <= period.to;
  }) || PERIODS[0];

export function TimePage({ data, onOpenActor, layer, candidates }) {
  const rows = data.relations.event_participation;
  const research = layer === "research" && candidates;
  const pendingRows = research ? candidates.relations.event_participation : [];
  const lang = useLang();
  const actorById = useMemo(
    () => new Map(data.actors.map((actor) => [actor.id, actor])),
    [data.actors],
  );

  const events = useMemo(() => {
    const byId = new Map();
    rows.forEach((row) => {
      const group =
        byId.get(row.event_id) || {
          id: row.event_id,
          label: row.event_label,
          date: row.event_date,
          rows: [],
          actions: new Set(),
          limits: new Set(),
        };
      group.rows.push(row);
      if (row.action_type) group.actions.add(row.action_type);
      if (row.interpretation_limit) group.limits.add(row.interpretation_limit);
      byId.set(row.event_id, group);
    });
    return [...byId.values()]
      .map((group) => ({ ...group, year: yearOf(group.date) }))
      .filter((group) => group.year);
  }, [rows]);

  const years = useMemo(() => {
    const counts = new Map();
    events.forEach((event) =>
      counts.set(event.year, (counts.get(event.year) || 0) + 1),
    );
    return [...counts.entries()].sort((a, b) => a[0].localeCompare(b[0]));
  }, [events]);

  const [year, setYear] = useState(() => {
    const pending = sessionStorage.getItem("nr3.year");
    if (pending && years.some(([value]) => value === pending)) {
      sessionStorage.removeItem("nr3.year");
      return pending;
    }
    return years.some(([value]) => value === "2015") ? "2015" : years[0]?.[0];
  });
  const maxCount = Math.max(...years.map(([, count]) => count), 1);
  const yearEvents = events.filter((event) => event.year === year);
  const registryRowCount = rows.filter((row) => row.is_registry_actor).length;
  const anchorCount = data.historicalAnchors.length;

  return (
    <main className="workspace time-workspace">
      <div className="workspace-top">
        <div className="page-intro">
          <h1>
            {tu("time.title", lang)}
            <ChartHelp title={tu("time.title", lang)}>
              <p>{tu("help.time.p1", lang)}</p>
              <p>{tu("help.time.p2", lang)}</p>
            </ChartHelp>
          </h1>
        </div>
        <div className="page-summary">
          <ClockCounterClockwise size={18} />
          {tu("time.summary", lang)
            .replace("{e}", events.length)
            .replace("{r}", rows.length)
            .replace("{a}", registryRowCount)}
          {research &&
            tu("time.pendingSuffix", lang).replace("{p}", pendingRows.length)}
        </div>
      </div>
      <div className="time-body">
        <div className="time-axis">
          {PERIODS.map((period) => {
            const periodYears = years.filter(([value]) => periodOf(value) === period);
            return (
              <section className="period-block" key={period.id}>
                <header>
                  <strong>
                    {period.id === "p4" ? tu("period.p4.range", lang) : period.range}
                  </strong>
                  <small>{tu(`period.${period.id}.focus`, lang)}</small>
                </header>
                <div className="period-years" role="tablist" aria-label={period.range}>
                  {periodYears.map(([value, count]) => (
                    <button
                      key={value}
                      role="tab"
                      aria-selected={year === value}
                      className={year === value ? "active" : ""}
                      onClick={() => setYear(value)}
                      type="button"
                    >
                      <span
                        className="bar"
                        style={{ height: `${14 + (count / maxCount) * 40}px` }}
                      />
                      <strong>{value}</strong>
                      <small>
                        {count}
                        {tu("time.eventUnit", lang)}
                      </small>
                    </button>
                  ))}
                  {!periodYears.length && (
                    <span className="period-empty">{tu("time.periodEmpty", lang)}</span>
                  )}
                </div>
              </section>
            );
          })}
        </div>
        <section className="genealogy-band">
          <header>
            <span>{tu("time.genealogy", lang)}</span>
            <small>{tu("time.genealogySub", lang)}</small>
          </header>
          {anchorCount ? null : (
            <div className="genealogy-gap">
              <strong>{tu("time.gapTitle", lang)}</strong>
              <p>{tu("time.gapText", lang)}</p>
            </div>
          )}
        </section>
        {research && pendingRows.length > 0 && (
          <section className="pending-strip">
            <header>
              <span>{tu("time.pendingHeader", lang)}</span>
              <small>{tu("time.pendingSub", lang)}</small>
            </header>
            <div className="pending-chips">
              {pendingRows.map((row) => (
                <span key={row.id}>
                  {row.event_label}
                  <PendingBadge>{tu("common.pending", lang)}</PendingBadge>
                </span>
              ))}
            </div>
          </section>
        )}
        <div className="time-events">
          {yearEvents.map((event) => {
            const registryRows = event.rows.filter((row) => row.is_registry_actor);
            const eventOnlyCount = event.rows.length - registryRows.length;
            return (
              <article className="event-card" key={event.id}>
                <header>
                  <h3>{event.label}</h3>
                  <p>{event.date}</p>
                </header>
                <div className="action-chips">
                  {[...event.actions].map((action) => (
                    <span key={action}>{tr(action, lang)}</span>
                  ))}
                </div>
                {!!registryRows.length && (
                  <div className="participant-chips">
                    {registryRows.map((row) => {
                      const actor = actorById.get(row.actor_id);
                      return (
                        <button
                          key={row.id}
                          type="button"
                          title={
                            actor
                              ? tu("overview.pickIssue", lang) + ` · ${labelOf(actor)}`
                              : row.actor_id
                          }
                          onClick={() => actor && onOpenActor(actor.id)}
                          disabled={!actor}
                        >
                          {row.participant_label || row.actor_id}
                        </button>
                      );
                    })}
                  </div>
                )}
                {eventOnlyCount > 0 && (
                  <p className="muted-line">
                    {tu("time.eventOnly", lang).replace("{n}", eventOnlyCount)}
                  </p>
                )}
                {event.limits.size > 0 && (
                  <p className="limit-line">{[...event.limits][0]}</p>
                )}
              </article>
            );
          })}
        </div>
      </div>
    </main>
  );
}
