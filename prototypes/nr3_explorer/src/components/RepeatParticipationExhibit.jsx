import {
  CalendarDots,
  CaretDown,
  Repeat,
  UsersThree,
  WarningCircle,
} from "@phosphor-icons/react";
import "./RepeatParticipationExhibit.css";

const COPY = {
  zh: {
    kicker: "R5 · 公开名单样本",
    title: "重复参与，不是组织联盟",
    subtitle:
      "三张完整公开名单按“事件 × 名称／严格身份”逐行统计。只有 registry ID 或经人工确认的 event-only identity 才能跨事件匹配。",
    observations: "名单观察",
    observationsNote: "每行只属于一个事件",
    events: "目的性事件",
    eventsNote: "不是复归后行动普查",
    repeats: "严格重复身份",
    repeatsNote: "至少出现于两张名单",
    boundaryTitle: "这张图不生成组织关系边",
    boundary:
      "共同署名或重复出现只能说明公开参与；不能据此推定成员关系、稳定联盟、持续协调、资金或影响力。",
    unmatched: "{n} 个其他 event-only 名称没有获准跨事件匹配。",
    sourceRows: "来源名单行",
    declared: "来源声明",
    structured: "结构化",
    registry: "registry 组织",
    reviewedEventOnly: "人审 event-only 身份",
    otherEventOnly: "其他 event-only 名称",
    target: "进入对象",
    sources: "来源",
    repeatList: "查看 {n} 个严格重复身份",
    repeatHint: "registry 与人审 event-only 分层列出",
    registryRepeat: "registry 组织",
    reviewedOnlyBadge: "经人审 · 未进 registry",
    sampledEvents: "样本事件",
    actorOpen: "打开组织 {id}",
    overlapList: "查看事件之间的两两重叠",
    overlapHint: "显示分母；不是联盟相似度",
    registryOverlap: "共享 registry",
    strictOverlap: "共享严格身份",
    denominators: "分母 {a} / {b}",
    noData: "当前发布包没有 R5 重复参与数据。",
    methodology: "选择与解释边界",
    purposeSample: "三个事件是目的性样本，不代表全部公开行动。",
    identityBoundary:
      "未核名称保持事件限定，不因写法相似而合并为同一组织。",
  },
  ja: {
    kicker: "R5 · 公開名簿サンプル",
    title: "反復参加であり、組織間同盟ではない",
    subtitle:
      "3つの完全な公開名簿を「イベント × 名称／厳格な同一性」で行単位に集計。イベント間照合は registry ID または人審済み event-only identity に限る。",
    observations: "名簿観察",
    observationsNote: "各行は一つのイベントのみ",
    events: "目的抽出イベント",
    eventsNote: "復帰後の行動全数ではない",
    repeats: "厳格な反復 identity",
    repeatsNote: "2つ以上の名簿に出現",
    boundaryTitle: "この表示は組織間の関係辺を作らない",
    boundary:
      "共同署名や反復出現が示すのは公開参加のみ。加盟、安定した同盟、継続的調整、資金、影響力は推定できない。",
    unmatched: "その他 event-only 名称 {n} 件はイベント間照合の対象外。",
    sourceRows: "出典名簿行",
    declared: "出典記載",
    structured: "構造化",
    registry: "registry 団体",
    reviewedEventOnly: "人審済み event-only identity",
    otherEventOnly: "その他 event-only 名称",
    target: "提出先",
    sources: "出典",
    repeatList: "厳格な反復 identity {n} 件を表示",
    repeatHint: "registry と人審済み event-only を分離",
    registryRepeat: "registry 団体",
    reviewedOnlyBadge: "人審済み・registry 外",
    sampledEvents: "サンプルイベント",
    actorOpen: "団体 {id} を開く",
    overlapList: "イベント間のペア重複を表示",
    overlapHint: "分母を明示。同盟類似度ではない",
    registryOverlap: "共有 registry",
    strictOverlap: "共有厳格 identity",
    denominators: "分母 {a} / {b}",
    noData: "現在の公開パッケージに R5 反復参加データはない。",
    methodology: "選択・解釈上の境界",
    purposeSample: "3イベントは目的抽出であり、公開行動の全数ではない。",
    identityBoundary:
      "未確認名称はイベント限定のまま扱い、表記の類似だけで同一組織に統合しない。",
  },
  en: {
    kicker: "R5 · Public-list sample",
    title: "Repeated participation, not an alliance",
    subtitle:
      "Three complete public lists are counted row by row as event × name/strict identity. Cross-event matching is limited to registry IDs and human-reviewed event-only identities.",
    observations: "List observations",
    observationsNote: "Each row belongs to one event",
    events: "Purposive events",
    eventsNote: "Not a post-reversion census",
    repeats: "Strict repeat identities",
    repeatsNote: "Present in at least two lists",
    boundaryTitle: "This exhibit creates no actor-relation edges",
    boundary:
      "Co-signing or repeated appearance shows public participation only. It does not establish membership, a stable alliance, continuing coordination, funding, or influence.",
    unmatched: "{n} other event-only names are excluded from cross-event matching.",
    sourceRows: "Source-list rows",
    declared: "Declared",
    structured: "Structured",
    registry: "Registry actors",
    reviewedEventOnly: "Reviewed event-only identities",
    otherEventOnly: "Other event-only names",
    target: "Target",
    sources: "Sources",
    repeatList: "Show {n} strict repeat identities",
    repeatHint: "Registry and reviewed event-only identities stay separate",
    registryRepeat: "Registry actor",
    reviewedOnlyBadge: "Human-reviewed · outside registry",
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
    identityBoundary:
      "Unreviewed names remain event-scoped and are never merged by name similarity.",
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
  joint_statement: {
    zh: "共同声明",
    ja: "共同声明",
    en: "Joint statement",
  },
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

function TierLegend({ counts, total, copy }) {
  const tiers = [
    ["registry_actor", "registry", "registry"],
    [
      "human_reviewed_event_only_identity",
      "reviewedEventOnly",
      "reviewed",
    ],
    ["other_event_only_name", "otherEventOnly", "other"],
  ];

  return (
    <div className="r5-repeat-tier-block">
      <div
        className="r5-repeat-stacked"
        role="img"
        aria-label={`${copy.registry} ${counts.registry_actor || 0}; ${
          copy.reviewedEventOnly
        } ${counts.human_reviewed_event_only_identity || 0}; ${
          copy.otherEventOnly
        } ${counts.other_event_only_name || 0}`}
      >
        {tiers.map(([key, , className]) => {
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
      <div className="r5-repeat-tier-legend">
        {tiers.map(([key, label, className]) => (
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
  const actionLabel = text(
    ACTION_LABELS[event.action_type],
    lang,
    event.action_type,
  );

  return (
    <article className="r5-repeat-event-card">
      <header>
        <div>
          <span className="r5-repeat-year">{event.event_year}</span>
          <span className="r5-repeat-action">{actionLabel}</span>
        </div>
        <strong>{total}</strong>
      </header>
      <h3>{eventLabel}</h3>
      <div className="r5-repeat-denominator">
        <span>
          {copy.sourceRows}
          <strong>{total}</strong>
        </span>
        <span>
          {copy.declared}
          <strong>{denominator.declared_participant_count}</strong>
        </span>
        <span>
          {copy.structured}
          <strong>{denominator.structured_participant_count}</strong>
        </span>
      </div>
      <TierLegend counts={counts} total={total} copy={copy} />
      <dl className="r5-repeat-event-meta">
        <div>
          <dt>{copy.target}</dt>
          <dd>{(event.target_institution || []).join(" · ")}</dd>
        </div>
        <div>
          <dt>{copy.sources}</dt>
          <dd>{(event.source_refs || []).join(" · ")}</dd>
        </div>
      </dl>
    </article>
  );
}

function RepeatIdentity({ row, copy, onOpenActor }) {
  const isActor = Boolean(row.actor_id);
  const canOpen = isActor && typeof onOpenActor === "function";
  const identityName = row.canonical_name || row.strict_identity_key;

  return (
    <li className="r5-repeat-identity">
      <div className="r5-repeat-identity-main">
        {canOpen ? (
          <button
            type="button"
            onClick={() => onOpenActor(row.actor_id)}
            title={fill(copy.actorOpen, { id: row.actor_id })}
          >
            {identityName}
          </button>
        ) : (
          <strong>{identityName}</strong>
        )}
        {isActor ? (
          <span className="r5-repeat-identity-badge registry">
            {copy.registryRepeat}
            <small>{row.actor_id}</small>
          </span>
        ) : (
          <span className="r5-repeat-identity-badge reviewed">
            {copy.reviewedOnlyBadge}
          </span>
        )}
      </div>
      <div className="r5-repeat-event-pills" aria-label={copy.sampledEvents}>
        {(row.event_years || []).map((year, index) => (
          <span key={`${row.strict_identity_key}-${year}-${index}`}>
            {year}
          </span>
        ))}
      </div>
    </li>
  );
}

function PairwiseOverlap({ row, eventById, lang, copy }) {
  const eventA = eventById.get(row.event_a);
  const eventB = eventById.get(row.event_b);
  const labelA =
    eventA?.event_year ||
    text(EVENT_LABELS[row.event_a], lang, row.event_a);
  const labelB =
    eventB?.event_year ||
    text(EVENT_LABELS[row.event_b], lang, row.event_b);

  return (
    <article className="r5-repeat-overlap-card">
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
          {copy.registryOverlap}
          <strong>{row.shared_registry_actor_count}</strong>
        </span>
        <span>
          {copy.strictOverlap}
          <strong>{row.shared_strict_identity_count}</strong>
        </span>
      </div>
    </article>
  );
}

export function RepeatParticipationExhibit({
  exhibit,
  lang = "zh",
  onOpenActor,
}) {
  const locale = safeLang(lang);
  const copy = COPY[locale];

  if (!exhibit?.summary || !Array.isArray(exhibit.events)) {
    return (
      <section className="r5-repeat-exhibit empty" aria-label={copy.title}>
        <WarningCircle size={24} />
        <p>{copy.noData}</p>
      </section>
    );
  }

  const summary = exhibit.summary;
  const displayTitle = text(exhibit.display?.title, locale, copy.title);
  const displaySubtitle = text(
    exhibit.display?.subtitle,
    locale,
    copy.subtitle,
  );
  const displayBoundary = text(
    exhibit.display?.interpretation_limit,
    locale,
    copy.boundary,
  );
  const unmatched =
    summary.observation_count_by_participant_tier?.other_event_only_name || 0;
  const repeats = exhibit.repeat_identities || [];
  const overlaps = exhibit.pairwise_overlaps || [];
  const eventById = new Map(
    exhibit.events.map((event) => [event.event_id, event]),
  );

  return (
    <section className="r5-repeat-exhibit" aria-label={displayTitle}>
      <header className="r5-repeat-heading">
        <div>
          <span className="r5-repeat-kicker">{copy.kicker}</span>
          <h2>{displayTitle}</h2>
          <p>{displaySubtitle}</p>
        </div>
        <span className="r5-repeat-method-badge">{copy.methodology}</span>
      </header>

      <div className="r5-repeat-metrics">
        <article>
          <UsersThree size={22} />
          <strong>{summary.observation_count}</strong>
          <span>{copy.observations}</span>
          <small>{copy.observationsNote}</small>
        </article>
        <article>
          <CalendarDots size={22} />
          <strong>{summary.event_count}</strong>
          <span>{copy.events}</span>
          <small>{copy.eventsNote}</small>
        </article>
        <article>
          <Repeat size={22} />
          <strong>{summary.strict_repeat_identity_count}</strong>
          <span>{copy.repeats}</span>
          <small>{copy.repeatsNote}</small>
        </article>
      </div>

      <aside className="r5-repeat-boundary">
        <WarningCircle size={22} weight="fill" />
        <div>
          <strong>{copy.boundaryTitle}</strong>
          <p>{displayBoundary}</p>
          <span>{fill(copy.unmatched, { n: unmatched })}</span>
        </div>
      </aside>

      <div className="r5-repeat-events">
        {exhibit.events.map((event) => (
          <EventCard
            event={event}
            lang={locale}
            copy={copy}
            key={event.event_id}
          />
        ))}
      </div>

      <div className="r5-repeat-disclosures">
        <details>
          <summary>
            <span>
              <strong>
                {fill(copy.repeatList, {
                  n: summary.strict_repeat_identity_count,
                })}
              </strong>
              <small>{copy.repeatHint}</small>
            </span>
            <CaretDown size={18} />
          </summary>
          <ol className="r5-repeat-identity-list">
            {repeats.map((row) => (
              <RepeatIdentity
                row={row}
                copy={copy}
                onOpenActor={onOpenActor}
                key={row.strict_identity_key}
              />
            ))}
          </ol>
        </details>

        <details>
          <summary>
            <span>
              <strong>{copy.overlapList}</strong>
              <small>{copy.overlapHint}</small>
            </span>
            <CaretDown size={18} />
          </summary>
          <div className="r5-repeat-overlap-grid">
            {overlaps.map((row) => (
              <PairwiseOverlap
                row={row}
                eventById={eventById}
                lang={locale}
                copy={copy}
                key={`${row.event_a}-${row.event_b}`}
              />
            ))}
          </div>
        </details>
      </div>

      <footer className="r5-repeat-footer">
        <strong>{copy.methodology}</strong>
        <span>{copy.purposeSample}</span>
        <span>{copy.identityBoundary}</span>
      </footer>
    </section>
  );
}
