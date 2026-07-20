import { useCallback, useEffect, useRef, useState } from "react";
import { geoMercator, geoPath } from "d3-geo";
import { House, Minus, Plus } from "@phosphor-icons/react";
import { regionMeta } from "../lib/data.js";
import { useLang } from "../lib/labels.js";
import { tu } from "../lib/ui_strings.js";

// Region label anchors: municipality name in the packaged GeoJSON plus a
// screen-pixel offset so the label sits in open sea next to its islands.
const LABEL_ANCHORS = {
  okinawa: { name: "沖縄市", dx: 96, dy: -50 },
  miyako: { name: "宮古島市", dx: 62, dy: -44 },
  yaeyama: { name: "石垣市", dx: -40, dy: -64 },
};

const clampZoom = (value) => Math.max(1, Math.min(2.6, value));

export function MapCanvas({
  geometry,
  presentation,
  selectedRegion,
  setSelectedRegion,
  zoom,
  setZoom,
  pan,
  setPan,
  mapState,
}) {
  const canvasRef = useRef(null);
  const wrapperRef = useRef(null);
  const [hover, setHover] = useState(null);
  const hitRef = useRef([]);
  const dragRef = useRef(null);
  const labelRefs = useRef({});
  const lang = useLang();

  const regionDimmed = useCallback(
    (region) => {
      if (mapState === "sakishima") {
        return region !== "miyako" && region !== "yaeyama";
      }
      return selectedRegion !== "all" && selectedRegion !== region;
    },
    [mapState, selectedRegion],
  );

  const regionSelectable = useCallback(
    (region) => mapState !== "sakishima",
    [mapState],
  );

  const draw = useCallback(() => {
    const canvas = canvasRef.current;
    const wrapper = wrapperRef.current;
    if (!canvas || !wrapper || !geometry) return;
    const width = wrapper.clientWidth;
    const height = wrapper.clientHeight;
    const dpr = window.devicePixelRatio || 1;
    canvas.width = width * dpr;
    canvas.height = height * dpr;
    canvas.style.width = `${width}px`;
    canvas.style.height = `${height}px`;
    const context = canvas.getContext("2d");
    context.setTransform(dpr, 0, 0, dpr, 0, 0);
    context.clearRect(0, 0, width, height);

    const projection = geoMercator().fitExtent(
      [
        [42, 30],
        [width - 46, height - 34],
      ],
      geometry,
    );
    const path = geoPath(projection, context);
    const pathText = geoPath(projection);
    hitRef.current = geometry.features.map((feature) => ({
      region: feature.properties.region,
      name: feature.properties.name,
      path2d: new Path2D(pathText(feature) || ""),
    }));

    const centerX = width / 2;
    const centerY = height / 2;
    context.save();
    context.translate(centerX + pan.x, centerY + pan.y);
    context.scale(zoom, zoom);
    context.translate(-centerX, -centerY);

    geometry.features.forEach((feature) => {
      const region = feature.properties.region;
      const dimmed = regionDimmed(region);
      context.beginPath();
      path(feature);
      context.fillStyle = dimmed
        ? "#dfe5e2"
        : regionMeta(region, presentation).color;
      context.globalAlpha = dimmed ? 0.55 : 0.92;
      context.fill();
      context.globalAlpha = 1;
      context.strokeStyle = "#f4f1e9";
      context.lineWidth = dimmed ? 0.5 : 0.85;
      context.stroke();
    });

    const focusFeatures = {
      okinawa: ["那覇市", "名護市", "宜野湾市", "沖縄市"],
      miyako: ["宮古島市"],
      yaeyama: ["石垣市", "与那国町"],
      other: ["久米島町"],
    };
    Object.entries(focusFeatures).forEach(([region, names]) => {
      names.forEach((name, index) => {
        const feature = geometry.features.find(
          (item) => item.properties.name === name,
        );
        if (!feature) return;
        const centroid = path.centroid(feature);
        if (!Number.isFinite(centroid[0])) return;
        const dimmed = regionDimmed(region);
        const radius = index === 0 ? 7 : 4.5;
        context.beginPath();
        context.arc(centroid[0], centroid[1], (radius + 3) / zoom, 0, Math.PI * 2);
        context.fillStyle = dimmed
          ? "rgba(236,240,237,.72)"
          : "rgba(248,247,241,.92)";
        context.fill();
        context.beginPath();
        context.arc(centroid[0], centroid[1], radius / zoom, 0, Math.PI * 2);
        context.fillStyle = dimmed
          ? "#b3bfbd"
          : regionMeta(region, presentation).color;
        context.fill();
        context.strokeStyle = "#ffffff";
        context.lineWidth = 1.5 / zoom;
        context.stroke();
      });
    });

    context.restore();

    Object.entries(LABEL_ANCHORS).forEach(([region, config]) => {
      const el = labelRefs.current[region];
      if (!el) return;
      const feature = geometry.features.find(
        (item) => item.properties.name === config.name,
      );
      if (!feature) return;
      const centroid = path.centroid(feature);
      if (!Number.isFinite(centroid[0])) return;
      const x = (centroid[0] - centerX) * zoom + centerX + pan.x + config.dx;
      const y = (centroid[1] - centerY) * zoom + centerY + pan.y + config.dy;
      el.style.transform = `translate(${Math.round(x)}px, ${Math.round(y)}px)`;
      el.style.display = mapState === "sakishima" ? "none" : "";
      el.classList.toggle("dim", mapState !== "all" && regionDimmed(region));
    });
  }, [geometry, mapState, pan, presentation, regionDimmed, zoom]);

  useEffect(() => {
    draw();
    const observer = new ResizeObserver(draw);
    if (wrapperRef.current) observer.observe(wrapperRef.current);
    return () => observer.disconnect();
  }, [draw]);

  // Native wheel listener: React registers wheel as passive, so preventDefault
  // inside onWheel fails and page scroll leaks through.
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const onWheel = (event) => {
      event.preventDefault();
      const rect = canvas.getBoundingClientRect();
      const x = event.clientX - rect.left;
      const y = event.clientY - rect.top;
      const centerX = rect.width / 2;
      const centerY = rect.height / 2;
      const nextZoom = clampZoom(zoom + (event.deltaY < 0 ? 0.2 : -0.2));
      const baseX = (x - centerX - pan.x) / zoom + centerX;
      const baseY = (y - centerY - pan.y) / zoom + centerY;
      setZoom(nextZoom);
      setPan({
        x: x - (baseX - centerX) * nextZoom - centerX,
        y: y - (baseY - centerY) * nextZoom - centerY,
      });
    };
    canvas.addEventListener("wheel", onWheel, { passive: false });
    return () => canvas.removeEventListener("wheel", onWheel);
  }, [pan, setPan, setZoom, zoom]);

  const locate = (event) => {
    const canvas = canvasRef.current;
    if (!canvas) return null;
    const rect = canvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;
    const centerX = rect.width / 2;
    const centerY = rect.height / 2;
    const baseX = (x - centerX - pan.x) / zoom + centerX;
    const baseY = (y - centerY - pan.y) / zoom + centerY;
    const context = canvas.getContext("2d");
    // isPointInPath interprets coordinates under the current transform; reset
    // to identity so CSS-pixel paths match CSS-pixel pointer math on any DPR.
    context.save();
    context.setTransform(1, 0, 0, 1, 0, 0);
    const hit = hitRef.current.find((area) =>
      context.isPointInPath(area.path2d, baseX, baseY),
    );
    context.restore();
    return hit ? { ...hit, x, y } : null;
  };

  const handlePointerDown = (event) => {
    event.currentTarget.setPointerCapture(event.pointerId);
    dragRef.current = {
      startX: event.clientX,
      startY: event.clientY,
      panX: pan.x,
      panY: pan.y,
      moved: false,
    };
  };

  const handlePointerMove = (event) => {
    const drag = dragRef.current;
    if (drag) {
      const dx = event.clientX - drag.startX;
      const dy = event.clientY - drag.startY;
      if (Math.abs(dx) + Math.abs(dy) > 4) drag.moved = true;
      if (drag.moved) {
        setPan({
          x: Math.max(-520, Math.min(520, drag.panX + dx)),
          y: Math.max(-380, Math.min(380, drag.panY + dy)),
        });
        setHover(null);
      }
      return;
    }
    const hit = locate(event);
    event.currentTarget.style.cursor =
      hit && regionSelectable(hit.region) ? "pointer" : "crosshair";
    setHover(hit);
  };

  const handlePointerUp = (event) => {
    const drag = dragRef.current;
    dragRef.current = null;
    if (drag?.moved) return;
    const hit = locate(event);
    if (hit && regionSelectable(hit.region)) setSelectedRegion(hit.region);
  };

  return (
    <div className="map-wrapper" ref={wrapperRef}>
      <canvas
        ref={canvasRef}
        role="img"
        aria-label={tu("map.aria", lang)}
        onPointerDown={handlePointerDown}
        onPointerMove={handlePointerMove}
        onPointerUp={handlePointerUp}
        onPointerLeave={() => {
          setHover(null);
          dragRef.current = null;
        }}
      />
      <div className="map-region-labels">
        {["okinawa", "miyako", "yaeyama"].map((region) => (
          <button
            key={region}
            ref={(el) => {
              labelRefs.current[region] = el;
            }}
            className={`region-label ${region} ${
              selectedRegion === region ? "active" : ""
            }`}
            onClick={() => {
              if (regionSelectable(region)) setSelectedRegion(region);
            }}
            type="button"
          >
            <i
              className="region-dot"
              style={{ background: regionMeta(region, presentation).color }}
            />
            {tu(`region.${region}`, lang)}
          </button>
        ))}
      </div>
      {hover && (
        <div
          className="map-tooltip"
          style={{ left: hover.x + 14, top: hover.y + 16 }}
        >
          <strong>{hover.name}</strong>
          <span>{tu(`region.${hover.region}`, lang)}</span>
        </div>
      )}
    </div>
  );
}

export function CanvasControls({ zoom, zoomBy, reset, min = 1, max = 2.6 }) {
  const lang = useLang();
  return (
    <div className="canvas-controls" aria-label={tu("controls.aria", lang)}>
      <button onClick={reset} title={tu("controls.reset", lang)} type="button">
        <House size={19} />
      </button>
      <button
        onClick={() => zoomBy(0.25)}
        title={tu("controls.zoomIn", lang)}
        type="button"
        disabled={zoom >= max}
      >
        <Plus size={19} />
      </button>
      <button
        onClick={() => zoomBy(-0.25)}
        title={tu("controls.zoomOut", lang)}
        type="button"
        disabled={zoom <= min}
      >
        <Minus size={19} />
      </button>
      <span className="zoom-readout">{Math.round(zoom * 100)}%</span>
    </div>
  );
}

export { clampZoom };
