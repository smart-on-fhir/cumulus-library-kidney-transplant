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

create table irae__cohort_casedef_pre as
with IndexDate as
(
    select      min(enc_period_start_day) as enc_period_start_day,
                valueset, subject_ref
    from        irae__cohort_rx_custom
    group by    valueset, subject_ref
),
Cohort as
(
    select distinct
            CaseDef.valueset,
            CaseDef.code,
            CaseDef.display,
            CaseDef.system,
            CaseDef.age_at_visit,
            CaseDef.subject_ref,
            CaseDef.encounter_ref,
            CaseDef.enc_period_start_day
    from    irae__cohort_rx_custom as CaseDef,
            IndexDate
    where   CaseDef.subject_ref = IndexDate.subject_ref
    and     CaseDef.valueset     = IndexDate.valueset
    and     CaseDef.enc_period_start_day < IndexDate.enc_period_start_day
)
select  distinct
        Cohort.valueset,
        Cohort.code,
        Cohort.display,
        Cohort.system,
        Timeline.*
from    IndexDate,
        irae__cohort_study_variables_timeline as Timeline
left join Cohort on Timeline.encounter_ref = cohort.encounter_ref
where   Timeline.subject_ref           = IndexDate.subject_ref
and     Timeline.enc_period_start_day  < IndexDate.enc_period_start_day
;
