#!/bin/bash

echo "=========================================="
echo "Spring Boot 4.x Enterprise Platform"
echo "Starting All Middleware Services..."
echo "=========================================="

# Start Docker containers
echo "Starting Docker containers..."
docker-compose up -d

echo ""
echo "Waiting for services to be healthy..."
sleep 10

# Check service status
echo ""
echo "Service Status:"
echo "----------------------------------------"

# MySQL
if docker exec enterprise-mysql mysqladmin ping -h localhost -uroot -ppassword &> /dev/null; then
    echo "✓ MySQL         : Running on port 3306"
else
    echo "✗ MySQL         : Not ready"
fi

# PostgreSQL
if docker exec enterprise-postgres pg_isready -U postgres &> /dev/null; then
    echo "✓ PostgreSQL    : Running on port 5432"
else
    echo "✗ PostgreSQL    : Not ready"
fi

# Redis
if docker exec enterprise-redis redis-cli ping &> /dev/null; then
    echo "✓ Redis         : Running on port 6379"
else
    echo "✗ Redis         : Not ready"
fi

# RabbitMQ
if docker exec enterprise-rabbitmq rabbitmq-diagnostics ping &> /dev/null; then
    echo "✓ RabbitMQ      : Running on port 5672"
    echo "  Management UI : http://localhost:15672 (admin/password)"
else
    echo "✗ RabbitMQ      : Not ready"
fi

# Kafka (simple check)
if docker ps | grep enterprise-kafka | grep -q Up; then
    echo "✓ Kafka         : Running on port 9092"
else
    echo "✗ Kafka         : Not ready"
fi

# Prometheus
if curl -s http://localhost:9090/-/healthy &> /dev/null; then
    echo "✓ Prometheus    : Running on http://localhost:9090"
else
    echo "✗ Prometheus    : Not ready"
fi

# Grafana
if curl -s http://localhost:3000/api/health &> /dev/null; then
    echo "✓ Grafana       : Running on http://localhost:3000 (admin/admin)"
else
    echo "✗ Grafana       : Not ready"
fi

echo "----------------------------------------"
echo ""
echo "All services started!"
echo ""
echo "Next steps:"
echo "1. Build the project: mvn clean install"
echo "2. Run user service: cd platform-services/service-user && mvn spring-boot:run"
echo ""
echo "To stop all services: docker-compose down"
echo "=========================================="
