--    drop table if exists irae__rx_cohort_sample;

create table irae__rx_cohort_sample as
select distinct
    RX.valueset,
    MR.category_code        as rx_category,
    MR.medication_code,
    MR.medication_system,
    MR.medication_display,
    E.class_code            as encounter_class_code,
    E.class_display         as encounter_class_display,
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
     core__medicationrequest as MR,
     core__documentreference as DR,
     core__encounter         as E,
     core__patient           as P,
     irae__rx_custom         as RX
where
     MR.encounter_ref = DR.encounter_ref    AND
     MR.encounter_ref = E.encounter_ref     AND
     E.subject_ref = P.subject_ref          AND
     MR.medication_code = RX.code           AND
     MR.medication_system = RX.system
order by
    P.subject_ref,
    E.encounter_ref,
    DR.documentreference_ref;

create table irae__rx_cohort_sample as
select distinct
    RX.valueset,
    MR.category_code        as rx_category,
    MR.medication_code,
    MR.medication_system,
    MR.medication_display,
    E.class_code            as encounter_class_code,
    E.class_display         as encounter_class_display,
    DR.type_code            as doc_type_code,
    DR.type_system          as doc_type_system,
    DR.type_display         as doc_type_display,
    DR.id                   as documentreference_id,
    DR.documentreference_ref,
    E.id                    as encounter_id,
    E.encounter_ref,
    P.subject_ref,
    P.id                    as subject_id
 from
     core__medicationrequest as MR,
     core__documentreference as DR,
     core__encounter         as E,
     core__patient           as P,
     irae__rx_custom         as RX
where 
     MR.encounter_ref = DR.encounter_ref    AND
     MR.encounter_ref = E.encounter_ref     AND
     E.subject_ref = P.subject_ref          AND
     MR.medication_code = RX.code           AND
     MR.medication_system = RX.system
order by
    P.subject_ref,
    E.encounter_ref,
    DR.documentreference_ref;

create table irae__rx_cohort_sample_100 as
select distinct
    subject_ref,
    documentreference_ref,
    subtype
from
    irae__rx_cohort_sample
where
    doc_type_display is not null and
    doc_type_display != 'unknown'
order by
    subject_ref,
    documentreference_ref
limit 100;

create table irae__rx_cohort_sample_1000 as
select distinct
    subject_id,
    documentreference_id,
    subtype
from
    irae__rx_cohort_sample
order by
    documentreference_id
limit 1000;


select count(distinct documentreference_ref) as cnt,
 subtype, rx_category, encounter_class_code, doc_type_display
 from   irae__rx_cohort_sample
 where
 doc_type_display is not null and
 doc_type_display != 'unknown'
 group by
 subtype, rx_category, encounter_class_code, doc_type_display
 order by cnt desc ;


 select count(distinct documentreference_ref) as cnt,
 subtype, encounter_class_code, doc_type_display
 from   irae__rx_cohort_sample
 where
 doc_type_display is not null and
 doc_type_display != 'unknown'
 group by
 subtype, encounter_class_code, doc_type_display
 order by cnt desc ;


