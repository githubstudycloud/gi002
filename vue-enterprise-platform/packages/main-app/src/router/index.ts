import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Layout',
    component: () => import('@/layouts/MainLayout.vue'),
    redirect: '/home',
    children: [
      {
        path: '/home',
        name: 'Home',
        component: () => import('@/views/Home.vue'),
        meta: { title: '首页' }
      },
      {
        path: '/sub-app-1/:pathMatch(.*)*',
        name: 'SubApp1',
        component: () => import('@/views/MicroAppContainer.vue'),
        meta: { title: '子应用1' }
      },
      {
        path: '/sub-app-2/:pathMatch(.*)*',
        name: 'SubApp2',
        component: () => import('@/views/MicroAppContainer.vue'),
        meta: { title: '子应用2' }
      }
    ]
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { title: '登录' }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/404.vue')
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  // 设置页面标题
  document.title = (to.meta.title as string) || 'Vue企业级平台'

  // 这里可以添加权限验证逻辑
  const token = localStorage.getItem('token')
  if (to.path !== '/login' && !token) {
    // next('/login')
    next() // 暂时允许所有访问
  } else {
    next()
  }
})

export default router
