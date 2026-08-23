package com.dasigolmok.domain.ai.dto;

import jakarta.validation.constraints.NotBlank;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class TagSuggestRequest {
    private String storyId;
    @NotBlank
    private String title;
    @NotBlank
    private String description;
}
