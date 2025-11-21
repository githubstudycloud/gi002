.PHONY: help install test lint format clean docker-up docker-down init-db run-user-service

# 默认目标
help:
	@echo "Python Enterprise Platform - 可用命令:"
	@echo ""
	@echo "  make install          - 安装所有依赖"
	@echo "  make test            - 运行所有测试"
	@echo "  make test-cov        - 运行测试并生成覆盖率报告"
	@echo "  make lint            - 运行代码检查"
	@echo "  make format          - 格式化代码"
	@echo "  make docker-up       - 启动所有Docker服务"
	@echo "  make docker-down     - 停止所有Docker服务"
	@echo "  make docker-logs     - 查看Docker日志"
	@echo "  make init-db         - 初始化数据库"
	@echo "  make run-user        - 运行用户服务"
	@echo "  make clean           - 清理临时文件"
	@echo "  make clean-all       - 清理所有生成文件和Docker数据"
	@echo ""

# 安装依赖
install:
	@echo "安装依赖..."
	pip install -r requirements.txt

# 使用poetry安装
install-poetry:
	@echo "使用Poetry安装依赖..."
	poetry install

# 运行测试
test:
	@echo "运行测试..."
	pytest tests/ -v

# 运行测试并生成覆盖率报告
test-cov:
	@echo "运行测试并生成覆盖率报告..."
	pytest tests/ -v --cov=. --cov-report=html --cov-report=term

# 代码检查
lint:
	@echo "运行代码检查..."
	flake8 core-framework services --max-line-length=100
	mypy core-framework services --ignore-missing-imports

# 格式化代码
format:
	@echo "格式化代码..."
	black core-framework services tests --line-length=100
	isort core-framework services tests --profile black

# 启动Docker服务
docker-up:
	@echo "启动Docker服务..."
	docker-compose up -d

# 启动基础设施服务
docker-up-infra:
	@echo "启动基础设施服务..."
	docker-compose up -d postgres redis mongodb rabbitmq elasticsearch

# 停止Docker服务
docker-down:
	@echo "停止Docker服务..."
	docker-compose down

# 查看Docker日志
docker-logs:
	@echo "查看Docker日志..."
	docker-compose logs -f

# 查看服务状态
docker-ps:
	@echo "服务状态:"
	docker-compose ps

# 初始化数据库
init-db:
	@echo "初始化数据库..."
	python scripts/init-db.py

# 运行用户服务
run-user:
	@echo "运行用户服务..."
	cd services/user-service && python main.py

# 清理Python临时文件
clean:
	@echo "清理临时文件..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.db" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf build/
	rm -rf dist/

# 清理所有(包括Docker数据)
clean-all: clean
	@echo "清理Docker数据..."
	docker-compose down -v
	rm -rf logs/

# 重启所有服务
restart: docker-down docker-up
	@echo "服务重启完成"

# 构建Docker镜像
docker-build:
	@echo "构建Docker镜像..."
	docker-compose build

# 查看用户服务日志
logs-user:
	@echo "用户服务日志:"
	docker-compose logs -f user-service

# 进入PostgreSQL
psql:
	@echo "连接PostgreSQL..."
	docker-compose exec postgres psql -U postgres -d enterprise_db

# 进入Redis CLI
redis-cli:
	@echo "连接Redis..."
	docker-compose exec redis redis-cli

# 进入MongoDB Shell
mongo:
	@echo "连接MongoDB..."
	docker-compose exec mongodb mongosh -u admin -p admin123

# 完整设置(首次使用)
setup: install docker-up-infra
	@echo "等待服务启动..."
	sleep 30
	@echo "初始化数据库..."
	make init-db
	@echo ""
	@echo "设置完成！可以运行以下命令启动服务:"
	@echo "  make run-user"
	@echo ""
	@echo "或使用Docker运行:"
	@echo "  make docker-up"
