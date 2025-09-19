---
id: 2025-09-19T07-23-46Z-frontend-auth-users-integration
date: 2025-09-19T07:23:46Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [frontend, auth, users, integration]
related_paths:
  - frontend/app/auth/login/page.tsx
  - frontend/app/auth/register/page.tsx
  - frontend/app/users/page.tsx
  - frontend/components/auth-gate.tsx
  - frontend/components/sidebar.tsx
  - frontend/components/ui/{input,label}.tsx
  - frontend/lib/api.ts
  - frontend/tsconfig.json
  - frontend/.env.local.example
  - backend/app/api/v1/auth.py
  - backend/app/main.py
  - backend/app/core/config.py
  - .env.example
summary: "整合前端用户注册/登录与用户列表，完善路由守卫、导航与环境配置；后端补充 CORS 并改进注册并发时的错误处理。"
---

内容要点
- 前端：
  - 页面：/auth/login、/auth/register；/users 列表页（无 token 自动跳转登录）。
  - 组件：AuthGate（全局守卫）、输入组件 Input/Label、清理侧边栏（移除登录/注册入口）。
  - 封装：lib/api.ts（统一读取 NEXT_PUBLIC_API_BASE_URL，管理 token，封装 login/register/fetchUsers）。
  - 体验：登录页与注册页互链便于切换；tsconfig 增加 @/lib 别名。
  - 配置：新增 frontend/.env.local.example 以配置后端地址。
- 后端：
  - CORS：默认允许本地 3000/3001 端口，或通过 ORION_CORS_ORIGINS 覆盖。
  - 安全：注册接口捕获唯一键并发错误，统一返回 400（Username already exists）。

验证
- 前端设置 NEXT_PUBLIC_API_BASE_URL 指向后端；后端设置 ORION_CORS_ORIGINS/SECRET_KEY。
- 注册 → 登录 → 跳转 /users 查看列表；未登录访问业务页面将被重定向到登录。

备注
- 下一步可切换为 Cookie 会话与服务端中间件控制路由；对用户接口增加分页与搜索。
