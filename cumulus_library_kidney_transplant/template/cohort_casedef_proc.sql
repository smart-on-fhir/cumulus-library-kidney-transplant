create table $prefix__cohort_casedef_proc as
select  distinct
        enc_period_start_day,
        age_at_visit,
        'casedef_proc'  as valueset,
        procedure_ref   as resource_ref,
        subject_ref,
        encounter_ref,
        casedef.*
from    $prefix__casedef   as casedef,
        $prefix__cohort_study_population_proc as studypop
where   casedef.system  = proc_system
and     casedef.code    = proc_code
;
