import { useEffect, useId, useMemo, useState } from "react";
import { BoundaryNote, ExhibitHeader, Unavailable } from "./exhibit/ExhibitKit.jsx";
import "./exhibit/exhibit.css";
import "./OfficialCollaborationExhibit.css";

const COPY = {
  zh: {
    eyebrow: "冲绳县 FY2024 · 官方记录",
    fallbackTitle: "县政府日常协作：616 条记录",
    sourceRows: "官方记录行",
    pdfPages: "原表页数",
    departments: "部门来源标签",
    mechanismShare: "机制 1–4 所占记录",
    adjacentShare: "人权／和平＋国际协力记录",
    modesLabel: "切换统计维度",
    modeDepartment: "部门",
    modeFunction: "事業分野",
    modeResource: "协作机制",
    countSuffix: "条",
    shareOfRows: "占 616 条记录",
    sourceLabel: "来源标签",
    offices: "处室来源标签",
    functions: "事業分野",
    resourceTypes: "协作机制",
    departmentsMeta: "部门",
    details: "有记录的交叉单元",
    detailsHint: "选择左侧汇总行，查看它与其他官方分类的交叉记录。",
    byResource: "按协作机制",
    byDepartment: "按部门",
    byFunction: "按事業分野",
    originalRows: "原表行",
    originalPages: "PDF 页",
    exactTrace: "完整压缩引用",
    noCells: "当前汇总项的交叉计数为 0。",
    boundaryTitle: "如何阅读",
    boundary: "每一条记录对应官方表中的一次协作记载。请按部门、事業分野或协作机制比较记录分布；付款与组织关系可进入具体记录核对。",
    mechanismBoundary: "按协作机制比较记录分布；付款信息请进入具体记录核对",
    functionBoundary: "按官方事業分野比较记录分布；组织宗旨与立场请查看组织档案",
    departmentBoundary: "按主管部门比较协作记录的分布；资源关系请查看具体合同或资助证据",
    unavailable: "展品数据尚未载入。",
    rowsNotActors: "616 条官方协作记录",
  },
  ja: {
    eyebrow: "沖縄県 FY2024 · 公式記録",
    fallbackTitle: "県の日常的な協働：616件の記録",
    sourceRows: "公式資料の行",
    pdfPages: "原資料の頁数",
    departments: "部局の資料表記",
    mechanismShare: "形態1–4に属する行",
    adjacentShare: "人権・平和＋国際協力の行",
    modesLabel: "集計軸を切り替える",
    modeDepartment: "部局",
    modeFunction: "事業分野",
    modeResource: "協働形態",
    countSuffix: "行",
    shareOfRows: "全616行に占める割合",
    sourceLabel: "資料表記",
    offices: "課室の資料表記",
    functions: "事業分野",
    resourceTypes: "協働形態",
    departmentsMeta: "部局",
    details: "非ゼロの交差セル",
    detailsHint: "左の集計行を選ぶと、他の公式分類との交差記録を確認できます。",
    byResource: "協働形態別",
    byDepartment: "部局別",
    byFunction: "事業分野別",
    originalRows: "原表の行",
    originalPages: "PDF頁",
    exactTrace: "全件の圧縮参照",
    noCells: "表示できる非ゼロの交差セルはありません。",
    boundaryTitle: "解釈上の境界",
    boundary: "各行は公式表に記載された一件の協働記録です。部局、事業分野、協働形態ごとに分布を比較し、支払いと団体関係は個別記録で確認できます。",
    mechanismBoundary: "協働形態ごとの記録分布。支払い情報は個別記録で確認",
    functionBoundary: "公式の事業分野ごとの記録分布。団体の目的と立場は団体資料で確認",
    departmentBoundary: "主管部局ごとの記録分布。資源関係は契約・助成記録で確認",
    unavailable: "展示データはまだ読み込まれていません。",
    rowsNotActors: "公式協働記録 616 行",
  },
  en: {
    eyebrow: "Okinawa FY2024 · official records",
    fallbackTitle: "Everyday Prefectural Collaboration: 616 Records",
    sourceRows: "Official source rows",
    pdfPages: "Pages in source",
    departments: "Department labels",
    mechanismShare: "Rows under mechanisms 1–4",
    adjacentShare: "Human rights/peace + international rows",
    modesLabel: "Switch aggregation dimension",
    modeDepartment: "Departments",
    modeFunction: "Official functions",
    modeResource: "Mechanisms",
    countSuffix: " rows",
    shareOfRows: "of all 616 source rows",
    sourceLabel: "source label",
    offices: "office source labels",
    functions: "official functions",
    resourceTypes: "mechanisms",
    departmentsMeta: "departments",
    details: "Non-zero cross-cells",
    detailsHint: "Select a summary row to inspect its intersections with other official categories.",
    byResource: "By mechanism",
    byDepartment: "By department",
    byFunction: "By official function",
    originalRows: "Source rows",
    originalPages: "PDF pages",
    exactTrace: "complete compact references",
    noCells: "No non-zero cross-cell is available for this item.",
    boundaryTitle: "Interpretation boundary",
    boundary: "Each row is one collaboration record in the official table. Compare distributions by department, function or mechanism, then open individual records to inspect payments and organizational relationships.",
    mechanismBoundary: "Compare records by collaboration mechanism; inspect individual records for payment details",
    functionBoundary: "Compare records by official function; consult actor profiles for organizational purpose and position",
    departmentBoundary: "Compare records by responsible department; consult contracts and awards for resource relationships",
    unavailable: "Exhibit data has not been loaded.",
    rowsNotActors: "616 official collaboration records",
  },
};

