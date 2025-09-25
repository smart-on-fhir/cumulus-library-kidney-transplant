-- ###############################]#########################################
-- "IndexDate" is the technical term for cohort based studies
--
--  The index date is frequently the date when individuals enter the study cohort
--  (e.g., enrollment date or the start of exposure to a treatment or risk factor).
--
--
-- "Pre" = pre-exposure (for drug/treatment studies) or
-- "Pre" = pre-diagnosis (for disease studies)
-- "Post" = post-exposure (for drug/treatment studies) or
-- "Post" = post-diagnosis (for disease studies)
--
-- ########################################################################

create table irae__cohort_casedef_index as
WITH
IndexDate as
(
    select      min(enc_period_start_day) as index_date,
                subject_ref
    from        irae__cohort_casedef_include
    group by    subject_ref
)
select  IndexDate.index_date,
        SP.*
from    irae__cohort_study_population as SP,
        IndexDate
where   SP.subject_ref = IndexDate.subject_ref
and     SP.enc_period_start_day = IndexDate.index_date
;