CREATE TABLE irae__count_enc_study_population_lab AS (
    WITH
    filtered_table AS (
        SELECT
            s.subject_ref,
            s.encounter_ref,
            --noqa: disable=RF03, AL02
            s."lab_observation_code"
            --noqa: enable=RF03, AL02
        FROM irae__cohort_study_population_lab AS s
        WHERE s.status = 'finished'
    ),
    
    null_replacement AS (
        SELECT
            subject_ref,
            encounter_ref,
            coalesce(
                cast(lab_observation_code AS varchar),
                'cumulus__none'
            ) AS lab_observation_code
        FROM filtered_table
    ),
    secondary_powerset AS (
        SELECT
            count(DISTINCT encounter_ref) AS cnt_encounter_ref,
            "lab_observation_code",
            concat_ws(
                '-',
                COALESCE("lab_observation_code",'')
            ) AS id
        FROM null_replacement
        GROUP BY
            cube(
            "lab_observation_code"
            )
    ),

    powerset AS (
        SELECT
            count(DISTINCT subject_ref) AS cnt_subject_ref,
            "lab_observation_code",
            concat_ws(
                '-',
                COALESCE("lab_observation_code",'')
            ) AS id
        FROM null_replacement
        GROUP BY
            cube(
            "lab_observation_code"
            )
    )

    SELECT
        s.cnt_encounter_ref AS cnt,
        p."lab_observation_code"
    FROM powerset AS p
    JOIN secondary_powerset AS s on s.id = p.id
    WHERE 
        cnt_subject_ref >= 10
);