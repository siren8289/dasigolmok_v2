package com.dasigolmok.infra.analytics;

import jakarta.persistence.EntityManager;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.context.ApplicationEventPublisher;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;

@Slf4j
@Component
@RequiredArgsConstructor
public class AnalyticsViewRefresher {

    private final EntityManager entityManager;
    private final ApplicationEventPublisher eventPublisher;

    /**
     * Request a refresh after the surrounding write transaction commits.
     * Does not run REFRESH on the caller thread.
     */
    public void refreshAll() {
        eventPublisher.publishEvent(new AnalyticsRefreshRequestedEvent());
    }

    /**
     * Actually refreshes materialized views. Invoked asynchronously after commit.
     */
    @Transactional
    public void executeRefresh() {
        log.debug("Refreshing analytics materialized views");
        entityManager.createNativeQuery(
                "REFRESH MATERIALIZED VIEW CONCURRENTLY mv_region_story_stats"
        ).executeUpdate();
        entityManager.createNativeQuery(
                "REFRESH MATERIALIZED VIEW CONCURRENTLY mv_story_curation_summary"
        ).executeUpdate();
        log.debug("Analytics materialized views refreshed");
    }
}
