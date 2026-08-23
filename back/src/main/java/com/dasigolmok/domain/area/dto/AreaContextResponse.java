package com.dasigolmok.domain.area.dto;

import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
public class AreaContextResponse {
    private String areaCode;
    private String areaName;
    private String areaTypeName;
    /** e.g. 2024Q1 — display as "데이터 기준일: YYYY-Qn" */
    private String basePeriod;
    private Integer storeCountTotal;
    private Double openRateAvg;
    private Double closeRateAvg;
    private Long monthlySalesTotal;
    private Boolean salesIsEstimate;
    private String areaMappingVersion;
    private String sourceName;
    private String sourceDataset;
    private String sourceUrl;
    private String licenseType;
    private String fetchedAt;
    private String attribution;
}
