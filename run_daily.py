#!/usr/bin/env python3
"""Daily pipeline: scrape GitHub Trending → chart → Xiaohongshu draft.

Selection rule
--------------
- Chart: Top ``--top-n`` repos by ``stars_today`` (default 10).
- Note focus: the #1 repo by ``stars_today`` (hottest today).
  Override with ``--pick N`` (1-based rank after sort) if needed.

Dates/paths use Asia/Shanghai.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from fetch_trending_chart import TRENDING_URL, fetch_trending, plot_chart

ROOT = Path(__file__).resolve().parent
TZ = ZoneInfo("Asia/Shanghai")


def today_str() -> str:
    return datetime.now(TZ).strftime("%Y-%m-%d")


def sort_by_stars_today(repos: list[dict]) -> list[dict]:
    return sorted(repos, key=lambda r: r["stars_today"], reverse=True)


def repo_url(repo: dict) -> str:
    href = (repo.get("href") or repo.get("name") or "").strip("/")
    return f"https://github.com/{href}"


def why_hot_one_liner(repo: dict, rank: int, total_on_page: int) -> str:
    """Short factual hook from scrape fields only — no invented vibes."""
    name = repo["name"]
    n = repo["stars_today"]
    lang = repo.get("language") or "多语言"
    desc = (repo.get("description") or "").strip()
    bits = [f"今日涨星榜第 {rank}/{total_on_page}", f"+{n:,} ⭐", lang]
    if desc:
        # keep one line tight for cover
        short = desc if len(desc) <= 48 else desc[:45] + "…"
        bits.append(short)
    return " · ".join(bits)


def cover_title(repo: dict) -> str:
    name = repo["name"]
    n = repo["stars_today"]
    return f"今日最热：{name} 涨了 +{n:,} ⭐"


def build_draft(repo: dict, rank: int, total_on_page: int, chart_name: str, date: str) -> str:
    name = repo["name"]
    url = repo_url(repo)
    lang = repo.get("language") or "n/a"
    stars_today = repo["stars_today"]
    total_stars = repo["total_stars"]
    desc = (repo.get("description") or "").strip() or "（页面未提供一句话描述）"
    why = why_hot_one_liner(repo, rank, total_on_page)
    title = cover_title(repo)

    # Geek reproducible breakdown — short lines, not a news list.
    body = f"""# {title}

> {why}

配图：`{chart_name}`（今日涨星 Top 榜横向柱状图）

日期：{date}（Asia/Shanghai） · 数据：github.com/trending?since=daily

---

## 今天拆谁

**{name}**

- 链接：{url}
- 语言：{lang}
- 今日涨星：+{stars_today:,} ⭐
- 总星标：{total_stars:,} ⭐
- 一句话：{desc}

---

## 它是干什么的

从 Trending 页面公开描述出发：

> {desc}

自己打开 README / About 核对一遍再转发——脚本不编造功能细节。

---

## 为什么突然火

可复现的事实（本次抓取）：

1. 它在 daily Trending 上按 `stars_today` 排到 **#{rank}**（同页共 {total_on_page} 仓）
2. 单日增量 **+{stars_today:,}**，相对总量 {total_stars:,} 很显眼
3. 语言标签：**{lang}**

推断（标注为推断，非官方声明）：

- 榜单热度来自「今日星标增量」，不是总星数；短时曝光 / 新版本 / 话题共振都可能推高 `stars_today`
- 要验证原因：看近 24–48h 的 Release、置顶 Issue、社交转发——以仓库公开页为准

---

## 你怎么自己试用

```bash
# 1) 打开仓库
# {url}

# 2) 本机重跑整条流水线（出图 + 小红书草稿）
cd github-trending-radar
python3 -m pip install -r requirements.txt
python3 run_daily.py
# 产物：output/{date}/ 与 output/latest/
```

试用该仓本身：优先读 README 的 Quick Start / Install；没有就 clone 后按官方文档来。不要跑来源不明的一键脚本。

---

## 涨星一图看懂

见同目录 `{chart_name}`。

读图规则：横轴是「今日涨星」，不是总星；条越长 = 今天越热。

---

## 建议话题标签

