create table $prefix__sample_casedef_$suffix_$size as
select distinct
    subject_ref,
    documentreference_ref,
    valueset
from
    $prefix__sample_casedef_$suffix
where
    doc_type_display is not null and
    doc_type_display != 'unknown'
order by
    subject_ref,
    documentreference_ref
limit $size;
