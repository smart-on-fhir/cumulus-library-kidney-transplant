--    drop table if exists irae__sample_dx_transplant;

create table irae__sample_dx_transplant_kidney as
with dx_transplant_kidney as
(
    select distinct valueset, subject_ref, min(enc_period_start_day) as min_start_day
    from irae__cohort_dx_transplant
    where valueset = 'dx_transplant_kidney'
    group by valueset, subject_ref
),
unordered as
(
    select distinct
        DX.valueset,
        DX.min_start_day,
        E.period_start_day,
        E.age_at_visit,
        E.gender,
        E.race_display,
        E.ethnicity_display,
        E.class_code            as enc_class_code,
        E.class_display         as enc_class_display,
        DR.type_code            as doc_type_code,
        DR.type_system          as doc_type_system,
        DR.type_display         as doc_type_display,
        DR.documentreference_ref,
        DR.id                   as documentreference_id,
        E.id                    as encounter_id,
        E.encounter_ref,
        P.subject_ref,
        P.id                    as subject_id
     from
        dx_transplant_kidney    as DX,
        core__documentreference as DR,
        core__encounter         as E,
        core__patient           as P
    where
        DX.subject_ref = P.subject_ref      AND
        DX.subject_ref = E.subject_ref      AND
        E.encounter_ref = DR.encounter_ref  AND
        DX.min_start_day <= E.period_start_day
)
select * from unordered order by
    subject_ref,
    period_start_day;

--            #################################################
--            Only on documents with a diagnosis
--            #################################################
--            create table irae__sample_dx_transplant as
--            with unordered as
--            (
--                select distinct
--                    DX.valueset             as dx_valueset,
--                    DX.dx_category_code,
--                    DX.dx_code,
--                    DX.dx_display,
--                    DX.dx_system,
--                    DX.min_start_day,
--                    DX.max_end_day,
--                    DX.cnt_days,
--                    DX.status,
--                    DX.age_at_visit,
--                    DX.gender,
--                    DX.race_display,
--                    DX.ethnicity_display,
--                    E.class_code            as enc_class_code,
--                    E.class_display         as enc_class_display,
--                    DR.documentreference_ref,
--                    DR.type_code            as doc_type_code,
--                    DR.type_system          as doc_type_system,
--                    DR.type_display         as doc_type_display,
--                    DR.id                   as documentreference_id,
--                    DX.condition_ref        as condition_ref,
--                    E.id                    as encounter_id,
--                    E.encounter_ref,
--                    P.subject_ref,
--                    P.id                    as subject_id
--                 from
--                    irae__cohort_dx_transplant as DX,
--                    core__documentreference as DR,
--                    core__encounter         as E,
--                    core__patient           as P
--                where
--                    DX.encounter_ref = E.encounter_ref     AND
--                    DX.encounter_ref = DR.encounter_ref    AND
--                    E.subject_ref = P.subject_ref
--            )
--            select * from unordered order by
--                subject_ref,
--                min_start_day,
--                cnt_days;
