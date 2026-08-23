package com.dasigolmok.domain.analytics.dto;

import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
public class KpiSnapshotResponse {
    private String metricKey;
    private String grainLabel;
    private String segmentJson;
    private Double metricValue;
    private Double numerator;
    private Double denominator;
    private String formulaVersion;
    private String computedAt;
    private String notes;
}
