# API Keys 管理与调用方式

- 入口：侧边栏“API Keys”。
- 新建：输入名称/描述，系统返回明文 token（仅显示一次）。
- 调用：推荐 `Authorization: Bearer <token>`；也可用 `X-API-Key` 或 `Basic api:<token>`。
- 启用/禁用：在列表中切换状态；删除后不可调用。
- 隔离：每个用户仅能看到并管理自己创建的 Key。
