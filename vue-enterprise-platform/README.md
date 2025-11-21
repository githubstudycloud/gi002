# Vue 企业级多项目框架平台

> 基于 Vue 3 + TypeScript + Vite + qiankun 的企业级微前端解决方案

## 项目简介

这是一个完整的 Vue 3 企业级多项目框架基座，集成了微前端架构、完整的组件示例、后端 API 服务和中间件服务。适合用于学习 Vue 3 的所有特性，以及构建大型企业级应用。

## 核心特性

- ⚡️ **Vite 5** - 极速开发体验
- 🎯 **Vue 3** - Composition API，完整类型支持
- 🔷 **TypeScript** - 全栈类型安全
- 🎨 **双UI框架** - Element Plus + Ant Design Vue
- 🔀 **微前端** - qiankun 2.x，支持应用独立开发部署
- 📦 **Monorepo** - pnpm workspace 统一管理
- 🗃️ **多数据库** - MySQL + MongoDB + Redis
- 🔐 **JWT认证** - 完整的权限控制
- 📝 **完整示例** - 涵盖 Vue 3 所有核心功能

## 项目结构

```
vue-enterprise-platform/
├── packages/                         # 前端应用
│   ├── main-app/                    # 主应用（基座）- 端口 3000
│   ├── vue-components-demo/         # Vue组件功能探究 - 端口 3001
│   ├── sub-app-1/                   # 子应用1 - 端口 3002
│   └── sub-app-2/                   # 子应用2 - 端口 3003
├── services/                         # 后端服务
│   ├── api-server/                  # API服务器 - 端口 4000
│   └── mcp-middleware/              # 中间件服务（Docker）
│       ├── MySQL                    # 端口 3306
│       ├── MongoDB                  # 端口 27017
│       └── Redis                    # 端口 6379
├── shared/                           # 共享代码
│   ├── utils/                       # 工具函数
│   └── types/                       # 类型定义
└── docs/                             # 文档
```

## 端口分配

| 服务 | 端口 | 说明 |
|------|------|------|
| 主应用 | 3000 | 微前端主应用基座 |
| 组件Demo | 3001 | Vue组件功能探究应用 |
| 子应用1 | 3002 | 业务子应用A |
| 子应用2 | 3003 | 业务子应用B |
| API服务 | 4000 | 后端REST API |
| MySQL | 3306 | 关系型数据库 |
| MongoDB | 27017 | 文档数据库 |
| Redis | 6379 | 缓存数据库 |
| Adminer | 8080 | 数据库管理界面 |
| Redis Commander | 8081 | Redis管理界面 |

## 快速开始

### 环境要求

- Node.js >= 18.0.0
- pnpm >= 8.0.0
- Docker (可选，用于运行中间件)

### 安装依赖

```bash
# 克隆项目
git clone <repository-url>
cd vue-enterprise-platform

# 安装依赖
pnpm install
```

### 启动中间件服务（可选）

```bash
cd services/mcp-middleware
docker-compose up -d
```

### 启动后端服务

```bash
cd services/api-server
cp .env.example .env
pnpm install
pnpm dev
```

后端服务将在 http://localhost:4000 启动

### 启动前端应用

```bash
# 方式1: 启动所有应用
pnpm dev

# 方式2: 单独启动
pnpm dev:main    # 主应用 - http://localhost:3000
pnpm dev:demo    # 组件Demo - http://localhost:3001
pnpm dev:sub1    # 子应用1 - http://localhost:3002
pnpm dev:sub2    # 子应用2 - http://localhost:3003
```

### 访问应用

- 主应用: http://localhost:3000
- Vue组件探究: http://localhost:3001
- API文档: http://localhost:4000/api/docs
- 数据库管理: http://localhost:8080
- Redis管理: http://localhost:8081

## Vue 3 组件功能探究

`vue-components-demo` 项目完整展示了 Vue 3 的所有核心功能：

### 基础特性
- ✅ 响应式基础（ref, reactive, computed, watch）
- ✅ 模板语法（插值、指令、事件处理）
- ✅ Class与Style绑定
- ✅ 条件渲染（v-if, v-show）
- ✅ 列表渲染（v-for）
- ✅ 表单输入绑定（v-model）

### 组合式API
- ✅ setup语法糖
- ✅ 响应式API（ref, reactive, toRefs, toRef）
- ✅ 计算属性与侦听器
- ✅ 生命周期钩子
- ✅ 依赖注入（provide/inject）
- ✅ 自定义组合式函数（Composables）

### 组件通信
- ✅ Props父传子
- ✅ Emits子传父
- ✅ v-model双向绑定
- ✅ Attrs透传
- ✅ Slots插槽（默认、具名、作用域）
- ✅ Provide/Inject跨层级通信

