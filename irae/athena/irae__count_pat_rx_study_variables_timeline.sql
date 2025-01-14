CREATE TABLE irae__count_pat_rx_study_variables_timeline AS (
    WITH
    filtered_table AS (
        SELECT
            s.subject_ref,
            s.encounter_ref,
            --noqa: disable=RF03, AL02
            s."variable",
            s."rx_custom",
            s."rx_diabetes",
            s."rx_diuretics",
            s."rx_immunosuppressive"
            --noqa: enable=RF03, AL02
        FROM irae__cohort_study_variables_timeline AS s
        WHERE s.status = 'finished'
    ),
    
    null_replacement AS (
        SELECT
            subject_ref,
            encounter_ref,
            coalesce(
                cast(variable AS varchar),
                'cumulus__none'
            ) AS variable,
            coalesce(
                cast(rx_custom AS varchar),
                'cumulus__none'
            ) AS rx_custom,
            coalesce(
                cast(rx_diabetes AS varchar),
                'cumulus__none'
            ) AS rx_diabetes,
            coalesce(
                cast(rx_diuretics AS varchar),
                'cumulus__none'
            ) AS rx_diuretics,
            coalesce(
                cast(rx_immunosuppressive AS varchar),
                'cumulus__none'
            ) AS rx_immunosuppressive
        FROM filtered_table
    ),
    secondary_powerset AS (
        SELECT
            count(DISTINCT encounter_ref) AS cnt_encounter_ref,
            "variable",
            "rx_custom",
            "rx_diabetes",
            "rx_diuretics",
            "rx_immunosuppressive",
            concat_ws(
                '-',
                COALESCE("variable",''),
                COALESCE("rx_custom",''),
                COALESCE("rx_diabetes",''),
                COALESCE("rx_diuretics",''),
                COALESCE("rx_immunosuppressive",'')
            ) AS id
        FROM null_replacement
        GROUP BY
            cube(
            "variable",
            "rx_custom",
            "rx_diabetes",
            "rx_diuretics",
            "rx_immunosuppressive"
            )
    ),

    powerset AS (
        SELECT
            count(DISTINCT subject_ref) AS cnt_subject_ref,
            "variable",
            "rx_custom",
            "rx_diabetes",
            "rx_diuretics",
            "rx_immunosuppressive",
            concat_ws(
                '-',
                COALESCE("variable",''),
                COALESCE("rx_custom",''),
                COALESCE("rx_diabetes",''),
                COALESCE("rx_diuretics",''),
                COALESCE("rx_immunosuppressive",'')
            ) AS id
        FROM null_replacement
        GROUP BY
            cube(
            "variable",
            "rx_custom",
            "rx_diabetes",
            "rx_diuretics",
            "rx_immunosuppressive"
            )
    )

    SELECT
        s.cnt_encounter_ref AS cnt,
        p."variable",
        p."rx_custom",
        p."rx_diabetes",
        p."rx_diuretics",
        p."rx_immunosuppressive"
    FROM powerset AS p
    JOIN secondary_powerset AS s on s.id = p.id
    WHERE 
        cnt_subject_ref >= 10
);