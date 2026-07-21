# 运行端功能烟测指南

本指南只验证隔离的 `SYSTEM CHECK` 课程，不写入生产课程。

```text
用 Notion 对《SYSTEM CHECK | Fixture Course Runtime》做一次运行端功能烟测。

课程首页 URL：https://app.notion.com/p/00000000000000000000000000000009
固定 Test ID：runtime_smoke_fixture_20260709_001000

占位符检查：如果课程名、课程首页 URL 或 Test ID 仍是模板变量、空值或不具体，立即停止，不要自行选择最近课程。只回复：“烟测 prompt 未渲染，请让 Codex 生成具体课程版本。”

如果课程首页 URL 打不开，报告失败，不要改用最近课程或相似课程。回读四个允许写入页面，并确认 Course_Map 与 Sources & Coverage 未被改动。
```
