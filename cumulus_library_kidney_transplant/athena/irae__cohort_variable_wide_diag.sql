CREATE  TABLE    irae__cohort_variable_wide_diag AS
SELECT  DISTINCT
,
encounter_ref,
subject_ref
FROM    irae__cohort_variable_union_diag
;