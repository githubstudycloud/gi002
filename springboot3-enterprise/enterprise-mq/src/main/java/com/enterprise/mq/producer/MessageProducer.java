package com.enterprise.mq.producer;

import com.enterprise.mq.config.RabbitMQConfig;
import com.enterprise.mq.message.BaseMessage;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.stereotype.Component;

/**
 * 消息生产者
 */
@Slf4j
@Component
@RequiredArgsConstructor
public class MessageProducer {

    private final RabbitTemplate rabbitTemplate;

    /**
     * 发送消息到默认队列
     */
    public void sendDefault(BaseMessage message) {
        send(RabbitMQConfig.DIRECT_EXCHANGE, RabbitMQConfig.DEFAULT_ROUTING_KEY, message);
    }

    /**
     * 发送邮件消息
     */
    public void sendEmail(BaseMessage message) {
        send(RabbitMQConfig.TOPIC_EXCHANGE, RabbitMQConfig.EMAIL_ROUTING_KEY, message);
    }

    /**
     * 发送短信消息
     */
    public void sendSms(BaseMessage message) {
        send(RabbitMQConfig.TOPIC_EXCHANGE, RabbitMQConfig.SMS_ROUTING_KEY, message);
    }

    /**
     * 发送消息
     */
    public void send(String exchange, String routingKey, Object message) {
        log.info("Sending message to exchange: {}, routingKey: {}, message: {}",
                exchange, routingKey, message);
        rabbitTemplate.convertAndSend(exchange, routingKey, message);
    }

    /**
     * 发送延迟消息
     */
    public void sendDelay(String exchange, String routingKey, Object message, long delayMs) {
        log.info("Sending delay message to exchange: {}, routingKey: {}, delay: {}ms",
                exchange, routingKey, delayMs);
        rabbitTemplate.convertAndSend(exchange, routingKey, message, msg -> {
            msg.getMessageProperties().setExpiration(String.valueOf(delayMs));
            return msg;
        });
    }
}
