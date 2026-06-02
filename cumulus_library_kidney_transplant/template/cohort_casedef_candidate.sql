CREATE TABLE {{ prefix }}__cohort_casedef_candidate AS
SELECT  DISTINCT
        'casedef_dx'            AS valueset,
        condition_ref           AS resource_ref,
        casedef.*,
        subject_ref,
        encounter_ref
FROM    {{ prefix }}__valueset_casedef  AS casedef,
        {{ prefix }}__cohort_study_population_dx
WHERE   casedef.system  = dx_system
AND     casedef.code    = dx_code

UNION ALL
SELECT  DISTINCT
        'casedef_proc'          AS valueset,
        procedure_ref           AS resource_ref,
        casedef.*,
        subject_ref,
        encounter_ref
FROM    {{ prefix }}__valueset_casedef   AS casedef,
        {{ prefix }}__cohort_study_population_proc
WHERE   casedef.system  = proc_system
AND     casedef.code    = proc_code

UNION ALL
SELECT  DISTINCT
        'casedef_lab'           AS valueset,
        observation_ref         AS resource_ref,
        casedef.*,
        subject_ref,
        encounter_ref
FROM    {{ prefix }}__valueset_casedef   AS casedef,
        {{ prefix }}__cohort_study_population_lab
WHERE   casedef.system  = lab_observation_system
AND     casedef.code    = lab_observation_code

UNION ALL
SELECT  DISTINCT
        'casedef_rx'            AS valueset,
        medicationrequest_ref   AS resource_ref,
        casedef.*,
        subject_ref,
        encounter_ref
FROM    {{ prefix }}__valueset_casedef   AS casedef,
        {{ prefix }}__cohort_study_population_rx
WHERE   casedef.system  = rx_system
AND     casedef.code    = rx_code

UNION ALL
SELECT  DISTINCT
        'casedef_diag'          AS valueset,
        result_ref              AS resource_ref,
        casedef.*,
        subject_ref,
        encounter_ref
FROM    {{ prefix }}__valueset_casedef   AS casedef,
        {{ prefix }}__cohort_study_population_diag
WHERE   casedef.system  = diag_system
AND     casedef.code    = diag_code

UNION ALL
SELECT  DISTINCT
        'casedef_doc'           AS valueset,
        documentreference_ref   AS resource_ref,
        casedef.*,
        subject_ref,
        encounter_ref
FROM    {{ prefix }}__valueset_casedef   AS casedef,
        {{ prefix }}__cohort_study_population_doc
WHERE   casedef.system  = doc_type_system
AND     casedef.code    = doc_type_code
;