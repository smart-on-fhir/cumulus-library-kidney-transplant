CREATE TABLE irae__count_enc_study_population_rx AS (
    WITH
    filtered_table AS (
        SELECT
            s.subject_ref,
            s.encounter_ref,
            --noqa: disable=RF03, AL02
            s."rx_category_code",
            s."rx_display"
            --noqa: enable=RF03, AL02
        FROM irae__cohort_study_population_rx AS s
        WHERE s.status = 'finished'
    ),
    
    null_replacement AS (
        SELECT
            subject_ref,
            encounter_ref,
            coalesce(
                cast(rx_category_code AS varchar),
                'cumulus__none'
            ) AS rx_category_code,
            coalesce(
                cast(rx_display AS varchar),
                'cumulus__none'
            ) AS rx_display
        FROM filtered_table
    ),
    secondary_powerset AS (
        SELECT
            count(DISTINCT encounter_ref) AS cnt_encounter_ref,
            "rx_category_code",
            "rx_display",
            concat_ws(
                '-',
                COALESCE("rx_category_code",''),
                COALESCE("rx_display",'')
            ) AS id
        FROM null_replacement
        GROUP BY
            cube(
            "rx_category_code",
            "rx_display"
            )
    ),

    powerset AS (
        SELECT
            count(DISTINCT subject_ref) AS cnt_subject_ref,
            "rx_category_code",
            "rx_display",
            concat_ws(
                '-',
                COALESCE("rx_category_code",''),
                COALESCE("rx_display",'')
            ) AS id
        FROM null_replacement
        GROUP BY
            cube(
            "rx_category_code",
            "rx_display"
            )
    )

    SELECT
        s.cnt_encounter_ref AS cnt,
        p."rx_category_code",
        p."rx_display"
    FROM powerset AS p
    JOIN secondary_powerset AS s on s.id = p.id
    WHERE 
        cnt_subject_ref >= 10
);