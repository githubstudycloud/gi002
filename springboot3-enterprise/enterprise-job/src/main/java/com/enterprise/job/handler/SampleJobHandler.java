package com.enterprise.job.handler;

import com.xxl.job.core.context.XxlJobHelper;
import com.xxl.job.core.handler.annotation.XxlJob;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

/**
 * 示例任务处理器 (XXL-JOB)
 */
@Slf4j
@Component
public class SampleJobHandler {

    /**
     * 简单任务示例
     */
    @XxlJob("sampleJobHandler")
    public void sampleJobHandler() throws Exception {
        XxlJobHelper.log("XXL-JOB, Sample Job Start.");

        // 任务逻辑
        for (int i = 0; i < 5; i++) {
            XxlJobHelper.log("processing... " + i);
            Thread.sleep(1000);
        }

        // 设置任务结果
        XxlJobHelper.handleSuccess("任务执行成功");
    }

    /**
     * 分片任务示例
     */
    @XxlJob("shardingJobHandler")
    public void shardingJobHandler() throws Exception {
        // 获取分片参数
        int shardIndex = XxlJobHelper.getShardIndex();
        int shardTotal = XxlJobHelper.getShardTotal();

        XxlJobHelper.log("分片参数：当前分片序号 = {}, 总分片数 = {}", shardIndex, shardTotal);

        // 业务逻辑
        for (int i = 0; i < shardTotal; i++) {
            if (i % shardTotal == shardIndex) {
                XxlJobHelper.log("第 {} 片, 命中分片开始处理", i);
            }
        }
    }

    /**
     * 命令行任务示例
     */
    @XxlJob("commandJobHandler")
    public void commandJobHandler() throws Exception {
        String command = XxlJobHelper.getJobParam();
        XxlJobHelper.log("Command: " + command);

        // 执行命令逻辑
        XxlJobHelper.handleSuccess("命令执行完成: " + command);
    }
}
