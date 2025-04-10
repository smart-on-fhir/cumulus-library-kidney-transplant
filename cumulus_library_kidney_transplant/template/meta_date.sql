CREATE TABLE $prefix__meta_date AS
WITH valid_period AS (
    SELECT DISTINCT
        enc_period_start_day as period_start_day,
        enc_period_end_day as period_end_day
    FROM
        $prefix__cohort_study_population
)
SELECT
    min(period_start_day) AS min_date,
    max(period_end_day) AS max_date
FROM valid_period;