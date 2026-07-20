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
    subtitle: "在宫古、石垣、与那国之间切换，下钻逐条观察与原始摘录。",
    unavailable: "R4 展品数据未载入。",
    methodFallback: "计数只表示限定线上语料的可见度。",
    placeTabs: "选择比较地点",
    frames: "框架可见计数",
    allFrames: "全部框架",
    observationsShort: "观察",
    excerptsShort: "摘录",
    observations: "正式观察",
    excerpts: "安全摘录",
    selectedPlace: "当前地点",
    selectedFrame: "当前框架",
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
    unitNote: "同一材料可含多个框架；两列分母不能相加。",
    reviewedRow: "人工复核",
    researchRow: "QA-safe",
    observationUnit: "条正式观察",
    excerptUnit: "条安全摘录",
    scopeNote: "已核 {a} 观察 · {b} 摘录；研究视图追加 {c} 观察 · {d} 摘录。",
  },
  ja: {
    title: "先島三地域：公開資料に現れる問題フレーム",
    subtitle: "宮古・石垣・与那国を切り替え、観察行と原文抜粋を確認できます。",
    unavailable: "R4 展示データを読み込めません。",
    methodFallback: "件数は限定オンライン資料での可視性です。",
    placeTabs: "比較地域を選択",
    frames: "フレーム可視件数",
    allFrames: "全フレーム",
    observationsShort: "観察",
    excerptsShort: "抜粋",
    observations: "正式観察",
    excerpts: "安全抜粋",
    selectedPlace: "選択地域",
    selectedFrame: "選択フレーム",
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
    unitNote: "同じ資料に複数フレームがあり得ます。分母は加算できません。",
    reviewedRow: "人手レビュー済み",
    researchRow: "QA-safe",
    observationUnit: "件の正式観察",
    excerptUnit: "件の安全抜粋",
    scopeNote: "已核 {a} 観察 · {b} 抜粋、研究表示で +{c} 観察 · +{d} 抜粋。",
  },
  en: {
    title: "Three Sakishima localities: frames in public records",
    subtitle: "Switch between Miyako, Ishigaki and Yonaguni, then drill into each observation and excerpt.",
    unavailable: "The R4 exhibit payload is unavailable.",
    methodFallback: "Counts describe visibility in a bounded online corpus only.",
    placeTabs: "Choose a comparison place",
    frames: "Frame visibility counts",
    allFrames: "All frames",
    observationsShort: "obs.",
    excerptsShort: "exc.",
    observations: "Formal observations",
    excerpts: "Safe excerpts",
    selectedPlace: "Selected place",
    selectedFrame: "Selected frame",
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
    unitNote: "One record may carry multiple frames; denominators cannot be added.",
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

  useEffect(() => {
    if (selectedFrame !== "all" && !frameRows.some((row) => row.frame_label === selectedFrame)) {
      setSelectedFrame("all");
    }
  }, [frameRows, selectedFrame]);

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
        {includeResearch
          ? localized(exhibit.display?.interpretation_limit, activeLang, copy.methodFallback)
          : fill(copy.scopeNote, {
              a: reviewedObservations.length,
              b: reviewedExcerpts.length,
              c: (exhibit.observations || []).length - reviewedObservations.length,
              d: (exhibit.excerpts || []).length - reviewedExcerpts.length,
            })}
      </BoundaryNote>

      <ExhibitTabs
        ariaLabel={copy.placeTabs}
        value={selectedPlace}
        onChange={setSelectedPlace}
        items={comparisonPlaces.map((place) => {
          const agg = aggregateByPlace.get(place);
          return {
            id: place,
            label: labelOf(placeById.get(place), activeLang, place),
            note: `${agg?.obs || 0} ${copy.observationsShort} · ${agg?.exc || 0} ${copy.excerptsShort}`,
          };
        })}
      />

      <div className="sf-body">
        <aside className="sf-frame-panel">
          <header>
            <span>{copy.frames}</span>
            <small>{copy.unitNote}</small>
          </header>
          <div className="sf-frame-list">
            <button
              type="button"
              className={selectedFrame === "all" ? "active" : ""}
              onClick={() => setSelectedFrame("all")}
            >
              <span>{copy.allFrames}</span>
              <b>
                <i>{aggregate.obs}</i>
                <i>{aggregate.exc}</i>
              </b>
            </button>
            {frameRows.map((row) => (
              <button
                type="button"
                className={selectedFrame === row.frame_label ? "active" : ""}
                onClick={() => setSelectedFrame(row.frame_label)}
                key={row.frame_label}
              >
                <span>{labelOf(frameById.get(row.frame_label), activeLang, row.frame_label)}</span>
                <b>
                  <i>{row.observation_count}</i>
                  <i>{row.safe_excerpt_count}</i>
                </b>
              </button>
            ))}
          </div>
          <footer>
            <span>{copy.observationsShort}</span>
            <span>{copy.excerptsShort}</span>
          </footer>
        </aside>

        <div className="sf-records">
          <section className="sf-record-column">
            <header>
              <span>
                <FileText size={15} aria-hidden="true" />
                {copy.observations}
              </span>
              <strong>{visibleObservations.length}</strong>
            </header>
            {visibleObservations.map((row) => (
              <ObservationCard
                row={row}
                copy={copy}
                lang={activeLang}
                frameById={frameById}
                onOpenActor={onOpenActor}
                key={row.observation_id}
              />
            ))}
            {!visibleObservations.length && <p className="sf-empty">{copy.noRows}</p>}
          </section>
          <section className="sf-record-column">
            <header>
              <span>
                <Quotes size={15} aria-hidden="true" />
                {copy.excerpts}
              </span>
              <strong>{visibleExcerpts.length}</strong>
            </header>
            {visibleExcerpts.map((row) => (
              <ExcerptCard row={row} copy={copy} lang={activeLang} frameById={frameById} key={row.corpus_source_id} />
            ))}
            {!visibleExcerpts.length && <p className="sf-empty">{copy.noRows}</p>}
          </section>
        </div>
      </div>
    </section>
  );
}
