import { useEffect, useState } from "react";
import { Compass, WarningCircle } from "@phosphor-icons/react";
import {
  EvidenceContext,
  useEvidenceData,
  useResearchCandidates,
  useResearchData,
} from "./lib/data.js";
import { LangContext, useLang } from "./lib/labels.js";
import { tu } from "./lib/ui_strings.js";
import { TopBar } from "./components/TopBar.jsx";
import { EvidenceDrawer } from "./components/EvidenceDrawer.jsx";
import { OverviewPage } from "./pages/OverviewPage.jsx";
import { ActorsPage } from "./pages/ActorsPage.jsx";
import { TimePage } from "./pages/TimePage.jsx";
import { PathwaysPage } from "./pages/PathwaysPage.jsx";
import { EvidencePage } from "./pages/EvidencePage.jsx";

function useRoute() {
  const routeFromHash = () => {
    if (window.location.hash === "#/actors") return "actors";
    if (window.location.hash === "#/time") return "time";
    if (window.location.hash === "#/pathways") return "pathways";
    if (window.location.hash === "#/evidence") return "evidence";
    return "overview";
  };
  const [route, setRoute] = useState(routeFromHash);

  useEffect(() => {
    const handler = () => setRoute(routeFromHash());
    window.addEventListener("hashchange", handler);
    return () => window.removeEventListener("hashchange", handler);
  }, []);

  return route;
}

function LoadingState({ error }) {
  const lang = useLang();
  return (
    <main className="loading-state">
      {error ? <WarningCircle size={32} /> : <Compass size={32} className="spin" />}
      <strong>{error ? tu("loading.error", lang) : tu("loading.busy", lang)}</strong>
      {error && <span>{tu("loading.errorHint", lang)}</span>}
    </main>
  );
}

export function App() {
  const route = useRoute();
  const data = useResearchData();
  const [layer, setLayer] = useState("demo");
  const [lang, setLang] = useState("zh");
  const [drawer, setDrawer] = useState({ open: false, sourceIds: [] });
  const candidatesState = useResearchCandidates(layer === "research");
  const evidenceState = useEvidenceData(drawer.open);
  const candidates =
    layer === "research" && candidatesState.status === "ready"
      ? candidatesState.candidates
      : null;

  const openActor = (actorId) => {
    sessionStorage.setItem("nr3.actor", actorId);
    window.location.hash = "#/actors";
  };

  const openEvidence = (sourceIds) => {
    if (sourceIds?.length) setDrawer({ open: true, sourceIds });
  };

  // Route change closes the evidence drawer so it never covers a new page.
  useEffect(() => {
    setDrawer((current) =>
      current.open ? { open: false, sourceIds: [] } : current,
    );
  }, [route]);

  const pageProps = { layer, candidates };

  return (
    <LangContext.Provider value={lang}>
      <EvidenceContext.Provider value={{ openEvidence }}>
        <div className="app-shell">
          <TopBar
            route={route}
            layer={layer}
            onLayerChange={setLayer}
            lang={lang}
            onLangChange={setLang}
          />
          {data.status === "ready" ? (
            route === "actors" ? (
              <ActorsPage data={data} {...pageProps} />
            ) : route === "time" ? (
              <TimePage data={data} onOpenActor={openActor} {...pageProps} />
            ) : route === "pathways" ? (
              <PathwaysPage data={data} onOpenActor={openActor} {...pageProps} />
            ) : route === "evidence" ? (
              <EvidencePage data={data} {...pageProps} />
            ) : (
              <OverviewPage data={data} {...pageProps} />
            )
          ) : (
            <LoadingState error={data.status === "error"} />
          )}
          {drawer.open && (
            <EvidenceDrawer
              state={evidenceState}
              sourceIds={drawer.sourceIds}
              onClose={() => setDrawer({ open: false, sourceIds: [] })}
            />
          )}
        </div>
      </EvidenceContext.Provider>
    </LangContext.Provider>
  );
}
