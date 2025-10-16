# 微信公众号消息发送集成设计（初稿）

## 背景与目标
- Orion 需要支持微信生态内的服务号/订阅号通知，满足业务侧「事件触达」「模板消息」等场景。
- 核心目标：保证消息可靠投递、可观测、可追踪，遵循现有通知生命周期（pending/sending/success/failed/...）。
- 期望复用既有通道抽象（发送器接口、任务调度、状态机），在领域层新增最小必要扩展。

## 场景与成功判定
- **事务模板消息**：业务事件触发，根据模板 ID 和数据项渲染后发送到指定用户 OpenID；成功以微信返回 `msgid` 且网关状态为 `success` 为准。
- **客服消息补发**：失败或人工干预后，通过客服接口再次推送；要求记录补发动作并限制发送窗口（48 小时）。
- **回执与状态同步**：支持接收微信服务器回调，记录送达/失败原因并触发重试/告警。

## 依赖与输入
- 微信公众平台服务号，开通模板消息或客服消息权限。
- 关键凭证：`AppID`、`AppSecret`、模板 ID 列表、消息示例、服务器回调 Token。
- 预估 QPS/配额：微信单应用默认限流，需在速率限制策略中体现（例如 10 qps，日发送配额与模板消息限制）。

## 集成范围
- **消息类型**：首期支持模板消息（`/cgi-bin/message/template/send`）与客服消息（`/cgi-bin/message/custom/send`）。
- **接入能力**：
  - 调用微信 API 获取并缓存 Access Token。
  - 渲染模板数据字段，支持跳转 URL/小程序路径。
  - 处理微信公众号回调（明文模式起步，后续扩展 AES）。
- **数据记录**：存储发送请求、微信返回 `msgid`、错误码、回调事件。
- **非目标**：暂不支持群发、订阅通知（一次性订阅接口）、素材管理。

## 架构与职责划分
- **核心层（Domain/Services）**：
  - 新增微信公众号渠道实体，定义模板参数、跳转信息等结构体。
  - 扩展网关服务路由表，识别 `channel=wechat_official_account`。
  - 统一重试与状态流转逻辑，区分可重试错误（系统繁忙、超时）与不可重试错误（参数错误、用户拒收）。
- **外部适配层（Adapters）**：
  - 提供 `OAuthTokenProvider` 用于 Access Token 缓存与刷新（Redis/DB/内存策略待定）。
  - 调用微信模板/客服消息 API，封装请求签名、错误码解析、限流处理。
  - 暴露 webhook 处理器验证 `signature|timestamp|nonce` 并解析消息体。
- **配置/基础设施**：
  - 新增渠道配置项（AppID、AppSecret、token 缓存 TTL、API 域名）。
  - 支撑组件：HTTP 客户端（httpx session）、异步任务队列（现有 `backend/tasks/`）。
  - 运行时依赖：Prometheus 指标、结构化日志、告警规则。

## 风险与假设
- Access Token 每次刷新有效期约 2 小时，需要全局共享缓存；假设将使用 Redis（后备：数据库表）。
- 模板字段需预先注册且大小写敏感；需要在请求校验阶段捕获缺失字段。
- 回调接口需要公网可达；本地开发使用隧道或模拟器。
- 需评估微信错误码稳定性，设计映射表并保持可更新。

## 成功交付前的里程碑
1. 设计文档冻结（本文件），确认功能范围与依赖。
2. 完成凭证管理方案并更新运行手册。
3. 后端配置与领域模型到位，确保可编译通过。
4. 适配器、服务、API、回调、监控分阶段上线，配套测试完成。
5. 发布后完成首轮数据回顾并归档 agents_chat 日志。

## 平台准备与凭证管理
- **账号开通**：确认服务号/订阅号主体拥有模板消息或客服消息权限，如未开通需在微信公众平台申请并通过企业认证。
- **模板管理**：与业务方确认模板列表、跳转链接、小程序路径，建立配置登记表（模板英文名称、模板 ID、示例 JSON）。
- **凭证采集**：收集 `AppID`、`AppSecret`、消息模板 ID、消息签名 Token/EncodingAESKey，登记到安全仓库；禁止在代码库硬编码。
- **权限划分**：区分「运营配置」与「推送调用」角色，运营侧负责模板维护，技术侧仅掌握调用凭证。
- **依赖检查**：确认外网出口、回调域名备案情况，准备测试号用于联调。
- **运维手册**：按季度轮换 AppSecret/Token，更新后需在密钥管理平台和 CI/CD Secret 中同步，并通知相关服务重启。

## 凭证滚动策略概要
- AppSecret 与 Token 轮换需遵循最小暴露面：使用密钥管理平台（如 Vault）存储，CI/CD 注入时仅在运行时解密。
- 变更流程：提交安全变更单 -> 运维生成新凭证 -> 在低环境验证 -> 在窗口期同步至生产 -> 观察 30 分钟确保稳定。
- 记录要求：每次轮换需在运行日志与 agents_chat 中记录时间点、责任人和变更摘要。
- 异常预案：若轮换失败导致发送异常，可在 5 分钟内回滚到上一个版本凭证，并触发告警升级。

