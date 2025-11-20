#!/bin/bash
# 配置Python和NPM源的脚本

set -e

echo "=== 配置Python和NPM源 ==="

# 配置pip源
configure_pip() {
    echo "正在配置pip源..."

    # 创建pip配置目录
    mkdir -p ~/.pip

    # 如果设置了环境变量PIP_INDEX_URL，使用环境变量配置
    if [ -n "$PIP_INDEX_URL" ]; then
        echo "使用环境变量配置pip源: $PIP_INDEX_URL"
        cat > ~/.pip/pip.conf <<EOF
[global]
index-url = $PIP_INDEX_URL
timeout = 120
retries = 5

[install]
EOF

        # 如果设置了trusted-host
        if [ -n "$PIP_TRUSTED_HOST" ]; then
            echo "trusted-host = $PIP_TRUSTED_HOST" >> ~/.pip/pip.conf
        fi
    # 否则检查是否有自定义配置文件
    elif [ -f "/app/config/pip.conf" ]; then
        echo "使用自定义pip配置文件"
        cp /app/config/pip.conf ~/.pip/pip.conf
    elif [ -f "/app/config/pip.conf.template" ]; then
        echo "使用默认pip配置模板"
        cp /app/config/pip.conf.template ~/.pip/pip.conf
    else
        echo "未找到pip配置，使用默认PyPI源"
    fi

    # 显示当前配置
    if [ -f ~/.pip/pip.conf ]; then
        echo "当前pip配置:"
        cat ~/.pip/pip.conf
    fi

    # 升级pip
    echo "升级pip..."
    python -m pip install --upgrade pip || true
}

# 配置npm源
configure_npm() {
    echo "正在配置npm源..."

    # 如果设置了环境变量NPM_REGISTRY，使用环境变量配置
    if [ -n "$NPM_REGISTRY" ]; then
        echo "使用环境变量配置npm源: $NPM_REGISTRY"
        npm config set registry "$NPM_REGISTRY"
    # 否则检查是否有自定义配置文件
    elif [ -f "/app/config/.npmrc" ]; then
        echo "使用自定义npm配置文件"
        cp /app/config/.npmrc ~/.npmrc
    elif [ -f "/app/config/npmrc.template" ]; then
        echo "使用默认npm配置模板"
        cp /app/config/npmrc.template ~/.npmrc
    else
        echo "未找到npm配置，使用默认npm源"
    fi

    # 显示当前配置
    echo "当前npm配置:"
    npm config get registry
}

# 测试网络连接
test_connectivity() {
    echo "测试网络连接..."

    # 测试pip源
    if [ -f ~/.pip/pip.conf ]; then
        PIP_INDEX=$(grep "index-url" ~/.pip/pip.conf | awk '{print $3}' | head -1)
        if [ -n "$PIP_INDEX" ]; then
            echo "测试pip源连接: $PIP_INDEX"
            curl -I --connect-timeout 5 "$PIP_INDEX" > /dev/null 2>&1 && echo "✓ pip源连接正常" || echo "✗ pip源连接失败"
        fi
    fi

    # 测试npm源
    NPM_REGISTRY=$(npm config get registry)
    if [ -n "$NPM_REGISTRY" ]; then
        echo "测试npm源连接: $NPM_REGISTRY"
        curl -I --connect-timeout 5 "$NPM_REGISTRY" > /dev/null 2>&1 && echo "✓ npm源连接正常" || echo "✗ npm源连接失败"
    fi
}

# 主函数
main() {
    echo "开始配置..."

    configure_pip
    echo ""

    configure_npm
    echo ""

    test_connectivity
    echo ""

    echo "=== 配置完成 ==="
}

# 如果直接运行此脚本，执行主函数
if [ "${BASH_SOURCE[0]}" == "${0}" ]; then
    main
fi
