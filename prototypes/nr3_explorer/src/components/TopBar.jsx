import {
  Books,
  Buildings,
  ClockCounterClockwise,
  Compass,
  GitBranch,
  MapTrifold,
} from "@phosphor-icons/react";
import { LANGS, useLang } from "../lib/labels.js";
import { tu } from "../lib/ui_strings.js";

const MAIN_NAV = [
  { id: "overview", key: "nav.overview", icon: MapTrifold, href: "#/" },
  { id: "actors", key: "nav.actors", icon: Buildings, href: "#/actors" },
  { id: "time", key: "nav.time", icon: ClockCounterClockwise, href: "#/time" },
  { id: "pathways", key: "nav.pathways", icon: GitBranch, href: "#/pathways" },
  { id: "evidence", key: "nav.evidence", icon: Books, href: "#/evidence" },
];

export function TopBar({ route, layer, onLayerChange, lang, onLangChange }) {
  const contextLang = useLang();
  const activeLang = lang || contextLang;
  return (
    <header className="topbar">
      <a className="brand" href="#/" aria-label={tu("topbar.home", activeLang)}>
        <span className="brand-mark" aria-hidden="true">
          <Compass weight="fill" />
        </span>
        <span>
          <strong>{tu("brand.name", activeLang)}</strong>
          <small>NGO / CIVIC EXPLORER</small>
        </span>
      </a>
      <nav className="main-nav" aria-label={tu("topbar.mainNav", activeLang)}>
        {MAIN_NAV.map((item) => {
          const Icon = item.icon;
          return (
            <a
              key={item.id}
              className={`${route === item.id ? "active" : ""}`}
              href={item.href}
            >
              <Icon size={18} weight={route === item.id ? "fill" : "regular"} />
              <span>{tu(item.key, activeLang)}</span>
            </a>
          );
        })}
      </nav>
      <div className="topbar-right">
        <div
          className="layer-switch lang-switch"
          role="group"
          aria-label={tu("topbar.langAria", activeLang)}
        >
          {LANGS.map((item) => (
            <button
              key={item.id}
              className={activeLang === item.id ? "active" : ""}
              onClick={() => onLangChange(item.id)}
              type="button"
            >
              {item.label}
            </button>
          ))}
        </div>
        <div
          className="layer-switch"
          role="group"
          aria-label={tu("layer.aria", activeLang)}
          title={tu("layer.hint", activeLang)}
        >
          <button
            className={layer === "demo" ? "active" : ""}
            onClick={() => onLayerChange("demo")}
            type="button"
          >
            {tu("layer.demo", activeLang)}
          </button>
          <button
            className={layer === "research" ? "active" : ""}
            onClick={() => onLayerChange("research")}
            type="button"
          >
            {tu("layer.research", activeLang)}
          </button>
        </div>
      </div>
    </header>
  );
}
