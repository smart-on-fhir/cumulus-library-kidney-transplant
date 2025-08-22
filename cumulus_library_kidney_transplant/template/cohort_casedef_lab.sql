create table irae__cohort_casedef_lab as
select  distinct
        enc_period_start_day,
        age_at_visit,
        'casedef_lab'   as valueset,
        observation_ref as resource_ref,
        subject_ref,
        encounter_ref,
        casedef.*
from    irae__casedef   as casedef,
        irae__cohort_study_population_lab as studypop
where   casedef.system  = lab_observation_system
and     casedef.code    = lab_observation_code
;
