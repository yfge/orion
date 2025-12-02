# 通过统一 Notify 接口使用微信推送

## 概述

本文档描述如何通过 Orion 的统一通知接口 `/api/v1/notify` 发送微信公众号消息。这种方式整合了微信推送到统一的消息调度系统中，支持：

- 📋 **消息模板管理**：在 UI 中配置消息定义和模板
- 🔀 **多渠道调度**：同一消息可同时发送到微信、HTTP、邮件等多个渠道
- 📊 **统一追踪**：所有渠道的发送记录在 `send_records` 表中统一管理
- 🔄 **模板渲染**：使用 `${ }` 语法进行动态变量替换

与直接调用 `/api/v1/notifications/wechat/template` 相比，统一接口更适合需要配置化管理、多渠道调度的场景。

---

## 架构说明

### 两种微信推送方式对比

| 特性 | 统一接口 (`/api/v1/notify`) | 直接接口 (`/api/v1/notifications/wechat/*`) |
|------|---------------------------|-------------------------------------------|
| **配置方式** | UI 配置 → 数据库 | 代码调用时指定 |
| **适用场景** | 需要配置化管理的业务消息 | 临时、一次性推送 |
| **多渠道** | ✅ 支持（同时发送到多个渠道） | ❌ 仅微信 |
| **模板管理** | ✅ UI 管理 | ❌ 代码硬编码 |
| **调度配置** | ✅ 支持 mapping 覆盖 | ❌ 无 |
| **发送记录** | ✅ 统一在 send_records 表 | ✅ 独立在 wechat 表 |

**建议**：
- 生产业务消息（订单通知、支付通知等）→ 使用统一接口
- 临时测试、脚本调用 → 使用直接接口

---

## 配置步骤

### 步骤 1: 创建业务系统

在 Orion UI 中创建或选择业务系统（如"订单系统"）。

### 步骤 2: 创建微信渠道端点

在"通知端点"页面创建新端点：

```json
{
  "name": "微信公众号-订单通知",
  "endpoint_url": "https://api.weixin.qq.com",
  "transport": "channel",
  "adapter_key": "channel.wechat_official_account",
  "config": {
    "app_id": "wx1234567890abcdef",
    "language": "zh_CN"
  }
}
```

**关键字段说明**：
- `transport`: 必须设置为 `"channel"`
- `adapter_key`: 必须设置为 `"channel.wechat_official_account"`
- `config.app_id`: 覆盖全局配置的 AppID（可选，多账号场景）
- `config.language`: 微信消息语言（可选）

### 步骤 3: 创建消息定义

在"消息定义"页面创建消息模板：

```json
{
  "name": "order_shipped_notification",
  "type": "notification",
  "schema": {
    "template_id": "TM00000001",
    "to_user": "${openid}",
    "data": {
      "first": {
        "value": "您的订单已发货"
      },
      "keyword1": {
        "value": "${order_no}"
      },
      "keyword2": {
        "value": "${shipping_company}",
        "color": "#173177"
      },
      "keyword3": {
        "value": "${tracking_no}"
      },
      "remark": {
        "value": "点击查看物流详情"
      }
    },
    "link": {
      "type": "url",
      "url": "https://example.com/orders/${order_no}/tracking"
    }
  }
}
```

**模板变量**：
- 使用 `${变量名}` 语法
- 调用时通过 `data` 参数传入实际值
- 支持嵌套引用（如 URL 中的 `${order_no}`）

### 步骤 4: 创建消息调度

将消息定义关联到微信端点：

1. 选择消息定义"order_shipped_notification"
2. 点击"添加调度"
3. 选择步骤 2 创建的微信端点
4. （可选）配置 Mapping 覆盖字段：

```json
{
  "link": {
    "type": "mini_program",
    "appid": "wx9876543210fedcba",
    "pagepath": "pages/order/logistics?order_no=${order_no}"
  }
}
```

**Mapping 用途**：
- 在消息定义的基础上覆盖或补充字段
- 适用于不同渠道需要不同参数的场景
- 优先级：Mapping > 消息 Schema > 端点 Config

---

## API 调用

### 同步调用

**请求**:
```bash
curl -X POST "https://api.example.com/api/v1/notify" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{
    "message_name": "order_shipped_notification",
    "data": {
      "openid": "oABCD1234567890",
      "order_no": "ORD20251202001",
      "shipping_company": "顺丰速运",
      "tracking_no": "SF1234567890"
    }
  }'
```

**响应**:
```json
{
  "results": [
    {
      "endpoint_bid": "abc123",
      "channel": "wechat_official_account",
      "message_bid": "wechat-msg-001",
      "vendor_msg_id": "1234567890",
      "status": "success",
      "success": true
    }
  ]
}
```

