CREATE TABLE irae__count_enc_lab_lft AS (
    WITH
    filtered_table AS (
        SELECT
            s.subject_ref,
            s.encounter_ref,
            --noqa: disable=RF03, AL02
            s."age_at_visit",
            s."enc_class_code",
            s."gender",
            s."lab_interpretation_display",
            s."lab_observation_code",
            s."race_display",
            s."valueset"
            --noqa: enable=RF03, AL02
        FROM irae__cohort_lab_lft AS s
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
                cast(lab_interpretation_display AS varchar),
                'cumulus__none'
            ) AS lab_interpretation_display,
            coalesce(
                cast(lab_observation_code AS varchar),
                'cumulus__none'
            ) AS lab_observation_code,
            coalesce(
                cast(race_display AS varchar),
                'cumulus__none'
            ) AS race_display,
            coalesce(
                cast(valueset AS varchar),
                'cumulus__none'
            ) AS valueset
        FROM filtered_table
    ),
    secondary_powerset AS (
        SELECT
            count(DISTINCT encounter_ref) AS cnt_encounter_ref,
            "age_at_visit",
            "enc_class_code",
            "gender",
            "lab_interpretation_display",
            "lab_observation_code",
            "race_display",
            "valueset",
            concat_ws(
                '-',
                COALESCE("age_at_visit",''),
                COALESCE("enc_class_code",''),
                COALESCE("gender",''),
                COALESCE("lab_interpretation_display",''),
                COALESCE("lab_observation_code",''),
                COALESCE("race_display",''),
                COALESCE("valueset",'')
            ) AS id
        FROM null_replacement
        GROUP BY
            cube(
            "age_at_visit",
            "enc_class_code",
            "gender",
            "lab_interpretation_display",
            "lab_observation_code",
            "race_display",
            "valueset"
            )
    ),

    powerset AS (
        SELECT
            count(DISTINCT subject_ref) AS cnt_subject_ref,
            "age_at_visit",
            "enc_class_code",
            "gender",
            "lab_interpretation_display",
            "lab_observation_code",
            "race_display",
            "valueset",
            concat_ws(
                '-',
                COALESCE("age_at_visit",''),
                COALESCE("enc_class_code",''),
                COALESCE("gender",''),
                COALESCE("lab_interpretation_display",''),
                COALESCE("lab_observation_code",''),
                COALESCE("race_display",''),
                COALESCE("valueset",'')
            ) AS id
        FROM null_replacement
        GROUP BY
            cube(
            "age_at_visit",
            "enc_class_code",
            "gender",
            "lab_interpretation_display",
            "lab_observation_code",
            "race_display",
            "valueset"
            )
    )

    SELECT
        s.cnt_encounter_ref AS cnt,
        p."age_at_visit",
        p."enc_class_code",
        p."gender",
        p."lab_interpretation_display",
        p."lab_observation_code",
        p."race_display",
        p."valueset"
    FROM powerset AS p
    JOIN secondary_powerset AS s on s.id = p.id
    WHERE 
        cnt_subject_ref >= 10
);