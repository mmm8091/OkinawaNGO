import { useEffect, useId, useMemo, useState } from "react";
import "./OfficialCollaborationExhibit.css";

const COPY = {
  zh: {
    eyebrow: "官方来源总体 · 描述性统计",
    fallbackTitle: "冲绳县 FY2024 NPO 等协作记录总体",
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
    details: "非零交叉单元",
    detailsHint: "选择左侧汇总行，查看它与其他官方分类的交叉记录。",
    byResource: "按协作机制",
    byDepartment: "按部门",
    byFunction: "按事業分野",
    originalRows: "原表行",
    originalPages: "PDF 页",
    exactTrace: "完整压缩引用",
    noCells: "该汇总项没有可显示的非零交叉单元。",
    boundaryTitle: "读取边界",
    boundary:
      "这里的单位始终是官方表中的记录行。协作机制不等于付款，重复出现不等于组织关系，机器排版标签不作为组织展示。",
    mechanismBoundary: "官方协作形态，不代表现金支付",
    functionBoundary: "官方事業分野，不代表组织自身宗旨或立场",
    departmentBoundary: "官方表中的部门可见度，不代表资源依赖",
    unavailable: "展品数据尚未载入。",
    rowsNotActors: "616 条记录，不是 616 个组织",
  },
  ja: {
    eyebrow: "公式資料の全行 · 記述統計",
    fallbackTitle: "沖縄県 FY2024 NPO等との協働実績・全記録",
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
    boundary:
      "単位は常に公式表の記録行です。協働形態は支払いを意味せず、反復掲載は組織関係を意味しません。機械整形した名称を組織として表示しません。",
    mechanismBoundary: "公式の協働形態であり、現金支払いを示しません",
    functionBoundary: "公式の事業分野であり、団体自身の目的や立場を示しません",
    departmentBoundary: "公式表での部局別可視性であり、資源依存を示しません",
    unavailable: "展示データはまだ読み込まれていません。",
    rowsNotActors: "616行であり、616団体ではありません",
  },
  en: {
    eyebrow: "Complete official source · descriptive statistics",
    fallbackTitle: "Okinawa FY2024 official NPO collaboration record universe",
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
    detailsHint:
      "Select a summary row to inspect its intersections with other official categories.",
    byResource: "By mechanism",
    byDepartment: "By department",
    byFunction: "By official function",
    originalRows: "Source rows",
    originalPages: "PDF pages",
    exactTrace: "complete compact references",
    noCells: "No non-zero cross-cell is available for this item.",
    boundaryTitle: "Interpretation boundary",
    boundary:
      "The unit is always an official table row. A mechanism is not a payment, repeated appearance is not an organizational relation, and machine-formatted labels are not presented as organizations.",
    mechanismBoundary: "Official collaboration form, not evidence of cash payment",
    functionBoundary:
      "Official function category, not an organization's own purpose or position",
    departmentBoundary:
      "Visibility under a source department, not evidence of resource dependence",
    unavailable: "Exhibit data has not been loaded.",
    rowsNotActors: "616 records, not 616 organizations",
  },
};

const MODES = [
  { id: "departments", copy: "modeDepartment" },
  { id: "functions", copy: "modeFunction" },
  { id: "resource_types", copy: "modeResource" },
];

function normalizedLang(lang) {
  return Object.hasOwn(COPY, lang) ? lang : "zh";
}

function localized(value, lang, fallback = "") {
  if (value && typeof value === "object") {
    return value[lang] || value.zh || value.ja || value.en || fallback;
  }
  return value || fallback;
}

function numberFormatter(lang) {
  const locale = lang === "ja" ? "ja-JP" : lang === "en" ? "en-US" : "zh-CN";
  return new Intl.NumberFormat(locale);
}

function rowKey(row, mode) {
  if (mode === "departments") return row.label;
  return row.code;
}

function rowLabel(row, mode) {
  if (mode === "departments") return row.label;
  return row.label || row.code;
}

function metricValue(exhibit, id, fallback) {
  return exhibit?.headline_metrics?.find((metric) => metric.id === id)?.value ?? fallback;
}

function SummaryMeta({ row, mode, copy }) {
  if (mode === "departments") {
    return (
      <>
        <span>
          {row.office_source_label_count} {copy.offices}
        </span>
        <span>
          {row.function_count} {copy.functions}
        </span>
        <span>
          {row.resource_type_count} {copy.resourceTypes}
        </span>
      </>
    );
  }
  if (mode === "functions") {
    return (
      <>
        <span>
          {row.department_count} {copy.departmentsMeta}
        </span>
        <span>
          {row.resource_type_count} {copy.resourceTypes}
        </span>
      </>
    );
  }
  return (
    <>
      <span>
        {row.department_count} {copy.departmentsMeta}
      </span>
      <span>
        {row.function_count} {copy.functions}
      </span>
    </>
  );
}

function TraceCell({ cell, copy }) {
  const rowRefs = cell.source_row_refs?.row_numbers_compact || "—";
  const pageRefs = cell.source_row_refs?.pdf_pages_compact || "—";
  return (
    <article className="oce-trace-cell">
      <div className="oce-trace-cell-top">
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
      <dl className="oce-ref-grid">
        <div>
          <dt>{copy.originalRows}</dt>
          <dd>
            <code title={rowRefs}>{rowRefs}</code>
          </dd>
        </div>
        <div>
          <dt>{copy.originalPages}</dt>
          <dd>
            <code title={pageRefs}>{pageRefs}</code>
          </dd>
        </div>
      </dl>
      <p>{copy.exactTrace}</p>
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
          <TraceCell
            cell={cell}
            copy={copy}
            key={`${cell.dimension_code_or_label}-${cell.resource_type_code}`}
          />
        ))}
      </div>
    </section>
  );
}

