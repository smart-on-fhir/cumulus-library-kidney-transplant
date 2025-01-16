CREATE TABLE irae__count_enc_lab_cbc AS (
    WITH
    filtered_table AS (
        SELECT
            s.subject_ref,
            s.encounter_ref,
            --noqa: disable=RF03, AL02
            s."race_display",
            s."gender",
            s."valueset",
            s."age_at_visit",
            s."lab_observation_code",
            s."enc_class_code"
            --noqa: enable=RF03, AL02
        FROM irae__cohort_lab_cbc AS s
        WHERE s.status = 'finished'
    ),
    
    null_replacement AS (
        SELECT
            subject_ref,
            encounter_ref,
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
                cast(age_at_visit AS varchar),
                'cumulus__none'
            ) AS age_at_visit,
            coalesce(
                cast(lab_observation_code AS varchar),
                'cumulus__none'
            ) AS lab_observation_code,
            coalesce(
                cast(enc_class_code AS varchar),
                'cumulus__none'
            ) AS enc_class_code
        FROM filtered_table
    ),
    secondary_powerset AS (
        SELECT
            count(DISTINCT encounter_ref) AS cnt_encounter_ref,
            "race_display",
            "gender",
            "valueset",
            "age_at_visit",
            "lab_observation_code",
            "enc_class_code",
            concat_ws(
                '-',
                COALESCE("race_display",''),
                COALESCE("gender",''),
                COALESCE("valueset",''),
                COALESCE("age_at_visit",''),
                COALESCE("lab_observation_code",''),
                COALESCE("enc_class_code",'')
            ) AS id
        FROM null_replacement
        GROUP BY
            cube(
            "race_display",
            "gender",
            "valueset",
            "age_at_visit",
            "lab_observation_code",
            "enc_class_code"
            )
    ),

    powerset AS (
        SELECT
            count(DISTINCT subject_ref) AS cnt_subject_ref,
            "race_display",
            "gender",
            "valueset",
            "age_at_visit",
            "lab_observation_code",
            "enc_class_code",
            concat_ws(
                '-',
                COALESCE("race_display",''),
                COALESCE("gender",''),
                COALESCE("valueset",''),
                COALESCE("age_at_visit",''),
                COALESCE("lab_observation_code",''),
                COALESCE("enc_class_code",'')
            ) AS id
        FROM null_replacement
        GROUP BY
            cube(
            "race_display",
            "gender",
            "valueset",
            "age_at_visit",
            "lab_observation_code",
            "enc_class_code"
            )
    )

    SELECT
        s.cnt_encounter_ref AS cnt,
        p."race_display",
        p."gender",
        p."valueset",
        p."age_at_visit",
        p."lab_observation_code",
        p."enc_class_code"
    FROM powerset AS p
    JOIN secondary_powerset AS s on s.id = p.id
    WHERE 
        cnt_subject_ref >= 10
);