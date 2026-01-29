CREATE TABLE irae__count_patient_casedef AS (
    WITH
    filtered_table AS (
        SELECT
            s.subject_ref,
            --noqa: disable=RF03, AL02
            s."age_at_dx_min",
            s."age_at_visit",
            s."dx_code",
            s."dx_display",
            s."gender",
            s."ordinal_since"
            --noqa: enable=RF03, AL02
        FROM irae__cohort_casedef AS s
    ),
    
    null_replacement AS (
        SELECT
            subject_ref,
            coalesce(
                cast(age_at_dx_min AS varchar),
                'cumulus__none'
            ) AS age_at_dx_min,
            coalesce(
                cast(age_at_visit AS varchar),
                'cumulus__none'
            ) AS age_at_visit,
            coalesce(
                cast(dx_code AS varchar),
                'cumulus__none'
            ) AS dx_code,
            coalesce(
                cast(dx_display AS varchar),
                'cumulus__none'
            ) AS dx_display,
            coalesce(
                cast(gender AS varchar),
                'cumulus__none'
            ) AS gender,
            coalesce(
                cast(ordinal_since AS varchar),
                'cumulus__none'
            ) AS ordinal_since
        FROM filtered_table
    ),

    powerset AS (
        SELECT
            count(DISTINCT subject_ref) AS cnt_subject_ref,
            "age_at_dx_min",
            "age_at_visit",
            "dx_code",
            "dx_display",
            "gender",
            "ordinal_since",
            concat_ws(
                '-',
                COALESCE("age_at_dx_min",''),
                COALESCE("age_at_visit",''),
                COALESCE("dx_code",''),
                COALESCE("dx_display",''),
                COALESCE("gender",''),
                COALESCE("ordinal_since",'')
            ) AS id
        FROM null_replacement
        GROUP BY
            cube(
            "age_at_dx_min",
            "age_at_visit",
            "dx_code",
            "dx_display",
            "gender",
            "ordinal_since"
            )
    )

    SELECT
        p.cnt_subject_ref AS cnt,
        p."age_at_dx_min",
        p."age_at_visit",
        p."dx_code",
        p."dx_display",
        p."gender",
        p."ordinal_since"
    FROM powerset AS p
    WHERE 
        p.cnt_subject_ref >= 10
);