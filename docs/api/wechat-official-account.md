# 微信公众号推送 API 接口文档

## 概述

本文档描述微信公众号消息推送的**直接 REST API 接口**，包括模板消息发送、消息状态查询、手动重试等功能。

> **💡 提示**：如果您需要配置化管理消息模板、多渠道调度，请参考 [通过统一 Notify 接口使用微信推送](./unified-notify-wechat.md)。
>
> **两种方式对比**：
> - **本文档（直接接口）**：适合临时调用、脚本集成，需要在代码中指定完整参数
> - **[统一接口](./unified-notify-wechat.md)**：适合生产业务，支持 UI 配置模板、多渠道调度、统一发送记录管理

**Base URL**: `/api/v1/notifications/wechat`

**认证方式**: 所有接口需要提供 API Key（通过 `X-API-Key` 请求头或环境变量配置）

**内容类型**: `application/json`

---

## 接口列表

### 1. 发送模板消息

发送微信公众号模板消息到指定用户。

**端点**: `POST /api/v1/notifications/wechat/template`

**请求头**:
```
Content-Type: application/json
X-API-Key: your-api-key-here
```

#### 请求参数

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `touser` | string | ✅ | 接收者 OpenID，最小长度 1 |
| `template_id` | string | ✅ | 微信公众平台注册的模板 ID |
| `data` | object | ✅ | 模板数据字段，key 为模板变量名 |
| `data.*.value` | string | ✅ | 字段值，支持模板渲染（见下方说明） |
| `data.*.color` | string | ❌ | 字段颜色，十六进制格式如 `#173177` |
| `context` | object | ❌ | 模板渲染上下文，用于变量替换 |
| `link` | object | ❌ | 消息跳转配置 |
| `link.type` | string | ❌ | 跳转类型：`url`（默认）或 `mini_program` |
| `link.url` | string | ❌ | H5 跳转链接（type=url 时使用） |
| `link.appid` | string | ❌ | 小程序 AppID（type=mini_program 时必填） |
| `link.pagepath` | string | ❌ | 小程序页面路径（type=mini_program 时使用） |
| `language` | string | ❌ | 消息语言，如 `zh_CN`、`en`，最大长度 10 |
| `client_msg_id` | string | ❌ | 幂等键，用于防止重复发送 |
| `appid` | string | ❌ | 覆盖默认 AppID（多账号场景） |

#### 请求示例

**基础模板消息**:
```json
{
  "touser": "oABCD1234567890",
  "template_id": "TM00000001",
  "data": {
    "first": {
      "value": "您的订单已发货"
    },
    "keyword1": {
      "value": "顺丰速运"
    },
    "keyword2": {
      "value": "SF1234567890",
      "color": "#173177"
    },
    "remark": {
      "value": "感谢您的购买！"
    }
  }
}
```

**带跳转链接的消息**:
```json
{
  "touser": "oABCD1234567890",
  "template_id": "TM00000002",
  "data": {
    "first": {"value": "活动通知"},
    "keyword1": {"value": "双11促销"},
    "remark": {"value": "点击查看详情"}
  },
  "link": {
    "type": "url",
    "url": "https://example.com/promotion"
  }
}
```

**跳转到小程序的消息**:
```json
{
  "touser": "oABCD1234567890",
  "template_id": "TM00000003",
  "data": {
    "thing1": {"value": "新订单提醒"},
    "time2": {"value": "2025-12-02 14:30"}
  },
  "link": {
    "type": "mini_program",
    "appid": "wx1234567890abcdef",
    "pagepath": "pages/order/detail?id=123"
  }
}
```

**使用模板渲染的消息**:
```json
{
  "touser": "oABCD1234567890",
  "template_id": "TM00000004",
  "data": {
    "first": {
      "value": "尊敬的 {{ user_name }}，您好！"
    },
    "keyword1": {
      "value": "{{ order_amount }} 元"
    }
  },
  "context": {
    "user_name": "张三",
    "order_amount": "299.00"
  }
}
```

**幂等性保证**:
```json
{
  "touser": "oABCD1234567890",
  "template_id": "TM00000005",
  "data": {
    "first": {"value": "支付成功"}
  },
  "client_msg_id": "order-123-payment-notification"
}
```

#### 响应参数

