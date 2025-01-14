CREATE TABLE irae__count_enc_rx_htn AS (
    WITH
    filtered_table AS (
        SELECT
            s.subject_ref,
            s.encounter_ref,
            --noqa: disable=RF03, AL02
            s."subtype",
            s."rx_display",
            s."rx_category_code"
            --noqa: enable=RF03, AL02
        FROM irae__cohort_rx_htn AS s
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
                cast(rx_display AS varchar),
                'cumulus__none'
            ) AS rx_display,
            coalesce(
                cast(rx_category_code AS varchar),
                'cumulus__none'
            ) AS rx_category_code
        FROM filtered_table
    ),
    secondary_powerset AS (
        SELECT
            count(DISTINCT encounter_ref) AS cnt_encounter_ref,
            "subtype",
            "rx_display",
            "rx_category_code",
            concat_ws(
                '-',
                COALESCE("subtype",''),
                COALESCE("rx_display",''),
                COALESCE("rx_category_code",'')
            ) AS id
        FROM null_replacement
        GROUP BY
            cube(
            "subtype",
            "rx_display",
            "rx_category_code"
            )
    ),

    powerset AS (
        SELECT
            count(DISTINCT subject_ref) AS cnt_subject_ref,
            "subtype",
            "rx_display",
            "rx_category_code",
            concat_ws(
                '-',
                COALESCE("subtype",''),
                COALESCE("rx_display",''),
                COALESCE("rx_category_code",'')
            ) AS id
        FROM null_replacement
        GROUP BY
            cube(
            "subtype",
            "rx_display",
            "rx_category_code"
            )
    )

    SELECT
        s.cnt_encounter_ref AS cnt,
        p."subtype",
        p."rx_display",
        p."rx_category_code"
    FROM powerset AS p
    JOIN secondary_powerset AS s on s.id = p.id
    WHERE 
        cnt_subject_ref >= 10
);