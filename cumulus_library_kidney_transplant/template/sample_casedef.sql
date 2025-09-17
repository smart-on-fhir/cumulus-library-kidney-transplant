CREATE table $prefix__sample_casedef_$period as
with unordered as (
    SELECT  distinct
            doc.subject_ref,
            doc.encounter_ref,
            doc.documentreference_ref,
            doc.doc_author_day, 
            doc.enc_period_start_day,
            etl.group_name
    FROM    etl__completion_encounters      as etl,
            irae__cohort_casedef_include    as include,
            irae__cohort_casedef_$period    as casedef_period,
            irae__cohort_study_population_doc as doc
    WHERE   casedef_period.subject_ref = include.subject_ref
    AND     casedef_period.encounter_ref = doc.encounter_ref
    AND     casedef_period.encounter_ref = concat('Encounter/', etl.encounter_id)
), 
ordered as (
    SELECT  distinct
            unordered.*,
            ROW_NUMBER() OVER (
                PARTITION   BY  subject_ref
                ORDER       BY  doc_author_day        NULLS LAST, 
                                enc_period_start_day  NULLS LAST, 
                                documentreference_ref
            )   AS doc_ordinal
    FROM    unordered
)
SELECT  ordered.*,
        doc.doc_type_code, 
        doc.doc_type_display, 
        doc.doc_type_system
from    ordered, 
        irae__cohort_study_population_doc as doc 
where   ordered.documentreference_ref = doc.documentreference_ref           
ORDER BY ordered.subject_ref, doc_ordinal