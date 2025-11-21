# 快速开始指南 / Quick Start Guide

## 🚀 5分钟开始AI小说创作

### 第一步：选择工具

#### 场景A：我想快速体验（云端方案）
推荐使用在线工具，无需安装：
- **中文**: 302_novel_writing
- **英文**: GPTAuthor 或 NovelAI

**优点**: 即开即用，无需技术背景
**缺点**: 需要API密钥，有使用成本

#### 场景B：我注重隐私（本地方案）
推荐本地部署：
- **工具**: AIStoryWriter + Ollama
- **模型**: Llama 3, Mistral

**优点**: 完全私密，无使用限制
**缺点**: 需要GPU，技术门槛较高

#### 场景C：我想人机协同（混合方案）
推荐半自动工具：
- **GPTAuthor**: 人工审核+AI生成
- **WriterAI**: AI辅助人类创作

**优点**: 平衡控制和效率
**缺点**: 需要时间投入

---

## 📋 环境准备

### 方案1：使用云端API

#### 1. 获取API密钥

**OpenAI**:
```bash
# 访问 https://platform.openai.com/api-keys
# 创建新密钥
export OPENAI_API_KEY="sk-..."
```

**Google Gemini**:
```bash
# 访问 https://makersuite.google.com/app/apikey
export GOOGLE_API_KEY="..."
```

**Kimi (月之暗面)**:
```bash
# 访问 https://platform.moonshot.cn/
export MOONSHOT_API_KEY="..."
```

#### 2. 安装Python依赖
```bash
pip install openai anthropic google-generativeai langchain
```

---

### 方案2：本地部署

#### 1. 安装Ollama
**MacOS/Linux**:
```bash
curl https://ollama.ai/install.sh | sh
```

**Windows**:
```bash
# 下载安装器
# https://ollama.ai/download/windows
```

#### 2. 下载模型
```bash
# 下载Llama 3 (推荐)
ollama pull llama3

# 或者下载Mistral
ollama pull mistral

# 或者中文优化的Qwen
ollama pull qwen
```

#### 3. 测试模型
```bash
ollama run llama3
```

---

## ✍️ 创作第一个故事

### 使用Python + OpenAI

#### 方式1：简单脚本
```python
import openai
import os

# 设置API密钥
openai.api_key = os.getenv("OPENAI_API_KEY")

# 定义提示词
prompt = """
请写一个科幻短篇小说的开头（约500字）。

设定：
- 时间：2157年
- 地点：火星殖民地
- 主角：年轻的工程师李明
- 冲突：发现了未知的地下结构

要求：
- 第三人称叙述
- 悬疑氛围
- 详细的场景描写
"""

# 生成内容
response = openai.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "你是一位专业的科幻小说作家。"},
        {"role": "user", "content": prompt}
    ],
    temperature=0.8,
    max_tokens=1000
)

# 输出结果
story = response.choices[0].message.content
print(story)

# 保存到文件
with open("chapter_01.txt", "w", encoding="utf-8") as f:
    f.write(story)
```

#### 方式2：使用LangChain
```python
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

# 初始化模型
llm = ChatOpenAI(
    model_name="gpt-4",
    temperature=0.8
)

# 创建提示词模板
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "你是一位{genre}小说作家。"),
    ("user", """
    请写一个{genre}小说的{part}（约{word_count}字）。

    设定：
    {setting}

    要求：
    {requirements}
    """)
])

# 创建链
chain = LLMChain(llm=llm, prompt=prompt_template)

# 生成内容
result = chain.run(
    genre="科幻",
    part="开头",
    word_count=500,
    setting="""
    - 时间：2157年
    - 地点：火星殖民地
    - 主角：年轻的工程师李明
    """,
    requirements="""
    - 第三人称叙述
    - 悬疑氛围
    - 详细的场景描写
    """
)

print(result)
```

---

### 使用本地模型（Ollama）

