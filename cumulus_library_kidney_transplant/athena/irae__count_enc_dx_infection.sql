CREATE TABLE irae__count_enc_dx_infection AS (
    WITH
    filtered_table AS (
        SELECT
            s.subject_ref,
            s.encounter_ref,
            --noqa: disable=RF03, AL02
            s."race_display",
            s."dx_display",
            s."gender",
            s."valueset",
            s."age_at_visit",
            s."enc_class_code",
            s."dx_category_code"
            --noqa: enable=RF03, AL02
        FROM irae__cohort_dx_infection AS s
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
                cast(dx_display AS varchar),
                'cumulus__none'
            ) AS dx_display,
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
                cast(enc_class_code AS varchar),
                'cumulus__none'
            ) AS enc_class_code,
            coalesce(
                cast(dx_category_code AS varchar),
                'cumulus__none'
            ) AS dx_category_code
        FROM filtered_table
    ),
    secondary_powerset AS (
        SELECT
            count(DISTINCT encounter_ref) AS cnt_encounter_ref,
            "race_display",
            "dx_display",
            "gender",
            "valueset",
            "age_at_visit",
            "enc_class_code",
            "dx_category_code",
            concat_ws(
                '-',
                COALESCE("race_display",''),
                COALESCE("dx_display",''),
                COALESCE("gender",''),
                COALESCE("valueset",''),
                COALESCE("age_at_visit",''),
                COALESCE("enc_class_code",''),
                COALESCE("dx_category_code",'')
            ) AS id
        FROM null_replacement
        GROUP BY
            cube(
            "race_display",
            "dx_display",
            "gender",
            "valueset",
            "age_at_visit",
            "enc_class_code",
            "dx_category_code"
            )
    ),

    powerset AS (
        SELECT
            count(DISTINCT subject_ref) AS cnt_subject_ref,
            "race_display",
            "dx_display",
            "gender",
            "valueset",
            "age_at_visit",
            "enc_class_code",
            "dx_category_code",
            concat_ws(
                '-',
                COALESCE("race_display",''),
                COALESCE("dx_display",''),
                COALESCE("gender",''),
                COALESCE("valueset",''),
                COALESCE("age_at_visit",''),
                COALESCE("enc_class_code",''),
                COALESCE("dx_category_code",'')
            ) AS id
        FROM null_replacement
        GROUP BY
            cube(
            "race_display",
            "dx_display",
            "gender",
            "valueset",
            "age_at_visit",
            "enc_class_code",
            "dx_category_code"
            )
    )

    SELECT
        s.cnt_encounter_ref AS cnt,
        p."race_display",
        p."dx_display",
        p."gender",
        p."valueset",
        p."age_at_visit",
        p."enc_class_code",
        p."dx_category_code"
    FROM powerset AS p
    JOIN secondary_powerset AS s on s.id = p.id
    WHERE 
        cnt_subject_ref >= 10
);