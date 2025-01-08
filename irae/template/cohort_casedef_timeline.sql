-- Timeline with "sequence of events" (soe) of patients matching case definition
--
create or replace view $prefix__cohort_casedef_timeline as
select 0 as soe, * from $prefix__cohort_casedef_pre
UNION ALL
select 1 as soe, * from $prefix__cohort_casedef_index
UNION ALL
select 2 as soe, * from $prefix__cohort_casedef_post
;