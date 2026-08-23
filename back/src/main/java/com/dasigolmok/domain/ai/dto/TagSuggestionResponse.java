package com.dasigolmok.domain.ai.dto;

import lombok.Builder;
import lombok.Getter;

import java.util.List;

@Getter
@Builder
public class TagSuggestionResponse {
    /** Always a suggestion — never an authoritative decision. */
    private String kind;
    private List<SuggestedTag> suggestions;
    private boolean usedFallback;
    private String engine;
    private String modelVersion;
    private String promptVersion;
    private Double confidence;
    private String disclaimer;

    @Getter
    @Builder
    public static class SuggestedTag {
        private String name;
        private String type;
        private String rationale;
    }
}
