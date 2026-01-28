create TABLE $prefix__cohort_casedef_include as
select  distinct
        $prefix__cohort_casedef_candidate.*
from    $prefix__cohort_casedef_candidate
where   subject_ref not in 
(select  distinct subject_ref from $prefix__cohort_casedef_exclude); 
