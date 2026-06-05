CREATE  TABLE    irae__cohort_variable_wide_proc AS
SELECT  DISTINCT
,
encounter_ref,
subject_ref
FROM    irae__cohort_variable_union_proc
;