## 配置与基础设施默认值
- API 基础域名：默认 `https://api.weixin.qq.com`，token 接口 `/cgi-bin/token`；模板与客服消息分别对应 `/cgi-bin/message/template/send`、`/cgi-bin/message/custom/send`。
- Access Token 缓存 TTL：默认 7000 秒（略低于微信官方 7200 秒），用于触发提前刷新。
- 速率限制：默认 400 req/min、突发 40；后续可通过环境变量覆写。
- 重试策略：最大 3 次，初始间隔 0.5 秒，指数退避系数 2.0，上限 30 秒，并引入 10% 抖动。
- 断路器：失败率阈值 50%，最少 20 次调用后生效，冷却 60 秒后尝试半开。
- 错误码分级：可重试代码默认包含 `-1`、`45009`、`50002`；不可重试代码默认包含授权/参数类错误（如 `40001`、`40037`、`48001` 等）。
- 环境变量使用 `ORION_WECHAT_OFFICIAL_ACCOUNT__<字段>` 形式覆写，满足 Pydantic 嵌套配置加载约定。

## 域模型与存储设计
- **实体**：`WechatOfficialAccountMessage` 聚合消息体（模板 ID、接收人 OpenID、跳转类型、数据字段、供应商 msgid、网关状态、失败原因）。
- **凭证缓存**：`WechatAccessTokenSnapshot` 基于 AppID 存储最新 Access Token、过期时间和刷新时间，并记录来源环境。
- **回执事件**：`WechatCallbackEvent` 记录微信推送事件（送达、撤回、用户行为等），保留原始 payload 及解析后的关键字段。
- **关联关系**：消息实体与 `send_records`/`send_details` 通过 send_record_bid 关联，保证跨通道统一追踪；回执事件与消息实体通过 msgid/内部 id 关联。
- **状态流转**：沿用网关状态机（pending → sending → success/failed → retrying/abandoned），并在事件中记录状态变化时间戳。
- **领域事件**：定义 `MessageQueued`, `VendorAccepted`, `VendorFailed`, `RetryScheduled`, `DeliveryConfirmed`, `DeliveryFailed` 等事件，驱动任务队列与告警。

## 适配器与外部集成
- **Access Token Provider**：使用 httpx 调用 `/cgi-bin/token`，凭据来自配置，成功后写入 `wechat_official_account_tokens`（缓存 expires_at、trace_id、environment）。缓存命中时需判断剩余有效期，TTL < 5 分钟时主动刷新。
- **消息发送**：封装模板消息 `/cgi-bin/message/template/send` 与客服消息 `/cgi-bin/message/custom/send`，构建请求体（touser、template_id、data、miniprogram/pagepath 等），附带 idempotency key（`client_msg_id`）避免重复。
- **错误码映射**：维护 `errcode` → 业务异常（认证、频率限制、参数错误等）映射表，转换为领域事件；对 `-1`、`45009` 等系统错误触发重试。
- **HTTP 客户端**：统一使用带审计的 httpx 客户端（超时 5s，可注入代理），日志记录 trace_id、url、errcode。
- **回调校验**：实现 `signature = sha1(sort([token, timestamp, nonce]))` 校验，解密 AES 消息留待后续；若启用 AES 模式，需要根据 EncodingAESKey 解密并校验 appId。
- **Webhook Handler**：暴露 `/api/v1/callbacks/wechat-oa`，支持 GET 验证（echostr）与 POST 消息，入库至 `wechat_official_account_events` 并关联消息聚合。


## 服务编排与业务流程
- **入口**：网关接收 `channel=wechat_official_account` 的请求，调用模板渲染器规范化字段（OpenID、模板 ID、数据项、跳转信息、语言）。
- **消息构建**：生成 `WechatOfficialAccountMessage`，写入 `wechat_official_account_messages`（pending 状态），记录 idempotency key 以支持幂等。
- **发送流程**：调用适配器发送；成功则更新消息状态为 `success` 并保存 `vendor_msg_id`；失败根据错误分类更新状态（failed/retrying）并触发重试策略。
- **重试策略**：结合配置的 `retry_policy`，在任务队列触发延迟重试（指数退避），记录下一次尝试时间与原因。
- **补发/撤回**：补发通过 `RetryScheduled` 事件驱动调用客服消息接口；撤回记录事件并通知业务系统。
- **可观测性**：每次发送与重试写入 `send_details`，回调事件更新消息状态并触发告警。



## 开放问题
- Access Token 缓存介质最终选型？（Redis vs. DB vs. 内存）
- 是否需要同时支持订阅号（限制模板消息能力）？
- 回调推送采用明文还是加密模式作为默认？
- 运营是否需要后台配置管理界面（模板 ID、跳转链接等）？

此文档作为后续实现迭代的规范参考，后续如有范围变更需先更新本文件再调整实现。
