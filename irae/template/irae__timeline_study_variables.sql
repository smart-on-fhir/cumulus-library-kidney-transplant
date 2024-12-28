create table irae__timeline_study_variables as
select distinct
    dx_autoimmune,
    dx_cancer,
    dx_compromised,
    dx_diabetes,
    dx_heart,
    dx_htn,
    dx_infection,
    dx_kidney,
    rx_custom_transplant,
    rx_diabetes,
    rx_diuretics,
    rx_htn,
    rx_immunosuppressive,
    SP.status,
    SP.age_at_visit,
    SP.gender,
    SP.race_display,
    SP.ethnicity_display,
    SP.enc_class_code,
    SP.enc_period_start_day,
    SP.enc_period_start_month,
    SP.enc_period_start_year,
    SP.enc_period_end_day,
    SP.encounter_ref,
    SP.subject_ref
from
    irae__cohort_study_population               as SP
left join irae__cohort_study_variables_table_dx as DX on SP.encounter_ref = DX.encounter_ref
left join irae__cohort_study_variables_table_rx as RX on SP.encounter_ref = RX.encounter_ref