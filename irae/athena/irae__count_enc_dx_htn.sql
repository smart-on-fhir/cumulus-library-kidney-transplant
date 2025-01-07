CREATE TABLE irae__count_enc_dx_htn AS (
    WITH
    filtered_table AS (
        SELECT
            s.subject_ref,
            s.encounter_ref,
            --noqa: disable=RF03, AL02
            s."subtype",
            s."dx_category_code",
            s."gender",
            s."age_at_visit",
            s."enc_class_code"
            --noqa: enable=RF03, AL02
        FROM irae__cohort_dx_htn AS s
        WHERE s.status = 'finished'
    ),
    
    null_replacement AS (
        SELECT
            subject_ref,
            encounter_ref,
            coalesce(
                cast(subtype AS varchar),
                'cumulus__none'
            ) AS subtype,
            coalesce(
                cast(dx_category_code AS varchar),
                'cumulus__none'
            ) AS dx_category_code,
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
            ) AS enc_class_code
        FROM filtered_table
    ),
    secondary_powerset AS (
        SELECT
            count(DISTINCT encounter_ref) AS cnt_encounter_ref,
            "subtype",
            "dx_category_code",
            "gender",
            "age_at_visit",
            "enc_class_code",
            concat_ws(
                '-',
                COALESCE("subtype",''),
                COALESCE("dx_category_code",''),
                COALESCE("gender",''),
                COALESCE("age_at_visit",''),
                COALESCE("enc_class_code",'')
            ) AS id
        FROM null_replacement
        GROUP BY
            cube(
            "subtype",
            "dx_category_code",
            "gender",
            "age_at_visit",
            "enc_class_code"
            )
    ),

    powerset AS (
        SELECT
            count(DISTINCT subject_ref) AS cnt_subject_ref,
            "subtype",
            "dx_category_code",
            "gender",
            "age_at_visit",
            "enc_class_code",
            concat_ws(
                '-',
                COALESCE("subtype",''),
                COALESCE("dx_category_code",''),
                COALESCE("gender",''),
                COALESCE("age_at_visit",''),
                COALESCE("enc_class_code",'')
            ) AS id
        FROM null_replacement
        GROUP BY
            cube(
            "subtype",
            "dx_category_code",
            "gender",
            "age_at_visit",
            "enc_class_code"
            )
    )

    SELECT
        s.cnt_encounter_ref AS cnt,
        p."subtype",
        p."dx_category_code",
        p."gender",
        p."age_at_visit",
        p."enc_class_code"
    FROM powerset AS p
    JOIN secondary_powerset AS s on s.id = p.id
    WHERE 
        cnt_subject_ref >= 10
);