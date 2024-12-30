create or replace view irae__cohort_casedef as
select * from irae__cohort_rx_custom;

-- ###############################]#########################################
-- IndexDate is the technical term for cohort based studies
--
--  " The index date is frequently the date when individuals enter the study cohort
--  (e.g., enrollment date or the start of exposure to a treatment or risk factor).
--
-- ########################################################################

create or replace view irae__cohort_casedef_index as
with IndexDate as
(
    select      min(enc_period_start_day) as enc_period_start_day,
                subtype, subject_ref
    from        irae__cohort_casedef
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
    from
        irae__cohort_casedef as CaseDef,
        IndexDate
    where   CaseDef.subject_ref = IndexDate.subject_ref
    and     CaseDef.subtype     = IndexDate.subtype
    and     CaseDef.enc_period_start_day = IndexDate.enc_period_start_day
)
select  distinct
        Cohort.subtype,
        Cohort.code,
        Cohort.display,
        Cohort.system,
        StudyPop.*
from    IndexDate,
        irae__cohort_study_population as StudyPop
left join Cohort on StudyPop.encounter_ref = cohort.encounter_ref
where   IndexDate.subject_ref           = StudyPop.subject_ref
and     IndexDate.enc_period_start_day  = StudyPop.enc_period_start_day
;

-- ########################################################################
-- "Pre" = pre-exposure (for drug/treatment studies) or
-- "Pre" = pre-diagnosis (for disease studies)
-- ########################################################################

create or replace view irae__cohort_casedef_pre as
with IndexDate as
(
    select      min(enc_period_start_day) as enc_period_start_day,
                subtype, subject_ref
    from        irae__cohort_casedef
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
    from    IndexDate,
            irae__cohort_casedef as CaseDef
    where   CaseDef.subject_ref = IndexDate.subject_ref
    and     CaseDef.subtype     = IndexDate.subtype
    and     CaseDef.enc_period_start_day < IndexDate.enc_period_start_day
)
select  distinct
        Cohort.subtype,
        Cohort.code,
        Cohort.display,
        Cohort.system,
        StudyPop.*
from    IndexDate,
        irae__cohort_study_population as StudyPop
left join Cohort on StudyPop.encounter_ref = cohort.encounter_ref
where   IndexDate.subject_ref = StudyPop.subject_ref
and     IndexDate.enc_period_start_day < StudyPop.enc_period_start_day
;


-- ########################################################################
-- "Post" = post-exposure (for drug/treatment studies) or
-- "Post" = post-diagnosis (for disease studies)
-- ########################################################################

create or replace view irae__cohort_casedef_post as
with IndexDate as
(
    select      min(enc_period_start_day) as enc_period_start_day,
                subtype, subject_ref
    from        irae__cohort_casedef
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
    from    IndexDate,
            irae__cohort_casedef as CaseDef
    where   CaseDef.subject_ref = IndexDate.subject_ref
    and     CaseDef.subtype     = IndexDate.subtype
    and     CaseDef.enc_period_start_day > IndexDate.enc_period_start_day
)
select  distinct
        Cohort.subtype,
        Cohort.code,
        Cohort.display,
        Cohort.system,
        StudyPop.*
from    IndexDate,
        irae__cohort_study_population as StudyPop
left join Cohort on StudyPop.encounter_ref = cohort.encounter_ref
where   IndexDate.subject_ref = StudyPop.subject_ref
and     IndexDate.enc_period_start_day > StudyPop.enc_period_start_day
;
