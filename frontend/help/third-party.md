# 第三方集成指南（对接商户/外部系统）

本文面向第三方/商户/外部系统，详细说明 Orion 的对接概念、对接流程与示例。

## 1. 基础信息

- 基础地址（本地示例）：`http://localhost:8080`
- 生产环境：以贵方配置的域名为准，建议通过 HTTPS 访问
- 所有公开接口均走同一前缀：`/api/v1`（例如：`/api/v1/notify`）

## 2. 鉴权（API Key）

- 由平台管理员在控制台“API Keys”新建并分发给第三方。
- 推荐在请求头使用 Bearer 方式：`Authorization: Bearer <token>`。
- 兼容：`X-API-Key: <token>` 或 `Authorization: Basic <base64("api:<token>")>`。

> 出于安全考虑：请勿将 API Key 暴露在前端代码或可共享介质中；建议保存在后端安全配置或密钥管理系统。

---

## 3. 核心概念与术语

- Business System（业务系统）：你要对接的业务域或应用空间（如“订单系统”、“结算系统”）。
- Endpoint（端点）：指向第三方渠道的连接配置，包含：
  - transport：传输方式（如 http、smtp）
  - adapter_key：适配器标识（如 http.generic、http.mailgun、http.sendgrid、smtp.generic）
  - config：适配器配置（如 URL、鉴权、超时等）
- Message Definition（消息定义）：以 JSON Schema + `${var}` 占位描述消息结构（例如飞书 text 消息）。
- Dispatch（派发映射）：将“消息定义”与一个或多个“端点”绑定；可在映射中用 mapping 覆盖/补充字段。
- Send Record / Send Detail（发送记录/明细）：发送的“总记录”与各“尝试/渠道”的明细记录，便于审计与排障。

---

## 4. 对接流程（通用）

1. 平台管理员为你开通 API Key（控制台“API Keys”新建）。
2. 平台侧配置：
   - 新建“业务系统”（可选，用于分类）
   - 新建“端点”（Endpoint），指向你的第三方渠道（HTTP/SMTP 等）
   - 新建“消息定义”（Message Definition），编写 JSON Schema（支持 `${var}` 占位）
   - 建立“派发映射”：将消息 → 端点绑定，可设置映射字段（mapping）
3. 你方调用公开 Notify API（同步或异步）传入 data，Orion 按映射下发到第三方；
4. 使用“发送记录”接口或控制台查看/检索结果（可按 request_id 回查）。

## 5. 同步发送（简单可靠）

- 接口：`POST /api/v1/notify`
- 请求体（二选一）：
  - `{ "message_name": "<name>", "data": { ... } }`
  - `{ "message_definition_bid": "<bid>", "data": { ... } }`
- 成功响应：`{"results": [{"dispatch_bid","endpoint_bid","status_code","body"}]}`

示例（curl）：

```bash
curl -X POST \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  http://localhost:8080/api/v1/notify \
  -d '{
    "message_name": "simple-text",
    "data": { "text": "hello from vendor" }
  }'
```

适用场景：消息量不大、对实时响应有要求；返回中可直接获取第三方渠道响应。

## 6. 异步发送（高并发友好）

- 接口：`POST /api/v1/notify/async`（202 Accepted）
- 请求体同同步发送，可额外携带 `request_id`（字符串，可由业务生成并保证唯一性），系统会在发送记录中以 remark 存储。
- 成功响应：`{"accepted":true, "request_id":"...", "estimated_dispatches": 2}`

示例：

```bash
REQ=$(uuidgen | tr 'A-Z' 'a-z' | tr -d '-')
curl -X POST \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  http://localhost:8080/api/v1/notify/async \
  -d "{\n  \"message_name\": \"simple-text\",\n  \"data\": { \"text\": \"async hello\" },\n  \"request_id\": \"$REQ\"\n}"
```

注意：当前 `request_id` 用于回查，不做幂等去重。若需严格幂等，可在业务侧保证同一 `request_id` 不重复提交，或后续接入幂等键策略。

## 7. 发送记录查询（API Key）

- 列表：`GET /api/v1/notify/send-records?limit=50&offset=0&message_definition_bid=&notification_api_bid=&status=&start_time=&end_time=&request_id=`
- 单条：`GET /api/v1/notify/send-records/{bid}`
- 明细：`GET /api/v1/notify/send-records/{bid}/details?limit=50&offset=0`

按 `request_id` 回查示例：

```bash
curl -H "Authorization: Bearer $API_KEY" \
  "http://localhost:8080/api/v1/notify/send-records?request_id=$REQ&limit=20&offset=0"
```

返回字段

- 记录：`send_record_bid`、`message_definition_bid`、`notification_api_bid`、`message_name`、`endpoint_name`、`business_system_name`、`send_time`、`result`、`remark`（即 request_id）、`status`、`created_at`
- 明细：`request_payload`、`response_payload`、`error`、`attempt_no`、`sent_at` 等

## 8. 错误码约定

