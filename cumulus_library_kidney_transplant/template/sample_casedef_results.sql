create table irae__cohort_casedef_post_1000_results as
WITH merged as
(
    select filename,ade,occurred, 'ATG'              as drug from mike__irea_output_results_atg_short_list_v1           UNION
    select filename,ade,occurred, 'azathioprine'     as drug from mike__irea_output_results_azathioprine_short_list_v1  UNION
    select filename,ade,occurred, 'cyclosporin'      as drug from mike__irea_output_results_cyclosporin_short_list_v1   UNION
    select filename,ade,occurred, 'mycophenolate'    as drug from mike__irea_output_results_mycophenolate_short_list_v1 UNION
    select filename,ade,occurred, 'sirolimus'        as drug from mike__irea_output_results_sirolimus_short_list_v1     UNION
    select filename,ade,occurred, 'tacrolimus'       as drug from mike__irea_output_results_tacrolimus_short_list_v1
),
parsed as
(
    select
        SPLIT_PART(filename, '.', 1) AS subject_id,
        SPLIT_PART(filename, '.', 2) AS documentreference_id,
        ade,
        drug
    from merged
    where occurred = True
),
join_docref as
(
    select  distinct
            parsed.drug,
            parsed.ade,
            doc.type_code       as doc_type_code,
            doc.type_system     as doc_type_system,
            doc.type_display    as doc_type_display,
            doc.author_month,
            doc.subject_ref,
            doc.encounter_ref,
            doc.documentreference_ref
    from    parsed,
            core__documentreference as doc
    where   doc.documentreference_ref = concat('DocumentReference/', parsed.documentreference_id)
),
join_encounter as
(
    select  distinct
            E.status,
            E.class_code    as enc_class_code,
            E.class_display as enc_class_display,
            E.period_start_day,
            E.period_start_month,
            E.age_at_visit,
            E.gender,
            E.race_display,
            E.ethnicity_display,
            join_docref.*
    from    join_docref,
            core__encounter as E
    where   join_docref.encounter_ref = E.encounter_ref
)
select * from join_encounter
