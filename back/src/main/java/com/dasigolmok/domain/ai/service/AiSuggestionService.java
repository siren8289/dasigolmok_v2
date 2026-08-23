package com.dasigolmok.domain.ai.service;

import com.dasigolmok.domain.ai.adapter.AiAdapter;
import com.dasigolmok.domain.ai.config.AiProperties;
import com.dasigolmok.domain.ai.dto.AiStatusResponse;
import com.dasigolmok.domain.ai.dto.TagSuggestionResponse;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Service;

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.util.HexFormat;
import java.util.List;
import java.util.UUID;

@Slf4j
@Service
@RequiredArgsConstructor
public class AiSuggestionService {

    private final AiProperties aiProperties;
    private final AiAdapter aiAdapter;
    private final RuleBasedTagSuggester ruleBasedTagSuggester;
    private final JdbcTemplate jdbcTemplate;
    private final ObjectMapper objectMapper;

    public AiStatusResponse status() {
        List<AiStatusResponse.FeatureFlagStatus> features = List.of(
                flag("tag_suggest", aiProperties.isTagSuggestEnabled(),
                        "스토리 태그 자동 제안. MVP OFF — 규칙 fallback."),
                flag("similar_place", false, "유사 장소/시대 추천. MVP OFF."),
                flag("summary_card", false, "요약 카드(LLM). MVP OFF."),
                flag("safety_prefilter", false, "사전 필터. 최종 결정은 관리자. MVP OFF.")
        );
        return AiStatusResponse.builder()
                .aiEnabled(aiProperties.isEnabled())
                .adapter(aiAdapter.name())
                .modelVersion(aiAdapter.modelVersion())
                .promptVersion(aiAdapter.promptVersion())
                .mvpPolicy("MVP에는 학습 모델·LLM·RAG·Agent·AI 영상 생성이 없습니다. 큐레이션은 결정론적 규칙입니다.")
                .features(features)
                .curationEngine("deterministic_rules")
                .build();
    }

    public TagSuggestionResponse suggestTags(String storyId, String title, String description) {
        TagSuggestionResponse response;
        boolean usedFallback = true;

        if (aiProperties.isTagSuggestEnabled()) {
            try {
                response = aiAdapter.suggestTags(title, description)
                        .map(r -> TagSuggestionResponse.builder()
                                .kind("PROPOSAL_ONLY")
                                .suggestions(r.getSuggestions())
                                .usedFallback(false)
                                .engine(aiAdapter.name())
                                .modelVersion(aiAdapter.modelVersion())
                                .promptVersion(aiAdapter.promptVersion())
                                .confidence(r.getConfidence())
                                .disclaimer("AI 제안입니다. 최종 태그는 사용자가 선택하며 승인/반려/공개를 자동 결정하지 않습니다.")
                                .build())
                        .orElseGet(() -> ruleBasedTagSuggester.suggest(title, description));
                usedFallback = response.isUsedFallback();
            } catch (Exception e) {
                log.warn("AI tag suggest failed — falling back to rules", e);
                response = ruleBasedTagSuggester.suggest(title, description);
                usedFallback = true;
            }
        } else {
            response = ruleBasedTagSuggester.suggest(title, description);
        }

        persistProposalLog(storyId, title, description, response, usedFallback);
        return response;
    }

    private void persistProposalLog(
            String storyId,
            String title,
            String description,
            TagSuggestionResponse response,
            boolean usedFallback) {
        try {
            String json = objectMapper.writeValueAsString(response);
            jdbcTemplate.update("""
                    INSERT INTO ai_proposal_logs (
                      id, feature_key, story_id, proposal_kind, input_hash, output_json,
                      used_fallback, model_version, prompt_version, confidence, status
                    ) VALUES (?, 'tag_suggest', ?, 'tag_suggest', ?, ?, ?, ?, ?, ?, 'PROPOSAL_ONLY')
                    """,
                    UUID.randomUUID().toString(),
                    storyId,
                    sha256(title + "|" + description),
                    json,
                    usedFallback,
                    response.getModelVersion(),
                    response.getPromptVersion(),
                    response.getConfidence());
        } catch (Exception e) {
            log.warn("Failed to persist AI proposal log (non-blocking)", e);
        }
    }

    private AiStatusResponse.FeatureFlagStatus flag(String key, boolean enabled, String description) {
        return AiStatusResponse.FeatureFlagStatus.builder()
                .featureKey(key)
                .enabled(enabled)
                .description(description)
                .build();
    }

    private String sha256(String value) {
        try {
            MessageDigest md = MessageDigest.getInstance("SHA-256");
            return HexFormat.of().formatHex(md.digest(value.getBytes(StandardCharsets.UTF_8)));
        } catch (Exception e) {
            return null;
        }
    }
}
