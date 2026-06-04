CREATE TABLE irae__cohort_variable_union_proc AS
SELECT DISTINCT
        var.variable,
        var.code,
        var.display,
        var.system,
        proc.*
FROM    irae__cohort_variable_union         AS var
JOIN    irae__cohort_study_population_proc  AS proc
ON      var.resource_ref = dx.condition_ref
AND     var.system = proc.proc_system
AND     var.code = proc.proc_code
WHERE   var.variable IN
(
 'proc_nephrectomy'
,'proc_transplant'
);