### 高级特性
- ✅ 动态组件（component is）
- ✅ 异步组件（defineAsyncComponent）
- ✅ Teleport传送门
- ✅ Suspense异步边界
- ✅ Transition动画过渡
- ✅ KeepAlive组件缓存
- ✅ 自定义指令
- ✅ 插件开发

### 性能优化
- ✅ 虚拟滚动
- ✅ 懒加载
- ✅ 代码分割
- ✅ Memo化（shallowRef/shallowReactive）

## 微前端架构

基于 qiankun 实现的微前端方案：

- 🎯 应用隔离：JS沙箱、样式隔离
- 🔄 应用通信：全局状态、事件总线
- 📦 独立部署：各应用独立开发、部署
- 🔌 动态加载：按需加载子应用
- 🎨 统一布局：主应用提供统一框架

## API服务

后端提供完整的RESTful API：

- 用户管理（CRUD）
- JWT认证
- Redis缓存
- MySQL持久化
- MongoDB文档存储
- 健康检查
- 错误处理

### API端点示例

```bash
# 健康检查
GET http://localhost:4000/health
GET http://localhost:4000/api/health

# 用户管理
GET    http://localhost:4000/api/users       # 获取用户列表
GET    http://localhost:4000/api/users/:id   # 获取单个用户
POST   http://localhost:4000/api/users       # 创建用户
PUT    http://localhost:4000/api/users/:id   # 更新用户
DELETE http://localhost:4000/api/users/:id   # 删除用户

# API文档
GET http://localhost:4000/api/docs
```

## 中间件服务

通过 Docker Compose 管理的中间件服务：

### MySQL
- 端口: 3306
- 用户: root
- 密码: password
- 数据库: vue_enterprise

### MongoDB
- 端口: 27017
- 用户: admin
- 密码: password
- 数据库: vue_enterprise

### Redis
- 端口: 6379
- 密码: (无)

### 管理界面
- Adminer (MySQL/MongoDB): http://localhost:8080
- Redis Commander: http://localhost:8081

## 技术栈

### 前端
- Vue 3.4+
- TypeScript 5.3+
- Vite 5.0+
- Vue Router 4.2+
- Pinia 2.1+
- Element Plus 2.5+
- Ant Design Vue 4.1+
- qiankun 2.10+
- Axios 1.6+

### 后端
- Node.js 18+
- Express 4.18+
- Sequelize 6.35+ (MySQL ORM)
- Mongoose 8.0+ (MongoDB ODM)
- Redis 4.6+
- JWT
- bcryptjs

### 开发工具
- ESLint
- Prettier
- TypeScript
- Sass
- pnpm

## 开发指南

### 代码规范

项目使用 ESLint + Prettier 进行代码规范管理：

```bash
# 代码检查
pnpm lint

# 代码格式化
pnpm format
```

### 构建部署

```bash
# 构建所有项目
pnpm build

# 单独构建
cd packages/main-app && pnpm build
```

### 目录说明

```
main-app/
├── src/
│   ├── micro/          # 微前端配置
│   ├── router/         # 路由配置
│   ├── store/          # 状态管理
│   ├── layouts/        # 布局组件
│   ├── views/          # 页面组件
│   ├── components/     # 公共组件
│   ├── api/            # API接口
│   ├── utils/          # 工具函数
│   └── styles/         # 样式文件
├── public/             # 静态资源
└── package.json
```

## 学习路径

1. **基础入门** - 从 `vue-components-demo` 开始学习 Vue 3 基础特性
2. **组合式API** - 深入理解 Composition API 的使用
3. **组件通信** - 掌握组件间的各种通信方式
4. **高级特性** - 学习动态组件、异步组件、Teleport等
5. **性能优化** - 了解 Vue 3 的性能优化技巧
6. **微前端** - 理解 qiankun 微前端架构
7. **全栈开发** - 学习前后端联调、数据库操作

## 常见问题

### 端口被占用

如果端口被占用，可以修改各项目的端口配置：
- 前端：修改 `vite.config.ts` 中的 `server.port`
- 后端：修改 `.env` 中的 `PORT`

### Docker 相关

```bash
# 查看运行中的容器
docker ps

# 查看日志
docker-compose logs -f mysql

# 重启服务
docker-compose restart

# 清理数据
docker-compose down -v
```

### 数据库连接失败

确保中间件服务已启动：
```bash
cd services/mcp-middleware
docker-compose up -d
docker-compose ps
```

## 贡献指南

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License

## 相关链接

- [Vue 3 文档](https://cn.vuejs.org/)
- [Vite 文档](https://cn.vitejs.dev/)
- [qiankun 文档](https://qiankun.umijs.org/zh)
- [Element Plus](https://element-plus.org/zh-CN/)
- [Ant Design Vue](https://antdv.com/)
- [Pinia](https://pinia.vuejs.org/zh/)

---

⭐ 如果这个项目对你有帮助，请给个 Star！
