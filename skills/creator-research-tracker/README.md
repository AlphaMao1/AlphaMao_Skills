# Creator Research Tracker

把 X / YouTube / newsletter 等个人信息源的持续更新，变成可审计、可验证、可接续的投研工作区。

这是原 PaiWork 版 Serenity 跟踪流程的 **通用本地版 / 非 PaiWork 依赖版**。它不替代 [`serenity-thesis-tracker`](../serenity-thesis-tracker/) 原版；Serenity 在这里只是一个内置信息源案例。这个 Skill 默认写入 `progressive-investment-research` 风格的 research dossier：每日观点报告、source leads、公司页、行业模块和 open questions。

## 适合

- 跟踪 Serenity、RihardJarc 或新增 X/Twitter 博主
- 把高质量个人信息源变成可审计研究线索，而不是看完就划走
- 每天生成 creator daily report：今天发了什么、哪些值得看、链接在哪里
- 把有价值更新拆到 `companies/`、`modules/`、`source-leads-index.md` 和 `open-questions.md`
- 在没有 PaiWork 的 Codex / Claude Code / Cursor / OpenCode 等 Agent 环境中运行

## 不适合

- 直接跟单或生成交易建议
- 把博主观点当作事实或 Current Model
- 用公开镜像、搜索摘要、UI 自动翻译文本替代 X 原文
- 不做验证就批量生成公司 thesis

## 它会做什么

- 用 Chrome 登录态、browser bridge、用户导出或手工材料收集 creator 更新
- 拦截 X UI 自动翻译、搜索摘要、公开镜像和未展开原文
- 生成 `archive/creator-daily/<source>/<date>.md` 每日报告
- 按 materiality 评分、content type、公司、行业机制和验证路径分类
- 自动路由到 `source-leads-index.md`、`modules/`、`companies/`、`open-questions.md`
- route 后要求继续按 progressive research 标准补证据状态，避免只留下“待验证后补齐”式空壳文件

## 内置来源

| source_id | 默认定位 | 说明 |
| --- | --- | --- |
| `serenity` | `@aleabitoreddit` / X-first | 原 PaiWork Serenity workflow 的通用本地案例。 |
| `rihardjarc` | `@RihardJarc` / X + newsletter | AI infrastructure、cloud CapEx、TPU/GPU economics、hyperscaler ASIC 线索。 |

新增信息源按 [`references/source-registry.md`](./references/source-registry.md) 接入。

内置来源目前只保留 Serenity 和 RihardJarc。其他 creator 必须显式接入，不在开源包里预设未完成案例。

## 核心产物

```text
dossier/
├── context.md
├── current-synthesis.md
├── model-map.md
├── source-leads-index.md
├── open-questions.md
├── update-log.md
├── companies/
├── modules/
└── archive/
    ├── creator-daily/
    ├── creator-raw/
    └── creator-parsed/
```

日报放在 `archive/creator-daily/`，主要给人查看；Agent 默认恢复应先读根目录 active surface，而不是翻 archive。

## 怎么触发

```text
整理 Serenity 今天的推文
生成 RihardJarc daily report
把这个博主加入跟踪
把这条 X 拆成研究线索
更新 creator 研究工作区
```

## 安装

```text
帮我安装这个 skill：https://github.com/AlphaMao1/AlphaMao_Skills/tree/main/skills/creator-research-tracker
```

同时需要安装或启用依赖 Skill：

```text
帮我安装这个 skill：https://github.com/AlphaMao1/AlphaMao_Skills/tree/main/skills/progressive-investment-research
```

## 自动化任务

安装后可以让 Agent 生成每日自动化任务，例如：

```text
为 Serenity 创建每日自动化任务：每天收集最新 X 原文，生成 creator daily report，再把有价值内容拆到 progressive research 工作区。
```

自动化任务应每天输出 `archive/creator-daily/<source>/<date>.md`，并记录抓取成功、登录失败、权限失败、字幕缺失、UI 自动翻译拦截和无有效更新之间的区别。

## 常用命令

创建 Serenity dossier：

```powershell
python scripts/scaffold_creator_dossier.py D:\research\creator-serenity --source-id serenity --display-name Serenity --platform x --locator https://x.com/aleabitoreddit --handle-or-channel aleabitoreddit
```

生成日报：

```powershell
python scripts/build_daily_report.py --dossier D:\research\creator-serenity --source-id serenity --display-name Serenity --date 2026-06-08 --x-jsonl D:\research\creator-serenity\archive\creator-raw\x\serenity\2026-06-08.jsonl --collection-manifest D:\research\creator-serenity\archive\creator-raw\x\serenity\2026-06-08-manifest.json
```

拆到研究工作区：

```powershell
python scripts/route_research_updates.py --dossier D:\research\creator-serenity --source-id serenity --display-name Serenity --date 2026-06-08 --daily-report D:\research\creator-serenity\archive\creator-daily\serenity\2026-06-08.md --x-jsonl D:\research\creator-serenity\archive\creator-raw\x\serenity\2026-06-08.jsonl
```

验证 Skill：

```powershell
python scripts/validate_contract.py
```

## 小红书讲解

这个通用版延续了 Serenity 案例笔记的核心目标：把高质量个人信息源变成可持续追踪的研究资产。

<http://xhslink.com/o/4y5hTyS0hnf>

## 文件

- [SKILL.md](./SKILL.md)
- [references/](./references/)
- [scripts/](./scripts/)
- [fixtures/](./fixtures/)
