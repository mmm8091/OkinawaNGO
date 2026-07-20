import { useMemo, useState } from "react";
import {
  ArrowsLeftRight,
  CaretRight,
  GitBranch,
  MapPin,
  WarningCircle,
  X,
} from "@phosphor-icons/react";
import { labelOf, placeDisplayRegion, regionMeta } from "../lib/data.js";
import { tr, useLang } from "../lib/labels.js";
import { tu } from "../lib/ui_strings.js";
import { PendingBadge } from "./ui.jsx";

function useRegionStats({
  region,
  places,
  issues,
  strictRelations,
  actorPlaces,
  candidates,
  research,
  presentation,
}) {
  return useMemo(() => {
    const regionPlaces = (() => {
      if (region === "all") return places;
      if (region === "sakishima") {
        return places.filter((place) =>
          ["miyako", "yaeyama"].includes(
            placeDisplayRegion(place, presentation),
          ),
        );
      }
      return places.filter(
        (place) => placeDisplayRegion(place, presentation) === region,
      );
    })();
    const placeIds = new Set(regionPlaces.map((place) => place.id));
    const placeLabels = new Set(regionPlaces.map((place) => place.display_label));
    const triples = strictRelations.filter((rel) => placeIds.has(rel.place_id));
    const candTriples = research
      ? candidates.relations.strict_place_issue.filter((rel) => placeIds.has(rel.place_id))
      : [];
    const actorIds = new Set(
      actorPlaces.filter((rel) => placeIds.has(rel.place_id)).map((rel) => rel.actor_id),
    );
    const candActorIds = research
      ? new Set(
          candidates.relations.actor_place
            .filter((rel) => placeIds.has(rel.place_id))
            .map((rel) => rel.actor_id),
        )
      : new Set();
    const issueCounts = new Map();
    triples.forEach((rel) =>
      issueCounts.set(rel.issue_id, (issueCounts.get(rel.issue_id) || 0) + 1),
    );
    const candIssueCounts = new Map();
    candTriples.forEach((rel) =>
      candIssueCounts.set(rel.issue_id, (candIssueCounts.get(rel.issue_id) || 0) + 1),
    );
    const topIssues = [...issueCounts.entries()]
      .sort((a, b) => b[1] - a[1])
      .slice(0, 5)
      .map(([id, count]) => {
        const issue = issues.find((item) => item.id === id);
        return issue ? { ...issue, count, pending: candIssueCounts.get(id) || 0 } : null;
      })
      .filter(Boolean);
    const topPendingIssues =
      research && !topIssues.length
        ? [...candIssueCounts.entries()]
            .sort((a, b) => b[1] - a[1])
            .slice(0, 5)
            .map(([id, count]) => {
              const issue = issues.find((item) => item.id === id);
              return issue ? { ...issue, count: 0, pending: count } : null;
            })
            .filter(Boolean)
        : [];
    return {
      regionPlaces,
      placeLabels,
      triples,
      candTriples,
      actorIds,
      candActorIds,
      topIssues,
      topPendingIssues,
    };
  }, [
    actorPlaces,
    candidates,
    issues,
    places,
    presentation,
    region,
    research,
    strictRelations,
  ]);
}

function RegionEpisodes({ stats, episodes, candidates, research, onPickEpisode, lang }) {
  const demoEpisodes = episodes.filter((episode) =>
    episode.place_labels?.some((label) => stats.placeLabels.has(label)),
  );
  const pendingEpisodes = research
    ? candidates.episodes.filter((episode) =>
        episode.place_labels?.some((label) => stats.placeLabels.has(label)),
      )
    : [];
  if (!demoEpisodes.length && !pendingEpisodes.length) return null;
  return (
    <section className="detail-section">
      <header>
        <span>{tu("overview.episodes", lang)}</span>
        <small>{tu("overview.episodesSub", lang)}</small>
      </header>
      <div className="issue-list">
        {demoEpisodes.map((episode) => (
          <button
            key={episode.id}
            type="button"
            title={tu("overview.pickEpisode", lang)}
            onClick={() => onPickEpisode(episode.id)}
          >
            <span>
              <strong>{labelOf(episode, lang)}</strong>
            </span>
            <GitBranch size={14} />
            <CaretRight size={15} />
          </button>
        ))}
        {pendingEpisodes.map((episode) => (
          <button
            key={episode.id}
            type="button"
            className="pending"
            title={tu("overview.pickEpisode", lang)}
            onClick={() => onPickEpisode(episode.id)}
          >
            <span>
              <strong>{labelOf(episode, lang)}</strong>
            </span>
            <PendingBadge>{tu("common.pending", lang)}</PendingBadge>
            <CaretRight size={15} />
          </button>
        ))}
      </div>
    </section>
  );
}

