--    drop table if exists irae__rx_cohort_sample;

create table irae__rx_cohort_sample as
select distinct
    RX.subtype,
    MR.category_code as rx_category,
--    MR.category_system,
--    MR.category_display,
    MR.medication_code,
    MR.medication_system,
    MR.medication_display,
    E.class_code as encounter_class_code,
    E.class_display as encounter_class_display,
    DR.type_code as doc_type_code,
    DR.type_system as doc_type_system,
    DR.type_display as doc_type_display,
    DR.documentreference_ref,
    MR.encounter_ref,
    MR.subject_ref
 from
     core__medicationrequest as MR,
     core__documentreference as DR,
     core__encounter         as E,
     irae__rx RX
where 
     MR.encounter_ref = DR.encounter_ref    AND
     MR.encounter_ref = E.encounter_ref     AND
     MR.medication_code = RX.code           AND
     MR.medication_system = RX.system
order by
    MR.subject_ref,
    MR.encounter_ref,
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


