import { useEffect, useId, useMemo, useState } from "react";
import {
  ArrowSquareOut,
  Buildings,
  FileText,
  MapPin,
  Quotes,
  User,
} from "@phosphor-icons/react";
import "./SakishimaFrameExhibit.css";

const COPY = {
  zh: {
    title: "先岛三地：公开材料中的问题框架",
    subtitle: "在宫古、石垣、与那国之间切换，并下钻到逐条观察、原始摘录与定位信息。",
    unavailable: "R4 展品数据未载入。",
    method: "读图边界",
    methodFallback:
      "计数只表示限定线上语料中的可见度，不代表组织数量、居民态度或动员强度。",
    placeTabs: "选择比较地点",
    frames: "框架可见计数",
    allFrames: "全部框架",
    observationsShort: "观察",
    excerptsShort: "摘录",
    observations: "正式观察",
    excerpts: "安全摘录",
    selectedPlace: "当前地点",
    selectedFrame: "当前框架",
    source: "来源",
    sources: "来源",
    locator: "定位",
    speaker: "说话者／材料所有者",
    sourceType: "来源类型",
    review: "复核状态",
    evidence: "证据等级",
    event: "事件／文件",
    relationBasis: "记录依据",
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
    unitNote: "同一材料可含多个框架；两列分母不同，不能相加。",
    reviewedScope:
      "已核视图有9条人工复核观察：8条进入三地比较，另1条只作先岛整体语境；并显示5条人工复核摘录。切换“研究”可查看另10条观察和19条 QA-safe 摘录。",
    reviewedRow: "人工复核",
    researchRow: "QA-safe 研究层",
    observationUnit: "条正式观察",
    excerptUnit: "条安全摘录",
  },
  ja: {
    title: "先島三地域：公開資料に現れる問題フレーム",
    subtitle: "宮古・石垣・与那国を切り替え、観察行、原文抜粋、所在情報まで確認できます。",
    unavailable: "R4 展示データを読み込めません。",
    method: "解釈上の境界",
    methodFallback:
      "件数は限定オンライン資料での可視性であり、団体数、住民意識、動員強度ではありません。",
    placeTabs: "比較地域を選択",
    frames: "フレーム可視件数",
    allFrames: "全フレーム",
    observationsShort: "観察",
    excerptsShort: "抜粋",
    observations: "正式観察",
    excerpts: "安全抜粋",
    selectedPlace: "選択地域",
    selectedFrame: "選択フレーム",
    source: "出典",
    sources: "出典",
    locator: "所在",
    speaker: "発話者／資料主体",
    sourceType: "資料種別",
    review: "レビュー状態",
    evidence: "証拠水準",
    event: "出来事／文書",
    relationBasis: "記録根拠",
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
    unitNote: "同じ資料に複数フレームがあり得ます。二つの分母は加算できません。",
    reviewedScope:
      "確認済み表示の人手レビュー済み観察は9件で、8件を三地域比較に用い、1件は先島全域の文脈としてのみ扱います。人手レビュー済み抜粋は5件です。「研究」に切り替えると、追加の観察10件とQA-safe抜粋19件を確認できます。",
    reviewedRow: "人手レビュー済み",
    researchRow: "QA-safe 研究層",
    observationUnit: "件の正式観察",
    excerptUnit: "件の安全抜粋",
  },
  en: {
    title: "Three Sakishima localities: frames visible in public records",
    subtitle:
      "Switch between Miyako, Ishigaki, and Yonaguni, then inspect each observation, excerpt, and source locator.",
    unavailable: "The R4 exhibit payload is unavailable.",
    method: "Reading boundary",
    methodFallback:
      "Counts describe visibility in a bounded online corpus, not organization totals, resident attitudes, or mobilization intensity.",
    placeTabs: "Choose a comparison place",
    frames: "Frame visibility counts",
    allFrames: "All frames",
    observationsShort: "observations",
    excerptsShort: "excerpts",
    observations: "Formal observations",
    excerpts: "Safe excerpts",
    selectedPlace: "Selected place",
    selectedFrame: "Selected frame",
    source: "Source",
    sources: "Sources",
    locator: "Locator",
    speaker: "Speaker / record owner",
    sourceType: "Source type",
    review: "Review status",
    evidence: "Evidence level",
    event: "Event / document",
    relationBasis: "Recorded basis",
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
    unitNote:
      "One record may carry multiple frames. The two denominators cannot be added.",
    reviewedScope:
      "The reviewed view contains 9 human-reviewed observations: 8 enter the three-place comparison and 1 remains Sakishima-wide context, alongside 5 human-reviewed excerpts. Switch to Research for 10 additional observations and 19 QA-safe excerpts.",
    reviewedRow: "Human reviewed",
    researchRow: "QA-safe research layer",
    observationUnit: "formal observations",
    excerptUnit: "safe excerpts",
  },
};

