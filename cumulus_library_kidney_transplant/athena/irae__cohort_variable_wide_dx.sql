CREATE  TABLE    irae__cohort_variable_wide_dx AS
SELECT  DISTINCT
,
encounter_ref,
subject_ref
FROM    irae__cohort_variable_union_dx
;