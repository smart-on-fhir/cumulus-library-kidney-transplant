CREATE  TABLE irae__cohort_casedef_dx AS
SELECT  DISTINCT
        
        casedef.days_since,
        casedef.ordinal_since,
        casedef.casedef_period,
        variable_union.variable,
        dx.*
FROM    irae__cohort_casedef as casedef
JOIN    irae__cohort_study_population_dx as dx
ON      casedef.encounter_ref = dx.encounter_ref
LEFT JOIN irae__cohort_variable_union AS variable_union
ON      dx.condition_ref = variable_union.resource_ref
;