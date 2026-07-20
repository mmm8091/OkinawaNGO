import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { forceCollide, forceManyBody, forceSimulation, forceX, forceY } from "d3-force";
import { CheckCircle, MagnifyingGlass } from "@phosphor-icons/react";
import { actorClassGroup, actorClassMeta } from "../lib/data.js";
import { tr, useLang } from "../lib/labels.js";
import { tu } from "../lib/ui_strings.js";
import { CanvasControls } from "./MapCanvas.jsx";

const clampK = (value) => Math.max(0.6, Math.min(3, value));

export function ActorCanvas({
  actors,
  issues,
  relations,
  selectedActor,
  setSelectedActor,
  classFilter,
  issueFilter,
  onPickIssue,
  search,
  layer,
  candidates,
  scopeNote,
  presentation,
}) {
  const canvasRef = useRef(null);
  const wrapperRef = useRef(null);
  const nodesRef = useRef([]);
  const dragRef = useRef(null);
  const [hoverNode, setHoverNode] = useState(null);
  const [view, setView] = useState({ k: 1, x: 0, y: 0 });
  const lang = useLang();

  const graph = useMemo(() => {
    const actorById = new Map(actors.map((actor) => [actor.id, actor]));
    const issueById = new Map(issues.map((issue) => [issue.id, issue]));
    const inScope = (edge) =>
      actorById.has(edge.actor_id) && issueById.has(edge.issue_id);
    const applyFilters = (list) => {
      let edges = list;
      if (classFilter !== "all") {
        edges = edges.filter(
          (edge) =>
            actorClassGroup(
              actorById.get(edge.actor_id)?.actor_class,
              presentation,
            ) === classFilter,
        );
      }
      if (issueFilter !== "all") {
        edges = edges.filter((edge) => edge.issue_id === issueFilter);
      }
      if (search.trim()) {
        const term = search.trim().toLowerCase();
        edges = edges.filter((edge) => {
          const actor = actorById.get(edge.actor_id);
          if (!actor) return false;
          const haystack = [actor.id, actor.display_label, ...(actor.aliases || [])]
            .join(" ")
            .toLowerCase();
          return haystack.includes(term);
        });
      }
      return edges;
    };

    const demoEdges = applyFilters(relations.actor_issue.filter(inScope));
    const pendingEdges =
      layer === "research"
        ? applyFilters((candidates?.relations.actor_issue || []).filter(inScope))
        : [];
    const edges = [
      ...demoEdges.map((edge) => ({ ...edge, pending: false })),
      ...pendingEdges.map((edge) => ({ ...edge, pending: true })),
    ];
    const actorIds = [...new Set(edges.map((edge) => edge.actor_id))];
    const issueIds = [...new Set(edges.map((edge) => edge.issue_id))];
    const pendingOnlyActors = new Set(
      actorIds.filter((id) => !demoEdges.some((edge) => edge.actor_id === id)),
    );
    const frozenCount = demoEdges.filter(
      (edge) => edge.display_state === "frozen_bounded",
    ).length;
    const scopeReviewedPendingCount = pendingEdges.filter(
      (edge) => edge.display_state === "scope_reviewed_fact_pending",
    ).length;
    const hasStates = edges.some((edge) => edge.display_state);
    return {
      edges,
      demoCount: demoEdges.length,
      pendingCount: pendingEdges.length,
      frozenCount,
      scopeReviewedPendingCount,
      hasStates,
      actorIds,
      issueIds,
      actorById,
      issueById,
      pendingOnlyActors,
    };
  }, [
    actors,
    candidates,
    classFilter,
    issueFilter,
    issues,
    layer,
    presentation,
    relations.actor_issue,
    search,
  ]);

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

    const issueNodes = graph.issueIds.map((id, index) => {
      const angle = (index / Math.max(graph.issueIds.length, 1)) * Math.PI * 2 - Math.PI / 2;
      return {
        id,
        kind: "issue",
        label: graph.issueById.get(id).display_label,
        x: width / 2 + Math.cos(angle) * Math.min(width * 0.32, 300),
        y: height / 2 + Math.sin(angle) * Math.min(height * 0.34, 235),
        fx: width / 2 + Math.cos(angle) * Math.min(width * 0.32, 300),
        fy: height / 2 + Math.sin(angle) * Math.min(height * 0.34, 235),
      };
    });
    const issuePosition = new Map(issueNodes.map((node) => [node.id, node]));
    const actorNodes = graph.actorIds.map((id, index) => {
      const linked = graph.edges
        .filter((edge) => edge.actor_id === id)
        .map((edge) => issuePosition.get(edge.issue_id))
        .filter(Boolean);
      const targetX =
        linked.reduce((sum, node) => sum + node.x, 0) / Math.max(linked.length, 1);
      const targetY =
        linked.reduce((sum, node) => sum + node.y, 0) / Math.max(linked.length, 1);
      return {
        id,
        kind: "actor",
        label: graph.actorById.get(id).display_label,
        actor: graph.actorById.get(id),
        x: targetX + ((index % 5) - 2) * 9,
        y: targetY + ((index % 7) - 3) * 8,
        targetX,
        targetY,
      };
    });
    const simulation = forceSimulation(actorNodes)
      .force("charge", forceManyBody().strength(-28))
      .force("collide", forceCollide(8.5))
      .force("x", forceX((d) => d.targetX).strength(0.13))
      .force("y", forceY((d) => d.targetY).strength(0.13))
      .stop();
    for (let i = 0; i < 160; i += 1) simulation.tick();
    const allNodes = [...issueNodes, ...actorNodes];
    nodesRef.current = allNodes;
    const nodeById = new Map(allNodes.map((node) => [node.id, node]));

    const toScreen = (node) => ({
      x: node.x * view.k + view.x,
      y: node.y * view.k + view.y,
    });

    // Geometry under the pan/zoom transform.
    context.save();
    context.translate(view.x, view.y);
    context.scale(view.k, view.k);

    graph.edges.forEach((edge) => {
      const a = nodeById.get(edge.actor_id);
      const b = nodeById.get(edge.issue_id);
      if (!a || !b) return;
      const active = selectedActor === edge.actor_id || issueFilter === edge.issue_id;
      context.beginPath();
      context.moveTo(a.x, a.y);
      context.lineTo(b.x, b.y);
      if (edge.pending) {
        context.setLineDash([3, 5]);
        context.strokeStyle = active
          ? "rgba(138,108,30,.6)"
          : "rgba(140,155,155,.32)";
      } else {
        context.strokeStyle = active
          ? "rgba(15,70,78,.68)"
          : "rgba(75,104,105,.15)";
      }
      context.lineWidth = (active ? 1.35 : 0.65) / view.k;
      context.stroke();
      context.setLineDash([]);
    });

    issueNodes.forEach((node) => {
      const active = issueFilter === node.id;
      context.beginPath();
      context.arc(node.x, node.y, active ? 10 : 8, 0, Math.PI * 2);
      context.fillStyle = active ? "#0f5961" : "#f5f2e9";
      context.fill();
      context.strokeStyle = "#2b7f80";
      context.lineWidth = 1.2 / view.k;
      context.stroke();
    });

    actorNodes.forEach((node) => {
      const selected = selectedActor === node.id;
      const meta = actorClassMeta(node.actor.actor_class, presentation);
      if (selected) {
        context.beginPath();
        context.arc(node.x, node.y, 9.5, 0, Math.PI * 2);
        context.fillStyle = "#faf8f1";
        context.fill();
      }
      context.beginPath();
      context.arc(node.x, node.y, selected ? 6.5 : 5, 0, Math.PI * 2);
      context.fillStyle = meta.color;
      context.fill();
      context.strokeStyle = "#ffffff";
      context.lineWidth = 1 / view.k;
      context.stroke();
      if (graph.pendingOnlyActors.has(node.id)) {
        context.beginPath();
        context.setLineDash([2.5, 2.5]);
        context.arc(node.x, node.y, 8.5, 0, Math.PI * 2);
        context.strokeStyle = "rgba(138,108,30,.75)";
        context.lineWidth = 1.1 / view.k;
        context.stroke();
        context.setLineDash([]);
      }
    });

    context.restore();

    // Text stays in screen space so labels keep a constant readable size.
    issueNodes.forEach((node) => {
      const pos = toScreen(node);
      const text = tr(node.label, lang);
      context.font = "600 11px 'Noto Sans SC', sans-serif";
      context.textAlign = "center";
      const labelY = pos.y + (pos.y < height / 2 ? -13 : 22);
      context.lineWidth = 3;
      context.strokeStyle = "rgba(238,242,238,.92)";
      context.strokeText(text, pos.x, labelY);
      context.fillStyle = "#34515a";
      context.fillText(text, pos.x, labelY);
    });

    const selectedNode = actorNodes.find((node) => node.id === selectedActor);
    if (selectedNode) {
      const pos = toScreen(selectedNode);
      const label =
        selectedNode.label.length > 24
          ? `${selectedNode.label.slice(0, 23)}…`
          : selectedNode.label;
      context.font = "600 12px 'Noto Sans SC', sans-serif";
      const textWidth = context.measureText(label).width;
      const pillWidth = textWidth + 24;
      const pillHeight = 26;
      let px = pos.x + 14;
      let py = pos.y - pillHeight - 10;
      px = Math.max(6, Math.min(px, width - pillWidth - 6));
      if (py < 6) py = pos.y + 12;
      context.beginPath();
      if (typeof context.roundRect === "function") {
        context.roundRect(px, py, pillWidth, pillHeight, 13);
      } else {
        context.rect(px, py, pillWidth, pillHeight);
      }
      context.fillStyle = "rgba(250,249,244,.96)";
      context.fill();
      context.strokeStyle = "#c4d2ce";
      context.lineWidth = 1;
      context.stroke();
      context.fillStyle = "#173540";
      context.textAlign = "left";
      context.textBaseline = "middle";
      context.fillText(label, px + 12, py + pillHeight / 2 + 0.5);
      context.textBaseline = "alphabetic";
    }
  }, [graph, issueFilter, lang, presentation, selectedActor, view]);

  useEffect(() => {
    draw();
    const observer = new ResizeObserver(draw);
    if (wrapperRef.current) observer.observe(wrapperRef.current);
    return () => observer.disconnect();
  }, [draw]);

  // Native wheel listener (React wheel handlers are passive).
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
    const canvas = canvasRef.current;
    const rect = canvas?.getBoundingClientRect();
    const cx = rect ? rect.width / 2 : 0;
    const cy = rect ? rect.height / 2 : 0;
    const nextK = clampK(view.k + delta);
    const worldX = (cx - view.x) / view.k;
    const worldY = (cy - view.y) / view.k;
    setView({ k: nextK, x: cx - worldX * nextK, y: cy - worldY * nextK });
  };

  const resetView = () => setView({ k: 1, x: 0, y: 0 });

  const hitAt = (event) => {
    const rect = canvasRef.current.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;
    const dist = (node) =>
      Math.hypot(node.x * view.k + view.x - x, node.y * view.k + view.y - y);
    const actorNode = nodesRef.current
      .filter((node) => node.kind === "actor")
      .map((node) => ({ ...node, distance: dist(node) }))
      .sort((a, b) => a.distance - b.distance)[0];
    const issueNode = nodesRef.current
      .filter((node) => node.kind === "issue")
      .map((node) => ({ ...node, distance: dist(node) }))
      .sort((a, b) => a.distance - b.distance)[0];
    return { actorNode, issueNode, x, y };
  };

  const issueTooltip = (node) => {
    const count = graph.edges.filter((edge) => edge.issue_id === node.id).length;
    return `${tr(node.label, lang)} · ${count}`;
  };

  return (
    <div className="actor-canvas-wrap" ref={wrapperRef}>
      <canvas
        ref={canvasRef}
        role="img"
        aria-label={tu("actors.canvasAria", lang)}
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
              setView((current) => ({
                ...current,
                x: drag.viewX + dx,
                y: drag.viewY + dy,
              }));
              setHoverNode(null);
            }
            return;
          }
          const { actorNode, issueNode } = hitAt(event);
          const overActor =
            actorNode &&
            actorNode.distance < 14 &&
            !(issueNode && issueNode.distance < actorNode.distance);
          const overIssue =
            !overActor && issueNode && issueNode.distance < 14;
          event.currentTarget.style.cursor =
            overActor || overIssue ? "pointer" : "crosshair";
          if (overActor) {
            const rect = event.currentTarget.getBoundingClientRect();
            setHoverNode({
              x: event.clientX - rect.left,
              y: event.clientY - rect.top,
              label: actorNode.label,
            });
          } else if (overIssue) {
            const rect = event.currentTarget.getBoundingClientRect();
            setHoverNode({
              x: event.clientX - rect.left,
              y: event.clientY - rect.top,
              label: issueTooltip(issueNode),
            });
          } else {
            setHoverNode(null);
          }
        }}
        onPointerUp={(event) => {
          const drag = dragRef.current;
          dragRef.current = null;
          if (drag?.moved) return;
          const { actorNode, issueNode } = hitAt(event);
          const pickActor =
            actorNode &&
            actorNode.distance < 16 &&
            !(issueNode && issueNode.distance < actorNode.distance);
          if (pickActor) {
            setSelectedActor(actorNode.id);
          } else if (issueNode && issueNode.distance < 14) {
            onPickIssue(issueFilter === issueNode.id ? "all" : issueNode.id);
          } else {
            setSelectedActor(null);
          }
        }}
        onPointerLeave={() => {
          setHoverNode(null);
          dragRef.current = null;
        }}
      />
      {hoverNode && (
        <div
          className="actor-tooltip"
          style={{ left: hoverNode.x + 12, top: hoverNode.y + 14 }}
        >
          {hoverNode.label}
        </div>
      )}
      <CanvasControls zoom={view.k} zoomBy={zoomBy} reset={resetView} min={0.6} max={3} />
      <div className="actor-canvas-note">
        <CheckCircle size={16} weight="fill" />
        {layer === "research"
          ? graph.hasStates
            ? tu("actors.noteResearch", lang)
                .replace("{d}", graph.demoCount)
                .replace("{p}", graph.pendingCount)
                .replace("{s}", graph.scopeReviewedPendingCount)
            : tu("actors.noteResearchLegacy", lang)
                .replace("{d}", graph.demoCount)
                .replace("{p}", graph.pendingCount)
          : graph.hasStates
            ? tu("actors.noteDemo", lang)
                .replace("{n}", graph.demoCount)
                .replace("{f}", graph.frozenCount)
            : tu("actors.noteDemoLegacy", lang).replace("{n}", graph.demoCount)}
        {scopeNote && <em className="edgeless-note">{scopeNote}</em>}
      </div>
      {!graph.edges.length && (
        <div className="canvas-empty">
          <MagnifyingGlass size={28} />
          <strong>{tu("actors.emptyTitle", lang)}</strong>
          <span>{tu("actors.emptyHint", lang)}</span>
        </div>
      )}
    </div>
  );
}
