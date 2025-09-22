---
id: 2025-09-22T03-00-00Z-frontend-i18n-provider-and-middleware
date: 2025-09-22T03:00:00Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [i18n, frontend]
related_paths:
  - frontend/app/layout.tsx
  - frontend/components/navbar.tsx
  - frontend/components/lang-switch.tsx
  - frontend/i18n/provider.tsx
  - frontend/i18n/locales.ts
  - frontend/messages/zh-CN.json
  - frontend/messages/en-US.json
  - frontend/middleware.ts
summary: "前端页面 i18n 初步接入：Provider、LANG Cookie 中间件与语言切换器"
---

## 用户原始需求与目标

- 先做前端页面相关的多语言接入，按最小单元提交并保留 agents_chat 记录。

## 本次变更

- 在根布局中加入 I18nProvider（基于 JSON messages），从 Cookie/Accept-Language 判定 locale，设置 `<html lang>`。
- Navbar 使用 `t('nav.tagline')` 并新增语言切换器组件 `LangSwitch`（写 Cookie 后刷新）。
- 新增 `frontend/middleware.ts`：若无 `LANG` 则依据 `Accept-Language` 设定默认 `LANG` Cookie，不改写路由。
- 增补 messages 键：`nav.tagline`。

## 关键决策与取舍

- 不引入外部依赖（如 next-intl），先以轻量 Provider 完成 UI 层接入，后续可无缝替换为 next-intl。
- 暂不改动路由结构（不加 `[locale]`），先实现可用与可切换。

## 结果与影响

- 页面显示随语言切换（Cookie）而变化；后续可逐步抽取更多文案与接入路由前缀。

## 下一步（TODO）

1. 抽取更多页面文案进入 messages；
2. 之后按计划切换到 `next-intl` 与 `[locale]` 路由；
3. 在文档中记录从轻量 Provider 迁移到 next-intl 的步骤与注意事项。

## 关联提交/PR

- 本条目所在提交：前端 Provider + 中间件 + 切换器 + 文案接入。
