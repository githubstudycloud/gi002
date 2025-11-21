# Vue 企业级多项目框架架构设计

## 项目概述
基于 Vue 3 + TypeScript + Vite 的企业级多项目微前端框架基座，支持多个子应用独立开发、部署和运行。

## 技术栈

### 前端技术
- **框架**: Vue 3.4+ (Composition API)
- **构建工具**: Vite 5.x
- **语言**: TypeScript 5.x
- **状态管理**: Pinia 2.x
- **路由**: Vue Router 4.x
- **UI组件库**: Element Plus + Ant Design Vue
- **微前端**: qiankun 2.x
- **HTTP客户端**: Axios
- **工具库**: lodash-es, dayjs

### 后端技术
- **运行时**: Node.js 18+
- **框架**: Express 4.x
- **数据库**: MySQL 8.0, MongoDB 6.0, Redis 7.0
- **ORM**: Sequelize (MySQL), Mongoose (MongoDB)
- **认证**: JWT + Redis Session

### 开发工具
- **代码规范**: ESLint + Prettier
- **Git钩子**: Husky + lint-staged
- **包管理**: pnpm (Monorepo)
- **CSS预处理**: SCSS

## 项目结构

```
vue-enterprise-platform/
├── packages/                    # 前端应用包
│   ├── main-app/               # 主应用（基座）- 端口:3000
│   │   ├── src/
│   │   │   ├── micro/          # 微前端配置
│   │   │   ├── router/         # 路由配置
│   │   │   ├── store/          # 状态管理
│   │   │   ├── layouts/        # 布局组件
│   │   │   ├── api/            # API接口
│   │   │   └── main.ts
│   │   └── package.json
│   ├── vue-components-demo/    # Vue组件功能探究 - 端口:3001
│   │   ├── src/
│   │   │   ├── examples/       # 组件示例
│   │   │   │   ├── basics/     # 基础特性
│   │   │   │   ├── composition-api/  # 组合式API
│   │   │   │   ├── directives/       # 指令
│   │   │   │   ├── lifecycle/        # 生命周期
│   │   │   │   ├── components/       # 组件通信
│   │   │   │   ├── slots/            # 插槽
│   │   │   │   ├── provide-inject/   # 依赖注入
│   │   │   │   ├── teleport/         # 传送门
│   │   │   │   ├── suspense/         # 异步组件
│   │   │   │   └── performance/      # 性能优化
│   │   │   └── main.ts
│   │   └── package.json
│   ├── sub-app-1/              # 子应用1（业务模块A）- 端口:3002
│   └── sub-app-2/              # 子应用2（业务模块B）- 端口:3003
├── services/                   # 后端服务
│   ├── api-server/             # API服务 - 端口:4000
│   │   ├── src/
│   │   │   ├── controllers/
│   │   │   ├── services/
│   │   │   ├── models/
│   │   │   ├── middleware/
│   │   │   ├── routes/
│   │   │   └── app.js
│   │   └── package.json
│   └── mcp-middleware/         # MCP中间件服务 - 端口:4001
│       ├── docker-compose.yml
│       ├── redis/              # Redis - 端口:6379
│       ├── mysql/              # MySQL - 端口:3306
│       └── mongodb/            # MongoDB - 端口:27017
├── shared/                     # 共享代码
│   ├── utils/                  # 工具函数
│   ├── types/                  # TypeScript类型定义
│   └── constants/              # 常量定义
├── docs/                       # 文档
├── pnpm-workspace.yaml         # pnpm工作区配置
├── package.json                # 根package.json
└── README.md

## 端口分配

| 服务名称 | 端口 | 说明 |
|---------|------|------|
| 主应用（基座） | 3000 | 微前端主应用入口 |
| Vue组件Demo | 3001 | Vue组件功能探究应用 |
| 子应用1 | 3002 | 业务子应用A |
| 子应用2 | 3003 | 业务子应用B |
| API服务器 | 4000 | 后端REST API |
| MCP中间件服务 | 4001 | 中间件管理服务 |
| MySQL | 3306 | 数据库 |
| MongoDB | 27017 | 文档数据库 |
| Redis | 6379 | 缓存/会话存储 |

## 核心功能模块

### 1. 主应用（基座）
- 微前端容器配置
- 统一登录认证
- 全局状态管理
- 通用布局（顶部导航、侧边栏、底部）
- 权限控制路由
- 子应用加载管理

### 2. Vue组件功能探究
探究并展示Vue 3所有核心功能：

#### 基础特性
- 响应式基础（ref, reactive, computed, watch）
- 模板语法（插值、指令、事件处理）
- Class与Style绑定
- 条件渲染（v-if, v-show）
- 列表渲染（v-for）
- 表单输入绑定（v-model）

#### 组合式API
- setup语法糖
- 响应式API（ref, reactive, toRefs, toRef）
- 生命周期钩子
- 依赖注入（provide/inject）
- 自定义组合式函数（Composables）

#### 组件通信
- Props父传子
- Emits子传父
- v-model双向绑定
- Attrs透传
- Slots插槽（默认、具名、作用域）
- Provide/Inject跨层级通信
- EventBus模式

#### 高级特性
- 动态组件（component is）
- 异步组件（defineAsyncComponent）
- Teleport传送门
- Suspense异步边界
- Transition动画过渡
- KeepAlive组件缓存
- 自定义指令
- 插件开发

#### 性能优化
- 虚拟滚动
- 懒加载
- 代码分割
- Memo化
- shallowRef/shallowReactive

### 3. 微前端架构
- qiankun主子应用注册
- 应用间通信（全局状态、事件总线）
- 样式隔离
- JS沙箱隔离
- 路由同步

### 4. 后端API服务
- RESTful API设计
- JWT认证中间件
- 请求日志记录
- 错误统一处理
- 数据验证
- CORS配置
- 文件上传
- 分页查询

### 5. MCP中间件集成
- Redis缓存管理
- MySQL数据持久化
- MongoDB文档存储
- 数据库连接池
- 健康检查接口

## 技术亮点

1. **Monorepo管理**: 使用pnpm workspace统一管理多个包
2. **TypeScript全栈**: 前后端完整类型支持
3. **微前端架构**: 支持独立开发部署，团队协作
4. **组件化开发**: 完整的组件示例和最佳实践
5. **中间件集成**: Docker化的数据库服务
6. **开发规范**: 统一的代码风格和提交规范

## 开发流程

1. 克隆项目
2. 安装依赖：`pnpm install`
3. 启动中间件：`cd services/mcp-middleware && docker-compose up -d`
4. 启动后端：`cd services/api-server && pnpm dev`
5. 启动主应用：`cd packages/main-app && pnpm dev`
6. 启动子应用：根据需要启动各子应用

## 部署方案

### 前端部署
- 各应用独立构建
- Nginx反向代理
- CDN静态资源加速

### 后端部署
- Docker容器化
- PM2进程管理
- Nginx负载均衡

### 数据库部署
- Docker Compose编排
- 数据卷持久化
- 定时备份策略
