import { Sequelize } from 'sequelize'
import mongoose from 'mongoose'
import redis from 'redis'

// MySQL连接（使用Sequelize）
export const sequelize = new Sequelize(
  process.env.MYSQL_DATABASE || 'vue_enterprise',
  process.env.MYSQL_USER || 'root',
  process.env.MYSQL_PASSWORD || 'password',
  {
    host: process.env.MYSQL_HOST || 'localhost',
    port: process.env.MYSQL_PORT || 3306,
    dialect: 'mysql',
    logging: false,
    pool: {
      max: 5,
      min: 0,
      acquire: 30000,
      idle: 10000
    }
  }
)

// MongoDB连接
const MONGODB_URI = process.env.MONGODB_URI || 'mongodb://localhost:27017/vue_enterprise'

export const connectMongoDB = async () => {
  try {
    await mongoose.connect(MONGODB_URI)
    console.log('✅ MongoDB连接成功')
  } catch (error) {
    console.error('❌ MongoDB连接失败:', error.message)
  }
}

// Redis连接
export const redisClient = redis.createClient({
  socket: {
    host: process.env.REDIS_HOST || 'localhost',
    port: process.env.REDIS_PORT || 6379
  },
  password: process.env.REDIS_PASSWORD || undefined
})

export const connectRedis = async () => {
  try {
    await redisClient.connect()
    console.log('✅ Redis连接成功')
  } catch (error) {
    console.error('❌ Redis连接失败:', error.message)
  }
}

// 连接所有数据库
export const connectDB = async () => {
  console.log('\n🔌 正在连接数据库...\n')

  // MySQL
  try {
    await sequelize.authenticate()
    console.log('✅ MySQL连接成功')
  } catch (error) {
    console.warn('⚠️  MySQL连接失败，将在无MySQL的情况下运行:', error.message)
  }

  // MongoDB
  await connectMongoDB()

  // Redis
  await connectRedis()

  console.log('')
}

// 优雅关闭
process.on('SIGINT', async () => {
  console.log('\n正在关闭数据库连接...')
  await sequelize.close()
  await mongoose.connection.close()
  await redisClient.quit()
  console.log('数据库连接已关闭')
  process.exit(0)
})
