package com.dasigolmok.recommend.service;

import com.dasigolmok.ai.AiClient;
import com.dasigolmok.recommend.dto.RecommendRequest;
import com.fasterxml.jackson.databind.JsonNode;
import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.Map;

/**
 * 메인 기능 2: 같은 동의 업종 추천
 * AI 서버가 업종별 점수를 계산하고, 이 서비스는 결과를 그대로 전달한다.
 */
@Service
public class RecommendService {

    private final AiClient aiClient;

    public RecommendService(AiClient aiClient) {
        this.aiClient = aiClient;
    }

    public JsonNode recommend(RecommendRequest request) {
        Map<String, Object> body = new HashMap<>();
        body.put("district", request.getDistrict());
        body.put("dong", request.getDong());
        return aiClient.recommend(body);
    }
}
