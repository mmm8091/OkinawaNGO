from __future__ import annotations

"""R5/R11 event-aware figure: collective-action repertoire over time.

Reads actor_relation_events_v1.csv and draws one bubble per event on
action-type lanes (y) against year (x); bubble area = registered participants.
Shows how base issues move across co-signing, litigation, referendum, and
international-request action over 1997-2020.

Current output: outputs/module_completion_v0/fig/fig_event_repertoire.html
The pre-HR-015 screenshot is retained as fig_event_repertoire_pre_hr015.png;
do not restore the canonical PNG name until a fresh screenshot is captured.

Palette: dataviz reference categorical slots 1-5 (validated: worst adjacent
CVD dE 24.2; contrast WARN relieved by labelled lanes + per-bubble labels).
"""

import csv
import math
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "outputs" / "module_completion_v0" / "actor_relation_events_v1.csv"
OUT = ROOT / "outputs" / "module_completion_v0" / "fig"

# action_type -> (lane index, label, light hex, dark hex)
ACTIONS = {
    "co_signing":     (0, "共同署名 co-signing",     "#2a78d6", "#3987e5"),
    "request_letter": (1, "共同要请 request",         "#1baf7a", "#199e70"),
    "litigation":     (2, "诉讼 litigation",          "#eda100", "#c98500"),
    "referendum":     (3, "公投 referendum",          "#008300", "#008300"),
    "opinion_ad":     (4, "意见广告 opinion-ad",       "#4a3aa7", "#9085e9"),
}
# event_id -> short label (bubbles)
EV_LABEL = {
    "EV1997_NAGO_REFERENDUM": "名护公投",
    "EV2003_DUGONG_LAWSUIT": "儒艮诉讼",
    "EV2010_WWF_67": "WWF 67",
    "EV2012_YONAGUNI_OPINION_AD": "与那国意见广告",
    "EV2015_NACSJ_31": "NACSJ 31",
    "EV2015_YONAGUNI_REFERENDUM": "与那国公投",
    "EV2019_PREF_REFERENDUM": "县民投票",
    "EV_ISHIGAKI_REFERENDUM": "石垣公投",
    "EV2020_OEJP_MMC_71": "OEJP/MMC 71",
}

W, H = 1000, 468
PL, PR, PT = 182, 966, 58
LANE_H = 66
AXIS_Y = PT + 5 * LANE_H + 6
YR_MIN, YR_MAX = 1996, 2021


def xpos(year: float) -> float:
    return PL + (year - YR_MIN) / (YR_MAX - YR_MIN) * (PR - PL)


def lane_y(i: int) -> float:
    return PT + i * LANE_H + LANE_H / 2


def main() -> None:
    rows = list(csv.DictReader(SRC.open(encoding="utf-8-sig")))
    events: dict[str, dict] = {}
    for r in rows:
        e = events.setdefault(r["event_id"], {
            "year": int(r["event_year"]), "action": r["action_type"], "n": 0,
            "actors": [],
        })
        e["n"] += 1
        e["actors"].append(r["actor_id"])

    # cross-event repeat actors (appear in >1 event)
    actor_events = Counter()
    for r in rows:
        actor_events[r["actor_id"]] += 1
    repeats = sorted(a for a, c in actor_events.items() if c > 1)

    # resolve same-lane same-year collisions with a small x offset
    placed: list[tuple[int, float]] = []
    offsets: dict[str, float] = {}
    for eid, e in sorted(events.items(), key=lambda kv: (ACTIONS[kv[1]["action"]][0], kv[1]["year"])):
        li = ACTIONS[e["action"]][0]
        base = xpos(e["year"])
        off = 0.0
        for pl, px in placed:
            if pl == li and abs(px - base) < 40:
                off = 26.0
        offsets[eid] = off
        placed.append((li, base + off))

    def r_of(n: int) -> float:
        return 6 + 4.2 * math.sqrt(n)

    svg = [f'<svg viewBox="0 0 {W} {H}" class="repviz" role="img" '
           f'aria-label="集体行动 repertoire 时间线">']

    # lane bands + labels
    for act, (i, label, _l, _d) in ACTIONS.items():
        y = PT + i * LANE_H
        if i % 2 == 0:
            svg.append(f'<rect x="{PL}" y="{y:.0f}" width="{PR-PL}" height="{LANE_H}" '
                       f'fill="var(--band)"/>')
        svg.append(f'<text x="{PL-14}" y="{lane_y(i)+4:.0f}" text-anchor="end" '
                   f'class="lane">{label}</text>')

    # year axis
    svg.append(f'<line x1="{PL}" y1="{AXIS_Y}" x2="{PR}" y2="{AXIS_Y}" class="axis"/>')
    for yr in (1997, 2003, 2010, 2012, 2015, 2019, 2020):
        x = xpos(yr)
        svg.append(f'<line x1="{x:.0f}" y1="{PT}" x2="{x:.0f}" y2="{AXIS_Y}" class="grid"/>')
        svg.append(f'<text x="{x:.0f}" y="{AXIS_Y+18:.0f}" text-anchor="middle" '
                   f'class="tick">{yr}</text>')

    # bubbles
    for eid, e in events.items():
        i, _label, lite, dark = ACTIONS[e["action"]][0], *ACTIONS[e["action"]][1:]
        cx = xpos(e["year"]) + offsets[eid]
        cy = lane_y(i)
        r = r_of(e["n"])
        var = f"--a{i}"
        svg.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r:.1f}" '
                   f'fill="var({var})" fill-opacity="0.82" stroke="var(--surface)" '
                   f'stroke-width="2"/>')
        # count inside big bubbles, beside small ones
        if r >= 15:
            svg.append(f'<text x="{cx:.0f}" y="{cy+4:.0f}" text-anchor="middle" '
                       f'class="cnt-in">{e["n"]}</text>')
        else:
            svg.append(f'<text x="{cx:.0f}" y="{cy-r-4:.0f}" text-anchor="middle" '
                       f'class="cnt">{e["n"]}</text>')
        # event label below bubble; stagger offset (collided) events one line lower
        lab = EV_LABEL.get(eid, eid)
        lab_y = cy + r + (27 if offsets[eid] else 14)
        svg.append(f'<text x="{cx:.0f}" y="{lab_y:.0f}" text-anchor="middle" '
                   f'class="evlab">{lab}</text>')
    svg.append("</svg>")

    repeats_txt = "、".join(repeats) if repeats else "（无）"
    lane_css = "".join(
        f"--a{i}:{lite};" for _a, (i, _l, lite, _d) in ACTIONS.items()
    )
    dark_css = "".join(
        f"--a{i}:{dark};" for _a, (i, _l, _l2, dark) in ACTIONS.items()
    )

    html = f"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<style>
