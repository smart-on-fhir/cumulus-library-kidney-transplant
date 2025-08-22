create table irae__cohort_casedef_diag as
select  distinct
        enc_period_start_day,
        age_at_visit,
        'casedef_diag'  as valueset,
        result_ref      as resource_ref,
        subject_ref,
        encounter_ref,
        casedef.*
from    irae__casedef   as casedef,
        irae__cohort_study_population_diag as studypop
where   casedef.system  = diag_code_system
and     casedef.code    = diag_code
;