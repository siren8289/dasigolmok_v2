package com.dasigolmok.infra.analytics;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Component;
import org.springframework.transaction.event.TransactionPhase;
import org.springframework.transaction.event.TransactionalEventListener;

@Slf4j
@Component
@RequiredArgsConstructor
public class AnalyticsRefreshEventListener {

    private final AnalyticsViewRefresher analyticsViewRefresher;

    @Async(AnalyticsAsyncConfig.ANALYTICS_REFRESH_EXECUTOR)
    @TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
    public void onRefreshRequested(AnalyticsRefreshRequestedEvent event) {
        try {
            analyticsViewRefresher.executeRefresh();
        } catch (Exception e) {
            log.error("Failed to refresh analytics materialized views", e);
        }
    }
}
