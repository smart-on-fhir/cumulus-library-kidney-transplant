create  table irae__cohort_casedef_rx as
select  distinct
        casedef.days_since,
        casedef.ordinal_since,
        casedef.dx_category_code,
        casedef.dx_system,
        casedef.dx_code,
        casedef.dx_display,
        rx.*
from    irae__cohort_casedef as casedef,
        irae__cohort_study_population_rx as rx
where   casedef.encounter_ref = rx.encounter_ref
;