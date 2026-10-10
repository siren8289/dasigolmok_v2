package com.dasigolmok.recommend.dto;

import jakarta.validation.constraints.NotBlank;

/** 업종 추천 요청. 행정동만 고르면 된다. */
public class RecommendRequest {

    @NotBlank
    private String district;

    @NotBlank
    private String dong;

    public String getDistrict() { return district; }
    public void setDistrict(String district) { this.district = district; }

    public String getDong() { return dong; }
    public void setDong(String dong) { this.dong = dong; }
}
