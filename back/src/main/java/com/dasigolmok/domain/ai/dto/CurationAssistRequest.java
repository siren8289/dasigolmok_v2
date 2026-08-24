package com.dasigolmok.domain.ai.dto;

import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotEmpty;
import lombok.Getter;
import lombok.Setter;

import java.util.ArrayList;
import java.util.List;

@Getter
@Setter
public class CurationAssistRequest {
    @NotEmpty
    private List<String> storyIds = new ArrayList<>();
    private List<String> preferTags = new ArrayList<>();
    @Min(1)
    @Max(50)
    private int limit = 10;
}
