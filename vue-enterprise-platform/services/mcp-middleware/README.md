# MCP 中间件服务

通过Docker Compose管理的中间件服务集合。

## 包含服务

| 服务 | 端口 | 说明 |
|------|------|------|
| MySQL | 3306 | 关系型数据库 |
| MongoDB | 27017 | 文档数据库 |
| Redis | 6379 | 缓存数据库 |
| Adminer | 8080 | 数据库管理界面 |
| Redis Commander | 8081 | Redis管理界面 |

## 启动服务

```bash
# 启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down

# 停止并删除数据
docker-compose down -v
```

## 连接信息

### MySQL
- **主机**: localhost
- **端口**: 3306
- **用户**: root
- **密码**: password
- **数据库**: vue_enterprise
- **管理界面**: http://localhost:8080

### MongoDB
- **主机**: localhost
- **端口**: 27017
- **用户**: admin
- **密码**: password
- **数据库**: vue_enterprise
- **连接URI**: mongodb://admin:password@localhost:27017/

### Redis
- **主机**: localhost
- **端口**: 6379
- **密码**: (无)
- **管理界面**: http://localhost:8081

## 数据持久化

数据存储在Docker volumes中：
- `mysql-data`: MySQL数据
- `mongodb-data`: MongoDB数据
- `redis-data`: Redis数据

## 初始化脚本

- `mysql/init/01-init.sql`: MySQL初始化SQL脚本
- `mongodb/init/init.js`: MongoDB初始化JS脚本

## 注意事项

1. 首次启动时会自动执行初始化脚本
2. 确保端口未被占用
3. 可以通过环境变量修改配置
4. 生产环境请修改默认密码
