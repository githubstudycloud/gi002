#!/bin/bash

# 启动所有中间件服务
echo "========================================="
echo "启动 Go Enterprise Platform 中间件服务"
echo "========================================="
echo ""

cd "$(dirname "$0")/../deployments/docker"

echo "检查 Docker 和 Docker Compose..."
if ! command -v docker &> /dev/null; then
    echo "错误: Docker 未安装"
    exit 1
fi

if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "错误: Docker Compose 未安装"
    exit 1
fi

echo "启动所有服务..."
echo ""

# 使用 docker compose 或 docker-compose
if docker compose version &> /dev/null; then
    docker compose up -d
else
    docker-compose up -d
fi

echo ""
echo "等待服务启动..."
sleep 10

echo ""
echo "服务状态:"
if docker compose version &> /dev/null; then
    docker compose ps
else
    docker-compose ps
fi

echo ""
echo "========================================="
echo "服务启动完成"
echo "========================================="
echo ""
echo "可用的服务:"
echo "  - MySQL:        localhost:3306"
echo "  - PostgreSQL:   localhost:5432"
echo "  - MongoDB:      localhost:27017"
echo "  - Redis:        localhost:6379"
echo "  - Memcached:    localhost:11211"
echo "  - RabbitMQ:     localhost:5672 (管理界面: http://localhost:15672)"
echo "  - Kafka:        localhost:9092"
echo "  - Consul:       http://localhost:8500"
echo "  - Etcd:         localhost:2379"
echo "  - Prometheus:   http://localhost:9090"
echo "  - Grafana:      http://localhost:3000 (admin/admin123456)"
echo "  - Jaeger:       http://localhost:16686"
echo ""
echo "运行 'bash scripts/test-services.sh' 测试服务连接"
echo ""
