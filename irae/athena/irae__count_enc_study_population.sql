CREATE TABLE irae__count_enc_study_population AS (
    WITH
    filtered_table AS (
        SELECT
            s.subject_ref,
            s.encounter_ref,
            --noqa: disable=RF03, AL02
            s."enc_class_code",
            s."race_display",
            s."age_at_visit",
            s."gender"
            --noqa: enable=RF03, AL02
        FROM irae__cohort_study_population AS s
        WHERE s.status = 'finished'
    ),
    
    null_replacement AS (
        SELECT
            subject_ref,
            encounter_ref,
            coalesce(
                cast(enc_class_code AS varchar),
                'cumulus__none'
            ) AS enc_class_code,
            coalesce(
                cast(race_display AS varchar),
                'cumulus__none'
            ) AS race_display,
            coalesce(
                cast(age_at_visit AS varchar),
                'cumulus__none'
            ) AS age_at_visit,
            coalesce(
                cast(gender AS varchar),
                'cumulus__none'
            ) AS gender
        FROM filtered_table
    ),
    secondary_powerset AS (
        SELECT
            count(DISTINCT encounter_ref) AS cnt_encounter_ref,
            "enc_class_code",
            "race_display",
            "age_at_visit",
            "gender",
            concat_ws(
                '-',
                COALESCE("enc_class_code",''),
                COALESCE("race_display",''),
                COALESCE("age_at_visit",''),
                COALESCE("gender",'')
            ) AS id
        FROM null_replacement
        GROUP BY
            cube(
            "enc_class_code",
            "race_display",
            "age_at_visit",
            "gender"
            )
    ),

    powerset AS (
        SELECT
            count(DISTINCT subject_ref) AS cnt_subject_ref,
            "enc_class_code",
            "race_display",
            "age_at_visit",
            "gender",
            concat_ws(
                '-',
                COALESCE("enc_class_code",''),
                COALESCE("race_display",''),
                COALESCE("age_at_visit",''),
                COALESCE("gender",'')
            ) AS id
        FROM null_replacement
        GROUP BY
            cube(
            "enc_class_code",
            "race_display",
            "age_at_visit",
            "gender"
            )
    )

    SELECT
        s.cnt_encounter_ref AS cnt,
        p."enc_class_code",
        p."race_display",
        p."age_at_visit",
        p."gender"
    FROM powerset AS p
    JOIN secondary_powerset AS s on s.id = p.id
    WHERE 
        cnt_subject_ref >= 10
);