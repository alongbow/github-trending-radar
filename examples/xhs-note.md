# 小红书笔记稿 · GitHub Trending 日更 Agent

**建议标题（任选）：**

1. 让 Agent 每天帮我扫 GitHub Trending，爽了
2. 极客日记：一键画出「今日涨星」榜
3. Prompt 配方：自动读仓 + 出图 + 发笔记

**建议标签：**
`#GitHub` `#Trending` `#Agent` `#开源` `#极客日常` `#Prompt` `#效率工具` `#程序员`

**配图：** `chart.png`（今日涨星横向柱状图，见同目录）

---

## 正文（可直接粘贴）

每天刷 GitHub Trending 真的会耗干注意力。
榜一刷完，仓库 README 还没读，星标又变了。

所以我写了一个 **可复用 Prompt**，丢给 Agent 就能日更：

> 抓 daily 榜 → 按「今日涨星」排序 → 快读 Top N → 画图 → 吐出分享草稿

不编造涨粉，不画饼变现，只吃公开数据。

---

### 今天实测（2026-10-16 · Asia/Shanghai）

在本机跑了 PoC 脚本：

```bash
cd github-trending-poc
python3 fetch_trending_chart.py
```

解析到 13 个 trending 仓，并生成了图表 → **见配图 `chart.png`**。

今日涨星 Top 切片（截断真实数据）：

1. **morluto/rea** · +32,314 ⭐ today  
   Agent 驱动的逆向工程：从行为到 native binary
2. **debpalash/VoiceStudio** · +3,024 ⭐ today  
   本地开源语音工作室（克隆 / 配音 / 听写）
3. **NationalSecurityAgency/ghidra** · +1,369 ⭐ today  
   NSA 开源 SRE 框架，老牌实力再冲榜
4. **K-Dense-AI/scientific-agent-skills** · +1,091 ⭐ today  
   把任意 Agent 武装成「AI 科学家」的 skills 库
5. **affaan-m/ECC** · +1,013 ⭐ today  
   Agent harness 性能优化：skills / memory / 安全

一眼读图：今天风口明显偏 **Agent 工具链 + 逆向/语音**，而不是又一个 CRUD 脚手架。

---

### Prompt 配方（核心三句话）

1. **目标**：日更 Trending，只信 stars today + 公开 README  
2. **步骤**：抓榜 → 读仓三行卡 → 出图 → 写短笔记  
3. **约束**：禁止虚构数字；失败就报失败；礼貌限速

完整可粘贴模板在同目录 `prompt.md`。

---

### 你怎么复现

```bash
# 依赖：requests / beautifulsoup4 / matplotlib
pip install -r requirements.txt
python3 fetch_trending_chart.py --top 10
# 输出：trending_stars_today.png
# 笔记包：note-v1/chart.png + prompt.md + xhs-note.md
```

把 `prompt.md` 整段丢给任意能上网的 Agent，把 `{{日期}}` 换成当天即可。

收藏这篇，明天让 Agent 再跑一轮——  
比你手刷榜快一个数量级。

（数据来自公开 GitHub Trending 页面，实时会变；以你本机当次运行为准。）