**成功响应** (HTTP 201):
```json
{
  "message_bid": "a1b2c3d4e5f6",
  "state": "success",
  "vendor_msg_id": "1234567890",
  "error": null,
  "retry_scheduled": false
}
```

**失败响应（可重试错误）** (HTTP 201):
```json
{
  "message_bid": "a1b2c3d4e5f6",
  "state": "retrying",
  "vendor_msg_id": null,
  "error": "rate limit exceeded",
  "retry_scheduled": false
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `message_bid` | string | 内部消息唯一标识符，用于后续查询 |
| `state` | string | 消息状态：`success`, `failed`, `retrying`, `sending` |
| `vendor_msg_id` | string | 微信返回的消息 ID（msgid），成功时返回 |
| `error` | string | 错误信息，失败时返回 |
| `retry_scheduled` | boolean | 是否已安排自动重试 |

#### 错误码

| HTTP 状态码 | 说明 |
|------------|------|
| 201 | 请求已接受（成功或已记录失败） |
| 400 | 请求参数错误 |
| 401 | API Key 无效或缺失 |
| 422 | 数据验证失败 |
| 500 | 服务器内部错误 |

---

### 2. 查询消息状态

查询指定消息的详细信息和状态。

**端点**: `GET /api/v1/notifications/wechat/{message_bid}`

**请求头**:
```
X-API-Key: your-api-key-here
```

**路径参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| `message_bid` | string | 发送接口返回的内部消息 ID |

#### 请求示例

```bash
curl -X GET "https://api.example.com/api/v1/notifications/wechat/a1b2c3d4e5f6" \
  -H "X-API-Key: your-api-key-here"
```

#### 响应示例

**成功响应** (HTTP 200):
```json
{
  "message_bid": "a1b2c3d4e5f6",
  "app_id": "wx1234567890",
  "to_user": "oABCD1234567890",
  "template_id": "TM00000001",
  "language": null,
  "link": {
    "type": "url",
    "url": "https://example.com/promotion",
    "app_id": null,
    "path": null
  },
  "data": {
    "first": {"value": "您的订单已发货"},
    "keyword1": {"value": "顺丰速运"}
  },
  "context": {},
  "state": "success",
  "vendor_msg_id": "1234567890",
  "last_error_code": null,
  "last_error_message": null,
  "retry_count": 0,
  "queued_at": "2025-12-02T06:30:00Z",
  "last_attempt_at": "2025-12-02T06:30:01Z",
  "updated_at": "2025-12-02T06:30:01Z"
}
```

**失败消息响应** (HTTP 200):
```json
{
  "message_bid": "x9y8z7w6v5u4",
  "app_id": "wx1234567890",
  "to_user": "oABCD1234567890",
  "template_id": "TM00000002",
  "state": "retrying",
  "vendor_msg_id": null,
  "last_error_code": 45009,
  "last_error_message": "reach max api daily quota limit",
  "retry_count": 2,
  "queued_at": "2025-12-02T06:30:00Z",
  "last_attempt_at": "2025-12-02T06:35:00Z",
  "updated_at": "2025-12-02T06:35:00Z"
}
```

#### 状态说明

| 状态 | 说明 |
|------|------|
| `pending` | 等待发送 |
| `sending` | 发送中 |
| `success` | 发送成功 |
| `failed` | 发送失败（不可重试） |
| `retrying` | 发送失败，等待重试 |
| `abandoned` | 重试次数耗尽，已放弃 |

#### 常见错误码

| 微信 errcode | 说明 | 是否可重试 |
|-------------|------|-----------|
| 0 | 成功 | - |
| 40001 | access_token 无效 | ✅ |
| 40037 | template_id 无效 | ❌ |
| 43004 | 用户拒收 | ❌ |
| 45009 | 接口调用超过限制 | ✅ |
| 47003 | 模板参数不符 | ❌ |
| 48001 | api 功能未授权 | ❌ |
| 50002 | 系统错误 | ✅ |

---

### 3. 手动重试发送

手动触发消息重试（适用于失败或 retrying 状态的消息）。

**端点**: `POST /api/v1/notifications/wechat/{message_bid}/retry`

**请求头**:
```
X-API-Key: your-api-key-here
```

**路径参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| `message_bid` | string | 要重试的消息 ID |

#### 请求示例

```bash
curl -X POST "https://api.example.com/api/v1/notifications/wechat/a1b2c3d4e5f6/retry" \
  -H "X-API-Key: your-api-key-here"
