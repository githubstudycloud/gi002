-- 用户数据库初始化脚本
CREATE DATABASE IF NOT EXISTS enterprise_user DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE enterprise_user;

-- 创建用户表
CREATE TABLE IF NOT EXISTS `user` (
  `id` BIGINT(20) NOT NULL AUTO_INCREMENT COMMENT '用户ID',
  `username` VARCHAR(50) NOT NULL COMMENT '用户名',
  `password` VARCHAR(255) NOT NULL COMMENT '密码',
  `nickname` VARCHAR(50) DEFAULT NULL COMMENT '昵称',
  `email` VARCHAR(100) DEFAULT NULL COMMENT '邮箱',
  `mobile` VARCHAR(20) DEFAULT NULL COMMENT '手机号',
  `status` TINYINT(1) DEFAULT '1' COMMENT '状态（0：禁用，1：正常）',
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_username` (`username`),
  KEY `idx_email` (`email`),
  KEY `idx_mobile` (`mobile`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

-- 插入测试数据
INSERT INTO `user` (`username`, `password`, `nickname`, `email`, `mobile`, `status`)
VALUES
('admin', '123456', '管理员', 'admin@example.com', '13800138000', 1),
('user1', '123456', '用户1', 'user1@example.com', '13800138001', 1),
('user2', '123456', '用户2', 'user2@example.com', '13800138002', 1);

-- 创建订单数据库
CREATE DATABASE IF NOT EXISTS enterprise_order DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE enterprise_order;

-- 创建订单表
CREATE TABLE IF NOT EXISTS `order` (
  `id` BIGINT(20) NOT NULL AUTO_INCREMENT COMMENT '订单ID',
  `order_no` VARCHAR(50) NOT NULL COMMENT '订单编号',
  `user_id` BIGINT(20) NOT NULL COMMENT '用户ID',
  `product_name` VARCHAR(200) NOT NULL COMMENT '商品名称',
  `quantity` INT(11) NOT NULL DEFAULT '1' COMMENT '商品数量',
  `amount` DECIMAL(10,2) NOT NULL COMMENT '订单金额',
  `status` TINYINT(1) DEFAULT '0' COMMENT '订单状态（0：待支付，1：已支付，2：已取消）',
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_order_no` (`order_no`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_create_time` (`create_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='订单表';

-- 插入测试订单数据
INSERT INTO `order` (`order_no`, `user_id`, `product_name`, `quantity`, `amount`, `status`)
VALUES
('ORD20240101001', 1, '商品A', 2, 199.98, 1),
('ORD20240101002', 2, '商品B', 1, 99.99, 0),
('ORD20240101003', 1, '商品C', 3, 299.97, 1);
