package com.enterprise.mq.config;

import org.springframework.amqp.core.*;
import org.springframework.amqp.rabbit.config.SimpleRabbitListenerContainerFactory;
import org.springframework.amqp.rabbit.connection.ConnectionFactory;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.amqp.support.converter.Jackson2JsonMessageConverter;
import org.springframework.amqp.support.converter.MessageConverter;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * RabbitMQ配置类
 */
@Configuration
public class RabbitMQConfig {

    // ==================== 交换机名称 ====================
    public static final String DIRECT_EXCHANGE = "enterprise.direct.exchange";
    public static final String TOPIC_EXCHANGE = "enterprise.topic.exchange";
    public static final String FANOUT_EXCHANGE = "enterprise.fanout.exchange";
    public static final String DEAD_LETTER_EXCHANGE = "enterprise.dlx.exchange";

    // ==================== 队列名称 ====================
    public static final String DEFAULT_QUEUE = "enterprise.default.queue";
    public static final String EMAIL_QUEUE = "enterprise.email.queue";
    public static final String SMS_QUEUE = "enterprise.sms.queue";
    public static final String DEAD_LETTER_QUEUE = "enterprise.dlx.queue";

    // ==================== 路由键 ====================
    public static final String DEFAULT_ROUTING_KEY = "enterprise.default";
    public static final String EMAIL_ROUTING_KEY = "enterprise.email";
    public static final String SMS_ROUTING_KEY = "enterprise.sms";

    /**
     * 消息转换器 - JSON
     */
    @Bean
    public MessageConverter messageConverter() {
        return new Jackson2JsonMessageConverter();
    }

    /**
     * RabbitTemplate配置
     */
    @Bean
    public RabbitTemplate rabbitTemplate(ConnectionFactory connectionFactory) {
        RabbitTemplate template = new RabbitTemplate(connectionFactory);
        template.setMessageConverter(messageConverter());
        // 开启强制投递
        template.setMandatory(true);
        // 发布确认回调
        template.setConfirmCallback((correlationData, ack, cause) -> {
            if (!ack) {
                // 记录日志或处理失败
            }
        });
        // 消息返回回调
        template.setReturnsCallback(returned -> {
            // 处理无法路由的消息
        });
        return template;
    }

    /**
     * 监听器容器工厂
     */
    @Bean
    public SimpleRabbitListenerContainerFactory rabbitListenerContainerFactory(ConnectionFactory connectionFactory) {
        SimpleRabbitListenerContainerFactory factory = new SimpleRabbitListenerContainerFactory();
        factory.setConnectionFactory(connectionFactory);
        factory.setMessageConverter(messageConverter());
        // 确认模式：手动确认
        factory.setAcknowledgeMode(AcknowledgeMode.MANUAL);
        // 并发消费者数量
        factory.setConcurrentConsumers(3);
        factory.setMaxConcurrentConsumers(10);
        // 预取数量
        factory.setPrefetchCount(1);
        return factory;
    }

    // ==================== Direct Exchange ====================

    @Bean
    public DirectExchange directExchange() {
        return ExchangeBuilder.directExchange(DIRECT_EXCHANGE)
                .durable(true)
                .build();
    }

    @Bean
    public Queue defaultQueue() {
        return QueueBuilder.durable(DEFAULT_QUEUE)
                .deadLetterExchange(DEAD_LETTER_EXCHANGE)
                .deadLetterRoutingKey(DEFAULT_ROUTING_KEY)
                .build();
    }

    @Bean
    public Binding defaultBinding() {
        return BindingBuilder.bind(defaultQueue())
                .to(directExchange())
                .with(DEFAULT_ROUTING_KEY);
    }

    // ==================== Topic Exchange ====================

    @Bean
    public TopicExchange topicExchange() {
        return ExchangeBuilder.topicExchange(TOPIC_EXCHANGE)
                .durable(true)
                .build();
    }

    @Bean
    public Queue emailQueue() {
        return QueueBuilder.durable(EMAIL_QUEUE).build();
    }

    @Bean
    public Queue smsQueue() {
        return QueueBuilder.durable(SMS_QUEUE).build();
    }

    @Bean
    public Binding emailBinding() {
        return BindingBuilder.bind(emailQueue())
                .to(topicExchange())
                .with(EMAIL_ROUTING_KEY);
    }

    @Bean
    public Binding smsBinding() {
        return BindingBuilder.bind(smsQueue())
                .to(topicExchange())
                .with(SMS_ROUTING_KEY);
    }

    // ==================== Dead Letter Exchange ====================

    @Bean
    public DirectExchange deadLetterExchange() {
        return ExchangeBuilder.directExchange(DEAD_LETTER_EXCHANGE)
                .durable(true)
                .build();
    }

    @Bean
    public Queue deadLetterQueue() {
        return QueueBuilder.durable(DEAD_LETTER_QUEUE).build();
    }

    @Bean
    public Binding deadLetterBinding() {
        return BindingBuilder.bind(deadLetterQueue())
                .to(deadLetterExchange())
                .with(DEFAULT_ROUTING_KEY);
    }
}