### 异步调用

**请求**:
```bash
curl -X POST "https://api.example.com/api/v1/notify/async" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{
    "message_name": "order_shipped_notification",
    "data": {
      "openid": "oABCD1234567890",
      "order_no": "ORD20251202002",
      "shipping_company": "中通快递",
      "tracking_no": "ZTO9876543210"
    },
    "request_id": "async-req-001"
  }'
```

**响应** (HTTP 202):
```json
{
  "accepted": true,
  "request_id": "async-req-001",
  "estimated_dispatches": 1
}
```

**查询发送记录**:
```bash
curl -X GET "https://api.example.com/api/v1/notify/send-records?request_id=async-req-001" \
  -H "X-API-Key: your-api-key"
```

---

## 高级配置

### 多渠道同时发送

为同一个消息定义添加多个调度（微信 + HTTP Webhook）：

1. 添加微信端点调度（参见步骤 4）
2. 添加 HTTP 端点调度：

```json
{
  "name": "Webhook Notification",
  "endpoint_url": "https://internal-system.com/webhooks/order-update",
  "transport": "http",
  "adapter_key": "http.generic"
}
```

调用 `/api/v1/notify` 时，消息会同时发送到微信和 HTTP 端点，返回结果中包含两个渠道的发送状态。

### 条件调度

通过 `enabled` 字段控制调度是否生效：

```python
# 在数据库或 API 中设置
dispatch.enabled = False  # 禁用此调度
```

### 模板继承与覆盖

**优先级顺序**（从低到高）：

1. **端点 Config**（最低优先级）
   ```json
   {
     "adapter_key": "channel.wechat_official_account",
     "config": {
       "app_id": "wx1234567890",
       "language": "zh_CN"
     }
   }
   ```

2. **消息 Schema**
   ```json
   {
     "schema": {
       "template_id": "TM00000001",
       "to_user": "${openid}",
       "data": { ... },
       "language": "en"
     }
   }
   ```

3. **调度 Mapping**（最高优先级）
   ```json
   {
     "mapping": {
       "language": "zh_TW",
       "link": { ... }
     }
   }
   ```

最终发送时，`language` 为 `"zh_TW"`（Mapping 覆盖了 Schema 和 Config）。

---

## 监控与追踪

### 查询发送记录

**列表查询**:
```bash
curl -X GET "https://api.example.com/api/v1/notify/send-records?message_definition_bid=MSG123&limit=50" \
  -H "X-API-Key: your-api-key"
```

**响应**:
```json
{
  "items": [
    {
      "send_record_bid": "rec001",
      "message_name": "order_shipped_notification",
      "endpoint_name": "微信公众号-订单通知",
      "status": 1,
      "result": {
        "success": true,
        "message_bid": "wechat-msg-001",
        "vendor_msg_id": "1234567890",
        "state": "success"
      },
      "send_time": "2025-12-02T06:30:00Z",
      "remark": "async-req-001"
    }
  ],
  "total": 1,
  "limit": 50,
  "offset": 0
}
```

### 查询发送详情

```bash
curl -X GET "https://api.example.com/api/v1/notify/send-records/rec001/details" \
  -H "X-API-Key: your-api-key"
```

**响应**:
```json
{
  "items": [
    {
      "send_detail_bid": "det001",
      "send_record_bid": "rec001",
      "endpoint_name": "微信公众号-订单通知",
      "attempt_no": 1,
      "request_payload": {
        "template_id": "TM00000001",
        "to_user": "oABCD1234567890",
        "data": { ... },
        "context": { ... },
        "app_id": "wx1234567890",
        "language": "zh_CN"
      },
      "response_payload": {
        "success": true,
        "message_bid": "wechat-msg-001",
        "vendor_msg_id": "1234567890",
        "state": "success"
      },
      "status": 1,
      "sent_at": "2025-12-02T06:30:01Z",
      "error": null
    }
  ],
  "total": 1
}
```

### Prometheus 指标

统一接口会触发微信网关的指标记录：

- `orion_wechat_send_attempts_total{result="success",app_id="wx1234567890",errcode="0"}` - 成功次数
- `orion_wechat_send_latency_seconds{app_id="wx1234567890"}` - 发送延迟

---

## 错误处理

### 常见错误

| 错误类型 | status | 原因 | 解决方案 |
|---------|--------|------|---------|
| 消息定义不存在 | -1 | `message_name` 拼写错误 | 检查消息名称 |
| 渠道未注册 | -1 | `adapter_key` 配置错误 | 确认为 `channel.wechat_official_account` |
| 微信 API 错误 | -1 | access_token 失效、限流等 | 查看 `send_detail.error` 字段 |
| 模板参数缺失 | -1 | `data` 缺少必需变量 | 补充缺失的模板变量 |

