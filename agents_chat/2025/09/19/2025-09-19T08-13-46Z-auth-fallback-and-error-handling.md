---
id: 2025-09-19T00-00-00Z-auth-fallback
date: 2025-09-19T08:13:46Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [auth, jwt, tests]
related_paths:
  - backend/app/core/security.py
  - backend/app/api/v1/users.py
summary: "为本地/测试环境增加 JWT Fallback（无 PyJWT 时使用 HS256 简易实现），并放宽 users API 的异常捕获。"
---

动机
- 在无网络或未安装 PyJWT 的环境中，也要保证测试可跑通；users API 不再强依赖 PyJWT 的异常类型。

变更
- core/security.py：若无法导入 PyJWT，则使用内置 HS256 编码/解码实现（仅测试用途）；保持 create_access_token/decode_token 接口不变。
- api/v1/users.py：用户鉴权从捕获具体 PyJWT 异常改为捕获通用异常，统一返回 401。