```

#### 响应示例

**重试成功** (HTTP 200):
```json
{
  "message_bid": "a1b2c3d4e5f6",
  "state": "success",
  "vendor_msg_id": "9876543210",
  "error": null,
  "retry_scheduled": false
}
```

**重试失败** (HTTP 200):
```json
{
  "message_bid": "a1b2c3d4e5f6",
  "state": "retrying",
  "vendor_msg_id": null,
  "error": "access_token invalid",
  "retry_scheduled": false
}
```

#### 错误码

| HTTP 状态码 | 说明 |
|------------|------|
| 200 | 重试已执行（查看 state 确认结果） |
| 404 | 消息不存在 |
| 500 | 服务器错误 |

---

## 微信回调接口

### 回调地址配置

在微信公众平台配置服务器地址：

**回调 URL**: `https://your-domain.com/api/v1/callbacks/wechat-oa`

**Token**: 需要在环境变量 `ORION_WECHAT_OFFICIAL_ACCOUNT__TOKEN` 中配置

**加密方式**: 明文模式或 AES 加密（需配置 EncodingAESKey）

### 回调验证 (GET)

微信首次配置时发送 GET 请求验证服务器。

**端点**: `GET /api/v1/callbacks/wechat-oa`

**查询参数**:
- `signature`: 微信加密签名
- `timestamp`: 时间戳
- `nonce`: 随机数
- `echostr`: 随机字符串

**响应**: 原样返回 `echostr` 参数值

### 接收事件推送 (POST)

微信推送消息状态和用户事件。

**端点**: `POST /api/v1/callbacks/wechat-oa`

**查询参数**:
- `signature`: 微信加密签名
- `timestamp`: 时间戳
- `nonce`: 随机数
- `msg_signature`: 消息签名（加密模式）
- `encrypt_type`: 加密类型（加密模式）

**请求体**: XML 格式的事件数据

```xml
<xml>
  <ToUserName><![CDATA[gh_xxx]]></ToUserName>
  <FromUserName><![CDATA[oABCD1234567890]]></FromUserName>
  <CreateTime>1640000000</CreateTime>
  <MsgType><![CDATA[event]]></MsgType>
  <Event><![CDATA[TEMPLATESENDJOBFINISH]]></Event>
  <MsgID>1234567890</MsgID>
  <Status><![CDATA[success]]></Status>
</xml>
```

**响应**: 返回 `"success"` 字符串

---

## 最佳实践

### 1. 幂等性保证

使用 `client_msg_id` 防止重复发送：

```json
{
  "touser": "oABCD1234567890",
  "template_id": "TM00000001",
  "data": {...},
  "client_msg_id": "order-12345-payment-notification"
}
```

### 2. 错误处理

```javascript
const response = await fetch('/api/v1/notifications/wechat/template', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-API-Key': 'your-api-key'
  },
  body: JSON.stringify(payload)
});

const result = await response.json();

if (result.state === 'success') {
  console.log('发送成功:', result.vendor_msg_id);
} else if (result.state === 'retrying') {
  console.warn('发送失败，已安排重试:', result.error);
  // 可以稍后通过 message_bid 查询状态
} else {
  console.error('发送失败:', result.error);
}
```

### 3. 状态轮询

对于需要确认送达的场景：

```javascript
async function waitForDelivery(messageBid, maxAttempts = 10) {
  for (let i = 0; i < maxAttempts; i++) {
    const response = await fetch(`/api/v1/notifications/wechat/${messageBid}`);
    const detail = await response.json();

    if (detail.state === 'success') {
      return { success: true, vendorMsgId: detail.vendor_msg_id };
    } else if (detail.state === 'failed' || detail.state === 'abandoned') {
      return { success: false, error: detail.last_error_message };
    }

    // 等待 2 秒后重试
    await new Promise(resolve => setTimeout(resolve, 2000));
  }

  return { success: false, error: 'timeout' };
}
```

### 4. 模板渲染

利用 `context` 动态渲染模板内容：

