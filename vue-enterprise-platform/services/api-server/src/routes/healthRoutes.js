import express from 'express'
import { sequelize, redisClient } from '../config/database.js'
import mongoose from 'mongoose'

const router = express.Router()

router.get('/', async (req, res) => {
  const health = {
    status: 'ok',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    databases: {
      mysql: { status: 'unknown', message: '' },
      mongodb: { status: 'unknown', message: '' },
      redis: { status: 'unknown', message: '' }
    }
  }

  // 检查MySQL
  try {
    await sequelize.authenticate()
    health.databases.mysql = { status: 'connected', message: '连接正常' }
  } catch (error) {
    health.databases.mysql = { status: 'disconnected', message: error.message }
  }

  // 检查MongoDB
  try {
    const state = mongoose.connection.readyState
    if (state === 1) {
      health.databases.mongodb = { status: 'connected', message: '连接正常' }
    } else {
      health.databases.mongodb = { status: 'disconnected', message: '未连接' }
    }
  } catch (error) {
    health.databases.mongodb = { status: 'error', message: error.message }
  }

  // 检查Redis
  try {
    if (redisClient.isOpen) {
      await redisClient.ping()
      health.databases.redis = { status: 'connected', message: '连接正常' }
    } else {
      health.databases.redis = { status: 'disconnected', message: '未连接' }
    }
  } catch (error) {
    health.databases.redis = { status: 'error', message: error.message }
  }

  res.json(health)
})

export default router
