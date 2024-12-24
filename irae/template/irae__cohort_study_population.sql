create table irae__cohort_study_population as
with study_period as
(
    select distinct encounter_ref, subject_ref
    from
        core__encounter as E,
        irae__include_study_period  as SP
    where
        (SP.include_history and E.period_start_day < SP.period_end) OR
        (E.period_start_day between SP.period_start and SP.period_end)
)
select distinct
    E.status,
    E.age_at_visit,
    E.gender,
    E.race_display,
    E.ethnicity_display,
    E.class_code          as enc_class_code,
    E.period_start_day    as enc_period_start_day,
    E.period_start_week   as enc_period_start_week,
    E.period_start_month  as enc_period_start_month,
    E.period_start_year   as enc_period_start_year,
    E.period_end_day      as enc_period_end_day,
    E.servicetype_code    as enc_servicetype_code,
    E.servicetype_system  as enc_servicetype_system,
    E.servicetype_display as enc_servicetype_display,
    E.type_code           as enc_type_code,
    E.type_system         as enc_type_system,
    E.type_display        as enc_type_display,
    E.encounter_ref,
    E.subject_ref
from
    core__encounter                 as E,
    study_period                    as SP,
    irae__include_gender            as G,
    irae__include_enc_class         as enc_class,
    irae__include_age_at_visit      as age
where
    (E.encounter_ref = SP.encounter_ref)  and
    (E.class_code = enc_class.code)       and
    (E.gender = G.code)                   and
    (E.age_at_visit between age.age_min and age.age_max)
;

