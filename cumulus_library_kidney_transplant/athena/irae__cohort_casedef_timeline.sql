-- Timeline with "sequence of events" (soe) of patients matching case definition
--
create or replace view irae__cohort_casedef_timeline as
select 0 as period, * from irae__cohort_casedef_pre
UNION
select 1 as period, * from irae__cohort_casedef_index
UNION
select 2 as period, * from irae__cohort_casedef_post
;