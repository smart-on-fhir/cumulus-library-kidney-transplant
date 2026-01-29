create table irae__cohort_variable_wide as
with lookup as
(
    select  distinct variable, encounter_ref
    from    irae__cohort_variable_union
),
join_study_period as
(
    select  distinct
            	IF(lookup.variable='doc_biopsy', True) AS doc_biopsy,
	IF(lookup.variable='dx_autoimmune', True) AS dx_autoimmune,
	IF(lookup.variable='dx_cancer', True) AS dx_cancer,
	IF(lookup.variable='dx_immunocompromised', True) AS dx_immunocompromised,
	IF(lookup.variable='dx_infection', True) AS dx_infection,
	IF(lookup.variable='dx_kidney', True) AS dx_kidney,
	IF(lookup.variable='dx_transplant', True) AS dx_transplant,
	IF(lookup.variable='lab_autoimmune', True) AS lab_autoimmune,
	IF(lookup.variable='lab_cbc', True) AS lab_cbc,
	IF(lookup.variable='lab_cmp', True) AS lab_cmp,
	IF(lookup.variable='lab_creatinine', True) AS lab_creatinine,
	IF(lookup.variable='lab_diabetes', True) AS lab_diabetes,
	IF(lookup.variable='lab_gfr', True) AS lab_gfr,
	IF(lookup.variable='lab_lft', True) AS lab_lft,
	IF(lookup.variable='proc_dialysis', True) AS proc_dialysis,
	IF(lookup.variable='proc_nephrectomy', True) AS proc_nephrectomy,
	IF(lookup.variable='proc_transplant', True) AS proc_transplant,
	IF(lookup.variable='rx_antibiotics', True) AS rx_antibiotics,
	IF(lookup.variable='rx_cancer', True) AS rx_cancer,
	IF(lookup.variable='rx_diabetes', True) AS rx_diabetes,
	IF(lookup.variable='rx_diuretics', True) AS rx_diuretics,
	IF(lookup.variable='rx_htn', True) AS rx_htn,
	IF(lookup.variable='rx_immunosuppressive', True) AS rx_immunosuppressive,
	IF(lookup.variable='lab_custom', True) AS lab_custom,
	IF(lookup.variable='rx_custom', True) AS rx_custom,
            SP.encounter_ref
    from    irae__cohort_study_period as SP
    left join lookup on SP.encounter_ref = lookup.encounter_ref
),
tabular as
(
    select  distinct
            	arbitrary(doc_biopsy)    FILTER (where doc_biopsy ) as doc_biopsy,
	arbitrary(dx_autoimmune)    FILTER (where dx_autoimmune ) as dx_autoimmune,
	arbitrary(dx_cancer)    FILTER (where dx_cancer ) as dx_cancer,
	arbitrary(dx_immunocompromised)    FILTER (where dx_immunocompromised ) as dx_immunocompromised,
	arbitrary(dx_infection)    FILTER (where dx_infection ) as dx_infection,
	arbitrary(dx_kidney)    FILTER (where dx_kidney ) as dx_kidney,
	arbitrary(dx_transplant)    FILTER (where dx_transplant ) as dx_transplant,
	arbitrary(lab_autoimmune)    FILTER (where lab_autoimmune ) as lab_autoimmune,
	arbitrary(lab_cbc)    FILTER (where lab_cbc ) as lab_cbc,
	arbitrary(lab_cmp)    FILTER (where lab_cmp ) as lab_cmp,
	arbitrary(lab_creatinine)    FILTER (where lab_creatinine ) as lab_creatinine,
	arbitrary(lab_diabetes)    FILTER (where lab_diabetes ) as lab_diabetes,
	arbitrary(lab_gfr)    FILTER (where lab_gfr ) as lab_gfr,
	arbitrary(lab_lft)    FILTER (where lab_lft ) as lab_lft,
	arbitrary(proc_dialysis)    FILTER (where proc_dialysis ) as proc_dialysis,
	arbitrary(proc_nephrectomy)    FILTER (where proc_nephrectomy ) as proc_nephrectomy,
	arbitrary(proc_transplant)    FILTER (where proc_transplant ) as proc_transplant,
	arbitrary(rx_antibiotics)    FILTER (where rx_antibiotics ) as rx_antibiotics,
	arbitrary(rx_cancer)    FILTER (where rx_cancer ) as rx_cancer,
	arbitrary(rx_diabetes)    FILTER (where rx_diabetes ) as rx_diabetes,
	arbitrary(rx_diuretics)    FILTER (where rx_diuretics ) as rx_diuretics,
	arbitrary(rx_htn)    FILTER (where rx_htn ) as rx_htn,
	arbitrary(rx_immunosuppressive)    FILTER (where rx_immunosuppressive ) as rx_immunosuppressive,
	arbitrary(lab_custom)    FILTER (where lab_custom ) as lab_custom,
	arbitrary(rx_custom)    FILTER (where rx_custom ) as rx_custom,
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