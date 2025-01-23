--    drop table if exists irae__rx_cohort_sample;

create table irae__sample_casedef_pre as
with unordered as
(
    select distinct
        RX.valueset,
        MR.category_code        as rx_category,
        MR.medication_code,
        MR.medication_system,
        MR.medication_display,
        E.class_code            as enc_class_code,
        E.class_display         as enc_class_display,
        DR.documentreference_ref,
        DR.type_code            as doc_type_code,
        DR.type_system          as doc_type_system,
        DR.type_display         as doc_type_display,
        DR.id                   as documentreference_id,
        E.id                    as encounter_id,
        E.encounter_ref,
        P.subject_ref,
        P.id                    as subject_id
     from
        irae__cohort_casedef_pre as CaseDef,
        irae__rx_custom         as RX,
        core__medicationrequest as MR,
        core__documentreference as DR,
        core__encounter         as E,
        core__patient           as P
    where
        CaseDef.encounter_ref = E.encounter_ref     AND
        CaseDef.encounter_ref = MR.encounter_ref    AND
        CaseDef.encounter_ref = DR.encounter_ref    AND
        E.subject_ref = P.subject_ref               AND
        MR.medication_code = RX.code                AND
        MR.medication_system = RX.system
)
select * from unordered order by
    subject_ref,
    encounter_ref,
    documentreference_ref;
