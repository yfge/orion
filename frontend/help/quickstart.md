# 快速开始

本页指引你在 10 分钟内完成从安装到发送一条通知。

## 一、启动与登录

方式 A（推荐）：Docker Compose 一键启动

1. 前置：安装 Docker Desktop（含 Compose）。
2. 在仓库根目录执行：

```bash
docker compose build && docker compose up -d
```

3. 打开控制台 http://localhost:8080，首次注册用户并登录（“用户”页右侧“注册新用户”）。

方式 B：本地开发模式

1. 后端：

```bash
pip install -e backend
scripts/migrate.sh upgrade head
uvicorn backend.app.main:app --reload
```

2. 前端（两种连后端方式二选一）：

- Dev 代理：在 `frontend/.env.local` 配置 `DEV_API_PROXY=http://127.0.0.1:8000`，然后 `npm i && npm run dev`
- 直连后端：在 `frontend/.env.local` 配置 `NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000`，然后 `npm i && npm run dev`

## 二、生成 API Key

1. 登录后进入“API Keys”页，新建一个 Key。系统会显示一次性明文 token。
2. 业务调用公开 Notify API 时，推荐使用 `Authorization: Bearer <token>`。

## 三、创建端到端链路

1. 新建“业务系统”：进入“业务系统”→“新建”。
2. 新建“通知 API”端点：进入“通知 API”→“新建”。常见示例：
   - 飞书机器人：`adapter_key=http.feishu_bot`，`endpoint_url=<飞书 webhook>`
   - Mailgun：`adapter_key=http.mailgun`，配置 URL 与 api_key
   - SendGrid：`adapter_key=http.sendgrid`，配置 URL 与 api_key
   - SMTP：`transport=smtp, adapter_key=smtp.generic`，配置 host/port/TLS/SSL 等
   - 微信公众号：`transport=channel, adapter_key=channel.wechat_official_account`，配置 `app_id/app_secret/language`（详见“第三方集成 → 微信”）
3. 新建“消息定义”：进入“消息定义”→“新建”，示例 schema：

```json
{
  "msg_type": "text",
  "content": { "text": "${text}" }
}
```

4. 建立“派发映射”：在“消息定义”详情页或端点编辑页，添加该消息→端点的映射。邮件类适配器可通过表单设置 `from/to/subject/text/html` 覆盖。
5. “发送测试”：在端点编辑页输入测试文本，验证连通性。

## 四、业务侧调用 Notify

请求示例（Bearer）：

```bash
curl -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  http://localhost:8080/api/v1/notify \
  -d '{
    "message_name": "simple-text",
    "data": { "text": "hello from orion" }
  }'
```

返回结果包含对每个派发端点的状态与 body；具体含义见“Notify API 调用与鉴权”。

## 五、查看发送记录

- “发送记录”页可按时间、消息/端点、状态过滤；点击记录可查看请求/响应详情，便于排障。

## 常见问题

- 401 未授权：请先登录控制台；前端自动携带用户 Token。公开 Notify 则使用 API Key（Bearer）。
- 307 重定向：已统一集合路由为无斜杠风格；如仍遇 307 导致 401，请刷新前端或清除缓存重试。
- 邮件发送失败：检查 `from/to`、域名权限与 SMTP 账号；必要时查看发送记录中的响应。
