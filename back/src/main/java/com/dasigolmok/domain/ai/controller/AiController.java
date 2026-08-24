package com.dasigolmok.domain.ai.controller;

import com.dasigolmok.domain.ai.dto.AiStatusResponse;
import com.dasigolmok.domain.ai.dto.ClassifySuggestionResponse;
import com.dasigolmok.domain.ai.dto.CurationAssistRequest;
import com.dasigolmok.domain.ai.dto.CurationCandidateResponse;
import com.dasigolmok.domain.ai.dto.StoryAnalyzeRequest;
import com.dasigolmok.domain.ai.dto.SummarySuggestionResponse;
import com.dasigolmok.domain.ai.dto.TagSuggestRequest;
import com.dasigolmok.domain.ai.dto.TagSuggestionResponse;
import com.dasigolmok.domain.ai.service.AiSuggestionService;
import com.dasigolmok.global.response.ApiResponse;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/ai")
@RequiredArgsConstructor
public class AiController {

    private final AiSuggestionService aiSuggestionService;

    @GetMapping("/status")
    public ApiResponse<AiStatusResponse> status() {
        return ApiResponse.ok(aiSuggestionService.status());
    }

    /**
     * Tag suggestions are proposals only. Never writes story status or review decisions.
     */
    @PostMapping("/suggestions/tags")
    public ApiResponse<TagSuggestionResponse> suggestTags(@Valid @RequestBody TagSuggestRequest request) {
        return ApiResponse.ok(
                aiSuggestionService.suggestTags(request.getStoryId(), request.getTitle(), request.getDescription()),
                "태그 제안입니다. 최종 선택은 사용자에게 있습니다.");
    }

    @PostMapping("/suggestions/summary")
    public ApiResponse<SummarySuggestionResponse> summarize(@Valid @RequestBody StoryAnalyzeRequest request) {
        return ApiResponse.ok(
                aiSuggestionService.summarize(request.getStoryId(), request.getTitle(), request.getDescription()),
                "요약 제안입니다. 역사적 사실을 확정하지 않습니다.");
    }

    @PostMapping("/suggestions/classify")
    public ApiResponse<ClassifySuggestionResponse> classify(@Valid @RequestBody StoryAnalyzeRequest request) {
        return ApiResponse.ok(
                aiSuggestionService.classify(
                        request.getStoryId(), request.getTitle(), request.getDescription(), request.getCategory()),
                "분류 후보입니다. 공개/반려는 관리자 검수가 결정합니다.");
    }

    @PostMapping("/suggestions/curation")
    public ApiResponse<CurationCandidateResponse> curation(@Valid @RequestBody CurationAssistRequest request) {
        return ApiResponse.ok(
                aiSuggestionService.curationCandidates(
                        request.getStoryIds(), request.getPreferTags(), request.getLimit()),
                "추천 후보입니다. 실제 노출은 APPROVED 콘텐츠와 Backend 정책을 따릅니다.");
    }
}
