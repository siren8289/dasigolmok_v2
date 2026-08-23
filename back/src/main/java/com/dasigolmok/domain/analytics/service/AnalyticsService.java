package com.dasigolmok.domain.analytics.service;

import com.dasigolmok.domain.analytics.dto.AreaEngagementResponse;
import com.dasigolmok.domain.analytics.dto.KpiSnapshotResponse;
import com.dasigolmok.domain.analytics.dto.RegionStatsResponse;
import com.dasigolmok.domain.analytics.repository.KpiQueryRepository;
import com.dasigolmok.domain.analytics.repository.RegionStatsQueryRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
@RequiredArgsConstructor
public class AnalyticsService {

    private final RegionStatsQueryRepository regionStatsQueryRepository;
    private final KpiQueryRepository kpiQueryRepository;

    @Transactional(readOnly = true)
    public List<RegionStatsResponse> getRegionStats() {
        return regionStatsQueryRepository.findAllRegionStats();
    }

    @Transactional(readOnly = true)
    public List<KpiSnapshotResponse> getLatestKpis() {
        return kpiQueryRepository.findLatestKpis();
    }

    @Transactional(readOnly = true)
    public List<AreaEngagementResponse> getAreaStoryDensity() {
        return kpiQueryRepository.findAreaStoryDensity();
    }
}
