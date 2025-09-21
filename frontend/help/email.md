# 邮件适配器（Mailgun/SendGrid/SMTP）

- Mailgun：`adapter_key=http.mailgun`，配置 `url=https://api.mailgun.net/v3/<domain>/messages`、`api_key`，可选 `from`/`to`。
- SendGrid：`adapter_key=http.sendgrid`，配置 `url=https://api.sendgrid.com/v3/mail/send`、`api_key`，可选 `from`/`to`。
- SMTP：`transport=smtp, adapter_key=smtp.generic`，配置 `host`、可选 `port`、`use_tls`/`use_ssl`、用户名/密码、默认 `from`/`to`。

“发送测试”会按适配器自动构造主题与正文。映射（mapping）支持 `from`、`to`、`subject`、`text`、`html` 字段。
