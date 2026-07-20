import { createContext, useContext, useEffect, useState } from "react";

export { labelOf, localizedFieldOf } from "./display_text.js";

const publicUrl = (path) =>
  `${import.meta.env.BASE_URL}${String(path).replace(/^\/+/, "")}`;

const requiredJson = (path) =>
  fetch(publicUrl(path)).then((response) => {
    if (!response.ok) {
      throw new Error(`Required release file unavailable: ${path} (${response.status})`);
    }
    return response.json();
  });

const publicationObjects = () =>
  requiredJson("views/exhibits.json").then((index) => {
    const entries = Array.isArray(index?.entries) ? index.entries : [];
    const exhibitEntries = entries.filter(
      (entry) => entry.payload_kind === "exhibit",
    );
    return Promise.all(
      exhibitEntries.map((entry) =>
        requiredJson(entry.path).then((payload) => [entry.catalog_id, payload]),
      ),
    ).then((rows) => ({
      index,
      exhibits: Object.fromEntries(rows),
    }));
  });

const reviewedRelations = () =>
  Promise.all([
    requiredJson("core/relations/actor_issue.json"),
    requiredJson("core/relations/actor_place.json"),
    requiredJson("core/events/participation.json"),
    requiredJson("core/legal/roles.json"),
    requiredJson("core/relations/strict_place_issue.json"),
    requiredJson("core/episodes/actor_links.json"),
  ]).then(
    ([
      actorIssue,
      actorPlace,
      eventParticipation,
      legalRoles,
      strictPlaceIssue,
      actorEpisode,
    ]) => ({
      actor_issue: actorIssue,
      actor_place: actorPlace,
      event_participation: eventParticipation,
      legal_roles: legalRoles,
      strict_place_issue: strictPlaceIssue,
      actor_episode: actorEpisode,
    }),
  );

const researchCandidateObjects = () =>
  Promise.all([
    requiredJson("research/actor_issue.json"),
    requiredJson("research/actor_place.json"),
    requiredJson("research/event_participation.json"),
    requiredJson("research/strict_place_issue.json"),
    requiredJson("research/actor_episode.json"),
    requiredJson("research/episodes.json"),
    requiredJson("research/outcomes.json"),
    requiredJson("research/dyadic_relations.json"),
    requiredJson("research/administrative_records.json"),
    requiredJson("research/aggregate_observations.json"),
    requiredJson("research/typed_event_participation.json"),
    requiredJson("research/relation_leads.json"),
    requiredJson("research/genealogy_anchors.json"),
  ]).then(
    ([
      actorIssue,
      actorPlace,
      eventParticipation,
      strictPlaceIssue,
      actorEpisode,
      episodes,
      outcomes,
      dyadicRelations,
      administrativeRecords,
      aggregateObservations,
      typedEventParticipation,
      relationLeads,
      genealogyAnchors,
    ]) => ({
      relations: {
        actor_issue: actorIssue,
        actor_place: actorPlace,
        event_participation: eventParticipation,
        strict_place_issue: strictPlaceIssue,
        actor_episode: actorEpisode,
      },
      episodes,
      outcomes,
      dyadic_relations: dyadicRelations,
      administrative_records: administrativeRecords,
      aggregate_observations: aggregateObservations,
      event_participation: typedEventParticipation,
      relation_leads: relationLeads,
      genealogy_anchors: genealogyAnchors,
    }),
  );

export const actorClassGroup = (actorClass, presentation) =>
  presentation?.actor_class_to_group?.[actorClass] || "unknown";

export const actorClassMeta = (actorClass, presentation) => {
  const groupId = actorClassGroup(actorClass, presentation);
  return (
    presentation?.actor_class_groups?.find((group) => group.id === groupId) ||
    presentation?.actor_class_groups?.find((group) => group.id === "unknown") || {
      id: "unknown",
      color: "#9aa6a8",
    }
  );
};

export const regionMeta = (region, presentation) =>
  presentation?.regions?.find((item) => item.id === region) || {
    id: region,
    color: "#9baeb3",
  };

export const placeDisplayRegion = (place, presentation) =>
  presentation?.place_display_regions?.[place.id] ||
  presentation?.default_place_display_region ||
  "okinawa";

