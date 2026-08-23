package com.dasigolmok.infra.analytics;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.task.TaskExecutor;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;

@Configuration
@EnableAsync
public class AnalyticsAsyncConfig {

    public static final String ANALYTICS_REFRESH_EXECUTOR = "analyticsRefreshExecutor";

    /**
     * Single-thread executor so REFRESH MATERIALIZED VIEW CONCURRENTLY
     * runs serially (PostgreSQL allows only one concurrent refresh per view).
     */
    @Bean(name = ANALYTICS_REFRESH_EXECUTOR)
    public TaskExecutor analyticsRefreshExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(1);
        executor.setMaxPoolSize(1);
        executor.setQueueCapacity(1000);
        executor.setThreadNamePrefix("analytics-refresh-");
        executor.initialize();
        return executor;
    }
}
