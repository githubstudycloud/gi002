<template>
  <div class="home-page">
    <a-card title="欢迎使用Vue企业级多项目框架平台" :bordered="false">
      <a-row :gutter="[16, 16]">
        <a-col :span="8">
          <a-statistic title="子应用数量" :value="2" suffix="个">
            <template #prefix>
              <AppstoreOutlined />
            </template>
          </a-statistic>
        </a-col>
        <a-col :span="8">
          <a-statistic title="在线用户" :value="128" suffix="人">
            <template #prefix>
              <UserOutlined />
            </template>
          </a-statistic>
        </a-col>
        <a-col :span="8">
          <a-statistic title="系统运行" :value="365" suffix="天">
            <template #prefix>
              <ClockCircleOutlined />
            </template>
          </a-statistic>
        </a-col>
      </a-row>
    </a-card>

    <a-row :gutter="[16, 16]" style="margin-top: 24px">
      <a-col :span="12">
        <a-card title="快速导航" :bordered="false">
          <a-list :data-source="quickLinks">
            <template #renderItem="{ item }">
              <a-list-item>
                <a-list-item-meta>
                  <template #title>
                    <a @click="handleNavigate(item.path)">{{ item.title }}</a>
                  </template>
                  <template #description>{{ item.desc }}</template>
                </a-list-item-meta>
              </a-list-item>
            </template>
          </a-list>
        </a-card>
      </a-col>
      <a-col :span="12">
        <a-card title="技术栈" :bordered="false">
          <a-descriptions :column="1">
            <a-descriptions-item label="前端框架">Vue 3.4 + TypeScript</a-descriptions-item>
            <a-descriptions-item label="构建工具">Vite 5</a-descriptions-item>
            <a-descriptions-item label="UI组件">Element Plus + Ant Design Vue</a-descriptions-item>
            <a-descriptions-item label="状态管理">Pinia 2</a-descriptions-item>
            <a-descriptions-item label="微前端">qiankun 2</a-descriptions-item>
            <a-descriptions-item label="后端服务">Node.js + Express</a-descriptions-item>
          </a-descriptions>
        </a-card>
      </a-col>
    </a-row>

    <a-card title="架构特性" :bordered="false" style="margin-top: 24px">
      <a-row :gutter="[16, 16]">
        <a-col :span="6" v-for="feature in features" :key="feature.title">
          <a-card hoverable>
            <template #cover>
              <div class="feature-icon">
                <component :is="feature.icon" style="font-size: 48px; color: #1890ff" />
              </div>
            </template>
            <a-card-meta :title="feature.title" :description="feature.desc" />
          </a-card>
        </a-col>
      </a-row>
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import {
  AppstoreOutlined,
  UserOutlined,
  ClockCircleOutlined,
  RocketOutlined,
  SafetyOutlined,
  ThunderboltOutlined,
  ApiOutlined
} from '@ant-design/icons-vue'

const router = useRouter()

const quickLinks = ref([
  { title: 'Vue组件功能探究', desc: '查看所有Vue 3组件功能示例', path: 'http://localhost:3001' },
  { title: '子应用1', desc: '业务模块A', path: '/sub-app-1' },
  { title: '子应用2', desc: '业务模块B', path: '/sub-app-2' },
  { title: 'API文档', desc: '查看后端接口文档', path: 'http://localhost:4000/docs' }
])

const features = ref([
  {
    icon: RocketOutlined,
    title: '微前端架构',
    desc: '基于qiankun的微前端解决方案，支持应用独立开发部署'
  },
  {
    icon: SafetyOutlined,
    title: 'TypeScript',
    desc: '全栈TypeScript支持，提供完整的类型安全保障'
  },
  {
    icon: ThunderboltOutlined,
    title: '开发体验',
    desc: 'Vite极速开发，HMR热更新，提升开发效率'
  },
  {
    icon: ApiOutlined,
    title: '中间件集成',
    desc: '集成Redis、MySQL、MongoDB等中间件服务'
  }
])

const handleNavigate = (path: string) => {
  if (path.startsWith('http')) {
    window.open(path, '_blank')
  } else {
    router.push(path)
  }
}
</script>

<style lang="scss" scoped>
.home-page {
  .feature-icon {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 120px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  }

  :deep(.ant-card) {
    margin-bottom: 0;
  }
}
</style>
