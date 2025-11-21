#!/bin/bash

echo "======================================"
echo "API 测试脚本"
echo "======================================"

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 基础 URL
GATEWAY_URL="http://localhost:18080/api"
USER_URL="http://localhost:18081"
ORDER_URL="http://localhost:18082"

echo -e "\n${YELLOW}1. 测试用户服务健康检查${NC}"
curl -s ${USER_URL}/user/health | jq '.'

echo -e "\n${YELLOW}2. 测试订单服务健康检查${NC}"
curl -s ${ORDER_URL}/order/health | jq '.'

echo -e "\n${YELLOW}3. 用户登录（获取 Token）${NC}"
LOGIN_RESPONSE=$(curl -s -X POST ${GATEWAY_URL}/user/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "123456"
  }')

echo "$LOGIN_RESPONSE" | jq '.'

# 提取 token
TOKEN=$(echo "$LOGIN_RESPONSE" | jq -r '.data.token')

if [ "$TOKEN" != "null" ] && [ -n "$TOKEN" ]; then
    echo -e "${GREEN}Token 获取成功: ${TOKEN:0:50}...${NC}"
else
    echo -e "\n${YELLOW}注意: Token 为空，跳过需要认证的测试${NC}"
    TOKEN=""
fi

echo -e "\n${YELLOW}4. 通过网关获取用户信息（需要 Token）${NC}"
if [ -n "$TOKEN" ]; then
    curl -s -X GET ${GATEWAY_URL}/user/1 \
      -H "Authorization: ${TOKEN}" | jq '.'
else
    echo "跳过（无 Token）"
fi

echo -e "\n${YELLOW}5. 直接调用用户服务（无需 Token）${NC}"
curl -s -X GET ${USER_URL}/user/1 | jq '.'

echo -e "\n${YELLOW}6. 创建订单（演示服务间调用）${NC}"
if [ -n "$TOKEN" ]; then
    curl -s -X POST ${GATEWAY_URL}/order/create \
      -H "Content-Type: application/json" \
      -H "Authorization: ${TOKEN}" \
      -d '{
        "userId": 1,
        "productName": "测试商品",
        "quantity": 2,
        "amount": 199.99
      }' | jq '.'
else
    echo "跳过（无 Token）"
fi

echo -e "\n${YELLOW}7. 获取订单详情（演示 Feign 调用）${NC}"
if [ -n "$TOKEN" ]; then
    curl -s -X GET ${GATEWAY_URL}/order/1/detail \
      -H "Authorization: ${TOKEN}" | jq '.'
else
    echo "跳过（无 Token）"
fi

echo -e "\n${YELLOW}8. 直接调用订单服务（无需 Token）${NC}"
curl -s -X GET ${ORDER_URL}/order/1 | jq '.'

echo -e "\n${GREEN}======================================"
echo "测试完成！"
echo "======================================${NC}"
echo ""
echo "更多测试："
echo "  - Eureka 控制台: http://localhost:18761"
echo "  - Admin 监控: http://localhost:18090"
echo "  - User API 文档: http://localhost:18081/swagger-ui.html"
echo "  - Order API 文档: http://localhost:18082/swagger-ui.html"
echo ""
