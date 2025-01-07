create table $prefix__cohort_study_population_lab as
select distinct
    lab.status                      as lab_status,
    observation_code                as lab_observation_code,
    observation_system              as lab_observation_system,
    valuecodeableconcept_code       as lab_concept_code,
    valuecodeableconcept_display    as lab_concept_display,
    valuecodeableconcept_system     as lab_concept_system,
    effectivedatetime_day           as lab_effectivedate,
    observation_ref,
    study_population.*
from
    $prefix__cohort_study_population as study_population,
    core__observation_lab as lab
where
    study_population.encounter_ref = lab.encounter_ref
;