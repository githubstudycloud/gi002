# LLM基础小说生成工具 / LLM-Based Novel Generation Tools

## 🤖 核心项目

### 1. AIStoryWriter
- **GitHub**: https://github.com/datacrystals/AIStoryWriter
- **特点**:
  - 专注高质量长篇输出
  - 支持完整长篇小说生成
  - 本地+云端双模式
- **支持模型**:
  - Ollama本地模型
  - Google Gemini
  - 可定制其他模型

### 2. NovelGenerator
- **GitHub**: https://github.com/KazKozDev/NovelGenerator
- **特点**:
  - 使用LLM代理系统
  - 完整小说自动生成
  - 连贯情节和角色发展
  - 多样化写作风格
- **技术架构**:
  - Agent-based设计
  - 上下文管理系统
  - 角色一致性维护

### 3. GPTAuthor
- **GitHub**: https://github.com/dylanhogg/gptauthor
- **特点**:
  - 长篇多章节故事
  - 人机协同创作
  - 概要审核机制
- **工作流程**:
  1. AI生成故事概要
  2. 生成章节摘要
  3. 人工审核修改
  4. 逐章迭代写作

### 4. kimi-writer
- **GitHub**: https://github.com/Doriandarko/kimi-writer
- **特点**:
  - 基于kimi-k2-thinking
  - 深度推理能力
  - 自主创作小说
  - 智能上下文管理
- **支持格式**:
  - 小说
  - 书籍
  - 多种文学形式

## 🔧 技术对比

### 模型选择

| 模型类型 | 优势 | 劣势 | 适用场景 |
|---------|------|------|---------|
| GPT-4 | 质量高，理解力强 | 成本高，速度慢 | 高质量短篇 |
| GPT-3.5 | 平衡性好，速度快 | 长文本连贯性一般 | 日常创作 |
| Gemini Pro | 长上下文，多模态 | API限制 | 长篇小说 |
| Llama 2/3 | 可本地部署，免费 | 需要GPU资源 | 隐私要求高 |
| Claude | 长文本理解好 | API访问限制 | 复杂情节 |

### 部署方式

#### 云端部署
**优点**:
- 无需本地算力
- 模型质量高
- 快速启动

**缺点**:
- API费用
- 网络依赖
- 隐私考虑

#### 本地部署
**优点**:
- 完全私密
- 无API费用
- 可定制化

**缺点**:
- 需要GPU
- 模型质量受限
- 技术门槛高

## 📊 生成质量因素

### 1. 上下文管理
- 长期记忆机制
- 角色设定维护
- 情节一致性检查

### 2. 提示词工程
- 详细的角色描述
- 清晰的情节大纲
- 风格和语气指导

### 3. 迭代优化
- 多轮生成
- 人工审核
- 渐进式改进

### 4. 结构化输出
- JSON schema约束
- 章节格式统一
- 元数据管理

## 🚀 最佳实践

### 初始化设置
```python
# 示例：使用Ollama本地模型
import ollama

# 准备角色和设定
characters = {
    "protagonist": "张三，25岁，程序员",
    "setting": "现代都市，科技公司"
}

# 生成章节
response = ollama.generate(
    model='llama2',
    prompt=f"根据以下设定写一章小说：{characters}"
)
```

### 章节生成流程
1. **准备阶段**
   - 定义世界观
   - 设计主要角色
   - 规划情节大纲

2. **生成阶段**
   - 逐章生成
   - 保持上下文连贯
   - 记录关键情节点

3. **优化阶段**
   - 人工审核
   - 润色修改
   - 一致性检查

## 🎯 项目选择指南

- **快速原型**: GPTAuthor (快速启动，人机协同)
- **高质量输出**: NovelGenerator (agent系统，质量保证)
- **隐私优先**: AIStoryWriter + Ollama (本地部署)
- **中文创作**: kimi-writer (kimi模型，中文友好)
- **长篇小说**: 使用支持长上下文的模型 (Gemini, Claude)

## 📚 相关资源

- [LangChain文档](https://python.langchain.com/)
- [Ollama模型库](https://ollama.ai/library)
- [Prompt工程指南](https://www.promptingguide.ai/)

## 🔄 持续更新

本列表持续更新中，欢迎贡献新的工具和使用经验。
