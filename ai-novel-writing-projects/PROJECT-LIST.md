# AI小说写作项目完整清单 / Complete Project List

## 📊 快速索引

| 项目名称 | 类型 | 语言 | Stars | 更新时间 | 特色功能 |
|---------|------|------|-------|---------|---------|
| 302_novel_writing | 中文工具 | 中文 | - | 2025 | 多风格章节生成 |
| digital-humanities-novel-database | 研究 | 中文 | - | 2025-09 | AI vs 人类对比研究 |
| AIStoryWriter | LLM工具 | 英文 | ⭐ | 活跃 | 长篇小说，本地+云端 |
| NovelGenerator | LLM工具 | 英文 | ⭐ | 活跃 | Agent系统，完整小说 |
| GPTAuthor | LLM工具 | 英文 | ⭐⭐ | 活跃 | 多章节，人机协同 |
| kimi-writer | LLM工具 | 多语言 | ⭐ | 2025 | 深度推理，智能上下文 |
| Story-Forge | 互动 | 英文 | ⭐ | 活跃 | 交互式故事，玩家主导 |
| WriterAI | 助手 | 英文 | ⭐ | 活跃 | 小说作家专用助手 |
| ainovelprompter | 助手 | 英文 | ⭐ | 活跃 | 提示词工程工具 |
| aistorybooks | 教育 | 多语言 | ⭐ | 活跃 | 语言学习故事书 |

---

## 🇨🇳 中文项目详细列表

### 1. 302_novel_writing
**GitHub**: https://github.com/302ai/302_novel_writing
**描述**: 🤖 302 AI 小说写作工具
**功能特点**:
- ✅ 多种写作风格（现代、古代、玄幻、科幻、悬疑、言情）
- ✅ 手动/自动生成模式
- ✅ AI智能续写
- ✅ 章节内容生成
- ✅ 风格一致性保持

**技术栈**: AI生成、Web界面
**适用场景**: 网文作家、业余写作者
**优点**: 中文优化好，风格多样
**缺点**: 需要云服务支持

---

### 2. digital-humanities-novel-database
**GitHub**: https://github.com/VidaYixuan/digital-humanities-novel-database
**描述**: 对比AI生成和人类创作的中文仙侠/修真小说的数字人文研究项目
**研究内容**:
- 📊 包含AI生成和人类创作的仙侠小说数据
- 📊 精选元数据（标题、作者、平台、类型、摘录）
- 📊 交互式Airtable视图用于筛选、比较和可视化
- 📊 可用于学术研究和内容分析

**发布时间**: 2025-09-22
**价值**: 学术研究、质量对比、数据集资源
**适用人群**: 研究者、学者、数据科学家

---

### 3. Chinese Novel Generator (Gemini)
**描述**: 基于Gemini模型的中文长篇网络小说生成器
**更新时间**: 2025-07-28
**Star数**: 36 ⭐
**特点**:
- 专注于中文长篇小说
- 利用Gemini的长上下文能力
- 适合网文创作

**技术**: Google Gemini API
**优点**: 长文本生成能力强
**缺点**: 依赖Google服务

---

## 🌍 英文/多语言项目详细列表

### 4. AIStoryWriter
**GitHub**: https://github.com/datacrystals/AIStoryWriter
**描述**: 专注于高质量长篇输出的LLM故事写作工具
**功能特点**:
- 📖 生成完整长篇小说（中长篇到长篇）
- 📖 连贯的叙事结构
- 📖 支持本地模型（Ollama）
- 📖 支持云服务提供商（目前支持Google）
- 📖 可定制提示词和模型选择
- 📖 多种语言模型选项

**技术栈**: Python, Ollama, Google AI
**部署方式**: 本地/云端混合
**适用场景**: 长篇小说创作、隐私敏感项目
**优点**: 灵活性高，支持本地部署
**缺点**: 需要一定技术背景

---

### 5. NovelGenerator
**GitHub**: https://github.com/KazKozDev/NovelGenerator
**描述**: 使用LLM代理创建完整小说，具有连贯情节、角色发展和多样写作风格
**核心特性**:
- 🤖 基于LLM代理的自主生成系统
- 🤖 保持叙事连贯性
- 🤖 角色一致性维护
- 🤖 多样化的写作风格
- 🤖 完整的小说生成流程
- 🤖 自动化情节规划

