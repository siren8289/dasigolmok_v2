package com.dasigolmok.domain.ai.service;

import com.dasigolmok.domain.ai.adapter.AiAdapter;
import com.dasigolmok.domain.ai.config.AiProperties;
import com.dasigolmok.domain.ai.dto.AiStatusResponse;
import com.dasigolmok.domain.ai.dto.ClassifySuggestionResponse;
import com.dasigolmok.domain.ai.dto.CurationCandidateResponse;
import com.dasigolmok.domain.ai.dto.SummarySuggestionResponse;
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
import java.util.Locale;
import java.util.UUID;
import java.util.stream.Collectors;

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
                        "스토리 태그 자동 제안. FastAPI 보조 또는 규칙 fallback."),
                flag("summary_card", aiProperties.isSummaryEnabled(),
                        "요약 카드 제안. 사실 확정·검수 대체 아님."),
                flag("classify", aiProperties.isClassifyEnabled(),
                        "카테고리/시대 분류 후보."),
                flag("curation_assist", aiProperties.isCurationAssistEnabled(),
                        "큐레이션 추천 후보. 실제 노출은 APPROVED+Backend 정책."),
                flag("similar_place", false, "유사 장소/시대 추천. 미구현."),
                flag("safety_prefilter", false, "사전 필터. 최종 결정은 관리자. 미구현.")
        );
        return AiStatusResponse.builder()
                .aiEnabled(aiProperties.isEnabled())
                .adapter(aiAdapter.name())
                .modelVersion(aiAdapter.modelVersion())
                .promptVersion(aiAdapter.promptVersion())
                .mvpPolicy("AI는 분석·태깅·요약·추천 보조만 수행합니다. 공개/반려는 관리자 검수가 결정하며 FastAPI 장애 시 핵심 CRUD는 유지됩니다.")
                .features(features)
                .curationEngine(aiProperties.isCurationAssistEnabled() ? "backend+fastapi_assist" : "deterministic_rules")
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
                                .engine(r.getEngine() != null ? r.getEngine() : aiAdapter.name())
                                .modelVersion(r.getModelVersion() != null ? r.getModelVersion() : aiAdapter.modelVersion())
                                .promptVersion(r.getPromptVersion() != null ? r.getPromptVersion() : aiAdapter.promptVersion())
                                .confidence(r.getConfidence())
                                .disclaimer(r.getDisclaimer() != null ? r.getDisclaimer()
                                        : "AI 제안입니다. 최종 태그는 사용자가 선택하며 승인/반려/공개를 자동 결정하지 않습니다.")
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

        persistProposalLog(storyId, "tag_suggest", title + "|" + description, response, usedFallback,
                response.getModelVersion(), response.getPromptVersion(), response.getConfidence());
        return response;
    }

    public SummarySuggestionResponse summarize(String storyId, String title, String description) {
        SummarySuggestionResponse response;
        boolean usedFallback = true;

        if (aiProperties.isSummaryEnabled()) {
            try {
                response = aiAdapter.summarize(title, description)
                        .orElseGet(() -> ruleSummary(title, description));
                usedFallback = response.isUsedFallback();
            } catch (Exception e) {
                log.warn("AI summary failed — falling back to rules", e);
                response = ruleSummary(title, description);
            }
        } else {
            response = ruleSummary(title, description);
        }

        persistProposalLog(storyId, "summary", title + "|" + description, response, usedFallback,
                response.getModelVersion(), response.getPromptVersion(), response.getConfidence());
        return response;
    }

    public ClassifySuggestionResponse classify(String storyId, String title, String description, String category) {
        ClassifySuggestionResponse response;
        boolean usedFallback = true;

        if (aiProperties.isClassifyEnabled()) {
            try {
                response = aiAdapter.classify(title, description, category)
                        .orElseGet(() -> ruleClassify(title, description, category));
                usedFallback = response.isUsedFallback();
            } catch (Exception e) {
                log.warn("AI classify failed — falling back to rules", e);
                response = ruleClassify(title, description, category);
            }
        } else {
            response = ruleClassify(title, description, category);
        }

        persistProposalLog(storyId, "classify", title + "|" + description, response, usedFallback,
                response.getModelVersion(), response.getPromptVersion(), response.getConfidence());
        return response;
    }

    public CurationCandidateResponse curationCandidates(List<String> storyIds, List<String> preferTags, int limit) {
        CurationCandidateResponse response;
        boolean usedFallback = true;

        if (aiProperties.isCurationAssistEnabled()) {
            try {
                response = aiAdapter.curationCandidates(storyIds, preferTags, limit)
                        .orElseGet(() -> ruleCuration(storyIds, limit));
                usedFallback = response.isUsedFallback();
            } catch (Exception e) {
                log.warn("AI curation assist failed — falling back to passthrough", e);
                response = ruleCuration(storyIds, limit);
            }
        } else {
            response = ruleCuration(storyIds, limit);
        }

        persistProposalLog(null, "curation_assist", String.join(",", storyIds), response, usedFallback,
                response.getModelVersion(), response.getPromptVersion(), null);
        return response;
    }

    private SummarySuggestionResponse ruleSummary(String title, String description) {
        String desc = description == null ? "" : description.trim();
        String shortDesc = desc.length() <= 100 ? desc : desc.substring(0, 97) + "...";
        return SummarySuggestionResponse.builder()
                .kind("PROPOSAL_ONLY")
                .summary("「" + title + "」 — " + shortDesc)
                .usedFallback(true)
                .engine("deterministic_rules")
                .modelVersion("rule-v1")
                .promptVersion("n/a")
                .confidence(0.5)
                .disclaimer("규칙 기반 요약입니다. 역사적 사실을 확정하지 않으며 관리자 검수를 대체하지 않습니다.")
                .build();
    }

    private ClassifySuggestionResponse ruleClassify(String title, String description, String category) {
        String text = ((title == null ? "" : title) + " " + (description == null ? "" : description))
                .toLowerCase(Locale.ROOT);
        String resolved = (category != null && !category.isBlank()) ? category : "거리";
        if (category == null || category.isBlank()) {
            if (text.contains("시장") || text.contains("상점")) {
                resolved = "상점";
            } else if (text.contains("학교")) {
                resolved = "학교";
            } else if (text.contains("한옥") || text.contains("유산")) {
                resolved = "문화유산";
            }
        }
        String period = null;
        if (text.contains("1970") || text.contains("70년대")) {
            period = "1970s";
        } else if (text.contains("1980") || text.contains("80년대")) {
            period = "1980s";
        } else if (text.contains("1990") || text.contains("90년대")) {
            period = "1990s";
        }
        return ClassifySuggestionResponse.builder()
                .kind("PROPOSAL_ONLY")
                .category(resolved)
                .periodTag(period)
                .labels(List.of(resolved))
                .usedFallback(true)
                .engine("deterministic_rules")
                .modelVersion("rule-v1")
                .promptVersion("n/a")
                .confidence(0.55)
                .disclaimer("규칙 기반 분류 후보입니다. 최종 공개는 관리자 검수가 결정합니다.")
                .build();
    }

    private CurationCandidateResponse ruleCuration(List<String> storyIds, int limit) {
        List<CurationCandidateResponse.Candidate> candidates = storyIds.stream()
                .limit(limit)
                .map(id -> CurationCandidateResponse.Candidate.builder()
                        .storyId(id)
                        .score(0.5)
                        .reason("passthrough — Backend가 APPROVED만 노출해야 함")
                        .build())
                .collect(Collectors.toList());
        return CurationCandidateResponse.builder()
                .kind("PROPOSAL_ONLY")
                .candidates(candidates)
                .usedFallback(true)
                .engine("deterministic_rules")
                .modelVersion("rule-v1")
                .promptVersion("n/a")
                .disclaimer("AI 미사용 passthrough입니다. 실제 노출은 Backend 정책을 따릅니다.")
                .build();
    }

    private void persistProposalLog(
            String storyId,
            String featureKey,
            String input,
            Object response,
            boolean usedFallback,
            String modelVersion,
            String promptVersion,
            Double confidence) {
        try {
            String json = objectMapper.writeValueAsString(response);
            jdbcTemplate.update("""
                    INSERT INTO ai_proposal_logs (
                      id, feature_key, story_id, proposal_kind, input_hash, output_json,
                      used_fallback, model_version, prompt_version, confidence, status
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'PROPOSAL_ONLY')
                    """,
                    UUID.randomUUID().toString(),
                    featureKey,
                    storyId,
                    featureKey,
                    sha256(input),
                    json,
                    usedFallback,
                    modelVersion,
                    promptVersion,
                    confidence);
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