function RegionColumn({
  region,
  stats,
  lang,
  onPickIssue,
  compact,
  presentation,
}) {
  return (
    <div className="compare-col">
      <h3>
        <span
          className="region-swatch"
          style={{
            background:
              region === "sakishima"
                ? "linear-gradient(90deg,#dc9a35,#bd547c)"
                : regionMeta(region, presentation).color,
          }}
        />
        {tu(`region.${region}`, lang)}
      </h3>
      <div className="compare-metrics">
        <div>
          <strong>{stats.regionPlaces.length}</strong>
          <span>{tu("metric.places", lang)}</span>
        </div>
        <div>
          <strong>
            {stats.actorIds.size}
            {stats.candActorIds.size > 0 && <em>+{stats.candActorIds.size}</em>}
          </strong>
          <span>{tu("metric.actors", lang)}</span>
        </div>
        <div>
          <strong>
            {stats.triples.length}
            {stats.candTriples.length > 0 && <em>+{stats.candTriples.length}</em>}
          </strong>
          <span>{tu("metric.triples", lang)}</span>
        </div>
      </div>
      <div className="issue-list">
        {stats.topIssues.slice(0, compact ? 3 : 5).map((issue) => (
          <button
            key={issue.id}
            type="button"
            title={tu("overview.pickIssue", lang)}
            onClick={() => onPickIssue(issue.id)}
          >
            <span>
              <strong>{tr(issue.display_label, lang)}</strong>
            </span>
            <em>
              {issue.count}
              {issue.pending > 0 && ` +${issue.pending}`}
            </em>
            <CaretRight size={15} />
          </button>
        ))}
        {!stats.topIssues.length &&
          stats.topPendingIssues.slice(0, compact ? 3 : 5).map((issue) => (
            <button
              key={issue.id}
              type="button"
              title={tu("overview.pickIssue", lang)}
              onClick={() => onPickIssue(issue.id)}
            >
              <span>
                <strong>{tr(issue.display_label, lang)}</strong>
              </span>
              <em>
                <PendingBadge>{`${tu("common.pending", lang)} ${issue.pending}`}</PendingBadge>
              </em>
              <CaretRight size={15} />
            </button>
          ))}
        {!stats.topIssues.length && !stats.topPendingIssues.length && (
          <div className="empty-note">
            <WarningCircle size={18} />
            {tu("empty.triples", lang)}
          </div>
        )}
      </div>
    </div>
  );
}

const COMPARE_REGIONS = ["all", "okinawa", "miyako", "yaeyama", "sakishima"];

