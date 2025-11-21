# 多媒体AI应用集合

## 📖 概述

本目录收集GitHub上流行的AI多媒体处理项目，涵盖视频、音频、图片和文本生成领域。

## 📂 分类导航

- [视频处理 (Video Processing)](./video-processing/)
- [音频处理 (Audio Processing)](./audio-processing/)
- [图片处理 (Image Processing)](./image-processing/)
- [文本生成 (Text Generation)](./text-generation/)

## 🎬 视频AI应用

### 顶级项目

#### 1. Open-Sora
- **GitHub**: https://github.com/hpcaitech/Open-Sora
- **版本**: v1.3 (1B) - 2025年2月发布
- **特点**:
  - 升级的VAE和Transformer架构
  - 支持2s-15s时长
  - 144p到720p分辨率
  - 任意宽高比
  - 完整视频处理管道

**功能**:
- Text-to-Video (文本生成视频)
- Text-to-Image (文本生成图片)
- Image-to-Video (图片生成视频)
- Video-to-Video (视频转换)
- 无限时长生成

#### 2. FastVideo
- **GitHub**: https://github.com/hao-ai-lab/FastVideo
- **发布**: 2025年8月
- **描述**: 统一的后训练和推理框架，用于加速视频生成

**特点**:
- 端到端统一管道
- 数据预处理到模型训练
- 微调和蒸馏
- FastWan模型
- Sparse-Distillation技术

#### 3. CogVideoX
- **技术**: Transformer架构
- **特点**:
  - 大规模语言和视觉模型
  - 高质量视频创作
  - 无缝输入混合

### 核心技术

#### GANs (生成对抗网络)
- 训练生成器和判别器
- 制作逼真的视频帧
- 简单架构，易于访问

#### Transformers
- 高质量视频创建
- 大规模模型
- 混合输入能力

### 研究进展

- CVPR 2025论文已更新
- 专业领域:
  - Text-to-Video
  - Image-to-Video
  - 个性化视频生成
  - 视频编辑

## 🎵 音频AI应用

### 综合工具包

#### 1. Amphion
- **GitHub**: https://github.com/open-mmlab/Amphion
- **描述**: 音频、音乐和语音生成工具包
- **目标**: 支持可复现研究，帮助研究人员入门

**2025年更新**:

##### Metis
- 统一语音生成基础模型
- 零样本TTS
- 语音转换
- 目标说话人提取
- 语音增强
- 唇语到语音

##### Vevo1.5
- 语音和歌声统一可控生成
- 应用: VC, TTS, AC, SVS, SVC
- 语音/歌声编辑
- 歌唱风格转换

##### Emilia-Large数据集
- 超过200,000小时数据

#### 2. Higgs Audio V2 (Boson AI)
- **GitHub**: https://github.com/boson-ai/higgs-audio
- **发布**: 2025

**功能**:
- 多语言自然对话生成
- 多说话人对话
- 叙述时自动韵律适配
- 克隆声音的旋律哼唱
- 同时生成语音和背景音乐

### TTS (文本转语音)

#### MaskGCT
- 完全非自回归TTS模型
- 在Emilia数据集上训练
- 达到SOTA零样本TTS性能

#### VALL-E X
- Microsoft零样本TTS模型的开源实现
- 高质量语音克隆

### 音乐生成

#### AudioLDM
- 文本到音频生成

#### MusicGen
- AI音乐生成

### 多模态Web UI

**Gradio + React WebUI**支持的扩展:
- ACE-Step
- Kimi Audio
- Piper TTS
- GPT-SoVITS
- CosyVoice
- XTTSv2
- DIA, Kokoro
- OpenVoice
- ParlerTTS
- Stable Audio
- MMS
- StyleTTS2
- MAGNet
- AudioGen
- Tortoise
- RVC (Real-time Voice Cloning)
- Vocos
- Demucs
- SeamlessM4T
- Bark

## 🎨 图片AI应用

### 三大主流平台 (2025)

全球超过5000万创作者使用这三大平台。

#### 1. Midjourney
**优势**: 艺术影响力
- 概念艺术
- 奇幻风景
- 风格化肖像
- 情感共鸣

**特点**:
- AI图像质量的黄金标准
- 照片级写实
- "电影级"画面
- 2025年质量和真实感领先

