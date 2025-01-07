CREATE TABLE irae__count_enc_study_population AS (
    WITH
    filtered_table AS (
        SELECT
            s.subject_ref,
            s.encounter_ref,
            --noqa: disable=RF03, AL02
            s."gender",
            s."race_display",
            s."ethnicity_display",
            s."gender",
            s."age_at_visit",
            s."enc_class_code",
            s."enc_period_start_month"
            --noqa: enable=RF03, AL02
        FROM irae__cohort_study_population AS s
        WHERE s.status = 'finished'
    ),
    
    null_replacement AS (
        SELECT
            subject_ref,
            encounter_ref,
            coalesce(
                cast(gender AS varchar),
                'cumulus__none'
            ) AS gender,
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
                cast(enc_period_start_month AS varchar),
                'cumulus__none'
            ) AS enc_period_start_month
        FROM filtered_table
    ),
    secondary_powerset AS (
        SELECT
            count(DISTINCT encounter_ref) AS cnt_encounter_ref,
            "gender",
            "race_display",
            "ethnicity_display",
            "gender",
            "age_at_visit",
            "enc_class_code",
            "enc_period_start_month",
            concat_ws(
                '-',
                COALESCE("gender",''),
                COALESCE("race_display",''),
                COALESCE("ethnicity_display",''),
                COALESCE("gender",''),
                COALESCE("age_at_visit",''),
                COALESCE("enc_class_code",''),
                COALESCE("enc_period_start_month",'')
            ) AS id
        FROM null_replacement
        GROUP BY
            cube(
            "gender",
            "race_display",
            "ethnicity_display",
            "gender",
            "age_at_visit",
            "enc_class_code",
            "enc_period_start_month"
            )
    ),

    powerset AS (
        SELECT
            count(DISTINCT subject_ref) AS cnt_subject_ref,
            "gender",
            "race_display",
            "ethnicity_display",
            "gender",
            "age_at_visit",
            "enc_class_code",
            "enc_period_start_month",
            concat_ws(
                '-',
                COALESCE("gender",''),
                COALESCE("race_display",''),
                COALESCE("ethnicity_display",''),
                COALESCE("gender",''),
                COALESCE("age_at_visit",''),
                COALESCE("enc_class_code",''),
                COALESCE("enc_period_start_month",'')
            ) AS id
        FROM null_replacement
        GROUP BY
            cube(
            "gender",
            "race_display",
            "ethnicity_display",
            "gender",
            "age_at_visit",
            "enc_class_code",
            "enc_period_start_month"
            )
    )

    SELECT
        s.cnt_encounter_ref AS cnt,
        p."gender",
        p."race_display",
        p."ethnicity_display",
        p."gender",
        p."age_at_visit",
        p."enc_class_code",
        p."enc_period_start_month"
    FROM powerset AS p
    JOIN secondary_powerset AS s on s.id = p.id
    WHERE 
        cnt_subject_ref >= 10
);