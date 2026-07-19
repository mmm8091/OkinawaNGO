from __future__ import annotations

import argparse
import io
import json
import math
import os
import tempfile
import urllib.request
import zipfile
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, Rectangle
from shapely.geometry import GeometryCollection, MultiPolygon, Polygon, mapping, shape
from shapely.geometry.polygon import orient
from shapely.ops import unary_union


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "outputs" / "learning_v1"
PNG_PATH = OUT_DIR / "okinawa_regions_research_map_v1.png"
GEOJSON_PATH = OUT_DIR / "okinawa_municipal_boundaries_simplified_v1.geojson"

DATA_URL = (
    "https://nlftp.mlit.go.jp/ksj/gml/data/N03/N03-2025/"
    "N03-20250101_47_GML.zip"
)
SOURCE_PAGE = "https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-N03-2025.html"

REGION_COLORS = {
    "okinawa": "#2A7F82",
    "miyako": "#D78F2B",
    "yaeyama": "#B45078",
    "other": "#8B98A5",
}

MAIN_MUNICIPALITIES = {
    "国頭村",
    "大宜味村",
    "東村",
    "今帰仁村",
    "本部町",
    "名護市",
    "恩納村",
    "宜野座村",
    "金武町",
    "読谷村",
    "嘉手納町",
    "北谷町",
    "沖縄市",
    "うるま市",
    "宜野湾市",
    "北中城村",
    "中城村",
    "浦添市",
    "西原町",
    "与那原町",
    "南風原町",
    "那覇市",
    "豊見城市",
    "南城市",
    "八重瀬町",
    "糸満市",
}
MIYAKO_MUNICIPALITIES = {"宮古島市", "多良間村"}
YAEYAMA_MUNICIPALITIES = {"石垣市", "竹富町", "与那国町"}


def choose_font() -> str:
    available = {f.name for f in font_manager.fontManager.ttflist}
    for candidate in ("Microsoft YaHei", "Yu Gothic", "SimHei", "MS Gothic"):
        if candidate in available:
            return candidate
    return "DejaVu Sans"


def download_geojson() -> dict:
    cache = Path(tempfile.gettempdir()) / "N03-20250101_47_GML.zip"
    if not cache.exists() or cache.stat().st_size < 1_000_000:
        urllib.request.urlretrieve(DATA_URL, cache)
    with zipfile.ZipFile(cache) as archive:
        raw = archive.read("N03-20250101_47.geojson")
    return json.loads(raw.decode("utf-8"))


def iter_polygons(geom):
    if isinstance(geom, Polygon):
        yield geom
    elif isinstance(geom, MultiPolygon):
        yield from geom.geoms
    elif isinstance(geom, GeometryCollection):
        for part in geom.geoms:
            yield from iter_polygons(part)


def region_for(name: str) -> str:
    if name in MAIN_MUNICIPALITIES:
        return "okinawa"
    if name in MIYAKO_MUNICIPALITIES:
        return "miyako"
    if name in YAEYAMA_MUNICIPALITIES:
        return "yaeyama"
    return "other"


def orient_for_d3(geom):
    """D3 spherical projections expect clockwise exterior rings."""
    if isinstance(geom, Polygon):
        return orient(geom, sign=-1.0)
    if isinstance(geom, MultiPolygon):
        return MultiPolygon([orient(part, sign=-1.0) for part in geom.geoms])
    if isinstance(geom, GeometryCollection):
        return GeometryCollection([orient_for_d3(part) for part in geom.geoms])
    return geom


def dissolve_municipalities(raw_geojson: dict) -> tuple[dict[str, object], dict]:
    grouped: dict[str, list] = defaultdict(list)
    for feature in raw_geojson["features"]:
        name = feature["properties"].get("N03_004") or "所属未定地"
        grouped[name].append(shape(feature["geometry"]))

    geometries = {}
    features = []
    for name, parts in sorted(grouped.items()):
        geom = unary_union(parts)
        geometries[name] = geom
        simplified = orient_for_d3(geom.simplify(0.002, preserve_topology=True))
        features.append(
            {
                "type": "Feature",
                "properties": {"name": name, "region": region_for(name)},
                "geometry": mapping(simplified),
            }
        )
    return geometries, {"type": "FeatureCollection", "features": features}


