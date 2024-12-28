create table irae__cohort_study_variables_dx as
with SP as
(
    select distinct encounter_ref, subject_ref   from irae__cohort_dx_autoimmune     UNION
    select distinct encounter_ref, subject_ref   from irae__cohort_dx_cancer         UNION
    select distinct encounter_ref, subject_ref   from irae__cohort_dx_compromised    UNION
    select distinct encounter_ref, subject_ref   from irae__cohort_dx_diabetes       UNION
    select distinct encounter_ref, subject_ref   from irae__cohort_dx_heart          UNION
    select distinct encounter_ref, subject_ref   from irae__cohort_dx_htn            UNION
    select distinct encounter_ref, subject_ref   from irae__cohort_dx_infection      UNION
    select distinct encounter_ref, subject_ref   from irae__cohort_dx_kidney
)
select distinct
    autoimmune.subtype as dx_autoimmune,
    cancer.subtype as dx_cancer,
    compromised.subtype as dx_compromised,
    diabetes.subtype as dx_diabetes,
    heart.subtype as dx_heart,
    htn.subtype as dx_htn,
    infection.subtype as dx_infection,
    kidney.subtype as dx_kidney,
    SP.encounter_ref,
    SP.subject_ref
from SP
left join irae__cohort_dx_autoimmune    as autoimmune   on SP.encounter_ref = autoimmune.encounter_ref
left join irae__cohort_dx_cancer        as cancer       on SP.encounter_ref = cancer.encounter_ref
left join irae__cohort_dx_compromised   as compromised  on SP.encounter_ref = compromised.encounter_ref
left join irae__cohort_dx_diabetes      as diabetes     on SP.encounter_ref = diabetes.encounter_ref
left join irae__cohort_dx_heart         as heart        on SP.encounter_ref = heart.encounter_ref
left join irae__cohort_dx_htn           as htn          on SP.encounter_ref = htn.encounter_ref
left join irae__cohort_dx_infection     as infection    on SP.encounter_ref = infection.encounter_ref
left join irae__cohort_dx_kidney        as kidney       on SP.encounter_ref = kidney.encounter_ref
