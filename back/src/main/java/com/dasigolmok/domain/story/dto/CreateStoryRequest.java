package com.dasigolmok.domain.story.dto;

import jakarta.validation.constraints.AssertTrue;
import jakarta.validation.constraints.DecimalMax;
import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class CreateStoryRequest {
    @NotBlank
    private String title;

    @NotBlank
    private String description;

    private String imageUrl;
    private String locationName;

    @NotNull(message = "위도는 필수입니다.")
    @DecimalMin(value = "-90.0", message = "위도는 -90~90 범위여야 합니다.")
    @DecimalMax(value = "90.0", message = "위도는 -90~90 범위여야 합니다.")
    private Double latitude;

    @NotNull(message = "경도는 필수입니다.")
    @DecimalMin(value = "-180.0", message = "경도는 -180~180 범위여야 합니다.")
    @DecimalMax(value = "180.0", message = "경도는 -180~180 범위여야 합니다.")
    private Double longitude;

    @NotBlank
    private String regionId;

    private String periodTag;
    private String category;
    private String sourceType;
    private Boolean copyrightAgreed;

    @AssertTrue(message = "저작권 동의가 필요합니다.")
    public boolean isCopyrightConsentGiven() {
        return Boolean.TRUE.equals(copyrightAgreed);
    }
}
