CREATE TABLE {{ prefix }}__medicationrequest_dn_dosage_route as
select  distinct
        rc."code"       AS route_code,
        rc."display"    AS route_display,
        rc."system"     AS route_system,
        di.route,
        id, concat('MedicationRequest', id) AS medicationrequest_ref
FROM    {{ prefix }}__cohort_study_population_rx AS SP,
        medicationRequest           AS mr,
        UNNEST(dosageInstruction)   AS t(DI),
        UNNEST(di.route.coding)     AS t(RC)
WHERE   sp.medicationrequest_ref = concat('MedicationRequest/', MR.id);
