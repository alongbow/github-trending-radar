# 标题（可直接粘贴）

GitHub今日涨星第一！REA +3.2万

# 正文（可直接粘贴）

今日涨星第一：morluto/rea
今日 +32,314 ｜ 总星 275,945
（Trending daily · 10-16）

【这是一个什么项目？】
REA = Reverse Engineer Anything。
给 AI 智能体用的本地逆向工具箱：一个 MCP，检查二进制、应用、网页和运行时。分析在本机，结论带证据。

【有什么用？】
想搞懂某个 App 功能（甚至想仿）但没源码时，让 Cursor / Claude Code / Codex 问 REA——它本地拆目标，交回伪代码、模块关系、调用链，再解释或帮你实现。
可拆 Electron/JS（官方案例 Notion 剪贴板）、接 Hopper/Ghidra/IDA 拆原生。只用于你有权分析的软件。

【原理是什么？】
Agent → MCP 调 REA → 本机逆向/静态工具检查 → 带证据交回 Agent。
静态 JS 不必装原生引擎；深度原生需 Hopper/Ghidra/IDA。

【如何结合你的 agent 使用？】
核心：把仓库链接丢给 agent，让它按官方 README setup。

可复制提示词：
「打开 https://github.com/morluto/rea ，按 README 执行 npx rea-agents setup（我用 Cursor），审改动后告诉我怎么重启，再说明能分析什么。」

或：npx rea-agents setup → 重启 agent → 开始问。

【小例子·刚跑过】
$ npx -y rea-agents@latest --help
→ rea@6.5.0 — Reverse engineer anything from your terminal or agent.
可见 analyze / analyze-javascript-application / doctor。

https://github.com/morluto/rea · https://rea.tools/ · npm: rea-agents

#GitHub #Trending #开源 #逆向工程 #MCP #AI智能体 #程序员 #极客日常 #今日涨星 #开发者工具

# 配图（output/latest/）

1. `card-rank.png` — 今日涨星榜（横轴：今日新增 Stars，不是总星；条标「今日 +xx」）
2. `card-focus.png` — 大数字：+32,314 / 总星 275,945
3. `card-howto.png` — 三步：丢链接 → setup → 开始问
4. `card-demo.png` — 真实 CLI：`npx -y rea-agents@latest --help`

# 元数据

- date: 2026-10-16 (Asia/Shanghai)
- focus: morluto/rea
- stars_today: 32314 (Trending scrape)
- total_stars: 275945 (GitHub API re-fetch)
- demo_ran: yes (`rea@6.5.0 --help`)
- body_non_newline_chars: 919
- feature claims: official README only
