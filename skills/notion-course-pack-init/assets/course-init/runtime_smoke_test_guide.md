# 运行端隔离烟测指南

这个测试验证 ChatGPT + Notion 插件的真实读写能力。写入对象必须是可删除或明确保留的 `SYSTEM CHECK` 隔离课程，不得使用生产课程。

## 已渲染测试对象

- 隔离课程：`{{system_check_course_title}}`
- 课程首页 URL：`{{system_check_course_home_url}}`
- 固定 Test ID：`{{test_id}}`
- 本地审计目录：`{{local_audit_dir}}`

如果仍有 `{{...}}`、课程名不含 `SYSTEM CHECK`，或 URL 与生产课程首页相同，停止测试并让 Codex 重新准备。

## 用户操作

1. 打开新的 ChatGPT 对话，确认已连接同一个 Notion 工作区。
2. 粘贴已渲染的隔离烟测 prompt。
3. 把 ChatGPT 返回的完整“运行端隔离烟测结果”交回 Codex。
4. 等 Codex 回读 Notion 并核对 Test ID 后，再删除隔离课程或明确选择保留。

不要自行选择最近课程；隔离课程 URL 打不开时，不得切换到相似课程。遇到未渲染变量时应返回“烟测 prompt 未渲染”。

## Codex 回读通过标准

Codex 必须逐项验证：

1. ChatGPT 返回的 Test ID 与固定 Test ID `{{test_id}}` 完全一致。
2. Runtime Snapshot、Course_State & Profile、Sessions、Notes Inbox 各出现一次该 Test ID。
3. Course_State & Profile 明确说明烟测不构成学习进度或掌握证据。
4. Sessions 明确标记为非正式课程记录。
5. Notes Inbox 明确没有生成正式候选知识笔记。
6. Course_Map 和 Sources & Coverage 的托管区域指纹不变，也没有该 Test ID。
7. 隔离课程已删除并回读确认，或用户明确要求保留且该决定写入 receipt。

只有 ChatGPT 报告、Codex 回读和清理/保留 receipt 三者一致，`runtime_smoke.status` 才能记为 `verified`。
