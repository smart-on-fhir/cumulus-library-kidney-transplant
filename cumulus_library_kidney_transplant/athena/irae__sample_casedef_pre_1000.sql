create table irae__sample_casedef_pre_1000 as
WITH
patient_list as (
    select  distinct subject_ref 
    from    case_documented_encounter
    limit 1000 
)
select      distinct doc.* 
from        irae__sample_casedef_pre as doc,
            patient_list as P
where       P.subject_ref = doc.subject_ref 
order by    subject_ref, 
            enc_period_start_day, 
            doc_author_day;