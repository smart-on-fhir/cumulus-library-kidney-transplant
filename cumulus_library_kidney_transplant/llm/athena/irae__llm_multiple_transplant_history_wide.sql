CREATE TABLE irae__llm_multiple_transplant_history_wide AS
SELECT DISTINCT
    nlp.note_ref,
    nlp.subject_ref,
    'irae__nlp_multiple_transplant_history_gpt_oss_120b' AS origin,
    nlp.generated_on,
    nlp.task_version,
    nlp.system_fingerprint,
    -- Multiple Transplant History
    nlp.result.multiple_transplant_history_mention.multiple_transplant_history
FROM
    irae__nlp_multiple_transplant_history_gpt_oss_120b AS nlp
WHERE
    task_version = 6
