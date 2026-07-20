import {
  CalendarDots,
  CaretDown,
  Repeat,
  UsersThree,
} from "@phosphor-icons/react";
import {
  BoundaryNote,
  ExhibitHeader,
  Unavailable,
} from "./exhibit/ExhibitKit.jsx";
import "./exhibit/exhibit.css";
import "./RepeatParticipationExhibit.css";

const COPY = {
  zh: {
    kicker: "三份公开名单 · 2010 / 2015 / 2020",
    title: "谁在不同公开行动中重复出现？",
    subtitle: "比较三份完整公开名单，观察跨事件重复参与的组织与身份。",
    observations: "名单观察",
    observationsNote: "每行只属于一个事件",
    events: "公开行动",
    eventsNote: "三份完整名单",
    repeats: "严格匹配的重复身份",
    repeatsNote: "至少出现于两张名单",
    boundaryTitle: "如何阅读",
    boundary: "共同出现说明公开参与，不直接代表组织关系。",
    unmatched: "{n} 个未核名称只计入单次事件，不跨事件匹配。",
    sourceRows: "来源名单行",
    declared: "来源声明",
    structured: "结构化",
    registry: "名录内组织",
    reviewedEventOnly: "已核的事件身份",
    otherEventOnly: "仅见于单次事件的名称",
    target: "进入对象",
    sources: "来源",
    repeatList: "查看 {n} 个严格匹配的重复身份",
    repeatHint: "名录组织与事件限定身份分层列出",
    registryRepeat: "名录内组织",
    reviewedOnlyBadge: "已核 · 未纳入名录",
    sampledEvents: "样本事件",
    actorOpen: "打开组织 {id}",
    overlapList: "查看事件之间的两两重叠",
    overlapHint: "显示分母；不是联盟相似度",
    registryOverlap: "共同出现的名录组织",
    strictOverlap: "严格匹配的共同身份",
    denominators: "分母 {a} / {b}",
    noData: "当前发布包没有 R5 重复参与数据。",
    methodology: "选择与解释边界",
    purposeSample: "三个事件是目的性样本，不代表全部公开行动。",
    identityBoundary: "未核名称保持事件限定，不因写法相似而合并为同一组织。",
  },
  ja: {
    kicker: "3つの公開名簿 · 2010 / 2015 / 2020",
    title: "複数の公開行動に繰り返し現れるのは誰か",
    subtitle: "3つの完全な公開名簿を比較し、イベントを越えた反復参加を見ます。",
    observations: "名簿観察",
    observationsNote: "各行は一つのイベントのみ",
    events: "公開行動",
    eventsNote: "3つの完全な名簿",
    repeats: "厳格な反復 identity",
    repeatsNote: "2つ以上の名簿に出現",
    boundaryTitle: "読み方",
    boundary: "共同出現は公開参加を示しますが、組織関係そのものではありません。",
    unmatched: "未確認の名称 {n} 件は単一イベント内だけで数え、イベント間では照合しません。",
    sourceRows: "出典名簿行",
    declared: "出典記載",
    structured: "構造化",
    registry: "名簿内の団体",
    reviewedEventOnly: "確認済みイベント限定 identity",
    otherEventOnly: "単一イベントのみの名称",
    target: "提出先",
    sources: "出典",
    repeatList: "厳格な反復 identity {n} 件を表示",
    repeatHint: "名簿内団体とイベント限定 identity を分離",
    registryRepeat: "名簿内の団体",
    reviewedOnlyBadge: "確認済み・名簿外",
    sampledEvents: "サンプルイベント",
    actorOpen: "団体 {id} を開く",
    overlapList: "イベント間のペア重複を表示",
    overlapHint: "分母を明示。同盟類似度ではない",
    registryOverlap: "共通する名簿内団体",
    strictOverlap: "共有厳格 identity",
    denominators: "分母 {a} / {b}",
    noData: "現在の公開パッケージに R5 反復参加データはない。",
    methodology: "選択・解釈上の境界",
    purposeSample: "3イベントは目的抽出であり、公開行動の全数ではない。",
    identityBoundary: "未確認名称はイベント限定のまま扱い、表記の類似で同一組織に統合しない。",
  },
  en: {
    kicker: "Three public lists · 2010 / 2015 / 2020",
    title: "Who Reappears Across Public Actions?",
    subtitle: "Compare three complete public lists to see which organizations and identities recur across events.",
    observations: "List observations",
    observationsNote: "Each row belongs to one event",
    events: "Public actions",
    eventsNote: "Three complete lists",
    repeats: "Strict repeat identities",
    repeatsNote: "Present in at least two lists",
    boundaryTitle: "How to read",
    boundary: "Co-appearance shows public participation, not an organizational relation by itself.",
    unmatched: "{n} other event-only names are excluded from matching.",
    sourceRows: "Source-list rows",
    declared: "Declared",
    structured: "Structured",
    registry: "Registry organizations",
    reviewedEventOnly: "Reviewed event-scoped identities",
    otherEventOnly: "Names seen in one event only",
    target: "Target",
    sources: "Sources",
    repeatList: "Show {n} strict repeat identities",
    repeatHint: "Registry organizations and event-scoped identities stay separate",
    registryRepeat: "Registry organization",
    reviewedOnlyBadge: "Reviewed · outside registry",
    sampledEvents: "Sampled events",
    actorOpen: "Open actor {id}",
    overlapList: "Show pairwise event overlap",
    overlapHint: "Denominators shown; not alliance similarity",
    registryOverlap: "Shared registry",
    strictOverlap: "Shared strict identities",
    denominators: "Denominators {a} / {b}",
    noData: "The current publication package has no R5 repeat-participation data.",
    methodology: "Selection and interpretation boundary",
    purposeSample: "The three events are purposively selected, not a census.",
    identityBoundary: "Unreviewed names remain event-scoped and are never merged by name similarity.",
  },
};

