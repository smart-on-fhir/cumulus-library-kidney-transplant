create table irae__cohort_study_variables_rx as
with SP as
(
    select distinct encounter_ref, subject_ref   from irae__cohort_rx_custom            UNION
    select distinct encounter_ref, subject_ref   from irae__cohort_rx_diabetes          UNION
    select distinct encounter_ref, subject_ref   from irae__cohort_rx_diuretics         UNION
    select distinct encounter_ref, subject_ref   from irae__cohort_rx_htn               UNION
    select distinct encounter_ref, subject_ref   from irae__cohort_rx_immunosuppressive
)
select distinct
    custom.subtype as rx_custom_transplant,
    diabetes.subtype as rx_diabetes,
    diuretics.subtype as rx_diuretics,
    htn.subtype as rx_htn,
    immuno.subtype as rx_immunosuppressive,
    SP.encounter_ref,
    SP.subject_ref
from SP
left join irae__cohort_rx_custom    as custom  on SP.encounter_ref = custom.encounter_ref
left join irae__cohort_rx_diabetes  as diabetes on SP.encounter_ref = diabetes.encounter_ref
left join irae__cohort_rx_diuretics as diuretics on SP.encounter_ref = diuretics.encounter_ref
left join irae__cohort_rx_htn       as htn       on SP.encounter_ref = htn.encounter_ref
left join irae__cohort_rx_immunosuppressive as immuno on SP.encounter_ref = immuno.encounter_ref












