# 快速启动指南

## 安装和启动步骤

### 1. 安装依赖

```bash
cd vue-enterprise-platform

# 安装所有依赖
pnpm install
```

### 2. 启动中间件服务

```bash
cd services/mcp-middleware

# 启动Docker容器
docker-compose up -d

# 检查状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

服务启动后可访问：
- Adminer (数据库管理): http://localhost:8080
- Redis Commander: http://localhost:8081

### 3. 启动后端API服务

```bash
cd services/api-server

# 复制环境变量文件
copy .env.example .env   # Windows
# 或
cp .env.example .env     # Mac/Linux

# 安装依赖
pnpm install

# 启动开发服务器
pnpm dev
```

API服务将在 http://localhost:4000 启动

测试API:
```bash
# 健康检查
curl http://localhost:4000/health

# 获取用户列表
curl http://localhost:4000/api/users
```

### 4. 启动主应用

```bash
cd packages/main-app

# 安装依赖
pnpm install

# 启动开发服务器
pnpm dev
```

主应用将在 http://localhost:3000 启动

### 5. 启动Vue组件探究应用

```bash
cd packages/vue-components-demo

# 安装依赖
pnpm install

# 启动开发服务器
pnpm dev
```

组件Demo将在 http://localhost:3001 启动

## 补充Vue组件示例文件

由于Vue组件示例文件较多，项目已创建了基础架构。以下是需要补充的示例文件模板：

### 基础特性示例

创建 `packages/vue-components-demo/src/examples/basics/` 下的文件：

1. **ClassStyle.vue** - Class与Style绑定
2. **Conditional.vue** - 条件渲染
3. **List.vue** - 列表渲染
4. **Form.vue** - 表单绑定
5. **Transition.vue** - 过渡动画
6. **KeepAliveDemo.vue** - KeepAlive缓存
7. **PluginsDemo.vue** - 插件开发

### 组合式API示例

创建 `packages/vue-components-demo/src/examples/composition-api/` 下的文件：

1. **Setup.vue** - setup语法
2. **Reactive.vue** - 响应式API
3. **ComputedWatch.vue** - computed与watch
4. **Composables.vue** - 组合式函数

### 组件通信示例

创建 `packages/vue-components-demo/src/examples/components/` 下的文件：

1. **PropsDemo.vue** - Props演示
2. **EmitsDemo.vue** - Emits演示
3. **VModelDemo.vue** - v-model双向绑定
4. **DynamicComponent.vue** - 动态组件

### 高级特性示例

创建以下目录和文件：

1. `examples/slots/SlotsDemo.vue` - 插槽
2. `examples/provide-inject/ProvideInject.vue` - 依赖注入
3. `examples/teleport/TeleportDemo.vue` - Teleport
4. `examples/suspense/SuspenseDemo.vue` - Suspense
5. `examples/suspense/AsyncComponent.vue` - 异步组件

### 自定义功能示例

1. `examples/directives/DirectivesDemo.vue` - 自定义指令

### 性能优化示例

创建 `packages/vue-components-demo/src/examples/performance/` 下的文件：

1. **VirtualScroll.vue** - 虚拟滚动
2. **LazyLoad.vue** - 懒加载
3. **MemoDemo.vue** - Memo化

### 生命周期示例

1. `examples/lifecycle/LifecycleHooks.vue` - 生命周期钩子

## 示例文件模板

每个示例文件遵循以下模板：

```vue
<template>
  <DemoContainer
    title="功能标题"
    description="功能描述"
  >
    <el-space direction="vertical" :size="20" style="width: 100%">
      <!-- 示例内容 -->
      <el-card header="示例1">
        <!-- 具体示例代码 -->
      </el-card>

      <!-- 更多示例 -->
    </el-space>
  </DemoContainer>
</template>

<script setup lang="ts">
import DemoContainer from '@/components/DemoContainer.vue'
import CodeBlock from '@/components/CodeBlock.vue'

// 示例逻辑
</script>

<style lang="scss" scoped>
// 样式
</style>
```

## 无Docker环境启动

如果没有Docker环境，后端API服务会自动跳过数据库连接，使用内存数据：

```bash
# 启动后端（会显示数据库连接警告，但不影响运行）
cd services/api-server
pnpm dev

# 前端正常启动
cd packages/main-app
pnpm dev
```

## 测试连接

### 测试后端API

```bash
# 健康检查
curl http://localhost:4000/health

# 获取用户列表
curl http://localhost:4000/api/users

# 创建用户
curl -X POST http://localhost:4000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name":"赵六","email":"zhao@example.com","age":26}'
```

### 测试数据库连接

访问 http://localhost:4000/api/health 查看数据库连接状态

## 常见问题解决

### 端口被占用

修改对应项目的 `vite.config.ts` 或 `.env` 文件中的端口号

### 依赖安装失败

```bash
# 清理缓存重新安装
rm -rf node_modules pnpm-lock.yaml
pnpm install
```

### Docker服务启动失败

```bash
# 查看日志
docker-compose logs

# 重启服务
docker-compose restart

# 完全重建
docker-compose down -v
docker-compose up -d
```

## 下一步

1. 根据上述模板补充Vue组件示例文件
2. 创建子应用项目（sub-app-1, sub-app-2）
3. 完善API服务的数据库模型
4. 添加单元测试
5. 完善文档

## 项目预览

启动所有服务后，访问：

- 主应用: http://localhost:3000
  - 查看微前端架构
  - 测试路由和权限
  - 访问子应用

- Vue组件探究: http://localhost:3001
  - 学习Vue 3所有核心功能
  - 查看组件示例
  - 理解最佳实践

- API文档: http://localhost:4000/api/docs
  - 查看可用API
  - 测试接口

- 数据库管理: http://localhost:8080
  - 管理MySQL和MongoDB
  - 查看表结构和数据
