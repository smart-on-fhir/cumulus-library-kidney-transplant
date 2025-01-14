CREATE TABLE irae__count_enc_study_population_dx AS (
    WITH
    filtered_table AS (
        SELECT
            s.subject_ref,
            s.encounter_ref,
            --noqa: disable=RF03, AL02
            s."dx_category_code",
            s."dx_display"
            --noqa: enable=RF03, AL02
        FROM irae__cohort_study_population_dx AS s
        WHERE s.status = 'finished'
    ),
    
    null_replacement AS (
        SELECT
            subject_ref,
            encounter_ref,
            coalesce(
                cast(dx_category_code AS varchar),
                'cumulus__none'
            ) AS dx_category_code,
            coalesce(
                cast(dx_display AS varchar),
                'cumulus__none'
            ) AS dx_display
        FROM filtered_table
    ),
    secondary_powerset AS (
        SELECT
            count(DISTINCT encounter_ref) AS cnt_encounter_ref,
            "dx_category_code",
            "dx_display",
            concat_ws(
                '-',
                COALESCE("dx_category_code",''),
                COALESCE("dx_display",'')
            ) AS id
        FROM null_replacement
        GROUP BY
            cube(
            "dx_category_code",
            "dx_display"
            )
    ),

    powerset AS (
        SELECT
            count(DISTINCT subject_ref) AS cnt_subject_ref,
            "dx_category_code",
            "dx_display",
            concat_ws(
                '-',
                COALESCE("dx_category_code",''),
                COALESCE("dx_display",'')
            ) AS id
        FROM null_replacement
        GROUP BY
            cube(
            "dx_category_code",
            "dx_display"
            )
    )

    SELECT
        s.cnt_encounter_ref AS cnt,
        p."dx_category_code",
        p."dx_display"
    FROM powerset AS p
    JOIN secondary_powerset AS s on s.id = p.id
    WHERE 
        cnt_subject_ref >= 10
);