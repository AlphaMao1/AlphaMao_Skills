# 课程初始化报告

## 摘要

- 课程名称：{{course_title}}
- Course ID：{{course_id}}
- 状态：{{status}}
- 课程首页：{{course_home_url}}
- 本地审计目录：{{local_audit_dir}}

## 材料覆盖

- 正式范围：{{formal_scope}}
- 覆盖状态：{{coverage_status}}
- 材料读取报告：{{material_read_report_path}}

## 课程设计校准

- 校准状态：{{calibration_status}}
- 学习目标：{{calibrated_learning_goal}}
- 预期用途：{{calibrated_intended_use}}
- 基础与深度摘要：{{calibrated_baseline_summary}}
- 第一讲入口：{{calibrated_first_entry}}
- 校准 Receipt：{{course_design_receipt_path}}
- 证据边界：route-calibration-only-not-mastery

## Notion 同步

- Manifest：{{manifest_path}}
- 同步报告：{{sync_report_path}}
- 回读校验：{{readback_validation_status}}
- 托管区域校验：{{managed_region_validation_status}}
- 幂等 / 重复页面校验：{{idempotency_validation_status}}
- Runtime Index：{{runtime_index_status}}

## 创建 / 更新的页面

| 页面职责 | URL | 状态 |
|---|---|---|
| {{page_role}} | {{url}} | {{status}} |

## ChatGPT 运行端隔离烟测

- 状态：{{runtime_smoke_status}}
- SYSTEM CHECK 课程：{{system_check_course_title}}
- 隔离课程首页：{{system_check_course_home_url}}
- 固定 Test ID：{{test_id}}
- 清理 / 保留结果：{{cleanup_status}}

生产课程启动口令：

```text
用 Notion 继续《{{course_title}}》。
```

隔离烟测指南：`{{runtime_smoke_test_guide_path}}`

交付给 ChatGPT 的烟测 prompt 必须是已渲染版本，包含具体 `SYSTEM CHECK` 课程名、隔离课程首页 URL 和固定 Test ID。不得把生产课程当作写烟测目标。

预期行为：

- ChatGPT 读取课程路由协议和隔离课程首页。
- ChatGPT 读取 Runtime Snapshot，并定位当前节点。
- ChatGPT 提出一个现场生成的课程推进问题。
- ChatGPT 写入明确标记为烟测的记录，不把它当作真实学习进度。
- ChatGPT 写入 Runtime Snapshot、Course_State & Profile、Sessions 和 Notes Inbox。
- ChatGPT 不更新 Course_Map 和 Sources & Coverage。
- 用户把 ChatGPT 返回结果发给 Codex 后，Codex 回读隔离课程，验证 Test ID、保护页指纹和清理 / 保留 receipt。

若用户未授权隔离烟测，写明 `Course Pack initialized; runtime smoke pending`，不要把初始化完成写成全系统就绪。

## 剩余风险

{{remaining_risks}}

## 下一步

{{next_action}}
