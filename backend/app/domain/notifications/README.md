# 微信公众号通知域模型

## 聚合与数据结构
- `WechatOfficialAccountMessage`: 聚合根，描述一次公众号消息发送的上下文，包含模板 ID、接收人 open_id、渲染后的数据、跳转配置、供应商 msgid、网关状态、重试次数。
- `WechatTemplateField`: 对模板数据项的封装，区分 `value`、`color`，支持渲染时的类型转换。
- `WechatLink`: 可跳转资源（URL 或小程序），记录类型、目标与额外参数。
- `WechatNotificationState`: Enum 定义状态机（pending/sending/success/failed/retrying/abandoned）。
- `WechatCallbackEvent`: 微信服务器推送的事件载体，记录事件类型、occurred_at、raw_payload 及解析后的关键信息。
- `WechatAccessTokenSnapshot`: 记录 Access Token 缓存状态（token、expires_at、来源、刷新时间戳），驱动适配器刷新逻辑。

## 领域事件
- `MessageQueued`: 消息入队准备发送。
- `VendorAccepted`: 微信返回成功并提供 `msgid`。
- `VendorFailed`: 微信返回错误码，需要根据重试策略分类处理。
- `RetryScheduled`: 调度下一次重试（包括延迟时间、原因）。
- `DeliveryConfirmed`: 微信回调确认送达。
- `DeliveryFailed`: 微信回调确认失败或用户退订，需要标记为失败/放弃并触发报警。

## 存储映射
- `wechat_official_account_messages`: 对应 `WechatOfficialAccountMessage` 核心字段，与 `send_records` 使用 `send_record_bid` 建立一对一映射。
- `wechat_official_account_events`: 存储 `WechatCallbackEvent`，以 `message_id`/`vendor_msg_id` 关联消息，保留原始 payload 供审计。
- `wechat_official_account_tokens`: 按 AppID 存储 Access Token 缓存及元数据，支持多账号扩展。

## 设计要点
- 所有实体均采用全量 JSON 字段存储原始请求/回执，便于追踪；结构化字段用于检索与状态判断。
- 域层不直接依赖 SQLAlchemy，采用 dataclass/pydantic 模型，通过仓储适配层转换。
- 状态变化将同时生成领域事件，交由任务/告警层消费。
- 所有时间字段使用 UTC，调用层负责时区格式化。
