create table $prefix__cohort_casedef_rx as
select  distinct
        enc_period_start_day,
        age_at_visit,
        'casedef_rx'            as valueset,
        medicationrequest_ref   as resource_ref,
        subject_ref,
        encounter_ref,
        casedef.*
from    $prefix__casedef           as casedef,
        $prefix__cohort_study_population_rx as studypop
where   casedef.system  = rx_system
and     casedef.code    = rx_code
;
