@echo off
chcp 65001 >nul
echo ======================================
echo Spring Boot 1.x 企业级框架启动脚本
echo ======================================

REM 检查 Java 环境
where java >nul 2>nul
if %errorlevel% neq 0 (
    echo 错误: 未找到 Java 环境，请先安装 JDK 1.8+
    pause
    exit /b 1
)

java -version

REM 1. 启动中间件
echo.
echo 步骤 1/7: 启动中间件（MySQL、Redis、RabbitMQ）
cd docker
docker-compose up -d
if %errorlevel% neq 0 (
    echo 中间件启动失败！请检查 Docker 服务是否运行
    pause
    exit /b 1
)
echo 等待中间件启动完成...
timeout /t 10 /nobreak >nul
cd ..

REM 2. 编译项目
echo.
echo 步骤 2/7: 编译项目
call mvn clean package -DskipTests
if %errorlevel% neq 0 (
    echo 编译失败！
    pause
    exit /b 1
)

REM 创建日志目录
if not exist logs mkdir logs

REM 3. 启动 Eureka
echo.
echo 步骤 3/7: 启动 Eureka 注册中心（端口: 18761）
start "Eureka Server" java -jar enterprise-eureka\target\enterprise-eureka-1.0.0-SNAPSHOT.jar
echo 等待 Eureka 启动...
timeout /t 15 /nobreak >nul

REM 4. 启动 Config Server
echo.
echo 步骤 4/7: 启动配置中心（端口: 18888）
start "Config Server" java -jar enterprise-config\target\enterprise-config-1.0.0-SNAPSHOT.jar
echo 等待 Config Server 启动...
timeout /t 10 /nobreak >nul

REM 5. 启动 Gateway
echo.
echo 步骤 5/7: 启动 API 网关（端口: 18080）
start "API Gateway" java -jar enterprise-gateway\target\enterprise-gateway-1.0.0-SNAPSHOT.jar
echo 等待 Gateway 启动...
timeout /t 10 /nobreak >nul

REM 6. 启动 Admin
echo.
echo 步骤 6/7: 启动监控中心（端口: 18090）
start "Admin Server" java -jar enterprise-admin\target\enterprise-admin-1.0.0-SNAPSHOT.jar
echo 等待 Admin 启动...
timeout /t 5 /nobreak >nul

REM 7. 启动业务服务
echo.
echo 步骤 7/7: 启动业务服务
echo 启动用户服务（端口: 18081）
start "User Service" java -jar enterprise-user-service\target\enterprise-user-service-1.0.0-SNAPSHOT.jar
timeout /t 5 /nobreak >nul

echo 启动订单服务（端口: 18082）
start "Order Service" java -jar enterprise-order-service\target\enterprise-order-service-1.0.0-SNAPSHOT.jar

REM 等待服务完全启动
echo.
echo 等待所有服务启动完成...
timeout /t 20 /nobreak >nul

REM 显示服务状态
echo.
echo ======================================
echo 所有服务已启动！
echo ======================================
echo.
echo 服务访问地址：
echo   Eureka:      http://localhost:18761
echo   Config:      http://localhost:18888
echo   Gateway:     http://localhost:18080
echo   Admin:       http://localhost:18090
echo   User API:    http://localhost:18081/swagger-ui.html
echo   Order API:   http://localhost:18082/swagger-ui.html
echo.
echo 中间件访问：
echo   MySQL:       localhost:13306 (root/root123)
echo   Redis:       localhost:16379
echo   RabbitMQ:    http://localhost:15672 (admin/admin123)
echo.
echo 祝你使用愉快！
echo.
pause
