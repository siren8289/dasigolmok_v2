package com.dasigolmok.domain.analytics.dto;

import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
public class AreaEngagementResponse {
    private String areaCode;
    private String areaName;
    private String areaTypeName;
    private String basePeriod;
    private Integer approvedStoryCount;
    private Integer storeCountTotal;
    private Double openRateAvg;
    private Double closeRateAvg;
    private String sourceName;
    private String licenseType;
    private String attribution;
    private String caveat;
}
