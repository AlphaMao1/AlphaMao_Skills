# Intake 契约

把 X 帖子、YouTube transcript、播客笔记或复制材料转成日报/研究输入前读这里。

## 每日批次字段

每次运行至少产出一个 batch 记录：

| 字段 | 含义 |
| --- | --- |
| `batch_id` | 稳定批次 id，通常是 `<source_id>-<YYYY-MM-DD>` |
| `source_id` | 注册表 id，如 `serenity`、`rihardjarc` 或新接入 creator |
| `display_name` | 人类可读名称 |
| `platform` | `x`、`youtube`、`website`、`podcast`、`newsletter`、`manual` |
| `captured_at` | 抓取时间 |
| `collection_status` | `ok`、`partial`、`blocked`、`dependency-missing`、`no-new-items`、`manual` |
| `raw_paths` | 为审计保留的 raw/transcript 文件 |
| `daily_report_path` | 写给人看的每日报告 |
| `known_gaps` | 未登录、缺字幕、发布时间未知、429 等 |

## 日报 item 字段

每条 item 必须保留：

| 字段 | 是否必填 | 含义 |
| --- | ---: | --- |
| `item_id` | 是 | 批次内稳定 id |
| `canonical_url` | 是 | 原帖/视频/来源链接；没有则写 `unknown` |
| `posted_at` | 是 | 原始发布时间；不知道写 `unknown` |
| `captured_at` | 是 | 抓取时间 |
| `summary` | 是 | 给人看的中文简明摘要；原文是英文时也要优先写中文摘要 |
| `topics` | 是 | 主题、ticker、公司或分析轴 |
| `importance` | 是 | `P0`、`P1`、`P2`、`noise` |
| `action` | 是 | 下方 action 枚举 |
| `source_status` | 是 | 如 `creator-original`、`secondary-transcript`、`manual-copy`、`missing-transcript` |
| `raw_ref` | 否 | raw/transcript artifact 路径 |
| `excerpt` | 否 | 短摘录，可保留原文；不要默认复制长版权文本 |

不要把抓取时间当发布时间。拿不到发布时间时写 `unknown`。

X/Twitter 的 `raw_ref` 和 `excerpt/source_text` 必须来自 source-language 原文或完整人工导出。中文日报摘要可以是 agent 自己写的中文，但不能把 X UI 自动翻译、搜索摘要、公开镜像片段、未展开 `显示原文/Show original` 或 `显示更多/Show more` 的文本当作 raw evidence。遇到这类输入时，`build_daily_report.py` 和 `route_research_updates.py` 必须失败，不得生成正式日报或 active 写入。

## 重要性

| importance | 含义 |
| --- | --- |
| `P0` | 可能改变核心 thesis、出现矛盾，或需要紧急验证 |
| `P1` | 值得进入 tracker/open question/company/module |
| `P2` | 背景信息、弱信号、低优先级观察 |
| `noise` | 闲聊、重复、纯市场波动、互动诱饵、非研究内容 |

## Action

| action | 含义 |
| --- | --- |
| `archive-only` | 只进日报归档，不写 active research |
| `open-question` | 新增或更新可验证问题 |
| `company-update` | 写入公司 source-lead 区域 |
| `module-update` | 写入稳定分析轴/模块 |
| `model-candidate` | 形成模型补丁候选，不当作事实 |
| `current-model-update` | 通过证据门禁后更新 Current Model |
| `bridge-to-dossier` | 路由到其他 dossier 的候选，不直接改外部 dossier |

## 证据对象映射

| 博主材料 | 研究对象 |
| --- | --- |
| 来源元信息 | Source Card，`source_tier: creator_source_lead`，fallback 到 `expert_interview` |
| 事实性说法 | Claim Row，`review_status: raw` 或 `parsed_ok` |
| 引语/短摘录 | Quote Row，必须保留 quote policy |
| 与现有模型冲突 | Conflict Row 或 open question |
| 数字说法 | 只有单位、周期、范围、方法齐全才可做 Number Row；否则做 open question |
| 模型影响 | Model Patch Candidate，`write_policy` 通常是 `review_required` 或 `crosscheck_required` |

搜索片段和社交帖子不能直接更新模型。

## 拆解提示

每条有意义的 item 至少拆：

- claim：博主实际主张什么。
- mechanism：其因果链/商业逻辑是什么。
- target：公司、行业、技术、政策、变量或场景。
- verification path：什么材料能确认或证伪。
- evidence object：source card、claim row、quote row、conflict row 或 model patch candidate。
- action：归档、开放问题、公司、模块、模型候选、当前模型或 bridge。

## 反模式

- “输出全是英文，用户再自己理解。”
- “博主说了 X，所以模型就写 X。”
- “每条帖子都建一个 module。”
- “没有 transcript，但标题看起来重要。”
- “登录失败等于没有更新。”
- “X UI 自动翻译看起来已经够懂了，可以先写入研究区。”
- “日报生成了，所以研究文件一定要改。”
- “提到 ticker 就是公司 thesis。”
