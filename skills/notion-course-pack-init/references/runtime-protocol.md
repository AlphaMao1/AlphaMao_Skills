# Runtime Protocol

This reference defines how ChatGPT should use a completed Course Pack after Codex initialization.

## Role Split

Codex handles low-frequency initialization, repair, audits, and structural maintenance. ChatGPT with a Notion app that has the required read/write capability handles daily lessons, interaction, progress updates, candidate notes, and light writeback.

ChatGPT must not perform full course initialization unaided.

## One Lesson, One Conversation

Default rule:

```text
One Lesson, One Conversation
```

Each lesson should start in a fresh ChatGPT conversation when practical. At the end of a completed lesson, ChatGPT writes back Notion updates and gives the user a short prompt for the next fresh conversation:

```text
用 Notion 继续《课程名》。
```

## Cold Start Read Set

At the beginning of a new lesson conversation, ChatGPT reads:

- route protocol;
- Course Home Runtime Index;
- Runtime Snapshot;
- Course_Map;
- Course_State & Profile;
- Tutor_Runtime_Prompt;
- Notes Inbox Notes_Spec summary.

If the same conversation continues without confusion, ChatGPT may use chat context as a hot cache and only confirm Runtime Snapshot when needed.

If state looks stale, conflicting, or the user says something is wrong, ChatGPT rereads Course Home Runtime Index and the required Course Pack pages.

## Initialization Diagnosis vs Progression Question

Initialization diagnosis questions happen before `course-init`. They collect design input and are not learning evidence.

Progression questions happen during lessons. They are not weak quiz questions and should not have an obvious answer in the wording. A good progression question:

- advances the current node;
- sits slightly above the user's current level;
- invites real thinking;
- reveals conceptual boundaries, mechanisms, counterexamples, or transfer ability;
- gives evidence for `skip`, `compress`, `teach`, `bridge`, or `branch`.

ChatGPT should usually ask one progression question at a time.

Do not use a progression question to repair a missing initialization calibration receipt. If Course_Map has no calibrated route section or Course_State claims a real content node without calibration evidence, stop the lesson and send a route-structure issue to Codex Handoff Queue.

## Lesson Loop

For each lesson:

1. Locate the current node.
2. Generate a live progression question for that node.
3. Read the user's answer.
4. Choose one strategy:
   - `skip`: user already meets the node standard;
   - `compress`: explain briefly and move forward;
   - `teach`: teach the current concept normally;
   - `bridge`: add the smallest necessary prerequisite, then return to the main line;
   - `branch`: answer a side question without changing the main route.
5. Explain, correct, or extend based on the user's answer.
6. Advance. Do not circle around the same concept unless the user's answer shows a real blocker.
7. Return to the Course_Map route.

## Branch Handling

If the user asks a side question, answer it normally. Do not rewrite Course_Map, change the current node, or write Codex Handoff Queue merely because the user branched.

If the branch creates a stable knowledge object or reveals user interest, create or update a candidate note in Notes Inbox and return to the main line.

Only propose Course_Map changes when the user explicitly asks to systematize the side topic, change direction, or spend more course time on it.

## Writeback Triggers

Do not write to Notion automatically without confirmation.

Writeback is triggered when:

- the user explicitly says to end and write back;
- ChatGPT judges the lesson goal complete and asks for confirmation;
- the user says next time, stop here, note this, or similar closing intent.

## Required Writeback Surfaces

Every successful lesson writeback updates:

- Course_State & Profile;
- Sessions;
- Notes Inbox;
- Runtime Snapshot.

Optional writeback:

- Codex Handoff Queue, only for structural or maintenance items that need Codex.

Daily lessons do not update Sources & Coverage.

## Successful Writeback Response

After successful writeback, ChatGPT should give a short user-facing summary:

```text
已写回：
- 当前进度：...
- 新增候选主题笔记：...
- 下一讲入口：...

下一讲请新开 ChatGPT 对话，输入：
用 Notion 继续《课程名》。
```

Do not paste full internal patches unless the user asks or writeback fails.

## Writeback Failure Block

If writeback fails, output a manual writeback block:

- failure step;
- pages not written;
- target page for each block;
- Markdown content to paste;
- whether the next lesson can continue;
- what must be manually patched first.

Never describe a failed Notion write as successful.

## Candidate Note Standard

Candidate notes are split by stable knowledge object, not by lesson or chapter.

Each candidate note records:

- knowledge structure;
- user learning evidence;
- where the user first erred, hesitated, or showed interest when relevant;
- next teaching hint.

Candidate notes remain in Notes Inbox until reviewed for Obsidian import.

## Codex Follow-Up Boundary

ChatGPT writes Codex Handoff Queue only for:

- new major materials;
- route restructure needs;
- Course_Map or Runtime Snapshot conflicts;
- damaged Notion pages;
- candidate notes ready for Obsidian review;
- configuration or permission issues.

Ordinary progress, side questions, and lesson notes stay in normal runtime pages.
