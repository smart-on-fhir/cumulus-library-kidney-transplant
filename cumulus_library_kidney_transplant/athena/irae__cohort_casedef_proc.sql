CREATE  TABLE irae__cohort_casedef_proc as
SELECT  DISTINCT
        casedef.subtype,
        casedef.days_since,
        casedef.ordinal_since,
        casedef.casedef_period,
        proc.*
FROM    irae__cohort_casedef as casedef
JOIN    irae__cohort_study_population_proc as proc
ON      casedef.encounter_ref = proc.encounter_ref
;