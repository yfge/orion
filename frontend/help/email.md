# 邮件适配器（Mailgun/SendGrid/SMTP）

## 适配器一览

- Mailgun（HTTP）：`adapter_key=http.mailgun`
  - 配置：`url=https://api.mailgun.net/v3/<domain>/messages`、`api_key`
  - 可选：默认 `from`、默认 `to`
- SendGrid（HTTP）：`adapter_key=http.sendgrid`
  - 配置：`url=https://api.sendgrid.com/v3/mail/send`、`api_key`
  - 可选：默认 `from`、默认 `to`
- SMTP（直连）：`transport=smtp, adapter_key=smtp.generic`
  - 配置：`host`、可选 `port`（25/465/587）、`use_tls`/`use_ssl`、`username`/`password`、默认 `from`/`to`

## 发送测试与映射

- “发送测试”会按适配器自动构造主题与正文（默认主题 “Orion Test”）。
- 派发映射（mapping）支持：`from`、`to`、`subject`、`text`、`html`；推荐使用表单（RJSF）填写，减少 JSON 手写错误。

示例（SendGrid 请求体局部）：

```json
{
  "from": { "email": "noreply@example.com" },
  "personalizations": [{ "to": [{ "email": "alice@example.com" }] }],
  "subject": "Hello",
  "content": [{ "type": "text/plain", "value": "Hi" }]
}
```

## 常见排障

- 401/403：Key 无效或权限不足；确认 `api_key` 正确、域与 IP 白名单设置。
- 400 Bad Request：收件人/发件人/域名未验证或格式错误。
- SMTP 失败：
  - 端口与 TLS/SSL：465=SSL，587=STARTTLS；25=明文（部分云厂商封禁）。
  - 认证失败：检查 `username/password` 与是否启用“第三方客户端/应用专用密码”。
  - HTML 编码：确保 `html` 正确闭合，避免被网关拒绝。
