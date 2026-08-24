package com.dasigolmok.domain.ai.adapter;

import com.dasigolmok.domain.ai.config.AiProperties;
import com.dasigolmok.domain.ai.dto.ClassifySuggestionResponse;
import com.dasigolmok.domain.ai.dto.CurationCandidateResponse;
import com.dasigolmok.domain.ai.dto.SummarySuggestionResponse;
import com.dasigolmok.domain.ai.dto.TagSuggestionResponse;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Getter;
import lombok.RequiredArgsConstructor;
import lombok.Setter;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClient;
import org.springframework.web.client.RestClientException;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.stream.Collectors;

/**
 * HTTP client to FastAPI AI assist service.
 * Failures return empty Optional so callers fall back to deterministic rules.
 */
@Slf4j
@Component
@ConditionalOnProperty(name = "app.ai.adapter", havingValue = "fastapi")
@RequiredArgsConstructor
public class FastApiAiAdapter implements AiAdapter {

    private final AiProperties aiProperties;
    private final RestClient aiRestClient;

    @Override
    public String name() {
        return "fastapi";
    }

    @Override
    public String modelVersion() {
        return aiProperties.getModelVersion();
    }

    @Override
    public String promptVersion() {
        return aiProperties.getPromptVersion();
    }

    @Override
    public Optional<TagSuggestionResponse> suggestTags(String title, String description) {
        try {
            FastTagResponse body = aiRestClient.post()
                    .uri("/v1/analyze/tags")
                    .contentType(MediaType.APPLICATION_JSON)
                    .body(analyzePayload(title, description, null))
                    .retrieve()
                    .body(FastTagResponse.class);
            if (body == null || body.getSuggestions() == null) {
                return Optional.empty();
            }
            List<TagSuggestionResponse.SuggestedTag> tags = body.getSuggestions().stream()
                    .map(s -> TagSuggestionResponse.SuggestedTag.builder()
                            .name(s.getName())
                            .type(s.getType())
                            .rationale(s.getRationale())
                            .build())
                    .collect(Collectors.toList());
            return Optional.of(TagSuggestionResponse.builder()
                    .kind("PROPOSAL_ONLY")
                    .suggestions(tags)
                    .usedFallback(false)
                    .engine(body.getEngine() != null ? body.getEngine() : name())
                    .modelVersion(body.getModelVersion() != null ? body.getModelVersion() : modelVersion())
                    .promptVersion(body.getPromptVersion() != null ? body.getPromptVersion() : promptVersion())
                    .confidence(body.getConfidence())
                    .disclaimer(body.getDisclaimer())
                    .build());
        } catch (RestClientException e) {
            log.warn("FastAPI tag suggest failed: {}", e.getMessage());
            return Optional.empty();
        }
    }

    @Override
    public Optional<SummarySuggestionResponse> summarize(String title, String description) {
        try {
            FastSummaryResponse body = aiRestClient.post()
                    .uri("/v1/analyze/summary")
                    .contentType(MediaType.APPLICATION_JSON)
                    .body(analyzePayload(title, description, null))
                    .retrieve()
                    .body(FastSummaryResponse.class);
            if (body == null || body.getSummary() == null || body.getSummary().isBlank()) {
                return Optional.empty();
            }
            return Optional.of(SummarySuggestionResponse.builder()
                    .kind("PROPOSAL_ONLY")
                    .summary(body.getSummary())
                    .usedFallback(false)
                    .engine(body.getEngine() != null ? body.getEngine() : name())
                    .modelVersion(body.getModelVersion() != null ? body.getModelVersion() : modelVersion())
                    .promptVersion(body.getPromptVersion() != null ? body.getPromptVersion() : promptVersion())
                    .confidence(body.getConfidence())
                    .disclaimer(body.getDisclaimer())
                    .build());
        } catch (RestClientException e) {
            log.warn("FastAPI summary failed: {}", e.getMessage());
            return Optional.empty();
        }
    }

