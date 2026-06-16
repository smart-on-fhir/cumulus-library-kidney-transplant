CREATE TABLE irae__llm_immunosuppressive_medications_highlights AS
-- One pass to get medication status information --
SELECT
    src.note_ref,
    src.subject_ref,
    src.generated_on,
    src.task_version,
    src.system_fingerprint,
    'irae__nlp_immunosuppressive_medications_gpt_oss_120b' AS origin,
    'Immunosuppressive Medication' AS label,
    CONCAT(CAST(span[1] AS VARCHAR), ':', CAST(span[2] AS VARCHAR)) AS span,
    'Medication Status' AS sublabel_name,
    medication.status AS sublabel_value
FROM 
    irae__nlp_immunosuppressive_medications_gpt_oss_120b AS src,
    UNNEST(src.result.immunosuppressive_medication_mentions) AS t1(medication),
    UNNEST(
        COALESCE(
            medication.spans, 
            CAST(ARRAY[ARRAY[]] AS ARRAY(ARRAY(INTEGER)))
        )
    ) AS t2(span)
WHERE 
    src.task_version = CAST('6' AS INT)
    AND medication.status <> 'None of the above'
-- Second pass to get medication ingredient information --
UNION ALL
SELECT
    src.note_ref,
    src.subject_ref,
    src.generated_on,
    src.task_version,
    src.system_fingerprint,
    'irae__nlp_immunosuppressive_medications_gpt_oss_120b' AS origin,
    'Immunosuppressive Medication' AS label,
    CONCAT(CAST(span[1] AS VARCHAR), ':', CAST(span[2] AS VARCHAR)) AS span,
    'Medication' AS sublabel_name,
    medication.ingredient AS sublabel_value
FROM 
    irae__nlp_immunosuppressive_medications_gpt_oss_120b AS src,
    UNNEST(src.result.immunosuppressive_medication_mentions) AS t1(medication),
    UNNEST(
        COALESCE(
            medication.spans, 
            CAST(ARRAY[ARRAY[]] AS ARRAY(ARRAY(INTEGER)))
        )
    ) AS t2(span)
WHERE 
    src.task_version = CAST('6' AS INT)
    AND medication.ingredient <> 'None of the above'