**定价**:
- 月订阅: $10/用户 (200张)
- 年度计划: $8/月

**法律动态**:
- 2025年6月11日: Universal和Disney提起版权侵权诉讼

#### 2. DALL-E 3
**优势**: 提示词准确性
- 产品可视化
- 精准场景组合
- 可靠商业内容

**特点**:
- 文本渲染能力
- 营销材料默认选择
- 广告和品牌内容

**定价**:
- ChatGPT免费: 每日3张图片
- ChatGPT Plus: $20/月 (更高限额)

#### 3. Stable Diffusion
**优势**: 专业控制
- 定制能力
- 角色一致性
- 品牌特定美学

**版本**: 3.5 (2025)
- 25亿参数
- 最强大的开源选项

**生态**:
- 数百个网站和应用
- Stability AI开源代码库
- 广泛的社区支持

### GitHub资源

#### altryne/awesome-ai-art-image-synthesis
- **链接**: https://github.com/altryne/awesome-ai-art-image-synthesis
- **内容**:
  - 提示工程工具
  - Colab notebooks
  - 模型集合
  - 辅助工具
- **覆盖**: DALL-E 2, Midjourney, Stable Diffusion

### 应用场景对比

| 平台 | 最佳用途 | 优势 | 价格模式 |
|------|----------|------|----------|
| Midjourney | 艺术创作 | 质量最高 | 订阅制 |
| DALL-E 3 | 商业设计 | 精准度高 | 按量/订阅 |
| Stable Diffusion | 定制开发 | 完全开源 | 免费 |

## 📝 文本AI应用

### LLM框架

#### 1. LangChain
- **GitHub**: https://github.com/langchain-ai/langchain
- **创建者**: Harrison Chase (2022年末)
- **地位**: LLM应用构建的事实标准

**特点**:
- 模块化架构
- 提示模板抽象
- 文档检索
- 工具调用
- Agent执行

#### 2. AI SDK (TypeScript)
- **创建者**: Next.js团队
- **描述**: 免费开源AI应用和Agent构建库

#### 3. Repomix
- **功能**: 将整个代码仓库打包成单个AI友好文件
- **支持**: Claude, ChatGPT, DeepSeek, Perplexity, Gemini等

### Claude AI项目

#### GUI应用和工具包
- **Stars**: 18.7k
- **功能**:
  - 创建自定义Agents
  - 管理交互式Claude Code会话
  - 运行安全后台Agents

#### 生产级Subagents集合
- **数量**: 100+ 专业AI Agents
- **领域**:
  - 全栈开发
  - DevOps
  - 数据科学
  - 业务运营

### 重大发布

#### OpenAI开源模型 (2025年8月5日)
- **gpt-oss-120b**: 1200亿参数
- **gpt-oss-20b**: 200亿参数
- **意义**: OpenAI自GPT-2以来首次开源语言模型

### 本地/自托管方案

- 免费开源替代OpenAI和Claude
- 自托管和本地优先
- 消费级硬件运行
- 无需GPU

**支持架构**:
- GGUF
- Transformers
- Diffusers

### 2025顶级LLM

#### 四大主流模型
1. **Claude** (Anthropic)
2. **Gemini** (Google)
3. **GPT-4** (OpenAI)
4. **LLaMA** (Meta)

### 应用工具

#### 代码辅助
- 最佳编码LLM (2025)
- 13+ 顶级模型
- 开发者专用优化

## 🔗 相关资源

### GitHub Topics
- `ai-video-generation`
- `text-to-audio`
- `text-to-speech`
- `music-generation`
- `image-generation`
- `text-generation`

### 学习资源
- CVPR 2025论文集
- 各平台官方文档
- 社区教程和指南

## 📊 技术栈总结

### 视频生成技术栈
- GANs
- Transformers
- Diffusion Models
- VAE (变分自编码器)

### 音频生成技术栈
- TTS引擎
- 语音克隆
- 音乐生成模型
- 多模态融合

### 图片生成技术栈
- Stable Diffusion
- DALL-E系列
- Midjourney API
- LoRA微调

### 文本生成技术栈
- LLM基础模型
- RAG架构
- Agent框架
- 向量数据库

---

*最后更新: 2025-11-20*
