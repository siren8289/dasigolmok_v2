package com.dasigolmok.ai;

import com.dasigolmok.global.exception.ApiException;
import com.fasterxml.jackson.databind.JsonNode;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;

import java.util.Map;

/**
 * FastAPI(AI 서버) 호출.
 *   GET  /api/v1/options    선택 목록
 *   POST /api/v1/diagnose   골목 상권 진단
 *   POST /api/v1/recommend  업종 추천
 */
@Component
public class AiClient {

    private final RestTemplate restTemplate;
    private final String baseUrl;

    public AiClient(RestTemplate restTemplate, @Value("${app.ai.base-url}") String baseUrl) {
        this.restTemplate = restTemplate;
        this.baseUrl = baseUrl;
    }

    public JsonNode options() {
        try {
            JsonNode response = restTemplate.getForObject(baseUrl + "/api/v1/options", JsonNode.class);
            if (response == null) {
                throw ApiException.aiError("AI 서버 응답이 비어 있습니다.", null);
            }
            return response;
        } catch (RestClientException e) {
            throw ApiException.aiError("AI 서버 호출에 실패했습니다.", e);
        }
    }

    public JsonNode diagnose(Map<String, Object> request) {
        return post("/api/v1/diagnose", request);
    }

    public JsonNode recommend(Map<String, Object> request) {
        return post("/api/v1/recommend", request);
    }

    private JsonNode post(String path, Map<String, Object> request) {
        try {
            JsonNode response = restTemplate.postForObject(baseUrl + path, request, JsonNode.class);
            if (response == null) {
                throw ApiException.aiError("AI 서버 응답이 비어 있습니다.", null);
            }
            return response;
        } catch (RestClientException e) {
            throw ApiException.aiError("AI 서버 호출에 실패했습니다.", e);
        }
    }
}
