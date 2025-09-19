---
id: 2025-09-19T07-06-51Z-backend-auth
date: 2025-09-19T07:06:51Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [backend, auth, jwt, users, api]
related_paths:
  - backend/app/api/v1/auth.py
  - backend/app/api/v1/users.py
  - backend/app/api/v1/router.py
  - backend/app/core/security.py
  - backend/app/deps/db.py
  - backend/app/repository/users.py
  - backend/app/schemas/auth.py
  - backend/pyproject.toml
summary: "实现基本用户注册/登录/JWT 与用户列表接口，新增安全与依赖模块。"
---

内容
- API：
  - POST `/api/v1/auth/register`：用户名+密码（可带邮箱），创建用户
  - POST `/api/v1/auth/login`：用户名+密码，返回 JWT（bearer）
  - GET `/api/v1/users/`：需带 Authorization: Bearer <token>，返回用户列表
- 安全：
  - `core/security.py`：`hash_password/verify_password`（passlib[bcrypt]），`create_access_token/decode_token`（PyJWT，HS256）
  - 秘钥：`ORION_SECRET_KEY`（未设则使用 dev fallback；建议在 .env 设置）
- 依赖：
  - `deps/db.py`：FastAPI DB 依赖
  - `repository/users.py`：用户 CRUD（部分）
  - `schemas/auth.py`：请求/响应模型
- 依赖声明：`backend/pyproject.toml` 新增 `PyJWT`、`passlib[bcrypt]`

使用
- 设置 `.env`：`ORION_SECRET_KEY=your-strong-secret`
- 安装：`pip install -e backend`
- 启动：`uvicorn backend.app.main:app --reload`
- 调试：Swagger `/docs` 下可直接调用（登录后拷贝 token 到用户列表）