    @Override
    public Optional<ClassifySuggestionResponse> classify(String title, String description, String category) {
        try {
            FastClassifyResponse body = aiRestClient.post()
                    .uri("/v1/analyze/classify")
                    .contentType(MediaType.APPLICATION_JSON)
                    .body(analyzePayload(title, description, category))
                    .retrieve()
                    .body(FastClassifyResponse.class);
            if (body == null || body.getCategory() == null) {
                return Optional.empty();
            }
            return Optional.of(ClassifySuggestionResponse.builder()
                    .kind("PROPOSAL_ONLY")
                    .category(body.getCategory())
                    .periodTag(body.getPeriodTag())
                    .labels(body.getLabels() != null ? body.getLabels() : List.of())
                    .usedFallback(false)
                    .engine(body.getEngine() != null ? body.getEngine() : name())
                    .modelVersion(body.getModelVersion() != null ? body.getModelVersion() : modelVersion())
                    .promptVersion(body.getPromptVersion() != null ? body.getPromptVersion() : promptVersion())
                    .confidence(body.getConfidence())
                    .disclaimer(body.getDisclaimer())
                    .build());
        } catch (RestClientException e) {
            log.warn("FastAPI classify failed: {}", e.getMessage());
            return Optional.empty();
        }
    }

    @Override
    public Optional<CurationCandidateResponse> curationCandidates(
            List<String> storyIds, List<String> preferTags, int limit) {
        try {
            Map<String, Object> payload = new HashMap<>();
            payload.put("story_ids", storyIds != null ? storyIds : List.of());
            payload.put("prefer_tags", preferTags != null ? preferTags : List.of());
            payload.put("limit", limit);
            FastCurationResponse body = aiRestClient.post()
                    .uri("/v1/curation/candidates")
                    .contentType(MediaType.APPLICATION_JSON)
                    .body(payload)
                    .retrieve()
                    .body(FastCurationResponse.class);
            if (body == null || body.getCandidates() == null) {
                return Optional.empty();
            }
            List<CurationCandidateResponse.Candidate> candidates = body.getCandidates().stream()
                    .map(c -> CurationCandidateResponse.Candidate.builder()
                            .storyId(c.getStoryId())
                            .score(c.getScore())
                            .reason(c.getReason())
                            .build())
                    .collect(Collectors.toList());
            return Optional.of(CurationCandidateResponse.builder()
                    .kind("PROPOSAL_ONLY")
                    .candidates(candidates)
                    .usedFallback(false)
                    .engine(body.getEngine() != null ? body.getEngine() : name())
                    .modelVersion(body.getModelVersion() != null ? body.getModelVersion() : modelVersion())
                    .promptVersion(body.getPromptVersion() != null ? body.getPromptVersion() : promptVersion())
                    .disclaimer(body.getDisclaimer())
                    .build());
        } catch (RestClientException e) {
            log.warn("FastAPI curation candidates failed: {}", e.getMessage());
            return Optional.empty();
        }
    }

    private Map<String, Object> analyzePayload(String title, String description, String category) {
        Map<String, Object> payload = new HashMap<>();
        payload.put("title", title);
        payload.put("description", description);
        if (category != null && !category.isBlank()) {
            payload.put("category", category);
        }
        return payload;
    }

    @Getter
    @Setter
    @JsonIgnoreProperties(ignoreUnknown = true)
    static class FastTagResponse {
        private List<FastSuggestedTag> suggestions;
        private Double confidence;
        private String engine;
        @JsonProperty("model_version")
        private String modelVersion;
        @JsonProperty("prompt_version")
        private String promptVersion;
        private String disclaimer;
    }

    @Getter
    @Setter
    @JsonIgnoreProperties(ignoreUnknown = true)
    static class FastSuggestedTag {
        private String name;
        private String type;
        private String rationale;
    }

    @Getter
    @Setter
    @JsonIgnoreProperties(ignoreUnknown = true)
    static class FastSummaryResponse {
        private String summary;
        private Double confidence;
        private String engine;
        @JsonProperty("model_version")
        private String modelVersion;
        @JsonProperty("prompt_version")
        private String promptVersion;
        private String disclaimer;
    }

    @Getter
    @Setter
    @JsonIgnoreProperties(ignoreUnknown = true)
    static class FastClassifyResponse {
        private String category;
        @JsonProperty("period_tag")
        private String periodTag;
        private List<String> labels;
        private Double confidence;
        private String engine;
        @JsonProperty("model_version")
        private String modelVersion;
        @JsonProperty("prompt_version")
        private String promptVersion;
        private String disclaimer;
    }

    @Getter
    @Setter
    @JsonIgnoreProperties(ignoreUnknown = true)
    static class FastCurationResponse {
        private List<FastCandidate> candidates;
        private String engine;
        @JsonProperty("model_version")
        private String modelVersion;
        @JsonProperty("prompt_version")
        private String promptVersion;
        private String disclaimer;
    }

    @Getter
    @Setter
    @JsonIgnoreProperties(ignoreUnknown = true)
    static class FastCandidate {
        @JsonProperty("story_id")
        private String storyId;
        private Double score;
        private String reason;
    }
}
