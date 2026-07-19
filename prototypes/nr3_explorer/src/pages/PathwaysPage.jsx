import { Fragment, useMemo, useState } from "react";
import {
  ArrowsLeftRight,
  CaretRight,
  Circle,
  CircleHalf,
  GitBranch,
  MapPin,
} from "@phosphor-icons/react";
import { labelOf } from "../lib/data.js";
import { tr, useLang } from "../lib/labels.js";
import { tu } from "../lib/ui_strings.js";
import { ChartHelp, PendingBadge, SourceChips } from "../components/ui.jsx";

const STAGE_KEYS = [
  "local_problem",
  "translation_frame",
  "venue_entry",
  "intermediate_output",
  "bounded_gain",
  "underlying_change",
];

function StatusChip({ status, lang }) {
  if (!status) {
    return <span className="status-chip context">{tu("chip.context", lang)}</span>;
  }
  const className = STATUS_CLASSES[status] || "unknown";
  const Icon = status === "mixed" ? CircleHalf : Circle;
  return (
    <span className={`status-chip ${className}`}>
      <Icon size={11} weight={status === "yes" ? "fill" : "regular"} />
      {tu(`chip.${status}`, lang)}
    </span>
  );
}

const STATUS_CLASSES = {
  yes: "yes",
  mixed: "mixed",
  no: "no",
  unknown: "unknown",
};

