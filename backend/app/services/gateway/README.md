# 网关服务（Gateway）

## 目标
- 负责将上层 API 请求转换为领域消息模型，并选择对应渠道适配器发送。
- 维持通知状态机（pending/sending/success/failed/retrying/abandoned）以及与任务队列、回调处理的协作。

## 结构
- `registry.py`: 注册各渠道的 `ChannelGateway` 实现，按 `channel` 字段路由。
- `base.py`: 定义 `ChannelGateway` 接口（构建消息、发送、重试、撤回）。
- `wechat_official_account.py`: 公众号具体实现，依赖模板渲染器、适配器、仓储。

## 流程概览
1. API 层调用 `NotificationGateway.enqueue(...)`，传入渠道、模板参数、上下文数据。
2. Gateway 解析并渲染消息，写入 `wechat_official_account_messages`，记录 send_record 与领域事件。
3. 调用适配器发送，成功即更新状态并生成 `VendorAccepted` 事件；失败根据错误码决定是否安排重试。
4. 重试任务在 `backend/tasks` 注册（后续实现），依据策略延迟执行 `_retry_send`。
5. 回调处理通过仓储更新消息状态，并触发告警/通知。

## 后续
- 与任务队列、告警系统集成。
- 支持多账号、模板动态配置、按业务系统维度的配额控制。
