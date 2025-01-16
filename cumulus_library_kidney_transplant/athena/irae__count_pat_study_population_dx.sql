CREATE TABLE irae__count_pat_study_population_dx AS (
    WITH
    filtered_table AS (
        SELECT
            s.subject_ref,
            --noqa: disable=RF03, AL02
            s."dx_display",
            s."gender",
            s."age_at_visit",
            s."enc_class_code",
            s."dx_category_code"
            --noqa: enable=RF03, AL02
        FROM irae__cohort_study_population_dx AS s
    ),
    
    null_replacement AS (
        SELECT
            subject_ref,
            coalesce(
                cast(dx_display AS varchar),
                'cumulus__none'
            ) AS dx_display,
            coalesce(
                cast(gender AS varchar),
                'cumulus__none'
            ) AS gender,
            coalesce(
                cast(age_at_visit AS varchar),
                'cumulus__none'
            ) AS age_at_visit,
            coalesce(
                cast(enc_class_code AS varchar),
                'cumulus__none'
            ) AS enc_class_code,
            coalesce(
                cast(dx_category_code AS varchar),
                'cumulus__none'
            ) AS dx_category_code
        FROM filtered_table
    ),

    powerset AS (
        SELECT
            count(DISTINCT subject_ref) AS cnt_subject_ref,
            "dx_display",
            "gender",
            "age_at_visit",
            "enc_class_code",
            "dx_category_code",
            concat_ws(
                '-',
                COALESCE("dx_display",''),
                COALESCE("gender",''),
                COALESCE("age_at_visit",''),
                COALESCE("enc_class_code",''),
                COALESCE("dx_category_code",'')
            ) AS id
        FROM null_replacement
        GROUP BY
            cube(
            "dx_display",
            "gender",
            "age_at_visit",
            "enc_class_code",
            "dx_category_code"
            )
    )

    SELECT
        p.cnt_subject_ref AS cnt,
        p."dx_display",
        p."gender",
        p."age_at_visit",
        p."enc_class_code",
        p."dx_category_code"
    FROM powerset AS p
    WHERE 
        cnt_subject_ref >= 10
);