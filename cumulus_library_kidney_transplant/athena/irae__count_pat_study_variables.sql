CREATE TABLE irae__count_pat_study_variables AS (
    WITH
    filtered_table AS (
        SELECT
            s.subject_ref,
            --noqa: disable=RF03, AL02
            s."race_display",
            s."gender",
            s."valueset",
            s."variable",
            s."age_at_visit",
            s."enc_class_code"
            --noqa: enable=RF03, AL02
        FROM irae__cohort_study_variables AS s
    ),
    
    null_replacement AS (
        SELECT
            subject_ref,
            coalesce(
                cast(race_display AS varchar),
                'cumulus__none'
            ) AS race_display,
            coalesce(
                cast(gender AS varchar),
                'cumulus__none'
            ) AS gender,
            coalesce(
                cast(valueset AS varchar),
                'cumulus__none'
            ) AS valueset,
            coalesce(
                cast(variable AS varchar),
                'cumulus__none'
            ) AS variable,
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
            "race_display",
            "gender",
            "valueset",
            "variable",
            "age_at_visit",
            "enc_class_code",
            concat_ws(
                '-',
                COALESCE("race_display",''),
                COALESCE("gender",''),
                COALESCE("valueset",''),
                COALESCE("variable",''),
                COALESCE("age_at_visit",''),
                COALESCE("enc_class_code",'')
            ) AS id
        FROM null_replacement
        GROUP BY
            cube(
            "race_display",
            "gender",
            "valueset",
            "variable",
            "age_at_visit",
            "enc_class_code"
            )
    )

    SELECT
        p.cnt_subject_ref AS cnt,
        p."race_display",
        p."gender",
        p."valueset",
        p."variable",
        p."age_at_visit",
        p."enc_class_code"
    FROM powerset AS p
    WHERE 
        cnt_subject_ref >= 10
);