**技术架构**: Agent-based, Multi-agent system
**亮点**: 自主性强，生成质量高
**相关文章**: [Building an AI-Powered Book Generator](https://medium.com/local-llm-lab/building-an-ai-powered-book-generator-a-journey-into-automated-storytelling-2d8f21b7046d)

---

### 6. GPTAuthor
**GitHub**: https://github.com/dylanhogg/gptauthor
**描述**: 根据故事提示词编写长篇、多章节故事的AI工具
**工作流程**:
1. ✍️ AI生成故事概要和章节摘要
2. ✍️ 人工审核概要，可选择修改
3. ✍️ 基于共同概要和前一章节，ChatGPT迭代写作各章节
4. ✍️ 人工可在任何阶段介入调整

**技术**: OpenAI GPT API
**特点**: 人机协同，可控性强
**适用**: 需要人工审核和调整的创作
**优点**: 平衡了自动化和可控性
**缺点**: 需要较多人工介入

---

### 7. kimi-writer
**GitHub**: https://github.com/Doriandarko/kimi-writer
**描述**: 由kimi-k2-thinking驱动的AI写作代理，具有深度推理能力
**核心能力**:
- 🧠 深度推理能力
- 🧠 自主创作小说和故事
- 🧠 多种格式支持（小说、书籍等）
- 🧠 智能上下文管理
- 🧠 长篇内容生成

**技术**: Kimi (Moonshot) API
**优势**: 中文友好，推理能力强
**适用**: 复杂情节，需要逻辑推理的故事
**更新**: 2025年新项目

---

### 8. Story-Forge
**GitHub**: https://github.com/SartajBhuvaji/Story-Forge
**描述**: 交互式LLM驱动的故事写作器
**互动特性**:
- 🎮 玩家成为故事主角
- 🎮 决策影响故事走向
- 🎮 实时生成分支剧情
- 🎮 动态角色互动
- 🎮 个性化故事体验

**类型**: 互动式故事游戏
**技术**: LLM + 交互式界面
**应用**: 游戏、教育、娱乐
**创新点**: 高度互动，无限可能性

---

### 9. WriterAI
**GitHub**: https://github.com/tinkvu/WriterAI
**描述**: 专为小说作家设计的AI写作助手
**辅助功能**:
- ✏️ 写作建议和灵感
- ✏️ 情节辅助和规划
- ✏️ 角色发展支持
- ✏️ 文字润色和优化
- ✏️ 创意激发

**定位**: 写作助手而非生成器
**适用**: 已有创意，需要辅助的作家
**优点**: 辅助性强，不过度干预创作

---

### 10. ainovelprompter
**GitHub**: https://github.com/danielsobrado/ainovelprompter
**描述**: 创建使用AI写小说所需的提示词工具
**核心功能**:
- 📝 提示词模板生成
- 📝 提示词优化建议
- 📝 场景描述生成
- 📝 提示词工程最佳实践
- 📝 提示词库管理

**价值**: 提升AI生成质量的关键工具
**适用**: 需要精细控制AI输出的用户
**学习曲线**: 需要了解提示词工程

---

### 11. aistorybooks
**GitHub**: https://github.com/ismailsimsek/aistorybooks
**描述**: 使用LLM代理为语言学习者生成故事书
**教育功能**:
- 📚 适配不同语言水平
- 📚 定制化学习内容
- 📚 互动式学习体验
- 📚 多语言支持
- 📚 教学导向设计

**应用场景**: 语言教学、自学、儿童教育
**特点**: 教育性 + 趣味性结合
**用户**: 教师、学生、家长

---

## 🔧 按技术栈分类

### 基于OpenAI GPT
- GPTAuthor
- WriterAI
- Story-Forge (部分)

### 基于Google Gemini
- AIStoryWriter (支持)
- Chinese Novel Generator

### 基于Kimi/Moonshot
- kimi-writer

### 支持本地部署
- AIStoryWriter (Ollama)
- NovelGenerator

### 多模型支持
- 302_novel_writing
- ainovelprompter

---

## 📊 按应用场景分类

### 🎯 长篇小说创作
1. **AIStoryWriter** - 高质量长篇
2. **NovelGenerator** - Agent系统生成
3. **GPTAuthor** - 多章节协同
4. **kimi-writer** - 深度推理

### 🎯 中文网文创作
1. **302_novel_writing** - 多风格支持
2. **Chinese Novel Generator** - Gemini驱动
3. **kimi-writer** - 中文友好

### 🎯 互动式体验
1. **Story-Forge** - 玩家主导故事

### 🎯 写作辅助
1. **WriterAI** - 全方位助手
2. **ainovelprompter** - 提示词工具

### 🎯 教育研究
1. **digital-humanities-novel-database** - 学术研究
2. **aistorybooks** - 语言学习

---

## ⚡ 快速选择指南

### 我想要...

**快速生成中文网文章节**
→ 推荐: `302_novel_writing`

**高质量英文长篇小说**
→ 推荐: `AIStoryWriter` 或 `NovelGenerator`

**人机协同创作，保持控制权**
→ 推荐: `GPTAuthor`

**本地部署，保护隐私**
→ 推荐: `AIStoryWriter` (with Ollama)

**互动式故事游戏**
→ 推荐: `Story-Forge`

**学习如何写好提示词**
→ 推荐: `ainovelprompter`

**辅助我的创作，不是替代**
→ 推荐: `WriterAI`

**研究AI生成内容质量**
→ 推荐: `digital-humanities-novel-database`

**为语言学习生成故事**
→ 推荐: `aistorybooks`

---

## 🆕 2025年新增/更新项目

- ✨ kimi-writer (2025新项目)
- ✨ 302_novel_writing (2025活跃)
- ✨ digital-humanities-novel-database (2025-09-22发布)
- ✨ Chinese Novel Generator (2025-07-28更新)

---

## 📈 Star数排名 (截至2025-11)

1. GPTAuthor - ⭐⭐⭐⭐
2. AIStoryWriter - ⭐⭐⭐
3. NovelGenerator - ⭐⭐⭐
4. Story-Forge - ⭐⭐
5. Chinese Novel Generator - ⭐ (36)

*注：实际star数请访问GitHub仓库查看*

---

## 🔗 GitHub Topics链接

- [ai-writing](https://github.com/topics/ai-writing)
- [ai-writer](https://github.com/topics/ai-writer)
- [novel-generator](https://github.com/topics/novel-generator)
- [novel-writing](https://github.com/topics/novel-writing)
- [ai-writing-assistant](https://github.com/topics/ai-writing-assistant)

---

## 📝 贡献新项目

发现新的优秀项目？欢迎补充：

1. 项目名称和GitHub链接
2. 简要描述（中英文）
3. 核心功能和特点
4. 适用场景
5. 技术栈
6. 优缺点评价

---

**最后更新**: 2025-11-20
**项目总数**: 11个核心项目
**覆盖领域**: 中文/英文/多语言，生成/辅助/研究/教育
