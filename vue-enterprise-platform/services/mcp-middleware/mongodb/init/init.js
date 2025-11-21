// 切换到vue_enterprise数据库
db = db.getSiblingDB('vue_enterprise');

// 创建用户集合并插入数据
db.users.insertMany([
  {
    name: '张三',
    email: 'zhang@example.com',
    age: 25,
    profile: {
      bio: '热爱编程的开发者',
      location: '北京',
      website: 'https://zhang.example.com'
    },
    tags: ['vue', 'javascript', 'typescript'],
    createdAt: new Date(),
    updatedAt: new Date()
  },
  {
    name: '李四',
    email: 'li@example.com',
    age: 30,
    profile: {
      bio: '全栈工程师',
      location: '上海',
      website: 'https://li.example.com'
    },
    tags: ['react', 'node.js', 'mongodb'],
    createdAt: new Date(),
    updatedAt: new Date()
  },
  {
    name: '王五',
    email: 'wang@example.com',
    age: 28,
    profile: {
      bio: '前端架构师',
      location: '深圳',
      website: 'https://wang.example.com'
    },
    tags: ['angular', 'rxjs', 'webpack'],
    createdAt: new Date(),
    updatedAt: new Date()
  }
]);

// 创建索引
db.users.createIndex({ email: 1 }, { unique: true });
db.users.createIndex({ tags: 1 });

// 创建文章集合
db.articles.insertMany([
  {
    title: 'Vue 3 组合式API完全指南',
    content: '深入探讨Vue 3组合式API的使用方法和最佳实践...',
    author: 'zhang@example.com',
    tags: ['vue3', 'composition-api'],
    views: 1024,
    likes: 88,
    createdAt: new Date(),
    updatedAt: new Date()
  },
  {
    title: 'TypeScript高级类型详解',
    content: '详细介绍TypeScript中的高级类型系统...',
    author: 'li@example.com',
    tags: ['typescript', 'types'],
    views: 856,
    likes: 66,
    createdAt: new Date(),
    updatedAt: new Date()
  }
]);

db.articles.createIndex({ author: 1 });
db.articles.createIndex({ tags: 1 });

print('MongoDB初始化完成！');
