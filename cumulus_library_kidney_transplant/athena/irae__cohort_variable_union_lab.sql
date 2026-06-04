CREATE  TABLE   irae__cohort_variable_union_lab AS
SELECT  DISTINCT
        var.variable,
        var.code,
        var.display,
        var.system,
        lab.*
FROM    irae__cohort_variable_union          AS var
JOIN    irae__cohort_study_population_lab    AS lab
ON      var.resource_ref = lab.observation_ref
AND     var.system = lab.lab_observation_system
AND     var.code = lab.lab_observation_code
WHERE   var.variable IN
(
 'lab_albumin'
,'lab_crp'
,'lab_drug_level_azathioprine'
,'lab_drug_level_cyclosporin'
,'lab_drug_level_mycophenolate'
,'lab_drug_level_sirolimus'
,'lab_drug_level_tacrolimus'
,'lab_esr'
,'lab_gfr_custom'
,'lab_hla'
,'lab_infection_viral_cmv'
,'lab_iron_ferritin'
,'lab_tpmt_gene'
);