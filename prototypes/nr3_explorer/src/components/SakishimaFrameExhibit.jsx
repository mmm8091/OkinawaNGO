import { useEffect, useMemo, useState } from "react";
import {
  ArrowSquareOut,
  Buildings,
  FileText,
  Quotes,
  User,
} from "@phosphor-icons/react";
import {
  BoundaryNote,
  ExhibitHeader,
  ExhibitTabs,
  LimitLine,
  MetaGrid,
  RecordCard,
  TierBadge,
  Unavailable,
} from "./exhibit/ExhibitKit.jsx";
import "./exhibit/exhibit.css";
import "./SakishimaFrameExhibit.css";

const COPY = {
  zh: {
    title: "先岛三地：公开材料中的问题框架",
    subtitle: "宫古、石垣、与那国各自在公开材料中主张什么问题。",
    unavailable: "R4 展品数据未载入。",
    methodFallback: "计数只表示限定线上语料的可见度。",
    fullLimit: "查看完整边界",
    placeTabs: "选择比较地点",
    allFrames: "全部框架",
    observations: "正式观察",
    excerpts: "安全摘录",
    allTypes: "全部",
    event: "事件／文件",
    relationBasis: "记录依据",
    review: "复核状态",
    locator: "定位",
    speaker: "说话者／材料所有者",
    sourceType: "来源类型",
    evidence: "证据等级",
    interpretationLimit: "解释边界",
    relationshipLimit: "关系边界",
    paraphraseZh: "中文释义",
    originalExcerpt: "原文短摘",
    openSource: "打开来源",
    noRows: "这一筛选下没有记录。",
    registryActor: "登记组织",
    institution: "行政／制度机构",
    namedPerson: "具名个人",
    anonymousEvent: "匿名事件话语",
    provisionalCollective: "一次性／待核集体",
    actorHint: "打开组织页",
    unitNote: "同一材料可含多个框架；两种计数不能相加。",
    reviewedRow: "人工复核",
    researchRow: "QA-safe",
    observationUnit: "条正式观察",
    excerptUnit: "条安全摘录",
    scopeNote: "已核 {a} 观察 · {b} 摘录；研究视图追加 {c} 观察 · {d} 摘录。",
  },
  ja: {
    title: "先島三地域：公開資料に現れる問題フレーム",
    subtitle: "宮古・石垣・与那国それぞれが公開資料で何を主張しているか。",
    unavailable: "R4 展示データを読み込めません。",
    methodFallback: "件数は限定オンライン資料での可視性です。",
    fullLimit: "完全な境界を表示",
    placeTabs: "比較地域を選択",
    allFrames: "全フレーム",
    observations: "正式観察",
    excerpts: "安全抜粋",
    allTypes: "すべて",
    event: "出来事／文書",
    relationBasis: "記録根拠",
    review: "レビュー状態",
    locator: "所在",
    speaker: "発話者／資料主体",
    sourceType: "資料種別",
    evidence: "証拠水準",
    interpretationLimit: "解釈上の境界",
    relationshipLimit: "関係上の境界",
    paraphraseZh: "中国語要約",
    originalExcerpt: "原文短抜粋",
    openSource: "出典を開く",
    noRows: "この条件に該当する記録はありません。",
    registryActor: "登録団体",
    institution: "行政・制度機関",
    namedPerson: "実名個人",
    anonymousEvent: "匿名のイベント発話",
    provisionalCollective: "単発・要確認の集団",
    actorHint: "団体ページを開く",
    unitNote: "同じ資料に複数フレームがあり得ます。二つの計数は加算できません。",
    reviewedRow: "人手レビュー済み",
    researchRow: "QA-safe",
    observationUnit: "件の正式観察",
    excerptUnit: "件の安全抜粋",
    scopeNote: "已核 {a} 観察 · {b} 抜粋、研究表示で +{c} 観察 · +{d} 抜粋。",
  },
  en: {
    title: "Three Sakishima localities: frames in public records",
    subtitle: "What Miyako, Ishigaki and Yonaguni each raise in public records.",
    unavailable: "The R4 exhibit payload is unavailable.",
    methodFallback: "Counts describe visibility in a bounded online corpus only.",
    fullLimit: "Show full boundary",
    placeTabs: "Choose a comparison place",
    allFrames: "All frames",
    observations: "Formal observations",
    excerpts: "Safe excerpts",
    allTypes: "All",
    event: "Event / document",
    relationBasis: "Recorded basis",
    review: "Review status",
    locator: "Locator",
    speaker: "Speaker / record owner",
    sourceType: "Source type",
    evidence: "Evidence level",
    interpretationLimit: "Interpretation limit",
    relationshipLimit: "Relationship limit",
    paraphraseZh: "Project paraphrase (zh)",
    originalExcerpt: "Short source excerpt",
    openSource: "Open source",
    noRows: "No records match this selection.",
    registryActor: "Registry actor",
    institution: "Administrative / institutional",
    namedPerson: "Named individual",
    anonymousEvent: "Anonymous event utterance",
    provisionalCollective: "One-off / provisional collective",
    actorHint: "Open actor page",
    unitNote: "One record may carry multiple frames; the two counts cannot be added.",
    reviewedRow: "Human reviewed",
    researchRow: "QA-safe",
    observationUnit: "formal observations",
    excerptUnit: "safe excerpts",
    scopeNote: "Reviewed: {a} observations · {b} excerpts. Research adds {c} observations · {d} excerpts.",
  },
};

