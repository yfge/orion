---
id: 2025-09-19T00-00-00Z-feishu-send-test
date: 2025-09-19T08:25:06Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [feishu, endpoints, http]
related_paths:
  - backend/app/api/v1/endpoints.py
  - backend/app/schemas/endpoints.py
  - backend/app/services/sender/http_sender.py
  - frontend/app/systems/[bid]/endpoints/[endpointBid]/page.tsx
  - frontend/lib/api.ts
summary: "打通飞书机器人全流程（最小闭环）：在端点编辑页一键测试发送文本消息，后端使用 HttpSender 将消息发至飞书机器人 webhook。"
---

步骤
- 后端新增：POST /api/v1/endpoints/{endpoint_bid}/send-test，输入 {text}，针对 http.feishu_bot 组装 {msg_type:"text", content:{text}} 并发送。
- 前端在端点编辑页加入“测试发送（Feishu）”输入与按钮，调用 send-test 并回显 HTTP 状态与响应。

使用
- 在系统下新建端点：transport=http，adapter_key=http.feishu_bot，endpoint_url=飞书机器人 webhook；保存。
- 打开该端点编辑页，输入一条测试文本，点击“发送”。
- 在飞书群中应收到消息；页面显示返回状态与响应体。

后续
- 支持签名校验/安全设置（带签名的 Feishu 机器人）；
- 将 JSON 配置表单化（JSON Schema）；
- 为 send-test 增加限流与审计记录。
