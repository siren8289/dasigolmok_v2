package com.dasigolmok.domain.ai.dto;

import lombok.Builder;
import lombok.Getter;

import java.util.List;

@Getter
@Builder
public class ClassifySuggestionResponse {
    private String kind;
    private String category;
    private String periodTag;
    private List<String> labels;
    private boolean usedFallback;
    private String engine;
    private String modelVersion;
    private String promptVersion;
    private Double confidence;
    private String disclaimer;
}
