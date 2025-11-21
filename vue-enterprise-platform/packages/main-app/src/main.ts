import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import Antd from 'ant-design-vue'
import App from './App.vue'
import router from './router'
import { registerMicroApps, start } from './micro'

import 'element-plus/dist/index.css'
import 'ant-design-vue/dist/reset.css'
import './styles/index.scss'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(ElementPlus)
app.use(Antd)

app.mount('#app')

// 注册并启动微前端应用
registerMicroApps()
start()

console.log('主应用已启动 - 端口: 3000')
