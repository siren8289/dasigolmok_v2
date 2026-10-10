package com.dasigolmok.recommend.controller;

import com.dasigolmok.ai.AiClient;
import com.dasigolmok.recommend.dto.RecommendRequest;
import com.dasigolmok.recommend.service.RecommendService;
import com.fasterxml.jackson.databind.JsonNode;
import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * GET  /api/options           자치구·행정동·업종 목록
 * POST /api/recommendations   같은 동의 업종 추천
 */
@RestController
@RequestMapping("/api")
public class RecommendController {

    private final RecommendService recommendService;
    private final AiClient aiClient;

    public RecommendController(RecommendService recommendService, AiClient aiClient) {
        this.recommendService = recommendService;
        this.aiClient = aiClient;
    }

    @GetMapping("/options")
    public JsonNode options() {
        return aiClient.options();
    }

    @PostMapping("/recommendations")
    public JsonNode recommend(@Valid @RequestBody RecommendRequest request) {
        return recommendService.recommend(request);
    }
}
