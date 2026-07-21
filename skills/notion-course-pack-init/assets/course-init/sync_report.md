# 同步报告｜{{course_title}}

## 摘要

- Course ID：{{course_id}}
- 同步开始：{{sync_started_at}}
- 同步结束：{{sync_finished_at}}
- 状态：{{sync_status}}

## 已创建页面

| 页面职责 | URL | 托管区域 ID | 来源指纹 | 结果 |
|---|---|---|---|---|
| {{page_role}} | {{url}} | {{region_id}} | {{source_fingerprint}} | {{result}} |

## 已更新页面

| 页面职责 | URL | 托管区域 ID | 来源指纹 | 结果 |
|---|---|---|---|---|
| {{page_role}} | {{url}} | {{region_id}} | {{source_fingerprint}} | {{result}} |

## 跳过页面

| 页面职责 | 原因 |
|---|---|
| {{page_role}} | {{reason}} |

## 回读校验

| 检查项 | 结果 | 备注 |
|---|---|---|
| 课程首页可读取 | {{result}} | {{notes}} |
| Runtime Index 链接可达 | {{result}} | {{notes}} |
| Runtime Snapshot 有当前节点摘要 | {{result}} | {{notes}} |
| Course_Map 节点字段完整 | {{result}} | {{notes}} |
| Course_Map 区分来源能力架构与个性化路线 | {{result}} | {{notes}} |
| 校准 Receipt 与页面路线一致 | {{result}} | {{notes}} |
| Sources & Coverage 映射完整 | {{result}} | {{notes}} |
| Notes Inbox 有候选笔记规则 | {{result}} | {{notes}} |
| Codex Handoff Queue 存在 | {{result}} | {{notes}} |

## 托管区域回读 Receipt

| 页面职责 | 回读标题 | 托管区域出现次数 | 指纹匹配 | 用户区块保留 | 结果 |
|---|---|---:|---|---|---|
| {{page_role}} | {{readback_title}} | {{region_occurrences}} | {{fingerprint_match}} | {{user_blocks_preserved}} | {{result}} |

每个页面的 `region_occurrences` 必须恰好为 `1`。更新只能替换 `managed_by=notion-course-pack-init` 且 `course_id`、`region_id` 匹配的托管区域；其他区块不得覆盖。

## 幂等校验 Receipt

- 查找策略：`upsert-by-course-id-and-page-role`
- Course Home 命中数：{{course_home_matches}}
- 重复页面职责：{{duplicate_page_roles}}
- 二次执行结果：{{idempotency_result}}

Course Home 命中数必须为 `1`，重复页面职责必须为空。否则停止更新并报告冲突。

## 运行端隔离烟测 Receipt

- Test ID：{{test_id}}
- SYSTEM CHECK 课程：{{system_check_course_title}}
- 隔离课程首页：{{system_check_course_home_url}}
- 四个允许写入页面：{{verified_write_pages}}
- 两个保护页保持不变：{{verified_unchanged_pages}}
- 隔离课程清理 / 保留状态：{{cleanup_status}}

## 失败项

{{failures}}

## 手动修复说明

{{manual_repair_instructions}}