### 查看错误详情

```bash
# 查看失败的发送记录
curl -X GET "https://api.example.com/api/v1/notify/send-records?status=-1&limit=10" \
  -H "X-API-Key: your-api-key"
```

查看返回的 `result.error` 字段获取详细错误信息。

---

## 完整示例

### 场景：订单支付成功通知

**1. 配置端点**（在 UI 或通过 API）:
```json
{
  "name": "微信公众号",
  "business_system_bid": "SYS001",
  "endpoint_url": "https://api.weixin.qq.com",
  "transport": "channel",
  "adapter_key": "channel.wechat_official_account",
  "config": {
    "app_id": "wx1234567890abcdef"
  }
}
```

**2. 配置消息定义**:
```json
{
  "name": "order_payment_success",
  "schema": {
    "template_id": "TM12345678",
    "to_user": "${user_openid}",
    "data": {
      "first": {"value": "支付成功"},
      "keyword1": {"value": "${order_no}"},
      "keyword2": {"value": "${amount}"},
      "keyword3": {"value": "${pay_time}"},
      "remark": {"value": "感谢您的购买！"}
    },
    "link": {
      "type": "mini_program",
      "appid": "${mini_program_appid}",
      "pagepath": "pages/order/detail?id=${order_id}"
    }
  }
}
```

**3. 创建调度**（关联消息定义和端点）

**4. 应用代码调用**:
```python
import requests

def notify_order_payment(order):
    response = requests.post(
        "https://api.example.com/api/v1/notify/async",
        headers={
            "X-API-Key": "your-api-key",
            "Content-Type": "application/json"
        },
        json={
            "message_name": "order_payment_success",
            "data": {
                "user_openid": order.user.wechat_openid,
                "order_no": order.order_no,
                "amount": f"{order.amount:.2f}元",
                "pay_time": order.paid_at.strftime("%Y-%m-%d %H:%M:%S"),
                "order_id": order.id,
                "mini_program_appid": "wx9876543210fedcba"
            },
            "request_id": f"order-{order.id}-payment-notify"
        }
    )
    return response.json()
```

---

## 与直接接口的对比

### 使用统一接口
```python
# 1. 在 UI 配置好消息模板
# 2. 调用时只需传递数据
requests.post("/api/v1/notify", json={
    "message_name": "order_shipped",
    "data": {"openid": "...", "order_no": "..."}
})
```

**优点**：
- 配置与代码分离
- 支持多渠道
- 统一发送记录
- 运营可在 UI 中修改模板

### 使用直接接口
```python
# 每次调用需要完整指定所有参数
requests.post("/api/v1/notifications/wechat/template", json={
    "touser": "...",
    "template_id": "TM00000001",
    "data": {
        "first": {"value": "..."},
        "keyword1": {"value": "..."},
        # ... 完整模板结构
    },
    "link": {"type": "url", "url": "..."}
})
```

**优点**：
- 灵活性高
- 无需预配置
- 适合临时调用

---

## 常见问题

### Q1: 如何在统一接口中使用不同的 AppID？

A: 在端点 `config` 中配置 `app_id` 字段：
```json
{
  "adapter_key": "channel.wechat_official_account",
  "config": {
    "app_id": "wx_specific_appid"
  }
}
```

### Q2: 能否同时发送到微信和邮件？

A: 可以！为同一个消息定义添加两个调度（一个微信端点，一个SMTP端点），调用 `/api/v1/notify` 时会同时发送到两个渠道。

### Q3: 如何调试微信模板变量？

A:
1. 查看 `send_records.result` 字段确认是否成功
2. 查看 `send_details.request_payload` 字段查看实际发送的完整payload
3. 对比 payload 中的 `data` 字段与微信模板要求

### Q4: 统一接口的发送记录在哪里？

A: 在 `send_records` 和 `send_details` 表，可通过 `/api/v1/notify/send-records` 查询。微信特有的状态也会记录在 `wechat_official_account_messages` 表中。

### Q5: 如何禁用某个渠道？

A: 在调度配置中设置 `enabled = false`，或在 UI 中禁用该调度。

---

## 参考文档

- [微信公众号 API 文档](./wechat-official-account.md) - 直接接口使用方式
- [微信公众号架构设计](../architecture/channels/wechat-official-account.md) - 底层实现原理
- [微信公众号运行手册](../operations/wechat-official-account-runbook.md) - 运维指南
- [统一通知系统概述](../architecture/overview.md) - 整体架构说明

---

**版本**: v1.0
**更新日期**: 2025-12-02
**维护者**: Orion 团队
