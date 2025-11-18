create table irae__cohort_study_variables_wide as
with lookup as
(
    select  distinct variable, valueset, encounter_ref
    from    irae__cohort_study_variables
),
join_study_period as
(
    select  distinct
            	IF(lookup.variable='doc_biopsy', lookup.valueset) AS doc_biopsy,
	IF(lookup.variable='dx_autoimmune', lookup.valueset) AS dx_autoimmune,
	IF(lookup.variable='dx_cancer', lookup.valueset) AS dx_cancer,
	IF(lookup.variable='dx_immunocompromised', lookup.valueset) AS dx_immunocompromised,
	IF(lookup.variable='dx_infection', lookup.valueset) AS dx_infection,
	IF(lookup.variable='dx_kidney', lookup.valueset) AS dx_kidney,
	IF(lookup.variable='dx_transplant', lookup.valueset) AS dx_transplant,
	IF(lookup.variable='lab_autoimmune', lookup.valueset) AS lab_autoimmune,
	IF(lookup.variable='lab_cbc', lookup.valueset) AS lab_cbc,
	IF(lookup.variable='lab_cmp', lookup.valueset) AS lab_cmp,
	IF(lookup.variable='lab_creatinine', lookup.valueset) AS lab_creatinine,
	IF(lookup.variable='lab_diabetes', lookup.valueset) AS lab_diabetes,
	IF(lookup.variable='lab_gfr', lookup.valueset) AS lab_gfr,
	IF(lookup.variable='lab_lft', lookup.valueset) AS lab_lft,
	IF(lookup.variable='proc_dialysis', lookup.valueset) AS proc_dialysis,
	IF(lookup.variable='proc_nephrectomy', lookup.valueset) AS proc_nephrectomy,
	IF(lookup.variable='proc_transplant', lookup.valueset) AS proc_transplant,
	IF(lookup.variable='rx_antibiotics', lookup.valueset) AS rx_antibiotics,
	IF(lookup.variable='rx_cancer', lookup.valueset) AS rx_cancer,
	IF(lookup.variable='rx_diabetes', lookup.valueset) AS rx_diabetes,
	IF(lookup.variable='rx_diuretics', lookup.valueset) AS rx_diuretics,
	IF(lookup.variable='rx_htn', lookup.valueset) AS rx_htn,
	IF(lookup.variable='rx_immunosuppressive', lookup.valueset) AS rx_immunosuppressive,
	IF(lookup.variable='lab_custom', lookup.valueset) AS lab_custom,
	IF(lookup.variable='rx_custom', lookup.valueset) AS rx_custom,
            SP.encounter_ref
    from    irae__cohort_study_period as SP
    left join lookup on SP.encounter_ref = lookup.encounter_ref
),
tabular as
(
    select  distinct
            	arbitrary(doc_biopsy)    FILTER (where doc_biopsy  is NOT null) as doc_biopsy,
	arbitrary(dx_autoimmune)    FILTER (where dx_autoimmune  is NOT null) as dx_autoimmune,
	arbitrary(dx_cancer)    FILTER (where dx_cancer  is NOT null) as dx_cancer,
	arbitrary(dx_immunocompromised)    FILTER (where dx_immunocompromised  is NOT null) as dx_immunocompromised,
	arbitrary(dx_infection)    FILTER (where dx_infection  is NOT null) as dx_infection,
	arbitrary(dx_kidney)    FILTER (where dx_kidney  is NOT null) as dx_kidney,
	arbitrary(dx_transplant)    FILTER (where dx_transplant  is NOT null) as dx_transplant,
	arbitrary(lab_autoimmune)    FILTER (where lab_autoimmune  is NOT null) as lab_autoimmune,
	arbitrary(lab_cbc)    FILTER (where lab_cbc  is NOT null) as lab_cbc,
	arbitrary(lab_cmp)    FILTER (where lab_cmp  is NOT null) as lab_cmp,
	arbitrary(lab_creatinine)    FILTER (where lab_creatinine  is NOT null) as lab_creatinine,
	arbitrary(lab_diabetes)    FILTER (where lab_diabetes  is NOT null) as lab_diabetes,
	arbitrary(lab_gfr)    FILTER (where lab_gfr  is NOT null) as lab_gfr,
	arbitrary(lab_lft)    FILTER (where lab_lft  is NOT null) as lab_lft,
	arbitrary(proc_dialysis)    FILTER (where proc_dialysis  is NOT null) as proc_dialysis,
	arbitrary(proc_nephrectomy)    FILTER (where proc_nephrectomy  is NOT null) as proc_nephrectomy,
	arbitrary(proc_transplant)    FILTER (where proc_transplant  is NOT null) as proc_transplant,
	arbitrary(rx_antibiotics)    FILTER (where rx_antibiotics  is NOT null) as rx_antibiotics,
	arbitrary(rx_cancer)    FILTER (where rx_cancer  is NOT null) as rx_cancer,
	arbitrary(rx_diabetes)    FILTER (where rx_diabetes  is NOT null) as rx_diabetes,
	arbitrary(rx_diuretics)    FILTER (where rx_diuretics  is NOT null) as rx_diuretics,
	arbitrary(rx_htn)    FILTER (where rx_htn  is NOT null) as rx_htn,
	arbitrary(rx_immunosuppressive)    FILTER (where rx_immunosuppressive  is NOT null) as rx_immunosuppressive,
	arbitrary(lab_custom)    FILTER (where lab_custom  is NOT null) as lab_custom,
	arbitrary(rx_custom)    FILTER (where rx_custom  is NOT null) as rx_custom,
            encounter_ref
    from    join_study_period
    group by encounter_ref
)
select  distinct
        tabular.*   ,
        subject_ref
from    irae__cohort_study_population as study_pop,
        tabular
where   tabular.encounter_ref = study_pop.encounter_ref
;