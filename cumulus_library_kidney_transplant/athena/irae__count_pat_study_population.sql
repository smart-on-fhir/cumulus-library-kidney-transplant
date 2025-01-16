CREATE TABLE irae__count_pat_study_population AS (
    WITH
    filtered_table AS (
        SELECT
            s.subject_ref,
            --noqa: disable=RF03, AL02
            s."enc_class_code",
            s."age_at_visit",
            s."race_display",
            s."ethnicity_display",
            s."gender"
            --noqa: enable=RF03, AL02
        FROM irae__cohort_study_population AS s
    ),
    
    null_replacement AS (
        SELECT
            subject_ref,
            coalesce(
                cast(enc_class_code AS varchar),
                'cumulus__none'
            ) AS enc_class_code,
            coalesce(
                cast(age_at_visit AS varchar),
                'cumulus__none'
            ) AS age_at_visit,
            coalesce(
                cast(race_display AS varchar),
                'cumulus__none'
            ) AS race_display,
            coalesce(
                cast(ethnicity_display AS varchar),
                'cumulus__none'
            ) AS ethnicity_display,
            coalesce(
                cast(gender AS varchar),
                'cumulus__none'
            ) AS gender
        FROM filtered_table
    ),

    powerset AS (
        SELECT
            count(DISTINCT subject_ref) AS cnt_subject_ref,
            "enc_class_code",
            "age_at_visit",
            "race_display",
            "ethnicity_display",
            "gender",
            concat_ws(
                '-',
                COALESCE("enc_class_code",''),
                COALESCE("age_at_visit",''),
                COALESCE("race_display",''),
                COALESCE("ethnicity_display",''),
                COALESCE("gender",'')
            ) AS id
        FROM null_replacement
        GROUP BY
            cube(
            "enc_class_code",
            "age_at_visit",
            "race_display",
            "ethnicity_display",
            "gender"
            )
    )

    SELECT
        p.cnt_subject_ref AS cnt,
        p."enc_class_code",
        p."age_at_visit",
        p."race_display",
        p."ethnicity_display",
        p."gender"
    FROM powerset AS p
    WHERE 
        cnt_subject_ref >= 10
);