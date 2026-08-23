package com.dasigolmok.domain.ai.config;

import lombok.Getter;
import lombok.Setter;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@Getter
@Setter
@Component
@ConfigurationProperties(prefix = "app.ai")
public class AiProperties {
    /** Master switch. MVP must remain false — no LLM/RAG/Agent in production path. */
    private boolean enabled = false;
    private String adapter = "disabled";
    private String modelVersion = "none-mvp";
    private String promptVersion = "none-mvp";
    private TagSuggest tagSuggest = new TagSuggest();

    @Getter
    @Setter
    public static class TagSuggest {
        private boolean enabled = false;
    }

    public boolean isTagSuggestEnabled() {
        return enabled && tagSuggest != null && tagSuggest.isEnabled();
    }
}
