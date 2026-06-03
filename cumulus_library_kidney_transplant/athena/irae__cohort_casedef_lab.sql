CREATE  TABLE irae__cohort_casedef_lab AS
SELECT  DISTINCT
        
        casedef.days_since,
        casedef.ordinal_since,
        casedef.casedef_period,
        variable_union.variable,
        lab.*
FROM    irae__cohort_casedef as casedef
JOIN    irae__cohort_study_population_lab as lab
ON      casedef.encounter_ref = lab.encounter_ref
LEFT JOIN irae__cohort_variable_union AS variable_union
ON      lab.observation_ref = variable_union.resource_ref
;