const ENTITY_META = {
  registry_actor: { copy: "registryActor", Icon: User },
  institution: { copy: "institution", Icon: Buildings },
  named_person: { copy: "namedPerson", Icon: User },
  anonymous_event_utterance: { copy: "anonymousEvent", Icon: Quotes },
  provisional_event_collective: { copy: "provisionalCollective", Icon: Quotes },
};

const DEFAULT_PLACES = ["Miyako", "Ishigaki", "Yonaguni"];
const normalizeLang = (lang) => (COPY[lang] ? lang : "zh");
const localized = (value, lang, fallback = "") =>
  value?.[lang] || value?.zh || value?.ja || value?.en || fallback;
const labelOf = (row, lang, fallback) =>
  row?.[`display_label_${lang}`] || row?.display_label || fallback;
const fill = (template, values) =>
  Object.entries(values).reduce(
    (result, [key, value]) => result.replace(`{${key}}`, String(value)),
    template,
  );

function EntityBadge({ kind, copy }) {
  const meta = ENTITY_META[kind] || { copy: kind, Icon: Quotes };
  return (
    <span className="sf-entity">
      <meta.Icon size={12} aria-hidden="true" />
      {copy[meta.copy] || kind}
    </span>
  );
}

function SubjectName({ subject, copy, onOpenActor }) {
  if (subject.actor_id && typeof onOpenActor === "function") {
    return (
      <button
        className="sf-actor-link"
        type="button"
        title={`${copy.actorHint} · ${subject.actor_id}`}
        onClick={(event) => {
          event.preventDefault();
          event.stopPropagation();
          onOpenActor(subject.actor_id);
        }}
      >
        {subject.entity_name}
        <small>{subject.actor_id}</small>
      </button>
    );
  }
  return (
    <strong className="sf-subject-name">
      {subject.entity_name}
      <small>{subject.entity_id}</small>
    </strong>
  );
}

function SourceLink({ source, copy }) {
  return (
    <a className="sf-source-link" href={source.url} target="_blank" rel="noreferrer">
      <b>{source.corpus_source_id}</b> {source.title} <ArrowSquareOut size={13} aria-hidden="true" />
    </a>
  );
}

