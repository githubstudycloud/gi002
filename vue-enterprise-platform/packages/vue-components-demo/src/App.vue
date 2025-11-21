<template>
  <div class="app">
    <el-container>
      <el-aside width="250px" class="sidebar">
        <div class="logo">
          <h2>Vue3 组件探究</h2>
        </div>
        <el-menu
          :default-active="route.path"
          router
          class="menu"
        >
          <el-sub-menu index="1">
            <template #title>
              <el-icon><Document /></el-icon>
              <span>基础特性</span>
            </template>
            <el-menu-item index="/basics/reactivity">响应式基础</el-menu-item>
            <el-menu-item index="/basics/template-syntax">模板语法</el-menu-item>
            <el-menu-item index="/basics/class-style">Class与Style</el-menu-item>
            <el-menu-item index="/basics/conditional">条件渲染</el-menu-item>
            <el-menu-item index="/basics/list">列表渲染</el-menu-item>
            <el-menu-item index="/basics/form">表单绑定</el-menu-item>
          </el-sub-menu>

          <el-sub-menu index="2">
            <template #title>
              <el-icon><Cpu /></el-icon>
              <span>组合式API</span>
            </template>
            <el-menu-item index="/composition/setup">setup语法</el-menu-item>
            <el-menu-item index="/composition/reactive">响应式API</el-menu-item>
            <el-menu-item index="/composition/computed-watch">computed & watch</el-menu-item>
            <el-menu-item index="/composition/composables">组合式函数</el-menu-item>
          </el-sub-menu>

          <el-sub-menu index="3">
            <template #title>
              <el-icon><Connection /></el-icon>
              <span>组件通信</span>
            </template>
            <el-menu-item index="/components/props">Props父传子</el-menu-item>
            <el-menu-item index="/components/emits">Emits子传父</el-menu-item>
            <el-menu-item index="/components/v-model">v-model双向绑定</el-menu-item>
            <el-menu-item index="/components/provide-inject">Provide/Inject</el-menu-item>
          </el-sub-menu>

          <el-sub-menu index="4">
            <template #title>
              <el-icon><Grid /></el-icon>
              <span>高级特性</span>
            </template>
            <el-menu-item index="/advanced/slots">插槽Slots</el-menu-item>
            <el-menu-item index="/advanced/dynamic">动态组件</el-menu-item>
            <el-menu-item index="/advanced/async">异步组件</el-menu-item>
            <el-menu-item index="/advanced/teleport">Teleport</el-menu-item>
            <el-menu-item index="/advanced/suspense">Suspense</el-menu-item>
            <el-menu-item index="/advanced/transition">Transition</el-menu-item>
            <el-menu-item index="/advanced/keep-alive">KeepAlive</el-menu-item>
          </el-sub-menu>

          <el-sub-menu index="5">
            <template #title>
              <el-icon><MagicStick /></el-icon>
              <span>自定义功能</span>
            </template>
            <el-menu-item index="/custom/directives">自定义指令</el-menu-item>
            <el-menu-item index="/custom/plugins">插件开发</el-menu-item>
          </el-sub-menu>

          <el-sub-menu index="6">
            <template #title>
              <el-icon><Odometer /></el-icon>
              <span>性能优化</span>
            </template>
            <el-menu-item index="/performance/virtual-scroll">虚拟滚动</el-menu-item>
            <el-menu-item index="/performance/lazy-load">懒加载</el-menu-item>
            <el-menu-item index="/performance/memo">Memo化</el-menu-item>
          </el-sub-menu>

          <el-sub-menu index="7">
            <template #title>
              <el-icon><Timer /></el-icon>
              <span>生命周期</span>
            </template>
            <el-menu-item index="/lifecycle/hooks">生命周期钩子</el-menu-item>
          </el-sub-menu>
        </el-menu>
      </el-aside>

      <el-main class="main-content">
        <router-view />
      </el-main>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'

const route = useRoute()
</script>

<style lang="scss">
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body, #app {
  width: 100%;
  height: 100%;
}

.app {
  width: 100%;
  height: 100%;

  .el-container {
    height: 100%;
  }

  .sidebar {
    background: #304156;
    color: #fff;

    .logo {
      height: 60px;
      display: flex;
      align-items: center;
      justify-content: center;
      background: #001529;

      h2 {
        color: #fff;
        font-size: 18px;
      }
    }

    .menu {
      border-right: none;
      background: #304156;
    }
  }

  .main-content {
    background: #f0f2f5;
    padding: 24px;
    overflow-y: auto;
  }
}
</style>
