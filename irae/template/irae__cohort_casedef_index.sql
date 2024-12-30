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

create table $prefix__cohort_casedef_$suffix as
with IndexDate as
(
    select      min(enc_period_start_day) as enc_period_start_day,
                subtype, subject_ref
    from        $prefix__cohort_casedef
    group by    subtype, subject_ref
),
Cohort as
(
    select distinct
            CaseDef.subtype,
            CaseDef.code,
            CaseDef.display,
            CaseDef.system,
            CaseDef.age_at_visit,
            CaseDef.subject_ref,
            CaseDef.encounter_ref,
            CaseDef.enc_period_start_day
    from    $prefix__cohort_casedef as CaseDef,
            IndexDate
    where   CaseDef.subject_ref = IndexDate.subject_ref
    and     CaseDef.subtype     = IndexDate.subtype
    and     CaseDef.enc_period_start_day $equality IndexDate.enc_period_start_day
)
select  distinct
        Cohort.subtype,
        Cohort.code,
        Cohort.display,
        Cohort.system,
        StudyPop.*
from    IndexDate,
        $prefix__cohort_study_population as StudyPop
left join Cohort on StudyPop.encounter_ref = cohort.encounter_ref
where   StudyPop.subject_ref           = IndexDate.subject_ref
and     StudyPop.enc_period_start_day  $equality IndexDate.enc_period_start_day
;
