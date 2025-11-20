# Chrome Selenium Automation Project

Docker-based Chrome Selenium automation environment for testing and web scraping.

## 项目结构

```
gi002/
├── README-ROOT.md                     # 项目总览（本文件）
├── drivers/                          # ChromeDriver 二进制文件
│   └── chromedriver/                # ChromeDriver 134.0.6998.36 (Windows)
└── chrome-selenium-docker/          # Docker 自动化项目主目录
    ├── README.md                    # 详细文档
    ├── Dockerfile                   # Docker 镜像定义
    ├── docker-compose.yml          # Docker Compose 配置
    ├── requirements.txt            # Python 依赖
    ├── app/                        # 应用代码
    ├── config/                     # 配置模板
    ├── scripts/                    # 脚本文件
    └── drivers/                    # 容器用 ChromeDriver
```

## 快速开始

### 本地使用

```bash
cd chrome-selenium-docker
docker-compose up --build
```

### 远程服务器部署

```bash
git clone git@github.com:githubstudycloud/gi002.git
cd gi002/chrome-selenium-docker
docker-compose up -d
```

## 特性

- ✅ 预装 Chrome 134 + ChromeDriver 134
- ✅ Python 3.10 Selenium 环境
- ✅ 支持配置 pip/npm 镜像源
- ✅ 多种启动方式（compose/dockerfile/IDE）
- ✅ 无头模式 + 虚拟显示
- ✅ 完整日志和截图功能

## 详细文档

查看 [chrome-selenium-docker/README.md](chrome-selenium-docker/README.md) 获取完整文档。

## 目录说明

- **drivers/**: 包含 Windows 版本的 ChromeDriver，用于本地开发
- **chrome-selenium-docker/**: Docker 项目主目录，包含所有运行所需文件

## 版本信息

- Chrome: 134.0.6998.36
- ChromeDriver: 134.0.6998.36
- Python: 3.10
- Selenium: >=4.15.0
- Ubuntu: 22.04

---

创建时间: 2025-11-17
