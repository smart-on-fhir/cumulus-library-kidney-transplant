CREATE TABLE irae__count_pat_study_population_rx AS (
    WITH
    filtered_table AS (
        SELECT
            s.subject_ref,
            --noqa: disable=RF03, AL02
            s."gender",
            s."rx_display",
            s."rx_category_code",
            s."age_at_visit",
            s."enc_class_code"
            --noqa: enable=RF03, AL02
        FROM irae__cohort_study_population_rx AS s
    ),
    
    null_replacement AS (
        SELECT
            subject_ref,
            coalesce(
                cast(gender AS varchar),
                'cumulus__none'
            ) AS gender,
            coalesce(
                cast(rx_display AS varchar),
                'cumulus__none'
            ) AS rx_display,
            coalesce(
                cast(rx_category_code AS varchar),
                'cumulus__none'
            ) AS rx_category_code,
            coalesce(
                cast(age_at_visit AS varchar),
                'cumulus__none'
            ) AS age_at_visit,
            coalesce(
                cast(enc_class_code AS varchar),
                'cumulus__none'
            ) AS enc_class_code
        FROM filtered_table
    ),

    powerset AS (
        SELECT
            count(DISTINCT subject_ref) AS cnt_subject_ref,
            "gender",
            "rx_display",
            "rx_category_code",
            "age_at_visit",
            "enc_class_code",
            concat_ws(
                '-',
                COALESCE("gender",''),
                COALESCE("rx_display",''),
                COALESCE("rx_category_code",''),
                COALESCE("age_at_visit",''),
                COALESCE("enc_class_code",'')
            ) AS id
        FROM null_replacement
        GROUP BY
            cube(
            "gender",
            "rx_display",
            "rx_category_code",
            "age_at_visit",
            "enc_class_code"
            )
    )

    SELECT
        p.cnt_subject_ref AS cnt,
        p."gender",
        p."rx_display",
        p."rx_category_code",
        p."age_at_visit",
        p."enc_class_code"
    FROM powerset AS p
    WHERE 
        cnt_subject_ref >= 10
);