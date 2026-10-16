# 今日最热：morluto/rea（XHS 正文 v2，可粘贴）

> 今日涨星榜第 1/13 · +32,314 ⭐ · TypeScript
> 日期：2026-10-16（Asia/Shanghai） · 数据：github.com/trending?since=daily
> 配图：同目录 `chart.png`
> 详细版见：`xhs-draft-v2.md`

---

## 标题

今天GitHub第一：REA是啥

## 正文

今天 GitHub 日榜第一，单日 +32314 星。
很多人点进去只看到一句 “agent reverse engineering”，完全看不懂。
这篇用人话讲清：REA 到底是什么。

——

它到底是什么

REA = Reverse Engineer Anything（逆向一切）。
官方定位：给 AI 智能体用的「逆向分析工具箱」，通过一个 MCP 服务，去检查二进制、应用、网页和运行时行为。

用人话说：
你看到某个 App 里有个功能很想搞懂（甚至想仿一个），
但手里没有源码。
你可以让 Cursor / Claude Code / Codex 这类智能体去问 REA——
它在本机拆解目标，把证据（伪代码、模块关系、调用链等）交还给智能体，
再由智能体解释，或帮你实现类似能力。

分析跑在本地；结论会带着证据和限制说明（官方 README 强调这一点）。

——

能干什么 / 典型场景

1）拆 Electron / JS 应用
例如官方案例：顺着 Notion 剪贴板功能，从渲染进程 → preload → IPC → 主进程一路追清楚。
静态 JS 分析不需要再装 Hopper/Ghidra。

2）拆原生二进制
接上已有的 Hopper / Ghidra / IDA，拿伪代码、汇编、字符串、调用关系。
官方案例：DX-Ball 声像计算、老 DOS 游戏 TH04 弹幕角度，都能追到指令级再重建。

3）更广一点
Android APK、.NET、网站行为、抓包等也在官方「可以分析什么」表里——按目标装对应依赖即可，不是万能一键黑盒。

适合谁：做互通/复现、安全研究、软件保护学习、想搞懂竞品实现细节的开发者。
（官方免责声明：只用于你有权分析的软件；合法研究/教育/互操作。）

——

怎么自己上手（官方步骤）

前置：Node.js 22.x（≥22.19）/ 24.x（≥24.11）/ 26+，以及 npm。

① 注册到你的智能体（推荐）
```
npx rea-agents setup
```
选 Claude Code / Codex / Cursor / Gemini CLI / Grok Build 等，
审一下改动再批准；它会加 MCP + 工作流指引，并备份旧配置。
然后重启智能体。

② 直接问一句（官方示例改写）
「弄清某某 App 的某某功能怎么工作，展示证据，并为我的项目实现类似功能。」

③ 或先用终端试 JS/Electron（不配原生引擎也能跑）
```
npx -y rea-agents@latest analyze-javascript-application /绝对路径/到/app --json
```

④ 想常驻 CLI：
```
npm install --global rea-agents
rea --help
```
原生深度分析需先按文档配置 Hopper/Ghidra/IDA。

官网与指南：https://rea.tools/
只从官方源装：github.com/morluto/rea · rea.tools · npm 包 rea-agents

——

为什么今天火

可核对事实（2026-10-16，GitHub daily Trending）：
• 日榜第 1
• 今日涨星 +32,314
• 语言标签 TypeScript
• About：Reverse engineer anything with agents, from app behavior down to native binaries.

热度来自「今日星标增量」，不是只看总星。具体原因还得看近 1–2 天的 Release / 讨论 / 转发——以仓库公开页为准。

——

仓库
https://github.com/morluto/rea

#GitHub #Trending #开源 #逆向工程 #MCP #AI智能体 #程序员 #极客日常 #今日涨星 #开发者工具