const ENTITY_COPY_KEY = {
  registry_actor: "registryActor",
  institution: "institution",
  named_person: "namedPerson",
  anonymous_event_utterance: "anonymousEvent",
  provisional_event_collective: "provisionalCollective",
};

const DEFAULT_COMPARISON_PLACES = ["Miyako", "Ishigaki", "Yonaguni"];

const normalizeLang = (lang) =>
  ["zh", "ja", "en"].includes(lang) ? lang : "zh";

function displayLabel(row, lang, fallback) {
  return (
    row?.[`display_label_${lang}`] ||
    row?.display_label ||
    fallback
  );
}

function localizedDisplay(value, lang, fallback) {
  return value?.[lang] || value?.zh || value?.ja || value?.en || fallback;
}

function buildDisplayAggregate(place, observations, excerpts) {
  const placeObservations = observations.filter((row) => row.place === place);
  const placeExcerpts = excerpts.filter((row) => row.place === place);
  const observationFrames = new Map();
  const excerptFrames = new Map();
  placeObservations.forEach((row) => {
    const ids = observationFrames.get(row.frame.label) || [];
    ids.push(row.observation_id);
    observationFrames.set(row.frame.label, ids);
  });
  placeExcerpts.forEach((row) => {
    row.frame_labels.forEach((frameLabel) => {
      const ids = excerptFrames.get(frameLabel) || [];
      ids.push(row.corpus_source_id);
      excerptFrames.set(frameLabel, ids);
    });
  });
  return {
    place,
    formal_observation_denominator: placeObservations.length,
    safe_excerpt_denominator: placeExcerpts.length,
    observation_frame_visibility: [...observationFrames.entries()].map(
      ([frame_label, observation_ids]) => ({
        frame_label,
        observation_count: observation_ids.length,
        observation_ids,
      }),
    ),
    excerpt_frame_visibility: [...excerptFrames.entries()].map(
      ([frame_label, corpus_source_ids]) => ({
        frame_label,
        safe_excerpt_count: corpus_source_ids.length,
        corpus_source_ids,
      }),
    ),
  };
}

function EntityBadge({ subject, copy }) {
  const kind = subject.entity_kind;
  const Icon =
    kind === "registry_actor"
      ? User
      : kind === "institution"
        ? Buildings
        : kind === "named_person"
          ? User
          : Quotes;
  return (
    <span className={`sf-entity-badge ${kind}`}>
      <Icon size={13} aria-hidden="true" />
      {copy[ENTITY_COPY_KEY[kind]] || kind}
    </span>
  );
}

function SubjectName({ subject, copy, onOpenActor }) {
  const actorId = subject.actor_id;
  if (actorId && typeof onOpenActor === "function") {
    return (
      <button
        className="sf-actor-link"
        type="button"
        title={`${copy.actorHint} · ${actorId}`}
        onClick={(event) => {
          event.preventDefault();
          event.stopPropagation();
          onOpenActor(actorId);
        }}
      >
        {subject.entity_name}
        <span>{actorId}</span>
      </button>
    );
  }
  return (
    <strong className="sf-subject-name">
      {subject.entity_name}
      <span>{subject.entity_id}</span>
    </strong>
  );
}

function SourceLink({ source, copy }) {
  return (
    <a
      className="sf-source-link"
      href={source.url}
      target="_blank"
      rel="noreferrer"
    >
      <span>
        <b>{source.corpus_source_id}</b>
        {source.title}
      </span>
      <span>
        {copy.openSource}
        <ArrowSquareOut size={14} aria-hidden="true" />
      </span>
    </a>
  );
}

