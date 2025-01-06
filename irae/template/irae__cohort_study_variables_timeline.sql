create table irae__cohort_study_variables_timeline as
with lookup as
(
    select  distinct variable, subtype, encounter_ref
    from    irae__cohort_study_variables
)
select distinct
    lookup.variable,
    lookup.subtype,
    if(lookup.variable='dx_autoimmune', lookup.subtype) as dx_autoimmune,
    if(lookup.variable='dx_cancer', lookup.subtype) as dx_cancer,
    if(lookup.variable='dx_compromised', lookup.subtype) as dx_compromised,
    if(lookup.variable='dx_diabetes', lookup.subtype) as dx_diabetes,
    if(lookup.variable='dx_heart', lookup.subtype) as dx_heart,
    if(lookup.variable='dx_htn', lookup.subtype) as dx_htn,
    if(lookup.variable='dx_infection', lookup.subtype) as dx_infection,
    if(lookup.variable='dx_kidney', lookup.subtype) as dx_kidney,

    if(lookup.variable='lab_autoimmune', lookup.subtype) as lab_autoimmune,
    if(lookup.variable='lab_creatinine', lookup.subtype) as lab_creatinine,
    if(lookup.variable='lab_custom', lookup.subtype) as lab_custom,
    if(lookup.variable='lab_diabetes', lookup.subtype) as lab_diabetes,
    if(lookup.variable='lab_gfr', lookup.subtype) as lab_gfr,
    if(lookup.variable='lab_lft', lookup.subtype) as lab_lft,

    if(lookup.variable='rx_transplant', lookup.subtype) as rx_transplant,
    if(lookup.variable='rx_diabetes', lookup.subtype) as rx_diabetes,
    if(lookup.variable='rx_diuretics', lookup.subtype) as rx_diuretics,
    if(lookup.variable='rx_immunosuppressive', lookup.subtype) as rx_immunosuppressive,

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
from irae__cohort_study_population as SP
left join lookup on SP.encounter_ref = lookup.encounter_ref
