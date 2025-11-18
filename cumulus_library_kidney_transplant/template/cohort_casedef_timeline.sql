-- Timeline with "sequence of events" (soe) of patients matching case definition
--
create or replace view $prefix__cohort_casedef_timeline as
select 'pre'   as casedef_period, studyvars.*
from    $prefix__cohort_casedef_pre as casedef,
        $prefix__cohort_study_variables_timeline as studyvars
where   casedef.encounter_ref = studyvars.encounter_ref
UNION ALL
select 'index' as casedef_period, studyvars.*
from    $prefix__cohort_casedef_index as casedef,
        $prefix__cohort_study_variables_timeline as studyvars
where   casedef.encounter_ref = studyvars.encounter_ref
UNION ALL
select 'post'  as casedef_period, studyvars.*
from    $prefix__cohort_casedef_post as casedef,
        $prefix__cohort_study_variables_timeline as studyvars
where   casedef.encounter_ref = studyvars.encounter_ref
;