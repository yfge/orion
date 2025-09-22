---
id: 2025-09-22T03-25-00Z-frontend-path-alias-i18n
date: 2025-09-22T03:25:00Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [frontend, config]
related_paths:
  - frontend/tsconfig.json
summary: "修复 '@/i18n/*' 路径别名，解决模块解析失败"
---

## 背景

- 抽取文案后在组件中使用 `@/i18n/provider`，但 `tsconfig.json` 未配置该 alias，Next 构建提示 module not found。

## 变更

- 在 `frontend/tsconfig.json` 的 `paths` 中新增：`"@/i18n/*": ["i18n/*"]`。

## 结果

- 允许通过别名 `@/i18n/*` 引用 i18n 相关模块，解决构建解析错误。
