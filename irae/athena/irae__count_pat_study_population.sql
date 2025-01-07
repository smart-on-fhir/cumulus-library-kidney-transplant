CREATE TABLE irae__count_pat_study_population AS (
    WITH
    filtered_table AS (
        SELECT
            s.subject_ref,
            --noqa: disable=RF03, AL02
            s."gender",
            s."race_display",
            s."ethnicity_display"
            --noqa: enable=RF03, AL02
        FROM irae__cohort_study_population AS s
    ),
    
    null_replacement AS (
        SELECT
            subject_ref,
            coalesce(
                cast(gender AS varchar),
                'cumulus__none'
            ) AS gender,
            coalesce(
                cast(race_display AS varchar),
                'cumulus__none'
            ) AS race_display,
            coalesce(
                cast(ethnicity_display AS varchar),
                'cumulus__none'
            ) AS ethnicity_display
        FROM filtered_table
    ),

    powerset AS (
        SELECT
            count(DISTINCT subject_ref) AS cnt_subject_ref,
            "gender",
            "race_display",
            "ethnicity_display",
            concat_ws(
                '-',
                COALESCE("gender",''),
                COALESCE("race_display",''),
                COALESCE("ethnicity_display",'')
            ) AS id
        FROM null_replacement
        GROUP BY
            cube(
            "gender",
            "race_display",
            "ethnicity_display"
            )
    )

    SELECT
        p.cnt_subject_ref AS cnt,
        p."gender",
        p."race_display",
        p."ethnicity_display"
    FROM powerset AS p
    WHERE 
        cnt_subject_ref >= 10
);