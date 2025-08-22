create table irae__cohort_casedef_doc as
select  distinct
        enc_period_start_day,
        age_at_visit,
        'casedef_doc'           as valueset,
        documentreference_ref   as resource_ref,
        subject_ref,
        encounter_ref,
        casedef.*
from    irae__casedef           as casedef,
        irae__cohort_study_population_doc as studypop
where   casedef.system  = doc_type_system
and     casedef.code    = doc_type_code
;