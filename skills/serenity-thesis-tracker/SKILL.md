---
name: serenity-thesis-tracker
description: 把 Serenity / X 博主更新转成 progressive-investment-research 研究工作区的可审计增量。适用于：跟踪 Serenity 或类似 X/Twitter 博主、生成每日报告、通过 Chrome 登录态或本地 browser bridge 抓 X、用 yt-dlp 抓 YouTube 字幕、把博主观点拆成 source leads、公司页、行业模块和 open questions。这个版本是原 PaiWork Serenity 跟踪 Skill 的通用本地版，不依赖 PaiWork 专有工具。
---

# Serenity Thesis Tracker

这个 Skill 的目标不是跟单，也不是评价博主本人，而是把 Serenity 这类高质量信息源的观点变成可审计、可验证、可接续的研究输入。

对人：每天先看到“博主今天发了什么、哪些值得看、链接在哪里、下一步查什么”。

对 agent：只把有研究价值的内容写入 `progressive-investment-research` 工作区；原始材料和低价值内容放进归档，不进入默认恢复面。

## 不可破坏的边界

- 面向用户和 agent 的说明、日报、dossier 模板必须中文为主；只有枚举、脚本参数、平台字段、源文本摘录等必要位置保留英文。
- 这是 Serenity Thesis Tracker 的通用本地版，不再依赖 PaiWork 的工作区状态、专有工具或专有数据源。
- Serenity、RihardJarc、Leopold 都只是内置信息源；不要为每个信息源再造一个单独 Skill。
- X/Twitter 默认不调用 `x-digest`；优先使用 Codex Chrome 插件，其次使用本 Skill 内置的 browser-bridge collector、用户导出材料，或未来显式配置的 API adapter。
- 公开镜像站、搜索片段、缓存页只能作为辅助线索；不能把它们当成 live X 验收成功。
- X/Twitter 正式日报和 active route 只能使用 source-language 原文或完整人工导出；X UI 自动翻译、搜索摘要、公开镜像、未点击“显示原文/Show original”或未展开“显示更多/Show more”的文本一律不合格。只抓到这类材料时，必须阻断并标记 blocked，不能生成正式日报，更不能写入研究工作区。
- 博主观点不能直接覆盖 `current-synthesis.md`、modules、companies 或 models。
- 每日报告放在 archive，供人查看和审计；agent 默认恢复只读 progressive research 的 active surface。
- X 帖子、YouTube transcript、播客、newsletter、复制片段都先按 source lead 处理，验证后才可能进入模型。

## 默认流程

1. **确认信息源和 dossier**
   - 选择 Serenity、RihardJarc、Leopold 或新增来源时，读 `references/source-registry.md`。
   - 如果还没有 dossier，用 `scripts/scaffold_creator_dossier.py` 创建 progressive research 骨架。
   - 如果 dossier 已存在，先读 `context.md`、`current-synthesis.md`、`model-map.md`、`source-leads-index.md`、`open-questions.md`、`update-log.md`，以及相关 `modules/`、`companies/`。

2. **收集更新**
   - X/Twitter：优先用 Codex Chrome 插件读取用户已登录 Chrome 中的 X 页面 DOM；不可用时再用 `scripts/fetch_x_daily.py` 连接用户授权的本地 browser bridge。
   - X/Twitter 抓取后必须通过原文质量门禁：抓取器会尝试点击 `显示原文/Show original` 和 `显示更多/Show more`；仍含 UI 翻译或未展开标记的条目会被剔除。若没有合格原文，本轮状态是 blocked，不得交付日报。
   - 如果 live X 抓取失败，可以用 `--fixture-jsonl`、用户导出或人工复制内容生成“非 live 日报”，但汇报必须标明 `collection_status`/`known_gaps`，不能说成无断点验收。
   - YouTube：用 `scripts/fetch_youtube_transcript.py` 调 `yt-dlp` 抓字幕/转录。缺 `yt-dlp` 是 setup failure，不是“没有更新”。
   - 手工输入：可以接收粘贴文本、本地文件、截图或导出材料，但必须标清来源状态。

3. **生成每日报告**
   - 主日报用 `scripts/build_daily_report.py` 生成 `archive/creator-daily/<source_id>/<YYYY-MM-DD>.md`，必须合并该博主当天所有已抓平台。
   - build 会硬拦截 `x-ui-auto-translated`、`summary-only`、`original text was not expanded`、搜索片段、公开镜像和 raw 文本中的 `翻译自/显示原文/显示更多` 等标记；遇到这些输入时不生成正式日报。
   - `scripts/normalize_intake.py` 只作为单平台归一化/调试工具；不能让单平台日报覆盖最终主日报。
   - 日报标准对齐 PaiWork 版：执行摘要、来源与抓取状态、今日变化、materiality 评分、content_type、研究对象/claim、低价值内容、最值得人工查看的链接、下一步研究任务。
   - 日报必须保留：链接、发布时间/抓取时间、主题/公司、重要性、建议动作、中文摘要、raw/transcript 引用。
   - 不默认保存长原文；长 transcript 单独保存并在日报里链接。

