# Docker 镜像分卷文件说明

## 镜像信息

- **镜像名称**: chrome-selenium-automation
- **版本标签**: latest, 142
- **Chrome版本**: 142.0.7444.175
- **ChromeDriver版本**: 142.0.7444.175
- **镜像大小**: 1.71GB
- **构建时间**: 2025-11-20
- **系统**: Ubuntu 22.04

## 分卷文件

由于GitHub文件大小限制（100MB），镜像已分卷压缩为以下文件（每份95MB）：

**Docker镜像部分1** (原partaa，500MB):
- `chrome-selenium-automation.tar.gz.partaa.aa` (95MB)
- `chrome-selenium-automation.tar.gz.partaa.ab` (95MB)
- `chrome-selenium-automation.tar.gz.partaa.ac` (95MB)
- `chrome-selenium-automation.tar.gz.partaa.ad` (95MB)
- `chrome-selenium-automation.tar.gz.partaa.ae` (95MB)
- `chrome-selenium-automation.tar.gz.partaa.af` (25MB)

**Docker镜像部分2** (原partab，205MB):
- `chrome-selenium-automation.tar.gz.partab.aa` (95MB)
- `chrome-selenium-automation.tar.gz.partab.ab` (95MB)
- `chrome-selenium-automation.tar.gz.partab.ac` (15MB)

**Chrome安装包** (113MB):
- `google-chrome-stable_current_amd64.deb.partab` (18MB)

注意：Chrome deb文件小于100MB，只需要partab部分（实际是完整文件，命名延续分卷格式）

总大小: 约818MB (所有分卷)

## 导入镜像

### Linux/Mac

```bash
# 先合并第一部分的所有分卷
cat chrome-selenium-automation.tar.gz.partaa.* > chrome-selenium-automation.tar.gz.partaa

# 再合并第二部分的所有分卷
cat chrome-selenium-automation.tar.gz.partab.* > chrome-selenium-automation.tar.gz.partab

# 最后合并两个大分卷并导入
cat chrome-selenium-automation.tar.gz.partaa chrome-selenium-automation.tar.gz.partab | gunzip | docker load

# 或者一条命令（推荐）
(cat chrome-selenium-automation.tar.gz.partaa.*; cat chrome-selenium-automation.tar.gz.partab.*) | gunzip | docker load
```

恢复Chrome deb文件：
```bash
# 如果是完整的partab文件，直接重命名
mv google-chrome-stable_current_amd64.deb.partab google-chrome-stable_current_amd64.deb
```

### Windows (PowerShell)

```powershell
# 合并分卷
Get-Content chrome-selenium-automation.tar.gz.part* -Raw | Set-Content chrome-selenium-automation.tar.gz -Encoding Byte

# 解压 (需要7-Zip或WinRAR)
7z x chrome-selenium-automation.tar.gz
docker load -i chrome-selenium-automation.tar
```

### Windows (Git Bash)

```bash
cat chrome-selenium-automation.tar.gz.part* | gunzip | docker load
```

## 验证镜像

```bash
# 查看导入的镜像
docker images | grep chrome-selenium

# 运行测试
docker run --rm chrome-selenium-automation:latest \
  bash -c 'google-chrome --version && chromedriver --version'
```

## 使用镜像

### 直接运行

```bash
docker run -it --rm \
  --name chrome-automation \
  chrome-selenium-automation:latest
```

### 使用 docker-compose

```bash
# 编辑 docker-compose.yml 中的镜像名
image: chrome-selenium-automation:latest

# 启动
docker-compose up
```

### 自定义配置

```bash
docker run -it --rm \
  -e CHROME_HEADLESS=true \
  -e PIP_INDEX_URL=https://mirrors.aliyun.com/pypi/simple/ \
  -v $(pwd)/app:/app/app \
  -v $(pwd)/logs:/app/logs \
  chrome-selenium-automation:latest
```

## 镜像内容

- Ubuntu 22.04 base
- Python 3.10 + pip
- Node.js 12 + npm
- Google Chrome 142
- ChromeDriver 142
- Selenium 4.38.0
- 完整的开发工具和网络工具
- Xvfb虚拟显示支持

## 重新导出镜像

如果需要重新导出：

```bash
# 导出为单个文件
docker save chrome-selenium-automation:latest | gzip > chrome-selenium-automation.tar.gz

# 导出并分卷 (每500MB)
docker save chrome-selenium-automation:latest | gzip | split -b 500M - chrome-selenium-automation.tar.gz.part
```

## 故障排查

### 合并文件失败

确保所有分卷文件在同一目录，且文件名连续：
- partaa, partab (Linux)
- part01, part02 (Windows)

### 导入失败

```bash
# 检查文件完整性
cat chrome-selenium-automation.tar.gz.part* | gunzip > /dev/null
# 如果没有错误，说明文件完整

# 检查Docker是否运行
docker ps
```

### 空间不足

解压和导入需要约3.5GB临时空间（1.71GB镜像 + 1.7GB临时文件）

## 更多信息

查看 [README.md](README.md) 获取完整的使用文档。
