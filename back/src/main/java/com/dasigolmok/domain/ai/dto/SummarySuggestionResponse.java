package com.dasigolmok.domain.ai.dto;

import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
public class SummarySuggestionResponse {
    private String kind;
    private String summary;
    private boolean usedFallback;
    private String engine;
    private String modelVersion;
    private String promptVersion;
    private Double confidence;
    private String disclaimer;
}
