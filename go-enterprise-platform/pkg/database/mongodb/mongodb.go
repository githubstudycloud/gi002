package mongodb

import (
	"context"
	"fmt"
	"time"

	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

// Config MongoDB配置
type Config struct {
	URI      string
	Database string
	Timeout  time.Duration
}

// Client MongoDB客户端
type Client struct {
	client   *mongo.Client
	database *mongo.Database
}

// NewClient 创建MongoDB客户端
func NewClient(cfg Config) (*Client, error) {
	ctx, cancel := context.WithTimeout(context.Background(), cfg.Timeout)
	defer cancel()

	clientOpts := options.Client().ApplyURI(cfg.URI)
	client, err := mongo.Connect(ctx, clientOpts)
	if err != nil {
		return nil, fmt.Errorf("failed to connect to mongodb: %w", err)
	}

	// 测试连接
	if err := client.Ping(ctx, nil); err != nil {
		return nil, fmt.Errorf("failed to ping mongodb: %w", err)
	}

	return &Client{
		client:   client,
		database: client.Database(cfg.Database),
	}, nil
}

// GetDatabase 获取数据库
func (c *Client) GetDatabase() *mongo.Database {
	return c.database
}

// GetCollection 获取集合
func (c *Client) GetCollection(name string) *mongo.Collection {
	return c.database.Collection(name)
}

// Close 关闭连接
func (c *Client) Close(ctx context.Context) error {
	return c.client.Disconnect(ctx)
}
