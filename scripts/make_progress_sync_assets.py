from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "interim"
OUT = ROOT / "outputs" / "progress_sync_v0"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def save_bar(counter: Counter[str], title: str, path: Path, *, top_n: int | None = None) -> None:
    items = counter.most_common(top_n)
    labels = [k for k, _ in items]
    values = [v for _, v in items]
    fig_h = max(4, 0.36 * len(items) + 1.6)
    fig, ax = plt.subplots(figsize=(9, fig_h))
    colors = ["#3d6f7f", "#c1694f", "#7a8b4f", "#8063a6", "#b58945", "#4f7d5a"]
    ax.barh(labels[::-1], values[::-1], color=[colors[i % len(colors)] for i in range(len(values))][::-1])
    ax.set_title(title, fontsize=14, pad=12)
    ax.set_xlabel("Count")
    ax.grid(axis="x", alpha=0.25)
    for spine in ["top", "right", "left"]:
        ax.spines[spine].set_visible(False)
    for i, value in enumerate(values[::-1]):
        ax.text(value + 0.2, i, str(value), va="center", fontsize=9)
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def save_matrix(rows: list[dict[str, str]], title: str, path: Path) -> None:
    place_focus = ["Henoko", "Oura Bay", "Ishigaki", "Miyako", "Yonaguni", "Kadena", "Camp Foster", "JICA Okinawa", "U.S. Consulate General Naha"]
    issue_focus = [
        "anti_base",
        "anti_military",
        "environment",
        "biodiversity",
        "groundwater",
        "life_safety",
        "health_risk",
        "local_autonomy",
        "referendum",
        "legal",
        "international_advocacy",
        "public_diplomacy",
        "military_family_service",
        "base_community_welfare",
        "international_cooperation",
        "frontline_prevention",
        "Taiwan_contingency",
    ]

    actor_issues: dict[str, set[str]] = defaultdict(set)
    actor_places: dict[str, set[str]] = defaultdict(set)
    for r in read_csv(DATA / "07_actor_issue_edges_initial_v0.csv"):
        actor_issues[r["actor_id"]].add(r["issue_label"])
    for r in read_csv(DATA / "08_actor_place_edges_initial_v0.csv"):
        actor_places[r["actor_id"]].add(r["place_name"])

    counts: dict[tuple[str, str], int] = defaultdict(int)
    for actor_id, places in actor_places.items():
        issues = actor_issues.get(actor_id, set())
        for p in places:
            if p not in place_focus:
                continue
            for issue in issues:
                if issue in issue_focus:
                    counts[(p, issue)] += 1

    data = [[counts[(p, issue)] for issue in issue_focus] for p in place_focus]
    fig, ax = plt.subplots(figsize=(13, 5.8))
    im = ax.imshow(data, cmap="YlGnBu")
    ax.set_xticks(range(len(issue_focus)), labels=issue_focus, rotation=45, ha="right", fontsize=8)
    ax.set_yticks(range(len(place_focus)), labels=place_focus, fontsize=9)
    ax.set_title(title, fontsize=14, pad=12)
    for i, row in enumerate(data):
        for j, val in enumerate(row):
            if val:
                ax.text(j, i, str(val), ha="center", va="center", fontsize=8, color="#1f2933")
    fig.colorbar(im, ax=ax, fraction=0.025, pad=0.02)
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    actors = read_csv(DATA / "01_actor_registry_initial_v0.csv")
    issue_edges = read_csv(DATA / "07_actor_issue_edges_initial_v0.csv")
    place_edges = read_csv(DATA / "08_actor_place_edges_initial_v0.csv")
    funding_edges = read_csv(DATA / "15_funding_or_support_edges_sample_v0.csv")
    sources = read_csv(DATA / "05_source_log_initial_v0.csv")

    actor_class = Counter(a["actor_class"] for a in actors)
    origin_type = Counter(a["origin_type"] for a in actors)
    evidence = Counter(a["evidence_level"] for a in actors)
    issues = Counter(e["issue_label"] for e in issue_edges)
    places = Counter(e["place_name"] for e in place_edges)
    funding_relation = Counter(e["relation_type"] for e in funding_edges)
    source_type = Counter(s["source_type"] for s in sources)

    write_csv(OUT / "actor_class_counts.csv", [{"actor_class": k, "count": v} for k, v in actor_class.most_common()], ["actor_class", "count"])
    write_csv(OUT / "origin_type_counts.csv", [{"origin_type": k, "count": v} for k, v in origin_type.most_common()], ["origin_type", "count"])
    write_csv(OUT / "actor_evidence_counts.csv", [{"evidence_level": k, "count": v} for k, v in evidence.most_common()], ["evidence_level", "count"])
    write_csv(OUT / "issue_edge_counts.csv", [{"issue_label": k, "count": v} for k, v in issues.most_common()], ["issue_label", "count"])
    write_csv(OUT / "place_edge_counts.csv", [{"place_name": k, "count": v} for k, v in places.most_common()], ["place_name", "count"])
    write_csv(OUT / "source_type_counts.csv", [{"source_type": k, "count": v} for k, v in source_type.most_common()], ["source_type", "count"])

    save_bar(actor_class, "Actor Types in Initial Registry (n=61)", OUT / "fig_actor_class_counts.png", top_n=14)
    save_bar(origin_type, "Actor Origins in Initial Registry", OUT / "fig_actor_origin_counts.png")
    save_bar(issues, "Top Issue Links in Initial Actor-Issue Table", OUT / "fig_issue_edge_counts.png", top_n=14)
    save_bar(places, "Top Place Links in Initial Actor-Place Table", OUT / "fig_place_edge_counts.png", top_n=12)
    save_bar(evidence, "Evidence Levels in Initial Actor Registry", OUT / "fig_actor_evidence_counts.png")
    save_bar(funding_relation, "Support / Funding Sample Relation Types", OUT / "fig_support_relation_types.png")
    save_matrix([], "Place-Issue Matrix from Initial Candidate Edges", OUT / "fig_place_issue_matrix.png")

    summary = [
        {"metric": "actors_initial", "value": len(actors)},
        {"metric": "sources_initial", "value": len(sources)},
        {"metric": "issue_edges_initial", "value": len(issue_edges)},
        {"metric": "place_edges_initial", "value": len(place_edges)},
        {"metric": "support_edges_sample", "value": len(funding_edges)},
        {"metric": "actor_classes", "value": len(actor_class)},
        {"metric": "origin_types", "value": len(origin_type)},
        {"metric": "issue_labels_linked", "value": len(issues)},
        {"metric": "places_linked", "value": len(places)},
    ]
    write_csv(OUT / "progress_summary_metrics.csv", summary, ["metric", "value"])


if __name__ == "__main__":
    main()
