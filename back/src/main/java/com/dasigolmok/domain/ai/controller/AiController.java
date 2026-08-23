package com.dasigolmok.domain.ai.controller;

import com.dasigolmok.domain.ai.dto.AiStatusResponse;
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
}
