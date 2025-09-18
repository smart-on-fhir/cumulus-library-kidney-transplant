-- Timeline with "sequence of events" (soe) of patients matching case definition
--
create or replace view $prefix__cohort_casedef_timeline as
select 0 as period_int, 'pre'   as period, * from $prefix__cohort_casedef_pre
UNION ALL
select 1 as period_int, 'index' as period, * from $prefix__cohort_casedef_index
UNION ALL
select 2 as period_int, 'post'  as period, * from $prefix__cohort_casedef_post
;