#GitHub #Trending #开源 #极客日常 #程序员 #今日涨星 #开源项目 #效率工具
"""
    return body


def write_outputs(
    repos: list[dict],
    out_dir: Path,
    top_n: int,
    pick: int,
    since: str,
    language: str,
) -> dict:
    ranked = sort_by_stars_today(repos)
    if not ranked:
        raise RuntimeError("No repos scraped.")

    pick_idx = pick - 1
    if pick_idx < 0 or pick_idx >= len(ranked):
        raise RuntimeError(f"--pick {pick} out of range (have {len(ranked)} repos).")

    focus = ranked[pick_idx]
    date = today_str()

    chart_name = "chart.png"
    chart_path = out_dir / chart_name
    title = f"GitHub 今日涨星 Top · 今日新增（不是总星）  ·  {date}"
    if language:
        title += f"  ({language})"
    plot_chart(ranked, chart_path, top_n=top_n, title=title)

    draft = build_draft(focus, rank=pick, total_on_page=len(ranked), chart_name=chart_name, date=date)
    draft_path = out_dir / "xhs-draft.md"
    draft_path.write_text(draft, encoding="utf-8")

    meta = {
        "date": date,
        "timezone": "Asia/Shanghai",
        "since": since,
        "language": language or None,
        "top_n_chart": top_n,
        "pick_rank": pick,
        "selection_rule": "hottest by stars_today; note uses --pick (default #1); chart uses top-n",
        "focus": {
            "name": focus["name"],
            "url": repo_url(focus),
            "stars_today": focus["stars_today"],
            "total_stars": focus["total_stars"],
            "language": focus.get("language") or "",
            "description": focus.get("description") or "",
        },
        "top": [
            {
                "rank": i,
                "name": r["name"],
                "stars_today": r["stars_today"],
                "total_stars": r["total_stars"],
                "language": r.get("language") or "",
            }
            for i, r in enumerate(ranked[:top_n], 1)
        ],
        "files": [chart_name, "xhs-draft.md", "meta.json"],
    }
    meta_path = out_dir / "meta.json"
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return meta


def sync_latest(dated_dir: Path, latest_dir: Path) -> None:
    if latest_dir.exists():
        shutil.rmtree(latest_dir)
    shutil.copytree(dated_dir, latest_dir)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--top-n",
        type=int,
        default=10,
        help="Chart bar count by stars_today (default 10)",
    )
    parser.add_argument(
        "--pick",
        type=int,
        default=1,
        help="Which rank (1-based) to feature in the Xiaohongshu draft (default 1 = hottest)",
    )
    parser.add_argument("--since", default="daily", choices=["daily", "weekly", "monthly"])
    parser.add_argument("--language", default="", help="Optional language slug, e.g. python")
    parser.add_argument(
        "--output-root",
        type=Path,
        default=ROOT / "output",
        help="Root for dated + latest folders (default: ./output)",
    )
    args = parser.parse_args()

    date = today_str()
    dated = args.output_root / date
    latest = args.output_root / "latest"
    dated.mkdir(parents=True, exist_ok=True)

    print(f"Fetching {TRENDING_URL}?since={args.since} ...", flush=True)
    repos = fetch_trending(since=args.since, language=args.language)
    print(f"Parsed {len(repos)} repositories.", flush=True)

    ranked = sort_by_stars_today(repos)
    for i, r in enumerate(ranked[:5], 1):
        print(
            f"  {i}. {r['name']}: +{r['stars_today']:,} today "
            f"(total {r['total_stars']:,}) [{r['language'] or 'n/a'}]",
            flush=True,
        )

    meta = write_outputs(
        repos,
        out_dir=dated,
        top_n=args.top_n,
        pick=args.pick,
        since=args.since,
        language=args.language,
    )
    sync_latest(dated, latest)

    # Convenience root chart (also gitignored via *.png)
    root_chart = ROOT / "trending_stars_today.png"
    shutil.copy2(dated / "chart.png", root_chart)

    print(f"Focus (#{meta['pick_rank']}): {meta['focus']['name']} +{meta['focus']['stars_today']:,}", flush=True)
    print(f"Wrote: {dated}/", flush=True)
    print(f"  - chart.png", flush=True)
    print(f"  - xhs-draft.md", flush=True)
    print(f"  - meta.json", flush=True)
    print(f"Synced: {latest}/", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
