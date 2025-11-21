# 研究资源 / Research Resources

## 📚 学术研究

### 数字人文项目

#### digital-humanities-novel-database
- **GitHub**: https://github.com/VidaYixuan/digital-humanities-novel-database
- **研究方向**: AI生成 vs 人类创作的中文仙侠小说对比
- **研究价值**:
  - 量化分析AI生成内容质量
  - 对比叙事结构差异
  - 评估读者接受度
  - 探索AI辅助创作的可行性
- **数据集包含**:
  - 小说标题和作者
  - 发布平台信息
  - 类型标签
  - 文本摘录
  - 交互式Airtable视图

### 研究主题

#### 1. AI生成内容质量评估
**研究问题**:
- 如何量化评估AI生成小说的质量？
- AI生成内容与人类创作的差异在哪里？
- 读者能否区分AI生成和人类创作？

**评估维度**:
- 情节连贯性
- 角色一致性
- 语言流畅度
- 创意新颖度
- 情感共鸣度

#### 2. 大语言模型在创意写作中的应用
**研究方向**:
- 不同模型在创意写作任务的表现
- 提示词工程对生成质量的影响
- 上下文长度对长篇创作的影响
- Fine-tuning在风格学习中的作用

#### 3. 人机协同创作
**研究焦点**:
- 最佳协作模式探索
- 创作效率提升研究
- 创意保留与AI辅助的平衡
- 作者接受度和使用体验

#### 4. 叙事学与AI
**研究内容**:
- AI生成的叙事结构分析
- 情节模式识别与生成
- 角色弧线的AI建模
- 文学理论在AI中的应用

## 📊 数据集资源

### 现有数据集

#### 1. 小说文本数据
- **书籍语料库**: Project Gutenberg, 中文小说库
- **网文数据**: 起点中文网公开数据, 晋江文学城
- **多语言**: CommonCrawl, Wikipedia

#### 2. 标注数据
- 情节标注
- 角色关系图谱
- 情感标注
- 写作风格分类

#### 3. 评估数据
- 人类评分数据
- AB测试结果
- 读者反馈
- 专家评审

### 数据集构建指南

#### 数据收集
```python
# 示例：小说文本爬取框架
class NovelCrawler:
    def __init__(self, source):
        self.source = source

    def fetch_metadata(self):
        # 获取元数据
        pass

    def fetch_chapters(self):
        # 获取章节内容
        pass

    def clean_text(self):
        # 文本清洗
        pass
```

#### 数据标注
- 人工标注指南
- 标注质量控制
- 跨标注者一致性
- 众包标注平台

## 📖 研究论文

### 关键论文方向

#### 自然语言生成
- GPT系列论文
- Transformer架构
- Long-context modeling
- Controllable generation

#### 创意AI
- Computational creativity
- AI-assisted authoring
- Story generation
- Character modeling

#### 评估方法
- Automatic evaluation metrics
- Human evaluation protocols
- Perplexity vs quality
- BLEU, ROUGE for creative text

### 会议和期刊

#### 顶会
- ACL (计算语言学)
- EMNLP (自然语言处理)
- NAACL (北美计算语言学)
- AAAI (人工智能)
- NeurIPS (机器学习)

#### 相关期刊
- Computational Linguistics
- Natural Language Engineering
- Digital Humanities Quarterly
- Literary and Linguistic Computing

## 🔬 实验设计

### 研究方法

#### 1. 对比实验
**设计**:
- 控制组：人类创作
- 实验组：AI生成
- 混合组：人机协同

**评估方法**:
- 盲测评分
- 问卷调查
- 阅读时长
- 完成度统计

#### 2. 消融研究
**变量**:
- 模型大小
- 提示词策略
- 上下文长度
- 温度参数

**测量指标**:
- 生成质量
- 多样性
- 连贯性
- 计算成本

#### 3. 用户研究
**方法**:
- 深度访谈
- 使用日志分析
- A/B测试
- 长期跟踪

**关注点**:
- 用户接受度
- 使用模式
- 痛点问题
- 改进建议

### 评估指标

#### 自动化指标
```python
# 常用评估指标
metrics = {
    "Perplexity": "语言模型困惑度",
    "BLEU": "与参考文本相似度",
    "ROUGE": "摘要质量",
    "BERTScore": "语义相似度",
    "Distinct-n": "文本多样性",
    "Self-BLEU": "输出多样性"
}
```

#### 人工评估标准
- **流畅度** (1-5分): 语言是否自然流畅
- **连贯性** (1-5分): 情节是否逻辑连贯
- **创意性** (1-5分): 内容是否新颖有趣
- **情感** (1-5分): 是否引发情感共鸣
- **整体质量** (1-5分): 综合评价

## 🛠️ 研究工具

### 文本分析工具

