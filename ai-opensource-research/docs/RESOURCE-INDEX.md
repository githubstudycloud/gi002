# AI开源项目资源索引

*快速查找和访问所有收集的AI开源项目*

## 📑 目录

- [提示词工程](#提示词工程)
- [Agent框架](#agent框架)
- [MCP服务器](#mcp服务器)
- [Skills和Hooks](#skills和hooks)
- [视频AI](#视频ai)
- [音频AI](#音频ai)
- [图片AI](#图片ai)
- [文本AI](#文本ai)

---

## 提示词工程

### 顶级项目

| 项目 | Stars | 链接 | 描述 |
|------|-------|------|------|
| Prompt-Engineering-Guide | 300万+ | [GitHub](https://github.com/dair-ai/Prompt-Engineering-Guide) | 最全面的提示词工程指南 |
| Prompt_Engineering | 20k+ | [GitHub](https://github.com/NirDiamant/Prompt_Engineering) | 实用教程和案例 |
| awesome-ai-system-prompts | 23k+ | [GitHub](https://github.com/dontriskit/awesome-ai-system-prompts) | 系统提示词集合 |
| Awesome-Prompt-Engineering | - | [GitHub](https://github.com/promptslab/Awesome-Prompt-Engineering) | GPT/ChatGPT提示词 |
| awesome-claude-prompts | - | [GitHub](https://github.com/langgptai/awesome-claude-prompts) | Claude提示词精选 |

### 关键技术
- Few-shot Learning
- Chain-of-Thought (CoT)
- Tree-of-Thought (ToT)
- ReAct框架

---

## Agent框架

### 主流框架对比

| 框架 | 市场份额 | GitHub | 最佳用途 |
|------|----------|--------|----------|
| LangChain | 30% | [链接](https://github.com/langchain-ai/langchain) | 通用LLM应用 |
| AutoGPT | 25% | [链接](https://github.com/Significant-Gravitas/AutoGPT) | 自主任务 |
| CrewAI | 20% | [链接](https://github.com/joaomdmoura/crewAI) | 多Agent协作 |
| AutoGen | - | [链接](https://github.com/microsoft/autogen) | 对话式Agent |
| LangGraph | - | [链接](https://github.com/langchain-ai/langgraph) | 状态工作流 |

### 其他框架
- SuperAGI
- BabyAGI
- AgentGPT
- Semantic Kernel
- Haystack

---

## MCP服务器

### 官方资源

| 资源 | 链接 | 说明 |
|------|------|------|
| MCP官网 | https://modelcontextprotocol.io | 协议文档 |
| MCP GitHub组织 | https://github.com/modelcontextprotocol | 官方仓库 |
| MCP服务器集合 | https://github.com/modelcontextprotocol/servers | 参考实现 |
| GitHub MCP Server | https://github.com/github/github-mcp-server | GitHub官方 |

### 预构建服务器

1. **Google Drive** - 文件管理
2. **Slack** - 消息集成
3. **GitHub** - 代码仓库
4. **Git** - 版本控制
5. **Postgres** - 数据库
6. **Puppeteer** - 浏览器自动化

### SDK支持

- TypeScript SDK
- Python SDK
- C# SDK (Microsoft)

### 采用情况

| 平台 | 支持时间 | 产品 |
|------|----------|------|
| Anthropic | 2024年11月 | Claude Desktop, Claude Code |
| OpenAI | 2025年3月 | ChatGPT, Agents SDK |
| Microsoft | 2025年 | Copilot Studio, VS Code |
| Google | 2025年4月 | Gemini |

---

## Skills和Hooks

### Claude Code生态

#### 四大组件
1. **Commands** - 斜杠命令
2. **Agents** - 专业助手
3. **Hooks** - 事件处理
4. **MCP** - 外部集成

### GitHub资源

| 项目 | Stars | 链接 | 描述 |
|------|-------|------|------|
| claude-plugin-ecosystem-hub | - | [GitHub](https://github.com/pluginagentmarketplace/claude-plugin-ecosystem-hub) | 500+ Claude扩展索引 |
| skills | - | [GitHub](https://github.com/anthropics/skills) | 官方Skills仓库 |
| awesome-claude-code | - | [GitHub](https://github.com/hesreallyhim/awesome-claude-code) | 命令和工作流集合 |
| claudekit | - | [GitHub](https://github.com/carlrannaberg/claudekit) | 自定义工具包 |

### Hooks类型
- `pre-edit` / `post-edit`
- `pre-write` / `post-write`
- `pre-bash` / `post-bash`
- `user-prompt-submit`

### GitHub Copilot扩展

**合作伙伴**: DataStax, Docker, MongoDB, Stripe等

---

## 视频AI

### 开源项目

| 项目 | 版本 | GitHub | 特点 |
|------|------|--------|------|
| Open-Sora | v1.3 | [链接](https://github.com/hpcaitech/Open-Sora) | 2-15s, 144p-720p |
| FastVideo | 2025 | [链接](https://github.com/hao-ai-lab/FastVideo) | 加速推理框架 |
| CogVideoX | - | - | Transformer架构 |

### 核心技术
- GANs (生成对抗网络)
- Transformers
- Diffusion Models

### 功能类型
- Text-to-Video
- Image-to-Video
- Video-to-Video
- 无限时长生成

---

## 音频AI

### 综合工具包

| 项目 | GitHub | 特点 |
|------|--------|------|
| Amphion | [链接](https://github.com/open-mmlab/Amphion) | 全功能音频工具包 |
| Higgs Audio V2 | [链接](https://github.com/boson-ai/higgs-audio) | 多模态音频生成 |

### TTS模型

| 模型 | 类型 | 特点 |
|------|------|------|
| MaskGCT | 非自回归 | SOTA零样本TTS |
| VALL-E X | 零样本 | Microsoft开源 |
| GPT-SoVITS | GPT架构 | 少样本学习 |
| CosyVoice | 情感TTS | 高保真 |
| XTTSv2 | 跨语言 | 多语言支持 |

### 音乐生成
- MusicGen (Meta)
- AudioLDM
- Stable Audio
- AudioGen

### 音频处理
- Demucs (音源分离)
- RVC (实时语音克隆)
- SeamlessM4T (翻译)

---

## 图片AI

### 三大平台对比

| 平台 | 优势 | 定价 | 开源 |
|------|------|------|------|
| Midjourney | 艺术质量 | $10/月 | ❌ |
| DALL-E 3 | 提示精准 | $20/月 | ❌ |
| Stable Diffusion | 完全控制 | 免费 | ✅ |

### 开源生态

#### 核心项目
- **AUTOMATIC1111/stable-diffusion-webui** - 最流行WebUI
- **ComfyUI** - 节点工作流
- **InvokeAI** - 专业界面

#### 控制技术
- **ControlNet** - 精确控制
- **LoRA** - 轻量微调
- **IP-Adapter** - 风格迁移

#### 资源库
- **awesome-ai-art-image-synthesis** - 工具集合
- **Civitai** - 模型社区
- **Hugging Face** - 模型托管

### 技术栈
- Latent Diffusion
- DreamBooth
- Textual Inversion
- ControlNet

---

## 文本AI

### 四大LLM (2025)

| 模型 | 开发者 | Context | 特点 |
|------|--------|---------|------|
| Claude 3.5 | Anthropic | 200K | 推理强 |
| GPT-4 | OpenAI | 128K | 生态丰富 |
| Gemini 1.5 | Google | 1M | 超长上下文 |
| LLaMA 3 | Meta | 可变 | 开源 |

### 应用框架

#### LangChain生态
- **LangChain** - 核心框架
- **LangSmith** - 调试监控
- **LangServe** - 部署服务
- **LangGraph** - 复杂工作流

#### 其他框架
- **AI SDK** (Vercel) - TypeScript
- **Haystack** - NLP搜索
- **Semantic Kernel** (Microsoft)

### 开发工具

| 工具 | 用途 | 链接 |
|------|------|------|
| Repomix | 代码打包 | - |
| Claude Code | 代码生成 | - |
| Ollama | 本地部署 | - |
| LM Studio | GUI管理 | - |

### 重大发布

**OpenAI开源模型** (2025年8月5日):
- gpt-oss-120b (1200亿参数)
- gpt-oss-20b (200亿参数)

---

## 🔍 快速查找

### 按用途查找

#### 内容创作
- 提示词: Prompt-Engineering-Guide
- 图片: Stable Diffusion, Midjourney
- 视频: Open-Sora
- 音频: Amphion, MusicGen
- 文本: LangChain, Claude

#### 开发工具
- Agent框架: LangChain, CrewAI
- MCP: 官方服务器集合
- Hooks: claudekit
- 代码生成: Claude Code

#### 企业应用
- 文档处理: LangChain + RAG
- 数据集成: MCP服务器
- 自动化: AutoGen, AutoGPT
- 客服: TTS + LLM

#### 研究学习
- 教程: dair-ai系列
- 模型: Hugging Face
- 数据集: 各领域开源数据集
- 论文: CVPR, arXiv

### 按技术栈查找

#### Python
- LangChain
- Transformers
- Diffusers
- Amphion

#### TypeScript/JavaScript
- AI SDK
- LangChain.js
- Vercel AI

#### 多语言
- MCP SDK (TS/Python/C#)
- Semantic Kernel
- Haystack

---

## 📊 统计数据

### 项目规模
- **提示词**: 5个顶级项目
- **Agent**: 10个主流框架
- **MCP**: 6个预构建服务器
- **Skills**: 500+ 扩展
- **视频**: 3个主要项目
- **音频**: 20+ TTS模型
- **图片**: 3大平台
- **文本**: 4大LLM

### 社区活跃度
- **GitHub Stars**: 累计100万+
- **用户数**: 5000万+ (图片AI)
- **学习者**: 300万+ (提示词工程)

---

## 🔗 重要链接

### 官方文档
- [MCP官网](https://modelcontextprotocol.io)
- [LangChain文档](https://docs.langchain.com)
- [Hugging Face](https://huggingface.co)
- [Anthropic文档](https://docs.anthropic.com)

### 社区资源
- [Civitai](https://civitai.com) - SD模型
- [Awesome Lists](https://github.com/topics/awesome)
- [Papers with Code](https://paperswithcode.com)

### 学习平台
- DeepLearning.AI
- Fast.ai
- Hugging Face Course
- Stanford CS224N

---

*最后更新: 2025-11-20*
*总项目数: 100+*
