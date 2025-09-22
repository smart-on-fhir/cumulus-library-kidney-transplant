create table $prefix__cohort_study_population as
WITH
StudyPopulation as
(
    select  distinct
            E.status,
            E.age_at_visit,
            E.gender,
            E.race_display,
            E.ethnicity_display,
            SP.period_ordinal       as enc_period_ordinal,
            E.period_start_day      as enc_period_start_day,
            E.period_start_week     as enc_period_start_week,
            E.period_start_month    as enc_period_start_month,
            E.period_start_year     as enc_period_start_year,
            E.period_end_day        as enc_period_end_day,
            E.class_code            as enc_class_code,
            E.servicetype_code      as enc_servicetype_code,
            E.servicetype_system    as enc_servicetype_system,
            E.servicetype_display   as enc_servicetype_display,
            E.type_code             as enc_type_code,
            E.type_system           as enc_type_system,
            E.type_display          as enc_type_display,
            E.subject_ref,
            E.encounter_ref
    from    core__encounter                 as E,
            $prefix__cohort_study_period       as SP,
            $prefix__include_gender            as G,
            $prefix__include_age_at_visit      as age
    where   (E.encounter_ref = SP.encounter_ref)  and
            (E.gender = G.code)                   and
            (E.age_at_visit between age.age_min and age.age_max)
),
Utilization as
(
    select  count(distinct enc_period_ordinal) as cnt_period,
            subject_ref
    from    StudyPopulation
    group by subject_ref
),
Duration as
(
    select  min(enc_period_start_day)   as min_start_day,
            max(enc_period_end_day)     as max_end_day,
            subject_ref
    from    StudyPopulation
    group by subject_ref
),
DateDiff as
(
    select  subject_ref,
            Duration.min_start_day,
            Duration.max_end_day,
            date_diff('day',
            Duration.min_start_day,
            Duration.max_end_day) as cnt_days
    from    Duration
)
select  StudyPopulation.*
from    StudyPopulation,
        Utilization,
        DateDiff,
        $prefix__include_utilization as Include
where   StudyPopulation.subject_ref = Utilization.subject_ref
and     StudyPopulation.subject_ref = DateDiff.subject_ref
and     Utilization.cnt_period      between Include.enc_min  and Include.enc_max
and     DateDiff.cnt_days           between Include.days_min and Include.days_max
;