function ObservationCard({ row, copy, lang, frameById, onOpenActor }) {
  return (
    <RecordCard
      id={row.observation_id}
      title={
        <>
          <SubjectName subject={row.subject} copy={copy} onOpenActor={onOpenActor} />{" "}
          <EntityBadge kind={row.subject.entity_kind} copy={copy} />
        </>
      }
      badges={
        <>
          <span className="sf-type obs">{copy.observations}</span>
          <span className="sf-frame">
            {labelOf(frameById.get(row.frame.label), lang, row.frame.label)}
          </span>
          <TierBadge
            tier={row.display_tier}
            labels={{ reviewed: copy.reviewedRow, research: copy.researchRow }}
          />
        </>
      }
    >
      <MetaGrid
        cols={4}
        items={[
          { label: copy.event, value: `${row.event_or_document} · ${row.event_year}` },
          { label: copy.relationBasis, value: row.relation_basis },
          { label: copy.review, value: `${row.evidence.review_status} · ${row.evidence.evidence_level}` },
          { label: copy.locator, value: row.evidence.source_locator_summary },
        ]}
      />
      <div className="sf-source-stack">
        {row.evidence.source_records.map((source) => (
          <SourceLink source={source} copy={copy} key={`${row.observation_id}-${source.corpus_source_id}`} />
        ))}
      </div>
      <LimitLine label={copy.interpretationLimit} text={row.interpretation_limit} />
      <LimitLine label={copy.relationshipLimit} text={row.relationship_limit} />
    </RecordCard>
  );
}

function ExcerptCard({ row, copy, lang, frameById }) {
  return (
    <RecordCard
      id={row.corpus_source_id}
      title={row.title}
      badges={
        <>
          <span className="sf-type exc">{copy.excerpts}</span>
          <span className="sf-frame">
            {row.frame_labels.map((frame) => labelOf(frameById.get(frame), lang, frame)).join(" · ")}
          </span>
          <TierBadge
            tier={row.display_tier}
            labels={{ reviewed: copy.reviewedRow, research: copy.researchRow }}
          />
        </>
      }
    >
      <blockquote className="sf-quote">
        <small>{copy.originalExcerpt}</small>
        {row.excerpt_short || "—"}
      </blockquote>
      <MetaGrid
        cols={4}
        items={[
          { label: copy.speaker, value: row.speaker_or_owner },
          { label: copy.sourceType, value: row.source_type },
          { label: copy.evidence, value: `${row.evidence_level} · ${row.review_status}` },
          { label: copy.locator, value: row.locator },
        ]}
      />
      {row.paraphrase_zh && (
        <p className="sf-paraphrase">
          <small>{copy.paraphraseZh}</small>
          {row.paraphrase_zh}
        </p>
      )}
      <SourceLink source={row} copy={copy} />
      <LimitLine label={copy.interpretationLimit} text={row.interpretation_limit} />
    </RecordCard>
  );
}

function buildAggregate(place, observations, excerpts) {
  const placeObs = observations.filter((row) => row.place === place);
  const placeExc = excerpts.filter((row) => row.place === place);
  const obsFrames = new Map();
  const excFrames = new Map();
  placeObs.forEach((row) => {
    const ids = obsFrames.get(row.frame.label) || [];
    ids.push(row.observation_id);
    obsFrames.set(row.frame.label, ids);
  });
  placeExc.forEach((row) => {
    row.frame_labels.forEach((frameLabel) => {
      const ids = excFrames.get(frameLabel) || [];
      ids.push(row.corpus_source_id);
      excFrames.set(frameLabel, ids);
    });
  });
  return { obs: placeObs.length, exc: placeExc.length, obsFrames, excFrames };
}

function FrameBars({ rows, frameById, lang, selected, onSelect, copy }) {
  const max = Math.max(...rows.map((row) => row.observation_count + row.safe_excerpt_count), 1);
  return (
    <div className="sf-frame-bars" role="group" aria-label={copy.allFrames}>
      <button
        type="button"
        className={`sf-frame-bar all ${selected === "all" ? "active" : ""}`}
        onClick={() => onSelect("all")}
      >
        <span className="sf-frame-bar-label">{copy.allFrames}</span>
        <span className="sf-frame-bar-track">
          <i className="obs" style={{ width: "100%" }} />
        </span>
        <span className="sf-frame-bar-count">
          {rows.reduce((sum, row) => sum + row.observation_count, 0)}·
          {rows.reduce((sum, row) => sum + row.safe_excerpt_count, 0)}
        </span>
      </button>
      {rows.map((row) => {
        const total = row.observation_count + row.safe_excerpt_count;
        return (
          <button
            type="button"
            key={row.frame_label}
            className={`sf-frame-bar ${selected === row.frame_label ? "active" : ""}`}
            onClick={() => onSelect(selected === row.frame_label ? "all" : row.frame_label)}
          >
            <span className="sf-frame-bar-label">
              {labelOf(frameById.get(row.frame_label), lang, row.frame_label)}
            </span>
            <span className="sf-frame-bar-track">
              <i className="obs" style={{ width: `${(row.observation_count / max) * 100}%` }} />
              <i className="exc" style={{ width: `${(row.safe_excerpt_count / max) * 100}%` }} />
            </span>
            <span className="sf-frame-bar-count">
              {row.observation_count}·{row.safe_excerpt_count}
            </span>
          </button>
        );
      })}
      <p className="sf-frame-bars-legend">
        <span>
          <i className="obs" /> {copy.observations}
        </span>
        <span>
          <i className="exc" /> {copy.excerpts}
        </span>
        <em>{copy.unitNote}</em>
      </p>
    </div>
  );
}

