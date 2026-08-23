package com.dasigolmok.domain.ai.dto;

import lombok.Builder;
import lombok.Getter;

import java.util.List;

@Getter
@Builder
public class AiStatusResponse {
    private boolean aiEnabled;
    private String adapter;
    private String modelVersion;
    private String promptVersion;
    private String mvpPolicy;
    private List<FeatureFlagStatus> features;
    private String curationEngine;

    @Getter
    @Builder
    public static class FeatureFlagStatus {
        private String featureKey;
        private boolean enabled;
        private String description;
    }
}
