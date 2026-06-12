CREATE TABLE irae__highlights_longitudinal AS
    SELECT
        src.note_ref,
        src.subject_ref,
        src.generated_on,
        src.task_version,
        src.system_fingerprint,
        'irae__nlp_longitudinal_gpt_oss_120b' AS origin,
        'Rx Therapeutic' AS label,
        CONCAT(CAST(span[1] AS VARCHAR), ':', CAST(span[2] AS VARCHAR)) AS span,
        -- Handle sublabel_name and sublabel_value per rx_therapeutic_status_mention
        'Rx Therapeutic' AS sublabel_name,
        CAST(src.result.rx_therapeutic_status_mention.rx_therapeutic_status AS VARCHAR) AS sublabel_value
    FROM 
        irae__nlp_longitudinal_gpt_oss_120b AS src, 
        UNNEST(src.result.rx_therapeutic_status_mention.spans) AS t3(span)
    -- Custom filtering per mention_key
    WHERE
        src.result.rx_therapeutic_status_mention.rx_therapeutic_status != 'None of the above'

    UNION ALL
    SELECT
        src.note_ref,
        src.subject_ref,
        src.generated_on,
        src.task_version,
        src.system_fingerprint,
        'irae__nlp_longitudinal_gpt_oss_120b' AS origin,
        'Rx Compliance' AS label,
        CONCAT(CAST(span[1] AS VARCHAR), ':', CAST(span[2] AS VARCHAR)) AS span,
        -- Handle sublabel_name and sublabel_value per rx_compliance_mention
        'Rx Compliance' AS sublabel_name,
        CAST(src.result.rx_compliance_mention.rx_compliance AS VARCHAR) AS sublabel_value
    FROM 
        irae__nlp_longitudinal_gpt_oss_120b AS src, 
        UNNEST(src.result.rx_compliance_mention.spans) AS t3(span)
    -- Custom filtering per mention_key
    WHERE
        src.result.rx_compliance_mention.rx_compliance != 'None of the above'

    UNION ALL
    SELECT
        src.note_ref,
        src.subject_ref,
        src.generated_on,
        src.task_version,
        src.system_fingerprint,
        'irae__nlp_longitudinal_gpt_oss_120b' AS origin,
        'DSA' AS label,
        CONCAT(CAST(span[1] AS VARCHAR), ':', CAST(span[2] AS VARCHAR)) AS span,
        -- Handle sublabel_name and sublabel_value per dsa_mention
        'DSA' AS sublabel_name,
        CAST(src.result.dsa_mention.dsa AS VARCHAR) AS sublabel_value
    FROM 
        irae__nlp_longitudinal_gpt_oss_120b AS src, 
        UNNEST(src.result.dsa_mention.spans) AS t3(span)
    -- Custom filtering per mention_key
    WHERE 
        src.result.dsa_mention.dsa_history
        AND src.result.dsa_mention.dsa != 'None of the above'

    UNION ALL
    SELECT
        src.note_ref,
        src.subject_ref,
        src.generated_on,
        src.task_version,
        src.system_fingerprint,
        'irae__nlp_longitudinal_gpt_oss_120b' AS origin,
        'Infection' AS label,
        CONCAT(CAST(span[1] AS VARCHAR), ':', CAST(span[2] AS VARCHAR)) AS span,
        -- Handle sublabel_name and sublabel_value per infection_mention
        'Infection' AS sublabel_name,
        CAST(src.result.infection_mention.infection AS VARCHAR) AS sublabel_value
    FROM 
        irae__nlp_longitudinal_gpt_oss_120b AS src, 
        UNNEST(src.result.infection_mention.spans) AS t3(span)
    -- Custom filtering per mention_key
    WHERE 
        src.result.infection_mention.infection_history
        AND src.result.infection_mention.infection != 'None of the above'

    UNION ALL
    SELECT
        src.note_ref,
        src.subject_ref,
        src.generated_on,
        src.task_version,
        src.system_fingerprint,
        'irae__nlp_longitudinal_gpt_oss_120b' AS origin,
        'Viral' AS label,
        CONCAT(CAST(span[1] AS VARCHAR), ':', CAST(span[2] AS VARCHAR)) AS span,
        -- Handle sublabel_name and sublabel_value per viral_infection_mention
        'Viral' AS sublabel_name,
        CAST(src.result.viral_infection_mention.viral_infection AS VARCHAR) AS sublabel_value
    FROM 
        irae__nlp_longitudinal_gpt_oss_120b AS src, 
        UNNEST(src.result.viral_infection_mention.spans) AS t3(span)
    -- Custom filtering per mention_key
    WHERE 
        src.result.viral_infection_mention.viral_infection_history
        AND src.result.viral_infection_mention.viral_infection != 'None of the above'

    UNION ALL
    SELECT
        src.note_ref,
        src.subject_ref,
        src.generated_on,
        src.task_version,
        src.system_fingerprint,
        'irae__nlp_longitudinal_gpt_oss_120b' AS origin,
        'Bacterial' AS label,
        CONCAT(CAST(span[1] AS VARCHAR), ':', CAST(span[2] AS VARCHAR)) AS span,
        -- Handle sublabel_name and sublabel_value per bacterial_infection_mention
        'Bacterial' AS sublabel_name,
        CAST(src.result.bacterial_infection_mention.bacterial_infection AS VARCHAR) AS sublabel_value
    FROM 
        irae__nlp_longitudinal_gpt_oss_120b AS src, 
        UNNEST(src.result.bacterial_infection_mention.spans) AS t3(span)
    -- Custom filtering per mention_key
    WHERE 
        src.result.bacterial_infection_mention.bacterial_infection_history
        AND src.result.bacterial_infection_mention.bacterial_infection != 'None of the above'

    UNION ALL
    SELECT
        src.note_ref,
        src.subject_ref,
        src.generated_on,
        src.task_version,
        src.system_fingerprint,
        'irae__nlp_longitudinal_gpt_oss_120b' AS origin,
        'Fungal' AS label,
        CONCAT(CAST(span[1] AS VARCHAR), ':', CAST(span[2] AS VARCHAR)) AS span,
        -- Handle sublabel_name and sublabel_value per fungal_infection_mention
        'Fungal' AS sublabel_name,
        CAST(src.result.fungal_infection_mention.fungal_infection AS VARCHAR) AS sublabel_value
    FROM 
        irae__nlp_longitudinal_gpt_oss_120b AS src, 
        UNNEST(src.result.fungal_infection_mention.spans) AS t3(span)
    -- Custom filtering per mention_key
    WHERE 
        src.result.fungal_infection_mention.fungal_infection_history
        AND src.result.fungal_infection_mention.fungal_infection != 'None of the above'

    UNION ALL
    SELECT
        src.note_ref,
        src.subject_ref,
        src.generated_on,
        src.task_version,
        src.system_fingerprint,
        'irae__nlp_longitudinal_gpt_oss_120b' AS origin,
        'Graft Rejection' AS label,
        CONCAT(CAST(span[1] AS VARCHAR), ':', CAST(span[2] AS VARCHAR)) AS span,
        -- Handle sublabel_name and sublabel_value per graft_rejection_mention
        'Graft Rejection' AS sublabel_name,
        CAST(src.result.graft_rejection_mention.graft_rejection AS VARCHAR) AS sublabel_value
    FROM 
        irae__nlp_longitudinal_gpt_oss_120b AS src, 
        UNNEST(src.result.graft_rejection_mention.spans) AS t3(span)
    -- Custom filtering per mention_key
    WHERE 
        src.result.graft_rejection_mention.graft_rejection_history
        AND src.result.graft_rejection_mention.graft_rejection != 'None of the above'

    UNION ALL
    SELECT
        src.note_ref,
        src.subject_ref,
        src.generated_on,
        src.task_version,
        src.system_fingerprint,
        'irae__nlp_longitudinal_gpt_oss_120b' AS origin,
        'Graft Failure' AS label,
        CONCAT(CAST(span[1] AS VARCHAR), ':', CAST(span[2] AS VARCHAR)) AS span,
        -- Handle sublabel_name and sublabel_value per graft_failure_mention
        'Graft Failure' AS sublabel_name,
        CAST(src.result.graft_failure_mention.graft_failure AS VARCHAR) AS sublabel_value
    FROM 
        irae__nlp_longitudinal_gpt_oss_120b AS src, 
        UNNEST(src.result.graft_failure_mention.spans) AS t3(span)
    -- Custom filtering per mention_key
    WHERE 
        src.result.graft_failure_mention.graft_failure_history
        AND src.result.graft_failure_mention.graft_failure != 'None of the above'

    UNION ALL
    SELECT
        src.note_ref,
        src.subject_ref,
        src.generated_on,
        src.task_version,
        src.system_fingerprint,
        'irae__nlp_longitudinal_gpt_oss_120b' AS origin,
        'PTLD' AS label,
        CONCAT(CAST(span[1] AS VARCHAR), ':', CAST(span[2] AS VARCHAR)) AS span,
        -- Handle sublabel_name and sublabel_value per ptld_mention
        'PTLD' AS sublabel_name,
        CAST(src.result.ptld_mention.ptld AS VARCHAR) AS sublabel_value
    FROM 
        irae__nlp_longitudinal_gpt_oss_120b AS src, 
        UNNEST(src.result.ptld_mention.spans) AS t3(span)
    -- Custom filtering per mention_key
    WHERE 
        src.result.ptld_mention.ptld_history
        AND src.result.ptld_mention.ptld != 'None of the above'

    UNION ALL
    SELECT
        src.note_ref,
        src.subject_ref,
        src.generated_on,
        src.task_version,
        src.system_fingerprint,
        'irae__nlp_longitudinal_gpt_oss_120b' AS origin,
        'Cancer' AS label,
        CONCAT(CAST(span[1] AS VARCHAR), ':', CAST(span[2] AS VARCHAR)) AS span,
        -- Handle sublabel_name and sublabel_value per cancer_mention
        'Cancer' AS sublabel_name,
        CAST(src.result.cancer_mention.cancer AS VARCHAR) AS sublabel_value
    FROM 
        irae__nlp_longitudinal_gpt_oss_120b AS src, 
        UNNEST(src.result.cancer_mention.spans) AS t3(span)
    -- Custom filtering per mention_key
    WHERE 
        src.result.cancer_mention.cancer_history
        AND src.result.cancer_mention.cancer != 'None of the above'

    UNION ALL
    SELECT
        src.note_ref,
        src.subject_ref,
        src.generated_on,
        src.task_version,
        src.system_fingerprint,
        'irae__nlp_longitudinal_gpt_oss_120b' AS origin,
        'Deceased' AS label,
        CONCAT(CAST(span[1] AS VARCHAR), ':', CAST(span[2] AS VARCHAR)) AS span,
        -- Handle sublabel_name and sublabel_value per deceased_mention
        'Deceased' AS sublabel_name,
        CAST(src.result.deceased_mention.deceased AS VARCHAR) AS sublabel_value
    FROM 
        irae__nlp_longitudinal_gpt_oss_120b AS src, 
        UNNEST(src.result.deceased_mention.spans) AS t3(span)
    -- Custom filtering per mention_key
    WHERE 
        src.result.deceased_mention.deceased IS NOT NULL
        AND src.result.deceased_mention.deceased

    
    -- Additional SELECT for deceased_mention.deceased_date
    UNION ALL 
    SELECT
        src.note_ref,
        src.subject_ref,
        'irae__nlp_longitudinal_gpt_oss_120b' AS origin,
        'deceased_mention' AS label,
        CONCAT(CAST(span[1] AS VARCHAR), ':', CAST(span[2] AS VARCHAR)) AS span,
        'Deceased Datetime' AS sublabel_name,
        src.result.deceased_mention.deceased_date AS sublabel_value
    FROM 
        irae__nlp_longitudinal_gpt_oss_120b AS src,
        UNNEST(src.result.deceased_mention.spans) AS t4(span)
    WHERE 
        src.result.deceased_mention.deceased IS NOT NULL
        AND src.result.deceased_mention.deceased 
