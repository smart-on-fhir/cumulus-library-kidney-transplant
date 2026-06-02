CREATE TABLE irae__cohort_casedef_exclude as WITH
-- https://github.com/smart-on-fhir/cumulus-library-kidney-transplant/issues/39
--    dx_transplant AS
--    (
--        SELECT  DISTINCT
--                'dx_transplant' as variable, system, code, display,
--                subject_ref
--        FROM    irae__cohort_dx_transplant  AS cohort
--        WHERE   CODE NOT IN ('Z94.9', 'V42.9')
--        AND     NOT EXISTS (
--                    SELECT  1
--                    FROM    irae__casedef   AS casedef
--                    WHERE   casedef.code    = cohort.code
--                    AND     casedef.system  = exclude.system
--                )
--    ),
--    proc_transplant AS
--    (
--        SELECT  DISTINCT
--                'proc_transplant' as variable, system, code, display,
--                subject_ref
--        FROM    irae__cohort_proc_transplant AS cohort
--        WHERE   NOT EXISTS (
--                    SELECT  1
--                    FROM    irae__casedef   AS casedef
--                    WHERE   casedef.code    = cohort.code
--                    AND     casedef.system  = cohort.system
--                )
--    ),
first_include AS
(
    SELECT  MIN(sp.enc_period_start_day)    AS index_date,
            sp.subject_ref
    FROM    irae__cohort_casedef_candidate  AS casedef
    JOIN    irae__cohort_study_population   AS sp
    ON      casedef.encounter_ref = sp.encounter_ref
    WHERE   include
    GROUP BY sp.subject_ref
),
first_exclude AS
(
    SELECT  MIN(sp.enc_period_start_day)    AS index_date,
            sp.subject_ref
    FROM    irae__cohort_casedef_candidate  AS casedef
    JOIN    irae__cohort_study_population   AS sp
    ON      casedef.encounter_ref = sp.encounter_ref
    WHERE NOT include
    GROUP BY sp.subject_ref
),
first_filter AS
(
    SELECT  DISTINCT
            first_exclude.subject_ref,
            first_include.index_date    as index_date_include,
            first_exclude.index_date    as index_date_exclude
    FROM    first_include
    JOIN    first_exclude
    ON      first_include.subject_ref   = first_exclude.subject_ref
    AND     first_include.index_date    > first_exclude.index_date
),
exclusion_list AS
(
--    select * from dx_transplant
--    UNION ALL
--    select * from proc_transplant
--    UNION ALL
    select * from first_filter
)
SELECT  DISTINCT
        index_date_include,
        index_date_exclude,
        casedef.*
FROM    exclusion_list
JOIN    irae__cohort_casedef_candidate AS casedef
ON      exclusion_list.subject_ref = casedef.subject_ref
;