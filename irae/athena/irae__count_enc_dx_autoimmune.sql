CREATE TABLE irae__count_enc_dx_autoimmune AS (
    WITH
    filtered_table AS (
        SELECT
            s.subject_ref,
            s.encounter_ref,
            --noqa: disable=RF03, AL02
            s."subtype",
            s."dx_display",
            s."dx_category_code"
            --noqa: enable=RF03, AL02
        FROM irae__cohort_dx_autoimmune AS s
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
                cast(dx_display AS varchar),
                'cumulus__none'
            ) AS dx_display,
            coalesce(
                cast(dx_category_code AS varchar),
                'cumulus__none'
            ) AS dx_category_code
        FROM filtered_table
    ),
    secondary_powerset AS (
        SELECT
            count(DISTINCT encounter_ref) AS cnt_encounter_ref,
            "subtype",
            "dx_display",
            "dx_category_code",
            concat_ws(
                '-',
                COALESCE("subtype",''),
                COALESCE("dx_display",''),
                COALESCE("dx_category_code",'')
            ) AS id
        FROM null_replacement
        GROUP BY
            cube(
            "subtype",
            "dx_display",
            "dx_category_code"
            )
    ),

    powerset AS (
        SELECT
            count(DISTINCT subject_ref) AS cnt_subject_ref,
            "subtype",
            "dx_display",
            "dx_category_code",
            concat_ws(
                '-',
                COALESCE("subtype",''),
                COALESCE("dx_display",''),
                COALESCE("dx_category_code",'')
            ) AS id
        FROM null_replacement
        GROUP BY
            cube(
            "subtype",
            "dx_display",
            "dx_category_code"
            )
    )

    SELECT
        s.cnt_encounter_ref AS cnt,
        p."subtype",
        p."dx_display",
        p."dx_category_code"
    FROM powerset AS p
    JOIN secondary_powerset AS s on s.id = p.id
    WHERE 
        cnt_subject_ref >= 10
);