#### 基础分析
- **NLTK**: Python自然语言工具包
- **spaCy**: 工业级NLP库
- **jieba**: 中文分词
- **HanLP**: 中文NLP

#### 高级分析
- **Stanza**: 斯坦福NLP
- **AllenNLP**: 深度学习NLP
- **Hugging Face**: Transformers库
- **TextBlob**: 情感分析

### 可视化工具
- **Voyant Tools**: 文本分析可视化
- **RAWGraphs**: 数据可视化
- **D3.js**: 交互式可视化
- **Tableau**: 商业智能可视化

### 标注工具
- **Label Studio**: 多功能标注平台
- **Prodigy**: 高效标注工具
- **Doccano**: 开源文本标注
- **INCEpTION**: 语义标注平台

## 📈 实验数据管理

### 版本控制
```bash
# 使用DVC进行数据版本控制
dvc init
dvc add data/novels.csv
git add data/novels.csv.dvc
git commit -m "Add novel dataset"
```

### 实验追踪
```python
# 使用MLflow追踪实验
import mlflow

with mlflow.start_run():
    mlflow.log_param("model", "gpt-4")
    mlflow.log_param("temperature", 0.7)
    mlflow.log_metric("quality_score", 4.2)
```

## 🎓 教育资源

### 在线课程
- **Coursera**: NLP Specialization
- **fast.ai**: Practical Deep Learning
- **DeepLearning.AI**: ChatGPT Prompt Engineering
- **Hugging Face**: NLP Course

### 书籍推荐
- *Speech and Language Processing* - Jurafsky & Martin
- *Natural Language Processing with Python* - Bird, Klein & Loper
- *Deep Learning for NLP* - Palash Goyal
- *The Creativity Code* - Marcus du Sautoy (AI与创意)

### 博客和教程
- Jay Alammar's Blog (可视化解释)
- Hugging Face Blog
- OpenAI Blog
- Anthropic Research Blog

## 🤝 研究社区

### 学术社区
- **ACL Portal**: 计算语言学门户
- **arXiv.org**: 预印本论文
- **Papers with Code**: 论文+代码
- **Semantic Scholar**: AI文献搜索

### 开发者社区
- **GitHub**: 开源项目
- **Hugging Face**: 模型和数据集
- **Kaggle**: 竞赛和数据集
- **Reddit**: r/MachineLearning, r/LanguageTechnology

### 中文社区
- **知乎**: AI写作话题
- **机器之心**: AI资讯和论文
- **PaperWeekly**: 论文分享
- **AI科技评论**: 学术报道

## 📋 研究项目模板

### 项目结构
```
research-project/
├── data/
│   ├── raw/              # 原始数据
│   ├── processed/        # 处理后数据
│   └── annotations/      # 标注数据
├── notebooks/            # Jupyter notebooks
├── src/
│   ├── data/            # 数据处理
│   ├── models/          # 模型定义
│   ├── evaluation/      # 评估脚本
│   └── visualization/   # 可视化
├── experiments/         # 实验配置和结果
├── papers/              # 相关论文
└── README.md
```

### 研究记录
- 实验日志
- 数据字典
- 模型卡片
- 结果分析
- 可重现性清单

## 🔗 相关链接

### 数据集仓库
- [Hugging Face Datasets](https://huggingface.co/datasets)
- [Kaggle Datasets](https://www.kaggle.com/datasets)
- [Google Dataset Search](https://datasetsearch.research.google.com/)
- [中文NLP数据集](https://github.com/InsaneLife/ChineseNLPCorpus)

### 模型仓库
- [Hugging Face Models](https://huggingface.co/models)
- [ModelScope](https://modelscope.cn/) (中文)
- [OpenAI Models](https://platform.openai.com/docs/models)

### 工具和框架
- [LangChain](https://github.com/langchain-ai/langchain)
- [LlamaIndex](https://github.com/run-llama/llama_index)
- [Haystack](https://github.com/deepset-ai/haystack)

## 📝 投稿指南

### 论文写作
1. **问题定义**: 清晰的研究问题
2. **相关工作**: 文献综述
3. **方法论**: 详细的技术描述
4. **实验**: 充分的实验验证
5. **结果**: 客观的结果分析
6. **讨论**: 深入的讨论和局限性
7. **结论**: 贡献总结

### 开源贡献
- 代码规范
- 文档完善
- 可重现性
- 许可证选择
- 社区维护

## 🌟 未来研究方向

1. **多模态小说生成**: 文本+图像+音频
2. **个性化写作助手**: 学习作者风格
3. **长篇叙事连贯性**: 百万字级别生成
4. **文化适应性**: 不同文化背景的创作
5. **伦理和版权**: AI生成内容的归属
6. **认知科学**: 理解创意过程

---

欢迎研究者和开发者贡献资源和研究成果！