export function SakishimaFrameExhibit({ exhibit, lang = "zh", onOpenActor, layer = "demo" }) {
  const activeLang = normalizeLang(lang);
  const copy = COPY[activeLang];
  const comparisonPlaces = exhibit?.comparison_places || DEFAULT_PLACES;
  const includeResearch = layer === "research";

  const eligibleObservations = useMemo(
    () => (exhibit?.observations || []).filter((row) => includeResearch || row.display_tier === "reviewed"),
    [exhibit, includeResearch],
  );
  const eligibleExcerpts = useMemo(
    () => (exhibit?.excerpts || []).filter((row) => includeResearch || row.display_tier === "reviewed"),
    [exhibit, includeResearch],
  );
  const reviewedObservations = useMemo(
    () => (exhibit?.observations || []).filter((row) => row.display_tier === "reviewed"),
    [exhibit],
  );
  const reviewedExcerpts = useMemo(
    () => (exhibit?.excerpts || []).filter((row) => row.display_tier === "reviewed"),
    [exhibit],
  );

  const placeById = useMemo(
    () => new Map((exhibit?.place_vocabulary || []).map((row) => [row.id, row])),
    [exhibit],
  );
  const frameById = useMemo(
    () => new Map((exhibit?.frame_vocabulary || []).map((row) => [row.id, row])),
    [exhibit],
  );
  const aggregateByPlace = useMemo(
    () =>
      new Map(
        comparisonPlaces.map((place) => [
          place,
          buildAggregate(place, eligibleObservations, eligibleExcerpts),
        ]),
      ),
    [comparisonPlaces, eligibleExcerpts, eligibleObservations],
  );

  const [selectedPlace, setSelectedPlace] = useState(comparisonPlaces[0]);
  const [selectedFrame, setSelectedFrame] = useState("all");
  const [typeFilter, setTypeFilter] = useState("all");

  useEffect(() => {
    if (!comparisonPlaces.includes(selectedPlace)) setSelectedPlace(comparisonPlaces[0]);
  }, [comparisonPlaces, selectedPlace]);
  useEffect(() => setSelectedFrame("all"), [selectedPlace]);

  const aggregate = aggregateByPlace.get(selectedPlace);

  const frameRows = useMemo(() => {
    if (!aggregate) return [];
    const labels = [...new Set([...aggregate.obsFrames.keys(), ...aggregate.excFrames.keys()])].sort(
      (a, b) =>
        labelOf(frameById.get(a), activeLang, a).localeCompare(
          labelOf(frameById.get(b), activeLang, b),
          activeLang === "zh" ? "zh-CN" : activeLang,
        ),
    );
    return labels.map((frameLabel) => ({
      frame_label: frameLabel,
      observation_count: aggregate.obsFrames.get(frameLabel)?.length || 0,
      safe_excerpt_count: aggregate.excFrames.get(frameLabel)?.length || 0,
      observation_ids: aggregate.obsFrames.get(frameLabel) || [],
      corpus_source_ids: aggregate.excFrames.get(frameLabel) || [],
    }));
  }, [activeLang, aggregate, frameById]);

  const selectedFrameRow = frameRows.find((row) => row.frame_label === selectedFrame);

  const visibleObservations = useMemo(() => {
    const placeRows = eligibleObservations.filter((row) => row.place === selectedPlace);
    if (!selectedFrameRow) return placeRows;
    const ids = new Set(selectedFrameRow.observation_ids);
    return placeRows.filter((row) => ids.has(row.observation_id));
  }, [eligibleObservations, selectedFrameRow, selectedPlace]);

  const visibleExcerpts = useMemo(() => {
    const placeRows = eligibleExcerpts.filter((row) => row.place === selectedPlace);
    if (!selectedFrameRow) return placeRows;
    const ids = new Set(selectedFrameRow.corpus_source_ids);
    return placeRows.filter((row) => ids.has(row.corpus_source_id));
  }, [eligibleExcerpts, selectedFrameRow, selectedPlace]);

  if (!exhibit || !aggregate) return <Unavailable text={copy.unavailable} />;

  const listItems = [
    ...visibleObservations.map((row) => ({ kind: "obs", row })),
    ...visibleExcerpts.map((row) => ({ kind: "exc", row })),
  ].filter((item) => typeFilter === "all" || item.kind === typeFilter);

  return (
    <section className="sf-exhibit">
      <ExhibitHeader
        kicker={exhibit.catalog_id}
        title={localized(exhibit.display?.title, activeLang, copy.title)}
        subtitle={localized(exhibit.display?.subtitle, activeLang, copy.subtitle)}
        metrics={[
          { value: eligibleObservations.length, label: copy.observationUnit },
          { value: eligibleExcerpts.length, label: copy.excerptUnit },
        ]}
      />

      <BoundaryNote>
        {fill(copy.scopeNote, {
          a: reviewedObservations.length,
          b: reviewedExcerpts.length,
          c: (exhibit.observations || []).length - reviewedObservations.length,
          d: (exhibit.excerpts || []).length - reviewedExcerpts.length,
        })}
        {" · "}
        {copy.methodFallback}
        {includeResearch && exhibit.display?.interpretation_limit && (
          <details className="sf-full-limit">
            <summary>{copy.fullLimit}</summary>
            <p>{localized(exhibit.display.interpretation_limit, activeLang)}</p>
          </details>
        )}
      </BoundaryNote>

      <div className="sf-filter-band">
        <ExhibitTabs
          ariaLabel={copy.placeTabs}
          value={selectedPlace}
          onChange={setSelectedPlace}
          items={comparisonPlaces.map((place) => {
            const agg = aggregateByPlace.get(place);
            return {
              id: place,
              label: labelOf(placeById.get(place), activeLang, place),
              note: `${agg?.obs || 0} ${copy.observations} · ${agg?.exc || 0} ${copy.excerpts}`,
            };
          })}
        />
        <FrameBars
          rows={frameRows}
          frameById={frameById}
          lang={activeLang}
          selected={selectedFrame}
          onSelect={setSelectedFrame}
          copy={copy}
        />
      </div>

      <div className="sf-type-tabs" role="tablist" aria-label={copy.allTypes}>
        {[
          { id: "all", label: `${copy.allTypes} ${visibleObservations.length + visibleExcerpts.length}` },
          { id: "obs", label: `${copy.observations} ${visibleObservations.length}` },
          { id: "exc", label: `${copy.excerpts} ${visibleExcerpts.length}` },
        ].map((item) => (
          <button
            key={item.id}
            type="button"
            role="tab"
            aria-selected={typeFilter === item.id}
            className={typeFilter === item.id ? "active" : ""}
            onClick={() => setTypeFilter(item.id)}
          >
            {item.label}
          </button>
        ))}
      </div>

      <div className="sf-record-list">
        {listItems.map((item) =>
          item.kind === "obs" ? (
            <ObservationCard
              row={item.row}
              copy={copy}
              lang={activeLang}
              frameById={frameById}
              onOpenActor={onOpenActor}
              key={`obs-${item.row.observation_id}`}
            />
          ) : (
            <ExcerptCard
              row={item.row}
              copy={copy}
              lang={activeLang}
              frameById={frameById}
              key={`exc-${item.row.corpus_source_id}`}
            />
          ),
        )}
        {!listItems.length && <p className="sf-empty">{copy.noRows}</p>}
      </div>
    </section>
  );
}