```json
{
  "touser": "oABCD1234567890",
  "template_id": "TM00000001",
  "data": {
    "first": {
      "value": "尊敬的 {{ customer_name }}，您好！"
    },
    "keyword1": {
      "value": "订单号：{{ order_no }}"
    },
    "keyword2": {
      "value": "{{ order_time }}"
    },
    "remark": {
      "value": "您的订单已完成，感谢您的信任！"
    }
  },
  "context": {
    "customer_name": "李四",
    "order_no": "202512020001",
    "order_time": "2025-12-02 14:30:00"
  }
}
```

### 5. 多账号支持

覆盖默认 AppID：

```json
{
  "touser": "oABCD1234567890",
  "template_id": "TM00000001",
  "data": {...},
  "appid": "wx9876543210fedcba"
}
```

---

## 限流与速率

### 微信官方限制

- **模板消息**: 根据公众号类型和认证状态不同，日发送量限制为数千到数百万不等
- **接口调用频率**: 默认 10 次/秒（部分接口更低）
- **单用户限制**: 同一用户每月接收模板消息有上限

### Orion 系统限制

通过配置控制：

```bash
# 环境变量
ORION_WECHAT_OFFICIAL_ACCOUNT__RATE_LIMIT__REQUESTS_PER_MINUTE=400
ORION_WECHAT_OFFICIAL_ACCOUNT__RATE_LIMIT__BURST=40
```

**建议**:
- 生产环境设置为微信限制的 80%，预留缓冲
- 监控 `orion_wechat_send_attempts_total` 指标
- 当收到 errcode 45009（频率限制）时，系统会自动重试

---

## 可观测性

### 指标

- `orion_wechat_send_attempts_total{result,app_id,errcode}`: 发送尝试次数
- `orion_wechat_send_latency_seconds{app_id}`: 发送延迟分布
- `orion_wechat_callback_events_total{event_type,status}`: 回调事件统计

### 日志

发送日志示例：
```json
{
  "event": "wechat.template.send.success",
  "message_bid": "a1b2c3d4e5f6",
  "vendor_msg_id": "1234567890",
  "app_id": "wx1234567890",
  "latency_ms": 156.78
}
```

失败日志示例：
```json
{
  "event": "wechat.template.send.failure",
  "message_bid": "a1b2c3d4e5f6",
  "app_id": "wx1234567890",
  "errcode": 45009,
  "errmsg": "reach max api daily quota limit",
  "retry_scheduled": true,
  "latency_ms": 234.56
}
```

---

## 常见问题

### Q1: 消息发送后显示 "retrying" 状态，如何处理？

A: `retrying` 状态表示首次发送失败，但错误可重试（如网络超时、限流）。系统会自动重试，您可以：
- 通过 GET 接口轮询状态变化
- 查看 `last_error_code` 确认失败原因
- 必要时使用 retry 接口手动重试

### Q2: 如何确认消息真正送达用户？

A:
1. 检查响应中的 `state` 为 `success` 且有 `vendor_msg_id`
2. 监听微信回调事件（推荐），回调会确认用户是否接收
3. 查询接口可查看 `last_attempt_at` 确认最后尝试时间

### Q3: errcode 40001 (access_token invalid) 如何处理？

A: 系统会自动刷新 Access Token 并重试。如果持续出现：
- 检查 `ORION_WECHAT_OFFICIAL_ACCOUNT__APP_ID` 和 `APP_SECRET` 配置
- 确认公众号未被封禁
- 查看日志中的 token 刷新记录

### Q4: 可以批量发送吗？

A: 当前版本不支持批量接口，建议：
- 并发调用发送接口（注意控制并发数在速率限制内）
- 使用相同的 `app_id` 共享 token 缓存
- 监控限流指标，避免触发 errcode 45009

### Q5: 如何测试接口？

A:
1. 使用微信公众平台测试号（免费申请）
2. 配置测试账号的 AppID、AppSecret、Token
3. 使用测试号的 OpenID 进行发送测试
4. 查看公众平台后台的"模板消息记录"确认

---

## 相关文档

- [架构设计](../architecture/channels/wechat-official-account.md)
- [运行手册](../operations/wechat-official-account-runbook.md)
- [可观测性指南](../operations/wechat-official-account-observability.md)
- [凭证管理](../operations/wechat-official-account-credentials.md)
- [微信官方文档](https://developers.weixin.qq.com/doc/offiaccount/Message_Management/Template_Message_Interface.html)

---

**版本**: v1.0
**更新日期**: 2025-12-02
**维护者**: Orion 团队
