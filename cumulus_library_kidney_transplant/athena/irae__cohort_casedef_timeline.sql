-- Timeline with "sequence of events" (soe) of patients matching case definition
--
create or replace view irae__cohort_casedef_timeline as
select 'pre'   as casedef_period, studyvars.*
from    irae__cohort_casedef_pre as casedef,
        irae__cohort_study_variables_timeline as studyvars
where   casedef.encounter_ref = studyvars.encounter_ref
UNION ALL
select 'index' as casedef_period, studyvars.*
from    irae__cohort_casedef_index as casedef,
        irae__cohort_study_variables_timeline as studyvars
where   casedef.encounter_ref = studyvars.encounter_ref
UNION ALL
select 'post'  as casedef_period, studyvars.*
from    irae__cohort_casedef_post as casedef,
        irae__cohort_study_variables_timeline as studyvars
where   casedef.encounter_ref = studyvars.encounter_ref
;