export function PathwaysPage({ data, onOpenActor, layer, candidates }) {
  const view = data.pathwaysView;
  const stageOrder = view?.stage_order || STAGE_KEYS;
  const research = layer === "research" && candidates;
  const lang = useLang();

  const episodes = useMemo(() => {
    const byId = new Map(data.episodes.map((episode) => [episode.id, episode]));
    const ordered = (view?.episode_ids || data.episodes.map((e) => e.id))
      .map((id) => byId.get(id))
      .filter(Boolean);
    if (research) return [...ordered, ...candidates.episodes];
    return ordered;
  }, [data.episodes, view, research, candidates]);

  const groups = useMemo(() => {
    const base = view?.route_families || [];
    const extra = [...new Set(episodes.map((episode) => episode.route_family))].filter(
      (family) => !base.includes(family),
    );
    return [...base, ...extra]
      .map((family) => ({
        family,
        items: episodes.filter((episode) => episode.route_family === family),
      }))
      .filter((group) => group.items.length);
  }, [episodes, view]);

  const [selectedId, setSelectedId] = useState(() => {
    const pending = sessionStorage.getItem("nr3.episode");
    if (pending && episodes.some((episode) => episode.id === pending)) {
      sessionStorage.removeItem("nr3.episode");
      return pending;
    }
    return episodes[0]?.id || null;
  });
  const [compareIds, setCompareIds] = useState([]);
  const episode = episodes.find((item) => item.id === selectedId) || episodes[0];

  const actorById = useMemo(
    () => new Map(data.actors.map((actor) => [actor.id, actor])),
    [data.actors],
  );
  const outcomesByEpisode = useMemo(() => {
    const map = new Map();
    const allOutcomes = research
      ? [...data.outcomes, ...candidates.outcomes]
      : data.outcomes;
    allOutcomes.forEach((outcome) => {
      const entry = map.get(outcome.episode_id) || new Map();
      entry.set(outcome.tier, outcome);
      map.set(outcome.episode_id, entry);
    });
    return map;
  }, [data.outcomes, candidates, research]);

  if (!episode) return null;
  const isPending = episode.display_status === "research";

  const stageContentFor = (ep) => ({
    local_problem: { text: ep.local_problem, status: null },
    translation_frame: {
      text: ep.translation_frame,
      status: ep.stage_status?.public_claim,
    },
    venue_entry: {
      text: ep.venue_label,
      status: ep.stage_status?.venue_entry,
    },
    intermediate_output: {
      text:
        outcomesByEpisode.get(ep.id)?.get("intermediate_output")?.display_label ||
        ep.observable_output,
      status: ep.stage_status?.intermediate_output,
    },
    bounded_gain: {
      text:
        outcomesByEpisode.get(ep.id)?.get("bounded_gain")?.display_label ||
        ep.substantive_result,
      status: ep.stage_status?.bounded_gain,
    },
    underlying_change: {
      text:
        outcomesByEpisode.get(ep.id)?.get("underlying_change")?.display_label ||
        ep.substantive_result,
      status: ep.stage_status?.underlying_change,
    },
  });

  const stageContent = stageContentFor(episode);
  const compareEpisodes = compareIds
    .map((id) => episodes.find((item) => item.id === id))
    .filter(Boolean);
  const toggleCompare = (id) =>
    setCompareIds((current) =>
      current.includes(id)
        ? current.filter((item) => item !== id)
        : current.length < 2
          ? [...current, id]
          : current,
    );

  return (
    <main className="workspace pathways-workspace">
      <div className="workspace-top">
        <div className="page-intro">
          <h1>
            {tu("pathways.title", lang)}
            <ChartHelp title={tu("pathways.title", lang)}>
              <p>{tu("help.pathways.p1", lang)}</p>
              <p>{tu("help.pathways.p2", lang)}</p>
            </ChartHelp>
          </h1>
        </div>
        <div className="path-summary">
          <GitBranch size={18} />
          {research
            ? tu("path.summaryResearch", lang)
                .replace("{d}", episodes.filter((e) => e.display_status !== "research").length)
                .replace("{p}", episodes.filter((e) => e.display_status === "research").length)
                .replace("{m}", groups.length)
            : tu("path.summary", lang)
                .replace("{n}", episodes.length)
                .replace("{m}", groups.length)}
        </div>
      </div>
      <div className="pathways-grid">
        <aside className="episode-rail">
          {groups.map((group) => (
            <section key={group.family}>
              <header>
                <span>{tr(group.family, lang)}</span>
                <small>{group.items.length}</small>
              </header>
              {group.items.map((item) => (
                <button
                  key={item.id}
                  className={`${item.id === episode.id ? "active" : ""} ${
                    item.display_status === "research" ? "pending" : ""
                  }`}
                  onClick={() => setSelectedId(item.id)}
                  type="button"
                >
                  <strong>
                    {item.display_label}
                    {item.display_status === "research" && (
                      <PendingBadge>{tu("common.pending", lang)}</PendingBadge>
                    )}
                  </strong>
                  <small>{tr(item.review_status, lang)}</small>
                </button>
              ))}
            </section>
          ))}
        </aside>
        <section className="stage-flow">
          {compareIds.length > 0 && (
            <div className="episode-compare-bar">
              <ArrowsLeftRight size={16} />
              <strong>{tu("compare.title", lang)}</strong>
              <span>
                {compareEpisodes.map((item) => item.display_label).join(" ↔ ")}
              </span>
              {compareIds.length < 2 && (
                <span className="hint">{tu("compare.hint", lang)}</span>
              )}
              <button onClick={() => setCompareIds([])} type="button">
                {tu("compare.clear", lang)}
              </button>
            </div>
          )}
          {compareEpisodes.length === 2 ? (
            <div className="stage-compare">
              <span className="sc-head" />
              <span className="sc-head">{compareEpisodes[0].display_label}</span>
              <span className="sc-head">{compareEpisodes[1].display_label}</span>
              {stageOrder.map((stageKey) => {
                const contentA = stageContentFor(compareEpisodes[0])[stageKey];
                const contentB = stageContentFor(compareEpisodes[1])[stageKey];
                return (
                  <Fragment key={stageKey}>
                    <span className="sc-head">{tu(`stage.${stageKey}`, lang)}</span>
                    <div className="sc-cell">
                      <StatusChip status={contentA?.status} lang={lang} />
                      <p>{contentA?.text || "—"}</p>
                    </div>
                    <div className="sc-cell">
                      <StatusChip status={contentB?.status} lang={lang} />
                      <p>{contentB?.text || "—"}</p>
                    </div>
                  </Fragment>
                );
              })}
            </div>
          ) : (
            <div className="stage-ladder">
              {stageOrder.map((stageKey, index) => {
                const content = stageContent[stageKey] || { text: "", status: null };
                return (
                  <div className="stage-row" key={stageKey}>
                    <div className="stage-rail">
                      <i className={`dot ${content.status || "context"}`} />
                      {index < stageOrder.length - 1 && <span className="line" />}
                    </div>
                    <div className="stage-head">
                      <strong>{tu(`stage.${stageKey}`, lang)}</strong>
                      <StatusChip status={content.status} lang={lang} />
                    </div>
                    <p>{content.text || "—"}</p>
                  </div>
                );
              })}
            </div>
          )}
        </section>
        <aside className="detail-panel path-panel">
          <div className="detail-eyebrow">
            <GitBranch size={13} />
            {tr(episode.route_family, lang)} · {episode.module}
            {isPending && <PendingBadge>{tu("common.pending", lang)}</PendingBadge>}
          </div>
          <div className="detail-heading">
            <div>
              <h2>{episode.display_label}</h2>
              <p>
                {episode.id} · {tr(episode.review_status, lang)} · {episode.evidence_level}
              </p>
            </div>
          </div>
          {!!episode.place_labels?.length && (
            <section className="detail-section compact">
              <header>
                <span>{tu("path.places", lang)}</span>
                <small>{episode.place_labels.length}</small>
              </header>
              <div className="place-tags">
                {episode.place_labels.map((label) => (
                  <span key={label}>
                    <MapPin size={13} />
                    {label}
                  </span>
                ))}
              </div>
            </section>
          )}
          <section className="detail-section">
            <header>
              <span>{tu("path.actors", lang)}</span>
              <small>
                {tu("path.actorsSub", lang).replace("{n}", episode.actor_ids.length)}
              </small>
            </header>
            <div className="participant-chips">
              {episode.actor_ids.map((actorId) => {
                const actor = actorById.get(actorId);
                return (
                  <button
                    key={actorId}
                    type="button"
                    disabled={!actor}
                    title={actor ? labelOf(actor) : actorId}
                    onClick={() => actor && onOpenActor(actorId)}
                  >
                    {actor ? labelOf(actor) : actorId}
                    {actor && <CaretRight size={13} />}
                  </button>
                );
              })}
            </div>
          </section>
          <section className="detail-section compact">
            <header>
              <span>{tu("path.sources", lang)}</span>
              <small>
                {tu("path.countUnit", lang).replace("{n}", episode.source_ids.length)}
              </small>
            </header>
            <SourceChips ids={episode.source_ids} />
            {!!episode.unresolved_source_refs?.length && (
              <div className="source-chips">
                <em>
                  {tu("sources.unresolved", lang).replace(
                    "{n}",
                    episode.unresolved_source_refs.length,
                  )}
                </em>
              </div>
            )}
          </section>
          {!!episode.case_ids?.length && (
            <section className="detail-section compact">
              <header>
                <span>{tu("path.cases", lang)}</span>
                <small>{episode.case_ids.length}</small>
              </header>
              <div className="source-chips">
                {episode.case_ids.map((id) => (
                  <span key={id}>{id}</span>
                ))}
              </div>
            </section>
          )}
          {episode.interpretation_limit && (
            <div className="interpretation-note">
              <GitBranch size={18} />
              <p>{episode.interpretation_limit}</p>
            </div>
          )}
          <button
            className="compare-button"
            type="button"
            onClick={() => toggleCompare(episode.id)}
          >
            <ArrowsLeftRight size={19} />
            {compareIds.includes(episode.id)
              ? tu("compare.clear", lang)
              : tu("compare.add", lang)}
          </button>
        </aside>
      </div>
    </main>
  );
}
