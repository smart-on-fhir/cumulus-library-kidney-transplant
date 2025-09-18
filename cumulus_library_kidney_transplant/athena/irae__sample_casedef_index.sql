CREATE table irae__sample_casedef_index as
with documented_encounters as (
    SELECT  distinct
            include.subject_ref,
            include.encounter_ref,
            doc.documentreference_ref,
            doc.doc_author_day, 
            doc.enc_period_start_day,
            etl.group_name
    FROM    etl__completion_encounters      as etl,
            irae__cohort_casedef_include    as include,
            irae__cohort_casedef_index    as casedef_period,
            irae__cohort_study_population_doc as doc
    WHERE   include.subject_ref = casedef_period.subject_ref
    AND     include.encounter_ref = doc.encounter_ref
    AND     include.encounter_ref = concat('Encounter/', etl.encounter_id)
    ORDER BY include.subject_ref
), 
ordered as (
    SELECT  distinct
            documented_encounters.*,
            ROW_NUMBER() OVER (
                PARTITION   BY  subject_ref
                ORDER       BY  doc_author_day        NULLS LAST, 
                                enc_period_start_day  NULLS LAST, 
                                documentreference_ref
            )   AS doc_ordinal
    FROM    documented_encounters
)
SELECT  ordered.*,
        doc.doc_type_code, 
        doc.doc_type_display, 
        doc.doc_type_system
from    ordered, 
        irae__cohort_study_population_doc as doc 
where   ordered.documentreference_ref = doc.documentreference_ref           
ORDER BY ordered.subject_ref, doc_ordinal