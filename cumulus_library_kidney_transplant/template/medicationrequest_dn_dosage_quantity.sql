CREATE  TABLE {{ prefix }}__medicationrequest_dn_dosage_quantity AS
with    workaround AS
(
    SELECT  DISTINCT
            json_extract(CAST(DAR AS json), '$.dosequantity') AS doseQuantity,
            json_extract(CAST(DAR AS json), '$.ratequantity') AS rateQuantity,
            mr.id,
            sp.medicationrequest_ref
    FROM    {{ prefix }}__cohort_study_population_rx AS sp,
            medicationRequest           AS mr,
            UNNEST(dosageInstruction)   AS t(di),
            UNNEST(di.doseAndRate)      AS t(dar)
    WHERE   SP.medicationrequest_ref = concat('MedicationRequest/', mr.id)
),
guard_schema AS
(
    SELECT  TRY_CAST(doseQuantity AS ROW(code VARCHAR, system VARCHAR, unit VARCHAR, value DOUBLE)) AS doseQuantity,
            TRY_CAST(rateQuantity AS ROW(code VARCHAR, system VARCHAR, unit VARCHAR, value DOUBLE)) AS rateQuantity,
            id, medicationrequest_ref
    FROM    workaround
)
select  distinct
        doseQuantity."code"     AS dose_code,
        doseQuantity."system"   AS dose_system,
        doseQuantity."unit"     AS dose_unit,
        doseQuantity."value"    AS dose_value,
        doseQuantity,
        rateQuantity."code"     AS rate_code,
        rateQuantity."system"   AS rate_system,
        rateQuantity."unit"     AS rate_unit,
        rateQuantity."value"    AS rate_value,
        rateQuantity
        id, medicationrequest_ref
from    guard_schema; 

