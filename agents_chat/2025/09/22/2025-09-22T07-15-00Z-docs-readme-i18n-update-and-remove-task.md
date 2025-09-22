---
id: 2025-09-22T07-15-00Z-docs-readme-i18n-update-and-remove-task
date: 2025-09-22T07:15:00Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [docs, readme, i18n]
related_paths:
  - README.md
  - README.zh-CN.md
  - task.md
summary: "移除 task.md（i18n 任务单），并在中英文 README 补充已落地的国际化能力与使用说明"
---

## 用户原始需求与目标

- 不再需要单独的 task.md；请将国际化的特性更新到中英文 README。

## 本次变更

- 删除根目录 `task.md`；
- 在 `README.md` 与 `README.zh-CN.md` 增补 “Internationalization (i18n)/多语言（i18n）” 小节：
  - 语言列表与 UI 文案来源（`frontend/messages/{locale}.json`）；
  - 语言检测（`LANG` Cookie 与 `Accept-Language`）、导航栏切换；
  - 后端中间件的语言协商与 `Content-Language` 响应头；
  - 帮助中心按 `help/<locale>/` 加载并回退；
  - 如何扩展语言与后续 next-intl 路线；
  - 前端 i18n 快速提示。

## 结果与影响

- README 清晰描述了已实现的 i18n 行为与扩展方式，降低上手成本；task.md 的内容已沉淀到文档与实现。
