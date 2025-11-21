import express from 'express'
import userRoutes from './userRoutes.js'
import healthRoutes from './healthRoutes.js'

const router = express.Router()

// API文档首页
router.get('/', (req, res) => {
  res.json({
    message: 'Vue企业级平台 API服务',
    version: '1.0.0',
    endpoints: {
      health: '/api/health',
      users: '/api/users',
      docs: '/api/docs'
    }
  })
})

// API文档
router.get('/docs', (req, res) => {
  res.json({
    title: 'API文档',
    version: '1.0.0',
    baseUrl: '/api',
    endpoints: [
      {
        path: '/health',
        method: 'GET',
        description: '健康检查和数据库状态'
      },
      {
        path: '/users',
        method: 'GET',
        description: '获取用户列表'
      },
      {
        path: '/users/:id',
        method: 'GET',
        description: '获取单个用户信息'
      },
      {
        path: '/users',
        method: 'POST',
        description: '创建新用户',
        body: {
          name: 'string',
          email: 'string',
          age: 'number'
        }
      }
    ]
  })
})

// 路由模块
router.use('/health', healthRoutes)
router.use('/users', userRoutes)

export default router
