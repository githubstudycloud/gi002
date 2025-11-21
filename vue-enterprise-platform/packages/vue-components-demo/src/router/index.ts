import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: '/basics/reactivity'
    },
    // 基础特性
    {
      path: '/basics/reactivity',
      component: () => import('@/examples/basics/Reactivity.vue')
    },
    {
      path: '/basics/template-syntax',
      component: () => import('@/examples/basics/TemplateSyntax.vue')
    },
    {
      path: '/basics/class-style',
      component: () => import('@/examples/basics/ClassStyle.vue')
    },
    {
      path: '/basics/conditional',
      component: () => import('@/examples/basics/Conditional.vue')
    },
    {
      path: '/basics/list',
      component: () => import('@/examples/basics/List.vue')
    },
    {
      path: '/basics/form',
      component: () => import('@/examples/basics/Form.vue')
    },
    // 组合式API
    {
      path: '/composition/setup',
      component: () => import('@/examples/composition-api/Setup.vue')
    },
    {
      path: '/composition/reactive',
      component: () => import('@/examples/composition-api/Reactive.vue')
    },
    {
      path: '/composition/computed-watch',
      component: () => import('@/examples/composition-api/ComputedWatch.vue')
    },
    {
      path: '/composition/composables',
      component: () => import('@/examples/composition-api/Composables.vue')
    },
    // 组件通信
    {
      path: '/components/props',
      component: () => import('@/examples/components/PropsDemo.vue')
    },
    {
      path: '/components/emits',
      component: () => import('@/examples/components/EmitsDemo.vue')
    },
    {
      path: '/components/v-model',
      component: () => import('@/examples/components/VModelDemo.vue')
    },
    {
      path: '/components/provide-inject',
      component: () => import('@/examples/provide-inject/ProvideInject.vue')
    },
    // 高级特性
    {
      path: '/advanced/slots',
      component: () => import('@/examples/slots/SlotsDemo.vue')
    },
    {
      path: '/advanced/dynamic',
      component: () => import('@/examples/components/DynamicComponent.vue')
    },
    {
      path: '/advanced/async',
      component: () => import('@/examples/suspense/AsyncComponent.vue')
    },
    {
      path: '/advanced/teleport',
      component: () => import('@/examples/teleport/TeleportDemo.vue')
    },
    {
      path: '/advanced/suspense',
      component: () => import('@/examples/suspense/SuspenseDemo.vue')
    },
    {
      path: '/advanced/transition',
      component: () => import('@/examples/basics/Transition.vue')
    },
    {
      path: '/advanced/keep-alive',
      component: () => import('@/examples/basics/KeepAliveDemo.vue')
    },
    // 自定义功能
    {
      path: '/custom/directives',
      component: () => import('@/examples/directives/DirectivesDemo.vue')
    },
    {
      path: '/custom/plugins',
      component: () => import('@/examples/basics/PluginsDemo.vue')
    },
    // 性能优化
    {
      path: '/performance/virtual-scroll',
      component: () => import('@/examples/performance/VirtualScroll.vue')
    },
    {
      path: '/performance/lazy-load',
      component: () => import('@/examples/performance/LazyLoad.vue')
    },
    {
      path: '/performance/memo',
      component: () => import('@/examples/performance/MemoDemo.vue')
    },
    // 生命周期
    {
      path: '/lifecycle/hooks',
      component: () => import('@/examples/lifecycle/LifecycleHooks.vue')
    }
  ]
})

export default router
