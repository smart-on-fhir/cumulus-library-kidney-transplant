CREATE TABLE irae__llm_donor_highlights AS
    SELECT
        src.note_ref,
        src.subject_ref,
        src.generated_on,
        src.task_version,
        src.system_fingerprint,
        'irae__nlp_donor_gpt_oss_120b' AS origin,
        'Transplant Date' AS label,
        CONCAT(CAST(span[1] AS VARCHAR), ':', CAST(span[2] AS VARCHAR)) AS span,
        -- Handle sublabel_name and sublabel_value per donor_transplant_date_mention
        'Transplant Date' AS sublabel_name,
        CAST(src.result.donor_transplant_date_mention.donor_transplant_date AS VARCHAR) AS sublabel_value
    FROM 
        irae__nlp_donor_gpt_oss_120b AS src, 
        UNNEST(src.result.donor_transplant_date_mention.spans) AS t3(span)
    -- Custom filtering per mention_key
    WHERE
        src.task_version = 8
        AND src.result.donor_transplant_date_mention IS NOT NULL
        AND src.result.donor_transplant_date_mention.donor_transplant_date IS NOT NULL
    UNION ALL
    SELECT
        src.note_ref,
        src.subject_ref,
        src.generated_on,
        src.task_version,
        src.system_fingerprint,
        'irae__nlp_donor_gpt_oss_120b' AS origin,
        'Donor Type' AS label,
        CONCAT(CAST(span[1] AS VARCHAR), ':', CAST(span[2] AS VARCHAR)) AS span,
        -- Handle sublabel_name and sublabel_value per donor_type_mention
        'Donor Type' AS sublabel_name,
        CAST(src.result.donor_type_mention.donor_type AS VARCHAR) AS sublabel_value
    FROM 
        irae__nlp_donor_gpt_oss_120b AS src, 
        UNNEST(src.result.donor_type_mention.spans) AS t3(span)
    -- Custom filtering per mention_key
    WHERE
        src.task_version = 8
        AND src.result.donor_type_mention IS NOT NULL
        AND src.result.donor_type_mention.donor_type != 'NOT_MENTIONED'
    UNION ALL
    SELECT
        src.note_ref,
        src.subject_ref,
        src.generated_on,
        src.task_version,
        src.system_fingerprint,
        'irae__nlp_donor_gpt_oss_120b' AS origin,
        'Donor Relationship' AS label,
        CONCAT(CAST(span[1] AS VARCHAR), ':', CAST(span[2] AS VARCHAR)) AS span,
        -- Handle sublabel_name and sublabel_value per donor_relationship_mention
        'Donor Relationship' AS sublabel_name,
        CAST(src.result.donor_relationship_mention.donor_relationship AS VARCHAR) AS sublabel_value
    FROM 
        irae__nlp_donor_gpt_oss_120b AS src, 
        UNNEST(src.result.donor_relationship_mention.spans) AS t3(span)
    -- Custom filtering per mention_key
    WHERE
        src.task_version = 8
        AND src.result.donor_relationship_mention IS NOT NULL
        AND src.result.donor_relationship_mention.donor_relationship != 'NOT_MENTIONED'
    UNION ALL
    SELECT
        src.note_ref,
        src.subject_ref,
        src.generated_on,
        src.task_version,
        src.system_fingerprint,
        'irae__nlp_donor_gpt_oss_120b' AS origin,
        'Hla Match Quality' AS label,
        CONCAT(CAST(span[1] AS VARCHAR), ':', CAST(span[2] AS VARCHAR)) AS span,
        -- Handle sublabel_name and sublabel_value per donor_hla_match_quality_mention
        'Hla Match Quality' AS sublabel_name,
        CAST(src.result.donor_hla_match_quality_mention.donor_hla_match_quality AS VARCHAR) AS sublabel_value
    FROM 
        irae__nlp_donor_gpt_oss_120b AS src, 
        UNNEST(src.result.donor_hla_match_quality_mention.spans) AS t3(span)
    -- Custom filtering per mention_key
    WHERE
        src.task_version = 8
        AND src.result.donor_hla_match_quality_mention IS NOT NULL
        AND src.result.donor_hla_match_quality_mention.donor_hla_match_quality != 'NOT_MENTIONED'
    UNION ALL
    SELECT
        src.note_ref,
        src.subject_ref,
        src.generated_on,
        src.task_version,
        src.system_fingerprint,
        'irae__nlp_donor_gpt_oss_120b' AS origin,
        'Hla Mismatch Count' AS label,
        CONCAT(CAST(span[1] AS VARCHAR), ':', CAST(span[2] AS VARCHAR)) AS span,
        -- Handle sublabel_name and sublabel_value per donor_hla_mismatch_count_mention
        'Hla Mismatch Count' AS sublabel_name,
        CAST(src.result.donor_hla_mismatch_count_mention.donor_hla_mismatch_count AS VARCHAR) AS sublabel_value
    FROM 
        irae__nlp_donor_gpt_oss_120b AS src, 
        UNNEST(src.result.donor_hla_mismatch_count_mention.spans) AS t3(span)
    -- Custom filtering per mention_key
    WHERE
        src.task_version = 8
        AND src.result.donor_hla_mismatch_count_mention IS NOT NULL
        AND src.result.donor_hla_mismatch_count_mention.donor_hla_mismatch_count != 'NOT_MENTIONED'
    UNION ALL
    SELECT
        src.note_ref,
        src.subject_ref,
        src.generated_on,
        src.task_version,
        src.system_fingerprint,
        'irae__nlp_donor_gpt_oss_120b' AS origin,
        'Donor Serostatus' AS label,
        CONCAT(CAST(span[1] AS VARCHAR), ':', CAST(span[2] AS VARCHAR)) AS span,
        -- Handle sublabel_name and sublabel_value per donor_serostatus_mention
        'Donor Serostatus' AS sublabel_name,
        CAST(src.result.donor_serostatus_mention.serostatus AS VARCHAR) AS sublabel_value
    FROM 
        irae__nlp_donor_gpt_oss_120b AS src, 
        UNNEST(src.result.donor_serostatus_mention.spans) AS t3(span)
    -- Custom filtering per mention_key
    WHERE
        src.task_version = 8
        AND src.result.donor_serostatus_mention IS NOT NULL
        AND src.result.donor_serostatus_mention.serostatus != 'NOT_MENTIONED'
    UNION ALL
    SELECT
        src.note_ref,
        src.subject_ref,
        src.generated_on,
        src.task_version,
        src.system_fingerprint,
        'irae__nlp_donor_gpt_oss_120b' AS origin,
        'Donor Serostatus CMV' AS label,
        CONCAT(CAST(span[1] AS VARCHAR), ':', CAST(span[2] AS VARCHAR)) AS span,
        -- Handle sublabel_name and sublabel_value per donor_serostatus_cmv_mention
        'Donor Serostatus CMV' AS sublabel_name,
        CAST(src.result.donor_serostatus_cmv_mention.serostatus AS VARCHAR) AS sublabel_value
    FROM 
        irae__nlp_donor_gpt_oss_120b AS src, 
        UNNEST(src.result.donor_serostatus_cmv_mention.spans) AS t3(span)
    -- Custom filtering per mention_key
    WHERE
        src.task_version = 8
        AND src.result.donor_serostatus_cmv_mention IS NOT NULL
        AND src.result.donor_serostatus_cmv_mention.serostatus != 'NOT_MENTIONED'
    UNION ALL
    SELECT
        src.note_ref,
        src.subject_ref,
        src.generated_on,
        src.task_version,
        src.system_fingerprint,
        'irae__nlp_donor_gpt_oss_120b' AS origin,
        'Donor Serostatus EBV' AS label,
        CONCAT(CAST(span[1] AS VARCHAR), ':', CAST(span[2] AS VARCHAR)) AS span,
        -- Handle sublabel_name and sublabel_value per donor_serostatus_ebv_mention
        'Donor Serostatus EBV' AS sublabel_name,
        CAST(src.result.donor_serostatus_ebv_mention.serostatus AS VARCHAR) AS sublabel_value
    FROM 
        irae__nlp_donor_gpt_oss_120b AS src, 
        UNNEST(src.result.donor_serostatus_ebv_mention.spans) AS t3(span)
    -- Custom filtering per mention_key
    WHERE
        src.task_version = 8
        AND src.result.donor_serostatus_ebv_mention IS NOT NULL
        AND src.result.donor_serostatus_ebv_mention.serostatus != 'NOT_MENTIONED'
    UNION ALL
    SELECT
        src.note_ref,
        src.subject_ref,
        src.generated_on,
        src.task_version,
        src.system_fingerprint,
        'irae__nlp_donor_gpt_oss_120b' AS origin,
        'Recipient Serostatus' AS label,
        CONCAT(CAST(span[1] AS VARCHAR), ':', CAST(span[2] AS VARCHAR)) AS span,
        -- Handle sublabel_name and sublabel_value per recipient_serostatus_mention
        'Recipient Serostatus' AS sublabel_name,
        CAST(src.result.recipient_serostatus_mention.serostatus AS VARCHAR) AS sublabel_value
    FROM 
        irae__nlp_donor_gpt_oss_120b AS src, 
        UNNEST(src.result.recipient_serostatus_mention.spans) AS t3(span)
    -- Custom filtering per mention_key
    WHERE
        src.task_version = 8
        AND src.result.recipient_serostatus_mention IS NOT NULL
        AND src.result.recipient_serostatus_mention.serostatus != 'NOT_MENTIONED'
    UNION ALL
    SELECT
        src.note_ref,
        src.subject_ref,
        src.generated_on,
        src.task_version,
        src.system_fingerprint,
        'irae__nlp_donor_gpt_oss_120b' AS origin,
        'Recipient Serostatus CMV' AS label,
        CONCAT(CAST(span[1] AS VARCHAR), ':', CAST(span[2] AS VARCHAR)) AS span,
        -- Handle sublabel_name and sublabel_value per recipient_serostatus_cmv_mention
        'Recipient Serostatus CMV' AS sublabel_name,
        CAST(src.result.recipient_serostatus_cmv_mention.serostatus AS VARCHAR) AS sublabel_value
    FROM 
        irae__nlp_donor_gpt_oss_120b AS src, 
        UNNEST(src.result.recipient_serostatus_cmv_mention.spans) AS t3(span)
    -- Custom filtering per mention_key
    WHERE
        src.task_version = 8
        AND src.result.recipient_serostatus_cmv_mention IS NOT NULL
        AND src.result.recipient_serostatus_cmv_mention.serostatus != 'NOT_MENTIONED'
    UNION ALL
    SELECT
        src.note_ref,
        src.subject_ref,
        src.generated_on,
        src.task_version,
        src.system_fingerprint,
        'irae__nlp_donor_gpt_oss_120b' AS origin,
        'Recipient Serostatus EBV' AS label,
        CONCAT(CAST(span[1] AS VARCHAR), ':', CAST(span[2] AS VARCHAR)) AS span,
        -- Handle sublabel_name and sublabel_value per recipient_serostatus_ebv_mention
        'Recipient Serostatus EBV' AS sublabel_name,
        CAST(src.result.recipient_serostatus_ebv_mention.serostatus AS VARCHAR) AS sublabel_value
    FROM 
        irae__nlp_donor_gpt_oss_120b AS src, 
        UNNEST(src.result.recipient_serostatus_ebv_mention.spans) AS t3(span)
    -- Custom filtering per mention_key
    WHERE
        src.task_version = 8
        AND src.result.recipient_serostatus_ebv_mention IS NOT NULL
        AND src.result.recipient_serostatus_ebv_mention.serostatus != 'NOT_MENTIONED'
    
