import express from 'express'
import cors from 'cors'
import morgan from 'morgan'
import dotenv from 'dotenv'
import routes from './routes/index.js'
import { errorHandler } from './middleware/errorHandler.js'
import { connectDB } from './config/database.js'

dotenv.config()

const app = express()
const PORT = process.env.PORT || 4000

// 中间件
app.use(cors())
app.use(express.json())
app.use(express.urlencoded({ extended: true }))
app.use(morgan('dev'))

// 健康检查
app.get('/health', (req, res) => {
  res.json({
    status: 'ok',
    timestamp: new Date().toISOString(),
    uptime: process.uptime()
  })
})

// API路由
app.use('/api', routes)

// 错误处理
app.use(errorHandler)

// 连接数据库并启动服务器
const startServer = async () => {
  try {
    // 连接数据库
    await connectDB()

    app.listen(PORT, () => {
      console.log(`\n=================================`)
      console.log(`🚀 API服务器已启动`)
      console.log(`📡 端口: ${PORT}`)
      console.log(`🔗 地址: http://localhost:${PORT}`)
      console.log(`💚 健康检查: http://localhost:${PORT}/health`)
      console.log(`📚 API文档: http://localhost:${PORT}/api/docs`)
      console.log(`=================================\n`)
    })
  } catch (error) {
    console.error('服务器启动失败:', error)
    process.exit(1)
  }
}

startServer()

export default app
