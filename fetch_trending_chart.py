#!/usr/bin/env python3
"""Fetch GitHub Trending (daily) and plot a bar chart of stars gained today."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup

TRENDING_URL = "https://github.com/trending"
DEFAULT_OUT = Path(__file__).resolve().parent / "trending_stars_today.png"
USER_AGENT = "GitHubTrendingPoC/1.0 (+https://github.com/trending; research)"


def parse_int(text: str) -> int:
    digits = re.sub(r"[^\d]", "", text or "")
    return int(digits) if digits else 0


def fetch_trending(since: str = "daily", language: str = "", timeout: int = 30) -> list[dict]:
    """Scrape https://github.com/trending for today's trending repositories."""
    params = {"since": since}
    url = TRENDING_URL if not language else f"{TRENDING_URL}/{language}"
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "en-US,en;q=0.9",
    }
    resp = requests.get(url, params=params, headers=headers, timeout=timeout)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    articles = soup.select("article.Box-row")
    if not articles:
        raise RuntimeError(
            "No trending rows found — GitHub HTML may have changed, or the page was blocked."
        )

    repos: list[dict] = []
    for article in articles:
        h2 = article.select_one("h2 a")
        if not h2:
            continue
        href = (h2.get("href") or "").strip("/")
        name = " ".join(h2.get_text().split()).replace(" / ", "/")
        if not name and href:
            name = href

        total_stars = 0
        for link in article.select("a"):
            link_href = link.get("href") or ""
            if link_href.endswith("/stargazers"):
                total_stars = parse_int(link.get_text())
                break

        body = article.get_text(" ", strip=True)
        m = re.search(r"([\d,]+)\s+stars?\s+today", body, re.I)
        stars_today = parse_int(m.group(1)) if m else 0

        lang_el = article.select_one("[itemprop=programmingLanguage]")
        lang = lang_el.get_text(strip=True) if lang_el else ""

        desc_el = article.select_one("p")
        desc = desc_el.get_text(strip=True) if desc_el else ""

        repos.append(
            {
                "name": name,
                "href": href,
                "stars_today": stars_today,
                "total_stars": total_stars,
                "language": lang,
                "description": desc,
            }
        )
    return repos


def format_stars(n: int) -> str:
    """Compact star delta for chart labels, e.g. +1.2k / +856."""
    if n >= 1000:
        k = n / 1000
        text = f"{k:.1f}k" if k < 10 else f"{k:.0f}k"
        if text.endswith(".0k"):
            text = text.replace(".0k", "k")
        return f"+{text}"
    return f"+{n}"


def format_today_label(n: int) -> str:
    """Bar label: 今日 +xx (explicitly today's gain, not total stars)."""
    return f"今日 {format_stars(n)}"


def _rank_colors(n: int) -> list[str]:
    """Light blue → indigo gradient; top rank (index 0 before reverse) darkest."""
    # matplotlib LinearSegmentedColormap without importing colors module name clutter
    from matplotlib.colors import LinearSegmentedColormap

    # indigo (dark/saturated) → light blue; index 0 = top rank = darkest
    cmap = LinearSegmentedColormap.from_list(
        "trending_blue",
        ["#2a3f7a", "#3d5a9e", "#6b8fd4", "#c5d8f0"],
    )
    return [cmap(i / max(n - 1, 1)) for i in range(n)]


def _setup_cjk_font() -> None:
    """Prefer Noto Sans CJK SC so axis labels with Chinese render correctly."""
    from matplotlib import font_manager

    preferred = [
        "Noto Sans CJK SC",
        "Noto Sans CJK JP",
        "Noto Serif CJK SC",
        "Source Han Sans SC",
        "WenQuanYi Micro Hei",
        "DejaVu Sans",
    ]
    available = {f.name for f in font_manager.fontManager.ttflist}
    for name in preferred:
        if name in available:
            plt.rcParams["font.sans-serif"] = [name, "DejaVu Sans"]
            plt.rcParams["axes.unicode_minus"] = False
            return