def draw_geometry(ax, geom, facecolor, edgecolor="#FFFFFF", lw=0.35, alpha=1.0):
    for poly in iter_polygons(geom):
        x, y = poly.exterior.xy
        ax.fill(x, y, facecolor=facecolor, edgecolor=edgecolor, linewidth=lw, alpha=alpha)
        for ring in poly.interiors:
            hx, hy = ring.xy
            ax.fill(hx, hy, facecolor=ax.get_facecolor(), edgecolor=edgecolor, linewidth=lw)


def draw_all(ax, geometries, extent, region_alpha=0.92, boundaries=True):
    xmin, xmax, ymin, ymax = extent
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_aspect(1 / math.cos(math.radians((ymin + ymax) / 2)))
    ax.set_facecolor("#EAF4F5")
    for name, geom in geometries.items():
        if geom.bounds[2] < xmin or geom.bounds[0] > xmax or geom.bounds[3] < ymin or geom.bounds[1] > ymax:
            continue
        region = region_for(name)
        draw_geometry(
            ax,
            geom,
            REGION_COLORS[region],
            edgecolor="#FFFFFF" if boundaries else REGION_COLORS[region],
            lw=0.36 if boundaries else 0.1,
            alpha=region_alpha if region != "other" else 0.55,
        )
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)


def panel_title(ax, title, subtitle=None):
    ax.text(
        0.02,
        0.98,
        title,
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=14,
        fontweight="bold",
        color="#173443",
        zorder=20,
    )
    if subtitle:
        ax.text(
            0.02,
            0.92,
            subtitle,
            transform=ax.transAxes,
            ha="left",
            va="top",
            fontsize=8.8,
            color="#48616D",
            zorder=20,
        )


def marker(ax, xy, number, color, status="solid", size=150):
    if status == "open":
        ax.scatter(*xy, s=size, facecolor="#FFFFFF", edgecolor=color, linewidth=2.0, zorder=10)
        text_color = color
    elif status == "half":
        ax.scatter(*xy, s=size, facecolor="#FFFFFF", edgecolor=color, linewidth=2.0, zorder=10)
        ax.scatter(*xy, s=size * 0.48, facecolor=color, edgecolor="none", zorder=11)
        text_color = "#FFFFFF"
    else:
        ax.scatter(*xy, s=size, facecolor=color, edgecolor="#FFFFFF", linewidth=1.2, zorder=10)
        text_color = "#FFFFFF"
    ax.text(*xy, str(number), ha="center", va="center", fontsize=8.5, fontweight="bold", color=text_color, zorder=12)


def callout(ax, xy, xytext, text, color, align="left"):
    ax.annotate(
        text,
        xy=xy,
        xytext=xytext,
        ha=align,
        va="center",
        fontsize=8.4,
        color="#173443",
        arrowprops=dict(arrowstyle="-", color=color, lw=1.1, shrinkA=3, shrinkB=4),
        bbox=dict(boxstyle="round,pad=0.35", facecolor="#FFFFFF", edgecolor=color, linewidth=0.8, alpha=0.96),
        zorder=15,
    )


def draw_overview(ax, geometries):
    draw_all(ax, geometries, (122.55, 131.55, 23.75, 27.2), boundaries=False)
    panel_title(ax, "全域定位", "岛链东西跨度很大；以下三幅为等比例局部放大")

    boxes = [
        (127.48, 25.98, 1.00, 1.03, "冲绳本岛", REGION_COLORS["okinawa"]),
        (124.92, 24.55, 0.82, 0.62, "宫古群岛", REGION_COLORS["miyako"]),
        (122.75, 23.90, 1.75, 0.82, "八重山群岛", REGION_COLORS["yaeyama"]),
    ]
    for x, y, w, h, label, color in boxes:
        ax.add_patch(Rectangle((x, y), w, h, fill=False, edgecolor=color, linewidth=1.6, linestyle=(0, (4, 3)), zorder=8))
        ax.text(x + w / 2, y + h + 0.06, label, ha="center", va="bottom", fontsize=9.5, fontweight="bold", color="#173443")

    ax.text(126.45, 26.17, "冲绳群岛\n（含久米、庆良间等）", ha="center", va="center", fontsize=8.2, color="#48616D")
    ax.text(131.22, 25.56, "大东群岛", ha="center", va="center", fontsize=8.2, color="#48616D")
    ax.annotate(
        "研究重心向西南延伸\n旧基地争议  →  新部署争议",
        xy=(124.0, 24.55),
        xytext=(127.15, 24.50),
        arrowprops=dict(arrowstyle="->", color="#173443", lw=1.5),
        ha="center",
        va="center",
        fontsize=9.2,
        color="#173443",
        bbox=dict(boxstyle="round,pad=0.45", facecolor="#FFFFFF", edgecolor="#B8CBD1", linewidth=0.8),
        zorder=12,
    )
    ax.text(122.70, 24.18, "← 台湾方向\n与那国—台湾约111km", ha="left", va="center", fontsize=8.2, color="#48616D")


