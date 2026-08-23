package com.dasigolmok.domain.area.repository;

import com.dasigolmok.domain.area.dto.AreaContextResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
@RequiredArgsConstructor
public class AreaContextQueryRepository {

    private final JdbcTemplate jdbcTemplate;

    public Optional<AreaContextResponse> findByPlaceId(String placeId) {
        String sql = """
                SELECT m.area_code, m.area_name, m.area_type_name, m.base_period,
                       m.store_count_total, m.open_rate_avg, m.close_rate_avg,
                       m.monthly_sales_total, m.sales_is_estimate, m.area_mapping_version,
                       m.source_name, m.source_dataset, m.source_url, m.license_type,
                       m.fetched_at
                FROM place_area_mappings pam
                JOIN mart_area_context m ON m.area_code = pam.area_code
                WHERE pam.place_id = ?
                """;
        List<AreaContextResponse> rows = jdbcTemplate.query(sql, (rs, rowNum) -> {
            String basePeriod = rs.getString("base_period");
            String sourceName = rs.getString("source_name");
            String license = rs.getString("license_type");
            return AreaContextResponse.builder()
                    .areaCode(rs.getString("area_code"))
                    .areaName(rs.getString("area_name"))
                    .areaTypeName(rs.getString("area_type_name"))
                    .basePeriod(basePeriod)
                    .storeCountTotal((Integer) rs.getObject("store_count_total"))
                    .openRateAvg(rs.getObject("open_rate_avg") != null ? rs.getDouble("open_rate_avg") : null)
                    .closeRateAvg(rs.getObject("close_rate_avg") != null ? rs.getDouble("close_rate_avg") : null)
                    .monthlySalesTotal(rs.getObject("monthly_sales_total") != null ? rs.getLong("monthly_sales_total") : null)
                    .salesIsEstimate(rs.getBoolean("sales_is_estimate"))
                    .areaMappingVersion(rs.getString("area_mapping_version"))
                    .sourceName(sourceName)
                    .sourceDataset(rs.getString("source_dataset"))
                    .sourceUrl(rs.getString("source_url"))
                    .licenseType(license)
                    .fetchedAt(rs.getTimestamp("fetched_at") != null
                            ? rs.getTimestamp("fetched_at").toInstant().toString() : null)
                    .attribution(String.format(
                            "출처: %s · 데이터 기준일: %s · %s (Context only, 추정값 포함 가능)",
                            sourceName, basePeriod, license))
                    .build();
        }, placeId);
        return rows.stream().findFirst();
    }
}
