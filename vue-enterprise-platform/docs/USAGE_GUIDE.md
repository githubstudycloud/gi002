# 使用指南

## 快速体验（3分钟）

### 最简启动方式

```bash
# 1. 进入项目目录
cd vue-enterprise-platform

# 2. 安装依赖（仅首次）
pnpm install

# 3. 启动主应用
cd packages/main-app
pnpm dev

# 4. 打开浏览器访问 http://localhost:3000
```

### 体验Vue组件示例

```bash
# 在新终端窗口
cd packages/vue-components-demo
pnpm dev

# 打开浏览器访问 http://localhost:3001
```

### 体验后端API

```bash
# 在新终端窗口
cd services/api-server
cp .env.example .env
pnpm install
pnpm dev

# 访问 http://localhost:4000/api/docs
```

## 完整部署（含数据库）

### 前提条件

- 已安装 Docker Desktop
- 已启动 Docker

### 启动步骤

```bash
# 1. 启动所有中间件
cd services/mcp-middleware
docker-compose up -d

# 等待约30秒，确保数据库初始化完成
docker-compose ps  # 查看状态，确保所有服务都是 Up

# 2. 启动后端API
cd ../../services/api-server
pnpm dev

# 3. 启动主应用
cd ../../packages/main-app
pnpm dev

# 4. 启动组件Demo
cd ../vue-components-demo
pnpm dev
```

### 验证部署

访问以下地址确认服务正常：

- ✅ 主应用: http://localhost:3000
- ✅ 组件Demo: http://localhost:3001
- ✅ API健康检查: http://localhost:4000/health
- ✅ 数据库管理: http://localhost:8080
- ✅ Redis管理: http://localhost:8081

## 功能使用指南

### 1. 主应用功能

#### 登录系统

1. 访问 http://localhost:3000
2. 默认会跳转到登录页
3. 输入用户名: `admin`，密码: `admin123`
4. 点击登录

#### 导航菜单

- **首页**: 查看系统概览和快速链接
- **子应用1**: 微前端子应用（需先创建并启动）
- **子应用2**: 微前端子应用（需先创建并启动）

#### 侧边栏功能

- **控制台**: 返回首页
- **组件示例**: 在新窗口打开Vue组件探究应用
- **用户管理**: 用户列表、角色管理
- **系统设置**: 系统配置、操作日志

### 2. Vue组件探究应用

#### 浏览组件示例

1. 访问 http://localhost:3001
2. 左侧菜单展示所有分类：
   - 基础特性
   - 组合式API
   - 组件通信
   - 高级特性
   - 自定义功能
   - 性能优化
   - 生命周期

3. 点击任意菜单项查看对应示例

#### 已完成示例

- **响应式基础**: ref, reactive, computed, watch 完整演示
- **模板语法**: 插值、指令、事件处理示例

#### 待补充示例

查看 `docs/COMPONENT_EXAMPLES_TODO.md` 了解待创建的示例

### 3. API服务使用

#### 查看API文档

访问 http://localhost:4000/api/docs 查看所有可用API

#### 测试API

使用curl或Postman测试：

```bash
# 获取用户列表
curl http://localhost:4000/api/users

# 获取单个用户
curl http://localhost:4000/api/users/1

# 创建用户
curl -X POST http://localhost:4000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name":"测试用户","email":"test@example.com","age":25}'

# 更新用户
curl -X PUT http://localhost:4000/api/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"更新后的名字"}'

# 删除用户
curl -X DELETE http://localhost:4000/api/users/1
```

#### Redis缓存验证

```bash
# 首次请求（从数据库）
curl http://localhost:4000/api/users
# 响应中包含 "source": "database"

# 再次请求（从缓存）
curl http://localhost:4000/api/users
# 响应中包含 "source": "cache"
```

### 4. 数据库管理

#### Adminer使用

1. 访问 http://localhost:8080
2. 选择数据库类型: MySQL
3. 输入连接信息:
   - 服务器: `mysql`（Docker内部网络）或 `localhost`
   - 用户名: `root`
   - 密码: `password`
   - 数据库: `vue_enterprise`
4. 点击登录

#### Redis Commander使用

1. 访问 http://localhost:8081
2. 自动连接到Redis
3. 查看所有key
4. 可以直接编辑、删除key

### 5. 微前端功能

#### 注册子应用

在 `packages/main-app/src/micro/index.ts` 中配置：

```typescript
const microApps = [
  {
    name: 'sub-app-1',
    entry: '//localhost:3002',
    container: '#micro-app-container',
    activeRule: '/sub-app-1',
    props: {
      routerBase: '/sub-app-1'
    }
  }
]
```

#### 访问子应用

