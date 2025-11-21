@echo off
chcp 65001
echo ===============================================
echo   Spring Boot 2.x 企业级框架启动脚本
echo ===============================================
echo.

echo [1/4] 启动网关服务 (端口: 9527)...
start "Enterprise Gateway" cmd /k "cd enterprise-gateway && mvn spring-boot:run"
timeout /t 5 /nobreak >nul

echo [2/4] 启动认证服务 (端口: 9200)...
start "Enterprise Auth" cmd /k "cd enterprise-auth && mvn spring-boot:run"
timeout /t 5 /nobreak >nul

echo [3/4] 启动系统服务 (端口: 9201)...
start "Enterprise System" cmd /k "cd enterprise-modules\system && mvn spring-boot:run"
timeout /t 5 /nobreak >nul

echo.
echo ===============================================
echo   所有服务启动中，请等待...
echo   - 网关服务: http://localhost:9527
echo   - 认证服务: http://localhost:9200
echo   - 系统服务: http://localhost:9201
echo ===============================================
echo.
pause
