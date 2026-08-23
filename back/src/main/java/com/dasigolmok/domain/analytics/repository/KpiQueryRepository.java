package com.dasigolmok.domain.analytics.repository;

import com.dasigolmok.domain.analytics.dto.AreaEngagementResponse;
import com.dasigolmok.domain.analytics.dto.KpiSnapshotResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
@RequiredArgsConstructor
public class KpiQueryRepository {

    private final JdbcTemplate jdbcTemplate;

    public List<KpiSnapshotResponse> findLatestKpis() {
        String sql = """
                SELECT DISTINCT ON (metric_key, grain_label, COALESCE(segment_json, ''))
                       metric_key, grain_label, segment_json, metric_value, numerator, denominator,
                       formula_version, computed_at, notes
                FROM da_kpi_snapshot
                ORDER BY metric_key, grain_label, COALESCE(segment_json, ''), computed_at DESC
                """;
        return jdbcTemplate.query(sql, (rs, i) -> KpiSnapshotResponse.builder()
                .metricKey(rs.getString("metric_key"))
                .grainLabel(rs.getString("grain_label"))
                .segmentJson(rs.getString("segment_json"))
                .metricValue(rs.getObject("metric_value") != null ? rs.getDouble("metric_value") : null)
                .numerator(rs.getObject("numerator") != null ? rs.getDouble("numerator") : null)
                .denominator(rs.getObject("denominator") != null ? rs.getDouble("denominator") : null)
                .formulaVersion(rs.getString("formula_version"))
                .computedAt(rs.getTimestamp("computed_at") != null
                        ? rs.getTimestamp("computed_at").toInstant().toString() : null)
                .notes(rs.getString("notes"))
                .build());
    }

    public List<AreaEngagementResponse> findAreaStoryDensity() {
        String sql = """
                SELECT da.area_code, da.area_name, da.area_type_name, da.base_period,
                       COUNT(f.story_id) AS approved_story_count,
                       fac.store_count_total, fac.open_rate_avg, fac.close_rate_avg,
                       fac.source_name, fac.license_type
                FROM fact_story_lifecycle f
                JOIN dim_area da ON da.area_sk = f.area_sk
                JOIN fact_area_context_snapshot fac ON fac.area_code = da.area_code
                JOIN dim_status s ON s.status_sk = f.status_sk AND s.status_code = 'APPROVED'
                GROUP BY da.area_code, da.area_name, da.area_type_name, da.base_period,
                         fac.store_count_total, fac.open_rate_avg, fac.close_rate_avg,
                         fac.source_name, fac.license_type
                ORDER BY approved_story_count DESC
                """;
        return jdbcTemplate.query(sql, (rs, i) -> {
            String source = rs.getString("source_name");
            String period = rs.getString("base_period");
            String license = rs.getString("license_type");
            return AreaEngagementResponse.builder()
                    .areaCode(rs.getString("area_code"))
                    .areaName(rs.getString("area_name"))
                    .areaTypeName(rs.getString("area_type_name"))
                    .basePeriod(period)
                    .approvedStoryCount(rs.getInt("approved_story_count"))
                    .storeCountTotal((Integer) rs.getObject("store_count_total"))
                    .openRateAvg(rs.getObject("open_rate_avg") != null ? rs.getDouble("open_rate_avg") : null)
                    .closeRateAvg(rs.getObject("close_rate_avg") != null ? rs.getDouble("close_rate_avg") : null)
                    .sourceName(source)
                    .licenseType(license)
                    .attribution(String.format("출처: %s · 데이터 기준일: %s · %s", source, period, license))
                    .caveat("스토리 밀도와 상권 지표의 연관만 관찰하며 인과를 단정하지 않습니다.")
                    .build();
        });
    }
}
