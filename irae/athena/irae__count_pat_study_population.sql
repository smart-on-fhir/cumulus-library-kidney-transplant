CREATE TABLE irae__count_pat_study_population AS (
    WITH
    filtered_table AS (
        SELECT
            s.subject_ref,
            --noqa: disable=RF03, AL02
            s."ethnicity_display",
            s."gender",
            s."race_display"
            --noqa: enable=RF03, AL02
        FROM irae__cohort_study_population AS s
    ),
    
    null_replacement AS (
        SELECT
            subject_ref,
            coalesce(
                cast(ethnicity_display AS varchar),
                'cumulus__none'
            ) AS ethnicity_display,
            coalesce(
                cast(gender AS varchar),
                'cumulus__none'
            ) AS gender,
            coalesce(
                cast(race_display AS varchar),
                'cumulus__none'
            ) AS race_display
        FROM filtered_table
    ),

    powerset AS (
        SELECT
            count(DISTINCT subject_ref) AS cnt_subject_ref,
            "ethnicity_display",
            "gender",
            "race_display",
            concat_ws(
                '-',
                COALESCE("ethnicity_display",''),
                COALESCE("gender",''),
                COALESCE("race_display",'')
            ) AS id
        FROM null_replacement
        GROUP BY
            cube(
            "ethnicity_display",
            "gender",
            "race_display"
            )
    )

    SELECT
        p.cnt_subject_ref AS cnt,
        p."ethnicity_display",
        p."gender",
        p."race_display"
    FROM powerset AS p
    WHERE 
        cnt_subject_ref >= 10
);