def plot_chart(repos: list[dict], out_path: Path, top_n: int, title: str) -> Path:
    _setup_cjk_font()
    top = sorted(repos, key=lambda r: r["stars_today"], reverse=True)[:top_n]
    if not top:
        raise RuntimeError("No repos to plot.")

    labels = [r["name"] for r in top]
    values = [r["stars_today"] for r in top]
    colors = _rank_colors(len(top))  # index 0 = top rank = darkest

    # Horizontal bar chart: reverse so top rank sits at the top of the plot
    labels = list(reversed(labels))
    values = list(reversed(values))
    colors = list(reversed(colors))

    fig_h = max(4.2, 0.48 * len(labels) + 1.8)
    fig, ax = plt.subplots(figsize=(11, fig_h), facecolor="#ffffff")
    ax.set_facecolor("#fafbfc")

    bars = ax.barh(
        labels,
        values,
        color=colors,
        edgecolor="none",
        height=0.72,
        zorder=3,
    )
    ax.bar_label(
        bars,
        labels=[format_today_label(v) for v in values],
        padding=6,
        fontsize=9,
        color="#334155",
        fontweight="normal",
    )

    # Explicitly: today's NEW stars, NOT total stars
    ax.set_xlabel("今日新增 Stars（不是总星）", fontsize=11, color="#475569", labelpad=10)
    ax.set_title(title, fontsize=14, fontweight="bold", color="#0f172a", pad=14, loc="left")
    ax.set_xlim(0, max(values) * 1.22 if values else 1)

    # Thin light-gray grid on x-axis only
    ax.xaxis.grid(True, color="#e2e8f0", linewidth=0.8, linestyle="-", zorder=0)
    ax.yaxis.grid(False)
    ax.set_axisbelow(True)

    # Clean minimal frame: remove spines clutter
    for spine in ("top", "right", "left"):
        ax.spines[spine].set_visible(False)
    ax.spines["bottom"].set_color("#cbd5e1")
    ax.spines["bottom"].set_linewidth(0.8)

    ax.tick_params(axis="y", length=0, labelsize=10, colors="#1e293b", pad=4)
    ax.tick_params(axis="x", length=0, labelsize=8, colors="#94a3b8")
    ax.yaxis.set_tick_params(which="both", left=False)

    # Subtle footer
    fig.text(
        0.99,
        0.01,
        "source: github.com/trending",
        ha="right",
        va="bottom",
        fontsize=7,
        color="#94a3b8",
    )

    fig.tight_layout(rect=(0, 0.03, 1, 1))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    return out_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--top", type=int, default=10, help="Top N repos by stars today (default 10)")
    parser.add_argument("--since", default="daily", choices=["daily", "weekly", "monthly"])
    parser.add_argument("--language", default="", help="Optional language slug, e.g. python")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=DEFAULT_OUT,
        help=f"PNG path (default: {DEFAULT_OUT.name})",
    )
    args = parser.parse_args()

    print(f"Fetching {TRENDING_URL}?since={args.since} ...", flush=True)
    repos = fetch_trending(since=args.since, language=args.language)
    print(f"Parsed {len(repos)} repositories.", flush=True)
    for i, r in enumerate(sorted(repos, key=lambda x: x["stars_today"], reverse=True)[:5], 1):
        print(
            f"  {i}. {r['name']}: +{r['stars_today']:,} today "
            f"(total {r['total_stars']:,}) [{r['language'] or 'n/a'}]",
            flush=True,
        )

    from datetime import datetime
    from zoneinfo import ZoneInfo

    today = datetime.now(ZoneInfo("Asia/Shanghai")).strftime("%Y-%m-%d")
    title = f"GitHub 今日涨星 Top · 今日新增（不是总星）  ·  {today}"
    if args.language:
        title += f"  ({args.language})"
    path = plot_chart(repos, args.output, top_n=args.top, title=title)
    print(f"Wrote chart: {path}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