export function RegionPanel({
  region,
  places,
  issues,
  strictRelations,
  actorPlaces,
  episodes,
  onPickIssue,
  onPickEpisode,
  layer,
  candidates,
  presentation,
}) {
  const research = layer === "research" && candidates;
  const lang = useLang();
  const [compareWith, setCompareWith] = useState(null);

  const shared = {
    places,
    issues,
    strictRelations,
    actorPlaces,
    candidates,
    research,
    presentation,
  };
  const stats = useRegionStats({ region, ...shared });
  const compareStats = useRegionStats({
    region: compareWith || "all",
    ...shared,
  });

  if (compareWith) {
    return (
      <aside className="detail-panel compare-panel">
        <div className="compare-head">
          <span>
            <ArrowsLeftRight size={16} />
            {tu("compare.title", lang)}
          </span>
          <button
            onClick={() => setCompareWith(null)}
            title={tu("compare.clear", lang)}
            type="button"
          >
            <X size={15} />
          </button>
        </div>
        <div className="compare-grid">
          <RegionColumn
            region={region}
            stats={stats}
            lang={lang}
            onPickIssue={onPickIssue}
            compact
            presentation={presentation}
          />
          <RegionColumn
            region={compareWith}
            stats={compareStats}
            lang={lang}
            onPickIssue={onPickIssue}
            compact
            presentation={presentation}
          />
        </div>
      </aside>
    );
  }

  return (
    <aside className="detail-panel">
      <div className="detail-eyebrow">
        <span
          className="region-swatch"
          style={{
            background:
              region === "sakishima"
                ? "linear-gradient(90deg,#dc9a35,#bd547c)"
                : regionMeta(region, presentation).color,
          }}
        />
        {tu("overview.eyebrow", lang)}
        {research && <PendingBadge>{tu("common.pending", lang)}</PendingBadge>}
      </div>
      <div className="detail-heading">
        <div>
          <h2>{tu(`region.${region}`, lang)}</h2>
        </div>
        <button
          className="icon-button"
          title={tu("compare.title", lang)}
          onClick={() =>
            setCompareWith(COMPARE_REGIONS.find((item) => item !== region) || "all")
          }
          type="button"
        >
          <ArrowsLeftRight size={19} />
        </button>
      </div>
      <div className="compare-picker">
        <label>
          {tu("compare.pickRegion", lang)}
          <select
            value=""
            onChange={(event) => {
              if (event.target.value) setCompareWith(event.target.value);
            }}
          >
            <option value="">—</option>
            {COMPARE_REGIONS.filter((item) => item !== region).map((item) => (
              <option key={item} value={item}>
                {tu(`region.${item}`, lang)}
              </option>
            ))}
          </select>
        </label>
      </div>
      <div className="metric-strip">
        <div>
          <strong>{stats.regionPlaces.length}</strong>
          <span>{tu("metric.places", lang)}</span>
        </div>
        <div>
          <strong>
            {stats.actorIds.size}
            {research && stats.candActorIds.size > 0 && <em>+{stats.candActorIds.size}</em>}
          </strong>
          <span>
            {tu("metric.actors", lang)}
            {research && `／${tu("common.pending", lang)}`}
          </span>
        </div>
        <div>
          <strong>
            {stats.triples.length}
            {research && stats.candTriples.length > 0 && <em>+{stats.candTriples.length}</em>}
          </strong>
          <span>
            {tu("metric.triples", lang)}
            {research && `／${tu("common.pending", lang)}`}
          </span>
        </div>
      </div>
      <section className="detail-section">
        <header>
          <span>{tu("overview.issues", lang)}</span>
          <small>{tu("overview.issuesSub", lang)}</small>
        </header>
        <div className="issue-list">
          {stats.topIssues.map((issue) => (
            <button
              key={issue.id}
              type="button"
              title={tu("overview.pickIssue", lang)}
              onClick={() => onPickIssue(issue.id)}
            >
              <span>
                <strong>{tr(issue.display_label, lang)}</strong>
              </span>
              <em>
                {issue.count}
                {research && issue.pending > 0 && ` +${issue.pending}`}
              </em>
              <CaretRight size={15} />
            </button>
          ))}
          {!stats.topIssues.length &&
            stats.topPendingIssues.map((issue) => (
              <button
                key={issue.id}
                type="button"
                title={tu("overview.pickIssue", lang)}
                onClick={() => onPickIssue(issue.id)}
              >
                <span>
                  <strong>{tr(issue.display_label, lang)}</strong>
                </span>
                <em>
                  <PendingBadge>{`${tu("common.pending", lang)} ${issue.pending}`}</PendingBadge>
                </em>
                <CaretRight size={15} />
              </button>
            ))}
          {!stats.topIssues.length && !stats.topPendingIssues.length && (
            <div className="empty-note">
              <WarningCircle size={18} />
              {tu("empty.triples", lang)}
            </div>
          )}
        </div>
      </section>
      <RegionEpisodes
        stats={stats}
        episodes={episodes}
        candidates={candidates}
        research={research}
        onPickEpisode={onPickEpisode}
        lang={lang}
      />
      <section className="detail-section compact">
        <header>
          <span>{tu("metric.places", lang)}</span>
          <small>{stats.regionPlaces.length}</small>
        </header>
        <div className="place-tags">
          {stats.regionPlaces.slice(0, 8).map((place) => (
            <span key={place.id}>
              <MapPin size={13} /> {tr(place.display_label, lang)}
            </span>
          ))}
        </div>
      </section>
    </aside>
  );
}
