CREATE table $prefix__sample_casedef_$suffix as
SELECT  distinct
        doc.subject_ref,
        doc.encounter_ref,
        doc.documentreference_ref,
        doc.doc_type_code,
        doc.doc_type_display,
        doc.doc_type_system,
        doc.doc_author_day,
        doc.enc_period_start_day
FROM    $prefix__cohort_casedef_include as include,
        $prefix__cohort_casedef_$suffix as casedef,
        $prefix__cohort_study_population_doc as doc
WHERE   casedef.subject_ref = include.subject_ref
AND     casedef.encounter_ref = doc.encounter_ref
ORDER BY
    subject_ref,
    enc_period_start_day,
    doc_author_day
;
