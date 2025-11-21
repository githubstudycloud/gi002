@echo off
echo ==========================================
echo Spring Boot 4.x Enterprise Platform
echo Starting All Middleware Services...
echo ==========================================

echo Starting Docker containers...
docker-compose up -d

echo.
echo Waiting for services to be healthy...
timeout /t 10 /nobreak >nul

echo.
echo Service Status:
echo ----------------------------------------

REM MySQL
docker exec enterprise-mysql mysqladmin ping -h localhost -uroot -ppassword >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] MySQL         : Running on port 3306
) else (
    echo [FAIL] MySQL       : Not ready
)

REM PostgreSQL
docker exec enterprise-postgres pg_isready -U postgres >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] PostgreSQL    : Running on port 5432
) else (
    echo [FAIL] PostgreSQL  : Not ready
)

REM Redis
docker exec enterprise-redis redis-cli ping >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Redis         : Running on port 6379
) else (
    echo [FAIL] Redis       : Not ready
)

REM RabbitMQ
docker exec enterprise-rabbitmq rabbitmq-diagnostics ping >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] RabbitMQ      : Running on port 5672
    echo      Management UI : http://localhost:15672 ^(admin/password^)
) else (
    echo [FAIL] RabbitMQ    : Not ready
)

REM Kafka
docker ps | findstr enterprise-kafka | findstr Up >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Kafka         : Running on port 9092
) else (
    echo [FAIL] Kafka       : Not ready
)

REM Prometheus
curl -s http://localhost:9090/-/healthy >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Prometheus    : Running on http://localhost:9090
) else (
    echo [FAIL] Prometheus  : Not ready
)

REM Grafana
curl -s http://localhost:3000/api/health >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Grafana       : Running on http://localhost:3000 ^(admin/admin^)
) else (
    echo [FAIL] Grafana     : Not ready
)

echo ----------------------------------------
echo.
echo All services started!
echo.
echo Next steps:
echo 1. Build the project: mvn clean install
echo 2. Run user service: cd platform-services\service-user ^&^& mvn spring-boot:run
echo.
echo To stop all services: docker-compose down
echo ==========================================
pause