export function OfficialCollaborationExhibit({ exhibit, lang = "zh" }) {
  const activeLang = normalizedLang(lang);
  const copy = COPY[activeLang];
  const titleId = useId();
  const formatNumber = useMemo(() => numberFormatter(activeLang), [activeLang]);
  const [mode, setMode] = useState("departments");
  const rows = exhibit?.summaries?.[mode] || [];
  const [selectedKey, setSelectedKey] = useState("");

  useEffect(() => {
    setSelectedKey(rows.length ? String(rowKey(rows[0], mode)) : "");
  }, [exhibit, mode, rows.length]);

  const selected = rows.find(
    (row) => String(rowKey(row, mode)) === selectedKey,
  );
  const departmentCells =
    exhibit?.drilldown?.department_by_resource_type_nonzero_cells || [];
  const functionCells =
    exhibit?.drilldown?.function_by_resource_type_nonzero_cells || [];

  const detailGroups = useMemo(() => {
    if (!selected) return [];
    if (mode === "departments") {
      return [
        {
          id: "resource",
          title: copy.byResource,
          cells: departmentCells.filter(
            (cell) => cell.dimension_code_or_label === selected.label,
          ),
        },
      ];
    }
    if (mode === "functions") {
      return [
        {
          id: "resource",
          title: copy.byResource,
          cells: functionCells.filter(
            (cell) => cell.dimension_code_or_label === selected.code,
          ),
        },
      ];
    }
    return [
      {
        id: "department",
        title: copy.byDepartment,
        cells: departmentCells.filter(
          (cell) => cell.resource_type_code === selected.code,
        ),
      },
      {
        id: "function",
        title: copy.byFunction,
        cells: functionCells.filter(
          (cell) => cell.resource_type_code === selected.code,
        ),
      },
    ];
  }, [copy, departmentCells, functionCells, mode, selected]);

  if (!exhibit) {
    return (
      <section className="official-collaboration-exhibit oce-unavailable">
        <p>{copy.unavailable}</p>
      </section>
    );
  }

  const denominator = exhibit.denominator || {};
  const maximum = Math.max(...rows.map((row) => row.source_row_count || 0), 1);
  const modeBoundary =
    mode === "departments"
      ? copy.departmentBoundary
      : mode === "functions"
        ? copy.functionBoundary
        : copy.mechanismBoundary;

  return (
    <section
      className="official-collaboration-exhibit"
      aria-labelledby={titleId}
    >
      <header className="oce-header">
        <div>
          <p className="oce-eyebrow">{copy.eyebrow}</p>
          <h2 id={titleId}>
            {localized(exhibit.display?.title, activeLang, copy.fallbackTitle)}
          </h2>
          <p className="oce-subtitle">
            {localized(exhibit.display?.subtitle, activeLang)}
          </p>
        </div>
        <span className="oce-source-chip">
          {denominator.source_id || "S002"} · FY{denominator.fiscal_year || 2024}
        </span>
      </header>

      <div className="oce-metrics" aria-label={copy.eyebrow}>
        <article className="oce-metric oce-metric-primary">
          <strong>{formatNumber.format(denominator.value || 616)}</strong>
          <span>{copy.sourceRows}</span>
          <small>{copy.rowsNotActors}</small>
        </article>
        <article className="oce-metric">
          <strong>{formatNumber.format(denominator.pdf_pages || 86)}</strong>
          <span>{copy.pdfPages}</span>
          <small>{denominator.source_row_range}</small>
        </article>
        <article className="oce-metric">
          <strong>
            {formatNumber.format(
              exhibit.drilldown?.dimensions?.departments || 15,
            )}
          </strong>
          <span>{copy.departments}</span>
          <small>{copy.sourceLabel}</small>
        </article>
        <article className="oce-metric oce-metric-accent">
          <strong>{metricValue(exhibit, "M12", 76.1)}%</strong>
          <span>{copy.mechanismShare}</span>
          <small>
            {formatNumber.format(metricValue(exhibit, "M11", 469))}
            {copy.countSuffix}
          </small>
        </article>
        <article className="oce-metric oce-metric-accent">
          <strong>{metricValue(exhibit, "M14", 3.1)}%</strong>
          <span>{copy.adjacentShare}</span>
          <small>
            {formatNumber.format(metricValue(exhibit, "M13", 19))}
            {copy.countSuffix}
          </small>
        </article>
      </div>

      <aside className="oce-boundary">
        <strong>{copy.boundaryTitle}</strong>
        <p>
          {localized(
            exhibit.display?.interpretation_limit,
            activeLang,
            copy.boundary,
          )}
        </p>
      </aside>

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
                    {mode !== "departments" && (
                      <em>{mode === "functions" ? row.code : `C${row.code}`}</em>
                    )}
                    <strong>{rowLabel(row, mode)}</strong>
                  </span>
                  <span className="oce-summary-meta">
                    <SummaryMeta row={row} mode={mode} copy={copy} />
                  </span>
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
