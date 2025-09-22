CREATE table irae__sample_casedef_post as
WITH
EncounterDoc as (
    SELECT  distinct
            ETL.group_name,
            CaseDef.subject_ref,
            CaseDef.encounter_ref,
            Doc.documentreference_ref,
            Doc.enc_period_ordinal,
            Doc.enc_period_start_day,
            Doc.doc_author_day,
            Doc.doc_date,
            case
            when (Doc.doc_author_day    is NOT null)    then Doc.doc_author_day
            when (Doc.doc_date          is NOT null)    then Doc.doc_date
            else Doc.enc_period_start_day               end as sort_by_date
    FROM    etl__completion_encounters          as ETL,
            irae__cohort_casedef_post        as CaseDef,
            irae__cohort_study_population_doc   as Doc
    WHERE   CaseDef.encounter_ref   = doc.encounter_ref
    AND     CaseDef.encounter_ref   = concat('Encounter/', etl.encounter_id)
    ORDER BY CaseDef.subject_ref
), 
ordered as (
    SELECT  distinct
            EncounterDoc.*,
            ROW_NUMBER() OVER (
                PARTITION   BY  subject_ref
                ORDER       BY  enc_period_start_day,
                                sort_by_date,
                                documentreference_ref
            )   AS doc_ordinal
    FROM    EncounterDoc
)
SELECT  ordered.*,
        doc.doc_type_code, 
        doc.doc_type_display, 
        doc.doc_type_system
from    ordered, 
        irae__cohort_study_population_doc as doc 
where   ordered.documentreference_ref = doc.documentreference_ref           
;