def draw_main_island(ax, geometries):
    draw_all(ax, geometries, (127.56, 128.68, 26.05, 26.92))
    panel_title(ax, "A  冲绳本岛", "既有美军基地：环境程序、损害认定、赔偿与全县动员")

    items = [
        (1, (128.20, 26.64), (128.48, 26.76), "高江／山原\n森林生态 × 直升机坪抗争", "half"),
        (2, (128.05, 26.52), (128.48, 26.58), "边野古／大浦湾\n生态证据 → 环评、诉讼、国际倡议", "solid"),
        (3, (127.77, 26.36), (128.45, 26.42), "嘉手纳／普天间\n噪音损害 → 认定与赔偿；未停止运行", "solid"),
        (4, (127.83, 26.31), (128.45, 26.30), "泡濑\n湿地与公金诉讼；两轮结果相反", "solid"),
        (5, (127.68, 26.21), (128.42, 26.18), "那霸\n全县网络、女性／人权、公投与行政入口", "solid"),
        (6, (127.89, 26.30), (128.45, 26.08), "胜连／宇流麻\n导弹部署 → 生命安全与前线化", "half"),
    ]
    for number, xy, xytext, text, status in items:
        marker(ax, xy, number, REGION_COLORS["okinawa"], status=status, size=122)
        callout(ax, xy, xytext, text, REGION_COLORS["okinawa"])


def draw_miyako(ax, geometries):
    draw_all(ax, geometries, (124.95, 125.68, 24.60, 25.12))
    panel_title(ax, "B  宫古群岛", "新部署如何被翻译成水源与生活条件问题")
    marker(ax, (125.30, 24.79), 7, REGION_COLORS["miyako"], status="half", size=125)
    callout(
        ax,
        (125.30, 24.79),
        (125.55, 24.88),
        "宫古岛\n自卫队／导弹部署 → 地下水、生命安全\n重点补：陈情、会报、水源材料",
        REGION_COLORS["miyako"],
    )
    ax.text(125.18, 24.70, "下地岛", fontsize=7.5, color="#48616D")


def draw_yaeyama(ax, geometries):
    draw_all(ax, geometries, (122.78, 124.36, 23.96, 24.68))
    panel_title(ax, "C  八重山群岛", "同为新部署：石垣争决定权，与那国争前线化与撤离")
    marker(ax, (124.15, 24.34), 8, REGION_COLORS["yaeyama"], status="half", size=125)
    callout(
        ax,
        (124.15, 24.34),
        (124.08, 24.10),
        "石垣岛\n住民投票、地方自治、诉讼",
        REGION_COLORS["yaeyama"],
        align="center",
    )
    marker(ax, (122.99, 24.46), 9, REGION_COLORS["yaeyama"], status="open", size=125)
    callout(
        ax,
        (122.99, 24.46),
        (123.18, 24.16),
        "与那国岛\n台湾邻近、前线化、撤离、公投\n重点补：町议会与行动组织材料",
        REGION_COLORS["yaeyama"],
    )
    ax.text(123.78, 24.30, "西表岛", fontsize=7.7, color="#48616D", ha="center")
    ax.text(123.99, 24.23, "竹富诸岛", fontsize=7.7, color="#48616D", ha="center")


