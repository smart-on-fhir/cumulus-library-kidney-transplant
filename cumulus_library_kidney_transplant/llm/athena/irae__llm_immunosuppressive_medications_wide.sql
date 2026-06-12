CREATE TABLE irae__llm_immunosuppressive_medications_wide AS
SELECT
    nlp.note_ref,
    nlp.subject_ref,
    'irae__nlp_immunosuppressive_medications_gpt_oss_120b' AS origin,
    nlp.generated_on,
    nlp.task_version,
    nlp.system_fingerprint,
    -- Medication identity
    medication.drug_class,
    medication.ingredient,
    -- Administration
    medication.status,
    medication.category,
    medication.route,
    medication.phase,
    medication.frequency,
    -- Dosing
    medication.quantity_value,
    medication.quantity_unit,
    -- Timing
    medication.start_date,
    medication.end_date,
    medication.expected_supply_days,
    medication.number_of_repeats_allowed
FROM
    irae__nlp_immunosuppressive_medications_gpt_oss_120b AS nlp,
    UNNEST(nlp.result.immunosuppressive_medication_mentions) AS t(medication)
WHERE
    task_version = 6
    AND medication.drug_class <> 'None of the above'
