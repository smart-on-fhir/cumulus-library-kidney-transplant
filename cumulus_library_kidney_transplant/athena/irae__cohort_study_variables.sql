create table irae__cohort_study_variables as
with variable_cohorts as
(
	select distinct 'doc_biopsy'	 as variable, valueset, code, display, system, encounter_ref, subject_ref  from irae__cohort_doc_biopsy UNION
	select distinct 'dx_autoimmune'	 as variable, valueset, code, display, system, encounter_ref, subject_ref  from irae__cohort_dx_autoimmune UNION
	select distinct 'dx_cancer'	 as variable, valueset, code, display, system, encounter_ref, subject_ref  from irae__cohort_dx_cancer UNION
	select distinct 'dx_diabetes'	 as variable, valueset, code, display, system, encounter_ref, subject_ref  from irae__cohort_dx_diabetes UNION
	select distinct 'dx_heart'	 as variable, valueset, code, display, system, encounter_ref, subject_ref  from irae__cohort_dx_heart UNION
	select distinct 'dx_htn'	 as variable, valueset, code, display, system, encounter_ref, subject_ref  from irae__cohort_dx_htn UNION
	select distinct 'dx_immunocompromised'	 as variable, valueset, code, display, system, encounter_ref, subject_ref  from irae__cohort_dx_immunocompromised UNION
	select distinct 'dx_infection'	 as variable, valueset, code, display, system, encounter_ref, subject_ref  from irae__cohort_dx_infection UNION
	select distinct 'dx_kidney'	 as variable, valueset, code, display, system, encounter_ref, subject_ref  from irae__cohort_dx_kidney UNION
	select distinct 'dx_transplant'	 as variable, valueset, code, display, system, encounter_ref, subject_ref  from irae__cohort_dx_transplant UNION
	select distinct 'lab_autoimmune'	 as variable, valueset, code, display, system, encounter_ref, subject_ref  from irae__cohort_lab_autoimmune UNION
	select distinct 'lab_cbc'	 as variable, valueset, code, display, system, encounter_ref, subject_ref  from irae__cohort_lab_cbc UNION
	select distinct 'lab_cmp'	 as variable, valueset, code, display, system, encounter_ref, subject_ref  from irae__cohort_lab_cmp UNION
	select distinct 'lab_creatinine'	 as variable, valueset, code, display, system, encounter_ref, subject_ref  from irae__cohort_lab_creatinine UNION
	select distinct 'lab_diabetes'	 as variable, valueset, code, display, system, encounter_ref, subject_ref  from irae__cohort_lab_diabetes UNION
	select distinct 'lab_gfr'	 as variable, valueset, code, display, system, encounter_ref, subject_ref  from irae__cohort_lab_gfr UNION
	select distinct 'lab_lft'	 as variable, valueset, code, display, system, encounter_ref, subject_ref  from irae__cohort_lab_lft UNION
	select distinct 'proc_dialysis'	 as variable, valueset, code, display, system, encounter_ref, subject_ref  from irae__cohort_proc_dialysis UNION
	select distinct 'proc_surgery'	 as variable, valueset, code, display, system, encounter_ref, subject_ref  from irae__cohort_proc_surgery UNION
	select distinct 'rx_antibiotics'	 as variable, valueset, code, display, system, encounter_ref, subject_ref  from irae__cohort_rx_antibiotics UNION
	select distinct 'rx_cancer'	 as variable, valueset, code, display, system, encounter_ref, subject_ref  from irae__cohort_rx_cancer UNION
	select distinct 'rx_diabetes'	 as variable, valueset, code, display, system, encounter_ref, subject_ref  from irae__cohort_rx_diabetes UNION
	select distinct 'rx_diuretics'	 as variable, valueset, code, display, system, encounter_ref, subject_ref  from irae__cohort_rx_diuretics UNION
	select distinct 'rx_htn'	 as variable, valueset, code, display, system, encounter_ref, subject_ref  from irae__cohort_rx_htn UNION
	select distinct 'rx_immunocompromised'	 as variable, valueset, code, display, system, encounter_ref, subject_ref  from irae__cohort_rx_immunocompromised UNION
	select distinct 'rx_immunosuppressive'	 as variable, valueset, code, display, system, encounter_ref, subject_ref  from irae__cohort_rx_immunosuppressive UNION
	select distinct 'lab_custom'	 as variable, valueset, code, display, system, encounter_ref, subject_ref  from irae__cohort_lab_custom UNION
	select distinct 'rx_custom'	 as variable, valueset, code, display, system, encounter_ref, subject_ref  from irae__cohort_rx_custom
)
select distinct
    variable_cohorts.variable,
    variable_cohorts.valueset,
    variable_cohorts.code,
    variable_cohorts.display,
    variable_cohorts.system,
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
    variable_cohorts,
    irae__cohort_study_population as SP
where
    variable_cohorts.encounter_ref = SP.encounter_ref
;

