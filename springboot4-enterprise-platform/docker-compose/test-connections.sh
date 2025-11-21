#!/bin/bash

echo "=========================================="
echo "Testing Middleware Connections"
echo "=========================================="

# Test MySQL
echo ""
echo "Testing MySQL..."
docker exec enterprise-mysql mysql -uroot -ppassword -e "SELECT VERSION();" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✓ MySQL connection successful"
    docker exec enterprise-mysql mysql -uroot -ppassword -e "SHOW DATABASES;" 2>/dev/null | grep user_db
    if [ $? -eq 0 ]; then
        echo "✓ Database 'user_db' exists"
    fi
else
    echo "✗ MySQL connection failed"
fi

# Test PostgreSQL
echo ""
echo "Testing PostgreSQL..."
docker exec enterprise-postgres psql -U postgres -c "SELECT version();" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✓ PostgreSQL connection successful"
    docker exec enterprise-postgres psql -U postgres -c "\l" 2>/dev/null | grep user_db
    if [ $? -eq 0 ]; then
        echo "✓ Database 'user_db' exists"
    fi
else
    echo "✗ PostgreSQL connection failed"
fi

# Test Redis
echo ""
echo "Testing Redis..."
REDIS_RESPONSE=$(docker exec enterprise-redis redis-cli PING 2>/dev/null)
if [ "$REDIS_RESPONSE" = "PONG" ]; then
    echo "✓ Redis connection successful"
    docker exec enterprise-redis redis-cli INFO SERVER | grep redis_version
    docker exec enterprise-redis redis-cli SET test_key "Hello from Enterprise Platform"
    REDIS_VALUE=$(docker exec enterprise-redis redis-cli GET test_key)
    echo "✓ Test write/read: $REDIS_VALUE"
    docker exec enterprise-redis redis-cli DEL test_key
else
    echo "✗ Redis connection failed"
fi

# Test RabbitMQ
echo ""
echo "Testing RabbitMQ..."
RABBITMQ_STATUS=$(docker exec enterprise-rabbitmq rabbitmqctl status 2>/dev/null | grep "RabbitMQ version")
if [ $? -eq 0 ]; then
    echo "✓ RabbitMQ connection successful"
    echo "$RABBITMQ_STATUS"
    echo "Management UI: http://localhost:15672"
    echo "Credentials: admin/password"
else
    echo "✗ RabbitMQ connection failed"
fi

# Test Kafka
echo ""
echo "Testing Kafka..."
if docker exec enterprise-kafka kafka-broker-api-versions.sh --bootstrap-server localhost:9092 &> /dev/null; then
    echo "✓ Kafka connection successful"
    echo "Creating test topic..."
    docker exec enterprise-kafka kafka-topics.sh --create --topic test-topic --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1 2>/dev/null
    echo "Listing topics..."
    docker exec enterprise-kafka kafka-topics.sh --list --bootstrap-server localhost:9092 2>/dev/null
else
    echo "✗ Kafka connection failed"
fi

# Test Prometheus
echo ""
echo "Testing Prometheus..."
PROM_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:9090/-/healthy)
if [ "$PROM_RESPONSE" = "200" ]; then
    echo "✓ Prometheus is healthy"
    echo "URL: http://localhost:9090"
else
    echo "✗ Prometheus connection failed"
fi

# Test Grafana
echo ""
echo "Testing Grafana..."
GRAFANA_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/api/health)
if [ "$GRAFANA_RESPONSE" = "200" ]; then
    echo "✓ Grafana is healthy"
    echo "URL: http://localhost:3000"
    echo "Credentials: admin/admin"
else
    echo "✗ Grafana connection failed"
fi

echo ""
echo "=========================================="
echo "Connection tests completed!"
echo "=========================================="
