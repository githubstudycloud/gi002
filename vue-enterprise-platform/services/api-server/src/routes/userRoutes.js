import express from 'express'
import { redisClient } from '../config/database.js'

const router = express.Router()

// 模拟用户数据
let users = [
  { id: 1, name: '张三', email: 'zhang@example.com', age: 25 },
  { id: 2, name: '李四', email: 'li@example.com', age: 30 },
  { id: 3, name: '王五', email: 'wang@example.com', age: 28 }
]

// 获取所有用户
router.get('/', async (req, res) => {
  try {
    // 尝试从Redis缓存获取
    if (redisClient.isOpen) {
      const cached = await redisClient.get('users:all')
      if (cached) {
        return res.json({
          success: true,
          data: JSON.parse(cached),
          source: 'cache'
        })
      }
    }

    // 从内存获取并缓存
    if (redisClient.isOpen) {
      await redisClient.setEx('users:all', 60, JSON.stringify(users))
    }

    res.json({
      success: true,
      data: users,
      source: 'database'
    })
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    })
  }
})

// 获取单个用户
router.get('/:id', async (req, res) => {
  try {
    const user = users.find(u => u.id === parseInt(req.params.id))

    if (!user) {
      return res.status(404).json({
        success: false,
        error: '用户不存在'
      })
    }

    res.json({
      success: true,
      data: user
    })
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    })
  }
})

// 创建用户
router.post('/', async (req, res) => {
  try {
    const { name, email, age } = req.body

    if (!name || !email) {
      return res.status(400).json({
        success: false,
        error: '姓名和邮箱为必填项'
      })
    }

    const newUser = {
      id: users.length + 1,
      name,
      email,
      age: age || 0
    }

    users.push(newUser)

    // 清除缓存
    if (redisClient.isOpen) {
      await redisClient.del('users:all')
    }

    res.status(201).json({
      success: true,
      data: newUser
    })
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    })
  }
})

// 更新用户
router.put('/:id', async (req, res) => {
  try {
    const userId = parseInt(req.params.id)
    const userIndex = users.findIndex(u => u.id === userId)

    if (userIndex === -1) {
      return res.status(404).json({
        success: false,
        error: '用户不存在'
      })
    }

    users[userIndex] = {
      ...users[userIndex],
      ...req.body,
      id: userId
    }

    // 清除缓存
    if (redisClient.isOpen) {
      await redisClient.del('users:all')
    }

    res.json({
      success: true,
      data: users[userIndex]
    })
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    })
  }
})

// 删除用户
router.delete('/:id', async (req, res) => {
  try {
    const userId = parseInt(req.params.id)
    const userIndex = users.findIndex(u => u.id === userId)

    if (userIndex === -1) {
      return res.status(404).json({
        success: false,
        error: '用户不存在'
      })
    }

    users.splice(userIndex, 1)

    // 清除缓存
    if (redisClient.isOpen) {
      await redisClient.del('users:all')
    }

    res.json({
      success: true,
      message: '用户已删除'
    })
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    })
  }
})

export default router
