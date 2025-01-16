CREATE TABLE irae__count_enc_lab_custom AS (
    WITH
    filtered_table AS (
        SELECT
            s.subject_ref,
            s.encounter_ref,
            --noqa: disable=RF03, AL02
            s."age_at_visit",
            s."enc_class_code",
            s."gender",
            s."race_display",
            s."valueset",
            s."lab_observation_code"
            --noqa: enable=RF03, AL02
        FROM irae__cohort_lab_custom AS s
        WHERE s.status = 'finished'
    ),
    
    null_replacement AS (
        SELECT
            subject_ref,
            encounter_ref,
            coalesce(
                cast(age_at_visit AS varchar),
                'cumulus__none'
            ) AS age_at_visit,
            coalesce(
                cast(enc_class_code AS varchar),
                'cumulus__none'
            ) AS enc_class_code,
            coalesce(
                cast(gender AS varchar),
                'cumulus__none'
            ) AS gender,
            coalesce(
                cast(race_display AS varchar),
                'cumulus__none'
            ) AS race_display,
            coalesce(
                cast(valueset AS varchar),
                'cumulus__none'
            ) AS valueset,
            coalesce(
                cast(lab_observation_code AS varchar),
                'cumulus__none'
            ) AS lab_observation_code
        FROM filtered_table
    ),
    secondary_powerset AS (
        SELECT
            count(DISTINCT encounter_ref) AS cnt_encounter_ref,
            "age_at_visit",
            "enc_class_code",
            "gender",
            "race_display",
            "valueset",
            "lab_observation_code",
            concat_ws(
                '-',
                COALESCE("age_at_visit",''),
                COALESCE("enc_class_code",''),
                COALESCE("gender",''),
                COALESCE("race_display",''),
                COALESCE("valueset",''),
                COALESCE("lab_observation_code",'')
            ) AS id
        FROM null_replacement
        GROUP BY
            cube(
            "age_at_visit",
            "enc_class_code",
            "gender",
            "race_display",
            "valueset",
            "lab_observation_code"
            )
    ),

    powerset AS (
        SELECT
            count(DISTINCT subject_ref) AS cnt_subject_ref,
            "age_at_visit",
            "enc_class_code",
            "gender",
            "race_display",
            "valueset",
            "lab_observation_code",
            concat_ws(
                '-',
                COALESCE("age_at_visit",''),
                COALESCE("enc_class_code",''),
                COALESCE("gender",''),
                COALESCE("race_display",''),
                COALESCE("valueset",''),
                COALESCE("lab_observation_code",'')
            ) AS id
        FROM null_replacement
        GROUP BY
            cube(
            "age_at_visit",
            "enc_class_code",
            "gender",
            "race_display",
            "valueset",
            "lab_observation_code"
            )
    )

    SELECT
        s.cnt_encounter_ref AS cnt,
        p."age_at_visit",
        p."enc_class_code",
        p."gender",
        p."race_display",
        p."valueset",
        p."lab_observation_code"
    FROM powerset AS p
    JOIN secondary_powerset AS s on s.id = p.id
    WHERE 
        cnt_subject_ref >= 10
);