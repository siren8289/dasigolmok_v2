package com.dasigolmok.domain.story.dto;

import com.dasigolmok.domain.area.dto.AreaContextResponse;
import lombok.Builder;
import lombok.Getter;

import java.util.List;

@Getter
@Builder
public class StoryDetailResponse {
    private String id;
    private String title;
    private String description;
    private String imageUrl;
    private String thumbnailUrl;
    private String status;
    private String periodTag;
    private String category;
    private String sourceType;
    private Integer likeCount;
    private Boolean liked;
    private String createdAt;
    private StoryCardResponse.CreatedBy createdBy;
    private PlaceDetail place;
    private List<TagItem> tags;
    /** Optional public-data context layer; null when unmapped or DE unavailable. */
    private AreaContextResponse areaContext;

    @Getter
    @Builder
    public static class PlaceDetail {
        private String locationName;
        private Double latitude;
        private Double longitude;
        private StoryCardResponse.RegionSummary region;
    }

    @Getter
    @Builder
    public static class TagItem {
        private TagRef tag;
    }

    @Getter
    @Builder
    public static class TagRef {
        private String name;
    }
}
