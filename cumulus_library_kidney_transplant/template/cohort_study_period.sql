CREATE TABLE irae__cohort_study_period as
WITH
Range as
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
History as
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
            FROM    Range
            WHERE   Range.subject_ref = E.subject_ref)
),
Merged as
(
    select  *  from Range
    UNION ALL
    select  *  from History
),
Uniq as
(
    SELECT  distinct
            subject_ref,
            period_start_day,
            period_end_day
    from    Merged
),
Ordinal as (
    SELECT  distinct
            subject_ref,
            period_start_day,
            period_end_day,
            ROW_NUMBER() OVER (
                PARTITION   BY  subject_ref
                ORDER       BY  period_start_day    NULLS LAST,
                                period_end_day      NULLS LAST
            )   AS period_ordinal
    FROM    Uniq
)
select  distinct
        Ordinal.subject_ref,
        Ordinal.period_ordinal,
        Ordinal.period_start_day,
        Ordinal.period_end_day,
        Merged.encounter_ref
from    Merged,
        Ordinal
where   Merged.subject_ref       = Ordinal.subject_ref
and     Merged.period_start_day  = Ordinal.period_start_day
and     Merged.period_end_day    = Ordinal.period_end_day
;