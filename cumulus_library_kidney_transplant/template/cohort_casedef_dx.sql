create table irae__cohort_casedef_dx as
select  distinct
        enc_period_start_day,
        age_at_visit,
        'casedef_dx'    as valueset,
        condition_ref   as resource_ref,
        subject_ref,
        encounter_ref,
        casedef.*
from    irae__casedef   as casedef,
        irae__cohort_study_population_dx as studypop
where   casedef.system  = dx_system
and     casedef.code    = dx_code
;