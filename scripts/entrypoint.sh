#!/bin/bash
# Docker容器入口脚本

set -e

echo "=========================================="
echo "Chrome Selenium自动化容器启动"
echo "=========================================="

# 显示环境信息
show_environment() {
    echo "环境信息:"
    echo "  - Python版本: $(python --version)"
    echo "  - Node版本: $(node --version 2>/dev/null || echo '未安装')"
    echo "  - NPM版本: $(npm --version 2>/dev/null || echo '未安装')"
    echo "  - Chrome版本: $(google-chrome --version 2>/dev/null || echo '未安装')"
    echo "  - ChromeDriver版本: $(chromedriver --version 2>/dev/null || echo '未安装')"
    echo "  - 工作目录: $(pwd)"
    echo "  - 时区: ${TZ:-UTC}"
    echo "  - 模式: ${APP_MODE:-production}"
    echo ""
}

# 配置源
setup_sources() {
    echo "配置Python和NPM源..."
    if [ -f "/app/scripts/configure-sources.sh" ]; then
        source /app/scripts/configure-sources.sh
    else
        echo "警告: 未找到configure-sources.sh，跳过源配置"
    fi
    echo ""
}

# 安装Python依赖
install_python_dependencies() {
    if [ -f "/app/requirements.txt" ]; then
        echo "安装Python依赖..."
        pip install -r /app/requirements.txt --no-cache-dir
        echo "Python依赖安装完成"
    else
        echo "未找到requirements.txt，跳过Python依赖安装"
    fi
    echo ""
}

# 安装NPM依赖
install_npm_dependencies() {
    if [ -f "/app/package.json" ]; then
        echo "安装NPM依赖..."
        cd /app
        npm install
        echo "NPM依赖安装完成"
    else
        echo "未找到package.json，跳过NPM依赖安装"
    fi
    echo ""
}

# 启动虚拟显示
start_virtual_display() {
    if [ "$CHROME_HEADLESS" != "true" ] || [ "$ENABLE_VNC" == "true" ]; then
        echo "启动虚拟显示 (Xvfb)..."
        Xvfb :99 -screen 0 1920x1080x24 -ac +extension GLX +render -noreset &
        export DISPLAY=:99
        echo "虚拟显示已启动 (DISPLAY=$DISPLAY)"
    else
        echo "使用无头模式，跳过虚拟显示"
    fi
    echo ""
}

# 检查Chrome和ChromeDriver
check_chrome() {
    echo "检查Chrome和ChromeDriver..."

    if ! command -v google-chrome &> /dev/null; then
        echo "错误: 未找到Google Chrome"
        exit 1
    fi

    if ! command -v chromedriver &> /dev/null; then
        echo "错误: 未找到ChromeDriver"
        exit 1
    fi

    # 检查版本兼容性
    CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | cut -d. -f1)
    DRIVER_VERSION=$(chromedriver --version | awk '{print $2}' | cut -d. -f1)

    echo "Chrome主版本: $CHROME_VERSION"
    echo "ChromeDriver主版本: $DRIVER_VERSION"

    if [ "$CHROME_VERSION" != "$DRIVER_VERSION" ]; then
        echo "警告: Chrome和ChromeDriver版本可能不兼容"
    else
        echo "✓ 版本兼容性检查通过"
    fi
    echo ""
}

# 创建必要的目录
create_directories() {
    echo "创建必要的目录..."
    mkdir -p /app/logs /app/data /app/screenshots /app/downloads
    chmod -R 755 /app/logs /app/data /app/screenshots /app/downloads
    echo "目录创建完成"
    echo ""
}

# 运行健康检查服务（可选）
start_health_check() {
    if [ -f "/app/scripts/health-check.py" ]; then
        echo "启动健康检查服务..."
        python /app/scripts/health-check.py &
    fi
}

# 主函数
main() {
    echo "开始初始化容器..."
    echo ""

    # 显示环境信息
    show_environment

    # 配置源
    setup_sources

    # 安装依赖
    install_python_dependencies
    install_npm_dependencies

    # 启动虚拟显示
    start_virtual_display

    # 检查Chrome
    check_chrome

    # 创建目录
    create_directories

    # 启动健康检查
    start_health_check

    echo "=========================================="
    echo "容器初始化完成，开始执行应用"
    echo "=========================================="
    echo ""

    # 执行传入的命令
    exec "$@"
}

# 捕获信号以优雅退出
trap 'echo "收到退出信号，正在关闭..."; exit 0' SIGTERM SIGINT

# 运行主函数
main "$@"
