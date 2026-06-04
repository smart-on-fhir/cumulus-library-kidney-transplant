CREATE TABLE irae__cohort_variable_union_diag AS
SELECT DISTINCT
        var.variable,
        var.code,
        var.display,
        var.system,
        diag.*
FROM    irae__cohort_variable_union          AS var
JOIN    irae__cohort_study_population_diag   AS diag
ON      var.resource_ref = diag.diagnosticreport_ref
AND     var.system = diag.diag_system
AND     var.code = diag.diag_code
WHERE   diag.diag_category_system in ('http://loinc.org', 'http://terminology.hl7.org/CodeSystem/v2-0074')
AND     var.variable IN
(
 
);