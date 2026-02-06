create table irae__cohort_variable_union as
with variable_cohorts as
(
	select 'doc_biopsy'	 as variable, code, display, system, encounter_ref  from irae__cohort_doc_biopsy UNION ALL
	select 'dx_autoimmune'	 as variable, code, display, system, encounter_ref  from irae__cohort_dx_autoimmune UNION ALL
	select 'dx_cancer'	 as variable, code, display, system, encounter_ref  from irae__cohort_dx_cancer UNION ALL
	select 'dx_immunocompromised'	 as variable, code, display, system, encounter_ref  from irae__cohort_dx_immunocompromised UNION ALL
	select 'dx_infection'	 as variable, code, display, system, encounter_ref  from irae__cohort_dx_infection UNION ALL
	select 'dx_kidney'	 as variable, code, display, system, encounter_ref  from irae__cohort_dx_kidney UNION ALL
	select 'dx_transplant'	 as variable, code, display, system, encounter_ref  from irae__cohort_dx_transplant UNION ALL
	select 'lab_autoimmune'	 as variable, code, display, system, encounter_ref  from irae__cohort_lab_autoimmune UNION ALL
	select 'lab_cbc'	 as variable, code, display, system, encounter_ref  from irae__cohort_lab_cbc UNION ALL
	select 'lab_cmp'	 as variable, code, display, system, encounter_ref  from irae__cohort_lab_cmp UNION ALL
	select 'lab_creatinine'	 as variable, code, display, system, encounter_ref  from irae__cohort_lab_creatinine UNION ALL
	select 'lab_diabetes'	 as variable, code, display, system, encounter_ref  from irae__cohort_lab_diabetes UNION ALL
	select 'lab_gfr'	 as variable, code, display, system, encounter_ref  from irae__cohort_lab_gfr UNION ALL
	select 'lab_lft'	 as variable, code, display, system, encounter_ref  from irae__cohort_lab_lft UNION ALL
	select 'proc_dialysis'	 as variable, code, display, system, encounter_ref  from irae__cohort_proc_dialysis UNION ALL
	select 'proc_nephrectomy'	 as variable, code, display, system, encounter_ref  from irae__cohort_proc_nephrectomy UNION ALL
	select 'proc_transplant'	 as variable, code, display, system, encounter_ref  from irae__cohort_proc_transplant UNION ALL
	select 'rx_antibiotics'	 as variable, code, display, system, encounter_ref  from irae__cohort_rx_antibiotics UNION ALL
	select 'rx_cancer'	 as variable, code, display, system, encounter_ref  from irae__cohort_rx_cancer UNION ALL
	select 'rx_diabetes'	 as variable, code, display, system, encounter_ref  from irae__cohort_rx_diabetes UNION ALL
	select 'rx_diuretics'	 as variable, code, display, system, encounter_ref  from irae__cohort_rx_diuretics UNION ALL
	select 'rx_htn'	 as variable, code, display, system, encounter_ref  from irae__cohort_rx_htn UNION ALL
	select 'rx_immunosuppressive'	 as variable, code, display, system, encounter_ref  from irae__cohort_rx_immunosuppressive UNION ALL
	select 'lab_custom'	 as variable, code, display, system, encounter_ref  from irae__cohort_lab_custom UNION ALL
	select 'rx_custom'	 as variable, code, display, system, encounter_ref  from irae__cohort_rx_custom
)
select distinct
    variable_cohorts.variable,
    variable_cohorts.code,
    variable_cohorts.display,
    variable_cohorts.system,
    SP.status,
    SP.age_at_visit,
    SP.gender,
    SP.race_display,
    SP.ethnicity_display,
    SP.enc_class_code,
    SP.enc_period_ordinal,
    SP.enc_period_start_day,
    SP.enc_period_end_day,
    SP.encounter_ref,
    SP.subject_ref
from
    variable_cohorts,
    irae__cohort_study_population as SP
where
    variable_cohorts.encounter_ref = SP.encounter_ref
;

