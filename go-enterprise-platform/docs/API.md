# API 文档

## 用户服务 API

基础 URL: `http://localhost:8081/api/v1`

### 统一响应格式

```json
{
  "code": 0,
  "message": "success",
  "data": {}
}
```

### 错误码

| 错误码 | 说明 |
|--------|------|
| 0 | 成功 |
| 1000 | 内部服务器错误 |
| 1001 | 参数错误 |
| 1002 | 资源未找到 |
| 1003 | 未授权 |
| 1004 | 禁止访问 |
| 2000 | 用户未找到 |
| 2001 | 用户已存在 |
| 2002 | 密码错误 |
| 2003 | 用户已禁用 |

## 用户相关接口

### 1. 用户注册

**接口**: `POST /users/register`

**请求参数**:
```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "password123",
  "nickname": "Test User"
}
```

**参数说明**:
- `username` (必填): 用户名，3-50 字符
- `email` (必填): 邮箱地址
- `password` (必填): 密码，最少 6 字符
- `nickname` (可选): 昵称，最多 50 字符

**成功响应**:
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "nickname": "Test User",
    "avatar": "",
    "status": 1,
    "created_at": "2025-01-20T10:00:00Z",
    "updated_at": "2025-01-20T10:00:00Z"
  }
}
```

**错误响应**:
```json
{
  "code": 2001,
  "message": "username already exists"
}
```

**示例**:
```bash
curl -X POST http://localhost:8081/api/v1/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123",
    "nickname": "Test User"
  }'
```

---

### 2. 用户登录

**接口**: `POST /users/login`

**请求参数**:
```json
{
  "username": "testuser",
  "password": "password123"
}
```

**参数说明**:
- `username` (必填): 用户名
- `password` (必填): 密码

**成功响应**:
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "token": "mock-token-1",
    "user": {
      "id": 1,
      "username": "testuser",
      "email": "test@example.com",
      "nickname": "Test User",
      "avatar": "",
      "status": 1,
      "created_at": "2025-01-20T10:00:00Z",
      "updated_at": "2025-01-20T10:00:00Z"
    }
  }
}
```

**错误响应**:
```json
{
  "code": 2000,
  "message": "user not found"
}
```

或

```json
{
  "code": 2002,
  "message": "invalid password"
}
```

**示例**:
```bash
curl -X POST http://localhost:8081/api/v1/users/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "password123"
  }'
```

---

### 3. 获取用户信息

**接口**: `GET /users/:id`

**路径参数**:
- `id`: 用户 ID

**成功响应**:
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "nickname": "Test User",
    "avatar": "",
    "status": 1,
    "created_at": "2025-01-20T10:00:00Z",
    "updated_at": "2025-01-20T10:00:00Z"
  }
}
```

**错误响应**:
```json
{
  "code": 2000,
  "message": "user not found"
}
```

**示例**:
```bash
curl http://localhost:8081/api/v1/users/1
```

---

### 4. 更新用户信息

**接口**: `PUT /users/:id`

**路径参数**:
- `id`: 用户 ID

**请求参数**:
```json
{
  "nickname": "New Nickname",
  "avatar": "https://example.com/avatar.jpg"
}
```

**参数说明**:
- `nickname` (可选): 昵称，最多 50 字符
- `avatar` (可选): 头像 URL，最多 255 字符

**成功响应**:
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "nickname": "New Nickname",
    "avatar": "https://example.com/avatar.jpg",
    "status": 1,
    "created_at": "2025-01-20T10:00:00Z",
    "updated_at": "2025-01-20T10:05:00Z"
  }
}
```

**示例**:
```bash
curl -X PUT http://localhost:8081/api/v1/users/1 \
  -H "Content-Type: application/json" \
  -d '{
    "nickname": "New Nickname",
    "avatar": "https://example.com/avatar.jpg"
  }'
```

---

### 5. 删除用户

**接口**: `DELETE /users/:id`

**路径参数**:
- `id`: 用户 ID

**成功响应**:
```json
{
  "code": 0,
  "message": "success",
  "data": null
}
```

**示例**:
```bash
curl -X DELETE http://localhost:8081/api/v1/users/1
```

---

### 6. 用户列表

**接口**: `GET /users`

**查询参数**:
- `page` (可选): 页码，默认 1
- `page_size` (可选): 每页数量，默认 10，最大 100

**成功响应**:
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "list": [
      {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "nickname": "Test User",
        "avatar": "",
        "status": 1,
        "created_at": "2025-01-20T10:00:00Z",
        "updated_at": "2025-01-20T10:00:00Z"
      }
    ],
    "total": 100,
    "page": 1,
    "page_size": 10
  }
}
```

**示例**:
```bash
curl "http://localhost:8081/api/v1/users?page=1&page_size=10"
```

---

## 系统接口

### 健康检查

**接口**: `GET /health`

**成功响应**:
```json
{
  "status": "ok",
  "time": 1705744800
}
```

**示例**:
```bash
curl http://localhost:8081/health
```

---

### Metrics 监控

**接口**: `GET /metrics`

**响应**: Prometheus 格式的监控指标

**示例**:
```bash
curl http://localhost:8081/metrics
```

---

## Postman 集合

可以导入以下 Postman 集合进行测试：

```json
{
  "info": {
    "name": "Go Enterprise Platform - User Service",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "User Register",
      "request": {
        "method": "POST",
        "url": "http://localhost:8081/api/v1/users/register",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"username\": \"testuser\",\n  \"email\": \"test@example.com\",\n  \"password\": \"password123\",\n  \"nickname\": \"Test User\"\n}"
        }
      }
    },
    {
      "name": "User Login",
      "request": {
        "method": "POST",
        "url": "http://localhost:8081/api/v1/users/login",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"username\": \"testuser\",\n  \"password\": \"password123\"\n}"
        }
      }
    },
    {
      "name": "Get User",
      "request": {
        "method": "GET",
        "url": "http://localhost:8081/api/v1/users/1"
      }
    },
    {
      "name": "Update User",
      "request": {
        "method": "PUT",
        "url": "http://localhost:8081/api/v1/users/1",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"nickname\": \"New Nickname\",\n  \"avatar\": \"https://example.com/avatar.jpg\"\n}"
        }
      }
    },
    {
      "name": "Delete User",
      "request": {
        "method": "DELETE",
        "url": "http://localhost:8081/api/v1/users/1"
      }
    },
    {
      "name": "List Users",
      "request": {
        "method": "GET",
        "url": "http://localhost:8081/api/v1/users?page=1&page_size=10"
      }
    }
  ]
}
```

保存为 `postman_collection.json` 并导入到 Postman 中使用。
