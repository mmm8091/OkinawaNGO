import { createContext, useContext, useEffect, useState } from "react";

export { labelOf, localizedFieldOf } from "./display_text.js";

export const REGION_META = {
  all: { label: "全部区域", short: "全域", color: "#2b7f80" },
  okinawa: { label: "冲绳本岛", short: "本岛", color: "#2b7f80" },
  miyako: { label: "宫古群岛", short: "宫古", color: "#dc9a35" },
  yaeyama: { label: "八重山群岛", short: "八重山", color: "#bd547c" },
  other: { label: "周边岛屿", short: "周边", color: "#9baeb3" },
  sakishima: { label: "先岛群岛（宫古 · 八重山）", short: "先岛", color: "#c9854e" },
};

export const CLASS_GROUPS = {
  civic: { label: "公民与地方组织", color: "#2b7f80" },
  international: { label: "国际与倡议组织", color: "#bd547c" },
  legal: { label: "法律与专业组织", color: "#55756b" },
  labor: { label: "劳动与教育组织", color: "#8a6c98" },
  service: { label: "服务与福利组织", color: "#6b7fa3" },
  public: { label: "公共与交流机构", color: "#8d6c57" },
  resource: { label: "企业与资源支持", color: "#dc9a35" },
  unknown: { label: "尚未归组", color: "#9aa6a8" },
};

export const CLASS_TO_GROUP = {
  local_civic_actor: "civic",
  domestic_japan_ngo: "civic",
  citizen_network: "civic",
  citizen_group: "civic",
  executive_committee: "civic",
  local_npo: "civic",
  womens_or_human_rights_ngo: "civic",
  womens_or_community_organization: "civic",
  womens_organization: "civic",
  international_advocacy_actor: "international",
  international_ngo: "international",
  local_international_cooperation_ngo: "international",
  media_or_advocacy_actor: "international",
  lawyers_network: "legal",
  labor_or_education_union: "labor",
  labor_union_federation: "labor",
  labor_union: "labor",
  base_community_service_actor: "service",
  base_spouse_charity_network: "service",
  base_spouse_club: "service",
  public_institution_partner: "public",
  public_diplomacy_or_exchange_actor: "public",
  public_diplomacy_grant_program: "public",
  local_business_sponsor: "resource",
  corporate_sponsor: "resource",
  funder_or_intermediary: "resource",
};

export const actorClassGroup = (actorClass) =>
  CLASS_TO_GROUP[actorClass] || "unknown";
export const actorClassMeta = (actorClass) =>
  CLASS_GROUPS[actorClassGroup(actorClass)];

// Presentation-only mapping from registry place to the four display regions.
// The central place registry keeps Miyako under "Sakishima"; the presentation
// layer separates Miyako from Yaeyama. Central data unchanged.
export const PLACE_DISPLAY_REGION = {
  P011: "yaeyama",
  P012: "yaeyama",
  P013: "miyako",
  P021: "sakishima",
};
export const placeDisplayRegion = (place) =>
  PLACE_DISPLAY_REGION[place.id] || "okinawa";

export function useResearchCandidates(enabled) {
  const [state, setState] = useState({ status: "idle", candidates: null });

  useEffect(() => {
    if (!enabled) return undefined;
    let mounted = true;
    setState((current) =>
      current.status === "idle" ? { status: "loading", candidates: null } : current,
    );
    fetch("/research/candidates.json")
      .then((r) => r.json())
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
    fetch("/demo/evidence.json")
      .then((r) => r.json())
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
      fetch("/manifest.json", { cache: "no-store" })
        .then((r) => r.json())
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
    const tolerantJson = (url, fallback) =>
      fetch(url)
        .then((r) => (r.ok ? r.json() : fallback))
        .then((data) => (Array.isArray(data) ? data : fallback))
        .catch(() => fallback);
    Promise.all([
      fetch("/demo/actors.json").then((r) => r.json()),
      fetch("/demo/places.json").then((r) => r.json()),
      fetch("/demo/issues.json").then((r) => r.json()),
      fetch("/demo/relations.json").then((r) => r.json()),
      fetch("/demo/historical_anchors.json").then((r) => r.json()),
      fetch("/demo/map_geometry.geojson").then((r) => r.json()),
      fetch("/demo/episodes.json").then((r) => r.json()),
      fetch("/demo/outcomes.json").then((r) => r.json()),
      fetch("/views/pathways.json").then((r) => r.json()),
      fetch("/views/evidence_coverage.json").then((r) => r.json()),
      fetch("/manifest.json").then((r) => r.json()),
      tolerantJson("/demo/dyadic_relations.json", []),
      tolerantJson("/demo/administrative_records.json", []),
      tolerantJson("/demo/aggregate_observations.json", []),
      tolerantJson("/demo/typed_event_participation.json", []),
      tolerantJson("/demo/case_roles.json", []),
      tolerantJson("/demo/genealogy_anchors.json", []),
    ])
      .then(
        ([
          actors,
          places,
          issues,
          relations,
          historicalAnchors,
          geometry,
          episodes,
          outcomes,
          pathwaysView,
          coverageView,
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
              historicalAnchors,
              geometry,
              episodes,
              outcomes,
              pathwaysView,
              coverageView,
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
