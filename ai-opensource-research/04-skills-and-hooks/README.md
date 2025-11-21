# Skills 和 Hooks 定义集合

## 📖 概述

Skills和Hooks是AI系统（特别是Claude Code和GitHub Copilot）的扩展机制，允许用户自定义和增强AI助手的能力。

## 🎯 Claude Code 扩展生态

### 四大组件类型

1. **Commands** (命令) - 自定义斜杠命令
2. **Agents** (代理) - 专业化AI助手
3. **Hooks** (钩子) - 事件处理器
4. **MCP** (Model Context Protocol) - 外部集成

## 🔧 Hooks (钩子)

### 什么是Hooks?

Hooks是用户定义的Shell命令，在Claude Code生命周期的各个关键点执行。它们提供对Claude Code行为的确定性控制，确保某些操作始终发生，而不是依赖LLM选择运行它们。

### 核心特点

- ✅ **确定性执行**: 保证在特定时机触发
- 🔄 **自动化工作流**: 减少重复性任务
- 🛡️ **安全控制**: 阻止敏感操作
- 📊 **日志追踪**: 记录所有操作

### Hook类型

#### 1. 文件操作Hooks
- `pre-edit`: 编辑文件前
- `post-edit`: 编辑文件后
- `pre-write`: 写入文件前
- `post-write`: 写入文件后

#### 2. 工具调用Hooks
- `pre-bash`: 执行Bash命令前
- `post-bash`: 执行Bash命令后
- `pre-read`: 读取文件前
- `post-read`: 读取文件后

#### 3. 会话Hooks
- `user-prompt-submit`: 用户提交提示后
- `session-start`: 会话开始时
- `session-end`: 会话结束时

### 常见应用场景

#### 自动格式化
```bash
# 编辑TypeScript文件后自动运行prettier
post-edit: prettier --write $file
```

#### 代码检查
```bash
# 编辑Python文件后运行linter
post-edit: pylint $file
```

#### 权限控制
```bash
# 阻止修改生产文件
pre-edit: check-production-file.sh $file
```

#### 日志记录
```bash
# 记录所有bash命令
pre-bash: log-command.sh "$command"
```

### 配置示例

```json
{
  "hooks": {
    "post-edit": {
      "*.ts": "prettier --write {{file}}",
      "*.py": "black {{file}}"
    },
    "pre-bash": {
      "*": "audit-command.sh {{command}}"
    }
  }
}
```

## 🧠 Skills (技能)

### 什么是Skills?

**发布日期**: 2025年10月16日

Skills是包含指令、脚本和资源的文件夹，Claude可以动态加载以提高专业任务的性能。它们教会Claude如何以可重复的方式完成特定任务。

### 核心特点

- 📦 **可组合**: 按需加载和组合
- 🔍 **可发现**: 自动检测和推荐
- 🎓 **专业化**: 针对特定任务优化
- 🔄 **可复用**: 跨项目共享

### Skill结构

```
.claude/skills/my-skill/
├── skill.json          # 技能元数据
├── instructions.md     # 详细指令
├── examples/           # 示例和模板
└── tools/             # 辅助脚本
```

### skill.json示例

```json
{
  "name": "my-skill",
  "version": "1.0.0",
  "description": "描述这个技能的用途",
  "triggers": ["关键词1", "关键词2"],
  "capabilities": [
    "capability1",
    "capability2"
  ]
}
```

### 实际应用

1. **数据分析Skill**: 自动化数据清洗和可视化
2. **测试生成Skill**: 基于代码自动生成单元测试
3. **文档编写Skill**: 生成API文档和使用说明
4. **代码审查Skill**: 执行代码质量检查

## 📦 Plugins (插件)

### 什么是Plugins?

插件是自定义命令、代理、MCP服务器和钩子的集合，可以通过单个命令安装。

### 插件组成

- **Slash Commands**: 自定义快捷操作
- **Subagents**: 专用开发任务的代理
- **MCP Servers**: 通过MCP连接工具和数据源
- **Hooks**: 自定义工作流行为

