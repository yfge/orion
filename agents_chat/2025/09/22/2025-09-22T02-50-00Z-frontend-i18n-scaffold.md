---
id: 2025-09-22T02-50-00Z-frontend-i18n-scaffold
date: 2025-09-22T02:50:00Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [i18n, frontend]
related_paths:
  - frontend/i18n/locales.ts
  - frontend/messages/zh-CN.json
  - frontend/messages/en-US.json
summary: "前端 i18n 初始脚手架：locale 常量与 messages 占位"
---

## 用户原始需求与目标

- 继续以最小单元推进 i18n，先提交前端消息文件与常量，暂不改动路由。

## 本次变更

- 新增 `frontend/i18n/locales.ts`：导出受支持语言与默认语言类型定义。
- 新增 `frontend/messages/{zh-CN,en-US}.json`：放置基础占位键（示例）。

## 结果与影响

- 为后续接入 `next-intl` 与中间件路由打基础；不影响现有页面行为。

## 下一步（TODO）

1. 新增 `middleware.ts` 与 `[locale]/` 布局（独立提交）。
2. 抽取现有页面中文文案到 `zh-CN.json` 并生成英文占位（独立提交）。

## 关联提交/PR

- 本条目所在提交：前端 i18n 初始脚手架。
