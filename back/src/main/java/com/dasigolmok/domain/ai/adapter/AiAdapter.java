package com.dasigolmok.domain.ai.adapter;

import com.dasigolmok.domain.ai.dto.TagSuggestionResponse;

import java.util.Optional;

/**
 * Future AI adapter seam. Implementations must never auto-approve/reject/publish content.
 * MVP uses {@link DisabledAiAdapter} and always falls back to deterministic rules.
 */
public interface AiAdapter {

    String name();

    String modelVersion();

    String promptVersion();

    /**
     * Optional tag suggestions. Empty means caller must use non-AI baseline.
     * Only APPROVED or draft-in-progress text should be considered; PENDING must not train models.
     */
    Optional<TagSuggestionResponse> suggestTags(String title, String description);
}
