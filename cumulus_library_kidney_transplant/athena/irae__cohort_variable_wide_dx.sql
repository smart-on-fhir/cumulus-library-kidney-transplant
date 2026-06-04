CREATE  TABLE    irae__cohort_variable_wide_dx AS
SELECT  DISTINCT
IF(variable='dx_transplant', dx_onset_date) as dx_transplant_onset,
IF(variable='dx_transplant', dx_category_code) as dx_transplant_category,
IF(variable='dx_transplant', dx_clinical_status) as dx_transplant_status,
IF(variable='dx_transplant', condition_ref) as dx_transplant_ref,
encounter_ref,
subject_ref
FROM    irae__cohort_variable_union_dx
;