const MODES = [
  { id: "departments", copy: "modeDepartment" },
  { id: "functions", copy: "modeFunction" },
  { id: "resource_types", copy: "modeResource" },
];

const normalizedLang = (lang) => (COPY[lang] ? lang : "zh");
const localized = (value, lang, fallback = "") =>
  value?.[lang] || value?.zh || value?.ja || value?.en || fallback;
const formatOf = (lang) =>
  new Intl.NumberFormat(lang === "ja" ? "ja-JP" : lang === "en" ? "en-US" : "zh-CN");

function rowKey(row, mode) {
  return mode === "departments" ? row.label : row.code;
}
function rowLabel(row, mode) {
  return mode === "departments" ? row.label : row.label || row.code;
}
function metricValue(exhibit, id) {
  const value = exhibit?.headline_metrics?.find((metric) => metric.id === id)?.value;
  return value === undefined || value === null || value === "" ? "—" : value;
}

const withUnit = (value, unit) => (value === "—" ? "—" : `${value}${unit}`);

function SummaryMeta({ row, mode, copy }) {
  const items =
    mode === "departments"
      ? [
          `${row.office_source_label_count} ${copy.offices}`,
          `${row.function_count} ${copy.functions}`,
          `${row.resource_type_count} ${copy.resourceTypes}`,
        ]
      : mode === "functions"
        ? [`${row.department_count} ${copy.departmentsMeta}`, `${row.resource_type_count} ${copy.resourceTypes}`]
        : [`${row.department_count} ${copy.departmentsMeta}`, `${row.function_count} ${copy.functions}`];
  return <span className="oce-row-meta">{items.join(" · ")}</span>;
}

function TraceCell({ cell, copy }) {
  const rowRefs = cell.source_row_refs?.row_numbers_compact || "—";
  const pageRefs = cell.source_row_refs?.pdf_pages_compact || "—";
  return (
    <article className="oce-trace-cell">
      <div className="oce-trace-top">
        <div>
          <strong>{cell.dimension_label}</strong>
          <small>{cell.resource_type_label}</small>
        </div>
        <span className="oce-cell-count">
          {cell.source_row_count}
          {copy.countSuffix}
        </span>
      </div>
      <div className="oce-cell-share">
        <span style={{ "--oce-cell-share": `${cell.share_of_denominator_percent}%` }} />
      </div>
      <details className="oce-trace-refs">
        <summary>{copy.exactTrace}</summary>
        <dl>
          <div>
            <dt>{copy.originalRows}</dt>
            <dd>
              <code>{rowRefs}</code>
            </dd>
          </div>
          <div>
            <dt>{copy.originalPages}</dt>
            <dd>
              <code>{pageRefs}</code>
            </dd>
          </div>
        </dl>
      </details>
    </article>
  );
}

function DetailGroup({ title, cells, totalCount, copy }) {
  if (!cells.length) return null;
  return (
    <section className="oce-detail-group">
      <header>
        <h4>{title}</h4>
        <span>
          {cells.length} · {totalCount}
          {copy.countSuffix}
        </span>
      </header>
      <div className="oce-cell-list">
        {cells.map((cell) => (
          <TraceCell cell={cell} copy={copy} key={`${cell.dimension_code_or_label}-${cell.resource_type_code}`} />
        ))}
      </div>
    </section>
  );
}

