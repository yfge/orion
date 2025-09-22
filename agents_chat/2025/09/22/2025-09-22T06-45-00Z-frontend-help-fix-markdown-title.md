---
id: 2025-09-22T06-45-00Z-frontend-help-fix-markdown-title
date: 2025-09-22T06:45:00Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [docs, frontend]
related_paths:
  - frontend/help/en-US/index.md
  - frontend/help/en-US/quickstart.md
  - frontend/help/en-US/notify.md
  - frontend/help/en-US/endpoints.md
  - frontend/help/en-US/api-keys.md
  - frontend/help/en-US/email.md
  - frontend/help/en-US/third-party.md
summary: "修复英文帮助 Markdown 首行标题错误，改用 # 而非 %"
---

## 背景

- 早前英文帮助文档使用了 `%` 作为标题前缀，Markdown 渲染不会识别，页面显示了字面 `%`。

## 变更

- 将所有 en-US 帮助文档的首行 `% ...` 改为 `# ...`，确保 Markdown 正常渲染一级标题。

## 结果

- 帮助页面不再显示 `%`，标题样式正确。
