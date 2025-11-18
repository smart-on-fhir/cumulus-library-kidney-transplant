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
            	arbitrary(doc_biopsy)    FILTER (WHERE doc_biopsy  IS NOT NULL) AS doc_biopsy,
	arbitrary(dx_autoimmune)    FILTER (WHERE dx_autoimmune  IS NOT NULL) AS dx_autoimmune,
	arbitrary(dx_cancer)    FILTER (WHERE dx_cancer  IS NOT NULL) AS dx_cancer,
	arbitrary(dx_immunocompromised)    FILTER (WHERE dx_immunocompromised  IS NOT NULL) AS dx_immunocompromised,
	arbitrary(dx_infection)    FILTER (WHERE dx_infection  IS NOT NULL) AS dx_infection,
	arbitrary(dx_kidney)    FILTER (WHERE dx_kidney  IS NOT NULL) AS dx_kidney,
	arbitrary(dx_transplant)    FILTER (WHERE dx_transplant  IS NOT NULL) AS dx_transplant,
	arbitrary(lab_autoimmune)    FILTER (WHERE lab_autoimmune  IS NOT NULL) AS lab_autoimmune,
	arbitrary(lab_cbc)    FILTER (WHERE lab_cbc  IS NOT NULL) AS lab_cbc,
	arbitrary(lab_cmp)    FILTER (WHERE lab_cmp  IS NOT NULL) AS lab_cmp,
	arbitrary(lab_creatinine)    FILTER (WHERE lab_creatinine  IS NOT NULL) AS lab_creatinine,
	arbitrary(lab_diabetes)    FILTER (WHERE lab_diabetes  IS NOT NULL) AS lab_diabetes,
	arbitrary(lab_gfr)    FILTER (WHERE lab_gfr  IS NOT NULL) AS lab_gfr,
	arbitrary(lab_lft)    FILTER (WHERE lab_lft  IS NOT NULL) AS lab_lft,
	arbitrary(proc_dialysis)    FILTER (WHERE proc_dialysis  IS NOT NULL) AS proc_dialysis,
	arbitrary(proc_nephrectomy)    FILTER (WHERE proc_nephrectomy  IS NOT NULL) AS proc_nephrectomy,
	arbitrary(proc_transplant)    FILTER (WHERE proc_transplant  IS NOT NULL) AS proc_transplant,
	arbitrary(rx_antibiotics)    FILTER (WHERE rx_antibiotics  IS NOT NULL) AS rx_antibiotics,
	arbitrary(rx_cancer)    FILTER (WHERE rx_cancer  IS NOT NULL) AS rx_cancer,
	arbitrary(rx_diabetes)    FILTER (WHERE rx_diabetes  IS NOT NULL) AS rx_diabetes,
	arbitrary(rx_diuretics)    FILTER (WHERE rx_diuretics  IS NOT NULL) AS rx_diuretics,
	arbitrary(rx_htn)    FILTER (WHERE rx_htn  IS NOT NULL) AS rx_htn,
	arbitrary(rx_immunosuppressive)    FILTER (WHERE rx_immunosuppressive  IS NOT NULL) AS rx_immunosuppressive,
	arbitrary(lab_custom)    FILTER (WHERE lab_custom  IS NOT NULL) AS lab_custom,
	arbitrary(rx_custom)    FILTER (WHERE rx_custom  IS NOT NULL) AS rx_custom,
            encounter_ref
    from    join_study_period
    group by encounter_ref
)
select  distinct
        status              	,
        age_at_visit        	,
        gender              	,
        race_display        	,
        ethnicity_display   	,
        enc_period_ordinal  	,
        enc_period_start_day	,
        enc_period_start_week	,
        enc_period_start_month	,
        enc_period_start_year	,
        enc_period_end_day  	,
        enc_class_code      	,
        enc_servicetype_code	,
        enc_servicetype_system	,
        enc_servicetype_display	,
        enc_type_code       	,
        enc_type_system     	,
        enc_type_display    	,
        study_pop.encounter_ref ,
        study_pop.subject_ref
from    irae__cohort_study_population as study_pop,
        tabular
where   tabular.encounter_ref = study_pop.encounter_ref




