import { useMemo, useState } from "react";
import { MagnifyingGlass, Network, ShareNetwork } from "@phosphor-icons/react";
import { actorClassGroup, labelOf } from "../lib/data.js";
import { tr, useLang } from "../lib/labels.js";
import { tu } from "../lib/ui_strings.js";
import { ChartHelp, SegmentedControl } from "../components/ui.jsx";
import { ActorCanvas } from "../components/ActorCanvas.jsx";
import { RelationCanvas } from "../components/RelationCanvas.jsx";
import { ActorPanel } from "../components/ActorPanel.jsx";

const GROUP_ORDER = [
  "civic",
  "international",
  "legal",
  "labor",
  "service",
  "public",
  "resource",
  "unknown",
];

const GROUP_COLORS = {
  civic: "#2b7f80",
  international: "#bd547c",
  legal: "#55756b",
  labor: "#8a6c98",
  service: "#6b7fa3",
  public: "#8d6c57",
  resource: "#dc9a35",
  unknown: "#9aa6a8",
};

export function ActorsPage({ data, layer, candidates }) {
  const lang = useLang();
  const firstReviewedActor =
    data.actors.find((actor) =>
      data.relations.actor_issue.some((edge) => edge.actor_id === actor.id),
    )?.id || null;
  const [selectedActor, setSelectedActor] = useState(() => {
    const pending = sessionStorage.getItem("nr3.actor");
    if (pending && data.actors.some((actor) => actor.id === pending)) {
      sessionStorage.removeItem("nr3.actor");
      return pending;
    }
    return firstReviewedActor;
  });
  const [classFilter, setClassFilter] = useState("all");
  const [issueFilter, setIssueFilter] = useState(() => {
    const pending = sessionStorage.getItem("nr3.issueFilter");
    if (pending && data.issues.some((issue) => issue.id === pending)) {
      sessionStorage.removeItem("nr3.issueFilter");
      return pending;
    }
    return "all";
  });
  const [search, setSearch] = useState("");
  const [graphMode, setGraphMode] = useState("ecology");
  const selected = data.actors.find((actor) => actor.id === selectedActor);
  const activeActors = useMemo(
    () => data.actors.filter((actor) => actor.scope_status !== "merged_duplicate"),
    [data.actors],
  );
  const searchResults = useMemo(() => {
    const term = search.trim().toLowerCase();
    if (!term) return [];
    return activeActors
      .filter((actor) =>
        [
          actor.id,
          actor.display_label,
          ...(actor.aliases || []).map((alias) => alias.label || alias),
        ]
          .join(" ")
          .toLowerCase()
          .includes(term),
      )
      .slice(0, 8);
  }, [activeActors, search]);
  const scopedActorIds = useMemo(() => {
    const ids = new Set(data.relations.actor_issue.map((edge) => edge.actor_id));
    if (layer === "research" && candidates) {
      candidates.relations.actor_issue.forEach((edge) => ids.add(edge.actor_id));
    }
    return ids;
  }, [data.relations.actor_issue, candidates, layer]);
  const classCounts = activeActors.reduce((counts, actor) => {
    if (!scopedActorIds.has(actor.id)) return counts;
    const group = actorClassGroup(actor.actor_class);
    counts[group] = (counts[group] || 0) + 1;
    return counts;
  }, {});
  const classes = GROUP_ORDER.filter((group) => classCounts[group]);
  const edgelessNote =
    layer === "research" && activeActors.length > scopedActorIds.size
      ? tu("actors.edgeless", lang).replace(
          "{n}",
          activeActors.length - scopedActorIds.size,
        )
      : "";

  return (
    <main className="workspace actors-workspace">
      <div className="workspace-top">
        <div className="page-intro">
          <h1>
            {graphMode === "ecology"
              ? tu("actors.title", lang)
              : tu("actors.title.relation", lang)}
            <ChartHelp
              title={
                graphMode === "ecology"
                  ? tu("actors.title", lang)
                  : tu("actors.title.relation", lang)
              }
            >
              {graphMode === "ecology" ? (
                <>
                  <p>{tu("help.actors.p1", lang)}</p>
                  <p>{tu("help.actors.p2", lang)}</p>
                </>
              ) : (
                <>
                  <p>{tu("help.relation.p1", lang)}</p>
                  <p>{tu("help.relation.p2", lang)}</p>
                </>
              )}
            </ChartHelp>
          </h1>
        </div>
        <SegmentedControl
          label={tu("actors.mode.ecology", lang)}
          value={graphMode}
          onChange={setGraphMode}
          items={[
            { id: "ecology", label: tu("actors.mode.ecology", lang), icon: Network },
            { id: "relation", label: tu("actors.mode.relation", lang), icon: ShareNetwork },
          ]}
        />
        <div className="toolbar-row">
          <div className="search-box">
            <MagnifyingGlass size={18} />
            <input
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              placeholder={tu("actors.search", lang)}
              aria-label={tu("actors.search", lang)}
            />
            {search.trim() && (
              <div className="search-results">
                {searchResults.map((actor) => (
                  <button
                    key={actor.id}
                    type="button"
                    onClick={() => {
                      setSelectedActor(actor.id);
                      setSearch("");
                    }}
                  >
                    <strong>
                      {labelOf(actor)}
                      {actor.scope_status === "watchlist_only" && (
                        <em className="scope-badge">{tr("watchlist_only", lang)}</em>
                      )}
                    </strong>
                    <small>
                      {actor.id} · {tu(`classGroup.${actorClassGroup(actor.actor_class)}`, lang)}
                    </small>
                  </button>
                ))}
                {!searchResults.length && (
                  <span className="no-match">{tu("actors.noMatch", lang)}</span>
                )}
              </div>
            )}
          </div>
          <div className="filter-row">
            <label>
              {tu("actors.classLabel", lang)}
              <select
                value={classFilter}
                onChange={(event) => setClassFilter(event.target.value)}
              >
                <option value="all">
                  {tu("actors.graphCount", lang)
                    .replace("{n}", scopedActorIds.size)
                    .replace("{t}", activeActors.length)}
                </option>
                {classes.map((value) => (
                  <option value={value} key={value}>
                    {tu(`classGroup.${value}`, lang)}（{classCounts[value]}）
                  </option>
                ))}
              </select>
            </label>
            {graphMode === "ecology" && (
              <label>
                {tu("actors.issueLabel", lang)}
                <select
                  value={issueFilter}
                  onChange={(event) => setIssueFilter(event.target.value)}
                >
                  <option value="all">{tu("actors.allIssues", lang)}</option>
                  {data.issues.map((issue) => (
                    <option value={issue.id} key={issue.id}>
                      {tr(issue.display_label, lang)}
                    </option>
                  ))}
                </select>
              </label>
            )}
          </div>
        </div>
      </div>
      <div className="overview-grid">
        <section className="visual-stage actor-stage">
          {graphMode === "ecology" && (
            <div className="actor-legend">
              {classes
                .filter((id) => id !== "unknown")
                .map((id) => (
                  <span key={id}>
                    <i style={{ background: GROUP_COLORS[id] }} />
                    {tu(`classGroup.${id}`, lang)}
                  </span>
                ))}
              {layer === "research" && (
                <span className="legend-pending">
                  <i />
                  {tu("actors.legendPending", lang)}
                </span>
              )}
            </div>
          )}
          {graphMode === "ecology" ? (
            <ActorCanvas
              actors={activeActors}
              issues={data.issues}
              relations={data.relations}
              selectedActor={selectedActor}
              setSelectedActor={setSelectedActor}
              classFilter={classFilter}
              issueFilter={issueFilter}
              onPickIssue={(id) => setIssueFilter(id)}
              search={search}
              layer={layer}
              candidates={candidates}
              scopeNote={edgelessNote}
            />
          ) : (
            <RelationCanvas
              actors={activeActors}
              dyadicRelations={data.dyadicRelations}
              layer={layer}
              candidates={candidates}
              selectedActor={selectedActor}
              setSelectedActor={setSelectedActor}
              search={search}
              classFilter={classFilter}
            />
          )}
        </section>
        <ActorPanel
          actor={selected}
          actors={data.actors}
          issues={data.issues}
          relations={data.relations}
          issueFilter={issueFilter}
          onPickIssue={(id) => setIssueFilter(id)}
          onPickYear={(year) => {
            if (year) {
              sessionStorage.setItem("nr3.year", year);
              window.location.hash = "#/time";
            }
          }}
          onSelectActor={(id) => setSelectedActor(id)}
          layer={layer}
          candidates={candidates}
          dyadicRelations={data.dyadicRelations}
          administrativeRecords={data.administrativeRecords}
          aggregateObservations={data.aggregateObservations}
          typedEventParticipation={data.typedEventParticipation}
          caseRoles={data.caseRoles}
        />
      </div>
    </main>
  );
}