```python
import ollama

# 定义提示词
prompt = """
请写一个都市言情小说的开头（约500字）。

设定：
- 地点：现代都市
- 女主：独立的职场女性，30岁
- 男主：神秘的总裁
- 冲突：意外的相遇

要求：
- 轻松幽默的语气
- 细腻的心理描写
- 对话自然生动
"""

# 生成内容
response = ollama.generate(
    model='llama3',
    prompt=prompt,
    options={
        'temperature': 0.8,
        'num_predict': 1000,
    }
)

story = response['response']
print(story)

# 保存
with open("romance_chapter_01.txt", "w", encoding="utf-8") as f:
    f.write(story)
```

---

## 📖 完整小说生成流程

### 阶段1：规划（Planning）

#### 1.1 定义小说框架
```python
novel_outline = {
    "title": "火星之谜",
    "genre": "科幻悬疑",
    "target_length": "中篇（5-10万字）",
    "main_characters": [
        {
            "name": "李明",
            "role": "主角",
            "description": "25岁工程师，好奇心强，逻辑思维缜密"
        },
        {
            "name": "张薇",
            "role": "女主",
            "description": "地质学家，勇敢独立"
        }
    ],
    "plot_points": [
        "发现地下结构",
        "探索神秘设施",
        "遭遇未知危险",
        "揭开真相",
        "做出选择"
    ],
    "chapters": 20
}
```

#### 1.2 生成章节大纲
```python
def generate_chapter_outline(novel_outline):
    prompt = f"""
    根据以下小说设定，生成详细的章节大纲：

    标题：{novel_outline['title']}
    类型：{novel_outline['genre']}
    章节数：{novel_outline['chapters']}

    主要角色：
    {format_characters(novel_outline['main_characters'])}

    关键情节点：
    {format_plot_points(novel_outline['plot_points'])}

    请为每一章生成：
    1. 章节标题
    2. 主要情节（2-3句话）
    3. 场景和角色
    4. 预计字数
    """

    # 调用AI生成
    outline = llm.generate(prompt)
    return outline

# 生成并保存大纲
chapter_outline = generate_chapter_outline(novel_outline)
with open("novel_outline.txt", "w", encoding="utf-8") as f:
    f.write(chapter_outline)
```

---

### 阶段2：生成（Generation）

#### 2.1 逐章生成
```python
def generate_chapter(chapter_number, chapter_info, previous_chapters):
    """生成单个章节"""

    # 构建上下文
    context = f"""
    小说标题：{novel_outline['title']}
    当前章节：第{chapter_number}章

    章节信息：
    {chapter_info}

    前情提要：
    {get_summary(previous_chapters)}

    角色状态：
    {get_character_states(chapter_number)}
    """

    # 生成章节内容
    prompt = f"""
    {context}

    请写第{chapter_number}章的内容（约3000-5000字）。

    要求：
    1. 保持角色性格一致
    2. 情节自然推进
    3. 场景描写细腻
    4. 对话真实生动
    5. 保持悬疑氛围
    """

    chapter_content = llm.generate(
        prompt,
        temperature=0.8,
        max_tokens=3000
    )

    return chapter_content

# 生成所有章节
chapters = []
for i in range(1, novel_outline['chapters'] + 1):
    print(f"正在生成第{i}章...")

    chapter_info = get_chapter_info(chapter_outline, i)
    chapter = generate_chapter(i, chapter_info, chapters)

    chapters.append(chapter)

    # 保存每章
    with open(f"chapter_{i:02d}.txt", "w", encoding="utf-8") as f:
        f.write(f"# 第{i}章\n\n")
        f.write(chapter)

    print(f"第{i}章生成完成！")
```

#### 2.2 保持连贯性
```python
def get_summary(previous_chapters, last_n=3):
    """获取前几章的摘要"""
    if not previous_chapters:
        return "这是第一章。"

    recent_chapters = previous_chapters[-last_n:]

    prompt = f"""
    请用2-3句话总结以下内容的关键情节：

    {' '.join(recent_chapters)}
    """

    summary = llm.generate(prompt, max_tokens=200)
    return summary
```

