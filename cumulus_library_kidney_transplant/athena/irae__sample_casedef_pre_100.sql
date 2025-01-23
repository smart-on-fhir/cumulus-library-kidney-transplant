create table irae__sample_casedef_pre_100 as
select distinct
    subject_ref,
    documentreference_ref,
    valueset
from
    irae__sample_casedef_pre
where
    doc_type_display is not null and
    doc_type_display != 'unknown'
order by
    subject_ref,
    documentreference_ref
limit 100;
