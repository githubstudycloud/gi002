# Vue组件示例文件待创建清单

## 说明

项目架构已完成，以下是需要补充的Vue组件示例文件列表。每个文件都应该包含完整的功能演示和代码示例。

## 待创建文件清单

### 基础特性 (packages/vue-components-demo/src/examples/basics/)

- [x] Reactivity.vue - 响应式基础（已创建）
- [x] TemplateSyntax.vue - 模板语法（已创建）
- [ ] ClassStyle.vue - Class与Style绑定
- [ ] Conditional.vue - 条件渲染
- [ ] List.vue - 列表渲染
- [ ] Form.vue - 表单输入绑定
- [ ] Transition.vue - 过渡动画
- [ ] KeepAliveDemo.vue - KeepAlive组件缓存
- [ ] PluginsDemo.vue - 插件开发

### 组合式API (packages/vue-components-demo/src/examples/composition-api/)

- [ ] Setup.vue - setup语法糖
- [ ] Reactive.vue - 响应式API详解
- [ ] ComputedWatch.vue - computed与watch
- [ ] Composables.vue - 自定义组合式函数

### 组件通信 (packages/vue-components-demo/src/examples/components/)

- [ ] PropsDemo.vue - Props父传子
- [ ] EmitsDemo.vue - Emits子传父
- [ ] VModelDemo.vue - v-model双向绑定
- [ ] DynamicComponent.vue - 动态组件

### 插槽 (packages/vue-components-demo/src/examples/slots/)

- [ ] SlotsDemo.vue - 插槽（默认、具名、作用域）

### 依赖注入 (packages/vue-components-demo/src/examples/provide-inject/)

- [ ] ProvideInject.vue - Provide/Inject跨层级通信

### Teleport (packages/vue-components-demo/src/examples/teleport/)

- [ ] TeleportDemo.vue - Teleport传送门

### Suspense (packages/vue-components-demo/src/examples/suspense/)

- [ ] SuspenseDemo.vue - Suspense异步边界
- [ ] AsyncComponent.vue - 异步组件

### 自定义指令 (packages/vue-components-demo/src/examples/directives/)

- [ ] DirectivesDemo.vue - 自定义指令

### 性能优化 (packages/vue-components-demo/src/examples/performance/)

- [ ] VirtualScroll.vue - 虚拟滚动
- [ ] LazyLoad.vue - 懒加载
- [ ] MemoDemo.vue - Memo化

### 生命周期 (packages/vue-components-demo/src/examples/lifecycle/)

- [ ] LifecycleHooks.vue - 生命周期钩子

## 示例文件通用模板

```vue
<template>
  <DemoContainer
    title="功能标题"
    description="功能描述"
  >
    <el-space direction="vertical" :size="20" style="width: 100%">
      <!-- 示例1 -->
      <el-card header="基本用法">
        <p>示例代码...</p>
        <CodeBlock
          :code="`// 代码示例\\nconst example = 'Hello'`"
          language="TypeScript"
        />
      </el-card>

      <!-- 示例2 -->
      <el-card header="高级用法">
        <p>更多示例...</p>
      </el-card>
    </el-space>
  </DemoContainer>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import DemoContainer from '@/components/DemoContainer.vue'
import CodeBlock from '@/components/CodeBlock.vue'

// 示例逻辑代码
const example = ref('Hello')
</script>

<style lang="scss" scoped>
// 样式
</style>
```

## 创建示例文件的要点

1. **完整性**: 每个示例应展示该功能的核心用法
2. **代码展示**: 使用 `CodeBlock` 组件展示关键代码
3. **交互性**: 添加按钮、输入框等交互元素
4. **注释说明**: 在代码中添加必要的注释
5. **最佳实践**: 展示Vue官方推荐的写法

## 快速开始开发

即使示例文件未全部创建，项目仍可运行：

```bash
# 1. 安装依赖
pnpm install

# 2. 启动组件Demo应用
cd packages/vue-components-demo
pnpm dev

# 3. 访问 http://localhost:3001
# 已创建的示例可以正常查看
# 未创建的示例会显示404或空白
```

## 批量创建占位文件命令

在项目根目录执行以下命令创建所有占位文件：

```bash
# Windows PowerShell
cd packages/vue-components-demo/src/examples

# 创建基础示例占位文件
New-Item -ItemType File -Path "basics/ClassStyle.vue" -Force
New-Item -ItemType File -Path "basics/Conditional.vue" -Force
New-Item -ItemType File -Path "basics/List.vue" -Force
New-Item -ItemType File -Path "basics/Form.vue" -Force
New-Item -ItemType File -Path "basics/Transition.vue" -Force
New-Item -ItemType File -Path "basics/KeepAliveDemo.vue" -Force
New-Item -ItemType File -Path "basics/PluginsDemo.vue" -Force

# 组合式API示例
New-Item -ItemType File -Path "composition-api/Setup.vue" -Force
New-Item -ItemType File -Path "composition-api/Reactive.vue" -Force
New-Item -ItemType File -Path "composition-api/ComputedWatch.vue" -Force
New-Item -ItemType File -Path "composition-api/Composables.vue" -Force

# 组件通信示例
New-Item -ItemType File -Path "components/PropsDemo.vue" -Force
New-Item -ItemType File -Path "components/EmitsDemo.vue" -Force
New-Item -ItemType File -Path "components/VModelDemo.vue" -Force
New-Item -ItemType File -Path "components/DynamicComponent.vue" -Force

# 其他示例...
```

## 优先级建议

建议按以下优先级创建示例文件：

### 高优先级（核心功能）
1. Setup.vue - setup语法
2. Reactive.vue - 响应式详解
3. PropsDemo.vue - Props通信
4. EmitsDemo.vue - Emits通信
5. SlotsDemo.vue - 插槽

### 中优先级（常用功能）
6. Form.vue - 表单绑定
7. List.vue - 列表渲染
8. Conditional.vue - 条件渲染
9. ComputedWatch.vue - 计算属性与侦听器
10. ProvideInject.vue - 依赖注入

### 低优先级（高级功能）
11. Transition.vue - 过渡动画
12. TeleportDemo.vue - Teleport
13. SuspenseDemo.vue - Suspense
14. DirectivesDemo.vue - 自定义指令
15. VirtualScroll.vue - 虚拟滚动

## 贡献指南

欢迎提交PR补充示例文件！每个示例应该：

1. 包含清晰的功能说明
2. 展示多个使用场景
3. 提供代码示例
4. 添加交互演示
5. 遵循项目代码规范

## 参考资源

- [Vue 3 官方文档](https://cn.vuejs.org/)
- [Vue 3 组合式API文档](https://cn.vuejs.org/api/composition-api-setup.html)
- [Element Plus 组件库](https://element-plus.org/zh-CN/)
