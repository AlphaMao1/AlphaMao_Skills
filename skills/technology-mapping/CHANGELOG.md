# Changelog

All notable changes to the technology-mapping skill will be documented in this file.

格式遵循 [Keep a Changelog](https://keepachangelog.com/)。

## [2.1.1] - 2026-03-22

### 🔴 布局正确性修复（Code Review 核心发现）

- **新增 `visual_spec.md` 布局约束规范**：6 个布局规则——边方向表（12 种边类型的 source/target 方向）、`cluster_` 流派聚类、edge weight/constraint 设置、时间轴 rank 锚定、节点排列顺序、生成后调试 checklist
- **SKILL.md Phase 4 新增步骤 4（布局约束）和步骤 7（布局验证）**：确保 agent 在生成图谱时不仅遵守颜色规范，也遵守位置规范
- **原问题**：v2.1.0 只约束了节点颜色/形状/边样式，但未约束 Graphviz dot 引擎的边方向、rank 约束、cluster 分组，导致生成图谱的节点位置不可预测

### 🐍 wikidata_client.py 修复

- **`_escape_sparql()`**：补充 `\n`、`\r`、`\t` 转义，完善注入防御
- **`batch_query_advisors()`**：去掉子串匹配（`name in person_label`），仅保留大小写不敏感的全等匹配，防止短名字误匹配
- **occupation QID 注释**：`FILTER` 中的 4 个 Wikidata QID 加入行内注释说明含义

### 📝 文档修复

- **`visual_spec.md` 节点配色表去重**：改为链接引用 `data_schema.md`，消除重复定义
- **删除 `scripts/__pycache__/`**

## [2.1.0] - 2026-03-20

### 🔴 安全修复

- **SPARQL 注入防御**：新增 `_escape_sparql()` 函数，所有 `query_doctoral_advisor()`、`query_students()`、`query_person_info()` 的人名参数在拼入 SPARQL 前均经过转义。修复了含引号名字（如 O'Brien）导致查询崩溃的问题

### 🏗️ SKILL.md 重构

- **SKILL.md 从 516 行精简至 ~230 行**：将可视化配色表、VC 分析框架、边样式规范提取为独立参考文档
- **新增 `references/visual_spec.md`**：Phase 4 节点配色、边样式、时间轴、Legend 的完整规范
- **新增 `references/vc_framework.md`**：VC 分析框架（创始人评估 + 技术路线 + 中外对比 + 可追溯性）
- **消除重复**：SKILL.md Phase 4 不再重复 `data_schema.md` 的配色表，改为链接引用
- **搜索降级**：从叙述句改为伪代码 checklist，明确 tavily-search → search_web → 标记未完成的降级路径
- **`<HARD-GATE>` 标签**：替换为标准 Markdown blockquote alert `> [!CAUTION]`
- **description 引号格式**：统一为中文书名号引号 `「」`

### 🐍 wikidata_client.py 增强

- **`batch_query_advisors()` 重写**：使用 SPARQL VALUES 批量查询替代 N 次串行 HTTP 请求，未匹配的名字才降级为单次查询
- **`query_person_info()` 消歧义**：新增 `expected_field` 参数，在多个 Q 实体匹配同名时，优先选择 `personDescription` 含该领域关键词的实体
- **缓存改进**：`_cache` 从裸 dict 改为 `OrderedDict` + `hashlib.sha256` key + `CACHE_MAX_SIZE=200` 上限（LRU 淘汰）
- **`print()` → `logging`**：8 处 `print()` 输出替换为 `logging.getLogger(__name__)` + 适当日志级别
- **User-Agent 版本号**更新为 2.1.0

### 📝 CHANGELOG

- v1.0.0 依赖列表增加废弃标注

---

## [2.0.1] - 2026-03-19

### 🔧 统一出图方案

- **废弃 Canvas 和 HTML 输出**：v2.0.1 起仅支持 Graphviz dot SVG 输出，不再支持 Obsidian Canvas (.canvas) 和 NetworkX + PyVis 交互式 HTML
- **Phase 4 添加 HARD-GATE**：明确禁止使用替代出图方案，`generate_techmap.py` 必须使用 `import graphviz` + `graphviz.Digraph`
- **删除 `references/canvas_layout.md`**：Canvas 布局规范文档已废弃

### 📊 References 颜色系统升级

- `data_schema.md`：从 Canvas Preset 编号 (`"0"` `"1"` `"5"`) 全面升级为 Graphviz HEX 色值 + SVG 属性体系（shape, fillcolor, penwidth）
- `connection_strength.md`：边色从 Canvas Preset 编号升级为 Graphviz HEX 色值，与 SKILL.md Phase 4 完全对齐

### 🔍 工作流改进

- **流派边框色动态化**：从硬编码领域名称（Caltech 系/苏黎世 INI 等）改为由 Phase 0 的 domain_profile 动态分配，按流派发现顺序使用预定义调色板
- **溯源终止年代阈值动态化**：从固定 40 年改为可根据领域特征调整（硬科技 60 年、AI/软件 20 年）
- **Phase 5 新增 VC 分析结论独立章节**：创始人技术深度排名、技术路线成熟度对比、中国公司海外溯源清晰度评级、投资风险信号汇总
- **国内搜索模板补充国际化注释**：提醒覆盖日本/韩国/以色列等非中国创业生态

### 🔗 依赖技能表更新

- 新增「必需」列，明确 Graphviz 为唯一必需系统依赖
- 新增废弃说明标注

### 🐍 wikidata_client.py 增强

- **指数退避重试**：HTTP 429/503/timeout 自动重试 3 次（2s/4s 间隔）
- **中英文双语搜索**：`query_doctoral_advisor()` 和 `query_person_info()` 同时搜索 @en 和 @zh 标签，提升中国学者覆盖率
- **内存缓存**：相同 SPARQL 查询不重复请求，新增 `clear_cache()` 方法
- **User-Agent 版本号**更新为 2.0.1

---

## [2.0.0] - 2026-03-17

### 🏗️ 架构重构（Breaking Change）

- **Phase 重编号为 0-5**：从原来的 Phase 1/1.5/2/3/4 重构为 Phase 0/1/2/3/4/5
- **新增 Phase 0：领域适应 & 策略生成** — LLM 在运行时动态分析领域特征，生成定制化搜索策略和溯源路径（LLM-as-Strategist），替代固定的 `academic_weight/opensource_weight/patent_weight` 模板
- **合并 Phase 1 + Phase 1.5** — 海外头部公司 + 国内创业公司 + 开源项目 + 学术里程碑一次完成
- **新增 Phase 5：质量验证 & 报告生成** — 从原 Phase 4 拆出报告部分，新增溯源质量统计

### 🔗 新增数据源

- **新增 Wikidata P184 集成**：新建 `scripts/wikidata_client.py`，直接查询 Wikidata 的 38 万条博士导师关系记录
  - `query_doctoral_advisor()` — 查某人的博士导师
  - `query_students()` — 查某导师的所有学生
  - `query_person_info()` — 获取人物学术信息（领域、机构）
  - `batch_query_advisors()` — 批量查询

### 🔍 Phase 2 溯源大改

- **Wikidata 优先**：溯源时先查 Wikidata P184，有结果直接使用，无结果再进入搜索漏斗
- **渐进式搜索漏斗**：替代固定 5 步策略链，分 3 层递进尝试，一旦找到可靠信息即停止
- **实验室横向扫描**：对核心导师/实验室批量查询所有学生，发现同门创业者
- **AI/开源领域适配**：新增"大厂核心团队 → 创业"溯源路径，与 PhD 链并列
- **溯源质量指标**：新增溯源完成率、多源验证率、孤儿率自动统计

### 🎨 Phase 4 出图方案

- **唯一输出**：Graphviz dot 引擎生成 SVG 矢量图谱
- **颜色系统**：完整 RGB 色值体系，fillcolor 按节点类型、边框色按流派、边色按连接类型
- **节点标注**：奠基人/核心贡献者粗边框，溯源终止节点 ⛔ 标注，VC 分析 🏷️ 标签

### 📚 References 更新

- `connection_strength.md`：新增边界案例 5-7（大厂 Lab 同事、框架依赖、Wikidata 验证），颜色使用 Graphviz HEX 色值
- `data_schema.md`：新增 AI 领域边类型（`spun_off`、`lab_colleague_industry`）+ Wikidata 置信度规则 + Graphviz 属性

### 🔧 其他

- 创建 `CHANGELOG.md`（本文件），为发布做准备

---

## [1.0.0] - 2026-03-15

### 初始版本

- 四阶段工作流（Phase 1/1.5/2/3/4）
- Obsidian JSON Canvas 输出 *(v2.0.1 已废弃，改用 Graphviz SVG)*
- 三级连接强度体系
- 依赖 tavily-search / openalex-database / networkx *(v2.0.1 已废弃)* / json-canvas *(v2.0.1 已废弃)*
