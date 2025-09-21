# 端点与映射（Endpoints & Dispatches）

## 概念速览

- 端点（Endpoints）：配置第三方渠道（HTTP/MQ/SMTP 等），由 `transport + adapter_key + config` 描述。
- 消息定义（Message Definitions）：以 JSON Schema + `${var}` 渲染消息体。
- 派发映射（Dispatches）：将消息与端点建立映射（消息 → 多端点），可附 `mapping` 覆盖字段。
- 发送记录（Send Records）：展示发送结果与详情，辅助排障。

## 操作流程

1. 新建端点：在“通知 API”→“新建”，选择适配器后填写配置表单；HTTP/SMTP 会提供对应 Schema 的表单。
2. 新建消息定义：在“消息定义”→“新建”，输入 JSON Schema（支持 `${var}` 占位）。
3. 建立派发映射：
   - 方式 A：在“消息定义”详情页添加映射（选择端点，填 `mapping`）。
   - 方式 B：在端点编辑页添加映射（选择消息定义，填 `mapping`）。
   - 邮件映射可表单化填写 `from/to/subject/text/html`。
4. 测试发送：端点编辑页“发送测试”，输入文本验证渠道连通。

## API 参考（片段）

- 列出端点（某系统）：`GET /api/v1/systems/{system_bid}/endpoints?limit=50&offset=0&q=`
- 新建端点：`POST /api/v1/systems/{system_bid}/endpoints`
- 端点详情：`GET /api/v1/endpoints/{endpoint_bid}`
- 端点测试发送：`POST /api/v1/endpoints/{endpoint_bid}/send-test`（body: `{ "text": "hi" }`）
- 为消息创建映射：`POST /api/v1/message-definitions/{message_bid}/dispatches`

## 小贴士

- 优先使用映射表单（RJSF），减少 JSON 手写错误。
- 发生错误先查看“发送记录”的 detail：包含请求体与第三方响应。
