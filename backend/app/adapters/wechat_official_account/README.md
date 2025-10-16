# 微信公众号适配器设计

## 组件划分
- `AccessTokenProvider`: 负责使用 AppID/AppSecret 向 `/cgi-bin/token` 拉取凭证，将结果写入/读取 `wechat_official_account_tokens`，并在凭证剩余有效期 < 5 分钟时提前刷新。
- `WeChatOfficialAccountClient`: 基于 httpx 的同步客户端，封装模板消息、客服消息发送接口，支持可观测性日志、重试策略以及 errcode → 领域异常映射。
- `WeChatErrorMapper`: 维护官方 errcode 映射，将其分类为 `retryable`、`non_retryable`、`configuration`、`rate_limit` 等枚举，供上层决策。
- `CallbackVerifier`: 校验微信回调 `signature`/`timestamp`/`nonce`，可选 AES 解密；抽取事件要素并生成 `WechatCallbackEvent`。
- `WebhookHandler`: FastAPI handler 将回调入库 `wechat_official_account_events`，用于驱动状态更新。

## 关键流程
1. **发送前**：
   - 调用 `AccessTokenProvider.get_token(app_id)`，若缓存命中且未接近过期则复用，否则刷新并入库。
   - `WeChatOfficialAccountClient` 组装请求体，带上 `access_token` 作为 query 参数，请求发送后解析 errcode/errmsg。
   - 成功返回 `msgid`，触发 `VendorAccepted` 领域事件；若失败，根据错误分类触发 `VendorFailed` 或 `RetryScheduled`。
2. **回调处理**：
   - GET 验证：返回 `echostr`。
   - POST 消息：`CallbackVerifier` 校验签名，解析事件类型、msgid、状态码；转为领域事件并写入 `wechat_official_account_events`。

## 可观测性
- 请求日志包含 `app_id`, `url`, `errcode`, `request_id`。
- 指标：发送耗时、成功率、按错误码分布；通过后续 metrics 模块导出。

## 外部依赖
- `httpx`、`hashlib`，可选 `cryptography`（AES 解密后续引入）。
- 依赖 `Settings.WECHAT_OFFICIAL_ACCOUNT` 提供默认配置与可重写参数。

该适配器将与服务层（Task 5）协作，提供与领域模型对齐的 API。
