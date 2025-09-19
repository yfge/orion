---
id: 2025-09-19T00-00-00Z-services-skeletons
date: 2025-09-19T07:43:30Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [services, auth, sender]
related_paths:
  - backend/app/services/auth/base.py
  - backend/app/services/auth/oauth2.py
  - backend/app/services/auth/hmac_.py
  - backend/app/services/auth/jwt_.py
  - backend/app/services/sender/base.py
  - backend/app/services/sender/http_sender.py
  - backend/app/services/sender/mq_sender.py
summary: "添加认证提供者与发送器的骨架：OAuth2 Client Credentials、HMAC、JWT 签发；HTTP/MQ Sender 初版接口。"
---

说明
- AuthProvider.apply(request) 负责向请求注入认证信息（Authorization、签名等），支持缓存/续期（OAuth2）。
- HttpSender/MQSender 暂为骨架，后续将接入重试、限流、熔断与模板渲染。
- 与前两步迁移配套，便于基于 endpoint.adapter_key/transport/config 选择合适的 Sender 与 AuthProvider。
