# 微信公众号凭证管理手册

## 适用范围
- 适用于 Orion 通知网关接入微信公众平台（服务号/订阅号）所需的凭证、模板与回调配置管理。
- 面向运维、安全与开发同事，覆盖测试、预发布、生产环境。

## 准备工作
- 拥有可操作的微信公众平台账号（企业主体已认证）。
- 具备密钥管理平台（如 HashiCorp Vault、AWS Secrets Manager）或等效方案。
- 明确各环境的消息发送域名、回调公网地址及白名单要求。

## 凭证采集流程
1. 登录微信公众平台 → 开发管理 → 开发设置，记录 `AppID(AppID)` 与 `AppSecret`。
2. 在「服务器配置」中生成/更新 `Token`、`EncodingAESKey`，并记录回调 URL（使用 Orion 暴露的公网地址）。
3. 模板消息：在「模板消息」模块申请业务所需模板，记录模板标题、模板 ID、示例参数；导出给业务确认。
4. 客服消息：在「开发者工具」中确认客服接口已启用，若需人工客服账号，提前创建并分配权限。
5. 将上述信息填写到《微信公众号配置登记表》（建议存放在企业网盘或 Confluence），并由安全负责人审核。

## 凭证存储规范
- 所有敏感字段必须写入密钥管理平台，禁止存储在代码库、明文文档或聊天工具。
- 密钥管理平台中按环境分级命名，例如：`orion/wechat_oa/{env}/{key}`。
- CI/CD 与运行环境通过动态注入方式加载凭证（Kubernetes Secret、GitHub Actions OIDC 等）。
- 对敏感字段开启访问审计，记录拉取时间、操作者和用途。

## 环境变量对照
- `ORION_WECHAT_OFFICIAL_ACCOUNT__APP_ID`：AppID，来自公众平台开发设置。
- `ORION_WECHAT_OFFICIAL_ACCOUNT__APP_SECRET`：AppSecret，用于 Access Token 刷新。
- `ORION_WECHAT_OFFICIAL_ACCOUNT__TOKEN`：服务器回调 Token，与微信端保持一致。
- `ORION_WECHAT_OFFICIAL_ACCOUNT__ENCODING_AES_KEY`：回调消息 AES Key。
- `ORION_WECHAT_OFFICIAL_ACCOUNT__API__BASE_URL`：默认 `https://api.weixin.qq.com`，如需代理可覆盖。
- `ORION_WECHAT_OFFICIAL_ACCOUNT__API__TOKEN_TTL_SECONDS`：Access Token 缓存 TTL，默认 7000 秒。
- `ORION_WECHAT_OFFICIAL_ACCOUNT__RATE_LIMIT__REQUESTS_PER_MINUTE`：每分钟限流，默认 400。
- `ORION_WECHAT_OFFICIAL_ACCOUNT__RATE_LIMIT__BURST_SIZE`：突发窗口大小，默认 40。
- `ORION_WECHAT_OFFICIAL_ACCOUNT__RETRY_POLICY__MAX_ATTEMPTS`：最大重试次数，默认 3。
- `ORION_WECHAT_OFFICIAL_ACCOUNT__RETRY_POLICY__INITIAL_INTERVAL_SECONDS`：首次重试间隔，默认 0.5 秒。
- `ORION_WECHAT_OFFICIAL_ACCOUNT__RETRY_POLICY__MAX_INTERVAL_SECONDS`：最大重试间隔，默认 30 秒。
- `ORION_WECHAT_OFFICIAL_ACCOUNT__RETRY_POLICY__MULTIPLIER`：退避倍率，默认 2.0。
- `ORION_WECHAT_OFFICIAL_ACCOUNT__RETRY_POLICY__JITTER`：抖动系数，默认 0.1。
- `ORION_WECHAT_OFFICIAL_ACCOUNT__CIRCUIT_BREAKER__FAILURE_RATE_THRESHOLD`：断路器失败率阈值，默认 0.5。
- `ORION_WECHAT_OFFICIAL_ACCOUNT__CIRCUIT_BREAKER__RECOVERY_TIMEOUT_SECONDS`：断路器冷却时间，默认 60 秒。
- `ORION_WECHAT_OFFICIAL_ACCOUNT__CIRCUIT_BREAKER__MINIMUM_CALLS`：触发断路器的最小调用次数，默认 20。
- `ORION_WECHAT_OFFICIAL_ACCOUNT__RETRYABLE_ERROR_CODES`：JSON 数组形式的可重试错误码，默认 `[-1,45009,50002]`。
- `ORION_WECHAT_OFFICIAL_ACCOUNT__NON_RETRYABLE_ERROR_CODES`：JSON 数组形式不可重试错误码，默认 `[40001,40003,40037,41028,41029,42001,48001,48002]`。

## 模板配置与变更
- 使用 `config/channels/wechat_oa_templates.yaml`（未来实现）维护模板与业务键值映射。
- 变更模板前需进行评审：业务确认字段、链接、合规性；技术确认模板字段标识与渲染逻辑。
- 每次模板变更需在 agents_chat 记录背景、影响范围与验证结果。

## 凭证轮换流程
1. 在密钥管理平台生成新 `AppSecret`/`Token`。
2. 在低环境（dev/staging）更新凭证，触发仪表板/日志监控，至少观察 30 分钟。
3. 准备生产变更窗口，通知相关系统暂停大批量推送。
4. 更新生产密钥管理条目，并触发 Orion 配置刷新/服务重启。
5. 通过健康检查 API 与手工发送消息验证成功。
6. 在 agents_chat 与变更系统归档轮换详情。

## 应急回滚
- 若轮换后发送失败率 > 5% 或回调校验失败：
  - 立即回滚至上一个版本凭证（在密钥管理平台中保留最近两版）。
  - 恢复后打开事故会议，分析失败原因（例如新 Token 未同步到平台）。
  - 完成事故报告并更新本手册中的注意事项。

## 审计与合规要求
- 每半年进行一次权限审计，确保只有运维与安全可访问密钥条目。
- 凭证下载应使用一次性临时文件，并在 24 小时内销毁。
- 对于包含个人信息的模板，需要通过法务合规审核，并在模板登记表中标明。

## 常见问题
- **Access Token 频繁过期**：检查是否存在多进程重复刷新，建议集中在适配器中处理缓存。
- **模板字段缺失**：业务调整模板后需更新配置同步，否则会触发微信 `40037` 等错误码。
- **回调校验失败**：确认 Token/EncodingAESKey 与 Orion 配置一致，且公网入口未被防火墙拦截。

## 参考资料
- [微信公众平台开发文档 - 模板消息](https://developers.weixin.qq.com/doc/offiaccount/Message_Management/Template_Message_Interface.html)
- [微信公众平台开发文档 - 客服消息](https://developers.weixin.qq.com/doc/offiaccount/Message_Management/Service_Center_messages.html)
- [微信公众平台开发文档 - 服务器配置](https://developers.weixin.qq.com/doc/offiaccount/Basic_Information/Access_Overview.html)
