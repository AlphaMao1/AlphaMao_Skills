# 信息源注册表

选择内置信息源或新增 X/YouTube/播客/newsletter 来源时读这里。

## 基本原则

这里记录的是“博主观点系统”的来源信息，不是博主评分，也不是研究结论。

注册表只回答：

- 跟踪谁；
- 从哪里收集；
- 通常影响哪些研究主题；
- 这些内容进入研究时必须带什么 caution label。

研究结论放在目标 dossier，不放在注册表。

## 来源字段

```yaml
source_id: serenity
display_name: Serenity
viewpoint_scope: AI infrastructure and public-market supply-chain theses
platforms:
  - platform: x
    locator: https://x.com/aleabitoreddit
    handle_or_channel: aleabitoreddit
    collection_method: chrome-plugin-first
status: active
default_topics:
  - ai-supply-chain
  - photonics-cpo
  - data-center-power
source_tier: creator_source_lead
research_tier_fallback: expert_interview
raw_material_policy: links-plus-structured-summary
caution_labels:
  - source-lead-not-fact
  - requires-primary-check
  - not-investment-advice
target_dossier: ""
notes: ""
```

必填字段：`source_id`、`display_name`、至少一个 platform locator、collection method、caution labels、source tier fallback。

## 内置种子

### Serenity

```yaml
source_id: serenity
display_name: Serenity
viewpoint_scope: AI infrastructure, supply chain, photonics/CPO, data-center power, and small-cap company leads
platforms:
  - platform: x
    locator: https://x.com/aleabitoreddit
    handle_or_channel: aleabitoreddit
    collection_method: chrome-plugin-first
status: active
default_topics:
  - ai-supply-chain
  - photonics-cpo
  - data-center-power
  - small-cap-company-leads
source_tier: creator_source_lead
research_tier_fallback: expert_interview
raw_material_policy: links-plus-structured-summary
caution_labels:
  - source-lead-not-fact
  - creator-performance-claims-unverified
  - requires-primary-check
  - not-investment-advice
notes: 来自旧 PaiWork 案例，但不能复用 PaiWork 工作区状态。
```

### Rihard Jarc

```yaml
source_id: rihardjarc
display_name: Rihard Jarc
viewpoint_scope: AI infrastructure, cloud CapEx, hyperscaler AI chips, TPU/GPU economics, semiconductor supply-chain theses
platforms:
  - platform: x
    locator: https://x.com/RihardJarc
    handle_or_channel: RihardJarc
    collection_method: chrome-plugin-first
  - platform: newsletter
    locator: https://www.uncoveralpha.com/
    handle_or_channel: UncoverAlpha
    collection_method: manual-or-web
status: active-candidate
default_topics:
  - ai-infrastructure
  - cloud-capex
  - ai-accelerators
  - hyperscaler-asic
  - semiconductor-supply-chain
source_tier: creator_source_lead
research_tier_fallback: expert_interview
raw_material_policy: links-plus-structured-summary
caution_labels:
  - source-lead-not-fact
  - requires-primary-check
  - newsletter-paywall-or-partial-access
  - not-investment-advice
notes: 账号拼写为 RihardJarc，不是 RichardJarc。先跑 3-10 条小样本 intake；X 用 Chrome 原文门禁，newsletter 仅作为补充来源，不替代 live X 验收。
```

内置来源目前只保留 Serenity 和 RihardJarc。其他 creator 即使未来可跟踪，也必须按“新来源接入流程”显式注册，不在开源包里预设未完成案例。

## 新来源接入流程

先判断来源类型：

| 情况 | 决策 | 写入位置 |
| --- | --- | --- |
| 同一个人新增平台 | 加到现有 source 的 platforms | 同一个 creator dossier |
| 博主引用的支撑来源 | 作为 supporting source | 同 dossier 的 source card 或日报 |
| 独立博主/观点系统 | 新 source，通常新 dossier | 新 creator dossier |

步骤：

1. 记录精确 locator：X handle/profile/list、YouTube channel/playlist/video、podcast feed、newsletter export 或本地文件来源。
2. 写清为什么这个来源进入研究系统，以及通常影响哪些分析轴。
3. 选择 collection method：
   - `chrome-plugin`：优先使用 Codex Chrome 插件读取用户现有 Chrome 登录态和页面 DOM。
   - `browser-bridge`：通过用户授权的本地浏览器桥抓 X/Twitter。
   - `yt-dlp`：抓 YouTube 字幕/转录。只在该 creator/source 明确注册了 YouTube 平台时使用；二手评论视频默认只是 supporting source，不进入每日预置跟踪。
   - `manual-or-web`：网站、复制文本、newsletter、PDF、公开页面。
   - `api-adapter`：只有未来显式配置 API adapter 时才用。
4. 默认使用 `source_tier: creator_source_lead`，并映射到 `research_tier_fallback: expert_interview`。
5. 添加 caution labels。必须包含 `source-lead-not-fact` 和 `requires-primary-check`。
6. 先跑 3-10 条小样本 intake，再决定是否持续跟踪。

## Live X 验收门

- X/Twitter 信息源的 live 验收优先顺序是：`chrome-plugin` -> `browser-bridge` -> 用户导出/人工复制。
- 公开镜像站、搜索结果片段、缓存页只能作为辅助发现线索，不能作为“live 成功”证据。
- X 原文质量门槛：正式日报和 active route 只能使用 source-language 原文或完整人工导出。含 `翻译自/显示原文/显示更多`、`x-ui-auto-translated`、搜索摘要、公开镜像、summary-only、未展开原文的材料必须阻断。
- 如果 live 链路不可用或只能得到 UI 翻译/摘要，不能生成正式日报；只能留下 blocked 状态记录或 rejected raw 归档。`partial` 只能用于“部分条目被剔除，但剩余条目已经是合格原文”的场景。

## 自动化任务

安装后可以让 Agent 生成每日自动化任务：固定时间抓取已注册来源，生成 `archive/creator-daily/<source_id>/<YYYY-MM-DD>.md`，再运行 `scripts/route_research_updates.py` 拆到 progressive research 工作区。自动化任务必须把登录失败、权限失败、字幕缺失、UI 翻译拦截和无有效更新分开记录，不能把失败伪装成“没有更新”。

## 依赖提示

本 Skill 的 active 写入标准依赖 `progressive-investment-research`。如果目标环境没有安装该 Skill，Agent 必须先提示安装或创建兼容 dossier，再继续 route；不能只生成日报后留下空白研究工作区。

## 维护规则

- 不在注册表写每日流水。
- 不在这里复制原帖全文。
- 不按收益率或名气给博主打分。
- 不把 PaiWork 专有工具名写成必要依赖。
- 登录失败、权限失败、字幕缺失要写成来源状态，不能伪装成“没有更新”。
