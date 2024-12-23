create table irae__cohort_study_population_dx as
select distinct
    DX.category_code    as dx_category_code,
    DX.code             as dx_code,
    DX.code_display     as dx_code_display,
    DX.system           as dx_system,
    DX.condition_ref    as condition_ref,
    study_population.*
from
    irae__cohort_study_population as study_population
left join core__condition as DX
    on DX.encounter_ref = study_population.encounter_ref
;
