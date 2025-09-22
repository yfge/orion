---
id: 2025-09-22T05-35-00Z-frontend-i18n-auth-login-register
date: 2025-09-22T05:35:00Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [i18n, frontend]
related_paths:
  - frontend/app/auth/login/page.tsx
  - frontend/app/auth/register/page.tsx
  - frontend/messages/zh-CN.json
  - frontend/messages/en-US.json
summary: "本地化 Auth（登录/注册）页面：标题、字段、按钮、错误与跳转提示"
---

## 变更内容

- 登录页：标题、用户名/密码标签、提交按钮（含加载态）、错误信息默认、无账号提示与跳转链接本地化；
- 注册页：标题、用户名/邮箱/密码标签、提交按钮（含加载态）、错误默认、已有账号提示与跳转链接本地化；
- 新增 `auth.login.*`、`auth.register.*` 文案键。

## 影响

- 登录/注册页完整随语言切换生效。
