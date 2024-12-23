create table irae__cohort_study_population_doc as
select distinct
    doc.docstatus       as doc_status,
    doc.type_code       as doc_type_code,
    doc.type_display    as doc_type_display,
    doc.type_system     as doc_type_system,
    doc.author_day      as doc_author_day,
    doc.documentreference_ref,
    study_population.*
from
    irae__cohort_study_population as study_population
left join core__documentreference as doc
    on doc.encounter_ref = study_population.encounter_ref
;
