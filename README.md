# GitHub Trending Radar

每日自动：抓取 **GitHub Trending（daily）** → 按「今日涨星」出图 → 挑最热仓写一版**可复现、极客向**的小红书草稿（本地 Markdown，不登录小红书）。

> 不编造 stars / 涨粉 / 变现数字。`examples/` 里的图和稿仅作 artifact；请自行重跑拿当日真实数据。

---

## 它做什么

1. 请求公开页 `https://github.com/trending?since=daily`（无需 GitHub API token）
2. 解析名称、今日星标增量、总星标、语言、描述
3. **选型规则**：按 `stars_today` 降序；**图表**画 Top N（默认 10）；**小红书草稿**默认拆解榜一（可用 `--pick` 改）
4. 写入 `output/YYYY-MM-DD/`（Asia/Shanghai）并同步 `output/latest/`：`chart.png` + `xhs-draft.md` + `meta.json`

---

## 一键跑完整流水线（推荐）

```bash
git clone https://github.com/alongbow/github-trending-radar.git
cd github-trending-radar
python3 -m pip install -r requirements.txt
python3 run_daily.py
```

产物目录示例：

```
output/2026-10-16/
├── chart.png        # 今日涨星横向柱状图（light-clean）
├── xhs-draft.md     # 小红书可粘贴草稿
└── meta.json        # 结构化元数据（榜单切片 + 选型）
output/latest/       # 同上，始终指向最近一次
```

### `run_daily.py` 参数

| 参数 | 说明 | 默认 |
|------|------|------|
| `--top-n N` | 柱状图条数（按 stars_today） | `10` |
| `--pick N` | 笔记拆解第几名（1 = 最热） | `1` |
| `--since daily\|weekly\|monthly` | 时间窗口 | `daily` |
| `--language python` | 语言 slug（空=全语言） | 空 |
| `--output-root DIR` | 输出根目录 | `./output` |

示例：

```bash
python3 run_daily.py --top-n 10 --pick 1
python3 run_daily.py --language python --top-n 15
```

草稿固定章节（短句、可复现，不是新闻列表）：

- 今天拆谁
- 它是干什么的
- 为什么突然火
- 你怎么自己试用
- 涨星一图看懂

文末附建议话题标签。脚本**只写本地文件**，不调用小红书 API。

---

## 只出图（旧入口仍可用）

```bash
python3 fetch_trending_chart.py
python3 fetch_trending_chart.py --top 10 --since daily -o out.png
python3 fetch_trending_chart.py --language python --top 15
```

| 参数 | 说明 | 默认 |
|------|------|------|
| `--top N` | 柱状图条数 | `10` |
| `--since daily\|weekly\|monthly` | 时间窗口 | `daily` |
| `--language python` | 语言 slug | 空 |
| `-o path.png` | 输出路径 | `trending_stars_today.png` |

### 依赖

见 `requirements.txt`：`requests`、`beautifulsoup4`、`matplotlib`（无新增大框架）。

### 示例产物

- `examples/sample_chart.png` — 某次真实抓取示例图（数字会过期）
- `examples/xhs-note.md` — 旧版分享草稿示例；**日更请以 `run_daily.py` 生成的 `xhs-draft.md` 为准**

---

## 数据源说明

- 主路径：抓取公开 HTML `https://github.com/trending`
- 若页面结构变更或请求被拦：脚本报错退出；**不要**手工填假数字
- 请礼貌限速、标明 User-Agent（脚本已内置研究用途 UA）
- 日期与输出目录名使用 **Asia/Shanghai**

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

也可直接跑本仓库流水线：

```bash
cd /path/to/github-trending-radar
python3 run_daily.py --top-n {{TopN}}
# 或只要图：
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
- 保存到：`{{输出目录}}/chart.png`（或 `output/YYYY-MM-DD/chart.png`）
- 图上数字用千分位，仓库名完整可读

#### Step 4 — 分享草稿（中文，小红书风 · 极客可复现）

优先用流水线生成的 `xhs-draft.md`；若手写，结构固定为：

1. 封面钩子 + 一行为什么热
2. 今天拆谁（链接 / 语言 / +今日 / 总量 / 描述）
3. 它是干什么的
4. 为什么突然火（事实 + 标注推断）
5. 你怎么自己试用（命令可复现）
6. 涨星一图看懂
7. 建议话题标签

约束：

- 不写虚假收益、不暗示「跟这个能赚钱」
- 不剧透未公开漏洞 / 不教人做恶意逆向
- 数字必须来自本次抓取；拿不到就写「抓取失败」
- 语气：极客冷静、短句、可复现拆解，**不是**新闻聚合列表

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

完整正文（含建议标题 + 标签）；推荐章节见上文 Step 4

#### E. 复现清单

```bash
cd /path/to/github-trending-radar
python3 run_daily.py --top-n {{TopN}}
```

### 可选参数（你可在开头声明）

- `since`: daily | weekly | monthly（本任务默认 daily）
- `language`: 空 = 全语言；或 `python` / `typescript` 等
- `top_n`: 默认 10（图表）
- `pick`: 默认 1（笔记拆解榜一）
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
├── run_daily.py              # 日更流水线入口（抓取 → 选型 → 出图 → 草稿）
├── fetch_trending_chart.py   # 抓取 + 出图（可被流水线复用）
├── requirements.txt
├── README.md                 # 本文件（含 Agent Prompt）
├── LICENSE                   # MIT
├── .gitignore
├── output/                   # 日更产物（默认 gitignore，本地重跑）
│   ├── YYYY-MM-DD/
│   └── latest/
└── examples/
    ├── sample_chart.png      # 示例图（可选）
    └── xhs-note.md           # 分享草稿示例
```

---

## License

MIT — 见 [LICENSE](LICENSE)。