4. **决定是否写入研究工作区**
   - 写入前读 `references/intake-contract.md` 和 `references/research-bridge.md`。
   - 本 Skill 写入的目标工作区默认依赖 `progressive-investment-research` 标准。若当前环境没有该 Skill、没有兼容 dossier 结构，或 agent 无法读到 `current-synthesis.md` / `model-map.md` / `modules/` / `companies/`，必须先提示安装/启用 `progressive-investment-research` 或创建兼容工作区；不得只生成空白 active files。
   - 每次主日报生成后，必须运行 `scripts/route_research_updates.py` 自动拆解到工作区。
   - route 只是第一步，不是最终交付。route 后必须按 progressive research 标准完成本轮能做的验证和填充：优先查一手来源或强二手来源，把模块页、公司页、关键关系、瓶颈、事实表、验证状态填到可接续；只有剩余无法验证或会改变模型的问题才进入 `open-questions.md`。
   - 自动产出必须回答：涉及哪些公司、是什么逻辑、属于什么行业、哪些待验证、哪些可以后续研究。
   - 自动 route 后必须更新 active 恢复面：`source-leads-index.md`、`model-map.md`、`current-synthesis.md`。`source-leads-index.md` 记录 source lead 路由，不代表模型变化。
   - 公司相关自动写 `companies/<slug>.md`；SIVE 这类对象不再建单独 tracker。
   - 行业/机制自动写 `modules/<axis>.md`。
   - `modules/` 和 `companies/` 不允许交付空壳：不要留下空表、仅写“待验证后补齐”、或只有模板字段。若证据不足，至少写明当前 source lead、已查来源、证据状态、可证伪路径、为什么暂时不能升级。
   - 只有真正需要继续研究或验证后才可能改变模型的内容写 `open-questions.md`；不要把所有日报条目都塞进 open questions。
   - `archive-only` 和 `noise` 不写 active files。
   - 影响核心模型时，必须先形成 `model-candidate` 或 `current-model-update`，并保留证据边界。
   - 涉及其他 dossier 时，只写 bridge candidate，不静默修改外部 dossier。

5. **收尾汇报按“每日报告优先”**
   - 先给每日报告路径和今天发了什么。
   - 再列研究写入、开放问题、bridge candidate、跳过/噪音、访问失败、验证结果。

## 内置信息源

- `serenity`：X-first 来源。种子定位：`@aleabitoreddit` / `https://x.com/aleabitoreddit`。所有观点先按未验证 source lead 处理。
- `rihardjarc`：X + newsletter 来源。种子定位：`@RihardJarc` / `https://x.com/RihardJarc`，补充来源为 UncoverAlpha。适合 AI infrastructure、cloud CapEx、TPU/GPU economics、hyperscaler ASIC 和半导体供应链 source leads。账号拼写是 `RihardJarc`，不是 `RichardJarc`。
- `leopold`：低频 X + website 来源。官方站点的 Twitter 链接指向 `@leopoldasch`；live collection 时必须先跑 X，官网长文只作为手动/公开补充。YouTube 不作为 Leopold 内置来源，除非未来确认 Leopold 自己的官方频道并显式加入；第三方解读视频只能作为 supporting source 或临时材料，不能算 Leopold 每日更新。

内置信息源只是默认配置，不是硬编码流程。实际运行时可以更新 locator。

YouTube 是可选平台能力，不是 Serenity/Leopold 的默认预置来源；只有 source registry 明确注册了该 creator 的 YouTube channel/playlist，或用户本轮显式给出 YouTube 材料，才纳入主日报。

## 常用命令

创建 Serenity dossier：

```powershell
python scripts/scaffold_creator_dossier.py D:\research\creator-serenity --source-id serenity --display-name Serenity --platform x --locator https://x.com/aleabitoreddit --handle-or-channel aleabitoreddit
```

生成每日报告：

```powershell
python scripts/build_daily_report.py --dossier D:\research\creator-serenity --source-id serenity --display-name Serenity --date 2026-06-08 --x-jsonl D:\research\creator-serenity\archive\creator-raw\x\serenity\2026-06-08.jsonl --collection-manifest D:\research\creator-serenity\archive\creator-raw\x\serenity\2026-06-08-manifest.json
```

自动拆解写入工作区：

```powershell
python scripts/route_research_updates.py --dossier D:\research\creator-serenity --source-id serenity --display-name Serenity --date 2026-06-08 --daily-report D:\research\creator-serenity\archive\creator-daily\serenity\2026-06-08.md --x-jsonl D:\research\creator-serenity\archive\creator-raw\x\serenity\2026-06-08.jsonl
```

验证 Skill：

```powershell
python scripts/validate_contract.py
```

## 参考文件

- `references/source-registry.md`：内置信息源、新来源接入、来源字段。
- `references/intake-contract.md`：日报字段、重要性/action 枚举、证据对象映射。
- `references/research-bridge.md`：写入 progressive research 工作区的门禁。
- `references/daily-analysis-prompt.md`：每日拆解和写入判断用的中文提示词。
