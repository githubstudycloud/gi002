#!/bin/bash

echo "==============================================="
echo "  Spring Boot 2.x 企业级框架启动脚本"
echo "==============================================="
echo ""

# 检查 Java 环境
if ! command -v java &> /dev/null; then
    echo "错误: 未找到 Java，请先安装 JDK 1.8+"
    exit 1
fi

# 检查 Maven 环境
if ! command -v mvn &> /dev/null; then
    echo "错误: 未找到 Maven，请先安装 Maven 3.6+"
    exit 1
fi

# 创建日志目录
mkdir -p logs

echo "[1/4] 启动网关服务 (端口: 9527)..."
cd enterprise-gateway
nohup mvn spring-boot:run > ../logs/gateway.log 2>&1 &
echo "网关服务 PID: $!"
cd ..
sleep 5

echo "[2/4] 启动认证服务 (端口: 9200)..."
cd enterprise-auth
nohup mvn spring-boot:run > ../logs/auth.log 2>&1 &
echo "认证服务 PID: $!"
cd ..
sleep 5

echo "[3/4] 启动系统服务 (端口: 9201)..."
cd enterprise-modules/system
nohup mvn spring-boot:run > ../../logs/system.log 2>&1 &
echo "系统服务 PID: $!"
cd ../..
sleep 5

echo ""
echo "==============================================="
echo "  所有服务启动完成！"
echo "  - 网关服务: http://localhost:9527"
echo "  - 认证服务: http://localhost:9200"
echo "  - 系统服务: http://localhost:9201"
echo "==============================================="
echo ""
echo "查看日志: tail -f logs/*.log"
echo ""
