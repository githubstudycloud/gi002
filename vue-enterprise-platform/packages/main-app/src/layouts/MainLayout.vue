<template>
  <a-layout class="main-layout">
    <!-- 顶部导航 -->
    <a-layout-header class="header">
      <div class="logo">
        <h2>Vue企业级平台</h2>
      </div>
      <a-menu
        v-model:selectedKeys="selectedKeys"
        theme="dark"
        mode="horizontal"
        :style="{ lineHeight: '64px' }"
      >
        <a-menu-item key="home" @click="router.push('/home')">
          首页
        </a-menu-item>
        <a-menu-item key="sub-app-1" @click="router.push('/sub-app-1')">
          子应用1
        </a-menu-item>
        <a-menu-item key="sub-app-2" @click="router.push('/sub-app-2')">
          子应用2
        </a-menu-item>
      </a-menu>
      <div class="user-info">
        <a-dropdown>
          <a class="ant-dropdown-link" @click.prevent>
            管理员
            <DownOutlined />
          </a>
          <template #overlay>
            <a-menu>
              <a-menu-item key="profile">个人中心</a-menu-item>
              <a-menu-item key="settings">设置</a-menu-item>
              <a-menu-divider />
              <a-menu-item key="logout" @click="handleLogout">退出登录</a-menu-item>
            </a-menu>
          </template>
        </a-dropdown>
      </div>
    </a-layout-header>

    <a-layout>
      <!-- 侧边栏 -->
      <a-layout-sider v-model:collapsed="collapsed" :trigger="null" collapsible>
        <a-menu
          v-model:selectedKeys="selectedKeys"
          mode="inline"
          :inline-collapsed="collapsed"
          :style="{ height: '100%', borderRight: 0 }"
        >
          <a-menu-item key="dashboard" @click="router.push('/home')">
            <template #icon>
              <DashboardOutlined />
            </template>
            <span>控制台</span>
          </a-menu-item>
          <a-menu-item key="components" @click="openComponentsDemo">
            <template #icon>
              <AppstoreOutlined />
            </template>
            <span>组件示例</span>
          </a-menu-item>
          <a-sub-menu key="sub1">
            <template #icon>
              <UserOutlined />
            </template>
            <template #title>用户管理</template>
            <a-menu-item key="users">用户列表</a-menu-item>
            <a-menu-item key="roles">角色管理</a-menu-item>
          </a-sub-menu>
          <a-sub-menu key="sub2">
            <template #icon>
              <SettingOutlined />
            </template>
            <template #title>系统设置</template>
            <a-menu-item key="config">系统配置</a-menu-item>
            <a-menu-item key="logs">操作日志</a-menu-item>
          </a-sub-menu>
        </a-menu>
      </a-layout-sider>

      <!-- 主内容区 -->
      <a-layout-content class="main-content">
        <div class="content-wrapper">
          <router-view />
        </div>
      </a-layout-content>
    </a-layout>
  </a-layout>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import {
  DownOutlined,
  DashboardOutlined,
  AppstoreOutlined,
  UserOutlined,
  SettingOutlined
} from '@ant-design/icons-vue'
import { useUserStore } from '@/store'

const router = useRouter()
const userStore = useUserStore()

const selectedKeys = ref(['home'])
const collapsed = ref(false)

const handleLogout = () => {
  userStore.logout()
  router.push('/login')
}

const openComponentsDemo = () => {
  window.open('http://localhost:3001', '_blank')
}
</script>

<style lang="scss" scoped>
.main-layout {
  height: 100%;

  .header {
    display: flex;
    align-items: center;
    background: #001529;
    padding: 0 24px;

    .logo {
      width: 200px;
      color: #fff;

      h2 {
        margin: 0;
        font-size: 18px;
        font-weight: 600;
      }
    }

    .ant-menu {
      flex: 1;
    }

    .user-info {
      color: #fff;

      a {
        color: #fff;

        &:hover {
          color: #1890ff;
        }
      }
    }
  }

  .main-content {
    background: #f0f2f5;
    padding: 24px;
    min-height: 280px;

    .content-wrapper {
      background: #fff;
      padding: 24px;
      border-radius: 4px;
      min-height: calc(100vh - 112px);
    }
  }
}
</style>
