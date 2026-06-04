CREATE TABLE irae__cohort_casedef_exclude as WITH
-- https://github.com/smart-on-fhir/cumulus-library-kidney-transplant/issues/39
candidate_list AS
(
    SELECT  casedef.system,
            casedef.code,
            casedef.display,
            casedef.include,
            sp.enc_period_start_day,
            sp.encounter_ref,
            sp.subject_ref
    FROM    irae__cohort_casedef_candidate  AS casedef
    JOIN    irae__cohort_study_population   AS sp
    ON      casedef.encounter_ref = sp.encounter_ref
),
any_transplant AS
(
    SELECT  system, code, display, 'dx_transplant'    AS exclude_reason
    FROM    irae__valueset_dx_transplant
    UNION ALL
    SELECT  system, code, display, 'proc_transplant' AS exclude_reason
    FROM    irae__cohort_proc_transplant
),
other_transplant AS
(
    SELECT  any_transplant.*
    FROM    any_transplant
    LEFT JOIN irae__valueset_casedef AS casedef
    ON      any_transplant.system = casedef.system
    AND     any_transplant.code   = casedef.code
    WHERE   casedef.code IS NULL
),
other_transplant_filter as 
(
    SELECT  MIN(enc_period_start_day)   AS exclude_date,
            subject_ref,
            exclude_reason
    FROM    candidate_list
    JOIN    other_transplant
    ON      candidate_list.system = other_transplant.system
    AND     candidate_list.code   = other_transplant.code
    GROUP BY subject_ref, exclude_reason
),
first_include AS
(
    SELECT  MIN(enc_period_start_day)    AS include_date,
            subject_ref
    FROM    candidate_list
    WHERE   include
    GROUP BY subject_ref
),
first_exclude AS
(
    SELECT  MIN(enc_period_start_day)    AS exclude_date,
            subject_ref
    FROM    candidate_list
    WHERE NOT include
    GROUP BY subject_ref
),
first_filter AS
(
    SELECT  DISTINCT
            first_exclude.subject_ref,
            first_exclude.exclude_date,
            'valueset_casedef' as exclude_reason
    FROM    first_include
    JOIN    first_exclude
    ON      first_include.subject_ref   = first_exclude.subject_ref
    AND     first_include.include_date  > first_exclude.exclude_date
),
exclusion_list AS
(
    select exclude_reason, exclude_date, subject_ref from other_transplant_filter
    UNION ALL
    select exclude_reason, exclude_date, subject_ref from first_filter
)
SELECT  DISTINCT
        exclusion_list.exclude_reason,
        exclusion_list.exclude_date,
        casedef.*
FROM    exclusion_list
JOIN    irae__cohort_casedef_candidate AS casedef
ON      exclusion_list.subject_ref = casedef.subject_ref
;