---
id: 2025-09-22T02-30-00Z-backend-i18n-middleware-wiring
date: 2025-09-22T02:30:00Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [i18n, backend]
related_paths:
  - backend/app/main.py
  - backend/app/core/i18n.py
summary: "挂载 I18nMiddleware 至 FastAPI 应用（最小接入）"
---

## 用户原始需求与目标

- 继续按最小单元推进 i18n，完成后端中间件接入。

## 背景与目标

- 将 `I18nMiddleware` 添加至应用，使请求具备语言协商与上下文能力；暂不修改业务返回文案。

## 本次变更

- 在 `backend/app/main.py` 中引入并注册 `I18nMiddleware`。

## 结果与影响

- 请求周期内可从 `request.state.locale` 与上下文读取语言；为后续错误消息本地化与模板渲染打基础。

## 下一步（TODO）

1. 在统一异常处理与响应构造处使用 `gettext_()` 返回本地化 `message`（独立提交）。
2. 初始化示例 PO 与最小键值，用于端到端验证（独立提交）。

## 关联提交/PR

- 本条目所在提交：在应用层挂载 i18n 中间件。