function ObservationCard({
  row,
  copy,
  lang,
  frameById,
  onOpenActor,
}) {
  return (
    <details className="sf-record sf-observation-record">
      <summary>
        <span className="sf-record-id">{row.observation_id}</span>
        <span className="sf-record-subject">
          <SubjectName
            subject={row.subject}
            copy={copy}
            onOpenActor={onOpenActor}
          />
          <EntityBadge subject={row.subject} copy={copy} />
        </span>
        <span className="sf-record-frame">
          {displayLabel(
            frameById.get(row.frame.label),
            lang,
            row.frame.label,
          )}
          <em className={`sf-tier-chip ${row.display_tier}`}>
            {row.display_tier === "reviewed"
              ? copy.reviewedRow
              : copy.researchRow}
          </em>
        </span>
      </summary>
      <div className="sf-record-body">
        <dl className="sf-record-meta">
          <div>
            <dt>{copy.event}</dt>
            <dd>
              {row.event_or_document} · {row.event_year}
            </dd>
          </div>
          <div>
            <dt>{copy.relationBasis}</dt>
            <dd>{row.relation_basis}</dd>
          </div>
          <div>
            <dt>{copy.review}</dt>
            <dd>
              {row.evidence.review_status} · {row.evidence.evidence_level}
            </dd>
          </div>
          <div>
            <dt>{copy.locator}</dt>
            <dd>{row.evidence.source_locator_summary}</dd>
          </div>
        </dl>
        <div className="sf-source-stack">
          {row.evidence.source_records.map((source) => (
            <SourceLink
              source={source}
              copy={copy}
              key={`${row.observation_id}-${source.corpus_source_id}`}
            />
          ))}
        </div>
        <div className="sf-limit-grid">
          <p>
            <b>{copy.interpretationLimit}</b>
            {row.interpretation_limit}
          </p>
          <p>
            <b>{copy.relationshipLimit}</b>
            {row.relationship_limit}
          </p>
        </div>
      </div>
    </details>
  );
}

function ExcerptCard({ row, copy, lang, frameById }) {
  return (
    <details className="sf-record sf-excerpt-record">
      <summary>
        <span className="sf-record-id">{row.corpus_source_id}</span>
        <span className="sf-excerpt-title">{row.title}</span>
        <span className="sf-record-frame">
          {row.frame_labels
            .map((frame) =>
              displayLabel(frameById.get(frame), lang, frame),
            )
            .join(" · ")}
          <em className={`sf-tier-chip ${row.display_tier}`}>
            {row.display_tier === "reviewed"
              ? copy.reviewedRow
              : copy.researchRow}
          </em>
        </span>
      </summary>
      <div className="sf-record-body">
        <blockquote>
          <span>{copy.originalExcerpt}</span>
          {row.excerpt_short || "—"}
        </blockquote>
        <dl className="sf-record-meta">
          <div>
            <dt>{copy.speaker}</dt>
            <dd>{row.speaker_or_owner}</dd>
          </div>
          <div>
            <dt>{copy.sourceType}</dt>
            <dd>{row.source_type}</dd>
          </div>
          <div>
            <dt>{copy.evidence}</dt>
            <dd>
              {row.evidence_level} · {row.review_status}
            </dd>
          </div>
          <div>
            <dt>{copy.locator}</dt>
            <dd>{row.locator}</dd>
          </div>
          <div className="sf-meta-wide">
            <dt>{copy.paraphraseZh}</dt>
            <dd>{row.paraphrase_zh || "—"}</dd>
          </div>
        </dl>
        <SourceLink source={row} copy={copy} />
        <p className="sf-inline-limit">
          <b>{copy.interpretationLimit}</b>
          {row.interpretation_limit}
        </p>
      </div>
    </details>
  );
}

