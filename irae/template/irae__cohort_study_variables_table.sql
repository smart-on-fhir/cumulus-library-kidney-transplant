create table irae__cohort_study_variables_table as
--with SUBSET as
--(
--    select distinct encounter_ref, subject_ref   from irae__cohort_dx_autoimmune     UNION
--    select distinct encounter_ref, subject_ref   from irae__cohort_dx_cancer         UNION
--    select distinct encounter_ref, subject_ref   from irae__cohort_dx_compromised    UNION
--    select distinct encounter_ref, subject_ref   from irae__cohort_dx_diabetes       UNION
--    select distinct encounter_ref, subject_ref   from irae__cohort_dx_heart          UNION
--    select distinct encounter_ref, subject_ref   from irae__cohort_dx_htn            UNION
--    select distinct encounter_ref, subject_ref   from irae__cohort_dx_infection      UNION
--    select distinct encounter_ref, subject_ref   from irae__cohort_dx_kidney         UNION
--    select distinct encounter_ref, subject_ref   from irae__cohort_rx_drug_levels    UNION
--    select distinct encounter_ref, subject_ref   from irae__cohort_rx_htn            UNION
--    select distinct encounter_ref, subject_ref   from irae__cohort_rx_immunosuppressive
--)
select distinct
    autoimmune.subtype as dx_autoimmune,
    cancer.subtype as dx_cancer,
    compromised.subtype as dx_compromised,
    diabetes.subtype as dx_diabetes,
    heart.subtype as dx_heart,
    htn.subtype as dx_htn,
    infection.subtype as dx_infection,
    kidney.subtype as dx_kidney,
    drug_levels.subtype as rx_tranSUBSETlant,
    rx_immuno.subtype as rx_immunosuppressive,
    SUBSET.encounter_ref,
    SUBSET.subject_ref
from irae__cohort_study_variables_lookup as SP
left join irae__cohort_dx_autoimmune    as autoimmune   on SUBSET.encounter_ref = autoimmune.encounter_ref
left join irae__cohort_dx_cancer        as cancer       on SUBSET.encounter_ref = cancer.encounter_ref
left join irae__cohort_dx_compromised   as compromised  on SUBSET.encounter_ref = compromised.encounter_ref
left join irae__cohort_dx_diabetes      as diabetes     on SUBSET.encounter_ref = diabetes.encounter_ref
left join irae__cohort_dx_heart         as heart        on SUBSET.encounter_ref = heart.encounter_ref
left join irae__cohort_dx_htn           as htn          on SUBSET.encounter_ref = htn.encounter_ref
left join irae__cohort_dx_infection     as infection    on SUBSET.encounter_ref = infection.encounter_ref
left join irae__cohort_dx_kidney        as kidney       on SUBSET.encounter_ref = kidney.encounter_ref
left join irae__cohort_rx_drug_levels   as drug_levels  on SUBSET.encounter_ref = drug_levels.encounter_ref
left join irae__cohort_rx_htn           as rx_htn       on SUBSET.encounter_ref = htn.encounter_ref
left join irae__cohort_rx_immunosuppressive as rx_immuno on SUBSET.encounter_ref = rx_immuno.encounter_ref








