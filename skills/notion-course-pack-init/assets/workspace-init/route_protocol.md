# 课程路由协议

本页是 ChatGPT 进入课程后的运行入口。它负责告诉 ChatGPT 先读什么、如何定位课程、何时写回；不负责创建新课程。

## 开始一门已有课程

当用户输入 `用 Notion 继续《课程名》`：

1. 按课程名和 Course ID 精确定位 Course Home。不要选择“最近”或“最相似”的课程。
2. 从 Course Home 的 Runtime Index 读取 Runtime Snapshot、Course_Map、Course_State & Profile、Notes Inbox。
3. 检查 Runtime Snapshot 与 Course_Map、Course_State & Profile 是否一致；有冲突时停止推进，并记录到 Codex Handoff Queue。
4. 找到当前节点和最低完成标准，现场生成一个略高于用户当前水平的课程推进问题。
5. 根据回答选择 `skip`、`compress`、`teach`、`bridge` 或 `branch`，然后继续推进主线。

## 一课一对话

一讲结束后，先询问用户是否写回。用户确认后更新：

- Runtime Snapshot
- Course_State & Profile
- Sessions
- Notes Inbox（仅在形成稳定知识对象时）

日常课程不更新 Course_Map 和 Sources & Coverage。结构性问题交给 Codex。

## 写回失败

不要把失败描述成成功。返回手动写回块，写清失败页面、错误原文、待粘贴内容、是否可以继续下一讲。

## 新课程请求

如果目标课程不存在，不要自行初始化。请用户回到 Codex，调用 `notion-course-pack-init` 并提供完整材料与目标工作区页面。
