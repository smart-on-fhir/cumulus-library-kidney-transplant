create or replace view irae__sample_casedef_peri_limit_patient_10 as
WITH
patient_list as (
    select  distinct
            subject_ref
    from    irae__sample_casedef_peri
    limit   10
)
select      distinct
            note.*
from        irae__sample_casedef_peri as note,
            patient_list as P
where       P.subject_ref = note.subject_ref
order by    subject_ref,
            enc_period_ordinal,
            note_ordinal;
