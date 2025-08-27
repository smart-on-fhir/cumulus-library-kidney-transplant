CREATE table irae__sample_casedef_pre as
SELECT  distinct
        doc.subject_ref,
        doc.encounter_ref,
        doc.documentreference_ref,
        doc.doc_type_code,
        doc.doc_type_display,
        doc.doc_type_system,
        doc.doc_author_day,
        doc.enc_period_start_day,
        etl.group_name
FROM    etl__completion_encounters      as etl,
        irae__cohort_casedef_include as include,
        irae__cohort_casedef_pre as casedef,
        irae__cohort_study_population_doc as doc
WHERE   casedef.subject_ref = include.subject_ref
AND     casedef.encounter_ref = doc.encounter_ref
AND     casedef.encounter_ref = concat('Encounter/', etl.encounter_id)
ORDER BY
    subject_ref,
    enc_period_start_day,
    doc_author_day
;
