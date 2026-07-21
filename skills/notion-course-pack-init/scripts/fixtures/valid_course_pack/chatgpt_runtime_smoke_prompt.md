# ChatGPT 运行端功能烟测 Prompt

这是隔离的 `SYSTEM CHECK` 烟测，不操作生产课程。

```text
用 Notion 对《SYSTEM CHECK | Fixture Course Runtime》做一次运行端功能烟测。

课程首页 URL：https://app.notion.com/p/00000000000000000000000000000009
固定 Test ID：runtime_smoke_fixture_20260709_001000

占位符检查：如果课程名、课程首页 URL 或 Test ID 仍是模板变量、空值或不具体，立即停止，不要自行选择最近课程。只回复：“烟测 prompt 未渲染，请让 Codex 生成具体课程版本。”

如果课程首页 URL 打不开，报告失败，不要改用最近课程或相似课程。只在隔离课程的 Runtime Snapshot、Course_State & Profile、Sessions 和 Notes Inbox 写入固定 Test ID；不要更新 Course_Map 或 Sources & Coverage。
```
