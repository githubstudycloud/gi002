.PHONY: help build run test clean docker-up docker-down proto

help: ## 显示帮助信息
	@echo "可用命令:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

init: ## 初始化项目依赖
	go mod download
	go mod tidy

build: ## 编译所有服务
	@echo "编译 API Gateway..."
	go build -o bin/api-gateway ./cmd/api-gateway
	@echo "编译 User Service..."
	go build -o bin/user-service ./cmd/user-service
	@echo "编译 Order Service..."
	go build -o bin/order-service ./cmd/order-service

run-gateway: ## 运行 API Gateway
	go run ./cmd/api-gateway/main.go

run-user: ## 运行 User Service
	go run ./cmd/user-service/main.go

run-order: ## 运行 Order Service
	go run ./cmd/order-service/main.go

test: ## 运行测试
	go test -v -race -coverprofile=coverage.txt -covermode=atomic ./...

test-coverage: ## 生成测试覆盖率报告
	go test -v -coverprofile=coverage.out ./...
	go tool cover -html=coverage.out -o coverage.html

lint: ## 代码检查
	golangci-lint run ./...

proto: ## 生成 protobuf 代码
	@echo "生成 protobuf 代码..."
	protoc --go_out=. --go_opt=paths=source_relative \
		--go-grpc_out=. --go-grpc_opt=paths=source_relative \
		api/proto/**/*.proto

docker-up: ## 启动所有中间件服务
	cd deployments/docker && docker-compose up -d

docker-down: ## 停止所有中间件服务
	cd deployments/docker && docker-compose down

docker-logs: ## 查看 Docker 日志
	cd deployments/docker && docker-compose logs -f

docker-ps: ## 查看运行中的容器
	cd deployments/docker && docker-compose ps

clean: ## 清理编译产物
	rm -rf bin/
	rm -f coverage.txt coverage.out coverage.html

deps-update: ## 更新依赖
	go get -u ./...
	go mod tidy

.DEFAULT_GOAL := help