.viz-root{{--surface:#fcfcfb;--band:#f4f3ef;--text-primary:#0b0b0b;--text-secondary:#52514e;
--muted:#898781;--axis:#c3c2b7;--grid:#e1e0d9;{lane_css}
background:var(--surface);padding:20px 22px 16px;max-width:1000px;
font-family:system-ui,-apple-system,"Segoe UI","Microsoft YaHei",sans-serif;}}
@media (prefers-color-scheme: dark){{.viz-root{{--surface:#1a1a19;--band:#232321;
--text-primary:#fff;--text-secondary:#c3c2b7;--muted:#898781;--axis:#383835;--grid:#2c2c2a;{dark_css}}}}}
.viz-root h3{{margin:0 0 2px;font-size:16px;color:var(--text-primary);}}
.viz-root .sub{{margin:0 0 6px;font-size:12.5px;color:var(--text-secondary);}}
.repviz{{width:100%;height:auto;display:block;}}
.lane{{font-size:12px;fill:var(--text-secondary);font-weight:600;}}
.axis{{stroke:var(--axis);stroke-width:1.5;}}
.grid{{stroke:var(--grid);stroke-width:1;}}
.tick{{font-size:11px;fill:var(--muted);font-variant-numeric:tabular-nums;}}
.cnt-in{{font-size:12px;fill:#fff;font-weight:700;font-variant-numeric:tabular-nums;}}
.cnt{{font-size:11px;fill:var(--text-secondary);font-weight:700;font-variant-numeric:tabular-nums;}}
.evlab{{font-size:10.5px;fill:var(--text-secondary);}}
.note{{margin:8px 0 0;font-size:12px;color:var(--text-secondary);line-height:1.5;}}
.note b{{color:var(--text-primary);}}
</style></head><body>
<div class="viz-root">
<h3>集体行动 repertoire 时间线（R5 / R11 事件感知层）</h3>
<p class="sub">每个气泡＝一次事件，落在其行动类型泳道上；气泡面积＝当前 registry 已录入的参与组织数；横轴＝年份。</p>
{''.join(svg)}
<p class="note"><b>读法：</b>基地议题的公开行动方式随时间从共同署名（2010/2015）扩展到国际要请（2020 MMC）、法律诉讼（2003 儒艮案）与住民投票（名护 1997 → 与那国 / 县民 / 石垣）。
跨事件重复出现的组织极少——仅 {repeats_txt}——其余多为一次性署名，<b>印证"共同署名≠稳定联盟"</b>。公投泳道气泡多为 1，因当前只录入了发起委员会一个组织，非全部参与者。</p>
</div></body></html>"""

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "fig_event_repertoire.html").write_text(html, encoding="utf-8")
    print(f"Wrote {(OUT / 'fig_event_repertoire.html').relative_to(ROOT)}; "
          f"{len(events)} events; repeat actors: {repeats_txt}")


if __name__ == "__main__":
    main()
