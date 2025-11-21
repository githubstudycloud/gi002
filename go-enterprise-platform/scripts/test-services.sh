#!/bin/bash

# 测试所有中间件服务连接
# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "========================================="
echo "Go Enterprise Platform - 服务连接测试"
echo "========================================="
echo ""

# 测试 MySQL
echo -n "测试 MySQL (3306)... "
if nc -zv localhost 3306 2>&1 | grep -q succeeded || nc -zv localhost 3306 2>&1 | grep -q open; then
    echo -e "${GREEN}✓ 连接成功${NC}"
    echo "  - 用户: appuser"
    echo "  - 密码: apppass123"
    echo "  - 数据库: enterprise_db"
else
    echo -e "${RED}✗ 连接失败${NC}"
fi
echo ""

# 测试 PostgreSQL
echo -n "测试 PostgreSQL (5432)... "
if nc -zv localhost 5432 2>&1 | grep -q succeeded || nc -zv localhost 5432 2>&1 | grep -q open; then
    echo -e "${GREEN}✓ 连接成功${NC}"
    echo "  - 用户: appuser"
    echo "  - 密码: apppass123"
    echo "  - 数据库: enterprise_db"
else
    echo -e "${RED}✗ 连接失败${NC}"
fi
echo ""

# 测试 MongoDB
echo -n "测试 MongoDB (27017)... "
if nc -zv localhost 27017 2>&1 | grep -q succeeded || nc -zv localhost 27017 2>&1 | grep -q open; then
    echo -e "${GREEN}✓ 连接成功${NC}"
    echo "  - 用户: admin"
    echo "  - 密码: admin123456"
    echo "  - URI: mongodb://admin:admin123456@localhost:27017"
else
    echo -e "${RED}✗ 连接失败${NC}"
fi
echo ""

# 测试 Redis
echo -n "测试 Redis (6379)... "
if nc -zv localhost 6379 2>&1 | grep -q succeeded || nc -zv localhost 6379 2>&1 | grep -q open; then
    echo -e "${GREEN}✓ 连接成功${NC}"
    echo "  - 密码: redis123456"
    if command -v redis-cli &> /dev/null; then
        REDIS_RESPONSE=$(redis-cli -a redis123456 ping 2>/dev/null)
        if [ "$REDIS_RESPONSE" = "PONG" ]; then
            echo "  - Ping测试: ${GREEN}成功${NC}"
        fi
    fi
else
    echo -e "${RED}✗ 连接失败${NC}"
fi
echo ""

# 测试 Memcached
echo -n "测试 Memcached (11211)... "
if nc -zv localhost 11211 2>&1 | grep -q succeeded || nc -zv localhost 11211 2>&1 | grep -q open; then
    echo -e "${GREEN}✓ 连接成功${NC}"
else
    echo -e "${RED}✗ 连接失败${NC}"
fi
echo ""

# 测试 RabbitMQ
echo -n "测试 RabbitMQ (5672)... "
if nc -zv localhost 5672 2>&1 | grep -q succeeded || nc -zv localhost 5672 2>&1 | grep -q open; then
    echo -e "${GREEN}✓ AMQP连接成功${NC}"
    echo "  - 用户: admin"
    echo "  - 密码: admin123456"
else
    echo -e "${RED}✗ AMQP连接失败${NC}"
fi

echo -n "测试 RabbitMQ 管理界面 (15672)... "
if nc -zv localhost 15672 2>&1 | grep -q succeeded || nc -zv localhost 15672 2>&1 | grep -q open; then
    echo -e "${GREEN}✓ 管理界面可访问${NC}"
    echo "  - URL: http://localhost:15672"
else
    echo -e "${RED}✗ 管理界面不可访问${NC}"
fi
echo ""

# 测试 Kafka
echo -n "测试 Kafka (9092)... "
if nc -zv localhost 9092 2>&1 | grep -q succeeded || nc -zv localhost 9092 2>&1 | grep -q open; then
    echo -e "${GREEN}✓ 连接成功${NC}"
else
    echo -e "${RED}✗ 连接失败${NC}"
fi

echo -n "测试 Zookeeper (2181)... "
if nc -zv localhost 2181 2>&1 | grep -q succeeded || nc -zv localhost 2181 2>&1 | grep -q open; then
    echo -e "${GREEN}✓ 连接成功${NC}"
else
    echo -e "${RED}✗ 连接失败${NC}"
fi
echo ""

# 测试 Consul
echo -n "测试 Consul (8500)... "
if nc -zv localhost 8500 2>&1 | grep -q succeeded || nc -zv localhost 8500 2>&1 | grep -q open; then
    echo -e "${GREEN}✓ 连接成功${NC}"
    echo "  - UI: http://localhost:8500"
else
    echo -e "${RED}✗ 连接失败${NC}"
fi
echo ""

# 测试 Etcd
echo -n "测试 Etcd (2379)... "
if nc -zv localhost 2379 2>&1 | grep -q succeeded || nc -zv localhost 2379 2>&1 | grep -q open; then
    echo -e "${GREEN}✓ 连接成功${NC}"
else
    echo -e "${RED}✗ 连接失败${NC}"
fi
echo ""

# 测试 Prometheus
echo -n "测试 Prometheus (9090)... "
if nc -zv localhost 9090 2>&1 | grep -q succeeded || nc -zv localhost 9090 2>&1 | grep -q open; then
    echo -e "${GREEN}✓ 连接成功${NC}"
    echo "  - UI: http://localhost:9090"
else
    echo -e "${RED}✗ 连接失败${NC}"
fi
echo ""

# 测试 Grafana
echo -n "测试 Grafana (3000)... "
if nc -zv localhost 3000 2>&1 | grep -q succeeded || nc -zv localhost 3000 2>&1 | grep -q open; then
    echo -e "${GREEN}✓ 连接成功${NC}"
    echo "  - UI: http://localhost:3000"
    echo "  - 用户: admin"
    echo "  - 密码: admin123456"
else
    echo -e "${RED}✗ 连接失败${NC}"
fi
echo ""

# 测试 Jaeger
echo -n "测试 Jaeger (16686)... "
if nc -zv localhost 16686 2>&1 | grep -q succeeded || nc -zv localhost 16686 2>&1 | grep -q open; then
    echo -e "${GREEN}✓ 连接成功${NC}"
    echo "  - UI: http://localhost:16686"
else
    echo -e "${RED}✗ 连接失败${NC}"
fi
echo ""

echo "========================================="
echo "测试完成"
echo "========================================="
