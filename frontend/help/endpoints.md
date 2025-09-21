# 端点与映射（Endpoints & Dispatches）

- 端点（Endpoints）：配置第三方渠道（HTTP/MQ/SMTP 等），`adapter_key+config` 描述细节。
- 消息定义（Message Definitions）：以 JSON Schema + `${var}` 渲染消息体。
- 派发映射（Dispatches）：将消息与端点建立映射，可在消息页或端点页创建，可包含覆盖字段的 `mapping`。
- 发送记录（Send Records）：展示每次发送的结果与详情，便于排障。

> 小贴士：在端点编辑页使用“发送测试”验证连通性；在映射处优先使用表单（RJSF）减少 JSON 手写错误。
