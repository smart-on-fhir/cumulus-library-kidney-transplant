CREATE TABLE irae__cohort_variable_union_rx AS
SELECT DISTINCT
        var.variable,
        var.code,
        var.display,
        var.system,
        rx.*
FROM    irae__cohort_variable_union      AS var
JOIN    irae__cohort_study_population_rx AS rx
ON      var.resource_ref = rx.medicationrequest_ref
AND     var.system = rx.rx_system
AND     var.code = rx.rx_code
WHERE   var.variable IN
(
 'rx_alemtuzumab'
,'rx_atg'
,'rx_azathioprine'
,'rx_basiliximab'
,'rx_belatacept'
,'rx_cyclosporin'
,'rx_cytogam'
,'rx_everolimus'
,'rx_ig'
,'rx_ivig'
,'rx_methylprednisolone'
,'rx_mycophenolate'
,'rx_prednisolone'
,'rx_prednisone'
,'rx_rituximab'
,'rx_sirolimus'
,'rx_tacrolimus'
);