package com.dasigolmok.domain.ai.adapter;

import com.dasigolmok.domain.ai.config.AiProperties;
import com.dasigolmok.domain.ai.dto.ClassifySuggestionResponse;
import com.dasigolmok.domain.ai.dto.CurationCandidateResponse;
import com.dasigolmok.domain.ai.dto.SummarySuggestionResponse;
import com.dasigolmok.domain.ai.dto.TagSuggestionResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.stereotype.Component;

import java.util.List;
import java.util.Optional;

/** MVP / default: no remote AI. Always empty → rule fallback. */
@Component
@ConditionalOnProperty(name = "app.ai.adapter", havingValue = "disabled", matchIfMissing = true)
@RequiredArgsConstructor
public class DisabledAiAdapter implements AiAdapter {

    private final AiProperties aiProperties;

    @Override
    public String name() {
        return "disabled";
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
        return Optional.empty();
    }

    @Override
    public Optional<SummarySuggestionResponse> summarize(String title, String description) {
        return Optional.empty();
    }

    @Override
    public Optional<ClassifySuggestionResponse> classify(String title, String description, String category) {
        return Optional.empty();
    }

    @Override
    public Optional<CurationCandidateResponse> curationCandidates(
            List<String> storyIds, List<String> preferTags, int limit) {
        return Optional.empty();
    }
}
