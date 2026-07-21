# 工作区初始化报告

## 摘要

- 工作区：{{workspace_url}}
- 模式：workspace-init
- 状态：{{ready_status}}
- 更新时间：{{updated_at}}

## Codex 侧 Notion 能力

- 可读取目标工作区：{{codex_fetch_status}}
- 已授权写入：{{codex_write_authorized}}
- 是否执行写入：{{codex_write_performed}}
- 写入结果：{{codex_write_result}}

## 共享页面

| 页面 | 状态 | URL | 备注 |
|---|---|---|---|
| 顶层工作区 | {{status}} | {{url}} | {{notes}} |
| 课程路由协议 | {{status}} | {{url}} | {{notes}} |
| 模板库 | {{status}} | {{url}} | {{notes}} |
| 手动写回模板 | {{status}} | {{url}} | {{notes}} |
| 视觉标准页 | {{status}} | {{url}} | {{notes}} |
| ChatGPT Notion App 配置说明 | {{status}} | {{url}} | {{notes}} |

## ChatGPT 侧连接

- Notion App：{{chatgpt_connection_status}}
- 用户下一步：{{chatgpt_connection_next_action}}

## 可选系统自检

- 用户是否要求：{{system_check_requested}}
- 是否创建页面：{{system_check_created}}
- URL：{{system_check_url}}
- 归档 / 删除说明：{{system_check_archive_note}}

## 用户下一步

{{user_next_action}}

## 阻塞 / 风险

{{blockers_or_risks}}

## 就绪声明

Codex 完成工作区初始化后，用户在 ChatGPT 连接 Notion App 即可开始课程。实际写入报错时再进入权限排查与手动写回流程。
