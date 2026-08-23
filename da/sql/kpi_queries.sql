-- Reference KPI queries (formula_version = v1)

-- map_to_detail
-- SELECT
--   (SELECT COUNT(*) FROM fact_user_engagement WHERE event_name='story_detail_view' AND source='map')::float
--   / NULLIF((SELECT COUNT(*) FROM fact_user_engagement WHERE event_name='map_view'), 0);

-- area_context_coverage
-- SELECT
--   COUNT(*) FILTER (WHERE has_area_context)::float / NULLIF(COUNT(*), 0)
-- FROM fact_story_lifecycle f
-- JOIN dim_status s ON s.status_sk = f.status_sk
-- WHERE s.status_code = 'APPROVED';

-- area engagement association (not causal)
-- SELECT has_area_context, COUNT(*) AS eng_events
-- FROM fact_user_engagement
-- WHERE event_name IN ('like_toggle','share','story_detail_view')
-- GROUP BY has_area_context;
