CREATE  TABLE irae__cohort_casedef_rx AS
SELECT  DISTINCT
        
        casedef.days_since,
        casedef.ordinal_since,
        casedef.casedef_period,
        variable_union.variable,
        rx.*
FROM    irae__cohort_casedef                AS casedef
JOIN    irae__cohort_study_population_rx    AS rx
ON      casedef.encounter_ref = rx.encounter_ref
LEFT JOIN irae__cohort_variable_union       AS variable_union
ON      rx.medicationrequest_ref = variable_union.resource_ref
;