const EVENT_LABELS = {
  EV2010_WWF_67: {
    zh: "2010 WWF 67 团体共同声明",
    ja: "2010 WWF 67団体共同声明",
    en: "2010 WWF 67-group joint statement",
  },
  EV2015_NACSJ_31: {
    zh: "2015 NACSJ／和平船 31 NGO 紧急声明",
    ja: "2015 NACSJ／ピースボート 31 NGO 緊急声明",
    en: "2015 NACSJ / Peace Boat 31-NGO statement",
  },
  EV2020_OEJP_MMC_71: {
    zh: "2020 OEJP 牵头的 71 团体 MMC 请求",
    ja: "2020 OEJP 主導 71団体 MMC 要請",
    en: "2020 OEJP-led 71-group MMC request",
  },
};

const ACTION_LABELS = {
  joint_statement: { zh: "共同声明", ja: "共同声明", en: "Joint statement" },
  request_letter_and_civil_society_report: {
    zh: "请求书／公民社会报告",
    ja: "要請書／市民社会報告",
    en: "Request letter / civil-society report",
  },
};

const safeLang = (lang) => (COPY[lang] ? lang : "zh");
const text = (entry, lang, fallback = "") =>
  entry?.[safeLang(lang)] || entry?.zh || fallback;
const fill = (template, values) =>
  Object.entries(values).reduce(
    (result, [key, value]) => result.replace(`{${key}}`, String(value)),
    template,
  );

const TIERS = [
  ["registry_actor", "registry", "registry"],
  ["human_reviewed_event_only_identity", "reviewedEventOnly", "reviewed"],
  ["other_event_only_name", "otherEventOnly", "other"],
];

function TierLegend({ counts, total, copy }) {
  return (
    <div className="r5-tiers">
      <div className="r5-stacked" role="img">
        {TIERS.map(([key, , className]) => {
          const value = counts[key] || 0;
          return value > 0 ? (
            <span
              className={className}
              style={{ width: `${(value / Math.max(total, 1)) * 100}%` }}
              key={key}
            />
          ) : null;
        })}
      </div>
      <div className="r5-tier-legend">
        {TIERS.map(([key, label, className]) => (
          <span key={key}>
            <i className={className} />
            {copy[label]} <strong>{counts[key] || 0}</strong>
          </span>
        ))}
      </div>
    </div>
  );
}

function EventCard({ event, lang, copy }) {
  const denominator = event.denominator || {};
  const counts = event.observation_count_by_participant_tier || {};
  const total = denominator.derived_observation_count || 0;
  const eventLabel = text(EVENT_LABELS[event.event_id], lang, event.event_name);
  const actionLabel = text(ACTION_LABELS[event.action_type], lang, event.action_type);

  return (
    <article className="r5-event-card">
      <header>
        <div>
          <span className="r5-year">{event.event_year}</span>
          <span className="r5-action">{actionLabel}</span>
        </div>
        <strong>{total}</strong>
      </header>
      <h3>{eventLabel}</h3>
      <div className="r5-denominator">
        <span>
          {copy.sourceRows} <strong>{total}</strong>
        </span>
        <span>
          {copy.declared} <strong>{denominator.declared_participant_count}</strong>
        </span>
        <span>
          {copy.structured} <strong>{denominator.structured_participant_count}</strong>
        </span>
      </div>
      <TierLegend counts={counts} total={total} copy={copy} />
      <div className="r5-event-meta">
        <span>
          {copy.target}：{(event.target_institution || []).join(" · ")}
        </span>
        <span>
          {copy.sources}：{(event.source_refs || []).join(" · ")}
        </span>
      </div>
    </article>
  );
}

