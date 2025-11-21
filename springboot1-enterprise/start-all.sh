#!/bin/bash

echo "======================================"
echo "Spring Boot 1.x 企业级框架启动脚本"
echo "======================================"

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 检查 Java 环境
if ! command -v java &> /dev/null; then
    echo -e "${RED}错误: 未找到 Java 环境，请先安装 JDK 1.8+${NC}"
    exit 1
fi

JAVA_VERSION=$(java -version 2>&1 | awk -F '"' '/version/ {print $2}')
echo -e "${GREEN}Java 版本: ${JAVA_VERSION}${NC}"

# 检查 Maven
if ! command -v mvn &> /dev/null; then
    echo -e "${RED}错误: 未找到 Maven，请先安装 Maven 3.3+${NC}"
    exit 1
fi

# 1. 启动中间件
echo -e "\n${YELLOW}步骤 1/7: 启动中间件（MySQL、Redis、RabbitMQ）${NC}"
cd docker
if docker-compose ps | grep -q "Up"; then
    echo -e "${GREEN}中间件已在运行${NC}"
else
    docker-compose up -d
    echo -e "${GREEN}等待中间件启动完成...${NC}"
    sleep 10
fi
cd ..

# 2. 编译项目
echo -e "\n${YELLOW}步骤 2/7: 编译项目${NC}"
mvn clean package -DskipTests
if [ $? -ne 0 ]; then
    echo -e "${RED}编译失败！${NC}"
    exit 1
fi

# 3. 启动 Eureka
echo -e "\n${YELLOW}步骤 3/7: 启动 Eureka 注册中心（端口: 18761）${NC}"
cd enterprise-eureka
nohup java -jar target/enterprise-eureka-1.0.0-SNAPSHOT.jar > ../logs/eureka.log 2>&1 &
echo $! > ../logs/eureka.pid
echo -e "${GREEN}Eureka 启动中... PID: $(cat ../logs/eureka.pid)${NC}"
sleep 15
cd ..

# 4. 启动 Config Server
echo -e "\n${YELLOW}步骤 4/7: 启动配置中心（端口: 18888）${NC}"
cd enterprise-config
nohup java -jar target/enterprise-config-1.0.0-SNAPSHOT.jar > ../logs/config.log 2>&1 &
echo $! > ../logs/config.pid
echo -e "${GREEN}Config Server 启动中... PID: $(cat ../logs/config.pid)${NC}"
sleep 10
cd ..

# 5. 启动 Gateway
echo -e "\n${YELLOW}步骤 5/7: 启动 API 网关（端口: 18080）${NC}"
cd enterprise-gateway
nohup java -jar target/enterprise-gateway-1.0.0-SNAPSHOT.jar > ../logs/gateway.log 2>&1 &
echo $! > ../logs/gateway.pid
echo -e "${GREEN}Gateway 启动中... PID: $(cat ../logs/gateway.pid)${NC}"
sleep 10
cd ..

# 6. 启动 Admin
echo -e "\n${YELLOW}步骤 6/7: 启动监控中心（端口: 18090）${NC}"
cd enterprise-admin
nohup java -jar target/enterprise-admin-1.0.0-SNAPSHOT.jar > ../logs/admin.log 2>&1 &
echo $! > ../logs/admin.pid
echo -e "${GREEN}Admin 启动中... PID: $(cat ../logs/admin.pid)${NC}"
sleep 5
cd ..

# 7. 启动业务服务
echo -e "\n${YELLOW}步骤 7/7: 启动业务服务${NC}"

echo "启动用户服务（端口: 18081）"
cd enterprise-user-service
nohup java -jar target/enterprise-user-service-1.0.0-SNAPSHOT.jar > ../logs/user-service.log 2>&1 &
echo $! > ../logs/user-service.pid
echo -e "${GREEN}User Service 启动中... PID: $(cat ../logs/user-service.pid)${NC}"
cd ..

sleep 5

echo "启动订单服务（端口: 18082）"
cd enterprise-order-service
nohup java -jar target/enterprise-order-service-1.0.0-SNAPSHOT.jar > ../logs/order-service.log 2>&1 &
echo $! > ../logs/order-service.pid
echo -e "${GREEN}Order Service 启动中... PID: $(cat ../logs/order-service.pid)${NC}"
cd ..

# 等待服务完全启动
echo -e "\n${YELLOW}等待所有服务启动完成...${NC}"
sleep 20

# 显示服务状态
echo -e "\n${GREEN}======================================"
echo "所有服务已启动！"
echo "======================================${NC}"
echo ""
echo "服务访问地址："
echo "  Eureka:      http://localhost:18761"
echo "  Config:      http://localhost:18888"
echo "  Gateway:     http://localhost:18080"
echo "  Admin:       http://localhost:18090"
echo "  User API:    http://localhost:18081/swagger-ui.html"
echo "  Order API:   http://localhost:18082/swagger-ui.html"
echo ""
echo "中间件访问："
echo "  MySQL:       localhost:13306 (root/root123)"
echo "  Redis:       localhost:16379"
echo "  RabbitMQ:    http://localhost:15672 (admin/admin123)"
echo ""
echo "查看日志："
echo "  tail -f logs/*.log"
echo ""
echo "停止服务："
echo "  ./stop-all.sh"
echo ""
echo -e "${GREEN}祝你使用愉快！${NC}"
