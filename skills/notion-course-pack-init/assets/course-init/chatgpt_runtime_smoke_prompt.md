# ChatGPT 运行端隔离烟测 Prompt

Codex 先创建或确认一个可删除的 `SYSTEM CHECK` 课程副本，再渲染下面所有变量。这个 prompt 只操作隔离副本，不得指向生产课程。

```text
用 Notion 对《{{system_check_course_title}}》做一次隔离的运行端功能烟测。

课程首页 URL：{{system_check_course_home_url}}
固定 Test ID：{{test_id}}

占位符检查：如果课程名、课程首页 URL 或 Test ID 看起来仍是模板变量、空值或不具体，立即停止，不要自行选择最近课程。只回复：“烟测 prompt 未渲染，请让 Codex 生成具体隔离课程版本。”

隔离检查：课程名必须包含 `SYSTEM CHECK`。如果不包含，或课程首页 URL 指向正式课程，立即停止。URL 打不开时直接报告失败，不要改用最近课程或相似课程。

测试目标：验证你能读取 Course Pack、定位当前节点、生成一个课程推进问题，并把固定 Test ID 写入隔离课程的运行页面。

本次提示词只授权对上述隔离课程执行烟测写入，不授权修改正式课程。测试记录不构成用户学习进度、掌握证据或正式候选知识笔记。

请按顺序执行：

1. 读取课程路由协议。
2. 只按上面的 URL 打开《{{system_check_course_title}}》课程首页。
3. 读取 Runtime Snapshot、Course_Map、Course_State & Profile、Notes Inbox 的 Notes_Spec 摘要，以及课程首页里的 Tutor_Runtime_Prompt。
4. 定位当前节点，并生成一个适合当前节点的课程推进问题。只生成问题，不要求我回答。
5. 使用固定 Test ID `{{test_id}}`；不要重新生成或改写 Test ID。
6. 把同一个 Test ID 写入以下四个页面，每个页面只写一个简短烟测记录：
   - Runtime Snapshot：Test ID、当前节点、推进问题、测试时间。
   - Course_State & Profile：Test ID，并注明“烟测，不构成学习进度或掌握证据”。
   - Sessions：一条非正式课程的烟测 session。
   - Notes Inbox：Test ID，并注明未生成正式候选知识笔记。
7. 不要更新 Course_Map。
8. 不要更新 Sources & Coverage。
9. 任何读取或写入失败时，不要假装成功；报告失败页面、步骤和错误信息。

完成后用中文返回：

运行端隔离烟测结果：
- Test ID：
- 隔离课程名称：
- 隔离课程首页 URL：
- 读取协议：通过 / 失败
- 找到课程首页：通过 / 失败
- 当前节点：
- 生成的课程推进问题：
- 写入 Runtime Snapshot：通过 / 失败
- 写入 Course_State & Profile：通过 / 失败
- 写入 Sessions：通过 / 失败
- 写入 Notes Inbox：通过 / 失败
- 是否更新 Course_Map：否 / 是
- 是否更新 Sources & Coverage：否 / 是
- 写入页面链接：
- 失败或限制：
- 请用户把本报告完整发回 Codex，由 Codex 回读隔离课程并验证。
```