function RepeatIdentity({ row, copy, onOpenActor }) {
  const isActor = Boolean(row.actor_id);
  const canOpen = isActor && typeof onOpenActor === "function";
  const identityName = row.canonical_name || row.strict_identity_key;

  return (
    <li className="r5-identity">
      <div className="r5-identity-main">
        {canOpen ? (
          <button type="button" onClick={() => onOpenActor(row.actor_id)} title={fill(copy.actorOpen, { id: row.actor_id })}>
            {identityName}
          </button>
        ) : (
          <strong>{identityName}</strong>
        )}
        {isActor ? (
          <span className="r5-badge registry">
            {copy.registryRepeat}
            <small>{row.actor_id}</small>
          </span>
        ) : (
          <span className="r5-badge reviewed">{copy.reviewedOnlyBadge}</span>
        )}
      </div>
      <div className="r5-event-pills" aria-label={copy.sampledEvents}>
        {(row.event_years || []).map((year, index) => (
          <span key={`${row.strict_identity_key}-${year}-${index}`}>{year}</span>
        ))}
      </div>
    </li>
  );
}

function PairwiseOverlap({ row, eventById, lang, copy }) {
  const eventA = eventById.get(row.event_a);
  const eventB = eventById.get(row.event_b);
  const labelA = eventA?.event_year || text(EVENT_LABELS[row.event_a], lang, row.event_a);
  const labelB = eventB?.event_year || text(EVENT_LABELS[row.event_b], lang, row.event_b);

  return (
    <article className="r5-overlap-card">
      <header>
        <strong>
          {labelA} ↔ {labelB}
        </strong>
        <span>
          {fill(copy.denominators, {
            a: row.strict_identity_denominator_a,
            b: row.strict_identity_denominator_b,
          })}
        </span>
      </header>
      <div>
        <span>
          {copy.registryOverlap} <strong>{row.shared_registry_actor_count}</strong>
        </span>
        <span>
          {copy.strictOverlap} <strong>{row.shared_strict_identity_count}</strong>
        </span>
      </div>
    </article>
  );
}

export function RepeatParticipationExhibit({ exhibit, lang = "zh", onOpenActor }) {
  const locale = safeLang(lang);
  const copy = COPY[locale];

  if (!exhibit?.summary || !Array.isArray(exhibit.events)) {
    return <Unavailable text={copy.noData} />;
  }

  const summary = exhibit.summary;
  const unmatched = summary.observation_count_by_participant_tier?.other_event_only_name || 0;
  const eventById = new Map(exhibit.events.map((event) => [event.event_id, event]));

  return (
    <section className="r5-exhibit">
      <ExhibitHeader
        kicker={copy.kicker}
        title={text(exhibit.display?.title, locale, copy.title)}
        subtitle={text(exhibit.display?.subtitle, locale, copy.subtitle)}
        metrics={[
          { value: summary.observation_count, label: copy.observations, note: copy.observationsNote, icon: UsersThree },
          { value: summary.event_count, label: copy.events, note: copy.eventsNote, icon: CalendarDots },
          { value: summary.strict_repeat_identity_count, label: copy.repeats, note: copy.repeatsNote, icon: Repeat },
        ]}
      />

      <BoundaryNote
        title={copy.boundaryTitle}
        fullText={`${text(exhibit.display?.interpretation_limit, locale, copy.boundary)} ${fill(copy.unmatched, { n: unmatched })} ${copy.purposeSample} ${copy.identityBoundary}`}
        helpOnly
      />

      <div className="r5-events">
        {exhibit.events.map((event) => (
          <EventCard event={event} lang={locale} copy={copy} key={event.event_id} />
        ))}
      </div>

      <div className="r5-disclosures">
        <details>
          <summary>
            <span>
              <strong>
                {fill(copy.repeatList, { n: summary.strict_repeat_identity_count })}
              </strong>
              <small>{copy.repeatHint}</small>
            </span>
            <CaretDown size={16} />
          </summary>
          <ol className="r5-identity-list">
            {(exhibit.repeat_identities || []).map((row) => (
              <RepeatIdentity row={row} copy={copy} onOpenActor={onOpenActor} key={row.strict_identity_key} />
            ))}
          </ol>
        </details>

        <details>
          <summary>
            <span>
              <strong>{copy.overlapList}</strong>
            </span>
            <CaretDown size={16} />
          </summary>
          <div className="r5-overlap-grid">
            {(exhibit.pairwise_overlaps || []).map((row) => (
              <PairwiseOverlap row={row} eventById={eventById} lang={locale} copy={copy} key={`${row.event_a}-${row.event_b}`} />
            ))}
          </div>
        </details>
      </div>
    </section>
  );
}
