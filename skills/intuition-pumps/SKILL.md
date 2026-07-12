---
name: intuition-pumps
description: Use when the user wants to route, choose, learn, or apply Dennett-style intuition pumps and thinking tools for hard problems, stuck reasoning, argument testing, concept confusion, weak explanations, or agent self-rescue after repeated unproductive reasoning.
---

# Intuition Pumps

This skill is a progressive-disclosure router over 77 standalone intuition-pump tool cards. Use the structured index to find tools, then load only the selected card.

## Status Guard

Before routing, applying, or teaching a tool, check whether `references/tool-index.json` exists. Before applying or teaching a selected tool, also check whether the matching `references/tools/NNN-*.md` card exists.

- If the index is missing, say the skill is installed but routing is unavailable.
- If a selected card is missing or incomplete, report the blocked tool card by id and title.
- Do not invent a missing tool card from memory.
- Do not batch-create missing cards.

## Reference Loading Rule

For point invocation, and after the user selects a tool from a routing menu, read the matching single tool card under `references/tools/`. Routing Menu itself is the deliberate exception: it must read the five candidate cards one by one so it can explain their names before asking the user to choose.

- Do not load all tool cards.
- Do not synthesize a card from the index alone.
- Do not complete a missing card during a normal tool-use request.
- If a selected card is missing or incomplete, report that the relevant tool-card issue is not finished.

## Tool Identity Disclosure

Any tool that is visible to the user must be explained before it is applied, recommended as a next step, or offered as an adjacent option. A command name is not self-explanatory; do not output a bare short command with only a functional reason.

For every visible tool, read its card's `身份`, `名称与思想实验`, and `原书机制转译` sections and give a compact identity block containing:

- 工具命令与卡片标题。
- 原书标题；如果卡片提供英文原名，也一并保留。
- 书中名字的背景：原书里的具体故事、思想实验、比喻或术语画面。
- 名字为什么和这个工具动作匹配：从书中画面到 skill 操作的对应关系。
- 这次工具实际要做什么，以及为什么适合当前问题。

“名称与思想实验”不能被一句用途副标题替代。至少要让一个不熟悉本书的人知道：名字指的是什么画面，画面暴露了什么思考陷阱，以及使用者要对哪个变量、命题或机制动手。

Routing Menu 因为会同时显示 5 个工具，必须逐张、独立读取这 5 张候选卡片后再输出；不得只根据 `tool-index.json` 的短命令、家族和 `use_when` 生成名称解释，也不得为了省上下文把所有候选压成同一种泛化描述。每张卡的说明可以控制在 2-4 句，但不能省略名字背景。

Point Invocation、Progress Mode 和相邻推荐使用完整身份块；Agent Self-Rescue 只有在需要向用户披露所用工具时使用轻量身份块。内部整理且不向用户显示工具名时，无需表演工具说明。

## Book Context References

- Read `references/book-structure.md` only when the user asks about the original book structure, wants book-level classification, or is maintaining a tool card.
- Read `references/appendix-pump-candidates.md` only when evaluating whether to add tools beyond the 77 numbered cards.
- Treat the book's 8 parts as a secondary classification layer. Routing still uses `tool-index.json`, `taxonomy.md`, and the current problem shape.
- Do not promote appendix candidates into active tools without a separate issue and enough source material for one complete card.

## Entry Modes

### Point Invocation

Use when the user names a tool by short command, number, full title, or alias.

Required behavior:

1. Look up the requested tool in `references/tool-index.json`.
2. Read only the matching single tool card.
3. First give the tool's identity block: what the book's name refers to, why the name fits the operation, and what the tool does here.
4. Apply that tool to the current problem.
5. Recommend adjacent tools only when they materially change the next step; recommend no more than 2. Explain each visible adjacent tool with the same compact identity block.

### Learning Mode

Use when the user asks to learn, understand, practice, or teach a named tool, including prompts like "学习 /工具名".

Required behavior:

1. Look up the requested tool in `references/tool-index.json`.
2. Read only the matching single tool card.
3. Explain the tool with this structure:
   - 工具身份：原书标题/英文原名（如有）、名字背景、名称与动作的对应关系
   - 名称与思想实验
   - 工具机制
   - 适用场景
   - 操作方法
   - 练习
   - 误用检查
4. Do not apply the tool to the user's live problem unless they explicitly ask for application.
5. If the user asks to learn a tool for the current problem but does not name one, run Routing Menu first, then teach only the selected tool.

### Routing Menu

Use when the user asks for recommendations because they do not know which tool to use.

Required behavior:

1. Read `references/tool-index.json`.
2. Classify the current problem type.
3. Select exactly 5 candidates, then read their five matching cards one by one and independently.
4. Recommend exactly 5 candidates:
   - 1 `建议先用`
   - 4 `可选探索`
5. Use the 5 slots defined in `references/routing-review.md`.
6. Give each candidate its identity block, reason, and explicit not-fit boundary.
7. Stop and wait for the user to choose unless the user asked for progress mode.

If the selected card does not exist yet, the menu may still recommend candidates from the index, but it must disclose that application is blocked until that card issue is implemented.

### Progress Mode

Use when the user says "我卡住了", "帮我想想", "直接处理", or equivalent.

Required behavior:

1. Produce the same 5-candidate routing menu.
2. Read the card for `建议先用` again if needed for application context.
3. Show its identity block before applying it.
4. Apply only that one tool.
5. Preserve the other 4 explained candidates for switching paths.

If the `建议先用` card is missing, do not invent it. Report the blocked card issue and stop after the recommendation menu.

### Agent Self-Rescue

Use only when the agent has a clear stuck signal:

- Repeated attempts produce no new evidence.
- A concept boundary remains unstable.
- An explanation contains a magic step.
- A reasoning path loops without progress.
- A proposed distinction keeps collapsing.

Do not trigger self-rescue merely because the task is complex.

Required behavior:

1. Route to one fitting tool.
2. Read only that tool card.
3. Apply the tool lightly.
4. Disclose the tool only if it changes the reasoning path, confidence, tradeoff, or next action; when disclosing it, include a compact identity block rather than only the command name.

For full self-rescue rules, read `references/self-rescue.md`.

## Non-Negotiables

- Do not register 77 UI-native slash commands.
- Do not put 77 tool cards into this `SKILL.md`.
- Do not generate tool cards in bulk.
- Do not treat a template-filled card as complete.
- Treat each tool card as an independent maintenance unit and acceptance target.

## Recommendation Records

Only record recommendation metadata when the user asks to record,复盘, or沉淀.

- Use `references/usage-log-template.md`.
- Do not record private chain-of-thought or full reasoning traces.
- If writing a log file is inappropriate, output a compact record block instead.
