# 基于Ubuntu 22.04的基础镜像
FROM ubuntu:22.04

# 设置环境变量避免交互式安装
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    DISPLAY=:99 \
    CHROME_VERSION=134.0.6998.36 \
    CHROMEDRIVER_VERSION=134.0.6998.36

# 设置工作目录
WORKDIR /app

# 安装基础工具和依赖
RUN apt-get update && apt-get install -y \
    # 基础网络工具
    curl \
    wget \
    net-tools \
    iputils-ping \
    dnsutils \
    traceroute \
    netcat \
    telnet \
    openssh-client \
    # 开发工具
    git \
    vim \
    unzip \
    ca-certificates \
    gnupg \
    # Python相关
    python3.10 \
    python3-pip \
    python3-dev \
    build-essential \
    # Node.js相关
    nodejs \
    npm \
    # Chrome依赖
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libwayland-client0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxkbcommon0 \
    libxrandr2 \
    xdg-utils \
    libu2f-udev \
    libvulkan1 \
    # 虚拟显示
    xvfb \
    # 字体支持
    fonts-noto-cjk \
    && rm -rf /var/lib/apt/lists/*

# 创建python和python3的软链接
RUN ln -sf /usr/bin/python3 /usr/bin/python

# 安装Google Chrome
RUN wget -q https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_${CHROME_VERSION}-1_amd64.deb -O /tmp/chrome.deb || \
    wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -O /tmp/chrome.deb && \
    apt-get update && \
    apt-get install -y /tmp/chrome.deb || true && \
    apt-get install -f -y && \
    rm /tmp/chrome.deb && \
    rm -rf /var/lib/apt/lists/*

# 复制预下载的ChromeDriver
COPY drivers/chromedriver/chromedriver-win64/chromedriver.exe /tmp/chromedriver-win.exe
# 下载Linux版本的ChromeDriver
RUN wget -q https://storage.googleapis.com/chrome-for-testing-public/${CHROMEDRIVER_VERSION}/linux64/chromedriver-linux64.zip -O /tmp/chromedriver.zip || \
    wget -q https://chromedriver.storage.googleapis.com/LATEST_RELEASE -O /tmp/latest && \
    wget -q https://chromedriver.storage.googleapis.com/$(cat /tmp/latest)/chromedriver_linux64.zip -O /tmp/chromedriver.zip && \
    unzip /tmp/chromedriver.zip -d /tmp/ && \
    mv /tmp/chromedriver-linux64/chromedriver /usr/local/bin/ || mv /tmp/chromedriver /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver && \
    rm -rf /tmp/chromedriver* /tmp/latest

# 创建配置目录
RUN mkdir -p /app/config /app/scripts /app/logs /app/data

# 复制配置文件模板
COPY config/pip.conf.template /app/config/ 2>/dev/null || echo "[global]" > /app/config/pip.conf.template
COPY config/npmrc.template /app/config/ 2>/dev/null || echo "registry=https://registry.npmjs.org/" > /app/config/npmrc.template

# 复制配置脚本
COPY scripts/configure-sources.sh /app/scripts/
RUN chmod +x /app/scripts/configure-sources.sh

# 复制入口脚本
COPY scripts/entrypoint.sh /app/scripts/
RUN chmod +x /app/scripts/entrypoint.sh

# 复制requirements.txt（如果存在）
COPY requirements.txt /app/ 2>/dev/null || echo "selenium>=4.15.0" > /app/requirements.txt

# 复制应用代码
COPY app/ /app/app/ 2>/dev/null || mkdir -p /app/app

# 暴露端口（根据需要调整）
EXPOSE 8080 4444

# 设置入口点
ENTRYPOINT ["/app/scripts/entrypoint.sh"]

# 默认命令
CMD ["python", "/app/app/main.py"]
