# Chrome Selenium 自动化 Docker 镜像

基于 Ubuntu 22.04 的 Python Selenium 自动化测试环境，预装 Google Chrome 和 ChromeDriver，支持灵活的镜像源配置和多种启动方式。

## 特性

- ✅ 预装 Google Chrome 134 和 ChromeDriver 134
- ✅ 支持外置配置 Python pip 和 NPM 镜像源
- ✅ 包含常用网络工具（curl, wget, ping, netcat等）
- ✅ 支持 docker-compose 启动
- ✅ 支持 Dockerfile 构建并启动
- ✅ 支持 IDEA/VSCode Docker 插件
- ✅ 无头模式和虚拟显示支持
- ✅ 完整的日志和截图功能

## 目录结构

```
.
├── Dockerfile                  # Docker镜像构建文件
├── docker-compose.yml          # Docker Compose配置
├── .env.example               # 环境变量示例
├── requirements.txt           # Python依赖
├── app/                       # 应用代码目录
│   └── main.py               # 示例自动化脚本
├── config/                    # 配置文件目录
│   ├── pip.conf.template     # pip源配置模板
│   └── npmrc.template        # npm源配置模板
├── scripts/                   # 脚本目录
│   ├── configure-sources.sh  # 源配置脚本
│   ├── entrypoint.sh        # 容器入口脚本
│   └── health-check.py      # 健康检查服务
├── drivers/                   # 驱动目录
│   └── chromedriver/         # ChromeDriver文件
├── logs/                      # 日志目录
├── data/                      # 数据目录
└── screenshots/              # 截图目录
```

## 快速开始

### 1. 克隆仓库

```bash
git clone git@github.com:githubstudycloud/gi002.git
cd gi002
```

### 2. 配置环境变量

```bash
# 复制环境变量示例文件
cp .env.example .env

# 编辑 .env 文件，配置镜像源等参数
vim .env
```

### 3. 配置镜像源（可选）

#### 方法1: 通过环境变量配置（推荐）

编辑 `.env` 文件：

```bash
# 使用阿里云镜像
PIP_INDEX_URL=https://mirrors.aliyun.com/pypi/simple/
PIP_TRUSTED_HOST=mirrors.aliyun.com
NPM_REGISTRY=https://registry.npmmirror.com/
```

#### 方法2: 通过配置文件

```bash
# 复制模板文件
cp config/pip.conf.template config/pip.conf
cp config/npmrc.template config/.npmrc

# 编辑配置文件
vim config/pip.conf
vim config/.npmrc
```

### 4. 启动方式

#### 方式1: 使用 docker-compose（推荐）

```bash
# 构建并启动
docker-compose up --build

# 后台运行
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止
docker-compose down
```

#### 方式2: 使用 Dockerfile

```bash
# 构建镜像
docker build -t chrome-selenium-automation:latest .

# 运行容器
docker run -it --rm \
  -v $(pwd)/app:/app/app \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/screenshots:/app/screenshots \
  -e PIP_INDEX_URL=https://mirrors.aliyun.com/pypi/simple/ \
  chrome-selenium-automation:latest

# 或者使用自定义命令
docker run -it --rm \
  -v $(pwd)/app:/app/app \
  chrome-selenium-automation:latest \
  python /app/app/main.py
```

#### 方式3: Linux 命令行启动

```bash
# 创建启动脚本
cat > run.sh << 'EOF'
#!/bin/bash
docker run -it --rm \
  --name chrome-automation \
  -v $(pwd)/app:/app/app \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/screenshots:/app/screenshots \
  -v $(pwd)/config:/app/config \
  -e PIP_INDEX_URL=${PIP_INDEX_URL} \
  -e NPM_REGISTRY=${NPM_REGISTRY} \
  -p 8080:8080 \
  chrome-selenium-automation:latest
EOF

chmod +x run.sh
./run.sh
```

#### 方式4: IDEA/VSCode 配置

##### IntelliJ IDEA

1. 打开项目
2. 右键 `Dockerfile` -> Run 'Dockerfile'
3. 或者配置 Run Configuration:
   - Type: Docker -> Dockerfile
   - Dockerfile: ./Dockerfile
   - Context folder: .
   - Container name: chrome-automation

