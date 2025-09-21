# API Keys 管理与调用方式

## 基本使用

- 入口：侧边栏“API Keys”。
- 新建：输入名称/描述，系统返回明文 token（仅显示一次）。
- 调用：推荐 `Authorization: Bearer <token>`；也可用 `X-API-Key` 或 `Basic api:<token>`。
- 启用/禁用：在列表中切换状态；删除后不可调用。
- 隔离：每个用户仅能看到并管理自己创建的 Key（owner_user_bid）。

## API 调用示例

- 创建（需先登录控制台获取用户 Token）：

```bash
curl -X POST \
  -H "Authorization: Bearer $USER_TOKEN" \
  -H "Content-Type: application/json" \
  http://localhost:8080/api/v1/api-keys \
  -d '{"name": "notify-public", "description": "公共调用"}'
```

- 列表：`GET /api/v1/api-keys?limit=50&offset=0&q=`

- 禁用：

```bash
curl -X PATCH \
  -H "Authorization: Bearer $USER_TOKEN" \
  -H "Content-Type: application/json" \
  http://localhost:8080/api/v1/api-keys/$BID \
  -d '{"status": 0}'
```

## 与 Notify 的关系

- 公开 Notify 校验逻辑：优先匹配环境变量 `ORION_PUBLIC_API_KEY`，否则校验 DB 中启用的 API Keys（sha256）。
- 建议统一由“API Keys”页面管理 Key，便于审计与轮换。
