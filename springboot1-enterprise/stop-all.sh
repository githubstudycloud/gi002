#!/bin/bash

echo "======================================"
echo "停止所有服务"
echo "======================================"

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# 停止 Spring Boot 服务
stop_service() {
    SERVICE_NAME=$1
    PID_FILE="logs/${SERVICE_NAME}.pid"

    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p $PID > /dev/null 2>&1; then
            echo -e "${YELLOW}停止 ${SERVICE_NAME}... (PID: ${PID})${NC}"
            kill -15 $PID
            sleep 2

            # 如果进程还在，强制杀死
            if ps -p $PID > /dev/null 2>&1; then
                echo -e "${RED}强制停止 ${SERVICE_NAME}${NC}"
                kill -9 $PID
            fi

            rm -f "$PID_FILE"
            echo -e "${GREEN}${SERVICE_NAME} 已停止${NC}"
        else
            echo -e "${YELLOW}${SERVICE_NAME} 未运行${NC}"
            rm -f "$PID_FILE"
        fi
    else
        echo -e "${YELLOW}未找到 ${SERVICE_NAME} 的 PID 文件${NC}"
    fi
}

# 按顺序停止服务（与启动顺序相反）
echo -e "\n${YELLOW}停止业务服务...${NC}"
stop_service "order-service"
stop_service "user-service"

echo -e "\n${YELLOW}停止基础服务...${NC}"
stop_service "admin"
stop_service "gateway"
stop_service "config"
stop_service "eureka"

# 询问是否停止中间件
echo -e "\n${YELLOW}是否停止中间件（MySQL、Redis、RabbitMQ）？ (y/n)${NC}"
read -r STOP_MIDDLEWARE

if [ "$STOP_MIDDLEWARE" = "y" ] || [ "$STOP_MIDDLEWARE" = "Y" ]; then
    echo -e "${YELLOW}停止中间件...${NC}"
    cd docker
    docker-compose down
    cd ..
    echo -e "${GREEN}中间件已停止${NC}"
else
    echo -e "${YELLOW}保持中间件运行${NC}"
fi

echo -e "\n${GREEN}======================================"
echo "所有服务已停止！"
echo "======================================${NC}"
