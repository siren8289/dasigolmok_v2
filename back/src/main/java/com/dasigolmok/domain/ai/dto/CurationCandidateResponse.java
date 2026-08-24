package com.dasigolmok.domain.ai.dto;

import lombok.Builder;
import lombok.Getter;

import java.util.List;

@Getter
@Builder
public class CurationCandidateResponse {
    private String kind;
    private List<Candidate> candidates;
    private boolean usedFallback;
    private String engine;
    private String modelVersion;
    private String promptVersion;
    private String disclaimer;

    @Getter
    @Builder
    public static class Candidate {
        private String storyId;
        private Double score;
        private String reason;
    }
}
