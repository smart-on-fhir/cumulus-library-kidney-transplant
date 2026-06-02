CREATE  TABLE irae__cohort_variable_union_doc AS
SELECT  DISTINCT
        var.variable,
        var.code,
        var.display,
        var.system,
        doc.*
FROM    irae__cohort_variable_union          AS var
JOIN    irae__cohort_study_population_doc    AS doc
ON      var.resource_ref = doc.documentreference_ref
AND     var.system = doc.doc_type_system
AND     var.code = doc.doc_type_code
WHERE   var.variable IN
(
 
);
;