# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-02-04

### Added
- **硬逻辑标记**: `⚠️ 必须执行` 标识不可跳过的学习步骤
- **费曼学习法强化**: 读完每篇材料后必须进行问答交互（禁止直接跳到下一篇）
- **笔记即时生成**: 每篇阅读的问答后立即生成笔记，关联用户提问
- **补漏机制**: 周末检查遗漏笔记，确保没有遗漏

### Changed
- **progress.md 时序优化**: 延迟到用户选择学习模式后才创建
- **引导流程**: Step 0 只问路径 → Step 1 选模式 → Step 2 创建文件
- **周完成流程**: 从"生成笔记和闪卡"改为"生成闪卡 + 补漏检查"

### Fixed
- 修复 progress.md 在模式选择前就创建的时序问题
- 修复笔记生成被跳过的问题（与用户交互一起被跳过）
- 修复笔记未关联用户提问的问题

## [1.0.0] - 2026-02-04

### Added
- **核心价值主张**: README 新增「为什么用这个系统学习」章节，阐述原版课程价值和学习系统优势
- **跨平台支持**: SKILL.md 目录创建逻辑支持 Windows/macOS/Linux

### Changed
- 版本号升级至 1.0.0 正式版
- README 安装说明更新为对话式配置（首次运行时询问路径）
- progress.md Week 引用同步为 9 周制结构

### Fixed
- 修复 Windows `mkdir -p` 不兼容问题
- 修复 progress.md 模板中 Week 9/10 残留引用
- 修复 README 中不存在的 YAML 配置说明

## [0.3.0] - 2026-02-03

### Added
- **content-audit.md**: 45篇阅读材料分类（Direct/Needs Context/Hands-On/Product-Heavy）
- **why-this-matters.md**: 4篇"Needs Context"材料的前置解释
- **flashcard-template.md**: 鲁棒格式参考模板
- **内容前置检查**: 阅读推送前根据类型提供不同引导

### Changed
- 闪卡格式: `??` + emoji → 单行 `Question::Answer` + `==cloze==`
- SKILL.md 增加闪卡格式规则（何时用 Q::A，何时用 cloze）

### Fixed
- 闪卡Q/A颠倒问题（切换到更鲁棒的格式）
- 内容相关性问题（增加"为什么读这篇"解释）

## [0.2.1] - 2026-02-03

### Fixed
- 修复文件操作语法：`copy` 改为正确的 `view_file` + `write_to_file`
- 修复追加模式逻辑：先读取现有内容，拼接后覆盖写入
- 修复目录读取：`view_file` 改为 `list_dir` 处理目录
- 添加翻译文件不存在时的错误处理

### Added
- 首次运行引导流程：询问 Vault 路径、创建目录结构
- 学习模式选择（精简/标准/完整）
- 更清晰的工具调用示例代码

## [0.2.0] - 2026-02-03

### Added
- **translations/**: 45篇预翻译阅读材料（Week 1-7, 9）
- **用户交互存储**: `interactions/weekX/` 记录问答、疑问
- **新手解释系统**: "解释 [术语]" 命令获得通俗解释
- **定制化闪卡**: 周末根据用户交互记录生成个性化闪卡
- **作业评价系统**: 基于笔记和学习内容的智能反馈
- **外部链接引导**: 标记需访问原链接的内容

### Changed
- 课程结构调整: 删除原 Week 8 (无Reading)，Week 9 → Week 8，Week 10 → Week 9
- course-content.md 添加 Slides 选读链接和翻译文件映射
- 作业系统: 可选模式，用户自定义交付文件夹
- SKILL.md 重构: 使用预翻译文件而非实时翻译

### Fixed
- 解决 AI 翻译倾向概括的问题（使用预翻译）
- 课程周数从10周调整为9周

---

## [0.1.1] - 2026-02-03

### Added
- README.md 项目说明文档
- CHANGELOG.md 版本记录
- TASK_TRANSLATION.md 翻译任务规范
- assignments-guide.md 简化版作业指南

### Changed
- 明确版本号为 V0.1.1
- SKILL.md 添加作业系统基础框架

---

## [0.1.0] - 2026-02-02

### Added
- SKILL.md 核心指令文件
- references/course-content.md 完整课程内容 (10周47篇)
- references/learning-methodology.md 学习方法论
- templates/progress.md 进度追踪模板
- templates/note-template.md 笔记模板
- templates/flashcard-template.md 闪卡模板
- templates/course-overview.canvas 可视化画布

### Features
- 中文优先的学习体验
- Zettelkasten 原子笔记法
- 闪卡间隔复习系统 (Obsidian SR 插件)
- 进度自动追踪
- 主动回忆式问答