### 安装插件

```bash
claude plugin install <plugin-name>
```

## 🌟 优秀资源

### 1. pluginagentmarketplace/claude-plugin-ecosystem-hub
- **GitHub**: https://github.com/pluginagentmarketplace/claude-plugin-ecosystem-hub
- **描述**: Claude AI扩展的权威索引
- **内容**: 500+ 插件、Skills、MCP、命令、代理和市场
- **分类**:
  - 425+ 精选资源
  - 所有类别全覆盖

### 2. anthropics/skills
- **GitHub**: https://github.com/anthropics/skills
- **描述**: Skills官方仓库
- **维护者**: Anthropic

### 3. hesreallyhim/awesome-claude-code
- **GitHub**: https://github.com/hesreallyhim/awesome-claude-code
- **描述**: Claude Code的命令、文件和工作流精选列表

### 4. carlrannaberg/claudekit
- **GitHub**: https://github.com/carlrannaberg/claudekit
- **描述**: Claude Code的自定义命令、钩子和实用工具工具包

## 🔗 GitHub Copilot Extensions

### 简介

GitHub Copilot Extensions将全球知识引入AI开发工具，使开发者能够使用自然语言和首选工具构建和部署到云。

### 合作伙伴 (初始)

- DataStax
- Docker
- LambdaTest
- LaunchDarkly
- McKinsey & Company
- Microsoft Azure & Teams
- MongoDB
- Octopus Deploy
- Pangea
- Pinecone
- Product Science
- ReadMe
- Sentry
- Stripe

### 官方资源

- **官网**: https://github.com/features/copilot
- **博客**: https://github.blog/news-insights/product-news/introducing-github-copilot-extensions/

## 📚 学习资源

### 官方文档

1. **Claude Code Hooks Guide**: https://docs.claude.com/en/docs/claude-code/hooks-guide
2. **Hooks Reference**: https://docs.claude.com/en/docs/claude-code/hooks
3. **Claude Code Plugins**: https://www.anthropic.com/news/claude-code-plugins

### 社区资源

1. **Claude Code Cheatsheet**: https://awesomeclaude.ai/code-cheatsheet
2. **Understanding Claude Code Full Stack**: https://alexop.dev/posts/understanding-claude-code-full-stack/
3. **Claude Code Hooks Tutorial**: https://www.cometapi.com/claude-code-hooks-what-is-and-how-to-use-it/

### 深度文章

- **Ultimate Claude Code Guide**: 所有隐藏技巧和功能
- **Customizing Claude Code**: 实战经验分享
- **Claude Code Developer Cheatsheet**: 命令、配置和工作流

## 🎯 最佳实践

### Hooks设计原则

1. **保持简单**: Hooks应该快速执行
2. **幂等性**: 多次执行结果相同
3. **错误处理**: 优雅地处理失败
4. **日志记录**: 记录重要操作
5. **可配置**: 支持不同环境

### Skills开发建议

1. **明确范围**: 每个Skill专注一个领域
2. **详细文档**: 提供清晰的使用说明
3. **示例丰富**: 包含多个使用案例
4. **版本控制**: 使用语义化版本
5. **测试验证**: 确保可靠性

## 🚀 2025年趋势

1. **标准化**: MCP成为事实标准
2. **市场化**: 插件市场生态繁荣
3. **企业采用**: 更多企业定制Skills
4. **AI Agent化**: Agents作为Skills载体
5. **跨平台**: Claude、Copilot等平台互通

## 📝 格式规范

### MCP Bundle (.mcpb)

2025年9月起，Desktop Extensions使用.mcpb格式:
- 统一的打包格式
- 包含所有依赖
- 简化安装流程

## 🌐 生态系统

### 市场平台

- **Claude Code Plugin Directory**: https://www.claudecodeplugin.com/
- **GitHub Copilot Marketplace**
- **Community Repositories**

### 统计数据

- 500+ Claude插件和扩展
- 425+ 精选资源
- 持续增长的开发者社区

---

*最后更新: 2025-11-20*
