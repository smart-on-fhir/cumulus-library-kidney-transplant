CREATE TABLE irae__count_pat_study_population_lab AS (
    WITH
    filtered_table AS (
        SELECT
            s.subject_ref,
            --noqa: disable=RF03, AL02
            s."lab_observation_code",
            s."enc_class_code",
            s."gender",
            s."age_at_visit"
            --noqa: enable=RF03, AL02
        FROM irae__cohort_study_population_lab AS s
    ),
    
    null_replacement AS (
        SELECT
            subject_ref,
            coalesce(
                cast(lab_observation_code AS varchar),
                'cumulus__none'
            ) AS lab_observation_code,
            coalesce(
                cast(enc_class_code AS varchar),
                'cumulus__none'
            ) AS enc_class_code,
            coalesce(
                cast(gender AS varchar),
                'cumulus__none'
            ) AS gender,
            coalesce(
                cast(age_at_visit AS varchar),
                'cumulus__none'
            ) AS age_at_visit
        FROM filtered_table
    ),

    powerset AS (
        SELECT
            count(DISTINCT subject_ref) AS cnt_subject_ref,
            "lab_observation_code",
            "enc_class_code",
            "gender",
            "age_at_visit",
            concat_ws(
                '-',
                COALESCE("lab_observation_code",''),
                COALESCE("enc_class_code",''),
                COALESCE("gender",''),
                COALESCE("age_at_visit",'')
            ) AS id
        FROM null_replacement
        GROUP BY
            cube(
            "lab_observation_code",
            "enc_class_code",
            "gender",
            "age_at_visit"
            )
    )

    SELECT
        p.cnt_subject_ref AS cnt,
        p."lab_observation_code",
        p."enc_class_code",
        p."gender",
        p."age_at_visit"
    FROM powerset AS p
    WHERE 
        cnt_subject_ref >= 10
);