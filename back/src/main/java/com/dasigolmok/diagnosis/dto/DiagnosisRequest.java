package com.dasigolmok.diagnosis.dto;

import jakarta.validation.constraints.NotBlank;

/**
 * 진단 요청 (프론트 → Spring).
 * 행정동과 업종만 고르면 된다.
 */
public class DiagnosisRequest {

    @NotBlank
    private String district;

    @NotBlank
    private String dong;

    @NotBlank
    private String industry;

    public String getDistrict() { return district; }
    public void setDistrict(String district) { this.district = district; }

    public String getDong() { return dong; }
    public void setDong(String dong) { this.dong = dong; }

    public String getIndustry() { return industry; }
    public void setIndustry(String industry) { this.industry = industry; }
}