def add_footer(fig):
    legend_x = 0.055
    legend_y = 0.060
    fig.text(legend_x, legend_y + 0.028, "资料状态", fontsize=8.5, fontweight="bold", color="#173443")
    for i, (fillstyle, label) in enumerate(
        [
            ("full", "线上证据较深"),
            ("left", "已有证据，仍需地方材料"),
            ("none", "地方一手材料是关键缺口"),
        ]
    ):
        x = legend_x + 0.095 * i
        fig.add_artist(
            plt.Line2D(
                [x],
                [legend_y],
                marker="o",
                markersize=6.5,
                markerfacecolor="#2A7F82",
                markeredgecolor="#2A7F82",
                fillstyle=fillstyle,
                linestyle="none",
                transform=fig.transFigure,
            )
        )
        fig.text(x + 0.010, legend_y, label, fontsize=7.6, color="#48616D", va="center")

    fig.text(
        0.39,
        0.060,
        "读图主线：本岛的既有基地争议更多进入环境程序、损害认定与赔偿；先岛的新部署争议更多进入水源、决定权、前线化与撤离。",
        fontsize=8.5,
        color="#173443",
        ha="left",
        va="center",
    )
    fig.text(
        0.055,
        0.027,
        "底图：日本国土数值情報 N03 行政区域（2025）。研究标记为地点近似位置，不表示设施边界；文字表示本项目当前研究重点，不表示组织数量或行动强度。",
        fontsize=7.3,
        color="#617985",
        ha="left",
    )


def make_png(geometries):
    plt.rcParams["font.family"] = choose_font()
    plt.rcParams["axes.unicode_minus"] = False
    fig = plt.figure(figsize=(16, 14), dpi=180, facecolor="#F7FAFB")
    gs = fig.add_gridspec(
        3,
        2,
        width_ratios=[1.12, 1.0],
        height_ratios=[1.15, 1.0, 1.0],
        left=0.045,
        right=0.975,
        top=0.86,
        bottom=0.11,
        wspace=0.07,
        hspace=0.09,
    )
    ax_overview = fig.add_subplot(gs[0, :])
    ax_main = fig.add_subplot(gs[1:, 0])
    ax_miyako = fig.add_subplot(gs[1, 1])
    ax_yaeyama = fig.add_subplot(gs[2, 1])

    fig.text(0.05, 0.95, "冲绳不是一座岛", fontsize=25, fontweight="bold", color="#173443", va="top")
    fig.text(
        0.05,
        0.905,
        "实际地理位置 × 本项目当前研究重点｜从冲绳本岛的既有基地，到先岛群岛的新部署",
        fontsize=12.5,
        color="#48616D",
        va="top",
    )

    draw_overview(ax_overview, geometries)
    draw_main_island(ax_main, geometries)
    draw_miyako(ax_miyako, geometries)
    draw_yaeyama(ax_yaeyama, geometries)
    add_footer(fig)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(PNG_PATH, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)


def inject_geojson(fragment_path: Path, geojson: dict):
    token = "/*__OKINAWA_GEOJSON__*/"
    content = fragment_path.read_text(encoding="utf-8")
    payload = json.dumps(geojson, ensure_ascii=False, separators=(",", ":"))
    if token in content:
        content = content.replace(token, payload)
    else:
        start_marker = "      const geo = "
        end_marker = ";\n      const svg ="
        start = content.find(start_marker)
        end = content.find(end_marker, start)
        if start < 0 or end < 0:
            raise RuntimeError(f"GeoJSON insertion markers missing from {fragment_path}")
        content = content[: start + len(start_marker)] + payload + content[end:]
    fragment_path.write_text(content, encoding="utf-8", newline="\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fragment", type=Path, help="Optional HTML fragment containing the GeoJSON token")
    args = parser.parse_args()

    raw = download_geojson()
    geometries, simplified = dissolve_municipalities(raw)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    GEOJSON_PATH.write_text(json.dumps(simplified, ensure_ascii=False), encoding="utf-8", newline="\n")
    make_png(geometries)
    if args.fragment:
        inject_geojson(args.fragment, simplified)
    print(PNG_PATH)
    print(GEOJSON_PATH)
    print(SOURCE_PAGE)


if __name__ == "__main__":
    main()
