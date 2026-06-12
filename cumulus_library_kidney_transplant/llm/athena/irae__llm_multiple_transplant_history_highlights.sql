CREATE TABLE irae__highlights_multiple_transplant_history AS
    SELECT
        src.note_ref,
        src.subject_ref,
        src.generated_on,
        src.task_version,
        src.system_fingerprint,
        'irae__nlp_multiple_transplant_history_gpt_oss_120b' AS origin,
        'Multiple Transplant History' AS label,
        CONCAT(CAST(span[1] AS VARCHAR), ':', CAST(span[2] AS VARCHAR)) AS span,
        -- Handle sublabel_name and sublabel_value per multiple_transplant_history_mention
        'Multiple Transplant History' AS sublabel_name,
        CAST(src.result.multiple_transplant_history_mention.multiple_transplant_history AS VARCHAR) AS sublabel_value
    FROM 
        irae__nlp_multiple_transplant_history_gpt_oss_120b AS src, 
        UNNEST(src.result.multiple_transplant_history_mention.spans) AS t3(span)
    -- Custom filtering per mention_key
    WHERE
        src.result.multiple_transplant_history_mention.multiple_transplant_history IS NOT NULL
        AND src.result.multiple_transplant_history_mention.multiple_transplant_history
    

