# 同步报告｜Fixture Course

- 页面写入：8 个页面均已完成。
- 托管区域：每个页面只有一个 `fixture_course:<page_role>:v1` 区域。
- 回读校验：8 个 URL、标题、托管区域与来源指纹均匹配。
- 幂等校验：课程首页命中 1 个，重复页面职责为空。
- 隔离烟测：`runtime_smoke_fixture_20260709_001000` 只写入四个运行页面。
- 保护页：Course_Map 与 Sources & Coverage 回读未变。
- 失败项：无。
