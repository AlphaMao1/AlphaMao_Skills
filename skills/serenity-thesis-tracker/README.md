# Serenity Thesis Tracker

把 Serenity 的 X 更新变成可持续追踪、可验证、可接续的投研工作区。

这是原 PaiWork 版 Serenity 跟踪 Skill 的 **通用本地版 / 非 PaiWork 依赖版**。它不再假设 PaiWork 的专有工作区、数据源或报告工具，而是把 Serenity 的更新写入 `progressive-investment-research` 风格的 research dossier：每日观点报告、source leads、公司页、行业模块和 open questions。

## 适合

- 跟踪 Serenity / `@aleabitoreddit` 的 X 更新
- 把高质量 X 信息源变成可审计研究线索，而不是看完就划走
- 每天生成 creator daily report：今天发了什么、哪些值得看、链接在哪里
- 把有价值更新拆到 `companies/`、`modules/`、`source-leads-index.md` 和 `open-questions.md`
- 在没有 PaiWork 的 Codex / Claude Code / Cursor / OpenCode 等 Agent 环境中运行

## 不适合

- 直接跟单或生成交易建议
- 把博主观点当作事实或 Current Model
- 用公开镜像、搜索摘要、UI 自动翻译文本替代 X 原文
- 不做验证就批量生成公司 thesis

## 它会做什么

- 用 Chrome 登录态、browser bridge、用户导出或手工材料收集 Serenity 更新
- 拦截 X UI 自动翻译、搜索摘要、公开镜像和未展开原文
- 生成 `archive/creator-daily/<source>/<date>.md` 每日报告
- 按 materiality、content type、公司、行业机制和验证路径分类
- 自动路由到 `source-leads-index.md`、`modules/`、`companies/`、`open-questions.md`
- route 后要求继续按 progressive research 标准补证据状态，避免只留下空壳文件；不能交付“待验证后补齐”式占位

## 内置来源

| source_id | 默认定位 | 说明 |
| --- | --- | --- |
| `serenity` | `@aleabitoreddit` / X-first | 默认主来源，原 PaiWork Serenity workflow 的通用版。 |
| `rihardjarc` | `@RihardJarc` / X + newsletter | AI infrastructure、cloud CapEx、TPU/GPU economics、hyperscaler ASIC 线索。 |
| `leopold` | `@leopoldasch` / X + website | 低频高材料性来源；YouTube 不作为默认内置来源。 |

新增信息源按 [`references/source-registry.md`](./references/source-registry.md) 接入。

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
生成 Serenity daily report
把 Serenity 这条 X 拆成研究线索
更新 Serenity 工作区
把这个博主加入跟踪
```

## 安装

```text
帮我安装这个 skill：https://github.com/AlphaMao1/AlphaMao_Skills/tree/main/skills/serenity-thesis-tracker
```

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

把 Serenity 的 X 变成可持续追踪的研究

<http://xhslink.com/o/4y5hTyS0hnf>

## 文件

- [SKILL.md](./SKILL.md)
- [references/](./references/)
- [scripts/](./scripts/)
- [fixtures/](./fixtures/)
