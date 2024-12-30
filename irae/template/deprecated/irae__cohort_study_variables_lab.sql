--    irae__cohort_lab_panel_cbc
--    irae__cohort_lab_panel_cmp
--    irae__cohort_lab_panel_lft

create table irae__cohort_study_variables_lab as
with SP as
(
    select distinct encounter_ref, subject_ref   from irae__cohort_lab_autoimmune       UNION
    select distinct encounter_ref, subject_ref   from irae__cohort_lab_custom           UNION
    select distinct encounter_ref, subject_ref   from irae__cohort_lab_creatinine       UNION
--    select distinct encounter_ref, subject_ref   from irae__cohort_lab_diabetes         UNION
    select distinct encounter_ref, subject_ref   from irae__cohort_lab_gfr              UNION
    select distinct encounter_ref, subject_ref   from irae__cohort_lab_lft
)
select distinct
    autoimmune.subtype  as lab_autoimmune,
    custom.subtype      as lab_custom,
    creatinine.subtype  as lab_creatinine,
--    diabetes.subtype    as lab_diabetes,
    gfr.subtype         as lab_gfr,
    lft.subtype         as lab_lft,
    SP.encounter_ref,
    SP.subject_ref
from SP
left join irae__cohort_lab_autoimmune   as autoimmune   on SP.encounter_ref = autoimmune.encounter_ref
left join irae__cohort_lab_custom       as custom       on SP.encounter_ref = custom.encounter_ref
left join irae__cohort_lab_creatinine   as creatinine   on SP.encounter_ref = creatinine.encounter_ref
--left join irae__cohort_lab_diabetes     as diabetes     on SP.encounter_ref = diabetes.encounter_ref
left join irae__cohort_lab_gfr          as gfr          on SP.encounter_ref = gfr.encounter_ref
left join irae__cohort_lab_lft          as lft          on SP.encounter_ref = lft.encounter_ref












