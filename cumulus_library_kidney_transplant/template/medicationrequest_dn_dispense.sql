CREATE TABLE {{ prefix }}__medicationrequest_dn_dispense  as
-- https://github.com/smart-on-fhir/cumulus/issues/66
WITH    workaround AS
(
    SELECT  DISTINCT
            CAST(dispenseRequest.validityPeriod AS json) AS validityPeriod,
            dispenseRequest.numberOfRepeatsAllowed,
            dispenseRequest.expectedSupplyDuration,
            dispenseRequest.quantity,
            mr.id,
            sp.medicationrequest_ref
    FROM    medicationRequest AS mr
    JOIN    {{ prefix }}__cohort_study_population_rx AS sp            
            ON sp.medicationrequest_ref = concat('MedicationRequest/', mr.id)
)
SELECT  DISTINCT
        DATE(from_iso8601_timestamp(json_extract_scalar(validityPeriod, '$.start')))    AS validity_start_date,
        DATE(from_iso8601_timestamp(json_extract_scalar(validityPeriod, '$.end')))      AS validity_end_date,
        numberOfRepeatsAllowed,
        expectedSupplyDuration."code"   AS duration_code,
        expectedSupplyDuration."system" AS duration_system,
        expectedSupplyDuration."unit"   AS duration_unit,
        expectedSupplyDuration."value"  AS duration_value,
        quantity."unit"                 AS quantity_unit,
        quantity."value"                AS quantity_value,
        expectedSupplyDuration,
        id,
        medicationrequest_ref
FROM    workaround;