启动子应用后，在主应用中点击对应菜单即可访问

## 开发工作流

### 添加新页面

#### 在主应用中

1. 创建页面组件 `packages/main-app/src/views/NewPage.vue`
2. 在路由中注册 `packages/main-app/src/router/index.ts`
3. 在布局中添加菜单项 `packages/main-app/src/layouts/MainLayout.vue`

#### 在组件Demo中

1. 创建示例组件 `packages/vue-components-demo/src/examples/xxx/Example.vue`
2. 在路由中注册 `packages/vue-components-demo/src/router/index.ts`
3. 在App.vue中添加菜单项

### 添加新API

1. 创建路由文件 `services/api-server/src/routes/xxxRoutes.js`
2. 在 `services/api-server/src/routes/index.js` 中注册
3. 添加控制器逻辑

### 添加数据库模型

#### MySQL (Sequelize)

创建 `services/api-server/src/models/User.js`:

```javascript
import { DataTypes } from 'sequelize'
import { sequelize } from '../config/database.js'

const User = sequelize.define('User', {
  name: {
    type: DataTypes.STRING,
    allowNull: false
  },
  email: {
    type: DataTypes.STRING,
    allowNull: false,
    unique: true
  }
})

export default User
```

#### MongoDB (Mongoose)

创建 `services/api-server/src/models/Article.js`:

```javascript
import mongoose from 'mongoose'

const articleSchema = new mongoose.Schema({
  title: { type: String, required: true },
  content: { type: String, required: true },
  author: { type: String, required: true }
}, { timestamps: true })

export default mongoose.model('Article', articleSchema)
```

## 常见问题解决

### 端口已被占用

```bash
# Windows查找并关闭占用端口的进程
netstat -ano | findstr :3000
taskkill /PID <进程ID> /F

# 或修改端口配置
# vite.config.ts 中修改 server.port
```

### Docker服务无法启动

```bash
# 查看日志
docker-compose logs mysql
docker-compose logs mongodb
docker-compose logs redis

# 重启服务
docker-compose restart

# 完全重建
docker-compose down -v
docker-compose up -d --build
```

### 依赖安装失败

```bash
# 清理并重新安装
rm -rf node_modules pnpm-lock.yaml
pnpm install

# 使用淘宝镜像
pnpm config set registry https://registry.npmmirror.com/
pnpm install
```

### API连接数据库失败

1. 确认Docker服务已启动: `docker-compose ps`
2. 检查环境变量配置: `services/api-server/.env`
3. 查看API日志了解详细错误

### 前端页面空白

1. 检查浏览器控制台错误
2. 确认端口是否正确
3. 尝试清除浏览器缓存
4. 检查路由配置

## 性能优化建议

### 开发环境

1. 使用pnpm而不是npm（已配置）
2. 启用Vite的预构建（已配置）
3. 合理使用HMR，避免全量刷新

### 生产环境

1. 构建前端应用:
```bash
cd packages/main-app
pnpm build
```

2. 启用Gzip压缩
3. 配置CDN加速
4. 使用Nginx反向代理

## 调试技巧

### 前端调试

1. 使用Vue DevTools浏览器扩展
2. 在组件中使用 `console.log` 或 `debugger`
3. 检查Network面板的API请求

### 后端调试

1. 使用nodemon自动重启（已配置）
2. 添加console.log查看请求信息
3. 使用Postman测试API

### 数据库调试

1. 使用Adminer查看数据
2. 使用Redis Commander查看缓存
3. 查看Docker日志: `docker-compose logs -f`

## 最佳实践

### 代码组织

1. 组件尽量保持单一职责
2. 提取公共逻辑到composables
3. 使用TypeScript类型
4. 遵循Vue官方风格指南

### Git工作流

```bash
# 创建功能分支
git checkout -b feature/new-feature

# 提交代码
git add .
git commit -m "feat: add new feature"

# 合并到主分支
git checkout main
git merge feature/new-feature
```

### 命名规范

- 组件: PascalCase (UserList.vue)
- 文件夹: kebab-case (user-management)
- 变量: camelCase (userData)
- 常量: UPPER_SNAKE_CASE (API_BASE_URL)

## 扩展阅读

- [Vue 3 官方文档](https://cn.vuejs.org/)
- [qiankun 微前端文档](https://qiankun.umijs.org/zh)
- [Element Plus 文档](https://element-plus.org/zh-CN/)
- [Ant Design Vue 文档](https://antdv.com/)
- [Vite 文档](https://cn.vitejs.dev/)

## 获取帮助

1. 查看项目文档
2. 搜索已有Issues
3. 提交新Issue
4. 参与讨论

---

祝你使用愉快！如有问题，请参考文档或提交Issue。
