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
    /**
     * Master switch. When false, adapters are not consulted and rule fallback is used.
     */
    private boolean enabled = false;
    /** disabled | fastapi */
    private String adapter = "disabled";
    private String modelVersion = "none-mvp";
    private String promptVersion = "none-mvp";
    private String baseUrl = "http://localhost:8000";
    private int connectTimeoutMs = 1000;
    private int readTimeoutMs = 3000;
    private TagSuggest tagSuggest = new TagSuggest();
    private Summary summary = new Summary();
    private Classify classify = new Classify();
    private CurationAssist curationAssist = new CurationAssist();

    @Getter
    @Setter
    public static class TagSuggest {
        private boolean enabled = false;
    }

    @Getter
    @Setter
    public static class Summary {
        private boolean enabled = false;
    }

    @Getter
    @Setter
    public static class Classify {
        private boolean enabled = false;
    }

    @Getter
    @Setter
    public static class CurationAssist {
        private boolean enabled = false;
    }

    public boolean isTagSuggestEnabled() {
        return enabled && tagSuggest != null && tagSuggest.isEnabled();
    }

    public boolean isSummaryEnabled() {
        return enabled && summary != null && summary.isEnabled();
    }

    public boolean isClassifyEnabled() {
        return enabled && classify != null && classify.isEnabled();
    }

    public boolean isCurationAssistEnabled() {
        return enabled && curationAssist != null && curationAssist.isEnabled();
    }
}
