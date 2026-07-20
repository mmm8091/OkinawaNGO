import { useState } from "react";
import { MapPin, MapTrifold, Quotes } from "@phosphor-icons/react";
import { useLang } from "../lib/labels.js";
import { tu } from "../lib/ui_strings.js";
import { ChartHelp, SegmentedControl } from "../components/ui.jsx";
import { CanvasControls, MapCanvas, clampZoom } from "../components/MapCanvas.jsx";
import { RegionPanel } from "../components/RegionPanel.jsx";
import { SakishimaFrameExhibit } from "../components/SakishimaFrameExhibit.jsx";

export function OverviewPage({ data, layer, candidates, onOpenActor }) {
  const [viewMode, setViewMode] = useState("map");
  const [region, setRegion] = useState("all");
  const [mapState, setMapState] = useState("all");
  const [zoom, setZoom] = useState(1);
  const [pan, setPan] = useState({ x: 0, y: 0 });
  const lang = useLang();
  const sakishimaExhibit = data.exhibits?.["PUB-MR-004"];

  const changeMapState = (next) => {
    setMapState(next);
    if (next === "sakishima") setRegion("sakishima");
    else if (region === "sakishima") setRegion("all");
  };

  const zoomBy = (delta) => {
    const nextZoom = clampZoom(zoom + delta);
    setPan((current) => ({
      x: (current.x * nextZoom) / zoom,
      y: (current.y * nextZoom) / zoom,
    }));
    setZoom(nextZoom);
  };

  const resetMap = () => {
    setZoom(1);
    setPan({ x: 0, y: 0 });
    setRegion("all");
    setMapState("all");
  };

  const pickIssue = (issueId) => {
    sessionStorage.setItem("nr3.issueFilter", issueId);
    window.location.hash = "#/actors";
  };

  const pickEpisode = (episodeId) => {
    sessionStorage.setItem("nr3.episode", episodeId);
    window.location.hash = "#/pathways";
  };

  const panelRegion = mapState === "sakishima" ? "sakishima" : region;

  return (
    <main className="workspace">
      <div className="workspace-top">
        <div className="page-intro">
          <h1>
            {tu("overview.title", lang)}
            <ChartHelp title={tu("overview.title", lang)}>
              <p>{tu("help.overview.p1", lang)}</p>
              <p>{tu("help.overview.p2", lang)}</p>
            </ChartHelp>
          </h1>
        </div>
        {sakishimaExhibit && (
          <SegmentedControl
            label={tu("overview.viewAria", lang)}
            value={viewMode}
            onChange={setViewMode}
            items={[
              {
                id: "map",
                label: tu("overview.viewMap", lang),
                icon: MapTrifold,
              },
              {
                id: "frames",
                label: tu("overview.viewFrames", lang),
                icon: Quotes,
              },
            ]}
          />
        )}
        {viewMode === "map" && (
          <SegmentedControl
            label={tu("map.stateAria", lang)}
            value={mapState}
            onChange={changeMapState}
            items={[
              { id: "all", label: tu("map.all", lang), icon: MapTrifold },
              { id: "sakishima", label: tu("map.sakishima", lang), icon: MapPin },
            ]}
          />
        )}
      </div>
      {viewMode === "frames" && sakishimaExhibit ? (
        <div className="published-exhibit-scroll">
          <SakishimaFrameExhibit
            exhibit={sakishimaExhibit}
            lang={lang}
            onOpenActor={onOpenActor}
            layer={layer}
          />
        </div>
      ) : (
        <div className="overview-grid">
          <section className="visual-stage">
            <MapCanvas
              geometry={data.geometry}
              presentation={data.presentation}
              selectedRegion={region}
              setSelectedRegion={setRegion}
              zoom={zoom}
              setZoom={setZoom}
              pan={pan}
              setPan={setPan}
              mapState={mapState}
            />
            <CanvasControls zoom={zoom} zoomBy={zoomBy} reset={resetMap} />
          </section>
          <RegionPanel
            region={panelRegion}
            presentation={data.presentation}
            places={data.places}
            issues={data.issues}
            strictRelations={data.relations.strict_place_issue}
            actorPlaces={data.relations.actor_place}
            episodes={data.episodes}
            onPickIssue={pickIssue}
            onPickEpisode={pickEpisode}
            layer={layer}
            candidates={candidates}
          />
        </div>
      )}
    </main>
  );
}
