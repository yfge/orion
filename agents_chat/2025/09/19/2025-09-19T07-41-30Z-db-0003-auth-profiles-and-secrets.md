---
id: 2025-09-19T00-00-00Z-db-0003
date: 2025-09-19T07:41:30Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [db, migration, auth, secrets]
related_paths:
  - backend/alembic/versions/0003_auth_profiles_and_secrets.py
  - backend/app/db/models.py
summary: "新增 auth_profiles 与 secrets 表，并为 notification_apis.auth_profile_id 增加外键（可空，删除置空）。"
---

说明
- auth_profiles：type（none/oauth2_client_credentials/hmac/jwt/custom）、config(JSON)
- secrets：key 唯一、value（演示用途；生产建议接入外部 SecretManager 或加密存储）
- 约束：notification_apis.auth_profile_id → auth_profiles.id（on delete SET NULL）
