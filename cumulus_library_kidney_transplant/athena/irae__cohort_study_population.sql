create table irae__cohort_study_population as
with StudyPeriodRange as
(
    select distinct encounter_ref, subject_ref
    from    core__encounter as E,
            irae__include_study_period  as Include
    where   (E.period_start_day between Include.period_start and Include.period_end)
    and     (E.period_end_day between Include.period_start and Include.period_end)
),
StudyPeriodHistory as
(
    select distinct E.encounter_ref, E.subject_ref
    from    StudyPeriodRange,
            core__encounter as E,
            irae__include_study_period  as Include
    where   Include.include_history
    and     E.period_start_day < Include.period_end
    and     E.subject_ref = StudyPeriodRange.subject_ref
),
StudyPeriod as
(
    select encounter_ref, subject_ref from StudyPeriodRange
    UNION
    select encounter_ref, subject_ref from StudyPeriodHistory
),
StudyPopulation as
(
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
        E.subject_ref,
        E.encounter_ref
    from
        core__encounter                 as E,
        StudyPeriod                     as SP,
        irae__include_gender            as G,
        irae__include_enc_class         as enc_class,
        irae__include_age_at_visit      as age
    where
        (E.encounter_ref = SP.encounter_ref)  and
        (E.gender = G.code)                   and
        (E.age_at_visit between age.age_min and age.age_max)
        -- https://github.com/smart-on-fhir/cumulus-library-kidney-transplant/issues/28
),
Utilization as
(
    select count(distinct encounter_ref) as cnt_encounter,
            subject_ref
    from    StudyPopulation
    group by subject_ref
),
Duration as
(
    select      min(enc_period_start_day)   as min_start_day,
                max(enc_period_end_day)     as max_end_day,
                subject_ref
    from        StudyPopulation
    group by    subject_ref
),
DateDiff as
(
    select      subject_ref,
                Duration.min_start_day,
                Duration.max_end_day,
                date_diff('day',
                        Duration.min_start_day,
                        Duration.max_end_day) as cnt_days
    from        Duration
)
select  Utilization.cnt_encounter,
        DateDiff.min_start_day,
        DateDiff.max_end_day,
        DateDiff.cnt_days,
        StudyPopulation.*
from    StudyPopulation,
        Utilization,
        DateDiff,
        irae__include_utilization as Include
where   StudyPopulation.subject_ref = Utilization.subject_ref
and     StudyPopulation.subject_ref = DateDiff.subject_ref
and     Include.enc_min <= Utilization.cnt_encounter
and     Include.enc_max >= Utilization.cnt_encounter
and     Include.days_min <= DateDiff.cnt_days
and     Include.days_max >= DateDiff.cnt_days
;
