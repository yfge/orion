# 快速开始

1. 在“业务系统”中新建系统。
2. 在“通知 API”中新建端点（HTTP/Mailgun/SendGrid/SMTP）。
3. 在“消息定义”中定义消息结构（JSON + ${var} 占位）。
4. 建立“派发映射”：消息 → 端点，可在消息页或端点页配置。
5. 通过“发送测试”验证端点连通。
6. 业务方调用 `POST /api/v1/notify` 完成发送。

> 建议先在“API Keys”生成一个 Bearer Token，并使用 Authorization: Bearer <token> 调用 Notify。