##### VSCode

1. 安装 Docker 扩展
2. 右键 `Dockerfile` -> Build Image
3. 或者右键 `docker-compose.yml` -> Compose Up

## 配置说明

### 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `PIP_INDEX_URL` | Python pip 镜像源 | `https://pypi.org/simple` |
| `PIP_TRUSTED_HOST` | pip 信任的主机 | 空 |
| `NPM_REGISTRY` | NPM 镜像源 | `https://registry.npmjs.org/` |
| `CHROME_HEADLESS` | 启用无头模式 | `true` |
| `CHROME_NO_SANDBOX` | 禁用沙箱 | `true` |
| `APP_MODE` | 应用模式 | `production` |
| `LOG_LEVEL` | 日志级别 | `INFO` |
| `TZ` | 时区 | `Asia/Shanghai` |

### 常用镜像源

#### Python (pip)

```bash
# 阿里云
PIP_INDEX_URL=https://mirrors.aliyun.com/pypi/simple/

# 清华大学
PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple/

# 中科大
PIP_INDEX_URL=https://pypi.mirrors.ustc.edu.cn/simple/

# 华为云
PIP_INDEX_URL=https://mirrors.huaweicloud.com/repository/pypi/simple/
```

#### NPM

```bash
# 淘宝镜像
NPM_REGISTRY=https://registry.npmmirror.com/

# 腾讯云
NPM_REGISTRY=https://mirrors.cloud.tencent.com/npm/

# 华为云
NPM_REGISTRY=https://mirrors.huaweicloud.com/repository/npm/
```

## 开发指南

### 编写自动化脚本

1. 在 `app/` 目录下创建 Python 脚本
2. 继承 `ChromeAutomation` 基类
3. 实现 `run()` 方法

示例：

```python
from app.main import ChromeAutomation

class MyAutomation(ChromeAutomation):
    def run(self):
        self.driver.get("https://example.com")
        self.take_screenshot("example")
        # 你的自动化逻辑
```

### 添加 Python 依赖

编辑 `requirements.txt`：

```bash
# 添加新的依赖
echo "beautifulsoup4>=4.12.0" >> requirements.txt

# 重新构建镜像
docker-compose build
```

### 调试技巧

```bash
# 进入运行中的容器
docker-compose exec chrome-automation bash

# 查看日志
docker-compose logs -f chrome-automation

# 查看截图
ls -lh screenshots/

# 测试 Chrome
docker-compose exec chrome-automation google-chrome --version
docker-compose exec chrome-automation chromedriver --version
```

## 高级用法

### 启动时安装依赖

docker-compose 会自动在容器启动时安装 `requirements.txt` 中的依赖。

### 使用 MCP 远程执行

```python
# 在 MCP 连接的远程服务器上运行
from mcp import exec_command

# 拉取镜像
exec_command("docker pull chrome-selenium-automation:latest")

# 运行容器
exec_command("docker run -d chrome-selenium-automation:latest")
```

### 持久化数据

```yaml
# docker-compose.yml
volumes:
  - ./data:/app/data        # 数据持久化
  - ./logs:/app/logs        # 日志持久化
  - ./screenshots:/app/screenshots  # 截图持久化
```

### 网络配置

```yaml
# docker-compose.yml
networks:
  automation-network:
    driver: bridge
```

## 故障排查

### Chrome 崩溃

```bash
# 增加共享内存
docker run --shm-size=2g ...

# 或在 docker-compose.yml 中
shm_size: '2gb'
```

### 权限问题

```bash
# 修改目录权限
chmod -R 755 logs/ screenshots/ data/
```

### 网络连接问题

```bash
# 测试网络
docker-compose exec chrome-automation ping -c 3 google.com

# 测试镜像源
docker-compose exec chrome-automation curl -I https://mirrors.aliyun.com/pypi/simple/
```

## 安全说明

- 生产环境建议使用非 root 用户运行
- 定期更新 Chrome 和 ChromeDriver 版本
- 不要在镜像中硬编码敏感信息
- 使用 `.env` 文件管理环境变量

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 更新日志

- 2025-11-17: 初始版本发布
  - 支持 Chrome 134.0.6998.36
  - 支持灵活的镜像源配置
  - 支持多种启动方式
