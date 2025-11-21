# Model Context Protocol (MCP) 服务器集合

## 📖 MCP 简介

Model Context Protocol (MCP) 是由Anthropic于2024年11月推出的开源标准，用于标准化AI系统（如大语言模型）与外部工具、系统和数据源的集成方式。

### 核心特点
- 🔓 **开源标准**: 由Anthropic主导的开放协议
- 🔌 **标准化集成**: 统一的数据共享和工具调用接口
- 🔒 **安全可控**: 提供对工具和数据的安全访问控制
- 🌐 **广泛采用**: OpenAI、Microsoft等主要厂商已支持

## 🏢 行业采用情况

### Anthropic
- Claude Desktop
- Claude Code
- Claude API

### OpenAI (2025年3月)
- ChatGPT Desktop App
- Agents SDK
- Responses API

### Microsoft
- Copilot Studio
- VS Code GitHub Copilot Agent Mode
- Semantic Kernel

## 🌟 官方MCP服务器

### 核心仓库
- **主仓库**: https://github.com/modelcontextprotocol
- **服务器集合**: https://github.com/modelcontextprotocol/servers

### 预构建的企业级MCP服务器

#### 1. Google Drive MCP Server
- 访问和管理Google Drive文件
- 搜索文档
- 协作功能

#### 2. Slack MCP Server
- 消息发送和接收
- 频道管理
- 用户交互

#### 3. GitHub MCP Server
- **2025年最新**: GitHub官方重写（Go语言）
- 100%旧功能保留
- 新增功能:
  - 自定义工具描述
  - 代码扫描支持
  - get_me函数

**链接**: https://github.com/github/github-mcp-server

#### 4. Git MCP Server
- 仓库操作
- 分支管理
- 提交历史

#### 5. Postgres MCP Server
- 数据库查询
- 数据操作
- 模式管理

#### 6. Puppeteer MCP Server
- 网页自动化
- 数据抓取
- 浏览器控制

## 🔧 社区MCP服务器

### 1. madhukarkumar/anthropic-mcp-servers
- **链接**: https://github.com/madhukarkumar/anthropic-mcp-servers
- MCP参考实现

### 2. AxiMinds/Anthropic-mcp-servers
- **链接**: https://github.com/AxiMinds/Anthropic-mcp-servers
- 社区维护的MCP服务器集合

## 📚 MCP SDK

### 官方SDK

#### TypeScript SDK
- 默认实现语言
- 完整的功能支持

#### Python SDK
- Python生态集成
- 数据科学友好

#### C# SDK (Microsoft)
- **2025年**: Microsoft与Anthropic合作开发
- .NET生态支持
- 企业级功能

### SDK特点
- 服务器和客户端实现
- 工具和资源定义
- 提示模板
- 采样支持

## 🚀 MCP应用场景

### 1. 开发工具集成
- IDE插件
- 代码审查
- 自动化测试

### 2. 企业系统连接
- CRM系统
- 项目管理
- 文档管理

### 3. 数据源访问
- 数据库
- API服务
- 文件系统

### 4. 自动化工作流
- CI/CD集成
- 部署管道
- 监控告警

## 📖 技术架构

### MCP组件

```
┌─────────────┐
│  AI Client  │ (Claude, ChatGPT, etc.)
└──────┬──────┘
       │ MCP Protocol
┌──────┴──────┐
│ MCP Server  │
└──────┬──────┘
       │
┌──────┴──────────┐
│  Data Sources   │ (GitHub, DB, Files, etc.)
└─────────────────┘
```

### 核心概念

#### Resources (资源)
- 文件内容
- 数据库记录
- API响应

#### Tools (工具)
- 函数调用
- 操作执行
- 服务调用

#### Prompts (提示)
- 模板化提示
- 上下文注入
- 动态生成

#### Sampling (采样)
- LLM调用
- 响应生成

## 🛠️ 开发指南

### 创建自定义MCP服务器

```typescript
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';

const server = new Server({
  name: 'my-mcp-server',
  version: '1.0.0',
}, {
  capabilities: {
    resources: {},
    tools: {},
  }
});

// 定义工具
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: 'my-tool',
      description: 'My custom tool',
      inputSchema: { /* ... */ }
    }
  ]
}));

// 启动服务器
const transport = new StdioServerTransport();
await server.connect(transport);
```

### 安装MCP服务器

在Claude Desktop配置文件中添加:

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "your-token"
      }
    }
  }
}
```

## 📋 开发路线图

查看官方路线图: https://modelcontextprotocol.io/development/roadmap

### 近期计划
- 更多语言SDK
- 性能优化
- 增强的安全功能
- 更多预构建服务器

## 🔗 重要链接

- **官方网站**: https://modelcontextprotocol.io
- **GitHub组织**: https://github.com/modelcontextprotocol
- **文档**: https://modelcontextprotocol.io/docs
- **Anthropic公告**: https://www.anthropic.com/news/model-context-protocol
- **维基百科**: https://en.wikipedia.org/wiki/Model_Context_Protocol

## 💡 最佳实践

1. **安全第一**: 始终验证和清理输入
2. **错误处理**: 实现完善的错误处理机制
3. **日志记录**: 记录所有操作用于调试
4. **版本管理**: 使用语义化版本控制
5. **文档完善**: 提供清晰的使用说明

## 🌍 生态系统

MCP正在成为AI工具集成的事实标准:
- 数百个应用程序已运行MCP
- Stability AI开源代码库
- 快速增长的社区
- 企业级采用加速

---

*最后更新: 2025-11-20*
