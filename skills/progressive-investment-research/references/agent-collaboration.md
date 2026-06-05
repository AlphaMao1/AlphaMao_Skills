# Subagent 协作

Subagent 只增强研究，不拥有事实源。主 agent 对模型更新负责。

## Codex 环境原则

- 只有用户明确允许或任务确实需要并行/独立上下文时才 spawn。
- 先判断哪些任务可并行，哪些必须由主 agent 本地完成。
- Subagent 默认只读，输出 findings。
- 不让 subagent 并发编辑核心 dossier。
- 不默认使用 Agent Teams，也不默认写 `team-runs/`。

## 搜索型 Subagent

适合：

- 多家公司或竞品并行查找。
- 政策、价格、交易案例、论文、客户案例。
- 不同地区或产业链环节的资料扫面。

可使用当前环境可用的较低成本模型。输出必须包含来源、置信度和不确定性。

提示词要给目标，不给工具动作：

```markdown
任务：核查 [问题] 是否有公开证据支持。
dossier：<path>
范围：只读；不要编辑文件。
输出：关键发现、来源、来源类型、置信度、仍未解决。
```

## 审计型 Subagent

适合：

- promote 前。
- major update 前。
- 核心判断冲突。
- 用户要求反方或逻辑检查。

审计 subagent 应使用独立上下文，不接收主 agent 的完整推理，只接收待审材料、相关模型摘要和明确问题。

输出：

```markdown
## Scope
## Claims Reviewed
## Overreach Or Unsupported Claims
## Evidence Gaps
## Fact/Judgment/Assumption Mixups
## Strongest Counter-Interpretation
## Recommended Changes
```

## 角色模板

现有 `agents/` 文件是提示词素材，不是必须全部使用。

- `source-auditor.md`：来源质量和循环引用。
- `devil-advocate-investor.md`：反方投资逻辑。
- `consistency-checker.md`：Current Model、map、模块之间的漂移。
- 其他 researcher/analyst 角色只在明确需要时读取。

默认优先使用一个综合审计任务。只有高风险或天然可并行时才拆多个角色。

## Findings 合并规则

主 agent 必须：

1. 检查来源质量。
2. 区分 fact / judgment / assumption / open question。
3. 标出与当前模型的关系：adds / strengthens / weakens / contradicts / no change。
4. 决定是否更新 Current Model、模块、开放问题或 update log。
5. 对未采纳的反对点说明原因。
