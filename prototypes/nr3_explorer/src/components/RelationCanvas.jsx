import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import {
  forceCollide,
  forceLink,
  forceManyBody,
  forceSimulation,
  forceX,
  forceY,
} from "d3-force";
import { X } from "@phosphor-icons/react";
import { actorClassGroup, labelOf } from "../lib/data.js";
import { tr, useLang } from "../lib/labels.js";
import { tu } from "../lib/ui_strings.js";
import { CanvasControls } from "./MapCanvas.jsx";

const FAMILY_COLORS = {
  resources_funding: "#b07a28",
  commission_service: "#6b7fa3",
  legal_collaboration: "#55756b",
  structural_affiliation: "#2b7f80",
  coordination: "#8a6c98",
};

const DIRECTED_DEFAULT = true;

const clampK = (value) => Math.max(0.5, Math.min(3, value));

const pick = (obj, key) => obj?.relations?.[key] || obj?.[key] || [];

export function RelationCanvas({
  actors,
  dyadicRelations,
  layer,
  candidates,
  selectedActor,
  setSelectedActor,
  search,
  classFilter,
  presentation,
}) {
  const canvasRef = useRef(null);
  const wrapperRef = useRef(null);
  const nodesRef = useRef([]);
  const edgesRef = useRef([]);
  const dragRef = useRef(null);
  const [hoverEdge, setHoverEdge] = useState(null);
  const [pinnedEdge, setPinnedEdge] = useState(null);
  const [hiddenFamilies, setHiddenFamilies] = useState(
    () => new Set(layer === "research" ? [] : ["coordination"]),
  );
  const [view, setView] = useState({ k: 1, x: 0, y: 0 });
  const lang = useLang();
  const research = layer === "research" && candidates;

  useEffect(() => {
    setHiddenFamilies(new Set(layer === "research" ? [] : ["coordination"]));
  }, [layer]);

  const actorById = useMemo(() => new Map(actors.map((a) => [a.id, a])), [actors]);

  const edges = useMemo(() => {
    let list = (dyadicRelations || [])
      .filter((row) => actorById.has(row.source_endpoint) && actorById.has(row.target_endpoint))
      .map((row) => ({ ...row, pending: false }));
    if (research) {
      list = [
        ...list,
        ...pick(candidates, "dyadic_relations")
          .filter((row) => actorById.has(row.source_endpoint) && actorById.has(row.target_endpoint))
          .map((row) => ({ ...row, pending: true })),
      ];
    }
    if (classFilter !== "all") {
      list = list.filter((row) =>
        [row.source_endpoint, row.target_endpoint].some(
          (id) =>
            actorClassGroup(
              actorById.get(id)?.actor_class,
              presentation,
            ) === classFilter,
        ),
      );
    }
    if (search.trim()) {
      const term = search.trim().toLowerCase();
      list = list.filter((row) =>
        [row.source_endpoint, row.target_endpoint].some((id) => {
          const actor = actorById.get(id);
          return [
            actor?.id,
            actor?.display_label,
            ...(actor?.aliases || []).map((alias) => alias.label || alias),
          ]
            .join(" ")
            .toLowerCase()
            .includes(term);
        }),
      );
    }
    return list;
  }, [
    actorById,
    candidates,
    classFilter,
    dyadicRelations,
    presentation,
    research,
    search,
  ]);

  const families = useMemo(() => {
    const counts = new Map();
    edges.forEach((row) => counts.set(row.relation_family, (counts.get(row.relation_family) || 0) + 1));
    return [...counts.entries()];
  }, [edges]);

  const visibleEdges = useMemo(
    () => edges.filter((row) => !hiddenFamilies.has(row.relation_family)),
    [edges, hiddenFamilies],
  );

  const counts = useMemo(() => {
    const of = (rows, status) => rows.filter((row) => row.claim_status === status).length;
    const demo = edges.filter((row) => !row.pending);
    return {
      s: of(demo, "supported"),
      b: of(demo, "supported_bounded"),
      c: edges.filter((row) => row.pending).length,
    };
  }, [edges]);

  const draw = useCallback(() => {
    const canvas = canvasRef.current;
    const wrapper = wrapperRef.current;
    if (!canvas || !wrapper) return;
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

    const actorIds = [...new Set(visibleEdges.flatMap((row) => [row.source_endpoint, row.target_endpoint]))];
    const nodes = actorIds.map((id, index) => {
      const angle = (index / Math.max(actorIds.length, 1)) * Math.PI * 2 - Math.PI / 2;
      return {
        id,
        label: actorById.get(id)?.display_label || id,
        x: width / 2 + Math.cos(angle) * Math.min(width * 0.3, 260),
        y: height / 2 + Math.sin(angle) * Math.min(height * 0.32, 220),
      };
    });
    const nodeById = new Map(nodes.map((node) => [node.id, node]));
    const links = visibleEdges
      .map((row) => ({ ...row, source: row.source_endpoint, target: row.target_endpoint }))
      .filter((row) => nodeById.has(row.source) && nodeById.has(row.target));
    const simulation = forceSimulation(nodes)
      .force(
        "link",
        forceLink(links)
          .id((d) => d.id)
          .distance(120)
          .strength(0.4),
      )
      .force("charge", forceManyBody().strength(-90))
      .force("collide", forceCollide(22))
      .force("x", forceX(width / 2).strength(0.06))
      .force("y", forceY(height / 2).strength(0.08))
      .stop();
    for (let i = 0; i < 200; i += 1) simulation.tick();
    nodesRef.current = nodes;
    edgesRef.current = links.map((row) => ({
      ...row,
      sx: nodeById.get(row.source)?.x ?? nodeById.get(row.source.id)?.x,
      sy: nodeById.get(row.source)?.y ?? nodeById.get(row.source.id)?.y,
      tx: nodeById.get(row.target)?.x ?? nodeById.get(row.target.id)?.x,
      ty: nodeById.get(row.target)?.y ?? nodeById.get(row.target.id)?.y,
    }));

    const toScreen = (x, y) => ({ x: x * view.k + view.x, y: y * view.k + view.y });

    context.save();
    context.translate(view.x, view.y);
    context.scale(view.k, view.k);

    edgesRef.current.forEach((row) => {
      const active = pinnedEdge?.id === row.id || hoverEdge?.id === row.id;
      const color = FAMILY_COLORS[row.relation_family] || "#9aa6a8";
      context.beginPath();
      context.moveTo(row.sx, row.sy);
      context.lineTo(row.tx, row.ty);
      context.strokeStyle = active ? color : `${color}${row.pending ? "99" : "cc"}`;
      context.lineWidth = (active ? 2 : 1.3) / view.k;
      if (row.pending) context.setLineDash([5, 5]);
      context.stroke();
      context.setLineDash([]);
      if (DIRECTED_DEFAULT) {
        const angle = Math.atan2(row.ty - row.sy, row.tx - row.sx);
        const ax = row.tx - Math.cos(angle) * 9;
        const ay = row.ty - Math.sin(angle) * 9;
        const size = (active ? 5.5 : 4) / view.k;
        context.beginPath();
        context.moveTo(ax + Math.cos(angle) * size * 2, ay + Math.sin(angle) * size * 2);
        context.lineTo(
          ax + Math.cos(angle + 2.5) * size,
          ay + Math.sin(angle + 2.5) * size,
        );
        context.lineTo(
          ax + Math.cos(angle - 2.5) * size,
          ay + Math.sin(angle - 2.5) * size,
        );
        context.closePath();
        context.fillStyle = color;
        context.fill();
      }
    });

    nodes.forEach((node) => {
      const selected = selectedActor === node.id;
      if (selected) {
        context.beginPath();
        context.arc(node.x, node.y, 10.5, 0, Math.PI * 2);
        context.fillStyle = "#faf8f1";
        context.fill();
      }
      context.beginPath();
      context.arc(node.x, node.y, selected ? 7 : 5.5, 0, Math.PI * 2);
      context.fillStyle = "#2b7f80";
      context.fill();
      context.strokeStyle = "#ffffff";
      context.lineWidth = 1.2 / view.k;
      context.stroke();
    });

    context.restore();

    nodes.forEach((node) => {
      const pos = toScreen(node.x, node.y);
      const label = node.label.length > 16 ? `${node.label.slice(0, 15)}…` : node.label;
      context.font = "600 11px 'Noto Sans SC', sans-serif";
      context.textAlign = "center";
      context.lineWidth = 3;
      context.strokeStyle = "rgba(238,242,238,.92)";
      context.strokeText(label, pos.x, pos.y + 20);
      context.fillStyle = "#34515a";
      context.fillText(label, pos.x, pos.y + 20);
    });
  }, [actorById, hoverEdge, pinnedEdge, selectedActor, view, visibleEdges]);

  useEffect(() => {
    draw();
    const observer = new ResizeObserver(draw);
    if (wrapperRef.current) observer.observe(wrapperRef.current);
    return () => observer.disconnect();
  }, [draw]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const onWheel = (event) => {
      event.preventDefault();
      const rect = canvas.getBoundingClientRect();
      const x = event.clientX - rect.left;
      const y = event.clientY - rect.top;
      const nextK = clampK(view.k * (event.deltaY < 0 ? 1.18 : 1 / 1.18));
      const worldX = (x - view.x) / view.k;
      const worldY = (y - view.y) / view.k;
      setView({ k: nextK, x: x - worldX * nextK, y: y - worldY * nextK });
    };
    canvas.addEventListener("wheel", onWheel, { passive: false });
    return () => canvas.removeEventListener("wheel", onWheel);
  }, [view]);

  const zoomBy = (delta) => {
    const rect = canvasRef.current?.getBoundingClientRect();
    const cx = rect ? rect.width / 2 : 0;
    const cy = rect ? rect.height / 2 : 0;
    const nextK = clampK(view.k + delta);
    const worldX = (cx - view.x) / view.k;
    const worldY = (cy - view.y) / view.k;
    setView({ k: nextK, x: cx - worldX * nextK, y: cy - worldY * nextK });
  };

  const hitTest = (event) => {
    const rect = canvasRef.current.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;
    const node = nodesRef.current
      .map((n) => ({ ...n, distance: Math.hypot(n.x * view.k + view.x - x, n.y * view.k + view.y - y) }))
      .sort((a, b) => a.distance - b.distance)[0];
    const edge = edgesRef.current
      .map((row) => {
        const x1 = row.sx * view.k + view.x;
        const y1 = row.sy * view.k + view.y;
        const x2 = row.tx * view.k + view.x;
        const y2 = row.ty * view.k + view.y;
        const len = Math.hypot(x2 - x1, y2 - y1) || 1;
        const t = Math.max(0, Math.min(1, ((x - x1) * (x2 - x1) + (y - y1) * (y2 - y1)) / (len * len)));
        const px = x1 + t * (x2 - x1);
        const py = y1 + t * (y2 - y1);
        return { ...row, distance: Math.hypot(px - x, py - y) };
      })
      .sort((a, b) => a.distance - b.distance)[0];
    return { node, edge, x, y };
  };

  const edgeTooltip = (row) =>
    row
      ? {
          title: tr(row.relation_type, lang),
          lines: [
            `${actorById.get(row.source_endpoint)?.display_label || row.source_endpoint} → ${
              actorById.get(row.target_endpoint)?.display_label || row.target_endpoint
            }`,
            `${tr(row.claim_status, lang)} · ${row.evidence_level} · ${tr(row.review_status, lang)}`,
          ],
        }
      : null;

  return (
    <div className="actor-canvas-wrap" ref={wrapperRef}>
      <div className="family-toggles">
        {families.map(([family, count]) => (
          <button
            key={family}
            className={hiddenFamilies.has(family) ? "off" : ""}
            onClick={() =>
              setHiddenFamilies((current) => {
                const next = new Set(current);
                if (next.has(family)) next.delete(family);
                else next.add(family);
                return next;
              })
            }
            type="button"
          >
            <i style={{ background: FAMILY_COLORS[family] || "#9aa6a8" }} />
            {tr(family, lang)}（{count}）
          </button>
        ))}
      </div>
      <canvas
        ref={canvasRef}
        role="img"
        aria-label={tu("actors.relationCanvasAria", lang)}
        onPointerDown={(event) => {
          event.currentTarget.setPointerCapture(event.pointerId);
          dragRef.current = {
            startX: event.clientX,
            startY: event.clientY,
            viewX: view.x,
            viewY: view.y,
            moved: false,
          };
        }}
        onPointerMove={(event) => {
          const drag = dragRef.current;
          if (drag) {
            const dx = event.clientX - drag.startX;
            const dy = event.clientY - drag.startY;
            if (Math.abs(dx) + Math.abs(dy) > 4) drag.moved = true;
            if (drag.moved) {
              setView((current) => ({ ...current, x: drag.viewX + dx, y: drag.viewY + dy }));
              setHoverEdge(null);
            }
            return;
          }
          const { node, edge, x, y } = hitTest(event);
          const overNode = node && node.distance < 14;
          const overEdge = !overNode && edge && edge.distance < 8;
          event.currentTarget.style.cursor = overNode || overEdge ? "pointer" : "crosshair";
          setHoverEdge(overEdge ? { ...edge, x, y } : null);
        }}
        onPointerUp={(event) => {
          const drag = dragRef.current;
          dragRef.current = null;
          if (drag?.moved) return;
          const { node, edge } = hitTest(event);
          if (node && node.distance < 16) {
            setSelectedActor(node.id === selectedActor ? null : node.id);
            setPinnedEdge(null);
          } else if (edge && edge.distance < 9) {
            setPinnedEdge(pinnedEdge?.id === edge.id ? null : edge);
          } else {
            setSelectedActor(null);
            setPinnedEdge(null);
          }
        }}
        onPointerLeave={() => {
          setHoverEdge(null);
          dragRef.current = null;
        }}
      />
      {hoverEdge && !pinnedEdge && (
        <div className="actor-tooltip" style={{ left: hoverEdge.x + 12, top: hoverEdge.y + 14 }}>
          <strong>{edgeTooltip(hoverEdge).title}</strong>
          {edgeTooltip(hoverEdge).lines.map((line) => (
            <span key={line} style={{ display: "block" }}>{line}</span>
          ))}
        </div>
      )}
      {pinnedEdge && (
        <div className="edge-card">
          <header>
            <strong>{tr(pinnedEdge.relation_type, lang)}</strong>
            <button onClick={() => setPinnedEdge(null)} title={tu("common.close", lang)} type="button">
              <X size={15} />
            </button>
          </header>
          <p className="edge-card-dir">
            {actorById.get(pinnedEdge.source_endpoint)?.display_label || pinnedEdge.source_endpoint}
            {" → "}
            {actorById.get(pinnedEdge.target_endpoint)?.display_label || pinnedEdge.target_endpoint}
          </p>
          <div className="relation-meta">
            <span className={`claim-chip ${pinnedEdge.claim_status}`}>{tr(pinnedEdge.claim_status, lang)}</span>
            <span>{pinnedEdge.evidence_level}</span>
            <span>{tr(pinnedEdge.review_status, lang)}</span>
          </div>
          {pinnedEdge.claim_status === "supported_bounded" && (
            <div className="scope-lines">
              {pinnedEdge.confirmed_scope && (
                <p>
                  <small>{tu("relation.confirmed", lang)}</small>
                  {pinnedEdge.confirmed_scope}
                </p>
              )}
              {pinnedEdge.missing_scope && (
                <p className="missing">
                  <small>{tu("relation.missing", lang)}</small>
                  {pinnedEdge.missing_scope}
                </p>
              )}
            </div>
          )}
          {(pinnedEdge.amount || pinnedEdge.amount_semantics || pinnedEdge.date_or_period) && (
            <small className="relation-amount">
              {pinnedEdge.amount ? `${pinnedEdge.amount} ${pinnedEdge.currency || ""} · ` : ""}
              {tr(pinnedEdge.amount_semantics, lang)}
              {pinnedEdge.date_or_period ? ` · ${pinnedEdge.date_or_period}` : ""}
            </small>
          )}
          {pinnedEdge.interpretation_limit && <p className="limit-line">{pinnedEdge.interpretation_limit}</p>}
        </div>
      )}
      <CanvasControls zoom={view.k} zoomBy={zoomBy} reset={() => setView({ k: 1, x: 0, y: 0 })} min={0.5} max={3} />
      <div className="actor-canvas-note relation-note">
        {tu("actors.relationNote", lang)
          .replace("{s}", counts.s)
          .replace("{b}", counts.b)
          .replace("{c}", counts.c)}
      </div>
    </div>
  );
}