export function OfficialCollaborationExhibit({ exhibit, lang = "zh" }) {
  const activeLang = normalizedLang(lang);
  const copy = COPY[activeLang];
  const titleId = useId();
  const formatNumber = useMemo(() => formatOf(activeLang), [activeLang]);
  const [mode, setMode] = useState("departments");
  const rows = exhibit?.summaries?.[mode] || [];
  const [selectedKey, setSelectedKey] = useState("");

  useEffect(() => {
    setSelectedKey(rows.length ? String(rowKey(rows[0], mode)) : "");
  }, [exhibit, mode, rows.length]);

  const selected = rows.find((row) => String(rowKey(row, mode)) === selectedKey);
  const departmentCells = exhibit?.drilldown?.department_by_resource_type_nonzero_cells || [];
  const functionCells = exhibit?.drilldown?.function_by_resource_type_nonzero_cells || [];

  const detailGroups = useMemo(() => {
    if (!selected) return [];
    if (mode === "departments") {
      return [
        {
          id: "resource",
          title: copy.byResource,
          cells: departmentCells.filter((cell) => cell.dimension_code_or_label === selected.label),
        },
      ];
    }
    if (mode === "functions") {
      return [
        {
          id: "resource",
          title: copy.byResource,
          cells: functionCells.filter((cell) => cell.dimension_code_or_label === selected.code),
        },
      ];
    }
    return [
      {
        id: "department",
        title: copy.byDepartment,
        cells: departmentCells.filter((cell) => cell.resource_type_code === selected.code),
      },
      {
        id: "function",
        title: copy.byFunction,
        cells: functionCells.filter((cell) => cell.resource_type_code === selected.code),
      },
    ];
  }, [copy, departmentCells, functionCells, mode, selected]);

  if (!exhibit) return <Unavailable text={copy.unavailable} />;

  const denominator = exhibit.denominator || {};
  const maximum = Math.max(...rows.map((row) => row.source_row_count || 0), 1);
  const modeBoundary =
    mode === "departments"
      ? copy.departmentBoundary
      : mode === "functions"
        ? copy.functionBoundary
        : copy.mechanismBoundary;

  return (
    <section className="oce-exhibit" aria-labelledby={titleId}>
      <ExhibitHeader
        kicker={copy.eyebrow}
        title={localized(exhibit.display?.title, activeLang, copy.fallbackTitle)}
        subtitle={localized(exhibit.display?.subtitle, activeLang)}
        metrics={[
          { value: denominator.value ? formatNumber.format(denominator.value) : "—", label: copy.sourceRows, note: copy.rowsNotActors },
          { value: withUnit(metricValue(exhibit, "M12"), "%"), label: copy.mechanismShare, note: withUnit(metricValue(exhibit, "M11"), copy.countSuffix) },
          { value: withUnit(metricValue(exhibit, "M14"), "%"), label: copy.adjacentShare, note: withUnit(metricValue(exhibit, "M13"), copy.countSuffix) },
        ]}
      />

      <BoundaryNote
        title={copy.boundaryTitle}
        fullText={localized(exhibit.display?.interpretation_limit, activeLang, copy.boundary)}
        helpOnly
      />

      <div className="oce-mode-tabs" role="tablist" aria-label={copy.modesLabel}>
        {MODES.map((item) => (
          <button
            aria-selected={mode === item.id}
            className={mode === item.id ? "active" : ""}
            key={item.id}
            onClick={() => setMode(item.id)}
            role="tab"
            type="button"
          >
            {copy[item.copy]}
            <span>{exhibit.summaries?.[item.id]?.length || 0}</span>
          </button>
        ))}
      </div>

      <div className="oce-explorer">
        <div className="oce-summary-list">
          <p className="oce-mode-boundary">{modeBoundary}</p>
          {rows.map((row) => {
            const key = String(rowKey(row, mode));
            const active = selectedKey === key;
            const width = ((row.source_row_count || 0) / maximum) * 100;
            return (
              <button
                aria-expanded={active}
                className={`oce-summary-row ${active ? "active" : ""}`}
                key={key}
                onClick={() => setSelectedKey(key)}
                type="button"
              >
                <span className="oce-summary-bar" style={{ "--oce-bar": `${width}%` }} />
                <span className="oce-summary-main">
                  <span className="oce-summary-title">
                    {mode !== "departments" && <em>{mode === "functions" ? row.code : `C${row.code}`}</em>}
                    <strong>{rowLabel(row, mode)}</strong>
                  </span>
                  <SummaryMeta row={row} mode={mode} copy={copy} />
                </span>
                <span className="oce-summary-value">
                  <strong>{formatNumber.format(row.source_row_count)}</strong>
                  <small>
                    {copy.countSuffix} · {row.share_of_denominator_percent}%
                  </small>
                </span>
              </button>
            );
          })}
        </div>

        <aside className="oce-details" aria-live="polite">
          <header className="oce-details-header">
            <div>
              <span>{copy.details}</span>
              <h3>{selected ? rowLabel(selected, mode) : "—"}</h3>
            </div>
            {selected && (
              <strong>
                {formatNumber.format(selected.source_row_count)}
                {copy.countSuffix}
              </strong>
            )}
          </header>
          <p className="oce-details-hint">{copy.detailsHint}</p>
          {detailGroups.map((group) => (
            <DetailGroup
              cells={group.cells}
              copy={copy}
              key={group.id}
              title={group.title}
              totalCount={selected?.source_row_count || 0}
            />
          ))}
          {selected && detailGroups.every((group) => !group.cells.length) && (
            <p className="oce-no-cells">{copy.noCells}</p>
          )}
        </aside>
      </div>
    </section>
  );
}

export default OfficialCollaborationExhibit;
