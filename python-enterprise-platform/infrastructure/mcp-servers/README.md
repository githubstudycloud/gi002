# MCP服务器配置

本目录包含通过MCP (Model Context Protocol) 连接各种中间件服务的配置。

## 支持的MCP服务器

### 1. PostgreSQL MCP Server
提供PostgreSQL数据库访问能力

### 2. Redis MCP Server
提供Redis缓存访问能力

### 3. MongoDB MCP Server
提供MongoDB文档数据库访问能力

### 4. RabbitMQ MCP Server
提供RabbitMQ消息队列访问能力

### 5. Elasticsearch MCP Server
提供Elasticsearch搜索引擎访问能力

## 配置说明

MCP服务器配置文件位于 `mcp-config.json`，包含所有中间件的连接信息。

## 使用示例

```python
from core_framework.middleware.mcp_client import MCPClient

# 初始化MCP客户端
mcp_client = MCPClient("infrastructure/mcp-servers/mcp-config.json")

# 连接PostgreSQL
await mcp_client.connect("postgresql")

# 执行查询
result = await mcp_client.execute(
    "postgresql",
    "SELECT * FROM users WHERE id = $1",
    [user_id]
)

# 连接Redis
await mcp_client.connect("redis")

# 设置缓存
await mcp_client.execute("redis", "SET", ["key", "value"])
```

## 安全注意事项

1. 不要将包含敏感信息的配置文件提交到版本控制系统
2. 使用环境变量存储密码和密钥
3. 在生产环境中使用加密连接
4. 定期轮换访问凭证