export function useResearchCandidates(enabled) {
  const [state, setState] = useState({ status: "idle", candidates: null });

  useEffect(() => {
    if (!enabled) return undefined;
    let mounted = true;
    setState((current) =>
      current.status === "idle" ? { status: "loading", candidates: null } : current,
    );
    researchCandidateObjects()
      .then((candidates) => {
        if (mounted) setState({ status: "ready", candidates });
      })
      .catch(() => {
        if (mounted) setState({ status: "error", candidates: null });
      });
    return () => {
      mounted = false;
    };
  }, [enabled]);

  return state;
}

export function useEvidenceData(enabled) {
  const [state, setState] = useState({ status: "idle", evidence: null });

  useEffect(() => {
    if (!enabled) return undefined;
    let mounted = true;
    setState((current) =>
      current.status === "idle" ? { status: "loading", evidence: null } : current,
    );
    requiredJson("core/evidence/sources.json")
      .then((evidence) => {
        if (mounted) setState({ status: "ready", evidence });
      })
      .catch(() => {
        if (mounted) setState({ status: "error", evidence: null });
      });
    return () => {
      mounted = false;
    };
  }, [enabled]);

  return state;
}

export const EvidenceContext = createContext({ openEvidence: () => {} });
export const useEvidence = () => useContext(EvidenceContext);

// Watches the NR-02 package build id and reports when the backend data has
// been rebuilt since this client loaded it.
export function useBuildWatch(currentBuildId) {
  const [newerBuild, setNewerBuild] = useState(null);

  useEffect(() => {
    if (!currentBuildId) return undefined;
    let cancelled = false;
    const check = () =>
      fetch(publicUrl("manifest.json"), { cache: "no-store" })
        .then((r) => {
          if (!r.ok) throw new Error(`Release manifest unavailable (${r.status})`);
          return r.json();
        })
        .then((manifest) => {
          if (!cancelled && manifest.build_id && manifest.build_id !== currentBuildId) {
            setNewerBuild(manifest.build_id);
          }
        })
        .catch(() => {});
    const interval = setInterval(check, 20000);
    const onFocus = () => check();
    window.addEventListener("focus", onFocus);
    return () => {
      cancelled = true;
      clearInterval(interval);
      window.removeEventListener("focus", onFocus);
    };
  }, [currentBuildId]);

  return newerBuild;
}

export function useResearchData() {
  const [state, setState] = useState({ status: "loading" });

  useEffect(() => {
    let mounted = true;
    Promise.all([
      requiredJson("core/entities/actors.json"),
      requiredJson("core/entities/places.json"),
      requiredJson("core/entities/issues.json"),
      reviewedRelations(),
      requiredJson("core/map/geometry.geojson"),
      requiredJson("core/episodes/episodes.json"),
      requiredJson("core/episodes/outcomes.json"),
      requiredJson("core/episodes/pathways.json"),
      requiredJson("core/coverage/audit.json"),
      requiredJson("core/presentation/rules.json"),
      requiredJson("views/core_surfaces.json"),
      publicationObjects(),
      requiredJson("manifest.json"),
      requiredJson("core/typed_relations/dyadic.json"),
      requiredJson("core/typed_relations/administrative.json"),
      requiredJson("core/typed_relations/aggregate.json"),
      requiredJson("core/typed_relations/event_participation.json"),
      requiredJson("core/typed_relations/case_roles.json"),
      requiredJson("core/lifecycle/anchors.json"),
    ])
      .then(
        ([
          actors,
          places,
          issues,
          relations,
          geometry,
          episodes,
          outcomes,
          pathwaysView,
          coverageView,
          presentation,
          coreSurfaces,
          publication,
          manifest,
          dyadicRelations,
          administrativeRecords,
          aggregateObservations,
          typedEventParticipation,
          caseRoles,
          genealogyAnchors,
        ]) => {
          if (mounted) {
            setState({
              status: "ready",
              actors: actors.filter((actor) => actor.display_status !== "hidden"),
              places,
              issues,
              relations,
              geometry,
              episodes,
              outcomes,
              pathwaysView,
              coverageView,
              presentation,
              coreSurfaces,
              publicationObjectIndex: publication.index,
              exhibits: publication.exhibits,
              manifest,
              dyadicRelations,
              administrativeRecords,
              aggregateObservations,
              typedEventParticipation,
              caseRoles,
              genealogyAnchors,
            });
          }
        },
      )
      .catch((error) => {
        if (mounted) setState({ status: "error", error });
      });
    return () => {
      mounted = false;
    };
  }, []);

  return state;
}
