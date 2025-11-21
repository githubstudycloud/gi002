package memcached

import (
	"fmt"

	"github.com/bradfitz/gomemcache/memcache"
)

// Config Memcached配置
type Config struct {
	Servers []string
}

// Client Memcached客户端
type Client struct {
	client *memcache.Client
}

// NewClient 创建Memcached客户端
func NewClient(cfg Config) (*Client, error) {
	if len(cfg.Servers) == 0 {
		return nil, fmt.Errorf("no memcached servers configured")
	}

	mc := memcache.New(cfg.Servers...)

	// 测试连接
	if err := mc.Ping(); err != nil {
		return nil, fmt.Errorf("failed to ping memcached: %w", err)
	}

	return &Client{client: mc}, nil
}

// Get 获取缓存
func (c *Client) Get(key string) (*memcache.Item, error) {
	return c.client.Get(key)
}

// Set 设置缓存
func (c *Client) Set(item *memcache.Item) error {
	return c.client.Set(item)
}

// Add 添加缓存(仅当key不存在时)
func (c *Client) Add(item *memcache.Item) error {
	return c.client.Add(item)
}

// Replace 替换缓存(仅当key存在时)
func (c *Client) Replace(item *memcache.Item) error {
	return c.client.Replace(item)
}

// Delete 删除缓存
func (c *Client) Delete(key string) error {
	return c.client.Delete(key)
}

// DeleteAll 清空所有缓存
func (c *Client) DeleteAll() error {
	return c.client.DeleteAll()
}

// Increment 递增
func (c *Client) Increment(key string, delta uint64) (uint64, error) {
	return c.client.Increment(key, delta)
}

// Decrement 递减
func (c *Client) Decrement(key string, delta uint64) (uint64, error) {
	return c.client.Decrement(key, delta)
}

// GetClient 获取原生客户端
func (c *Client) GetClient() *memcache.Client {
	return c.client
}