---

### 阶段3：润色（Refinement）

#### 3.1 内容检查
```python
def check_consistency(chapters):
    """检查情节一致性"""
    prompt = f"""
    请检查以下小说内容的一致性问题：

    {combine_chapters(chapters)}

    请指出：
    1. 时间线矛盾
    2. 角色性格不一致
    3. 情节逻辑问题
    4. 前后矛盾之处
    """

    issues = llm.generate(prompt)
    return issues

# 运行检查
issues = check_consistency(chapters)
print(issues)
```

#### 3.2 文字润色
```python
def polish_text(chapter_text):
    """润色单章内容"""
    prompt = f"""
    请润色以下文字，提升表达质量：

    {chapter_text}

    要求：
    1. 保持原意和风格
    2. 优化语言表达
    3. 增强情感渲染
    4. 改进对话真实性
    5. 删除冗余内容
    """

    polished = llm.generate(prompt, temperature=0.7)
    return polished

# 润色所有章节
polished_chapters = []
for i, chapter in enumerate(chapters):
    print(f"正在润色第{i+1}章...")
    polished = polish_text(chapter)
    polished_chapters.append(polished)

    # 保存润色版本
    with open(f"chapter_{i+1:02d}_polished.txt", "w", encoding="utf-8") as f:
        f.write(polished)
```

---

### 阶段4：整合（Assembly）

#### 4.1 合并成完整小说
```python
def assemble_novel(title, chapters):
    """合并所有章节"""
    novel = f"# {title}\n\n"
    novel += "---\n\n"

    for i, chapter in enumerate(chapters, 1):
        novel += f"## 第{i}章\n\n"
        novel += chapter
        novel += "\n\n---\n\n"

    return novel

# 生成完整小说
full_novel = assemble_novel(novel_outline['title'], polished_chapters)

# 保存
with open("full_novel.txt", "w", encoding="utf-8") as f:
    f.write(full_novel)

print(f"完整小说已生成！总字数：{len(full_novel)}")
```

---

## 🎯 提示词技巧

### 基础模板
```
角色：你是[角色描述]
任务：[具体任务]
背景：[相关背景信息]
要求：[具体要求清单]
格式：[输出格式]
```

### 高质量提示词示例

#### 场景描写
```
请描写一个雨夜的都市街道场景（约200字）。

时间：深夜11点
地点：市中心商业街
天气：暴雨
氛围：孤独、压抑
视角：第三人称，跟随主角

要求：
1. 调动多种感官（视觉、听觉、触觉）
2. 使用比喻和意象
3. 营造情绪氛围
4. 避免陈词滥调
5. 语言简洁有力
```

#### 角色对话
```
请写一段两人的对话（约300字）。

场景：咖啡厅
角色A：李明，25岁，程序员，内向理性
角色B：张薇，27岁，设计师，外向感性
关系：同事，暗生情愫
冲突：讨论是否接受新的工作机会

要求：
1. 符合角色性格
2. 对话自然生动
3. 有潜台词和张力
4. 推进情节发展
5. 适当加入动作和神态描写
```

#### 情节转折
```
当前情节：主角以为找到了真相
转折：发现一切都是假象
要求：
1. 在3个段落内完成转折
2. 第一段铺垫暗示
3. 第二段揭示转折
4. 第三段情感冲击
5. 保持悬念感
```

---

## 🛠️ 实用工具脚本

### 字数统计
```python
def count_words(text):
    """统计中英文字数"""
    import re

    # 中文字符
    chinese = len(re.findall(r'[\u4e00-\u9fff]', text))
    # 英文单词
    english = len(re.findall(r'\b[a-zA-Z]+\b', text))

    return {
        'chinese': chinese,
        'english': english,
        'total': chinese + english
    }

# 使用
stats = count_words(full_novel)
print(f"中文字符：{stats['chinese']}")
print(f"英文单词：{stats['english']}")
print(f"总字数：{stats['total']}")
```

