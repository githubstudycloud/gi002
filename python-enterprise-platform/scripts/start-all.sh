#!/bin/bash

# 启动所有服务的脚本

echo "================================================"
echo "  Python Enterprise Platform - 启动脚本"
echo "================================================"
echo ""

# 检查Docker是否运行
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker未运行，请先启动Docker"
    exit 1
fi

echo "✅ Docker运行正常"
echo ""

# 启动基础设施
echo "📦 启动基础设施服务..."
docker-compose up -d postgres redis mongodb rabbitmq elasticsearch

echo ""
echo "⏳ 等待服务启动 (30秒)..."
sleep 30

# 检查服务健康状态
echo ""
echo "🔍 检查服务状态..."

services=("postgres" "redis" "mongodb" "rabbitmq" "elasticsearch")

for service in "${services[@]}"; do
    if docker-compose ps $service | grep -q "Up"; then
        echo "  ✅ $service: 运行中"
    else
        echo "  ❌ $service: 未运行"
    fi
done

echo ""
echo "================================================"
echo "  服务访问地址"
echo "================================================"
echo "  PostgreSQL:     localhost:5432"
echo "  Redis:          localhost:6379"
echo "  MongoDB:        localhost:27017"
echo "  RabbitMQ:       localhost:5672"
echo "  RabbitMQ管理:   http://localhost:15672 (guest/guest)"
echo "  Elasticsearch:  http://localhost:9200"
echo "================================================"
echo ""

echo "✅ 基础设施启动完成！"
echo ""
echo "下一步："
echo "  1. 安装Python依赖: pip install -r requirements.txt"
echo "  2. 初始化数据库:   python scripts/init-db.py"
echo "  3. 启动用户服务:   cd services/user-service && python main.py"
echo ""
echo "或使用Docker启动服务:"
echo "  docker-compose up -d user-service"
echo ""
