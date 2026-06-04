CREATE  TABLE {{ prefix }}__medicationrequest_dn_dosage_timing AS
SELECT  DISTINCT
        date(from_iso8601_timestamp(di.timing.repeat.boundsperiod."start")) AS timing_start_date,
        date(from_iso8601_timestamp(di.timing.repeat.boundsperiod."end"))   AS timing_end_date,
        di.timing.code.text                     AS timimg_text,
        di.timing.repeat.duration               AS repeat_duration,
        di.timing.repeat.durationUnit           AS repeat_durationunit,
        di.timing.repeat."count"                AS repeat_count,
        id, concat('MedicationRequest/', id)    AS medicationrequest_ref
FROM    {{ prefix }}__cohort_study_population_rx AS sp,
        medicationRequest                       AS mr,
        UNNEST(dosageInstruction)               AS t(di)
WHERE   SP.medicationrequest_ref = concat('MedicationRequest/', MR.id)
;