### 关键词提取
```python
def extract_keywords(text, top_n=20):
    """提取文本关键词"""
    # 可以使用 jieba, NLTK 等
    import jieba.analyse

    keywords = jieba.analyse.extract_tags(
        text,
        topK=top_n,
        withWeight=True
    )

    return keywords

# 使用
keywords = extract_keywords(full_novel)
for word, weight in keywords:
    print(f"{word}: {weight:.4f}")
```

### 导出多种格式
```python
def export_novel(content, title, formats=['txt', 'md', 'docx']):
    """导出多种格式"""

    # TXT
    if 'txt' in formats:
        with open(f"{title}.txt", "w", encoding="utf-8") as f:
            f.write(content)

    # Markdown
    if 'md' in formats:
        with open(f"{title}.md", "w", encoding="utf-8") as f:
            f.write(content)

    # DOCX
    if 'docx' in formats:
        from docx import Document
        doc = Document()
        doc.add_heading(title, 0)
        for para in content.split('\n\n'):
            if para.strip():
                doc.add_paragraph(para)
        doc.save(f"{title}.docx")

    print(f"已导出格式：{', '.join(formats)}")

# 使用
export_novel(full_novel, novel_outline['title'])
```

---

## 💡 常见问题

### Q1: 生成的内容质量不高怎么办？
**A**:
1. 优化提示词，提供更多细节
2. 使用更强大的模型（如GPT-4）
3. 增加temperature来提升创意
4. 多次生成，选择最佳版本
5. 人工审核和修改

### Q2: 如何保持长篇小说的一致性？
**A**:
1. 维护角色卡片和设定文档
2. 每章生成时包含前情摘要
3. 定期运行一致性检查
4. 使用向量数据库存储上下文
5. 人工审核关键情节点

### Q3: 成本大概是多少？
**A**:
- GPT-4: ~$0.03/1K tokens（约$30-50/万字）
- GPT-3.5: ~$0.002/1K tokens（约$2-5/万字）
- Gemini: 免费配额，付费较便宜
- 本地模型：免费，但需要GPU

### Q4: 生成速度太慢怎么办？
**A**:
1. 使用更快的模型（GPT-3.5 vs GPT-4）
2. 减少max_tokens
3. 并行生成多个章节
4. 使用本地模型
5. 考虑使用GPU加速

### Q5: 能否商用AI生成的小说？
**A**:
- 各平台政策不同，需要查看具体条款
- OpenAI: 用户拥有生成内容的权利
- 建议进行人工编辑和修改
- 了解目标平台的AI内容政策
- 咨询法律专业人士

---

## 📚 进阶学习

### 推荐阅读
1. **提示词工程**: [PromptingGuide.ai](https://www.promptingguide.ai/)
2. **LangChain文档**: [python.langchain.com](https://python.langchain.com/)
3. **OpenAI Cookbook**: [GitHub](https://github.com/openai/openai-cookbook)

### 实践项目
1. 生成一个完整的短篇小说（5000字）
2. 创建自己的提示词模板库
3. 实现自动化的章节生成流程
4. 开发一个简单的Web界面

### 加入社区
- Reddit: r/AIWriting
- Discord: AI Writing Communities
- GitHub: 参与开源项目

---

## 🎉 开始创作吧！

现在你已经掌握了AI小说写作的基础知识和工具，开始你的创作之旅吧！

记住：
- AI是助手，不是替代品
- 保持你的创意和风格
- 多实践，多尝试
- 享受创作的过程

祝创作愉快！✨

---

**有问题？**
- 查看 [README.md](README.md) 了解更多项目
- 查看 [PROJECT-LIST.md](PROJECT-LIST.md) 选择合适的工具
- 参考各分类目录的详细文档
