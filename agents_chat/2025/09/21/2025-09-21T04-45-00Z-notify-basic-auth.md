---
id: 2025-09-21T04-45-00Z-notify-basic-auth
date: 2025-09-21T04:45:00Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [backend, notify, auth]
related_paths:
  - backend/app/deps/api_key.py
  - backend/app/api/v1/notify.py
  - backend/tests/test_notify_basic_auth.py
  - README.md
  - README.zh-CN.md
summary: "Add Basic auth support to Notify API and a key preview endpoint; document usage"
---

User original prompt and requirements

- 为 /notify 增加基础权限验证，支持在后台生成 key；建议使用 Basic Auth。

Background and goals

- 原实现只支持 `X-API-Key`；为更通用的集成方式，增加 Basic Auth（兼容 Mailgun 风格 `api:<key>`）。提供一个“随机 key”预览接口，方便生成后配置到环境变量。

Changes

- deps/api_key: 支持 `Authorization: Basic base64("api:<key>")`（也接受空用户名或 `key:<key>`）。保留 `X-API-Key`。
- api/v1/notify: 新增 `POST /api/v1/notify/keys/preview` 返回随机 key（不持久化，需运维配置至 `ORION_PUBLIC_API_KEY`）。
- tests: 新增 `test_notify_basic_auth.py` 覆盖 Basic 正确/错误、X-API-Key 正确、key 预览接口。
- docs: 更新中英文 README 的 Notify 鉴权与生成 key 用法。

Outcome and impact

- 现有 X-API-Key 不受影响；新增 Basic 方式更易集成。预览接口便于生成强随机 key 并交由运维配置。

Next steps (TODO)

- 如需“在线旋转 key/多 key 管理”，可在数据库增加 API Keys 表与后台 UI，现阶段先用环境变量满足需求。
