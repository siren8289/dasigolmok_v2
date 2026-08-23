package com.dasigolmok.domain.ai.service;

import com.dasigolmok.domain.ai.dto.TagSuggestionResponse;
import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Locale;
import java.util.Set;

/**
 * Deterministic keyword rules for tag suggestions (non-AI baseline).
 * Used when AI is disabled or the adapter fails.
 */
@Component
public class RuleBasedTagSuggester {

    public TagSuggestionResponse suggest(String title, String description) {
        String text = ((title == null ? "" : title) + " " + (description == null ? "" : description))
                .toLowerCase(Locale.ROOT);

        Set<String> themes = new LinkedHashSet<>();
        Set<String> periods = new LinkedHashSet<>();

        if (containsAny(text, "시장", "장터", "가게", "상점", "점포")) {
            themes.add("시장");
            themes.add("상점");
        }
        if (containsAny(text, "골목", "거리", "도로", "네온")) {
            themes.add("거리");
        }
        if (containsAny(text, "한옥", "문화", "유산", "공장", "흔적")) {
            themes.add("문화유산");
        }
        if (containsAny(text, "카페", "커피")) {
            themes.add("상점");
        }
        if (containsAny(text, "1970", "70년대", "70s")) {
            periods.add("1970s");
        }
        if (containsAny(text, "1980", "80년대", "80s")) {
            periods.add("1980s");
        }
        if (containsAny(text, "1990", "90년대", "90s")) {
            periods.add("1990s");
        }
        if (containsAny(text, "2000", "00년대", "2000s")) {
            periods.add("2000s");
        }

        if (themes.isEmpty()) {
            themes.add("거리");
        }

        List<TagSuggestionResponse.SuggestedTag> suggestions = new ArrayList<>();
        for (String t : themes) {
            suggestions.add(TagSuggestionResponse.SuggestedTag.builder()
                    .name(t)
                    .type("THEME")
                    .rationale("규칙 기반 키워드 매칭")
                    .build());
        }
        for (String p : periods) {
            suggestions.add(TagSuggestionResponse.SuggestedTag.builder()
                    .name(p)
                    .type("PERIOD")
                    .rationale("규칙 기반 연대 키워드 매칭")
                    .build());
        }

        return TagSuggestionResponse.builder()
                .kind("PROPOSAL_ONLY")
                .suggestions(suggestions)
                .usedFallback(true)
                .engine("deterministic_rules")
                .modelVersion("rule-v1")
                .promptVersion("n/a")
                .confidence(0.55)
                .disclaimer("AI가 아닌 결정론적 규칙 제안입니다. 최종 태그는 사용자가 선택하며, 공개/검수 결정을 자동으로 내리지 않습니다.")
                .build();
    }

    private boolean containsAny(String text, String... keys) {
        for (String k : keys) {
            if (text.contains(k.toLowerCase(Locale.ROOT))) {
                return true;
            }
        }
        return false;
    }
}
