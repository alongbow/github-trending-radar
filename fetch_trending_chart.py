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


def plot_chart(repos: list[dict], out_path: Path, top_n: int, title: str) -> Path:
    top = sorted(repos, key=lambda r: r["stars_today"], reverse=True)[:top_n]
    if not top:
        raise RuntimeError("No repos to plot.")

    labels = [r["name"] for r in top]
    values = [r["stars_today"] for r in top]
    # Horizontal bar chart: easiest to read long repo names
    labels = list(reversed(labels))
    values = list(reversed(values))

    fig_h = max(4.0, 0.45 * len(labels) + 1.5)
    fig, ax = plt.subplots(figsize=(10, fig_h))
    bars = ax.barh(labels, values, color="#2da44e", edgecolor="#1a7f37", linewidth=0.5)
    ax.bar_label(bars, labels=[f"{v:,}" for v in values], padding=4, fontsize=9)
    ax.set_xlabel("Stars gained today")
    ax.set_title(title)
    ax.set_xlim(0, max(values) * 1.18 if values else 1)
    ax.grid(axis="x", linestyle="--", alpha=0.35)
    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
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

    title = f"GitHub Trending — stars today (since={args.since}"
    if args.language:
        title += f", lang={args.language}"
    title += ")"
    path = plot_chart(repos, args.output, top_n=args.top, title=title)
    print(f"Wrote chart: {path}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
