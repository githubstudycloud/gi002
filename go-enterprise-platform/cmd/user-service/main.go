package main

import (
	"context"
	"fmt"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/yourname/go-enterprise-platform/internal/user/handler"
	"github.com/yourname/go-enterprise-platform/internal/user/model"
	"github.com/yourname/go-enterprise-platform/internal/user/repository"
	"github.com/yourname/go-enterprise-platform/internal/user/service"
	"github.com/yourname/go-enterprise-platform/pkg/config"
	"github.com/yourname/go-enterprise-platform/pkg/database/mysql"
	ginserver "github.com/yourname/go-enterprise-platform/pkg/http/gin"
	"github.com/yourname/go-enterprise-platform/pkg/logger"
	"go.uber.org/zap"
	"gorm.io/gorm/logger"
)

func main() {
	// 加载配置
	cfg, err := config.Load("config/config-dev.yaml")
	if err != nil {
		panic(fmt.Sprintf("failed to load config: %v", err))
	}

	// 初始化日志
	if err := logger.Init(logger.Config{
		Level:      cfg.Log.Level,
		Format:     cfg.Log.Format,
		OutputPath: cfg.Log.OutputPath,
	}); err != nil {
		panic(fmt.Sprintf("failed to init logger: %v", err))
	}
	defer logger.Sync()

	logger.Info("Starting user service", zap.String("version", cfg.App.Version))

	// 初始化数据库
	db, err := mysql.NewClient(mysql.Config{
		Host:            cfg.Database.MySQL.Host,
		Port:            cfg.Database.MySQL.Port,
		Username:        cfg.Database.MySQL.Username,
		Password:        cfg.Database.MySQL.Password,
		Database:        cfg.Database.MySQL.Database,
		Charset:         cfg.Database.MySQL.Charset,
		MaxIdleConns:    cfg.Database.MySQL.MaxIdleConns,
		MaxOpenConns:    cfg.Database.MySQL.MaxOpenConns,
		ConnMaxLifetime: cfg.Database.MySQL.ConnMaxLifetime,
		LogLevel:        logger.Info,
	})
	if err != nil {
		logger.Fatal("Failed to connect to MySQL", zap.Error(err))
	}
	logger.Info("Connected to MySQL successfully")

	// 自动迁移数据库表
	if err := db.AutoMigrate(&model.User{}); err != nil {
		logger.Fatal("Failed to migrate database", zap.Error(err))
	}
	logger.Info("Database migration completed")

	// 初始化仓库、服务和处理器
	userRepo := repository.NewUserRepository(db)
	userService := service.NewUserService(userRepo)
	userHandler := handler.NewUserHandler(userService)

	// 创建HTTP服务器
	httpCfg := ginserver.Config{
		Host:         cfg.Server.HTTP.Host,
		Port:         8081, // 用户服务端口
		ReadTimeout:  cfg.Server.HTTP.ReadTimeout,
		WriteTimeout: cfg.Server.HTTP.WriteTimeout,
		Mode:         "debug",
	}
	server := ginserver.NewServer(httpCfg)

	// 注册路由
	api := server.GetEngine().Group("/api/v1")
	userHandler.RegisterRoutes(api)

	// 启动HTTP服务器
	go func() {
		logger.Info("Starting HTTP server", zap.Int("port", 8081))
		if err := server.Start(); err != nil {
			logger.Fatal("Failed to start HTTP server", zap.Error(err))
		}
	}()

	// 优雅关闭
	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit

	logger.Info("Shutting down server...")

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	if err := server.Shutdown(ctx); err != nil {
		logger.Error("Server forced to shutdown", zap.Error(err))
	}

	logger.Info("Server exited")
}
