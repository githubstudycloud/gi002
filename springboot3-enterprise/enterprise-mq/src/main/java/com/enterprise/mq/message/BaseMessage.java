package com.enterprise.mq.message;

import lombok.Data;
import lombok.experimental.Accessors;

import java.io.Serializable;
import java.time.LocalDateTime;
import java.util.UUID;

/**
 * 基础消息
 */
@Data
@Accessors(chain = true)
public class BaseMessage implements Serializable {

    private static final long serialVersionUID = 1L;

    /**
     * 消息ID
     */
    private String messageId;

    /**
     * 消息类型
     */
    private String messageType;

    /**
     * 消息内容
     */
    private Object data;

    /**
     * 创建时间
     */
    private LocalDateTime createTime;

    /**
     * 重试次数
     */
    private Integer retryCount = 0;

    public BaseMessage() {
        this.messageId = UUID.randomUUID().toString().replace("-", "");
        this.createTime = LocalDateTime.now();
    }

    public static BaseMessage of(String messageType, Object data) {
        BaseMessage message = new BaseMessage();
        message.setMessageType(messageType);
        message.setData(data);
        return message;
    }
}