export function SakishimaFrameExhibit({
  exhibit,
  lang = "zh",
  onOpenActor,
  layer = "demo",
}) {
  const activeLang = normalizeLang(lang);
  const copy = COPY[activeLang];
  const titleId = useId();
  const comparisonPlaces =
    exhibit?.comparison_places || DEFAULT_COMPARISON_PLACES;
  const includeResearch = layer === "research";
  const eligibleObservations = useMemo(
    () =>
      (exhibit?.observations || []).filter(
        (row) => includeResearch || row.display_tier === "reviewed",
      ),
    [exhibit, includeResearch],
  );
  const eligibleExcerpts = useMemo(
    () =>
      (exhibit?.excerpts || []).filter(
        (row) => includeResearch || row.display_tier === "reviewed",
      ),
    [exhibit, includeResearch],
  );
  const aggregateByPlace = useMemo(
    () =>
      new Map(
        comparisonPlaces.map((place) => [
          place,
          buildDisplayAggregate(
            place,
            eligibleObservations,
            eligibleExcerpts,
          ),
        ]),
      ),
    [comparisonPlaces, eligibleExcerpts, eligibleObservations],
  );
  const placeById = useMemo(
    () =>
      new Map(
        (exhibit?.place_vocabulary || []).map((row) => [row.id, row]),
      ),
    [exhibit],
  );
  const frameById = useMemo(
    () =>
      new Map(
        (exhibit?.frame_vocabulary || []).map((row) => [row.id, row]),
      ),
    [exhibit],
  );
  const [selectedPlace, setSelectedPlace] = useState(comparisonPlaces[0]);
  const [selectedFrame, setSelectedFrame] = useState("all");

  useEffect(() => {
    if (!comparisonPlaces.includes(selectedPlace)) {
      setSelectedPlace(comparisonPlaces[0]);
    }
  }, [comparisonPlaces, selectedPlace]);

  useEffect(() => {
    setSelectedFrame("all");
  }, [selectedPlace]);

  const placeAggregate = aggregateByPlace.get(selectedPlace);

  const frameRows = useMemo(() => {
    if (!placeAggregate) return [];
    const observationsByFrame = new Map(
      placeAggregate.observation_frame_visibility.map((row) => [
        row.frame_label,
        row,
      ]),
    );
    const excerptsByFrame = new Map(
      placeAggregate.excerpt_frame_visibility.map((row) => [
        row.frame_label,
        row,
      ]),
    );
    const labels = [
      ...new Set([
        ...observationsByFrame.keys(),
        ...excerptsByFrame.keys(),
      ]),
    ].sort((a, b) =>
      displayLabel(frameById.get(a), activeLang, a).localeCompare(
        displayLabel(frameById.get(b), activeLang, b),
        activeLang === "zh" ? "zh-CN" : activeLang,
      ),
    );
    return labels.map((frameLabel) => ({
      frame_label: frameLabel,
      observation_count:
        observationsByFrame.get(frameLabel)?.observation_count || 0,
      safe_excerpt_count:
        excerptsByFrame.get(frameLabel)?.safe_excerpt_count || 0,
      observation_ids:
        observationsByFrame.get(frameLabel)?.observation_ids || [],
      corpus_source_ids:
        excerptsByFrame.get(frameLabel)?.corpus_source_ids || [],
    }));
  }, [activeLang, frameById, placeAggregate]);

  const selectedFrameRow = frameRows.find(
    (row) => row.frame_label === selectedFrame,
  );

  useEffect(() => {
    if (
      selectedFrame !== "all" &&
      !frameRows.some((row) => row.frame_label === selectedFrame)
    ) {
      setSelectedFrame("all");
    }
  }, [frameRows, selectedFrame]);

  const visibleObservations = useMemo(() => {
    const placeRows = eligibleObservations.filter(
      (row) => row.place === selectedPlace,
    );
    if (!selectedFrameRow) return placeRows;
    const selectedIds = new Set(selectedFrameRow.observation_ids);
    return placeRows.filter((row) => selectedIds.has(row.observation_id));
  }, [eligibleObservations, selectedFrameRow, selectedPlace]);

  const visibleExcerpts = useMemo(() => {
    const placeRows = eligibleExcerpts.filter(
      (row) => row.place === selectedPlace,
    );
    if (!selectedFrameRow) return placeRows;
    const selectedIds = new Set(selectedFrameRow.corpus_source_ids);
    return placeRows.filter((row) => selectedIds.has(row.corpus_source_id));
  }, [eligibleExcerpts, selectedFrameRow, selectedPlace]);

  if (!exhibit || !placeAggregate) {
    return (
      <section className="sakishima-frame-exhibit sf-unavailable" role="alert">
        <MapPin size={22} aria-hidden="true" />
        <strong>{copy.unavailable}</strong>
      </section>
    );
  }

  const selectedFrameLabel =
    selectedFrame === "all"
      ? copy.allFrames
      : displayLabel(
          frameById.get(selectedFrame),
          activeLang,
          selectedFrame,
        );

  return (
    <section
      className="sakishima-frame-exhibit"
      aria-labelledby={titleId}
    >
      <header className="sf-exhibit-header">
        <div>
          <span className="sf-kicker">
            <MapPin size={15} aria-hidden="true" />
            {exhibit.catalog_id}
          </span>
          <h2 id={titleId}>
            {localizedDisplay(exhibit.display?.title, activeLang, copy.title)}
          </h2>
          <p>
            {localizedDisplay(
              exhibit.display?.subtitle,
              activeLang,
              copy.subtitle,
            )}
          </p>
        </div>
        <div className="sf-global-denominators">
          <span>
            <strong>
              {eligibleObservations.length}
            </strong>
            {copy.observationUnit}
          </span>
          <span>
            <strong>{eligibleExcerpts.length}</strong>
            {copy.excerptUnit}
          </span>
        </div>
      </header>

      <aside className="sf-method-note">
        <b>{copy.method}</b>
        <p>
          {includeResearch
            ? localizedDisplay(
                exhibit.display?.interpretation_limit,
                activeLang,
                copy.methodFallback,
              )
            : copy.reviewedScope}
        </p>
      </aside>

      <div
        className="sf-place-tabs"
        role="tablist"
        aria-label={copy.placeTabs}
      >
        {comparisonPlaces.map((place) => {
          const aggregate = aggregateByPlace.get(place);
          return (
            <button
              type="button"
              role="tab"
              aria-selected={selectedPlace === place}
              className={selectedPlace === place ? "active" : ""}
              onClick={() => setSelectedPlace(place)}
              key={place}
            >
              <strong>
                {displayLabel(placeById.get(place), activeLang, place)}
              </strong>
              <span>
                {aggregate?.formal_observation_denominator || 0}{" "}
                {copy.observationsShort} ·{" "}
                {aggregate?.safe_excerpt_denominator || 0} {copy.excerptsShort}
              </span>
            </button>
          );
        })}
      </div>

      <div className="sf-exhibit-body">
        <aside className="sf-frame-panel">
          <header>
            <div>
              <span>{copy.frames}</span>
              <small>
                {displayLabel(
                  placeById.get(selectedPlace),
                  activeLang,
                  selectedPlace,
                )}
              </small>
            </div>
            <p>{copy.unitNote}</p>
          </header>
          <div className="sf-frame-list">
            <button
              type="button"
              className={selectedFrame === "all" ? "active" : ""}
              aria-pressed={selectedFrame === "all"}
              onClick={() => setSelectedFrame("all")}
            >
              <span>{copy.allFrames}</span>
              <b>
                <i>{placeAggregate.formal_observation_denominator}</i>
                <i>{placeAggregate.safe_excerpt_denominator}</i>
              </b>
            </button>
            {frameRows.map((row) => (
              <button
                type="button"
                className={selectedFrame === row.frame_label ? "active" : ""}
                aria-pressed={selectedFrame === row.frame_label}
                onClick={() => setSelectedFrame(row.frame_label)}
                key={row.frame_label}
              >
                <span>
                  {displayLabel(
                    frameById.get(row.frame_label),
                    activeLang,
                    row.frame_label,
                  )}
                </span>
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

        <div className="sf-evidence-panel">
          <header className="sf-selection-header">
            <span>
              <small>{copy.selectedPlace}</small>
              <strong>
                {displayLabel(
                  placeById.get(selectedPlace),
                  activeLang,
                  selectedPlace,
                )}
              </strong>
            </span>
            <span>
              <small>{copy.selectedFrame}</small>
              <strong>{selectedFrameLabel}</strong>
            </span>
          </header>

          <div className="sf-record-columns">
            <section className="sf-record-column">
              <header>
                <span>
                  <FileText size={16} aria-hidden="true" />
                  {copy.observations}
                </span>
                <strong>{visibleObservations.length}</strong>
              </header>
              <div className="sf-record-list">
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
                {!visibleObservations.length && (
                  <p className="sf-empty">{copy.noRows}</p>
                )}
              </div>
            </section>

            <section className="sf-record-column">
              <header>
                <span>
                  <Quotes size={16} aria-hidden="true" />
                  {copy.excerpts}
                </span>
                <strong>{visibleExcerpts.length}</strong>
              </header>
              <div className="sf-record-list">
                {visibleExcerpts.map((row) => (
                  <ExcerptCard
                    row={row}
                    copy={copy}
                    lang={activeLang}
                    frameById={frameById}
                    key={row.corpus_source_id}
                  />
                ))}
                {!visibleExcerpts.length && (
                  <p className="sf-empty">{copy.noRows}</p>
                )}
              </div>
            </section>
          </div>
        </div>
      </div>
    </section>
  );
}
