CREATE TABLE irae__count_pat_study_population_doc AS (
    WITH
    filtered_table AS (
        SELECT
            s.subject_ref,
            --noqa: disable=RF03, AL02
            s."doc_type_display",
            s."enc_class_code",
            s."gender",
            s."age_at_visit"
            --noqa: enable=RF03, AL02
        FROM irae__cohort_study_population_doc AS s
    ),
    
    null_replacement AS (
        SELECT
            subject_ref,
            coalesce(
                cast(doc_type_display AS varchar),
                'cumulus__none'
            ) AS doc_type_display,
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
            "doc_type_display",
            "enc_class_code",
            "gender",
            "age_at_visit",
            concat_ws(
                '-',
                COALESCE("doc_type_display",''),
                COALESCE("enc_class_code",''),
                COALESCE("gender",''),
                COALESCE("age_at_visit",'')
            ) AS id
        FROM null_replacement
        GROUP BY
            cube(
            "doc_type_display",
            "enc_class_code",
            "gender",
            "age_at_visit"
            )
    )

    SELECT
        p.cnt_subject_ref AS cnt,
        p."doc_type_display",
        p."enc_class_code",
        p."gender",
        p."age_at_visit"
    FROM powerset AS p
    WHERE 
        cnt_subject_ref >= 10
);