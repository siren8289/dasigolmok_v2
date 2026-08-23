package com.dasigolmok.domain.ai.adapter;

import com.dasigolmok.domain.ai.config.AiProperties;
import com.dasigolmok.domain.ai.dto.TagSuggestionResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.context.annotation.Primary;
import org.springframework.stereotype.Component;

import java.util.Optional;

/** MVP default: no LLM/RAG/Agent. Always empty → rule fallback. */
@Primary
@Component
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
}