- 401 Unauthorized：API Key 无效/缺失
- 404 Not Found：资源不存在（如消息名错误）
- 5xx：系统异常或第三方渠道错误（建议重试/告警）

## 9. 最佳实践

- 鉴权：统一用 Bearer 方式；API Key 定期轮换
- 异步发送：大流量下建议优先使用 `/notify/async`，并以 `request_id` 回查
- 重试策略：对 5xx 采用指数退避；对 4xx 先排查参数/鉴权
- 可观测性：结合“发送记录”接口与控制台页面，建立告警与看板

## 10. 安全建议

---

## 附：典型对接示例（端到端）

### 示例 A：通用 HTTP JSON API

1. 端点配置（adapter_key = http.generic）：

```json
{
  "method": "POST",
  "url": "https://api.vendor.example.com/v1/notify",
  "timeout": 10,
  "headers": { "Authorization": "Bearer VENDOR_API_TOKEN" }
}
```

2. 消息定义：

```json
{
  "title": "Generic JSON",
  "type": "object",
  "properties": {
    "title": { "type": "string" },
    "content": { "type": "string" },
    "user_id": { "type": "string" }
  },
  "required": ["title", "content"]
}
```

3. 派发映射：

```json
{ "title": "${text}", "content": "通知内容：${text}", "user_id": "${uid}" }
```

4. 调用：参见第 5 节（同步）/第 6 节（异步）。

### 示例 B：Mailgun（HTTP 表单）

1. 端点配置（adapter_key = http.mailgun）：

```json
{
  "url": "https://api.mailgun.net/v3/YOUR_DOMAIN/messages",
  "api_key": "MAILGUN_KEY",
  "body_format": "form",
  "from": "noreply@your.com",
  "to": "user@dest.com"
}
```

2. 映射：

```json
{ "subject": "${subject}", "text": "${text}", "html": "<b>${text}</b>" }
```

### 示例 C：SMTP（直连）

1. 端点配置（transport=smtp, adapter_key=smtp.generic）：

```json
{
  "host": "smtp.your.com",
  "port": 587,
  "use_tls": true,
  "username": "mailer",
  "password": "secret",
  "from": "noreply@your.com",
  "to": "user@dest.com"
}
```

2. 映射：

```json
{ "subject": "${subject}", "text": "${text}", "html": "<p>${text}</p>" }

### 示例 D：微信公众号（WeChat Official Account）

1. 端点配置（adapter_key = channel.wechat_official_account）：

在“通知 API → 新建”中选择：

- `transport=channel`
- `adapter_key=channel.wechat_official_account`

配置示例：

```json
{
  "app_id": "wx1234567890",
  "app_secret": "your-app-secret",
  "language": "zh_CN",
  "timeout": 5
}
```

说明：

- `app_id/app_secret`：来自公众平台后台的服务号 AppID/AppSecret，用于获取 access_token；
- `language`：模板消息语言，通常为 `zh_CN`。

2. 消息定义（模板消息）：

在“消息定义”中创建模板消息定义，结构为“模板请求体模板”，例如：

```json
{
  "template_id": "TM00000001",
  "to_user": "${openid}",
  "data": {
    "first": { "value": "课程预约结果通知" },
    "time": { "value": "${time}" },
    "shifu_title": { "value": "${shifu_title}" },
    "student_name": { "value": "${student_name}" },
    "teacher_name": { "value": "${teacher_name}" }
  },
  "link": {
    "type": "url",
    "url": "${link_url}"
  }
}
```

约定：

- `to_user` 可以使用 `${openid}` 这种占位符，业务在调用 `/notify` 时传入 `data.openid`；
- `data` 下各字段的 `value` 支持 `${var}` 模板占位；
- `link.url` 支持 `${order_no}` 等占位，用于跳转详情页。

3. 派发映射（可选）：

对于简单场景，一般无需额外映射，直接依赖消息定义中的 `${var}` 占位即可。如果需要补充 link 信息，可以在映射中只填 link：

```json
{
  "link": {
    "type": "url",
    "url": "https://example.com/order/${order_no}"
  }
}
```

4. 业务侧调用示例：

```bash
curl -X POST \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  http://localhost:8080/api/v1/notify/ \
  -d '{
    "message_name": "课程预约结果通知",
    "data": {
      "link_url": "https://example.com/order/ORD20251202001",
      "time": "2025-11-29 10:00:00~12:00:00",
      "shifu_title": "TIT园地",
      "student_name": "可可",
      "teacher_name": "麦多多-英文,melody",
      "openid": "oABCD1234567890"
    }
  }'
```

发送后：

- Orion 会按消息定义渲染模板，生成 WeChat 消息体；
- 根据 endpoint 配置中的 app_id/app_secret 获取 access_token 并调用公众号模板消息接口；
- 发送记录可在“发送记录”中按 message_name / endpoint 过滤查看。
```

- 仅在服务端存放 API Key；所有调用通过后端转发
- 强制 HTTPS；限制来源 IP；必要时加入签名/时间戳验证
- 及时禁用不再使用的 Key，避免泄露风险
