package com.dasigolmok.domain.ai.adapter;

import com.dasigolmok.domain.ai.dto.ClassifySuggestionResponse;
import com.dasigolmok.domain.ai.dto.CurationCandidateResponse;
import com.dasigolmok.domain.ai.dto.SummarySuggestionResponse;
import com.dasigolmok.domain.ai.dto.TagSuggestionResponse;

import java.util.List;
import java.util.Optional;

/**
 * AI assist seam. Implementations must never auto-approve/reject/publish content
 * and must not write Story/Review state. Empty Optional → caller uses rule fallback.
 */
public interface AiAdapter {

    String name();

    String modelVersion();

    String promptVersion();

    Optional<TagSuggestionResponse> suggestTags(String title, String description);

    Optional<SummarySuggestionResponse> summarize(String title, String description);

    Optional<ClassifySuggestionResponse> classify(String title, String description, String category);

    Optional<CurationCandidateResponse> curationCandidates(List<String> storyIds, List<String> preferTags, int limit);
}
