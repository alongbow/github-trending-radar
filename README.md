# GitHub Trending Radar

抓取 **GitHub Trending（daily）** 当日榜，按「今日涨星」画横向柱状图；README 内嵌可直接粘贴给 Agent 的日更 Prompt。

> 不编造 stars / 涨粉 / 变现数字。示例图仅作 artifact；请自行重跑脚本拿当日真实数据。

---

## 它做什么

1. 请求公开页 `https://github.com/trending?since=daily`（无需 GitHub API token）
2. 解析每个仓库的名称、今日星标增量、总星标、语言、描述
3. 输出 PNG 横向柱状图（默认 Top 10）

可选：把下方 **Agent Prompt** 整段丢给 Agent，让它顺带快读 Top 仓、写分享草稿。

---

## 快速开始

```bash
git clone https://github.com/alongbow/github-trending-radar.git
cd github-trending-radar
python3 -m pip install -r requirements.txt
python3 fetch_trending_chart.py
```

### 可选参数

| 参数 | 说明 | 默认 |
|------|------|------|
| `--top N` | 柱状图条数 | `10` |
| `--since daily\|weekly\|monthly` | 时间窗口 | `daily` |
| `--language python` | 语言 slug（空=全语言） | 空 |
| `-o path.png` | 输出路径 | `trending_stars_today.png` |

示例：

```bash
python3 fetch_trending_chart.py --top 10 --since daily -o out.png
python3 fetch_trending_chart.py --language python --top 15
```

### 依赖

见 `requirements.txt`：`requests`、`beautifulsoup4`、`matplotlib`。

### 示例产物

`examples/sample_chart.png` — 某次真实抓取的示例图（数字会过期，请重跑）。  
`examples/xhs-note.md` — 分享草稿示例，非独立 Prompt 产品。

---

## 数据源说明

- 主路径：抓取公开 HTML `https://github.com/trending`
- 若页面结构变更或请求被拦：脚本会报错退出；**不要**手工填假数字
- 请礼貌限速、标明 User-Agent（脚本已内置研究用途 UA）

---

## Agent Prompt（可直接粘贴）

> 把 `{{日期}}` / `{{TopN}}` / `{{输出目录}}` 换成你的值即可。

### 目标

你是我的「GitHub Trending 日更助手」。今天是 **{{日期}}**（时区 Asia/Shanghai）。

请你：

1. 抓取 GitHub Trending（daily）当日榜
2. 自动阅读 / 分析 **上升最快**（stars today 最高）的仓库
3. 产出可读图表 + 可分享的短笔记草稿

**不要**编造涨粉、变现、带货数字；只基于公开页面与仓库 README / About 的事实。

### 步骤（按顺序执行）

#### Step 1 — 抓取榜单

- 打开：`https://github.com/trending?since=daily`
- 解析每个 `article.Box-row`：仓库名、今日星标增量、总星标、语言、一句话描述
- 按 `stars today` 降序排序，取 Top **{{TopN}}**（默认 10）
- 若页面结构变了或请求被拦：说明原因，并给出可复现的备用方案（本地脚本 / `gh` / RSS），**不要编数据**

也可直接跑本仓库脚本：

```bash
cd /path/to/github-trending-radar
python3 fetch_trending_chart.py --top {{TopN}} -o {{输出目录}}/chart.png
```

#### Step 2 — 快速读仓（每个 Top 仓 ≤ 2 分钟）

对每个 Top 仓，只读公开信息：

- About / 首段 README
- 最近 1–3 个 release 或高互动 Issue/PR 标题（如有）
- 语言栈与「为什么今天会爆」的合理假设（标注为推断）

输出每个仓的三行卡：

```
仓库: owner/name
今日: +N ⭐ | 总量: M | 语言: Lang
一句话: …
为何上升(推断): …  | 证据: …
```

#### Step 3 — 出图

- 用横向柱状图画 Top N 的「今日星标」
- 标题含日期与 `since=daily`
- 保存到：`{{输出目录}}/chart.png`（或项目约定路径）
- 图上数字用千分位，仓库名完整可读

#### Step 4 — 分享草稿（中文，小红书风）

写一版 **短、可扫、极客向** 的笔记草稿，结构：

1. 痛点（每天刷 Trending 太慢）
2. Prompt / 流水线一句话（怎么让 Agent 日更）
3. 今日 Top 亮点（3–5 个，含真实 `+N today`）
4. 复现方式（命令 / 脚本路径）
5. 结尾 CTA（收藏 / 私信要 Prompt）

约束：

- 不写虚假收益、不暗示「跟这个能赚钱」
- 不剧透未公开漏洞 / 不教人做恶意逆向
- 数字必须来自本次抓取；拿不到就写「抓取失败」

### 硬性约束

| 项 | 要求 |
|----|------|
| 数据源 | 仅公开 GitHub Trending + 目标仓公开页 |
| 真实性 | 禁止虚构 stars / 描述 / 作者言论 |
| 频率 | 建议每日同一时段跑一次，避免狂刷 |
| User-Agent | 标明研究/个人脚本用途，礼貌限速 |
| 输出语言 | 分析与分享稿用中文；仓库名保持英文原样 |

### 输出格式（必须严格遵守）

#### A. 今日榜单表

| # | 仓库 | +今日 | 总量 | 语言 | 一句话 |
|---|------|------|------|------|--------|
| 1 | … | … | … | … | … |

#### B. 上升原因速览（Top 3–5）

对每个：事实 → 推断 → 证据链接（Trending / README）

#### C. 图表

- 文件路径：`…/chart.png`
- 一句话读图结论

#### D. 分享草稿

完整正文（含建议标题 + 3–8 个标签）

#### E. 复现清单

```bash
cd /path/to/github-trending-radar
python3 fetch_trending_chart.py --top {{TopN}}
```

### 可选参数（你可在开头声明）

- `since`: daily | weekly | monthly（本任务默认 daily）
- `language`: 空 = 全语言；或 `python` / `typescript` 等
- `top_n`: 默认 10
- `tone`: 极客冷静 / 轻松吐槽（默认极客冷静）

### 验收标准

- [ ] Top N 数字与当日 Trending 页面一致（或说明偏差原因）
- [ ] 有 `chart.png` 且文件时间戳为本次运行
- [ ] 分享草稿可直接粘贴发小红书（仍建议人工过一眼）
- [ ] 无虚假变现 / 无恶意利用指引

---

## 目录结构

```
github-trending-radar/
├── fetch_trending_chart.py   # 抓取 + 出图
├── requirements.txt
├── README.md                 # 本文件（含 Agent Prompt）
├── LICENSE                   # MIT
├── .gitignore
└── examples/
    ├── sample_chart.png      # 示例图（可选）
    └── xhs-note.md           # 分享草稿示例
```

---

## License

MIT — 见 [LICENSE](LICENSE)。
