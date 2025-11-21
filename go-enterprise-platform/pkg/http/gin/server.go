package gin

import (
	"context"
	"fmt"
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/prometheus/client_golang/prometheus/promhttp"
)

// Config HTTP服务配置
type Config struct {
	Host         string
	Port         int
	ReadTimeout  time.Duration
	WriteTimeout time.Duration
	Mode         string // debug, release, test
}

// Server HTTP服务器
type Server struct {
	engine *gin.Engine
	server *http.Server
	config Config
}

// NewServer 创建HTTP服务器
func NewServer(cfg Config) *Server {
	if cfg.Mode != "" {
		gin.SetMode(cfg.Mode)
	} else {
		gin.SetMode(gin.ReleaseMode)
	}

	engine := gin.New()

	// 全局中间件
	engine.Use(gin.Logger())
	engine.Use(gin.Recovery())
	engine.Use(CORS())

	// 健康检查接口
	engine.GET("/health", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"status": "ok",
			"time":   time.Now().Unix(),
		})
	})

	// Prometheus metrics 接口
	engine.GET("/metrics", gin.WrapH(promhttp.Handler()))

	addr := fmt.Sprintf("%s:%d", cfg.Host, cfg.Port)
	server := &http.Server{
		Addr:         addr,
		Handler:      engine,
		ReadTimeout:  cfg.ReadTimeout,
		WriteTimeout: cfg.WriteTimeout,
	}

	return &Server{
		engine: engine,
		server: server,
		config: cfg,
	}
}

// GetEngine 获取Gin引擎
func (s *Server) GetEngine() *gin.Engine {
	return s.engine
}

// Start 启动服务器
func (s *Server) Start() error {
	return s.server.ListenAndServe()
}

// Shutdown 优雅关闭服务器
func (s *Server) Shutdown(ctx context.Context) error {
	return s.server.Shutdown(ctx)
}

// CORS 跨域中间件
func CORS() gin.HandlerFunc {
	return func(c *gin.Context) {
		c.Writer.Header().Set("Access-Control-Allow-Origin", "*")
		c.Writer.Header().Set("Access-Control-Allow-Credentials", "true")
		c.Writer.Header().Set("Access-Control-Allow-Headers", "Content-Type, Content-Length, Authorization, Accept, X-Requested-With")
		c.Writer.Header().Set("Access-Control-Allow-Methods", "POST, OPTIONS, GET, PUT, DELETE")

		if c.Request.Method == "OPTIONS" {
			c.AbortWithStatus(http.StatusNoContent)
			return
		}

		c.Next()
	}
}
