CREATE TABLE irae__meta_date AS
with study_period as
(
    select
        min(period_start_day)   as min_date,
        max(period_end_day)     as max_date
    FROM
        irae__cohort_study_period
)
select  min_date,
        LEAST(max_date,     CURRENT_DATE)   as max_date
FROM    study_period;
