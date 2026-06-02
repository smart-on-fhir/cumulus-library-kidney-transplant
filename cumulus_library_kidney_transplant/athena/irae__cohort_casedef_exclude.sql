CREATE TABLE irae__cohort_casedef_exclude as WITH
dx_transplant AS
(
    SELECT  DISTINCT
            'dx_transplant' as variable, system, code, display,
            subject_ref
    FROM    irae__cohort_dx_transplant  AS cohort
    WHERE   CODE NOT IN ('Z94.9', 'V42.9') -- https://github.com/smart-on-fhir/cumulus-library-kidney-transplant/issues/39
    AND     NOT EXISTS (
                SELECT  1
                FROM    irae__casedef   AS casedef
                WHERE   casedef.code    = cohort.code
                AND     casedef.system  = exclude.system
            )
),
proc_transplant AS
(
    SELECT  DISTINCT
            'proc_transplant' as variable, system, code, display,
            subject_ref
    FROM    irae__cohort_proc_transplant AS cohort
    WHERE   NOT EXISTS (
                SELECT  1
                FROM    irae__casedef   AS casedef
                WHERE   casedef.code    = cohort.code
                AND     casedef.system  = cohort.system
            )
),
first_visit AS
(
    SELECT  MIN(enc_period_start_day) AS index_date,
            subject_ref
    FROM    irae__cohort_casedef_candidate
    WHERE   include
    GROUP BY subject_ref
),
complication AS
(
    SELECT  MIN(enc_period_start_day) AS index_date,
            subject_ref, valueset, code, display, system
    FROM    irae__cohort_casedef_candidate
    WHERE   NOT include
    GROUP BY subject_ref, valueset, code, display, system
),
first_visit_complication AS
(
    SELECT  DISTINCT
            valueset, system, code, display,
            complication.subject_ref
    FROM    first_visit, complication
    WHERE   first_visit.subject_ref = complication.subject_ref
    AND     first_visit.index_date > complication.index_date
),
exclusion_list AS
(
    select * from dx_transplant
    UNION ALL
    select * from proc_transplant
    UNION ALL
    select * from first_visit_complication
)
SELECT  DISTINCT
        exclusion_list.*
FROM    exclusion_list,
        irae__cohort_casedef_candidate AS casedef
WHERE   exclusion_list.subject_ref = casedef.subject_ref
;