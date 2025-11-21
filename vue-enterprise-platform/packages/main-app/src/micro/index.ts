import { registerMicroApps as qiankunRegister, start as qiankunStart, setDefaultMountApp } from 'qiankun'

/**
 * 微应用配置
 */
const microApps = [
  {
    name: 'sub-app-1',
    entry: '//localhost:3002',
    container: '#micro-app-container',
    activeRule: '/sub-app-1',
    props: {
      routerBase: '/sub-app-1'
    }
  },
  {
    name: 'sub-app-2',
    entry: '//localhost:3003',
    container: '#micro-app-container',
    activeRule: '/sub-app-2',
    props: {
      routerBase: '/sub-app-2'
    }
  }
]

/**
 * 注册微应用
 */
export const registerMicroApps = () => {
  qiankunRegister(microApps, {
    beforeLoad: [
      (app) => {
        console.log('[主应用] 开始加载微应用:', app.name)
        return Promise.resolve()
      }
    ],
    beforeMount: [
      (app) => {
        console.log('[主应用] 微应用挂载前:', app.name)
        return Promise.resolve()
      }
    ],
    afterMount: [
      (app) => {
        console.log('[主应用] 微应用挂载完成:', app.name)
        return Promise.resolve()
      }
    ],
    beforeUnmount: [
      (app) => {
        console.log('[主应用] 微应用卸载前:', app.name)
        return Promise.resolve()
      }
    ],
    afterUnmount: [
      (app) => {
        console.log('[主应用] 微应用已卸载:', app.name)
        return Promise.resolve()
      }
    ]
  })
}

/**
 * 启动qiankun
 */
export const start = () => {
  qiankunStart({
    sandbox: {
      experimentalStyleIsolation: true // 样式隔离
    },
    prefetch: true, // 预加载
    singular: false // 是否为单实例场景
  })
}

export { setDefaultMountApp }
