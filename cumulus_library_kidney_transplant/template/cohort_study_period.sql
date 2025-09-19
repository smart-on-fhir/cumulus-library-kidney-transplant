CREATE TABLE irae__cohort_study_period as
WITH
StudyPeriodRange as
(
    select  distinct
            E.subject_ref,
            E.period_start_day,
            E.period_end_day,
            E.encounter_ref
    from    core__encounter             as E,
            irae__include_study_period  as Include
    where   (E.period_start_day between Include.period_start and Include.period_end)
    and     (E.period_end_day   between Include.period_start and Include.period_end)
),
StudyPeriodHistory as
(
    SELECT  DISTINCT
            E.subject_ref,
            E.period_start_day,
            E.period_end_day,
            E.encounter_ref
    FROM    core__encounter             as E
    JOIN    irae__include_study_period  as Include
      ON    Include.include_history
     AND    e.period_start_day < Include.period_start
    WHERE   EXISTS  (
            SELECT  1
            FROM    StudyPeriodRange
            WHERE   StudyPeriodRange.subject_ref = E.subject_ref)
),
StudyPeriodUnion as
(
    select  *  from StudyPeriodRange
    UNION ALL
    select  *  from StudyPeriodHistory
),
StudyPeriodDistinct as
(
    SELECT  distinct
            subject_ref,
            period_start_day,
            period_end_day
    from    StudyPeriodUnion
),
StudyPeriodOrdinal as (
    SELECT  distinct
            subject_ref,
            period_start_day,
            period_end_day,
            ROW_NUMBER() OVER (
                PARTITION   BY  subject_ref
                ORDER       BY  period_start_day    NULLS LAST,
                                period_end_day      NULLS LAST
            )   AS period_ordinal
    FROM    StudyPeriodDistinct
),
StudyPeriod as (
    select  distinct
            O.subject_ref,
            O.period_ordinal,
            O.period_start_day,
            O.period_end_day,
            U.encounter_ref
    from    StudyPeriodUnion    as U,
            StudyPeriodOrdinal  as O
    where   U.subject_ref       = O.subject_ref
    and     U.period_start_day  = O.period_start_day
    and     U.period_end_day    = O.period_end_day
)
select      *
from        StudyPeriod
order by    subject_ref,
            period_ordinal,
            encounter_ref;
